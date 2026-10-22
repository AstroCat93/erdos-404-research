#!/usr/bin/env python3
"""rstar_in_gaps.py -- is R* (vectors/vec8_compact.txt), restricted to the primes in a third-party
list of unsettled case vectors, one of those vectors (up to a unit of Z/8)?

Usage:  python3 -I rstar_in_gaps.py RSTAR_FILE GAPS_FILE
GAPS_FILE: lines "UNSETTLED: q=v q=v ..." (the format of data/gaps_k8_P300_L1500000.txt in the
repository cited as [Ar] in paper/note.md).  Other lines are ignored.  The file is read as data only.
Standard library only.
"""
import sys

rstar = {}
for line in open(sys.argv[1]):
    t = line.split()
    if len(t) == 2 and not line.startswith('#'):
        rstar[int(t[0])] = int(t[1]) % 8
vecs = []
for line in open(sys.argv[2]):
    if line.startswith('UNSETTLED:'):
        vecs.append({int(a): int(b) % 8 for a, b in (tok.split('=') for tok in line.split()[1:])})
print(f"unsettled vectors in the file: {len(vecs)}; primes per vector: {sorted(set(len(v) for v in vecs))}")
hits = []
for i, v in enumerate(vecs, 1):
    for u in (1, 3, 5, 7):
        if all((u * rstar.get(q, 1)) % 8 == x for q, x in v.items()):
            hits.append((i, u))
print("R* restricted to these primes equals vector number (1-based), unit:", hits)
sys.exit(0 if hits else 1)
