"""b3check.py -- independent exact L^2 masses of tail measures (check of R3F B1/B3, round 3).
Shares no code with l2_dp.py (which counts modulo two 62-bit primes with CRT); here: exact int64 subset-sum
counts mod p^K (counts <= 2^n_K < 2^63), exact sums of squares via 21-bit limbs into Python ints.

Tail from N0: x_n = n!/p^{e0}, e0 = v_p(N0!), all n >= N0 with v_p(x_n) < K.  For every k <= K:
  L2(k) = p^k Coll_k / 4^{n_K} - 1   (counts folded mod p^k; elements of level >= k only double every count),
  Q(k) = L2(k) - L2(k-1),  ratio to the random model Q(k) / (N_k 2^{-n_k}).
usage: python3 -I b3check.py p N0 K
"""
import sys
import time
from fractions import Fraction
from math import factorial

import numpy as np


def vp_fact(n, p):
    s, q = 0, p
    while q <= n:
        s += n // q
        q *= p
    return s


def sumsq(c):
    """exact sum of squares of a nonnegative int64 array (entries < 2^63): three 21-bit limbs,
    limb products < 2^42 summed over chunks of 2^18 entries (< 2^60), accumulated in Python ints."""
    assert int(c.min()) >= 0
    L = [(c >> (21 * i)) & ((1 << 21) - 1) for i in range(3)]
    tot = 0
    for a in range(0, len(c), 1 << 18):
        Ls = [x[a:a + (1 << 18)] for x in L]
        for i in range(3):
            for j in range(3):
                tot += int((Ls[i] * Ls[j]).sum()) << (21 * (i + j))
    return tot


def main():
    p, N0, K = (int(a) for a in sys.argv[1:4])
    t0 = time.time()
    e0 = vp_fact(N0, p)
    mod = p ** K
    xs, lv = [], []
    n = N0
    while True:
        v = vp_fact(n, p) - e0
        if v >= K and n >= N0 + p:
            break
        if v < K:
            xs.append((factorial(n) // p ** e0) % mod)
            lv.append(v)
        n += 1
    nK = len(xs)
    assert nK <= 62
    c = np.zeros(mod, dtype=np.int64); c[0] = 1
    for x in xs:
        c = c + np.roll(c, x)
    prev = Fraction(0)
    print(f'# p={p} N0={N0} K={K} n_K={nK}')
    print('# k  n_k  L2(k)  Q(k)  Q(k)/(N_k 2^-n_k)')
    for k in range(1, K + 1):
        ck = c.reshape(-1, p ** k).sum(axis=0) if k < K else c
        L2 = Fraction(p ** k * sumsq(ck), 4 ** nK) - 1
        Q = L2 - prev
        nk = sum(1 for v in lv if v < k)
        rnd = Fraction(p ** k - p ** (k - 1), 2 ** nk)
        print(f'{k:3d} {nk:3d}  {float(L2):.6g}  {float(Q):.6g}  {float(Q / rnd):.4g}', flush=True)
        prev = L2
    print(f'# wall {time.time() - t0:.1f}s')


if __name__ == '__main__':
    main()
