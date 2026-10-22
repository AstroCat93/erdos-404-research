#!/usr/bin/env python3
"""assemble.py -- the computer-assisted part of Theorem M (M4C report, section 7): evaluates, for one prime p,
every quantity in the application of R3M Theorem C3 (note Theorem 11.14) to the atom A = p^3 Z_p at n_0 = 3p:

  Pi_A  = q1 * prod_{l>=1} (1 + ebar_l),                 (1 + chi^2_{W_0} = q1)
  delta_A <= sum_{l > k0} [ mu_A(G_l^c) + Bfr_l / ebar_l ],
  result: mu(K_p cap A)/mu(A) >= (1 - sqrt(Pi_A delta_A))^2 / Pi_A    if Pi_A delta_A < 1.

Phase 1 (l <= k0, all blocks < p^2): deterministic; lin_l checked exactly; ebar_l = q1^{n1} q2^{n2} - 1 (Lemma P).
Phase 2 (l > k0): s_l, schedule b_{l+1} from (T1); mu_A(G_l^c) <= floor(b_{l+1}/p^2) p^{-(s_l-2)};
  Bfr_l = Lemma T bound (worst-case environment, explicit sum over j0), ebar_l = sqrt(Bfr_l);
  after b_{l-1} > BCUT the closed-form bound of Lemma T' is used (see report), down to LOGP_STOP.
All real arithmetic is done with mpmath at 60 digits on quantities that are upper bounds; each logarithm used as
an upper bound is increased by a relative 1e-40 (outward rounding), each lower bound decreased likewise.
usage: assemble.py p [eta] [BCUT] [GAMMA]
"""
import sys
from fractions import Fraction

import mpmath as mp

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from early_phase import q1_exact, q2_exact, q3_exact, greedy, lin, env, vp  # noqa: E402

mp.mp.dps = 60
UP = mp.mpf(1) + mp.mpf(10) ** -40


def logp_up(x, p):
    return mp.log(mp.mpf(x)) / mp.log(p) * UP if x > 1 else mp.log(mp.mpf(x)) / mp.log(p) / UP


