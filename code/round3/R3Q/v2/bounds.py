#!/usr/bin/env python3
"""Exact evaluation of the explicit bounds of data/round3/reports/R3Q.md (restarted R3Q track).
Floating point is used only to SEARCH parameters; the bound for the chosen parameters is recomputed in exact
rational arithmetic (Fraction, exact binomial sums) and that exact value is what is printed.
  Theorem A : classes C0 = 8Z_2 (slope 1), C2 = 2+16Z_2, C6 = 6+16Z_2 (slope 3)  -> terms A1, A4, A5
  Theorem B : class C14 = 14+16Z_2                                               -> terms B1..B5
usage: bounds.py A|B|D K1 K2 step      (G = 2^K; D prints the total bound for delta_G(2))"""
import sys, math
from fractions import Fraction as Fr
def s2(n): return bin(n).count("1")
def flog2(n): return n.bit_length() - 1
def beta(n): return n - s2(n) - flog2(n)
def z(n): return (n + 1) // 2 - 1                      # Lemma 4: Z_n <= 2^{z(n)}
def lrmin(lam): return -flog2(2 * lam)                # Lemma 6: rho >= 2^{lrmin}
def bin_lt(K, k):                                     # P(Bin(K,1/2) < k), exact
    if k <= 0: return Fr(0)
    if K <= 0: return Fr(1)
    return Fr(sum(math.comb(K, i) for i in range(min(k, K + 1))), 2 ** K)
def lbin_lt(K, k):                                    # log2 of an upper bound of the same (search only)
    if k <= 0: return -1e9
    if K <= 0 or 2 * (k - 1) >= K: return 0.0
    kk = k - 1
    lc = (math.lgamma(K + 1) - math.lgamma(kk + 1) - math.lgamma(K - kk + 1)) / math.log(2)
    return min(0.0, lc - K + math.log2((K - kk + 1) / (K - 2 * kk + 1)))
def mu_one(r, a, i, b):
    """mu{x in r + 2^a Z_2 : v(x+i) >= b}, exact."""
    if b <= 0: return Fr(1, 2 ** a)
    if b <= a: return Fr(1, 2 ** a) if (r + i) % (1 << b) == 0 else Fr(0)
    return Fr(1, 2 ** b) if (r + i) % (1 << a) == 0 else Fr(0)
def cnt_res(i0, i1, res, mod):                        # #{i0 <= i <= i1 : i = res mod mod}
    if i1 < i0: return 0
    f = lambda t: (t - res) // mod
    return f(i1) - f(i0 - 1)
def mu_const(r, a, i0, i1, b):
    """sum_{i0<=i<=i1} mu{x in C : v(x+i) >= b} for constant b > a, exact (union bound)."""
    return cnt_res(i0, i1, (-r) % (1 << a), 1 << a) * Fr(1, 2 ** b)
def mu_fail(r, a, i0, i1, lam):
    """sum_{i0<=i<=i1} mu{x in C : v(x+i) >= beta(i-1) - lam + 1}; thresholds nondecreasing in i."""
    tot = Fr(0); i = i0
    while i <= i1 and i < i0 + 3000:
        tot += mu_one(r, a, i, beta(i - 1) - lam + 1); i += 1
    if i <= i1:   # tail: beta(i-1) >= i - 2 - 2log2(i-1), so term <= 2^{lam+1} (i-1)^2 2^{-i}; ratio <= 0.51 (i >= 100)
        assert i >= 100
        tot += Fr(41, 20) * (i - 1) ** 2 * Fr(2) ** (lam + 1 - i)
    return tot
def t5(muC, a, lowbits, K, k, m1, lratio, zs):
    """martingale term: muC * [P(Bin(K-m1) < k) + 2^{1-k+lratio+zs} 2^{-lowbits} (3/4)^{m1-a}] (m1 >= a),
       or (m1 = 0) muC * [P(Bin(K-a) < k - lowbits) + 2^{1-k+lratio+zs}]."""
    if m1 == 0: return muC * (bin_lt(K - a, k - lowbits) + Fr(2) ** (1 - k + lratio + zs))
    return muC * (bin_lt(K - m1, k) + Fr(2) ** (1 - k + lratio + zs - lowbits) * Fr(3, 4) ** (m1 - a))
def l5(a, lowbits, K, k, m1, lratio, zs):
    if m1 == 0: return max(lbin_lt(K - a, k - lowbits), 1 - k + lratio + zs) - a
    return max(lbin_lt(K - m1, k), 1 - k + lratio + zs - lowbits + (m1 - a) * math.log2(0.75)) - a
