#!/usr/bin/env python3
"""pred_eval.py (round 3, track R3C; added when the track was completed, 2026-10-13).

Compares every row of data/round3/R3C/PREDICTIONS_registered.txt (registered 06:12:36 UTC) with the
outcomes in the R3C logs, and classifies each row:
  proved      -- refuted by counting or Lemma 10.11 (marked 'proved' in the registration; not a test)
  known       -- outcome known before registration (t = 1: Lemma 10.11, Cov(p,1,H) iff H >= rho0+1;
                 Cov(p,5,p) holds and Cov(p,6,p) fails because L_29 = L_31 = 5, note.md 3.5)
  test        -- band FAIL or HOLD, outcome unknown at registration, run after registration
  mixed       -- band MIXED (the law makes no prediction)
  not run     -- no outcome in the logs
Outcomes: uniform rows from the scan logs (program A decides; a failing class is recomputed by
program C with an identical exact miss count; a hold needs A and C over all classes); depth-7
position rows from data/round3/R3C/p29_t7*/ (programs A and D; C where it was run).  A FAIL-band
position row ("fails at >= 1 of the n positions") counts as confirmed when one position fails with
the same exact miss count in at least two programs.
usage: python3 pred_eval.py   (run from the repository root)
"""
import glob
import re

ROOT = 'data/round3/R3C'
reg = open(f'{ROOT}/PREDICTIONS_registered.txt').read().splitlines()

# ---- outcomes of uniform Cov(p,t,H) from the scan logs
uni = {}
for fn in sorted(glob.glob(f'{ROOT}/scan*_p*.log')):
    for ln in open(fn):
        m = re.match(r'p=(\d+) t=(\d+) H=(\d+) .*?: (HOLDS|FAILS|A_HOLDS_C_DISAGREES)(.*)', ln.strip())
        if not m:
            continue
        p, t, H = map(int, m.groups()[:3])
        verdict, rest = m.group(4), m.group(5)
        if verdict == 'FAILS' and ('by counting' in rest or 'Lemma 10.11' in rest):
            how = 'FAIL (proved)'
        elif verdict == 'FAILS':
            mm = re.search(r'class K=(\d+): A missing=(\d+), C miss=(\d+) \[(\w+)\]', rest)
            how = f'FAIL (K\'={mm.group(1)}: A {mm.group(2)}, C {mm.group(3)} missed, {mm.group(4)})'
        elif verdict == 'HOLDS':
            how = 'HOLD (A and C, all classes)'
        else:
            how = 'A holds, C disagrees'
        uni[(p, t, H)] = (how, fn.split('/')[-1])

# ---- outcomes of depth-7 positions (programs A and D)
pos = {}
for fn in glob.glob(f'{ROOT}/p29_t7*/*.log'):
    for ln in open(fn):
        ln = ln.strip()
        m = re.match(r'(A|D) p=(\d+) t=(\d+) H=(\d+) .*? K=(\d+) .*?missing=(\d+) (COVERED|NOT_COVERED)', ln)
        mc = re.match(r'C p=(\d+) t=(\d+) H=(\d+) M=\d+ K=(\d+) Kmodpc=\d+ miss=(\d+) (COVERED|UNCOVERED)', ln)
        if m:
            prog, p, t, H, K, miss = m.group(1), *map(int, m.groups()[1:6])
            pos.setdefault((p, t, H), {}).setdefault(K, {})[prog] = miss
        elif mc:
            p, t, H, K, miss = map(int, mc.groups()[:5])
            pos.setdefault((p, t, H), {}).setdefault(K, {})['C'] = miss


