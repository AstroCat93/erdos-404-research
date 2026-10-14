#!/usr/bin/env python3
"""Checks of the far-tail argument of M4C §7.2 (beyond b = 10^60).

(a) Analytic decay rate of the Lemma T' bound under the far-tail schedule
    (N_W >= b/4 - 1, N <= 9b/16 + 1, s = O(log b)):
      kappa_p = (1-1/p)|log rho|/(8 alpha)
                - (9/16)[log q1 + log q2/p + log q3/p^2 + log p/(p^2 (p-1))],
    compared with the printed kappa_p column of §7.3.
(b) Empirical continuation: the explicit schedule is continued from 10^60 up to
    10^BIGEXP with the same rules, asserting (T1), (T2), N >= p, s_k <= 3+10 ln b,
    and recording max over windows of log(Lemma T' bound)/b.
"""
import sys, math
from fractions import Fraction
import mpmath as mm
sys.path.insert(0, __import__('os').path.dirname(__file__))
from qconst_indep import q_exact
import cert

PRINTED_KAPPA = {11: 0.226, 13: 0.270, 17: 0.313, 19: 0.329, 23: 0.358, 29: 0.392, 31: 0.401, 37: 0.427,
                 41: 0.441, 43: 0.448, 47: 0.460, 53: 0.477, 59: 0.492, 61: 0.497, 67: 0.510, 71: 0.517,
                 73: 0.521, 79: 0.532, 83: 0.539, 89: 0.548, 97: 0.560}


def kappa(p):
    q1, _, _ = q_exact(p, 1); q2, _, _ = q_exact(p, 2); q3, _, _ = q_exact(p, 3)
    lq1 = mm.log(mm.mpf(q1.numerator) / q1.denominator)
    lq2 = mm.log(mm.mpf(q2.numerator) / q2.denominator)
    lq3 = mm.log(mm.mpf(q3.numerator) / q3.denominator)
    pp = mm.mpf(p)
    alpha = 1 + 1 / pp + 1 / pp ** 2 + 1 / (pp ** 2 * (pp - 1))
    lrho = lq2 - mm.log(pp)
    return (1 - 1 / pp) * (-lrho) / (8 * alpha) - mm.mpf(9) / 16 * (lq1 + lq2 / p + lq3 / p ** 2 + mm.log(pp) / (pp ** 2 * (pp - 1)))


def continue_schedule(p, BIGEXP):
    mm.mp.dps = 40
    res = cert.run(p, BIG=10 ** BIGEXP, verbose=False)
    b = res['b']; k0 = res['k0']
    # recompute per-window log T' / b for windows with b_{k-1} >= 10^60, and the s-bound
    q1, _, _ = q_exact(p, 1); q2, _, _ = q_exact(p, 2); q3, _, _ = q_exact(p, 3)
    lq1 = mm.log1p(mm.mpf(q1.numerator - q1.denominator) / q1.denominator)
    lq2 = mm.log1p(mm.mpf(q2.numerator - q2.denominator) / q2.denominator)
    lq3 = mm.log1p(mm.mpf(q3.numerator - q3.denominator) / q3.denominator)
    worst = None; sviol = 0; nw = 0
    for k in range(k0 + 1, len(b) - 1):
        bkm1 = b[k - 1]
        if bkm1 < 10 ** 60:
            continue
        s = cert.s_rule(p, bkm1, k, k0, Fraction(1, 20))
        if s > 3 + 10 * math.log(bkm1):
            sviol += 1
        lB, _ = cert.lemmaTp_log(p, s, b[k] - bkm1, b[k + 1] - bkm1, lq1, lq2, lq3)
        r = lB / bkm1
        worst = r if worst is None else max(worst, r)
        nw += 1
    return nw, worst, sviol, res


if __name__ == "__main__":
    BIGEXP = int(sys.argv[1])
    ps = [int(a) for a in sys.argv[2:]]
    mm.mp.dps = 40
    print("(a) analytic kappa_p vs printed:")
    for p in sorted(PRINTED_KAPPA):
        k = kappa(p)
        print("   p=%d kappa_analytic=%.6f printed>=%.3f  consistent(printed<=analytic): %s" % (
            p, float(k), PRINTED_KAPPA[p], PRINTED_KAPPA[p] <= float(k)))
    print("(b) continuation of the schedule to b = 10^%d:" % BIGEXP)
    for p in ps:
        nw, worst, sviol, res = continue_schedule(p, BIGEXP)
        print("   p=%d: %d windows with 10^60 <= b_(k-1) <= 10^%d; all (T1),(T2),N>=p asserted; s_k > 3+10 ln b in %d windows; "
              "max log(T' bound)/b = %s (kappa_analytic %.6f); delta_A with this longer explicit range = %s, c_p = %s" % (
                  p, nw, BIGEXP, sviol, mm.nstr(worst, 8), float(kappa(p)), mm.nstr(res['delta'], 12), mm.nstr(res['cp'], 12)), flush=True)
