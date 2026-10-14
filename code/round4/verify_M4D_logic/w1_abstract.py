#!/usr/bin/env python3
"""w1_abstract.py -- the algebra of M4D Lemmas W1-W3, Prop W4 and Cor W5 in the linearised model.

The proofs of W1-W5 use the window structure only through the linearisation of R3M Lemma 2(b) and (F2):
inside the cylinder, with the fresh digits Wf in Z/p^K (K = D + D'), uniform,
  parent e (target tau_e mod p^K, unit beta_e mod p^K, weight w_e >= 0)
  child (e,f) alive  <=>  s_f == tau_e - beta_e Wf   (mod p^D)
  its target mod p^D' = u^{-1} * ((tau_e - beta_e Wf - s_f) mod p^K) / p^D
  grandchild (e,f,g) alive <=> s'_g == (child target)  (mod p^D')
Here the s_f (mod p^K) and s'_g (mod p^D') are ARBITRARY multisets (not only window sums), so this tests the
Fourier / Cauchy-Schwarz / Minkowski algebra in more generality than the statements need.
Functionals (the common factor p^m dropped):  M_n = sum_e w_e,  M_N = p^D sum_{alive (e,f)} w_e q_f,
  M_N' = p^K sum_{alive (e,f,g)} w_e q_f q'_g.

Checks per random system (exact Fractions unless marked float):
  W1   E M_N == M_n and E M_N' == M_n (q' adapted: may depend on c = Wf mod p^D)
  W2   Var M_N == sum_{eta != 0} |A(eta)|^2 (float, rel 1e-9);  Var M_N <= M_n^2 chi2_q (exact)
  W3a  for every parent, the q-weighted child-target multiset aggregated over all Wf is uniform mod p^D' (exact;
       equivalent to E Psi(xi) = 0 for all xi != 0, per parent)
  W3b  E|p^D Psi_P(xi)|^2 <= W(P)^2 F^q(xi) for every class P and xi != 0 (float, tol 1e-9)
  W4t  E M_N'^2 - E M_N^2 <= eps~^q M_n^2 (exact), q' varying with c
  W4s  q' fixed: E M_N'^2 - E M_N^2 <= eps^{q,q'} M_n^2 (exact); eps^{q,q'} from composite collisions ==
       sum_xi |hat mu^{q'}(xi)|^2 F^q(xi) (float);  eps~ == sum_xi F^q(xi) (float)
  W4eq single parent, q' fixed: the sharp form is an EQUALITY (exact)  [both CS steps are equalities]
  W5   eps~^{q*} == m (exact); eps~^q >= m for all tested q (exact); if m == 0, with q = q* and q' adapted
       random: M_N' constant on every C' (= every class c) and equal to M_N(c) (exact)
Controls (must be able to fail):
  NEG1 q' depending on the fresh digit Wf (not only on c): W1 for M_N' should fail
  NEG2 W5(c) with uniform q instead of q*: M_N' non-constant on some C'
  NEG3 W4s with the composite law built with unit 2u: equality for a single parent should fail
usage: w1_abstract.py p seed nsys D Dp H Hp npar [mode]
  mode: rand (random residues) | win (sums of y_i = prod_{s<=i}(a+s), a random) | dense (2^H >> p^K)
"""
import random
import sys
import cmath
from fractions import Fraction

from wlib import (subset_sums, law, coll, fine_tilde, chi2, composite_fine, fourier, F_fibre,
                  hm_and_qstar, rand_prob)


