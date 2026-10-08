"""Reference (slow, simple) implementation for Erdos #404, behaviour angle.

Notation.  For a >= 1, prime p:
  f(a,p) = sup{ v_p(sum_{n in A} n!) : A finite, min A = a }
  g(a,p) = f(a,p) - v_p(a!)
Dividing by a!:  g(a,p) = sup_T v_p( P_T(a) ),  P_T(x) = sum_{k in T} (x+1)(x+2)...(x+k),
T finite subset of {0,1,2,...} containing 0 (empty product = 1).

ge(a,p,G) decides g(a,p) >= G exactly (pruned residue DP; see README for proof of exactness).
"""
import itertools


def vp(x, p):
    if x == 0:
        raise ValueError
    v = 0
    while x % p == 0:
        x //= p
        v += 1
    return v


def vp_fact(n, p):
    v = 0
    while n:
        n //= p
        v += n
    return v


def terms(a, p, G):
    """List of (k, v_k, u_k mod p^G) for k>=1 with v_k = v_p(t_k(a)) < G, in increasing k.
    t_k(a) = (a+1)...(a+k) = p^{v_k} u_k."""
    M = p ** G
    out = []
    v, u, k = 0, 1, 0
    while True:
        k += 1
        x = a + k
        w = vp(x, p)
        v += w
        u = (u * (x // p ** w)) % M
        if v >= G:
            return out
        out.append((k, v, u))


def ge(a, p, G, want_witness=False):
    """Exact decision of g(a,p) >= G.  Returns bool (and a witness set T if asked)."""
    if G <= 0:
        return (True, [0]) if want_witness else True
    M = p ** G
    # states: dict residue(mod p^(G-L)) -> witness tuple (only if want_witness)
    L = 0
    Mc = M
    R = {1 % M: (0,)}
    if 0 in R:
        return (True, [0]) if want_witness else True
    for (k, v, u) in terms(a, p, G):
        if v > L:
            d = p ** (v - L)
            R = {s // d: w for s, w in R.items() if s % d == 0}
            Mc //= d
            L = v
            if not R:
                return (False, None) if want_witness else False
        x = u % Mc
        new = dict(R)
        for s, w in R.items():
            t = (s + x) % Mc
            if t not in new:
                new[t] = w + (k,) if want_witness else None
        R = new
        if 0 in R:
            if want_witness:
                return True, list(R[0])
            return True
    return (False, None) if want_witness else False


def g_value(a, p, cap=60):
    """Exact g(a,p) if < cap, else returns cap (meaning g >= cap)."""
    G = 0
    while G < cap and ge(a, p, G + 1):
        G += 1
    return G


def check_witness(a, p, T, K):
    """Definition-level check: p^K | sum_{k in T} (a+k)!  (T contains 0)."""
    from math import factorial
    s = sum(factorial(a + k) for k in T)
    return s % p ** K == 0


def frozen_set(p):
    """Phi_p = { r in [0,p-1] : no I subset (r,p-1] with r! + sum_{i in I} i! == 0 mod p }."""
    fac = [1] * p
    for i in range(1, p):
        fac[i] = fac[i - 1] * i % p
    out = []
    for r in range(p):
        reach = {fac[r]}
        for i in range(r + 1, p):
            reach |= {(s + fac[i]) % p for s in reach}
        if 0 not in reach:
            out.append(r)
    return out