def f_fail(r, a, i0, i1, lam):
    """float version of mu_fail (search only)."""
    tot = 0.0; i = i0
    while i <= i1 and i < i0 + 3000:
        b = beta(i - 1) - lam + 1
        if b <= a: tot += 2.0 ** -a if (r + i) % (1 << max(b, 0)) == 0 else 0.0
        elif (r + i) % (1 << a) == 0: tot += 2.0 ** -b
        if b > 1100 or (b > a and tot > 0 and 2.0 ** -b < tot * 1e-18): break
        i += 1
    return tot
def lse(*xs):
    m = max(xs); return m + math.log2(sum(2.0 ** (x - m) for x in xs))
# ------------------------------------------------------------------------------ Theorem A
CLASSES = {"C0": (0, 3, 1, 6), "C2": (2, 4, 3, 8), "C6": (6, 4, 3, 10)}   # r, a, slope lambda_C, n_C
def lratio_A(lam): return 0 if lam == 1 else (lam - 1) - lrmin(lam)    # log2(rho_max/rho_min), rho_max <= 2^{lam-1}
def thmA_terms(name, G, T, ns, k, m1):
    r, a, lam, nC = CLASSES[name]; muC = Fr(1, 2 ** a)
    assert ns >= nC and beta(ns) >= lam + 1 and T <= G and (m1 == 0 or a <= m1 <= ns - s2(ns))
    K = flog2(T - ns - 2 * lam)
    A1 = mu_const(r, a, 1, T, G - T + 3)
    A4 = mu_fail(r, a, ns + 1, T, lam)
    A5 = t5(muC, a, s2((r + ns) % (1 << a)), K, k, m1, lratio_A(lam), z(ns))
    return dict(A1=A1, A4=A4, A5=A5), K
def best_A(name, G):
    r, a, lam, nC = CLASSES[name]; T = G - 2 * flog2(G) - 12; best = None
    for ns in range(nC, nC + 120):
        if beta(ns) < lam + 1: continue
        K = flog2(T - ns - 2 * lam); lb = s2((r + ns) % (1 << a)); m0 = ns - s2(ns)
        f4 = f_fail(r, a, ns + 1, T, lam); l4 = math.log2(f4) if f4 > 0 else -1e9
        for m1 in [0] + list(range(a, min(m0, K) + 1)):
            for k in range(1, K):
                v = lse(l4, l5(a, lb, K, k, m1, lratio_A(lam), z(ns)))
                if best is None or v < best[0]: best = (v, ns, k, m1)
    _, ns, k, m1 = best
    terms, K = thmA_terms(name, G, T, ns, k, m1)
    return min(sum(terms.values()), Fr(1, 2 ** a)), dict(T=T, ns=ns, k=k, m1=m1, K=K), terms
# ------------------------------------------------------------------------------ Theorem B
def window_ok(n, N, Ms):   # (W1) beta(n) >= 2M*+1, (W2) L + 2M* <= beta(n)+1, (W3) beta(N) <= 2 beta(n)
    return N > n and beta(n) >= 2 * Ms + 1 and (N - n) + 2 * Ms <= beta(n) + 1 and beta(N) <= 2 * beta(n)
def phi(n, N, j):          # Lemma 8 exponent with m' <= n - 2
    L = N - n
    return L - (L - 1) // 2 - max(0, beta(N) - (n - 2) - 1 - j)
def b3_exact(seq, Ms):     # sum_{J=4}^{M*} mu(C14, v(x+2)=J) 2^{z(n_1) + sum_i phi_J}
    return sum(Fr(2) ** (-J - 1 + z(seq[0]) + sum(phi(seq[i], seq[i + 1], J) for i in range(len(seq) - 1)))
               for J in range(4, Ms + 1))
def b3_log(seq, Ms):
    ex = [-J - 1 + z(seq[0]) + sum(phi(seq[i], seq[i + 1], J) for i in range(len(seq) - 1)) for J in range(4, Ms + 1)]
    return lse(*ex) if ex else -1e9
