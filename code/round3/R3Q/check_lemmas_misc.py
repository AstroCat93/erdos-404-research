#!/usr/bin/env python3
"""Exact random tests of the elementary inequalities of the R3Q report (Lemmas 2 and 6).

 (2b) V_{n+i} - V_n >= i - s(i)
 (2c) Z_n <= 2^{ceil(n/2)-1} (x even, n >= 2);  Z_n <= 2^{n/2-2} (x in 8Z_2, n even >= 6)
 (2d) W_{n0} - W_{n0+N_K(z)} >= s(z mod 2^K) - 1,   z = x + n0
 (2e) V_n - M_n >= beta(n) = n - s(n) - floor(log2 n);  beta nondecreasing (checked for n <= 10^5)
 (2f) v(pi_i'(x)) >= beta(i)
 (2g) v(pi_i^[2](x)) >= beta2(i) = i - s(i) - 2 floor(log2 i)
 (6a) rho_n^{(lam)}(s) > 0  =>  rho >= 1/(4 lam)   (lam >= 1), and rho <= 2^lam
usage: check_lemmas_misc.py seed samples
"""
import random, sys
from fractions import Fraction

def v2(a): return (a & -a).bit_length() - 1 if a else 10**9
def s2(n): return bin(n).count("1")
def flog2(n): return n.bit_length() - 1
def beta(n): return n - s2(n) - flog2(n)
def beta2(n): return n - s2(n) - 2 * flog2(n)

def main():
    seed, S = int(sys.argv[1]), int(sys.argv[2])
    rnd = random.Random(seed)
    P = 700; MOD = 1 << P
    fails = {k: 0 for k in ("2b", "2c", "2c8", "2d", "2e", "2f", "2g", "6a", "6amax")}
    counts = {k: 0 for k in fails}
    for n in range(1, 100001):
        if beta(n + 1) < beta(n):
            fails["2e"] += 1
    for t in range(S):
        x = (rnd.getrandbits(P) << 1) % MOD
        if t % 3 == 0:
            x = (rnd.getrandbits(P) << 3) % MOD          # 8Z_2
        nmax = 120
        vals = [None] + [v2(x + i) for i in range(1, 2 * nmax + 2)]
        V = [0]
        for i in range(1, 2 * nmax + 1):
            V.append(V[-1] + vals[i])
        # (2b), (2e)
        for n in range(1, nmax):
            Mn = max(vals[1:n + 1])
            counts["2e"] += 1
            if V[n] - Mn < beta(n): fails["2e"] += 1
            for i in range(0, nmax):
                counts["2b"] += 1
                if V[n + i] - V[n] < i - s2(i): fails["2b"] += 1
        # (2f), (2g): pi_i', pi_i^[2] mod 2^P
        p0, p1, p2 = 1, 0, 0
        for i in range(1, nmax + 1):
            a = x + i
            p2 = (p2 * a + p1) % MOD
            p1 = (p1 * a + p0) % MOD
            p0 = p0 * a % MOD
            counts["2f"] += 1; counts["2g"] += 1
            if v2(p1) < beta(i): fails["2f"] += 1
            if i >= 2 and v2(p2) < beta2(i): fails["2g"] += 1
        # (2d)
        for _ in range(5):
            n0 = rnd.randrange(0, 60) * 2
            K = rnd.randrange(1, 7)
            z = x + n0
            NK = next(tt for tt in range(1, 2 ** K + 1) if (z + tt) % (2 ** K) == 0)
            W = lambda n: n - V[n]
            if n0 + NK < len(V):
                counts["2d"] += 1
                if W(n0) - W(n0 + NK) < s2(z % (2 ** K)) - 1: fails["2d"] += 1
        # (6a)
        for _ in range(3):
            n = rnd.randrange(4, 80); lam = rnd.randrange(1, 12)
            mod = 1 << lam
            dist = {0: 1}; tot = 1; c = 1; i = 0
            while v2(c) < lam:
                cm = c % mod; nd = {}
                for tt, k in dist.items():
                    nd[tt] = nd.get(tt, 0) + k
                    u = (tt + cm) % mod
                    nd[u] = nd.get(u, 0) + k
                dist = nd; tot *= 2; i += 1; c *= (x + n + i)
            for sres, k in dist.items():
                r = Fraction(k * mod, tot)
                counts["6a"] += 1; counts["6amax"] += 1
                if r > 0 and r < Fraction(1, 4 * lam): fails["6a"] += 1
                if r > mod: fails["6amax"] += 1
    # (2c): Z_n bounds by BFS
    for t in range(max(1, S // 4)):
        x = (rnd.getrandbits(P) << 1) % MOD
        if t % 2:
            x = (rnd.getrandbits(P) << 3) % MOD
        pop = [(0, P)]
        for j in range(60):
            d = v2(x + j + 1); u = (x + j + 1) >> d
            new = []
            for tau, prec in pop:
                for e in ((1,) if j == 0 else (0, 1)):
                    tt = (tau - e) % (1 << prec)
                    if d and (tt & ((1 << d) - 1)): continue
                    npr = prec - d
                    new.append((((tt >> d) * pow(u, -1, 1 << npr)) % (1 << npr), npr))
            pop = new
            n = j + 1
            if n >= 2:
                counts["2c"] += 1
                if len(pop) > 2 ** ((n + 1) // 2 - 1): fails["2c"] += 1
            if x % 8 == 0 and n >= 6 and n % 2 == 0:
                counts["2c8"] += 1
                if len(pop) > 2 ** (n // 2 - 2): fails["2c8"] += 1
    print("checks:", counts)
    print("failures:", fails)

if __name__ == "__main__":
    main()
