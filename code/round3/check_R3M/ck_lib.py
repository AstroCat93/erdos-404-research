"""ck_lib.py -- independent helper library for the check of track R3M (round 3).

Written from the statements in data/round3/reports/R3M.md only; shares no code with
code/round3/R3M/.  Exact p-adic arithmetic is done with Python integers modulo p^PREC.

Conventions (R3M.md section 1):
  pi_j(x) = (x+1)...(x+j),  V_n = v(pi_n(x)),  M_n = max_{i<=n} v(x+i),  c_n = 2^-n p^{V_n}.
  A path of length n is a bitmask e with bit 0 set (e_0 = 1); S_e(x) = sum_{j<n} e_j pi_j(x).
  e is alive at n if v(S_e(x)) >= V_n; target tau_n = -S_e/pi_n; slope = v(S_e'(x)).
"""
from fractions import Fraction


class PAdic:
    """Fixed-precision context: integers mod p^prec."""

    def __init__(self, p, prec):
        self.p = p
        self.prec = prec
        self.mod = p ** prec

    def v(self, a):
        """valuation of a (an integer, read mod p^prec); prec if a == 0 mod p^prec."""
        a %= self.mod
        if a == 0:
            return self.prec
        k = 0
        p = self.p
        while a % p == 0:
            a //= p
            k += 1
        return k

    def unit_part(self, a):
        a %= self.mod
        k = self.v(a)
        return a // self.p ** k, k


def products(P, x, N):
    """lists pi[j], dpi[j] (j = 0..N) of pi_j(x), pi_j'(x) mod p^prec, and vals v(x+i), i=1..N."""
    mod = P.mod
    pi = [1] * (N + 1)
    dpi = [0] * (N + 1)
    vals = [None] * (N + 1)
    for j in range(1, N + 1):
        pi[j] = pi[j - 1] * (x + j) % mod
        dpi[j] = (dpi[j - 1] * (x + j) + pi[j - 1]) % mod
        vals[j] = P.v(x + j)
    return pi, dpi, vals


def Vn(vals, n):
    return sum(vals[1:n + 1])


def Mn(vals, n):
    return max(vals[1:n + 1]) if n >= 1 else 0


def extend(P, pi, dpi, vals, start, N, roots):
    """roots: list of (bits, S, dS) for paths of length `start` alive at `start`.
    Returns all extensions of length N alive at N, as (bits, S, dS), by depth-first search
    with prefix pruning (a prefix of an alive path is alive: backward integrality)."""
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
        # append e_k = 0 or 1, check alive at k+1
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
    """all paths of length n alive at n (n >= 1)."""
    root = (1, 1, 0)  # e_0 = 1: S = pi_0 = 1, S' = 0
    if P.v(1) < vals[1]:
        # path (1) of length 1 is alive at 1 iff v(1) >= V_1, i.e. v(x+1) = 0
        return []
    return extend(P, pi, dpi, vals, 1, n, [root])


def target(P, S, pin, Vn_):
    """tau = -S/pi_n as an integer mod p^(prec - Vn_)  (requires v(S) >= Vn_)."""
    p = P.p
    q = p ** Vn_
    assert S % q == 0
    num = (-(S // q)) % P.mod
    u = pin // q
    prec2 = P.prec - Vn_
    m2 = p ** prec2
    return num * pow(u % m2, -1, m2) % m2


def subset_sum_law(elems, modulus):
    """dict residue -> count of the 2^len uniform subset sums of elems mod modulus."""
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
