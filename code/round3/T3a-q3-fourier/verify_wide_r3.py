#!/usr/bin/env python3
"""verify_wide_r3.py -- independent check of the 'wide' (M > 64) code path of l2dp.c (round 3, this instance).
For (p, N0, k) with more than 64 elements, recompute S = sum_r N(r)^2 modulo 2^64 (uint64 wrap-around counts) and modulo
the prime P1 = 2^31 - 1 (int64 counts reduced mod P1), with numpy roll-add, and compare with S reconstructed (CRT) from the
l2dp output file.  Agreement mod 2^64 * P1 (~2^95) is a strong check of the exact value.
Usage: python3 verify_wide_r3.py p N0 k"""
import sys, os
from math import factorial
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_l2_r3 import vfact, file_C
from fractions import Fraction
P1 = 2**31 - 1
def main():
    p, N0, k = map(int, sys.argv[1:4])
    e0 = vfact(N0, p); mod = p**k
    els = []; n = N0
    while vfact(n, p) - e0 < k:
        els.append((factorial(n) // p**e0) % mod); n += 1
    M = len(els)
    A = np.zeros(mod, dtype=np.uint64); A[0] = 1
    B = np.zeros(mod, dtype=np.int64); B[0] = 1
    for a in els:
        A = A + np.roll(A, a)            # wraps mod 2^64
        B = (B + np.roll(B, a)) % P1
    S64 = int(np.sum(A * A, dtype=np.uint64))          # wraps mod 2^64
    SP = 0
    for chunk in np.array_split(B, 64):
        SP = (SP + int(np.sum((chunk * chunk) % P1))) % P1
    C, fn = file_C(p, N0, k)
    S_file = C * 4**M / p**k
    assert S_file.denominator == 1
    S_file = S_file.numerator
    ok = (S_file % 2**64 == S64) and (S_file % P1 == SP)
    print("p=%d N0=%d k=%d M=%d  file %s: S mod 2^64 %s, S mod (2^31-1) %s  -> %s" % (
        p, N0, k, M, fn, S_file % 2**64 == S64, S_file % P1 == SP, "AGREE" if ok else "MISMATCH"), flush=True)
if __name__ == '__main__':
    main()
