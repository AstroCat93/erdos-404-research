#!/usr/bin/env python3
"""ck_edge.py -- sharp (equality-case) and boundary tests of R3M Proposition C2 and Proposition A.
Second check_R3M instance (round 3).  Uses only ck_lib.py (validated against brute force in
validate_lib.log); shares no code with code/round3/R3M/.

mode C2eq  p seed nx n H H2 where maxpar kmax
  Windows W=[n,N), W'=[N,N'), N=n+H, N'=N+H2, m=V_n(x), D=V_N-m, D'=V_N'-V_N, K=D+D'.
  where = in   : (5.2) D+D' <= m-M_N', M_N' < m           (hypothesis of Prop C2)
          edge : D+D' == m-M_N' exactly, M_N' < m           (boundary, still inside)
          out  : D+D' == m-M_N'+1, M_N' < m                 (just outside (5.2))
          s<k> : m-M_N'-(D+D') == k exactly (k may be negative: further outside (5.2))
  For each slope-0 parent e (at most maxpar per x) the descendants of e alone are followed:
  for EVERY w mod p^K, x' = x0 + p^m w + p^(m+K) z (z random high digits, fresh per w),
    Z1(w) = #children of e alive at N at x',  Z2(w) = #grandchildren alive at N' at x'.
  The proof of Prop C2 (Cauchy-Schwarz over parents in Lemma C1(b), Minkowski over classes) is
  lossless when the parent set is a single path, so it predicts the EXACT identity
      c_N'^2 E[Z2^2] - c_N^2 E[Z1^2] == eps(W,W') c_n^2 ,
  eps = p^K Coll_K - p^D Coll_D of the composite window (exact rationals).  Also checked:
  martingale c_N E Z1 = c_N' E Z2 = c_n, every child/grandchild has slope 0 at x' (A(i)).
  In addition, for the FULL slope-0 population (if it has at most maxpar members) the C2
  inequality itself is checked, and x with Z^0_n = 1 give the full-population equality case.
  When (5.2) holds, also the equality case of Prop B / Prop N for a single parent:
      c_N^2 E[Z1^2] - c_n^2 == c_n^2 chi^2_W,   chi^2_W = p^D Coll_D(W) - 1   (exact).

mode Aedge p seed nx n N L where maxpar
  Prop A(iii) at the boundary of its hypotheses (W1) N-n >= pL, (W2) D+L <= m-M_n,
  (W3) L < m-M_N:  where = w2edge (D+L == m-M_n), w3edge (L == m-M_N-1),
  w2out (D+L == m-M_n+1, W1,W3 hold), w3out (L == m-M_N, W1,W2 hold).
  For each parent of slope lam <= L and each state s mod p^lam:
      avg over w mod p^(D+L+1) [one extra digit, z random] of #{children in state s}
      == 2^(N-n) p^-D a_n^(lam)(s_e)          (exact Fractions)
  a_n^(lam) by enumeration of all 2^(p lam) subsets of the first p*lam window terms.
"""
import random
import sys
from fractions import Fraction

from ck_lib import PAdic, products, alive_from_scratch, extend, target, collision


def window_elems(x, a, b):
    """[pi_j(x)/pi_a(x) for a <= j < b] as exact integers."""
    out = []
    q = 1
    for j in range(a, b):
        if j > a:
            q *= x + j
        out.append(q)
    return out


def eval_path(P, pi, dpi, n, b):
    S = 0
    dS = 0
    for j in range(n):
        if (b >> j) & 1:
            S += pi[j]
            dS += dpi[j]
    return S % P.mod, dS % P.mod


