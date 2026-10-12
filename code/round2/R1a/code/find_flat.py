import random, sys
from hier_lib import *
from collections import Counter
rnd = random.Random(int(sys.argv[1])); trials = int(sys.argv[2])
c = Counter()
for t in range(trials):
    w = rnd.randrange(2, 9); n = rnd.randrange(8, 30)
    y = (1 << 90) - 2 + ((rnd.getrandbits(70) | 1) << w)
    for p in valid_paths(y, n, cap=60):
        u = hier(y, p); m = flat_order(u)
        if m < 2: continue
        P, M, pin = env(y, n)
        lam = vf(m * u[m] * pin); sig = P - lam
        c[(m, n // 8 * 8, sig >= lam + M + 1)] += 1
print(sorted(c.items()))
