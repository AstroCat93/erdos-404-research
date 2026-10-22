#!/usr/bin/env python3
"""What Corollary P1 does and does not say (exact arithmetic).
For each prime: (1) the range of G on which delta_G(p) is sandwiched,
B_p - (N-n0)p^-(T+1) <= delta_{v_p(N!)} <= delta_{G0} (census, exact), at eps = 0.01;
(2) the threshold G_vac beyond which the lower bound is <= 0 (vacuous): the bound
gives nothing about mu(K_p) = lim_G delta_G;
(3) for N - n0 <= p^(T+1) the events {v(x+i) >= T+1}, n0 < i <= N, are pairwise
disjoint, so the union bound in step (iii) is an equality for the measure of the
removed set (the bound's loss is not slack in the union bound itself)."""
from fractions import Fraction as F
import math
CERT = {7: [4,7,19,26,28,34], 11: [5,10,18,22,30,33], 13: [6,10,19,24,32,35,39],
        17: [5,11,16,25,30,34,43], 19: [5,12,17,27,31,35], 23: [7,12,18,23,33,37]}
CENSUS = {7: (8, 3596877), 11: (6, 1239663), 13: (5, 280157), 17: (4, 63219), 19: (4, 101379), 23: (3, 10417)}
def vfact(p, N):
    s, q = 0, p
    while q <= N:
        s += N // q; q *= p
    return s
for p, H in CERT.items():
    T, n0 = len(H), max(H)
    G0, cnt = CENSUS[p]
    d0 = F(cnt, p ** G0)
    b = sum(-(-n0 // p ** k) for k in range(1, 40) if p ** k <= n0)
    k1 = min(k for k in range(1, 40) if p ** k > n0)
    k0 = G0 - b + k1
    B = F(round(float(d0) * 1e5), 10 ** 5) - F(1, 10 ** 5) - F(n0, p ** k0)
    P = p ** (T + 1)
    Nvac = n0 + math.ceil(B * P)          # smallest N with loss >= B
    Gvac = vfact(p, Nvac)
    N1 = n0 + math.floor(F(1, 100) * P)
    # disjointness check of the gate events in (n0, N]: |i-i'| < p^(T+1) for N-n0 <= p^(T+1)
    disjoint = (N1 - n0) <= P
    print(f"p={p}: delta_G in [{float(B - F(N1 - n0, P)):.5f}, {float(d0):.5f}] for {G0} <= G <= {vfact(p, N1)}; "
          f"lower bound vacuous from G ~ {Gvac} (N = {Nvac}); gate events disjoint on the eps=0.01 range: {disjoint}; "
          f"mu(K_{p}) <= delta_G for all G, and the bound says nothing about lim delta_G")
