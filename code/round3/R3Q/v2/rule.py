#!/usr/bin/env python3
"""Theorem C of the R3Q report: the fixed parameter rule R(K) (no search) and its exact evaluation.
Rule, for G = 2^K, M = floor(K/64):
  T = G - 2K - 12;  chain n_1 = 6M, n_{i+1} = n_i + floor(n_i/2) (i=1,2,3), n_U = n_4, Lam = beta(n_U) - 1;
  Theorem B: M* = Mf = M, n_s = n_U + 2M, m1 = 0, k = lratio_B(Lam, M) + z(n_s) + M;
  Theorem A (each class): n_s = 2M + 16, m1 = 0, k = lratio_A(lambda_C) + z(n_s) + M.
Prints the exact bound (log2) and the closed-form majorant of the report, and checks bound <= majorant <= 2^{-K/80}.
usage: rule.py K1 K2 step"""
import sys, math, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
import bounds as B
def params(K):
    M = K // 64; ch = [6 * M]
    for _ in range(3): ch.append(ch[-1] + ch[-1] // 2)
    return M, ch
def exact(K):
    G = 2 ** K; T = G - 2 * K - 12; M, ch = params(K)
    Lam = B.beta(ch[-1]) - 1; ns = ch[-1] + 2 * M
    kB = B.lratio_B(Lam, M) + B.z(ns) + M
    tB, info = B.thmB_terms(G, T, M, M, ch, ns, kB, 0)
    tot = sum(tB.values()); parts = dict(tB)
    for nm, (r, a, lam, nC) in B.CLASSES.items():
        nsA = 2 * M + 16; kA = B.lratio_A(lam) + B.z(nsA) + M
        tA, _ = B.thmA_terms(nm, G, T, nsA, kA, 0)
        for q, v in tA.items(): parts[nm + q] = v
        tot += sum(tA.values())
    return tot, parts, dict(M=M, chain=ch, Lam=Lam, ns=ns, kB=kB, Kt=info["K"])
def H(q): return -q * math.log2(q) - (1 - q) * math.log2(1 - q)
def majorant(K):
    """closed-form bound of the report (Theorem C proof), as log2; valid for K >= 2400."""
    M = K // 64
    terms = [math.log2(2 * M + 1) - M,                      # B2
             -2.125 * M + 2.05 + 6 * math.log2(20.25 * M),   # B3
             -2 * M + 2 * math.log2(22.25 * M + 1),          # B4
             -M - 3,                                         # B5 (second part)
             -0.0573 * (K - 5) - 4,                          # B5 (binomial, q <= 0.36)
             -M - 1,                                         # A5 (second parts, all classes)
             -0.5 * (K - 5) - 2,                             # A5 binomial (q <= 0.25, H(0.25) < 0.82)
             -2 * M - 7 + 2 * math.log2(2 * M + 17),         # A4 (three classes)
             -K + 1]                                         # A1 + B1
    mx = max(terms)
    return mx + math.log2(sum(2.0 ** (t - mx) for t in terms))
if __name__ == "__main__":
    K1, K2, st = map(int, sys.argv[1:4])
    for K in range(K1, K2 + 1, st):
        tot, parts, p = exact(K); le = math.log2(tot.numerator) - math.log2(tot.denominator)
        lm = majorant(K); big = max(parts, key=lambda q: parts[q])
        ok = le <= lm + 1e-9 and lm <= -K / 80
        print(f"RULE K={K} M={p['M']} chain={p['chain']} Lam={p['Lam']} ns={p['ns']} kB={p['kB']} Kt={p['Kt']}: "
              f"exact log2={le:.2f} (-/K={-le/K:.4f}; largest {big}) majorant log2={lm:.2f} vs -K/80={-K/80:.2f} {'OK' if ok else 'CHECK'}", flush=True)
def fmt_line(K):
    """the rule's parameters in the log format read by verify_bounds.py"""
    tot, parts, p = exact(K); M, ch = params(K); out = [f"K={K} delta<={float(tot):.4e}"]
    for nm, (r, a, lam, nC) in B.CLASSES.items():
        nsA = 2 * M + 16; out.append(f"{nm}=0(ns={nsA},k={B.lratio_A(lam) + B.z(nsA) + M},m1=0)")
    out.append(f"C14=0(M*={M},Mf={M},chain={ch},ns={p['ns']},k={p['kB']},m1=0)")
    return " ".join(out)
