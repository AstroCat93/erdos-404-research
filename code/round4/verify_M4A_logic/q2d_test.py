#!/usr/bin/env python3
"""q2d_test.py -- targeted exact test of the 2D factor of M4A Lemma Q (verify_M4A_logic, round 4).

Chooses u with long runs of depth-1 gates (so that many blocks qualify as "2D"), large slope level f, and
compares the exact P(v(T)>=k, v(T')>=f) (joint residue DP, d_0 = 1) with the Lemma Q bound, recording the
number of 2D blocks used by the bound.  CTRL=1 strengthens the 2D factor to q_2/p^3 (must fail).
usage: q2d_test.py p SEED NTEST KMAX FMAX TMAX [CTRL]
"""
import random
import sys
from fractions import Fraction

from vl_lib import vp, q_consts, P0_table, signed_dp_joint, pis_and_derivs, lemmaQ_bound


def n2d(dep, k, f):
    t = len(dep) - 1
    gates = [g for g in range(1, t + 1) if dep[g] > 0]
    s = [None] + [dep[g] for g in gates]
    L = [0]
    for r in range(1, len(gates) + 1):
        L.append(L[-1] + s[r])
    M = [0]
    for r in range(1, len(gates) + 1):
        M.append(max(M[-1], s[r]))
    c = 0
    r = 1
    while r < len(gates) and L[r] < k:
        if s[r + 1] == 1 and L[r + 1] <= min(f, k - M[r + 1]):
            c += 1
        r += 1
    return c


def main():
    p, seed, ntest, kmax, fmax, tmax = (int(x) for x in sys.argv[1:7])
    ctrl = int(sys.argv[7]) if len(sys.argv) > 7 else 0
    rng = random.Random(seed)
    S = 10
    q = q_consts(p, S)
    if ctrl:
        q = dict(q)
        q[2] = q[2] / p
    P0 = P0_table(p, 12)
    stats = {}
    viol = 0
    done = 0
    while done < ntest:
        u = rng.randrange(p ** 10)
        t = rng.randint(2 * p, tmax)
        dep = [0] + [vp(u + g, p) for g in range(1, t + 1)]
        Vt = sum(dep)
        k = rng.randint(max(1, min(Vt, kmax) - 2), min(Vt, kmax))
        f = rng.randint(max(1, fmax - 2), fmax)
        nb = n2d(dep, k, f)
        if nb == 0 and rng.random() < 0.8:
            continue
        pi, dpi = pis_and_derivs(u, t)
        arr, tot = signed_dp_joint(pi, dpi, p ** k, p ** f, first_fixed=True)
        P = Fraction(int(arr[0, 0]), tot)
        B = lemmaQ_bound(dep, k, f, p, q, S, P0)
        done += 1
        st = stats.setdefault(nb, [0, 0, Fraction(0)])
        st[0] += 1
        if P > B:
            st[1] += 1
            viol += 1
        if B > 0:
            st[2] = max(st[2], P / B)
    for nb in sorted(stats):
        c, v, w = stats[nb]
        print(f"  #2D blocks={nb}: tests={c} violations={v} max P/bound={float(w):.6f}")
    print(f"Q2D p={p} seed={seed} ctrl={ctrl} kmax={kmax} fmax={fmax} tmax={tmax}: tests={done} violations={viol}")


if __name__ == "__main__":
    main()
