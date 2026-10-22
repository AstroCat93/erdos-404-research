#!/usr/bin/env python3
"""alive_targets_validate.py -- compare lift_scan.alive_targets (numpy DP over S_e(x) mod p^(V_n+D)) with the
set of targets tau_n(e,x) mod p^D of the alive paths found by the validated DFS (m4d_lib.alive_from_scratch).
usage: alive_targets_validate.py seed ntests"""
import random, sys
import numpy as np
from m4d_lib import PAdic, products, alive_from_scratch, target, vp_int
from lift_scan import alive_targets

seed, nt = int(sys.argv[1]), int(sys.argv[2])
rnd = random.Random(seed)
bad = done = 0
while done < nt:
    p = rnd.choice([3, 5, 7, 11])
    n = rnd.randint(2, {3: 16, 5: 18, 7: 20, 11: 22}[p])
    D = rnd.randint(0, 4)
    P = PAdic(p, 80)
    x = rnd.randrange(P.mod)
    pi, dpi, vals = products(P, x, n)
    if max(vals[1:]) > 6:
        continue
    Vn = sum(vals[1:n + 1])
    if p ** (Vn + D) > 3 * 10 ** 6:
        continue
    done += 1
    par = alive_from_scratch(P, pi, dpi, vals, n)
    ref = set(target(P, S, pi[n], Vn) % p ** D for (b, S, dS) in par)
    T = alive_targets(x, n, p, Vn, D, [0] + [vp_int(x + i, p, 80) for i in range(1, n + 1)])
    got = set(int(i) for i in np.nonzero(T)[0])
    if ref != got:
        bad += 1
        print("MISMATCH", p, n, D, len(ref), len(got))
print(f"RESULT alive_targets_validate seed={seed} tests={nt} mismatches={bad}")
