#!/usr/bin/env python3
"""Exact check of M4C Proposition W (slope-0 path alive at 3p on A = p^3 Z_p).

For random x = p^3 u (exact integers) we
  * check V_{3p}(x) = 3 and M_{3p}(x) = 1, v(x+4p) = 1 (admissibility data);
  * build the path of Prop W: first block {0,p-1} (or the special block at the
    Wilson prime 13), second block = a RANDOM solution of
        sum_u e_{p+u} u! = w_p/(xi+1)  (mod p)       [as stated in the report]
    (for a general first block: (k_e + xi*lambda_e)/(xi+1)),
    third block = a random subset that makes S_e(x) = 0 mod p^3 (found by DP);
  * evaluate S_e(x) and S'_e(x) exactly as integers and check
        v(S_e(x)) >= 3  and  v(S'_e(x)) = 0,
    and the stated value S'_e(x) = -w_p/(xi+1) mod p.
Also: the 'general first block' criterion (slope 0 iff lambda_e != k_e mod p)
is tested on random first blocks with p | sum e_j j!.
No code shared with code/round4/M4C/.
"""
import sys, random, math

def vp(n, p):
    if n == 0:
        return 10**9
    v = 0
    while n % p == 0:
        n //= p; v += 1
    return v

def pis_and_derivs(x, n):
    """pi_j(x) and pi_j'(x) for j=0..n-1 (exact integers)."""
    P = [1]; D = [0]
    for j in range(1, n):
        D.append(D[-1] * (x + j) + P[-1])
        P.append(P[-1] * (x + j))
    return P, D

def subset_with_sum(vals, target, m, rng):
    """random subset of indices of vals with sum = target mod m (DP, m small)."""
    idx = list(range(len(vals)))
    rng.shuffle(idx)
    reach = [dict() for _ in range(len(idx) + 1)]
    reach[0] = {0: None}
    for k, i in enumerate(idx):
        cur = reach[k]; nxt = {}
        for r in cur:
            if r not in nxt:
                nxt[r] = (r, False)
            r2 = (r + vals[i]) % m
            if r2 not in nxt or rng.random() < 0.5:
                nxt[r2] = (r, True)
        reach[k + 1] = nxt
    if target % m not in reach[len(idx)]:
        return None
    chosen = []
    r = target % m
    for k in range(len(idx), 0, -1):
        prev, take = reach[k][r]
        if take:
            chosen.append(idx[k - 1])
        r = prev
    return sorted(chosen)

