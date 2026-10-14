#!/usr/bin/env python3
"""eps_factorial.py -- exact (deterministic) diagnostic: the fine-scale mass of FACTORIAL windows.

If v(x+n) = s0 is large, then for 0 <= c < p^s0 the window elements y_{n+c} = (x+n+1)...(x+n+c) satisfy
y_{n+c} == c! * (unit == 1 mod p^{s0 - v(c!)-...}); so the composite window [n, n+L+L') "looks like" the
factorials 0!, 1!, ..., (L+L'-1)! modulo p^{s0 - O(log)}.  This program computes, exactly,
   eps_fact(L, L') = p^K Coll_K - p^D Coll_D  for the elements c!,  D = v(L!), K = v((L+L')!),
and also the per-window chi^2 of the first window.  It is the value of eps right after a gate deep enough
(position-independent part, Corollary B2' of the M4B report).  Exact rationals; printed as floats.
usage: eps_factorial.py p KMAX ratio L1 L2 ...
"""
import sys
from fractions import Fraction

from m4b_lib import unsigned_dist, fold, sumsq


def vfact(n, p):
    s, q = 0, p
    while q <= n:
        s += n // q
        q *= p
    return s


def main():
    p, KMAX = int(sys.argv[1]), int(sys.argv[2])
    ratio = float(sys.argv[3])
    for L in (int(a) for a in sys.argv[4:]):
        L2 = int(round(ratio * L))
        T = L + L2
        D, K = vfact(L, p), vfact(T, p)
        if K > KMAX or D < 1:
            print(f"ROW p={p} L={L} L'={L2}: skipped (D={D}, K={K})")
            continue
        elems = []
        f = 1
        for c in range(T):
            elems.append(f)
            f *= (c + 1)
        m = unsigned_dist(elems, p ** K)
        cK = Fraction(sumsq(m), 4 ** T)
        cD = Fraction(sumsq(fold(m, p ** D)), 4 ** T)
        eps = p ** K * cK - p ** D * cD
        m1 = unsigned_dist(elems[:L], p ** D)
        chi1 = p ** D * Fraction(sumsq(m1), 4 ** L) - 1
        thetaL = Fraction(p ** D, 2 ** L)
        print(f"ROW p={p} L={L} L'={L2} D={D} K={K}: eps_fact={float(eps):.6g}  chi2_first={float(chi1):.4g}  "
              f"c_L/c_0={float(thetaL):.3g}  eps_fact/(c_L/c_0)={float(eps / thetaL):.4g}", flush=True)


if __name__ == "__main__":
    main()
