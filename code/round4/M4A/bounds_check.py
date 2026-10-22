#!/usr/bin/env python3
"""bounds_check.py -- exact tests of Proposition E (averaged bound on E_B eps) and Proposition D (pointwise
bound on p^K Coll_K, hence on eps) of data/round4/reports/M4A.md, against exact collision computations.
usage: bounds_check.py p SEED NB n H1 H2 b KMAX
"""
import random
import sys
from fractions import Fraction

import numpy as np

from bounds import qconsts, propE_bound, propD_bound, block0_table
from m4a_lib import vp


def coll_counts(elems, p, K):
    mod = p ** K
    dist = np.zeros(mod, dtype=np.int64)
    dist[0] = 1
    for y in elems:
        dist = dist + np.roll(dist, int(y % mod))
    return dist


def main():
    p, seed, NB, n, H1, H2, b, KMAX = (int(a) for a in sys.argv[1:9])
    N, N2 = n + H1, n + H1 + H2
    H = N2 - n
    q = qconsts(p, 7)
    P0 = block0_table(p, 12)
    rnd = random.Random(seed)
    done = okE = okD = tries = 0
    worstE = worstD = 0.0
    while done < NB and tries < 200000:
        tries += 1
        xB = rnd.randrange(p ** b)
        if any((xB + i) % p ** b == 0 for i in range(1, N2 + 1)):
            continue
        depth = [0] + [vp(xB + i, p) for i in range(1, N2 + 1)]
        D = sum(depth[n + 1:N + 1])
        K = sum(depth[n + 1:N2 + 1])
        if D < 1 or K > KMAX or K <= D:
            continue
        MW = max(depth[n + 1:N2 + 1])
        th = min((D + 1) // 2, D - b + 1)
        if th > 0 and K - MW < th:
            continue
        done += 1
        nw = p ** max(0, K - b)
        Eeps = Fraction(0)
        maxPK = Fraction(0)
        for w in range(nw):
            x = xB + p ** b * w
            ys = []
            y = 1
            for c in range(H):
                ys.append(y)
                y = y * (x + n + c + 1)
            dist = coll_counts(ys, p, K)
            cK = int(np.dot(dist, dist))
            fD = dist.reshape(-1, p ** D).sum(axis=0)
            cD = int(np.dot(fD, fD))
            pKC = Fraction(p ** K * cK, 4 ** H)
            Eeps += pKC - Fraction(p ** D * cD, 4 ** H)
            maxPK = max(maxPK, pKC)
        Eeps /= nw
        bE, th = propE_bound(depth, n, N, N2, b, p, q, P0)
        bD = propD_bound(depth, n, N, N2, p, q, 'K', P0)
        gE = Eeps <= bE
        gD = maxPK <= bD
        okE += gE
        okD += gD
        worstE = max(worstE, float(Eeps / bE))
        worstD = max(worstD, float(maxPK / bD))
        print(f"B#{done}: xB={xB} D={D} K={K} th={th}  E_B eps={float(Eeps):.4e} <= propE={float(bE):.4e}: {gE};  "
              f"max_B p^K Coll_K={float(maxPK):.4e} <= propD={float(bD):.4e}: {gD}", flush=True)
    print(f"RESULT p={p} n={n} H1={H1} H2={H2} b={b}: Prop E holds in {okE}/{done}, Prop D in {okD}/{done}; "
          f"max ratios E: {worstE:.4f}, D: {worstD:.4f}")


if __name__ == "__main__":
    main()
