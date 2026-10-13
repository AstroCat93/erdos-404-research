#!/usr/bin/env python3
"""ck_mc_M.py -- independent Monte Carlo of the slope-0 martingale M^0_n = c_n Z^0_n (heuristic).

Exact DFS of all alive paths (ck_lib) for Haar-random x (PREC p-adic digits); for each n in the
list, reports P(Z>0), P(Z^0>0), E[M^0_n], E[(M^0_n)^2] with standard errors (plain sample s.e.),
the largest single-sample share of the sum of (M^0_n)^2 (a heavy-tail indicator), and the
ratio E[M^2]/E[M]^2.  Used only to cross-check the numbers of R3M section 7.1.
usage: ck_mc_M.py p seed nx n1,n2,...
"""
import math
import random
import sys

from ck_lib import PAdic, products, alive_from_scratch


def main():
    p, seed, nx = (int(a) for a in sys.argv[1:4])
    ns = [int(t) for t in sys.argv[4].split(",")]
    nmax = max(ns)
    P = PAdic(p, 3 * nmax + 60)
    rnd = random.Random(seed)
    data = {n: [] for n in ns}
    alive_any = {n: 0 for n in ns}
    for _ in range(nx):
        x = rnd.randrange(P.mod)
        pi, dpi, vals = products(P, x, nmax)
        for n in ns:
            al = alive_from_scratch(P, pi, dpi, vals, n)
            Vn = sum(vals[1:n + 1])
            Z0 = sum(1 for (_, _, dS) in al if P.v(dS) == 0)
            alive_any[n] += len(al) > 0
            data[n].append(Z0 * p ** Vn / 2 ** n)
    for n in ns:
        d = data[n]
        k = len(d)
        m1 = sum(d) / k
        sq = [t * t for t in d]
        m2 = sum(sq) / k
        se1 = math.sqrt(max(0.0, sum((t - m1) ** 2 for t in d) / (k - 1) / k))
        se2 = math.sqrt(max(0.0, sum((t - m2) ** 2 for t in sq) / (k - 1) / k))
        share = max(sq) / sum(sq) if sum(sq) > 0 else 0.0
        pz0 = sum(1 for t in d if t > 0) / k
        print(f"TABLE p={p} n={n} samples={k}: P(Z>0)={alive_any[n] / k:.4f} P(Z0>0)={pz0:.4f} "
              f"E[M]={m1:.4f}+-{se1:.4f} E[M^2]={m2:.4f}+-{se2:.4f} ratio={m2 / m1 ** 2 if m1 else 0:.2f} "
              f"max single-sample share of sum M^2={share:.3f}")
    print(f"RESULT mcM p={p} seed={seed} samples={nx} done")


if __name__ == "__main__":
    main()
