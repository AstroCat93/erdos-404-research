#!/usr/bin/env python3
"""eprime_check.py -- consistency test of Proposition E' (closed form) against the block-level formula of
Proposition E (fe_lib.blocklevel), from which E' is derived by further upper bounds (P0 <= 1, Legendre counts,
sum over levels).  Since E' >= blocklevel must hold for every window and gate pattern, any violation would expose
an error in the derivation of E'.  Random x (Haar, integer-like, or with planted deep gates), random windows.
usage: eprime_check.py p SEED NW nmin nmax
"""
import math
import random
import sys

from mpmath import mpf

from fe_lib import Consts, blocklevel, Eprime, up
from m4a_lib import vp


def main():
    p, seed, NW, nmin, nmax = (int(a) for a in sys.argv[1:6])
    C = Consts(p)
    rnd = random.Random(seed)
    tested = bad = 0
    worst = None
    while tested < NW:
        x = rnd.randrange(p ** 60)
        mode = rnd.randrange(3)
        n = rnd.randrange(nmin, nmax)
        N = n + rnd.randrange(n // 5, n // 2)
        N2 = N + rnd.randrange(n // 5, n // 2)
        if mode == 1:
            x = (rnd.randrange(1, 10 ** 6) + p ** 50 * rnd.randrange(1, p)) % p ** 60
        elif mode == 2:
            g0 = n + rnd.randrange(1, 3 * p)
            x = (-g0 + p ** rnd.randrange(2, 7) * rnd.randrange(1, p) + p ** 40 * rnd.randrange(p)) % p ** 60
        depth = [0] + [vp(x + i, p) for i in range(1, N2 + 1)]
        V = [0] * (N2 + 1)
        for i in range(1, N2 + 1):
            V[i] = V[i - 1] + depth[i]
        D, K = V[N] - V[n], V[N2] - V[n]
        MW = max(depth[n + 1:N2 + 1])
        b = MW + 1
        th = min((D + 1) // 2, D - b + 1)
        if th < 1 or K - MW < th:
            continue
        sig = MW
        fpr = min(th, K - sig)
        bl = up(blocklevel(C, depth, V, n, N2, K, th, MW))
        ep = up(Eprime(C, K, N2 - n, fpr, sig))
        tested += 1
        ratio = float(mpf.__truediv__(bl, ep)) if ep > 0 else float('inf')
        if not bl <= ep:
            bad += 1
            print(f"VIOLATION mode={mode} n={n} N={N} N2={N2} D={D} K={K} MW={MW} th={th}: block={float(bl):.4e} > E'={float(ep):.4e}")
        if worst is None or ratio > worst:
            worst = ratio
    print(f"RESULT p={p} windows={tested}: E' >= block-level in {tested - bad}/{tested}; max block/E' = {worst:.4e}")


if __name__ == "__main__":
    main()
