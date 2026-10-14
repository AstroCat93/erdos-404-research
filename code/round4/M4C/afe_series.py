#!/usr/bin/env python3
"""afe_series.py -- the explicit quantities of Theorem F' / Corollary F'' of the M4C report at a given p,
for the block schedule n_k = b_k p (b_0 = 3, b_1 = 4, ...) on the class x in pZ_p (x = p xi):

  base  (rigorous, exact):  (p-4)/p * 1/(4 p q_p),  q_p = P(sum_{u<p} d_u u! = 0 mod p), d_u lazy signed;
                            this is the lower bound sum_A mu(A|pZ_p) / (4(1+chi^2_{W_0}))  (chi^2 = p q_p - 1)
  lin   (rigorous upper bound on mu(U and some lin_k fails | pZ_p), Lemma L of the report; exact evaluation)
  terms (HEURISTIC Monte Carlo): E_{z in pZ_p}[min(1, 16 eps_k)] for k = 1..kmax, where eps_k is the band
        mass of the composite window [n_{k-1}, n_{k+1}) at z = x + n_{k-1}; samples with K > KMAX count as 1.

usage: afe_series.py p SEED NZ KMAX J0 KTERMS ETA   (greedy block schedule, see schedule())
"""
import random
import sys
import time
from math import factorial

import numpy as np


def vp(a, p, cap=80):
    if a == 0:
        return cap
    k = 0
    while a % p == 0 and k < cap:
        a //= p
        k += 1
    return k


def q_exact(p):
    """P(sum_u d_u u! = 0 mod p), d_u i.i.d. lazy signed (exact rational via integer DP, weights x4)."""
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
    return dist[0], 4 ** p


def eps_at(z, L, L2, p, KMAX, MODBIG):
    vals = [vp((z + i) % MODBIG, p) for i in range(1, L + L2 + 1)]
    D = sum(vals[:L])
    K = sum(vals)
    if K > KMAX:
        return None
    if K == D:
        return 0.0
    mod = p ** K
    dist = np.zeros(mod, dtype=np.float64)
    dist[0] = 1.0
    y = 1
    for c in range(L + L2):
        dist = 0.5 * (dist + np.roll(dist, y % mod))
        y = y * (z + c + 1) % mod
    F = np.fft.fft(dist)
    idx = np.arange(mod)
    band = (idx % p ** (K - D)) != 0
    a = np.abs(F[band])
    return float(np.sum(a * a))


def s_least(l, bprev, p):
    """least tau >= 0 violating  l + 1 + tau + sum_{a=1}^{tau} ceil(l/p^a) <= bprev  (sufficient condition for lin_k
    when T_k <= tau).  lin_k can fail only if T_k := max_{j<=b_{k+1}} t(j) >= s_least."""
    lhs = l + 1
    tau = 0
    while lhs <= bprev:
        tau += 1
        lhs += 1 + -(-l // p ** tau)
    return tau


def s_required(bnext, k, p, J0, eta):
    """least s >= 1 with (bnext - J0)^+ * p^{1-s}/(p-J0) <= eta * 2^{-k}   (per-window union-bound budget)."""
    if bnext <= J0:
        return 1
    s = 1
    while (bnext - J0) * p ** (1 - s) / (p - J0) > eta * 2.0 ** (-k):
        s += 1
    return s


def schedule(p, J0, kmax, eta):
    """greedy block schedule: b0=3, b1=4, b_{k+1} = largest b > b_k with s_least(b-b_{k-1}, b_{k-1}) >= s_required."""
    b = [3, 4]
    while len(b) < kmax:
        k = len(b) - 1
        bp = b[-2]
        best = None
        lo, hi = b[-1] + 1, 2 * bp
        while lo <= hi:
            mid = (lo + hi) // 2
            if s_least(mid - bp, bp, p) >= s_required(mid, k, p, J0, eta):
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1
        if best is None:
            return b
        b.append(best)
    return b


def lin_bound(p, b, J0):
    """Rigorous bound on mu(exists k <= len(b)-2: lin_k fails | x in U), U = {x = p xi : t(j) = 0 for j <= J0},
    t(j) = v(xi + j).  lin_k holds if l + 1 + T_k + S_k <= b_{k-1} (l = b_{k+1}-b_{k-1}, T_k = max_{j<=b_{k+1}} t(j),
    S_k = sum over the window of t(j) <= sum_{a<=T_k} ceil(l/p^a)); so it fails only if T_k >= s_k := s_least.
    P(T_k >= s_k | U) <= sum_{J0 < j <= b_{k+1}} P(p^{s_k} | xi + j | U) <= (b_{k+1}-J0)^+ p^{-s_k} * p/(p-J0)."""
    tot = 0.0
    for k in range(1, len(b) - 1):
        s = s_least(b[k + 1] - b[k - 1], b[k - 1], p)
        if s == 0:
            return float("inf")
        if b[k + 1] > J0:
            tot += (b[k + 1] - J0) * p ** (-s) * p / (p - J0)
    return tot


def main():
    p, seed, NZ, KMAX, J0, KTERMS = (int(a) for a in sys.argv[1:7])
    eta = float(sys.argv[7])
    rnd = random.Random(seed)
    MODBIG = p ** 80
    num, den = q_exact(p)
    q = num / den
    b = schedule(p, J0, 60, eta)
    lb = lin_bound(p, b, J0)
    frac = (p - J0) / p
    base = frac / (4 * p * q)
    print(f"# afe_series p={p} seed={seed} NZ={NZ} KMAX={KMAX} J0={J0} eta={eta}; block schedule = {b}")
    print(f"RIGOROUS q_p = {num}/{den} = {q:.6e} (p q_p = 1+chi^2 = {p*q:.4f});  mu(U|pZ_p) = {frac:.4f}")
    print(f"RIGOROUS base = mu(U|pZ_p)/(4 p q_p) = {base:.4e};  lin-failure bound (listed k) = {frac*lb:.4e} (relative to pZ_p)")
    tot = 0.0
    for k in range(1, KTERMS + 1):
        L, L2 = (b[k] - b[k - 1]) * p, (b[k + 1] - b[k]) * p
        t0 = time.time()
        vals, over = [], 0
        for _ in range(NZ):
            z = p * rnd.randrange(MODBIG // p)  # z = x + n_{k-1} is Haar on pZ_p
            e = eps_at(z, L, L2, p, KMAX, MODBIG)
            if e is None:
                over += 1
                vals.append(1.0)
            else:
                vals.append(min(1.0, 16 * e))
        m = float(np.mean(vals))
        se = float(np.std(vals) / np.sqrt(NZ))
        tot += m
        print(f"TERM k={k} composite blocks [{b[k-1]},{b[k+1]}) (L={L},L'={L2}): "
              f"E[min(1,16eps)] ~ {m:.3e} +- {se:.1e}  (K>KMAX counted as 1: {over}/{NZ})  [{time.time()-t0:.0f}s]",
              flush=True)
    print(f"HEURISTIC partial sum (k<={KTERMS}) = {tot:.3e};  base - lin - partial = {base - frac*lb - tot:.3e}")


if __name__ == "__main__":
    main()
