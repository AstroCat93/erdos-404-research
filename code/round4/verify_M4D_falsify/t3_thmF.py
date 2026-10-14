"""t3: Theorem F (theta-lifting criterion), finite horizon, exhaustive over the
critical theta sequences; special cases (Tao block lemma, theta=1 / R2b);
Prop F2(a) counting bound and the F2(b) key step; negative controls.

Chain: times n_0 < ... < n_{L+1} (windows W_0..W_L), D_l = V_{n_{l+1}} - V_{n_l}.
  T_l      = {tau_{n_l}(e) mod p^{D_l} : e alive at n_l}   (independent DP)
  cnt_l[r] = |Lift_l(r)|, r mod p^{D_l}, band D_{l+1}       (l = 0..L-1)
For start j in [0, L-1] and theta_l = c_l / p^{D_l} (l = j+1..L):
  G_l   = {r : cnt_l[r] >= c_{l+1}}                         (l = j..L-1)
  (I)   T_j meets G_j
  (II_l) |G_l| > p^{D_l} - c_l                               (l = j+1..L-1)
  claim |T_l| >= c_l                                         (l = j+1..L)
Theta only matters through the thresholds; within each interval where G_{l-1}
is constant, the largest theta_l makes (II_l) easiest and the conclusion
hardest, so the critical values c_l in {distinct positive cnt_{l-1}} cover
every theta sequence (exhaustive).  A random subset is also re-evaluated
literally with Fractions (and with random non-critical theta) to validate
this integer reformulation.

Usage: python3 t3_thmF.py p seed nsamples [Hmin Hmax]   (override => L = 2)
"""
import itertools
import random
import sys
import time
from collections import Counter
from fractions import Fraction

from fz_core import (Vlist, Window, alive_paths_dfs, lift_counts, pis,
                     sample_x, target, target_sets_dp, vp, x_with_gate)

MAXMOD = 2 * 10 ** 7
MAXCOMB = 6000
PARAMS = {3: dict(n0=(2, 8), H=(3, 7), L=(2, 4)),
          5: dict(n0=(2, 10), H=(4, 9), L=(2, 4)),
          7: dict(n0=(3, 14), H=(5, 12), L=(2, 4)),
          11: dict(n0=(5, 14), H=(8, 13), L=(2, 3))}
KINDS = ["rand", "rand", "near-2", "negint", "gate-start", "gate-mid",
         "gate-end", "deepgate-F2b"]


def tset(x, p, t, prec):
    """T at time t: targets of alive paths mod p^prec (needs prec <= V_?)."""
    V = Vlist(x, t, p)
    dp = target_sets_dp(x, [t], p, V[t] + prec)
    return {z % p ** prec for z in dp[t]}


