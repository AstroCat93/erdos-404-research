#!/usr/bin/env python3
"""smc_dstats.py -- pooled per-group defect estimates D_hat = p^J mean(f) - 1 from SMC output files [HEURISTIC].
Groups are binned by level range and by jump J; prints mean D_hat, its standard error, and the number of groups.
Theorem 1: true D >= 0, and log C_K = sum over groups of log(1 + D); so a level-range mean of D_hat that is
statistically indistinguishable from 0 indicates no growth of C in that range.
Usage: python3 smc_dstats.py file1 [file2 ...]"""
import sys, math
bins = [(1, 20), (20, 100), (100, 300), (300, 1000), (1000, 4001)]
data = {}
for fn in sys.argv[1:]:
    for line in open(fn):
        if line.startswith('lvl'):
            _, lvl, C, D, J = line.split()
            lvl, D, J = int(lvl), float(D), int(J)
            for lo, hi in bins:
                if lo <= lvl < hi:
                    key = (lo, hi, min(J, 3)); data.setdefault(key, []).append(D)
for key in sorted(data):
    xs = data[key]; n = len(xs); m = sum(xs) / n
    se = math.sqrt(sum((x - m) ** 2 for x in xs) / max(1, n - 1) / n)
    print("levels [%4d,%4d) J%s%d : n=%5d  mean D_hat = %+.3e  +- %.1e (1 s.e.)" % (key[0], key[1], '>=' if key[2] == 3 else '=', key[2], n, m, se))
