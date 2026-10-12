#!/usr/bin/env python3
"""Exact-ish (float64 probabilities, error ~1e-14) DP of the subset-sum distribution of
{n!/p : p <= n < p(K+1)} mod p^K, to test Corollary 10.17 directly and to cross-check the shell
sums by Parseval:  mean_y theta_y^2 = sum_{k<=K} T2(k).   usage: equidist_dp.py p K"""
import sys
import numpy as np
p, K = int(sys.argv[1]), int(sys.argv[2])
Q = p ** K
prob = np.zeros(Q); prob[0] = 1.0
f = 1
for n in range(1, p * (K + 1)):
    f *= n
    if n < p:
        continue
    x = (f // p) % Q
    if x == 0:
        continue
    prob = 0.5 * (prob + np.roll(prob, x))
theta = prob * Q - 1.0
print(f"p={p} K={K} elements={p*K} max|theta|={np.abs(theta).max():.6e} min={theta.min():.6e} "
      f"mean_theta^2={np.mean(theta**2):.12e} zero_classes={(prob==0).sum()}")
