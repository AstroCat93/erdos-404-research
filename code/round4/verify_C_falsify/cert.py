#!/usr/bin/env python3
"""Independent recomputation of the Theorem M certificate of M4C (report §§6-7).

Implemented from the report text only (no code shared with code/round4/M4C/):
  * Phase 1: greedy schedule b_0=3, b_1=4, b_{k+1} = largest b <= p^2-1 with (6.1);
    eps_bar_k = q1^{n1(k)} q2^{n2(k)} - 1.
  * Phase 2 (b_{k-1} <= BCUT): s-rule, (T1)-maximal b capped by 2 b_{k-1} and by
    b_k + ceil(gamma (b_k - b_{k-1})); eps_bar_k = sqrt(B'_k) with B' = Lemma T
    (term by term) if N <= 6000, else Lemma T' closed form.
  * Far tail (b_{k-1} > BCUT): same s-rule; b_{k+1} = floor(5 b_k / 4); evaluated
    while b_{k-1} <= 10^60; then remainder eta*2^{-(l*-k0)+1} (deep gates) and
    10^-1000 (fine scale), as in §7.2.
  * delta_A = sum_k [floor(b_{k+1}/p^2) p^{-(s_k-2)} + sqrt(B'_k)],
    log Pi_A = log q1 + sum_k log(1+eps_bar_k),
    c_p = (1 - sqrt(Pi_A delta_A))^2 / Pi_A.
All checks (6.1), (T1), (T2), N >= p are asserted in exact integer arithmetic.
Also checks Lemma T' >= Lemma T on every window with N <= 6000 (free test).
Arithmetic: mpmath, 60 digits; q's are exact rationals from qconst_indep.py.
"""
import sys, math, time
from fractions import Fraction
import mpmath as mm
sys.path.insert(0, __import__('os').path.dirname(__file__))
from qconst_indep import q_exact

mm.mp.dps = 60


def vp(n, p):
    v = 0
    while n % p == 0:
        n //= p; v += 1
    return v


