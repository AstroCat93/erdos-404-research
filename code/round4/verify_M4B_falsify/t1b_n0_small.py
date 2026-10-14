"""t1b_n0_small.py -- sensitivity of Lemma B1a to the hypothesis n_0 >= 2p: with n_0 in [p, 2p) the
cylinder x + p^{V_{n_0}(x)} Z_p need not have constant V_{n_0} (expected failures), while for
n_0 >= 2p it always does.  Usage: python3 t1b_n0_small.py SEED NX"""
import sys, random
from fz_lib import *
seed, NX = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
for p in (3, 5, 7):
    for n0 in (p, p + 1, 2 * p - 1, 2 * p, 2 * p + 1):
        bad = 0; tot = 0
        for _ in range(NX):
            X = rng.randrange(p ** 40)
            m0 = prefix(vals(X, p, n0))[0][n0]
            for _ in range(5):
                Y = X + p ** m0 * rng.randrange(p ** 20)
                tot += 1
                if prefix(vals(Y, p, n0))[0][n0] != m0:
                    bad += 1
        print(f"RESULT p={p} n0={n0} ({'>= 2p' if n0 >= 2 * p else '< 2p'}): V_n0 non-constant on its cylinder in {bad}/{tot} lifts")
