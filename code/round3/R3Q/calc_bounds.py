#!/usr/bin/env python3
"""Exact evaluation of the explicit bounds of the R3Q report (Theorems B and C, Corollary D).

Search for parameters uses floating point (log2 domain); the bound for the chosen parameters is then
recomputed in exact rational arithmetic (fractions.Fraction) and that exact value is reported.

Theorem B (certified class C = r + 2^a Z_2 with uniform slope lam0 for v(S_e) >= c0):
   mu(x in C : g(x) >= G) / mu(C) <= T1 + T2 + T3 + T4      (report, Theorem B)
Theorem C (all of Z_2):
   delta_G(2) <= TC1 + TC2 + TC4 + TC6 + TC7 + TC8          (report, Theorem C)
usage:
   calc_bounds.py B r a c0 lam0 Kmin Kmax step
   calc_bounds.py D Kmin Kmax step          (Corollary D: 1/16 + class bounds)
   calc_bounds.py C Kmin Kmax step
"""
import sys, math
from fractions import Fraction as Fr
from functools import lru_cache

def s2(n): return bin(n).count("1")
def flog2(n): return n.bit_length() - 1
def clog2(n): return (n - 1).bit_length()
def beta(n): return n - s2(n) - flog2(n)            # Lemma 2(e): V_n - M_n >= beta(n); nondecreasing
def beta2(n): return n - s2(n) - 2 * flog2(n)       # Lemma 2(g); nondecreasing for n >= 2
def pow2(e): return Fr(2) ** e
def NofG(G): return G - clog2(G * G) - 3           # N = G - ceil(2 log2 G) - 3

@lru_cache(maxsize=None)
def binom_cdf(K, k):
    if k < 0: return Fr(0)
    k = min(k, K)
    return Fr(sum(math.comb(K, i) for i in range(k + 1)), 2 ** K)

def log2_binom_cdf_float(K, k):
    """log2 of an upper bound for P(Bin(K,1/2) <= k) (search only):
       for k < K/2: C(K,k) 2^{-K} (K-k+1)/(K-2k+1); otherwise 0."""
    if k < 0: return -1e18
    if 2 * k >= K: return 0.0
    lc = (math.lgamma(K + 1) - math.lgamma(k + 1) - math.lgamma(K - k + 1)) / math.log(2)
    return lc - K + math.log2((K - k + 1) / (K - 2 * k + 1))

def lse(xs):
    m = max(xs)
    return m + math.log2(sum(2.0 ** (x - m) for x in xs))

def zexp(n):   # Lemma 2(c): Z_n <= 2^{ceil(n/2)-1} for even x
    return (n + 1) // 2 - 1

# ------------------------------------------------------------------ Theorem B (certified class)
def classB_terms(G, r, a, c0, lam0, ns, k, exact=True):
    """r + 2^a Z_2, uniform slope lam0 on paths with v(S_e) >= c0 (certificate), ns multiple of 2^a."""
    N = NofG(G)
    if ns % (1 << a) or N - ns - 2 * lam0 < 16: return None
    # V_ns >= c0 for all x in the class and beta(ns) >= lam0 + a + 1
    if ns - s2(ns) < c0 or beta(ns) < lam0 + a + 1: return None
    K = flog2(N - ns - 2 * lam0)
    if K <= a: return None
    sr = s2(r % (1 << a))
    cnt1 = N // (1 << a) + 1          # T1: only i = -r mod 2^a can have v(x+i) >= a
    e1 = G - N + 1 - a
    ratio_log = 0.0 if lam0 <= 1 else lam0 + math.log2(4 * lam0)
    # Z_ns bound: Lemma 2(c): 2^{ns/2-2} on 8Z_2 (ns even >= 6), 2^{ceil(ns/2)-1} in general
    zx = ns // 2 - 2 if (r % 8 == 0 and a >= 3) else zexp(ns)
    first = ns + ((-r - ns - 1) % (1 << a))     # first n >= ns with n+1 = -r mod 2^a
    if not exact:
        t1 = math.log2(cnt1) - e1
        t2 = -(beta(first) - lam0 + 1 - a) + 0.05
        t3 = log2_binom_cdf_float(K - a, k - sr)
        t4 = ratio_log - k + zx
        return lse([t1, t2, t3, t4])
    T1 = Fr(cnt1) * pow2(-e1)
    T2 = Fr(0)                                   # failures of C_n (n >= ns)
    n = first
    while n < min(N, ns + 6000):
        T2 += pow2(-(beta(n) - lam0 + 1 - a))
        n += (1 << a)
    if n < N:   # tail: terms <= 2^{lam0 + a + 2 log2 n - n}, consecutive ratio <= 2^{-2^a+1} <= 1/2
        T2 += Fr(2) * pow2(lam0 + a - n) * Fr(n * n)
    T3 = binom_cdf(K - a, k - sr)                # s(z mod 2^K) <= k
    ratio = Fr(1) if lam0 <= 1 else pow2(lam0) * 4 * lam0
    T4 = ratio * pow2(-k) * pow2(zx)             # Markov at the stopping time
    return [T1, T2, T3, T4]

