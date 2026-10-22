#!/usr/bin/env python3
"""twowin_check.py -- exact test of the one-window Fourier bound (Lemma R3M-C1) and of the
two-window variance inequality (Proposition R3M-C2) for the slope-0 population at odd p.

x random in Z_p; times n < N = n+H < N2 = N+H2; m = V_n, D = V_N - m, D2 = V_N2 - V_N;
hypothesis checked: D + D2 <= m - M_{N2} (implies all linear-regime conditions used).
Parents: slope-0 paths alive at n.  For every w mod p^(D+D2), x_w = x0 + p^m w + (digits >= m+D+D2 of x):
   Z1(w) = #{(e,f) alive at N},  Z2(w) = #{(e,f,f2) alive at N2},   computed by direct evaluation;
   targets of the (e,f) mod p^D2 for the Fourier bound.
Normalisers c_t = 2^-t p^{V_t}.  Tested (exact rationals unless noted):
   (mart)  c_N E_w Z1 = c_N2 E_w Z2 = c_n Z0;
   (C1)    for every xi in p^-D2 Z/Z:  E_w |c_N sum_(e,f) e(xi tau)|^2 <= (c_n Z0)^2 F(xi)   [floating point],
           F(xi) = sum_{theta: p^D theta = xi/u} |muhat_W(theta)|^2,  u = pi_N/(p^D pi_n) mod p^D2;
   (C2)    c_N2^2 E_w Z2^2 - c_N^2 E_w Z1^2 <= eps * (c_n Z0)^2,
           eps = p^(D+D2) Coll_(D+D2) - p^D Coll_D of the composite window [n, N2)   [exact];
   also prints the ratio (C2 lhs)/(eps M_n^2) and the CS-type quantity chi^2 of the second window.
usage: twowin_check.py p SEED NX n H H2 [KMAX]
"""
import cmath
import random
import sys
from fractions import Fraction

PREC = 100


def vp(a, p):
    if a == 0:
        return PREC
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def coll(elems, p, K):
    """Sum_r nu(r)^2 for the uniform subset-sum law of elems mod p^K (exact Fraction)."""
    mod = p ** K
    dist = {0: 1}
    for y in elems:
        y %= mod
        new = dict(dist)
        for r, c in dist.items():
            r2 = (r + y) % mod
            new[r2] = new.get(r2, 0) + c
        dist = new
    T = 2 ** len(elems)
    return Fraction(sum(c * c for c in dist.values()), T * T)


