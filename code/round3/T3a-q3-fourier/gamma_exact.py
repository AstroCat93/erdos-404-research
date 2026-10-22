#!/usr/bin/env python3
"""gamma_exact.py -- exact block constants for the L^2 route (track T3a, round 3, 2026-10-21).

For an odd prime p let e_u = (p-1)! (-1)^u / u!  (u = 0..p-1) be the gate pattern (note Thm 3.9(b)).
Let eta_u be i.i.d. in {-1,0,1} with probabilities 1/4,1/2,1/4 and W = sum_u eta_u e_u.
  Gamma_p(J) := p^J P(W == 0 mod p^J) - 1  = sum_{u != 0 mod p^J} prod_r cos^2(pi u e_r / p^J)   (Parseval)
  I_2(p)     := P(W = 0 exactly)  = 4^{-p} #{weighted eta with W = 0}
  Sigma(p)   := sum_u |e_u|   (the largest frequency of the trigonometric polynomial prod cos^2)
Theorem B'(b): Gamma_p(J) = p^J I_2(p) - 1 whenever p^J > Sigma(p).
Also Gamma'_p := p P(sum_{r=1}^{p-1} eta_r r! == 0 mod p) - 1 (the partial first block of N0 = 1),
and Gamma_p(1) with the pattern r! (same as e_u mod p up to the unit (p-1)!/... -- checked here).
Everything is exact (Fractions); floats are printed for comparison with data/cpJ.txt (double precision).
Usage: python3 -I gamma_exact.py [p ...]   (default 3 5 7 11 13), writes data/gamma_exact.txt
"""
import sys, os
from fractions import Fraction
from math import factorial

def signed_sum_counts(elems, mod=None):
    """weighted counts (weights 2 for eta=0, 1 for eta=+-1) of sum eta_i elems_i, mod `mod` (None: exact integers)."""
    cnt = {0: 1}
    for a in elems:
        new = {}
        for s, c in cnt.items():
            for d, w in ((0, 2), (a, 1), (-a, 1)):
                t = s + d
                if mod is not None: t %= mod
                new[t] = new.get(t, 0) + c * w
        cnt = new
    return cnt

def pattern(p):
    return [factorial(p - 1) * (-1) ** u // factorial(u) for u in range(p)]

def gamma(p, J, elems=None):
    elems = pattern(p) if elems is None else elems
    m = p ** J
    cnt = signed_sum_counts([e % m for e in elems], m)
    return Fraction(m * cnt.get(0, 0), 4 ** len(elems)) - 1

def main():
    ps = [int(a) for a in sys.argv[1:]] or [3, 5, 7, 11, 13]
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    out = []
    def pr(s):
        print(s); out.append(s)
    for p in ps:
        e = pattern(p)
        Sig = sum(abs(x) for x in e)
        cnt = signed_sum_counts(e)
        I2 = Fraction(cnt.get(0, 0), 4 ** p)
        pr("p=%d  e_u=%s  Sigma=%d  I_2(p)=%s = %.10e  (2^-p = %.10e, ratio I_2*2^p = %s)" % (
            p, e, Sig, I2, float(I2), 2.0 ** -p, I2 * 2 ** p))
        # partial first block (N0=1): elements 1!,...,(p-1)! mod p
        gp = gamma(p, 1, [factorial(r) for r in range(1, p)])
        pr("p=%d  Gamma'_p (partial first block {1!..(p-1)!} mod p) = %s = %.10f" % (p, gp, float(gp)))
        g1r = gamma(p, 1, [factorial(r) for r in range(p)])
        pr("p=%d  Gamma_p(1) with pattern r! = %s = %.10f" % (p, g1r, float(g1r)))
        J = 1
        while p ** J <= 20_000_000:
            g = gamma(p, J)
            pred = p ** J * I2 - 1
            pr("p=%d J=%d  Gamma_p(J)=%s = %.10e   p^J I_2 - 1 = %.10e   identity holds: %s   (p^J > Sigma: %s)" % (
                p, J, g, float(g), float(pred), g == pred, p ** J > Sig))
            J += 1
    open(os.path.join(base, 'data', 'gamma_exact.txt'), 'w').write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
