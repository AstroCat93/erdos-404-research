"""corM_phase_contrast.py -- Corollary M' version of phase_contrast.py: on the actual atom A_p of M4A's Corollary M'
(p = 11, 13, 17, 19, 23), compare for each composite window l the pointwise, gate-pattern-only bound
Prop D - 1 (a deterministic L^2 bound: the kind constrained by Theorem 3.10 / Prop 11.23 and by Cor 10.20 /
Prop 11.24) with the averaged bound Prop E for E_A[eps] (Theorem 1 on the ball B = A, b = m).

Exact rationals via M4A's code/round4/M4A/bounds.py, imported read-only: these bounds are the objects whose
obstruction-compatibility is checked.  Constants exactly as in M4A's fe_lib.Consts: enumeration with S = 8,
S0 = 12 for p <= 13; residue DP with S = S0 = 4 for p > 13 (validated in corM_consts.log by this track's own DP).

Usage: python3 corM_phase_contrast.py ATOMFILE LMAX
Also prints, per window, the maximal gate depth M_W and the number of gates of depth >= 2 and >= 3.
"""
import os
import sys
import math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(HERE, '..', 'M4A'))
from vo_lib import vp  # noqa: E402
import bounds as M4A  # noqa: E402


def log10F(f):
    if f <= 0:
        return float('-inf')
    return math.log10(f.numerator) - math.log10(f.denominator)


def main():
    kv = dict(line.split('=', 1) for line in open(sys.argv[1]).read().split() if '=' in line)
    p, n0, xA, m = int(kv['p']), int(kv['n0']), int(kv['xA']), int(kv['m'])
    LMAX = int(sys.argv[2])
    times = [n0]
    for _ in range(LMAX + 2):
        times.append(-(-27 * times[-1] // 20))
    NMAX = times[LMAX + 1]
    depth = [0] + [vp(xA + i, p) for i in range(1, NMAX + 1)]
    if p <= 13:
        q, P0 = M4A.qconsts(p, 8), M4A.block0_table(p, 12)
    else:
        q, P0 = M4A.qconsts_dp(p, 4), M4A.block0_table_dp(p, 4)
    print(f"p={p} m={m}: q_1={float(q[1]):.9f} q_2={float(q[2]):.9f}")
    W0 = M4A.propD_bound(depth, times[0], times[1], times[1], p, q, 'K', P0) - 1
    print(f"W_0 [{times[0]},{times[1]}): chi^2_0 <= Prop D - 1 = {float(W0):.6g}")
    for l in range(1, LMAX + 1):
        n, N, N2 = times[l - 1], times[l], times[l + 1]
        D, K, a, MW = M4A.window_data(depth, n, N, N2)
        g2 = sum(1 for i in range(n + 1, N2 + 1) if depth[i] >= 2)
        g3 = sum(1 for i in range(n + 1, N2 + 1) if depth[i] >= 3)
        pd = M4A.propD_bound(depth, n, N, N2, p, q, 'K', P0) - 1
        th = min((D + 1) // 2, D - m + 1)
        if th <= 0 or K - MW >= th:
            pe, th2 = M4A.propE_bound(depth, n, N, N2, m, p, q, P0)
            pes = f"{log10F(pe):9.3f}"
        else:
            pes = "  (n/a)"
        print(f"l={l:2d} [{n},{N},{N2}) D={D:3d} K={K:3d} M_W={MW} #depth>=2: {g2} #depth>=3: {g3} theta={th:4d}:  "
              f"log10(PropD-1) = {log10F(pd):8.3f}   log10 PropE(E_A eps) = {pes}", flush=True)


if __name__ == '__main__':
    main()
