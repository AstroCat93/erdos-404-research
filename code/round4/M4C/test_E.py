#!/usr/bin/env python3
"""test_E.py -- exact test of Theorem E (pathwise two-window Chebyshev bound) of the M4C report.

For random x with the linear-regime condition (5.2) for the windows W=[n0,n1), W'=[n1,n2):
  D + D' <= m - M_{n2},  M_{n2} < m,   m = V_{n0}(x),
let A = x + p^m Z_p (atom), P = slope-0 paths alive at n0 (constant on A: checked).  For every w mod p^K
(x' = x0 + p^m w; K = D + D' fresh digits suffice) compute exactly M1 = c_{n1} Z^0_{n1}(x'), M2 = c_{n2} Z^0_{n2}(x')
(DFS descendants of P; inheritance of slope 0 is checked) and check
  (i)   E_w[M1] = M0 = c_{n0}|P|    (Cor A')
  (ii)  E_w[(M2 - M1)^2] <= M0^2 * eps,  eps = p^K Coll_K - p^D Coll_D  (exact)    [Theorem E, variance step]
  (iii) P_w(M2 < M1 - theta*M0) <= eps/theta^2 for theta in a grid                  [Theorem E]
usage: test_E.py p SEED NX n0 n1 n2 [PREC]
"""
import random
import sys
from fractions import Fraction

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from m4c_lib import v, products, cumV, initial_paths, alive_paths, composite_counts, band_L2_exact  # noqa: E402


def main():
    p, seed, NX, n0, n1, n2 = (int(a) for a in sys.argv[1:7])
    prec = int(sys.argv[7]) if len(sys.argv) > 7 else 50
    rnd = random.Random(seed)
    st = dict(tried=0, lin=0, atoms_with_P0=0, mean_fail=0, var_fail=0, cheb_fail=0, inherit_fail=0,
              P0_const_fail=0, max_var_ratio=0.0, cheb_checks=0, nontriv_cheb=0)
    for _ in range(NX):
        x = rnd.randrange(p ** prec)
        pi, dpi, vals = products(x, n2, p, prec)
        Vc = cumV(vals)
        m = Vc[n0]
        D, K = Vc[n1] - m, Vc[n2] - m
        Mn2 = max(vals[1:n2 + 1])
        st["tried"] += 1
        if not (K <= m - Mn2 and Mn2 < m):
            continue
        st["lin"] += 1
        P_all = initial_paths(pi, dpi, Vc, n0, p, prec)
        P0 = sorted(b for (S, dS, b) in P_all if v(dS, p, prec) == 0)
        if not P0:
            continue
        st["atoms_with_P0"] += 1
        x0 = x % p ** m
        cnt = composite_counts(x, n0, n2, K, p)
        eps = band_L2_exact(cnt, D, K, p, 2 ** (n2 - n0))
        c0 = Fraction(p ** m, 2 ** n0)
        c1 = Fraction(p ** Vc[n1], 2 ** n1)
        c2 = Fraction(p ** Vc[n2], 2 ** n2)
        M0 = c0 * len(P0)
        M1s, M2s = [], []
        for w in range(p ** K):
            xp = x0 + p ** m * w
            pi2, dpi2, vals2 = products(xp, n2, p, prec)
            Vc2 = cumV(vals2)
            P2 = sorted(b for (S, dS, b) in initial_paths(pi2, dpi2, Vc2, n0, p, prec) if v(dS, p, prec) == 0)
            if P2 != P0:
                st["P0_const_fail"] += 1
            roots = []
            for b in P0:
                S = sum(pi2[j] for j in range(n0) if b >> j & 1)
                dS = sum(dpi2[j] for j in range(n0) if b >> j & 1)
                roots.append((S, dS, b))
            ch1 = alive_paths(pi2, dpi2, Vc2, n0, n1, roots, p, prec)
            ch2 = alive_paths(pi2, dpi2, Vc2, n0, n2, roots, p, prec)
            if any(v(dS, p, prec) != 0 for (_, dS, _) in ch1 + ch2):
                st["inherit_fail"] += 1
            M1s.append(c1 * len(ch1))
            M2s.append(c2 * len(ch2))
        N = len(M1s)
        if sum(M1s, Fraction(0)) / N != M0:
            st["mean_fail"] += 1
        var = sum(((a - b) ** 2 for a, b in zip(M2s, M1s)), Fraction(0)) / N
        if var > M0 * M0 * eps:
            st["var_fail"] += 1
            print("VAR FAIL", x, float(var), float(M0 * M0 * eps))
        if eps > 0:
            st["max_var_ratio"] = max(st["max_var_ratio"], float(var / (M0 * M0 * eps)))
        for theta in (Fraction(1, 64), Fraction(1, 16), Fraction(1, 4), Fraction(1, 2)):
            frac = Fraction(sum(1 for a, b in zip(M2s, M1s) if a < b - theta * M0), N)
            st["cheb_checks"] += 1
            if frac > 0:
                st["nontriv_cheb"] += 1
            if frac > eps / theta ** 2:
                st["cheb_fail"] += 1
                print("CHEB FAIL", x, theta, float(frac), float(eps / theta ** 2))
    print(f"# test_E p={p} seed={seed} NX={NX} n=({n0},{n1},{n2}) prec={prec}")
    print("RESULT", st)


if __name__ == "__main__":
    main()
