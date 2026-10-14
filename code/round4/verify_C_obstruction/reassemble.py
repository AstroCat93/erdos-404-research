#!/usr/bin/env python3
"""reassemble.py -- third, independent re-implementation (by the obstruction verifier, sharing no code with
code/round4/M4C/) of the assembly of M4C's Theorem M, from the text of data/round4/reports/M4C.md sections 6-7.

For one prime p it builds the window schedule n_k = b_k p, and evaluates
  Pi_A    = q1 * prod_k (1 + ebar_k),
  delta_A = sum_{k > k0} [ floor(b_{k+1}/p^2) p^{-(s_k-2)} + sqrt(Bfr_k) ] + eta 2^{-(l*-k0)+1} + 1e-1000,
  c_p     = (1 - sqrt(Pi_A delta_A))^2 / Pi_A,
with
  phase 1 (greedy (6.1), all blocks < p^2):  ebar_k = q1^{n1} q2^{n2} - 1      (Prop P1, pointwise on A);
  phase 2 (b_{k-1} <= 3000):  s-rule, b_{k+1} = min(max{b <= 2 b_{k-1}: (T1)}, b_k + ceil(1.6 (b_k - b_{k-1})));
  far tail (3000 < b_{k-1} <= 10^60):  b_{k+1} = floor(5 b_k / 4);
  Bfr_k = Lemma T bound for N <= 6000, Lemma T' closed form otherwise; ebar_k = sqrt(Bfr_k).
All of this is done in natural logarithms with float64 (sufficient for 4 printed digits); integer conditions
((6.1), (T1), (T2), N >= p, the s-rule) are decided exactly in integers.

It also prints the obstruction data used in the report data/round4/checks/M4C_obstruction.md:
  * the phase-1 thresholds ebar_k (pointwise bounds; they do not decay);
  * the first window l* whose SECOND half (b_l, b_{l+1}] contains a p^2-multiple j (random-depth gate on A),
    with D, K_det (K with that gate's depth set to 3), N p, for Proposition O1' (untruncated mean is +infinity).
q-constants are read from the Fourier values of qfourier.py (passed on the command line) and inflated by a
relative 1e-9 on q-1.
usage: reassemble.py p q1m1 q2m1 q3m1 [greedy_cap]   (greedy_cap=1: also require b_{k+1} <= 2 b_{k-1} in phase 1)
"""
import math
import sys


