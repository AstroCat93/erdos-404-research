"""w6_chain: M4D Theorem W6 end to end at finite horizon, by exhaustive exact
enumeration of an admissible atom A (round 4, verify_M4D_falsify).

Setting (R3M Theorem C3 / M4D Theorem W6) with j = 0: deterministic times
n_0 < n_1 < ... < n_{Lh+1}; G_l = partition into the cylinders x + p^{m_l} Z_p
(m_l = V_{n_l}(x)); A = an admissible atom of G_0.  For every atom of every
G_l inside A (down to level Lh) the weighted slope-0 population is computed
from scratch: each child (e,f) is tested for aliveness at n_{l+1} exactly at a
point of the child atom, and its slope v(S'_{(e,f)}) mod p is computed
exactly.  Window weights q_l are ADAPTED (a function of the atom of G_l) or
PREDICTABLE (a function of the atom of G_{l-1}); parent weights
w_{l+1}((e,f)) = w_l(e) q_l(f); M_l = p^{m_l} sum_e w_l(e).  The stopping time
tau = first l > 0 with B_l false, B_l = {D_{l-1}+D_l <= m_{l-1} - M_{n_{l+1}},
M_{n_{l+1}} < m_{l-1}} and {eps~_l <= ebar_l} (eps~_l = eps~^{q_{l-1}}(W_{l-1};
D_l); with --sharp and a predictable schedule, eps_l = eps^{q_{l-1},q_l}).

Checks (exact unless marked):
  MART   E[M_{l+1} | atom of G_l] = M_l on every atom with tau > l     (W1)
  SLOPE  every alive child of a weighted slope-0 parent has slope 0       (W1(a))
  FIRST  E_A[M_1^2] <= M_0^2 (1 + chi^2_{q_0})                            (W2)
  STEP   on every atom C of G_{l-1} with tau > l:
         E_C[M_{l+1}^2] - E_C[M_l^2] <= eps~_l(C) M_{l-1}(C)^2           (W4)
  MEAS   q_l, eps~_{l+1}, D_l, D_{l+1} and the regime flags are the same
         at two further random points of the atom                       (adaptedness)
  BAL    q = q* and eps~_{l+1}(C) = 0 (a complete coset):
         M_{l+2} = M_{l+1} on every atom of G_{l+2} inside C            (Remark 2)
  GLOB   a_l = E_A[Mt_l^2]: a_1 <= (1+chi^2) a_0, a_{l+1} <= a_l + ebar_l a_{l-1},
         a_l <= M_0^2 Pi^{(l)}; E_A[Mt_l] = M_0
  ALIVE  on every leaf atom reached (tau >= Lh) with M_Lh > 0, the weighted
         paths are alive at n_Lh at the representative AND at a random
         further point of the atom
  PZ     mu_A(Y > 0) >= (E Y)^2/E Y^2 >= (1 - sqrt(Pi delta'))^2/Pi  (float for
         the sqrt), Y = Mt_Lh 1{tau >= Lh}, delta' = mu_A(tau < Lh)
Usage: python3 w6_chain.py p seed natoms n0 H Lh sched ebar [P0max] [sharp]
  sched: unif | qstar | rand | point | sparse | mixed | pred |
         nonadapt (NEGATIVE CONTROL: q depends on the child's digits; MART must fail)
  ebar:  a number (same ebar for every l), or 'inf'
"""
import math
import random
import sys
import time
from fractions import Fraction

import numpy as np

from wz_core import (V_upto, M_upto, vp, exact_pis, exact_dpis, alive_paths,
                     random_alive_paths, wsums, law, coll, coarsen, eps_tilde,
                     composite_law, lifts, qstar, frac_to_int_weights, welems)
from w2_cyl import Stat


