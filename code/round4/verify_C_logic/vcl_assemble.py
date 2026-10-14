#!/usr/bin/env python3
"""vcl_assemble.py -- independent re-derivation (verify_C_logic track) of the numbers in M4C Theorem M (report §§6-7).

Written from the report text only; shares no code with code/round4/M4C/.  Constants q1,q2,q3 come from vcl_q.py
(exact rationals).  Real arithmetic: mpmath at 50 digits; every quantity that is an upper bound is multiplied by
UP = 1 + 1e-30 after evaluation (rounding errors are below 1e-45 relative); q's are rounded up first.

Steps (report numbering):
  phase 1  (Prop P1): greedy b_{k+1} = largest c <= p^2-1 with (6.1); Pi_1 = q1 * prod_k q1^{n1} q2^{n2}.
  phase 2  (Thm M proof): s_k = least s >= 3 with floor(2 b_{k-1}/p^2) p^{-(s-2)} <= eta 2^{-(k-k0)};
           b_{k+1} = min( max{b <= 2 b_{k-1} : (T1)}, b_k + ceil(gamma (b_k - b_{k-1})) ), while b_{k-1} <= 3000;
           checks (T1), (T2), N >= p; mu(G^c) <= floor(b_{k+1}/p^2) p^{-(s-2)} (Lemma L(a));
           Bfr = Lemma T bound (term by term); ebar = sqrt(Bfr).
  far tail (b_{k-1} > 3000, up to 10^60): b_{k+1} = floor(5 b_k / 4); Lemma T if N <= 6000, else Lemma T'.
  remainder (b_{k-1} > 10^60): explicit analytic bound derived in the check report (§ far tail), evaluated here:
           sum mu(G^c) <= eta 2^{-(l*-k0)+1}; sum sqrt(Bfr) and sum log(1+ebar) bounded via an explicit
           linear-minus-log majorant of log Bfr (see function remainder()).
  result   c_p = (1 - sqrt(Pi_A delta_A))^2 / Pi_A with Pi_A, delta_A upper bounds.
usage: vcl_assemble.py p [eta_num/eta_den] [BCUT] [gamma_num/gamma_den]
"""
import sys
from fractions import Fraction

import mpmath as mp

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from vcl_q import q1 as Q1, q2 as Q2, q3 as Q3  # noqa: E402

mp.mp.dps = 50
UP = 1 + mp.mpf(10) ** -30


def up(fr):
    return mp.mpf(fr.numerator) / mp.mpf(fr.denominator) * UP


