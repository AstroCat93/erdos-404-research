#!/usr/bin/env python3
"""ladder_vs_fixed.py -- HEURISTIC Monte Carlo (exact eps per sample, Haar-random x): fine-scale mass
eps of a composite window started at a FIXED time n0 versus started at the first C'-LADDER point
n >= n0, i.e. the first n with c_{n+d}/c_n = 2^-d p^{V_{n+d}-V_n} <= C' for all 1 <= d <= T (T the
composite length).  Window lengths: H = ceil((r-1) n), H2 = ceil((r-1)(n+H)).  The ladder start is a
G-measurable choice in the sense of Theorem B1 when the relevant valuations are visible (see report).
Prints quantiles of eps over the samples for both rules, and the mean of eps restricted to K <= KMAX.
usage: ladder_vs_fixed.py p SEED NX n0 r Cprime SEARCH KMAX
"""
import math
import random
import sys

from m4b_lib import Ctx, valuations, window_elems, eps_composite


def lengths(n, r):
    H = math.ceil((r - 1) * n)
    H2 = math.ceil((r - 1) * (n + H))
    return H, H2


def main():
    p, seed, NX, n0 = (int(a) for a in sys.argv[1:5])
    r, Cp = float(sys.argv[5]), float(sys.argv[6])
    SEARCH, KMAX = int(sys.argv[7]), int(sys.argv[8])
    C = Ctx(p, 200)
    rnd = random.Random(seed)
    res = {'fixed': [], 'ladder': []}
    skipped = {'fixed': 0, 'ladder': 0}
    noladder = 0
    for it in range(NX):
        x = rnd.randrange(C.mod)
        Hm, H2m = lengths(n0 + SEARCH, r)
        vals, V = valuations(C, x, n0 + SEARCH + Hm + H2m + 2)
        starts = {'fixed': n0}
        lad = None
        for n in range(n0, n0 + SEARCH):
            H, H2 = lengths(n, r)
            T = H + H2
            if all(V[n + d] - V[n] <= (d * math.log(2) + math.log(Cp)) / math.log(p) + 1e-12 for d in range(1, T + 1)):
                lad = n
                break
        if lad is None:
            noladder += 1
            continue
        starts['ladder'] = lad
        for rule, n in starts.items():
            H, H2 = lengths(n, r)
            N, N2 = n + H, n + H + H2
            D, K = V[N] - V[n], V[N2] - V[n]
            if K > KMAX:
                skipped[rule] += 1
                res[rule].append(float('inf'))
                continue
            y = window_elems(C, x, n, N2)
            res[rule].append(float(eps_composite(y, p, D, K)))
    print(f"RESULT p={p} n0={n0} r={r} C'={Cp}: {NX} samples, no ladder point within {SEARCH}: {noladder}")
    for rule in ('fixed', 'ladder'):
        v = sorted(res[rule])
        m = len(v)
        if m == 0:
            continue
        q = lambda f: v[min(m - 1, int(f * m))]
        fin = [t for t in v if t != float('inf')]
        print(f"ROW {rule:6s}: n={m}, K>{KMAX} (eps not computed, counted as +inf): {skipped[rule]}; "
              f"median {q(0.5):.3g}, 90% {q(0.9):.3g}, 99% {q(0.99):.3g}, max {v[-1]:.3g}; "
              f"mean over computed {sum(fin)/max(1,len(fin)):.3g}; P(eps>0.01) {sum(t>0.01 for t in v)/m:.3f}, "
              f"P(eps>0.05) {sum(t>0.05 for t in v)/m:.3f}", flush=True)


if __name__ == "__main__":
    main()
