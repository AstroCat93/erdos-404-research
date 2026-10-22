# Exact-ish (float64) C_k = p^k P(sum eta_n x_n == 0 mod p^k), x_n = n!/p^{v(N0!)}, n>=N0,
# compared level by level with the per-group bound of Thm 11.36(iv)+Lemma 11.37 and with Thm 11.38's
# product bound  prod_groups (1+Gamma_p(j)) (first partial group bounded by its own Gamma).
import sys, math, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from gamma_theta import stats
from fractions import Fraction

def vp(n, p):
    c = 0
    while n % p == 0: n //= p; c += 1
    return c
def vfact(n, p):
    c = 0; q = p
    while q <= n: c += n//q; q *= p
    return c

def run(p, N0, kmax, G):
    e0 = vfact(N0, p)
    q = p**kmax
    dist = np.zeros(q); dist[0] = 1.0
    # groups by level
    n = N0; groups = []
    while True:
        a = vfact(n, p) - e0
        if a >= kmax: break
        if groups and groups[-1][0] == a: groups[-1][1].append(n)
        else: groups.append((a, [n]))
        n += 1
    out = []; worst = 0.0
    Cprev = 1.0; logbound = 0.0
    for gi, (a, ns) in enumerate(groups):
        anext = groups[gi+1][0] if gi+1 < len(groups) else kmax
        for n in ns:
            x = (math.factorial(n)//p**e0) % q
            dist = 0.5*dist + 0.25*np.roll(dist, x) + 0.25*np.roll(dist, -x)
        # C at levels a+1..min(anext,kmax)
        Ca = Cprev
        for j in range(1, anext - a + 1):
            k = a + j
            if k > kmax: break
            Ck = p**k * dist[::p**k][:].sum() if False else p**k * dist[0::p**k].sum()
            # group bound: generic group (partial or full): Gamma of this group at depth j, computed directly
            xs = [(math.factorial(m)//p**e0)//p**a for m in ns]
            P0 = group_gamma(xs, p, j)
            ratio = Ck/Ca
            if ratio > (1+P0)*(1+1e-9): worst = max(worst, ratio/(1+P0)); print('VIOLATION 11.36(iv)', p, N0, a, j, ratio, 1+P0)
            # for full blocks also check Gamma_group == Gamma_p(j)
            if len(ns) == p and j in G and abs(P0 - float(G[j])) > 1e-12:
                print('VIOLATION 11.37(a)', p, N0, a, j, P0, G[j])
            out.append((k, Ck, a, j))
        logbound += math.log(1+group_gamma(xs, p, anext - a if anext <= kmax else kmax - a), p)
        Cprev = Ck
    return out, logbound

_cache = {}
def group_gamma(xs, p, j):
    q = p**j
    d = {0: 1.0}
    for x in xs:
        nd = {}
        for r, w in d.items():
            for s, ww in ((0, .5), (1, .25), (-1, .25)):
                rr = (r + s*x) % q; nd[rr] = nd.get(rr, 0) + w*ww
        d = nd
    return q*d.get(0, 0) - 1

if __name__ == '__main__':
    cases = [(2,1,22),(2,2,22),(2,3,22),(2,5,22),(2,7,22),(3,1,13),(3,2,13),(3,3,13),(3,4,13),(3,8,13),(3,9,13),
             (5,1,8),(5,3,8),(5,5,8),(5,7,8),(5,25,8),(7,1,7),(7,4,7),(7,7,7),(7,49,7),(11,1,5),(11,6,5),(13,1,5),(13,13,5)]
    Gs = {}
    for p, N0, kmax in cases:
        if p not in Gs: Gs[p] = {j: v for j, v in stats(p, 9 if p < 11 else 6)[1].items()}
        out, lb = run(p, N0, kmax, Gs[p])
        k, Ck, a, j = out[-1]
        print(f'p={p} N0={N0} k={k} C_k={Ck:.9g} log_p C_k={math.log(Ck,p):.6f} sum log_p(1+Gamma_group)={lb:.6f}', flush=True)
