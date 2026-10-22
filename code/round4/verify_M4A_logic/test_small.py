#!/usr/bin/env python3
"""test_small.py -- exact small-case tests for the LOGIC check of M4A (verify_M4A_logic, round 4).

modes:
  Q   p SEED NTEST KMAX FMAX [CTRL]   Lemma Q: exact P(v(T)>=k, v(T')>=f) (joint residue DP) vs the bound of the
                                      statement.  Families: random u, planted first gate (g,s), integer-like u.
                                      CTRL=1: negative control, 2D factor q_2/p^2 replaced by q_2/p^3.
  T1  p SEED NCASE b HMIN HMAX KMAX   Theorem 1 identity (exact equality), Prop D (pointwise), Prop E (averaged)
                                      on balls B = x0 + p^b Z_p with constant gate pattern on (n, N'].
Everything is exact (python ints, Fractions, int64 counts < 4^31).  Written from data/round4/reports/M4A.md.
"""
import random
import sys
from fractions import Fraction

import numpy as np

from vl_lib import (vp, q_consts, P0_table, signed_dp_0, signed_dp_joint, pis_and_derivs, lemmaQ_bound,
                    propDE_bound, window_vals)


def mode_Q(p, seed, ntest, kmax, fmax, ctrl):
    rng = random.Random(seed)
    S = 10
    q = q_consts(p, S)
    if ctrl:
        q = dict(q)
        q[2] = q[2] / p      # claim strengthened: 2D factor q_2/p^3
    P0 = P0_table(p, 12)
    nviol = ntot = n2d = 0
    worst = Fraction(0)
    for it in range(ntest):
        fam = it % 4
        if fam == 0:
            u = rng.randrange(p ** 12)
        elif fam == 1:   # planted first gate at g with depth >= s (g = 2: double root of (y+2)^2)
            g0, s0 = rng.choice([2, 2, 1, 3, p]), rng.randint(2, 6)
            u = (-g0) % p ** s0 + p ** s0 * rng.randrange(p ** 6)
        elif fam == 2:   # integer-like small u (u = natural number)
            u = rng.randrange(1, 4 * p * p)
        else:            # planted deep gate later in the range
            g0, s0 = rng.randint(1, 3 * p), rng.randint(2, 5)
            u = (-g0) % p ** s0 + p ** s0 * rng.randrange(p ** 6)
        t = rng.randint(p + 1, min(30, 5 * p))
        dep = [0] + [vp(u + g, p) for g in range(1, t + 1)]
        Vt = sum(dep)
        k = rng.randint(1, min(Vt, kmax))
        f = rng.randint(-1, fmax)
        pi, dpi = pis_and_derivs(u, t)
        if f <= 0:
            cnt, tot = signed_dp_0(pi, p ** k, first_fixed=True)
        else:
            arr, tot = signed_dp_joint(pi, dpi, p ** k, p ** f, first_fixed=True)
            cnt = int(arr[0, 0])
        P = Fraction(cnt, tot)
        B = lemmaQ_bound(dep, k, f, p, q, S, P0)
        # count 2D blocks (for reporting)
        ntot += 1
        if P > B:
            nviol += 1
            if nviol <= 5:
                print(f"  VIOLATION u={u} t={t} k={k} f={f} dep={dep[1:]} P={P} bound={B}")
        if B > 0:
            worst = max(worst, P / B)
    print(f"Q p={p} seed={seed} ctrl={ctrl}: tests={ntot} violations={nviol} max P/bound={float(worst):.6f}")
    return nviol


def find_ball(rng, p, b, H):
    """random x0 mod p^b and n with all v(x0+i) < b for n < i <= n+H (constant pattern on x0 + p^b Z_p)."""
    for _ in range(10000):
        x0 = rng.randrange(p ** b)
        n = rng.randrange(0, 3 * p ** b)
        if all(vp(x0 + i, p) < b for i in range(n + 1, n + H + 1)):
            return x0, n
    return None


