#!/usr/bin/env python3
"""l2_dp.py -- L^2 (collision) shell sums of factorial tail measures by exact counting (round 3, R3F, target (b)).

nu = law of X = sum_{n >= N0} eps_n x_n,  x_n = n!/p^{e0},  e0 = v_p(N0!),  eps_n fair coins.
For K >= 1 let E_K = {n >= N0 : v_p(x_n) < K} (n_K elements).  Then (Parseval on Z/p^K)
   L2cum(K) := sum_{0 != xi in p^-K Z/Z} |hat nu(xi)|^2 = p^K * Coll_K / 4^{n_K} - 1,
   Coll_K = #{(S,S') subsets of E_K : sum_S x = sum_S' x  (mod p^K)} = sum_r c_K(r)^2,
   c_K(r) = #{S subset of E_K : sum_S x = r (mod p^K)},
and the level-K shell is Q(K) = L2cum(K) - L2cum(K-1).
c_K is computed EXACTLY: subset-sum counting modulo two primes P1, P2 < 2^62 with numpy (each step
c <- c + roll(c, x mod p^K) mod Pi), and Chinese remaindering (c_K(r) < 2^{n_K} < P1*P2); Coll_K is then summed in
Python integers.  Output: exact rationals L2cum(K) (printed as decimals) and Q(K), with the random-model value
N_K 2^{-n_K} (N_K = p^K - p^{K-1}) and the Cauchy-Schwarz L^1 bound sqrt(N_K Q(K)).
Modes:  fact p N0 Kmax   (tail measure from N0; N0 = 0 gives the full factorial measure 0!,1!,2!,...)
usage: l2_dp.py p N0 Kmax
"""
import sys, math
import numpy as np
from fractions import Fraction

P1 = 4611686018427387847   # prime < 2^62
P2 = 4611686018427387817   # prime < 2^62


def vp(n, p):
    c = 0
    while n and n % p == 0:
        n //= p; c += 1
    return c


def elements(p, N0, K):
    f = math.factorial(N0); e0 = vp(f, p)
    out = []; n = N0
    while True:
        lev = vp(f, p) - e0          # levels are nondecreasing in n
        if lev >= K:
            break
        out.append(f // p ** e0)
        n += 1; f *= n
    return out, e0


def counts_mod(xs, M, P):
    c = np.zeros(M, dtype=np.int64); c[0] = 1
    for x in xs:
        s = x % M
        if s == 0:
            c = (2 * c) % P
        else:
            c = (c + np.roll(c, s)) % P
    return c


def main():
    p, N0, Kmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    assert P1 * P2 > 2 ** 122   # counts are < 2^n with n <= 120
    prev = Fraction(0)
    print(f"# l2_dp p={p} N0={N0} Kmax={Kmax}   (exact counts; CRT mod two 62-bit primes)")
    print("# K  n_K  L2cum(K)  Q(K)  N_K 2^-n_K (random)  Q/random  sqrt(N_K Q(K))")
    for K in range(1, Kmax + 1):
        M = p ** K
        xs, e0 = elements(p, N0, K)
        n = len(xs)
        assert n <= 120
        c1 = counts_mod(xs, M, P1); c2 = counts_mod(xs, M, P2)
        # CRT: c = c1 + P1 * ((c2 - c1) * inv(P1) mod P2)
        inv = pow(P1, -1, P2)
        coll = 0
        tot = 0
        for a, b in zip(c1.tolist(), c2.tolist()):
            t = ((b - a) * inv) % P2
            c = a + P1 * t
            coll += c * c; tot += c
        assert tot == 2 ** n, "count check failed"
        L2 = Fraction(M * coll, 4 ** n) - 1
        Q = L2 - prev
        N = M - M // p
        rnd = N / 2 ** n
        print(f"{K:2d} {n:3d} {float(L2):.12e} {float(Q):.12e} {rnd:.6e} {float(Q)/rnd:.6f} {math.sqrt(max(0.0, N*float(Q))):.6e}", flush=True)
        prev = L2


if __name__ == "__main__":
    main()
