"""Aggregate the check tables of the logs in data/round4/verify_D_W6_falsify (t_cyl and t_chain runs).

usage: python3 aggregate.py LOGDIR
Only completed runs (those followed by '# exit 0') are counted.
"""
import sys, os, re, glob
from collections import defaultdict

logdir = sys.argv[1]
tot = defaultdict(lambda: [0, 0])
per_p = defaultdict(lambda: defaultdict(lambda: [0, 0]))
maxr = defaultdict(float)
eqs = defaultdict(int)
ncyl = defaultdict(int)
for f in sorted(glob.glob(os.path.join(logdir, '*.log'))):
    txt = open(f).read()
    runs = txt.split('================================================================')
    for r in runs:
        if '# exit 0' not in r:
            continue
        m = re.search(r'^p=(\d+)', r, re.M)
        if not m:
            continue
        p = int(m.group(1))
        kind = 'chain' if 't_chain.py' in r else ('adv' if 't_adv.py' in r else 'cyl')
        mc = re.search(r'^cylinders: (\d+)', r, re.M)
        if mc:
            ncyl[(kind, p)] += int(mc.group(1))
        ma = re.search(r'^atoms: (\d+)', r, re.M)
        if ma:
            ncyl[(kind, p)] += int(ma.group(1))
        for line in r.splitlines():
            mm = re.match(r'^\s+(.*): checks (\d+) failures (\d+)$', line)
            if mm:
                name = mm.group(1)
                key = (kind, name)
                tot[key][0] += int(mm.group(2))
                tot[key][1] += int(mm.group(3))
                per_p[key][p][0] += int(mm.group(2))
                per_p[key][p][1] += int(mm.group(3))
            mr = re.match(r'^\s+(W[^:]*LHS/RHS[^:]*|W2 Var/bound): ([0-9.e+-]+)', line)
            if mr:
                maxr[(kind, mr.group(1), p)] = max(maxr[(kind, mr.group(1), p)], float(mr.group(2)))
            me = re.match(r'^exact equalities: (\{.*\})$', line)
            if me:
                d = eval(me.group(1))
                for k, v in d.items():
                    eqs[(k, p)] += v
print("units (cylinders / atoms) per (kind, p):", dict(ncyl))
for kind in ('cyl', 'chain'):
    print(f"\n== {kind}: name | total checks | failures | per p (checks/failures)")
    for key in sorted(k for k in tot if k[0] == kind):
        c, fl = tot[key]
        pp = ' '.join(f"p{p}:{v[0]}/{v[1]}" for p, v in sorted(per_p[key].items()))
        print(f"  {key[1]} | {c} | {fl} | {pp}")
print("\nmax ratios:")
for k, v in sorted(maxr.items()):
    print("  ", k, v)
print("\nexact equalities:")
for k, v in sorted(eqs.items()):
    print("  ", k, v)
