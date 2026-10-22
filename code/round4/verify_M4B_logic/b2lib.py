"""b2lib.py -- independent exact helpers for the logic check of M4B Lemma B2a / Corollary B2'.

Written from the definitions (R3M report section 1, Prop C2; M4B report section 3); no code is
shared with code/round4/M4B/.

Window conventions.  For a composite window [n,N') = [n,N) u [N,N') the elements are
  y_j = pi_j(x)/pi_n(x) = prod_{i=n+1}^{j} (x+i),   n <= j < N'   (so y_n = 1);
D = V_N - V_n, K = V_N' - V_n.  nu_k = law mod p^k of sum_j b_j y_j with b_j i.i.d. uniform in {0,1};
Coll_k = sum_r nu_k(r)^2;  eps(W,W') = p^K Coll_K - p^D Coll_D   (R3M Prop C2).
Signed law: delta_j i.i.d. with P(0)=1/2, P(+-1)=1/4 (weights 1,2,1 out of 4).
x is an integer representative of a p-adic number modulo p^PREC; every valuation used is checked
to be < PREC, so the results hold for the whole cylinder x + p^PREC Z_p.
"""
from fractions import Fraction
import numpy as np


def vp(a, p, cap):
    """p-adic valuation of the integer a, returns cap if p^cap | a."""
    if a == 0:
        return cap
    k = 0
    while a % p == 0 and k < cap:
        a //= p
        k += 1
    return k


def elems(x, lo, hi, mod):
    """[prod_{i=lo+1}^{j} (x+i) mod `mod` for lo <= j < hi]."""
    out = []
    y = 1 % mod
    for j in range(lo, hi):
        if j > lo:
            y = y * (x + j) % mod
        out.append(y)
    return out


def unsigned_counts(ys, M):
    """counts[r] = #{b in {0,1}^L : sum b_j y_j == r mod M} (exact, int64; L <= 30 keeps < 2^62)."""
    assert len(ys) <= 30
    c = np.zeros(M, dtype=np.int64)
    c[0] = 1
    for y in ys:
        c = c + np.roll(c, y % M)
    assert int(c.sum()) == 2 ** len(ys)
    return c


def signed_counts(ys, M):
    """counts[r] = sum over delta in {-1,0,1}^L of prod w(delta_j), w(0)=2, w(+-1)=1, with
    sum delta_j y_j == r mod M.  Total 4^L.  P(r) = counts[r]/4^L."""
    assert len(ys) <= 30
    c = np.zeros(M, dtype=np.int64)
    c[0] = 1
    for y in ys:
        c = 2 * c + np.roll(c, y % M) + np.roll(c, -(y % M))
    assert int(c.sum()) == 4 ** len(ys)
    return c


def fold(c, M):
    """fold counts mod a multiple of M down to mod M."""
    return c.reshape(-1, M).sum(axis=0)


def coll_scaled(cK, p, k, L):
    """p^k Coll_k as an exact Fraction, from unsigned counts mod p^K (K >= k)."""
    ck = fold(cK, p ** k)
    assert L <= 30          # sum of squares <= (2^L)^2 <= 2^60: no int64 overflow
    s = int(np.dot(ck, ck))
    return Fraction(p ** k * s, 4 ** L)


def eps_def(ys, p, D, K):
    """eps = p^K Coll_K - p^D Coll_D by the R3M definition (unsigned subset-sum law)."""
    L = len(ys)
    cK = unsigned_counts(ys, p ** K)
    return coll_scaled(cK, p, K, L) - coll_scaled(cK, p, D, L)


def vals_and_V(x, p, n, Nmax, cap):
    """v(x+i) for n < i <= Nmax and the partial sums VV[j] = V_j - V_n for n <= j <= Nmax."""
    v = {}
    VV = {n: 0}
    for i in range(n + 1, Nmax + 1):
        v[i] = vp(x + i, p, cap)
        assert v[i] < cap, "valuation reached precision cap"
        VV[i] = VV[i - 1] + v[i]
    return v, VV
