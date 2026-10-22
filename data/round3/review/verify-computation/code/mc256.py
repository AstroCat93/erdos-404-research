# Haar Monte Carlo of min(g_2, cap) with the big-integer recursion of g2deep.py (independent of gdec.c)
import sys, random, time
sys.path.insert(0, sys.argv[4]); from g2deep import g2
cap, n, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(seed); hist = {}; t0 = time.time()
for i in range(n):
    x = rng.getrandbits(cap)
    g = g2(x, cap); hist[g] = hist.get(g, 0) + 1
print(f"# cap={cap} n={n} seed={seed} time={time.time()-t0:.0f}s")
for G in [64,128,192,256,384,512]:
    if G<=cap: print(f"G={G} survivors={sum(c for g,c in hist.items() if g>=G)}")
