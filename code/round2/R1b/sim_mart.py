#!/usr/bin/env python3
"""Monte Carlo illustration (NOT part of the proof): follow the window martingale
   M_k = 2^{-W_{n_k}} * sum_{e alive at n_k, lambda_e <= L} rho_k(e)
along the windows n_{k+1} = min(max(next record, n_k + 2L + 2), floor(5 n_k / 4)) for random x,
and report (i) the sample mean of M_k at each window index (should stay ~constant: martingale),
(ii) the fraction of x whose lambda<=L population is still alive, (iii) the full population.
Usage: sim_mart.py seed samples n0 L nmax P
"""
import random, sys
from collections import defaultdict

def v2(a):
    return (a & -a).bit_length() - 1 if a else 10**9

def rho(x, n, lam, tau):
    if lam == 0:
        return 1.0
    mod = 1 << lam
    terms = []; prod = 1
    for j in range(n, n + 2 * lam):
        terms.append(prod % mod); prod = prod * (x + j + 1) % mod
    cnt = 0
    for f in range(1 << len(terms)):
        s = sum(terms[i] for i in range(len(terms)) if (f >> i) & 1)
        cnt += ((s - tau) % mod == 0)
    return cnt * (1 << lam) / (1 << len(terms))

def run(x, n0, L, nmax, P):
    # population: list of (tau mod 2^prec, Sprime mod 2^P); start: DFS to n0
    pop = [(0, 0)]  # tau_0 = 0, S' = 0 at time 0
    prec = P
    pi, dpi = 1, 0  # pi_j, pi'_j at current j
    j = 0
    V = 0
    rec_mu = max(v2(x + i) for i in range(1, n0 + 1))
    out = []
    windows = [n0]
    n = n0
    while True:
        Nn = n + 2 * L + 2
        # next record after n
        t = n + 1
        while v2(x + t) <= rec_mu and t < 4 * n:
            t += 1
        nxt = min(max(t, n + 2 * L + 2), (5 * n) // 4)
        windows.append(nxt)
        n = nxt
        if n > nmax:
            break
        rec_mu = max(rec_mu, max(v2(x + i) for i in range(windows[-2] + 1, n + 1)))
    # advance population step by step, recording M at window times
    wset = set(windows)
    Mlist = []
    for j in range(0, windows[-2] + 1):
        if j in wset and j >= n0:
            W = j - V
            tot = 0.0; zl = 0
            for tau, sp in pop:
                lam = v2(sp)
                if lam <= L:
                    zl += 1
                    tot += rho(x, j, lam, tau)
            Mlist.append((j, W, tot * 2.0 ** (-W), zl, len(pop)))
        d = v2(x + j + 1); u = (x + j + 1) >> d
        nprec = prec - d
        inv = pow(u, -1, 1 << nprec)
        new = []
        for tau, sp in pop:
            for e in ((1,) if j == 0 else (0, 1)):
                tt = (tau - e) % (1 << prec)
                if d and (tt & ((1 << d) - 1)):
                    continue
                new.append((((tt >> d) * inv) % (1 << nprec), (sp + e * dpi) % (1 << P)))
        pop = new
        prec = nprec
        # update pi_j -> pi_{j+1}
        dpi_new = (dpi * (x + j + 1) + pi) % (1 << P)
        pi = pi * (x + j + 1) % (1 << P)
        dpi = dpi_new
        V += d
    return Mlist

if __name__ == "__main__":
    seed, S, n0, L, nmax, P = (int(a) for a in sys.argv[1:7])
    rnd = random.Random(seed)
    agg = defaultdict(list)
    for s in range(S):
        x = rnd.getrandbits(P) & ~1
        Ml = run(x, n0, L, nmax, P)
        for k, (j, W, M, zl, z) in enumerate(Ml):
            agg[k].append((M, zl > 0, z > 0, W, j))
    for k in sorted(agg):
        rows = agg[k]
        meanM = sum(r[0] for r in rows) / len(rows)
        alive_l = sum(r[1] for r in rows) / len(rows)
        alive = sum(r[2] for r in rows) / len(rows)
        meanW = sum(r[3] for r in rows) / len(rows)
        meanj = sum(r[4] for r in rows) / len(rows)
        print(f"k={k:3d} mean n_k={meanj:8.1f} mean W={meanW:6.2f} mean M_k={meanM:9.4f} "
              f"P(pop lam<=L alive)={alive_l:.4f} P(any alive)={alive:.4f} samples={len(rows)}")
