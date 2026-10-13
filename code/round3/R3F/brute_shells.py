#!/usr/bin/env python3
"""brute_shells.py -- brute-force reference (mpmath, 40 digits) for the L^1 and L^2 shell sums
T1(k), T2(k) of the factorial tail measure from N0 (validation of ivshell.c and shells_mpfr.py).
usage: brute_shells.py p N0 kmax"""
import sys, math
from mpmath import mp, mpf, cos, pi
mp.dps = 40
p, N0, kmax = map(int, sys.argv[1:4])
def vp(n):
    c = 0
    while n % p == 0: n //= p; c += 1
    return c
f = math.factorial(N0); e0 = vp(f); xs = []; n = N0
while vp(f) - e0 < kmax:
    xs.append((f // p**e0, vp(f) - e0)); n += 1; f *= n
for k in range(1, kmax + 1):
    M = p**k; T1 = mpf(0); T2 = mpf(0)
    els = [x % M for (x, l) in xs if l < k]
    for u in range(1, M):
        if u % p == 0: continue
        pr = mpf(1)
        for x in els: pr *= abs(cos(pi * ((u * x) % M) / M))
        T1 += pr; T2 += pr * pr
    print(f"p={p} N0={N0} k={k} T1={mp.nstr(T1, 20)} T2={mp.nstr(T2, 20)}")