def chain_for(nU, Ms):
    seq = [nU]
    while True:
        N = seq[-1]; p = next((q for q in range(max(2, N // 3), N) if window_ok(q, N, Ms)), None)
        if p is None: break
        seq.append(p)
    seq.reverse()
    return min(((b3_log(seq[i:], Ms), seq[i:]) for i in range(len(seq))), key=lambda t: t[0])
def lratio_B(Lam, Mf):     # log2(rho_max/rho_min): rho_max <= 2^{min(Lam-1, (Lam+Mf)/2-1)} (integer ceiling)
    return min(Lam - 1, -(-(Lam + Mf) // 2) - 1) - lrmin(Lam)
def thmB_terms(G, T, Ms, Mf, seq, ns, k, m1):
    r, a = 14, 4; muC = Fr(1, 16); nU = seq[-1]; Lam = beta(nU) - 1
    assert all(window_ok(seq[i], seq[i + 1], Ms) for i in range(len(seq) - 1))
    assert ns >= nU and beta(ns) >= Lam + 1 and T <= G and Mf >= Ms and (m1 == 0 or a <= m1 <= ns - s2(ns))
    K = flog2(T - ns - 2 * Lam)
    B1 = mu_const(r, a, 1, T, G - T + 3)
    B2 = mu_const(r, a, 1, nU, Ms + 1) + mu_const(r, a, nU + 1, ns + 2 * Lam, Mf + 1)
    B3 = b3_exact(seq, Ms)
    B4 = mu_fail(r, a, ns + 1, T, Lam)
    B5 = t5(muC, a, s2((r + ns) % 16), K, k, m1, lratio_B(Lam, Mf), z(ns))
    return dict(B1=B1, B2=B2, B3=B3, B4=B4, B5=B5), dict(K=K, Lam=Lam)
def best_B(G):
    KG = flog2(G); T = G - 2 * KG - 12; best = None
    for Ms in range(6, max(8, KG // 8), max(1, KG // 160)):
        for nU in range(4 * Ms + 8, max(4 * Ms + 9, int(0.7 * KG)), max(1, KG // 60)):
            ch = chain_for(nU, Ms)
            if ch[0] > -4: continue
            Lam = beta(nU) - 1; l2a = math.log2(nU / 16 + 1) - Ms - 1
            for dns in range(8, 64, 8):
                ns = nU
                while beta(ns) < Lam + dns: ns += 1
                K = flog2(max(2, T - ns - 2 * Lam)); lb = s2((14 + ns) % 16); m0 = ns - s2(ns)
                f4 = f_fail(14, 4, ns + 1, T, Lam); l4 = math.log2(f4) if f4 > 0 else -1e9
                for Mf in (Ms, Ms + 5, Ms + 10):
                    l2 = max(l2a, math.log2((ns + 2 * Lam) / 16 + 1) - Mf - 1); lr = lratio_B(Lam, Mf)
                    base = lse(l2, ch[0], l4)
                    for m1 in [0] + list(range(4, min(m0, K) + 1, max(1, m0 // 5))):
                        k0 = max(1, int(lr + z(ns) - 0.415 * max(0, m1 - 4)) - 6)
                        for k in range(k0, K):
                            v5 = l5(a=4, lowbits=lb, K=K, k=k, m1=m1, lratio=lr, zs=z(ns))
                            v = lse(base, v5)
                            if best is None or v < best[0]: best = (v, Ms, Mf, ch[1], ns, k, m1)
                            if lbin_lt(K - max(m1, 4), k) - 4 > v + 1: break
    if best is None: return None
    _, Ms, Mf, seq, ns, k, m1 = best
    terms, info = thmB_terms(G, T, Ms, Mf, seq, ns, k, m1)
    return min(sum(terms.values()), Fr(1, 16)), dict(T=T, Ms=Ms, Mf=Mf, chain=seq, ns=ns, k=k, m1=m1, **info), terms
if __name__ == "__main__":
    w = sys.argv[1]; K1, K2, st = map(int, sys.argv[2:5])
    for KG in range(K1, K2 + 1, st):
        G = 2 ** KG; out = []
        if w in "AD":
            totA = Fr(0)
            for nm in CLASSES:
                b, p, t = best_A(nm, G); totA += b
                out.append(f"{nm}={float(b):.4e}(ns={p['ns']},k={p['k']},m1={p['m1']})")
        if w in "BD":
            res = best_B(G)
            bB = res[0] if res else Fr(1, 16)
            if res:
                p, t = res[1], res[2]
                out.append(f"C14={float(bB):.4e}(M*={p['Ms']},Mf={p['Mf']},chain={p['chain']},ns={p['ns']},k={p['k']},m1={p['m1']},K={p['K']},Lam={p['Lam']}; "
                           + ",".join(f"{q}={float(v):.1e}" for q, v in t.items()) + ")")
        if w == "D":
            tot = totA + bB
            out.insert(0, f"delta<={float(tot):.4e} (log2 {math.log2(tot):.2f}; -log2/K={-math.log2(tot)/KG:.4f})")
        print(f"K={KG}", " ".join(out), flush=True)
