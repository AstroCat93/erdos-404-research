#!/usr/bin/env python3
"""contradictions.py -- check of track R3C: the chain checkers accept a certificate if ANY log line
reports it covered and ignore lines that report the same (program, p, t, H, K) NOT covered.  This
script lists every (program, p, t, H, K) that has both kinds of line in data/round3/R3C (all
subdirectories), and every (p, t, H, K) on which two programs report different miss counts.
usage: python3 contradictions.py   (from the repository root)"""
import glob
import re
from collections import defaultdict
PAT = [('A', re.compile(r'^A p=(\d+) t=(\d+) H=(\d+) c=\d+ M=\d+ K=(\d+) missing=(\d+) ')),
       ('C', re.compile(r'^C p=(\d+) t=(\d+) H=(\d+) M=\d+ K=(\d+) Kmodpc=\d+ miss=(\d+)(?:\S*) ')),
       ('D', re.compile(r'^D p=(\d+) t=(\d+) H=(\d+) c=\d+ M=\d+ k=\d+ K=(\d+) Kmodpc=\d+ missing=(\d+) '))]
seen = defaultdict(set)
files = defaultdict(set)
n = 0
for fn in glob.glob('data/round3/R3C/**/*.log', recursive=True):
    for ln in open(fn, errors='replace'):
        s = ln.strip()
        for prog, rx in PAT:
            m = rx.match(s)
            if m:
                p, t, H, K, miss = map(int, m.groups())
                seen[(prog, p, t, H, K)].add(miss)
                files[(prog, p, t, H, K)].add(fn)
                n += 1
print(f'{n} result lines parsed, {len(seen)} distinct (program, p, t, H, K)')
bad = [(k, v) for k, v in seen.items() if len(v) > 1]
print(f'(program, p, t, H, K) with more than one miss count: {len(bad)}')
for k, v in bad:
    print('  ', k, sorted(v), sorted(files[k]))
byKey = defaultdict(dict)
for (prog, p, t, H, K), v in seen.items():
    byKey[(p, t, H, K)][prog] = v
dis = [(k, d) for k, d in byKey.items() if len(d) > 1 and len({frozenset(x) for x in d.values()}) > 1]
print(f'(p, t, H, K) run by >= 2 programs: {sum(1 for d in byKey.values() if len(d) > 1)}; with different counts: {len(dis)}')
for k, d in dis:
    print('  ', k, d)
