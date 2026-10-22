#!/usr/bin/env python3
"""t4_Qbound.py -- the bound used in the proof of B1' for "Q_j < infinity", and its dependence on n_j.

usage: t4_Qbound.py p seed nx n_list(comma-separated) [maxpar]
For x Haar-random (half of them with a forced gate v(x+i) = s, i <= n, s drawn up to log_p(e(i-1)!)+1):
  (G)  Observation G: if Z^0_n(x) != 0 (n >= 2p) then every i <= n has p^{v(x+i)} <= e (i-1)!;
  (V)  V_n < n/(p-1) + M_n  (R3M Lemma 1(b));
  (B)  M := c_n Z^0_n <= p^{V_n}/2 <= p^{n/(p-1) + log_p(e (n-1)!)}/2 =: Bnd(n).
Reports, per n, the failures of (G), (V), (B), the maximum of c_n Z^0_n seen, and log10 Bnd(n), to show that
the bound proving boundedness of M_j depends on n_j (it is finite for each fixed n_j only).
"""
import math
import random
import sys
from fractions import Fraction

from vlib import PAdic, alive_from_scratch, products


def main():
    a = sys.argv[1:]
    p, seed, nx = int(a[0]), int(a[1]), int(a[2])
    nl = [int(t) for t in a[3].split(',')]
    P = PAdic(p, 200)
    rnd = random.Random(seed)
    print(f"RESULT t4 p={p} nx={nx} per n")
    for n in nl:
        fG = fV = fB = 0
        nz = 0
        best = Fraction(0)
        best_forced = Fraction(0)
        for it in range(nx):
            x = rnd.randrange(P.mod)
            forced = it % 2 == 1
            if forced:
                i = rnd.randrange(3, n + 1)
                smax = int(math.log(math.e * math.factorial(i - 1), p)) + 1
                s = rnd.randrange(1, smax + 1)
                x = (-i + p ** s * (1 + p * rnd.randrange(p ** 150))) % P.mod
            pi, dpi, vals = products(P, x, n)
            par = alive_from_scratch(P, pi, dpi, vals, n)
            Z = sum(1 for t in par if P.v(t[2]) == 0)
            Vn = sum(vals[1:n + 1])
            Mn = max(vals[1:n + 1])
            fV += not (Vn < n / (p - 1) + Mn)
            if Z:
                nz += 1
                fG += any(p ** vals[i] > math.e * math.factorial(i - 1) for i in range(1, n + 1))
                M = Fraction(p ** Vn * Z, 2 ** n)
                logB = (n / (p - 1)) * math.log10(p) + math.log10(math.e * math.factorial(n - 1)) - math.log10(2)
                fB += not (M <= Fraction(p ** Vn, 2) and math.log10(float(M)) <= logB + 1e-9)
                if forced:
                    best_forced = max(best_forced, M)
                else:
                    best = max(best, M)
        logB = (n / (p - 1)) * math.log10(p) + math.log10(math.e * math.factorial(n - 1)) - math.log10(2)
        print(f"  n={n}: Z^0!=0 in {nz}/{nx}; failures G {fG}, V {fV}, B {fB}; max M (Haar) {float(best):.4g}, "
              f"max M (forced gate) {float(best_forced):.4g}; log10 Bnd(n) = {logB:.2f}")


if __name__ == "__main__":
    main()
