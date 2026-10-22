#!/usr/bin/env python3
"""Independent recomputation of q1(p), q2(p), q3(p) of M4C report section 4.1.

Definitions used (read from the report text only):
  delta_r i.i.d. lazy signed (0 w.p. 1/2, +-1 w.p. 1/4), r = 0..p-1.
  A = sum delta_r r!   (integers r!)
  B = sum delta_r r! H_r  mod p   (r! H_r is an integer: |s(r+1,2)|)
  F_r = prod_{s=1}^r (s - p)
  q1 = p   max_a  P(A = a mod p)
  q2 = p^2 max_{a,b} P(A = a mod p, floor(A/p) - B = b mod p)
  q3 = p^3 max_a  P(sum delta_r F_r = a mod p^3)

Method 1 (exact): weighted count DP (weights 2,1,1; total 4^p), modulo several
  word-size primes, CRT; we compute the FULL count vector and its maximum.
  For q2 the state is the residue of A - p*B mod p^2, which encodes the pair
  (A mod p, floor(A/p) - B mod p) bijectively (digit 0 and digit 1).
Method 2 (independent, floating): Fourier/Parseval
  q = sum_xi prod_r cos^2(pi xi c_r / m)  (valid for the value at residue 0;
  the max is at 0 because the law is an autocorrelation) -> gives q - 1 as a
  sum of nonnegative terms, accurate in relative terms.
Method 3 (p <= 13): brute force over all 3^p signed vectors with exact integer
  A and Python floor division (checks the reading of floor(A/p) for negative A).
"""
import sys, math, time
from fractions import Fraction
import numpy as np

PRIMES = [2147483647, 2147483629, 2147483587, 2147483579, 2147483563,
          2147483549, 2147483543, 2147483497, 2147483489, 2147483477]


