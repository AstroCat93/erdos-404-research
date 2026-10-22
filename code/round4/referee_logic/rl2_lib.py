"""Helpers for the round-4 logic referee, second instance (rl2_*).

Written from the definitions in R3M section 1 / note.md section 1.2 only; it
shares no code with the tracks, the verifiers, or the earlier rl_*.py files.

Conventions
  pi_c(y) = (y+1)...(y+c), pi_0 = 1.
  A path e has e_0 = 1 and S_e(y) = sum_j e_j pi_j(y).
  A "lazy signed" digit is 0 w.p. 1/2 and +1, -1 w.p. 1/4 each; we carry the
  integer weights (2, 1, 1), so a vector of n digits has total weight 4^n.
"""
from fractions import Fraction
import numpy as np


def v_p(a, p):
    """p-adic valuation of a nonzero integer or Fraction."""
    if isinstance(a, Fraction):
        return v_p(a.numerator, p) - v_p(a.denominator, p)
    a = int(a)
    if a == 0:
        raise ValueError("v_p(0)")
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def vals(y, n, p):
    """[v(y+1), ..., v(y+n)] for an integer y (no y+i may vanish)."""
    return [v_p(y + i, p) for i in range(1, n + 1)]


def Vn(y, n, p):
    return sum(vals(y, n, p))


def Mn(y, n, p):
    vs = vals(y, n, p)
    return max(vs) if vs else 0


def pi_list(y, n, mod=None):
    """[pi_0(y), ..., pi_{n-1}(y)] as python ints (reduced mod `mod` if given)."""
    out, cur = [1], 1
    for c in range(1, n):
        cur = cur * (y + c)
        if mod:
            cur %= mod
        out.append(cur)
    return out


def pi_and_deriv(y, n, mod):
    """pi_c(y) and pi_c'(y) mod `mod` for c < n, by the product rule."""
    P, Dv = [1 % mod], [0]
    cp, cd = 1, 0
    for c in range(1, n):
        cd = (cd * (y + c) + cp) % mod
        cp = (cp * (y + c)) % mod
        P.append(cp)
        Dv.append(cd)
    return P, Dv


def signed_law_1d(elems, mod, first_fixed=False):
    """Weights of sum_c delta_c elems[c] mod `mod` (lazy signed; delta_0 = 1 if
    first_fixed).  Python-int object array, exact."""
    cur = np.zeros(mod, dtype=object)
    cur[0] = 1
    for c, a in enumerate(elems):
        a = int(a) % mod
        if c == 0 and first_fixed:
            cur = np.roll(cur, a)
            continue
        cur = 2 * cur + np.roll(cur, a) + np.roll(cur, -a)
    return cur


def pk_coll(elems, k, p):
    """p^k Coll_k for the uniform subset-sum law of `elems` mod p^k, exact.
    Coll_k = P(two independent uniform subset sums agree mod p^k)
           = P(signed sum == 0 mod p^k)."""
    mod = p ** k
    law = signed_law_1d(elems, mod)
    return Fraction(int(law[0]) * mod, 4 ** len(elems))


def composite_elems(x, n, Np, mod):
    """Elements pi_j(x)/pi_n(x) = pi_{j-n}(x+n), n <= j < N', mod `mod`."""
    return pi_list(x + n, Np - n, mod)


def eps_coll(x, n, N, Np, p):
    """eps(W, W') = p^K Coll_K - p^D Coll_D of the composite [n, N'), exact."""
    D = Vn(x + n, N - n, p)
    K = Vn(x + n, Np - n, p)
    el = composite_elems(x, n, Np, p ** K)
    return pk_coll(el, K, p) - pk_coll(el, D, p), D, K


def harmonic_mod(r, p):
    return sum(pow(s, -1, p) for s in range(1, r + 1)) % p
