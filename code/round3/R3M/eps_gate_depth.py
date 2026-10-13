#!/usr/bin/env python3
"""eps_gate_depth.py -- heuristic experiment (not a proof): growth of the fine-scale mass eps(W,W') of a composite
window [n, n+2H) (split at n+H) when a gate of depth exactly s sits at distance d from the window start,
i.e. v(x+n+d) = s, the other digits of x random.  Counts exact (numpy int64), sums of squares float64.
usage: eps_gate_depth.py p SEED NREP SMAX "n1,H1;n2,H2;..." "d1,d2,..."
"""
import random
import sys

import numpy as np

PREC = 160


def main():
    p, seed, NREP, SMAX = (int(a) for a in sys.argv[1:5])
    configs = [tuple(int(t) for t in c.split(',')) for c in sys.argv[5].split(';')]
    ds = [int(t) for t in sys.argv[6].split(',')]
    MOD = p ** PREC
    rnd = random.Random(seed)

    def vp(a):
        a %= MOD
        if a == 0:
            return PREC
        k = 0
        while a % p == 0:
            a //= p
            k += 1
        return k

    def eps_of(x, n, N, N2):
        V = [0]
        for i in range(1, N2 + 1):
            V.append(V[-1] + vp(x + i))
        D, K = V[N] - V[n], V[N2] - V[n]
        if K > 14:
            return None
        mod = p ** K
        dist = np.zeros(mod, dtype=np.int64)
        dist[0] = 1
        y = 1
        for k in range(N2 - n):
            dist = dist + np.roll(dist, int(y % mod))
            y = y * (x + n + k + 1) % MOD

        def cp(j):
            f = dist.reshape(-1, p ** j).sum(axis=0).astype(np.float64)
            return float(np.dot(f, f))
        return (p ** K * cp(K) - p ** D * cp(D)) / 4.0 ** (N2 - n)

    for (n, H) in configs:
        N, N2 = n + H, n + 2 * H
        for d in ds:
            row = []
            for s in range(1, SMAX + 1):
                vals = []
                for _ in range(NREP):
                    u = rnd.randrange(1, p ** 60)
                    while u % p == 0:
                        u = rnd.randrange(1, p ** 60)
                    x = (-(n + d) + p ** s * u) % MOD
                    r = eps_of(x, n, N, N2)
                    if r is not None:
                        vals.append(r)
                if vals:
                    vals.sort()
                    row.append(f"s={s}: median {vals[len(vals)//2]:.3g} mean {sum(vals)/len(vals):.3g} (n={len(vals)})")
            print(f"TABLE p={p} window [{n},{N2}) split {N}, gate at distance d={d}: " + "; ".join(row), flush=True)


if __name__ == "__main__":
    main()
