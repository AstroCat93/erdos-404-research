#!/usr/bin/env python3
"""fe_indep.py -- independent re-evaluation of the FE certificate of M4A Theorem M (verify_M4A_logic, round 4).

Shares no code with code/round4/M4A/.  Reads only the atom data (x_A, path) from data/round4/M4A/atom_p7.txt
and re-derives everything else:
  atom      V_300(x_A), M_300, the slope-0 path (exact integers), i_A, the window times, D_0, M_405;
  digits    V_N(x) on A for N < i_A by counting multiples floor((x_A+N)/p^s) - floor(x_A/p^s) (s <= 51),
            cross-checked against direct valuations;
  phase 0/1 Prop D (statement of M4A section 5) for chi^2_0 and eps_bar_l, l <= L1 (mpmath, 320 bits);
  phase 2   Prop E with theta = min(ceil(D/2), D-b+1), b = m, after asserting M_W <= K - theta and the linear
            regime; full c-sum (no truncation);  E' is also evaluated there and compared;
  phase 3   Prop E' with exact D, K, sigma = M_{n_{l+1}}; linear regime and Lemma F condition asserted;
  phase 4   own closed-form argument (explicit -a n + b ln n + c bounds and monotonicity), not the tangent code;
  total     Pi_A, delta_A, and the Paley-Zygmund lower bound of Theorem C3.
Floating point: mpmath mpf at 320 bits (not interval arithmetic); the margins checked are >= 19 decimal orders.
usage: fe_indep.py ATOMFILE L1 NBLOCK
"""
import math
import sys
from fractions import Fraction

import mpmath
from mpmath import mpf

from vl_lib import vp, q_consts, P0_table, pis_and_derivs

mpmath.mp.prec = 320
R_NUM, R_DEN = 27, 20


def propDE_mp(depth, V, n, N2, Kt, p, qmp, S, P0mp, fprime=None):
    """mp version of the Prop D / Prop E bound (statement of M4A section 5); full c-sum."""
    H = N2 - n
    gates = [i for i in range(n + 1, N2 + 1) if depth[i] > 0]
    lam = {G: V[G] - V[n] for G in gates}
    fac = []
    for j in range(len(gates) - 1):
        G, G2 = gates[j], gates[j + 1]
        if lam[G] >= Kt:
            break
        if fprime is not None and depth[G2] == 1 and lam[G2] <= fprime:
            fac.append(qmp[2] / p ** 2)
        else:
            d = min(depth[G2], Kt - lam[G])
            qd = qmp[d] if d <= S else qmp[S] * mpf(p) ** (d - S)
            fac.append(qd / mpf(p) ** d)
    suf = [mpf(1)] * (len(gates) + 1)
    for j in range(len(fac) - 1, -1, -1):
        suf[j] = fac[j] * suf[j + 1]
    tot = mpf(2) ** (-H)
    gi = 0
    half = mpf(1) / 2
    w = half
    for c in range(H):
        ac = V[n + c] - V[n]
        if ac >= Kt:
            tot += w
        else:
            while gates[gi] <= n + c:
                gi += 1
            G = gates[gi]
            g1, s1 = G - n - c, depth[G]
            tot += w * P0mp[g1][min(s1, Kt - ac, len(P0mp[g1]) - 1)] * suf[gi]
        w *= half
    return mpf(p) ** Kt * tot


