#!/usr/bin/env python3
"""t2_atom_c2.py -- exact martingale and two-window (C2) steps of Theorem B1 with random window times,
on atoms of G_{l-1}, plus a NEGATIVE CONTROL showing that two-step predictability is load-bearing.

usage: t2_atom_c2.py p seed nx n0 n1 L rule kmax [maxpar] [Hc] [dmin]
(dmin: require D = V_N - V_n >= dmin, so that C contains p^D >= p atoms of G_l; default 1)
For random x: window times n_0..n_L by `rule` (two-step predictable; vlib.window_times).  For a random
l in [1, L-1] let C = x + p^{m_{l-1}} Z_p (an atom of G_{l-1}), n = n_{l-1}, N = n_l, N2 = n_{l+1}.
Require (5.2): D+D2 <= m - M_{N2}, M_{N2} < m, with K = D+D2 <= kmax, D2 >= 1, Z^0_n >= 1.
Enumerate w mod p^K, x' = x0 + p^m w + p^(m+K) z (z random):
  (meas) the window times recomputed from scratch at x' agree with n_{l-1}, n_l, n_{l+1};
  (mart0) c_N E_C Z^0_N == c_n Z^0_n;   (mart1) on every atom C' of G_l inside C: c_N2 E_C' Z^0_N2 == c_N Z^0_N;
  (C2)   c_N2^2 E_C (Z^0_N2)^2 - c_N^2 E_C (Z^0_N)^2 <= eps(W,W') (c_n Z^0_n)^2   [exact];
  (eq)   equality in (C2) when Z^0_n = 1 (single parent; predicted by the round-3 check).
ONE-STEP times (not covered by Theorem B1): candidates N2_k = N + h, 1 <= h <= Hc, satisfying (5.2) on C with
K_k <= kmax.  A choice k(C') per atom C' of G_l (w mod p^D) is a function of x mod p^{m_l}: one-step predictable.
  (negfix) C2 for each fixed k;
  (mon)    Var_C'(c Z^0) is nondecreasing in the end time among valid candidates, on every C';
  (cap)    E_C[max_k Var_C'(k)] <= max_k eps_k (c_n Z^0_n)^2  (one-step times with a G_(l-1)-measurable cap);
  NEGATIVE CONTROL: greedy k(C') maximising Var_C'(k) - eps_k (c_n Z^0_n)^2, compared with the naive bound
  E_C[eps_{k(C')}] (c_n Z^0_n)^2 that uses the G_l-measurable eps of the chosen window.
"""
import random
import sys
from fractions import Fraction

from vlib import (PAdic, alive_from_scratch, eps_composite, extend, products, rule_hash, rule_ladder,
                  window_times)