def best_classB(G, r, a, c0, lam0):
    K0 = flog2(G)
    cand = None
    step = 1 << a
    for ns in range(step, max(4 * step, K0 // 2 + 8 * step), step):
        for k in range(1, K0):
            v = classB_terms(G, r, a, c0, lam0, ns, k, exact=False)
            if v is not None and (cand is None or v < cand[0]):
                cand = (v, ns, k)
    if cand is None: return None
    _, ns, k = cand
    t = classB_terms(G, r, a, c0, lam0, ns, k)
    return (sum(t), ns, k, t)

CLASSES = [  # (r, a, c0, lam0, measure)  -- certificates: slope_cert.py
    (0, 3, 4, 1, Fr(1, 8)),
    (2, 4, 7, 3, Fr(1, 16)),
    (6, 4, 11, 3, Fr(1, 16)),
]

# ------------------------------------------------------------------ Theorem C
def window_ok(n, Np, Ms):
    L = Np - n
    if L < 1: return False
    lowV = n - s2(n)
    return (lowV >= max(4, 3 * Ms + 1)                 # (U0)
            and L + Ms <= min(beta(n), lowV - 1)       # (U1) with D <= L + Ms
            and Ms < beta2(n)                          # (U2)
            and beta(n) > 2 * Ms                       # (U3)
            and Ms < lowV                              # (U6)
            and beta(Np) <= 2 * lowV)                  # (U4) Theta_N <= 2m

def window_phi(n, Np, Ms):
    """Integer upper bound for log2 of the factor of Lemma 7 with Theta = beta:
       L - floor((L-1)/2) - max(0, beta(N') - m - 1 - kappa), m <= n - s(n) + M_n, M_n <= Ms, kappa <= Ms."""
    L = Np - n
    r = (L - 1) // 2
    gain = beta(Np) - (n - s2(n) + Ms) - 1 - Ms
    return L - r - max(0, gain)

def greedy_chain(nU, Ms):
    """Backward greedy chain ending at nU with maximal windows; best start along it."""
    lo = max(8, 3 * Ms + 2)
    seq = [nU]
    while True:
        n = seq[-1]
        p = None
        for q in range(max(lo, n // 2 - 4), n):
            if window_ok(q, n, Ms):
                p = q; break
        if p is None: break
        seq.append(p)
    seq.reverse()
    phis = [window_phi(seq[i], seq[i + 1], Ms) for i in range(len(seq) - 1)]
    best = None; tail = 0
    for i in range(len(seq) - 1, -1, -1):
        if i < len(seq) - 1:
            tail += phis[i]
        v = zexp(seq[i]) + tail
        if best is None or v < best[0]:
            best = (v, tuple(seq[i:]))
    return best

def nU_of(Lam):
    n = 8
    while beta(n + 1) <= Lam + 1:
        n += 1
    return n if beta(n) <= Lam + 1 else None

def thmC_terms(G, Lam, ns, Ms, k, exact=True, ch=None):
    N = NofG(G)
    if ns % 2 or ns < 8 or N - ns - 2 * Lam < 16: return None
    if Lam > beta(ns) - 1: return None
    K = flog2(N - ns - 2 * Lam)
    nU = nU_of(Lam)
    if nU is None or nU > ns: return None
    if ch is None: ch = greedy_chain(nU, Ms)
    if not exact:
        return lse([math.log2(N) - (G - N + 1), math.log2(nU) - (Ms + 1), -2 + ch[0],
                    -(beta(ns) - Lam + 1) + 1.05, -1 + log2_binom_cdf_float(K - 1, k),
                    1 + math.log2(Lam) - k + zexp(ns) + Lam])
    TC1 = Fr(N) * pow2(-(G - N + 1))             # M_N > G - N
    TC2 = Fr(nU) * pow2(-(Ms + 1))               # M_{n_U} > M*
    TC4 = Fr(1, 4) * pow2(ch[0])                 # U_{n_U} nonempty on the good set
    TC6 = Fr(0)                                  # failures of C_n, n >= ns
    n = ns
    while n < min(N, ns + 6000):
        e = beta(n) - Lam + 1
        TC6 += pow2(-e) if e > 0 else Fr(1)
        n += 1
    if n < N:   # tail: 2^{-(beta(n)-Lam+1)} <= 2^{Lam + 2 log2 n - n}; ratio <= 0.51
        TC6 += Fr(100, 49) * pow2(Lam - n) * Fr(n * n)
    TC7 = Fr(1, 2) * binom_cdf(K - 1, k)        # even x with s(z mod 2^K) <= k
    TC8 = Fr(1, 2) * 4 * Lam * pow2(-k) * pow2(zexp(ns) + Lam)   # Markov, rho_min >= 1/(4 Lam)
    return [TC1, TC2, TC4, TC6, TC7, TC8], (N, K, nU, ch)

def best_C(G):
    K0 = flog2(G)
    N = NofG(G)
    cand = None
    for Lam in range(16, max(32, int(0.5 * K0)), max(1, K0 // 150)):
        nU = nU_of(Lam)
        for Ms in range(2, max(4, int(0.25 * nU) + 2), max(1, nU // 100)):
            ch = greedy_chain(nU, Ms)
            if ch is None or ch[0] > 40: continue
            for dns in range(0, max(16, K0 // 4), max(2, 2 * (K0 // 300))):
                ns = nU + 4 + dns; ns += ns % 2
                if Lam > beta(ns) - 1 or N - ns - 2 * Lam < 16: continue
                KK = flog2(N - ns - 2 * Lam)
                base8 = 1 + math.log2(Lam) + zexp(ns) + Lam
                bestk = None
                for k in range(max(0, int(base8) - 5), KK):
                    t7 = -1 + log2_binom_cdf_float(KK - 1, k)
                    v = lse([t7, base8 - k])
                    if bestk is None or v < bestk[0]: bestk = (v, k)
                    if t7 > base8 - k + 3: break
                if bestk is None: continue
                v = lse([math.log2(N) - (G - N + 1), math.log2(nU) - (Ms + 1), -2 + ch[0],
                         -(beta(ns) - Lam + 1) + 1.05, bestk[0]])
                if cand is None or v < cand[0]:
                    cand = (v, Lam, ns, Ms, bestk[1], ch)
    if cand is None: return None
    _, Lam, ns, Ms, k, ch = cand
    t, info = thmC_terms(G, Lam, ns, Ms, k, ch=ch)
    return (sum(t), Lam, ns, Ms, k, t, info)

if __name__ == "__main__":
    which = sys.argv[1]
    if which == "B":
        r, a, c0, lam0, Kmin, Kmax, step = (int(t) for t in sys.argv[2:9])
        for K in range(Kmin, Kmax + 1, step):
            b = best_classB(2 ** K, r, a, c0, lam0)
            if b is None: print(K, "none"); continue
            tot, ns, k, t = b
            print(f"K={K:6d} bound={float(tot):.4e} log2={math.log2(tot):10.3f} exp={-math.log2(tot)/K:.4f} "
                  f"ns={ns} k={k} terms=" + " ".join(f"{float(x):.2e}" for x in t), flush=True)
    elif which == "D":
        Kmin, Kmax, step = (int(t) for t in sys.argv[2:5])
        for K in range(Kmin, Kmax + 1, step):
            G = 2 ** K
            tot = Fr(1, 16)
            parts = []
            for (r, a, c0, lam0, meas) in CLASSES:
                b = best_classB(G, r, a, c0, lam0)
                val = min(Fr(1), b[0]) if b is not None else Fr(1)
                parts.append(float(val)); tot += meas * val
            print(f"K={K:5d} G=2^{K}: delta_G(2) <= {float(tot):.5f}   class bounds (8Z,2+16Z,6+16Z) = "
                  + " ".join(f"{p:.4e}" for p in parts), flush=True)
    else:
        Kmin, Kmax, step = (int(t) for t in sys.argv[2:5])
        for K in range(Kmin, Kmax + 1, step):
            b = best_C(2 ** K)
            if b is None: print(K, "none"); continue
            tot, Lam, ns, Ms, k, t, info = b
            N, KK, nU, ch = info
            print(f"K={K:6d} bound={float(tot):.4e} log2={math.log2(tot):10.3f} exp={-math.log2(tot)/K:.4f} "
                  f"Lam={Lam} ns={ns} M*={Ms} k={k} nU={nU} chain={ch[1]} chainexp={ch[0]} terms="
                  + " ".join(f"{float(x):.2e}" for x in t), flush=True)
