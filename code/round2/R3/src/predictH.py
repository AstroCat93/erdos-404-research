#!/usr/bin/env python3
"""predictH.py -- HEURISTIC: least H (with H+1 < p^t) such that the bottleneck ratio
R*(p,t,H) (levels k <= min(c,t), K-independent) is >= Rcrit.  Prints table for several Rcrit."""
import sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from bottleneck import profile, vf

def pred(p, t, Rc, Hmax=200):
    for H in range(2, Hmax):
        if H + 1 >= p**t: return None
        c = vf(H-1, p)
        if 2.0**H / p**(t+c) < Rc: continue
        o = profile(p, t, H, kmax=min(c, t))
        if o['Rstar'] >= Rc: return H, o['Rstar'], o['R0']
    return None

if __name__ == '__main__':
    ps = [int(x) for x in sys.argv[1].split(',')]
    T = int(sys.argv[2])
    for p in ps:
        for Rc in (20, 30, 40):
            row = []
            for t in range(1, T+1):
                r = pred(p, t, Rc)
                row.append(str(r[0]) if r else '-')
            print(f"p={p} Rcrit={Rc}: H_t(pred) t=1..{T}: {' '.join(row)}")
