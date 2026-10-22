#!/usr/bin/env python3
"""t3_global_finite.py -- exact end-to-end test of the chain of Theorems B1 / B1' at a finite horizon.

usage: t3_global_finite.py p n0 n1 rule epsbar L mcap [seed]
  j = 0; window times n_0 < n_1 deterministic, n_2 (and n_3 if L = 3) by the two-step rule `rule`
  (n_2 from x mod p^{m_0}, n_3 from x mod p^{m_1}).  epsbar: deterministic threshold (a Fraction string),
  B_l = {first event (5.2) for [n_{l-1}, n_{l+1})} n {eps_l <= epsbar}, tau = min{l >= 1 : x not in B_l}.
  S := the union of the admissible atoms of G_0 with m_0 <= mcap (mcap = 0: all of them).  The proof of
  B1' uses only that every atom of S is admissible, so it applies verbatim to such a sub-union.
Every atom of G_0 is enumerated exactly (refinement of residues mod p^k); inside each admissible atom the
G_1-, G_2-, G_3-atoms are enumerated exactly.  All quantities are exact Fractions.
Finite-horizon versions of the steps of the proof (stopped process Mt_l = M_{min(l,tau)} 1_S, l <= L;
Y_L = 1_{tau > L-1} M_L 1_S; Pi_L = (1+epsbar)^(L-1); delta_L = mu(S n {tau <= L-1})):
  (mart)  E Mt_l = m* for l = 1..L                           [Cor A' with random times]
  (mono)  a_0 <= a_1 <= ... <= a_L                            [martingale]
  (PropB) a_1 <= Q = E[(1+chi_0^2) M_0^2 1_S]
  (C2rec) a_{l+1} <= a_l + epsbar a_{l-1}, 1 <= l <= L-1     [Prop C2 on atoms of G_{l-1}]
  (CS)    E[Mt_L 1_{tau <= L-1}]^2 <= a_L delta_L
  (PZ)    mu(Y_L > 0) E[Y_L^2] >= (E Y_L)^2
  (final) if m* > sqrt(Pi_L Q delta_L): mu(Y_L > 0) >= (m* - sqrt(Pi_L Q delta_L))^2 / (Pi_L Q)
  (atom)  per atom A of S (Theorem B1 form): if delta_A < 1/Pi_A, mu_A(Y_L>0) >= (1-sqrt(Pi_A delta_A))^2/Pi_A,
          Pi_A = (1+chi_0^2(A)) Pi_L, delta_A = mu_A(tau <= L-1).
  ({Y_L > 0} = {tau > L-1, Z^0_{n_L} != 0} n S by definition; mu(Y_L > 0) is computed exactly.)
"""
import math
import random
import sys
from fractions import Fraction

from vlib import (PAdic, alive_from_scratch, chi2_window, eps_composite, extend, products, rule_hash,
                  rule_ladder, vfact, vtrunc)


def enumerate_atoms(p, n0, kres):
    """atoms of G_0: list of (r, m0) with r < p^m0, M_{n0}(r) < m0 = V_{n0}(r); plus unresolved measure."""
    atoms = []
    unresolved = Fraction(0)
    level = list(range(p))
    k = 1
    while level:
        nxt = []
        for r in level:
            tv = [vtrunc(r + i, p, k) for i in range(1, n0 + 1)]
            if max(tv) < k:
                m0 = sum(tv)
                if m0 == k:
                    atoms.append((r, m0))
                    continue
                assert m0 > k, (r, k, m0)
            if k == kres:
                unresolved += Fraction(1, p ** k)
            else:
                nxt.extend(r + p ** k * t for t in range(p))
        level = nxt
        k += 1
    return atoms, unresolved


