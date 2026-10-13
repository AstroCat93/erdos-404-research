#!/usr/bin/env python3
"""pred_recount.py -- check of track R3C (round 3, 2026-10-13): recount the registered predictions
of Conjecture 10.24 (data/round3/R3C/PREDICTIONS_registered.txt) against the outcomes in the logs,
independently of code/round3/R3C/pred_eval.py (own parser, own classification rules).

Classification (the R3C report's categories, rules restated here):
  proved   -- row marked '(proved, Lemma 10.11)' in the registration
  known    -- t = 1 (Lemma 10.11), or Cov(p,5,p) / Cov(p,6,p) (L_29 = L_31 = 5)
  mixed    -- band MIXED
  test     -- band FAIL or HOLD with an outcome in the logs: confirmed / falsified
  not run  -- no outcome
Outcome sources: scan verdict lines (scan*_p*.log): 'HOLDS' / 'FAILS ... [AGREE]'; depth-7 positions:
lines 'A|D ... K=.. missing=..' and 'C ... miss=..' in p29_t7*/.
It also evaluates the registration's own headline prediction, 'predicted minimal H (first HOLD-band H)',
for p = 29, 31 and t = 2..6, against the minimal uniform H_t found in the scans.
usage: python3 pred_recount.py   (from the repository root)
"""
import glob
import re

R = 'data/round3/R3C'
out = {}
for fn in glob.glob(f'{R}/scan*_p*.log'):
    for ln in open(fn):
        m = re.match(r'p=(\d+) t=(\d+) H=(\d+) [^:]*: (HOLDS|FAILS)(.*)', ln.strip())
        if m:
            key = tuple(map(int, m.groups()[:3]))
            v = m.group(4)
            if v == 'FAILS' and 'by counting' not in m.group(5) and 'Lemma' not in m.group(5) and '[AGREE]' not in m.group(5):
                v = 'DISAGREE'
            if key in out and out[key] != v:
                print('CONFLICT', key, out[key], v)
            out[key] = v
pos = {}
for fn in glob.glob(f'{R}/p29_t7*/*.log'):
    for ln in open(fn):
        s = ln.strip()
        m = re.match(r'^([AD]) p=(\d+) t=7 H=(\d+) .* K=(\d+) (?:Kmodpc=\d+ )?missing=(\d+) ', s)
        mc = re.match(r'^C p=(\d+) t=7 H=(\d+) M=\d+ K=(\d+) Kmodpc=\d+ miss=(\d+) ', s)
        if m:
            pos.setdefault((int(m.group(2)), int(m.group(3))), {}).setdefault(int(m.group(4)), {})[m.group(1)] = int(m.group(5))
        elif mc:
            pos.setdefault((int(mc.group(1)), int(mc.group(2))), {}).setdefault(int(mc.group(3)), {})['C'] = int(mc.group(4))

rows = []
cur = None
for ln in open(f'{R}/PREDICTIONS_registered.txt'):
    m = re.match(r'p=(\d+) t=(\d+) \[(uniform|positions n=\d+)\] predicted minimal H \(first HOLD-band H\) = (\d+)', ln)
    if m:
        cur = (int(m.group(1)), int(m.group(2)), m.group(3).startswith('pos'), int(m.group(4)))
        continue
    m = re.match(r'\s+H=(\d+)(.*)', ln)
    if m and cur:
        H = int(m.group(1))
        band = 'proved' if 'proved' in m.group(2) else re.search(r'-> (\w+)', m.group(2)).group(1)
        rows.append((cur[0], cur[1], H, cur[2], band))
        continue
    m = re.match(r'extra: p=(\d+) t=(\d+) H=(\d+) n=(\d+) .* -> (\w+)', ln)
    if m and int(m.group(4)) > 1:
        rows.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), True, m.group(5)))

cnt = {}
near = []
for p, t, H, isPos, band in rows:
    if band == 'proved':
        cls = 'proved'
    elif t == 1 or (t in (5, 6) and H == p):
        cls = 'known'
    elif band == 'MIXED':
        cls = 'mixed'
    else:
        if isPos:
            d = pos.get((p, H), {})
            if band == 'HOLD':
                ok = all(d.get(K, {}).get('A') == 0 and d.get(K, {}).get('D') == 0 for K in range(1, p))
                o = 'HOLD' if ok else None
            else:
                f = [K for K, v in d.items() if len([x for x in v.values() if x > 0]) >= 2]
                o = 'FAIL' if f else None
        else:
            o = {'HOLDS': 'HOLD', 'FAILS': 'FAIL'}.get(out.get((p, t, H)))
        if o is None:
            cls = 'not run'
        else:
            cls = 'confirmed' if o == band else 'FALSIFIED'
    cnt[cls] = cnt.get(cls, 0) + 1
    if cls == 'FALSIFIED':
        print('falsified row:', p, t, H, 'pos' if isPos else 'uniform', band)
print('rows:', len(rows), ' classes:', dict(sorted(cnt.items())))

# the registration's headline: minimal uniform H_t = first HOLD-band H (p = 29, 31; t = 2..6)
print('minimal-H_t predictions (registered first HOLD-band H vs scans):')
cur = None
for ln in open(f'{R}/PREDICTIONS_registered.txt'):
    m = re.match(r'p=(\d+) t=(\d+) \[uniform\] predicted minimal H \(first HOLD-band H\) = (\d+)', ln)
    if m and 2 <= int(m.group(2)) <= 6:
        p, t, Hp = map(int, m.groups())
        holds = sorted(H for (pp, tt, H), v in out.items() if (pp, tt) == (p, t) and v == 'HOLDS')
        Hmin = holds[0] if holds else None
        # minimality: every H < Hmin must have a FAILS verdict or be excluded by counting (absent from the scan)
        print(f'  p={p} t={t}: registered {Hp}, observed minimal {Hmin} -> {"confirmed" if Hp == Hmin else "NOT confirmed"}')
