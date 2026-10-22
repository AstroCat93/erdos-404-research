#!/usr/bin/env python3
"""vcl_propW.py -- independent check of M4C Proposition W (an explicit slope-0 path alive at 3p on A = p^3 Z_p).

For x in A = p^3 Z_p and any 0/1 path e of length 3p (e_0 = 1):
  S_e(x) = S_e(0) mod p^3 and S_e'(x) = S_e'(0) mod p^3 (integer polynomials), V_3p(x) = 3 (p >= 5),
  S_e(0) = sum e_j j!,  S_e'(0) = sum e_j j! H_j  (an integer).
So Z^0_{3p} >= 1 on all of A iff some e has sum e_j j! = 0 mod p^3 and sum e_j j! H_j != 0 mod p.
This script builds e by the report's recipe (first block given; second and third blocks found by an
exhaustive subset-sum DP), checks the two congruences exactly, checks the report's slope formula
S'_e = -w_p/(xi+1) = -w_p mod p for the first block {0,p-1}, and re-evaluates S_e, S'_e directly at random
x in A (exact integers modulo p^12) as a second check.  It also confirms that at the Wilson prime 13 the block
{0,p-1} gives slope >= 1 and that the report's block {0,1,2,3,4,8,9} gives lambda_e = 12, k_e = 0 mod 13.
usage: vcl_propW.py p1 p2 ...
"""
import random
import sys
from math import factorial


def subset_with_sum(vals, target, mod):
    """find a subset (list of indices) of vals with sum = target mod `mod`, by DP over residues."""
    reach = {0: []}
    for i, v in enumerate(vals):
        new = dict(reach)
        for r, idx in reach.items():
            r2 = (r + v) % mod
            if r2 not in new:
                new[r2] = idx + [i]
        reach = new
    return reach.get(target % mod)


def jHj(j):
    f = factorial(j)
    return sum(f // i for i in range(1, j + 1))


def build_path(p, first):
    e = [0] * (3 * p)
    for j in first:
        e[j] = 1
    assert e[0] == 1
    s0 = sum(factorial(j) for j in first)
    assert s0 % p == 0, "first block must have sum = 0 mod p"
    # second block: elements (p+u)! = p * (p-1)! * prod... ; work with exact integers mod p^2
    m2 = p * p
    vals2 = [factorial(p + u) % m2 for u in range(p)]  # all divisible by p
    vals2r = [v // p for v in vals2]
    need = (-(s0 % m2) // p) % p
    idx = subset_with_sum(vals2r, need, p)
    if idx is None:
        return None
    for u in idx:
        e[p + u] = 1
    s1 = sum(factorial(j) for j in range(2 * p) if e[j])
    assert s1 % m2 == 0
    m3 = p ** 3
    vals3r = [(factorial(2 * p + u) % m3) // m2 for u in range(p)]
    need3 = (-(s1 % m3) // m2) % p
    idx3 = subset_with_sum(vals3r, need3, p)
    if idx3 is None:
        return None
    for u in idx3:
        e[2 * p + u] = 1
    return e


def direct_eval(e, x, mod):
    """S_e(x) and S_e'(x) modulo mod, exact integer arithmetic (product rule)."""
    S = 0
    Sd = 0
    pi = 1      # pi_j(x)
    pid = 0     # pi_j'(x)
    for j in range(len(e)):
        if j > 0:
            pid = (pid * (x + j) + pi) % mod
            pi = pi * (x + j) % mod
        if e[j]:
            S = (S + pi) % mod
            Sd = (Sd + pid) % mod
    return S, Sd


def v(n, p):
    if n == 0:
        return 99
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def main():
    rng = random.Random(404)
    allok = True
    for p in [int(t) for t in sys.argv[1:]]:
        wp = (factorial(p - 1) + 1) // p
        wilson = (wp % p == 0)
        first = [0, 1, 2, 3, 4, 8, 9] if (wilson and p == 13) else [0, p - 1]
        if wilson and p != 13:
            print(f"p={p}: Wilson prime other than 13 -- no block given in the report")
            allok = False
            continue
        e = build_path(p, first)
        if e is None:
            print(f"p={p}: FAILED to build path")
            allok = False
            continue
        S0 = sum(factorial(j) for j in range(3 * p) if e[j])
        Sd0 = sum(jHj(j) for j in range(3 * p) if e[j])
        alive = (S0 % p ** 3 == 0)
        slope0 = (Sd0 % p != 0)
        msg = f"p={p} wilson={int(wilson)} first={first}: S_e(0)=0 mod p^3: {alive}; S_e'(0) mod p = {Sd0 % p} (slope 0: {slope0})"
        if not wilson:
            pred = (-wp) % p
            msg += f"; report's prediction -w_p mod p = {pred} -> {'agrees' if pred == Sd0 % p else 'DISAGREES'}"
            if pred != Sd0 % p:
                allok = False
        else:
            ke = (sum(factorial(j) for j in first) // p) % p
            lam = sum(jHj(j) for j in first) % p
            ke2 = (sum(factorial(j) for j in [0, p - 1]) // p) % p
            lam2 = sum(jHj(j) for j in [0, p - 1]) % p
            msg += f"; block {first}: k_e={ke}, lambda_e={lam}; block [0,p-1]: k_e={ke2}, lambda_e={lam2} (equal -> slope>=1)"
        # direct evaluation at random x in A
        mod = p ** 12
        ok_direct = 0
        for _ in range(20):
            x = p ** 3 * rng.randrange(p ** 9)
            S, Sd = direct_eval(e, x, mod)
            V3p = sum(v(x + i, p) for i in range(1, 3 * p + 1))
            if v(S, p) >= V3p == 3 and Sd % p != 0:
                ok_direct += 1
        msg += f"; direct eval at 20 random x in A: alive & slope 0 in {ok_direct}/20"
        print(msg, flush=True)
        if not (alive and slope0 and ok_direct == 20):
            allok = False
    print("ALL OK" if allok else "SOME FAILURE")


if __name__ == "__main__":
    main()
