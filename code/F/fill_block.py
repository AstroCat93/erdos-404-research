#!/usr/bin/env python3
"""Exact extension of a window check by one extra block in front.
Given holes H_in of COVER(A,B) (relative to p^{e(A)}, as residues mod p^{e(B)-e(A)}, listed as
'HOLE r=.. z=..' lines from wincheck2 with j1 = e(M)-e(A): value = r + p^{j1} z), and A0 < A,
decide COVER(A0,B) exactly: y (mod p^{e(B)-e(A0)}) is a hole iff for every subset T of [A0,A) with
sum_T == y (mod p^{e(A)-e(A0)}), (y - sum_T)/p^{e(A)-e(A0)} lies in H_in.
usage: fill_block.py p A0 A M B holesfile"""
import sys, re, itertools
p, A0, A, M, B = map(int, sys.argv[1:6]); hf = sys.argv[6]
def vp(n):
    v = 0
    while n % p == 0: n //= p; v += 1
    return v
V = {}
def e(N): return sum(vp(k) for k in range(1, N + 1))
eA0, eA, eM, eB = e(A0), e(A), e(M), e(B)
j1 = eM - eA; Din = eB - eA; d0 = eA - eA0; Dtot = eB - eA0
H = set()
txt = open(hf).read()
if 'whole cosets' in txt or 'INCONCLUSIVE' in txt or 'RESULT' not in txt:
    print('RESULT: INVALID (inner hole list incomplete)'); sys.exit(0)
for l in txt.splitlines():
    m = re.match(r'HOLE r=(\d+) z=(\d+)', l)
    if m: H.add((int(m.group(1)) + p ** j1 * int(m.group(2))) % p ** Din)
print(f"inner holes: {len(H)}  (d0={d0}, Din={Din})")
# unit part of A0! mod p^Dtot
mod = p ** Dtot
U = 1
for n in range(1, A0 + 1):
    m = n
    while m % p == 0: m //= p
    U = U * m % mod
els = []
cur = U
for n in range(A0, A):
    els.append(cur * p ** (e(n) - eA0) % mod)
    m = n + 1
    while m % p == 0: m //= p
    cur = cur * m % mod
sums = []
for k in range(len(els) + 1):
    for T in itertools.combinations(range(len(els)), k):
        sums.append(sum(els[i] for i in T) % mod)
cls = set(s % p ** d0 for s in sums)
print(f"block [{A0},{A}) subset sums hit {len(cls)} of {p**d0} classes mod p^{d0}")
holes = set()
for s0 in sums:
    for h in H:
        y = (s0 + p ** d0 * h) % mod
        if all(((y - s) % mod) // p ** d0 in H for s in sums if (y - s) % p ** d0 == 0):
            holes.add(y)
missing_classes = p ** d0 - len(cls)
print(f"holes of COVER({A0},{B}): {len(holes)} (+ whole cosets for {missing_classes} missed classes)")
print("RESULT:", "HOLDS" if not holes and missing_classes == 0 else "FAILS")
