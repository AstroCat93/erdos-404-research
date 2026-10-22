#!/usr/bin/env python3
"""ck_propA.py -- independent exact test of R3M Proposition A (odd-p one-window identity),
Corollary A' (weighted martingale identity) and the inheritance statement A(i).

For random x (PREC p-adic digits) satisfying (W1) N-n >= pL, (W2) D+L <= m-M_n, (W3) L < m-M_N
and M_N < m, where m = V_n(x), D = V_N(x)-m:
  * parents = paths alive at n for x (all slopes); P^{1,L}_n = those with slope <= L;
  * for EVERY w mod p^(D+L) and x' = x0 + p^m w + p^(m+D+L) z (z random high digits,
    x0 = x mod p^m), all alive-at-N extensions of ALL alive-at-n paths are found by DFS;
  * checks: (i) every alive child with slope <= L at x' has a parent of slope <= L and the same
    slope; slope of the parent at x' equals slope at x; (ii) tau_n(e,x') mod p^lambda constant;
    (iii) for every parent e and EVERY state s mod p^lambda:
        avg_w #{children in state s} == 2^(N-n) p^-D a_n^(lambda)(s_e)       (exact Fractions);
    (A') avg_w c_N sum_{children} p^lambda a_N^(lambda)(s; x') == c_n sum_e rho_n(e)   (exact).
  a_n^(lambda)(t) is computed by brute-force enumeration of all 2^(p*lambda) subsets.
  Also (2.1): #{f in {0,1}^(N-n): Q_f(x) == t mod p^lambda} == 2^(N-n) a_n^(lambda)(t), all t.
Option NEG=1: skip the hypothesis filter (W1)-(W3) (only M_N < m and D>=0 kept) and report how
often (iii) fails, to show that the test is not vacuous.
usage: ck_propA.py p seed nx n N L [NEG] [MAXPAR]
"""
import random
import sys
from fractions import Fraction

from ck_lib import PAdic, products, alive_from_scratch, extend, target


def frozen_law(P, pi, n, lam):
    """a_n^(lam)(t), t mod p^lam, by enumerating all subsets of the first p*lam window terms."""
    p = P.p
    md = p ** lam
    if lam == 0:
        return {0: Fraction(1)}
    L = p * lam
    # y_i = pi_{n+i}/pi_n = prod_{k=n+1}^{n+i}(x+k): recomputed as a product (not from the pi list)
    cnt = {}
    # enumerate subsets directly
    ys = []
    for i in range(L):
        q = 1
        for k in range(n + 1, n + i + 1):
            q *= X_GLOBAL[0] + k
        ys.append(q % md)
    for mask in range(2 ** L):
        s = 0
        for i in range(L):
            if (mask >> i) & 1:
                s += ys[i]
        s %= md
        cnt[s] = cnt.get(s, 0) + 1
    return {t: Fraction(c, 2 ** L) for t, c in cnt.items()}


X_GLOBAL = [0]