def main():
    a = sys.argv[1:]
    p, seed, nsys, D, Dp, H, Hp, npar = (int(t) for t in a[:8])
    mode = a[8] if len(a) > 8 else 'rand'
    rnd = random.Random(seed)
    K = D + Dp
    pK, pD, pDp = p ** K, p ** D, p ** Dp
    st = {k: 0 for k in ['sys', 'W1', 'W2id', 'W2', 'W3a', 'W3b', 'W4t', 'W4s', 'W4sid', 'W4tid', 'W4eq',
                         'W4eq_n', 'W5b', 'W5a', 'W5a_n', 'W5c_n', 'W5c', 'NEG1', 'NEG2', 'NEG2_n', 'NEG3',
                         'NEG3_n', 'W3b_n']}
    worst_t = worst_s = 0.0
    for it in range(nsys):
        # --- random system ---
        if mode == 'win':
            aa = rnd.randrange(p ** 20)
            ys = []
            y = 1
            for i in range(H):
                ys.append(y % pK)
                y = y * (aa + i + 1)
            sums = subset_sums(ys, pK)
            aa2 = rnd.randrange(p ** 20)
            ys2 = []
            y = 1
            for i in range(Hp):
                ys2.append(y % pDp)
                y = y * (aa2 + i + 1)
            sums2 = subset_sums(ys2, pDp) if Dp > 0 else [0] * (1 << Hp)
        elif mode == 'dense':
            ys = [rnd.randrange(pK) for _ in range(H)]
            ys[0] = 1
            sums = subset_sums(ys, pK)
            ys2 = [rnd.randrange(pDp) if Dp > 0 else 0 for _ in range(Hp)]
            sums2 = subset_sums(ys2, pDp) if Dp > 0 else [0] * (1 << Hp)
        else:
            sums = [rnd.randrange(pK) for _ in range(1 << H)]
            sums2 = [rnd.randrange(pDp) for _ in range(1 << Hp)]
        units = [b for b in range(1, pK) if b % p]
        u = rnd.choice([b for b in range(1, max(pDp, 2)) if b % p]) if Dp > 0 else 1
        pars = []
        for _ in range(npar):
            pars.append((rnd.randrange(pK), rnd.choice(units), Fraction(rnd.randint(1, 5))))
        if rnd.random() < 0.3 and npar >= 2:  # force a shared class / shared Newton point sometimes
            t0, b0, w0 = pars[0]
            pars[1] = (t0 if rnd.random() < 0.5 else rnd.randrange(pK), b0, pars[1][2])
        Mn = sum(w for (_, _, w) in pars)
        m, qstar, _a = hm_and_qstar(sums, p, D, Dp)
        # weights q to test
        qlist = [('unif', [Fraction(1, 1 << H)] * (1 << H)), ('rand', rand_prob(rnd, 1 << H)),
                 ('sparse', rand_prob(rnd, 1 << H, zero_frac=0.8)), ('qstar', qstar)]
        pm = [Fraction(0)] * (1 << H)
        pm[rnd.randrange(1 << H)] = Fraction(1)
        qlist.append(('point', pm))
        st['sys'] += 1
        for qname, q in qlist:
            lawK = law(sums, q, pK)
            lawD = law(sums, q, pD)
            q2fixed = rand_prob(rnd, 1 << Hp, zero_frac=0.3)
            q2by = {c: rand_prob(rnd, 1 << Hp, zero_frac=0.3) for c in range(pD)}
            law2fixed = law(sums2, q2fixed, pDp)
            law2by = {c: law(sums2, q2by[c], pDp) for c in range(pD)}
            # NEG1: q' depending on the full fresh digit
            q2neg = {Wf: rand_prob(rnd, 1 << Hp, zero_frac=0.3) for Wf in range(pK)}
            law2neg = {Wf: law(sums2, q2neg[Wf], pDp) for Wf in range(pK)}
            uinv = pow(u, -1, pDp) if Dp > 0 else 0
            u2inv = pow(2 * u % pDp, -1, pDp) if (Dp > 0 and (2 * u) % p) else uinv
            sMN = sMN2 = Fraction(0)
            sMNt = sMNt2 = sMNs = sMNs2 = sneg = Fraction(0)
            sMNeq2 = Fraction(0)
            sMNneg3 = Fraction(0)
            per_par_targets = [dict() for _ in pars]
            Mn_by_c = {}
            byc_t = {}
            # classes by beta mod p^Dp (for W3b)
            classes = {}
            for i, (t, b, w) in enumerate(pars):
                classes.setdefault(b % pDp if Dp > 0 else 0, []).append(i)
            psi = {}  # (class, xi) -> list over Wf of complex Psi
            for Wf in range(pK):
                MN = Fraction(0)
                MNt = MNs = MNneg = MNneg3 = Fraction(0)
                kids_by_par = []
                for i, (t, b, w) in enumerate(pars):
                    tW = (t - b * Wf) % pK
                    kids = []
                    for s, c in lawK.items():
                        if (s - tW) % pD == 0:
                            tgt = ((tW - s) % pK) // pD * uinv % pDp if Dp > 0 else 0
                            kids.append((tgt, w * c, tW, s))
                            per_par_targets[i][tgt] = per_par_targets[i].get(tgt, 0) + c
                            MN += w * c
                    kids_by_par.append(kids)
                MN *= pD
                cW = Wf % pD
                for i, kids in enumerate(kids_by_par):
                    for (tgt, wc, tW, s) in kids:
                        MNt += wc * law2by[cW].get(tgt, 0)
                        MNs += wc * law2fixed.get(tgt, 0)
                        MNneg += wc * law2neg[Wf].get(tgt, 0)
                        if Dp > 0:
                            tg3 = ((tW - s) % pK) // pD * u2inv % pDp
                            MNneg3 += wc * law2fixed.get(tg3, 0)
                MNt *= pK
                MNs *= pK
                MNneg *= pK
                MNneg3 *= pK
                sMN += MN
                sMN2 += MN * MN
                sMNt2 += MNt * MNt
                sMNt += MNt
                sMNs += MNs
                sMNs2 += MNs * MNs
                sneg += MNneg
                sMNneg3 += MNneg3 * MNneg3
                byc_t.setdefault(cW, []).append((MN, MNt))
                # Psi for W3b (float), k = Dp
                if Dp > 0 and qname in ('rand', 'qstar', 'sparse'):
                    for cl, idx in classes.items():
                        for xi in range(1, pDp):
                            z = 0j
                            for i in idx:
                                for (tgt, wc, tW, s) in kids_by_par[i]:
                                    z += float(wc) * cmath.exp(2j * cmath.pi * xi * tgt / pDp)
                            psi.setdefault((cl, xi), []).append(z)
            EMN, EMN2 = sMN / pK, sMN2 / pK
            if EMN != Mn or sMNt / pK != Mn or sMNs / pK != Mn:
                st['W1'] += 1
            if sneg / pK != Mn:
                st['NEG1'] += 1
            var = EMN2 - EMN * EMN
            # W2 identity (float)
            beta_inv = [pow(b, -1, pD) if D > 0 else 0 for (_, b, _) in pars]
            if D > 0:
                tot = 0.0
                for eta in range(1, pD):
                    z = 0j
                    for i, (t, b, w) in enumerate(pars):
                        phi = (t % pD) * beta_inv[i] % pD
                        z += float(w) * fourier(lawD, eta * beta_inv[i] % pD, pD) * cmath.exp(
                            2j * cmath.pi * eta * phi / pD)
                    tot += abs(z) ** 2
                if abs(tot - float(var)) > 1e-9 * max(1.0, float(Mn) ** 2):
                    st['W2id'] += 1
            if var > Mn * Mn * chi2(sums, q, p, D):
                st['W2'] += 1
            # W3a: per parent, aggregated child targets uniform mod p^Dp
            if Dp > 0:
                for i in range(len(pars)):
                    vals = [per_par_targets[i].get(s, 0) for s in range(pDp)]
                    if len(set(vals)) != 1:
                        st['W3a'] += 1
                        break
            # W3b
            if psi:
                for (cl, xi), lst in psi.items():
                    WP = float(sum(pars[i][2] for i in classes[cl]))
                    lhs = (pD ** 2) * sum(abs(z) ** 2 for z in lst) / pK
                    rhs = WP ** 2 * F_fibre(sums, q, p, D, Dp, xi, u)
                    st['W3b_n'] += 1
                    if lhs > rhs * (1 + 1e-9) + 1e-9:
                        st['W3b'] += 1
            # W4 adapted
            et = fine_tilde(sums, q, p, D, Dp)
            lhs_t = sMNt2 / pK - EMN2
            if lhs_t > et * Mn * Mn:
                st['W4t'] += 1
            if et > 0:
                worst_t = max(worst_t, float(lhs_t / (et * Mn * Mn)))
            # W4 sharp
            es = composite_fine(sums, q, sums2, q2fixed, u, p, D, Dp)
            lhs_s = sMNs2 / pK - EMN2
            if lhs_s > es * Mn * Mn:
                st['W4s'] += 1
            if es > 0:
                worst_s = max(worst_s, float(lhs_s / (es * Mn * Mn)))
            if Dp > 0 and qname in ('rand', 'qstar'):
                fs = [F_fibre(sums, q, p, D, Dp, xi, u) for xi in range(1, pDp)]
                es_f = sum(abs(fourier(law2fixed, xi, pDp)) ** 2 * fs[xi - 1] for xi in range(1, pDp))
                if abs(es_f - float(es)) > 1e-9 * max(1.0, abs(float(es))):
                    st['W4sid'] += 1
                if abs(sum(fs) - float(et)) > 1e-9 * max(1.0, abs(float(et))):
                    st['W4tid'] += 1
            if len(pars) == 1:
                st['W4eq_n'] += 1
                if lhs_s != es * Mn * Mn:
                    st['W4eq'] += 1
                if Dp > 0 and (2 * u) % pDp != u % pDp and (2 * u) % p:
                    st['NEG3_n'] += 1
                    if sMNneg3 / pK - EMN2 != es * Mn * Mn:
                        st['NEG3'] += 1
            # W5
            if et < m:
                st['W5a'] += 1
            st['W5a_n'] += 1
            if qname == 'qstar':
                if et != m:
                    st['W5b'] += 1
                if m == 0:
                    st['W5c_n'] += 1
                    for cW, lst in byc_t.items():
                        if any(t2 != lst[0][0] for (_, t2) in lst):
                            st['W5c'] += 1
                            break
            if qname == 'unif' and m == 0:
                st['NEG2_n'] += 1
                if any(any(t2 != lst[0][1] for (_, t2) in lst) for lst in byc_t.values()):
                    st['NEG2'] += 1
    print(f"RESULT w1_abstract p={p} D={D} D'={Dp} H={H} H'={Hp} npar={npar} mode={mode} systems={st['sys']} "
          f"(x5 weightings): W1 fails {st['W1']}; W2 identity fails {st['W2id']}; W2 bound fails {st['W2']}; "
          f"W3a fails {st['W3a']}; W3b fails {st['W3b']}/{st['W3b_n']}; W4~ fails {st['W4t']} (max ratio "
          f"{worst_t:.4f}); W4 sharp fails {st['W4s']} (max ratio {worst_s:.4f}); Fourier ids fail "
          f"{st['W4sid']}+{st['W4tid']}; single-parent equality fails {st['W4eq']}/{st['W4eq_n']}; "
          f"W5a fails {st['W5a']}/{st['W5a_n']}; W5b fails {st['W5b']}; W5c fails {st['W5c']}/{st['W5c_n']} | "
          f"CONTROLS: NEG1 (q' uses fresh digit) W1 broken in {st['NEG1']}/{st['sys'] * 5}; "
          f"NEG2 (uniform q, m=0) non-constant in {st['NEG2']}/{st['NEG2_n']}; "
          f"NEG3 (unit 2u) equality broken in {st['NEG3']}/{st['NEG3_n']}")


if __name__ == "__main__":
    main()
