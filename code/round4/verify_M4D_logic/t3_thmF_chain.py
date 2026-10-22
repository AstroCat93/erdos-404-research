#!/usr/bin/env python3
"""t3_thmF_chain.py -- exact test of M4D Theorem F in its STRONG (quantitative) form, finite horizon.

Times n_0 < n_1 < ... < n_{L+1} (deterministic), windows W_l = [n_l, n_{l+1}), jumps D_l (l = 0..L).
Exact data per sample x (nonnegative integer, so every quantity is exact):
  * T_l = { tau_{n_l}(e) mod p^{D_l} : e alive at n_l } for l = 0..L, from the single-step carry
    recursion (validated against brute force in t2) -- an independent route from window sums;
  * lift counts |Lift_l(r)| for the pair (W_l, W_{l+1}) (band D_{l+1}), l = 0..L-1, from window sums.
Theorem F with j = 0, truncated at L, says: if (I) T_0 meets G_0 and (II_l) |G_l| > (1-theta_l) p^{D_l}
for l = 1..L-1, where G_l = { r : |Lift_l(r)| >= theta_{l+1} p^{D_{l+1}} }, then |T_l| >= theta_l p^{D_l}
for l = 1..L.   (The proof's induction gives exactly this finite statement.)
theta schedules tried on every sample (exact Fractions):
  opt_a   : integer thresholds by backward recursion, t_L = a (a = 1, ceil(p^{D_L}/2), p^{D_L}),
            t_l = max(1, p^{D_l} - #{r: Lift_l(r) >= t_{l+1}} + 1); theta_l = t_l / p^{D_l}
  c       : theta_l = c for c in {1, 3/4, 1/2, 1/4, 1/10}
  tao     : theta_l = p^{-D_l}  (Tao's block lemma, chained)
  rand    : theta_l random in (0,1]: 6 draws per sample (lattice t/p^D and non-lattice k/997)
Checks: VIOLATIONS of the conclusion (must be 0); tightness (min |T_l| / (theta_l p^{D_l}), #equalities).
Unconditional per-step check (direct consequence of Lemma L): |T_{l+1}| >= max_{r in T_l} |Lift_l(r)|.
Exact union identity (Lemma L summed over all parents), when cheap:
  T_{l+1} = U_{t in T_l^(K)} { u_l^{-1}(t - s)/p^{D_l} mod p^{D_{l+1}} : s in Lift_l(t mod p^{D_l}) }.
Negative controls (expected to fail sometimes):
  NEG1: (I) alone  =>  T_L nonempty;
  NEG2: (II) weakened to '>=' (t_l = max(1, p^{D_l} - #G_l)) => conclusion.
usage: t3_thmF_chain.py p seed nx KCAP n_0 n_1 ... n_{L+1} [--gate POS DEPTH]
"""
import random
import sys
from fractions import Fraction
from math import ceil

import numpy as np

from vF import make_x, valuations, step_targets_np, subset_sums, window_elems, unit_of_window


