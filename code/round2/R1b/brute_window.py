#!/usr/bin/env python3
"""Second, brute-force implementation of the one-window identity (shares no code with mart_check2.py).

For random even x (P-bit integer standing for an element of Z_2), times n < N, m = V_n(x), D = V_N(x)-m:
  * parents: all e in {0,1}^n (e_0 = 1) with 2^m | S_e(x) -- found by a meet-in-the-middle-free
    exhaustive search over e restricted to the first n bits is too big, so parents are found by a
    plain recursive search that tests divisibility of the partial polynomial sums directly
    (pruning: a prefix e_{<j} can only extend to an alive path if 2^{V_j} | S_{e_{<j}}(x)).
  * children: ALL f in {0,1}^{N-n}, tested directly by 2^{V_N(x_w)} | S_{e,f}(x_w) for every w mod 2^D,
  * lambda, tau mod 2^lambda, rho: computed directly from the polynomial values.
Checks: avg_w sum_children rho_N(child) == 2^{W_N - W_n} rho_n(parent)  (exact Fractions).
Usage: brute_window.py seed instances n N P DMAX
"""
import random, sys
from fractions import Fraction

def val(a):
    if a == 0:
        return 10**9
    c = 0
    while a % 2 == 0:
        a //= 2; c += 1
    return c

def poly_tables(x, n, MOD):
    p = [1]
    for j in range(1, n + 1):
        p.append(p[-1] * (x + j) % MOD)
    dp = [0]
    for j in range(1, n + 1):
        # derivative of prod_{i<=j}(X+i) at x = sum_i prod_{l != i}
        s = 0
        for i in range(1, j + 1):
            t = 1
            for l in range(1, j + 1):
                if l != i:
                    t = t * (x + l) % MOD
            s += t
        dp.append(s % MOD)
    return p, dp

def Vn(x, n):
    return sum(val(x + i) for i in range(1, n + 1))

def parents_of(x, n, MOD, p):
    Vs = [0] + [Vn(x, j) for j in range(1, n + 1)]
    out = []
    def rec(j, mask, S):
        # S = S_{e_<j}(x) mod MOD ; need 2^{V_j} | S
        if val(S % MOD) < Vs[j] and S % MOD != 0:
            return
        if j == n:
            out.append(mask); return
        for e in ((1,) if j == 0 else (0, 1)):
            rec(j + 1, mask | (e << j), (S + e * p[j]) % MOD)
    rec(0, 0, 0)
    return out

def rho_direct(x, n, lam, tau, MOD):
    if lam == 0:
        return Fraction(1)
    k = 2 * lam
    q = [1]
    for j in range(n + 1, n + k):
        q.append(q[-1] * (x + j))
    hits = 0
    for f in range(1 << k):
        s = sum(q[i] for i in range(k) if (f >> i) & 1)
        if (s - tau) % (1 << lam) == 0:
            hits += 1
    return Fraction(hits << lam, 1 << k)

def tau_lam(mask, x, n, MOD, p, dp):
    S = sum(p[j] for j in range(n) if (mask >> j) & 1) % MOD
    Sp = sum(dp[j] for j in range(n) if (mask >> j) & 1) % MOD
    Vx = val(p[n])
    assert val(S) >= Vx
    lam = val(Sp)
    P2 = MOD.bit_length() - 1
    prec = P2 - Vx
    tau = (-(S >> Vx) * pow(p[n] >> Vx, -1, 1 << prec)) % (1 << prec)
    return tau, lam

if __name__ == "__main__":
    seed, inst, n, N, P, DMAX = (int(a) for a in sys.argv[1:7])
    rnd = random.Random(seed); MOD = 1 << P
    tot = ok = 0; done = 0; tries = 0
    while done < inst and tries < 50000:
        tries += 1
        x = rnd.getrandbits(P) & ~1
        m = Vn(x, n); D = Vn(x, N) - m
        if D < 1 or D > DMAX:
            continue
        p, dp = poly_tables(x, N, MOD)
        par = parents_of(x, n, MOD, p)
        info = {}
        for e in par:
            tau, lam = tau_lam(e, x, n, MOD, p, dp)
            if lam <= D and lam <= m:
                info[e] = (lam, rho_direct(x, n, lam, tau, MOD))
        if not info:
            continue
        done += 1
        x0 = x % (1 << m); rest = x >> (m + D)
        acc = {e: Fraction(0) for e in info}
        for w in range(1 << D):
            xw = x0 + (w << m) + (rest << (m + D))
            pw, dpw = poly_tables(xw, N, MOD)
            VNw = val(pw[N])
            for e in info:
                lam, _ = info[e]
                Se = sum(pw[j] for j in range(n) if (e >> j) & 1)
                for f in range(1 << (N - n)):
                    S = Se + sum(pw[n + i] for i in range(N - n) if (f >> i) & 1)
                    if S % (1 << VNw) == 0:
                        c = e | (f << n)
                        tauN, lamN = tau_lam(c, xw, N, MOD, pw, dpw)
                        assert lamN == lam, ("lambda not inherited", lam, lamN)
                        acc[e] += rho_direct(xw, N, lam, tauN, MOD)
        WnN = (N - Vn(x, N)) - (n - m)
        for e, (lam, r) in info.items():
            tot += 1
            ok += (acc[e] / (1 << D) == Fraction(2) ** WnN * r)
        print(f"inst {done}: m={m} D={D} parents={len(info)} lams={sorted(set(l for l,_ in info.values()))} ok so far {ok}/{tot}", flush=True)
    print(f"BRUTE-FORCE TOTAL exact identities: {ok}/{tot}")
