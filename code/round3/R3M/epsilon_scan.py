#!/usr/bin/env python3
"""epsilon_scan.py -- heuristic scan (not a proof) of the hypothesis of Theorem R3M-C3:
the high-band L^2 Fourier mass of composite windows,
    eps_l(x) = p^K Coll_K - p^D Coll_D,   composite window [n_{l-1}, n_{l+1}),
    D = V_{n_l} - V_{n_{l-1}},  K = V_{n_{l+1}} - V_{n_{l-1}},  Coll_j = sum_r nu(r)^2 (nu = subset-sum law mod p^j
    of the elements pi_j(x)/pi_{n_{l-1}}(x), j in [n_{l-1}, n_{l+1})),
for Haar-random x and deterministic times n_{l+1} = ceil(r * n_l).  Also records whether the linear-regime
condition K <= m_{l-1} - M_{n_{l+1}} holds.  Counts exact (numpy int64, 2^H < 2^62); sums of squares in float64.
usage: epsilon_scan.py p SEED NX n0 ratio KMAX
"""
import math
import random
import sys

import numpy as np

PREC = 200


def vp(a, p):
    if a == 0:
        return PREC
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def coll_profile(elems, p, K):
    """Return [4^H * sum_r nu_j(r)^2 for j = 0..K] for the subset-sum law of elems (counts exact in int64,
    the sums of squares in float64: relative error ~1e-15, adequate for this heuristic scan)."""
    mod = p ** K
    dist = np.zeros(mod, dtype=np.int64)
    dist[0] = 1
    for y in elems:
        dist = dist + np.roll(dist, int(y % mod))
    out = []
    for j in range(K + 1):
        md = p ** j
        folded = dist.reshape(-1, md).sum(axis=0).astype(np.float64)
        out.append(float(np.dot(folded, folded)))
    return out


def main():
    p, seed, NX = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    n0, ratio, KMAX = int(sys.argv[4]), float(sys.argv[5]), int(sys.argv[6])
    times = [n0]
    while len(times) < 40:
        times.append(math.ceil(ratio * times[-1]))
    MOD = p ** PREC
    rnd = random.Random(seed)
    stats = {}
    for it in range(NX):
        x = rnd.randrange(MOD)
        Vcache = {}
        Mcache = {}
        v = 0
        mx = 0
        for i in range(1, times[-1] + 1):
            d = vp((x + i) % MOD, p)
            v += d
            mx = max(mx, d)
            Vcache[i] = v
            Mcache[i] = mx
        for l in range(1, len(times) - 1):
            a, b, c = times[l - 1], times[l], times[l + 1]
            D = Vcache[b] - Vcache[a]
            K = Vcache[c] - Vcache[a]
            if K > KMAX:
                break
            lin = K <= Vcache[a] - Mcache[c]
            elems = []
            y = 1
            for k in range(c - a):
                elems.append(y)
                y = y * (x + a + k + 1) % p ** K
            prof = coll_profile(elems, p, K)
            T2 = 4 ** (c - a)
            eps = (p ** K * prof[K] - p ** D * prof[D]) / T2
            dmax = max(vp((x + i) % MOD, p) for i in range(a + 1, c + 1))
            stats.setdefault(l, []).append((eps, lin, a, c, dmax))
    print(f"# epsilon_scan p={p} seed={seed} NX={NX} times={times[:12]}... KMAX={KMAX}")
    print("# l  window          samples  frac_lin  median_eps  q90_eps  q99_eps  max_eps  (eps over samples with the linear condition)")
    for l in sorted(stats):
        rows = stats[l]
        e = sorted(r[0] for r in rows if r[1])
        if not e:
            continue
        q = lambda f: e[min(len(e) - 1, int(f * len(e)))]
        print(f"TABLE {l:2d} [{rows[0][2]},{rows[0][3]})  {len(rows):6d}  {len(e)/len(rows):.3f}  {q(0.5):.4e}  {q(0.9):.4e}  "
              f"{q(0.99):.4e}  {e[-1]:.4e}")
        bydep = {}
        for r in rows:
            if r[1]:
                bydep.setdefault(r[4], []).append(r[0])
        print("TABLE    by max gate depth d in the window: " + "; ".join(
            f"d={d}: n={len(v)} median={sorted(v)[len(v)//2]:.3e} max={max(v):.3e}" for d, v in sorted(bydep.items())))


if __name__ == "__main__":
    main()
