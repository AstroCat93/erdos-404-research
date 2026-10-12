#!/usr/bin/env python3
"""Brute-force reference for covchk: numpy boolean subset-sum DP over Z/p^M using ACTUAL factorial
ratios n!/(N*-H)! (computed with Python big integers from math.factorial for small N*), and compares
the number of uncovered residues with covchk for several fibre depths k."""
import math, subprocess, sys, random, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
def vp(n, p):
    s = 0
    while n % p == 0 and n:
        n //= p; s += 1
    return s
def leg(n, p):
    s = 0
    while n:
        n //= p; s += n
    return s

def brute(p, t, H, K):
    c = leg(H - 1, p); M = t + c; Q = p ** M
    Ns = p ** t * K
    ys = []; acc = 1
    for i in range(H):
        if i: acc *= (Ns - H + i)
        ys.append(acc % Q)
    S = np.zeros(Q, dtype=bool); S[0] = True
    for y in ys:
        S = S | np.roll(S, y)
    return int(Q - S.sum()), M

def prog(p, t, H, k, Ks):
    out = subprocess.run([os.path.join(HERE, 'covchk'), str(p), str(t), str(H), str(k), 'pos'] + [str(K) for K in Ks],
                         capture_output=True, text=True).stdout
    res = {}
    for ln in out.splitlines():
        if ln.startswith('C '):
            f = dict(x.split('=') for x in ln.split() if '=' in x)
            res[int(f['K'])] = int(f['miss'])
    return res

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
cases = []
for p in (3, 5, 7, 11, 13):
    for t in (1, 2, 3, 4):
        for H in range(2, min(p ** t, 60) + 1):
            c = leg(H - 1, p); M = t + c
            if p ** M > 3_000_000 or p ** M < 5:
                continue
            cases.append((p, t, H))
random.shuffle(cases)
cases = cases[:int(sys.argv[2]) if len(sys.argv) > 2 else 120]
ncmp = nfail = nmis = 0
for (p, t, H) in cases:
    c = leg(H - 1, p); M = t + c
    Ks = [K for K in random.sample(range(1, 40), 6) if K % p]
    ref = {K: brute(p, t, H, K)[0] for K in Ks}
    for k in range(0, M + 1):
        nlo = sum(1 for i in range(H) if leg(H - 1, p) - leg(H - 1 - i, p) < k)
        if nlo > 26: continue
        got = prog(p, t, H, k, Ks)
        for K in Ks:
            ncmp += 1
            if ref[K]: nfail += 1
            if got.get(K) != ref[K]:
                nmis += 1
                print('MISMATCH', p, t, H, k, K, ref[K], got.get(K))
print(f'comparisons={ncmp} failing_cases={nfail} mismatches={nmis}')
