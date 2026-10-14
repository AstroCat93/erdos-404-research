#!/usr/bin/env python3
"""lift_lemma_check.py -- exact test of the lifting lemma (Lemma L in data/round4/reports/M4D.md).

Setting: windows W=[n,N), W'=[N,N2) at a Haar-random x in Z_p (prec digits), jumps D=V_N-V_n, D2=V_N2-V_N.
For r mod p^D let Lift(r) = { s mod p^(D+D2) : s == r mod p^D, s = Q_f(x) mod p^(D+D2) for some f in {0,1}^H },
where Q_f = sum_i f_i pi_{n+i}(x)/pi_n(x).  Lemma L claims, for every path e alive at n with target tau:
   { tau_N((e,f), x) mod p^(D2) : (e,f) alive at N }  =  { u^{-1} (tau - s)/p^D mod p^(D2) : s in Lift(tau mod p^D) }
with u = pi_N/(p^D pi_n) a unit; in particular the children's targets cover Z/p^(D2) iff Lift(tau mod p^D) is
full, and the number of distinct children targets mod p^(D2) equals |Lift(tau mod p^D)|.
Children are found by BRUTE FORCE over all f (direct evaluation of v(S_(e,f)(x)) >= V_N); Lift is computed
with Python sets (no numpy); a numpy recount of the lift sizes is cross-checked.  Also checks the inductive
step of Theorem F: |T_N| >= max_{r in T_n} |Lift(r)| for the full target sets T_n, T_N.
usage: lift_lemma_check.py p seed nx n H H2 [maxpar] [NEG]
"""
import random
import sys

import numpy as np

from m4d_lib import PAdic, products, alive_from_scratch, target, window_elems, unit_cofactor, \
    support_np, lift_sizes


def main():
    a = sys.argv[1:]
    p, seed, nx, n, H, H2 = (int(t) for t in a[:6])
    maxpar = int(a[6]) if len(a) > 6 else 400
    neg = int(a[7]) if len(a) > 7 else 0   # NEG control: use the wrong unit 2u (should break set equality)
    N, N2 = n + H, n + H + H2
    prec = 3 * N2 // (p - 1) + 40
    P = PAdic(p, prec)
    rnd = random.Random(seed)
    stats = dict(samples=0, parents=0, eq_fail=0, size_fail=0, full_iff_fail=0, np_fail=0, step_fail=0,
                 full_parents=0, nonfull_parents=0, zero_child=0)
    tries = 0
    while stats['samples'] < nx and tries < 100000:
        tries += 1
        x = rnd.randrange(P.mod)
        pi, dpi, vals = products(P, x, N2)
        m = sum(vals[1:n + 1])
        VN = sum(vals[1:N + 1])
        VN2 = sum(vals[1:N2 + 1])
        D, D2 = VN - m, VN2 - VN
        if max(vals[1:N2 + 1]) > 40 or D + D2 > 12 or D2 < 1:
            continue
        par = alive_from_scratch(P, pi, dpi, vals, n)
        if not par:
            continue
        stats['samples'] += 1
        K = D + D2
        mK, mD, mD2 = p ** K, p ** D, p ** D2
        ys = window_elems(x, n, N, mK)
        # all subset sums mod p^K (python sets)
        sums = {0}
        for y in ys:
            sums |= {(s + y) % mK for s in sums}
        lift = {}
        for s in sums:
            lift.setdefault(s % mD, set()).add(s)
        # numpy cross-check of the lift sizes
        L = lift_sizes(support_np(ys, mK), p, D, D2)
        for r in range(mD):
            if L[r] != len(lift.get(r, ())):
                stats['np_fail'] += 1
                break
        u = unit_cofactor(x, n, N, p, D, mD2)
        uinv = pow(u, -1, mD2) if mD2 > 1 else 0
        if neg:
            uinv = pow(2 * u % mD2, -1, mD2)
        Tn, TN = set(), set()
        rnd.shuffle(par)
        for idx, (b, S, dS) in enumerate(par):
            tau = target(P, S, pi[n], m)
            Tn.add(tau % mD)
            if idx >= maxpar:
                continue
            stats['parents'] += 1
            kids = set()
            nk = 0
            for f in range(1 << H):
                S2 = S
                for i in range(H):
                    if (f >> i) & 1:
                        S2 += pi[n + i]
                S2 %= P.mod
                if P.v(S2) >= VN:
                    nk += 1
                    kids.add(target(P, S2, pi[N], VN) % mD2)
            TN |= kids
            r = tau % mD
            # predicted children targets: u^{-1}(tau - s)/p^D mod p^D2 over the lifts s of r
            pred = set()
            for s in lift.get(r, ()):
                diff = (tau - s) % mK
                assert diff % mD == 0
                pred.add((diff // mD) * uinv % mD2)
            if kids != pred:
                stats['eq_fail'] += 1
            if len(kids) != len(lift.get(r, ())):
                stats['size_fail'] += 1
            full = len(lift.get(r, ())) == mD2
            if full:
                stats['full_parents'] += 1
            else:
                stats['nonfull_parents'] += 1
            if (len(kids) == mD2) != full:
                stats['full_iff_fail'] += 1
            if nk == 0:
                stats['zero_child'] += 1
        # inductive step of Theorem F (only meaningful if all parents were processed)
        if len(par) <= maxpar:
            best = max(len(lift.get(r, ())) for r in Tn)
            if len(TN) < best:
                stats['step_fail'] += 1
    print(f"RESULT liftlemma{' NEG-CONTROL' if neg else ''} p={p} n={n} H={H} H2={H2} samples={stats['samples']} parents={stats['parents']} "
          f"(full lift {stats['full_parents']}, non-full {stats['nonfull_parents']}, childless {stats['zero_child']}): "
          f"set-equality fails={stats['eq_fail']}, size fails={stats['size_fail']}, "
          f"full<=>cover fails={stats['full_iff_fail']}, numpy-lift mismatches={stats['np_fail']}, "
          f"induction-step fails={stats['step_fail']}")


if __name__ == "__main__":
    main()