def mode_C2eq(p, seed, nx, n, H, H2, where, maxpar, kmax):
    N, N2 = n + H, n + H + H2
    prec = max(80, 3 * N2 // (p - 1) + 40)
    P = PAdic(p, prec)
    rnd = random.Random(seed)
    done = tries = 0
    n_par = n_eq = n_mart_f = n_slope_f = 0
    n_full = n_full_f = n_full_one = n_full_one_eq = 0
    n_B1 = n_B1_eq = 0
    ratios = []
    while done < nx and tries < 300000:
        tries += 1
        x = rnd.randrange(P.mod)
        pi, dpi, vals = products(P, x, N2)
        m = sum(vals[1:n + 1])
        VN = sum(vals[1:N + 1])
        VN2 = sum(vals[1:N2 + 1])
        D, D2 = VN - m, VN2 - VN
        K = D + D2
        MN2 = max(vals[1:N2 + 1])
        if not (MN2 < m and D2 >= 1 and K <= kmax):
            continue
        slack = m - MN2 - K
        if where == "in" and slack < 0:
            continue
        if where == "edge" and slack != 0:
            continue
        if where == "out" and slack != -1:
            continue
        if where.startswith("s") and slack != int(where[1:]):
            continue
        par_all = alive_from_scratch(P, pi, dpi, vals, n)
        par0 = [b for (b, S, dS) in par_all if P.v(dS) == 0]
        if not par0:
            continue
        done += 1
        full = len(par0) <= maxpar
        chosen = par0 if full else rnd.sample(par0, maxpar)
        x0 = x % p ** m
        cn = Fraction(p ** m, 2 ** n)
        cN = Fraction(p ** VN, 2 ** N)
        cN2 = Fraction(p ** VN2, 2 ** N2)
        ys = window_elems(x, n, N2)
        eps = p ** K * collision(ys, p ** K) - p ** D * collision(ys, p ** D)
        chi2W = p ** D * collision(ys[:N - n], p ** D) - 1   # chi^2 of the first window W alone
        mdK = p ** K
        s1 = {b: 0 for b in chosen}
        s1q = {b: 0 for b in chosen}
        s2 = {b: 0 for b in chosen}
        s2q = {b: 0 for b in chosen}
        f1 = f1q = f2 = f2q = 0
        for w in range(mdK):
            z = rnd.randrange(p ** 8)
            xp = x0 + p ** m * w + p ** (m + K) * z
            pi2, dpi2, vals2 = products(P, xp, N2)
            T1 = T2 = 0
            for b in chosen:
                S, dS = eval_path(P, pi2, dpi2, n, b)
                kids = extend(P, pi2, dpi2, vals2, n, N, [(b, S, dS)])
                gk = extend(P, pi2, dpi2, vals2, N, N2, kids)
                if slack >= 0:
                    if any(P.v(t[2]) != 0 for t in kids) or any(P.v(t[2]) != 0 for t in gk):
                        n_slope_f += 1
                z1, z2 = len(kids), len(gk)
                s1[b] += z1
                s1q[b] += z1 * z1
                s2[b] += z2
                s2q[b] += z2 * z2
                T1 += z1
                T2 += z2
            f1 += T1
            f1q += T1 * T1
            f2 += T2
            f2q += T2 * T2
        for b in chosen:
            n_par += 1
            if not (cN * Fraction(s1[b], mdK) == cn and cN2 * Fraction(s2[b], mdK) == cn):
                n_mart_f += 1
            # Prop B / Prop N equality case |P| = 1:  Var_C(c_N Z1) == c_n^2 chi^2_W
            if slack >= 0:
                n_B1 += 1
                n_B1_eq += cN ** 2 * Fraction(s1q[b], mdK) - cn ** 2 == cn ** 2 * chi2W
            lhs = cN2 ** 2 * Fraction(s2q[b], mdK) - cN ** 2 * Fraction(s1q[b], mdK)
            rhs = eps * cn ** 2
            if lhs == rhs:
                n_eq += 1
            if rhs != 0:
                ratios.append(float(lhs / rhs))
        if full:
            n_full += 1
            lhs = cN2 ** 2 * Fraction(f2q, mdK) - cN ** 2 * Fraction(f1q, mdK)
            rhs = eps * (cn * len(par0)) ** 2
            if lhs > rhs:
                n_full_f += 1
            if len(par0) == 1:
                n_full_one += 1
                n_full_one_eq += lhs == rhs
    rmin = min(ratios) if ratios else float("nan")
    rmax = max(ratios) if ratios else float("nan")
    print(f"RESULT C2eq p={p} n={n} H={H} H2={H2} where={where} samples={done}: single-parent pairs={n_par}, "
          f"exact equality lhs==eps*c_n^2 in {n_eq}/{n_par} (lhs/rhs range [{rmin:.6g},{rmax:.6g}]); "
          f"martingale fails={n_mart_f}; slope-0 inheritance fails={n_slope_f}; "
          f"full-population C2 inequality fails={n_full_f}/{n_full}; full population of size 1: "
          f"equality {n_full_one_eq}/{n_full_one}; Prop B equality |P|=1 (Var == c_n^2 chi^2_W): "
          f"{n_B1_eq}/{n_B1}")


def frozen_law(x, p, n, lam):
    md = p ** lam
    if lam == 0:
        return {0: Fraction(1)}
    L = p * lam
    ys = [y % md for y in window_elems(x, n, n + L)]
    cnt = {}
    for mask in range(2 ** L):
        s = 0
        for i in range(L):
            if (mask >> i) & 1:
                s += ys[i]
        s %= md
        cnt[s] = cnt.get(s, 0) + 1
    return {t: Fraction(c, 2 ** L) for t, c in cnt.items()}


def mode_Aedge(p, seed, nx, n, N, L, where, maxpar):
    prec = max(80, 3 * N // (p - 1) + 40)
    P = PAdic(p, prec)
    rnd = random.Random(seed)
    done = tries = 0
    n_par = n_ok = n_states = n_states_bad = 0
    while done < nx and tries < 300000:
        tries += 1
        x = rnd.randrange(P.mod)
        pi, dpi, vals = products(P, x, N)
        m = sum(vals[1:n + 1])
        VN = sum(vals[1:N + 1])
        D = VN - m
        Mn_, MN = max(vals[1:n + 1]), max(vals[1:N + 1])
        if not MN < m:
            continue
        W1 = N - n >= p * L
        W2 = D + L <= m - Mn_
        W3 = L < m - MN
        if where == "w2edge" and not (W1 and W3 and D + L == m - Mn_):
            continue
        if where == "w3edge" and not (W1 and W2 and L == m - MN - 1):
            continue
        if where == "w2out" and not (W1 and W3 and D + L == m - Mn_ + 1):
            continue
        if where == "w3out" and not (W1 and W2 and L == m - MN):
            continue
        par_all = alive_from_scratch(P, pi, dpi, vals, n)
        par = [(b, S, dS) for (b, S, dS) in par_all if P.v(dS) <= L]
        if not par:
            continue
        done += 1
        if len(par) > maxpar:
            par = rnd.sample(par, maxpar)
        lam_of = {b: P.v(dS) for (b, S, dS) in par}
        s_e = {b: target(P, S, pi[n], m) % p ** lam_of[b] for (b, S, dS) in par}
        a_n = {lam: frozen_law(x, p, n, lam) for lam in set(lam_of.values())}
        R = D + L + 1
        x0 = x % p ** m
        counts = {b: {} for b in lam_of}
        for w in range(p ** R):
            z = rnd.randrange(p ** 8)
            xp = x0 + p ** m * w + p ** (m + R) * z
            pi2, dpi2, vals2 = products(P, xp, N)
            for b in lam_of:
                S, dS = eval_path(P, pi2, dpi2, n, b)
                for (b2, S2, dS2) in extend(P, pi2, dpi2, vals2, n, N, [(b, S, dS)]):
                    lam = lam_of[b]
                    st = target(P, S2, pi2[N], VN) % p ** lam
                    counts[b][st] = counts[b].get(st, 0) + 1
        for b in lam_of:
            lam = lam_of[b]
            n_par += 1
            pred = Fraction(2 ** (N - n), p ** D) * a_n[lam].get(s_e[b], 0)
            good = True
            for s in range(p ** lam):
                n_states += 1
                if Fraction(counts[b].get(s, 0), p ** R) != pred:
                    good = False
                    n_states_bad += 1
            n_ok += good
    print(f"RESULT Aedge p={p} n={n} N={N} L={L} where={where} samples={done}: parents with (iii) exact "
          f"{n_ok}/{n_par}; (parent,state) mismatches {n_states_bad}/{n_states}")


def main():
    mode = sys.argv[1]
    a = sys.argv[2:]
    if mode == "C2eq":
        p, seed, nx, n, H, H2 = (int(t) for t in a[:6])
        where = a[6]
        maxpar, kmax = int(a[7]), int(a[8])
        mode_C2eq(p, seed, nx, n, H, H2, where, maxpar, kmax)
    elif mode == "Aedge":
        p, seed, nx, n, N, L = (int(t) for t in a[:6])
        mode_Aedge(p, seed, nx, n, N, L, a[6], int(a[7]))


if __name__ == "__main__":
    main()
