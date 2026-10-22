#!/usr/bin/env python3
"""propW_check.py -- independent check of M4C Proposition W (slope-0 path alive at 3p on A = p^3 Z_p) and of the
admissibility of A for R3M Theorem C3 (j = 0, n_0 = 3p, n_1 = 4p).  Written by the obstruction verifier; no M4C code.

Reduction used: S_e is in Z[X], so for x in A (x = 0 mod p^3), S_e(x) = S_e(0) mod p^3 and S_e'(x) = S_e'(0) mod p.
Also V_{3p}(x) = 3 and M_{4p}(x) = 1 on A for p >= 5.  So "Z^0_{3p} >= 1 on all of A" is equivalent to the
existence of e (e_0 = 1, length 3p) with  sum e_j j! = 0 mod p^3  and  sum e_j (j! H_j) != 0 mod p,
where j! H_j = sum_{i<=j} j!/i is the integer pi_j'(0).  We test M4C's explicit construction (first block {0,p-1};
for the Wilson prime 13 the block {0,1,2,3,4,8,9}), completed by our own residue DP, and we also re-evaluate the
completed path at random x in A to precision p^12 (direct product evaluation).
usage: propW_check.py p1 p2 ...
"""
import random
import sys
from math import factorial


def subset_hitting(vals, target, p):
    """indices U with sum_{u in U} vals[u] = target mod p (one witness), or None."""
    reach = {0: []}
    for i, a in enumerate(vals):
        new = dict(reach)
        for r, w in reach.items():
            r2 = (r + a) % p
            if r2 not in new:
                new[r2] = w + [i]
        reach = new
    return reach.get(target % p)


def jfH(j):
    """pi_j'(0) = j! H_j as an integer."""
    f = factorial(j)
    return sum(f // i for i in range(1, j + 1))


def vp(n, p):
    if n == 0:
        return 10 ** 9
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def build(p, first):
    e = [0] * (3 * p)
    for j in first:
        e[j] = 1
    s1 = sum(factorial(j) for j in first)
    assert s1 % p == 0, "first block must sum to 0 mod p"
    # block 2: elements (p+u)! = p * (p-1)! * u! * (p+1)...(p+u)/u!  -> valuation 1; choose residues mod p of /p
    v2 = [(factorial(p + u) // p) % p for u in range(p)]
    need2 = (-(s1 // p)) % p
    U2 = subset_hitting(v2, need2, p)
    assert U2 is not None
    for u in U2:
        e[p + u] = 1
    s12 = s1 + sum(factorial(p + u) for u in U2)
    assert s12 % (p * p) == 0
    v3 = [(factorial(2 * p + u) // (p * p)) % p for u in range(p)]
    need3 = (-(s12 // (p * p))) % p
    U3 = subset_hitting(v3, need3, p)
    assert U3 is not None
    for u in U3:
        e[2 * p + u] = 1
    return e


def eval_at(e, x, mod):
    S = 0
    Sd = 0
    pi = 1          # pi_j(x)
    pid = 0         # pi_j'(x)
    for j in range(len(e)):
        if j > 0:
            pid = (pid * (x + j) + pi) % mod
            pi = pi * (x + j) % mod
        if e[j]:
            S = (S + pi) % mod
            Sd = (Sd + pid) % mod
    return S, Sd


def main():
    random.seed(404)
    for p in [int(a) for a in sys.argv[1:]]:
        wq = (factorial(p - 1) + 1) // p
        wilson = (wq % p == 0)
        out = []
        for name, first in (("{0,p-1}", [0, p - 1]), ("{0,1,2,3,4,8,9}", [0, 1, 2, 3, 4, 8, 9] if p == 13 else None)):
            if first is None:
                continue
            k_e = sum(factorial(j) for j in first) // p
            lam = sum(jfH(j) for j in first)
            e = build(p, first)
            S0 = sum(factorial(j) for j in range(3 * p) if e[j])
            Sd0 = sum(jfH(j) for j in range(3 * p) if e[j])
            V3p = vp(factorial(3 * p), p)
            alive = vp(S0, p) >= V3p
            slope0 = Sd0 % p != 0
            pred = (lam - k_e) % p != 0     # M4C: slope 0 iff lambda_e != k_e (mod p) at xi = 0
            # random x in A, precision p^12
            mod = p ** 12
            okr = 0
            for _ in range(20):
                x = p ** 3 * random.randrange(p ** 9)
                S, Sd = eval_at(e, x, mod)
                Vx = sum(vp(x + i, p) for i in range(1, 3 * p + 1))
                okr += int(vp(S, p) >= Vx and Vx == 3 and Sd % p != 0)
            out.append(f"{name}: V_3p={V3p} alive={alive} slope0={slope0} (S'(0) mod p={Sd0 % p}, "
                       f"-w_p mod p={(-wq) % p}, lambda-k mod p={(lam - k_e) % p}, predicted slope0={pred}); "
                       f"random x in A ok {okr}/20")
        # admissibility data on A: m_0 = V_3p, D_0 = v(x+4p), M_4p
        x = p ** 3 * random.randrange(1, p ** 6)
        m0 = sum(vp(x + i, p) for i in range(1, 3 * p + 1))
        D0 = vp(x + 4 * p, p)
        M4p = max(vp(x + i, p) for i in range(1, 4 * p + 1))
        adm = (D0 <= m0 - M4p) and (M4p < m0)
        print(f"p={p} wilson={wilson}: " + " | ".join(out) +
              f" | admissibility: m0={m0} D0={D0} M_4p={M4p} -> {adm}", flush=True)


if __name__ == "__main__":
    main()
