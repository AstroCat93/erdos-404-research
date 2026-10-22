# Independent 2-adic toolkit for adversarial checks of Corollary 11.30 (note_v3 §11.3).
# Written from the definitions in note_v3 §10.1 only (no code reused from T2 or the lead).
# 2-adic numbers are Python ints taken mod 2^P.
import random

P = 400
MASK = (1 << P) - 1


def v(a, cap=P):
    a &= MASK
    if a == 0:
        return cap
    return (a & -a).bit_length() - 1


def s(n):
    return bin(n).count("1")


def pis(x, n):
    """pi_0..pi_n and derivatives pi_j' at x (mod 2^P)."""
    pi = [1]
    dpi = [0]
    for j in range(n):
        pi.append((pi[-1] * (x + j + 1)) & MASK)
        dpi.append((dpi[-1] * (x + j + 1) + pi[-2]) & MASK)
    return pi, dpi


def Vn(x, n):
    return sum(v(x + i) for i in range(1, n + 1))


def Mn(x, n):
    return max(v(x + i) for i in range(1, n + 1))


def alive_paths(x, n, pi=None, dpi=None):
    """All paths e (tuple e_0..e_{n-1}, e_0=1) alive at n, with S_e(x), S_e'(x)."""
    if pi is None:
        pi, dpi = pis(x, n)
    V = [0]
    for j in range(1, n + 1):
        V.append(V[-1] + v(x + j))
    cur = [((1,), 1, 0)]
    if v(1) < V[1]:
        return [], V
    for j in range(1, n):
        nxt = []
        for e, S, dS in cur:
            for b in (0, 1):
                S2 = (S + b * pi[j]) & MASK
                if v(S2) >= V[j + 1]:
                    nxt.append((e + (b,), S2, (dS + b * dpi[j]) & MASK))
        cur = nxt
    return cur, V


def inv_odd(u, k):
    return pow(u, -1, 1 << k)


def tau_mod(S, pin, Vn_, k):
    """tau_n = -S/pi_n mod 2^k (S divisible by 2^{Vn})."""
    if k == 0:
        return 0
    a = (S >> Vn_)
    b = (pin >> Vn_)
    return (-a * inv_odd(b, k)) % (1 << k)


_acache = {}


def a_dist(x, n, lam):
    """a_n^{(lam)}(t) as a list of exact probabilities * 4^lam (ints)."""
    key = (x % (1 << max(lam, 1)), n % (1 << max(lam, 1)), lam)
    if key in _acache:
        return _acache[key]
    mod = 1 << lam
    coef = []
    c = 1
    for i in range(2 * lam):
        coef.append(c % mod if lam else 0)
        c = c * (x + n + i + 1)
    cnt = [0] * mod
    for f in range(1 << (2 * lam)):
        t = 0
        for i in range(2 * lam):
            if f >> i & 1:
                t += coef[i]
        cnt[t % mod] += 1
    _acache[key] = cnt
    return cnt  # a(t) = cnt[t]/4^lam


def rho(x, n, S, dS, pin, Vn_):
    """rho_n(e) = 2^lam a_n^{(lam)}(tau mod 2^lam); returned as Fraction-free (num, den=4^lam/2^lam)."""
    from fractions import Fraction
    lam = v(dS)
    cnt = a_dist(x, n, lam)
    t = tau_mod(S, pin, Vn_, lam)
    return Fraction((1 << lam) * cnt[t], 4 ** lam), lam


def rand_in_class(r0, k, rng):
    return (r0 + (rng.getrandbits(P - k) << k)) & MASK
