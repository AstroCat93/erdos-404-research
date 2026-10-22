#!/usr/bin/env python3
"""ck_deepgate_M2.py -- heuristic importance-sampling probe of the tail of E[(M^0_n)^2] at odd p.

M^0_n = c_n Z^0_n, c_n = 2^-n p^{V_n}, Z^0_n = # slope-0 paths alive at n (exact DFS, ck_lib).
For a fixed gate position i <= n and depth s, sample x = -i + p^s (u + p*h) with u a random unit
digit and h random high digits (so v(x+i) = s exactly), and estimate
    contrib(i,s) = mu{v(x+i) = s} * E[(M^0_n)^2 | v(x+i) = s] = (1-1/p) p^-s E[(M^0_n)^2 | ...],
the part of the unconditional second moment E[(M^0_n)^2] coming from that event; also the same for
the first moment.  If contrib(i,s) does not decay in s, then plain Monte Carlo with S samples cannot
see the contributions of depths s > log_p S, and the unconditional second moment is the sum of
roughly (number of crossable depths) such terms.
usage: ck_deepgate_M2.py p seed nsamp n i smax
"""
import random
import sys
from fractions import Fraction

from ck_lib import PAdic, products, alive_from_scratch


def main():
    p, seed, ns, n, i, smax = (int(a) for a in sys.argv[1:7])
    P = PAdic(p, 3 * n + 60)
    rnd = random.Random(seed)
    tot1 = tot2 = 0.0
    for s in range(1, smax + 1):
        m1 = m2 = 0.0
        nz = 0
        for _ in range(ns):
            u = rnd.randrange(1, p)
            h = rnd.randrange(P.mod // p ** (s + 1))
            x = (-i + p ** s * (u + p * h)) % P.mod
            pi, dpi, vals = products(P, x, n)
            assert vals[i] == s
            Vn = sum(vals[1:n + 1])
            al = alive_from_scratch(P, pi, dpi, vals, n)
            Z0 = sum(1 for (_, _, dS) in al if P.v(dS) == 0)
            M = Z0 * p ** Vn / 2 ** n
            m1 += M
            m2 += M * M
            nz += Z0 > 0
        w = (1 - 1 / p) * p ** (-s)
        c1, c2 = w * m1 / ns, w * m2 / ns
        tot1 += c1
        tot2 += c2
        print(f"TABLE p={p} n={n} gate i={i} depth s={s}: P(Z0>0|gate)={nz / ns:.3f} "
              f"E[M|gate]={m1 / ns:.4g} E[M^2|gate]={m2 / ns:.4g} contrib1={c1:.4g} contrib2={c2:.4g}")
    print(f"RESULT deepgate p={p} n={n} i={i} samples/depth={ns}: sum_s contrib1={tot1:.4g} sum_s contrib2={tot2:.4g}")


if __name__ == "__main__":
    main()