def main():
    a = sys.argv[1:]
    p, seed, nx, n0, n1, L = (int(t) for t in a[:6])
    rname = a[6]
    kmax = int(a[7])
    maxpar = int(a[8]) if len(a) > 8 else 4000
    Hc = int(a[9]) if len(a) > 9 else 6
    dmin = int(a[10]) if len(a) > 10 else 1
    rule = rule_ladder() if rname == "ladder" else rule_hash()
    P = PAdic(p, 160)
    rnd = random.Random(seed)
    done = tries = 0
    f = dict(meas=0, mart0=0, mart1=0, c2=0, eq=0, negfix=0, mon=0, cap=0)
    c = dict(meas=0, mart0=0, mart1=0, c2=0, eq=0, negfix=0, mon=0, cap=0)
    neg_cases = neg_viol = neg_vary = 0
    worst_neg = 0.0
    worst_naive = 0.0
    worst_c2 = 0.0
    while done < nx and tries < 100000:
        tries += 1
        x = rnd.randrange(P.mod)
        ns, ms = window_times(p, x, n0, n1, rule, L, P)
        l = rnd.randrange(1, L)
        n, N, N2 = ns[l - 1], ns[l], ns[l + 1]
        m = ms[l - 1]
        Nmax = N + Hc
        pi, dpi, vals = products(P, x, max(N2, Nmax))
        M2 = max(vals[1:N2 + 1])
        D, D2 = ms[l] - m, ms[l + 1] - ms[l]
        K = D + D2
        if not (M2 < m and K <= m - M2 and K <= kmax and D2 >= 1 and D >= dmin):
            continue
        par_all = alive_from_scratch(P, pi, dpi, vals, n)
        par0 = [t for t in par_all if P.v(t[2]) == 0]
        if not par0:
            continue
        roots_src = par_all if len(par_all) <= maxpar else par0
        # negative-control candidates N + h satisfying (5.2) on C
        cands = []
        for h in range(1, Hc + 1):
            Nc = N + h
            Mc = max(vals[1:Nc + 1])
            Dc = sum(vals[N + 1:Nc + 1])
            Kc = D + Dc
            if Mc < m and Kc <= m - Mc and Kc <= kmax and Dc >= 1:
                cands.append((Nc, Dc, Kc))
        done += 1
        Kmax = max([K] + [kc for (_, _, kc) in cands])
        x0 = x % p ** m
        Zn = len(par0)
        cn = Fraction(p ** m, 2 ** n)
        cN = Fraction(p ** ms[l], 2 ** N)
        cN2 = Fraction(p ** ms[l + 1], 2 ** N2)
        ends = sorted(set([N2] + [nc for (nc, _, _) in cands]))
        # per class (w mod p^D): Z_N, and sums over the class of Z_end and Z_end^2 for each end
        ZN_cls = {}
        S1 = {e: {} for e in ends}
        S2 = {e: {} for e in ends}
        npts = p ** Kmax
        for w in range(npts):
            z = rnd.randrange(p ** 8)
            xp = x0 + p ** m * w + p ** (m + Kmax) * z
            if w % max(1, npts // 16) == 0:  # measurability of the times at x' (subsample)
                ns2, _ = window_times(p, xp, n0, n1, rule, l + 1, P)
                c['meas'] += 1
                f['meas'] += ns2[:l + 2] != ns[:l + 2]
            pi2, dpi2, vals2 = products(P, xp, ends[-1])
            roots = []
            for (b, _, _) in roots_src:
                S = sum(pi2[j] for j in range(n) if (b >> j) & 1) % P.mod
                dS = sum(dpi2[j] for j in range(n) if (b >> j) & 1) % P.mod
                roots.append((b, S, dS))
            kids = extend(P, pi2, dpi2, vals2, n, N, roots)
            ZN = sum(1 for t in kids if P.v(t[2]) == 0)
            cls = w % p ** D
            if cls in ZN_cls:
                assert ZN_cls[cls] == ZN
            ZN_cls[cls] = ZN
            cur, start = kids, N
            for e in ends:
                cur = extend(P, pi2, dpi2, vals2, start, e, cur)
                start = e
                Z = sum(1 for t in cur if P.v(t[2]) == 0)
                S1[e][cls] = S1[e].get(cls, 0) + Z
                S2[e][cls] = S2[e].get(cls, 0) + Z * Z
        per = npts // p ** D  # points per class
        ncls = p ** D
        # (mart0)
        c['mart0'] += 1
        EZN = Fraction(sum(ZN_cls.values()), ncls)
        f['mart0'] += cN * EZN != cn * Zn
        # (mart1) and (C2) for the rule's N2
        for cls in range(ncls):
            c['mart1'] += 1
            f['mart1'] += cN2 * Fraction(S1[N2][cls], per) != cN * ZN_cls[cls]
        lhs = cN2 ** 2 * Fraction(sum(S2[N2].values()), npts) - cN ** 2 * Fraction(
            sum(z * z for z in ZN_cls.values()), ncls)
        eps = eps_composite(x, n, N, N2, p, D, K)
        rhs = eps * (cn * Zn) ** 2
        c['c2'] += 1
        f['c2'] += lhs > rhs
        if rhs > 0:
            worst_c2 = max(worst_c2, float(lhs / rhs))
        if Zn == 1:
            c['eq'] += 1
            f['eq'] += lhs != rhs
        # negative control
        if len(cands) >= 2:
            neg_cases += 1
            var = {}
            epsk = {}
            for (Nc, Dc, Kc) in cands:
                cNc = Fraction(p ** (ms[l] + Dc), 2 ** Nc)
                var[Nc] = [cNc ** 2 * Fraction(S2[Nc][cls], per) - (cN * ZN_cls[cls]) ** 2 for cls in range(ncls)]
                epsk[Nc] = eps_composite(x, n, N, Nc, p, D, Kc)
                c['negfix'] += 1
                f['negfix'] += Fraction(sum(var[Nc]), ncls) > epsk[Nc] * (cn * Zn) ** 2
            cM2 = (cn * Zn) ** 2
            # (MON) Var_C'(N'_1) <= Var_C'(N'_2) for valid candidates N'_1 < N'_2, on every atom C' of G_l
            cs = sorted(t[0] for t in cands)
            for i1 in range(len(cs) - 1):
                for cls in range(ncls):
                    c['mon'] += 1
                    f['mon'] += var[cs[i1]][cls] > var[cs[i1 + 1]][cls]
            # (NC2) one-step choice, bound with the G_(l-1)-measurable cap max_k eps_k: expected to HOLD
            adv = Fraction(sum(max(var[Nc][cls] for (Nc, _, _) in cands) for cls in range(ncls)), ncls)
            bound = max(epsk.values()) * cM2
            c['cap'] += 1
            f['cap'] += adv > bound
            if bound > 0:
                worst_neg = max(worst_neg, float(adv / bound))
            # (NC1) one-step greedy choice k(C') maximising Var_k(C') - eps_k M^2, compared with the
            # AVERAGED eps E_C[eps_k(C')] M^2: a naive one-step analogue of C2; expected to FAIL sometimes
            ch = [max(cands, key=lambda t: var[t[0]][cls] - epsk[t[0]] * cM2)[0] for cls in range(ncls)]
            lhs1 = Fraction(sum(var[ch[cls]][cls] for cls in range(ncls)), ncls)
            rhs1 = Fraction(sum(epsk[ch[cls]] for cls in range(ncls)), ncls) * cM2
            neg_vary += len(set(ch)) > 1
            if lhs1 > rhs1:
                neg_viol += 1
                if rhs1 > 0:
                    worst_naive = max(worst_naive, float(lhs1 / rhs1))
    print(f"RESULT t2 p={p} n0={n0} n1={n1} L={L} rule={rule.name} kmax={kmax} samples={done} (tries {tries})")
    for k, lab in (('meas', 'window times at x\' agree (G_(l-1)-measurable)'),
                   ('mart0', 'c_N E_C Z_N == c_n Z_n'),
                   ('mart1', 'c_N2 E_C\' Z_N2 == c_N Z_N on every G_l atom'),
                   ('c2', 'C2 with random times, exact'),
                   ('eq', 'C2 equality for a single slope-0 parent'),
                   ('negfix', 'C2 for each fixed candidate window N+h (sanity)'),
                   ('mon', 'Var_C\'(N\'_1) <= Var_C\'(N\'_2) for valid N\'_1 < N\'_2 (monotonicity)'),
                   ('cap', 'one-step choice bounded with cap max_k eps_k (expected to hold)')):
        print(f"  ({k}) {lab}: failures {f[k]}/{c[k]}")
    print(f"  max lhs/(eps M^2) under the rule = {worst_c2:.4f}")
    print(f"  max ratio E_C[max_k Var_k]/(max_k eps_k M^2) = {worst_neg:.4f}")
    print(f"  NEGATIVE CONTROL (naive one-step bound with averaged eps): violated in {neg_viol}/{neg_cases} atoms "
          f"(choice non-constant in {neg_vary}); max violation ratio = {worst_naive:.4f}")


if __name__ == "__main__":
    main()
