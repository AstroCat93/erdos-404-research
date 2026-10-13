#!/usr/bin/env python3
"""ck_propB.py -- independent exact test of R3M Proposition B (slope-0 second moment) and
Proposition N (lower bound chi^2_W >= s(p-s)/4^r >= (p-1)/4^p, equality case).

Window W=[n,N) with (W2') D <= m - M_n and (W3') M_N < m.  P = slope-0 paths alive at n for x.
For every w mod p^D, x' = x0 + p^m w + p^(m+D) z (z random), x0 = x mod p^m (integer in [0,p^m)):
  Y(w) = total number of alive-at-N children of P at x'  (DFS, direct evaluation).
Checks:
  (B-i)  per parent, child count == m_W(tau0_e - beta_e w mod p^D)   [exact]
         with tau0_e = tau_n(e,x0) mod p^D, beta_e = omega^-1 S_e'(x0) mod p^D, omega = pi_n(x0)/p^m;
  (B-ii) E Y == |P| T p^-D [exact]; Var_C(c_N Y) computed exactly from the Y(w) equals
         c_n^2 sum_{eta != 0} |sum_e muhat(eta/beta_e) e(eta phi_e/p^D)|^2  [float, rel 1e-9];
         Var <= (c_n|P|)^2 chi^2_W [exact, chi^2 = p^D Coll_D - 1];
  (N)    chi^2_W >= s(p-s)/4^r >= (p-1)/4^p  [exact], r = # valuation-0 window elements;
         equality Var == M^2 chi^2 when |P| = 1  [exact].
usage: ck_propB.py p seed nx n N [MAXPAR]
"""
import cmath
import random
import sys
from fractions import Fraction

from ck_lib import PAdic, products, alive_from_scratch, extend, target, subset_sum_law


def main():
    p, seed, nx, n, N = (int(a) for a in sys.argv[1:6])
    maxpar = int(sys.argv[6]) if len(sys.argv) > 6 else 10 ** 9
    prec = max(60, 3 * N // (p - 1) + 30)
    P = PAdic(p, prec)
    rnd = random.Random(seed)
    done = tries = 0
    nBi = nBi_fail = nBii = nBii_fail = nineq = nineq_fail = nN = nN_fail = neq = neq_fail = 0
    worst_ratio = 0.0
    while done < nx and tries < 100000:
        tries += 1
        x = rnd.randrange(P.mod)
        pi, dpi, vals = products(P, x, N)
        m = sum(vals[1:n + 1])
        VN = sum(vals[1:N + 1])
        D = VN - m
        if not (max(vals[1:N + 1]) < m and D <= m - max(vals[1:n + 1]) and D >= 1):
            continue
        par_all = alive_from_scratch(P, pi, dpi, vals, n)
        par = [(b, S, dS) for (b, S, dS) in par_all if P.v(dS) == 0]
        if not par:
            continue
        if len(par) > maxpar:
            par = rnd.sample(par, maxpar)
        done += 1
        md = p ** D
        x0 = x % p ** m
        pi0, dpi0, _ = products(P, x0, N)
        omega = pi0[n] // p ** m
        # window elements y_i = pi_{n+i}/pi_n (exact products) and law m_W mod p^D
        ys = []
        for i in range(N - n):
            q = 1
            for k in range(n + 1, n + i + 1):
                q *= x + k
            ys.append(q)
        mW = subset_sum_law(ys, md)
        T = 2 ** (N - n)
        # Prop N
        r = sum(1 for yv in ys if yv % p != 0)
        coll = Fraction(sum(c * c for c in mW.values()), T * T)
        chi2 = md * coll - 1
        s_ = pow(2, r, p)
        nN += 1
        if not (chi2 >= Fraction(s_ * (p - s_), 4 ** r) >= Fraction(p - 1, 4 ** p)):
            nN_fail += 1
        # parent data at x0
        tau0 = {}
        beta = {}
        for (b, _, _) in par:
            S = sum(pi0[j] for j in range(n) if (b >> j) & 1)
            dS = sum(dpi0[j] for j in range(n) if (b >> j) & 1)
            tau0[b] = target(P, S, pi0[n], m) % md
            beta[b] = dS * pow(omega, -1, md) % md
            assert beta[b] % p != 0
        Ys = []
        for w in range(md):
            z = rnd.randrange(p ** 6)
            xp = x0 + p ** m * w + p ** (m + D) * z
            pi2, dpi2, vals2 = products(P, xp, N)
            roots = []
            for (b, _, _) in par:
                S = sum(pi2[j] for j in range(n) if (b >> j) & 1) % P.mod
                dS = sum(dpi2[j] for j in range(n) if (b >> j) & 1) % P.mod
                roots.append((b, S, dS))
            kids = extend(P, pi2, dpi2, vals2, n, N, roots)
            per = {}
            for (b2, _, _) in kids:
                pb = b2 & ((1 << n) - 1)
                per[pb] = per.get(pb, 0) + 1
            for (b, _, _) in par:
                nBi += 1
                if per.get(b, 0) != mW.get((tau0[b] - beta[b] * w) % md, 0):
                    nBi_fail += 1
            Ys.append(len(kids))
        cn = Fraction(p ** m, 2 ** n)
        cN = Fraction(p ** VN, 2 ** N)
        EY = Fraction(sum(Ys), md)
        nBii += 1
        ok = EY == Fraction(len(par) * T, md)
        var = cN ** 2 * (Fraction(sum(yv * yv for yv in Ys), md) - EY ** 2)
        # Fourier side
        muhat = [sum(c * cmath.exp(-2j * cmath.pi * rr * xi / md) for rr, c in mW.items()) / T
                 for xi in range(md)]
        four = 0.0
        for eta in range(1, md):
            A = 0j
            for (b, _, _) in par:
                bi = pow(beta[b], -1, md)
                phi = tau0[b] * bi % md
                A += muhat[eta * bi % md] * cmath.exp(2j * cmath.pi * eta * phi / md)
            four += abs(A) ** 2
        four *= float(cn) ** 2
        if abs(four - float(var)) > 1e-9 * max(1.0, abs(float(var)), abs(four)):
            ok = False
        if not ok:
            nBii_fail += 1
        Mv = cn * len(par)
        nineq += 1
        if var > Mv ** 2 * chi2:
            nineq_fail += 1
        if Mv ** 2 * chi2 > 0:
            worst_ratio = max(worst_ratio, float(var / (Mv ** 2 * chi2)))
        if len(par) == 1:
            neq += 1
            if var != Mv ** 2 * chi2:
                neq_fail += 1
    print(f"RESULT propB p={p} n={n} N={N} samples={done}: (B-i) pointwise counts fails={nBi_fail}/{nBi}; "
          f"(B-ii) mean+Fourier identity fails={nBii_fail}/{nBii}; Var<=M^2chi^2 fails={nineq_fail}/{nineq} "
          f"(max ratio {worst_ratio:.4f}); PropN bound fails={nN_fail}/{nN}; equality |P|=1 fails={neq_fail}/{neq}")


if __name__ == "__main__":
    main()
