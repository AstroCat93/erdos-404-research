#!/usr/bin/env python3
"""w2_concrete.py -- M4D Lemmas W1-W3, Prop W4, Cor W5(c) on REAL windows, aliveness by direct valuations.

x is a random nonnegative integer; W=[n,N), W'=[N,N2); m=V_n, D=V_N-m, D'=V_N2-V_N, K=D+D'.
Only samples satisfying (5.2): D+D' <= m - M_{N2} and M_{N2} < m (M = max valuation) are used.
Parents: the slope-0 paths alive at n for x (a random subset of at most MAXPAR, random weights w >= 0).
For every fresh digit block Wf mod p^K, the point x'' = x0 + p^m Wf + p^(m+K) z (z random) is used and the
children / grandchildren are found by depth-first search with DIRECT valuations at x'' (no linearisation).
Window weights: q on {0,1}^H (fixed on C) in modes unif/rand/sparse/qstar; q' on {0,1}^H2 either fixed
(sharp form) or different on every C' (adapted form; C' = class of Wf mod p^D).

Checks:
  BR   (bridge) child count of each parent at x'' == mu^q_D(tau0_e - beta_e Wf) computed from x0 only
  INH  every child and grandchild has slope 0 (R3M Prop A(i), L=0, used by W1(a))
  FULL (optional, first FULLPTS points) slope-0 paths alive at N computed from scratch at x'' == children
  W1   E_C M_N == E_C M_N2 == M_n (exact)
  W2   Var_C M_N == p^(2m) sum_{eta!=0}|A(eta)|^2 (float rel 1e-9) and <= M_n^2 chi2_q (exact)
  W3a  per parent: q-weighted child targets tau_N((e,f),x'') mod p^D' aggregated over Wf are uniform (exact)
  W3b  per beta-class P_{bu}: E_C|p^{V_N} Psi(xi)|^2 <= (p^m W(P))^2 F^q(xi) (float)
  W4t  E M_N2^2 - E M_N^2 <= eps~^q M_n^2 (exact), q' varying with C'
  W4s  q' fixed: same with eps^{q,q'} (exact)
  W5c  if m(W;D') == 0 and q = q*: M_N2 constant on every C' and equal to M_N(C') (exact)
usage: w2_concrete.py p seed nsamp n H H2 [MAXPAR] [KMAX] [FULLPTS]
"""
import random
import sys
import cmath
from fractions import Fraction

from wlib import (vp, prods, Vof, Mof, grow, alive_slope0, win_elems, win_unit, subset_sums, law, chi2,
                  fine_tilde, composite_fine, fourier, F_fibre, hm_and_qstar, rand_prob, S_and_dS)


