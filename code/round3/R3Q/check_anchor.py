#!/usr/bin/env python3
"""Exact numerical test of the anchor lemmas (R3Q report, Lemmas 1-3).

For random 2-adic x (integers mod 2^P, P large) in a prescribed residue class, enumerate every path
e = (e_0=1, e_1, ..., e_{n-1}) alive at n (2^{V_n(x)} | S_e(x)) by BFS, tracking exactly the Taylor
coefficients S_e^{[i]}(x) = sum_j e_j pi_j^{[i]}(x), i = 0..3 (mod 2^P), where pi_j^{[i]} = pi_j^{(i)}/i!.
Checks, at every time n <= nmax and for every alive path:
  (L1) x = 0 mod 8 and V_n >= 4  =>  (e1,e2,e3) = (1,0,1) and v(S') = 1.
  (L2) x = 2 mod 16 and V_n >= 7 =>  v(S') = 3.          x = 10 mod 16 and V_n >= 7 => no alive path.
  (L2') x = 6 mod 16 and V_n >= T6 => v(S') = 3   (T6 = 11, see report).
  (L3) x = 2 mod 4, V_n >= 4, v(S') >= 3  =>  v(S^[2]) <= 1 or v(S^[3]) = 0.
  (L4) x = 2 mod 4, j = v(x+2), V_n > 3j  =>  v(S') <= 2j or v(S^[2]) <= j.
usage: check_anchor.py seed samples nmax residue modulus
"""
import random, sys

def v2(a):
    return (a & -a).bit_length() - 1 if a else 10**9

def check(x, nmax, P, res, modu, stats):
    MOD = 1 << P
    j2 = v2(x + 2)
    # pi^{[i]}_j for i=0..3 at current j
    pis = [1, 0, 0, 0]
    pop = [((0, 0, 0, 0), (1 if True else 0, None))]  # (S^[0..3], prefix bits e1..e3)
    pop = [((0, 0, 0, 0), ())]
    V = 0
    for j in range(nmax):
        new = []
        for (S, pre) in pop:
            for e in ((1,) if j == 0 else (0, 1)):
                S2 = tuple((S[i] + e * pis[i]) % MOD for i in range(4))
                npre = pre + (e,) if 1 <= j <= 3 else pre
                new.append((S2, npre))
        # advance pi_j -> pi_{j+1}: multiply by (X + j + 1) at X = x
        a = x + j + 1
        pis = [(pis[0] * a) % MOD, (pis[1] * a + pis[0]) % MOD, (pis[2] * a + pis[1]) % MOD,
               (pis[3] * a + pis[2]) % MOD]
        V += v2(a)
        n = j + 1
        pop = [(S, pre) for (S, pre) in new if v2(S[0]) >= V]
        if len(pop) > 200000:
            stats['capped'] += 1
            return
        for (S, pre) in pop:
            lam, k2, k3 = v2(S[1]), v2(S[2]), v2(S[3])
            stats['paths'] += 1
            if modu == 8 and res == 0 and V >= 4:
                stats['L1'] += 1
                if not (pre == (1, 0, 1) and lam == 1):
                    stats['fail'].append(('L1', x, n, pre, lam))
            if modu == 16 and res == 2 and V >= 7:
                stats['L2'] += 1
                if lam != 3:
                    stats['fail'].append(('L2', x, n, lam))
            if modu == 16 and res == 10 and V >= 7:
                stats['fail'].append(('L2dead', x, n))
            if modu == 16 and res == 6 and V >= 11:
                stats['L2p'] += 1
                if lam != 3:
                    stats['fail'].append(('L2p', x, n, lam))
            if x % 4 == 2 and V >= 4 and lam >= 3:
                stats['L3'] += 1
                if not (k2 <= 1 or k3 == 0):
                    stats['fail'].append(('L3', x, n, lam, k2, k3))
            if x % 4 == 2 and V > 3 * j2:
                stats['L4'] += 1
                if not (lam <= 2 * j2 or k2 <= j2):
                    stats['fail'].append(('L4', x, n, j2, lam, k2))
                stats['maxlam_minus_2j'] = max(stats['maxlam_minus_2j'], lam - 2 * j2)

if __name__ == "__main__":
    seed, S, nmax, res, modu = (int(a) for a in sys.argv[1:6])
    P = 4 * nmax + 96
    rnd = random.Random(seed)
    stats = {'paths': 0, 'L1': 0, 'L2': 0, 'L2p': 0, 'L3': 0, 'L4': 0, 'fail': [], 'capped': 0,
             'maxlam_minus_2j': -10**9}
    for s in range(S):
        x = (res + modu * rnd.getrandbits(P)) % (1 << P)
        check(x, nmax, P, res, modu, stats)
    print(f"class {res} mod {modu}: samples={S} nmax={nmax} paths_checked={stats['paths']} "
          f"L1={stats['L1']} L2={stats['L2']} L2'={stats['L2p']} L3={stats['L3']} L4={stats['L4']} "
          f"capped={stats['capped']} max(lambda-2j | L4 scope)={stats['maxlam_minus_2j']} "
          f"failures={len(stats['fail'])}")
    for f in stats['fail'][:10]:
        print("FAIL", f)
