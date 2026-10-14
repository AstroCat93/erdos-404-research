#!/usr/bin/env python3
"""Exact test of M4C Lemma L(b) (lin_l holds on G_l under (T1)) and of the
G-complement count of Lemma L(a), on the actual phase-2 schedule.

For each explicit phase-2 window l (b_{l+1} <= BMAX) and x = p^3 xi' in G_l
(random xi', and adversarial xi' = -u0 + p^(s-3) w planting the deepest gate
allowed in G_l at u0 = j/p^2 inside the composite window), compute the exact
valuations v(x + i) and check the linear-regime condition of R3M Theorem C3:
  D_{l-1} + D_l <= m_{l-1} - M_{n_{l+1}},   M_{n_{l+1}} < m_{l-1}.
Lemma L(a): for p^2 | j, v(x+jp) > s iff v(xi' + j/p^2) >= s-2: probability
p^-(s-2) each (checked by the identity v(x+jp) = 3 + v(xi'+j/p^2))."""
import sys, random
sys.path.insert(0, __import__('os').path.dirname(__file__))
from fractions import Fraction
import cert
from vlib import vp


def main():
    p = int(sys.argv[1]); nx = int(sys.argv[2]); BMAX = int(sys.argv[3])
    rng = random.Random(123 + p)
    res = cert.run(p, verbose=False)
    b, k0 = res['b'], res['k0']
    P2 = p * p
    nchk = 0; nfail = 0; nG = 0; nidfail = 0
    for k in range(k0 + 1, len(b) - 1):
        if b[k + 1] > BMAX:
            break
        s = cert.s_rule(p, b[k - 1], k, k0, Fraction(1, 20))
        lo, mid, hi = b[k - 1], b[k], b[k + 1]
        us = [j // P2 for j in range(P2, hi + 1, P2)]
        for it in range(nx):
            w = rng.randrange(1, p ** 40)
            if it % 2 == 1 and us and s > 3:
                u0 = rng.choice([u for u in us if u * P2 > lo] or us)
                xi = -u0 + p ** (s - 3) * (w * p + rng.randrange(1, p))   # v(xi+u0) = s-3 exactly
            else:
                xi = w
            x = p ** 3 * xi
            dep = [0] + [vp(x + j * p, p) for j in range(1, hi + 1)]
            for j in range(P2, hi + 1, P2):
                if dep[j] != 3 + vp(xi + j // P2, p):
                    nidfail += 1
            if max(dep[1:]) > s:
                continue   # not in G_l
            nG += 1
            m = sum(dep[1:lo + 1]); D1 = sum(dep[lo + 1:mid + 1]); D2 = sum(dep[mid + 1:hi + 1])
            Mn = max(dep[1:hi + 1])
            nchk += 1
            if not (D1 + D2 <= m - Mn and Mn < m):
                nfail += 1
                print("  LIN FAILS on G", p, k, lo, mid, hi, s, m, D1, D2, Mn)
    print("p=%d: windows with b_(l+1) <= %d; points in G_l tested %d; lin_l failures %d; identity v(x+jp)=3+v(xi'+j/p^2) failures %d" % (
        p, BMAX, nchk, nfail, nidfail), flush=True)


if __name__ == "__main__":
    main()
