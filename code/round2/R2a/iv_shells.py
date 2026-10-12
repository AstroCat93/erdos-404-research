#!/usr/bin/env python3
"""iv_shells.py -- rigorous (interval-arithmetic) upper bounds for the first Fourier shell sums
T_p(k) = sum_{u unit mod p^k} prod_{n>=N0} |cos(pi u n!/(p^{e0} p^k))|   (note_v2.md Section 10.4),
using mpmath.iv (outward-rounded interval arithmetic).  Lead author's check, 2026-10-12.

Each factor |cos(pi r/p^k)| with r = u*x_n mod p^k is enclosed by an interval; the product and the
sum are interval operations, and we report the upper endpoint.  Symmetry u <-> -u is used (the
factor depends on min(r, p^k - r)), so only u with first digit in [1, (p-1)/2] are enumerated and
the result is doubled (an exact operation).
usage: iv_shells.py p N0 kmax
"""
import sys
from mpmath import iv, mpf

iv.prec = 80


def main():
    p, N0, kmax = (int(a) for a in sys.argv[1:4])
    BIG = p ** kmax
    # x_n = n!/p^{e0} mod p^kmax with level l_n = v(n!) - e0 < kmax
    fact = 1
    for k in range(1, N0 + 1):
        fact *= k
    e0 = 0
    f = fact
    while f % p == 0:
        f //= p
        e0 += 1
    xs = []
    n = N0
    cur = fact
    while True:
        v = 0
        c = cur
        while c % p == 0:
            c //= p
            v += 1
        lev = v - e0
        if lev >= kmax:
            break
        xs.append(((cur // p ** e0) % BIG, lev))
        n += 1
        cur *= n
    cache = {}
    cum = iv.mpf(0)
    for k in range(1, kmax + 1):
        M = p ** k
        els = [x % M for (x, l) in xs if l < k]
        tot = iv.mpf(0)
        half = (p - 1) // 2
        for u in range(1, M):
            if u % p == 0 or u % p > half:
                continue
            prod = iv.mpf(1)
            for x in els:
                r = (u * x) % M
                r = min(r, M - r)
                key = (r, M)
                fac = cache.get(key)
                if fac is None:
                    fac = abs(iv.cos(iv.pi * iv.mpf(r) / M))
                    cache[key] = fac
                prod = prod * fac
            tot = tot + prod
        tot = 2 * tot
        cum = cum + tot
        print(f"k={k} T in [{float(tot.a):.10e}, {float(tot.b):.10e}]  cum_upper={float(cum.b):.10e}", flush=True)


if __name__ == "__main__":
    main()
