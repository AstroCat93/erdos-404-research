# Explore: distribution of the derivative offset kappa = v2(B_n), B_n = sum_{i<=n} gamma_i(x) pi_{i-1}(x)
# for valid paths of the forward carry process at p=2.  Exploration only.
import random, sys
from collections import Counter
def v2(n):
    if n == 0: return 10**9
    return (n & -n).bit_length() - 1
def run(x, nsteps, M, K=40):
    # population: dict (gamma mod 2^M', B mod 2^K) -> count ; we keep gamma as integer mod 2^Mcur
    modK = 1 << K
    # step 0: gamma_0 = 0, e_0 = 1 -> gamma_1 = 1/(x+1)
    Mcur = M
    pi_prev = 1  # pi_0 mod 2^K
    pop = Counter()
    # gamma_1
    d = v2(x + 1)
    if d > 0: return None
    u = (x + 1) % (1 << Mcur)
    g1 = pow(u, -1, 1 << Mcur)
    B = (g1 * pi_prev) % modK
    pop[(g1, B)] = 1
    pi_prev = (x + 1) % modK
    hist = []
    for n in range(2, nsteps + 1):
        d = v2(x + n)
        Mnew = Mcur - d
        u = ((x + n) >> d) % (1 << Mnew)
        inv = pow(u, -1, 1 << Mnew)
        new = Counter()
        for (g, B), c in pop.items():
            for e in (0, 1):
                y = (g + e) % (1 << Mcur)
                if d and (y & ((1 << d) - 1)): continue
                gn = ((y >> d) * inv) % (1 << Mnew)
                Bn = (B + gn * pi_prev) % modK
                new[(gn, Bn)] += c
        pop = new
        Mcur = Mnew
        pi_prev = (pi_prev * (x + n)) % modK
        kap = Counter()
        for (g, B), c in pop.items(): kap[min(v2(B), K)] += c
        hist.append((n, d, sum(pop.values()), dict(kap)))
        if not pop: break
    return hist
if __name__ == "__main__":
    rnd = random.Random(int(sys.argv[1]))
    nsteps = int(sys.argv[2]); ns = int(sys.argv[3])
    for it in range(ns):
        x = rnd.getrandbits(4000) & ~1
        h = run(x, nsteps, 4000)
        if h is None: continue
        last = h[-1]
        print("x mod 64 =", x % 64, "v(x+2)=", v2(x+2), "steps", len(h)+1, "final pop", last[2], "kappa dist", last[3])
