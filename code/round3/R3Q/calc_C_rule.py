#!/usr/bin/env python3
"""Theorem C with FIXED parameter rules (no search), for the 'for all G >= G0' statement.

For G = 2^K the parameters are
   Lam = floor(ell*K),  n_U = max{n : beta(n) <= Lam+1},  M* = floor(mu*n_U),
   chain: backward rule  n_t = n_U,  n_{i-1} = least p with p + beta(p) - M* >= n_i (window [p, n_i]),
          continued while the start conditions hold; the start n_1 is the best prefix point,
   n_s = least even n >= n_U with beta(n) >= Lam + 1 + ceil(delta*K),
   k = floor(a*K).
The bound is evaluated EXACTLY (fractions) by calc_bounds.thmC_terms with this chain.
usage: calc_C_rule.py ell mu delta a Kmin Kmax step     -> exact bounds on a grid
       calc_C_rule.py opt K                              -> float optimisation of (ell,mu,delta,a) at K
"""
import sys, math
sys.path.insert(0, __import__("os").path.dirname(__file__))
from calc_bounds import (beta, beta2, s2, flog2, zexp, window_ok, window_phi, nU_of, thmC_terms,
                         log2_binom_cdf_float, lse, NofG)
from fractions import Fraction as Fr

from functools import lru_cache

@lru_cache(maxsize=None)
def rule_chain(nU, Ms):
    seq = [nU]
    while True:
        n = seq[-1]
        p = None
        for q in range(max(8, n // 2 - 4 - Ms), n):
            if q + beta(q) - Ms >= n and window_ok(q, n, Ms):
                p = q; break
        if p is None: break
        seq.append(p)
    seq.reverse()
    phis = [window_phi(seq[i], seq[i + 1], Ms) for i in range(len(seq) - 1)]
    best = None; tail = 0
    for i in range(len(seq) - 1, -1, -1):
        if i < len(seq) - 1: tail += phis[i]
        v = zexp(seq[i]) + tail
        if best is None or v < best[0]: best = (v, tuple(seq[i:]))
    return best

@lru_cache(maxsize=None)
def nU_c(Lam):
    return nU_of(Lam)

def params(K, ell, mu, delta, a):
    Lam = int(ell * K)
    nU = nU_c(Lam)
    Ms = int(mu * nU)
    ch = rule_chain(nU, Ms)
    target = Lam + 1 + math.ceil(delta * K)
    ns = nU + (nU % 2)
    while beta(ns) < target: ns += 2
    k = int(a * K)
    return Lam, ns, Ms, k, ch

def float_bound(K, ell, mu, delta, a):
    G = 2 ** K
    Lam, ns, Ms, k, ch = params(K, ell, mu, delta, a)
    v = thmC_terms(G, Lam, ns, Ms, k, exact=False, ch=ch)
    return v

if __name__ == "__main__":
    if sys.argv[1] == "opt":
        K = int(sys.argv[2])
        best = None
        for ell in [x / 1000 for x in range(150, 400, 10)]:
            for mu in [x / 1000 for x in range(30, 90, 5)]:
                for delta in [x / 1000 for x in range(6, 30, 2)]:
                    for a in [x / 1000 for x in range(300, 480, 5)]:
                        v = float_bound(K, ell, mu, delta, a)
                        if v is not None and (best is None or v < best[0]):
                            best = (v, ell, mu, delta, a)
        print("K", K, "best log2 bound", best[0], "exponent", -best[0] / K, "params", best[1:])
    else:
        ell, mu, delta, a = (float(t) for t in sys.argv[1:5])
        Kmin, Kmax, step = (int(t) for t in sys.argv[5:8])
        for K in range(Kmin, Kmax + 1, step):
            G = 2 ** K
            Lam, ns, Ms, k, ch = params(K, ell, mu, delta, a)
            r = thmC_terms(G, Lam, ns, Ms, k, ch=ch)
            if r is None: print(K, "invalid"); continue
            t, info = r
            tot = sum(t)
            print(f"K={K:6d} bound={float(tot):.4e} log2={math.log2(tot):10.3f} exp={-math.log2(tot)/K:.5f} "
                  f"Lam={Lam} ns={ns} M*={Ms} k={k} nU={info[2]} chain={ch[1]} chainexp={ch[0]} terms="
                  + " ".join(f"{float(x):.2e}" for x in t), flush=True)
