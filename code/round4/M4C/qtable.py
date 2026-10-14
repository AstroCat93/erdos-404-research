#!/usr/bin/env python3
"""qtable.py -- table of the exact constants q1(p), q2(p), q3(p) of the M4C report (section 4.3), printed from the
exact rationals of early_phase.py (q1-1 and q2-1 converted with mpmath, so no float underflow).
usage: qtable.py p1 p2 ...
"""
import sys
from math import factorial

import mpmath as mp

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from early_phase import q1_exact, q2_exact, q3_exact  # noqa: E402

mp.mp.dps = 30


def f(x):
    return mp.nstr(mp.mpf(x.numerator) / x.denominator, 4)


for p in (int(a) for a in sys.argv[1:]):
    w = ((factorial(p - 1) + 1) // p) % p == 0
    q1, q2, q3 = q1_exact(p), q2_exact(p), q3_exact(p)
    print(f"p={p} wilson={int(w)} q1-1={f(q1 - 1)} q2-1={f(q2 - 1)} q3={f(q3)} q3-1={f(q3 - 1)}", flush=True)
