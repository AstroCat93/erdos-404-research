"""obstr_tests.py -- exact small-scale tests of how M4A's argument sits relative to the known obstructions.

Usage:
  python3 obstr_tests.py floor  p SEED NTESTS KMAX         # T1: Prop 11.12 floor holds for chi^2_W, not for eps
  python3 obstr_tests.py shadow p SEED n N N2 istar SMAX   # T2: deep gate at distance 2 (Prop 11.15(b) / N3)
  python3 obstr_tests.py consts PMAX SMAX                  # T3: q_s, P_0; Cor 10.20 / Prop 11.24 and Thm 3.2(a)
  python3 obstr_tests.py ball   p SEED NBALLS b KMAX       # T4: sup vs mean of eps on a ball (barrier loophole)
  python3 obstr_tests.py nonuniform p SEED t SMAX          # T5: high-slope mass is not uniformly bounded over cylinders
  python3 obstr_tests.py thm1   p SEED NBALLS b KMAX [CTRL]      # T6: M4A Theorem 1 identity on frozen balls with a depth-(b-1) gate [CTRL=1: theta+1]

Exact rational arithmetic throughout (vo_lib.py).  M4A's bound evaluators (code/round4/M4A/bounds.py) are
imported read-only, only to compare the bounds under test with exact values.
"""
import os
import random
import sys
import itertools
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(HERE, '..', 'M4A'))
from vo_lib import vp, window, coll_pair, chi2_window, depths  # noqa: E402
import bounds as M4A  # noqa: E402  (read-only use of the bounds under test)


def t1_floor(p, seed, ntests, kmax):
    """Prop 11.12: chi^2_W >= (p-1) 4^-p for every window with D >= 1.  The composite band mass eps has no
    such floor -- that is how Theorem C3 (and hence M4A) evades Prop 11.12."""
    rng = random.Random(seed)
    floor = Fraction(p - 1, 4 ** p)
    done = 0
    chi_viol = 0
    eps_below = 0
    min_eps = None
    min_chi = None
    while done < ntests:
        x = rng.randrange(p ** 20)
        n = rng.randrange(2 * p, 3 * p + 12)
        H1 = rng.randrange(p, 17)
        H2 = rng.randrange(p, 31 - H1 + 1)
        N, N2 = n + H1, n + H1 + H2
        dep, D, K, MW = window(x, n, N, N2, p)
        if K > kmax or D < 1 or D == K:
            continue
        PK, PD, D_, K_ = coll_pair(x, n, N, N2, p)[:4]
        eps = PK - PD
        chi1, _ = chi2_window(x, n, N, p)
        chi2, D2 = chi2_window(x, N, N2, p)
        assert eps >= 0
        for ch, d in ((chi1, D), (chi2, D2)):
            if d >= 1:
                if ch < floor:
                    chi_viol += 1
                min_chi = ch if min_chi is None else min(min_chi, ch)
        if eps < floor:
            eps_below += 1
        min_eps = eps if min_eps is None else min(min_eps, eps)
        done += 1
        if done <= 6:
            print(f"  x={x} [n,N,N')=[{n},{N},{N2}) D={D} K={K} M_W={MW}: chi2_W={float(chi1):.4g} chi2_W'={float(chi2):.4g} eps={float(eps):.4g}")
    print(f"T1 p={p}: {done} composite windows (K<={kmax}); floor (p-1)4^-p = {float(floor):.4g}")
    print(f"   chi^2 of single windows below the floor: {chi_viol} (Prop 11.12 predicts 0); min chi^2 = {float(min_chi):.4g}")
    print(f"   composite eps below the floor: {eps_below}/{done}; min eps = {float(min_eps):.4g}")


