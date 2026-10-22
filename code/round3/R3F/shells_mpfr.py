#!/usr/bin/env python3
"""shells_mpfr.py -- independent rigorous UPPER bounds for Fourier L^1 shell sums (round 3, track R3F).

  T1(k) = sum_{u in (Z/p^k)^x} prod_{i: l_i<k} |cos(pi u x_i / p^k)|

Shares no code with ivshell.c.  Differences: exact Python big-integer factorials; full residues x_i mod p^k
(not unit parts); a single table of cosine upper bounds computed with MPFR (gmpy2) in directed rounding;
products and sums in numpy float64 (round-to-nearest) with an explicit a-posteriori rounding factor;
plain enumeration of all units u (no digit recursion).

Cosine table (M = p^kmax, 0 <= r <= (M-1)/2):
  x_lo = RD(RD(pi_lo * r) / M) at 64 bits, where pi_lo = RD(pi) at 64 bits, so x_lo <= pi r/M <= pi/2;
  c[r] = RU(cos(x_lo)) at 53 bits (MPFR cos is correctly rounded), hence c[r] >= cos(pi r/M) = |cos(pi r/M)|.
  Shell k uses c[rho * p^(kmax-k)], rho = min(r, M_k - r), r = u x mod M_k.
Products: each partial product is replaced by max(fl(prod), 2^-900) (only increases it; prevents underflow), so
  computed term >= true term * (1-2^-53)^(n-1)  (n = number of factors).
Sums: any summation order of N nonnegative computed terms gives  S_comp >= (1-2^-53)^(N-1) * sum(terms).
Hence  T1_true <= 2 * S_comp / (1-2^-53)^(N+n)   (the factor 2: u and -u give the same product; we enumerate
u with u mod p in [1,(p-1)/2]).  The final multiplication is done in exact rational arithmetic and rounded up.

usage:  shells_mpfr.py fact p N0 kmax     |   shells_mpfr.py file p kmax FILE   (lines "U l")
"""
import sys, math, time
from fractions import Fraction
import numpy as np
import gmpy2
from gmpy2 import mpfr


def vp(n, p):
    c = 0
    while n % p == 0:
        n //= p; c += 1
    return c


def elements_fact(p, N0, kmax):
    f = math.factorial(N0)
    e0 = vp(f, p)
    out = []
    n = N0
    while True:
        lev = vp(f, p) - e0
        if lev >= kmax:
            break
        out.append(((f // p ** e0) % p ** kmax, lev))
        n += 1
        f *= n
    return out, e0


def cos_table(M):
    """c[r] >= cos(pi r/M) for 0 <= r <= (M-1)//2, as float64."""
    half = (M - 1) // 2
    tab = np.empty(half + 1, dtype=np.float64)
    ctx_dn = gmpy2.context(precision=64, round=gmpy2.RoundDown)
    ctx_up = gmpy2.context(precision=53, round=gmpy2.RoundUp)
    gmpy2.set_context(ctx_dn)
    pi_lo = gmpy2.const_pi()
    Mm = mpfr(M)   # exact (M < 2^64)
    CH = 1 << 20
    for a in range(0, half + 1, CH):
        b = min(half + 1, a + CH)
        gmpy2.set_context(ctx_dn)
        xs = [gmpy2.div(gmpy2.mul(pi_lo, r), Mm) for r in range(a, b)]
        gmpy2.set_context(ctx_up)
        tab[a:b] = [float(gmpy2.cos(x)) for x in xs]
    gmpy2.set_context(gmpy2.context())
    return tab


def fup(q):
    """smallest double >= the rational q (for printing certified upper bounds)"""
    f = float(q)
    if Fraction(f) < q:
        f = math.nextafter(f, math.inf)
    return f


def main():
    mode = sys.argv[1]
    p = int(sys.argv[2])
    if mode == "fact":
        N0, kmax = int(sys.argv[3]), int(sys.argv[4])
        els, e0 = elements_fact(p, N0, kmax)
        print(f"# shells_mpfr fact p={p} N0={N0} e0={e0} kmax={kmax} elements={len(els)}")
    else:
        kmax = int(sys.argv[3])
        els = []
        for line in open(sys.argv[4]):
            if line.strip():
                U, l = line.split()
                els.append((int(U) % p ** kmax, int(l)))
        print(f"# shells_mpfr file p={p} kmax={kmax} elements={len(els)} source={sys.argv[4]}")
    Mmax = p ** kmax
    assert Mmax < 2 ** 53
    t0 = time.time()
    tab = cos_table(Mmax)
    print(f"# cosine table: {len(tab)} entries, {time.time()-t0:.1f} s", flush=True)
    u53 = Fraction(1, 2 ** 53)
    cum = Fraction(0)
    half = (p - 1) // 2
    for k in range(1, kmax + 1):
        M = p ** k
        scale = p ** (kmax - k)
        xs = [x % M for (x, l) in els if l < k]
        n = len(xs)
        S = 0.0
        N = 0
        CH = 1 << 22
        # u ranges over 1..M-1 with u mod p in [1, half]; enumerate u = p*q + a
        q_all = np.arange(0, M // p + 1, dtype=np.int64)
        for a in range(1, half + 1):
            us_all = q_all * p + a
            us_all = us_all[us_all < M]
            for c0 in range(0, len(us_all), CH):
                us = us_all[c0:c0 + CH]
                prod = np.ones(len(us), dtype=np.float64)
                for x in xs:
                    r = (us * x) % M
                    rho = np.minimum(r, M - r)
                    prod *= tab[rho * scale]
                    np.maximum(prod, 2.0 ** -900, out=prod)
                S += float(np.sum(prod))
                N += len(us)
        # Along the computation path of any single term there are at most n product roundings
        # (the first multiplication 1.0*f is exact, so n-1 in fact) and at most N summation roundings
        # (numpy chunk sum + Python accumulation of chunk sums).  So T_true <= 2 S / (1-u)^R with
        # R = N + n, and (1-u)^-R <= 1 + 2 R u for R u <= 1/2.
        R = N + n
        assert R * u53 < Fraction(1, 2)
        bound = 2 * Fraction(S) * (1 + 2 * R * u53)
        cum += bound
        print(f"k={k:2d} units/2={N} factors={n} T1_upper={fup(bound):.12e} cum_upper={fup(cum):.12e}", flush=True)
    print(f"# total time {time.time()-t0:.1f} s")


if __name__ == "__main__":
    main()
