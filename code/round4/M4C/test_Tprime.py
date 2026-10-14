#!/usr/bin/env python3
"""test_Tprime.py -- consistency test of Lemma T' (M4C report section 7.1): the closed form must dominate the
term-by-term bound B of Lemma T (as evaluated by assemble.phase2_window) on every window where both apply.
Windows: b_{l-1} = bm, b_l = floor(5 bm/4), b_{l+1} = floor(5 b_l/4) (far-tail rule), several s with (T2).
usage: test_Tprime.py p1 p2 ...
"""
import sys
from fractions import Fraction

import mpmath as mp

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from assemble import phase2_window, Xi  # noqa: E402
from early_phase import q1_exact, q2_exact, q3_exact  # noqa: E402

mp.mp.dps = 50


def closed(p, bm, bk, bp, s, Q1, Q2, Q3):
    N, NW = bp - bm, bk - bm
    alpha = Fraction(1) + Fraction(1, p) + Fraction(1, p * p) + Fraction(1, p * p * (p - 1))
    aF = mp.mpf(alpha.numerator) / alpha.denominator
    rho = Q2 / p
    r1 = mp.mpf(2) ** (-p) * mp.mpf(p) ** aF * rho ** (-(1 - mp.mpf(1) / p))
    hw = -(-NW // 2)
    num = hw - s
    Ilow = max(0, -(-(num * alpha.denominator) // alpha.numerator) - 1) if num > 0 else 0
    U = -(-N // (p * p))
    lp = mp.log(p)
    logC1 = N * mp.log(Q1) + (-(-N // p)) * mp.log(Q2) + U * mp.log(Q3) + Xi(U, p, s) * lp
    t1 = -N * p * mp.log(2) + (aF * N + s) * lp
    t2 = mp.log(1 / (1 - r1)) + logC1 + (aF + s) * lp + (Ilow * (1 - mp.mpf(1) / p) - 1) * mp.log(rho)
    return mp.e ** t1 + mp.e ** t2


for p in (int(a) for a in sys.argv[1:]):
    Q1, Q2, Q3 = (mp.mpf(q.numerator) / q.denominator for q in (q1_exact(p), q2_exact(p), q3_exact(p)))
    st = dict(windows=0, fail=0, min_log10_ratio=None)
    for bm in list(range(40, 400, 7)) + list(range(400, 4000, 97)):
        bk = 5 * bm // 4
        bp = 5 * bk // 4
        if bp - bm < p:
            continue
        for s in range(3, 12):
            if bk - bm < 2 * s + 2:
                continue
            B, _, _, _ = phase2_window(p, bm, bk, bp, s, Q1, Q2, Q3)
            C = closed(p, bm, bk, bp, s, Q1, Q2, Q3)
            st["windows"] += 1
            r = mp.log10(C) - mp.log10(B)
            if st["min_log10_ratio"] is None or r < st["min_log10_ratio"]:
                st["min_log10_ratio"] = r
            if C < B:
                st["fail"] += 1
                print("FAIL", p, bm, bk, bp, s, mp.nstr(B, 5), mp.nstr(C, 5))
    st["min_log10_ratio"] = mp.nstr(st["min_log10_ratio"], 5)
    print(f"p={p}: closed form (Lemma T') >= term-by-term (Lemma T): {st}", flush=True)