def t2_shadow(p, seed, n, N, N2, istar, smax):
    """A gate at i* in the SECOND half (N,N') with v(x+i*) = s, at distance 2 from c = i*-2-n.  Exact eps(x_s);
    rigorous lower bound p^(K0+s) 2^-(H+2) - p^D (double root (u+2)^2, R3M Prop N3); Prop D (pointwise, M4A)
    must dominate p^K Coll_K, so it must grow like p^s too (barrier: no depth-uniform deterministic bound)."""
    rng = random.Random(seed)
    H = N2 - n
    c = istar - 2 - n
    assert N < istar < N2 and c >= 0
    q = M4A.qconsts(p, 8)
    P0 = M4A.block0_table(p, 10)
    R = 60
    w = rng.randrange(1, p ** 30)
    while w % p == 0:
        w = rng.randrange(1, p ** 30)
    print(f"T2 p={p}: window [{n},{N},{N2}) H={H}, gate at i*={istar} (c={c}), unit w={w}")
    cum = Fraction(0)
    fails = 0
    for s in range(1, smax + 1):
        x = (p ** s * w - istar) % p ** R
        assert vp(x + istar, p) == s
        dep, D, K, MW = window(x, n, N, N2, p)
        K0 = K - s
        a_c = sum(dep[n + 1:n + c + 1])
        PK, PD, _, _, _ = coll_pair(x, n, N, N2, p)
        eps = PK - PD
        lb = Fraction(p ** K, 2 ** (H + 2)) - p ** D if a_c + 2 * s >= K else None
        pd = M4A.propD_bound(dep, n, N, N2, p, q, 'K', P0)
        ok_lb = (lb is None) or eps >= lb
        ok_pd = PK <= pd
        if not (ok_lb and ok_pd):
            fails += 1
        cum += Fraction(p - 1, p) * Fraction(1, p ** s) * eps
        print(f"  s={s:2d} K={K:2d} D={D} M_W={MW}: eps={float(eps):.5g}  eps/p^s={float(eps / p ** s):.5g}  "
              f"lowerbd={'n/a' if lb is None else f'{float(lb):.4g}'}  PropD(p^K Coll_K)={float(pd):.5g} >= p^K Coll_K={float(PK):.5g}: {ok_pd}"
              f"  partial sum_s mu(depth=s) eps = {float(cum):.5g}")
    print(f"T2 p={p}: failures (eps < lower bound, or Prop D < exact): {fails}")


def t3_consts(pmax, smax):
    """q_s and P_0(g,s) by direct enumeration (own code).  Checks:
       q_1 > 1 (the value-only, supremum-type per-level factor is >= 1: Cor 10.20 / Prop 11.24 analogue);
       q_2/p < 1 (the 2D gain exists only with the slope condition);
       P_0(2,s) = 1/4 for all s (the double root (y+2)^2, Prop 11.15(b));
       P_0(g,s) = 0 for g != 2 and s large: the signed block-0 sum at -g never vanishes (signed Thm 3.2(a))."""
    for p in [pp for pp in (3, 5, 7, 11, 13) if pp <= pmax]:
        pk = [1]
        for k in range(1, p):
            pk.append(pk[-1] * (k - p))
        law = {}
        for d in itertools.product((-1, 0, 1), repeat=p):
            wt = 1
            for e in d:
                wt *= 2 if e == 0 else 1
            z = sum(a * b for a, b in zip(d, pk))
            law[z] = law.get(z, 0) + wt
        qs = []
        for s in range(1, smax + 1):
            F = {}
            for z, cc in law.items():
                F[z % p ** s] = F.get(z % p ** s, 0) + cc
            qs.append(Fraction(p ** s * max(F.values()), 4 ** p))
        maxatom = Fraction(max(law.values()), 4 ** p)
        print(f"T3 p={p}: q_1={qs[0]} ({float(qs[0]):.6f}) > 1: {qs[0] > 1};  q_2/p={float(qs[1] / p):.5f} < 1: {qs[1] < p};"
              f"  q_s/p^s -> max atom of Z = {maxatom}; q_s/p^s at s={smax}: {qs[-1] / p ** smax}")
        if p == 7:
            print(f"       M4A values: q_1=8309/8192 {qs[0] == Fraction(8309, 8192)}, q_2=4557/4096 {qs[1] == Fraction(4557, 4096)},"
                  f" q_3=33271/8192 {qs[2] == Fraction(33271, 8192)}, q_s=7^s*3/256 (s>=4) {all(qs[s - 1] == Fraction(3 * 7 ** s, 256) for s in range(4, smax + 1))}")
        # block 0
        zero_ok = True
        for g in range(1, p + 1):
            vals = [1]
            for cc in range(1, g):
                vals.append(vals[-1] * (cc - g))
            dist = {}
            for d in itertools.product((-1, 0, 1), repeat=g - 1):
                wt = 1
                for e in d:
                    wt *= 2 if e == 0 else 1
                z = 1 + sum(a * b for a, b in zip(d, vals[1:]))
                dist[z] = dist.get(z, 0) + wt
            exact_zero = Fraction(dist.get(0, 0), 4 ** (g - 1))
            if (g == 2 and exact_zero != Fraction(1, 4)) or (g != 2 and exact_zero != 0):
                zero_ok = False
            if g >= 3:  # S == 1 mod (g-1)
                assert all((z - 1) % (g - 1) == 0 for z in dist)
            P0 = [Fraction(sum(cc for z, cc in dist.items() if z % p ** s == 0), 4 ** (g - 1)) for s in range(1, smax + 1)]
            if p == 7 or g <= 3:
                print(f"       P_0({g},s), s=1..{smax}: {[str(v) for v in P0]};  P(sum == 0 exactly) = {exact_zero}")
        print(f"       only g=2 has an exact zero (prob 1/4), every g>=3 has S == 1 mod (g-1): {zero_ok}")


