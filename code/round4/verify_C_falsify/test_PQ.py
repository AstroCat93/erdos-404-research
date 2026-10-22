#!/usr/bin/env python3
"""Exact tests of M4C Lemma P and Lemma Q (report §3) at p = 7, 11, 13.

For y = -g1 + p*u (u a random p-adic integer, represented by a large integer)
with an optionally planted deep gate, and window length t, we compute exactly
  LHS_P = P(v(T) >= k),   LHS_Q = P(v(T) >= k, v(T') >= f),
T = sum_{c<t} delta_c pi_c(y), T' = sum delta_c pi_c'(y), delta_c i.i.d. lazy
signed for c >= 1 and delta_0 either lazy or fixed = 1, and the bounds
  RHS_P = prod_{l_i<k} max_a P(S_i = a mod p^{e_i}),
  RHS_Q = (q2/p^2)^{|J|} prod_{l_i<k, i not in J} max_a P(S_i = a mod p^{e_i}).
Controls: (q2/p^3)^{|J|} in place of (q2/p^2)^{|J|} (must be violated
sometimes), and runs outside the hypothesis f <= k - d_max (informative).
"""
import sys, random, time
from fractions import Fraction
sys.path.insert(0, __import__('os').path.dirname(__file__))
from vlib import vp, pis, prob_joint_zero, prob_zero, block_max, gate_data
from qconst_indep import q_exact


def make_y(p, g1, deep_at, deep_d, rng):
    # y + g_i = p*(u + i - 1); plant v(u + deep_at - 1) = deep_d - 1
    R = 40
    if deep_at is None:
        while True:
            u = rng.randrange(p ** R)
            if all((u + i) % p != 0 for i in range(0, min(4, p - 1))):
                break
    else:
        w = rng.randrange(1, p ** R)
        while w % p == 0:
            w = rng.randrange(1, p ** R)
        u = -(deep_at - 1) + p ** (deep_d - 1) * w
        # other gates near: depth 1 automatically for |i - deep_at| < p
    return -g1 + p * u