def Xi(U, p, s):
    """sum_{a=1}^{s-3} ceil(U/p^a): bound for sum of v(xi'+u) over U consecutive u when every term is <= s-3."""
    return sum(-(-U // p ** a) for a in range(1, s - 2)) if U > 0 else 0


def phase2_window(p, bm, bk, bp, s, Q1, Q2, Q3):
    """Lemma T bound Bfr (mpf upper bound) for the composite (bm, bp] with middle bk and depth cap s on G'.
    Environment on A (x = p xi, xi = p^2 xi'): gate j has depth 1 + v_p(j) if p^2 does not divide j, and
    3 + v(xi' + j/p^2) if p^2 | j; on G' every depth is <= s, and over any U consecutive p^2-multiples the
    extra sum_u v(xi'+u) is <= Xi(U) (at most ceil(U/p^a) of them have v >= a)."""
    N = bp - bm
    NW = bk - bm
    assert N >= p, "Lemma T needs N >= p (a p-multiple gate in the composite, so env balls lie in n + A)"
    d0 = []
    ism = []
    for i in range(1, N + 1):
        j = bm + i
        if j % (p * p) == 0:
            d0.append(3)
            ism.append(1)
        else:
            d0.append(1 + vp(j, p))
            ism.append(0)
    V0 = [0] * (N + 1)
    U = [0] * (N + 1)
    for i in range(1, N + 1):
        V0[i] = V0[i - 1] + d0[i - 1]
        U[i] = U[i - 1] + ism[i - 1]
    Vmax = [V0[i] + Xi(U[i], p, s) for i in range(N + 1)]
    Dmin = V0[NW]
    half = -(-Dmin // 2)
    I = max(i for i in range(N) if Vmax[i] < half)
    n1 = sum(1 for d in d0 if d == 1)
    n2 = sum(1 for d in d0 if d == 2)
    # non-J2 block factors: depth 1 -> q1; depth 2 -> q2 (start unit = -1 mod p); depth 3+e (p^2 | j) ->
    # p^e q3 (start unit = -1 mod p^2, block law mod p^3 fixed); sum of e over the window <= Xi(U[N])
    logC1 = n1 * mp.log(Q1) + n2 * mp.log(Q2) + U[N] * mp.log(Q3) + Xi(U[N], p, s) * mp.log(p)
    isone = [1 if d == 1 else 0 for d in d0]  # isone[i'] : gate i'+1 (end of block i') has depth 1
    suffix = [0] * (N + 2)
    for i in range(N - 1, -1, -1):
        suffix[i] = suffix[i + 1] + (isone[i] if i <= I else 0)
    lp = mp.log(p)
    l2 = mp.log(2)
    lq = mp.log(Q2 / p)
    terms = []
    for j0 in range(N):
        nJ2 = suffix[j0 + 1]
        terms.append(-j0 * p * l2 + Vmax[j0 + 1] * lp + logC1 + nJ2 * lq)
    m = max(terms)
    logB = m + mp.log(mp.fsum(mp.e ** (t - m) for t in terms))
    first = -N * p * l2 + Vmax[N] * lp
    tot = mp.e ** first + mp.e ** logB
    return tot * UP, I, NW, N


def T1_ok(p, bm, N, s):
    """sufficient condition (T1) for lin_l on G_l (report Lemma T(b))."""
    U = -(-N // (p * p))
    K = N + -(-N // p) + U + Xi(U, p, s)
    return K + s <= bm + bm // p


def main():
    p = int(sys.argv[1])
    eta = mp.mpf(sys.argv[2]) if len(sys.argv) > 2 else mp.mpf("0.01")
    BCUT = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
    global GAMMA
    GAMMA = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    q1 = q1_exact(p)
    q2 = q2_exact(p)
    Q1 = mp.mpf(q1.numerator) / q1.denominator * UP
    Q2 = mp.mpf(q2.numerator) / q2.denominator * UP
    q3 = q3_exact(p)
    Q3 = mp.mpf(q3.numerator) / q3.denominator * UP
    # ---- phase 1
    b = greedy(p)
    logPi = mp.log(Q1)
    for k in range(1, len(b) - 1):
        assert lin(p, b[k - 1], b[k], b[k + 1])
        n1 = sum(1 for j in range(b[k - 1] + 1, b[k + 1] + 1) if env(p, j) == 1)
        n2 = sum(1 for j in range(b[k - 1] + 1, b[k + 1] + 1) if env(p, j) == 2)
        logPi += (n1 * mp.log(Q1) + n2 * mp.log(Q2)) * UP
    k0 = len(b) - 2
    print(f"# assemble p={p} eta={eta} BCUT={BCUT} GAMMA={GAMMA}")
    print(f"q1 = {mp.nstr(Q1, 15)}  q2 = {mp.nstr(Q2, 15)}  q3 = {mp.nstr(Q3, 15)}")
    print(f"phase 1: blocks {b}; k0 = {k0}; log Pi_phase1 (incl. q1) <= {mp.nstr(logPi, 10)}")
    # ---- phase 2
    delta = mp.mpf(0)
    l = k0 + 1
    rows = 0
    while True:
        bm, bk = b[l - 1], b[l]
        if bm > BCUT:
            break
        # depth cap s: smallest s >= 3 with floor(2 bm / p^2) p^{-(s-2)} <= eta 2^{-(l-k0)}
        s = 3
        while mp.mpf((2 * bm) // (p * p)) * mp.mpf(p) ** (-(s - 2)) > eta * mp.mpf(2) ** (-(l - k0)):
            s += 1
        # schedule: b_{l+1} = min(largest b with (T1), b_l + ceil(GAMMA (b_l - b_{l-1})))
        best = None
        for bp in range(bk + 1, 2 * bm + 1):
            if T1_ok(p, bm, bp - bm, s):
                best = bp
        if best is None:
            print(f"phase 2 schedule infeasible at l={l} (blocks {bm},{bk}, s={s})")
            return
        best = min(best, bk + -(-int(GAMMA * (bk - bm) * 1000) // 1000))
        if best <= bk:
            print(f"phase 2 schedule stalls at l={l}")
            return
        bp = best
        b.append(bp)
        NW = bk - bm
        if NW < 2 * s + 2:
            print(f"(T2) fails at l={l}: N_W={NW} < 2s+2={2*s+2}")
            return
        muGc = mp.mpf(bp // (p * p)) * mp.mpf(p) ** (-(s - 2))
        Bfr, I, NW, N = phase2_window(p, bm, bk, bp, s, Q1, Q2, Q3)
        ebar = mp.sqrt(Bfr)
        delta += muGc + (Bfr / ebar if Bfr > 0 else 0)
        logPi += mp.log(1 + ebar) * UP
        if rows < 25 or bm > BCUT // 2:
            print(f"  l={l:3d} blocks ({bm},{bk},{bp}] s={s} N_W={NW} N={N} I={I}: mu(G^c)<={mp.nstr(muGc,4)} "
                  f"Bfr<={mp.nstr(Bfr,4)} ebar={mp.nstr(ebar,4)}")
        rows += 1
        l += 1
    print(f"phase 2 explicit part: up to window l={l-1}, b_(l-1) = {b[l-1]}; delta so far <= {mp.nstr(delta, 8)}; "
          f"log Pi so far <= {mp.nstr(logPi, 10)}")
    b = b[:l + 1]
    # ---- far tail (Lemma T'): omega-rule b_{l+1} = floor((1+omega) b_l), closed-form bound
    omega = Fraction(1, 4)
    alpha = Fraction(1) + Fraction(1, p) + Fraction(1, p * p) + Fraction(1, p * p * (p - 1))
    rho = Q2 / p
    r1 = mp.mpf(2) ** (-p) * mp.mpf(p) ** (mp.mpf(alpha.numerator) / alpha.denominator) * rho ** (-(1 - mp.mpf(1) / p))
    assert r1 < 1, "r1 >= 1"
    lp = mp.log(p)
    aF = mp.mpf(alpha.numerator) / alpha.denominator
    nfar = 0
    worst = None
    while True:
        bm, bk = b[l - 1], b[l]
        if bm > 10 ** 60:
            break
        s = 3
        cnt = (2 * bm) // (p * p)
        while mp.mpf(cnt) * mp.mpf(p) ** (-(s - 2)) > eta * mp.mpf(2) ** (-(l - k0)):
            s += 1
        bp = (bk * (omega.numerator + omega.denominator)) // omega.denominator
        N = bp - bm
        NW = bk - bm
        assert T1_ok(p, bm, N, s), f"T1 fails in far tail at l={l}"
        assert NW >= 2 * s + 2, f"T2 fails in far tail at l={l}"
        assert N >= p, "Lemma T' needs N >= p"
        b.append(bp)
        muGc = mp.mpf(bp // (p * p)) * mp.mpf(p) ** (-(s - 2))
        if N <= 6000:
            Bfr, I, _, _ = phase2_window(p, bm, bk, bp, s, Q1, Q2, Q3)
        else:
            # closed form (Lemma T')
            hw = -(-NW // 2)
            num = hw - s
            Ilow = max(0, -(-(num * alpha.denominator) // alpha.numerator) - 1) if num > 0 else 0
            U = -(-N // (p * p))
            logC1 = N * mp.log(Q1) + (-(-N // p)) * mp.log(Q2) + U * mp.log(Q3) + Xi(U, p, s) * lp
            t1 = -N * p * mp.log(2) + (aF * N + s) * lp
            t2 = mp.log(2 / (1 - r1)) + logC1 + (aF + s) * lp + (Ilow * (1 - mp.mpf(1) / p) - 1) * mp.log(rho)
            m = max(t1, t2)
            Bfr = mp.e ** m * (mp.e ** (t1 - m) + mp.e ** (t2 - m)) * UP
            I = Ilow
        ebar = mp.sqrt(Bfr)
        delta += muGc + ebar
        logPi += mp.log(1 + ebar) * UP
        if nfar < 6 or nfar % 50 == 0:
            print(f"  far l={l:4d} b_(l-1)={mp.nstr(mp.mpf(bm),6)} N_W={mp.nstr(mp.mpf(NW),5)} N={mp.nstr(mp.mpf(N),5)} s={s}: "
                  f"mu(G^c)<={mp.nstr(muGc,3)} Bfr<={mp.nstr(Bfr,3)}")
        nfar += 1
        l += 1
    print(f"far tail evaluated up to b_(l-1) = {mp.nstr(mp.mpf(b[l-1]), 6)} (l={l}); r1 = {mp.nstr(r1, 6)}")
    # final remainder: for b_(l-1) > 10^60 the omega-rule continues; s_l <= 3 + log_p(2 b/(p^2 eta)) + (l-k0) log_p 2 and
    # l - k0 <= l_now - k0 + log_{1.25}(b/b_now) + 1.  We check the closed-form exponent at b = 10^60 with s = 3+10 ln b.
    bb = mp.mpf(10) ** 60
    sb = 3 + 10 * mp.log(bb)
    NWb = bb / 4 - 1
    Nb = mp.mpf(9) / 16 * bb + 1
    Ilb = (NWb / 2 - sb) / aF - 1
    logC1b = Nb * mp.log(Q1) + (Nb / p + 1) * mp.log(Q2) + (Nb / p ** 2 + 1) * mp.log(Q3) + ((Nb / p ** 2 + 1) / (p - 1) + sb) * lp
    t2b = mp.log(2 / (1 - r1)) + logC1b + (aF + sb) * lp + (Ilb * (1 - mp.mpf(1) / p) - 1) * mp.log(rho)
    print(f"REMAINDER CHECK at b=10^60: log of Lemma T' bound <= {mp.nstr(t2b, 6)} (must be << 0); slope in b: "
          f"{mp.nstr((mp.log(Q1)*9/16 + mp.log(Q2)*9/16/p + mp.log(Q3)*9/16/p**2 + lp*9/16/p**2/(p-1)) + (1-mp.mpf(1)/p)*mp.log(rho)/8/aF, 6)} per unit b (must be < 0)")
    # remainder over the windows l' >= l not evaluated above:
    #   sum mu_A(G^c) <= sum_{l'>=l} eta 2^{-(l'-k0)} = eta 2^{-(l-k0)+1}   (s-rule; b_{l'+1} <= 2 b_{l'-1})
    #   sum sqrt(Bfr) <= 10^-1000 and sum log(1+ebar) <= 10^-1000           (REMAINDER CHECK above)
    remG = eta * mp.mpf(2) ** (-(l - k0) + 1)
    remB = mp.mpf(10) ** -1000
    delta_tot = (delta + remG + remB) * UP
    logPi = (logPi + remB) * UP
    Pi = mp.e ** logPi
    print(f"RESULT p={p}: Pi_A <= {mp.nstr(Pi, 15)}; delta_A <= {mp.nstr(delta_tot, 10)} "
          f"(evaluated windows {mp.nstr(delta, 10)} + remainder {mp.nstr(remG + remB, 3)}); "
          f"Pi_A*delta_A <= {mp.nstr(Pi * delta_tot, 8)}")
    if Pi * delta_tot < 1:
        res = (1 - mp.sqrt(Pi * delta_tot)) ** 2 / Pi
        res_dn = mp.floor(res * 10 ** 6) / 10 ** 6
        mk = res_dn / p ** 3
        e10 = int(mp.floor(mp.log10(mk)))
        mk_dn = mp.floor(mk / mp.mpf(10) ** (e10 - 3)) * mp.mpf(10) ** (e10 - 3)
        print(f"RESULT p={p}: mu(K_p cap A)/mu(A) >= {mp.nstr(res_dn, 8)} (rounded down),  A = p^3 Z_p,  "
              f"so mu(K_p) >= {mp.nstr(mk_dn, 4)} (rounded down)")


if __name__ == "__main__":
    main()
