#!/usr/bin/env python3
"""smc_table.py -- aggregate SMC estimates of C_k across seeds [HEURISTIC].
Usage: python3 smc_table.py LEVELS FILE...   (LEVELS comma-separated; for each level the last group end <= level is used and printed; C is nondecreasing)
Prints, per level: mean, sample s.d., min, max of C_est over the files, and the refined random model value for p=2.
"""
import sys, math, bisect
levels = [int(x) for x in sys.argv[1].split(',')]
files = sys.argv[2:]
runs = []
for fn in files:
    pts = []
    for line in open(fn):
        if line.startswith('lvl'):
            _, l, C, D, J = line.split(); pts.append((int(l), float(C)))
    runs.append(pts)
def at(pts, L):
    ls = [l for l, _ in pts]; i = bisect.bisect_right(ls, L) - 1
    return (pts[i][0], pts[i][1]) if i >= 0 else None
def rm2(K):
    def vf(n):
        v = 0; m = n
        while m: m //= 2; v += m
        return v
    vs = [vf(n) for n in range(1, 3 * K + 50)]
    s = 1.0
    for k in range(1, K + 1):
        mk = bisect.bisect_left(vs, k); gk = mk - bisect.bisect_left(vs, k - 1)
        if gk == 0: s += 2.0 ** (k - 1 - mk)
    return s
print("# %d files: %s" % (len(files), ' '.join(f.split('/')[-1] for f in files)))
for L in levels:
    ys = [at(r, L) for r in runs]; ys = [y for y in ys if y is not None]
    lv = sorted(set(y[0] for y in ys)); xs = [y[1] for y in ys]
    m = sum(xs) / len(xs); sd = math.sqrt(sum((x - m) ** 2 for x in xs) / max(1, len(xs) - 1))
    print("k=%5d (group end used: %s)  mean C=%9.4f  sd=%8.4f  min=%9.4f  max=%9.4f   (p=2 refined random model %.3f)" % (L, ','.join(map(str, lv)), m, sd, min(xs), max(xs), rm2(lv[0])))
