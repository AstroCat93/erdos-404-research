#!/usr/bin/env python3
"""thmF_e2e.py -- end-to-end exact test of Theorem F (data/round4/reports/M4D.md), finite horizon.
For Haar-random x and windows W_l = [n_l, n_{l+1}) (l = 0..L-1, lengths H0 + l*h), compute the lift counts
|Lift_l(r)| (band D_{l+1}) and the alive targets T_0 at n_0, run the optimal adaptive-theta chain
    t_L := 1,  t_l := max(1, p^{D_l} + 1 - #{r : |Lift_l(r)| >= t_{l+1}})   (l = L-1..1),
certified iff all t_l <= p^{D_l} and T_0 meets {r : |Lift_0(r)| >= t_1}.  Theorem F (with theta_l = t_l/p^{D_l},
truncated after window L-1) then asserts P(x, n_L): some path is alive at n_L.  P(x, n_L) is decided EXACTLY by
the target-set recursion of plateau_check.P_holds (independent code).  Reports certified/verified counts and
the number of non-certified samples that are nevertheless alive (the criterion is only sufficient).
Also the theta = 1 (complete-coset) chain.
usage: thmF_e2e.py p seed NX n0 H0 h L KMAX
"""
import random
import sys

import numpy as np

from m4d_lib import vp_int, window_elems
from lift_scan import lift_counts, alive_targets
from plateau_check import P_holds


def main():
    p, seed, NX, n0, H0, h, L, KMAX = (int(t) for t in sys.argv[1:9])
    rnd = random.Random(seed)
    times = [n0]
    for l in range(L + 1):
        times.append(times[-1] + H0 + l * h)
    PREC = 3 * times[-1] // (p - 1) + 60
    MOD = p ** PREC
    st = dict(n=0, cens=0, cert=0, cert_ok=0, cert_bad=0, noncert_alive=0, noncert_dead=0,
              fl_cert=0, fl_bad=0)
    while st['n'] < NX:
        x = rnd.randrange(MOD)
        vals = [0] + [vp_int((x + i) % MOD, p, PREC) for i in range(1, times[-1] + 2)]
        if max(vals[1:]) > 30:
            continue
        V = np.cumsum(vals)
        Dl = [int(V[times[l + 1]] - V[times[l]]) for l in range(L + 1)]
        if any(Dl[l] + Dl[l + 1] > KMAX for l in range(L)):
            st['cens'] += 1
            continue
        st['n'] += 1
        Ls = []
        for l in range(L):
            mK = p ** (Dl[l] + Dl[l + 1])
            Ls.append(lift_counts(window_elems(x, times[l], times[l + 1], mK), p, Dl[l], Dl[l + 1]))
        T0 = alive_targets(x, times[0], p, int(V[times[0]]), Dl[0], vals)
        # optimal adaptive chain
        tnext, ok = 1, True
        for l in range(L - 1, 0, -1):
            tl = max(1, p ** Dl[l] + 1 - int(np.sum(Ls[l] >= tnext)))
            if tl > p ** Dl[l]:
                ok = False
                break
            tnext = tl
        if ok:
            ok = bool((T0 & (Ls[0] >= tnext)).any())
        # theta = 1 chain (complete cosets): every window from 1 on has a complete class, T0 meets a complete class
        fl = bool((T0 & (Ls[0] == p ** Dl[1])).any()) and all((Ls[l] == p ** Dl[l + 1]).any() for l in range(1, L))
        alive = P_holds(x, p, [times[L]])[times[L]]
        if ok:
            st['cert'] += 1
            st['cert_ok' if alive else 'cert_bad'] += 1
        else:
            st['noncert_alive' if alive else 'noncert_dead'] += 1
        if fl:
            st['fl_cert'] += 1
            if not alive:
                st['fl_bad'] += 1
    print(f"RESULT thmF_e2e p={p} times={times} samples={st['n']} (censored {st['cens']}): "
          f"opt-theta certified={st['cert']} of which alive at n_L={st['cert_ok']}, VIOLATIONS={st['cert_bad']}; "
          f"theta=1 certified={st['fl_cert']}, VIOLATIONS={st['fl_bad']}; "
          f"not certified: alive={st['noncert_alive']}, dead={st['noncert_dead']}")


if __name__ == "__main__":
    main()
