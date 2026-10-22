#!/usr/bin/env python3
"""check_vector.py -- least n with f_R(n) = f_R(n+1) = 0 (mod k) for a full assignment R.

Usage:  python3 -I check_vector.py k LMAX VECTORFILE [DEFAULT]

VECTORFILE has lines "q v" (q prime, v an integer, read mod k).  Primes absent from the
file get DEFAULT (mod k); without DEFAULT every prime <= LMAX+1 must be in the file.
Prints the least n <= LMAX with f(n) = f(n+1) = 0, or reports that none exists.
f is computed by the recursion f(m) = f(m / spf(m)) + R(spf(m)) over a smallest-prime-
factor table.  Standard library only.
"""
import sys
from math import isqrt


def main():
    k, LMAX = int(sys.argv[1]), int(sys.argv[2])
    default = int(sys.argv[4]) % k if len(sys.argv) > 4 else None
    N = LMAX + 1
    R = {}
    with open(sys.argv[3]) as fh:
        for line in fh:
            t = line.split()
            if len(t) == 2:
                q, v = int(t[0]), int(t[1])
                if q in R:
                    sys.exit(f"duplicate prime {q}")
                R[q] = v % k
    spf = list(range(N + 1))
    for i in range(2, isqrt(N) + 1):
        if spf[i] == i:
            for j in range(i * i, N + 1, i):
                if spf[j] == j:
                    spf[j] = i
    for q in R:
        if q < 2 or q > N or spf[q] != q:
            if q <= N:
                sys.exit(f"{q} in the vector file is not a prime")
    missing = [p for p in range(2, N + 1) if spf[p] == p and p not in R]
    if missing and default is None:
        sys.exit(f"{len(missing)} primes <= {N} missing from the vector (first {missing[0]}) and no DEFAULT given")
    f = bytearray(N + 1)
    for m in range(2, N + 1):
        p = spf[m]
        f[m] = (f[m // p] + R.get(p, default)) % k
    for n in range(1, LMAX + 1):
        if f[n] == 0 and f[n + 1] == 0:
            print(f"k={k} R(2)={R.get(2, default)} vector primes={len(R)} default={default}: least zero pair n = {n} (<= {LMAX})")
            return
    print(f"k={k} R(2)={R.get(2, default)} vector primes={len(R)} default={default}: no zero pair with n <= {LMAX}")


if __name__ == '__main__':
    main()
