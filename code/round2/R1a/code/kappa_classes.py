# For x in a given residue class, list valid paths through n and their kappa_n = v(B_n(x,x)); exact rationals.
import random, sys
from fractions import Fraction as Fr
from hier_lib import v2i, vf, valid_paths, hier
def kappa(y, p):
    n = len(p); u = hier(y, p, 2)
    pin = 1
    for l in range(1, n + 1): pin *= (y + l)
    return vf(u[1] * pin)
rnd = random.Random(1)
for (res, mod) in [(0, 8), (2, 8), (6, 16), (14, 32), (30, 64)]:
    seen = {}
    for t in range(40):
        y = (rnd.getrandbits(80) // mod) * mod + res
        for n in (8, 12, 16, 24):
            for p in valid_paths(y, n, cap=200):
                k = kappa(y, p)
                seen.setdefault((n, p[:6]), set()).add(k)
    print(f"class {res} mod {mod}:")
    agg = {}
    for (n, pre), ks in seen.items(): agg.setdefault(n, set()).update(ks)
    for n in sorted(agg): print("   n=", n, "kappa values:", sorted(agg[n]))
    pref = {}
    for (n, pre), ks in seen.items():
        if n == 24: pref[pre] = sorted(ks)
    print("   n=24 prefixes -> kappa:", pref)
