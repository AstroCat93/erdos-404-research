#!/usr/bin/env python3
"""Exploration (heuristic, not part of any proof): alive populations at p=2 with slopes.

For an even 2-adic x (an integer mod 2^P with P large) and time n, a path e (e_0 = 1) is alive
at n iff 2^{V_n(x)} | S_e(x) = sum_{j<n} e_j pi_j(x).  We run a BFS over j, keeping for each
alive path its target tau_j = -S_e(x)/pi_j(x) (mod 2^{prec}) and S_e'(x) mod 2^P, and record at
the requested times the multiset of slopes lambda_e = v(S_e'(x)).

usage: explore_pop.py seed samples nmax residue modulus [cap]
  x is drawn uniformly from residue + modulus*Z_2 (P = 4*nmax+64 bits).
"""
import random, sys
from collections import Counter

def v2(a):
    return (a & -a).bit_length() - 1 if a else 10**9

def run(x, nmax, P, cap):
    MOD = 1 << P
    pop = [(1 % MOD * 0, 0)]  # placeholder replaced below
    # state at time j: list of (tau mod 2^prec, Sprime mod 2^P); start j=0 with S=0 (empty), tau=0
    pop = [(0, 0)]
    prec = P
    pi, dpi = 1, 0
    V = 0
    out = {}
    for j in range(nmax):
        # step j -> j+1 : choose e_j, then divide by (x+j+1)
        d = v2(x + j + 1); u = (x + j + 1) >> d
        nprec = prec - d
        inv = pow(u, -1, 1 << nprec)
        new = []
        for tau, sp in pop:
            for e in ((1,) if j == 0 else (0, 1)):
                t = (tau - e) % (1 << prec)
                if d and (t & ((1 << d) - 1)):
                    continue
                new.append((((t >> d) * inv) % (1 << nprec), (sp + e * dpi) % MOD))
        if len(new) > cap:
            return out, True
        pop = new; prec = nprec
        dpi = (dpi * (x + j + 1) + pi) % MOD
        pi = pi * (x + j + 1) % MOD
        V += d
        n = j + 1
        out[n] = (V, [v2(sp) for _, sp in pop])
    return out, False

if __name__ == "__main__":
    seed, S, nmax, res, modu = (int(a) for a in sys.argv[1:6])
    cap = int(sys.argv[6]) if len(sys.argv) > 6 else 200000
    P = 4 * nmax + 64
    rnd = random.Random(seed)
    checkpoints = [n for n in (10, 20, 40, 60, 80, 120, 160, 200, 300, 400) if n <= nmax]
    stats = {n: [0, 0, Counter(), 0] for n in checkpoints}  # nonempty, total, slope hist, maxslope
    capped = 0
    for s in range(S):
        x = res + modu * rnd.getrandbits(P)
        x %= (1 << P)
        out, cp = run(x, nmax, P, cap)
        capped += cp
        for n in checkpoints:
            if n not in out:
                continue
            V, sl = out[n]
            if sl:
                stats[n][0] += 1
                stats[n][1] += len(sl)
                for l in sl:
                    stats[n][2][min(l, 999)] += 1
                stats[n][3] = max(stats[n][3], max(sl))
    print(f"# class {res} mod {modu}, samples {S}, nmax {nmax}, capped {capped}")
    for n in checkpoints:
        ne, tot, h, mx = stats[n]
        print(f"n={n:4d} P(nonempty)={ne/S:.4f} E[Z]={tot/S:.3f} maxslope={mx} hist={sorted(h.items())[:25]}")
