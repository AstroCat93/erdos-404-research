#!/usr/bin/env python3
"""Theorem A' of the R3Q report: for each class C in {C0, C2, C6} and every K >= 1024,
mu(C and g_2 >= 2^K) <= 2^{-K/7}.  Rule: T = 2^K - 2K - 12, n_s = floor(K/6), m1 = 0,
k = l_C + z(n_s) + ceil(K/6) + 1.  Closed-form majorant (proof in the report):
   log2 of  2^{-K-15} + 0.911 K^2 2^{-K/6} + mu(C) (2^{-0.1732 (K-5)} + 2^{-K/6}).
(1) checks majorant <= -K/7 (and q <= 0.26) for every K in [1024, 4*10^6];
(2) evaluates the exact bound (bounds.thmA_terms) at sample K and checks exact <= majorant.
usage: rule_A.py"""
import math, sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bounds as B
def maj(K, a):
    t = [-K - 15, math.log2(0.911) + 2 * math.log2(K) - K / 6, -a - 0.1732 * (K - 5), -a - K / 6]
    m = max(t); return m + math.log2(sum(2.0 ** (u - m) for u in t))
bad = None
for K in range(1024, 4_000_001):
    q = (K / 4 + 5) / (K - 5)
    if not (q <= 0.26 and max(maj(K, 3), maj(K, 4)) <= -K / 7): bad = K
print("largest K in [1024, 4e6] violating the closed-form claim:", bad)
for K in (1024, 1536, 2048, 4096):
    G = 2 ** K; T = G - 2 * K - 12; ns = K // 6
    for nm, (r, a, lam, nC) in B.CLASSES.items():
        k = B.lratio_A(lam) + B.z(ns) + (-(-K // 6)) + 1
        t, Kt = B.thmA_terms(nm, G, T, ns, k, 0); ex = sum(t.values())
        le = math.log2(ex.numerator) - math.log2(ex.denominator)
        print(f"K={K} {nm}: exact log2={le:.2f}  majorant={maj(K, a):.2f}  -K/7={-K/7:.2f}  {'OK' if le <= maj(K, a) <= -K/7 else 'CHECK'}")
