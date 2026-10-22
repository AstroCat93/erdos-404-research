#!/usr/bin/env python3
"""smc_l2.py -- sequential Monte Carlo estimate of the L^2 mass C_k(p,N0) at large depth k  [HEURISTIC NUMERICS].

C_k = p^k P( sum_{n>=N0} eta_n x_n == 0 mod p^k ),  x_n = n!/p^{v(N0!)},  eta iid {-1,0,1} w.p. 1/4,1/2,1/4.
Exact carry recursion (Theorem 1 of the writeup): process the elements level by level (a level = the group of
consecutive n with the same v(x_n) = a; the next level is a' = a + J).  The carry c = (partial sum)/p^a mod p^{K-a}
survives the group iff c + y == 0 mod p^J, y = sum_{group} eta_n x_n/p^a; then c' = (c + y)/p^J.
Particle filter: each particle holds an exact carry mod p^{K-a} (Python int).  At each group a particle's survival
probability f = P(y == -c mod p^J) is computed exactly from the enumerated group law, a surviving configuration is
sampled from the conditional law, and particles are resampled in proportion to f (systematic resampling).
Z_hat = prod_groups mean(f) is an unbiased estimator of P(survive to K); C_k estimates are p^a' * running product.
Also prints the per-group defect estimate D = p^J mean(f) - 1 (exact value: Theorem 1 block factor 1 + D).
Usage: python3 smc_l2.py p N0 K P seed [report_every_levels]
Output lines: 'lvl a' C_est D_est J  (one per group end), and a final summary.
"""
import sys, random, bisect, math
from math import log

def vp(n, p):
    v = 0
    while n % p == 0:
        n //= p; v += 1
    return v

def main():
    p, N0, K, P, seed = map(int, sys.argv[1:6])
    rng = random.Random(seed)
    modK = p ** K
    # elements: level a_n = v(n!) - e0 and unit U(n) = n!/p^{v(n!)} mod p^K
    v = 0; U = 1
    for m in range(1, N0):
        t = vp(m, p); v += t; U = (U * (m // p ** t)) % modK
    e0 = None
    groups = []  # (a, [units])
    n = N0
    while True:
        t = vp(n, p); v += t; U = (U * (n // p ** t)) % modK
        if e0 is None: e0 = v
        a = v - e0
        if a >= K: break
        if groups and groups[-1][0] == a: groups[-1][1].append(U)
        else: groups.append((a, [U]))
        n += 1
    carries = [0] * P
    logZ = 0.0
    print("# p=%d N0=%d K=%d P=%d seed=%d groups=%d last element n=%d" % (p, N0, K, P, seed, len(groups), n - 1), flush=True)
    for gi, (a, units) in enumerate(groups):
        a_next = groups[gi + 1][0] if gi + 1 < len(groups) else K
        J = a_next - a
        mod = p ** (K - a); pJ = p ** J
        # enumerate group law: y mod p^(K-a) with weights (eta=0 weight 2, +-1 weight 1); total 4^g
        confs = [(0, 1)]
        for u in units:
            nc = []
            for y, w in confs:
                nc.append((y, 2 * w)); nc.append(((y + u) % mod, w)); nc.append(((y - u) % mod, w))
            confs = nc
        tot = 4 ** len(units)
        table = {}
        for y, w in confs:
            r = y % pJ
            ent = table.get(r)
            if ent is None:
                ent = [[], [], 0]; table[r] = ent
            ent[2] += w; ent[0].append(ent[2]); ent[1].append(y)
        fs = [0.0] * P; newc = [0] * P
        for i, c in enumerate(carries):
            r = (-c) % pJ
            ent = table.get(r)
            if ent is None: continue
            fs[i] = ent[2] / tot
            j = bisect.bisect_right(ent[0], rng.random() * ent[2])
            if j >= len(ent[1]): j = len(ent[1]) - 1
            cy = (c + ent[1][j]) % mod
            newc[i] = cy // pJ
        mf = sum(fs) / P
        if mf == 0.0:
            print("EXTINCT at group %d level %d" % (gi, a)); return
        logZ += log(mf)
        # systematic resampling proportional to fs
        step = sum(fs) / P; u0 = rng.random() * step
        res = []; cum = 0.0; k = 0
        for i in range(P):
            cum += fs[i]
            while k < P and u0 + k * step < cum:
                res.append(newc[i]); k += 1
        while len(res) < P: res.append(newc[max(range(P), key=lambda q: fs[q])])
        carries = res
        logC = a_next * log(p) + logZ
        print("lvl %d %.10g %.6e %d" % (a_next, math.exp(logC), pJ * mf - 1, J), flush=True)
    print("# final C_%d estimate %.10g (log %.6f)" % (K, math.exp(K * log(p) + logZ), K * log(p) + logZ))

if __name__ == '__main__':
    main()
