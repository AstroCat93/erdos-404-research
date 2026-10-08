"""For small p and levels G, list all classes c mod p^(G+1) with g(c,p) = G exactly (well defined by locality),
and test whether each is a 'shadow' of a negative integer: c == -m mod p^(G+1) with gamma(m,p) = G.
Uses the C pruned DP (./gtab) on representatives c in [1, p^(G+1)]."""
import subprocess, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shadow import all_C, vp
here = os.path.dirname(os.path.abspath(__file__))
def gamma(m, p):
    vals = all_C(m)
    if any(v == 0 for v in vals): return math.inf
    return max(vp(v, p) for v in vals)
p = int(sys.argv[1]); Gmax = int(sys.argv[2]); Mmax = int(sys.argv[3])
gam = {m: gamma(m, p) for m in range(1, Mmax + 1)}
N = p ** (Gmax + 1)
out = subprocess.run([f"{here}/gtab", "gtab", str(p), "1", str(N), str(Gmax + 1)], capture_output=True, text=True).stdout.split()
g = {int(out[i]): int(out[i + 1]) for i in range(0, len(out), 2)}
for G in range(0, Gmax + 1):
    mod = p ** (G + 1)
    cls = sorted(c for c in range(1, mod + 1) if g[c] == G)
    cls = [c % mod for c in cls]
    tagged = []
    for c in cls:
        ms = [m for m in range(1, Mmax + 1) if (c + m) % mod == 0 and gam[m] == G]
        tagged.append((c, ms[0] if ms else None))
    nsh = sum(1 for _, m in tagged if m is not None)
    print(f"p={p} G={G}: {len(cls)} classes mod p^{G+1} with g=G exactly (density {len(cls)/mod:.6f}); "
          f"{nsh} are shadows of -m (m<={Mmax}); non-shadow classes: {[c for c,m in tagged if m is None][:30]}")
    print("    shadows:", [(c, -m) for c, m in tagged if m is not None][:30])