def cdiv(a, b):
    return -((-a) // b)


def Xi(U, s, p):
    return sum(cdiv(U, p ** a) for a in range(1, s - 2))  # a = 1..s-3


def phase1(p):
    P2 = p * p
    d = [0] + [1 + vp(j, p) for j in range(1, P2)]
    V = [0] * P2; Mx = [0] * P2
    for j in range(1, P2):
        V[j] = V[j - 1] + d[j]; Mx[j] = max(Mx[j - 1], d[j])
    b = [3, 4]
    while b[-1] < P2 - 1:
        km1 = b[-2]
        best = None
        for c in range(P2 - 1, b[-1], -1):
            if V[c] - V[km1] <= V[km1] - Mx[c] and Mx[c] < V[km1]:
                best = c; break
        if best is None:
            raise RuntimeError("phase 1 greedy stuck at %s" % b)
        b.append(best)
    k0 = len(b) - 2   # b_{k0+1} = p^2 - 1
    # windows k = 1..k0 use (b_{k-1}, b_{k+1}]
    wins = []
    for k in range(1, k0 + 1):
        lo, hi = b[k - 1], b[k + 1]
        assert V[hi] - V[lo] <= V[lo] - Mx[hi] and Mx[hi] < V[lo]
        n1 = sum(1 for j in range(lo + 1, hi + 1) if d[j] == 1)
        n2 = sum(1 for j in range(lo + 1, hi + 1) if d[j] == 2)
        assert n1 + n2 == hi - lo
        wins.append((k, lo, hi, n1, n2))
    return b, k0, wins


def s_rule(p, bkm1, k, k0, eta):
    f = (2 * bkm1) // (p * p)
    s = 3
    thr = eta / Fraction(2 ** (k - k0))
    while Fraction(f, p ** (s - 2)) > thr:
        s += 1
    return s


def T1_ok(p, bkm1, N, s):
    UN = cdiv(N, p * p)
    return N + cdiv(N, p) + UN + Xi(UN, s, p) + s <= bkm1 + bkm1 // p


def max_T1_b(p, bkm1, s):
    # largest b <= 2 bkm1 with (T1) for N = b - bkm1 (monotone in N): binary search
    lo, hi = 0, bkm1
    if not T1_ok(p, bkm1, 0, s):
        return None
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if T1_ok(p, bkm1, mid, s):
            lo = mid
        else:
            hi = mid - 1
    return bkm1 + lo


def lemmaT_log(p, s, bkm1, bk, bkp1, lq1, lq2, lq3):
    """log of B (Lemma T, term by term)."""
    N = bkp1 - bkm1; NW = bk - bkm1
    P2 = p * p
    d0 = [0] * (N + 1); V0 = [0] * (N + 1); U = [0] * (N + 1); Vp = [0] * (N + 1)
    for i in range(1, N + 1):
        j = bkm1 + i
        if j % P2 == 0:
            d0[i] = 3
        else:
            d0[i] = 1 + vp(j, p)
        V0[i] = V0[i - 1] + d0[i]
        U[i] = U[i - 1] + (1 if j % P2 == 0 else 0)
        Vp[i] = V0[i] + Xi(U[i], s, p)
    Dm = V0[NW]
    hD = cdiv(Dm, 2)
    I = max(i for i in range(0, N) if Vp[i] < hD)
    # nu(j0) = #{i in (j0, I] : p does not divide bkm1 + i + 1}
    good = [0] * (N + 2)
    for i in range(1, N + 1):
        good[i] = good[i - 1] + (1 if (bkm1 + i + 1) % p != 0 else 0)
    def nu(j0):
        return good[I] - good[j0] if I > j0 else 0
    n1 = sum(1 for j in range(bkm1 + 1, bkp1 + 1) if j % p != 0)
    n2 = sum(1 for j in range(bkm1 + 1, bkp1 + 1) if j % p == 0 and j % P2 != 0)
    UU = sum(1 for j in range(bkm1 + 1, bkp1 + 1) if j % P2 == 0)
    lp = mm.log(p); l2 = mm.log(2); lrho = lq2 - lp
    first = -N * p * l2 + Vp[N] * lp
    terms = [-j0 * p * l2 + Vp[j0 + 1] * lp + nu(j0) * lrho for j0 in range(N)]
    m = max(terms)
    ssum = mm.fsum(mm.exp(t - m) for t in terms)
    second = n1 * lq1 + n2 * lq2 + UU * lq3 + Xi(UU, s, p) * lp + m + mm.log(ssum)
    mx = max(first, second)
    return mx + mm.log(mm.exp(first - mx) + mm.exp(second - mx)), I


def lemmaTp_log(p, s, NW, N, lq1, lq2, lq3):
    """log of the Lemma T' closed-form bound."""
    pp = mm.mpf(p)
    alpha = 1 + 1 / pp + 1 / pp ** 2 + 1 / (pp ** 2 * (pp - 1))
    lp = mm.log(pp); l2 = mm.log(2)
    lrho = lq2 - lp
    assert lrho < 0
    lr1 = -p * l2 + alpha * lp - (1 - 1 / pp) * lrho
    assert lr1 < 0
    Ip = max(0, int(mm.ceil((cdiv(NW, 2) - s) / alpha)) - 1)
    first = -N * p * l2 + (alpha * N + s) * lp
    second = (-mm.log(1 - mm.exp(lr1)) + N * lq1 + cdiv(N, p) * lq2 + cdiv(N, p * p) * lq3
              + Xi(cdiv(N, p * p), s, p) * lp + (alpha + s) * lp + (Ip * (1 - 1 / pp) - 1) * lrho)
    mx = max(first, second)
    return mx + mm.log(mm.exp(first - mx) + mm.exp(second - mx)), Ip


def run(p, eta=Fraction(1, 20), BCUT=3000, gamma=Fraction(8, 5), BIG=10 ** 60, verbose=True):
    t0 = time.time()
    q1, _, _ = q_exact(p, 1); q2, _, _ = q_exact(p, 2); q3, _, _ = q_exact(p, 3)
    lq1 = mm.log1p(mm.mpf(q1.numerator - q1.denominator) / q1.denominator)
    lq2 = mm.log1p(mm.mpf(q2.numerator - q2.denominator) / q2.denominator)
    lq3 = mm.log1p(mm.mpf(q3.numerator - q3.denominator) / q3.denominator)
    b, k0, wins = phase1(p)
    logPi = lq1
    for (k, lo, hi, n1, n2) in wins:
        logPi += n1 * lq1 + n2 * lq2
    logPi1 = logPi
    if verbose:
        print("p=%d q1-1=%.6e q2-1=%.6e q3-1=%.6e" % (p, float(q1 - 1), float(q2 - 1), float(q3 - 1)))
        print("  phase1 b=%s k0=%d log Pi_phase1(incl q1)=%s" % (b, k0, mm.nstr(logPi1, 12)))
    delta_G = mm.mpf(0); delta_F = mm.mpf(0)
    nTcheck = 0; minmargin = None
    k = k0 + 1
    nexpl = 0
    while True:
        bkm1, bk = b[k - 1], b[k]
        if bkm1 > BIG:
            break
        s = s_rule(p, bkm1, k, k0, eta)
        if bkm1 <= BCUT:
            bT1 = max_T1_b(p, bkm1, s)
            assert bT1 is not None
            bnext = min(min(bT1, 2 * bkm1), bk + cdiv(gamma.numerator * (bk - bkm1), gamma.denominator))
            rule = "ph2"
        else:
            bnext = (5 * bk) // 4
            rule = "far"
        assert bnext > bk
        b.append(bnext)
        N = bnext - bkm1; NW = bk - bkm1
        # exact checks
        assert T1_ok(p, bkm1, N, s), ("T1 fails", p, k)
        assert NW >= 2 * s + 2, ("T2 fails", p, k, NW, s)
        assert N >= p
        assert bnext <= 2 * bkm1 or rule == "far"
        muG = mm.mpf(bnext // (p * p)) / mm.mpf(p) ** (s - 2)
        if N <= 6000:
            lB, I = lemmaT_log(p, s, bkm1, bk, bnext, lq1, lq2, lq3)
            lBp, Ip = lemmaTp_log(p, s, NW, N, lq1, lq2, lq3)
            nTcheck += 1
            mg = lBp - lB
            minmargin = mg if minmargin is None else min(minmargin, mg)
            assert lBp >= lB, ("Lemma T' < Lemma T", p, k)
        else:
            lB, I = lemmaTp_log(p, s, NW, N, lq1, lq2, lq3)
        sq = mm.exp(lB / 2)
        delta_G += muG; delta_F += sq
        logPi += mm.log1p(sq)
        nexpl += 1
        if verbose and (rule == "ph2" or k - k0 <= 12 or (k - k0) % 100 == 0):
            print("  l=%d %s (%d,%d,%d] s=%d N_W=%d N=%d I=%d mu(G^c)<=%s sqrtB=%s" % (
                k, rule, bkm1, bk, bnext, s, NW, N, I, mm.nstr(muG, 6), mm.nstr(sq, 6)) if bkm1 < 10 ** 7 else
                  "  l=%d %s b_(l-1)=%.5e N_W=%.4e N=%.4e s=%d mu(G^c)<=%s log10 sqrtB=%s" % (
                k, rule, bkm1, NW, N, s, mm.nstr(muG, 4), mm.nstr(lB / 2 / mm.log(10), 8)))
        k += 1
    lstar = k
    rem_G = eta * Fraction(2) / Fraction(2 ** (lstar - k0))
    delta = delta_G + delta_F + mm.mpf(rem_G.numerator) / rem_G.denominator + mm.mpf(10) ** (-1000)
    logPi += mm.mpf(10) ** (-1000)
    Pi = mm.exp(logPi)
    prod = Pi * delta
    cp = (1 - mm.sqrt(prod)) ** 2 / Pi
    if verbose:
        print("  l*=%d l*-k0=%d remainder(deep gates)=%s; windows evaluated: %d; Lemma T'>=T checked on %d windows, min log-margin %s" % (
            lstar, lstar - k0, mm.nstr(mm.mpf(rem_G.numerator) / rem_G.denominator, 4), nexpl, nTcheck,
            mm.nstr(minmargin, 4) if minmargin is not None else "-"))
        print("RESULT p=%d: log Pi_A=%s Pi_A=%s delta_A=%s (muG %s + sqrtB %s) Pi*delta=%s c_p=%s mu(K_p)>=%s  [%.1fs]" % (
            p, mm.nstr(logPi, 15), mm.nstr(Pi, 15), mm.nstr(delta, 12), mm.nstr(delta_G, 12), mm.nstr(delta_F, 6),
            mm.nstr(prod, 10), mm.nstr(cp, 12), mm.nstr(cp / p ** 3, 6), time.time() - t0), flush=True)
    return dict(b=b, k0=k0, logPi=logPi, Pi=Pi, delta=delta, cp=cp, lstar=lstar)


if __name__ == "__main__":
    ps = [int(a) for a in sys.argv[1:]] or [11, 13, 17, 23, 97]
    for p in ps:
        run(p)
