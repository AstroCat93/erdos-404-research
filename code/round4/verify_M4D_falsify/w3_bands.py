"""w3_bands: M4D Lemma W3 (weighted fresh-randomness lemma) for EVERY band k
allowed by its hypothesis (5.1): D + k <= m - M_N and M_N < m (round 4,
verify_M4D_falsify).  w2_cyl.py tests only k = D'.

For a cylinder C, a parent set P (subset of P^0_n(x), integer weights) and an
integer window weight q, with u = pi_N/(p^D pi_n) mod p^k:
  W3a     sum over x' in C of T[x', t] is independent of t  (E_C Psi(xi) = 0)
  W3bsum  sum_{xi != 0} E|p^{V_N} Psi(xi)|^2 <= (p^m W(P))^2 sum_{xi != 0} F^q(xi)  (exact)
  W3bxi   the same for each xi separately (float64 FFT, tolerance 1e-9 relative)
  F0      F^q(0) = 1 + chi^2_q  (exact, from the definition of F^q)
  NC4     per-xi bound with F^q(xi u) in place of F^q(xi u^{-1}) (control)
Usage: python3 w3_bands.py p seed ncyl n H mode [Pmax] [smax]
"""
import random
import sys
import time
from fractions import Fraction

import numpy as np

from wz_core import (Cyl, alive_paths, random_alive_paths, exact_dpis, vp, wsums,
                     law, coll, coarsen, chi2)
from w_engine import Tmat, mq_from
from w2_cyl import Stat, sample_x, fft_check_W3


def main(p, seed, ncyl, n, H, mode, Pmax=80, smax=4):
    rng = random.Random(seed)
    N = n + H
    st = Stat()
    t0 = time.time()
    done = tries = 0
    ks = {}
    while done < ncyl and tries < 300 * ncyl:
        tries += 1
        x, desc = sample_x(rng, p, mode, n, N, N + 1, smax)
        if x <= 0:
            continue
        c = Cyl(p, x, n, N, N)
        if not (c.MN < c.m):
            continue
        kmax = c.m - c.MN - c.D
        while kmax >= 1 and p ** (c.D + kmax) > 2401:
            kmax -= 1
        if kmax < 1:
            continue
        Pall = alive_paths(x, n, p, cap=20000)
        if Pall is None:
            Pall = random_alive_paths(x, n, p, 3 * Pmax, rng)
        if not Pall:
            continue
        dP = exact_dpis(x, n)
        P0 = [e for e in Pall if sum(dP[j] for j, b in enumerate(e) if b) % p]
        if not P0:
            continue
        if len(P0) > Pmax:
            P0 = rng.sample(P0, Pmax)
        done += 1
        for k in range(1, kmax + 1):
            ks[k] = ks.get(k, 0) + 1
            Kk = c.D + k
            tau, bad = c.parent_targets(P0, Kk, check_windows=False)
            # u mod p^k must be constant on C: check at a few points
            for w in (1, 2, p ** Kk - 1):
                xp = x + p ** c.m * w
                ys = 1
                for s in range(1, H + 1):
                    ys *= xp + n + s
                if vp(ys, p) != c.D or (ys // p ** c.D) % p ** k != c.u_mod(k):
                    bad += 1
            st.chk('engine', bad == 0, (p, x, desc, k))
            if bad:
                continue
            u = c.u_mod(k)
            QK = wsums(x, n, N, p ** Kk)
            for wn in ('ones', 'rand', 'single'):
                if wn == 'ones':
                    wts = [1] * len(P0)
                elif wn == 'rand':
                    wts = [rng.randrange(0, 6) for _ in P0]
                else:
                    j = rng.randrange(len(P0))
                    wts = [1 if i == j else 0 for i in range(len(P0))]
                if sum(wts) == 0:
                    wts[0] = 1
                for qn in ('unif', 'rand', 'point'):
                    if qn == 'unif':
                        q = [1] * 2 ** H
                    elif qn == 'rand':
                        q = [rng.randrange(0, 10) for _ in range(2 ** H)]
                    else:
                        j = rng.randrange(2 ** H)
                        q = [1 if i == j else 0 for i in range(2 ** H)]
                    if sum(q) == 0:
                        q[0] = 1
                    A = sum(q)
                    mq = mq_from(QK, q, p ** Kk)
                    muK = [Fraction(t, A) for t in mq]
                    T = Tmat(tau, wts, p, c.D, k, u, mq)
                    npts = p ** Kk
                    tag = (p, x, desc, n, N, c.m, c.D, k, wn, qn)
                    col = [sum(int(T[w][t]) for w in range(npts)) for t in range(p ** k)]
                    st.chk('W3a', len(set(col)) == 1, tag)
                    SN = [sum(int(t) for t in T[w]) for w in range(npts)]
                    lhs = Fraction(p ** (2 * (c.m + c.D)) * sum(
                        p ** k * sum(int(t) ** 2 for t in T[w]) - SN[w] ** 2
                        for w in range(npts)), npts * A * A)
                    et = p ** Kk * coll(muK) - p ** c.D * coll(coarsen(muK, p, c.D))
                    Mn = p ** c.m * sum(wts)
                    st.chk('W3bsum', lhs <= et * Mn * Mn, (tag, float(lhs), float(et * Mn * Mn)))
                    if et > 0:
                        st.ratio('W3bsum LHS/RHS', lhs / (et * Mn * Mn))
                    # F^q(0) = sum_{zeta = 0 mod p^k} |mu^(zeta)|^2 = p^D Coll_D = 1 + chi^2
                    st.chk('F0', p ** c.D * coll(coarsen(muK, p, c.D)) ==
                           1 + chi2(coarsen(muK, p, c.D), p, c.D), tag)
                    worst, nc4 = fft_check_W3(T, A, sum(wts), muK, p, c.m, c.D, k, u)
                    st.chk('W3bxi', worst >= -1e-9, (tag, worst))
                    st.chk('NC4', nc4 == 0, tag)
    print('p=%d seed=%d ncyl=%d n=%d H=%d mode=%s Pmax=%d smax=%d' %
          (p, seed, ncyl, n, H, mode, Pmax, smax))
    print('cylinders %d, bands tested (k: count) %s, %.1f s' % (done, ks, time.time() - t0))
    st.report()
    core = [k for k in st.c if not k.startswith('NC')]
    nf = sum(st.f.get(k, 0) for k in core)
    print('NEGATIVE CONTROLS (failures expected):',
          {k: '%d/%d' % (st.f.get(k, 0), st.c[k]) for k in st.c if k.startswith('NC')})
    print('RESULT', 'FAIL' if nf else 'OK', 'core failures=%d' % nf)


if __name__ == '__main__':
    a = sys.argv[1:]
    main(int(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4]), a[5], *[int(t) for t in a[6:]])