class Chain:
    def __init__(self, p, times, sched, ebar, seed, sharp=False, popcap=200000):
        self.p, self.t, self.sched, self.ebar, self.seed = p, times, sched, ebar, seed
        self.sharp = sharp
        self.Lh = len(times) - 2
        self.st = Stat()
        self.popcap = popcap
        self.natoms = [0] * (self.Lh + 1)
        self.stops = [0] * (self.Lh + 1)
        self.balanced = 0
        self.leaves = []
        if sharp and sched not in ('pred', 'unif'):
            raise ValueError('the sharp form needs a predictable schedule')

    # ---------------------------------------------------------- valuations
    def vals(self, xa, l):
        """(m_l, D_l, D_{l+1} or None, M_{n_l}, M_{n_{l+1}}, M_{n_{l+2}}) at xa."""
        p, t = self.p, self.t
        top = t[min(l + 2, len(t) - 1)]
        V = V_upto(xa, top, p)
        m = V[t[l]]
        D = V[t[l + 1]] - m
        D1 = V[t[l + 2]] - V[t[l + 1]] if l + 2 < len(t) else None
        Mn = M_upto(xa, t[l], p)
        M1 = M_upto(xa, t[l + 1], p)
        M2 = M_upto(xa, t[l + 2], p) if l + 2 < len(t) else None
        return m, D, D1, Mn, M1, M2

    # ---------------------------------------------------------- weights
    def qsel(self, l, xa, m_l, m_prev):
        """Window weight q_l on W_l (integer numerators), adapted to G_l or
        (sched 'pred') predictable: a function of the atom of G_{l-1}."""
        p, t = self.p, self.t
        H = t[l + 1] - t[l]
        kind = self.sched
        if kind == 'pred':
            key = (self.seed, l, xa % p ** m_prev if l > 0 else xa % p ** m_l)
            r = random.Random(hash(key))
            return [r.randrange(0, 10) or (1 if i == 0 else 0) for i in range(2 ** H)]
        key = (self.seed, l, xa % p ** m_l)
        r = random.Random(hash(key))
        if kind == 'nonadapt':
            kind = 'rand'
        if kind == 'mixed':
            kind = r.choice(['unif', 'qstar', 'rand', 'point', 'sparse'])
        if kind == 'unif':
            return [1] * 2 ** H
        if kind == 'rand':
            q = [r.randrange(0, 10) for _ in range(2 ** H)]
        elif kind == 'point':
            j = r.randrange(2 ** H)
            q = [1 if i == j else 0 for i in range(2 ** H)]
        elif kind == 'sparse':
            q = [r.randrange(1, 10) if r.random() < 0.1 else 0 for _ in range(2 ** H)]
        elif kind == 'qstar':
            m, D, D1, Mn, M1, M2 = self.vals(xa, l)
            if D1 is None or M2 >= m_l or D + D1 > m_l:
                return [1] * 2 ** H
            QK = wsums(xa, t[l], t[l + 1], p ** (D + D1))
            L = lifts(QK, p, D, D1)
            qi, _ = frac_to_int_weights(qstar(QK, L, p, D, D1))
            return qi
        else:
            raise ValueError(kind)
        if sum(q) == 0:
            q[0] = 1
        return q

    def eps_next(self, l, xa, q, D, D1, m_l):
        """eps~_{l+1} = eps~^{q_l}(W_l; D_{l+1}) (or the sharp form)."""
        p, t = self.p, self.t
        K = D + D1
        QK = wsums(xa, t[l], t[l + 1], p ** K)
        mu = law(QK, q, p ** K)
        et = eps_tilde(mu, p, D, D1)
        if not self.sharp:
            return et, et
        # predictable q_{l+1}: constant on this atom of G_l
        q1 = self.qsel(l + 1, xa, m_l + D, m_l)
        Q2 = wsums(xa, t[l + 1], t[l + 2], p ** D1)
        mu2 = law(Q2, q1, p ** D1)
        _, yH = welems(xa, t[l], t[l + 1])
        u = (yH // p ** D) % (p ** D1) if D1 > 0 else 0
        nu = composite_law(mu, mu2, p, D, D1, u)
        es = p ** K * coll(nu) - p ** D * coll(coarsen(nu, p, D))
        self.st.chk('ORDER', es <= et, (l, xa))
        return es, et

    # ---------------------------------------------------------- children
    def children(self, l, xp, rows, nums, q, m_l, D):
        """Weighted slope-0 alive children at n_{l+1} for the point xp."""
        p, t = self.p, self.t
        n, N = t[l], t[l + 1]
        H = N - n
        pis = exact_pis(xp, N)
        dps = exact_dpis(xp, N)
        modM = p ** (m_l + D) if D > 0 else p ** (m_l + 1)
        assert modM * n < 2 ** 62
        pv = np.array([v % modM for v in pis[:n]], dtype=np.int64)
        S = (rows.astype(np.int64) @ pv) % modM
        ok_alive = not np.any(S % p ** m_l)
        self.st.chk('PARALIVE', ok_alive, (l, xp))
        om = pis[n] // p ** m_l
        assert vp(pis[n], p) == m_l
        modD = p ** D
        a = (S // p ** m_l) % modD if D > 0 else np.zeros(len(S), dtype=np.int64)
        Qf = wsums(xp, n, N, modD if D > 0 else 1)
        b = (Qf * (om % modD)) % modD if D > 0 else np.zeros(2 ** H, dtype=np.int64)
        dv = np.array([v % p for v in dps[:n]], dtype=np.int64)
        Sd = (rows.astype(np.int64) @ dv) % p
        # window derivative contributions: pi'_{n+i}(xp) mod p
        wd = np.array([dps[n + i] % p for i in range(H)], dtype=np.int64)
        fb = ((np.arange(2 ** H)[:, None] >> np.arange(H)[None, :]) & 1).astype(np.int64)
        Wd = (fb @ wd) % p
        qa = np.array([int(v) > 0 for v in q])
        alive = ((a[:, None] + b[None, :]) % modD == 0) & qa[None, :] if D > 0 else \
            np.broadcast_to(qa[None, :], (len(S), 2 ** H)).copy()
        ei, fi = np.nonzero(alive)
        slope0 = (Sd[ei] + Wd[fi]) % p != 0
        self.st.chk('SLOPE', bool(np.all(slope0)), (l, xp))
        ei, fi = ei[slope0], fi[slope0]
        if len(ei) > self.popcap:
            raise RuntimeError('population cap exceeded: %d' % len(ei))
        newrows = np.concatenate([rows[ei], fb[fi].astype(np.int8)], axis=1)
        newnums = [nums[i] * int(q[j]) for i, j in zip(ei.tolist(), fi.tolist())]
        return newrows, newnums

    # ---------------------------------------------------------- recursion
    def explore(self, l, xa, rows, nums, den, tau_gt_l, m_prev, meas):
        """Returns (stats, eqflag): stats[lev] = (E M~_lev, E M~_lev^2) over
        this atom (relative Haar measure), lev = l..Lh; eqflag: whether every
        child atom at level l+1 has M_{l+1} == M_l (for BAL)."""
        p, t, Lh = self.p, self.t, self.Lh
        m_l = V_upto(xa, t[l], p)[t[l]]
        self.natoms[l] += 1
        Ml = Fraction(p ** m_l * sum(nums), den)
        stats = {l: (Ml, Ml * Ml)}
        if not tau_gt_l or l == Lh:
            if not tau_gt_l:
                self.stops[l] += 1
            self.leaves.append((meas, Ml, l == Lh))
            if l == Lh and Ml > 0:
                # ALIVE: weighted paths alive at n_Lh at xa and at a random point
                r = random.Random(hash((self.seed, 2, xa)))
                for xx in (xa, xa + p ** m_l * r.randrange(1, p ** 6)):
                    pis = exact_pis(xx, t[l])
                    mod = p ** m_l
                    pv = np.array([v % (mod * p) for v in pis[:t[l]]], dtype=np.int64)
                    pos = [i for i, v in enumerate(nums) if v > 0]
                    S = (rows[pos].astype(np.int64) @ pv) % (mod * p)
                    okv = V_upto(xx, t[l], p)[t[l]] == m_l
                    self.st.chk('ALIVE', okv and not np.any(S % mod), (l, xa))
            for lev in range(l + 1, Lh + 1):
                stats[lev] = (Ml, Ml * Ml)
            return stats, True, Ml
        m, D, D1, Mn, M1, M2 = self.vals(xa, l)
        assert m == m_l
        self.st.chk('W2p', D <= m_l - Mn and M1 < m_l, (l, xa))
        q = self.qsel(l, xa, m_l, m_prev)
        A = sum(int(v) for v in q)
        # B_{l+1} (G_l-measurable)
        if D1 is not None and M2 < m_l and D + D1 <= m_l - M2:
            eps_use, et = self.eps_next(l, xa, q, D, D1, m_l)
            B = eps_use <= self.ebar
        else:
            eps_use, et, B = None, None, False
        # MEAS: same objects at two other points of the atom
        r = random.Random(hash((self.seed, 1, l, xa)))
        for _ in range(2):
            xx = xa + p ** m_l * r.randrange(1, p ** 8)
            vv = self.vals(xx, l)
            same = vv[:2] == (m, D) and (vv[4] < m_l) == (M1 < m_l)
            if D1 is not None and M2 < m_l:
                same = same and vv[2] == D1 and vv[5] == M2
            same = same and self.qsel(l, xx, m_l, m_prev) == q
            if eps_use is not None and same:
                same = self.eps_next(l, xx, q, D, D1, m_l)[0] == eps_use
            self.st.chk('MEAS', same, (l, xa, xx))
        # children atoms
        cstats = []
        ceq = []
        cM = []
        for w in range(p ** D):
            xp = xa + p ** m_l * w
            qw, Aw = q, A
            if self.sched == 'nonadapt':
                # NEGATIVE CONTROL: the window weight depends on the fresh digits
                r2 = random.Random(hash((self.seed, 3, l, xp % p ** (m_l + D))))
                qw = [r2.randrange(0, 10) for _ in range(len(q))]
                qw[0] += 1
                Aw = sum(qw)
            nr, nn = self.children(l, xp, rows, nums, qw, m_l, D)
            assert V_upto(xp, t[l + 1], p)[t[l + 1]] == m_l + D
            s, eq, Mc = self.explore(l + 1, xp, nr, nn, den * Aw, tau_gt_l and B, m_l,
                                     meas / p ** D)
            cstats.append(s)
            ceq.append(eq)
            cM.append(Mc)
        k = len(cstats)
        for lev in range(l + 1, Lh + 1):
            stats[lev] = (sum(s[lev][0] for s in cstats) / k, sum(s[lev][1] for s in cstats) / k)
        # MART
        self.st.chk('MART', stats[l + 1][0] == Ml, (l, xa))
        if l == 0:
            QD = wsums(xa, t[0], t[1], p ** D if D > 0 else 1)
            muD = law(QD, q, p ** D if D > 0 else 1)
            c2 = p ** D * coll(muD) - 1
            self.chi2_0 = c2
            self.st.chk('FIRST', stats[1][1] <= Ml * Ml * (1 + c2), (xa,))
        # STEP at this atom C (level l) for the pair (W_l, W_{l+1}) when tau > l+1
        if B and l + 2 <= Lh:
            lhs = stats[l + 2][1] - stats[l + 1][1]
            self.st.chk('STEP', lhs <= eps_use * Ml * Ml, (l, xa, float(lhs), float(eps_use * Ml * Ml)))
            if eps_use > 0 and Ml > 0:
                self.st.ratio('STEP LHS/(eps M^2)', lhs / (eps_use * Ml * Ml))
            if et == 0 and self.sched in ('qstar',):
                self.balanced += 1
                self.st.chk('BAL', all(ceq), (l, xa))
        eqflag = all(Mc == Ml for Mc in cM)
        return stats, eqflag, Ml


def find_atom(p, times, rng, P0max, tries=4000):
    n0, n1 = times[0], times[1]
    for _ in range(tries):
        x = rng.randrange(1, p ** 14)
        V = V_upto(x, n1, p)
        m0 = V[n0]
        D0 = V[n1] - m0
        M1 = M_upto(x, n1, p)
        if not (M1 < m0 and D0 <= m0 - M1):
            continue
        Pall = alive_paths(x, n0, p, cap=20000)
        if Pall is None:
            Pall = random_alive_paths(x, n0, p, 4 * P0max, rng)
        if not Pall:
            continue
        dP = exact_dpis(x, n0)
        P0 = [e for e in Pall if sum(dP[j] for j, b in enumerate(e) if b) % p]
        if not P0:
            continue
        full = len(P0) <= P0max
        if not full:
            P0 = rng.sample(P0, P0max)
        xa = x % p ** m0
        if xa == 0:
            xa = p ** m0
        return xa, m0, P0, full
    return None


def main(p, seed, natoms, n0, H, Lh, sched, ebar, P0max=40, sharp=0):
    rng = random.Random(seed)
    times = [n0 + H * i for i in range(Lh + 2)]
    eb = math.inf if ebar == 'inf' else Fraction(ebar)
    tot = Stat()
    t0 = time.time()
    summ = []
    for ia in range(natoms):
        at = find_atom(p, times, rng, P0max)
        if at is None:
            print('no admissible atom found')
            break
        xa, m0, P0, full = at
        ch = Chain(p, times, sched, eb, seed * 1000 + ia, sharp=bool(sharp))
        rows = np.array(P0, dtype=np.int8)
        stats, _, M0 = ch.explore(0, xa, rows, [1] * len(P0), 1, True, m0, Fraction(1))
        st = ch.st
        # GLOB
        a = [stats[l][1] for l in range(Lh + 1)]
        means_ok = all(stats[l][0] == M0 for l in range(Lh + 1))
        st.chk('GLOBmean', means_ok, (xa,))
        ebf = eb if eb != math.inf else None
        st.chk('GLOB1', a[1] <= (1 + ch.chi2_0) * a[0], (xa,))
        if ebf is not None:
            for l in range(1, Lh):
                st.chk('GLOBrec', a[l + 1] <= a[l] + ebf * a[l - 1], (xa, l))
            for l in range(1, Lh + 1):
                Pi = (1 + ch.chi2_0) * (1 + ebf) ** (l - 1)
                st.chk('GLOBpi', a[l] <= M0 * M0 * Pi, (xa, l))
        # PZ at the horizon: Y = M_Lh on atoms reached, 0 on atoms stopped before Lh
        # recompute Y moments: stops before Lh are frozen; use stats bookkeeping
        # delta' = measure of atoms stopped at levels < Lh
        Y1, Y2, muY, dlt = ch_Y(ch, xa, P0, stats)
        if Y2 > 0:
            pz = Y1 * Y1 / Y2
            st.chk('PZ1', muY >= pz, (xa,))
            if ebf is not None:
                Pi = float((1 + ch.chi2_0) * (1 + ebf) ** (Lh - 1))
                if Pi * float(dlt) < 1:
                    bound = (1 - math.sqrt(Pi * float(dlt))) ** 2 / Pi
                    st.chk('PZ2', float(muY) >= bound - 1e-12, (xa, float(muY), bound))
        summ.append((xa, m0, len(P0), full, ch.natoms, ch.stops, float(M0),
                     [float(v) for v in a], float(muY), float(dlt), ch.balanced))
        for k_ in st.c:
            tot.c[k_] = tot.c.get(k_, 0) + st.c[k_]
            if k_ in st.f:
                tot.f[k_] = tot.f.get(k_, 0) + st.f[k_]
                tot.ex.setdefault(k_, st.ex.get(k_))
        for k_, v in st.mx.items():
            tot.ratio(k_, v)
    print('p=%d seed=%d natoms=%d times=%s sched=%s ebar=%s P0max=%d sharp=%d' %
          (p, seed, natoms, times, sched, ebar, P0max, sharp))
    for s in summ:
        print('  atom x_A=%d m0=%d |P|=%d full=%s atoms/level=%s stops/level=%s M0=%.4g '
              'E[M~^2]=%s mu(Y>0)=%.4f delta\'=%.4f balanced=%d' %
              (s[0], s[1], s[2], s[3], s[4], s[5], s[6], ['%.4g' % v for v in s[7]],
               s[8], s[9], s[10]))
    print('%.1f s' % (time.time() - t0))
    tot.report()
    nf = sum(tot.f.values())
    print('RESULT', 'FAIL' if nf else 'OK', 'failures=%d' % nf)


def ch_Y(ch, xa, P0, stats):
    """Moments of Y = M~_Lh 1{tau >= Lh}, mu(Y>0) and delta' = mu(tau < Lh),
    from the leaf atoms recorded by the first pass."""
    Lh = ch.Lh
    leaves = ch.leaves
    Y1 = sum(mu * M for mu, M, r in leaves if r)
    Y2 = sum(mu * M * M for mu, M, r in leaves if r)
    muY = sum(mu for mu, M, r in leaves if r and M > 0)
    dlt = sum(mu for mu, M, r in leaves if not r)
    ch.st.chk('YMEAS', sum(mu for mu, M, r in leaves) == 1, (xa,))
    ch.st.chk('YCONS', sum(mu * M for mu, M, r in leaves) == stats[Lh][0], (xa,))
    return Y1, Y2, muY, dlt


if __name__ == '__main__':
    a = sys.argv[1:]
    main(int(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4]), int(a[5]), a[6], a[7],
         *[int(v) for v in a[8:]])
