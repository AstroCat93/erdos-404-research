"""b2_lib.py -- independent exact-arithmetic library for falsification tests of
M4B Lemma B2a, Proposition B2 and Corollary B2' (round 4).

Written from the definitions in the M4B report (section 1 and 3) and R3M Prop C2; shares no
code with code/round4/M4B/ or code/round3/.

Conventions
-----------
* x is a Python int in [0, p^PREC); it stands for the cylinder x + p^PREC Z_p.  Every
  valuation v(x+i) actually used is asserted to be < PREC - 2, so it is constant on that
  cylinder and every quantity below is a function of the cylinder.
* Window elements y_j = pi_j(x)/pi_n(x) = prod_{i=n+1}^{j} (x+i)  (exact integers, n <= j < N').
* Signed digits delta in {-1,0,1} with weights 2:1:1 out of 4 (P(0)=1/2, P(+-1)=1/4).
  All probabilities are exact Fractions with denominator 4^m.
* Coll_k = P(sum_j delta_j y_j == 0 mod p^k)  (= sum_r nu_k(r)^2, nu = uniform subset-sum law;
  the identity is cross-checked in coll_unsigned()).
* eps(W,W') = p^K Coll_K - p^D Coll_D with D = V_N - V_n, K = V_N' - V_n.
Probabilities of residue events are computed by meet-in-the-middle over two halves of the
element list (dicts residue -> integer weight), so arbitrarily deep gates (huge K) are
handled exactly as long as the number of elements is <= ~24.
"""
from collections import defaultdict
from fractions import Fraction as Fr
import math
import random

import numpy as np

PREC = 400

# rational bracket for e (e is irrational, so p^s > e*(d-1)! is decided exactly unless the
# integer ratio falls inside this bracket, which we detect and report)
E_LO = Fr(2718281828459045, 10 ** 15)
E_HI = Fr(2718281828459046, 10 ** 15)


def vp(a, p):
    """p-adic valuation of a nonzero integer."""
    assert a != 0
    a = abs(a)
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def vx(x, i, p):
    """v(x+i) for the cylinder x + p^PREC Z_p (asserted well defined)."""
    k = vp(x + i, p)
    assert k < PREC - 2, "valuation not determined by the cylinder"
    return k


def Vrel(x, n, j, p):
    """V_j - V_n = sum_{n<i<=j} v(x+i)."""
    return sum(vx(x, i, p) for i in range(n + 1, j + 1))


def elems(x, n, Np):
    """y_j = prod_{i=n+1}^{j}(x+i) for n <= j < Np (exact integers)."""
    ys = [1]
    for j in range(n + 1, Np):
        ys.append(ys[-1] * (x + j))
    return ys


def hyp_deep(p, s, d):
    """Exact decision of p^s > e*(d-1)!  (returns True/False, or None if undecidable)."""
    f = math.factorial(d - 1)
    if p ** s > E_HI * f:
        return True
    if p ** s < E_LO * f:
        return False
    return None


# ----------------------------------------------------------------------------------------
# signed laws by meet in the middle
# ----------------------------------------------------------------------------------------
def signed_dict(ys, mod):
    """dict residue -> integer weight of sum delta_j y_j mod `mod`; total weight 4^len(ys)."""
    d = {0: 1}
    for y in ys:
        r = y % mod
        nd = defaultdict(int)
        if r == 0:
            for k, c in d.items():
                nd[k] += 4 * c
        else:
            for k, c in d.items():
                nd[k] += 2 * c
                nd[(k + r) % mod] += c
                nd[(k - r) % mod] += c
        d = nd
    return d


def rekey(d, mod):
    nd = defaultdict(int)
    for k, c in d.items():
        nd[k % mod] += c
    return nd


class SignedLaw:
    """Exact law of S = sum delta_j y_j modulo p^Kmax, via two halves."""

    def __init__(self, ys, p, Kmax):
        self.p = p
        self.m = len(ys)
        self.Kmax = Kmax
        h = len(ys) // 2
        mod = p ** Kmax
        self.h1 = signed_dict(ys[:h], mod)
        self.h2 = signed_dict(ys[h:], mod)
        self._cache = {Kmax: (self.h1, self.h2)}

    def halves(self, k):
        if k not in self._cache:
            mod = self.p ** k
            self._cache[k] = (rekey(self.h1, mod), rekey(self.h2, mod))
        return self._cache[k]

    def prob(self, k, t=0):
        """P(S == t mod p^k), exact Fraction."""
        if k == 0:
            return Fr(1)
        assert k <= self.Kmax
        mod = self.p ** k
        a, b = self.halves(k)
        t %= mod
        tot = 0
        if len(a) > len(b):
            for kk, c in b.items():
                c2 = a.get((t - kk) % mod)
                if c2:
                    tot += c * c2
        else:
            for kk, c in a.items():
                c2 = b.get((t - kk) % mod)
                if c2:
                    tot += c * c2
        return Fr(tot, 4 ** self.m)

    def rho(self, k, t=0):
        """rho_k(t) = p^k P(S == t mod p^k)."""
        return self.p ** k * self.prob(k, t)


def window_data(x, n, N, Np, p):
    D = Vrel(x, n, N, p)
    K = Vrel(x, n, Np, p)
    return D, K


def eps(x, n, N, Np, p, law=None):
    """eps(W,W') for W=[n,N), W'=[N,Np): p^K Coll_K - p^D Coll_D (exact)."""
    D, K = window_data(x, n, N, Np, p)
    if law is None:
        law = SignedLaw(elems(x, n, Np), p, K)
    return p ** K * law.prob(K) - p ** D * law.prob(D), D, K


# ----------------------------------------------------------------------------------------
# full-array laws (numpy, exact int64) for small moduli
# ----------------------------------------------------------------------------------------
def signed_array(ys, mod):
    assert len(ys) <= 31
    arr = np.zeros(mod, dtype=np.int64)
    arr[0] = 1
    for y in ys:
        r = int(y % mod)
        if r == 0:
            arr = 4 * arr
        else:
            arr = 2 * arr + np.roll(arr, r) + np.roll(arr, -r)
    return arr


def subset_array(ys, mod):
    """uniform subset-sum counts (unsigned digits 0/1), total 2^m."""
    assert len(ys) <= 62
    arr = np.zeros(mod, dtype=np.int64)
    arr[0] = 1
    for y in ys:
        r = int(y % mod)
        arr = arr + np.roll(arr, r)
    return arr


def coll_unsigned(ys, p, k, K):
    """Coll_k = sum_r nu_k(r)^2 from the subset-sum law (R3M definition), exact."""
    arr = subset_array(ys, p ** K)
    f = arr.reshape(-1, p ** k).sum(axis=0) if k > 0 else np.array([arr.sum()])
    tot = sum(int(v) * int(v) for v in f if v)
    return Fr(tot, 4 ** len(ys))


def rand_unit(p, rnd, digits=PREC - 5):
    while True:
        w = rnd.randrange(1, p ** digits)
        if w % p:
            return w


def forced_x(p, pos, s, rnd, extra=None):
    """x with v(x+pos) = s exactly; optional extra = (t, s2): additionally
    v(x+pos+t*p^s) = s + s2 (requires p does not divide t)."""
    if extra is None:
        w = rand_unit(p, rnd, PREC - s - 5)
    else:
        t, s2 = extra
        assert t % p
        w2 = rand_unit(p, rnd, PREC - s - s2 - 5)
        w = -t + p ** s2 * w2
    x = (-pos + p ** s * w) % p ** PREC
    assert vx(x, pos, p) == s
    return x
