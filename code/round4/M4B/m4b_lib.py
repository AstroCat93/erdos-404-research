"""m4b_lib.py -- small exact-arithmetic library for track M4B (round 4).

Conventions (note.md section 10.1, R3M report section 1), at an odd prime p:
  pi_j(x) = (x+1)...(x+j),  V_n(x) = v(pi_n(x)),  M_n(x) = max_{i<=n} v(x+i),  c_n = 2^-n p^{V_n}.
Composite window [n, N') = [n, N) u [N, N'): elements y_j = pi_j(x)/pi_n(x), n <= j < N'.
  D = V_N - V_n, K = V_N' - V_n,  eps = p^K Coll_K - p^D Coll_D  (R3M Prop C2).
Signed digits delta in {-1,0,1} with P(0) = 1/2, P(+-1) = 1/4 (integer weights 2,1,1 out of 4).

All p-adic numbers are Python integers read modulo p^PREC.  Distributions are numpy arrays of
exact integer weights (int64 when the total weight fits, Python ints (dtype=object) otherwise).
"""
from fractions import Fraction

import numpy as np

PREC = 200


class Ctx:
    def __init__(self, p, prec=PREC):
        self.p = p
        self.prec = prec
        self.mod = p ** prec

    def v(self, a):
        a %= self.mod
        if a == 0:
            return self.prec
        p = self.p
        k = 0
        while a % p == 0:
            a //= p
            k += 1
        return k


def valuations(C, x, Nmax):
    """vals[i] = v(x+i) for 1 <= i <= Nmax (vals[0] unused), and cumulative V[i]."""
    vals = [0] * (Nmax + 1)
    V = [0] * (Nmax + 1)
    for i in range(1, Nmax + 1):
        vals[i] = C.v(x + i)
        V[i] = V[i - 1] + vals[i]
    return vals, V


def window_elems(C, x, n, N2):
    """[pi_j(x)/pi_n(x) mod p^prec for n <= j < N2]."""
    out = []
    y = 1
    for k in range(N2 - n):
        out.append(y)
        y = y * (x + n + k + 1) % C.mod
    return out


def _dtype_for(total):
    return np.int64 if total < 2 ** 62 else object


def unsigned_dist(elems, mod):
    """exact counts m(r) = #{f in {0,1}^L : sum f_i y_i == r mod `mod`} (total 2^L)."""
    L = len(elems)
    dist = np.zeros(mod, dtype=_dtype_for(2 ** L))
    dist[0] = 1
    for y in elems:
        dist = dist + np.roll(dist, int(y % mod))
    return dist


def signed_dist(elems, mod):
    """exact weights w(r) = 4^L * P(sum delta_i y_i == r mod `mod`), delta i.i.d. (1/4,1/2,1/4)."""
    L = len(elems)
    dist = np.zeros(mod, dtype=_dtype_for(4 ** L))
    dist[0] = 1
    for y in elems:
        s = int(y % mod)
        dist = 2 * dist + np.roll(dist, s) + np.roll(dist, -s)
    return dist


def fold(dist, mod_small):
    """reduce a distribution mod p^K to mod p^k (mod_small divides len(dist))."""
    return dist.reshape(-1, mod_small).sum(axis=0)


def sumsq(a):
    return sum(int(c) * int(c) for c in a)


def coll(elems, p, k):
    """Coll_k = P(two independent uniform subset sums agree mod p^k), exact Fraction."""
    L = len(elems)
    m = unsigned_dist(elems, p ** k)
    return Fraction(sumsq(m), 4 ** L)


def eps_composite(elems, p, D, K):
    """eps = p^K Coll_K - p^D Coll_D for the full element list (exact).  Uses a dense residue array
    when p^K <= 4e6, otherwise a sparse dictionary of the (at most 2^L) distinct subset sums."""
    L = len(elems)
    if p ** K <= 4_000_000:
        m = unsigned_dist(elems, p ** K)
        cK = Fraction(sumsq(m), 4 ** L)
        cD = Fraction(sumsq(fold(m, p ** D)), 4 ** L)
    else:
        mod = p ** K
        dist = {0: 1}
        for y in elems:
            y %= mod
            new = dict(dist)
            for r, c in dist.items():
                r2 = (r + y) % mod
                new[r2] = new.get(r2, 0) + c
            dist = new
        cK = Fraction(sum(c * c for c in dist.values()), 4 ** L)
        modD = p ** D
        dd = {}
        for r, c in dist.items():
            dd[r % modD] = dd.get(r % modD, 0) + c
        cD = Fraction(sum(c * c for c in dd.values()), 4 ** L)
    return p ** K * cK - p ** D * cD


def random_x(C, rnd):
    return rnd.randrange(C.mod)


def forced_gate_x(C, rnd, pos, s):
    """x Haar-random subject to v(x+pos) = s exactly."""
    p = C.p
    while True:
        u = rnd.randrange(1, p ** (C.prec - s))
        if u % p:
            return (-pos + p ** s * u) % C.mod
