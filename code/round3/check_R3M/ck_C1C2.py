#!/usr/bin/env python3
"""ck_C1C2.py -- independent test of R3M Lemma C1 and Proposition C2 (two-window inequality),
including the identification eps = p^(D+D') Coll_(D+D') - p^D Coll_D.

Windows W=[n,N), W'=[N,N'); hypothesis (5.2): D+D' <= m - M_N' and M_N' < m.
For every w mod p^(D+D'), x' = x0 + p^m w + p^(m+D+D') z (z random):
  Z_N(x')  = # slope-0 paths alive at N at x'   (extensions of ALL alive-at-n paths, slope tested at x')
  Z_N'(x') = # slope-0 paths alive at N' at x'  (same, from scratch over all alive-at-n paths)
  Psi_P(xi; x') for P = slope-0 parents, and for a random nonempty subset P' of them.
Checks:
  (mart)  E c_N Z_N = E c_N' Z_N' = c_n Z_n  [exact]
  (C1a)   |E Psi_P(xi)| < tol for xi != 0;  (C1b) E|c_N Psi_P(xi)|^2 <= (c_n|P|)^2 F_W(xi)(1+1e-9), all xi
  (C2)    c_N'^2 E Z_N'^2 - c_N^2 E Z_N^2 <= eps (c_n Z_n)^2  [exact, eps from collisions]
  (eps)   collision form == Fourier fibre form sum_{xi!=0}|muhat_W'(xi)|^2 F_W(xi)   [float, rel 1e-9]
NEG=1 drops the (5.2) filter (keeps only M_N' < m) and reports violations, to show non-vacuity.
usage: ck_C1C2.py p seed nx n H H2 [NEG] [MAXPAR] [KMAX]
"""
import cmath
import random
import sys
from fractions import Fraction

from ck_lib import PAdic, products, alive_from_scratch, extend, target, subset_sum_law, collision


def dft(law, md, T):
    return [sum(c * cmath.exp(-2j * cmath.pi * (r * xi % md) / md) for r, c in law.items()) / T
            for xi in range(md)]


