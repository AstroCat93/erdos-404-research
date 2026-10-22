# Independent numerical test of Cor 11.39 / Thm 11.36 / Thm 11.38 / Lemma 11.35(c) / Lemma 11.37(a)
# on small p, N0, depth k.  float64 probabilities (errors ~1e-15 relative), all inequalities checked with tol.
# usage: python3 l2check.py p N0 K   [random]   (random: replace factorials by random x_n with the same valuations)
import sys, math, random
import numpy as np
from math import factorial

def vp(n, p):
    c = 0
    while n % p == 0 and n:
        n //= p; c += 1
    return c

def vfact(n, p):
    s, q = 0, p
    while q <= n:
        s += n // q; q *= p
    return s

def run(p, N0, K, rand=False, seed=1):
    mod = p**K
    e0 = vfact(N0, p)
    xs = []   # (n, x_n mod p^K, level)
    n = N0
    rng = random.Random(seed)
    while True:
        lev = vfact(n, p) - e0
        if lev >= K: break
        if rand:
            u = rng.randrange(1, p**(K-lev+1))
            while u % p == 0: u = rng.randrange(1, p**(K-lev+1))
            x = (u * p**lev) % mod
        else:
            # n!/p^e0 mod p^K, exact
            x = (factorial(n) // p**e0) % mod
        xs.append((n, x, lev))
        n += 1
    # distribution of Z mod p^K
    P = np.zeros(mod); P[0] = 1.0
    for (_, x, _) in xs:
        P = 0.5*P + 0.25*np.roll(P, x) + 0.25*np.roll(P, -x)
    C = [1.0]
    for j in range(1, K+1):
        C.append(p**j * P[::p**j].sum() if p**j < mod else p**K * P[0])
    # Gamma_p(j) exact via integer law of W
    e = [(-1)**u * factorial(p-1)//factorial(u) for u in range(p)]
    dist = {0: 1}
    for x in e:
        nd = {}
        for w, c in dist.items():
            for s, wt in ((-1, 1), (0, 2), (1, 1)):
                nd[w+s*x] = nd.get(w+s*x, 0)+c*wt
        dist = nd
    _gc = {}
    def Gam(j):
        if j not in _gc:
            _gc[j] = p**j*sum(c for w, c in dist.items() if w % p**j == 0)/4**p - 1
        return _gc[j]
    # level groups
    levels = sorted(set(l for (_, _, l) in xs))
    worst = 0.0; viol = []
    # Thm 11.36(iv) generic: factor C_{a+j}/C_a <= 1+Gamma_{G_a}(j) computed from the actual group
    for idx, a in enumerate(levels):
        J = (levels[idx+1] - a) if idx+1 < len(levels) else K - a
        grp = [x // p**a for (_, x, l) in xs if l == a]
        for j in range(1, J+1):
            if a + j > K: break
            m = p**j
            Q = np.zeros(m); Q[0] = 1.0
            for y in grp:
                y %= m
                Q = 0.5*Q + 0.25*np.roll(Q, y) + 0.25*np.roll(Q, -y)
            G = m*Q[0] - 1
            fac = C[a+j]/C[a]
            if fac > 1 + G + 1e-9: viol.append(("11.36(iv)", a, j, fac, 1+G))
            if fac < 1 - 1e-9: viol.append(("D<0", a, j, fac))
            if not rand and len(grp) == p:
                if abs(G - Gam(j)) > 1e-9: viol.append(("11.37(a) Gamma", a, j, G, Gam(j)))
    # Thm 11.38 product bound (no o(k) slack): log C_k <= log(first partial factor) + sum log(1+Gamma(J_m))
    res = []
    if not rand:
        for k in range(1, K+1):
            bound = 1.0
            for idx, a in enumerate(levels):
                if a >= k: break
                J = (levels[idx+1] - a) if idx+1 < len(levels) else 10**9
                j = min(J, k - a)
                grp = [x for (_, x, l) in xs if l == a]
                if len(grp) < p: bound *= p**j
                else: bound *= 1 + Gam(j)  # j=min(J,k-a) <= J; stronger than the proof's 1+Gamma(J)
            if C[k] > bound*(1+1e-9): viol.append(("11.38 product", k, C[k], bound))
            res.append((k, C[k], bound))
    # Lemma 11.35(c): T(k) <= sqrt(p^k (1-1/p)(C_k - C_{k-1})); and C_k - C_{k-1} == sum over ord p^k of prod cos^2
    for k in range(1, min(K, 7)+1):
        mk = p**k
        if mk > 3*10**6: break
        u = np.arange(mk); u = u[u % p != 0]
        logabs = np.zeros(len(u)); prod2 = np.ones(len(u))
        for (_, x, l) in xs:
            if l >= k: continue
            t = (u * (x % mk)) % mk
            c = np.abs(np.cos(np.pi * t / mk))
            prod2 *= c*c
            logabs += np.log(np.maximum(c, 1e-300))
        T = np.exp(logabs).sum(); S2 = prod2.sum()
        if abs(S2 - (C[k]-C[k-1])) > 1e-9*max(1, C[k]): viol.append(("Parseval", k, S2, C[k]-C[k-1]))
        if T > math.sqrt(mk*(1-1/p)*S2)*(1+1e-9): viol.append(("11.35c", k, T, math.sqrt(mk*(1-1/p)*S2)))  # S2 = C_k-C_{k-1} computed directly (no cancellation)
        if C[k]-C[k-1] > T + 1e-12: viol.append(("11.35c lower", k))
        res.append(("T", k, T, math.sqrt(mk*(1-1/p)*S2), S2, math.sqrt(mk*C[k])))
    return C, res, viol

if __name__ == "__main__":
    p, N0, K = map(int, sys.argv[1:4])
    rand = len(sys.argv) > 4
    seeds = range(1, 6) if rand else [1]
    for s in seeds:
        C, res, viol = run(p, N0, K, rand, s)
        print(f"p={p} N0={N0} K={K} rand={rand} seed={s}  C_k-1 =", " ".join(f"{c-1:.6g}" for c in C[1:]))
        for r in res:
            print("   ", r)
        print("   VIOLATIONS:", viol if viol else "none")
