#!/usr/bin/env python3
"""results_table.py (2026-10-20) -- tabulate every depth-8 (p=19) position log and the depth-7 class logs in logs/:
program, K, outcome, misses, per-position wall time, max RSS, start/end timestamps, and whether the log is complete (# END line)."""
import glob, os, re
W=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def parse(fn):
    d=dict(name=os.path.basename(fn)[:-4], start=None, end=None, exit=None, rss=None, rows=[], complete=False, wall=None)
    for line in open(fn, errors='replace'):
        m=re.match(r"# START (\S+ \S+ \S+)",line)
        if m: d['start']=m.group(1)
        m=re.match(r"# END (\S+ \S+ \S+) unix=\d+ exit=(\d+)",line)
        if m: d['end']=m.group(1); d['exit']=int(m.group(2)); d['complete']=True
        m=re.search(r"(\d+)\s+maximum resident set size",line)
        if m: d['rss']=int(m.group(1))/2**30
        m=re.match(r"\s*([\d.]+) real",line)
        if m: d['wall']=float(m.group(1))
        m=re.match(r"A p=(\d+) t=(\d+) H=(\d+) c=\d+ M=\d+ K=(\d+) missing=(\d+) (\S+) \[([\d.]+)s\]",line)
        if m: d['rows'].append(('A',)+tuple(int(x) for x in m.groups()[:5])+(m.group(6),float(m.group(7))))
        m=re.match(r"C p=(\d+) t=(\d+) H=(\d+) M=\d+ K=(\d+) Kmodpc=\d+ miss=(\d+)(\S*) (\S+) ([\d.]+)s",line)
        if m: d['rows'].append(('C',)+tuple(int(x) for x in m.groups()[:5])+(m.group(7)+m.group(6),float(m.group(8))))
    return d
print("## depth-8 positions, p=19 (one log per (K,program))")
print("| log | prog | p,t,H | K'' | misses | outcome | wall (s) | max RSS (GB) | start | end | complete |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for fn in sorted(glob.glob(W+'/logs/P19_t8_*.log'), key=lambda f:(int(re.search(r'H(\d+)',f).group(1)), int(re.search(r'_K(\d+)_',f).group(1)), f)):
    d=parse(fn)
    if not d['rows']:
        print(f"| {d['name']} | | | | | (no result line) | | | {d['start']} | {d['end']} | {d['complete']} |"); continue
    for r in d['rows']:
        print(f"| {d['name']} | {r[0]}' | {r[1]},{r[2]},{r[3]} | {r[4]} | {r[5]} | {r[6]} | {r[7]:.0f} | {d['rss'] and round(d['rss'],2)} | {d['start']} | {d['end']} | {d['complete']} |")
print()
print("## depth-7 classes K'' mod 19^2 at H=45 (program A', chunks)")
print("| log | classes | covered | failed | total wall (s) | start | end | complete |")
print("|---|---|---|---|---|---|---|---|")
allK={}
for fn in sorted(glob.glob(W+'/logs/U19_t7_H45_A_chunk*.log'), key=lambda f:(int(re.search(r'chunk(\d+)',f).group(1)), f)):
    d=parse(fn)
    cov=[r[4] for r in d['rows'] if r[5]==0]; fail=[r[4] for r in d['rows'] if r[5]]
    for r in d['rows']:
        if 'INTERRUPTED' not in d['name']: allK[r[4]]=r[5]
    ks=sorted(r[4] for r in d['rows'])
    print(f"| {d['name']} | {len(ks)} ({ks[0] if ks else '-'}..{ks[-1] if ks else '-'}) | {len(cov)} | {len(fail)} {fail if fail else ''} | {d['wall'] and round(d['wall'])} | {d['start']} | {d['end']} | {d['complete']} |")
need=[K for K in range(19,361) if K%19]
print(f"\nclasses 19<K''<361 certified by A' (complete logs only): {sum(1 for K in need if K in allK and allK[K]==0)}/{len(need)}; failures: {[K for K in need if K in allK and allK[K]]}; missing: {[K for K in need if K not in allK][:20]}{'...' if sum(1 for K in need if K not in allK)>20 else ''}")
