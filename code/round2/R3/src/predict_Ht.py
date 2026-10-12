#!/usr/bin/env python3
"""HEURISTIC prediction of the minimal uniform H_t:  least H with H+1<p^t, (H-1) mod p >= rho0(p) and
nu = R*/ln(p^(t+c) * phi(p^c)) >= 1.25  (bottleneck levels k <= min(c,t,4))."""
import sys, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bottleneck import profile, vf
def pred(p, t):
    for H in range(2, 400):
        if H + 1 >= p**t: return None
        c = vf(H - 1, p); M = t + c; n = (p**c - p**(c-1)) if c else 1
        if 2.0**H / p**M < 1.25 * math.log(p**M * n): continue
        o = profile(p, t, H, kmax=min(c, t, 4))
        if o['Rstar'] > 0 and o['Rstar'] / math.log(p**M * n) >= 1.25: return H
for p in map(int, sys.argv[1].split(',')):
    T = int(sys.argv[2])
    print(f"p={p}: predicted H_t, t=1..{T}:", [pred(p, t) for t in range(1, T + 1)])
