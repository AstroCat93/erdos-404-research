#!/usr/bin/env python3
"""compare_logs.py -- line-by-line comparison of the window schedule printed by M4C's assemble.log (last run per p,
i.e. the runs after the remainder fix) with this track's reassemble.log: phase-1 blocks, and for every phase-2 window
printed by both, the tuple (l, b_{l-1}, b_l, b_{l+1}, s_l, N_W, N, I).  Reads logs only.
usage: compare_logs.py data/round4/M4C/assemble.log data/round4/verify_C_obstruction/reassemble.log"""
import re
import sys

txt = open(sys.argv[1]).read()
theirs = {}
for r in re.split(r'### command: ', txt):
    m = re.search(r'assemble\.py (\d+) 0\.05 3000 1\.6', r)
    if not m:
        continue
    rows = re.findall(r'l=\s*(\d+) blocks \((\d+),(\d+),(\d+)\] s=(\d+) N_W=(\d+) N=(\d+) I=(\d+)', r)
    bl = re.search(r'phase 1: blocks \[([^\]]*)\]', r)
    theirs[int(m.group(1))] = (bl.group(1) if bl else None, rows)
mine, cur = {}, None
for line in open(sys.argv[2]):
    m = re.match(r'p=(\d+) phase1 blocks=\[([^\]]*)\]', line)
    if m:
        cur = int(m.group(1)); mine[cur] = (m.group(2), []); continue
    m = re.search(r'l=(\d+) \((\d+),(\d+),(\d+)\] s=(\d+) N_W=(\d+) N=(\d+) I=(\d+)', line)
    if m and cur:
        mine[cur][1].append(m.groups())
tot = bad = 0
for p in sorted(mine):
    b1, r1 = mine[p]
    b2, r2 = theirs[p]
    d2 = {r[0]: r for r in r2}
    cmp = [(a, d2[a[0]]) for a in r1 if a[0] in d2]
    nb = sum(1 for a, b in cmp if a != b)
    tot += len(cmp); bad += nb
    print(f"p={p}: phase-1 schedule identical: {b1.replace(' ', '') == b2.replace(' ', '')}; "
          f"phase-2 windows compared: {len(cmp)}, mismatches: {nb}")
print(f"TOTAL phase-2 windows compared: {tot}, mismatches: {bad}")