def main():
    atomfile, L1, NBLOCK = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    kv = dict(line.split('=', 1) for line in open(atomfile).read().split() if '=' in line)
    p, n0, xA, m_claim = int(kv['p']), int(kv['n0']), int(kv['xA']), int(kv['m'])
    path = kv['path']
    print(f"# independent FE evaluation: p={p} n0={n0} r={R_NUM}/{R_DEN} L1={L1} NBLOCK={NBLOCK}")
    # ---------------- atom
    dep300 = [vp(xA + i, p) for i in range(1, n0 + 1)]
    m = sum(dep300)
    M300 = max(dep300)
    print(f"atom: V_300(x_A) = {m} (claimed {m_claim}); M_300 = {M300} < m: {M300 < m}")
    assert m == m_claim and M300 < m and n0 >= 2 * p
    pi, dpi = pis_and_derivs(xA, n0)
    assert len(path) == n0 and path[0] == '1'
    Se = sum(pi[j] for j in range(n0) if path[j] == '1')
    dSe = sum(dpi[j] for j in range(n0) if path[j] == '1')
    vS = vp(Se, p)
    print(f"slope-0 path: v(S_e(x_A)) = {vS} >= {m}: {vS >= m};  v(S_e'(x_A)) = {vp(dSe, p)} (S' mod p = {dSe % p})")
    assert vS >= m and dSe % p != 0
    pm = p ** m
    iA = (-xA) % pm or pm
    print(f"i_A = {iA} ({float(iA):.4e})")

    def cnt(s, N):          # #{1 <= i <= N : p^s | x_A + i}
        return (xA + N) // p ** s - xA // p ** s

    def VA(N):              # V_N(x) for x in A, N < i_A
        assert N < iA and cnt(m, N) == 0
        return sum(cnt(s, N) for s in range(1, m))

    def MA(N):
        assert N < iA
        return max(s for s in range(1, m) if cnt(s, N) > 0)

    for N in [1, 7, 49, 299, 300, 405, 1000, 3000]:
        assert VA(N) == sum(vp(xA + i, p) for i in range(1, N + 1)), N
    # ---------------- times
    times = [n0]
    while times[-1] < 20 * iA:
        times.append(-((-R_NUM * times[-1]) // R_DEN))
    lstar = next(l for l in range(1, len(times) - 1) if times[l + 1] >= iA)
    print(f"times: {times[:11]} ...; first l with n_(l+1) >= i_A: l* = {lstar}; n_(l*-1) = {times[lstar - 1]:.6e}, "
          f"n_(l*+1) = {times[lstar + 1]:.6e}, n_(l*) = {times[lstar]:.6e}")
    D0, M1 = VA(times[1]) - m, MA(times[1])
    print(f"W_0 = [{times[0]},{times[1]}): D_0 = {D0}, M_(n_1) = {M1}; admissible: {D0 <= m - M1 and M1 < m}")
    assert D0 <= m - M1 and M1 < m
    # ---------------- constants
    S = 8
    qF = q_consts(p, S)
    P0F = P0_table(p, 14)
    qmp = {s: mpf(qF[s].numerator) / qF[s].denominator for s in range(1, S + 1)}
    P0mp = {g: [mpf(x.numerator) / x.denominator for x in row] for g, row in P0F.items()}
    print("q_s:", ", ".join(f"q_{s}={qF[s]}" for s in range(1, 5)), f"; max atom P(Z=z) = {qF['atom']}")
    print("P0:", {g: [str(P0F[g][s]) for s in range(1, 5)] for g in range(1, p + 1)})
    lq = {s: mpmath.log(qmp[s]) for s in range(1, S + 1)}
    rho1 = lq[1] + sum((lq[s] - lq[s - 1]) / mpf(p) ** (s - 1) for s in range(2, S + 1)) \
        + mpmath.log(p) * sum(mpf(p) ** (-(s - 1)) for s in range(S + 1, S + 400))
    gamma = lq[1] - mpmath.log(qmp[2] / p)
    kappa = (p - 1) * mpmath.log(2) - mpmath.log(p) + rho1 - gamma * mpf(p - 1) ** 2 / p ** 2
    print(f"rho1 = {mpmath.nstr(rho1, 8)}, gamma = {mpmath.nstr(gamma, 8)}, kappa = {mpmath.nstr(kappa, 8)}")
    assert kappa > 0

    def lqt(s):
        return lq[s] if s <= S else lq[S] + (s - S) * mpmath.log(p)

    ek = mpmath.exp(-kappa)
    geo = ek / (1 - ek)

    def Eprime_log(K, H, fpr, sig):
        """ln of Prop E' (statement, M4A section 5)."""
        lt1 = K * mpmath.log(p) - H * mpmath.log(2) + mpmath.log(1 + mpf(2) ** p)
        lt2 = ((p + sig * (p - 1)) * mpmath.log(2) + K * rho1 + lqt(sig) - lq[1] + gamma * (2 - mpf(1) / p)
               - gamma * (fpr - sig + 1) * mpf(p - 1) ** 2 / p ** 2 + mpmath.log(geo))
        hi = max(lt1, lt2)
        return hi + mpmath.log(mpmath.exp(lt1 - hi) + mpmath.exp(lt2 - hi))

    # ---------------- depth arrays for phases 0-2
    NMAX = min(NBLOCK, iA - 1)
    depth = [0] + [vp(xA + i, p) for i in range(1, NMAX + 1)]
    V = [0] * (NMAX + 1)
    for i in range(1, NMAX + 1):
        V[i] = V[i - 1] + depth[i]
    chi = propDE_mp(depth, V, times[0], times[1], D0, p, qmp, S, P0mp) - 1
    print(f"phase 0: chi^2_0 <= {mpmath.nstr(chi, 8)}")
    logPi = mpmath.log10(1 + chi)
    fail = mpf(0)
    rows = []
    l = 1
    nlin = 0
    while True:
        n, N, N2 = times[l - 1], times[l], times[l + 1]
        if N2 >= iA:
            break
        mm = VA(n)
        D, K = VA(N) - mm, VA(N2) - mm
        Mn2 = MA(N2)
        assert K <= mm - Mn2 and Mn2 < mm, f"linear regime fails at l={l}"
        nlin += 1
        th = min((D + 1) // 2, D - m + 1)
        if l <= L1:
            eb = propDE_mp(depth, V, n, N2, K, p, qmp, S, P0mp) - 1
            logPi += mpmath.log10(1 + max(eb, 0))
            rows.append(f"l={l} [{n},{N},{N2}) D={D} K={K} phase1 eps_bar=PropD-1={mpmath.nstr(eb, 6)}")
        else:
            MW = max(depth[n + 1:N2 + 1]) if N2 <= NMAX else Mn2
            assert th >= 1 and MW <= K - th, (l, th, K, MW)   # Lemma F hypothesis
            fpr = min(th, K - MW)
            if N2 <= NMAX:
                e = propDE_mp(depth, V, n, N2, K, p, qmp, S, P0mp, fprime=fpr)
                le = mpmath.log10(e)
                lep = Eprime_log(K, N2 - n, min(th, K - Mn2), Mn2) / mpmath.log(10)
                rows.append(f"l={l} [{n},{N},{N2}) D={D} K={K} theta={th} M_W={MW} phase2 log10 E_A eps <= "
                            f"{mpmath.nstr(le, 8)}  (E' gives {mpmath.nstr(lep, 8)}; E' >= E: {lep >= le})")
            else:
                le = Eprime_log(K, N2 - n, min(th, K - Mn2), Mn2) / mpmath.log(10)
                if l < L1 + 30 or l % 50 == 0 or N2 * R_NUM > iA * R_DEN:
                    rows.append(f"l={l} D={D} K={K} theta={th} sigma={Mn2} phase3 log10 E_A eps <= {mpmath.nstr(le, 10)}")
            fl = mpf(10) ** le * mpf(2) ** (l - L1)
            fail += fl
        l += 1
    lastl = l - 1
    for rw in rows:
        print(rw)
    print(f"linear regime checked exactly for l = 1..{lastl} ({nlin} windows); phases 2-3 failure sum <= "
          f"{mpmath.nstr(fail, 10)}")
    assert lastl == lstar - 1
    # ---------------- phase 4: own argument for all l >= l*
    r = mpf(R_NUM) / R_DEN
    ln7 = mpmath.log(p)
    nstar = times[lstar - 1]
    # bounds for n = n_{l-1} >= nstar (l >= l*):
    #   H in [(r^2-1) n, (r^2-1) n + r + 1];  sigma_l <= Sig(n) := m + 12 + 2 log_p(2 n)  (n >= 14);
    #   K <= H/(p-1) + Sig;  D >= Dm(n) := (r-1) n/(p-1) - log_p n - 1;  f' >= D/2 >= Dm/2 (needs D >= 2 sigma_l);
    #   l - L1 <= 1 + ln(n/n0)/ln r.  Each ln bound has the form -a n + b ln n + c.
    # Write Sig = s0 + s1 ln n with s0 = m + 12 + 2 log_p 2, s1 = 2/ln p.
    s0 = m + 12 + 2 * mpmath.log(2) / ln7
    s1 = 2 / ln7
    lnw = (mpmath.log(2) * (1 - mpmath.log(n0) / mpmath.log(r)), mpmath.log(2) / mpmath.log(r))   # c, b of Markov factor
    g2 = gamma * mpf(p - 1) ** 2 / p ** 2
    L2 = mpmath.log(2)
    # ln t1 <= -(r^2-1)(ln2 - ln p/(p-1)) n + Sig ln p + ln(1+2^p)    [uses K <= H/(p-1)+Sig, H >= (r^2-1) n]
    a1 = (r ** 2 - 1) * (L2 - ln7 / (p - 1))
    b1 = s1 * ln7
    c1 = s0 * ln7 + mpmath.log(1 + mpf(2) ** p)
    # ln t2 <= (p + (p-1) Sig) ln2 + rho1 (((r^2-1) n + r + 1)/(p-1) + Sig) + ln q_S - ln q_1 + (Sig - S) ln p
    #          + gamma (2 - 1/p) - g2 (Dm/2 - Sig + 1) + ln(geo)
    a2 = g2 * (r - 1) / (2 * (p - 1)) - rho1 * (r ** 2 - 1) / (p - 1)
    b2 = s1 * ((p - 1) * L2 + rho1 + ln7 + g2) + g2 / (2 * ln7)
    c2 = (p * L2 + s0 * ((p - 1) * L2 + rho1 + ln7 + g2) + rho1 * (r + 1) / (p - 1) + lq[S] - lq[1] - S * ln7
          + gamma * (2 - mpf(1) / p) + g2 / 2 - g2 + mpmath.log(geo))
    cprime = min(a1, a2) / 2
    ok = True
    for (a, b, c, name) in [(a1, b1, c1, "t1"), (a2, b2, c2, "t2")]:
        # ln fail <= [ln 2 + Markov] + ln t_i  <=  -(a) n + (b + lnw_b) ln n + (c + ln2 + lnw_c)
        B = b + lnw[1]
        Cc = c + L2 + lnw[0]
        # g(n) = (a - c') n - B ln n - Cc must be > 0 for n >= nstar: g(nstar) > 0 and g' > 0 there (g convex)
        gst = (a - cprime) * nstar - B * mpmath.log(nstar) - Cc
        gpr = (a - cprime) - B / nstar
        print(f"phase4 {name}: a={mpmath.nstr(a, 8)} b={mpmath.nstr(B, 6)} c={mpmath.nstr(Cc, 6)}; "
              f"g(n*)={mpmath.nstr(gst, 6)} g'(n*)={mpmath.nstr(gpr, 6)}")
        ok = ok and gst > 0 and gpr > 0
    # side conditions for n >= nstar: D >= 2 sigma_l  and  K + M <= m_{l-1} (linear regime), M < m_{l-1}
    #   Dm(n) - 2 Sig(n) = (r-1) n/(p-1) - (1/ln p + 2 s1) ln n - 1 - 2 s0
    hA = (r - 1) / (p - 1)
    hB = 1 / ln7 + 2 * s1
    hC = 1 + 2 * s0
    side1 = hA * nstar - hB * mpmath.log(nstar) - hC
    side1p = hA - hB / nstar
    #   m_{l-1} - K - M >= n/(p-1) - log_p n - 1 - ((r^2-1) n + r + 1)/(p-1) - 2 Sig
    lA = (2 - r ** 2) / (p - 1)
    lB = 1 / ln7 + 2 * s1
    lC = 1 + (r + 1) / (p - 1) + 2 * s0
    side2 = lA * nstar - lB * mpmath.log(nstar) - lC
    side2p = lA - lB / nstar
    print(f"phase4 side conditions at n*: D-2sigma >= {mpmath.nstr(side1, 6)} (slope {mpmath.nstr(side1p, 4)}), "
          f"m-K-M >= {mpmath.nstr(side2, 6)} (slope {mpmath.nstr(side2p, 4)})")
    ok = ok and side1 > 0 and side1p > 0 and side2 > 0 and side2p > 0 and nstar >= 14
    lntail = -cprime * nstar - mpmath.log(1 - mpmath.exp(-cprime))
    PG = mpf(p) ** (-10) * (mpf(iA) ** -2 + mpf(p) ** (-2 * m) * mpmath.pi ** 2 / 6)
    print(f"phase4: c' = {mpmath.nstr(cprime, 8)}; all l >= {lstar}: ln fail_l <= -c' n_(l-1): {ok}; "
          f"ln(tail sum) <= {mpmath.nstr(lntail, 8)}; mu_A(G'^c) <= {mpmath.nstr(PG, 8)}")
    assert ok
    delta = fail + mpmath.exp(lntail) + PG
    prodtail = mpf(1)
    for i in range(1, 400):
        prodtail *= 1 + mpf(2) ** (-i)
    logPi += mpmath.log10(prodtail)
    Pi = mpf(10) ** logPi
    val = Pi * delta
    lb = (1 - mpmath.sqrt(val)) ** 2 / Pi
    print(f"RESULT prod_(i>=1)(1+2^-i) = {mpmath.nstr(prodtail, 12)}")
    print(f"RESULT log10 Pi_A = {mpmath.nstr(logPi, 8)}; delta_A = {mpmath.nstr(delta, 8)}; "
          f"log10(Pi_A delta_A) = {mpmath.nstr(mpmath.log10(val), 8)}; FE: {val < 1}")
    print(f"RESULT mu(K_p cap A)/mu(A) >= {mpmath.nstr(lb, 8)};  mu(A) = p^-{m} = {mpmath.nstr(mpf(p) ** (-m), 6)}; "
          f"mu(K_p) >= {mpmath.nstr(lb * mpf(p) ** (-m), 6)}")


if __name__ == "__main__":
    main()
