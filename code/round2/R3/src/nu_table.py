#!/usr/bin/env python3
"""nu = R*/ln(p^M * n) for every observed outcome (n = #classes or #positions tested). HEURISTIC calibration."""
import re, glob, os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bottleneck import profile, vf
obs = {}
for fn in glob.glob(os.path.join(os.path.dirname(__file__), '..', 'logs', 'scan_p*.log')):
    for line in open(fn):
        m = re.match(r"p=(\d+) t=(\d+) H=(\d+) c=(\d+) M=(\d+).*(HOLDS|FAILS)", line)
        if m and 'counting' not in line:
            p, t, H = map(int, m.groups()[:3]); c = int(m.group(4))
            n = (p**c - p**(c-1)) if c else 1
            obs[(p, t, H, n)] = m.group(6)
# position / single-class observations (n = number of positions/classes tested)
for k, v in {(13,8,45,1):'FAILS',(13,8,46,1):'FAILS',(13,8,47,12):'HOLDS',(11,7,39,1):'FAILS',(11,7,40,110):'FAILS',
             (11,7,41,1):'HOLDS',(19,7,45,18):'HOLDS',(17,7,43,16):'HOLDS',(5,5,35,312500):'FAILS',(5,5,38,312500):'FAILS',
             (7,7,40,42):'HOLDS',(11,8,44,10):'HOLDS',(17,7,42,272):'FAILS',(17,7,43,272):'HOLDS',(19,7,44,18):'FAILS',(23,7,43,22):'HOLDS',(7,8,46,6):'HOLDS',(7,8,47,6):'HOLDS',(17,8,47,16):'HOLDS',(13,7,38,156):'FAILS',(13,7,39,156):'HOLDS'}.items():
    obs.setdefault(k, v)
rows = []
for (p, t, H, n), st in obs.items():
    if t < 3: continue
    c = vf(H - 1, p); M = t + c
    o = profile(p, t, H, kmax=min(c, t, 5))
    if o['Rstar'] <= 0: continue
    rows.append((o['Rstar'] / math.log(p**M * n), p, t, H, n, o['Rstar'], st))
rows.sort()
fails = [r for r in rows if r[-1] == 'FAILS']; holds = [r for r in rows if r[-1] == 'HOLDS']
print("max nu among FAILS:", max(fails)[:6]); print("min nu among HOLDS:", min(holds)[:6])
print(f"n_obs={len(rows)} fails={len(fails)} holds={len(holds)}")
for r in rows:
    if 0.8 <= r[0] <= 1.7: print(f"nu={r[0]:.3f} p={r[1]} t={r[2]} H={r[3]} n={r[4]} R*={r[5]:.2f} {r[6]}")
