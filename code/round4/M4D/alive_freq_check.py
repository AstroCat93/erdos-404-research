#!/usr/bin/env python3
"""alive_freq_check.py -- frequency of P(x,n) for Haar-random x by the exact target-set recursion
(plateau_check.P_holds) and by the numpy DP of lift_scan.alive_targets (D=0), for cross-checking the scans'
'P(alive at n0)' against the census value delta_8(7)=0.62394 <= mu{P(x,21)} + mu{V_21 > 8}.
usage: alive_freq_check.py p seed NX n"""
import random, sys
from m4d_lib import vp_int
from plateau_check import P_holds
from lift_scan import alive_targets
p, seed, NX, n = (int(t) for t in sys.argv[1:5])
rnd = random.Random(seed)
a = b = dis = 0
for _ in range(NX):
    x = rnd.randrange(p ** 80)
    vals = [0] + [vp_int(x + i, p, 80) for i in range(1, n + 1)]
    r1 = P_holds(x, p, [n])[n]
    r2 = bool(alive_targets(x, n, p, sum(vals), 0, vals).any())
    a += r1; b += r2; dis += (r1 != r2)
print(f"RESULT alive_freq p={p} n={n} NX={NX}: P(x,n) recursion={a/NX:.4f}, numpy DP={b/NX:.4f}, disagreements={dis}")