class Ev:
    def __init__(self, p, n0, rule, epsbar, L, rnd):
        self.p, self.n0, self.rule, self.epsbar, self.L, self.rnd = p, n0, rule, epsbar, L, rnd
        self.P = PAdic(p, 200)
        self.ndfs = 0
        self.fails_contain = 0

    def zcount(self, x, roots_bits, n_from, n_to):
        """Z^0_{n_to}(x): slope-0 paths alive at n_to, extending all given alive-at-n_from paths."""
        P = self.P
        pi, dpi, vals = products(P, x, n_to)
        roots = []
        for b in roots_bits:
            S = sum(pi[j] for j in range(n_from) if (b >> j) & 1) % P.mod
            dS = sum(dpi[j] for j in range(n_from) if (b >> j) & 1) % P.mod
            roots.append((b, S, dS))
        kids = extend(P, pi, dpi, vals, n_from, n_to, roots)
        self.ndfs += 1
        return sum(1 for t in kids if P.v(t[2]) == 0)

    def vals(self, x, n):
        return [None] + [self.P.v(x + i) for i in range(1, n + 1)]

    def first_event(self, x, ns, ms_prev, ms_cur, l):
        """(5.2) for [n_{l-1}, n_{l+1}) on the G_{l-1} atom of x; returns (ok, D, K, D2)."""
        nn = ns[l + 1]
        v = self.vals(x, nn)
        M = max(v[1:nn + 1])
        m = ms_prev
        if not M < m:
            return False, None, None, None
        Vnext = sum(v[1:nn + 1])
        D = ms_cur - m
        D2 = Vnext - ms_cur
        return D + D2 <= m - M, D, D + D2, D2


