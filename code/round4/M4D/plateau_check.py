#!/usr/bin/env python3
"""plateau_check.py -- exact test of Theorem P (deep-gate localization) of data/round4/reports/M4D.md at p=7
(certified depths t <= 6, n0 = 34):  if P(x,34) and v(x+i) <= 6 for 34 < i <= N, then P(x,N).
P(x,n) = "some path of length n is alive at n" is decided EXACTLY by the target-set recursion
   tau_{n+1} = (tau_n - e_n)/(x+n+1),  allowed iff tau_n == e_n mod p^{v(x+n+1)},
with tau_n stored mod p^{V_N - V_n} (exactly the precision needed to decide aliveness at N).
Mode 'thm': random x with a forced gate of exact depth t in [1,6] at a random i in [35, i_max]; checks
   P(x,34) => P(x,N) for N = i + extra.  Mode 'ctrl': forced gate of depth t in [2,6] at i in [3,30] (too close
   to the start for the certificates): counts cases with P(x,i-1) true and P(x,i) false (the hypothesis
   n0 >= max H_t is needed).  A cross-check of the recursion against the DFS of m4d_lib is included (small n).
usage: plateau_check.py p seed nx mode i_max extra
"""
import random
import sys

from m4d_lib import PAdic, products, alive_from_scratch, vp_int


def P_holds(x, p, n_list, prec_cap=400):
    """returns dict n -> P(x,n) for n in n_list (all n <= max(n_list)); exact."""
    N = max(n_list)
    vals = [0] + [vp_int(x + i, p, prec_cap) for i in range(1, N + 1)]
    V = [0] * (N + 1)
    for i in range(1, N + 1):
        V[i] = V[i - 1] + vals[i]
    res = {}
    # we run one recursion per requested n (precision depends on the end time)
    for n_end in sorted(set(n_list)):
        if vals[1] > 0:
            res[n_end] = False
            continue
        R = V[n_end] - V[1]
        mod = p ** R
        T = {(-pow(x + 1, -1, mod)) % mod if mod > 1 else 0}
        for n in range(1, n_end):
            s = vals[n + 1]
            R2 = V[n_end] - V[n + 1]
            mod2 = p ** R2
            unit = ((x + n + 1) // p ** s) % mod2 if mod2 > 1 else 0
            uinv = pow(unit, -1, mod2) if mod2 > 1 else 0
            ps = p ** s
            new = set()
            for tau in T:
                for e in (0, 1):
                    d = tau - e
                    if d % ps == 0:
                        new.add(((d // ps) * uinv) % mod2 if mod2 > 1 else 0)
            T = new
            if not T:
                break
        res[n_end] = bool(T)
    return res


def main():
    p, seed, nx = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    mode, imax, extra = sys.argv[4], int(sys.argv[5]), int(sys.argv[6])
    rnd = random.Random(seed)
    PREC = 200
    # cross-check of the recursion against the DFS on small n
    xc_bad = 0
    for _ in range(60):
        x = rnd.randrange(p ** 40)
        n = rnd.randint(2, 18)
        P = PAdic(p, 60)
        pi, dpi, vals = products(P, x, n)
        ref = bool(alive_from_scratch(P, pi, dpi, vals, n))
        if P_holds(x, p, [n])[n] != ref:
            xc_bad += 1
    tested = held = fails = ctrl_hits = 0
    depth_hist = {}
    for _ in range(nx):
        if mode == 'thm':
            t = rnd.randint(1, 6)
            i = rnd.randint(35, imax)
        else:
            t = rnd.randint(2, 6)
            i = rnd.randint(3, 30)
        # x == -i mod p^t exactly (depth t), other digits random
        while True:
            x = (-i + p ** t * rnd.randrange(1, p ** 30)) % p ** PREC
            if vp_int(x + i, p, PREC) == t:
                break
        Nend = i + extra
        vals = [vp_int(x + k, p, PREC) for k in range(1, Nend + 1)]
        if mode == 'thm':
            if max(vals[34:]) > 6:
                continue          # hypothesis of Theorem P not met (a depth >= 7 gate); skip
            r = P_holds(x, p, [34, Nend])
            if r[34]:
                tested += 1
                depth_hist[t] = depth_hist.get(t, 0) + 1
                if r[Nend]:
                    held += 1
                else:
                    fails += 1
        else:
            r = P_holds(x, p, [i - 1, i])
            tested += 1
            if r[i - 1] and not r[i]:
                ctrl_hits += 1
    if mode == 'thm':
        print(f"RESULT plateau_check p={p} mode=thm samples with P(x,34)={tested} (forced depths {sorted(depth_hist.items())}): "
              f"P(x,N) held={held}, FAILURES={fails}; recursion vs DFS mismatches={xc_bad}/60")
    else:
        print(f"RESULT plateau_check p={p} mode=ctrl (gate depth 2..6 at i<=30): samples={tested}, "
              f"P(x,i-1) and not P(x,i): {ctrl_hits}; recursion vs DFS mismatches={xc_bad}/60")


if __name__ == "__main__":
    main()
