"""Referee re-evaluation of Corollary 11.30 constants (own code; T2's constants*.py and the lead's
lead_t2_constants.py not read).  Theorem 11.29 bound:
 mu(C & g>=G) <= B_L(n0) + n0 2^-K + 2^-c E_C + 2^-k P(Bin(K-k,1/2) <= c+s_L-s(r0))
 n0 = ceil(4 log2 G)+3L+40, c = floor(a(K-k)) - s_L + s(r0), a=0.227,
 T=floor(G/2), K=floor(log2(T-l0+1)), h_L(n)=(n-log2 n-3L-4)/2,
 B_L(n0)=sum_{i>=1} 2^{-floor(h_L(max(n0,i-l0)))-1}."""
import mpmath as mp
from math import comb
mp.mp.dps = 60
a = mp.mpf('0.227')
classes = {'C0': dict(k=3, r0=0, L=1, l0=4, sL=2, EC=1, mu=mp.mpf(1)/8),
           'C2': dict(k=3, r0=2, L=3, l0=8, sL=3, EC=64, mu=mp.mpf(1)/8),
           'C6': dict(k=4, r0=6, L=6, l0=14, sL=3, EC=16384, mu=mp.mpf(1)/16)}
def s2(n): return bin(n).count('1')
def ceil4log2(G):  # smallest m with 2^m >= G^4
    G4 = G ** 4; m = G4.bit_length() - 1
    return m if (1 << m) >= G4 else m + 1
def floorlog2(n): return n.bit_length() - 1
def h(n, L): return (n - mp.log(n, 2) - 3 * L - 4) / 2
def BL(n0, L, l0):
    # i = 1..n0+l0 : max(n0, i-l0) = n0 ; i > n0+l0 : n = i - l0 > n0
    t = (n0 + l0) * mp.mpf(2) ** (-mp.floor(h(n0, L)) - 1)
    n = n0 + 1
    while True:
        term = mp.mpf(2) ** (-mp.floor(h(n, L)) - 1)
        t += term
        if term < mp.mpf(10) ** -45 and n > n0 + 50: break
        n += 1
    # tail bound: h(n) >= n/2 - log2(n)/2 - ..., terms decay geometrically ~2^{-n/2}; remaining < 4*term
    return t
# main term constants
print("main-term constants (2^{1+sL-s(r0)} E_C + 2^-k) 2^{a k} 8^a:")
for nm, d in classes.items():
    m = (mp.mpf(2) ** (1 + d['sL'] - s2(d['r0'])) * d['EC'] + mp.mpf(2) ** (-d['k'])) * mp.mpf(2) ** (a * d['k']) * mp.mpf(8) ** a
    d['main'] = m
    print(" ", nm, mp.nstr(m, 8))
print("check 1-H2(0.227) =", mp.nstr(1 - (-(a * mp.log(a, 2) + (1 - a) * mp.log(1 - a, 2))), 8))
def bound(G, d):
    k, L, l0 = d['k'], d['L'], d['l0']
    T = G // 2
    K = floorlog2(T - l0 + 1)
    n0 = ceil4log2(G) + 3 * L + 40
    assert T >= n0 + l0 and (1 << K) >= l0 and K > k, (G, T, n0, K)
    c = int(mp.floor(a * (K - k))) - d['sL'] + s2(d['r0'])
    side = BL(n0, L, l0) + n0 * mp.mpf(2) ** (-K)
    thr = c + d['sL'] - s2(d['r0'])
    N = K - k
    binom = mp.mpf(sum(comb(N, i) for i in range(0, max(-1, min(thr, N)) + 1))) / mp.mpf(2) ** N
    full = side + mp.mpf(2) ** (-c) * d['EC'] + mp.mpf(2) ** (-k) * binom
    return side, full, n0, K
# candidate right endpoints
for nm, d in classes.items():
    cands = set([2 ** 400])
    for m in range(40, 1601 + 1):
        # largest G with ceil(4log2 G) = m  -> G^4 <= 2^m -> G = floor(2^(m/4))
        import math as _m
        G = _m.isqrt(_m.isqrt(2 ** m))  # floor of 4th root, exact
        assert G ** 4 <= 2 ** m < (G + 1) ** 4
        if 2 ** 10 <= G <= 2 ** 400: cands.add(G)
    for K in range(5, 402):
        T = (1 << (K + 1)) + d['l0'] - 2
        for G in (2 * T + 1, 2 * T - 1, 2 * T):
            if 2 ** 10 <= G <= 2 ** 400: cands.add(G)
    best_side = (0, None); best_full = (0, None); best_min = (0, None)
    for G in sorted(cands):
        side, full, n0, K = bound(G, d)
        ga = mp.mpf(G) ** a
        if side * ga > best_side[0]: best_side = (side * ga, G)
        if full * ga > best_full[0]: best_full = (full * ga, G)
        mm = min(d['mu'], full) * ga
        if mm > best_min[0]: best_min = (mm, G)
    print(f"{nm}: sup side*G^a = {mp.nstr(best_side[0], 6)} at G~2^{mp.nstr(mp.log(best_side[1], 2), 5)}; "
          f"main+side = {mp.nstr(d['main'] + best_side[0], 8)}; sup min(mu,full)*G^a = {mp.nstr(best_min[0], 6)} "
          f"at G~2^{mp.nstr(mp.log(best_min[1], 2), 5)}; sup full*G^a={mp.nstr(best_full[0], 6)}")
print("G<=2^10: mu(C)<=1/8 vs 0.61*G^-a at G=2^10:", mp.nstr(mp.mpf('0.61') * mp.mpf(1024) ** (-a), 6))
# where does the bound beat trivial mu(C)?
for nm, d in classes.items():
    for e in range(10, 120):
        side, full, n0, K = bound(2 ** e, d)
        if full < d['mu']:
            print(f"{nm}: full RHS (this n0, c choice) first < mu(C) at G=2^{e}"); break
