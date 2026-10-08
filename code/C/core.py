"""Core exact routines for Erdos #404 (angle C: large p).

All arithmetic is exact (Python ints / Fractions).  Nothing here is heuristic.
"""
from fractions import Fraction
from itertools import combinations
from math import factorial


def vp(n, p):
    """p-adic valuation of a nonzero integer (or Fraction)."""
    if isinstance(n, Fraction):
        return vp(n.numerator, p) - vp(n.denominator, p)
    if n == 0:
        return float("inf")
    v = 0
    n = abs(n)
    while n % p == 0:
        n //= p
        v += 1
    return v


def vp_fact(n, p):
    """Legendre: v_p(n!)."""
    s, q = 0, n
    while q:
        q //= p
        s += q
    return s


def e_block(m, p):
    """e_m = v_p((pm)!) = m + v_p(m!)."""
    return m + vp_fact(m, p)


def max_val_at_least(a, p, K):
    """Exact test of f(a,p) >= K.

    f(a,p) >= K  iff  there is T subset [a, N_K) with min T = a and
    p^K | sum_{n in T} n!, where N_K = least N with v_p(N!) >= K
    (every n >= N_K has p^K | n!).  Dynamic programming over reachable
    residues mod p^K with the exact pruning: before n is considered, the
    partial sum must be 0 mod p^{min(K, v_p(n!))} (all later terms are
    divisible by p^{v_p(n!)}).
    """
    if K <= 0:
        return True
    mod = p ** K
    N = 0
    while vp_fact(N, p) < K:
        N += 1
    if a >= N:
        return True  # a! itself is divisible by p^K
    fa = factorial(a) % mod
    states = {fa}
    f = fa
    for n in range(a + 1, N):
        f = (f * n) % mod
        e = min(K, vp_fact(n, p))
        q = p ** e
        # prune first (states must be 0 mod p^{e} before adding n)
        states = {s for s in states if s % q == 0}
        if not states:
            return False
        new = set(states)
        for s in states:
            new.add((s + f) % mod)
        states = new
    return 0 in states


def f_exact_upto(a, p, Kmax):
    """Return f(a,p) if it is < Kmax, else Kmax (meaning f >= Kmax)."""
    K = 0
    while K < Kmax and max_val_at_least(a, p, K + 1):
        K += 1
    return K


def Q(S):
    """Q_S = sum_{u in S} (-1)^u / u!  (exact rational)."""
    return sum((Fraction((-1) ** u, factorial(u)) for u in S), Fraction(0))


def tau(k, p):
    """tau(k,p) = max v_p(Q_S) over S with k-1 in S subset {0..k-1}.

    Returns (tau, argmax S, any_zero) ; any_zero True iff some Q_S == 0.
    """
    best, arg, zero = -1, None, False
    rest = list(range(k - 1))
    for r in range(len(rest) + 1):
        for c in combinations(rest, r):
            S = c + (k - 1,)
            q = Q(S)
            if q == 0:
                zero = True
                continue
            v = vp(q, p)
            if v > best:
                best, arg = v, S
    return best, arg, zero


def tauK(K, p, cap=None):
    """General tau(K,p) for any K >= 1:
    max v_p(N_S) over S with K-1 in S subset {0..K-1}, N_S = sum_{u in S} (-1)^u (K-1)!/u!  (integers).
    Returns (tau, any_zero).  Exact enumeration over 2^(K-1) subsets (use K <= ~22).
    Uses a meet-in-the-middle-free direct DP on the multiset of integer subset sums.
    """
    d = K - 1
    F = factorial(d)
    terms = [(-1) ** u * (F // factorial(u)) for u in range(d)]  # u = 0..d-1
    top = (-1) ** d
    sums = {0}
    for t in terms:
        sums |= {s + t for s in sums}
    best, zero = -1, False
    for s in sums:
        x = s + top
        if x == 0:
            zero = True
            continue
        v = vp(x, p)
        if v > best:
            best = v
    return best, zero


def tauK_mitm(K, p, Lcap=200):
    """Exact tau(K,p) by meet-in-the-middle (for K up to ~36).
    tau = max_{S' subset [0,K-2]} v_p(top + sum_{u in S'} c_u), c_u = (-1)^u (K-1)!/u!, top = (-1)^{K-1}.
    Returns (tau, zero_found)."""
    d = K - 1
    F = factorial(d)
    cs = [(-1) ** u * (F // factorial(u)) for u in range(d)]
    top = (-1) ** d
    h = len(cs) // 2
    A = [0]
    for c in cs[:h]:
        A = A + [x + c for x in A]
    B = [0]
    for c in cs[h:]:
        B = B + [x + c for x in B]
    Bset = set(B)
    zero = any((-(a + top)) in Bset for a in A)
    levels = []
    q = 1
    for l in range(1, Lcap + 1):
        q *= p
        levels.append((q, {b % q for b in B}))
    best = -1
    for a in A:
        x = -(a + top)
        l = 0
        for q, S in levels:
            if x % q in S:
                l += 1
            else:
                break
        if l > best:
            best = l
    return best, zero
