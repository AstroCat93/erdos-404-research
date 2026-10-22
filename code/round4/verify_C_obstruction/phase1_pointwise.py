#!/usr/bin/env python3
"""phase1_pointwise.py -- exact (float64 DP over all residues) evaluation of the fine-scale mass
    eps = p^K Coll_K - p^D Coll_D
for the first phase-1 composite windows of M4C's schedule on A = p^3 Z_p, at random points x in A, compared with
M4C's pointwise threshold ebar = q1^{n1} q2^{n2} - 1 (Prop P1).  Purpose (obstruction lens): confirm that the
deterministic phase-1 bound holds, is nearly attained, and does not decay along the windows (as note
Prop 11.23 / Cor 10.20 and Prop 11.24 force for any deterministic, supremum-type L^2 bound).
Coll_k = P(sum_c delta_c pi_c(z) = 0 mod p^k), delta i.i.d. lazy signed, z = x + n_{k-1}, c < (b_{k+1}-b_{k-1}) p.
usage: phase1_pointwise.py p q1m1 q2m1 maxmod b0 b1 b2 ...   (windows with p^K <= maxmod are evaluated)
"""
import math
import random
import sys

import numpy as np


def vp(n, p):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def coll(elems, m):
    P = np.zeros(m)
    P[0] = 1.0
    for a in elems:
        a %= m
        P = 0.5 * P + 0.25 * np.roll(P, a) + 0.25 * np.roll(P, -a)
    return P


def main():
    p = int(sys.argv[1])
    q1, q2 = 1 + float(sys.argv[2]), 1 + float(sys.argv[3])
    maxmod = int(sys.argv[4])
    b = [int(t) for t in sys.argv[5:]]
    random.seed(7)
    for k in range(1, len(b) - 1):
        bm, bk, bp = b[k - 1], b[k], b[k + 1]
        n1 = sum(1 for j in range(bm + 1, bp + 1) if j % p)
        n2 = sum(1 for j in range(bm + 1, bp + 1) if j % p == 0)
        ebar = q1 ** n1 * q2 ** n2 - 1
        L = (bp - bm) * p
        res = []
        for trial in range(3):
            x = p ** 3 * random.randrange(p ** 12)
            z = x + bm * p
            D = sum(vp(z + i, p) for i in range(1, (bk - bm) * p + 1))
            K = sum(vp(z + i, p) for i in range(1, L + 1))
            m = p ** K
            if m > maxmod:
                res = None
                break
            elems = []
            pi = 1
            for c in range(L):
                if c > 0:
                    pi = pi * (z + c) % m
                elems.append(pi)
            PK = coll(elems, m)
            collK = PK[0]
            collD = PK[:: (p ** D)].sum()      # residues t mod p^K with t = 0 mod p^D
            eps = m * collK - p ** D * collD
            res.append((D, K, eps))
        if res is None:
            print(f"k={k} ({bm},{bp}]: p^K too large, stop")
            break
        print(f"k={k} composite ({bm},{bk},{bp}] D={res[0][0]} K={res[0][1]} n1={n1} n2={n2}: "
              f"eps at 3 random x in A = {', '.join(f'{r[2]:.4e}' for r in res)}; ebar(P1) = {ebar:.4e}; "
              f"holds: {all(r[2] <= ebar * (1 + 1e-9) for r in res)}; ratio max eps/ebar = {max(r[2] for r in res)/ebar:.4f}",
              flush=True)


if __name__ == "__main__":
    main()