def harm_fact(j):
    f = math.factorial(j)
    return sum(f // s for s in range(1, j + 1))

def build_and_check(p, x, first, rng):
    n = 3 * p
    xi = x // p
    P, D = pis_and_derivs(x, n + p + 1)
    V3p = sum(vp(x + i, p) for i in range(1, n + 1))
    M3p = max(vp(x + i, p) for i in range(1, n + 1))
    v4p = vp(x + 4 * p, p)
    M4p = max(vp(x + i, p) for i in range(1, 4 * p + 1))
    e = [0] * n
    for j in first:
        e[j] = 1
    s1 = sum(math.factorial(j) for j in first)
    assert s1 % p == 0
    k_e = (s1 // p) % p
    lam_e = sum(harm_fact(j) for j in first) % p
    inv = pow((xi + 1) % p, -1, p)
    target2 = ((k_e + xi * lam_e) * inv) % p
    U2 = subset_with_sum([math.factorial(u) % p for u in range(p)], target2, p, rng)
    assert U2 is not None
    for u in U2:
        e[p + u] = 1
    S2 = sum(e[j] * P[j] for j in range(2 * p))
    ok2 = (S2 % (p * p) == 0)
    # third block: digit at p^2
    vals = [(P[2 * p + u] // (p * p)) % p for u in range(p)]
    assert all(vp(P[2 * p + u], p) == 2 for u in range(p))
    tgt = (-(S2 // (p * p))) % p if ok2 else 0
    U3 = subset_with_sum(vals, tgt, p, rng)
    for u in U3:
        e[2 * p + u] = 1
    S = sum(e[j] * P[j] for j in range(n))
    Sd = sum(e[j] * D[j] for j in range(n))
    alive = vp(S, p) >= V3p
    slope = vp(Sd, p)
    w_p = (math.factorial(p - 1) + 1) // p
    pred_slope_val = (-(w_p * inv)) % p
    gen_pred = ((lam_e - k_e) * inv) % p
    return dict(V3p=V3p, M3p=M3p, v4p=v4p, M4p=M4p, ok2=ok2, alive=alive, slope=slope,
                Sd_mod_p=Sd % p, pred=pred_slope_val, gen_pred=gen_pred, lam_e=lam_e, k_e=k_e)

def main():
    ps = [int(a) for a in sys.argv[1:]] or [7, 11, 13, 17, 19, 23]
    rng = random.Random(20261014)
    for p in ps:
        w_p = (math.factorial(p - 1) + 1) // p
        wilson = (w_p % p == 0)
        nx = 40
        stats = dict(n=0, adm=0, ok2=0, alive=0, slope0=0, formula=0, genformula=0)
        std_first = [0, p - 1]
        special = [0, 1, 2, 3, 4, 8, 9] if p == 13 else None
        firsts = [("std", std_first)] + ([("special13", special)] if special else [])
        for name, first in firsts:
            st = dict(n=0, adm=0, ok2=0, alive=0, slope0=0, formula=0, genformula=0)
            for t in range(nx):
                # x = p^3 u, u random with occasional extra p-divisibility
                u = rng.randrange(1, p ** 25)
                if t % 4 == 1:
                    u *= p ** rng.randrange(1, 6)
                if t % 4 == 2:
                    u = -u
                x = p ** 3 * u
                r = build_and_check(p, x, first, rng)
                st['n'] += 1
                st['adm'] += (r['V3p'] == 3 and r['M3p'] == 1 and r['v4p'] == 1 and r['M4p'] == 1)
                st['ok2'] += r['ok2']
                st['alive'] += r['alive']
                st['slope0'] += (r['slope'] == 0)
                if name == "std":
                    st['formula'] += (r['Sd_mod_p'] == r['pred'])
                st['genformula'] += (r['Sd_mod_p'] == r['gen_pred'])
            print("p=%d wilson=%s first=%s(%s): trials %d; V3p=3,M3p=1,v(x+4p)=1,M4p=1: %d; S=0 mod p^2 after block 2: %d; alive at 3p: %d; slope 0: %d; S'=-w_p/(xi+1) mod p: %s; S'=(lam-k)/(xi+1): %d"
                  % (p, wilson, name, first, st['n'], st['adm'], st['ok2'], st['alive'], st['slope0'],
                     st['formula'] if name == "std" else "n/a", st['genformula']), flush=True)
        # general first block criterion
        cnt = dict(tot=0, agree=0, lam_ne_k=0)
        tries = 0
        while cnt['tot'] < 60 and tries < 200000:
            tries += 1
            first = [0] + [j for j in range(1, p) if rng.random() < 0.5]
            if sum(math.factorial(j) for j in first) % p != 0:
                continue
            u = rng.randrange(1, p ** 25)
            x = p ** 3 * u
            r = build_and_check(p, x, first, rng)
            assert r['alive'], "general block: not alive"
            pred0 = (r['lam_e'] != r['k_e'])
            cnt['tot'] += 1
            cnt['agree'] += (pred0 == (r['slope'] == 0))
            cnt['lam_ne_k'] += pred0
        print("p=%d general first blocks (random, p | sum e_j j!): %d tested, criterion 'slope 0 iff lambda_e != k_e' agrees in %d; lambda!=k in %d"
              % (p, cnt['tot'], cnt['agree'], cnt['lam_ne_k']), flush=True)
        if p == 13:
            first = [0, 1, 2, 3, 4, 8, 9]
            s = sum(math.factorial(j) for j in first)
            print("p=13 special block: sum j! = %d = 13*%d, k_e mod 13 = %d, lambda_e mod 13 = %d"
                  % (s, s // 13, (s // 13) % 13, sum(harm_fact(j) for j in first) % 13))

if __name__ == "__main__":
    main()