def mode_T1(p, seed, ncase, b, hmin, hmax, kmax):
    rng = random.Random(seed)
    S = 10
    q = q_consts(p, S)
    P0 = P0_table(p, 12)
    done = idfail = dfail = efail = eskip = 0
    tries = 0
    worstD = worstE = Fraction(0)
    while done < ncase and tries < 400:
        tries += 1
        H = rng.randint(hmin, hmax)
        fb = find_ball(rng, p, b, H)
        if fb is None:
            continue
        x0, n = fb
        N2 = n + H
        N = n + rng.randint(1, H - 1)
        depth = {i: vp(x0 + i, p) for i in range(n + 1, N2 + 1)}
        D = sum(depth[i] for i in range(n + 1, N + 1))
        K = sum(depth[i] for i in range(n + 1, N2 + 1))
        if D < 1 or K <= b or K > kmax:
            continue
        th = min((D + 1) // 2, D - b + 1)
        thq = max(th, 0)
        modT = p ** thq if thq > 0 else 1
        # exact averages over B: x = x0 + p^b w, w mod p^(K-b)
        npts = p ** (K - b)
        sumCK = sumCD = sumAK = sumAD = 0
        epsmax = Fraction(-10 ** 9)
        for w in range(npts):
            x = x0 + p ** b * w
            ys, dys = window_vals(x, n, H, p ** K, modT)
            arr, tot = signed_dp_joint(ys, dys, p ** K, modT)
            CK = int(arr[0, :].sum())
            CD = int(arr[::p ** D, :].sum())       # residues s == 0 mod p^D
            AK = int(arr[0, 0])
            AD = int(arr[::p ** D, 0].sum())
            sumCK += CK
            sumCD += CD
            sumAK += AK
            sumAD += AD
            eps = Fraction(p ** K * CK - p ** D * CD, tot)
            epsmax = max(epsmax, eps)
        tot = 4 ** H
        LHS = Fraction(p ** K * sumCK - p ** D * sumCD, tot * npts)
        z = 2 ** H   # weight of delta = 0 (it is counted in every class; S=0, S'=0)
        RHS = Fraction(z * (p ** K - p ** D), tot) + \
            Fraction(p ** K * (sumAK - z * npts) - p ** D * (sumAD - z * npts), tot * npts)
        ok_id = (LHS == RHS)
        idfail += (not ok_id)
        # Prop D (pointwise; pattern constant on B, so one bound for all x in B)
        depth_arr = [0] * (N2 + 1)
        for i in range(n + 1, N2 + 1):
            depth_arr[i] = depth[i]
        bD = propDE_bound(depth_arr, n, N, N2, p, q, S, P0)
        okD = epsmax <= bD - 1
        dfail += (not okD)
        worstD = max(worstD, (epsmax + 1) / bD)
        # Prop E (averaged): needs M_W <= K - theta (Lemma F)
        MW = max(depth.values())
        if MW <= K - th:
            bE = propDE_bound(depth_arr, n, N, N2, p, q, S, P0, theta=th)
            okE = LHS <= bE
            # Lemma F (+Q) directly: high-slope mass p^K P(delta!=0, v(S)>=K, v(S')>=theta) <= PropE - p^K 2^-H
            HS = Fraction(p ** K * (sumAK - z * npts), tot * npts)
            okF = HS <= bE - Fraction(p ** K, 2 ** H)
            okE = okE and okF
            efail += (not okE)
            if LHS > 0:
                worstE = max(worstE, LHS / bE)
            Es = f"E_B eps={float(LHS):.4g} HS={float(HS):.4g} PropE={float(bE):.4g} okE&F={okE}"
        else:
            eskip += 1
            Es = "PropE skipped (M_W > K-theta)"
        done += 1
        print(f"  case p={p} b={b} x0={x0} [n,N,N')=[{n},{N},{N2}) D={D} K={K} theta={th} M_W={MW} "
              f"identity={'EXACT' if ok_id else 'FAIL'} LHS={float(LHS):.6g} max eps={float(epsmax):.4g} "
              f"PropD-1={float(bD - 1):.4g} okD={okD}; {Es}")
    print(f"T1 p={p} seed={seed} b={b}: cases={done} identity failures={idfail} PropD failures={dfail} "
          f"PropE/LemmaF failures={efail} (skipped {eskip}); max (eps+1)/PropD={float(worstD):.4f}, "
          f"max E_B eps/PropE={float(worstE):.4f}")
    return idfail + dfail + efail


if __name__ == "__main__":
    mode = sys.argv[1]
    a = [int(x) for x in sys.argv[2:]]
    if mode == 'Q':
        bad = mode_Q(a[0], a[1], a[2], a[3], a[4], a[5] if len(a) > 5 else 0)
        sys.exit(0)
    elif mode == 'T1':
        bad = mode_T1(*a)
        sys.exit(1 if bad else 0)
