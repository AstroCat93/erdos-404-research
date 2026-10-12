#!/usr/bin/env python3
"""Spot-check of the Fourier shell sums T_p(k) of §10.4.1 for small k (numpy float64, exact residues)."""
import math, numpy as np

def vf(n, p):
    s = 0
    while n:
        n //= p; s += n
    return s

def T(p, k):
    M = p ** k
    # elements n >= p with v(n!) - 1 < k
    xs = []
    n = p
    while vf(n, p) - 1 < k:
        xs.append((math.factorial(n) // p) % M)
        n += 1
    u = np.array([w for w in range(1, M) if w % p], dtype=np.int64)
    prod = np.ones(len(u))
    for x in xs:
        r = (u * x) % M
        prod *= np.abs(np.cos(np.pi * r / M))
    return prod.sum(), len(xs)

for p, kmax in [(13, 4), (11, 5)]:
    tot = 0
    for k in range(1, kmax + 1):
        t, ne = T(p, k)
        tot += t
        print(f"T_{p}({k}) = {t:.6e}  (elements {ne})  running sum {tot:.7e}")
