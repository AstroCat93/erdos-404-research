"""Small exact helpers for the round-4 logic referee (written from the
definitions in R3M section 1 and note.md section 1.2; shares no code with any
track or verifier).

Conventions: pi_c(y) = (y+1)...(y+c), pi_0 = 1.  Paths e have e_0 = 1 and
S_e(y) = sum_j e_j pi_j(y).  A "lazy signed" digit is 0 w.p. 1/2, +1 and -1
w.p. 1/4 each; we use integer weights 2,1,1 (total 4 per digit).
"""
from fractions import Fraction
import numpy as np


def vp(a, p):
    """p-adic valuation of a nonzero integer (or Fraction)."""
    if isinstance(a, Fraction):
        return vp(a.numerator, p) - vp(a.denominator, p)
    a = int(a)
    if a == 0:
        raise ValueError("valuation of 0")
    v = 0
    while a % p == 0:
        a //= p
        v += 1
    return v


def V(y, n, p):
    """V_n(y) = v_p(pi_n(y)) for an integer y with y+i != 0."""
    return sum(vp(y + i, p) for i in range(1, n + 1))


def Mx(y, n, p):
    return max([vp(y + i, p) for i in range(1, n + 1)] + [0])


def pis_mod(y, n, mod):
    """[pi_0(y), ..., pi_{n-1}(y)] mod `mod` (python ints)."""
    out = [1 % mod]
    cur = 1
    for c in range(1, n):
        cur = cur * (y + c) % mod
        out.append(cur)
    return out


def pis_and_derivs_mod(y, n, mod):
    """pi_c(y) and pi_c'(y) mod `mod`, c < n (product rule, exact ints)."""
    P = [1 % mod]
    Dv = [0]
    cp, cd = 1, 0
    for c in range(1, n):
        cd = (cd * (y + c) + cp) % mod
        cp = cp * (y + c) % mod
        P.append(cp)
        Dv.append(cd)
    return P, Dv


def subset_sums(elems, mod):
    """All 2^len(elems) subset sums mod `mod` as an int64 numpy array
    (index bit i <-> element i)."""
    arr = np.zeros(1, dtype=np.int64)
    for a in elems:
        a = int(a) % mod
        arr = np.concatenate([arr, (arr + a) % mod])
    return arr


def signed_law(elems, mod):
    """Law of sum_c delta_c * elems[c] mod `mod` with lazy signed delta,
    as integer weights (total 4^len)."""
    w = np.zeros(mod, dtype=object)
    w[0] = 1
    w = w.astype(object)
    cur = np.zeros(mod, dtype=np.int64)
    cur[0] = 1
    for a in elems:
        a = int(a) % mod
        cur = 2 * cur + np.roll(cur, a) + np.roll(cur, -a)
    return cur


def coll_times_pk(elems, k, p):
    """p^k * Coll_k of the uniform subset-sum law of `elems` mod p^k, as a
    Fraction. Coll_k = sum_r nu(r)^2 = P(signed sum == 0 mod p^k)."""
    mod = p ** k
    law = signed_law(elems, mod)
    tot = 4 ** len(elems)
    return Fraction(int(law[0]) * mod, tot)
