#!/usr/bin/env python3
"""lemma_f_check.py -- exact test of Lemma F + Lemma Q at the level of the composite window (report Section 3):
the high-slope term of Theorem 1,
    HS := p^K P_{delta, x in B}( delta != 0, v(S_delta(x)) >= K, v(S_delta'(x)) >= theta ),
computed exactly (integer DP over (S mod p^K, S' mod p^theta) for every x in B mod p^K), is compared with the
first-index sum of Proposition E,  sum_{a_c>=K} 2^-c-1 p^K + sum_{a_c<K} 2^-c-1 p^a_c G_c  (Lemma Q bounds G_c,
exact block-0 probabilities).  Prints max HS / bound (sensitivity) and the number of 2D factors used.
usage: lemma_f_check.py p SEED NB n H1 H2 b KMAX
"""
import random
import sys
from fractions import Fraction

import numpy as np

from bounds import qconsts, block0_table, lemmaQ_bound, window_data
from m4a_lib import vp


def signed_joint(ys, dys, p, K, th):
    m1, m2 = p ** K, p ** th
    st = np.zeros((m1, m2), dtype=np.int64)
    st[0, 0] = 1
    for y, dy in zip(ys, dys):
        a, bb = int(y % m1), int(dy % m2)
        st = 2 * st + np.roll(np.roll(st, a, axis=0), bb, axis=1) + np.roll(np.roll(st, -a, axis=0), -bb, axis=1)
    return st


def main():
    p, seed, NB, n, H1, H2, b, KMAX = (int(a) for a in sys.argv[1:9])
    N, N2 = n + H1, n + H1 + H2
    H = N2 - n
    q = qconsts(p, 8)
    P0 = block0_table(p, 12)
    rnd = random.Random(seed)
    done = ok = tries = 0
    worst = 0.0
    while done < NB and tries < 300000:
        tries += 1
        xB = rnd.randrange(p ** b)
        if any((xB + i) % p ** b == 0 for i in range(1, N2 + 1)):
            continue
        depth = [0] + [vp(xB + i, p) for i in range(1, N2 + 1)]
        D, K, a, MW = window_data(depth, n, N, N2)
        if D < 2 or K > KMAX or K <= D:
            continue
        th = min((D + 1) // 2, D - b + 1)
        if th < 1 or K - MW < th or p ** (K + th) > 4 * 10 ** 6:
            continue
        done += 1
        nw = p ** max(0, K - b)
        hs = Fraction(0)
        for w in range(nw):
            x = xB + p ** b * w
            ys, dys = [], []
            y, dy = 1, 0
            for c in range(H):
                ys.append(y)
                dys.append(dy)
                f = x + n + c + 1
                y, dy = y * f, dy * f + y
            st = signed_joint(ys, dys, p, K, th)
            hs += Fraction(int(st[0, 0]) - 2 ** H, 4 ** H)
        hs = p ** K * hs / nw
        bnd = Fraction(0)
        for c in range(H):
            wgt = Fraction(1, 2 ** (c + 1))
            if a[c] >= K:
                bnd += wgt * p ** K
            else:
                bnd += wgt * p ** a[c] * lemmaQ_bound(depth, n + c, H - c, K - a[c], th - a[c], p, q, P0)
        good = hs <= bnd
        ok += good
        if hs > 0:
            worst = max(worst, float(hs / bnd))
        print(f"B#{done}: xB={xB} D={D} K={K} th={th}  HS={float(hs):.5e} <= bound={float(bnd):.5e}: {good}  ratio={float(hs/bnd) if bnd else 0:.4f}", flush=True)
    print(f"RESULT p={p} n={n} H1={H1} H2={H2} b={b}: Lemma F+Q bound holds in {ok}/{done}; max HS/bound = {worst:.4f}")


if __name__ == "__main__":
    main()
