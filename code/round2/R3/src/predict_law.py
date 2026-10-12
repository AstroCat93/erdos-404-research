#!/usr/bin/env python3
"""HEURISTIC threshold law (fitted on the scan data of logs/rstar_table.txt):
   Cov(p,t,H) holds (for the tested set of n_classes classes/positions)  iff
   nu := R*(p,t,H) / ln(p^(t+c) * n_classes) >= nu_c,   nu_c in (1.13, 1.21).
Prints, for given p,t and class-count mode, nu(H) for a range of H and the predicted minimal H."""
import sys, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bottleneck import profile, vf
p, t, Hlo, Hhi = map(int, sys.argv[1:5]); mode = sys.argv[5]  # 'uniform' or 'pos:N'
for H in range(Hlo, Hhi + 1):
    c = vf(H - 1, p); M = t + c
    n = (p ** c - p ** (c - 1) if c else 1) if mode == 'uniform' else int(mode.split(':')[1])
    o = profile(p, t, H, kmax=min(c, t, 5))
    nu = o['Rstar'] / math.log(p ** M * n) if o['Rstar'] > 0 else 0
    pred = 'HOLD' if nu >= 1.21 else ('FAIL' if nu <= 1.13 else 'borderline')
    print(f"p={p} t={t} H={H} c={c} rho={(H-1)%p} R*={o['Rstar']:.4g} n={n} nu={nu:.3f} -> predicted {pred}")