def main():
    p, seed, NX, n, H, H2 = (int(a) for a in sys.argv[1:7])
    KMAX = int(sys.argv[7]) if len(sys.argv) > 7 else 5
    N, N2 = n + H, n + H + H2
    MOD = p ** PREC
    rnd = random.Random(seed)
    done = tries = 0
    nC1 = okC1 = okC2 = okM = 0
    worst = 0.0
    while done < NX and tries < 200000:
        tries += 1
        x = rnd.randrange(MOD)
        vs = [vp((x + i) % MOD, p) for i in range(1, N2 + 1)]
        m = sum(vs[:n]); D = sum(vs[n:N]); D2 = sum(vs[N:N2])
        Mn = max(vs)
        if D < 1 or D2 < 1 or D + D2 > KMAX or D + D2 > m - Mn:
            continue

        def table(xx, upto):
            P = [1]; dP = [0]
            for j in range(1, upto + 1):
                dP.append((dP[-1] * (xx + j) + P[-1]) % MOD)
                P.append(P[-1] * (xx + j) % MOD)
            return P, dP

        P, dP = table(x, N2)
        Vpre = [0]
        for v in vs:
            Vpre.append(Vpre[-1] + v)
        parents = []
        stack = [(1, (1,), 1, 0)]
        while stack:
            j, bits, S, Sd = stack.pop()
            if vp(S % MOD, p) < Vpre[j]:
                continue
            if j == n:
                if Sd % p:
                    parents.append(bits)
                continue
            stack.append((j + 1, bits + (0,), S, Sd))
            stack.append((j + 1, bits + (1,), (S + P[j]) % MOD, (Sd + dP[j]) % MOD))
        if not parents:
            continue
        done += 1
        Z0 = len(parents)
        x0 = x % p ** m
        hi = x - x % p ** (m + D + D2)
        K = D + D2
        W = p ** K
        sumZ1 = sumZ2 = sumZ1sq = sumZ2sq = 0
        pD2 = p ** D2
        # Fourier accumulators: for each xi index a (xi = a/p^D2), E_w |sum e(a tau/p^D2)|^2
        four = [0.0] * pD2
        VN, VN2 = m + D, m + D + D2
        for w in range(W):
            xw = x0 + p ** m * w + hi
            Pw, _ = table(xw, N2)
            q1 = [0]
            for k in range(H):
                q1 = q1 + [(s + Pw[n + k]) % MOD for s in q1]
            q2 = [0]
            for k in range(H2):
                q2 = q2 + [(s + Pw[N + k]) % MOD for s in q2]
            invN = pow((Pw[N] // p ** VN) % MOD, -1, MOD)
            z1 = z2 = 0
            taus = []
            for e in parents:
                Se = sum(Pw[j] for j in range(n) if e[j]) % MOD
                for s in q1:
                    S1 = (Se + s) % MOD
                    if vp(S1, p) < VN:
                        continue
                    z1 += 1
                    taus.append(((-(S1 // p ** VN)) * invN) % pD2)
                    for s2 in q2:
                        if vp((S1 + s2) % MOD, p) >= VN2:
                            z2 += 1
            sumZ1 += z1; sumZ2 += z2; sumZ1sq += z1 * z1; sumZ2sq += z2 * z2
            for a in range(pD2):
                acc = sum(cmath.exp(2j * cmath.pi * a * t / pD2) for t in taus)
                four[a] += abs(acc) ** 2
        cn = Fraction(p ** m, 2 ** n); cN = Fraction(p ** VN, 2 ** N); cN2 = Fraction(p ** VN2, 2 ** N2)
        M0 = cn * Z0
        mart = (cN * Fraction(sumZ1, W) == M0) and (cN2 * Fraction(sumZ2, W) == M0)
        okM += mart
        lhs2 = cN2 ** 2 * Fraction(sumZ2sq, W) - cN ** 2 * Fraction(sumZ1sq, W)
        # composite window elements y_j = pi_j/pi_n at x, j in [n, N2)
        comp = []
        y = 1
        for k in range(H + H2):
            comp.append(y)
            y = y * (x + n + k + 1) % MOD
        eps = p ** K * coll(comp, p, K) - p ** D * coll(comp, p, D)
        c2 = lhs2 <= eps * M0 * M0
        okC2 += c2
        # C1: F(xi) from window W=[n,N) at x
        u = (P[N] * pow((P[n] // p ** m) % MOD, -1, MOD) // p ** D) if False else None
        # u = pi_N/(p^D pi_n) mod p^D2, computed from the integer product (x+n+1)...(x+N)
        prod = 1
        for k in range(n + 1, N + 1):
            prod *= (x + k)
        u = (prod // p ** D) % pD2
        uinv = pow(u, -1, pD2)
        qW = [0]
        y = 1
        for k in range(H):
            qW = qW + [(s + y) % p ** K for s in qW]
            y = y * (x + n + k + 1)
        T = 2 ** H
        for a in range(pD2):
            classes = {}
            for qf in qW:
                r = qf % p ** D
                hiq = (qf - r) // p ** D  # digits D..K-1
                classes.setdefault(r, 0)
                classes[r] += cmath.exp(2j * cmath.pi * a * hiq * uinv / pD2)
            F = p ** D * sum(abs(v) ** 2 for v in classes.values()) / T ** 2
            lhs1 = float(cN) ** 2 * four[a] / W
            rhs1 = float(M0) ** 2 * F
            nC1 += 1
            ok1 = lhs1 <= rhs1 * (1 + 1e-9) + 1e-15
            okC1 += ok1
            if not ok1:
                print("FAIL C1", a, lhs1, rhs1)
        ratio = float(lhs2 / (eps * M0 * M0)) if eps > 0 else float('nan')
        worst = max(worst, ratio if ratio == ratio else 0)
        print(f"x#{done}: m={m} D={D} D2={D2} Z0={Z0} mart={mart} C2: lhs={float(lhs2):.3e} eps*M^2={float(eps*M0*M0):.3e} "
              f"ratio={ratio:.4f} eps={float(eps):.4f}", flush=True)
    print(f"RESULT p={p} n={n} H={H} H2={H2}: martingale exact {okM}/{done}; C1 bounds {okC1}/{nC1}; "
          f"C2 inequality {okC2}/{done}; max ratio lhs/(eps M^2) = {worst:.4f}")


if __name__ == "__main__":
    main()