def bounds(p, y, t, k, f, q2, fixed0):
    P, D = pis(y, t)
    gates, depths, levels, blocks = gate_data(y, t, p)
    I = len(gates)
    dmax = max(depths) if depths else 0
    J = [i for i in range(1, I) if depths[i] == 1 and levels[i] < f]  # depths[i] = d_{i+1}
    rhsP = Fraction(1); rhsQ = Fraction(1)
    for i in range(I + 1):
        li = levels[i]
        if li >= k:
            continue
        lnext = levels[i + 1] if i + 1 <= I else 10 ** 9
        e = min(lnext, k) - li
        vals = [P[c] // p ** li for c in blocks[i]]
        assert all(vp(P[c], p) == li for c in blocks[i])
        bm = block_max(vals, e, p, fixed_first=(fixed0 and i == 0))
        rhsP *= bm
        if i not in J:
            rhsQ *= bm
    rhsQ_ctrl = rhsQ * (q2 / p ** 3) ** len(J)
    rhsQ *= (q2 / p ** 2) ** len(J)
    return P, D, gates, depths, levels, J, dmax, rhsP, rhsQ, rhsQ_ctrl


def main():
    p = int(sys.argv[1]); ntr = int(sys.argv[2]); maxstate = int(sys.argv[3])
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    mode = sys.argv[5] if len(sys.argv) > 5 else 'rand'
    rng = random.Random(1000 * p + seed)
    q2, _, _ = q_exact(p, 2)
    st = dict(P=0, Pfail=0, Q=0, Qfail=0, QJ=0, ctrl_viol=0, out=0, out_viol=0)
    maxratioP = 0; maxratioQ = 0; maxratioQJ = 0
    t0 = time.time()
    for tr in range(ntr):
        g1 = rng.randrange(1, p + 1)
        nb = rng.choice([2, 3, 3, 4]) if mode == 'rand' else rng.choice([3, 4])
        deep_at = rng.choice([None, None, 1, 2, 3, nb])
        deep_d = rng.choice([2, 2, 3])
        y = make_y(p, g1, deep_at if (deep_at is None or deep_at <= nb) else None, deep_d, rng)
        t = g1 + (nb - 1) * p + rng.randrange(1, p + 1)  # last block partial or full
        gates, depths, levels, blocks = gate_data(y, t, p)
        dmax = max(depths)
        fixed0 = rng.random() < 0.5
        # choose f, k
        f = rng.choice([1, 1, 2, 2, 3]) if mode == 'rand' else rng.choice([2, 2, 3, 3, 4])
        k = f + dmax + rng.choice([0, 0, 0, 1])
        outside = False
        if mode == 'J':
            Jt = [i for i in range(1, len(gates)) if depths[i] == 1 and levels[i] < f]
            if not Jt:
                continue
        if rng.random() < 0.12:
            k = f + dmax - 1   # outside hypothesis f <= k - dmax
            outside = True
        if k <= f or p ** (k + f) > maxstate:
            continue
        P_, D_, gates, depths, levels, J, dmax, rhsP, rhsQ, rhsQc = bounds(p, y, t, k, f, q2, fixed0)
        a = [x % p ** k for x in P_]; b = [x % p ** f for x in D_]
        lhsQ = prob_joint_zero(a, b, k, f, p, fixed0=fixed0)
        lhsP = prob_zero(a, k, p, fixed0=fixed0)
        st['P'] += 1
        if lhsP > rhsP:
            st['Pfail'] += 1
            print("  LEMMA P VIOLATION", p, y % p ** 8, t, k, gates, depths, float(lhsP), float(rhsP))
        maxratioP = max(maxratioP, float(lhsP / rhsP))
        if outside:
            st['out'] += 1
            if lhsQ > rhsQ:
                st['out_viol'] += 1
            continue
        st['Q'] += 1
        if J and float(lhsQ / rhsQ) > 0.6:
            print("   high-ratio J case:", dict(p=p, g1=gates[0], t=t, k=k, f=f, gates=gates, depths=depths, levels=levels, J=J,
                  fixed0=fixed0, lhsQ=float(lhsQ), rhsQ=float(rhsQ), ratio=float(lhsQ / rhsQ), lhsP=float(lhsP), rhsP=float(rhsP)), flush=True)
        if J:
            st['QJ'] += 1
            maxratioQJ = max(maxratioQJ, float(lhsQ / rhsQ))
            if lhsQ > rhsQc:
                st['ctrl_viol'] += 1
        if lhsQ > rhsQ:
            st['Qfail'] += 1
            print("  LEMMA Q VIOLATION", dict(p=p, y=y % p ** 8, t=t, k=k, f=f, gates=gates, depths=depths, J=J,
                                              lhs=float(lhsQ), rhs=float(rhsQ), fixed0=fixed0))
        maxratioQ = max(maxratioQ, float(lhsQ / rhsQ))
        if tr % 10 == 0:
            print("   [tr %d] t=%d gates=%s depths=%s k=%d f=%d J=%s fixed0=%s LHS_Q=%.4g RHS_Q=%.4g ratio=%.4g  (%.0fs)" % (
                tr, t, gates, depths, k, f, J, fixed0, float(lhsQ), float(rhsQ), float(lhsQ / rhsQ), time.time() - t0), flush=True)
    print("mode=%s " % mode + "p=%d: Lemma P tests %d, violations %d, max LHS/RHS %.4f" % (p, st['P'], st['Pfail'], maxratioP))
    print("mode=%s " % mode + "p=%d: Lemma Q tests %d (with J nonempty: %d), violations %d, max LHS/RHS %.4f (J nonempty: %.4f); control (q2/p^3 per J-block) violated in %d of %d J-tests" % (
        p, st['Q'], st['QJ'], st['Qfail'], maxratioQ, maxratioQJ, st['ctrl_viol'], st['QJ']))
    print("p=%d: outside hypothesis (k = f + d_max - 1): %d runs, bound exceeded in %d (informative only)" % (p, st['out'], st['out_viol']))


if __name__ == "__main__" and not (len(sys.argv) > 5 and sys.argv[5] == 'edge'):
    main()


def edge_main(p, maxstate, seed=7, only_deep1=False):
    """Deterministic grid of edge configurations with J nonempty."""
    rng = random.Random(77 * p + seed)
    q2, _, _ = q_exact(p, 2)
    n = 0; viol = 0; ctrl = 0; maxr = 0.0; cats = {}
    t0 = time.time()
    for nb in (3, 4):
        for deep_at in ((1,) if only_deep1 else (None, 1, 2, 3, 4)):
            if deep_at is not None and deep_at > nb:
                continue
            for deep_d in ((2,) if deep_at is None else (2, 3)):
                for g1 in sorted(set([1, 2, p - 1, p])):
                    for f in ((1, 2, 3, 4, 5) if p <= 5 else (1, 2, 3, 4)):
                        for fixed0 in (False, True):
                            for tail in ('full', 'part'):
                                y = make_y(p, g1, deep_at, deep_d, rng)
                                t = g1 + (nb - 1) * p + (p if tail == 'full' else rng.randrange(1, p))
                                gates, depths, levels, blocks = gate_data(y, t, p)
                                dmax = max(depths)
                                for k in (f + dmax, f + dmax + 1):
                                    if k <= f or p ** (k + f) > maxstate:
                                        continue
                                    J = [i for i in range(1, len(gates)) if depths[i] == 1 and levels[i] < f]
                                    if not J:
                                        continue
                                    P_, D_, gates, depths, levels, J, dmax, rhsP, rhsQ, rhsQc = bounds(p, y, t, k, f, q2, fixed0)
                                    a = [x % p ** k for x in P_]; b = [x % p ** f for x in D_]
                                    lhs = prob_joint_zero(a, b, k, f, p, fixed0=fixed0)
                                    n += 1
                                    r = float(lhs / rhsQ)
                                    maxr = max(maxr, r)
                                    key = "deep_at=%s,d=%s,J=%s" % (deep_at, deep_d if deep_at else '-', J)
                                    c = cats.setdefault(key, [0, 0.0])
                                    c[0] += 1; c[1] = max(c[1], r)
                                    if lhs > rhsQ:
                                        viol += 1
                                        print("  LEMMA Q VIOLATION", dict(p=p, g1=g1, t=t, k=k, f=f, gates=gates, depths=depths, J=J,
                                                                          fixed0=fixed0, lhs=float(lhs), rhs=float(rhsQ)), flush=True)
                                    if lhs > rhsQc:
                                        ctrl += 1
    for key in sorted(cats):
        print("   %-40s tests %3d  max ratio %.4f" % (key, cats[key][0], cats[key][1]))
    print("edge p=%d: Lemma Q edge-grid tests %d (all with J nonempty), violations %d, max LHS/RHS %.4f; control q2/p^3 violated in %d  [%.0fs]" % (
        p, n, viol, maxr, ctrl, time.time() - t0), flush=True)


if __name__ == "__main__" and len(sys.argv) > 5 and sys.argv[5] == 'edge':
    edge_main(int(sys.argv[1]), int(sys.argv[3]), int(sys.argv[4]), only_deep1=(len(sys.argv) > 6 and sys.argv[6] == 'deep1'))
