"""t2: Lemma L (lifting lemma) by brute force, with edge cases.

For a window W=[n,N), next window W'=[N,N'), D=V_N-V_n, D'=V_N'-V_N, K=D+D':
  Sigma   = {Q_f mod p^K}           (numpy bitset of the 2^H window sums)
  Lift(r) = {s in Sigma: s = r mod p^D}
  lambda  : s -> u^{-1} (tau - s)/p^D mod p^D'
Claim (Lemma L): for every parent e alive at n with target tau, r = tau mod p^D,
  lambda is injective on Lift(r) and lambda(Lift(r)) = C(e) :=
  {tau_N((e,f)) mod p^D' : (e,f) alive at N}.
C(e) is computed by BRUTE FORCE over all 2^H words f, with aliveness decided
by the definition p^{V_N} | S_e + sum_i f_i pi_{n+i} (exact integers) and the
target by the definition -S/pi_N.  No use of (F2), Q_f, or u on this side.

Also checked: lift_counts() (used in t3/t4) == |Lift(r)| by set filtering;
"children cover Z/p^D' iff r complete".
Negative controls: lambda with 2u in place of u; lambda with p^(D+1) in place
of p^D (when meaningful).  Records slopes v(S_e'(x)) of the tested parents
and whether R3M's linear-regime condition D+D' <= V_n - M_N' holds.

Usage: python3 t2_lemmaL.py p seed nsamples [Hmax]
"""
import random
import sys
import time
from collections import Counter

from fz_core import (Mval, Vlist, Window, alive_paths_dfs, dpis, lift_counts,
                     pis, rand_unit, sample_x, target, vp, x_with_gate)

KINDS = ["rand", "near-1", "near-2", "negint", "gate-W-start", "gate-W-mid",
         "gate-at-N", "gate-W'-start", "gate-W'-mid", "gate-at-N'"]
MAXMOD = 3 * 10 ** 7