def main():
    args = sys.argv[1:]
    p, seed, nx, n, N, L = (int(a) for a in args[:6])
    neg = int(args[6]) if len(args) > 6 else 0
    maxpar = int(args[7]) if len(args) > 7 else 10 ** 9
    prec = max(60, 3 * N // (p - 1) + 30)
    P = PAdic(p, prec)
    rnd = random.Random(seed)
    done = tries = 0
    n_par = n_ident = n_fail = n_inh_fail = n_const_fail = n_mart = n_mart_fail = n_21 = n_21_fail = 0
    lam_hist = {}
    while done < nx and tries < 200000:
        tries += 1
        x = rnd.randrange(P.mod)
        pi, dpi, vals = products(P, x, N)
        m = sum(vals[1:n + 1])
        VN = sum(vals[1:N + 1])
        D = VN - m
        Mn_ = max(vals[1:n + 1])
        MN = max(vals[1:N + 1])
        if not MN < m:
            continue
        if not neg:
            if not (N - n >= p * L and D + L <= m - Mn_ and L < m - MN):
                continue
        par_all = alive_from_scratch(P, pi, dpi, vals, n)
        par = [(b, S, dS) for (b, S, dS) in par_all if P.v(dS) <= L]
        if not par:
            continue
        partial = False
        if len(par) > maxpar:
            par = rnd.sample(par, maxpar)
            partial = True  # only sampled parents are extended; inheritance check is then one-sided
        done += 1
        X_GLOBAL[0] = x
        cn = Fraction(p ** m, 2 ** n)
        cN = Fraction(p ** VN, 2 ** N)
        lam_of = {b: P.v(dS) for (b, S, dS) in par}
        maxlam = max(lam_of.values())
        R = D + L if not neg else D + maxlam
        x0 = x % p ** m
        # frozen laws at x for each needed lambda
        a_n = {lam: frozen_law(P, pi, n, lam) for lam in set(lam_of.values())}
        # direct (2.1) check with explicit window elements y_i = pi_{n+i}/pi_n (exact division)
        ys = []
        for i in range(N - n):
            q = 1
            for k in range(n + 1, n + i + 1):
                q *= x + k
            ys.append(q)
        for lam in a_n:
            if N - n < p * lam:
                continue
            md = p ** lam
            cnt = {}
            for mask in range(2 ** (N - n)):
                s = 0
                for i in range(N - n):
                    if (mask >> i) & 1:
                        s += ys[i]
                s %= md
                cnt[s] = cnt.get(s, 0) + 1
            for t in range(md):
                n_21 += 1
                if Fraction(cnt.get(t, 0), 2 ** (N - n)) != a_n[lam].get(t, 0):
                    n_21_fail += 1
        # parent targets at x
        s_e = {}
        for (b, S, dS) in par:
            lam = lam_of[b]
            tau = target(P, S, pi[n], m)
            s_e[b] = tau % p ** lam
        rho_sum = sum(p ** lam_of[b] * a_n[lam_of[b]].get(s_e[b], 0) for b in lam_of)
        # tallies
        counts = {b: {} for b in lam_of}
        wsum = Fraction(0)
        a_N_cache = {}
        nw = p ** R
        for w in range(nw):
            z = rnd.randrange(p ** 8)
            xp = x0 + p ** m * w + p ** (m + R) * z
            pi2, dpi2, vals2 = products(P, xp, N)
            assert vals2[1:N + 1] == vals[1:N + 1]
            # alive-at-n set at x' must equal that at x (all slopes): recompute from scratch
            if w < 3:
                par2 = alive_from_scratch(P, pi2, dpi2, vals2, n)
                if sorted(b for b, _, _ in par2) != sorted(b for b, _, _ in par_all):
                    n_const_fail += 1
                for (b, S, dS) in par2:
                    if b in lam_of:
                        if P.v(dS) != lam_of[b]:
                            n_const_fail += 1
                        if target(P, S, pi2[n], m) % p ** lam_of[b] != s_e[b]:
                            n_const_fail += 1
            # roots: all alive-at-n paths evaluated at x'
            roots = []
            for (b, _, _) in (par_all if not partial else par):
                S = 0
                dS = 0
                for j in range(n):
                    if (b >> j) & 1:
                        S += pi2[j]
                        dS += dpi2[j]
                roots.append((b, S % P.mod, dS % P.mod))
            kids = extend(P, pi2, dpi2, vals2, n, N, roots)
            for (b2, S2, dS2) in kids:
                lam2 = P.v(dS2)
                if lam2 > L and not neg:
                    continue
                parent = b2 & ((1 << n) - 1)
                if parent not in lam_of:
                    if lam2 <= L and not neg:
                        n_inh_fail += 1  # child of slope <= L whose parent is not in P^{1,L}_n
                    continue
                if lam2 != lam_of[parent]:
                    if not neg:
                        n_inh_fail += 1
                    continue
                lam = lam2
                st = target(P, S2, pi2[N], VN) % p ** lam
                counts[parent][st] = counts[parent].get(st, 0) + 1
                if lam not in a_N_cache:
                    X_GLOBAL[0] = xp
                    a_N_cache[lam] = frozen_law(P, pi2, N, lam)
                    X_GLOBAL[0] = x
                wsum += p ** lam * a_N_cache[lam].get(st, 0)
        # (iii) state by state
        for b in lam_of:
            lam = lam_of[b]
            n_par += 1
            lam_hist[lam] = lam_hist.get(lam, 0) + 1
            pred = Fraction(2 ** (N - n), p ** D) * a_n[lam].get(s_e[b], 0)
            bad = False
            for s in range(p ** lam):
                n_ident += 1
                got = Fraction(counts[b].get(s, 0), nw)
                if got != pred:
                    bad = True
            if bad:
                n_fail += 1
        # (A')
        n_mart += 1
        lhs = cN * wsum / nw
        rhs = cn * rho_sum
        if lhs != rhs:
            n_mart_fail += 1
    tag = "NEG(no W1-W3 filter)" if neg else "hypotheses W1-W3 enforced"
    print(f"RESULT propA p={p} n={n} N={N} L={L} [{tag}] samples={done} parents={n_par} "
          f"(parent,state) identities={n_ident} parents failing (iii)={n_fail} "
          f"inheritance failures={n_inh_fail} constancy failures={n_const_fail} "
          f"A' identity fails={n_mart_fail}/{n_mart} (2.1) fails={n_21_fail}/{n_21} "
          f"lambda hist={dict(sorted(lam_hist.items()))}")


if __name__ == "__main__":
    main()
