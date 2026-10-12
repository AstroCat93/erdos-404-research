#!/usr/bin/env python3
"""Probe Observation 10.1.2 ('slope 2 never occurs among alive paths at p=2').
Enumerates alive paths at n for various even x (random, and near -2) and tallies slopes v2(S_e'(x))."""
import random, sys
sys.path.insert(0, '.')
from p2_window import alive_paths, v2, B

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
tally = {}
examples = {}
for trial in range(int(sys.argv[2]) if len(sys.argv) > 2 else 400):
    kind = trial % 3
    if kind == 0:
        x = rng.getrandbits(B) & ~1
    elif kind == 1:
        k = rng.randint(2, 12)
        x = (-2 + (1 << k) * (2 * rng.getrandbits(B - k - 2) + 1)) % (1 << B)
    else:
        x = (rng.getrandbits(B) << 3)  # x == 0 mod 8
    for n in (12, 20, 30, 40):
        pop, V = alive_paths(x, n)
        if len(pop) > 20000:
            break
        for (w, S, dS) in pop:
            lam = v2(dS)
            tally[(kind, n, lam)] = tally.get((kind, n, lam), 0) + 1
            if lam == 2 and (kind, n) not in examples:
                examples[(kind, n)] = (x % (1 << 40), w)
agg = {}
for (kind, n, lam), c in tally.items():
    agg.setdefault((kind, n), {})[lam] = c
for key in sorted(agg):
    print(key, sorted(agg[key].items())[:12])
print("lambda=2 examples:", examples)
