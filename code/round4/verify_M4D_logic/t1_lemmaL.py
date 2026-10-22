#!/usr/bin/env python3
"""t1_lemmaL.py -- brute-force exact test of M4D Lemma L (and of (F2), on which it rests).

Windows W=[n,N), W'=[N,N2), N=n+H, N2=N+H2, jumps D=V_N-V_n, D2=V_N2-V_N, K=D+D2, unit u=pi_N/(p^D pi_n).
For every path e of length n alive at n (found by DFS, validated in t2), with exact target tau:
  * children by BRUTE FORCE: all f in {0,1}^H, S_(e,f) = S_e + sum_i f_i pi_{n+i}(x) as exact integers,
    alive iff v(S_(e,f)) >= V_N; child target = -S_(e,f)/pi_N mod p^D2 (target_mod, exact);
  * (F2) check: (e,f) alive  <=>  Q_f = tau (mod p^D), where Q_f is computed from the window elements y_i
    (independent of the S-route); and child target == u^{-1}(tau - Q_f)/p^D (mod p^D2);
  * Lemma L: { child targets mod p^D2 } == lambda(Lift(tau mod p^D)),  lambda(s) = u^{-1}(tau - s)/p^D mod p^D2;
    |children targets| == |Lift(r)|;  lambda injective on the whole coset r + p^D Z/p^K (bijection onto Z/p^D2);
  * full-lift  <=>  children targets cover Z/p^D2.
NEG control (neg=1): lambda computed with 2u in place of u  -> set equality must fail for some parents.
usage: t1_lemmaL.py p seed nx n H H2 [maxpar] [neg] [gate_pos gate_depth]
"""
import random
import sys

from vF import make_x, valuations, products, alive_dfs, target_mod, lift_sets, unit_of_window, \
    window_elems, vp


def main():
    a = sys.argv[1:]
    p, seed, nx, n, H, H2 = (int(t) for t in a[:6])
    maxpar = int(a[6]) if len(a) > 6 else 200
    neg = int(a[7]) if len(a) > 7 else 0
    forced = ((int(a[8]), int(a[9])),) if len(a) > 9 else ()
    N, N2 = n + H, n + H + H2
    rng = random.Random(seed)
    st = dict(samples=0, parents=0, f2_fail=0, f2tgt_fail=0, eq_fail=0, size_fail=0, inj_fail=0,
              full_fail=0, full=0, nonfull=0, childless=0, D0=0, D20=0, tried=0)
    while st['samples'] < nx:
        st['tried'] += 1
        if st['tried'] > 5000:   # guard: some forced-gate classes have no alive path at n at all
            print(f"GUARD: stopped after {st['tried'] - 1} draws with only {st['samples']} admissible samples")
            break
        x = make_x(rng, p, 3 * N2 // (p - 1) + 25, forced)
        vals, V = valuations(x, p, N2)
        D, D2 = V[N] - V[n], V[N2] - V[N]
        if D + D2 > 14:      # keep p^K small enough for python sets
            continue
        pi = products(x, N2)
        par = alive_dfs(x, p, n, pi, V)
        if not par:
            continue
        st['samples'] += 1
        st['D0'] += (D == 0)
        st['D20'] += (D2 == 0)
        K = D + D2
        mK, mD, mD2 = p ** K, p ** D, p ** D2
        lift = lift_sets(x, p, n, H, D, D2)
        u = unit_of_window(x, p, n, H, D)
        assert u % p != 0
        uu = (2 * u) if neg else u
        uinv = pow(uu % mD2, -1, mD2) if D2 > 0 else 0
        ys = window_elems(x, n, H, mK)
        rng.shuffle(par)
        for (mask, S) in par[:maxpar]:
            st['parents'] += 1
            tau = target_mod(S, pi[n], V[n], p, K + 5)   # tau mod p^(K+5)
            r = tau % mD
            kids = set()
            nk = 0
            for f in range(1 << H):
                S2 = S
                Q = 0
                for i in range(H):
                    if (f >> i) & 1:
                        S2 += pi[n + i]
                        Q += ys[i]
                alive = (S2 == 0) or vp(S2, p) >= V[N]
                if alive != ((Q - tau) % mD == 0):
                    st['f2_fail'] += 1
                if alive:
                    nk += 1
                    c = target_mod(S2, pi[N], V[N], p, D2)
                    kids.add(c)
                    if D2 > 0:
                        pred = ((tau - Q) % mK) // mD * pow(u % mD2, -1, mD2) % mD2
                        if pred != c:
                            st['f2tgt_fail'] += 1
            L = lift.get(r, set())
            pred_set = {((tau - s) % mK) // mD * uinv % mD2 if D2 > 0 else 0 for s in L}
            if kids != pred_set:
                st['eq_fail'] += 1
            if len(kids) != len(L):
                st['size_fail'] += 1
            # lambda on the whole coset r + p^D Z / p^K is a bijection onto Z/p^D2
            if not neg:
                img = {((tau - (r + k * mD)) % mK) // mD * uinv % mD2 if D2 > 0 else 0 for k in range(mD2)}
                if len(img) != mD2:
                    st['inj_fail'] += 1
            full = (len(L) == mD2)
            st['full' if full else 'nonfull'] += 1
            if full != (len(kids) == mD2):
                st['full_fail'] += 1
            if nk == 0:
                st['childless'] += 1
    print(f"RESULT t1{' NEG-CONTROL(2u)' if neg else ''} p={p} seed={seed} n={n} H={H} H2={H2} forced={forced}: "
          f"samples={st['samples']} (with D=0: {st['D0']}, D2=0: {st['D20']}), parents={st['parents']} "
          f"(full lift {st['full']}, non-full {st['nonfull']}, childless {st['childless']}); "
          f"(F2) aliveness fails={st['f2_fail']}, (F2) target-formula fails={st['f2tgt_fail']}, "
          f"LemmaL set-equality fails={st['eq_fail']}, size fails={st['size_fail']}, "
          f"coset-bijection fails={st['inj_fail']}, full<=>cover fails={st['full_fail']}")


if __name__ == "__main__":
    main()
