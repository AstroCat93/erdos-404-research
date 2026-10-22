#!/usr/bin/env python3
"""spectral_mc.py -- heuristic Monte Carlo study (not a proof) of the conditional variance of the
slope-0 martingale at odd p, using the exact identity of Proposition R3M-B:
   Var_w(Y) = p^-D sum_w (sum_e m(tau_e^0 - beta_e w))^2 - (Z T / p^D)^2 ,   T = 2^(N-n),
for the slope-0 population P at time n (Z = |P|) and a window [n, N) with D <= m - M_n, M_N < m.
For each sample it records, in units (T/p^D)^2:
   var   = Var_w(Y),     diag = Z*chi^2,     cs = Z^2*chi^2  (Cauchy-Schwarz bound),
   chi^2 = p^D sum_r m(r)^2 / T^2 - 1   (L^2 Fourier mass of the window's subset-sum law mod p^D),
and the normalised increment  c_n^2 * var  (= Var(M_N | cylinder), M = c Z, c_n = 2^-n p^V_n).
usage: spectral_mc.py p SEED NX n H     (window [n, n+H))
"""
import random
import statistics
import sys

PREC = 120


def vp(a, p):
    if a == 0:
        return PREC
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def main():
    p, seed, NX, n, H = (int(a) for a in sys.argv[1:6])
    N = n + H
    MOD = p ** PREC
    rnd = random.Random(seed)
    rows = []
    tries = 0
    while len(rows) < NX and tries < 50 * NX:
        tries += 1
        x = rnd.randrange(MOD)
        vs = [vp((x + i) % MOD, p) for i in range(1, N + 1)]
        m = sum(vs[:n]); D = sum(vs[n:]); Mn = max(vs[:n]); MN = max(vs)
        if D < 1 or D > m - Mn or MN >= m or p ** D > 3 ** 9:
            continue
        x0 = x % p ** m
        P = [1]; dP = [0]
        for j in range(1, N + 1):
            dP.append((dP[-1] * (x0 + j) + P[-1]) % MOD)
            P.append(P[-1] * (x0 + j) % MOD)
        Vpre = [0]
        for i in range(n):
            Vpre.append(Vpre[-1] + vs[i])
        pD = p ** D
        omega_inv = pow((P[n] // p ** m) % pD, -1, pD)
        taus, betas = [], []
        stack = [(1, 1, 0)]
        while stack:
            j, S, Sd = stack.pop()
            if vp(S % MOD, p) < Vpre[j]:
                continue
            if j == n:
                if Sd % p:
                    taus.append((-(S // p ** m) * omega_inv) % pD)
                    betas.append((Sd * omega_inv) % pD)
                continue
            stack.append((j + 1, S, Sd))
            stack.append((j + 1, (S + P[j]) % MOD, (Sd + dP[j]) % MOD))
        Z = len(taus)
        logc = -n * 1.0 + Vpre[n] * __import__('math').log2(p)
        if Z == 0:
            rows.append((0, 0, 0, 0, 0, 0, logc))
            continue
        mc = [0] * pD
        sums = [0]
        y = 1
        for k in range(H):
            sums = sums + [(s + y) % pD for s in sums]
            y = y * (x0 + n + k + 1) % pD
        for s in sums:
            mc[s] += 1
        T = 2 ** H
        chi2 = pD * sum(c * c for c in mc) / T ** 2 - 1
        acc2 = 0
        for w in range(pD):
            Y = 0
            for t, b in zip(taus, betas):
                Y += mc[(t - b * w) % pD]
            acc2 += Y * Y
        unit = (T / pD) ** 2
        var = (acc2 / pD - (Z * T / pD) ** 2) / unit
        rows.append((Z, chi2, var, Z * chi2, Z * Z * chi2, D, logc))
    nz = [r for r in rows if r[0] > 0]
    print(f"# spectral_mc p={p} seed={seed} NX={NX} n={n} H={H}: samples={len(rows)} with Z0>0: {len(nz)}")
    if nz:
        rd = [r[2] / r[3] for r in nz if r[3] > 0]
        rc = [r[2] / r[4] for r in nz if r[4] > 0]
        print("SUMMARY median Z0 = %.1f; mean chi^2 = %.4f; median var/diag = %.4f; mean var/diag = %.4f; "
              "median var/CS = %.3e; max var/diag = %.4f" % (statistics.median(r[0] for r in nz),
              statistics.mean(r[1] for r in nz), statistics.median(rd), statistics.mean(rd),
              statistics.median(rc), max(rd)))
        # normalised increments E[c_n^2 var] and E[M_n^2] = E[c_n^2 Z^2] over all samples (zeros included)
        import math
        inc = sum((2 ** r[6]) ** 2 * r[2] for r in rows) / len(rows)
        incdiag = sum((2 ** r[6]) ** 2 * r[3] for r in rows) / len(rows)
        incCS = sum((2 ** r[6]) ** 2 * r[4] for r in rows) / len(rows)
        m2 = sum((2 ** r[6]) ** 2 * r[0] ** 2 for r in rows) / len(rows)
        print("SUMMARY E[c_n^2 Var] = %.3e ; diagonal part E[c_n^2 Z chi^2] = %.3e ; CS bound E[c_n^2 Z^2 chi^2] = %.3e ; "
              "E[M_n^2] = %.4f" % (inc, incdiag, incCS, m2))


if __name__ == "__main__":
    main()
