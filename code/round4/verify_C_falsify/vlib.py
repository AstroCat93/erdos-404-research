"""Small exact library for the M4C falsification checks (independent code).

All probabilities are exact rationals: weighted counts (weights 2,1,1 for a lazy
signed digit 0,+1,-1; total 4 per random digit) are computed modulo several
31-bit primes with numpy int64 and reconstructed by CRT (only the entries that
are needed).
"""
import math
from fractions import Fraction
import numpy as np

PR = [2147483647, 2147483629, 2147483587, 2147483579, 2147483563, 2147483549,
      2147483543, 2147483497, 2147483489, 2147483477, 2147483423, 2147483399]


def vp(n, p):
    if n == 0:
        return 10 ** 9
    v = 0
    while n % p == 0:
        n //= p; v += 1
    return v


def pis(y, t):
    """[pi_c(y)] and [pi_c'(y)] for c = 0..t-1 (exact integers)."""
    P = [1]; D = [0]
    for c in range(1, t):
        D.append(D[-1] * (y + c) + P[-1])
        P.append(P[-1] * (y + c))
    return P, D


def nprimes_for(nrand):
    return (2 * nrand + 3) // 30 + 1


def _crt(vals, primes):
    x, M = 0, 1
    for v, P in zip(vals, primes):
        t = ((int(v) - x) * pow(M, -1, P)) % P
        x += M * t; M *= P
    return x, M


def prob_joint_zero(a, b, k, f, p, fixed0=False, laws=None):
    """P( sum delta_c a_c = 0 mod p^k  and  sum delta_c b_c = 0 mod p^f ).
    delta_c i.i.d. lazy signed, except delta_0 = 1 if fixed0. f may be 0."""
    mk, mf = p ** k, p ** max(f, 0)
    nrand = len(a) - (1 if fixed0 else 0)
    prs = PR[:nprimes_for(nrand)]
    res = []
    for P in prs:
        v = np.zeros((mk, mf), dtype=np.int64)
        start = 0
        if fixed0:
            v[a[0] % mk, b[0] % mf] = 1; start = 1
        else:
            v[0, 0] = 1
        for c in range(start, len(a)):
            sa, sb = a[c] % mk, b[c] % mf
            v = (2 * v + np.roll(v, (sa, sb), axis=(0, 1)) + np.roll(v, (-sa, -sb), axis=(0, 1))) % P
        res.append(v[0, 0])
    cnt, M = _crt(res, prs)
    assert cnt < M // 2
    return Fraction(cnt, 4 ** nrand)


def prob_zero(a, k, p, fixed0=False):
    return prob_joint_zero(a, [0] * len(a), k, 0, p, fixed0)


def block_max(vals, e, p, fixed_first=False):
    """max_a P(sum delta_c vals_c = a mod p^e), exact (small blocks only)."""
    m = p ** e
    v = np.zeros(m, dtype=object)
    start = 0
    if fixed_first:
        v[vals[0] % m] = 1; start = 1
    else:
        v[0] = 1
    for c in range(start, len(vals)):
        s = vals[c] % m
        v = 2 * v + np.roll(v, s) + np.roll(v, -s)
    nr = len(vals) - start
    return Fraction(int(max(v)), 4 ** nr)


def gate_data(y, t, p):
    """gates g in [1,t-1] with p | y+g, depths, levels, blocks (M4C §1)."""
    gates = [g for g in range(1, t) if (y + g) % p == 0]
    depths = [vp(y + g, p) for g in gates]
    levels = [0]
    for d in depths:
        levels.append(levels[-1] + d)
    bounds = [0] + gates + [t]
    blocks = [list(range(bounds[i], bounds[i + 1])) for i in range(len(gates) + 1)]
    return gates, depths, levels, blocks
