#!/usr/bin/env python3
"""liftprof_validate.py -- compare bin/liftprof (C bitset) with the numpy routine support_np/lift_sizes on
random inputs (p, K, D, H, random residues and random window elements).  usage: liftprof_validate.py seed ntests"""
import random, subprocess, sys
import numpy as np
from m4d_lib import support_np, lift_sizes, window_elems

def run_c(p, K, D, ys):
    inp = f"{p} {K} {D} {len(ys)} " + " ".join(str(int(y)) for y in ys)
    out = subprocess.run(["./bin/liftprof"], input=inp, capture_output=True, text=True, check=True).stdout.split()
    assert out[0] == "LIFT"
    return int(out[1]), np.array([int(t) for t in out[2:]])

seed, nt = int(sys.argv[1]), int(sys.argv[2])
rnd = random.Random(seed)
bad = 0
for it in range(nt):
    p = rnd.choice([3, 5, 7, 11, 13])
    K = rnd.randint(1, {3: 12, 5: 8, 7: 7, 11: 5, 13: 5}[p])
    D = rnd.randint(0, K)
    H = rnd.randint(1, 18)
    mK = p ** K
    if rnd.random() < 0.5:
        ys = [rnd.randrange(mK) for _ in range(H)]
    else:
        x = rnd.randrange(p ** 40); n = rnd.randint(1, 60)
        ys = window_elems(x, n, n + H, mK)
    S = support_np(ys, mK)
    Lnp = lift_sizes(S, p, D, K - D)
    cnt, Lc = run_c(p, K, D, ys)
    if cnt != int(S.sum()) or not np.array_equal(Lnp, Lc):
        bad += 1
        print("MISMATCH", p, K, D, H)
print(f"RESULT liftprof_validate seed={seed} tests={nt} mismatches={bad}")
