"""w4_cw5: M4D Corollary W5 on many windows, with an independent minimiser,
and the scope of "the minimum over weights" (round 4, verify_M4D_falsify).

For a window W = [n,N) at x and a band D' (the jump of the next window
W' = [N,N2), or an arbitrary D' in mode 'free'):
  W5z    m(W;D') = 0  <=>  some class r mod p^D is complete
  W5b    eps~^{q*} = m(W;D') exactly (q* as defined in M4D)
  W5a    eps~^q >= m(W;D') for: uniform, 40 random, all point masses (H <= 10),
         sparse, and random perturbations of q* along feasible directions
  MIN    an independent float minimiser (projected gradient on the simplex of
         laws on the attained residues, 6 random starts) never goes below
         m(W;D') (relative tolerance 1e-9); reports how close it gets
  FORM   the closed form: m = p^D / sum_r a_r^{-1} recomputed from the lifts by
         a second, separate routine (exact)
  SHARP  the scope remark: min over PAIRS (q, q') of the sharp predictable mass
         eps^{q,q'} (Prop W4, q' constant on C).  When W' covers Z/p^{D'}, the
         residue-uniform q' gives eps^{q,q'} = 0 for EVERY q, even when
         m(W;D') > 0.  Counted exactly.
Usage: python3 w4_cw5.py p seed nwin n H H2 mode
  mode: next (D' = jump of W') | free (D' drawn in 0..3, K <= 6)
"""
import random
import sys
import time
from fractions import Fraction

import numpy as np

from wz_core import (Cyl, V_upto, vp, wsums, law, coll, coarsen, eps_tilde,
                     composite_law, lifts, harmonic_m, qstar, frac_to_int_weights)
from w2_cyl import Stat


def form2(QK, p, D, D2):
    """Independent recomputation of m(W;D') from scratch."""
    K = D + D2
    res = set(int(s) % p ** K for s in QK.tolist())
    lif = [0] * (p ** D)
    for s in res:
        lif[s % p ** D] += 1
    if any(c == p ** D2 for c in lif):
        return Fraction(0)
    tot = Fraction(0)
    for c in lif:
        if c:
            tot += 1 / (Fraction(p ** D2, c) - 1)
    return Fraction(p ** D) / tot


def eps_float(mu, p, D, D2):
    """eps~ for a float law on residues mod p^K (numpy)."""
    K = D + D2
    cD = np.bincount(np.arange(p ** K) % p ** D, weights=mu, minlength=p ** D)
    return p ** K * np.dot(mu, mu) - p ** D * np.dot(cD, cD)


def proj_simplex(v):
    u = np.sort(v)[::-1]
    css = np.cumsum(u)
    rho = np.nonzero(u * np.arange(1, len(v) + 1) > (css - 1))[0][-1]
    th = (css[rho] - 1) / (rho + 1.0)
    return np.maximum(v - th, 0)


def minimise(support, p, D, D2, rng, starts=6, iters=3000):
    K = D + D2
    sup = np.array(sorted(support))
    cls = sup % p ** D
    best = np.inf
    for s in range(starts):
        x = np.array([rng.random() for _ in sup])
        x /= x.sum()
        lr = 0.5 / p ** K
        for it in range(iters):
            cD = np.bincount(cls, weights=x, minlength=p ** D)
            g = 2 * p ** K * x - 2 * p ** D * cD[cls]
            x = proj_simplex(x - lr * g)
        mu = np.zeros(p ** K)
        mu[sup] = x
        best = min(best, eps_float(mu, p, D, D2))
    return best


