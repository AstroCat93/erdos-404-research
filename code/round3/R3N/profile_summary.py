#!/usr/bin/env python3
"""Summarise a dfsWp population profile (alive paths at window boundaries M_j).
Usage: python3 -I profile_summary.py PROFILE a
Prints: the overall maximum, the boundary populations just below and just above each power
of two, and the mean-field prediction 2^{s(M)-s(a)-1} (binary digit sums) for comparison.
"""
import sys

path, a = sys.argv[1], int(sys.argv[2])
rows = []
for line in open(path):
    if line.startswith('#'):
        continue
    j, M, lo, c = line.split()
    rows.append((int(j), int(M), int(lo), int(c)))
s = lambda n: bin(n).count('1')
mx = max(rows, key=lambda r: r[3])
print(f"levels={len(rows)} last boundary M={rows[-1][1]} pop={rows[-1][3]}")
print(f"max population {mx[3]} at M={mx[1]}")
print("power-of-two crossings (last boundary below 2^k, first above):")
k = 10
while (1 << k) <= rows[-1][1]:
    P = 1 << k
    below = [r for r in rows if r[1] < P]
    above = [r for r in rows if r[1] >= P]
    if below and above:
        b, u = below[-1], above[0]
        print(f"  2^{k}={P}: M={b[1]} pop={b[3]} (mean-field {2.0**(s(b[1])-s(a)-1):.3g})  ->  M={u[1]} pop={u[3]} (mean-field {2.0**(s(u[1])-s(a)-1):.3g})")
    k += 1
print("tail (last 12 boundaries):")
for r in rows[-12:]:
    print(f"  j={r[0]} M={r[1]} v2(M!)={r[2]} pop={r[3]}")
tot = sum(r[3] for r in rows)
print(f"sum of boundary populations = {tot}")
