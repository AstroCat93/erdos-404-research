#!/usr/bin/env python3
"""Independent exact re-evaluation of the explicit bounds of R3Q (data/round3/reports/R3Q.md), written from the
statements of Theorem A, Theorem B, Proposition 10 and Corollary D in the report (not from code/round3/R3Q).

Differences from the track's evaluator, on purpose:
  * the failure sums A_4/B_4 are summed exactly up to i = n_s + 6000 (or T), and the remainder is bounded by a
    dyadic-block geometric bound (beta(i-1) >= (i-1) - 2t - 1 on 2^t <= i-1 < 2^{t+1}), not by a ratio bound;
  * mu(C and v(x+i) >= b) is computed as 2^{-max(a,b)} [2^{min(a,b)} | r+i]  (b >= 1), mu(C) if b <= 0;
  * every side condition of the theorems is re-checked (windows (W1)-(W3), beta(n_s) >= Lam+1, ranges of m1, K_t).
usage:
  bounds_check.py table          re-derive every row of the report's tables from the logged parameters
  bounds_check.py ruleC K1 K2 st exact bound under the rule R(K) of Theorem C
  bounds_check.py ruleA K...     exact bound under the rule of Theorem A'
  bounds_check.py closed         closed-form checks of Theorems A' and C on their K ranges (+ side conditions)"""
import sys, re, math, glob, os
from fractions import Fraction as Fr

