#!/usr/bin/env python3
"""Theorem C bookkeeping: (1) for every K in [2400, 4*10^6] check the closed-form majorant <= -K/80 and the
side conditions M >= 22, qA = (K/32+10)/(K-5) <= 0.04 and q(K) = (22.75M - 1.5 + log2(40.5M))/(K-5) <= 0.36; report the largest failing K.
(2) For K > 4*10^6 the report gives a one-line argument. usage: rule_K0.py"""
import math, sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rule import majorant
last_fail = None
for K in range(2400, 4_000_001):
    M = K // 64
    q = (22.75 * M - 1.5 + math.log2(40.5 * M)) / (K - 5)
    qA = (K / 32 + 10) / (K - 5)
    if not (M >= 22 and q <= 0.36 and qA <= 0.04 and majorant(K) <= -K / 80): last_fail = K
print("largest K in [2400, 4e6] violating (majorant <= -K/80, M>=22, q<=0.36):", last_fail)
