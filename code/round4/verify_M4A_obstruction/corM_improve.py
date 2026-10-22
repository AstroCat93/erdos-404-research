"""corM_improve.py -- observation (not part of the verdict): the phase-1 thresholds of M4A's Corollary M' discard the
mod-p level of the first half of each composite window, which is Prop 11.12's mechanism and is large at p = 11, 17.

eps_l = p^K Coll_K - p^D Coll_D, and p^D Coll_D >= p Coll_1 (the L^2 mass p^j Coll_j is nondecreasing in j: the
frequencies mod p^j are a subset of those mod p^(j+1), all terms |mu^|^2 >= 0).  Mod p^D the composite sum equals the
first-half sum (second-half elements are 0 mod p^D).  So on all of A
      eps_l <= (Prop D bound for p^K Coll_K) - p Coll_1(first half),
and p Coll_1(first half) is constant on A (it depends on x mod p).  M4A uses 1 in place of p Coll_1.
Prop D values: M4A's own interval evaluator (code/round4/M4A/fe_lib.py, read-only), exactly as in fe_verify.py.
Mod-p collision: this track's exact DP (integer weights).  delta_A is taken from M4A's certificate (unchanged).

Usage: python3 corM_improve.py ATOMFILE L1 DELTA_A_UPPER
"""
import os
import sys
from fractions import Fraction

import numpy as np
from mpmath import iv, mpf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(HERE, '..', 'M4A'))
from vo_lib import vp  # noqa: E402
from fe_lib import Consts, blocklevel, up  # noqa: E402

iv.prec = 200


def coll1(xA, n, N, p):
    """exact p * P(sum_{c<N-n} delta_c y_c == 0 mod p), y_c = (xA+n+1)...(xA+n+c)."""
    cnt = np.zeros(p, dtype=object)
    cnt[0] = 1
    y = 1
    for c in range(N - n):
        a = y % p
        cnt = 4 * cnt if a == 0 else 2 * cnt + np.roll(cnt, a) + np.roll(cnt, -a)
        y = y * (xA + n + c + 1) % p
    return p * Fraction(int(cnt[0]), 4 ** (N - n))


def main():
    kv = dict(line.split('=', 1) for line in open(sys.argv[1]).read().split() if '=' in line)
    p, n0, xA, m = int(kv['p']), int(kv['n0']), int(kv['xA']), int(kv['m'])
    L1 = int(sys.argv[2])
    delta = iv.mpf(sys.argv[3])
    C = Consts(p)
    times = [n0]
    for _ in range(L1 + 2):
        times.append(-(-27 * times[-1] // 20))
    NMAX = times[L1 + 1]
    depth = [0] + [vp(xA + i, p) for i in range(1, NMAX + 1)]
    V = [0] * (NMAX + 1)
    for i in range(1, NMAX + 1):
        V[i] = V[i - 1] + depth[i]
    D0 = V[times[1]] - V[times[0]]
    chi = up(blocklevel(C, depth, V, times[0], times[1], D0, 0, max(depth[times[0] + 1:times[1] + 1]))) - 1
    logPi_old = iv.log(1 + iv.mpf(chi))
    logPi_new = iv.log(1 + iv.mpf(chi))
    print(f"p={p} m={m}: chi^2_0 <= {float(chi):.6g}")
    for l in range(1, L1 + 1):
        n, N, N2 = times[l - 1], times[l], times[l + 1]
        K = V[N2] - V[n]
        bD = up(blocklevel(C, depth, V, n, N2, K, 0, max(depth[n + 1:N2 + 1])))
        c1 = coll1(xA, n, N, p)
        old = max(bD - 1, mpf(0))                                         # M4A's eps_bar (as in fe_verify.py)
        new = max(up(iv.mpf(bD) - iv.mpf(c1.numerator) / c1.denominator), mpf(0))   # outward-rounded upper end
        logPi_old += iv.log(1 + iv.mpf(old))
        logPi_new += iv.log(1 + iv.mpf(new))
        print(f"  l={l} [{n},{N},{N2}): Prop D - 1 = {float(old):.6g};  p Coll_1(first half) = {float(c1):.6g};"
              f"  improved eps_bar = {float(new):.6g}")
    tail = iv.log(iv.mpf(23843) / 10000)
    for name, lp in (("M4A", logPi_old), ("improved", logPi_new)):
        Pi = iv.exp(lp + tail)
        val = Pi * delta
        lb = (1 - iv.sqrt(val)) ** 2 / Pi
        print(f"  {name:8s}: Pi_A <= {float(up(Pi)):.6g};  mu(K_p cap A)/mu(A) >= {float(mpf(lb.a)):.6g}")


if __name__ == '__main__':
    main()
