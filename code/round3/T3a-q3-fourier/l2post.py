#!/usr/bin/env python3
"""l2post.py -- post-process l2dp output: exact rational L^2 Fourier masses.

Usage: python3 -I l2post.py out_p5_E11_N0_5.txt [--brute]

For each E' the file gives S(E') mod 2^128 and mod q=2^61-1 (and a long double).
We reconstruct S(E') exactly by CRT, then
  P(E')      = S(E') / 4^M                      (collision probability mod p^{E'})
  L2tot(k)   = p^k P(k+e0),  e0 = v_p(N0!)      (sum over ALL xi in p^{-k}Z/Z of |nu-hat|^2)
  T2(k)      = L2tot(k) - L2tot(k-1)           (shell of exact order p^k), L2tot(0)=1
  rm(k)      = p^k (1-1/p) 2^{-m_k}, m_k = #{n>=N0 : v(n!) < k+e0}   (random model shell)
With --brute, the collision probabilities are recomputed by brute force for small cases.
"""
import sys, itertools
from fractions import Fraction
from math import factorial

Q = 2**61 - 1
TWO128 = 2**128

def vp(n, p):
    v = 0
    while n % p == 0:
        n //= p; v += 1
    return v

def vfact(n, p):
    v = 0; m = n
    while m:
        m //= p; v += m
    return v

def crt(hi, lo, sq):
    a = (hi << 64) | lo          # S mod 2^128
    # S = a + 2^128 * t,  with (a + 2^128 t) == sq mod Q
    inv = pow(TWO128 % Q, -1, Q)
    t = ((sq - a) % Q) * inv % Q
    return a + TWO128 * t

def read(fn):
    p = E = N0 = M = None; rows = []
    for line in open(fn):
        if line.startswith('# p='):
            parts = dict(kv.split('=') for kv in line[2:].split())
            p, E, N0, M = int(parts['p']), int(parts['E']), int(parts['N0']), int(parts['M'])
        elif line.startswith('#') or not line.strip():
            continue
        else:
            f = line.split()
            rows.append((int(f[0]), int(f[1]), int(f[2]), int(f[3]), int(f[4]), float(f[5]), int(f[7]) if len(f) > 7 else -1))
    return p, E, N0, M, rows

def brute(p, E, N0):
    """collision probabilities by explicit enumeration of eta in {-1,0,1}^M (small only)."""
    els = []
    n = N0
    while vfact(n, p) < E:
        els.append(factorial(n)); n += 1
    M = len(els)
    mod = p**E
    out = {}
    from collections import Counter
    cnt = Counter({0: 1})
    for a in els:
        a %= mod
        new = Counter()
        for r, c in cnt.items():
            new[r] += c; new[(r + a) % mod] += c
        cnt = new
    for Ep in range(1, E + 1):
        m = p**Ep
        fold = Counter()
        for r, c in cnt.items(): fold[r % m] += c
        out[Ep] = Fraction(sum(c * c for c in fold.values()), 4**M)
    return out, M

def main():
    fn = sys.argv[1]
    p, E, N0, M, rows = read(fn)
    e0 = vfact(N0, p)
    S = {}
    hits = {}
    for Ep, Mp, hi, lo, sq, sd, hit in rows:
        hits[Ep] = hit
        s = crt(hi, lo, sq)
        assert s < 2**189, "CRT range exceeded"
        assert abs(float(s) - sd) <= 2e-6 * sd + 1, (Ep, s, sd)  # printed with 6 digits
        S[Ep] = (s, Mp)
    if '--brute' in sys.argv:
        bp, Mb = brute(p, E, N0)
        assert Mb == M
        for Ep in range(1, E + 1):
            assert bp[Ep] == Fraction(S[Ep][0], 4**M), ("brute mismatch", Ep)
        print("# brute-force check passed for p=%d E=%d N0=%d (M=%d)" % (p, E, N0, M))
    print("# p=%d N0=%d e0=%d M=%d" % (p, N0, e0, M))
    print("# k  Eprime  m_k  P(Eprime)=S/4^M   L2tot(k)=p^k P   T2(k) shell   rm(k) random-model shell   T2/rm   L2tot-1   hit/p^Eprime  1/L2tot(CS bound)")
    prev = Fraction(1)
    for Ep in range(1, E + 1):
        k = Ep - e0
        if k < 1: continue
        s, Mp = S[Ep]
        P = Fraction(s, 4**M)
        L2 = Fraction(p)**k * P
        T2 = L2 - prev
        rm = Fraction(p)**k * Fraction(p - 1, p) / Fraction(2)**Mp
        hf = hits[Ep] / p**Ep if hits[Ep] >= 0 else float("nan")
        print("%3d %3d %3d  %.6e  %.10g  %.6e  %.6e  %.4f  %.10g  %.8f  %.8f" % (k, Ep, Mp, float(P), float(L2), float(T2), float(rm), float(T2 / rm), float(L2 - 1), hf, 1 / float(L2)))
        prev = L2
    # exact rationals of the last two totals, for the record
    for Ep in (E - 1, E):
        if Ep >= 1:
            s, Mp = S[Ep]
            print("# exact S(%d) = %d ; 4^M = 2^%d ; L2tot(k=%d) = p^k S / 4^M" % (Ep, s, 2 * M, Ep - e0))

if __name__ == '__main__':
    main()