def s2(n): return bin(n).count("1")
def flog2(n): return n.bit_length() - 1
def beta(n): return n - s2(n) - flog2(n)
def z(n): return (n + 1) // 2 - 1
def ceil_div(a, b): return -((-a) // b)

def mu_cls(r, a, i, b):
    if b <= 0: return Fr(1, 1 << a)
    lo, hi = min(a, b), max(a, b)
    return Fr(1, 1 << hi) if (r + i) % (1 << lo) == 0 else Fr(0)

def count_cong(i0, i1, res, mod):
    """#{i0 <= i <= i1 : i = res (mod mod)}"""
    if i1 < i0: return 0
    first = i0 + ((res - i0) % mod)
    return 0 if first > i1 else (i1 - first) // mod + 1

def mu_const_sum(r, a, i0, i1, b):
    """sum_{i0<=i<=i1} mu(C and v(x+i) >= b), constant b."""
    if b <= 0: return Fr(max(0, i1 - i0 + 1), 1 << a)
    lo, hi = min(a, b), max(a, b)
    return Fr(count_cong(i0, i1, (-r) % (1 << lo), 1 << lo), 1 << hi)

def fail_sum(r, a, ns, T, lam, nexact=6000):
    """sum_{i=ns+1}^{T} mu(C and v(x+i) >= beta(i-1) - lam + 1): exact head, rigorous dyadic tail."""
    tot = Fr(0)
    i_end = min(T, ns + nexact)
    for i in range(ns + 1, i_end + 1):
        tot += mu_cls(r, a, i, beta(i - 1) - lam + 1)
    if i_end < T:
        # tail i >= A = i_end + 1: term <= 2^{-(i - 1 - 2t - lam)} with t = floor(log2(i-1)); valid since mu <= 2^{-b}
        A = i_end + 1
        t = flog2(A - 1)
        tail = Fr(0)
        # block t (partial), t+1, t+2 exactly, then t+3.. bounded by the t+2 block (ratio <= 1/2 for t >= 2)
        for tt in range(t, t + 3):
            start = max(A, (1 << tt) + 1); end = (1 << (tt + 1))       # i-1 in [2^tt, 2^{tt+1})
            # sum_{i=start}^{end} 2^{-(i-1-2tt-lam)} <= 2^{1+2tt+lam} * 2^{-start+1}
            tail += Fr(2) ** (2 + 2 * tt + lam - start)
        tail += Fr(2) ** (2 + 2 * (t + 2) + lam - ((1 << (t + 2)) + 1))   # geometric remainder (<= last block)
        assert t >= 4
        tot += tail
    return tot

def bin_lt(N, k):
    if k <= 0: return Fr(0)
    if N <= 0: return Fr(1)
    s = 0; c = 1
    for i in range(0, min(k, N + 1)):
        s += c; c = c * (N - i) // (i + 1)
    return Fr(s, 1 << N)

CLS = {"C0": (0, 3, 1, 6), "C2": (2, 4, 3, 8), "C6": (6, 4, 3, 10)}

def ell_C(lam): return 0 if lam == 1 else (lam - 1) + flog2(2 * lam)

def thmA(name, K, T, ns, k, m1):
    r, a, lam, nC = CLS[name]; G = 1 << K; muC = Fr(1, 1 << a)
    conds = [ns >= nC, beta(ns) >= lam + 1, T <= G, T >= 2, k >= 1, ns - s2(ns) >= a, ns >= 4]
    Kt = flog2(T - ns - 2 * lam)
    conds += [Kt >= a, ns + (1 << Kt) + 2 * lam <= T]
    if m1 != 0: conds += [a <= m1 <= min(ns - s2(ns), Kt)]
    if not all(conds): raise ValueError(f"Theorem A hypotheses fail for {name} K={K} {conds}")
    A1 = mu_const_sum(r, a, 1, T, G - T + 3)
    A4 = fail_sum(r, a, ns, T, lam)
    l0 = s2((r + ns) % (1 << a)); lc = ell_C(lam)
    if m1 == 0:
        A5 = muC * (bin_lt(Kt - a, k - l0) + Fr(2) ** (1 - k + lc + z(ns)))
    else:
        A5 = muC * (bin_lt(Kt - m1, k) + Fr(2) ** (1 - k + lc + z(ns) - l0) * Fr(3, 4) ** (m1 - a))
    return dict(A1=A1, A4=A4, A5=A5), Kt

def window_ok(n, N, Ms):
    L = N - n
    return N > n and beta(n) >= 2 * Ms + 1 and L + 2 * Ms <= beta(n) + 1 and beta(N) <= 2 * beta(n)

def phi(n, N, J):
    L = N - n
    return L - (L - 1) // 2 - max(0, beta(N) - n + 1 - J)

def thmB(K, T, Ms, Mf, chain, ns, k, m1):
    G = 1 << K; r, a = 14, 4; muC = Fr(1, 16)
    nU = chain[-1]; Lam = beta(nU) - 1
    conds = [Ms >= 4, Mf >= Ms, all(window_ok(chain[i], chain[i + 1], Ms) for i in range(len(chain) - 1)),
             ns >= nU, ns - s2(ns) >= 4, beta(ns) >= Lam + 1, T <= G, k >= 1, chain[0] >= 2, Lam >= 1]
    Kt = flog2(T - ns - 2 * Lam)
    conds += [Kt >= 4, ns + (1 << Kt) + 2 * Lam <= T]
    if m1 != 0: conds += [4 <= m1 <= min(ns - s2(ns), Kt)]
    if not all(conds): raise ValueError(f"Theorem B hypotheses fail K={K} {conds}")
    B1 = mu_const_sum(r, a, 1, T, G - T + 3)
    B2 = mu_const_sum(r, a, 1, nU, Ms + 1) + mu_const_sum(r, a, nU + 1, ns + 2 * Lam, Mf + 1)
    B3 = sum(Fr(2) ** (-J - 1 + z(chain[0]) + sum(phi(chain[i], chain[i + 1], J) for i in range(len(chain) - 1)))
             for J in range(4, Ms + 1))
    B4 = fail_sum(r, a, ns, T, Lam)
    lB = min(Lam - 1, ceil_div(Lam + Mf, 2) - 1) + flog2(2 * Lam)
    l0 = s2((14 + ns) % 16)
    if m1 == 0:
        B5 = muC * (bin_lt(Kt - 4, k - l0) + Fr(2) ** (1 - k + lB + z(ns)))
    else:
        B5 = muC * (bin_lt(Kt - m1, k) + Fr(2) ** (1 - k + lB + z(ns) - l0) * Fr(3, 4) ** (m1 - 4))
    return dict(B1=B1, B2=B2, B3=B3, B4=B4, B5=B5), dict(Kt=Kt, Lam=Lam)

def lg(q): return math.log2(q.numerator) - math.log2(q.denominator) if q > 0 else float("-inf")

def parse_line(line):
    K = int(re.match(r"K=(\d+)", line).group(1))
    out = {"K": K}
    for nm in ("C0", "C2", "C6"):
        m = re.search(nm + r"=[^(]*\(ns=(\d+),k=(\d+),m1=(\d+)\)", line)
        if m: out[nm] = tuple(map(int, m.groups()))
    m = re.search(r"C14=[^(]*\(M\*=(\d+),Mf=(\d+),chain=\[([\d, ]+)\],ns=(\d+),k=(\d+),m1=(\d+)", line)
    if m:
        out["C14"] = (int(m.group(1)), int(m.group(2)), [int(t) for t in m.group(3).split(",")],
                      int(m.group(4)), int(m.group(5)), int(m.group(6)))
    m = re.search(r"delta<=([0-9.e+-]+)", line)
    out["logged"] = float(m.group(1)) if m else None
    return out

def delta_bound(p):
    K = p["K"]; T = (1 << K) - 2 * K - 12
    parts = {}
    tot = Fr(0)
    for nm in ("C0", "C2", "C6"):
        ns, k, m1 = p[nm]
        t, _ = thmA(nm, K, T, ns, k, m1)
        b = min(sum(t.values()), Fr(1, 1 << CLS[nm][1]))
        parts[nm] = b; tot += b
    if "C14" in p:
        Ms, Mf, ch, ns, k, m1 = p["C14"]
        t, info = thmB(K, T, Ms, Mf, ch, ns, k, m1)
        b = min(sum(t.values()), Fr(1, 16)); parts["C14"] = b; parts["B_terms"] = t
    else:
        b = Fr(1, 16); parts["C14"] = b
    tot += b
    return tot, parts

# report table values (Corollary D table, §7) and Theorem A table (§4), as printed in the report
REPORT_D = {32: 0.1352, 36: 0.1059, 37: 0.1005, 38: 0.09606, 39: 0.0946, 40: 0.09103, 44: 0.07778, 48: 0.07085,
            56: 0.06492, 64: 0.06322, 96: 0.06253, 128: 0.0625, 192: 0.0625, 256: 0.0625, 320: 0.0625, 384: 0.0625,
            448: 0.04555, 512: 0.02055, 576: 0.008596, 640: 0.001901, 768: 0.0004322, 896: 4.291e-05,
            1024: 4.936e-06, 1280: 7.434e-08, 1536: 2.108e-09, 2048: 6.495e-13, 2560: 1.217e-15, 3072: 4.023e-20,
            3584: 8.752e-21, 4096: 1.394e-22}
REPORT_A = {32: (9.94e-3, 4.09e-2, 2.20e-2), 36: (7.09e-3, 2.40e-2, 1.24e-2), 40: (8.04e-3, 1.37e-2, 6.81e-3),
            48: (2.25e-3, 4.13e-3, 1.98e-3), 64: (2.01e-4, 3.47e-4, 1.76e-4), 448: (9.8e-25, 1.2e-24, 4.5e-24)}

def cmd_table():
    files = sorted(glob.glob(os.path.join(os.path.dirname(__file__), "../../../data/round3/R3Q/scan_D*.log")))
    rows = {}
    for f in files:
        for line in open(f):
            if line.startswith("K=") and "delta<=" in line:
                p = parse_line(line); rows[p["K"]] = p
    worst = 0
    for K in sorted(rows):
        p = rows[K]
        tot, parts = delta_bound(p)
        rep = REPORT_D.get(K)
        rel = abs(float(tot) / rep - 1) if rep else None
        if rel is not None: worst = max(worst, rel)
        extra = ""
        if "B_terms" in parts:
            extra = " B: " + ",".join(f"{q}=2^{lg(v):.2f}" for q, v in parts["B_terms"].items())
        print(f"K={K}: delta <= {float(tot):.6e} (2^{lg(tot):.4f}); report {rep}; rel.diff {rel:.2e}; "
              f"C0={float(parts['C0']):.4e} C2={float(parts['C2']):.4e} C6={float(parts['C6']):.4e} C14={float(parts['C14']):.4e}{extra}", flush=True)
        if K in REPORT_A:
            ra = REPORT_A[K]
            print(f"   Thm A table check K={K}: " + " ".join(
                f"{nm}: ours {float(parts[nm]):.4e} report {ra[i]:.3g} ({'ok' if abs(float(parts[nm]) / ra[i] - 1) < 6e-3 else 'MISMATCH'})"
                for i, nm in enumerate(("C0", "C2", "C6"))))
    print(f"worst relative difference to the report's Corollary D table: {worst:.2e}")
    # monotone staircase consistency: the report says each row also bounds larger G
    ks = sorted(rows); vals = [float(delta_bound(rows[K])[0]) for K in ks]
    print("staircase non-increasing in K:", all(vals[i + 1] <= vals[i] * (1 + 1e-12) for i in range(len(vals) - 1)))

def rule_params(K):
    M = K // 64; ch = [6 * M]
    for _ in range(3): ch.append(ch[-1] + ch[-1] // 2)
    nU = ch[-1]; Lam = beta(nU) - 1; ns = nU + 2 * M
    lB = min(Lam - 1, ceil_div(Lam + M, 2) - 1) + flog2(2 * Lam)
    kB = lB + z(ns) + M
    return M, ch, Lam, ns, kB

def exact_rule(K):
    T = (1 << K) - 2 * K - 12
    M, ch, Lam, ns, kB = rule_params(K)
    tB, info = thmB(K, T, M, M, ch, ns, kB, 0)
    tot = sum(tB.values()); parts = dict(tB)
    for nm, (r, a, lam, nC) in CLS.items():
        nsA = 2 * M + 16; kA = ell_C(lam) + z(nsA) + M
        tA, _ = thmA(nm, K, T, nsA, kA, 0)
        for q, v in tA.items(): parts[nm + q] = v
        tot += sum(tA.values())
    return tot, parts, (M, ch, Lam, ns, kB, info["Kt"])

def cmd_ruleC(K1, K2, st):
    worst = None
    for K in range(K1, K2 + 1, st):
        tot, parts, prm = exact_rule(K)
        l = lg(tot); big = max(parts, key=lambda q: parts[q])
        ok = l <= -K / 80
        if worst is None or l + K / 80 > worst[0]: worst = (l + K / 80, K)
        print(f"RULE K={K} M={prm[0]} chain={prm[1]} Lam={prm[2]} ns={prm[3]} kB={prm[4]} Kt={prm[5]}: exact log2={l:.3f} "
              f"(largest {big}) vs -K/80={-K / 80:.2f} {'OK' if ok else 'VIOLATION'}", flush=True)
    print(f"max over tested K of (exact log2 + K/80) = {worst[0]:.3f} at K={worst[1]} (must be <= 0)")

def cmd_ruleA(Ks):
    for K in Ks:
        T = (1 << K) - 2 * K - 12; ns = K // 6
        for nm, (r, a, lam, nC) in CLS.items():
            k = ell_C(lam) + z(ns) + ceil_div(K, 6) + 1
            t, Kt = thmA(nm, K, T, ns, k, 0)
            l = lg(sum(t.values()))
            print(f"RULE-A K={K} {nm}: exact log2={l:.3f} Kt={Kt} vs -K/7={-K / 7:.2f} {'OK' if l <= -K / 7 else 'VIOLATION'}", flush=True)

def H(q): return -q * math.log2(q) - (1 - q) * math.log2(1 - q)

def lse(ts):
    m = max(ts); return m + math.log2(sum(2.0 ** (t - m) for t in ts))

def cmd_closed(Kmax=4_000_000):
    # ---- Theorem A': report's closed form 2^{-K-15} + 0.911 K^2 2^{-K/6} + mu(C)(2^{-0.1732(K-5)} + 2^{-K/6}) <= 2^{-K/7}
    hA = 1 - H(0.26)
    assert hA >= 0.1732, hA
    min_marginA = (1e9, None); bad_sideA = []
    for K in range(1024, Kmax + 1):
        ns = K // 6
        if K <= 20000 or K % 997 == 0:      # integer side conditions (cheap but not needed at every large K)
            for nm, (r, a, lam, nC) in CLS.items():
                k = ell_C(lam) + z(ns) + ceil_div(K, 6) + 1
                Kt = K - 1   # claimed; verify: floor(log2(T - ns - 2lam)) with T = 2^K - 2K - 12
                Tm = (1 << K) - 2 * K - 12 - ns - 2 * lam if K < 3000 else None
                if Tm is not None and flog2(Tm) != K - 1: bad_sideA.append((K, nm, "Kt"))
                if not (ns >= nC and beta(ns) >= lam + 1 and ns + 1 >= 88): bad_sideA.append((K, nm, "ns"))
                if (k - 1) / (Kt - a) > 0.26: bad_sideA.append((K, nm, "q"))
                if k - 1 > K / 4 + 5: bad_sideA.append((K, nm, "k-1"))
        for a in (3, 4):
            m = lse([-K - 15, math.log2(0.911) + 2 * math.log2(K) - K / 6, -a - 0.1732 * (K - 5), -a - K / 6])
            if -K / 7 - m < min_marginA[0]: min_marginA = (-K / 7 - m, K)
    print(f"Thm A': min over K in [1024,{Kmax}] of (-K/7 - log2 closed form) = {min_marginA[0]:.4f} at K={min_marginA[1]}; "
          f"side-condition failures: {bad_sideA[:5]} (count {len(bad_sideA)})", flush=True)
    # ---- Theorem C: the nine closed-form terms of the report's proof
    hB = 1 - H(0.36); hAA = 1 - H(0.04)
    assert hB >= 0.0573 and hAA >= 0.757, (hB, hAA)
    min_margin = (1e9, None); bad = []; last_fail = None
    for K in range(2400, Kmax + 1):
        M = K // 64
        terms = [
            -K + 1,                                                   # A1 + B1
            math.log2(3 * 2.05 * 8) + 2 * math.log2(2 * M + 16) - 2 * M - 16,   # sum A4
            math.log2(0.25) + 1 - M,                                  # sum A5, second parts
            math.log2(0.25) - 0.75 * (K - 5),                         # sum A5, binomial
            math.log2(2 * M + 1) - M,                                 # B2
            -2.125 * M + 2.05 + 6 * math.log2(20.25 * M),             # B3
            -2 * M + 2 * math.log2(22.25 * M + 1),                    # B4
            -0.0573 * (K - 5) - 4,                                    # B5 binomial
            -M - 3]                                                   # B5 second part
        m = lse(terms)
        q = (22.75 * M - 1.5 + math.log2(40.5 * M)) / (K - 5)
        qA = (2 * M + 10) / (K - 5)
        ok = m <= -K / 80 and q <= 0.36 and qA <= 0.04 and M >= 22
        if not ok: last_fail = K
        if K >= 3072 and -K / 80 - m < min_margin[0]: min_margin = (-K / 80 - m, K)
        if K >= 3072 and (K <= 30000 or K % 1009 == 0):
            # integer side conditions of the rule, checked exactly
            M_, ch, Lam, ns, kB = rule_params(K)
            c = [all(window_ok(ch[i], ch[i + 1], M_) for i in range(3)), Lam <= ch[-1] - 2,
                 ch[-1] >= 20.25 * M_ - 1.25, ch[-1] <= 20.25 * M_, beta(ns) >= Lam + 1,
                 kB - 1 <= 22.75 * M_ - 1.5 + math.log2(40.5 * M_), (kB - 1) / (K - 5) <= 0.36,
                 ns + 2 * Lam <= 62.75 * M_]
            nsA = 2 * M_ + 16
            for nm, (r, a, lam, nC) in CLS.items():
                kA = ell_C(lam) + z(nsA) + M_
                c += [kA - 1 <= 2 * M_ + 10, (kA - 1) / (K - 1 - a) <= 0.04, beta(nsA) >= lam + 1, nsA + 1 >= 88]
            if not all(c): bad.append((K, c))
    print(f"Thm C: largest K in [2400,{Kmax}] where closed form > -K/80 or q>0.36 or qA>0.04: {last_fail}; "
          f"min margin on [3072,{Kmax}] = {min_margin[0]:.4f} at K={min_margin[1]}; integer side-condition failures: {bad[:3]} (count {len(bad)})")

if __name__ == "__main__":
    c = sys.argv[1]
    if c == "table": cmd_table()
    elif c == "ruleC": cmd_ruleC(*map(int, sys.argv[2:5]))
    elif c == "ruleA": cmd_ruleA(list(map(int, sys.argv[2:])))
    elif c == "closed": cmd_closed(int(sys.argv[2]) if len(sys.argv) > 2 else 4_000_000)
