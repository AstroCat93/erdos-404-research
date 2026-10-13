#!/usr/bin/env python3
"""spectral_check.py -- exact test of the odd-p second-moment (spectral) identity, Proposition R3M-B.

Setting: p odd, x in Z_p, n < N, m = V_n(x), D = V_N(x) - m, with (W2) D <= m - M_n and (W3) M_N < m
(slope bound L = 0).  For every slope-0 path e alive at n (lambda_e = v(S_e'(x)) = 0) put
    tau_e^0 = tau_n(e, x0) mod p^D   (x0 = x mod p^m),     beta_e = S_e'(x0)/omega mod p^D,
    omega = pi_n(x0)/p^m,    m(r) = #{f in {0,1}^(N-n): Q_f(x) == r mod p^D},  Q_f = sum f_j pi_{n+j}/pi_n.
Claims tested EXACTLY over all w mod p^D (x_w = x0 + p^m w + unchanged digits >= m+D):
  (B1) for each slope-0 parent e and each w:  #{f: (e,f) alive at N for x_w} = m(tau_e^0 - beta_e w mod p^D);
  (B2) E_w[Y^2] = p^-2D sum_eta |sum_e mhat(eta/beta_e) e(eta*phi_e)|^2, phi_e = tau_e^0/beta_e,
       where Y(w) = number of alive children of all slope-0 parents and mhat(xi) = sum_r m(r) e(-r xi);
       checked by computing the left side by brute force (exact integers) and the right side by an
       explicit complex DFT (floating point, relative tolerance 1e-9).
Also prints the diagonal part Z*chi^2 and the Cauchy-Schwarz bound Z^2*chi^2 (in units (2^(N-n) p^-D)^2).
usage: spectral_check.py p SEED NX n N [DMAX]
"""
import cmath
import random
import sys

PREC = 100


def vp(a, p):
    if a == 0:
        return PREC
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def main():
    p, seed, NX, n, N = (int(a) for a in sys.argv[1:6])
    DMAX = int(sys.argv[6]) if len(sys.argv) > 6 else 4
    MOD = p ** PREC
    rnd = random.Random(seed)
    done = tries = 0
    b1_tot = b1_ok = b2_ok = 0
    while done < NX and tries < 100000:
        tries += 1
        x = rnd.randrange(MOD)
        vs = [vp((x + i) % MOD, p) for i in range(1, N + 1)]
        m = sum(vs[:n]); D = sum(vs[n:]); Mn = max(vs[:n]); MN = max(vs)
        if D < 1 or D > DMAX or D > m - Mn or MN >= m:
            continue

        def table(xx):
            P = [1]; dP = [0]
            for j in range(1, N + 1):
                dP.append((dP[-1] * (xx + j) + P[-1]) % MOD)
                P.append(P[-1] * (xx + j) % MOD)
            return P, dP

        P, dP = table(x)
        # alive slope-0 paths at n (DFS on S mod p^PREC with backward-integrality pruning)
        Vpre = [0]
        for i in range(n):
            Vpre.append(Vpre[-1] + vs[i])
        par = []
        stack = [(1, (1,), 1, 0)]  # (j, bits, S, S')
        while stack:
            j, bits, S, Sd = stack.pop()
            if vp(S % MOD, p) < Vpre[j]:
                continue
            if j == n:
                if Sd % p:
                    par.append((bits, S, Sd))
                continue
            stack.append((j + 1, bits + (0,), S, Sd))
            stack.append((j + 1, bits + (1,), (S + P[j]) % MOD, (Sd + dP[j]) % MOD))
        if len(par) < 2:
            continue
        done += 1
        pD = p ** D
        x0 = x % p ** m
        P0, dP0 = table(x0)
        omega = (P0[n] // p ** m) % pD
        winv = pow(omega, -1, pD)
        taus, betas = [], []
        for bits, _, _ in par:
            S0 = sum(P0[j] for j in range(n) if bits[j])
            Sd0 = sum(dP0[j] for j in range(n) if bits[j])
            tau0 = (-(S0 // p ** m) * winv) % pD
            taus.append(tau0)
            betas.append((Sd0 * winv) % pD)
        # window count function m(r) at x (constant on the cylinder since D <= m)
        mcount = [0] * pD
        sums = [0]
        y = 1  # y = pi_{n+k}(x)/pi_n(x) = (x+n+1)...(x+n+k), reduced mod p^D
        for k in range(N - n):
            sums = sums + [(s + y) % pD for s in sums]
            y = y * (x + n + k + 1) % pD
        for s in sums:
            mcount[s] += 1
        # brute force over w
        hi = x - x % p ** (m + D)
        Y2 = 0; Ysum = 0
        for w in range(pD):
            xw = x0 + p ** m * w + hi
            Pw, _ = table(xw)
            VN = m + D
            wsums = [0]
            for k in range(N - n):
                wsums = wsums + [(s + Pw[n + k]) % MOD for s in wsums]
            Y = 0
            for i, (bits, _, _) in enumerate(par):
                Se = sum(Pw[j] for j in range(n) if bits[j]) % MOD
                c = sum(1 for s in wsums if vp((Se + s) % MOD, p) >= VN)
                b1_tot += 1
                pred = mcount[(taus[i] - betas[i] * w) % pD]
                b1_ok += (c == pred)
                if c != pred:
                    print("MISMATCH B1", m, D, i, w, c, pred)
                Y += c
            Ysum += Y; Y2 += Y * Y
        lhs = Y2 / pD
        # Fourier side
        tot = 0.0
        for eta in range(pD):
            acc = 0j
            for i in range(len(par)):
                xi = (eta * pow(betas[i], -1, pD)) % pD
                mh = sum(mcount[r] * cmath.exp(-2j * cmath.pi * r * xi / pD) for r in range(pD) if mcount[r])
                phi = (taus[i] * pow(betas[i], -1, pD)) % pD
                acc += mh * cmath.exp(2j * cmath.pi * eta * phi / pD)
            tot += abs(acc) ** 2
        rhs = tot / pD ** 2
        ok = abs(lhs - rhs) <= 1e-9 * max(1.0, lhs)
        b2_ok += ok
        if not ok:
            print("MISMATCH B2", lhs, rhs)
        T = 2 ** (N - n)
        EY = Ysum / pD
        chi2 = pD * sum(c * c for c in mcount) / T ** 2 - 1
        Z = len(par)
        unit = (T / pD) ** 2
        print(f"x#{done}: m={m} D={D} Z0={Z} EY={EY:.4f} (pred {Z*T/pD:.4f}) Var/unit={(lhs-EY**2)/unit:.4f} "
              f"diag Z*chi2={Z*chi2:.4f} CS Z^2*chi2={Z*Z*chi2:.4f} betas_distinct_mod_p={len(set(b % p for b in betas))}",
              flush=True)
    print(f"RESULT p={p} n={n} N={N}: B1 pointwise child counts exact {b1_ok}/{b1_tot}; B2 identity {b2_ok}/{done}")


if __name__ == "__main__":
    main()
