# Test C: Monte Carlo checks of Prop 11.26 (first-moment bound), the supermartingale
# E[Y_l 1_C] nonincreasing (Lemma 11.27), and the barrier inequality Prop 11.28.
import sys, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from lib import *

cname = sys.argv[1]; SAMPLES = int(sys.argv[2]); seed = int(sys.argv[3])
CL = {'C0': (0, 3, 1, 4, 1), 'C2': (2, 3, 3, 7, 8), 'C6': (6, 4, 6, 11, 256)}
r0, k, L, Vc, I26 = CL[cname]
l0 = 2 * L + 2
n0 = int(sys.argv[4]) if len(sys.argv) > 4 else 19
LSTAR = int(sys.argv[5]) if len(sys.argv) > 5 else 4
rng = random.Random(seed)
Nmax = n0 + (LSTAR + 1) * l0
sumZ = 0.0; sumY = [0.0] * (LSTAR + 1)
cs = [-2, -1, 0, 1, 2, 3]
hit = {c: 0 for c in cs}
for it in range(SAMPLES):
    x = rand_in_class(r0, k, rng)
    pi, dpi = pis(x, Nmax)
    V = [0]
    for j in range(1, Nmax + 1):
        V.append(V[-1] + v(x + j))
    def M(n): return Mn(x, n)
    def Gam(n): return 2 * M(n + l0) + 3 * L + 3 <= V[n]
    # alive paths at each n_l via one BFS
    cur = [((1,), 1, 0)]
    alive_at = {}
    nl = [n0 + l * l0 for l in range(LSTAR + 2)]
    for j in range(1, Nmax):
        nxt = []
        for e, S, dS in cur:
            for b in (0, 1):
                S2 = (S + b * pi[j]) & MASK
                if v(S2) >= V[j + 1]:
                    nxt.append((e + (b,), S2, (dS + b * dpi[j]) & MASK))
        cur = nxt
        if j + 1 in nl:
            alive_at[j + 1] = cur
    # Prop 11.26 at n0
    n = n0
    if V[n] >= max(Vc, 2 * L + 1, L + k) and V[n] - L > M(n):
        sumZ += 2.0 ** (V[n] - n) * len(alive_at[n])
    # Y_l
    goodsofar = True
    Ys = []
    for l in range(LSTAR + 1):
        n = nl[l]
        goodsofar = goodsofar and Gam(n)
        if goodsofar:
            Ml = 2.0 ** (V[n] - n) * sum(float(rho(x, n, S, dS, pi[n], V[n])[0]) for e, S, dS in alive_at[n])
        else:
            Ml = 0.0
        sumY[l] += Ml
        Ys.append(goodsofar)
    # barrier: Hit = exists l<=LSTAR: Gam_0..Gam_l and W_{n_{l+1}} <= -c ; and P_{n_{l+1}} nonempty for all l
    allalive = all(len(alive_at[nl[l + 1]]) > 0 for l in range(LSTAR + 1))
    for c in cs:
        H = any(Ys[l] and (nl[l + 1] - V[nl[l + 1]]) <= -c for l in range(LSTAR + 1))
        if H and allalive:
            hit[c] += 1
mu = 2.0 ** -k
print(f"{cname}: samples={SAMPLES}")
print(f"  Prop 11.26: int_(C cap Gamma*) Z_n0 ~ {mu*sumZ/SAMPLES:.4g}  (bound {I26})")
print("  E[Y_l 1_C] for l=0..%d:" % LSTAR, ["%.4g" % (mu * y / SAMPLES) for y in sumY])
EY0 = mu * sumY[0] / SAMPLES
for c in cs:
    p = mu * hit[c] / SAMPLES
    se = mu * (hit[c] ** 0.5) / SAMPLES
    print(f"  barrier c={c}: mu(C cap Hit cap alive) ~ {p:.4g} +- {se:.2g}  vs 2^-c E[Y0 1_C] = {2.0**-c*EY0:.4g}")
