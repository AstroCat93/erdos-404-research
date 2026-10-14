#!/usr/bin/env python3
"""vcl_q.py -- independent exact computation of the block constants of the M4C report (section 4.1),
written by the verify_C_logic track from the report's definitions only (no code shared with code/round4/M4C/).

Lazy signed digits: delta in {0,+1,-1} with weights 2,1,1 (out of 4).
  q1(p) = p   * max_a P( sum_r delta_r r!            = a  mod p   )
  q2(p) = p^2 * max_{a,b} P( A = a mod p, floor(A/p) - B = b mod p ),  A = sum delta_r r!, B = sum delta_r r! H_r mod p
        computed here through the bijection (a0, a1 - B) <-> A - pB mod p^2, i.e. as
        p^2 * max_c P( sum_r delta_r (r! - p * r!H_r) = c mod p^2 )   [r!H_r = |s(r+1,2)| is an integer]
        and, for p <= 31, ALSO directly from the 2D definition (cross-check of the bijection).
  q3(p) = p^3 * max_a P( sum_r delta_r F_r = a mod p^3 ),  F_r = prod_{s=1}^r (s - p).
All counts are exact Python integers (numpy object arrays); results are exact Fractions.
usage: vcl_q.py p1 p2 ...
"""
import sys
import time
from fractions import Fraction
from math import factorial

import numpy as np


def lazy_dp(elems, mod):
    dist = np.zeros(mod, dtype=object)
    dist[:] = 0
    dist[0] = 1
    for a in elems:
        a %= mod
        dist = 2 * dist + np.roll(dist, a) + np.roll(dist, -a)
    return dist


def rfHr(r):
    """r! * H_r as an exact integer (sum_{i=1}^r r!/i)."""
    f = factorial(r)
    return sum(f // i for i in range(1, r + 1))


def q1(p):
    d = lazy_dp([factorial(r) for r in range(p)], p)
    return Fraction(p * int(max(d)), 4 ** p)


def q2(p):
    m = p * p
    d = lazy_dp([factorial(r) - p * rfHr(r) for r in range(p)], m)
    return Fraction(m * int(max(d)), 4 ** p)


def q2_direct(p):
    """2D DP over (A mod p^2, B mod p), then fold to (A mod p, floor(A/p) - B mod p)."""
    m = p * p
    dist = np.zeros((m, p), dtype=object)
    dist[:, :] = 0
    dist[0, 0] = 1
    for r in range(p):
        a = factorial(r) % m
        b = rfHr(r) % p
        dist = 2 * dist + np.roll(np.roll(dist, a, axis=0), b, axis=1) + np.roll(np.roll(dist, -a, axis=0), -b, axis=1)
    fold = {}
    for A in range(m):
        for B in range(p):
            c = dist[A, B]
            if c:
                key = (A % p, (A // p - B) % p)
                fold[key] = fold.get(key, 0) + c
    return Fraction(m * max(fold.values()), 4 ** p)


def q3(p):
    m = p ** 3
    F = []
    f = 1
    for r in range(p):
        if r > 0:
            f *= (r - p)
        F.append(f)
    d = lazy_dp(F, m)
    return Fraction(m * int(max(d)), 4 ** p)


def fmt(q):
    # print q-1 to 6 significant digits from the exact rational
    x = q - 1
    if x == 0:
        return "0"
    from mpmath import mp, mpf
    mp.dps = 30
    return mp.nstr(mpf(x.numerator) / x.denominator, 6)


if __name__ == "__main__":
    for p in [int(t) for t in sys.argv[1:]]:
        t0 = time.time()
        a, b, c = q1(p), q2(p), q3(p)
        extra = ""
        if p <= 31:
            b2 = q2_direct(p)
            extra = f" q2_direct==q2: {b2 == b}"
        print(f"p={p} q1-1={fmt(a)} q2-1={fmt(b)} q3-1={fmt(c)}{extra}  "
              f"[exact: q1={a.numerator}/{a.denominator.bit_length()-1}bits q2num={b.numerator} q3num={c.numerator}] "
              f"({time.time()-t0:.1f}s)", flush=True)