def vp(n, p):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def cdiv(a, b):
    return -(-a // b)


def Xi(U, p, s):
    # sum_{a=1}^{s-3} ceil(U/p^a)
    return sum(cdiv(U, p ** a) for a in range(1, s - 2)) if U > 0 else 0


def depth_phase1(j, p):
    assert j % (p * p) != 0
    return 1 + vp(j, p)


def phase1(p):
    """greedy schedule from (6.1); every block index < p^2 so depths are deterministic (Lemma 5.1)."""
    Vc = [0]
    Mc = [0]
    for j in range(1, p * p):
        d = depth_phase1(j, p)
        Vc.append(Vc[-1] + d)
        Mc.append(max(Mc[-1], d))
    b = [3, 4]
    while True:
        bm, bk = b[-2], b[-1]
        cand = [c for c in range(bk + 1, p * p) if (Vc[c] - Vc[bm] <= Vc[bm] - Mc[c]) and Mc[c] < Vc[bm]]
        if not cand:
            break
        b.append(max(cand))
    return b, Vc


def lemmaT_bound(p, bm, bk, bp, s, lq1, lq2, lq3):
    """log of the Lemma T bound B_l (upper bound), following the report's definitions literally."""
    N = bp - bm
    NW = bk - bm
    lp = mp.log(p)
    d0 = [None]  # 1-based
    pm2 = []
    for i in range(1, N + 1):
        j = bm + i
        if j % (p * p) == 0:
            d0.append(3)
            pm2.append(1)
        else:
            d0.append(1 + vp(j, p))
            pm2.append(0)
    V0 = [0] * (N + 1)
    Ui = [0] * (N + 1)
    for i in range(1, N + 1):
        V0[i] = V0[i - 1] + d0[i]
        Ui[i] = Ui[i - 1] + pm2[i - 1]
    Vplus = [V0[i] + Xi(Ui[i], p, s) for i in range(N + 1)]
    Dminus = V0[NW]
    hD = cdiv(Dminus, 2)
    I = max(i for i in range(0, N) if Vplus[i] < hD)
    n1 = sum(1 for i in range(1, N + 1) if d0[i] == 1)
    n2 = sum(1 for i in range(1, N + 1) if d0[i] == 2)
    U = Ui[N]

    def nu(j0):
        # #{ i in (j0, I] : p does not divide b_{l-1} + i + 1 }
        return sum(1 for i in range(j0 + 1, I + 1) if (bm + i + 1) % p != 0)

    logC = n1 * lq1 + n2 * lq2 + U * lq3 + Xi(U, p, s) * lp
    lrho = lq2 - lp
    logs = [-(j0 * p) * mp.log(2) + Vplus[j0 + 1] * lp + nu(j0) * lrho for j0 in range(N)]
    m = max(logs)
    lsum = m + mp.log(mp.fsum(mp.exp(t - m) for t in logs))
    t1 = -(N * p) * mp.log(2) + Vplus[N] * lp
    t2 = logC + lsum
    mm = max(t1, t2)
    return mm + mp.log(mp.exp(t1 - mm) + mp.exp(t2 - mm)), dict(N=N, NW=NW, I=I, n1=n1, n2=n2, U=U)


def lemmaTprime_bound(p, N, NW, s, lq1, lq2, lq3):
    lp = mp.log(p)
    alpha = Fraction(1) + Fraction(1, p) + Fraction(1, p * p) + Fraction(1, p * p * (p - 1))
    a = mp.mpf(alpha.numerator) / alpha.denominator
    lrho = lq2 - lp
    lr1 = -p * mp.log(2) + a * lp - (1 - mp.mpf(1) / p) * lrho
    r1 = mp.exp(lr1)
    assert r1 < 1 and lrho < 0
    num = cdiv(NW, 2) - s
    Ip = max(0, cdiv(num * alpha.denominator, alpha.numerator) - 1) if num > 0 else 0
    U = cdiv(N, p * p)
    t1 = -(N * p) * mp.log(2) + (a * N + s) * lp
    t2 = (-mp.log(1 - r1) + N * lq1 + cdiv(N, p) * lq2 + U * lq3 + Xi(U, p, s) * lp + (a + s) * lp
          + (Ip * (1 - mp.mpf(1) / p) - 1) * lrho)
    mm = max(t1, t2)
    return mm + mp.log(mp.exp(t1 - mm) + mp.exp(t2 - mm))


def T1_holds(p, bm, N, s):
    U = cdiv(N, p * p)
    return N + cdiv(N, p) + U + Xi(U, p, s) + s <= bm + bm // p


def s_rule(p, bm, k, k0, eta):
    s = 3
    cnt = (2 * bm) // (p * p)
    while Fraction(cnt, p ** (s - 2)) > eta / 2 ** (k - k0):
        s += 1
    return s


def remainder(p, lq1, lq2, lq3, eta, dl, b_star):
    """Rigorous bound for windows with b_{k-1} >= b_star (= first b_{k-1} > 10^60), k - k0 >= dl.
    For such k (far-tail rule b_{k+1} = floor(5 b_k/4)): b := b_{k-1}; N_W >= b/4 - 1, N <= 9b/16 (+0),
    b_{k-1} >= b_star * 1.2499^{k - l*}, so k - k0 <= dl + log(b/b_star)/log(1.2499);
    s <= S(b) := 4 + log_p(2 b /(p^2 eta)) + (k-k0) log_p 2.
    Returns (log of a bound on sum_k sqrt(Bfr_k), slope a, and the constant pieces)."""
    lp = mp.log(p)
    alpha = Fraction(1) + Fraction(1, p) + Fraction(1, p * p) + Fraction(1, p * p * (p - 1))
    A = mp.mpf(alpha.numerator) / alpha.denominator
    lrho = lq2 - lp
    r1 = mp.exp(-p * mp.log(2) + A * lp - (1 - mp.mpf(1) / p) * lrho)
    g = mp.log(mp.mpf("1.2499"))
    # S(b) <= sA * ln b + sB  for b >= b_star
    sA = 1 / lp + (mp.log(2) / lp) / g
    sB = 4 + (mp.log(2) - 2 * lp - mp.log(mp.mpf(eta.numerator) / eta.denominator)) / lp \
        + (dl - mp.log(b_star) / g) * mp.log(2) / lp
    # log T2 <= -ln(1-r1) + (9b/16+1)[lq1 + lq2/p + lq3/p^2 + lp/(p^2(p-1))] + lq2 + lq3 + lp/(p-1)
    #           + (2s - 3 + A) lp + ([(b/8 - 1/2 - s)/A - 1](1 - 1/p) - 1) lrho
    slopeT2 = mp.mpf(9) / 16 * (lq1 + lq2 / p + lq3 / p ** 2 + lp / (p ** 2 * (p - 1))) + (1 - mp.mpf(1) / p) * lrho / (8 * A)
    # coefficient of s in log T2 bound: 2 lp - (1 - 1/p) lrho / A   (>0)
    cs2 = 2 * lp - (1 - mp.mpf(1) / p) * lrho / A
    c0_2 = (-mp.log(1 - r1) + (lq1 + lq2 / p + lq3 / p ** 2 + lp / (p ** 2 * (p - 1))) + lq2 + lq3 + lp / (p - 1)
            + (A - 3) * lp + ((-mp.mpf(1) / 2 / A - 1) * (1 - mp.mpf(1) / p) - 1) * lrho)
    # log T1 <= (b/4 - 1)(A lp - p ln2) + s lp     (decreasing in N, N >= N_W >= b/4 - 1)
    slopeT1 = (A * lp - p * mp.log(2)) / 4
    c0_1 = -(A * lp - p * mp.log(2))
    cs1 = lp
    assert slopeT2 < 0 and slopeT1 < 0
    # log Bfr <= ln 2 + max(logT1, logT2) <= ln2 + max(slope) * b + max(cs) * S(b) + max(c0)
    slope = max(slopeT1, slopeT2)
    cs = max(cs1, cs2)
    c0 = max(c0_1, c0_2) + mp.log(2)
    # f(b) = slope*b + cs*(sA ln b + sB) + c0 ; claim f(b) <= slope*b/2 for b >= b_star:
    # g(b) = slope*b/2 + cs*sA*ln b + cs*sB + c0 is decreasing for b >= 2 cs sA/|slope|, check g(b_star) <= 0
    assert b_star >= 2 * cs * sA / (-slope)
    gstar = slope * b_star / 2 + cs * sA * mp.log(b_star) + cs * max(sB, 0) + c0
    assert gstar <= 0
    # then sqrt(Bfr_k) <= exp(slope*b_{k-1}/4), b_{k-1} >= b_star*1.2499^m, m = 0,1,...
    # sum <= exp(slope*b_star/4) * sum_m exp(slope*b_star*(1.2499^m - 1)/4) <= 2 exp(slope*b_star/4)
    logsum = slope * b_star / 4 + mp.log(2)
    return logsum, slope, slopeT2


def main():
    p = int(sys.argv[1])
    eta = Fraction(sys.argv[2]) if len(sys.argv) > 2 else Fraction(1, 20)
    BCUT = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
    gamma = Fraction(sys.argv[4]) if len(sys.argv) > 4 else Fraction(8, 5)
    q1, q2, q3 = Q1(p), Q2(p), Q3(p)
    lq1, lq2, lq3 = mp.log(up(q1)), mp.log(up(q2)), mp.log(up(q3))
    lp = mp.log(p)
    # ---------------- phase 1
    b, Vc = phase1(p)
    k0 = len(b) - 2
    assert b[-1] <= p * p - 1
    logPi = lq1                    # 1 + chi^2_{W_0} = q1  (window [3p,4p): elements u! mod p)
    for k in range(1, k0 + 1):
        n1 = sum(1 for j in range(b[k - 1] + 1, b[k + 1] + 1) if depth_phase1(j, p) == 1)
        n2 = sum(1 for j in range(b[k - 1] + 1, b[k + 1] + 1) if depth_phase1(j, p) == 2)
        assert n1 + n2 == b[k + 1] - b[k - 1]
        logPi += n1 * lq1 + n2 * lq2
    logPi1 = logPi
    print(f"# vcl_assemble p={p} eta={eta} BCUT={BCUT} gamma={gamma}")
    print(f"phase 1: b = {b} (k0 = {k0}); log Pi_phase1 (incl. q1) <= {mp.nstr(logPi1 * UP, 12)}")
    # ---------------- phase 2 explicit and far tail
    delta = mp.mpf(0)
    k = k0 + 1
    nexp = 0
    while True:
        bm, bk = b[k - 1], b[k]
        if bm > 10 ** 60:
            break
        s = s_rule(p, bm, k, k0, eta)
        if bm <= BCUT:
            best = None
            for c in range(bk + 1, 2 * bm + 1):
                if T1_holds(p, bm, c - bm, s):
                    best = c
            assert best is not None, f"no b_(k+1) with (T1) at k={k}"
            bp = min(best, bk + cdiv(gamma.numerator * (bk - bm), gamma.denominator))
            regime = "explicit"
        else:
            bp = (5 * bk) // 4
            regime = "far"
        N, NW = bp - bm, bk - bm
        assert bp > bk and bp <= 2 * bm
        assert T1_holds(p, bm, N, s), f"(T1) fails k={k}"
        assert NW >= 2 * s + 2, f"(T2) fails k={k}"
        assert N >= p, f"N<p k={k}"
        b.append(bp)
        muGc = mp.mpf(bp // (p * p)) / mp.mpf(p) ** (s - 2)
        if regime == "explicit" or N <= 6000:
            lB, info = lemmaT_bound(p, bm, bk, bp, s, lq1, lq2, lq3)
        else:
            lB = lemmaTprime_bound(p, N, NW, s, lq1, lq2, lq3)
            info = {}
        lB = lB + mp.mpf(10) ** -30          # outward
        ebar = mp.exp(lB / 2)
        delta += muGc + ebar                 # Markov: mu(G' & eps > ebar) <= Bfr/ebar = sqrt(Bfr)
        logPi += mp.log1p(ebar)
        if regime == "explicit":
            nexp += 1
            print(f"  k={k} ({bm},{bk},{bp}] s={s} N_W={NW} N={N} I={info.get('I')} muGc={mp.nstr(muGc, 6)} "
                  f"log10 Bfr={mp.nstr(lB / mp.log(10), 8)} ebar={mp.nstr(ebar, 6)}")
        k += 1
    lstar = k
    print(f"explicit phase-2 windows: {nexp}; far tail stops at l*={lstar} (l*-k0={lstar-k0}), b_(l*-1)={mp.nstr(mp.mpf(b[lstar-1]), 8)}")
    # ---------------- remainder
    remG = mp.mpf(eta.numerator) / eta.denominator * mp.mpf(2) ** (-(lstar - k0) + 1)
    logrem, slope, slopeT2 = remainder(p, lq1, lq2, lq3, eta, lstar - k0, mp.mpf(b[lstar - 1]))
    remB = mp.exp(logrem)
    print(f"remainder: deep gates <= {mp.nstr(remG, 4)}; fine scale: sum sqrt(Bfr) <= 10^({mp.nstr(logrem / mp.log(10), 6)}); "
          f"slope of log T2 bound per unit b = {mp.nstr(slopeT2, 6)}")
    deltaA = (delta + remG + remB) * UP
    logPiA = (logPi + remB) * UP
    PiA = mp.exp(logPiA)
    prod = PiA * deltaA
    print(f"RESULT p={p}: log Pi_A <= {mp.nstr(logPiA, 15)}, Pi_A <= {mp.nstr(PiA, 15)}, delta_A <= {mp.nstr(deltaA, 12)}, "
          f"Pi_A*delta_A <= {mp.nstr(prod, 10)}")
    if prod < 1:
        c = (1 - mp.sqrt(prod)) ** 2 / PiA
        print(f"RESULT p={p}: c_p >= {mp.nstr(c, 12)} (value of the C3 bound at these upper bounds; any smaller "
              f"number is a valid lower bound)")
    else:
        print(f"RESULT p={p}: FE FAILS (Pi_A delta_A >= 1)")


if __name__ == "__main__":
    main()