def main():
    p = int(sys.argv[1])
    seed = int(sys.argv[2])
    ns = int(sys.argv[3])
    rng = random.Random(seed)
    t0 = time.time()
    stat = Counter()
    slopes = Counter()
    kinds_done = Counter()
    fails = Counter()
    neg = Counter()
    Hmax = int(sys.argv[4]) if len(sys.argv) > 4 else (11 if p >= 5 else 10)
    for it in range(ns):
        kind = KINDS[it % len(KINDS)]
        n = rng.randint(1, 16 if p >= 5 else 12)
        H = rng.randint(1, Hmax)
        H2 = rng.randint(1, 10)
        N, N2 = n + H, n + H + H2
        s = rng.randint(1, 6 if p >= 5 else 4)
        if kind in ("rand", "near-1", "near-2", "negint"):
            x, lab = sample_x(p, rng, kind, N2)
        else:
            if kind == "gate-W-start":
                i = n + 1
            elif kind == "gate-W-mid":
                i = n + max(1, H // 2)
            elif kind == "gate-at-N":
                i = N
            elif kind == "gate-W'-start":
                i = N + 1
            elif kind == "gate-W'-mid":
                i = N + max(1, H2 // 2)
            else:
                i = N2
            x = x_with_gate(p, rng, i, s)
            lab = "%s(i=%d,s=%d)" % (kind, i, s)
        V = Vlist(x, N2, p)
        D, D2 = V[N] - V[n], V[N2] - V[N]
        K = D + D2
        if p ** K > MAXMOD:
            stat["skipped (p^K too large)"] += 1
            continue
        P = pis(x, N2)
        dP = dpis(x, N2)
        parents = alive_paths_dfs(x, n, p, P=P, V=V, cap=300000)
        if parents is None:
            stat["skipped (too many parents)"] += 1
            continue
        kinds_done[kind] += 1
        if D == 0:
            stat["windows with D = 0"] += 1
        if D2 == 0:
            stat["windows with D' = 0"] += 1
        if D >= 3 or D2 >= 3:
            stat["windows with D or D' >= 3"] += 1
        regime = (K <= V[n] - Mval(x, N2, p)) and (Mval(x, N2, p) < V[n])
        stat["windows"] += 1
        stat["windows in linear regime" if regime else "windows OUTSIDE linear regime"] += 1
        if not parents:
            stat["windows with no alive parent"] += 1
            continue
        W = Window(x, n, N, p)
        assert W.D == D
        M = p ** K
        arr = W.sums_mask(K)
        Sigma = [int(z) for z in arr.nonzero()[0]]
        cnts = lift_counts(W, D2)
        pD, pD2 = p ** D, p ** D2
        uinv = pow(W.unit, -1, pD2) if pD2 > 1 else 0
        uinv_bad = pow(2 * W.unit, -1, pD2) if pD2 > 1 else 0
        # exact subset sums of pi_{n+i}, i<H, for the brute-force children
        PS = [0]
        for i in range(H):
            PS = PS + [z + P[n + i] for z in PS]
        qN = p ** V[N]
        # parent selection: all if few, else random + highest slope
        def slope(e):
            return vp(sum(dP[j] for j in range(n) if e[j]) or p ** 99, p)
        if len(parents) > 40:
            sl = sorted(parents, key=lambda es: -slope(es[0]))
            chosen = sl[:10] + rng.sample(sl[10:], 30)
        else:
            chosen = parents
        for e, Se in chosen:
            sv = slope(e)
            slopes[min(sv, 6)] += 1
            tau = target(Se, P[n], p, K)
            r = tau % pD
            lift = [s_ for s_ in Sigma if s_ % pD == r]
            lam = [(((tau - s_) // pD) * uinv) % pD2 if pD2 > 1 else 0 for s_ in lift]
            # brute-force children
            C = set()
            nchild = 0
            for z in PS:
                Sc = Se + z
                if Sc % qN == 0:
                    nchild += 1
                    C.add(target(Sc, P[N], p, D2))
            stat["parents"] += 1
            stat["children (brute force)"] += nchild
            if nchild == 0:
                stat["childless parents"] += 1
            if len(lift) == pD2:
                stat["parents with complete lift"] += 1
            if set(lam) != C:
                fails["image"] += 1
                print("FAIL image", lab, x, n, N, N2, e)
            if len(set(lam)) != len(lift):
                fails["injective"] += 1
                print("FAIL injective", lab, x, n, N, N2, e)
            if len(C) != len(lift):
                fails["count"] += 1
            if int(cnts[r]) != len(lift):
                fails["lift_counts helper"] += 1
            if (len(C) == pD2) != (len(lift) == pD2):
                fails["cover iff complete"] += 1
            # negative controls (only meaningful when D2 >= 1 and children exist)
            if D2 >= 1 and lift:
                stat["NEG-eligible parents"] += 1
                lam_bad = {(((tau - s_) // pD) * uinv_bad) % pD2 for s_ in lift}
                if lam_bad != C:
                    neg["2u detected"] += 1
                if K + 1 <= K and False:
                    pass
                # wrong divisor: shift by one extra p (uses tau mod p^K only)
                if D2 >= 2:
                    lam_bad2 = {((((tau - s_) // pD) // p) * uinv) % pD2 for s_ in lift}
                    stat["NEG2-eligible parents"] += 1
                    if lam_bad2 != C:
                        neg["p^(D+1) detected"] += 1
    print("p=%d seed=%d samples=%d  time=%.1fs" % (p, seed, ns, time.time() - t0))
    for k in sorted(stat):
        print("  %-34s %d" % (k, stat[k]))
    print("  kinds:", dict(kinds_done))
    print("  parent slopes v(S_e'(x)) (6 = >=6):", dict(sorted(slopes.items())))
    print("  NEG controls:", dict(neg))
    print("  failures:", dict(fails))
    print("TOTAL FAILURES", sum(fails.values()))


if __name__ == "__main__":
    main()
