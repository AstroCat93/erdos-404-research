#!/usr/bin/env python3
"""check_assemble.py -- independent re-implementation (shares no code with assemble.py / early_phase.py) of the
explicit part of Theorem M (M4C report, sections 6-7): phase 1 and the phase-2 windows with b_{l-1} <= BCUT.

Everything is exact rational arithmetic (fractions.Fraction); logarithms are taken only at the very end.
It recomputes from the report's text alone:
  * q1, q2, q3 by its own dictionary DP;
  * the greedy phase-1 schedule and the conditions (6.1);
  * the phase-2 rule for s_l and b_{l+1} (eta = 1/20, gamma = 8/5 exactly), (T1), (T2), N >= p;
  * mu_A(G_l^c) <= floor(b_{l+1}/p^2) p^{-(s-2)} and the bound B_l of Lemma T, term by term;
and prints sum_l [mu(G^c) + sqrt(B_l)] and log prod (1+ebar) (incl. q1) over this explicit part, to be compared
with the line "phase 2 explicit part: ... delta so far <= ...; log Pi so far <= ..." of assemble.py.
usage: check_assemble.py p [BCUT]
"""
import sys
from fractions import Fraction
from math import factorial

import mpmath as mp

mp.mp.dps = 50


def val(n, p):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def consts(p):
    H = [Fraction(0)]
    for r in range(1, p):
        H.append(H[-1] + Fraction(1, r))
    Hm = [h.numerator * pow(h.denominator, -1, p) % p for h in H]
    law1 = {0: 1}
    law2 = {(0, 0): 1}
    law3 = {0: 1}
    m3 = p ** 3
    for r in range(p):
        f = factorial(r)
        F = 1
        for s in range(1, r + 1):
            F *= (s - p)
        new1, new2, new3 = {}, {}, {}
        for d, w in ((0, 2), (1, 1), (-1, 1)):
            for a, c in law1.items():
                k = (a + d * f) % p
                new1[k] = new1.get(k, 0) + c * w
            for (a, b), c in law2.items():
                k = ((a + d * f) % (p * p), (b + d * f * Hm[r]) % p)
                new2[k] = new2.get(k, 0) + c * w
            for a, c in law3.items():
                k = (a + d * F) % m3
                new3[k] = new3.get(k, 0) + c * w
        law1, law2, law3 = new1, new2, new3
    folded = {}
    for (a, b), c in law2.items():
        k = (a % p, (a // p - b) % p)
        folded[k] = folded.get(k, 0) + c
    W = 4 ** p
    return (Fraction(p * max(law1.values()), W), Fraction(p * p * max(folded.values()), W),
            Fraction(m3 * max(law3.values()), W))


def main():
    p = int(sys.argv[1])
    BCUT = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    eta = Fraction(1, 20)
    gamma = Fraction(8, 5)
    q1, q2, q3 = consts(p)
    print(f"# check_assemble p={p} BCUT={BCUT}: q1-1={float(q1-1):.6e} q2-1={float(q2-1):.6e} q3={float(q3):.9f}")

    def dep(j):          # deterministic depth bound of gate j on A: exact for p^2 ∤ j, lower value 3 for p^2 | j
        return 3 if j % (p * p) == 0 else 1 + val(j, p)

    # ---- phase 1: (6.1) with exact depths (all b < p^2)
    def Vb(b):
        return sum(1 + val(j, p) for j in range(1, b + 1))

    def Mx(b):
        return max(1 + val(j, p) for j in range(1, b + 1))

    def ok61(bm, bp):
        return Vb(bp) - Vb(bm) <= Vb(bm) - Mx(bp) and Mx(bp) < Vb(bm)

    b = [3, 4]
    while True:
        cands = [c for c in range(b[-1] + 1, min(2 * b[-2], p * p - 1) + 1) if ok61(b[-2], c)]
        if not cands:
            break
        b.append(max(cands))
    k0 = len(b) - 2
    logPi = mp.log(mp.mpf(q1.numerator) / q1.denominator)
    for k in range(1, k0 + 1):
        n1 = sum(1 for j in range(b[k - 1] + 1, b[k + 1] + 1) if val(j, p) == 0)
        n2 = sum(1 for j in range(b[k - 1] + 1, b[k + 1] + 1) if val(j, p) == 1)
        e = q1 ** n1 * q2 ** n2
        logPi += mp.log(mp.mpf(e.numerator) / e.denominator)
    print(f"phase 1 schedule {b} (k0={k0}); log Pi_phase1 = {mp.nstr(logPi, 12)}")

    # ---- phase 2 explicit part
    def Xi(U, s):
        return sum(-(-U // p ** a) for a in range(1, s - 2)) if U > 0 else 0

    def T1(bm, N, s):
        U = -(-N // (p * p))
        return N + -(-N // p) + U + Xi(U, s) + s <= bm + bm // p

    delta = Fraction(0)
    deltaf = mp.mpf(0)
    l = k0 + 1
    while b[l - 1] <= BCUT:
        bm, bk = b[l - 1], b[l]
        s = 3
        while Fraction((2 * bm) // (p * p), p ** (s - 2)) > eta / 2 ** (l - k0):
            s += 1
        tmax = max(c for c in range(bk + 1, 2 * bm + 1) if T1(bm, c - bm, s))
        cap = bk + -(-(gamma * (bk - bm)).numerator // (gamma * (bk - bm)).denominator)
        bp = min(tmax, cap)
        assert bp > bk
        b.append(bp)
        N, NW = bp - bm, bk - bm
        assert NW >= 2 * s + 2 and N >= p
        muG = Fraction(bp // (p * p), p ** (s - 2))
        # Lemma T, term by term
        js = list(range(bm + 1, bp + 1))
        V0 = [0]
        Uc = [0]
        for j in js:
            V0.append(V0[-1] + dep(j))
            Uc.append(Uc[-1] + (1 if j % (p * p) == 0 else 0))
        Vp = [V0[i] + Xi(Uc[i], s) for i in range(N + 1)]
        Dm = V0[NW]
        h = -(-Dm // 2)
        I = max(i for i in range(N) if Vp[i] < h)
        n1 = sum(1 for j in js if val(j, p) == 0)
        n2 = sum(1 for j in js if val(j, p) == 1)
        U = Uc[N]
        C = q1 ** n1 * q2 ** n2 * q3 ** U * p ** Xi(U, s)
        rho = q2 / p
        S = Fraction(0)
        for j0 in range(N):
            nu = sum(1 for i in range(j0 + 1, I + 1) if (bm + i + 1) % p != 0)
            S += Fraction(p ** Vp[j0 + 1], 2 ** (j0 * p)) * rho ** nu
        Bfr = Fraction(p ** Vp[N], 2 ** (N * p)) + C * S
        Bm = mp.mpf(Bfr.numerator) / Bfr.denominator
        eb = mp.sqrt(Bm)
        delta += muG
        deltaf += eb
        logPi += mp.log(1 + eb)
        print(f"  l={l} ({bm},{bk},{bp}] s={s} N_W={NW} N={N} I={I} mu(G^c)={float(muG):.4g} "
              f"log10 B={mp.nstr(mp.log10(Bm), 8)}")
        l += 1
    tot = mp.mpf(delta.numerator) / delta.denominator + deltaf
    print(f"CHECK p={p}: explicit part up to window l={l-1}, b_(l-1)={b[l-1]}: delta = {mp.nstr(tot, 12)}; "
          f"log Pi = {mp.nstr(logPi, 12)}")

    # ---- far tail (b_{l+1} = floor(5 b_l / 4)) up to b_{l-1} = 10^60, own implementation (log domain, mpmath)
    lp, l2 = mp.log(p), mp.log(2)
    lq1, lq2, lq3 = (mp.log(mp.mpf(q.numerator) / q.denominator) for q in (q1, q2, q3))
    lrho = lq2 - lp
    alpha = Fraction(1) + Fraction(1, p) + Fraction(1, p * p) + Fraction(1, p * p * (p - 1))
    aM = mp.mpf(alpha.numerator) / alpha.denominator
    r1 = mp.e ** (-p * l2 + aM * lp - (1 - mp.mpf(1) / p) * lrho)
    assert r1 < 1

    def logT_exact(bm, bk, bp, s):       # Lemma T, term by term, in logs (suffix counts for nu)
        N, NW = bp - bm, bk - bm
        V0, Uc = [0], [0]
        for j in range(bm + 1, bp + 1):
            V0.append(V0[-1] + dep(j))
            Uc.append(Uc[-1] + (1 if j % (p * p) == 0 else 0))
        Vp = [V0[i] + Xi(Uc[i], s) for i in range(N + 1)]
        h = -(-V0[NW] // 2)
        I = max(i for i in range(N) if Vp[i] < h)
        n1 = sum(1 for j in range(bm + 1, bp + 1) if j % p)
        n2 = sum(1 for j in range(bm + 1, bp + 1) if j % p == 0 and j % (p * p))
        logC = n1 * lq1 + n2 * lq2 + Uc[N] * lq3 + Xi(Uc[N], s) * lp
        nu = [0] * (N + 1)                # nu[j0] = #{i in (j0, I]: p does not divide bm+i+1}
        for j0 in range(N - 1, -1, -1):
            i = j0 + 1
            nu[j0] = nu[j0 + 1] + (1 if (i <= I and (bm + i + 1) % p) else 0) if j0 + 1 <= N else 0
        logs = [-N * p * l2 + Vp[N] * lp] + [-j0 * p * l2 + Vp[j0 + 1] * lp + logC + nu[j0] * lrho for j0 in range(N)]
        m = max(logs)
        return m + mp.log(mp.fsum(mp.e ** (t - m) for t in logs))

    def logT_closed(bm, bk, bp, s):      # Lemma T' with the constant 1/(1-r1)
        N, NW = bp - bm, bk - bm
        num = -(-NW // 2) - s
        Ip = max(0, -(-(num * alpha.denominator) // alpha.numerator) - 1) if num > 0 else 0
        U = -(-N // (p * p))
        t1 = -N * p * l2 + (aM * N + s) * lp
        t2 = (-mp.log(1 - r1) + N * lq1 + (-(-N // p)) * lq2 + U * lq3 + Xi(U, s) * lp + (aM + s) * lp
              + (Ip * (1 - mp.mpf(1) / p) - 1) * lrho)
        m = max(t1, t2)
        return m + mp.log(mp.e ** (t1 - m) + mp.e ** (t2 - m))

    b = b[:l + 1]
    farG = Fraction(0)
    farB = mp.mpf(0)
    while b[l - 1] <= 10 ** 60:
        bm, bk = b[l - 1], b[l]
        s = 3
        while Fraction((2 * bm) // (p * p), p ** (s - 2)) > eta / 2 ** (l - k0):
            s += 1
        bp = 5 * bk // 4
        b.append(bp)
        N, NW = bp - bm, bk - bm
        assert T1(bm, N, s) and NW >= 2 * s + 2 and N >= p and bp <= 2 * bm
        farG += Fraction(bp // (p * p), p ** (s - 2))
        lb = logT_exact(bm, bk, bp, s) if N <= 6000 else logT_closed(bm, bk, bp, s)
        eb = mp.e ** (lb / 2)
        farB += eb
        logPi += mp.log(1 + eb)
        l += 1
    remG = eta / 2 ** (l - k0 - 1)
    dtot = tot + mp.mpf(farG.numerator) / farG.denominator + farB + mp.mpf(remG.numerator) / remG.denominator \
        + mp.mpf(10) ** -1000
    logPi += mp.mpf(10) ** -1000
    Pi = mp.e ** logPi
    c = (1 - mp.sqrt(Pi * dtot)) ** 2 / Pi
    print(f"CHECK p={p}: far tail up to l={l-1} (l_*-k0 = {l-k0}): mu(G^c) part {float(farG):.6e}, sqrt(B) part "
          f"{mp.nstr(farB, 4)}, remainder {float(remG):.3e}")
    print(f"CHECK p={p}: Pi_A = {mp.nstr(Pi, 15)}; delta_A = {mp.nstr(dtot, 10)}; c_p = {mp.nstr(c, 10)}")


if __name__ == "__main__":
    main()
