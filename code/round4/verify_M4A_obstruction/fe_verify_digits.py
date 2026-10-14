#!/usr/bin/env python3
# fe_verify_digits.py -- VERBATIM COPY of code/round4/M4A/fe_verify.py (track M4A, round 4), made by track
# verify_M4A_obstruction only to print the certified interval endpoints of the final RESULT lines with 12
# significant digits (M4A prints 4-6 digits, rounded to nearest).  The only changes are: this header, the
# sys.path line that points at code/round4/M4A/ (read-only import of fe_lib, m4a_lib), and the RESULT prints.
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'M4A'))
"""fe_verify.py -- computer-assisted verification of hypothesis FE of R3M's Theorem C3 (note.md Theorem 11.14)
for one explicit admissible atom A = xA + 7^m Z_7 at time n_0 = 300 (track M4A, round 4; report
data/round4/reports/M4A.md, Theorem M).  All bounds are outward-rounded intervals (fe_lib.py, mpmath.iv, 200 bits).

Phases (l indexes the composite window [n_{l-1}, n_l) u [n_l, n_{l+1}), times n_{l+1} = ceil(r n_l), r = RNUM/RDEN):
  0      : admissibility of A (path re-verified by direct evaluation), window conditions of W_0, chi^2_0 <= Prop D.
  1      : l <= L1           eps_bar_l := Prop D bound (holds on all of A; no failure probability).
  2      : L1 < l, n_{l+1} <= NBLOCK   e_l := Prop E (block level, ball B = A), eps_bar_l := 2^-(l-L1), Markov.
  3      : NBLOCK < n_{l+1} < iA        e_l := Prop E' with exact D, K (from the digits of xA), sigma = M_{n_{l+1}}.
  4      : n_{l+1} >= iA                random gates; closed-form bound checked at the first such window and an
                                       analytic monotonicity argument (report, Section 6) for all later windows.
The linear-regime condition of Theorem C3 is checked exactly for every window of phases 1-3.
usage: fe_verify.py ATOMFILE L1 NBLOCK [RNUM RDEN]
"""
import math
import sys
from fractions import Fraction

from mpmath import iv, mpf, log10 as mlog10
import mpmath as mp

from fe_lib import Consts, blocklevel, Eprime, up, I
from m4a_lib import vp

iv.prec = 200