def main():
    args = sys.argv[1:]
    forced = ()
    if '--gate' in args:
        k = args.index('--gate')
        forced = ((int(args[k + 1]), int(args[k + 2])),)
        args = args[:k]
    p, seed, nx, KCAP = (int(a) for a in args[:4])
    times = [int(a) for a in args[4:]]
    L = len(times) - 2
    assert L >= 1
    rng = random.Random(seed)
    stats = {}

    def rec(name, hyp, viol, ratios=None, eq=0):
        s = stats.setdefault(name, dict(hyp=0, viol=0, minratio=None, eq=0))
        if hyp:
            s['hyp'] += 1
            s['viol'] += viol
            s['eq'] += eq
            if ratios:
                mr = min(ratios)
                s['minratio'] = mr if s['minratio'] is None else min(s['minratio'], mr)

    nsamp = cens = step_fail = union_checked = union_fail = alive_end = 0
    neg1_hyp = neg1_viol = 0
    while nsamp < nx:
        x = make_x(rng, p, 3 * times[-1] // (p - 1) + 30, forced)
        vals, V = valuations(x, p, times[-1])
        D = [V[times[l + 1]] - V[times[l]] for l in range(L + 1)]
        if any(D[l] + D[l + 1] > KCAP for l in range(L)):
            cens += 1
            continue
        nsamp += 1
        tg = step_targets_np(x, p, vals, V, times[-1], times[:L + 1])
        # T_l mod p^{D_l} and T_l^(K) mod p^{D_l + D_{l+1}}
        T = [set(int(t) % p ** D[l] for t in tg[times[l]]) for l in range(L + 1)]
        TK = [set(int(t) % p ** (D[l] + D[l + 1]) for t in tg[times[l]]) for l in range(L)]
        sup, Lc = [], []
        for l in range(L):
            m = p ** (D[l] + D[l + 1])
            s = subset_sums(window_elems(x, times[l], times[l + 1] - times[l], m), m)
            sup.append(s)
            Lc.append(np.bincount(np.nonzero(s)[0] % p ** D[l], minlength=p ** D[l]))
        if T[L]:
            alive_end += 1
        # unconditional per-step inequality
        for l in range(L):
            if T[l]:
                best = max(int(Lc[l][r]) for r in T[l])
                if len(T[l + 1]) < best:
                    step_fail += 1
        # exact union identity (when cheap)
        for l in range(L):
            mD, mD2 = p ** D[l], p ** D[l + 1]
            cost = sum(int(Lc[l][t % mD]) for t in TK[l])
            if cost > 2_000_000:
                continue
            u = unit_of_window(x, p, times[l], times[l + 1] - times[l], D[l])
            uinv = pow(u % mD2, -1, mD2) if D[l + 1] > 0 else 0
            img = set()
            for t in TK[l]:
                r = t % mD
                th = t // mD
                for k in range(mD2):
                    if sup[l][r + k * mD]:
                        img.add(((th - k) * uinv) % mD2 if D[l + 1] > 0 else 0)
            union_checked += 1
            if img != T[l + 1]:
                union_fail += 1

        def check(name, theta):
            # theta[l] for l = 1..L (theta[0] unused)
            G = [None] * L
            for l in range(L):
                thr = theta[l + 1] * p ** D[l + 1]
                G[l] = {r for r in range(p ** D[l]) if Lc[l][r] >= thr}
            hyp = bool(T[0] & G[0]) and all(len(G[l]) > (1 - theta[l]) * p ** D[l] for l in range(1, L))
            if not hyp:
                rec(name, False, 0)
                return
            ratios, viol, eq = [], 0, 0
            for l in range(1, L + 1):
                need = theta[l] * p ** D[l]
                if len(T[l]) < need:
                    viol += 1
                ratios.append(Fraction(len(T[l])) / need)
                eq += (len(T[l]) == need)
            rec(name, True, viol, ratios, eq)

        # opt schedules
        for tag, tL in (('opt_1', 1), ('opt_half', ceil(p ** D[L] / 2)), ('opt_full', p ** D[L])):
            t = [0] * (L + 1)
            t[L] = tL
            ok = True
            for l in range(L - 1, 0, -1):
                g = int(np.sum(Lc[l] >= t[l + 1]))
                t[l] = max(1, p ** D[l] - g + 1)
                if t[l] > p ** D[l]:
                    ok = False
                    break
            if ok:
                check(tag, [None] + [Fraction(t[l], p ** D[l]) for l in range(1, L + 1)])
            else:
                rec(tag, False, 0)
        for c in (Fraction(1), Fraction(3, 4), Fraction(1, 2), Fraction(1, 4), Fraction(1, 10)):
            check(f'const_{c}', [None] + [c] * L)
        check('tao', [None] + [Fraction(1, p ** D[l]) for l in range(1, L + 1)])
        for _ in range(3):
            check('rand_lattice', [None] + [Fraction(rng.randint(1, p ** D[l]), p ** D[l]) for l in range(1, L + 1)])
            check('rand_k/997', [None] + [Fraction(rng.randint(1, 997), 997) for l in range(1, L + 1)])
        # NEG1: (I) alone => T_L nonempty   (G_0 with theta_1 = p^{-D_1}, i.e. some child exists)
        G0 = {r for r in range(p ** D[0]) if Lc[0][r] >= 1}
        if T[0] & G0:
            neg1_hyp += 1
            if not T[L]:
                neg1_viol += 1
        # NEG2: weakened (II): t_l = max(1, p^{D_l} - #G_l)  (so only |G_l| >= (1-theta_l) p^{D_l})
        t = [0] * (L + 1)
        t[L] = 1
        ok = True
        for l in range(L - 1, 0, -1):
            g = int(np.sum(Lc[l] >= t[l + 1]))
            t[l] = max(1, p ** D[l] - g)
        G = [None] * L
        th = [None] + [Fraction(t[l], p ** D[l]) for l in range(1, L + 1)]
        for l in range(L):
            G[l] = {r for r in range(p ** D[l]) if Lc[l][r] >= th[l + 1] * p ** D[l + 1]}
        hyp = bool(T[0] & G[0]) and all(len(G[l]) >= (1 - th[l]) * p ** D[l] for l in range(1, L))
        viol = sum(len(T[l]) < th[l] * p ** D[l] for l in range(1, L + 1)) if hyp else 0
        rec('NEG2_weak(>=)', hyp, viol)

    print(f"RESULT t3 p={p} seed={seed} times={times} L={L} KCAP={KCAP} forced={forced}: samples={nsamp} "
          f"(censored {cens}), alive at n_L: {alive_end}; per-step |T_l+1|>=max|Lift| fails={step_fail}; "
          f"union identity: checked {union_checked}, fails={union_fail}; "
          f"NEG1 ((I) alone => alive at n_L): hyp {neg1_hyp}, violations {neg1_viol}")
    for name, s in stats.items():
        mr = s['minratio']
        mrs = 'n/a' if mr is None else f"{float(mr):.4f}"
        print(f"  schedule {name:14s}: hypotheses (I)+(II) hold in {s['hyp']:4d} samples; "
              f"conclusion VIOLATIONS {s['viol']}; min |T_l|/(theta_l p^D_l) = {mrs}; equalities {s['eq']}")


if __name__ == "__main__":
    main()
