import random, sys
from collections import Counter, defaultdict
from kappa import run, v2
rnd = random.Random(int(sys.argv[1]))
nsteps = int(sys.argv[2]); ns = int(sys.argv[3])
stats = defaultdict(Counter)
for it in range(ns):
    x = rnd.getrandbits(3000) & ~1
    h = run(x, nsteps, 3000)
    if h is None: continue
    w = v2(x + 2)
    # record kappa distribution at the last step with nonempty population with n>=20
    for (n, d, P, kap) in h:
        if n == min(len(h)+1, nsteps) or (P and n == 30):
            pass
    # take kappa at step 30 if alive
    for (n, d, P, kap) in h:
        if n == 30 and P:
            for k, c in kap.items(): stats[w][k] += c
for w in sorted(stats): print("v(x+2)=", w, dict(sorted(stats[w].items())))