def main():
    a = sys.argv[1:]
    p, seed, nsamp, n, H, H2 = (int(t) for t in a[:6])
    maxpar = int(a[6]) if len(a) > 6 else 12
    kmax = int(a[7]) if len(a) > 7 else 6
    fullpts = int(a[8]) if len(a) > 8 else 0
    N, N2 = n + H, n + H + H2
    rnd = random.Random(seed)
    prec = 4 * (N2 // (p - 1) + 12)
    mod = p ** prec
    st = {}

    def bump(k, v=1):
        st[k] = st.get(k, 0) + v

    worst = {'t': 0.0, 's': 0.0}
    done = tries = 0
    while done < nsamp and tries < 200000:
        tries += 1
        x = rnd.randrange(p ** 40)
        pi, dpi, vals = prods(x, N2, p, prec)
        m = Vof(vals, n)
        D = Vof(vals, N) - m
        Dp = Vof(vals, N2) - Vof(vals, N)
        MN2 = Mof(vals, N2)
        if not (MN2 < m and D + Dp <= m - MN2) or D < 1 or Dp < 1 or D + Dp > kmax:
            continue
        par0 = alive_slope0(x, n, p, prec)
        if not par0:
            continue
        done += 1
        bump('samples')
        K = D + Dp
        pK, pD, pDp = p ** K, p ** D, p ** Dp
        if len(par0) > maxpar:
            par0 = rnd.sample(par0, maxpar)
        wts = {b: Fraction(rnd.randint(0, 4)) for b in par0}
        if sum(wts.values()) == 0:
            wts[par0[0]] = Fraction(1)
        Mn = p ** m * sum(wts.values())
        x0 = x % p ** m
        # linearisation data at x0
        pi0, dpi0, _ = prods(x0, N2, p, prec)
        omega = (pi0[n] // p ** m) % mod
        tau0, beta = {}, {}
        for b in par0:
            S, dS = S_and_dS(b, n, pi0, dpi0, mod)
            assert vp(S, p, prec) >= m and vp(dS, p, prec) == 0
            tau0[b] = (-(S // p ** m)) * pow(omega, -1, pK) % pK
            beta[b] = dS * pow(omega, -1, pK) % pK
        ys = win_elems(x, n, N, pK)
        sums = subset_sums(ys, pK)
        ys2 = win_elems(x, N, N2, pDp)
        sums2 = subset_sums(ys2, pDp)
        u = win_unit(x, n, N, p, pDp)
        mm, qstar, _ = hm_and_qstar(sums, p, D, Dp)
        qmodes = [('unif', [Fraction(1, 1 << H)] * (1 << H)), ('rand', rand_prob(rnd, 1 << H)),
                  ('sparse', rand_prob(rnd, 1 << H, zero_frac=0.75)), ('qstar', qstar)]
        q2fixed = rand_prob(rnd, 1 << H2, zero_frac=0.3)
        q2by = {c: rand_prob(rnd, 1 << H2, zero_frac=0.3) for c in range(pD)}
        # enumerate the cylinder once; store children / grandchildren per Wf
        data = []
        maskn, maskH = (1 << n) - 1, (1 << H) - 1
        for Wf in range(pK):
            z = rnd.randrange(p ** 8)
            xx = x0 + p ** m * Wf + p ** (m + K) * z
            pi2, dpi2, vals2 = prods(xx, N2, p, prec)
            assert Vof(vals2, n) == m and Vof(vals2, N) == m + D and Vof(vals2, N2) == m + K
            kids = grow(par0, n, N, xx, p, prec, pi2, dpi2, vals2)
            gkids = grow([k[0] for k in kids], N, N2, xx, p, prec, pi2, dpi2, vals2)
            for (bb, S, dS) in kids + gkids:
                if vp(dS, p, prec) != 0:
                    bump('INH')
            # child targets mod p^Dp at xx
            VN = m + D
            unitN = (pi2[N] // p ** VN) % mod
            ktg = []
            for (bb, S, dS) in kids:
                t = (-(S // p ** VN)) * pow(unitN, -1, pDp) % pDp
                ktg.append((bb & maskn, (bb >> n) & maskH, t))
            gk = [(bb & maskn, (bb >> n) & maskH, bb >> N) for (bb, S, dS) in gkids]
            if done <= 2 and Wf < fullpts:
                full = alive_slope0(xx, N, p, prec)
                allkids = grow(alive_slope0(xx, n, p, prec), n, N, xx, p, prec, pi2, dpi2, vals2)
                if sorted(full) != sorted(k[0] for k in allkids if vp(k[2], p, prec) == 0) or \
                        any(vp(k[2], p, prec) != 0 for k in allkids):
                    bump('FULL')
                bump('FULL_n')
            data.append((Wf, ktg, gk))
        for qname, q in qmodes:
            lawD = law(sums, q, pD)
            s1 = s1sq = s2t = s2t2 = s2s = s2s2 = Fraction(0)
            per_par = {b: {} for b in par0}
            byc = {}
            classes = {}
            for b in par0:
                classes.setdefault(beta[b] % pDp, []).append(b)
            psi = {}
            for (Wf, ktg, gk) in data:
                Z1 = Fraction(0)
                cnt = {}
                for (e, f, t) in ktg:
                    Z1 += wts[e] * q[f]
                    cnt[e] = cnt.get(e, 0) + q[f]
                    per_par[e][t] = per_par[e].get(t, 0) + q[f]
                # bridge
                if qname == 'unif' or qname == 'rand':
                    for e in par0:
                        pred = lawD.get((tau0[e] - beta[e] * Wf) % pD, 0)
                        if cnt.get(e, 0) != pred:
                            bump('BR')
                    bump('BR_n', len(par0))
                Z2t = Z2s = Fraction(0)
                c = Wf % pD
                for (e, f, g) in gk:
                    Z2t += wts[e] * q[f] * q2by[c][g]
                    Z2s += wts[e] * q[f] * q2fixed[g]
                M1 = p ** (m + D) * Z1
                M2t = p ** (m + K) * Z2t
                M2s = p ** (m + K) * Z2s
                s1 += M1
                s1sq += M1 * M1
                s2t += M2t
                s2t2 += M2t * M2t
                s2s += M2s
                s2s2 += M2s * M2s
                byc.setdefault(c, []).append((M1, M2t))
                if qname in ('rand', 'qstar'):
                    for cl, mem in classes.items():
                        for xi in range(1, pDp):
                            zz = 0j
                            for (e, f, t) in ktg:
                                if beta[e] % pDp == cl:
                                    zz += float(wts[e] * q[f]) * cmath.exp(2j * cmath.pi * xi * t / pDp)
                            psi.setdefault((cl, xi), []).append(zz)
            E1 = s1 / pK
            if E1 != Mn or s2t / pK != Mn or s2s / pK != Mn:
                bump('W1')
            var = s1sq / pK - E1 * E1
            tot = 0.0
            for eta in range(1, pD):
                zz = 0j
                for e in par0:
                    bi = pow(beta[e], -1, pD)
                    phi = (tau0[e] % pD) * bi % pD
                    zz += float(wts[e]) * fourier(lawD, eta * bi % pD, pD) * cmath.exp(2j * cmath.pi * eta * phi / pD)
                tot += abs(zz) ** 2
            tot *= float(p ** (2 * m))
            if abs(tot - float(var)) > 1e-9 * max(1.0, float(Mn) ** 2):
                bump('W2id')
            if var > Mn * Mn * chi2(sums, q, p, D):
                bump('W2')
            for e in par0:
                v = [per_par[e].get(s, 0) for s in range(pDp)]
                if len(set(v)) != 1:
                    bump('W3a')
                    break
            for (cl, xi), lst in psi.items():
                WP = float(p ** m * sum(wts[e] for e in classes[cl]))
                lhs = float(p ** (2 * (m + D))) * sum(abs(zz) ** 2 for zz in lst) / pK
                rhs = WP ** 2 * F_fibre(sums, q, p, D, Dp, xi, u)
                bump('W3b_n')
                if lhs > rhs * (1 + 1e-9) + 1e-6:
                    bump('W3b')
            et = fine_tilde(sums, q, p, D, Dp)
            lt = s2t2 / pK - s1sq / pK
            if lt > et * Mn * Mn:
                bump('W4t')
            if et > 0:
                worst['t'] = max(worst['t'], float(lt / (et * Mn * Mn)))
            es = composite_fine(sums, q, sums2, q2fixed, u, p, D, Dp)
            ls = s2s2 / pK - s1sq / pK
            if ls > es * Mn * Mn:
                bump('W4s')
            if es > 0:
                worst['s'] = max(worst['s'], float(ls / (es * Mn * Mn)))
            bump('W4_n')
            if qname == 'qstar' and mm == 0:
                bump('W5c_n')
                if any(any(t2 != lst[0][0] for (_, t2) in lst) for lst in byc.values()):
                    bump('W5c')
            if qname == 'unif' and mm == 0:
                bump('NEGc_n')
                if any(any(t2 != lst[0][0] for (_, t2) in lst) for lst in byc.values()):
                    bump('NEGc')
            if qname == 'qstar' and et != mm:
                bump('W5b')
    g = lambda k: st.get(k, 0)
    print(f"RESULT w2_concrete p={p} n={n} H={H} H2={H2} samples={g('samples')} (tries {tries}): "
          f"bridge fails {g('BR')}/{g('BR_n')}; slope-inheritance fails {g('INH')}; full-population fails "
          f"{g('FULL')}/{g('FULL_n')}; W1 fails {g('W1')}; W2 identity fails {g('W2id')}; W2 bound fails {g('W2')}; "
          f"W3a fails {g('W3a')}; W3b fails {g('W3b')}/{g('W3b_n')}; W4~ fails {g('W4t')}/{g('W4_n')} (max ratio "
          f"{worst['t']:.4f}); W4 sharp fails {g('W4s')}/{g('W4_n')} (max ratio {worst['s']:.4f}); W5b fails "
          f"{g('W5b')}; W5c fails {g('W5c')}/{g('W5c_n')} | CONTROL uniform q with m=0: M_N2 non-constant on some C' "
          f"in {g('NEGc')}/{g('NEGc_n')}")


if __name__ == "__main__":
    main()
