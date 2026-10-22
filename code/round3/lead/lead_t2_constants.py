# Lead-author independent evaluation of the explicit bound of T2 Theorem 5.3 with the
# parameter choice of Corollary 5.4 (note section 11.3).  Shares no code with T2's constants*.py.
#
# For each class C in {8Z_2, 2+8Z_2, 6+16Z_2} the right-hand side of Theorem 5.3,
#   RHS(G) = B_L(n0) + n0*2^-K + 2^-c * E_C + 2^-k * P(Bin(K-k,1/2) <= c + s_L - s(r0)),
# with n0 = ceil(4 log2 G) + 3L + 40, T = floor(G/2), K = floor(log2(T - l0 + 1)),
# c = floor(alpha (K-k)) - s_L + s(r0), depends on G only through (n0, K).  It is therefore
# constant on the integer intervals where (n0, K) is constant, and sup_G G^alpha * min(mu(C), RHS(G))
# over such an interval is attained at its right end.  We enumerate every right end exactly
# (integer arithmetic for n0, K, c, the binomial tail and B_L), for 2^10 <= G <= 2^GMAX_LOG.
# Floats are used only for the final products with G^alpha.
from fractions import Fraction
from math import comb, floor, log2
import sys

ALPHA = Fraction(227, 1000)
GMAX_LOG = int(sys.argv[1]) if len(sys.argv) > 1 else 400

def s2(n):
    return bin(n).count("1")

classes = {
    "C0=8Z2":     dict(k=3, r0=0, L=1, EC=Fraction(1)),
    "C2=2+8Z2":   dict(k=3, r0=2, L=3, EC=Fraction(2**3 * 2**(3 - 1 + max(0, 3 + 1 - 3)))),
    "C6=6+16Z2":  dict(k=4, r0=6, L=6, EC=Fraction(2**6 * 2**(6 - 1 + max(0, 6 + 1 - 4)))),
}

def ceil_log2(n):            # exact ceil(log2 n), n >= 1
    return (n - 1).bit_length()

def floor_h(n, L):           # exact floor((n - log2 n - 3L - 4)/2)
    A = n - 3 * L - 4
    return (A - ceil_log2(n)) // 2   # floor division handles negatives

def B_L(n0, L, l0, extra=300):
    # sum_{i>=1} 2^{-floor h(max(n0, i-l0)) - 1}; every term is an exact power of 2, summed in floats
    from math import ldexp
    tot = (n0 + l0) * ldexp(1.0, -(floor_h(n0, L) + 1))
    for n in range(n0 + 1, n0 + extra + 1):
        tot += ldexp(1.0, -(floor_h(n, L) + 1))
    # remainder n >= N1 = n0+extra+1: floor h(n) + 1 >= (n - log2 n - 3L - 4)/2, and 0.5*log2 n <= n/8
    # for n >= 64, so term <= 2^{(3L+4)/2} 2^{-3n/8}; geometric tail <= 2^{(3L+4)/2 - 3 N1/8}/(1-2^{-3/8}).
    N1 = n0 + extra + 1
    assert N1 >= 64
    rem = 2.0 ** ((3 * L + 4) / 2 - 3 * N1 / 8) / (1 - 2 ** (-3 / 8))
    return tot, rem

def binom_tail(N, t):        # P(Bin(N,1/2) <= t), exact
    if t < 0:
        return Fraction(0)
    t = min(t, N)
    return Fraction(sum(comb(N, i) for i in range(t + 1)), 2 ** N)

def iroot4_pow2(m):          # largest integer G with G^4 <= 2^m (exact integer bisection)
    lo, hi = 1, 1 << (m // 4 + 2)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid ** 4 <= (1 << m):
            lo = mid
        else:
            hi = mid
    return lo

def params(G, c):
    k, r0, L = c["k"], c["r0"], c["L"]
    l0 = 2 * L + 2
    sL = max(s2(d) for d in range(l0))
    n0 = ceil_log2(G ** 4) + 3 * L + 40
    T = G // 2
    if T - l0 + 1 < 1:
        return None
    K = (T - l0 + 1).bit_length() - 1
    if not (T >= n0 + l0 and 2 ** K >= l0 and K > k and n0 >= 19):
        return None
    cc = floor(ALPHA * (K - k)) - sL + s2(r0)
    return dict(n0=n0, K=K, c=cc, sL=sL, l0=l0)

def rhs(G, c):
    P = params(G, c)
    if P is None:
        return None
    k, r0, L, EC = c["k"], c["r0"], c["L"], c["EC"]
    B, rem = B_L(P["n0"], L, P["l0"])
    side = B + float(Fraction(P["n0"], 2 ** P["K"]))
    main1 = (Fraction(2 ** (-P["c"])) if P["c"] <= 0 else Fraction(1, 2 ** P["c"])) * EC
    main2 = Fraction(1, 2 ** k) * binom_tail(P["K"] - k, P["c"] + P["sL"] - s2(r0))
    return side, rem, main1, main2

alpha = float(ALPHA)
for name, c in classes.items():
    mu = Fraction(1, 2 ** c["k"])
    L = c["L"]; l0 = 2 * L + 2
    ends = set()
    for m in range(40, 4 * GMAX_LOG + 1):
        g = iroot4_pow2(m)
        if 2 ** 10 <= g <= 2 ** GMAX_LOG:
            ends.add(g)
    for K in range(5, GMAX_LOG):
        T = 2 ** (K + 1) + l0 - 2
        for g in (2 * T + 1,):
            if 2 ** 10 <= g <= 2 ** GMAX_LOG:
                ends.add(g)
    ends.add(2 ** GMAX_LOG)
    best_full = best_side = 0.0
    arg_full = arg_side = None
    max_rem = 0.0
    nopar = 0
    for G in sorted(ends):
        r = rhs(G, c)
        if r is None:
            nopar += 1
            val = float(mu) * G ** alpha
            if val > best_full:
                best_full, arg_full = val, G
            continue
        side, rem, m1, m2 = r
        max_rem = max(max_rem, rem)
        tot = side + float(m1 + m2) + rem
        val = min(float(mu), tot) * float(G) ** alpha
        if val > best_full:
            best_full, arg_full = val, G
        sv = (float(side) + rem) * float(G) ** alpha
        if sv > best_side:
            best_side, arg_side = sv, G
    k, r0, EC = c["k"], c["r0"], c["EC"]
    sL = max(s2(d) for d in range(l0))
    main_const = (2 ** (1 + sL - s2(r0)) * float(EC) + 2.0 ** (-k)) * 2 ** (alpha * k) * 8 ** alpha
    # small G: mu(C) <= const * G^-alpha for G <= 2^10 needs const >= mu * 2^(10 alpha)
    small = float(mu) * 2 ** (10 * alpha)
    print(f"{name}: pieces={len(ends)} (no-hypothesis pieces {nopar}); "
          f"sup_G min(mu,RHS) G^a = {best_full:.4f} at log2 G = {log2(arg_full):.2f}; "
          f"sup side-terms*G^a = {best_side:.4f} (log2 G = {log2(arg_side):.2f}); "
          f"Chernoff main-term const = {main_const:.2f}; main+side = {main_const + best_side:.2f}; "
          f"small-G requirement = {small:.3f}; max B_L remainder = {max_rem:.2e}")