def vp(n, p):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def cdiv(a, b):
    return -(-a // b)


def Xi(U, p, s):
    return sum(cdiv(U, p ** a) for a in range(1, s - 2)) if U > 0 else 0


def lse(xs):
    m = max(xs)
    return m + math.log(sum(math.exp(x - m) for x in xs))


def main():
    p = int(sys.argv[1])
    q1m1, q2m1, q3m1 = (float(a) * (1 + 1e-9) for a in sys.argv[2:5])
    cap = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    lq1, lq2, lq3 = math.log1p(q1m1), math.log1p(q2m1), math.log1p(q3m1)
    lp, l2 = math.log(p), math.log(2)
    eta_num, eta_den = 1, 20          # eta = 0.05
    gamma_num, gamma_den = 8, 5       # gamma = 1.6
    BCUT = 3000
    P2 = p * p

    def d1(j):                         # depth on A for j < p^2 (Lemma 5.1)
        return 1 + vp(j, p)

    def Vb(b):
        return sum(d1(j) for j in range(1, b + 1))

    def Mxb(b):
        return max(d1(j) for j in range(1, b + 1))

    # ---------------- phase 1
    b = [3, 4]
    while True:
        bm, bk = b[-2], b[-1]
        hi = min(2 * bm, P2 - 1) if cap else P2 - 1
        best = None
        for c in range(bk + 1, hi + 1):
            if Vb(c) - Vb(bm) <= Vb(bm) - Mxb(c) and Mxb(c) < Vb(bm):
                best = c
        if best is None:
            break
        b.append(best)
    k0 = len(b) - 2
    logPi = lq1
    ebars1 = []
    for k in range(1, k0 + 1):
        n1 = sum(1 for j in range(b[k - 1] + 1, b[k + 1] + 1) if d1(j) == 1)
        n2 = sum(1 for j in range(b[k - 1] + 1, b[k + 1] + 1) if d1(j) == 2)
        lg = n1 * lq1 + n2 * lq2
        logPi += lg
        ebars1.append(math.expm1(lg))
    print(f"p={p} phase1 blocks={b} k0={k0} logPi_phase1(incl q1)={logPi:.10g}")
    print("  phase-1 ebar_k: " + " ".join(f"{e:.3e}" for e in ebars1))

    # ---------------- phase 2 helpers
    def T1(bm, N, s):
        U = cdiv(N, P2)
        K = N + cdiv(N, p) + U + Xi(U, p, s)
        return K + s <= bm + bm // p

    def s_rule(bm, l):
        cnt = (2 * bm) // P2
        s = 3
        # cnt p^{-(s-2)} <= eta 2^{-(l-k0)}  <=>  cnt * 2^{l-k0} * eta_den <= eta_num * p^{s-2}
        while cnt * 2 ** (l - k0) * eta_den > eta_num * p ** (s - 2):
            s += 1
        return s

    lrho = lq2 - lp

    def lemmaT(bm, bk, bp, s):
        N, NW = bp - bm, bk - bm
        d0, ism = [], []
        for i in range(1, N + 1):
            j = bm + i
            if j % P2 == 0:
                d0.append(3); ism.append(1)
            else:
                d0.append(1 + vp(j, p)); ism.append(0)
        V0 = [0]; U = [0]
        for i in range(N):
            V0.append(V0[-1] + d0[i]); U.append(U[-1] + ism[i])
        Vp = [V0[i] + Xi(U[i], p, s) for i in range(N + 1)]
        Dm = V0[NW]
        half = cdiv(Dm, 2)
        I = max(i for i in range(N) if Vp[i] < half)
        n1 = sum(1 for j in range(bm + 1, bp + 1) if j % p)
        n2 = sum(1 for j in range(bm + 1, bp + 1) if j % p == 0 and j % P2)
        Uw = sum(1 for j in range(bm + 1, bp + 1) if j % P2 == 0)
        logQ = n1 * lq1 + n2 * lq2 + Uw * lq3 + Xi(Uw, p, s) * lp
        # nu(j0) = #{i in (j0, I]: p does not divide bm+i+1}
        # suffix counts: cnt[i] = #{i' in [i, I]: p does not divide bm+i'+1}
        cnt = [0] * (N + 2)
        for i in range(N - 1, -1, -1):
            cnt[i] = cnt[i + 1] + (1 if (i <= I and (bm + i + 1) % p) else 0)
        terms = []
        for j0 in range(N):
            nu = cnt[j0 + 1]
            terms.append(-j0 * p * l2 + Vp[j0 + 1] * lp + nu * lrho)
        logB = lse([-N * p * l2 + Vp[N] * lp, logQ + lse(terms)])
        return logB, I

    alpha = 1 + 1 / p + 1 / P2 + 1 / (P2 * (p - 1))
    r1 = math.exp(-p * l2 + alpha * lp - (1 - 1 / p) * lrho)
    assert r1 < 1 and lrho < 0

    def lemmaTprime(bm, bk, bp, s):
        N, NW = bp - bm, bk - bm
        num = cdiv(NW, 2) - s
        Ilow = max(0, math.ceil(num / alpha) - 1) if num > 0 else 0
        U = cdiv(N, P2)
        logC = N * lq1 + cdiv(N, p) * lq2 + U * lq3 + Xi(U, p, s) * lp
        t1 = -N * p * l2 + (alpha * N + s) * lp
        t2 = -math.log1p(-r1) + logC + (alpha + s) * lp + (Ilow * (1 - 1 / p) - 1) * lrho
        return lse([t1, t2]), Ilow

    delta = 0.0
    sum_muG = 0.0
    sum_mark = 0.0
    l = k0 + 1
    lstar = None
    nexp = 0
    while True:
        bm, bk = b[l - 1], b[l]
        if bm > 10 ** 60:
            break
        s = s_rule(bm, l)
        if bm <= BCUT:
            best = None
            for c in range(bk + 1, 2 * bm + 1):
                if T1(bm, c - bm, s):
                    best = c
            assert best is not None, f"schedule infeasible at l={l}"
            bp = min(best, bk + cdiv(gamma_num * (bk - bm), gamma_den))
            assert bp > bk
        else:
            bp = (5 * bk) // 4
            assert T1(bm, bp - bm, s), f"T1 fails at l={l}"
        N, NW = bp - bm, bk - bm
        assert NW >= 2 * s + 2, f"T2 fails at l={l}"
        assert N >= p
        b.append(bp)
        # obstruction data: first window whose second half contains a p^2-multiple
        if lstar is None and any(j % P2 == 0 for j in range(bk + 1, bp + 1)):
            firsthalf = any(j % P2 == 0 for j in range(bm + 1, bk + 1))
            D = sum((3 if j % P2 == 0 else 1 + vp(j, p)) for j in range(bm + 1, bk + 1))
            Kdet = sum((3 if j % P2 == 0 else 1 + vp(j, p)) for j in range(bm + 1, bp + 1))
            mults = [j for j in range(bk + 1, bp + 1) if j % P2 == 0]
            lstar = (l, bm, bk, bp, D, Kdet, N * p, mults, firsthalf, s)
        muGc = (bp // P2) * float(p) ** (-(s - 2))
        if N <= 6000:
            logB, I = lemmaT(bm, bk, bp, s)
        else:
            logB, I = lemmaTprime(bm, bk, bp, s)
        ebar = math.exp(logB / 2) if logB / 2 > -745 else 0.0
        delta += muGc + ebar
        sum_muG += muGc
        sum_mark += ebar
        logPi += math.log1p(ebar)
        if nexp < 14:
            print(f"  l={l} ({bm},{bk},{bp}] s={s} N_W={NW} N={N} I={I}: muGc={muGc:.4g} logB={logB:.6g} ebar={ebar:.4g}")
        nexp += 1
        l += 1
    rem = 0.05 * 2.0 ** (-(l - k0) + 1) + 0.0
    delta_tot = delta + rem
    Pi = math.exp(logPi)
    prod = Pi * delta_tot
    cp = (1 - math.sqrt(prod)) ** 2 / Pi if prod < 1 else float("nan")
    print(f"  delta breakdown: deep-gate truncation sum mu_A(G^c) = {sum_muG:.6g}; Markov terms sum sqrt(Bfr) = {sum_mark:.6g}")
    print(f"  windows evaluated after phase 1: {l - k0 - 1} (l*-k0 = {l - k0}); remainder eta 2^-(l*-k0)+1 = {rem:.3g}")
    L = lstar
    print(f"  OBSTRUCTION l*={L[0]} composite blocks ({L[1]},{L[2]},{L[3]}]: p^2-multiples in 2nd half {L[7]}, "
          f"also in 1st half: {L[8]}; D={L[4]} K_det={L[5]} Np={L[6]} s_cap={L[9]}; "
          f"delta=0 term 2^-Np p^K exceeds p^D once v(xi'+u) >= {math.ceil(L[6]*l2/lp - (L[5]-L[4]))}")
    print(f"RESULT p={p}: logPi={logPi:.6g} Pi={Pi:.10g} delta={delta_tot:.10g} Pi*delta={prod:.8g} c_p={cp:.8g} "
          f"mu(K_p)>={cp / p**3:.6g}")


if __name__ == "__main__":
    main()
