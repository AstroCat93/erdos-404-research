#!/usr/bin/env python3
"""Tabulate R* (bottleneck ratio, K-independent levels k<=min(c,t)) against the observed outcome
(uniform scans: HOLDS/FAILS; position runs: covered/not) -- calibration of the heuristic threshold."""
import re, glob, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bottleneck import profile, vf
rows = {}
for fn in glob.glob(os.path.join(os.path.dirname(__file__), '..', 'logs', 'scan_p*.log')):
    for line in open(fn):
        m = re.match(r"p=(\d+) t=(\d+) H=(\d+) c=(\d+) M=(\d+).*(HOLDS|FAILS)", line)
        if m and 'counting' not in line:
            p, t, H = map(int, m.groups()[:3]); rows[(p, t, H)] = m.group(6)
extra = {(13,7,38):'FAILS',(13,7,39):'HOLDS',(13,8,45):'FAILS@K1',(13,8,46):'FAILS@K1',(13,8,47):'HOLDS@12pos',
         (11,7,39):'FAILS@K1',(11,7,40):'FAILS@K37(1/110pos)',(11,7,41):'HOLDS@K37',(19,7,45):'HOLDS@18pos',(17,7,43):'HOLDS@16pos',
         (5,5,35):'FAILS',(5,5,38):'FAILS',(5,5,39):'sample0/391'}
for k,v in extra.items(): rows.setdefault(k, v)
out = []
for (p, t, H), st in sorted(rows.items()):
    if t < 3: continue
    c = vf(H - 1, p)
    o = profile(p, t, H, kmax=min(c, t, 6))
    out.append((o['Rstar'], p, t, H, o['R0'], st))
out.sort()
for r, p, t, H, R0, st in out:
    if r == 0: continue
    print(f"R*={r:9.2f}  R0={R0:10.3g}  p={p:2d} t={t} H={H:2d}  {st}")
