#!/usr/bin/env python3
"""Theorem C with the ANALYTIC parameter rule (report, Theorem C(ii)), exact evaluation and closed form.

Rule, for G = 2^K (K integer), constants ell, a, delta (fractions):
   Lam = floor(ell*K);  n_U = max{n : beta(n) <= Lam+1};  M* = floor(n_U/64);
   S   = 16 M* + 16 ceil(log2 n_U) + 24;
   chain: n_t = n_U, n_{i-1} = ceil(2 n_i / 3), stop at the last point >= S  (= n_1);
   n_s = least even n >= n_U with beta(n) >= Lam + 1 + ceil(delta*K);   k = floor(a*K).
Exact value: calc_bounds.thmC_terms with this chain (exponent recomputed with window_phi).
Closed form (report, proof of Theorem C(ii)):
   log2 TC2 <= log2(n_U) - n_U/64,   log2 TC4 <= -2 + 0.75 S + 1 - n_U/4 ... (see report), etc.
usage: calc_C_analytic.py ell a delta Kmin Kmax step
"""
import sys, math
sys.path.insert(0, __import__("os").path.dirname(__file__))
from fractions import Fraction as Fr
from calc_bounds import beta, zexp, window_ok, window_phi, nU_of, thmC_terms

def analytic_chain(nU, Ms):
    S = 16 * Ms + 16 * math.ceil(math.log2(nU)) + 24
    seq = [nU]
    while True:
        p = -(-2 * seq[-1] // 3)          # ceil(2n/3)
        if p < S or p >= seq[-1]: break
        seq.append(p)
    seq.reverse()
    if seq[0] < S: return None
    ok = all(window_ok(seq[i], seq[i + 1], Ms) for i in range(len(seq) - 1))
    if not ok: return "invalid"
    expo = zexp(seq[0]) + sum(window_phi(seq[i], seq[i + 1], Ms) for i in range(len(seq) - 1))
    return (expo, tuple(seq))

def run(ell, a, delta, K):
    G = 2 ** K
    Lam = int(ell * K)
    nU = nU_of(Lam)
    Ms = nU // 64
    ch = analytic_chain(nU, Ms)
    if ch is None or ch == "invalid": return None, ch
    target = Lam + 1 + math.ceil(delta * K)
    ns = nU + (nU % 2)
    while beta(ns) < target: ns += 2
    k = int(a * K)
    r = thmC_terms(G, Lam, ns, Ms, k, ch=ch)
    return r, (Lam, nU, Ms, ns, k, ch)

if __name__ == "__main__":
    ell, a, delta = (Fr(t) for t in sys.argv[1:4])
    Kmin, Kmax, step = (int(t) for t in sys.argv[4:7])
    for K in range(Kmin, Kmax + 1, step):
        r, info = run(ell, a, delta, K)
        if r is None:
            print(K, "no valid chain", info); continue
        t, _ = r
        tot = sum(t)
        Lam, nU, Ms, ns, k, ch = info
        print(f"K={K:7d} bound={float(tot):.4e} log2={math.log2(tot):11.3f} exp={-math.log2(tot)/K:.5f} "
              f"target(K/256)={-K/256:.2f} Lam={Lam} nU={nU} M*={Ms} ns={ns} k={k} chainlen={len(ch[1])} "
              f"chainexp={ch[0]} terms=" + " ".join(f"{float(x):.2e}" for x in t), flush=True)