def main():
    p = int(sys.argv[1])
    seed = int(sys.argv[2])
    ns = int(sys.argv[3])
    rng = random.Random(seed)
    prm = dict(PARAMS[p])
    if len(sys.argv) > 5:  # optional window-length range override
        prm["H"] = (int(sys.argv[4]), int(sys.argv[5]))
        prm["L"] = (2, 2)
    t0 = time.time()
    st = Counter()
    fails = Counter()
    neg = Counter()
    tight = Counter()
    for it in range(ns):
        kind = KINDS[it % len(KINDS)]
        L = rng.randint(*prm["L"])
        n0 = rng.randint(*prm["n0"])
        Hs = [rng.randint(*prm["H"]) for _ in range(L + 1)]
        times = [n0]
        for h in Hs:
            times.append(times[-1] + h)
        NT = times[-1]
        s = rng.randint(2, 5)
        gate = None
        if kind in ("rand", "near-2", "negint"):
            x, lab = sample_x(p, rng, kind, NT)
        else:
            l = rng.randint(1, L)  # window index receiving the gate
            if kind == "gate-start":
                i = times[l] + 1
            elif kind == "gate-mid":
                i = times[l] + max(1, Hs[l] // 2)
            elif kind == "gate-end":
                i = times[l + 1]
            else:  # deep gate near start of W_{l}, depth s with p^s > 2^d + 2^{H_{l-1}}
                l = rng.randint(1, max(1, L - 1))
                d = rng.randint(1, 2)
                i = times[l] + d
                s = 1
                while p ** s <= 2 ** d + 2 ** Hs[l - 1]:
                    s += 1
                gate = (l, d, s)
            x = x_with_gate(p, rng, i, s)
            lab = "%s(i=%d,s=%d)" % (kind, i, s)
        V = Vlist(x, NT, p)
        Ds = [V[times[l + 1]] - V[times[l]] for l in range(L + 1)]
        if any(p ** (Ds[l] + Ds[l + 1]) > MAXMOD for l in range(L)):
            st["skipped (modulus)"] += 1
            continue
        try:
            Ts = [tset(x, p, times[l], Ds[l]) for l in range(L + 1)]
        except MemoryError:
            st["skipped (memory)"] += 1
            continue
        # cross-check T_0, T_1 with exact DFS when cheap
        for l in range(min(2, L + 1)):
            if times[l] <= (22 if p >= 5 else 16):
                P = pis(x, times[l])
                paths = alive_paths_dfs(x, times[l], p, P=P, cap=200000)
                if paths is not None:
                    st["T cross-checks DP vs DFS"] += 1
                    ref = {target(S, P[-1], p, Ds[l]) for _e, S in paths}
                    if ref != Ts[l]:
                        fails["T DP vs DFS"] += 1
                        print("FAIL T DP vs DFS", lab, x, times[l])
        wins = [Window(x, times[l], times[l + 1], p) for l in range(L + 1)]
        cnts = [lift_counts(wins[l], Ds[l + 1]) for l in range(L)]
        st["chains"] += 1
        pw = [p ** d for d in Ds]

        # ---- special cases, per window pair
        for l in range(L):
            cov = wins[l].sums_mask(Ds[l])
            covers = bool(cov.all())
            Gmin = int((cnts[l] >= 1).sum())
            # Tao: theta_l = p^-D_l  ->  (II_l) <=> W_l covers Z/p^{D_l}
            if (Gmin > pw[l] - 1) != covers:
                fails["Tao special case"] += 1
            # Tao block lemma itself: T_l nonempty and covering -> T_{l+1} nonempty
            if l + 1 <= L and Ts[l] and covers:
                st["Tao block-lemma instances"] += 1
                if not Ts[l + 1]:
                    fails["Tao block lemma"] += 1
            # theta = 1: complete classes; T_l full and a complete class -> T_{l+1} full
            ncomp = int((cnts[l] == pw[l + 1]).sum())
            if len(Ts[l]) == pw[l] and ncomp > 0:
                st["full->full instances"] += 1
                if len(Ts[l + 1]) != pw[l + 1]:
                    fails["fullness propagation"] += 1
            # R2b Thm 10.12 (ii)=>(i) and (i)=>(ii) in M4D's normalisation
            K = Ds[l] + Ds[l + 1]
            arr = wins[l].sums_mask(K)
            Sig = arr.nonzero()[0]
            pK = p ** K
            uinv = pow(wins[l].unit, -1, pw[l + 1]) if pw[l + 1] > 1 else 0
            bycls = {}
            for s_ in Sig:
                bycls.setdefault(int(s_) % pw[l], set()).add(int(s_))
            # build R: one lift tau_rho mod p^K per class rho
            R = []
            for rho in range(pw[l]):
                lifts = [rho + pw[l] * t for t in range(pw[l + 1])]
                if ncomp == 0:
                    miss = [z for z in lifts if z not in bycls.get(rho, set())]
                    R.append(miss[0])
                else:
                    R.append(rng.choice(lifts))
            img = set()
            for tau in R:
                for s_ in bycls.get(tau % pw[l], ()):
                    img.add((((tau - s_) // pw[l]) * uinv) % pw[l + 1] if pw[l + 1] > 1 else 0)
            st["R2b instances"] += 1
            if ncomp > 0 and len(img) != pw[l + 1]:
                fails["R2b (ii)=>(i)"] += 1
            if ncomp == 0 and 0 in img:
                fails["R2b (i)=>(ii) construction"] += 1
            # F2(b) key step: gate at distance d in W_l -> |Sigma_l mod p^s| <= 2^d
        if gate is not None:
            l, d, sg = gate
            m = wins[l].sums_mask(sg)
            st["F2(b) gate instances"] += 1
            if int(m.sum()) > 2 ** d:
                fails["F2(b) |Sigma mod p^s| <= 2^d"] += 1

        # ---- Theorem F, exhaustive critical thetas
        for j in range(L):
            cand = []
            for l in range(j + 1, L + 1):
                cand.append(sorted({int(c) for c in cnts[l - 1] if c > 0}))
            if any(not c for c in cand):
                st["(j) no positive lift anywhere -> hyp. impossible"] += 1
                continue
            ncomb = 1
            for c in cand:
                ncomb *= len(c)
            if ncomb > MAXCOMB:
                combos = [tuple(rng.choice(c) for c in cand) for _ in range(MAXCOMB)]
                combos.append(tuple(c[0] for c in cand))
                combos.append(tuple(c[-1] for c in cand))
                st["theta-sets sampled (too many)"] += 1
            else:
                combos = itertools.product(*cand)
            def hyp_of(c):
                G = {l: {r for r in range(pw[l]) if cnts[l][r] >= c[l + 1]}
                     for l in range(j, L)}
                return bool(Ts[j] & G[j]) and all(
                    len(G[l]) > pw[l] - c[l] for l in range(j + 1, L))
            h_min = hyp_of({l: 1 for l in range(j + 1, L + 1)})
            h_one = hyp_of({l: pw[l] for l in range(j + 1, L + 1)})
            any_hyp = False
            for cs in combos:
                c = {l: cs[l - j - 1] for l in range(j + 1, L + 1)}
                G = {l: {r for r in range(pw[l]) if cnts[l][r] >= c[l + 1]}
                     for l in range(j, L)}
                I = bool(Ts[j] & G[j])
                II = {l: len(G[l]) > pw[l] - c[l] for l in range(j + 1, L)}
                IIge = {l: len(G[l]) >= pw[l] - c[l] for l in range(j + 1, L)}
                concl = {l: len(Ts[l]) >= c[l] for l in range(j + 1, L + 1)}
                hyp = I and all(II.values())
                st["theta-sequences evaluated"] += 1
                if hyp:
                    any_hyp = True
                    st["... with hypotheses true"] += 1
                    if not all(concl.values()):
                        fails["Theorem F"] += 1
                        print("FAIL ThmF", lab, x, times, j, cs)
                    for l in range(j + 1, L + 1):
                        st["... conclusion instances"] += 1
                        slack = len(Ts[l]) - c[l]
                        if slack == 0:
                            tight["|T_l| = theta_l p^D_l exactly"] += 1
                        if c[l] > 1:
                            st["... nontrivial conclusions (theta p^D >= 2)"] += 1
                    # F2(a)
                    for l in range(j + 1, L):
                        lhs = (pw[l] - c[l]) * c[l + 1]
                        if not lhs < 2 ** Hs[l]:
                            fails["F2(a) strict"] += 1
                        if not c[l + 1] <= 2 ** Hs[l]:
                            fails["F2(a) second"] += 1
                # F2(b) consequence: hypotheses must fail
                if gate is not None:
                    lg = gate[0]  # gate in W_lg; need j <= lg-1 and lg <= L-1
                    if j <= lg - 1 and lg <= L - 1:
                        st["F2(b) theta-sets checked"] += 1
                        if hyp:
                            fails["F2(b) criterion should fail"] += 1
                # negative controls
                if I and all(IIge.values()) and not all(concl.values()):
                    neg["'>=' in (II): conclusion fails"] += 1
                if all(II.values()) and not all(concl.values()):
                    neg["drop (I): conclusion fails"] += 1
                # index slip: G_l with theta_l instead of theta_{l+1}
                Gs = {l: {r for r in range(pw[l]) if cnts[l][r] * pw[l] >= c.get(l, 1) * pw[l + 1]}
                      for l in range(j, L)}
                if (Ts[j] & Gs[j]) and all(len(Gs[l]) > pw[l] - c[l] for l in range(j + 1, L)) \
                        and not all(concl.values()):
                    neg["index slip: conclusion fails"] += 1
            if any_hyp:
                st["(j) some theta works"] += 1
                if h_min:
                    st["(j) ... theta=p^-D (Tao) works"] += 1
                if h_one:
                    st["(j) ... theta=1 (R2b) works"] += 1
                if not h_min and not h_one:
                    st["(j) ... ONLY intermediate theta works"] += 1
            # literal Fraction evaluation with random (non-critical) thetas
            for _ in range(12):
                th = {}
                for l in range(j + 1, L + 1):
                    if rng.random() < 0.5:
                        th[l] = Fraction(rng.choice(cand[l - j - 1]), pw[l])
                    else:
                        th[l] = Fraction(rng.randint(1, 10 ** 6), 10 ** 6)
                G = {}
                for l in range(j, L):
                    ok = {cv: Fraction(cv, pw[l + 1]) >= th[l + 1]
                          for cv in {int(z) for z in cnts[l]}}
                    G[l] = {r for r in range(pw[l]) if ok[int(cnts[l][r])]}
                hyp = bool(Ts[j] & G[j]) and all(
                    len(G[l]) > (1 - th[l]) * pw[l] for l in range(j + 1, L))
                st["literal Fraction theta-sets"] += 1
                if hyp:
                    st["... literal with hypotheses true"] += 1
                    if not all(len(Ts[l]) >= th[l] * pw[l] for l in range(j + 1, L + 1)):
                        fails["Theorem F (literal Fractions)"] += 1
                        print("FAIL ThmF literal", lab, x, times, j, th)
    print("p=%d seed=%d samples=%d  time=%.1fs" % (p, seed, ns, time.time() - t0))
    for k in sorted(st):
        print("  %-48s %d" % (k, st[k]))
    print("  tightness:", dict(tight))
    print("  NEG controls:", dict(neg))
    print("  failures:", dict(fails))
    print("TOTAL FAILURES", sum(fails.values()))


if __name__ == "__main__":
    main()