def main():
    atomfile, L1, NBLOCK = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    RNUM, RDEN = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (27, 20)
    kv = dict(line.split('=', 1) for line in open(atomfile).read().split() if '=' in line)
    p, n0, xA, m = int(kv['p']), int(kv['n0']), int(kv['xA']), int(kv['m'])
    bits = kv['path']  # e_0 e_1 ... e_{n0-1}
    C = Consts(p)
    print(f"# p={p} n0={n0} m={m} r={RNUM}/{RDEN} L1={L1} NBLOCK={NBLOCK}")
    print(f"# constants: q_1={float(up(C.qI[1])):.6f} q_2={float(up(C.qI[2])):.6f} rho1={float(up(C.rho1)):.6f} "
          f"gamma(lower)={float(C.gamma.a):.6f} kappa(lower)={float(C.kappa.a):.6f}")
    assert C.kappa.a > 0
    # ---- digit data: i_s = (-xA) mod p^s (or p^s); v(x+i) >= s iff i == i_s mod p^s, for s <= m-1, x in A
    iss = [None] + [((-xA) % p ** s) or p ** s for s in range(1, m + 1)]
    iA = iss[m]                       # first i >= 1 with xA + i == 0 mod p^m: before it, no random gate

    def Vf(N):                         # V_N(x) for x in A, valid for N < iA
        assert N < iA
        return sum((N - iss[s]) // p ** s + 1 for s in range(1, m) if iss[s] <= N)

    def Mf(N):
        assert N < iA
        return max([s for s in range(1, m) if iss[s] <= N], default=0)

    # sanity: formula vs direct valuations
    for N in list(range(1, 400)) + [1000, 5000, 20000]:
        assert Vf(N) == sum(vp(xA + i, p) for i in range(1, N + 1)), N
    assert Vf(n0) == m, (Vf(n0), m)
    # ---- admissibility: the slope-0 path, re-verified by direct evaluation with exact integers
    assert len(bits) == n0 and bits[0] == '1'
    S = dS = 0
    Pc, dPc = 1, 0
    for c in range(n0):
        if bits[c] == '1':
            S += Pc
            dS += dPc
        dPc = dPc * (xA + c + 1) + Pc
        Pc = Pc * (xA + c + 1)
    vS = vp(S, p)
    print(f"ADMISSIBLE: v(S_e(xA)) = {vS} >= m = {m}: {vS >= m};  S_e'(xA) mod p = {dS % p} (slope 0: {dS % p != 0})")
    assert vS >= m and dS % p != 0
    # ---- times
    times = [n0]
    while times[-1] < 10 * iA:
        times.append(-((-RNUM * times[-1]) // RDEN))
    D0, M1 = Vf(times[1]) - m, Mf(times[1])
    print(f"window W_0 = [{times[0]},{times[1]}): D_0={D0}, M_(n_1)={M1}: (W2') {D0 <= m - M1}, (W3') {M1 < m}")
    assert D0 <= m - M1 and M1 < m
    # depth array for the block-level phases
    NMAX = min(NBLOCK, iA - 1)
    depth = [0] + [vp(xA + i, p) for i in range(1, NMAX + 1)]
    V = [0] * (NMAX + 1)
    for i in range(1, NMAX + 1):
        V[i] = V[i - 1] + depth[i]
    chi = up(blocklevel(C, depth, V, times[0], times[1], D0, 0, max(depth[times[0] + 1:times[1] + 1]))) - 1
    logPi = iv.log(1 + iv.mpf(chi)) / iv.log(iv.mpf(10))
    print(f"chi^2_0 <= {float(chi):.6g}")
    fail = iv.mpf(0)
    Pi_tail = mpf(1)
    l = 1
    first4 = None
    rows = []
    while True:
        n, N, N2 = times[l - 1], times[l], times[l + 1]
        if N2 >= iA:
            first4 = l
            break
        mm = Vf(n)
        D, K = Vf(N) - mm, Vf(N2) - mm
        Mw = Mf(N2)                     # >= every depth in the window
        lin = (K <= mm - Mf(N2)) and (Mf(N2) < mm)
        assert lin, f"linear regime fails at l={l}"
        th = min((D + 1) // 2, D - m + 1)
        if l <= L1:
            assert N2 <= NMAX
            bD = up(blocklevel(C, depth, V, n, N2, K, 0, max(depth[n + 1:N2 + 1])))
            epsbar = max(bD - 1, mpf(0))
            logPi += iv.log(1 + iv.mpf(epsbar)) / iv.log(iv.mpf(10))
            rows.append(f"l={l} [{n},{N},{N2}) D={D} K={K} lin=True phase1 eps_bar(PropD)={float(epsbar):.4g}")
        else:
            assert th >= 1 and K - Mw >= th, (l, th, K, Mw)
            if N2 <= NMAX:
                e = up(blocklevel(C, depth, V, n, N2, K, th, max(depth[n + 1:N2 + 1])))
                ph = 2
            else:
                fpr = min(th, K - Mw)
                e = up(Eprime(C, K, N2 - n, fpr, Mw))
                ph = 3
            f_l = iv.mpf(e) * iv.mpf(2) ** (l - L1)
            fail += f_l
            if ph == 2 or l < L1 + 40 or l % 25 == 0:
                rows.append(f"l={l} [{n},{N},{N2}) D={D} K={K} theta={th} sigma<={Mw} lin=True phase{ph} "
                            f"log10 E_A eps <= {float(mlog10(e)):.3f}  log10 fail_l <= {float(mlog10(up(f_l))):.3f}")
        l += 1
    for rw in rows:
        print(rw)
    # prod_{i>=1} (1 + 2^-i) < 2.3843 (eps_bar_l = 2^-(l-L1) for l > L1): added below
    # ---- phase 4 (n_{l+1} >= iA): rigorous analytic bound for ALL such windows (report, Section 6).
    # For n := n_{l-1} >= n_star (first phase-4 window) and r = RNUM/RDEN:
    #   H <= Hp(n) = (r^2-1) n + r + 1,  n_{l+1} <= r^2 n + r + 1,  N - n >= (r-1) n,
    #   sigma_l := m + ceil(2 log_p n_{l+1}) + 11 <= sig(n) := m + 12 + 2 log_p(r^2 n + r + 1),
    #   K <= Hp/(p-1) + sig,  D >= Dm(n) := (r-1) n/(p-1) - log_p(Hp) - 1,  f' >= Dm/2,
    #   l - L1 <= l <= 1 + ln(n/n0)/ln r.
    # Phi(n) := ln 2 * (1 + ln(n/n0)/ln r) + ln 2 + max(ln t1(n), ln t2(n)) bounds ln fail_l.  Every log term in
    # Phi is concave and increasing in n, so Phi(n) + c n <= [Phi(n*) + c n*] + (n - n*) * slope(n*), where slope(n*)
    # is computed with the tangent lines at n*; both brackets are checked to be <= 0 with c = CRATE.
    r = Fraction(RNUM, RDEN)
    rI = I(r)
    P = iv.mpf(p)
    LP = iv.log(P)
    L2 = iv.log(iv.mpf(2))
    nstar = times[first4 - 1]
    gp = C.gamma * iv.mpf(p - 1) ** 2 / P ** 2
    # asymptotic decay rate of ln E' per unit n: c = gp (r-1)/(2(p-1)) - (r^2-1) rho1/(p-1); use half of it
    crate = gp * (rI - 1) / (2 * (p - 1)) - (rI ** 2 - 1) * C.rho1 / (p - 1)
    assert crate.a > 0, "no asymptotic decay"
    CRATE = iv.mpf(mpf(crate.a) / 2)
    ek = iv.exp(-C.kappa)

    def pieces(n):
        nI = iv.mpf(n)
        Hp = (rI ** 2 - 1) * nI + rI + 1
        sig = m + 12 + 2 * iv.log(rI ** 2 * nI + rI + 1) / LP
        Kp = Hp / (p - 1) + sig
        Dm = (rI - 1) * nI / (p - 1) - iv.log(Hp) / LP - 1
        lt1 = iv.log(1 + iv.mpf(2) ** p) + sig * LP - (rI ** 2 - 1) * nI * (L2 - LP / (p - 1))
        Dtot = C.logq[C.S] - C.logq[1] + (sig - C.S) * LP
        lt2 = ((p + sig * (p - 1)) * L2 + Kp * C.rho1 + Dtot + C.gamma * (2 - iv.mpf(1) / p)
               - gp * (Dm / 2 - sig + 1) + iv.log(ek / (1 - ek)))
        lw = L2 * (1 + iv.log(nI / n0) / iv.log(rI)) + L2
        lin = nI / (p - 1) - iv.log(nI) / LP - 1 - (Hp / (p - 1) + 2 * sig)   # m_{l-1} - M - K >= this
        return lt1, lt2, lw, sig, Dm, lin

    lt1, lt2, lw, sig, Dm, lin = pieces(nstar)
    val1 = up(lw + lt1 + CRATE * nstar + L2)
    val2 = up(lw + lt2 + CRATE * nstar + L2)
    # slopes at n*: derivative of each concave log term at n* (tangent-line bound), linear parts exact
    nI = iv.mpf(nstar)
    dlog = 1 / nI                         # d/dn ln(a n + b) <= 1/n for a, b >= 0
    dsig = 2 * dlog / LP
    s1 = -(rI ** 2 - 1) * (L2 - LP / (p - 1)) + dsig * LP + CRATE
    s2 = ((rI ** 2 - 1) * C.rho1 / (p - 1) - gp * (rI - 1) / (2 * (p - 1))
          + dsig * ((p - 1) * L2 + C.rho1 + LP + gp) + gp * dlog / (2 * LP) + CRATE)
    sw = L2 * dlog / iv.log(rI)
    print(f"phase4: first window l={first4}, n* = n_(l-1) = {nstar:.6e}; sigma(n*) <= {float(up(sig)):.2f}, "
          f"D >= {float(Dm.a):.4e}")
    print(f"phase4: decay rate used CRATE = {float(CRATE.a):.6f} (half of the asymptotic rate)")
    print(f"phase4: ln fail + CRATE n at n*: branch1 <= {float(val1):.4e}, branch2 <= {float(val2):.4e}; "
          f"slopes <= {float(up(s1 + sw)):.4e}, {float(up(s2 + sw)):.4e}")
    ok4 = val1 < 0 and val2 < 0 and up(s1 + sw) < 0 and up(s2 + sw) < 0
    # side conditions (D >= 2 sigma; linear regime) are increasing in n beyond n*: check value and slope at n*
    okside = (Dm - 2 * sig).a > 0 and lin.a > 0
    okside = okside and up(-(rI - 1) / (p - 1) + dlog / LP + 2 * dsig) < 0 and \
        up(-(1 - (rI ** 2 - 1)) / (p - 1) + dlog / LP + 2 * dsig * 2) < 0
    print(f"phase4: all windows l >= {first4} satisfy ln fail_l <= -CRATE n_(l-1): {ok4}; side conditions "
          f"(D >= 2 sigma, linear regime on G): {okside}")
    assert ok4 and okside
    # sum over l >= first4 of exp(-CRATE n_{l-1}) <= sum_{N >= n*} exp(-CRATE N)  (the n_{l-1} are distinct integers)
    tail4 = iv.exp(-CRATE * nstar) / (1 - iv.exp(-CRATE))
    PG = P ** (-10) * (iv.mpf(iA) ** -2 + P ** (-2 * m) * (iv.pi ** 2 / 6))
    print(f"phase4 tail sum <= {mpf(up(tail4))};  mu_A(G^c) <= {float(up(PG)):.4e}")
    delta = fail + tail4 + PG
    logPi_up = logPi + iv.log(iv.mpf(23843) / 10000) / iv.log(iv.mpf(10))
    print(f"RESULT log10 Pi_A in [{mp.nstr(mpf(logPi_up.a), 12)}, {mp.nstr(mpf(logPi_up.b), 12)}]")
    print(f"RESULT delta_A <= {mp.nstr(up(delta), 12)}")
    valI = logPi_up + iv.log(delta) / iv.log(iv.mpf(10))
    print(f"RESULT log10(Pi_A delta_A) <= {mp.nstr(up(valI), 12)}   FE holds: {up(valI) < 0}")
    if up(valI) < 0:
        lbI = (1 - iv.mpf(10) ** (valI / 2)) ** 2 * iv.mpf(10) ** (-logPi_up)
        print(f"RESULT certified lower endpoint: mu(K_p cap A)/mu(A) >= {mp.nstr(mpf(lbI.a), 12)}; "
              f"mu(K_p) >= {mp.nstr(mpf(lbI.a) * mpf(p) ** (-m), 8)} (= that times p^-{m})")

if __name__ == "__main__":
    main()
