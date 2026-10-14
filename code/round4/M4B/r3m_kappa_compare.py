#!/usr/bin/env python3
"""r3m_kappa_compare.py -- exact predictions of Corollary B2' (gate at distance d = 1 from the window start)
for the deep-gate experiment of round 3 (R3M, data/round3/R3M/eps_gate_depth.log, p = 3, d = 1):
   eps = (p^s/2) * eps_post,  and eps_post -> eps_fact (factorial window) as s -> infinity,
with eps_fact computed exactly from the elements 0!, 1!, ..., (L+L'-1)!.  R3M's logged medians are quoted
for comparison (they are float values from 8 random samples per depth).
usage: r3m_kappa_compare.py
"""
from fractions import Fraction

from m4b_lib import unsigned_dist, fold, sumsq


def vf(n, p):
    s, q = 0, p
    while q <= n:
        s += n // q
        q *= p
    return s


def efact(p, L, L2):
    T = L + L2
    f = [1]
    for c in range(1, T):
        f.append(f[-1] * c)
    D, K = vf(L, p), vf(T, p)
    m = unsigned_dist(f, p ** K)
    return p ** K * Fraction(sumsq(m), 4 ** T) - p ** D * Fraction(sumsq(fold(m, p ** D)), 4 ** T)


rows = [((16, 21, 26), "4.59 13.8 41.3"), ((24, 32, 40), "4.12 12.5 38"), ((32, 42, 52), "0.511 1.82 4.75")]
for (n, N, N2), r3m in rows:
    L, L2 = N - n - 1, N2 - N
    e = efact(3, L, L2)
    K_post = vf(L + L2, 3)
    pred = [float(3 ** s * e / 2) for s in (4, 5, 6)]
    print(f"ROW p=3 window [{n},{N2}) split {N}, gate at d=1: eps_fact(post lengths {L},{L2})={float(e):.6g} "
          f"(K_post={K_post}); s->infinity prediction (p^s/2)eps_fact at s=4,5,6: "
          + " ".join(f"{v:.4g}" for v in pred) + f" | R3M medians: {r3m}")
