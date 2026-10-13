#!/usr/bin/env python3
"""Exact random tests of Lemmas 1, 4, 6, 7 of data/round3/reports/R3Q.md (restarted track).
 L1b  V_n <= n + M_n - 2 (x even, n>=2)          L1c V_n - M_n >= beta(n); V_n - M_n and beta nondecreasing
 L1d  V_{n+i} - V_n >= i - s(i)                    L1e W_{n0+N_K(z)} - W_{n0} <= 1 - s(z mod 2^K), z = x+n0
 L4   Z_n <= 2^{ceil(n/2)-1} (x even, n >= 2)
 L6   rho_n^{(lam)}(s) <= 2^{min(lam-1, floor((lam+Mt)/2)-1)}, Mt = max_{1<=i<=2lam} min(v(x+n+i), lam); and if a path alive at n with
      slope lam has a descendant alive at n + 2lam then rho_n(state) >= 2^{-floor(log2(2lam))}
 L7   x = 2 mod 4, j = v(x+2), e alive at n with V_n >= 3j+1  =>  v(S_e') <= 2j or v(S_e^[2]) <= j
usage: test_elementary.py seed samples nmax"""
import sys, random, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
def main():
    seed, S, nmax = map(int, sys.argv[1:4]); rnd = random.Random(seed)
    cnt = dict(L1=0, L1e=0, L4=0, L6=0, L6min=0, L7=0, L7hi=0); bad = 0
    for b in range(1, 100001):     # beta nondecreasing
        if beta(b + 1) < beta(b): bad += 1; print("beta not monotone", b)
    for t in range(S):
        mode = t % 3
        if mode == 0: x = 2 * rnd.getrandbits(P - 2)
        elif mode == 1: x = (-2 + (2 * rnd.getrandbits(40) + 1) * 2 ** rnd.randrange(2, 12)) % MOD
        else: x = (rnd.choice([0, 2, 6, 14]) + 16 * rnd.getrandbits(P - 6)) % MOD
        prevVM = -1
        for n in range(2, nmax + 1):
            V, M = env(x, n); cnt["L1"] += 1
            if V > n + M - 2 or V - M < beta(n) or V - M < prevVM: bad += 1; print("L1 fail", n, V, M)
            prevVM = V - M
        for _ in range(5):
            n0 = rnd.randrange(1, nmax); i = rnd.randrange(1, nmax)
            if env(x, n0 + i)[0] - env(x, n0)[0] < i - s2(i): bad += 1; print("L1d fail")
            K = rnd.randrange(1, 9); z = x + n0; r = z % (1 << K); NK = (1 << K) - r if r else (1 << K)
            W = lambda n: n - env(x, n)[0]
            cnt["L1e"] += 1
            if W(n0 + NK) - W(n0) > 1 - s2(r): bad += 1; print("L1e fail")
        n = rnd.randrange(2, nmax + 1); pop = alive_paths(x, n)
        if pop is None: continue
        cnt["L4"] += 1
        if len(pop) > 2 ** ((n + 1) // 2 - 1): bad += 1; print("L4 fail", n, len(pop))
        V, M = env(x, n); j = v2(x + 2)
        for e, Sv, S1, S2 in pop:
            lam = v2(S1)
            if x % 4 == 2 and V >= 3 * j + 1:
                cnt["L7"] += 1; cnt["L7hi"] += lam > 2 * j
                if lam > 2 * j and v2(S2) > j: bad += 1; print("L7 FAIL", x % 4096, n, j, lam, v2(S2))
            if 1 <= lam <= 12 and lam < V:
                tau = target(x, n, Sv); r_ = rho(x, n, lam, tau)
                Mt = max(min(v2(x + n + i), lam) for i in range(1, 2 * lam + 1)); cnt["L6"] += 1
                if r_ > 2 ** min(lam - 1, (lam + Mt) // 2 - 1): bad += 1; print("L6 upper fail", lam, Mt, r_)
                # descendant at n+2lam?
                big = alive_paths(x, n + 2 * lam, cap=100000)
                if big is not None and any(q[0][:n] == e for q in big):
                    cnt["L6min"] += 1
                    if r_ < 2.0 ** (-((2 * lam).bit_length() - 1)): bad += 1; print("L6 lower fail", lam, r_)
    print("tests:", cnt, "failures:", bad)
main()
