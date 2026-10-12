# For random x, track over valid paths: max (kappa_n - v(pi_n)) and the number of 'flat' paths (kappa_n >= v(pi_n)),
# and the number of unstable paths (sigma < kappa + M + 1).
import random, sys
from collections import Counter
def v2(n):
    if n == 0: return 10**9
    return (n & -n).bit_length() - 1
def run(x, nsteps, M=2500, K=200):
    modK = 1 << K
    if v2(x + 1): return []
    Mcur = M
    g1 = pow((x + 1) % (1 << M), -1, 1 << M)
    pop = Counter({(g1, g1 % modK): 1})
    pi_prev = (x + 1) % modK; vpi = 0; Menv = 0
    out = []
    for n in range(2, nsteps + 1):
        d = v2(x + n); vpi += d; Menv = max(Menv, d)
        Mnew = Mcur - d
        inv = pow(((x + n) >> d) % (1 << Mnew), -1, 1 << Mnew)
        new = Counter()
        for (g, B), c in pop.items():
            for e in (0, 1):
                y = (g + e) % (1 << Mcur)
                if d and (y & ((1 << d) - 1)): continue
                gn = ((y >> d) * inv) % (1 << Mnew)
                new[(gn, (B + gn * pi_prev) % modK)] += c
        pop = new; Mcur = Mnew
        pi_prev = (pi_prev * (x + n)) % modK
        if not pop: out.append((n, 0, None, 0, 0)); break
        kaps = [(min(v2(B), K), c) for (g, B), c in pop.items()]
        mx = max(k for k, c in kaps) - vpi
        flat = sum(c for k, c in kaps if k >= vpi)
        unst = sum(c for k, c in kaps if vpi - k < k + Menv + 1)
        out.append((n, sum(pop.values()), mx, flat, unst))
    return out
if __name__ == "__main__":
    rnd = random.Random(int(sys.argv[1])); nsteps = int(sys.argv[2]); ns = int(sys.argv[3])
    checkpoints = [16, 32, 64, 128, 256, 512]
    agg = {c: Counter() for c in checkpoints}
    for it in range(ns):
        w = int(sys.argv[4]) if len(sys.argv) > 4 else None
        if w:
            x = (-2 + ((rnd.getrandbits(2400) | 1) << w)) % (1 << 2500)
        else:
            x = rnd.getrandbits(2500) & ~1
        out = run(x, nsteps)
        for (n, P, mx, flat, unst) in out:
            if n in agg:
                agg[n]['alive'] += (P > 0); agg[n]['flatx'] += (flat > 0); agg[n]['unstx'] += (unst > 0)
                agg[n]['flatpaths'] += flat; agg[n]['paths'] += P
    for c in checkpoints:
        if agg[c]: print(c, dict(agg[c]))
