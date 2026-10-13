#!/usr/bin/env python3
"""Sanity checks for the 'environment walk' remarks in data/round3/reports/S0.md.

(1) Identity: for even a and n >= 0, with Kitamura's pair-gate convention
    (step 0: 2 options, e_0 = v2(a+2); step k >= 1: 4 options, e_k = v2(a+2k+2)),
        sum_{k<=n} (log2 #options_k - e_k) = s2(a+2n+2) - s2(a) - 1.
(2) Lemma S0.1: for Haar-random y in Z_2 and n >= 1,
        (m+2)/2^(m+2) <= P( s2(y+k) - s2(y) >= 0 for all 1<=k<=n ) <= (m+2)/2^(m+1),  m = floor(log2 n).
    Checked exactly by enumerating y mod 2^J; residues with y + n >= 2^J (a carry may leave the
    window) are counted separately, giving rigorous lower/upper bounds for the Haar probability.

Usage: python3 -I env_walk_check.py J NMAX
"""
import sys

import numpy as np


def v2(n):
    return (n & -n).bit_length() - 1


def s2(n):
    return bin(n).count("1")


def check_identity(amax=3000, nmax=400):
    bad = 0
    for a in range(2, amax, 2):
        S = 0
        for k in range(nmax):
            S += (1 if k == 0 else 2) - v2(a + 2 * k + 2)
            if S != s2(a + 2 * k + 2) - s2(a) - 1:
                bad += 1
    return bad


def popcount(arr):
    c = np.zeros_like(arr)
    x = arr.copy()
    while np.any(x):
        c += x & 1
        x >>= 1
    return c


def main():
    J, NMAX = int(sys.argv[1]), int(sys.argv[2])
    print(f"identity mismatches (even a < 3000, n < 400): {check_identity()}")
    y = np.arange(1 << J, dtype=np.int64)
    sy = popcount(y)
    alive = np.ones(1 << J, dtype=bool)
    n = 0
    for target in [2 ** i for i in range(0, 64) if 2 ** i <= NMAX] + ([NMAX] if NMAX & (NMAX - 1) else []):
        while n < target:
            n += 1
            alive &= popcount(y + n) >= sy
        inside = y + n < (1 << J)
        lo = np.count_nonzero(alive & inside) / (1 << J)
        hi = (np.count_nonzero(alive & inside) + np.count_nonzero(~inside)) / (1 << J)
        m = n.bit_length() - 1
        print(f"n={n:6d} m={m:2d}  P in [{lo:.6f}, {hi:.6f}]   lemma bounds [{(m + 2) / 2 ** (m + 2):.6f}, {(m + 2) / 2 ** (m + 1):.6f}]"
              f"   ok={(m + 2) / 2 ** (m + 2) <= hi and lo <= (m + 2) / 2 ** (m + 1)}")


if __name__ == "__main__":
    main()