def main():
    a = sys.argv[1:]
    p, seed, nx, n, H, H2 = (int(t) for t in a[:6])
    neg = int(a[6]) if len(a) > 6 else 0
    maxpar = int(a[7]) if len(a) > 7 else 10 ** 9
    kmax = int(a[8]) if len(a) > 8 else 8
    N, N2 = n + H, n + H + H2
    prec = max(60, 3 * N2 // (p - 1) + 30)
    P = PAdic(p, prec)
    rnd = random.Random(seed)
    done = tries = 0
    c_mart = c_mart_f = c_c1 = c_c1a_f = c_c1b_f = c_c2 = c_c2_f = c_eps_f = 0
    worst = 0.0
    nontriv = 0
    while done < nx and tries < 200000:
        tries += 1
        x = rnd.randrange(P.mod)
        pi, dpi, vals = products(P, x, N2)
        m = sum(vals[1:n + 1])
        VN = sum(vals[1:N + 1])
        VN2 = sum(vals[1:N2 + 1])
        D, D2 = VN - m, VN2 - VN
        MN2 = max(vals[1:N2 + 1])
        if not MN2 < m:
            continue
        if not neg and not (D + D2 <= m - MN2):
            continue
        if D + D2 > kmax or D2 < 1:
            continue
        par_all = alive_from_scratch(P, pi, dpi, vals, n)
        par0 = [t for t in par_all if P.v(t[2]) == 0]
        if not par0:
            continue
        roots_src = par_all
        if len(par_all) > maxpar:
            # restricted mode: extend only slope-0 parents (relies on A(i); flagged in output)
            roots_src = par0
        done += 1
        K = D + D2
        mdK, mdD, mdD2 = p ** K, p ** D, p ** D2
        x0 = x % p ** m
        sub = [b for (b, _, _) in par0 if rnd.random() < 0.5] or [par0[0][0]]
        subset = set(sub)
        par0b = set(b for (b, _, _) in par0)
        Zn = len(par0)
        cn = Fraction(p ** m, 2 ** n)
        cN = Fraction(p ** VN, 2 ** N)
        cN2 = Fraction(p ** VN2, 2 ** N2)
        sumZ1 = sumZ1sq = sumZ2 = sumZ2sq = 0
        psi_sum = {0: [0j] * mdD2, 1: [0j] * mdD2}
        psi_sq = {0: [0.0] * mdD2, 1: [0.0] * mdD2}
        for w in range(mdK):
            z = rnd.randrange(p ** 6)
            xp = x0 + p ** m * w + p ** (m + K) * z
            pi2, dpi2, vals2 = products(P, xp, N2)
            roots = []
            for (b, _, _) in roots_src:
                S = sum(pi2[j] for j in range(n) if (b >> j) & 1) % P.mod
                dS = sum(dpi2[j] for j in range(n) if (b >> j) & 1) % P.mod
                roots.append((b, S, dS))
            kids = extend(P, pi2, dpi2, vals2, n, N, roots)
            kids0 = [t for t in kids if P.v(t[2]) == 0]
            Z1 = len(kids0)
            gkids = extend(P, pi2, dpi2, vals2, N, N2, kids)
            Z2 = sum(1 for t in gkids if P.v(t[2]) == 0)
            sumZ1 += Z1
            sumZ1sq += Z1 * Z1
            sumZ2 += Z2
            sumZ2sq += Z2 * Z2
            # Psi for P = all slope-0 parents (key 0) and for the random subset (key 1)
            acc = {0: [0j] * mdD2, 1: [0j] * mdD2}
            for (b2, S2, dS2) in kids:
                pb = b2 & ((1 << n) - 1)
                if pb not in par0b:
                    continue
                tau = target(P, S2, pi2[N], VN) % mdD2
                for xi in range(mdD2):
                    ph = cmath.exp(2j * cmath.pi * xi * tau / mdD2)
                    acc[0][xi] += ph
                    if pb in subset:
                        acc[1][xi] += ph
            for k in (0, 1):
                for xi in range(mdD2):
                    psi_sum[k][xi] += acc[k][xi]
                    psi_sq[k][xi] += abs(acc[k][xi]) ** 2
        # martingale
        c_mart += 1
        if not (cN * Fraction(sumZ1, mdK) == cn * Zn and cN2 * Fraction(sumZ2, mdK) == cn * Zn):
            c_mart_f += 1
        # eps by collisions (exact) on the composite window [n, N2)
        ys = []
        for i in range(N2 - n):
            q = 1
            for k in range(n + 1, n + i + 1):
                q *= x + k
            ys.append(q)
        eps = mdK * collision(ys, mdK) - mdD * collision(ys, mdD)
        # Fourier fibre form
        T = 2 ** (N - n)
        T2 = 2 ** (N2 - N)
        lawW = subset_sum_law(ys[:N - n], mdK)
        muW = dft(lawW, mdK, T)
        ys2 = []
        for i in range(N2 - N):
            q = 1
            for k in range(N + 1, N + i + 1):
                q *= x + k
            ys2.append(q)
        muW2 = dft(subset_sum_law(ys2, mdD2), mdD2, T2)
        piN_over = 1
        for k in range(n + 1, N + 1):
            piN_over *= x + k
        u = (piN_over // p ** D) % mdD2
        uinv = pow(u, -1, mdD2)
        F = [sum(abs(muW[zeta]) ** 2 for zeta in range(mdK) if (zeta - xi * uinv) % mdD2 == 0)
             for xi in range(mdD2)]
        eps_f = sum(abs(muW2[xi]) ** 2 * F[xi] for xi in range(1, mdD2))
        if abs(eps_f - float(eps)) > 1e-9 * max(1.0, abs(eps_f)):
            c_eps_f += 1
        # C1
        for k, PP in ((0, len(par0)), (1, len(subset))):
            for xi in range(mdD2):
                c_c1 += 1
                mean = psi_sum[k][xi] / mdK
                if xi != 0 and abs(mean) > 1e-7 * max(1, PP):
                    c_c1a_f += 1
                lhs = float(cN) ** 2 * psi_sq[k][xi] / mdK
                rhs = (float(cn) * PP) ** 2 * F[xi]
                if lhs > rhs * (1 + 1e-9) + 1e-300:
                    c_c1b_f += 1
        # C2
        c_c2 += 1
        lhs = cN2 ** 2 * Fraction(sumZ2sq, mdK) - cN ** 2 * Fraction(sumZ1sq, mdK)
        rhs = eps * (cn * Zn) ** 2
        if lhs > rhs:
            c_c2_f += 1
        if rhs > 0:
            worst = max(worst, float(lhs / rhs))
            if lhs > 0:
                nontriv += 1
    mode = "NEG (no (5.2) filter)" if neg else "(5.2) enforced"
    print(f"RESULT C1C2 p={p} n={n} H={H} H2={H2} [{mode}] samples={done}: mart fails={c_mart_f}/{c_mart}; "
          f"C1a fails={c_c1a_f}/{c_c1}; C1b fails={c_c1b_f}/{c_c1}; eps(coll)==eps(Fourier) fails={c_eps_f}/{done}; "
          f"C2 fails={c_c2_f}/{c_c2}; max lhs/(eps M^2)={worst:.4f}; samples with lhs>0: {nontriv}")


if __name__ == "__main__":
    main()