def main():
    a = sys.argv[1:]
    p, n0, n1 = int(a[0]), int(a[1]), int(a[2])
    rname = a[3]
    epsbar = Fraction(a[4])
    L = int(a[5])
    mcap = int(a[6])
    seed = int(a[7]) if len(a) > 7 else 1
    assert L in (2, 3) and n0 >= 2 * p and n1 > n0
    rule = rule_ladder() if rname == "ladder" else rule_hash()
    rnd = random.Random(seed)
    E = Ev(p, n0, rule, epsbar, L, rnd)
    P = E.P
    kres = math.ceil(n0 / (p - 1)) + math.floor(math.log(math.e * math.factorial(n0 - 1), p)) + 2
    atoms, unres = enumerate_atoms(p, n0, kres)
    tot = sum(Fraction(1, p ** m) for (_, m) in atoms) + unres
    assert tot == 1, tot
    # global accumulators (exact)
    G = dict(mstar=Fraction(0), Q=Fraction(0), delta=Fraction(0), EY=Fraction(0), EY2=Fraction(0),
             muY=Fraction(0), stopmass=Fraction(0), muS=Fraction(0), adm_excl=Fraction(0))
    EM = [Fraction(0)] * (L + 1)
    a2 = [Fraction(0)] * (L + 1)
    natoms_adm = natoms_S = 0
    atom_checks = atom_fail = 0
    atom_nontriv = 0
    epslist = []
    partial = []
    for (r, m0) in atoms:
        muA = Fraction(1, p ** m0)
        x = r + p ** m0 * rnd.randrange(1, p ** 20)
        pi, dpi, vals = products(P, x, max(n1, n0))
        if not max(vals[1:n1 + 1]) < m0:
            continue
        V1 = sum(vals[1:n1 + 1])
        D0 = V1 - m0
        if not D0 <= m0 - max(vals[1:n1 + 1]):
            continue
        if mcap and m0 > mcap:
            # not enumerated: counts toward an UPPER bound on the excluded admissible measure
            G['adm_excl'] += muA
            continue
        par_all = alive_from_scratch(P, pi, dpi, vals, n0)
        Z0 = sum(1 for t in par_all if P.v(t[2]) == 0)
        if Z0 == 0:
            continue
        natoms_adm += 1
        natoms_S += 1
        bits0 = [t[0] for t in par_all]
        M0 = Fraction(p ** m0 * Z0, 2 ** n0)
        chi2 = chi2_window(x, n0, n1, p, D0)
        # n_2 is a function of x mod p^{m_0}
        n2 = rule(p, r % p ** m0, m0, [n0, n1])
        ns = [n0, n1, n2]
        ok1, Da, K1, D1 = E.first_event(x, ns, m0, V1, 1)
        B1 = False
        if ok1:
            e1 = eps_composite(x, n0, n1, n2, p, Da, K1)
            epslist.append(float(e1))
            B1 = e1 <= epsbar
        # per-atom accumulators (averages over A)
        A_EM = [Fraction(0)] * (L + 1)
        A_EM2 = [Fraction(0)] * (L + 1)
        A_EM[0], A_EM2[0] = M0, M0 * M0
        A_EY = A_EY2 = A_muY = A_stop = A_stopM = Fraction(0)
        w1n = p ** D0
        for w1 in range(w1n):
            x1 = r + p ** m0 * w1 + p ** (m0 + D0) * rnd.randrange(1, p ** 20)
            Z1 = E.zcount(x1, bits0, n0, n1)
            M1 = Fraction(p ** V1 * Z1, 2 ** n1)
            wt1 = Fraction(1, w1n)
            A_EM[1] += wt1 * M1
            A_EM2[1] += wt1 * M1 * M1
            if not B1:  # tau = 1
                for l in range(2, L + 1):
                    A_EM[l] += wt1 * M1
                    A_EM2[l] += wt1 * M1 * M1
                A_stop += wt1
                A_stopM += wt1 * M1
                continue
            m1 = V1
            V2 = m1 + D1
            if L == 2:
                w2n = p ** D1
                for w2 in range(w2n):
                    x2 = r + p ** m0 * w1 + p ** m1 * w2 + p ** V2 * rnd.randrange(1, p ** 20)
                    Z2 = E.zcount(x2, bits0, n0, n2)
                    M2 = Fraction(p ** V2 * Z2, 2 ** n2)
                    wt = wt1 / w2n
                    A_EM[2] += wt * M2
                    A_EM2[2] += wt * M2 * M2
                    A_EY += wt * M2
                    A_EY2 += wt * M2 * M2
                    if M2 > 0:
                        A_muY += wt
                continue
            # L == 3: n_3 is a function of x mod p^{m_1}
            n3 = rule(p, (r + p ** m0 * w1) % p ** m1, m1, [n0, n1, n2])
            ns3 = [n0, n1, n2, n3]
            ok2, Db, K2, D2 = E.first_event(x1, ns3, m1, V2, 2)
            B2 = False
            if ok2:
                e2 = eps_composite(x1, n1, n2, n3, p, Db, K2)
                B2 = e2 <= epsbar
            w2n = p ** D1
            for w2 in range(w2n):
                x2 = r + p ** m0 * w1 + p ** m1 * w2 + p ** V2 * rnd.randrange(1, p ** 20)
                Z2 = E.zcount(x2, bits0, n0, n2)
                M2 = Fraction(p ** V2 * Z2, 2 ** n2)
                wt2 = wt1 / w2n
                A_EM[2] += wt2 * M2
                A_EM2[2] += wt2 * M2 * M2
                if not B2:  # tau = 2
                    A_EM[3] += wt2 * M2
                    A_EM2[3] += wt2 * M2 * M2
                    A_stop += wt2
                    A_stopM += wt2 * M2
                    continue
                V3 = V2 + D2
                w3n = p ** D2
                for w3 in range(w3n):
                    x3 = r + p ** m0 * w1 + p ** m1 * w2 + p ** V2 * w3 + p ** V3 * rnd.randrange(1, p ** 20)
                    Z3 = E.zcount(x3, bits0, n0, n3)
                    M3 = Fraction(p ** V3 * Z3, 2 ** n3)
                    wt = wt2 / w3n
                    A_EM[3] += wt * M3
                    A_EM2[3] += wt * M3 * M3
                    A_EY += wt * M3
                    A_EY2 += wt * M3 * M3
                    if M3 > 0:
                        A_muY += wt
        # global accumulation
        G['muS'] += muA
        G['mstar'] += muA * M0
        G['Q'] += muA * (1 + chi2) * M0 * M0
        G['delta'] += muA * A_stop
        G['EY'] += muA * A_EY
        G['EY2'] += muA * A_EY2
        G['muY'] += muA * A_muY
        G['stopmass'] += muA * A_stopM
        for l in range(L + 1):
            EM[l] += muA * A_EM[l]
            a2[l] += muA * A_EM2[l]
        # per-atom (Theorem B1 form)
        PiA = (1 + chi2) * (1 + epsbar) ** (L - 1)
        if 0 < A_stop < 1:
            partial.append((float(A_stop), float(PiA), float(A_stop * PiA)))
        if A_stop * PiA < 1:
            atom_checks += 1
            if 0 < A_stop:
                atom_nontriv += 1
            bnd = (1 - math.sqrt(float(PiA * A_stop))) ** 2 / float(PiA)
            if float(A_muY) < bnd * (1 - 1e-12):
                atom_fail += 1
    PiL = (1 + epsbar) ** (L - 1)
    mstar, Q, delta = G['mstar'], G['Q'], G['delta']
    print(f"RESULT t3 p={p} n0={n0} n1={n1} rule={rule.name} epsbar={epsbar} L={L} mcap={mcap} kres={kres}")
    print(f"  G_0 atoms: {len(atoms)}; unresolved measure {float(unres):.3e} (non-admissible by Obs. G); "
          f"admissible (m0<=mcap) {natoms_adm}, in S {natoms_S}; mu(S) = {float(G['muS']):.6f}; "
          f"mu(atoms with m0>mcap passing the valuation part of admissibility; upper bound for excluded adm) = "
          f"{float(G['adm_excl']):.3e}; DFS calls {E.ndfs}")
    if epslist:
        es = sorted(epslist)
        print(f"  eps_1 on atoms with the first event: n={len(es)}, min {es[0]:.4g}, median {es[len(es)//2]:.4g}, "
              f"max {es[-1]:.4g}")
    ok = lambda b: "ok" if b else "FAIL"
    print(f"  (mart)  E Mt_l = m* for l=1..L: {ok(all(EM[l] == mstar for l in range(L + 1)))}   m* = {float(mstar):.6g}")
    print(f"  (mono)  a_0<=...<=a_L: {ok(all(a2[l] <= a2[l + 1] for l in range(L)))}   a = "
          + ", ".join(f"{float(t):.6g}" for t in a2))
    print(f"  (PropB) a_1 <= Q: {ok(a2[1] <= Q)}   Q = {float(Q):.6g}")
    c2ok = all(a2[l + 1] <= a2[l] + epsbar * a2[l - 1] for l in range(1, L))
    slack = [float(a2[l] + epsbar * a2[l - 1] - a2[l + 1]) for l in range(1, L)]
    print(f"  (C2rec) a_(l+1) <= a_l + epsbar a_(l-1): {ok(c2ok)}   slack {slack}")
    print(f"  (CS)    E[Mt_L 1_(tau<=L-1)]^2 <= a_L delta: {ok(G['stopmass'] ** 2 <= a2[L] * delta)}   delta = {float(delta):.6g}")
    EY, EY2, muY = G['EY'], G['EY2'], G['muY']
    print(f"  (EY)    E Y_L = m* - E[Mt_L 1_(tau<=L-1)]: {ok(EY == mstar - G['stopmass'])}")
    print(f"  (PZ)    mu(Y>0) E Y^2 >= (E Y)^2: {ok(muY * EY2 >= EY * EY)}   mu(Y_L>0) = {float(muY):.6g}, "
          f"PZ ratio (EY)^2/EY^2 = {float(EY * EY / EY2) if EY2 else 0:.6g}")
    thr = math.sqrt(float(PiL * Q * delta))
    if float(mstar) > thr:
        bnd = (float(mstar) - thr) ** 2 / float(PiL * Q)
        print(f"  (final) m* > sqrt(Pi Q delta) [{float(mstar):.6g} > {thr:.6g}]: bound {bnd:.6g} <= mu(Y_L>0) "
              f"{float(muY):.6g}: {ok(bnd <= float(muY) * (1 + 1e-12))}")
    else:
        print(f"  (final) hypothesis m* > sqrt(Pi Q delta) fails [{float(mstar):.6g} <= {thr:.6g}]: no bound")
    print(f"  (atom)  per-atom B1 bound: checked on {atom_checks} atoms ({atom_nontriv} with 0<delta_A), "
          f"failures {atom_fail}")
    if partial:
        partial.sort(key=lambda t: t[2])
        print(f"          atoms with 0<delta_A<1: {len(partial)}; smallest Pi_A delta_A = {partial[0][2]:.4g} "
              f"(delta_A={partial[0][0]:.4g}, Pi_A={partial[0][1]:.4g})")


if __name__ == "__main__":
    main()
