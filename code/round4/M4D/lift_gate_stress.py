#!/usr/bin/env python3
"""lift_gate_stress.py -- heuristic stress test (not a proof) of the lifting criterion of Theorem F at a forced
gate of exact depth s inside the middle window of three windows W_0=[n0,n1), W_1=[n1,n2), W_2=[n2,n3).
The gate sits at index n1 + d, d in {1 (start), H1//2 (middle), H1-1 (end)} (mode).
For Haar-random x conditioned on v(x + n1 + d) = s computes:
  FL_0 : W_0 has a complete class modulo p^{D_0+D_1}   (theta = 1 step into the band containing the gate)
  FL_1 : W_1 has a complete class modulo p^{D_1+D_2}
  opt  : the optimal adaptive-theta chain over (W_0, W_1) with t_2 = 1 (Theorem F, two windows)
  cnt  : the counting bound of Prop F2(a): 2^{H_0} >= p^{D_1} (necessary for any theta_1 >= ... at l=0)
usage: lift_gate_stress.py p seed NX n0 H s mode KMAX       (all three windows have length H)
"""
import random
import sys

import numpy as np

from m4d_lib import vp_int, window_elems
from lift_scan import lift_counts


def main():
    p, seed, NX, n0, H, s = (int(t) for t in sys.argv[1:7])
    mode, KMAX = sys.argv[7], int(sys.argv[8])
    rnd = random.Random(seed)
    n1, n2, n3, n4 = n0 + H, n0 + 2 * H, n0 + 3 * H, n0 + 4 * H
    d = {'start': 1, 'mid': H // 2, 'end': H - 1}[mode]
    i = n1 + d
    PREC = 3 * n4 // (p - 1) + 80
    MOD = p ** PREC
    st = dict(n=0, cens=0, fl0=0, fl1=0, opt=0, cnt=0, both=0)
    tries = 0
    while st['n'] < NX and tries < 50 * NX:
        tries += 1
        x = (-i + p ** s * rnd.randrange(1, p ** 40)) % MOD
        if vp_int(x + i, p, PREC) != s:
            continue
        vals = [0] + [vp_int((x + k) % MOD, p, PREC) for k in range(1, n4 + 2)]
        V = np.cumsum(vals)
        D = [int(V[b] - V[a]) for a, b in ((n0, n1), (n1, n2), (n2, n3), (n3, n4))]
        if D[0] + D[1] > KMAX or D[1] + D[2] > KMAX:
            st['cens'] += 1
            continue
        st['n'] += 1
        L0 = lift_counts(window_elems(x, n0, n1, p ** (D[0] + D[1])), p, D[0], D[1])
        L1 = lift_counts(window_elems(x, n1, n2, p ** (D[1] + D[2])), p, D[1], D[2])
        fl0 = bool((L0 == p ** D[1]).any())
        fl1 = bool((L1 == p ** D[2]).any())
        st['fl0'] += fl0
        st['fl1'] += fl1
        st['both'] += fl0 and fl1
        st['cnt'] += 2 ** H >= p ** D[1]
        t1 = max(1, p ** D[1] + 1 - int(np.sum(L1 >= 1)))      # t_2 = 1
        ok = t1 <= p ** D[1] and bool((L0 >= t1).any())          # some class of W_0 lifts to >= t1 targets
        st['opt'] += ok
    n = max(st['n'], 1)
    print(f"RESULT gate_stress p={p} windows=[{n0},{n1},{n2},{n3}) H={H} gate depth s={s} at n1+{d} ({mode}): "
          f"samples={st['n']} (censored {st['cens']}): P(FL_0)={st['fl0'] / n:.3f} P(FL_1)={st['fl1'] / n:.3f} "
          f"P(both)={st['both'] / n:.3f} P(opt-theta chain over W_0,W_1)={st['opt'] / n:.3f} "
          f"P(counting 2^H >= p^D1)={st['cnt'] / n:.3f}")


if __name__ == "__main__":
    main()
