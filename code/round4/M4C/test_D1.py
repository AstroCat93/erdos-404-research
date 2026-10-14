#!/usr/bin/env python3
"""test_D1.py -- exact test of Lemma D1 (deterministic two-window recursion, L^1 band form) of the M4C report.

For random x and times n0 < n1 < n2 (no linear-regime assumption), with parent set P = (random subset of) the
paths alive at n0:
  (a) Z1 = sum_{g in P} m_W(tau_g mod p^D) and Z2 = sum_g m(tau_g mod p^K)   [checked exactly against a DFS count]
  (b) fibre inequality |nu(t) - p^{-D'} nu_D(t mod p^D)| <= p^{-K} B for every t    [B float64 FFT, rel. tol 1e-9]
  (c) c_{n2} Z2 >= (1 - B/theta)^+ (c_{n1} Z1 - theta c_{n0} Z0) for theta in a grid  [Z exact, B float]
usage: test_D1.py p SEED NX n0 n1 n2 [PREC]
"""
import random
import sys
from fractions import Fraction

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from m4c_lib import v, products, cumV, initial_paths, alive_paths, target, composite_counts  # noqa: E402


def main():
    p, seed, NX, n0, n1, n2 = (int(a) for a in sys.argv[1:7])
    prec = int(sys.argv[7]) if len(sys.argv) > 7 else 60
    rnd = random.Random(seed)
    stats = dict(samples=0, nonempty=0, ident_fail=0, fibre_fail=0, rec_fail=0, rec_checks=0, minslack=None,
                 max_fibre_ratio=0.0, control_fail_B_over_8=0)
    for _ in range(NX):
        x = rnd.randrange(p ** prec)
        pi, dpi, vals = products(x, n2 + 1, p, prec)
        Vc = cumV(vals)
        if max(vals[1:n2 + 1]) >= prec // 3:
            continue
        stats["samples"] += 1
        P0 = initial_paths(pi, dpi, Vc, n0, p, prec)
        if not P0:
            continue
        # random subset (keep at least one)
        P = [g for g in P0 if rnd.random() < 0.7] or P0[:1]
        stats["nonempty"] += 1
        D = Vc[n1] - Vc[n0]
        K = Vc[n2] - Vc[n0]
        Dp = K - D
        Z1dfs = len(alive_paths(pi, dpi, Vc, n0, n1, P, p, prec))
        Z2dfs = len(alive_paths(pi, dpi, Vc, n0, n2, P, p, prec))
        cnt = composite_counts(x, n0, n2, K, p)
        cntW = composite_counts(x, n0, n1, D, p)
        taus = [target(S, pi[n0], Vc[n0], p, prec) for (S, dS, b) in P]
        Z1 = sum(cntW[t % p ** D] for t in taus)
        Z2 = sum(cnt[t % p ** K] for t in taus)
        if Z1 != Z1dfs or Z2 != Z2dfs:
            stats["ident_fail"] += 1
            print("IDENTITY FAIL", x, Z1, Z1dfs, Z2, Z2dfs)
        T = 2 ** (n2 - n0)
        nu = np.array(cnt, dtype=np.float64) / T
        mod = p ** K
        F = np.fft.fft(nu)
        idx = np.arange(mod)
        band = (idx % p ** Dp) != 0
        B = float(np.sum(np.abs(F[band])))
        # fibre check
        nuD = nu.reshape(-1, p ** D).sum(axis=0)
        dev = np.abs(nu - nuD[idx % p ** D] / p ** Dp)
        if B > 0:
            stats["max_fibre_ratio"] = max(stats["max_fibre_ratio"], float(np.max(dev) / (p ** (-K) * B)))
            if np.max(dev) > p ** (-K) * (B / 8):
                stats["control_fail_B_over_8"] += 1
        if np.max(dev) > p ** (-K) * B * (1 + 1e-9) + 1e-15:
            stats["fibre_fail"] += 1
            print("FIBRE FAIL", x, np.max(dev), p ** (-K) * B)
        c0 = Fraction(p ** Vc[n0], 2 ** n0)
        c1 = Fraction(p ** Vc[n1], 2 ** n1)
        c2 = Fraction(p ** Vc[n2], 2 ** n2)
        M0, M1, M2 = c0 * len(P), c1 * Z1, c2 * Z2
        for theta in (0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0):
            fac = max(0.0, 1 - B / theta) * (1 - 1e-9)
            rhs = fac * float(M1 - Fraction(theta) * M0)
            stats["rec_checks"] += 1
            if float(M2) < rhs - 1e-12 * float(M0 + M1 + M2):
                stats["rec_fail"] += 1
                print("RECURSION FAIL", x, theta, float(M2), rhs)
            if rhs > 0:
                s = float(M2) / rhs
                stats["minslack"] = s if stats["minslack"] is None else min(stats["minslack"], s)
    print(f"# test_D1 p={p} seed={seed} NX={NX} n=({n0},{n1},{n2}) prec={prec}")
    print("RESULT", stats)


if __name__ == "__main__":
    main()
