#!/usr/bin/env python3
"""w4_cw5_adv.py -- adversarial test of M4D Corollary W5 (optimal weights), plus a scope probe.

eps~(q) = p^K Coll_K(mu^q) - p^D Coll_D(mu^q) is the quadratic form q^T Q q with
  Q[f,f'] = p^K [s_f = s_f' mod p^K] - p^D [s_f = s_f' mod p^D].
(1) PSD: Q is positive semidefinite (float eigenvalues, small cases), so eps~ is convex on the simplex.
(2) KKT (exact): at q*, g = Q q* satisfies g_f >= lam for all f, with equality on supp(q*), lam = q*^T Q q* = m.
    For a convex quadratic this certifies that q* is a GLOBAL minimiser and min eps~ = m(W;D') -- an
    independent proof-check of Cor W5(a),(b).
(3) Attack (float): projected-gradient descent from random starts tries to get eps~(q) < m; reports the
    smallest eps~/m found (must be >= 1 - 1e-9) and how close it gets (should approach 1).
(4) Formula: m == 0 iff some class is complete (exact).
(5) SCOPE (not a defect of W5 as stated): the SHARP fine mass eps^{q,q'} of Prop W4 / Thm W6 (predictable
    form) is also minimised over q'.  If the next window W' covers Z/p^D', the q' that is uniform over the
    residues mod p^D' gives hat mu^{q'}(xi) = 0 for xi != 0, hence eps^{q,q'} = 0 even when m(W;D') > 0.
    Counts such window pairs (exact).
Sources: 'win' = real consecutive windows W=[n,N), W'=[N,N2) of a random x; 'rand' = random residue multisets.
usage: w4_cw5_adv.py p seed nsys n H H2 src [KMAX] [NSTART]
"""
import random
import sys
from fractions import Fraction

import numpy as np

from wlib import (vp, prods, Vof, win_elems, win_unit, subset_sums, law, fine_tilde, composite_fine,
                  hm_and_qstar, lifts_of)


def proj_simplex(v):
    u = np.sort(v)[::-1]
    css = np.cumsum(u)
    k = np.arange(1, len(v) + 1)
    cond = u - (css - 1) / k > 0
    r = k[cond][-1]
    th = (css[r - 1] - 1) / r
    return np.maximum(v - th, 0)