def t4_ball(p, seed, nballs, b, kmax):
    """On a ball B = x0 + p^b Z_p with constant gate pattern on (n,N'], enumerate x mod p^(K+M_W) exactly.
    Compare sup_B eps, E_B eps, Prop D (pointwise; depends only on the pattern) and Prop E (averaged)."""
    rng = random.Random(seed)
    q = M4A.qconsts(p, 8)
    P0 = M4A.block0_table(p, 10)
    done = 0
    tries = 0
    while done < nballs and tries < 20000:
        tries += 1
        x0 = rng.randrange(p ** b)
        n = rng.randrange(2 * p, 3 * p + 10)
        H1 = rng.randrange(p, 15)
        H2 = rng.randrange(p, 31 - H1 + 1)
        N, N2 = n + H1, n + H1 + H2
        dep, D, K, MW = window(x0, n, N, N2, p)
        if MW >= b or K > kmax or D < 2:
            continue
        th = min((D + 1) // 2, D - b + 1)
        if th > 0 and K - MW < th:
            continue
        R = K + MW
        npts = p ** (R - b)
        if npts > 6000:
            continue
        tot = Fraction(0)
        mx = Fraction(0)
        for t in range(npts):
            x = x0 + p ** b * t
            PK, PD, D_, K_, MW_ = coll_pair(x, n, N, N2, p)
            assert (D_, K_, MW_) == (D, K, MW)
            e = PK - PD
            tot += e
            mx = max(mx, e)
        mean = tot / npts
        pdb = M4A.propD_bound(dep, n, N, N2, p, q, 'K', P0) - 1
        peb, th2 = M4A.propE_bound(dep, n, N, N2, b, p, q, P0)
        okD = mx <= pdb
        okE = mean <= peb
        print(f"T4 p={p} B={x0}+{p}^{b}Z [{n},{N},{N2}) D={D} K={K} M_W={MW} theta={th2} pts={npts}: "
              f"E_B eps={float(mean):.4g}  sup_B eps={float(mx):.4g}  sup/mean={float(mx / mean) if mean else float('inf'):.3g}  "
              f"PropD-1={float(pdb):.4g} >= sup: {okD}  PropE={float(peb):.4g} >= mean: {okE}")
        done += 1
    print(f"T4 p={p}: {done} balls")


def t5_nonuniform(p, seed, t, smax):
    """No bound on the normalised HIGH-SLOPE mass can be uniform over cylinders (so (S) of the brief can only
    hold in a gate-pattern-dependent form, as in M4A's Lemma Q).  At u with v(u+2) = s, the signed path
    (1,1,1,0,...,0) has T = (u+2)^2, T' = 2(u+2): v(T) = 2s, v(T') = s.  With k = V_t(u), f = s:
       G(u;t,k,f) = p^k P(v(T) >= k, v(T') >= f) >= p^k 2^-(t+1),  k = s + v((t-2)!) -> infinity.
    Exact G by a DP over (T mod p^k, T' mod p^f); compare with the path lower bound and with M4A's Lemma Q."""
    import numpy as np
    rng = random.Random(seed)
    P0 = M4A.block0_table(p, 12)
    q = M4A.qconsts(p, 8)
    for s in range(1, smax + 1):
        w = rng.randrange(1, p ** 20)
        while w % p == 0:
            w = rng.randrange(1, p ** 20)
        u = p ** s * w - 2
        assert u >= 0 and vp(u + 2, p) == s
        T = 1 + (u + 1) + (u + 1) * (u + 2)
        dT = 1 + (2 * u + 3)  # derivative of 1 + (u+1) + (u+1)(u+2)
        assert T == (u + 2) ** 2 and vp(T, p) == 2 * s and vp(dT, p) == s
        dep = [0] + [vp(u + i, p) for i in range(1, t + 1)]
        k = sum(dep)
        f = s
        if 2 * s < k:
            print(f"T5 p={p} s={s}: 2s < k={k}, skipped")
            continue
        mk, mf = p ** k, p ** f
        if mk * mf > 6 * 10 ** 6:
            print(f"T5 p={p} s={s}: state space too large, skipped")
            continue
        cnt = np.zeros((mk, mf), dtype=np.int64)
        cnt[1 % mk, 0] = 1
        pi, dpi = 1, 0
        for c in range(1, t):
            dpi = dpi * (u + c) + pi
            pi = pi * (u + c)
            a, b = pi % mk, dpi % mf
            cnt = 2 * cnt + np.roll(np.roll(cnt, a, axis=0), b, axis=1) + np.roll(np.roll(cnt, -a, axis=0), -b, axis=1)
        Gex = p ** k * Fraction(int(cnt[0, 0]), 4 ** (t - 1))
        lb = Fraction(p ** k, 2 ** (t + 1))
        Q = M4A.lemmaQ_bound(dep, 0, t, k, f, p, q, P0)
        print(f"T5 p={p} t={t} s={s}: k=V_t(u)={k} f={f}  exact G={float(Gex):.5g} >= path bound p^k 2^-(t+1)={float(lb):.5g}: {Gex >= lb}"
              f"   Lemma Q bound={float(Q):.5g} >= exact: {Q >= Gex}")


def t6_thm1(p, seed, nballs, b, kmax, ctrl=0):
    """Theorem 1 of M4A (the averaging step that exploits the barrier loophole), tested exactly on balls with a
    frozen gate pattern that contains a gate of the maximal frozen depth b-1:
       E_B[eps] = 2^-H (p^K - p^D) + E_delta[1_{delta!=0} (p^K mu_B{v(S)>=K, v(S')>=theta} - p^D mu_B{v(S)>=D, v(S')>=theta})].
    Own DP over (S mod p^K, S' mod p^theta) for each x in B (x enumerated mod p^R, R = K + M_W >= theta + 2 M_W)."""
    import numpy as np
    rng = random.Random(seed)
    done = tries = 0
    bad = 0
    while done < nballs and tries < 50000:
        tries += 1
        x0 = rng.randrange(p ** b)
        n = rng.randrange(2 * p, 3 * p + 10)
        H1 = rng.randrange(p, 15)
        H2 = rng.randrange(p, 25 - H1 + 1)
        N, N2 = n + H1, n + H1 + H2
        dep, D, K, MW = window(x0, n, N, N2, p)
        if MW != b - 1 or K > kmax or D < 2:
            continue
        th = min((D + 1) // 2, D - b + 1)
        if th < 1:
            continue
        if ctrl:  # negative control: a slope threshold one above the one allowed by Lemma H
            th += 1
            if K - th < 0:
                continue
        R = max(K + MW, th + 2 * MW)
        npts = p ** (R - b)
        if npts * p ** (K + th) > 4 * 10 ** 8:
            continue
        H = N2 - n
        lhs = Fraction(0)
        rhs_hs = Fraction(0)
        mk, mt = p ** K, p ** th
        for tt in range(npts):
            x = x0 + p ** b * tt
            PK, PD, D_, K_, MW_ = coll_pair(x, n, N, N2, p)
            assert (D_, K_, MW_) == (D, K, MW)
            lhs += PK - PD
            cnt = np.zeros((mk, mt), dtype=np.int64)
            cnt[0, 0] = 1
            y, dy = 1, 0
            for c in range(H):
                a, bb = y % mk, dy % mt
                cnt = 2 * cnt + np.roll(np.roll(cnt, a, axis=0), bb, axis=1) + np.roll(np.roll(cnt, -a, axis=0), -bb, axis=1)
                dy = dy * (x + n + c + 1) + y
                y = y * (x + n + c + 1)
            zero = 2 ** H  # weight of delta = 0 (it lies in state (0,0))
            cK = int(cnt[0, 0]) - zero
            cD = int(cnt[0::p ** D, 0].sum()) - zero
            rhs_hs += Fraction(p ** K * cK - p ** D * cD, 4 ** H)
        lhs /= npts
        rhs = Fraction(p ** K - p ** D, 2 ** H) + rhs_hs / npts
        ok = (lhs == rhs)
        bad += (not ok)
        print(f"T6 p={p} B={x0}+{p}^{b}Z [{n},{N},{N2}) D={D} K={K} M_W={MW} theta={th} pts={npts}: "
              f"E_B eps={float(lhs):.6g}  RHS={float(rhs):.6g}  exact equality: {ok}")
        done += 1
    print(f"T6 p={p}{' CONTROL theta+1' if ctrl else ''}: {done} balls, {bad} failures")


if __name__ == '__main__':
    cmd = sys.argv[1]
    a = [int(z) for z in sys.argv[2:]]
    if cmd == 'floor':
        t1_floor(*a)
    elif cmd == 'shadow':
        t2_shadow(*a)
    elif cmd == 'consts':
        t3_consts(*a)
    elif cmd == 'ball':
        t4_ball(*a)
    elif cmd == 'nonuniform':
        t5_nonuniform(*a)
    elif cmd == 'thm1':
        t6_thm1(*a)
