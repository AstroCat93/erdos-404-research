"""w5_slopes: M4D Lemma W1(a) = R3M Prop A(i) with L = 0, tested from the
definitions on full populations, including high-slope parents near x = -2 and
gates inside the window (round 4, verify_M4D_falsify).

Under (W2') D <= m - M_n and (W3') M_N < m, for points x' of C = x + p^m Z_p:
  A1  every path alive at N for x' has its n-prefix alive at n for x
  A2  P^0_N(x') = { alive children at N of P^0_n(x) }: every alive child of a
      slope-0 parent has slope 0, and no alive child of a slope>=1 parent has
      slope 0
  A3  (extra, R3M Prop A(i)) a child of a parent of slope lam < m - M_N has
      slope exactly lam
All alive paths at N are enumerated at x' by prefix DFS from exact integers;
slopes v(S'(x')) are exact.  Also reports, for each sample, the slope profile
of the parents, so that high-slope parents are seen to be present.
Usage: python3 w5_slopes.py p seed nsamp n H mode [npts] [smax]
  mode: rand | near2 | nega | gateW
"""
import random
import sys
import time

from wz_core import (Cyl, alive_paths, exact_dpis, vp, V_upto, M_upto)
from w2_cyl import Stat, sample_x


def slopes_of(paths, x, p, L):
    dP = exact_dpis(x, L)
    out = {}
    for g in paths:
        s = sum(dP[j] for j, b in enumerate(g) if b)
        out[g] = vp(s, p) if s else 99
    return out


def main(p, seed, nsamp, n, H, mode, npts=4, smax=4):
    rng = random.Random(seed)
    N = n + H
    st = Stat()
    t0 = time.time()
    done = tries = 0
    prof = {}
    nchild = 0
    while done < nsamp and tries < 300 * nsamp:
        tries += 1
        x, desc = sample_x(rng, p, mode, n, N, N + 1, smax)
        if x <= 0:
            continue
        c = Cyl(p, x, n, N, N)
        if not (c.W2p and c.W3p):
            continue
        Pn = alive_paths(x, n, p, cap=30000)
        if not Pn:
            continue
        sln = slopes_of(Pn, x, p, n)
        hi = sum(1 for v in sln.values() if v >= 1)
        done += 1
        for v in sln.values():
            prof[min(v, 9)] = prof.get(min(v, 9), 0) + 1
        Pset = set(Pn)
        lamcap = c.m - c.MN
        for k in range(npts):
            w = 0 if k == 0 else rng.randrange(1, p ** 8)
            xp = x + p ** c.m * w
            AN = alive_paths(xp, N, p, cap=400000)
            if AN is None:
                st.chk('cap', False, (p, x, desc))
                continue
            slN = slopes_of(AN, xp, p, N)
            for g in AN:
                e = g[:n]
                nchild += 1
                ok1 = e in Pset
                st.chk('A1', ok1, (p, x, desc, w))
                if not ok1:
                    continue
                lam = sln[e]
                st.chk('A2', (slN[g] == 0) == (lam == 0), (p, x, desc, w, lam, slN[g]))
                if lam < lamcap:
                    st.chk('A3', slN[g] == lam, (p, x, desc, w, lam, slN[g]))
        tag = (desc, c.m, c.MN, len(Pn), hi)
    print('p=%d seed=%d nsamp=%d n=%d H=%d mode=%s npts=%d smax=%d' %
          (p, seed, nsamp, n, H, mode, npts, smax))
    print('samples %d; alive children examined %d; parent slope profile (slope: count) %s; %.1f s'
          % (done, nchild, dict(sorted(prof.items())), time.time() - t0))
    st.report()
    nf = sum(st.f.values())
    print('RESULT', 'FAIL' if nf else 'OK', 'failures=%d' % nf)


if __name__ == '__main__':
    a = sys.argv[1:]
    main(int(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4]), a[5], *[int(t) for t in a[6:]])