def main():
    a = sys.argv[1:]
    p, seed, nsys, n, H, H2 = (int(t) for t in a[:6])
    src = a[6]
    kmax = int(a[7]) if len(a) > 7 else 6
    nstart = int(a[8]) if len(a) > 8 else 4
    rnd = random.Random(seed)
    nrng = np.random.default_rng(seed)
    N, N2 = n + H, n + H + H2
    prec = 4 * (N2 // (p - 1) + 12)
    st = dict(sys=0, psd=0, psd_n=0, kkt=0, val=0, attack=0, iff=0, mpos=0, scope=0, scope_cov=0)
    best_ratio = None
    min_ratio = None
    tries = 0
    while st['sys'] < nsys and tries < 100000:
        tries += 1
        if src == 'win':
            x = rnd.randrange(p ** 40)
            _, _, vals = prods(x, N2, p, prec)
            D = Vof(vals, N) - Vof(vals, n)
            Dp = Vof(vals, N2) - Vof(vals, N)
            if D + Dp > kmax or Dp < 1:
                continue
            K = D + Dp
            sums = subset_sums(win_elems(x, n, N, p ** K), p ** K)
            sums2 = subset_sums(win_elems(x, N, N2, p ** Dp), p ** Dp)
            u = win_unit(x, n, N, p, p ** Dp)
        else:
            D, Dp = rnd.randint(0, 2), rnd.randint(1, 2)
            if D + Dp > kmax:
                continue
            K = D + Dp
            sums = [rnd.randrange(p ** K) for _ in range(1 << H)]
            sums2 = [rnd.randrange(p ** Dp) for _ in range(1 << H2)]
            u = rnd.choice([b for b in range(1, p ** Dp) if b % p])
        st['sys'] += 1
        pK, pD = p ** K, p ** D
        m, qs, avals = hm_and_qstar(sums, p, D, Dp)
        # (4)
        complete = any(v == 0 for v in avals.values())
        if complete != (m == 0):
            st['iff'] += 1
        if m > 0:
            st['mpos'] += 1
        # exact Q q* via laws
        lK = law(sums, qs, pK)
        lD = law(sums, qs, pD)
        g = [pK * lK.get(s % pK, 0) - pD * lD.get(s % pD, 0) for s in sums]
        val = fine_tilde(sums, qs, p, D, Dp)
        if val != m:
            st['val'] += 1
        supp = [f for f in range(len(sums)) if qs[f] > 0]
        lam = g[supp[0]]
        if any(g[f] != lam for f in supp) or any(g[f] < lam for f in range(len(sums))) or lam != val:
            st['kkt'] += 1
        # (1) PSD, float, only for small matrices
        nf = len(sums)
        sK = np.array([s % pK for s in sums])
        sD = np.array([s % pD for s in sums])
        Q = pK * (sK[:, None] == sK[None, :]).astype(float) - pD * (sD[:, None] == sD[None, :]).astype(float)
        if nf <= 256:
            st['psd_n'] += 1
            ev = np.linalg.eigvalsh(Q)
            if ev.min() < -1e-8 * max(1.0, abs(ev).max()):
                st['psd'] += 1
        # (3) attack by projected gradient
        L = max(1.0, float(np.abs(np.linalg.eigvalsh(Q)).max())) if nf <= 256 else float(pK)
        for s in range(nstart):
            qv = nrng.dirichlet(np.ones(nf) * (0.2 if s % 2 else 1.0))
            for it in range(1500):
                qv = proj_simplex(qv - (1.0 / (2 * L)) * 2 * (Q @ qv))
            fv = float(qv @ Q @ qv)
            if m > 0:
                r = fv / float(m)
                if r < 1 - 1e-9:
                    st['attack'] += 1
                best_ratio = r if best_ratio is None or r < best_ratio else best_ratio
            else:
                if fv < -1e-9:
                    st['attack'] += 1
        # random exact q (sparse) never below m
        for _ in range(6):
            raw = [0 if rnd.random() < 0.7 else rnd.randint(1, 9) for _ in range(nf)]
            if sum(raw) == 0:
                raw[0] = 1
            q = [Fraction(c, sum(raw)) for c in raw]
            fq = fine_tilde(sums, q, p, D, Dp)
            if fq < m:
                st['attack'] += 1
            if m > 0:
                rr = fq / m
                min_ratio = rr if min_ratio is None or rr < min_ratio else min_ratio
        # (5) scope probe
        res2 = {}
        for g2, s2 in enumerate(sums2):
            res2.setdefault(s2 % p ** Dp, []).append(g2)
        if len(res2) == p ** Dp:
            st['scope_cov'] += 1
            q2 = [Fraction(0)] * len(sums2)
            for r, gl in res2.items():
                for g2 in gl:
                    q2[g2] = Fraction(1, p ** Dp * len(gl))
            es = composite_fine(sums, qs, sums2, q2, u, p, D, Dp)
            if es == 0 and m > 0:
                st['scope'] += 1
            if es != 0:
                st['scope_err'] = st.get('scope_err', 0) + 1
    print(f"RESULT w4_cw5_adv p={p} src={src} n={n} H={H} H2={H2} systems={st['sys']} (m>0 in {st['mpos']}): "
          f"PSD fails {st['psd']}/{st['psd_n']}; KKT certificate fails {st['kkt']}; eps~(q*) != m: {st['val']}; "
          f"'m=0 iff complete' fails {st['iff']}; attacks below m: {st['attack']} (best descent eps~/m = "
          f"{best_ratio if best_ratio is None else round(best_ratio, 10)}; min exact random eps~/m = "
          f"{None if min_ratio is None else float(min_ratio):}) | SCOPE: W' covers mod p^D' in "
          f"{st['scope_cov']}; of these, sharp eps^(q*,q'_unif-res) = 0 while m(W;D') > 0 in {st['scope']} "
          f"(nonzero sharp eps despite cover: {st.get('scope_err', 0)})")


if __name__ == "__main__":
    main()
