"""w1_validate: validate the fast engine of wz_core/w_engine against a brute
force that uses only the DEFINITIONS of M4D's W1/W4 quantities.

For a cylinder C = x + p^m Z_p and every point x' = x + p^m w, w < p^K:
  brute force:  enumerate ALL alive paths at N and at N2 for x' (prefix DFS,
                exact integers), compute every slope exactly, keep the slope-0
                ones, and evaluate
                  M_N(x')  = p^{V_N}  sum_{g in P^0_N(x')}  w(g|n) q(g[n:N])
                  M_N2(x') = p^{V_N2} sum_{g in P^0_N2(x')} w(g|n) q(g[n:N]) q'(g[N:N2])
                with w := 0 off P^0_n(x).  Also counts slope-0 alive paths at
                N, N2 whose n-prefix is NOT in P^0_n(x) (W1(a): must be 0) and
                alive children of slope>=1 parents that have slope 0.
  engine:       w_engine.Tmat from the parent targets (uses only (F2)).
Usage: python3 w1_validate.py p seed ncyl n H H2 [maxpaths [neg]]
  neg=1: NEGATIVE CONTROL, the engine uses the wrong unit 2u (mismatches expected).
"""
import random
import sys
from fractions import Fraction

import numpy as np

from wz_core import (Cyl, alive_paths, exact_dpis, vp, wsums, V_upto)
from w_engine import Tmat, mq_from


def run(p, seed, ncyl, n, H, H2, maxpaths=60000, neg=0):
    rng = random.Random(seed)
    N, N2 = n + H, n + H + H2
    stats = dict(cyl=0, pts=0, mismatchN=0, mismatchN2=0, w1a_bad=0,
                 hislope_child_slope0=0, children_checked=0, void=0,
                 DD=[], nP0=0, nPall=0)
    tries = 0
    while stats['cyl'] < ncyl and tries < 50 * ncyl:
        tries += 1
        x = rng.randrange(1, p ** 12)
        if rng.random() < 0.4:            # edge cases: a gate inside [1, N2]
            a = rng.randrange(1, N2 + 1)
            s = rng.randrange(2, 5)
            x = rng.randrange(1, p ** 4) * p ** s - a
            if x <= 0 or vp(x + a, p) != s:
                continue
        c = Cyl(p, x, n, N, N2)
        if not c.r52 or c.D2 == 0:
            stats['void'] += 1
            continue
        Pall = alive_paths(x, n, p, cap=maxpaths)
        if not Pall:
            stats['void'] += 1
            continue
        dP = exact_dpis(x, n)
        sl = {}
        for e in Pall:
            s_ = sum(dP[j] for j, b in enumerate(e) if b)
            sl[e] = vp(s_, p) if s_ else 99
        P0 = [e for e in Pall if sl[e] == 0]
        if not P0:
            stats['void'] += 1
            continue
        # random weights
        wts = [rng.randrange(0, 4) for _ in P0]
        if sum(wts) == 0:
            wts[0] = 1
        wmap = {e: wt for e, wt in zip(P0, wts)}
        q = [rng.randrange(0, 4) for _ in range(2 ** H)]
        q2 = [rng.randrange(0, 4) for _ in range(2 ** H2)]
        if sum(q) == 0:
            q[0] = 1
        if sum(q2) == 0:
            q2[0] = 1
        A, A2 = sum(q), sum(q2)
        tau, bad = c.parent_targets(P0, c.K)
        assert bad == 0, bad
        mq = mq_from(wsums(x, n, N, p ** c.K), q, p ** c.K)
        uu = c.u_mod(c.D2) if not neg else (2 * c.u_mod(c.D2)) % (p ** c.D2)
        T = Tmat(tau, wts, p, c.D, c.D2, uu, mq)
        Q2 = wsums(x, N, N2, p ** c.D2)
        mq2 = [0] * (p ** c.D2)
        for t, wt in zip(Q2.tolist(), q2):
            mq2[t] += wt
        stats['cyl'] += 1
        stats['DD'].append((c.D, c.D2))
        stats['nP0'] += len(P0)
        stats['nPall'] += len(Pall)
        for w in range(p ** c.K):
            xp = x + p ** c.m * w
            VV = V_upto(xp, N2, p)
            # brute force populations at N and N2
            dPN = exact_dpis(xp, N2)
            for (L, MM, key) in ((N, None, 'mismatchN'), (N2, None, 'mismatchN2')):
                AL = alive_paths(xp, L, p, cap=maxpaths * 50)
                tot = 0
                for g in AL:
                    s_ = sum(dPN[j] for j, b in enumerate(g) if b)
                    if s_ % p == 0:
                        continue           # slope >= 1
                    e = g[:n]
                    if e not in wmap:
                        stats['w1a_bad'] += 1
                        continue
                    f = sum(g[n + i] << i for i in range(H))
                    val = wmap[e] * q[f]
                    if L == N2:
                        f2 = sum(g[N + i] << i for i in range(H2))
                        val *= q2[f2]
                    tot += val
                if L == N:
                    brute = Fraction(p ** VV[N] * tot, A)
                    eng = Fraction(p ** (c.m + c.D) * sum(T[w]), A)
                else:
                    brute = Fraction(p ** VV[N2] * tot, A * A2)
                    eng = Fraction(p ** (c.m + c.K) * sum(
                        int(T[w][t]) * mq2[t] for t in range(p ** c.D2)), A * A2)
                if brute != eng:
                    stats[key] += 1
            stats['pts'] += 1
        # high-slope parents: all alive children at N, slopes
        hs = [e for e in Pall if sl[e] > 0]
        for w in range(min(p ** c.K, 9)):
            xp = x + p ** c.m * w
            AL = alive_paths(xp, N, p, cap=maxpaths * 50)
            dPN = exact_dpis(xp, N)
            hsset = set(hs)
            for g in AL:
                if g[:n] in hsset:
                    stats['children_checked'] += 1
                    s_ = sum(dPN[j] for j, b in enumerate(g) if b)
                    if s_ % p != 0:
                        stats['hislope_child_slope0'] += 1
    return stats


if __name__ == '__main__':
    a = [int(t) for t in sys.argv[1:]]
    st = run(*a)
    print('p=%d seed=%d ncyl=%d n=%d H=%d H2=%d' % tuple(a[:6]))
    print(st)
    fails = st['mismatchN'] + st['mismatchN2'] + st['w1a_bad'] + st['hislope_child_slope0']
    print('RESULT', 'FAIL' if fails else 'OK', 'failures=%d' % fails)
