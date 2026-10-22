#!/usr/bin/env python3
"""qconst_brute.py -- independent brute-force recomputation of q1, q2, q3 (M4C report, section 6) by enumerating
all 3^p signed vectors d in {-1,0,1}^p with weight 2^{#zeros}/4^p (no DP, no shared code with early_phase.py).
  q1 = p   max_a     P(A = a mod p),                A = sum_r d_r r!
  q2 = p^2 max_{a,b} P(A = a mod p, floor(A/p) - B = b mod p),  B = sum_r d_r r! H_r mod p
  q3 = p^3 max_a     P(sum_r d_r F_r = a mod p^3),  F_r = prod_{s=1}^r (s - p)
usage: qconst_brute.py p1 p2 ...      (p <= 13 is practical)
"""
import itertools
import sys
from collections import Counter
from fractions import Fraction
from math import factorial


def main():
    for p in (int(a) for a in sys.argv[1:]):
        fact = [factorial(r) for r in range(p)]
        H = [Fraction(0)]
        for j in range(1, p):
            H.append(H[-1] + Fraction(1, j))
        Hm = [h.numerator * pow(h.denominator, -1, p) % p for h in H]
        F = [1]
        for r in range(1, p):
            F.append(F[-1] * (r - p))
        c1, c2, c3 = Counter(), Counter(), Counter()
        for d in itertools.product((-1, 0, 1), repeat=p):
            w = 2 ** d.count(0)
            A = sum(di * f for di, f in zip(d, fact))
            B = sum(di * f * h for di, f, h in zip(d, fact, Hm)) % p
            c1[A % p] += w
            c2[(A % p, ((A // p) - B) % p)] += w
            c3[sum(di * f for di, f in zip(d, F)) % p ** 3] += w
        W = 4 ** p
        q1 = Fraction(p * max(c1.values()), W)
        q2 = Fraction(p * p * max(c2.values()), W)
        q3 = Fraction(p ** 3 * max(c3.values()), W)
        print(f"p={p}: q1={q1} ({float(q1):.12f})  q2={q2} ({float(q2):.12f})  q3={q3} ({float(q3):.12f})", flush=True)


if __name__ == "__main__":
    main()