def harmonic_int(r, p):
    """r! H_r as an exact integer."""
    f = math.factorial(r)
    return sum(f // s for s in range(1, r + 1))


def coeffs(p, which):
    if which == 1:
        m = p
        c = [math.factorial(r) % m for r in range(p)]
    elif which == 2:
        m = p * p
        c = [(math.factorial(r) - p * (harmonic_int(r, p) % p)) % m for r in range(p)]
    elif which == 3:
        m = p ** 3
        c = []
        for r in range(p):
            F = 1
            for s in range(1, r + 1):
                F *= (s - p)
            c.append(F % m)
    return m, c


def count_dp_mod(m, c, P):
    v = np.zeros(m, dtype=np.int64)
    v[0] = 1
    for a in c:
        a = int(a) % m
        v = (2 * v + np.roll(v, a) + np.roll(v, -a)) % P
    return v


def crt_pair(r1, m1, r2, m2):
    # combine x = r1 mod m1, x = r2 mod m2
    t = ((r2 - r1) * pow(m1, -1, m2)) % m2
    return r1 + m1 * t, m1 * m2


def exact_counts_max(m, c, nprimes):
    """Return (count at 0, max count, argmax residues list) exactly via CRT.
    max is found by: the residues with maximal value are the same under every
    prime only if values are reconstructed; we reconstruct the full vector with
    object arithmetic (vectorised CRT)."""
    vecs = [count_dp_mod(m, c, P) for P in PRIMES[:nprimes]]
    # vectorised CRT with python ints via object arrays
    R = vecs[0].astype(object)
    M = PRIMES[0]
    for v, P in zip(vecs[1:], PRIMES[1:nprimes]):
        inv = pow(M, -1, P)
        t = ((v.astype(object) - R) * inv) % P
        R = R + M * t
        M *= P
    return R, M


def q_exact(p, which):
    m, c = coeffs(p, which)
    total = 4 ** len(c)
    nbits = 2 * len(c) + 2
    nprimes = nbits // 30 + 2  # one spare prime
    R, M = exact_counts_max(m, c, nprimes)
    assert int(sum(R)) == total, "count total mismatch"
    mx = max(R)
    assert mx < M // 2
    c0 = R[0]
    return Fraction(m * int(mx), total), Fraction(m * int(c0), total), [int(i) for i in np.nonzero(R == mx)[0][:5]]


def q_fourier_minus1(p, which):
    m, c = coeffs(p, which)
    xi = np.arange(1, m, dtype=np.float64)
    logs = np.zeros(m - 1)
    for a in c:
        # (xi*a mod m)/m exactly in float64? xi*a < m^2 <= 9.4e11 -> exact in int64
        r = (np.arange(1, m, dtype=np.int64) * a) % m
        x = r.astype(np.float64) / m
        cs = np.cos(np.pi * x) ** 2
        with np.errstate(divide='ignore'):
            logs += np.log(cs)
    mxl = logs.max()
    s = np.exp(logs - mxl).sum()
    return math.exp(mxl) * s  # q - 1


def brute(p):
    # all 3^p vectors; exact integers; floor division
    import itertools
    fac = [math.factorial(r) for r in range(p)]
    hb = [harmonic_int(r, p) for r in range(p)]
    # vectorise: build arrays of A and B over all vectors progressively
    A = np.zeros(1, dtype=object)
    Bv = np.zeros(1, dtype=object)
    W = np.ones(1, dtype=object)
    for r in range(p):
        A = np.concatenate([A, A + fac[r], A - fac[r]])
        Bv = np.concatenate([Bv, Bv + hb[r], Bv - hb[r]])
        W = np.concatenate([2 * W, W, W])
    cnt1 = {}
    cnt2 = {}
    for a, b, w in zip(A, Bv, W):
        a = int(a); b = int(b); w = int(w)
        k1 = a % p
        k2 = (a % p, ((a // p) - b) % p)
        cnt1[k1] = cnt1.get(k1, 0) + w
        cnt2[k2] = cnt2.get(k2, 0) + w
    tot = 4 ** p
    return Fraction(p * max(cnt1.values()), tot), Fraction(p * p * max(cnt2.values()), tot)


def brute_q3(p):
    m = p ** 3
    F = []
    for r in range(p):
        x = 1
        for s in range(1, r + 1):
            x *= (s - p)
        F.append(x)
    S = np.zeros(1, dtype=np.int64)
    W = np.ones(1, dtype=np.int64)
    for f in F:
        S = np.concatenate([S, S + f, S - f])
        W = np.concatenate([2 * W, W, W])
    res = S % m
    cnt = np.bincount(res, weights=W.astype(np.float64), minlength=m)
    # weights up to 2^p, counts up to 4^p ~ 6.7e7 for p=13: exact in float64
    return Fraction(m * int(cnt.max()), 4 ** p)


def fmt(fr):
    # q - 1 as float with high relative precision
    d = fr - 1
    if d == 0:
        return "0"
    return "%.6e" % (d.numerator / d.denominator) if abs(d.numerator) < 10**300 else str(float(d))


if __name__ == "__main__":
    ps = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else [11, 13, 17, 19, 23, 29, 31]
    for p in ps:
        t0 = time.time()
        out = {}
        for w in (1, 2, 3):
            qmax, q0, arg = q_exact(p, w)
            assert qmax == q0, (p, w, "max not at residue 0", arg)
            qf = q_fourier_minus1(p, w)
            dm1 = qmax - 1
            rel = abs(float(dm1) - qf) / float(dm1) if dm1 != 0 else abs(qf)
            out[w] = (qmax, qf, rel)
        line = "p=%d" % p
        for w in (1, 2, 3):
            qmax, qf, rel = out[w]
            d = qmax - 1
            line += "  q%d-1=%s (fourier %.6e, rel.diff %.1e)" % (w, "%.6e" % float(d) if d > Fraction(1, 10**300) else repr(d), qf, rel)
        line += "  [%.1fs]" % (time.time() - t0)
        print(line, flush=True)
        # exact rationals (num/den sizes) for the record
        for w in (1, 2, 3):
            qmax = out[w][0]
            print("   exact q%d(%d) = %d / %d" % (w, p, qmax.numerator, qmax.denominator), flush=True)
        if p <= 13:
            b1, b2 = brute(p)
            b3 = brute_q3(p)
            print("   brute force 3^%d: q1 %s, q2 %s, q3 %s" % (p, b1 == out[1][0], b2 == out[2][0], b3 == out[3][0]), flush=True)
