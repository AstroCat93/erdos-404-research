# Test D: independent evaluation of the right side of Theorem 11.29 with the choices of
# Corollary 11.30, over every (n0,K)-interval of G in [2^10, 2^GMAXEXP], plus G in [2,2^10].
import sys
from mpmath import mp, mpf, log, floor, ceil, power
from math import comb
mp.dps = 60
alpha = mpf('0.227')
GMAXEXP = int(sys.argv[1]) if len(sys.argv) > 1 else 200

def H2(a):
    return -a * log(a, 2) - (1 - a) * log(1 - a, 2)
print("1-H2(0.227) =", 1 - H2(alpha))

def s(n): return bin(n).count('1')

CL = {'C0': dict(k=3, r0=0, L=1, l0=4, sL=2, E=1, claim=29),
      'C2': dict(k=3, r0=2, L=3, l0=8, sL=3, E=64, claim=1325),
      'C6': dict(k=4, r0=6, L=6, l0=14, sL=3, E=16384, claim=198000)}
for d in CL.values():
    assert d['sL'] == max(s(t) for t in range(d['l0']))

def hfloor(n, L):
    # floor((n - log2 n - 3L - 4)/2), exact enough at 60 digits (log2 n irrational unless power of 2)
    return int(floor((n - log(n, 2) - 3 * L - 4) / 2))

def B(n0, L, l0):
    tot = mpf(0)
    tot += (n0 + l0) * power(2, -hfloor(n0, L) - 1)
    i = n0 + l0 + 1
    # sum explicitly up to i where terms < 2^-400 relative, then bound the tail geometrically
    while True:
        t = power(2, -hfloor(i - l0, L) - 1)
        tot += t
        if t < power(2, -500) * tot:
            # remaining terms decrease at least like 2^{-(j)/2 + log} : bound tail crudely by 100*t*...
            tot += t * 64  # generous: after this point terms halve at least every 3 steps
            break
        i += 1
    return tot

def binom_tail(Nn, c):
    if c < 0: return mpf(0)
    return mpf(sum(comb(Nn, j) for j in range(0, min(c, Nn) + 1))) / mpf(2) ** Nn

def n0_of(G, L):
    return int(ceil(4 * log(G, 2))) + 3 * L + 40

def rhs(G, d):
    k, r0, L, l0, sL, E = d['k'], d['r0'], d['L'], d['l0'], d['sL'], d['E']
    T = G // 2
    n0 = n0_of(G, L)
    K = (T - l0 + 1).bit_length() - 1
    assert n0 >= 19 and T >= n0 + l0 and (1 << K) >= l0 and K > k, (G, n0, K)
    c = int(floor(alpha * (K - k))) - sL + s(r0)
    main1 = power(2, -c) * E
    main2 = power(2, -k) * binom_tail(K - k, c + sL - s(r0))
    side = B(n0, L, l0) + mpf(n0) / mpf(2) ** K
    return main1, main2, side, n0, K

for name, d in CL.items():
    L, l0 = d['L'], d['l0']
    # breakpoints: n0 changes when ceil(4 log2 G) changes; K changes when T-l0+1 crosses 2^K.
    pts = set()
    for j in range(40, 4 * GMAXEXP + 1):
        # ceil(4 log2 G) = j  <=>  2^{(j-1)/4} < G <= 2^{j/4}
        hi = int(floor(power(2, mpf(j) / 4)))
        for g in (hi - 1, hi, hi + 1):
            pts.add(g)
    for K in range(5, GMAXEXP + 2):
        g = 2 * ((1 << K) + l0 - 1)  # smallest G with T-l0+1 >= 2^K
        for gg in (g - 2, g - 1, g, g + 1):
            pts.add(gg)
    pts = sorted(p for p in pts if (1 << 10) <= p <= (1 << GMAXEXP))
    pts.append(1 << 10)
    best_full = best_main = best_side = mpf(0)
    worst_G = None
    for G in sorted(set(pts)):
        m1, m2, sd, n0, K = rhs(G, d)
        Ga = power(G, alpha)
        # check the corollary's chain: 2^K > G/8
        assert (1 << K) * 8 > G
        f = (m1 + m2 + sd) * Ga
        if f > best_full:
            best_full, worst_G = f, G
        best_main = max(best_main, (m1 + m2) * Ga)
        best_side = max(best_side, sd * Ga)
    print(f"{name}: sup over breakpoints of RHS*G^a = {mp.nstr(best_full,8)} at G~2^{mp.nstr(log(worst_G,2),6)}; sup main*G^a = {mp.nstr(best_main,8)}; sup side*G^a = {mp.nstr(best_side,6)}; claimed constant {d['claim']}; OK={best_full <= d['claim']}")
    # small G: trivial bound
    mu = mpf(1) / 2 ** d['k']
    print(f"   small G<=2^10: mu(C)={mu}, claim*G^-a at 2^10 = {mp.nstr(d['claim'] * power(1024, -alpha), 6)}")
print("sum of claimed constants:", sum(d['claim'] for d in CL.values()))
