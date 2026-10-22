#!/usr/bin/env python3
"""verify_l2_r3.py -- independent re-check (round 3, 2026-10-21, this instance) of the exact L^2 masses
C_k(p,N0) = p^k * P( sum_n eta_n x_n == 0 mod p^k ),  x_n = n!/p^{v(N0!)}, n >= N0, eta iid {-1,0,1} w.p. 1/4,1/2,1/4,
against the files data/l2/p*_E*_N*.txt written by l2dp.c (previous instance).

Method here (independent code path):
  (a) subset-sum counts N(r) = #{B subset of {n: v(x_n) < k} : sum_B x_n == r mod p^k} by numpy roll-add on int64
      (exact while #elements <= 62), then S = sum_r N(r)^2 in Python integers and C_k = p^k S / 4^M (exact Fraction).
      Uses sum_r N(r)^2 = #{(B,B'): sums equal} = 4^M P(eta-sum == 0).
  (b) for p^k <= 2e5 also the Fourier formula C_k = sum_{xi mod p^k} prod_n cos^2(pi xi x_n / p^k) in float64.
Usage: python3 -I verify_l2_r3.py   (runs the built-in list of cases; prints one line per case)
"""
import sys, os, re
from fractions import Fraction
from math import factorial
import numpy as np

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
Q = 2**61 - 1

def vfact(n, p):
    v, m = 0, n
    while m:
        m //= p; v += m
    return v

def file_C(p, N0, k):
    """C_k from the l2dp output files (any E >= k + e0), via CRT of (S mod 2^128, S mod q)."""
    e0 = vfact(N0, p)
    for fn in sorted(os.listdir(os.path.join(BASE, 'data', 'l2'))):
        m = re.match(r'p(\d+)_E(\d+)_N(\d+)\.txt$', fn)
        if not m or int(m.group(1)) != p or int(m.group(3)) != N0: continue
        M = None
        for line in open(os.path.join(BASE, 'data', 'l2', fn)):
            if line.startswith('# p='):
                M = int(dict(kv.split('=') for kv in line[2:].split())['M'])
            elif not line.startswith('#') and line.strip():
                f = line.split()
                if int(f[0]) == k + e0:
                    a = (int(f[2]) << 64) | int(f[3])
                    t = ((int(f[4]) - a) % Q) * pow(2**128 % Q, -1, Q) % Q
                    S = a + 2**128 * t
                    return Fraction(p**k * S, 4**M), fn
    return None, None

def direct_C(p, N0, k):
    e0 = vfact(N0, p); mod = p**k
    els = []
    n = N0
    while vfact(n, p) - e0 < k:
        els.append((factorial(n) // p**e0) % mod); n += 1
    M = len(els)
    if M > 62: return None, M
    A = np.zeros(mod, dtype=np.int64); A[0] = 1
    for a in els:
        A = A + np.roll(A, a)
    S = sum(int(x) * int(x) for x in A.tolist())
    return Fraction(mod * S, 4**M), M

def fourier_C(p, N0, k):
    e0 = vfact(N0, p); mod = p**k
    els = []; n = N0
    while vfact(n, p) - e0 < k:
        els.append((factorial(n) // p**e0) % mod); n += 1
    xi = np.arange(mod, dtype=np.float64)
    prod = np.ones(mod)
    for a in els:
        prod *= np.cos(np.pi * ((xi * a) % mod) / mod) ** 2
    return float(prod.sum())

def main():
    cases = []
    for p, N0, kmax in [(2, 1, 21), (2, 2, 20), (3, 1, 13), (3, 3, 12), (5, 1, 8), (5, 5, 7), (7, 1, 7), (7, 7, 6),
                        (11, 1, 5), (11, 11, 4), (13, 1, 5), (13, 13, 4)]:
        for k in range(1, kmax + 1):
            cases.append((p, N0, k))
    bad = 0; n = 0
    for p, N0, k in cases:
        if p**k > 4_000_000: continue
        Cd, M = direct_C(p, N0, k)
        Cf, fn = file_C(p, N0, k)
        if Cd is None or Cf is None: continue
        n += 1
        ok = (Cd == Cf)
        extra = ''
        if p**k <= 200_000:
            fc = fourier_C(p, N0, k)
            extra = ' fourier=%.12f |diff|=%.1e' % (fc, abs(fc - float(Cd)))
        if not ok: bad += 1
        print('p=%d N0=%d k=%d M=%d C=%.12f file(%s) equal=%s%s' % (p, N0, k, M, float(Cd), fn, ok, extra), flush=True)
    print('cases checked: %d, mismatches: %d' % (n, bad))

if __name__ == '__main__':
    main()
