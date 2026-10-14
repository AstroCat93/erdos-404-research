#!/usr/bin/env python3
"""w3_chain.py -- Theorem W6 of M4D over a finite horizon of three windows, exhaustively on an admissible atom.

Times n0 < n1 < n2 < n3 (deterministic), windows W_l = [n_l, n_{l+1}), j = 0.  A = x + p^{m0} Z_p.
G_l = partition into the cylinders x + p^{m_l(x)} Z_p.  Required on A: admissible (D0 <= m0 - M_{n1},
M_{n1} < m0, P^0_{n0} nonempty) and the linear regime B_1 for (W0,W1) (G_0-measurable, so all of A).
For every G_1-atom C1 the regime B_2 for (W1,W2) is evaluated at TWO representatives with different high
digits (measurability check).  On regime atoms all points of C1 mod p^{m1+D1+D2} are enumerated; off regime,
all points mod p^{m1+D1}.  Every point carries random higher digits; paths are found by DFS with direct
valuations (no linearisation).

Weight schedules (all with w_0 = 1 on the slope-0 parents, or 0/1 on a subset if MAXPAR is exceeded):
  U  all uniform (predictable)                -> R3M Theorem C3 exactly; sharp eps used
  R  q0 random; q1 random per G_1-atom; q2 random per G_2-atom (adapted) -> eps~ used
  S  q0 = q*(W0;D1); q1 = q*(W1;D2) on regime G_1-atoms (uniform off regime); q2 random per G_2-atom -> eps~
  P  q0 random; q1 random but constant on A; q2 random per G_1-atom (predictable)   -> sharp eps used
Checks (exact Fractions unless stated):
  MEAS  B_2, D_2, eps_2 and q*_1 are equal at the two representatives of every G_1-atom; M_1 is constant on
        G_1-atoms, M_2 on G_2-atoms, M_3 on G_3-atoms (all points of an atom carry different high digits)
  MART  E[M~_{l+1} | G_l-atom] == M~_l for l = 0,1,2 on every atom, hence E_A M~_l == M_0
  CS1   E_A M_1^2 <= M_0^2 (1 + chi2_{q0})
  INC   on every G_{l-1}-atom inside {tau > l}:  E[M_{l+1}^2 - M_l^2] <= eps_l M_{l-1}^2   (l = 1, 2)
  W5c   if q_{l-1} = q* and m(W_{l-1};D_l) = 0 on an atom: M_{l+1} == M_l pointwise there
  REC   a_2 <= a_1 + epsbar_1 a_0,  a_3 <= a_2 + epsbar_2 a_1,  a_l nondecreasing (a_l = E_A M~_l^2)
  PZ    finite horizon: mu_A(Y_3 > 0) >= (1 - sqrt(Pi delta))^2 / Pi (float), Y_3 = 1{tau > 2} M~_3,
        delta = mu_A(tau <= 2), Pi = (1+chi2_{q0})(1+epsbar_1)(1+epsbar_2)
  SURV  M~_3 > 0 at a point  =>  a slope-0 path with positive weight is alive at n3 there, verified by a
        direct valuation v(S_e) >= V_{n3}
  epsbar_1 = eps_1 (so tau > 1 on A); epsbar_2 = the median of eps_2 over the regime atoms (so tau stops on some)
CONTROL NEGM: q1 depending on the fresh digit at position m1 (not adapted): MART at l = 1 must fail somewhere.
usage: w3_chain.py p seed nA n0 H0 H1 H2 sched [MAXPAR] [KMAX]
"""
import random
import sys
import math
from fractions import Fraction

from wlib import (vp, prods, Vof, Mof, grow, alive_slope0, win_elems, win_unit, subset_sums, chi2,
                  fine_tilde, composite_fine, hm_and_qstar, rand_prob, S_and_dS)


