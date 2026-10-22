#!/usr/bin/env python3
"""afe_cond.py -- the quantities of Corollary F'' of the M4C report on the set U_a = {x : x = 0 mod p^(a+1)}
(so x = p xi with xi = 0 mod p^a; the gates up to block p^a have the deterministic depths 1 + v(j)).

Block schedule n_k = b_k p, b_0 = 3, b_1 = 4 (W_0 = [3p,4p) is one block), later b_k chosen greedily so that
lin_k holds for every x in U_a whenever all gates up to n_{k+1} have depth <= 1 + max(v(j), cap_k), see sched().

Printed:
  RIGOROUS  base = 1/(4 p q_p)  (= mu_U-average of 1/(4(1+chi^2_{W_0})), chi^2_{W_0} = p q_p - 1 on every atom;
            requires a slope-0 path at 3p on every atom of U_a: Proposition W, non-Wilson p)
  HEURISTIC (Monte Carlo over x in U_a): for k = 1..KT: the empirical frequency of 'lin_k fails' and
            E[1_{lin_k} min(1, 16 eps_k)]; samples whose composite has K > KMAX count as 1 (conservative).
usage: afe_cond.py p a SEED NX KMAX KT b0 b1 b2 ...
"""
import random
import sys
import time
from math import factorial

import numpy as np


def vp(a, p, cap):
    a %= p ** cap
    if a == 0:
        return cap
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def q_exact(p):
    dist = [0] * p
    dist[0] = 1
    for u in range(p):
        a = factorial(u) % p
        new = [0] * p
        for t in range(p):
            if dist[t]:
                new[t] += 2 * dist[t]
                new[(t + a) % p] += dist[t]
                new[(t - a) % p] += dist[t]
        dist = new
    return dist[0] / 4 ** p


def eps_comp(x, n0, n2, D, K, p):
    mod = p ** K
    dist = np.zeros(mod, dtype=np.float64)
    dist[0] = 1.0
    y = 1
    for c in range(n0, n2):
        if c > n0:
            y = y * (x + c) % mod
        dist = 0.5 * (dist + np.roll(dist, y % mod))
    F = np.fft.fft(dist)
    idx = np.arange(mod)
    band = (idx % p ** (K - D)) != 0
    a = np.abs(F[band])
    return float(np.sum(a * a))


def main():
    p, a, seed, NX, KMAX, KT = (int(t) for t in sys.argv[1:7])
    b = [int(t) for t in sys.argv[7:]]
    n = [bi * p for bi in b]
    rnd = random.Random(seed)
    PREC = 60
    q = q_exact(p)
    base = 1 / (4 * p * q)
    print(f"# afe_cond p={p} a={a} seed={seed} NX={NX} KMAX={KMAX} KT={KT} blocks={b}")
    print(f"RIGOROUS q_p={q:.6e}, 1+chi^2_W0 = p q_p = {p*q:.5f}, base = 1/(4 p q_p) = {base:.4e} (conditional on U_a)")
    linfail = [0] * (KT + 1)
    terms = [0.0] * (KT + 1)
    over = [0] * (KT + 1)
    t0 = time.time()
    for it in range(NX):
        x = p ** (a + 1) * rnd.randrange(p ** (PREC - a - 1))
        N = n[KT + 1]
        vals = [0] + [vp(x + i, p, PREC) for i in range(1, N + 1)]
        V = [0] * (N + 1)
        M = [0] * (N + 1)
        for i in range(1, N + 1):
            V[i] = V[i - 1] + vals[i]
            M[i] = max(M[i - 1], vals[i])
        for k in range(1, KT + 1):
            m = V[n[k - 1]]
            D = V[n[k]] - m
            K = V[n[k + 1]] - m
            lin = (K <= m - M[n[k + 1]]) and (M[n[k + 1]] < m)
            if not lin:
                linfail[k] += 1
                continue
            if K > KMAX:
                over[k] += 1
                terms[k] += 1.0
                continue
            e = eps_comp(x, n[k - 1], n[k + 1], D, K, p)
            terms[k] += min(1.0, 16 * e)
    tot = 0.0
    for k in range(1, KT + 1):
        lf = linfail[k] / NX
        tm = terms[k] / NX
        tot += lf + tm
        print(f"TERM k={k} composite blocks [{b[k-1]},{b[k+1]}): P(lin_k fails) ~ {lf:.3e}; "
              f"E[1_lin min(1,16 eps_k)] ~ {tm:.3e} (K>KMAX counted as 1: {over[k]})")
    print(f"HEURISTIC partial sum (k<={KT}) = {tot:.3e};  base - partial = {base - tot:.3e}   [{time.time()-t0:.0f}s]")


if __name__ == "__main__":
    main()
