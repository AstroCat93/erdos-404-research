#!/usr/bin/env python3
"""winpair_stats.py -- heuristic (Monte Carlo) statistics of a single Haar-random window pair.

For z Haar in Z_p and lengths L, L' the composite window has elements y_c = (z+1)...(z+c), 0 <= c < L+L'.
D = V_L(z), K = V_{L+L'}(z).  nu = law of a uniformly random subset sum mod p^K.  The band is the set of
frequencies zeta in Z/p^K with zeta != 0 mod p^{D'} (D' = K - D), i.e. of order in (p^D, p^K].
  eps = sum_band |nu^(zeta)|^2   (the L^2 band mass of R3M Prop C2)
  B   = sum_band |nu^(zeta)|     (the L^1 band mass used in the deterministic recursion, report Lemma D1)
Counts are exact (int64 via numpy roll-add); Fourier transforms are float64 FFTs (heuristic only).
Samples with K > KMAX are reported as 'skipped' (they contain a deep gate); they are NOT dropped silently.
usage: winpair_stats.py p SEED NZ L L' KMAX
"""
import random
import sys

import numpy as np


def vp(a, p, cap=60):
    if a == 0:
        return cap
    k = 0
    while a % p == 0 and k < cap:
        a //= p
        k += 1
    return k


def law(elems, mod):
    dist = np.zeros(mod, dtype=np.int64)
    dist[0] = 1
    for y in elems:
        dist = dist + np.roll(dist, int(y % mod))
    return dist


def main():
    p, seed, NZ, L, L2, KMAX = (int(a) for a in sys.argv[1:7])
    rnd = random.Random(seed)
    PREC = 60
    MOD = p ** PREC
    res = []
    skipped = 0
    for _ in range(NZ):
        z = rnd.randrange(MOD)
        vals = [vp((z + i) % MOD, p) for i in range(1, L + L2 + 1)]
        D = sum(vals[:L])
        K = sum(vals)
        if K > KMAX:
            skipped += 1
            continue
        if K == D:
            res.append((0.0, 0.0, D, K, max(vals)))
            continue
        mod = p ** K
        elems = []
        y = 1
        for c in range(L + L2):
            elems.append(y)
            y = y * (z + c + 1) % mod
        dist = law(elems, mod).astype(np.float64) / 2.0 ** (L + L2)
        F = np.fft.fft(dist)
        idx = np.arange(mod)
        band = (idx % p ** (K - D)) != 0
        a = np.abs(F[band])
        res.append((float(np.sum(a * a)), float(np.sum(a)), D, K, max(vals)))
    print(f"# winpair_stats p={p} seed={seed} NZ={NZ} L={L} L'={L2} KMAX={KMAX} skipped(K>KMAX)={skipped}")
    if not res:
        return
    e = sorted(r[0] for r in res)
    b = sorted(r[1] for r in res)
    q = lambda arr, f: arr[min(len(arr) - 1, int(f * len(arr)))]
    print(f"RESULT eps: mean={np.mean(e):.4e} median={q(e,.5):.4e} q90={q(e,.9):.4e} q99={q(e,.99):.4e} max={e[-1]:.4e}")
    print(f"RESULT B  : mean={np.mean(b):.4e} median={q(b,.5):.4e} q90={q(b,.9):.4e} q99={q(b,.99):.4e} max={b[-1]:.4e}")
    for thr in (1e-1, 1e-2, 1e-3):
        print(f"RESULT P(B>{thr:g}) = {sum(1 for x in b if x > thr)/NZ:.4f}   P(eps>{thr:g}) = {sum(1 for x in e if x > thr)/NZ:.4f}")
    bydep = {}
    for r in res:
        bydep.setdefault(r[4], []).append(r)
    for d in sorted(bydep):
        rr = bydep[d]
        print(f"RESULT maxdepth={d}: n={len(rr)} median eps={sorted(x[0] for x in rr)[len(rr)//2]:.3e} "
              f"median B={sorted(x[1] for x in rr)[len(rr)//2]:.3e} max B={max(x[1] for x in rr):.3e}")


if __name__ == "__main__":
    main()
