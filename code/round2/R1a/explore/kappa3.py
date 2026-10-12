# max kappa over valid paths vs w = v(x+2), sampling x near -2.
import random, sys
from collections import Counter, defaultdict
from kappa import run, v2
rnd = random.Random(int(sys.argv[1]))
nsteps = int(sys.argv[2]); ns = int(sys.argv[3]); wmax = int(sys.argv[4])
res = defaultdict(Counter); alive = Counter(); tot = Counter()
for w in range(1, wmax + 1):
    for it in range(ns):
        u = rnd.getrandbits(3000) | 1
        x = (-2 + (u << w)) % (1 << 3000)
        h = run(x, nsteps, 3000, K=80)
        tot[w] += 1
        if h is None or not h or h[-1][2] == 0: continue
        alive[w] += 1
        for k, c in h[-1][3].items(): res[w][k - w] += c
for w in range(1, wmax + 1):
    print("w=", w, "alive", alive[w], "/", tot[w], "kappa-w dist:", dict(sorted(res[w].items())))
