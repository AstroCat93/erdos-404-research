"""m4d_lib.py -- helper library for track M4D (round 4).

Exact p-adic arithmetic with Python integers modulo p^prec.  The first part (PAdic, products,
extend, alive_from_scratch, target, subset_sum_law, collision) is copied, with minor changes, from the
independently validated library code/round3/check_R3M/ck_lib.py (validated there against brute force,
4392 alive paths, 0 failures).  The numpy routines below are new.

Conventions (note.md section 10.1 at odd p; R3M report section 1):
  pi_j(x) = (x+1)...(x+j),  V_n = v(pi_n(x)),  M_n = max_{i<=n} v(x+i).
  A path of length n is a bitmask e with bit 0 set (e_0 = 1); S_e(x) = sum_{j<n} e_j pi_j(x).
  e is alive at n if v(S_e(x)) >= V_n; target tau_n = -S_e/pi_n; slope = v(S_e'(x)).
  Window W = [n, N): elements y_i = pi_{n+i}(x)/pi_n(x), i = 0..N-n-1; Q_f = sum f_i y_i; jump D = V_N - V_n.
"""
from fractions import Fraction

import numpy as np


class PAdic:
    def __init__(self, p, prec):
        self.p = p
        self.prec = prec
        self.mod = p ** prec

    def v(self, a):
        a %= self.mod
        if a == 0:
            return self.prec
        k = 0
        p = self.p
        while a % p == 0:
            a //= p
            k += 1
        return k


def vp_int(a, p, cap=10 ** 9):
    """p-adic valuation of a nonzero integer (cap returned for 0)."""
    if a == 0:
        return cap
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def products(P, x, N):
    mod = P.mod
    pi = [1] * (N + 1)
    dpi = [0] * (N + 1)
    vals = [None] * (N + 1)
    for j in range(1, N + 1):
        pi[j] = pi[j - 1] * (x + j) % mod
        dpi[j] = (dpi[j - 1] * (x + j) + pi[j - 1]) % mod
        vals[j] = P.v(x + j)
    return pi, dpi, vals


def extend(P, pi, dpi, vals, start, N, roots):
    """roots: list of (bits, S, dS) for paths of length `start` alive at `start`; returns all
    extensions of length N alive at N (DFS with prefix pruning; backward integrality)."""
    out = []
    Vcum = [0] * (N + 1)
    for j in range(1, N + 1):
        Vcum[j] = Vcum[j - 1] + vals[j]
    stack = [(b, S, dS, start) for (b, S, dS) in roots]
    mod = P.mod
    while stack:
        b, S, dS, k = stack.pop()
        if k == N:
            out.append((b, S, dS))
            continue
        for bit in (0, 1):
            if bit:
                S2 = (S + pi[k]) % mod
                dS2 = (dS + dpi[k]) % mod
                b2 = b | (1 << k)
            else:
                S2, dS2, b2 = S, dS, b
            if P.v(S2) >= Vcum[k + 1]:
                stack.append((b2, S2, dS2, k + 1))
    return out


def alive_from_scratch(P, pi, dpi, vals, n):
    if 0 < vals[1]:
        return []
    return extend(P, pi, dpi, vals, 1, n, [(1, 1, 0)])


def target(P, S, pin, Vn_):
    """tau = -S/pi_n as an integer mod p^(prec - Vn_) (requires v(S) >= Vn_)."""
    p = P.p
    q = p ** Vn_
    assert S % q == 0
    num = (-(S // q)) % P.mod
    u = pin // q
    prec2 = P.prec - Vn_
    m2 = p ** prec2
    return num * pow(u % m2, -1, m2) % m2


def subset_sum_law(elems, modulus):
    dist = {0: 1}
    for y in elems:
        y %= modulus
        new = {}
        for r, c in dist.items():
            new[r] = new.get(r, 0) + c
            r2 = (r + y) % modulus
            new[r2] = new.get(r2, 0) + c
        dist = new
    return dist


def collision(elems, modulus):
    d = subset_sum_law(elems, modulus)
    T = 2 ** len(elems)
    return Fraction(sum(c * c for c in d.values()), T * T)


# ----------------------------------------------------------------------------------------------
# new in M4D

def window_elems(x, n, N, mod):
    """[pi_j(x)/pi_n(x) mod mod for j = n..N-1] = [1, (x+n+1), (x+n+1)(x+n+2), ...]."""
    out = []
    y = 1
    for k in range(N - n):
        out.append(y % mod)
        y = y * (x + n + k + 1) % mod
    return out


def unit_cofactor(x, n, N, p, D, mod):
    """u = pi_N(x) / (p^D pi_n(x)) mod `mod` (a unit), where D = V_N - V_n."""
    q = 1
    for k in range(n + 1, N + 1):
        q *= x + k
    assert q % p ** D == 0 and (q // p ** D) % p != 0
    return (q // p ** D) % mod


def support_np(elems, mod):
    """boolean array S of length mod with S[r] = True iff r is a subset sum of elems mod `mod`."""
    S = np.zeros(mod, dtype=bool)
    S[0] = True
    for y in elems:
        y = int(y % mod)
        if y:
            S = S | np.roll(S, y)
    return S


def counts_np(elems, mod):
    """int64 array of subset-sum counts mod `mod` (requires 2^len(elems) < 2^62)."""
    assert len(elems) < 62
    C = np.zeros(mod, dtype=np.int64)
    C[0] = 1
    for y in elems:
        C = C + np.roll(C, int(y % mod))
    return C


def lift_sizes(S, p, D, D2):
    """S: support mod p^(D+D2).  Returns int array L of length p^D with L[r] = #{lifts s of r mod
    p^(D+D2) (s = r + p^D t) that lie in S}."""
    A = S.reshape(p ** D2, p ** D)        # A[t, r] = S[r + p^D t]
    return A.sum(axis=0)


def gates(x, n, N, p, cap=60):
    """list of (i, v(x+i)) for n < i <= N with v(x+i) >= 1."""
    out = []
    for i in range(n + 1, N + 1):
        k = vp_int(x + i, p, cap)
        if k >= 1:
            out.append((i, k))
    return out


def V_of(x, n, p, cap=60):
    return sum(vp_int(x + i, p, cap) for i in range(1, n + 1))