def pos_outcome(p, t, H, n):
    d = pos.get((p, t, H))
    if not d:
        return None
    both = {K: v for K, v in d.items() if 'A' in v and 'D' in v}
    fails = {K: v for K, v in d.items() if any(x > 0 for x in v.values())}
    if len(both) == n and not fails:
        return f'HOLD at all {n} positions (A and D)'
    # a FAIL-band prediction says "fails at >= 1 position": confirmed by one position at which two
    # programs report the same nonzero exact miss count
    two = {K: v for K, v in fails.items() if len([x for x in v.values() if x > 0]) >= 2 and len(set(v.values())) == 1}
    if two:
        K, v = sorted(two.items())[0]
        return (f"FAIL at K''={K} ({', '.join(f'{x} {v[x]}' for x in sorted(v))} missed); "
                f"{len(d)} of {n} positions run")
    s = f'{len(d)} of {n} positions run'
    if fails:
        s += '; not covered: ' + ', '.join(f"K''={K} ({'/'.join(f'{x} {v[x]}' for x in sorted(v))} missed)" for K, v in sorted(fails.items()))
    else:
        s += ', all covered so far (programs: ' + ','.join(sorted({x for v in d.values() for x in v})) + ')'
    return s


KNOWN = {(29, 5, 29): 'HOLD (L_29=5)', (31, 5, 31): 'HOLD (L_31=5)', (29, 6, 29): 'FAIL (L_29=5)', (31, 6, 31): 'FAIL (L_31=5)'}
counts = {}
cur = None
print('# p t H | nu | band | outcome | class   (source log)')
for ln in reg:
    m = re.match(r'p=(\d+) t=(\d+) \[(uniform|positions n=(\d+))\] predicted minimal H .*= (\w+)', ln)
    if m:
        cur = (int(m.group(1)), int(m.group(2)), m.group(3), int(m.group(4)) if m.group(4) else None, m.group(5))
        continue
    m = re.match(r'\s+H=(\d+)(.*)', ln)
    m2 = re.match(r'extra: p=(\d+) t=(\d+) H=(\d+) n=(\d+) R\*=\S+ nu=([\d.]+) -> (\w+)', ln)
    if m2:
        p, t, H, n = map(int, m2.groups()[:4])
        nu, band = float(m2.group(5)), m2.group(6)
        mode = 'pos'
    elif m and cur:
        p, t, mode, n = cur[0], cur[1], cur[2], cur[3]
        H = int(m.group(1))
        if 'proved' in m.group(2):
            nu, band = None, 'proved-FAIL'
        else:
            mm = re.search(r'nu=([\d.]+) -> (\w+)', m.group(2))
            nu, band = float(mm.group(1)), mm.group(2)
        mode = 'pos' if mode.startswith('positions') else 'uni'
    else:
        continue
    if mode == 'uni':
        o = uni.get((p, t, H))
        out, src = (o if o else (None, ''))
    else:
        out = pos_outcome(p, t, H, n if n > 1 else p - 1)
        src = f'{ROOT}/p29_t7*' if out else ''
        if n == 1:
            # 'extra' rows with n = 1: the same block judged one position at a time (annotation only;
            # the registered prediction is the n = p-1 row above, so these rows are not counted)
            nus = f'{nu:.3f}'
            print(f"{p} {t} {H} pos (n=1 annotation) | {nus} | {band} | {out} | not counted   ({src})")
            continue
    if band == 'proved-FAIL':
        cls = 'proved (not a test)'
    elif t == 1:
        cls = 'known (Lemma 10.11)'
    elif (p, t, H) in KNOWN:
        cls = 'known (' + KNOWN[(p, t, H)] + ')'
    elif band.startswith('MIXED'):
        cls = 'mixed (no prediction)'
    elif out is None:
        cls = 'NOT RUN'
    else:
        pred = band.split()[0]
        obs = 'HOLD' if out.startswith('HOLD') else ('FAIL' if out.startswith('FAIL') else 'partial')
        if obs == 'partial':
            cls = 'test, incomplete'
        else:
            cls = 'test: ' + ('CONFIRMED' if pred == obs else 'FALSIFIED')
    counts[cls] = counts.get(cls, 0) + 1
    nus = f'{nu:.3f}' if nu is not None else '-'
    print(f"{p} {t} {H}{' pos' if mode == 'pos' else ''} | {nus} | {band} | {out} | {cls}   ({src})")
print('# summary:', '; '.join(f'{k}: {v}' for k, v in sorted(counts.items())))