def main(p, seed, nwin, n, H, H2, mode):
    rng = random.Random(seed)
    st = Stat()
    t0 = time.time()
    done = 0
    nmin = 0
    gap_min = np.inf
    sharp_zero_mpos = 0
    mpos = 0
    complete_cnt = 0
    while done < nwin:
        x = rng.randrange(1, p ** 16)
        if rng.random() < 0.5:
            a = rng.randrange(n + 1, n + H + H2 + 1)
            s = rng.randrange(2, 5)
            x = rng.randrange(1, p ** 6) * p ** s - a
            if x <= 0:
                continue
        N, N2 = n + H, n + H + H2
        V = V_upto(x, N2, p)
        D = V[N] - V[n]
        if mode == 'next':
            D2 = V[N2] - V[N]
        else:
            D2 = rng.randrange(0, 4)
        K = D + D2
        if K > 6 or p ** K > 4096:
            continue
        done += 1
        tag = (p, x, n, N, D, D2)
        QK = wsums(x, n, N, p ** K)
        L = lifts(QK, p, D, D2)
        mh = harmonic_m(L, p, D, D2)
        st.chk('FORM', form2(QK, p, D, D2) == mh, tag)
        complete = any(len(l) == p ** D2 for l in L.values())
        complete_cnt += complete
        st.chk('W5z', (mh == 0) == complete, tag)
        qs = qstar(QK, L, p, D, D2)
        qsi, _ = frac_to_int_weights(qs)
        st.chk('W5b', eps_tilde(law(QK, qsi, p ** K), p, D, D2) == mh, tag)
        Hn = 2 ** H
        fams = [('unif', [1] * Hn)]
        for _ in range(40):
            dens = rng.choice([1.0, 0.5, 0.1, 0.02])
            fams.append(('rand', [rng.randrange(1, 20) if rng.random() < dens else 0
                                  for _ in range(Hn)]))
        if H <= 10:
            for j in range(Hn):
                fams.append(('point', [1 if i == j else 0 for i in range(Hn)]))
        for nm, qq in fams:
            if sum(qq) == 0:
                continue
            et = eps_tilde(law(QK, qq, p ** K), p, D, D2)
            st.chk('W5a', et >= mh, (tag, nm))
            if mh > 0:
                st.ratio('W5a -(eps~/m)', -(et / mh))
        # feasible perturbations of q* in the space of laws on residues
        muq = law(QK, qsi, p ** K)
        res = sorted(set(int(s) for s in QK.tolist()))
        for _ in range(20):
            d = {s: Fraction(rng.randrange(-5, 6)) for s in res}
            mean = sum(d.values()) / len(res)
            d = {s: v - mean for s, v in d.items()}
            for tt in (Fraction(1, 10 ** 6), Fraction(1, 1000), Fraction(1, 10)):
                mu = list(muq)
                for s in res:
                    mu[s] += tt * d[s] / len(res)
                if min(mu) < 0:
                    continue
                et = p ** K * coll(mu) - p ** D * coll(coarsen(mu, p, D))
                st.chk('W5a', et >= mh, (tag, 'pert'))
        # independent float minimiser
        if p ** K <= 1024 and len(res) >= 2:
            best = minimise(res, p, D, D2, rng)
            nmin += 1
            st.chk('MIN', best >= float(mh) * (1 - 1e-9) - 1e-12, (tag, best, float(mh)))
            if mh > 0:
                gap_min = min(gap_min, best / float(mh))
        # scope of the minimum: sharp predictable form with q' on W'
        if mode == 'next' and D2 > 0:
            Q2 = wsums(x, N, N2, p ** D2)
            cov = len(set(Q2.tolist())) == p ** D2
            if mh > 0:
                mpos += 1
                if cov:
                    # residue-uniform q' on W': one representative f' per residue
                    rep = {}
                    for j, s in enumerate(Q2.tolist()):
                        rep.setdefault(s, j)
                    q2 = [0] * (2 ** H2)
                    for j in rep.values():
                        q2[j] = 1
                    c = Cyl(p, x, n, N, N2)
                    u = c.u_mod(D2)
                    mu2 = law(Q2, q2, p ** D2)
                    nu = composite_law(muq, mu2, p, D, D2, u)
                    es = p ** K * coll(nu) - p ** D * coll(coarsen(nu, p, D))
                    st.chk('SHARP0', es == 0, tag)
                    if es == 0:
                        sharp_zero_mpos += 1
    print('p=%d seed=%d nwin=%d n=%d H=%d H2=%d mode=%s' % (p, seed, nwin, n, H, H2, mode))
    print('windows %d (with a complete class: %d); minimiser runs %d; %.1f s' %
          (done, complete_cnt, nmin, time.time() - t0))
    if gap_min < np.inf:
        print('smallest (minimiser value)/m over windows with m>0: %.12f' % gap_min)
    if mode == 'next':
        print('windows with m(W;D\')>0: %d; of these, W\' covers Z/p^{D\'} and the sharp '
              'mass eps^{q*,q\'} = 0 for residue-uniform q\': %d' % (mpos, sharp_zero_mpos))
    st.report()
    nf = sum(st.f.values())
    print('RESULT', 'FAIL' if nf else 'OK', 'failures=%d' % nf)


if __name__ == '__main__':
    a = sys.argv[1:]
    main(int(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4]), int(a[5]), a[6])