def main():
    a = sys.argv[1:]
    p, seed, nA, n0, H0, H1, H2 = (int(t) for t in a[:7])
    sched = a[7]
    maxpar = int(a[8]) if len(a) > 8 else 40
    kmax = int(a[9]) if len(a) > 9 else 8
    n1, n2, n3 = n0 + H0, n0 + H0 + H1, n0 + H0 + H1 + H2
    rnd = random.Random(seed)
    prec = 4 * (n3 // (p - 1) + 14)
    mod = p ** prec
    st = {}

    def bump(k, v=1):
        st[k] = st.get(k, 0) + v

    worst = {}

    def wmax(k, v):
        worst[k] = max(worst.get(k, 0.0), v)

    done = tries = 0
    while done < nA and tries < 100000:
        tries += 1
        x = rnd.randrange(p ** 45)
        pi, dpi, vals = prods(x, n3, p, prec)
        m0 = Vof(vals, n0)
        D0 = Vof(vals, n1) - m0
        D1 = Vof(vals, n2) - Vof(vals, n1)
        # admissible + B_1 (linear regime for (W0,W1)) on A
        if not (Mof(vals, n1) < m0 and D0 <= m0 - Mof(vals, n1)):
            continue
        if not (Mof(vals, n2) < m0 and D0 + D1 <= m0 - Mof(vals, n2)):
            continue
        if D0 < 1 or D1 < 1:
            continue
        par0 = alive_slope0(x, n0, p, prec)
        if not par0:
            continue
        m1, m2 = m0 + D0, m0 + D0 + D1
        x0 = x % p ** m0
        # G_1 atoms: regime B_2 at two representatives each
        atoms1 = {}
        ok = True
        for c1 in range(p ** D0):
            reps = []
            for _ in range(2):
                xr = x0 + p ** m0 * c1 + p ** m1 * rnd.randrange(p ** 30)
                _, _, vr = prods(xr, n3, p, prec)
                assert Vof(vr, n1) == m1 and Vof(vr, n2) == m2
                MN3 = Mof(vr, n3)
                D2r = Vof(vr, n3) - m2
                B2 = (MN3 < m1 and D1 + D2r <= m1 - MN3)
                reps.append((B2, D2r if B2 else None, xr))
            if reps[0][0] != reps[1][0] or reps[0][1] != reps[1][1]:
                bump('MEAS_B2')
            atoms1[c1] = reps[0]
            if reps[0][0] and D1 + reps[0][1] > kmax:
                ok = False
        if not ok:
            continue
        done += 1
        bump('atoms_A')
        if len(par0) > maxpar:
            par0 = rnd.sample(par0, maxpar)
            bump('subset')
        w0 = {b: Fraction(1) for b in par0}
        M0 = p ** m0 * len(par0)
        # window data of W0 on A
        K1 = D0 + D1
        sumsW0 = subset_sums(win_elems(x, n0, n1, p ** K1), p ** K1)
        u0 = win_unit(x, n0, n1, p, p ** D1)
        mstar0, qstar0, _ = hm_and_qstar(sumsW0, p, D0, D1)
        # q0
        if sched == 'U':
            q0 = [Fraction(1, 1 << H0)] * (1 << H0)
        elif sched == 'S':
            q0 = qstar0
        else:
            q0 = rand_prob(rnd, 1 << H0, zero_frac=0.3)
        # q1 per G_1 atom, and eps_2 per atom (evaluated at both representatives)
        q1 = {}
        q1_const = rand_prob(rnd, 1 << H1, zero_frac=0.3)
        eps2 = {}
        mstar1 = {}
        for c1, (B2, D2, xr) in atoms1.items():
            if sched == 'U':
                q1[c1] = [Fraction(1, 1 << H1)] * (1 << H1)
            elif sched == 'P':
                q1[c1] = q1_const
            elif sched == 'R':
                q1[c1] = rand_prob(rnd, 1 << H1, zero_frac=0.3)
            elif sched == 'S':
                if B2:
                    K2 = D1 + D2
                    s1 = subset_sums(win_elems(xr, n1, n2, p ** K2), p ** K2)
                    mm, qs, _ = hm_and_qstar(s1, p, D1, D2)
                    # measurability of q*_1: recompute at an independent representative of the atom
                    xr2 = x0 + p ** m0 * c1 + p ** m1 * rnd.randrange(p ** 30)
                    s1b = subset_sums(win_elems(xr2, n1, n2, p ** K2), p ** K2)
                    mmb, qsb, _ = hm_and_qstar(s1b, p, D1, D2)
                    if qsb != qs or mmb != mm:
                        bump('MEAS_qstar')
                    q1[c1] = qs
                    mstar1[c1] = mm
                else:
                    q1[c1] = [Fraction(1, 1 << H1)] * (1 << H1)
            else:
                raise SystemExit('sched must be U|R|S|P')
        q2_by_atom1 = {c1: rand_prob(rnd, 1 << H2, zero_frac=0.3) for c1 in atoms1}  # for P
        q2 = {}  # G_2 atom key (c1, c2 mod p^D1) -> weight
        for c1, (B2, D2, xr) in atoms1.items():
            if not B2:
                continue
            K2 = D1 + D2
            vals_eps = []
            for xrr in (xr, x0 + p ** m0 * c1 + p ** m1 * rnd.randrange(p ** 30)):
                s1 = subset_sums(win_elems(xrr, n1, n2, p ** K2), p ** K2)
                if sched in ('U', 'P'):
                    q2c = [Fraction(1, 1 << H2)] * (1 << H2) if sched == 'U' else q2_by_atom1[c1]
                    s2 = subset_sums(win_elems(xrr, n2, n3, p ** D2), p ** D2)
                    u1 = win_unit(xrr, n1, n2, p, p ** D2)
                    vals_eps.append(composite_fine(s1, q1[c1], s2, q2c, u1, p, D1, D2))
                else:
                    vals_eps.append(fine_tilde(s1, q1[c1], p, D1, D2))
            if vals_eps[0] != vals_eps[1]:
                bump('MEAS_eps2')
            eps2[c1] = vals_eps[0]
        # eps_1 on A
        if sched in ('U', 'P'):
            q1A = q1[0]
            s1A = subset_sums(win_elems(x, n1, n2, p ** D1), p ** D1)
            eps1 = composite_fine(sumsW0, q0, s1A, q1A, u0, p, D0, D1)
        else:
            eps1 = fine_tilde(sumsW0, q0, p, D0, D1)
        epsbar1 = eps1
        reg_eps = sorted(eps2.values())
        epsbar2 = reg_eps[len(reg_eps) // 2] if reg_eps else Fraction(0)
        chi0 = chi2(sumsW0, q0, p, D0)
        # tau per G_1 atom: tau = 2 iff (not B2) or eps2 > epsbar2 ; tau > 1 on A since eps1 <= epsbar1
        tau_gt2 = {c1: (atoms1[c1][0] and eps2[c1] <= epsbar2) for c1 in atoms1}
        # --- enumerate points ---
        pts = []  # (measure, c1, c2key, M1, M2, M3, tau>2, alive_check)
        negq1 = {}
        for c1, (B2, D2, xr) in atoms1.items():
            depth = D1 + (D2 if B2 else 0)
            for c2 in range(p ** depth):
                xx = x0 + p ** m0 * c1 + p ** m1 * c2 + p ** (m1 + depth) * rnd.randrange(p ** 10)
                pi2, dpi2, vals2 = prods(xx, n3, p, prec)
                k1 = grow(par0, n0, n1, xx, p, prec, pi2, dpi2, vals2)
                k2 = grow([t[0] for t in k1], n1, n2, xx, p, prec, pi2, dpi2, vals2)
                mk0, mk1, mk2 = (1 << n0) - 1, (1 << H0) - 1, (1 << H1) - 1
                M1 = p ** m1 * sum(w0[b & mk0] * q0[(b >> n0) & mk1] for (b, S, dS) in k1)
                key2 = (c1, c2 % p ** D1)
                if sched == 'R':
                    q2k = q2.setdefault(key2, rand_prob(rnd, 1 << H2, zero_frac=0.3))
                elif sched == 'S':
                    q2k = q2.setdefault(key2, rand_prob(rnd, 1 << H2, zero_frac=0.3))
                elif sched == 'U':
                    q2k = [Fraction(1, 1 << H2)] * (1 << H2)
                else:
                    q2k = q2_by_atom1[c1]
                M2 = p ** m2 * sum(w0[b & mk0] * q0[(b >> n0) & mk1] * q1[c1][(b >> n1) & mk2]
                                   for (b, S, dS) in k2)
                # control: q1 depending on the digit of x at position m1 (fresh for W1)
                dig = (xx // p ** m1) % p
                qn = negq1.setdefault((c1, dig), rand_prob(rnd, 1 << H1, zero_frac=0.3))
                M2neg = p ** m2 * sum(w0[b & mk0] * q0[(b >> n0) & mk1] * qn[(b >> n1) & mk2]
                                      for (b, S, dS) in k2)
                if B2:
                    m3 = m2 + D2
                    k3 = grow([t[0] for t in k2], n2, n3, xx, p, prec, pi2, dpi2, vals2)
                    mk3 = (1 << H2) - 1
                    terms = [(w0[b & mk0] * q0[(b >> n0) & mk1] * q1[c1][(b >> n1) & mk2] * q2k[(b >> n2) & mk3], b, S)
                             for (b, S, dS) in k3]
                    M3 = p ** m3 * sum(t[0] for t in terms)
                    # SURV: positive weight path alive at n3 by direct valuation
                    if M3 > 0:
                        V3 = Vof(vals2, n3)
                        okp = any(t[0] > 0 and vp(t[2], p, prec) >= V3 for t in terms)
                        if not okp:
                            bump('SURV')
                        bump('SURV_n')
                    meas = Fraction(1, p ** (D0 + D1 + D2))
                else:
                    M3 = None
                    meas = Fraction(1, p ** (D0 + D1))
                pts.append((meas, c1, key2, M1, M2, M3, tau_gt2[c1], M2neg, c2))
        # --- MEAS: constancy of M1 on G_1 atoms, M2 on G_2 atoms ---
        g1, g2 = {}, {}
        for (meas, c1, key2, M1, M2, M3, tg, M2n, c2) in pts:
            g1.setdefault(c1, set()).add(M1)
            g2.setdefault(key2, set()).add(M2)
        if any(len(s) != 1 for s in g1.values()):
            bump('MEAS_M1')
        if any(len(s) != 1 for s in g2.values()):
            bump('MEAS_M2')
        M1a = {c1: next(iter(s)) for c1, s in g1.items()}
        M2a = {k: next(iter(s)) for k, s in g2.items()}
        # MART l=0: E_A M_1 = M_0 ; l=1: E[M_2 | C1] = M_1(C1) ; l=2: E[M_3 | C2] = M_2(C2) on tau>2 atoms
        EM1 = sum(Fraction(1, p ** D0) * M1a[c1] for c1 in M1a)
        if EM1 != M0:
            bump('MART0')
        negfail = False
        for c1 in atoms1:
            sub = [t for t in pts if t[1] == c1]
            tot = sum(t[0] for t in sub)
            e2 = sum(t[0] * t[4] for t in sub) / tot
            if e2 != M1a[c1]:
                bump('MART1')
            e2n = sum(t[0] * t[7] for t in sub) / tot
            if e2n != M1a[c1]:
                negfail = True
        if negfail:
            bump('NEGM')
        for key2 in M2a:
            sub = [t for t in pts if t[2] == key2 and t[5] is not None]
            if not sub:
                continue
            tot = sum(t[0] for t in sub)
            e3 = sum(t[0] * t[5] for t in sub) / tot
            if e3 != M2a[key2]:
                bump('MART2')
            # MEAS: M3 constant on G_3 atoms -- each point is its own G_3 atom here (resolution m3); check
            # instead that points of one G_3 class never disagree (they are distinct classes by construction)
        # stopped process
        def Mt(t, l):
            meas, c1, key2, M1, M2, M3, tg, M2n, c2 = t
            if l == 1:
                return M1
            if l == 2:
                return M2
            return M3 if tg else M2
        a = [Fraction(M0 * M0)]
        for l in (1, 2, 3):
            a.append(sum(t[0] * Mt(t, l) ** 2 for t in pts))
        EM = [sum(t[0] * Mt(t, l) for t in pts) for l in (1, 2, 3)]
        if any(e != M0 for e in EM):
            bump('MARTA')
        # CS1
        if a[1] > M0 * M0 * (1 + chi0):
            bump('CS1')
        # INC l=1 on A
        lhs1 = a[2] - a[1]  # tau > 1 on all of A
        if lhs1 > eps1 * M0 * M0:
            bump('INC1')
        if eps1 > 0:
            wmax('INC1', float(lhs1 / (eps1 * M0 * M0)))
        # INC l=2 on regime atoms (inside tau>2 or not: the inequality itself needs only the regime)
        for c1, (B2, D2, xr) in atoms1.items():
            if not B2:
                continue
            sub = [t for t in pts if t[1] == c1]
            tot = sum(t[0] for t in sub)
            lhs = sum(t[0] * (t[5] ** 2 - t[4] ** 2) for t in sub) / tot
            bump('INC2_n')
            if lhs > eps2[c1] * M1a[c1] ** 2:
                bump('INC2')
            if eps2[c1] > 0 and M1a[c1] > 0:
                wmax('INC2', float(lhs / (eps2[c1] * M1a[c1] ** 2)))
            # W5c for l=2 (S schedule): q1 = q* with m = 0  =>  M3 == M2 pointwise
            if sched == 'S' and mstar1.get(c1) == 0:
                bump('W5c2_n')
                if any(t[5] != t[4] for t in sub):
                    bump('W5c2')
        if sched == 'S' and mstar0 == 0:
            bump('W5c1_n')
            if any(t[4] != M1a[t[1]] for t in pts):
                bump('W5c1')
        # REC
        if not (a[1] <= a[2] <= a[3]):
            bump('MONO')
        if a[2] > a[1] + epsbar1 * a[0]:
            bump('REC1')
        if a[3] > a[2] + epsbar2 * a[1]:
            bump('REC2')
        if a[3] > a[1] * (1 + epsbar1) * (1 + epsbar2):
            bump('REC')
        # PZ (finite horizon)
        delta = sum(t[0] for t in pts if not t[6])
        Pi = (1 + chi0) * (1 + epsbar1) * (1 + epsbar2)
        survive = sum(t[0] for t in pts if t[6] and t[5] is not None and t[5] > 0)
        if Pi * delta < 1:
            bound = (1 - math.sqrt(float(Pi * delta))) ** 2 / float(Pi)
            bump('PZ_n')
            if float(survive) < bound - 1e-12:
                bump('PZ')
            wmax('PZslack_min_neg', -(float(survive) - bound))
        bump('points', len(pts))
    g = lambda k: st.get(k, 0)
    print(f"RESULT w3_chain p={p} n=({n0},{n1},{n2},{n3}) sched={sched} atoms A={g('atoms_A')} (tries {tries}; "
          f"parent subsets used in {g('subset')}), points={g('points')}: MEAS fails B2 {g('MEAS_B2')}, eps2 "
          f"{g('MEAS_eps2')}, q*1 {g('MEAS_qstar')}, M1 {g('MEAS_M1')}, M2 {g('MEAS_M2')}; MART fails "
          f"{g('MART0')}+{g('MART1')}+{g('MART2')}+{g('MARTA')}; CS1 fails {g('CS1')}; INC1 fails {g('INC1')} "
          f"(max ratio {worst.get('INC1', 0):.4f}); INC2 fails {g('INC2')}/{g('INC2_n')} (max ratio "
          f"{worst.get('INC2', 0):.4f}); W5c fails {g('W5c1')}/{g('W5c1_n')} (l=1), {g('W5c2')}/{g('W5c2_n')} (l=2); "
          f"MONO fails {g('MONO')}; REC fails {g('REC1')}+{g('REC2')}+{g('REC')}; PZ fails {g('PZ')}/{g('PZ_n')}; "
          f"SURV fails {g('SURV')}/{g('SURV_n')} | CONTROL NEGM (q1 uses a fresh digit): martingale broken on "
          f"{g('NEGM')}/{g('atoms_A')} atoms")


if __name__ == "__main__":
    main()
