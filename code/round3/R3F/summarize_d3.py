#!/usr/bin/env python3
"""summarize_d3.py -- D3: rigorous Cauchy-Schwarz bound sum_k sqrt(N_k Q(k)) from the certified L^2 shells
(column T2_hi of an ivshell log; printed values rounded up by one unit in the 13th digit), next to the certified L^1 sum.
usage: summarize_d3.py IVSHELL_LOG p"""
import sys
from fractions import Fraction
from mpmath import iv
iv.prec = 100
path, p = sys.argv[1], int(sys.argv[2])
tot = iv.mpf(0); l1 = Fraction(0)
for line in open(path):
    if line.startswith('#') or not line.strip():
        continue
    w = line.split(); k = int(w[0])
    def up(x):
        m, e = x.lower().split('e'); return Fraction(m) * Fraction(10) ** int(e) + Fraction(1, 10 ** 12) * Fraction(10) ** int(e)
    Q = up(w[4]); T = up(w[2])
    N = p ** k - p ** (k - 1)
    term = iv.sqrt(iv.mpf(N) * (iv.mpf(Q.numerator) / Q.denominator))
    tot += term; l1 += T
    print(f"k={k}  sqrt(N_k Q(k)) <= {float(term.b):.6e}   T1(k) <= {float(T):.6e}   ratio {float(term.b)/float(T):.3f}")
print(f"SUM: C-S bound <= {float(tot.b):.8f}   certified L1 sum <= {float(l1):.8f}   factor {float(tot.b)/float(l1):.3f}")
