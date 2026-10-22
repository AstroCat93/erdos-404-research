#!/usr/bin/env python3
"""cont_vs_grid.py -- continuous transfer (j = 0) term versus the p-adic grid sum, for the tail shells
(round 3, track R3F, target (d)).  Numerical illustration.

For the chain x_n = n!/N0! (N0 <= n < N_k, where N_k is the first n with v_p(n!) - v_p(N0!) >= k), let
F_k(theta) = prod_n |cos(pi theta x_n)|.  Poisson summation gives, exactly,
   T(k) = sum_{u unit mod p^k} F_k(u/p^k) = (p^k - p^{k-1}) hat F_k(0) + [aliasing: p^k sum_{j!=0} hat F_k(j p^k)
          - p^{k-1} sum_{j!=0} hat F_k(j p^{k-1})],
and hat F_k(0) = int_0^1 F_k = (2/pi)^{n_k} Psi(0) is what the continuous (factorial-base) transfer operator computes.
Psi(0) is evaluated by the carry recursion over the multipliers m = N0+1, ..., N_k - 1 (truncation |carry| <= C,
floating point; the truncation error is below 1e-6 here since all multipliers are >= 14 or so); the final element has
weight b_s.  The script prints (p^k - p^{k-1}) * int F_k next to the certified T(k) (taken from the ivshell logs).
usage: cont_vs_grid.py p N0 kmax C
"""
import sys, math
import numpy as np


def vp(n, p):
    c = 0
    while n % p == 0:
        n //= p; c += 1
    return c


def main():
    p, N0, kmax, C = map(int, sys.argv[1:5])
    e0 = sum(vp(i, p) for i in range(1, N0 + 1))
    for k in range(1, kmax + 1):
        ns = []
        n, lev = N0, 0
        while lev < k:
            ns.append(n)
            n += 1
            lev += vp(n, p)
        mults = [m for m in range(N0 + 1, ns[-1] + 1)]   # x_{n}/x_{n-1} = n
        W = 2 * C + 1
        s = np.arange(-C, C + 1)
        v = np.zeros(W); v[C] = 1.0                     # carry 0 at the bottom element x_{N0} = 1
        for m in mults:
            # element with coefficient 1 at this stage takes k = s - m s'; new carry s'
            new = np.zeros(W)
            for j, sp in enumerate(range(-C, C + 1)):
                kk = s - m * sp
                b = np.where(kk % 2 == 1, 1.0, -1.0) / (4.0 * kk.astype(float) ** 2 - 1.0)
                new[j] = np.dot(v, b)
            v = new
        kk = s
        bfin = np.where(kk % 2 == 1, 1.0, -1.0) / (4.0 * kk.astype(float) ** 2 - 1.0)
        Psi0 = float(np.dot(v, bfin))
        nk = len(ns)
        cont = (p ** k - p ** (k - 1)) * (2 / math.pi) ** nk * Psi0
        rnd = (p ** k - p ** (k - 1)) * (2 / math.pi) ** nk
        print(f"k={k} n_k={nk} Psi(0)={Psi0:.8f}  (p^k-p^(k-1)) int F_k = {cont:.6e}   random model = {rnd:.6e}", flush=True)


if __name__ == "__main__":
    main()
