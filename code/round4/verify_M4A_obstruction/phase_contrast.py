"""phase_contrast.py -- on the actual atom A of Theorem M, compare for each composite window l the
pointwise (supremum-type, gate-pattern-only) bound Prop D - 1 for eps with the averaged bound Prop E for
E_A[eps] (ball B = A, b = m).  Exact rationals via M4A's code/round4/M4A/bounds.py (imported read-only:
these bounds are the objects whose obstruction-compatibility is being checked).

Usage: python3 phase_contrast.py ATOMFILE LMAX

Expected if the argument respects Cor 10.20 / Prop 11.24 / Prop 11.23: the pointwise bound does NOT decay
(it grows with l), and every bit of decay comes from the averaged bound (Theorem 1 + Lemma Q 2D factor).
"""
import os
import sys
import math
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(HERE, '..', 'M4A'))
from vo_lib import vp  # noqa: E402
import bounds as M4A  # noqa: E402


def log10F(f):
    if f <= 0:
        return float('-inf')
    return math.log10(f.numerator) - math.log10(f.denominator)  # math.log10 accepts arbitrarily large ints


def main():
    kv = dict(line.split('=', 1) for line in open(sys.argv[1]).read().split() if '=' in line)
    p, n0, xA, m = int(kv['p']), int(kv['n0']), int(kv['xA']), int(kv['m'])
    LMAX = int(sys.argv[2])
    times = [n0]
    for _ in range(LMAX + 2):
        times.append(-(-27 * times[-1] // 20))
    NMAX = times[LMAX + 1]
    depth = [0] + [vp(xA + i, p) for i in range(1, NMAX + 1)]
    q = M4A.qconsts(p, 8)
    P0 = M4A.block0_table(p, 10)
    for l in range(1, LMAX + 1):
        n, N, N2 = times[l - 1], times[l], times[l + 1]
        D, K, a, MW = M4A.window_data(depth, n, N, N2)
        pd = M4A.propD_bound(depth, n, N, N2, p, q, 'K', P0) - 1
        th = min((D + 1) // 2, D - m + 1)
        if th <= 0 or K - MW >= th:
            pe, th2 = M4A.propE_bound(depth, n, N, N2, m, p, q, P0)
            pes = f"{log10F(pe):9.3f}"
        else:
            pes = "  (n/a)"
        print(f"l={l:2d} [{n},{N},{N2}) D={D:3d} K={K:3d} M_W={MW} theta={th:3d}:  log10(PropD-1) = {log10F(pd):8.3f}   "
              f"log10 PropE(E_A eps) = {pes}", flush=True)


if __name__ == '__main__':
    main()
