"""cm_lib: second, independent exact-arithmetic library for the numerical-falsification check of
round-4 track M4A, Corollary M' (p = 11, 13, 17, 19, 23).  Written from the statements in
data/round4/reports/M4A.md; it shares no code with code/round4/M4A/ and none with vf_lib.py
(the earlier p = 7 check of this track); different algorithms are used on purpose:
  * q_s by an int64 residue DP over Z mod p^s (exact, since all counts are < 4^23 = 2^46),
    cross-checked by full enumeration (p <= 13) and by a floating FFT of the characteristic
    function (all p);
  * P_0(g, s) by exact meet-in-the-middle over the signed digits (any s);
  * V_N, M_N on an atom by Legendre's formula, V_N(x_A) = v((x_A+N)!) - v(x_A!);
  * Props D/E by suffix products over gates (exact gmpy2 rationals), and, for small windows,
    literally per c through a separate Lemma Q evaluator;
  * Prop E' re-derived from its displayed formula.
Signed digit: P(0) = 1/2, P(+1) = P(-1) = 1/4 (weights 2, 1, 1 out of 4).
"""
import math
from fractions import Fraction
from functools import lru_cache
import numpy as np
import gmpy2
from gmpy2 import mpq, mpz

# ------------------------------------------------------------------ basic p-adic helpers
def vp(n, p):
    n = abs(int(n))
    if n == 0:
        raise ValueError("v(0)")
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def legendre(N, p):
    """v_p(N!) for an integer N >= 0"""
    s, q = 0, p
    while q <= N:
        s += N // q
        q *= p
    return s


def pi_int(y, k):
    r = 1
    for i in range(1, k + 1):
        r *= (y + i)
    return r


# ------------------------------------------------------------------ constants q_s
def q_counts_dp(p, s):
    """exact counts (int64 numpy, total 4^p) of Z mod p^s, Z = sum_{k<p} zeta_k pi_k(-p), all zeta signed"""
    mod = p ** s
    assert 4 ** p < 2 ** 62
    c = np.zeros(mod, dtype=np.int64)
    c[0] = 1
    for k in range(p):
        a = pi_int(-p, k) % mod
        c = 2 * c + np.roll(c, a) + np.roll(c, -a)
    assert int(c.sum()) == 4 ** p
    return c


def q_from_counts(p, s, c):
    return Fraction(p ** s * int(c.max()), 4 ** p)


def q_counts_fft(p, s):
    """floating check: probabilities of Z mod p^s from the characteristic function"""
    mod = p ** s
    xi = np.arange(mod, dtype=np.float64)
    F = np.ones(mod)
    for k in range(p):
        a = pi_int(-p, k) % mod
        F *= 0.5 + 0.5 * np.cos(2 * np.pi * ((xi * a) % mod) / mod)
    P = np.fft.fft(F).real / mod
    return P


def enum_values(coeffs, first_fixed):
    """full enumeration (int64; requires sum |coeffs| < 2^62): integer values and integer weights of
    sum zeta_c coeffs[c]; returns (vals, weights, total weight)"""
    assert sum(abs(int(a)) for a in coeffs) < 2 ** 62
    vals = np.array([coeffs[0] if first_fixed else 0], dtype=np.int64)
    wts = np.array([1], dtype=np.int64)
    rest = coeffs[1:] if first_fixed else coeffs
    for a in rest:
        vals = np.concatenate([vals - a, vals, vals + a])
        wts = np.concatenate([wts, 2 * wts, wts])
    return vals, wts, 4 ** len(rest)


def q_enum(p, smax):
    """q_s for s <= smax by full enumeration of the 3^p digit vectors (p <= 13)"""
    coeffs = [pi_int(-p, k) for k in range(p)]
    vals, wts, tot = enum_values(coeffs, False)
    out = {}
    for s in range(1, smax + 1):
        mod = p ** s
        r = vals % mod
        order = np.argsort(r, kind="stable")
        rs = r[order]; ws = wts[order]
        cuts = np.flatnonzero(np.diff(rs)) + 1
        sums = np.add.reduceat(ws, np.concatenate([[0], cuts]))
        out[s] = Fraction(mod * int(sums.max()), tot)
    return out


# ------------------------------------------------------------------ P_0(g, s) by meet in the middle
def _half(coeffs, mod):
    r = np.zeros(1, dtype=np.int64)
    w = np.ones(1, dtype=np.int64)
    for a in coeffs:
        a %= mod
        r = np.concatenate([(r - a) % mod, r, (r + a) % mod])
        w = np.concatenate([w, 2 * w, w])
    order = np.argsort(r, kind="stable")
    r = r[order]; w = w[order]
    if len(r) > 1:
        cuts = np.flatnonzero(np.diff(r)) + 1
        starts = np.concatenate([[0], cuts])
        return r[starts], np.add.reduceat(w, starts)
    return r, w


@lru_cache(maxsize=None)
def P0(p, g, s):
    """P(sum_{c<g} zeta_c pi_c(-g) = 0 mod p^s), zeta_0 = 1, others signed; exact Fraction"""
    if s <= 0:
        return Fraction(1)
    mod = p ** s
    assert mod < 2 ** 62
    co = [pi_int(-g, c) for c in range(1, g)]
    h = len(co) // 2
    rA, wA = _half(co[:h], mod)
    rB, wB = _half(co[h:], mod)
    need = (-1 - rA) % mod          # 1 + a + b = 0
    idx = np.searchsorted(rB, need)
    idx2 = np.minimum(idx, len(rB) - 1)
    hit = (rB[idx2] == need)
    cnt = sum(int(a) * int(b) for a, b in zip(wA[hit], wB[idx2[hit]]))
    return Fraction(cnt, 4 ** (g - 1))


def P0_dp(p, g, s):
    """validation of P0 by residue DP (small p^s)"""
    mod = p ** s
    c = np.zeros(mod, dtype=object)
    c[1 % mod] = 1
    for k in range(1, g):
        a = pi_int(-g, k) % mod
        c = 2 * c + np.roll(c, a) + np.roll(c, -a)
    return Fraction(int(c[0]), 4 ** (g - 1))


class Consts:
    """exact q_s for s <= sx (computed); qt(s) = q-tilde used in Prop E' (S = 8 for p <= 13, 4 above);
    qb(d) = an upper bound for q_d valid for every d (exact when d <= sx)."""

    def __init__(self, p, sx=None, S=None):
        self.p = p
        if sx is None:
            sx = 8 if p <= 13 else 5
        self.sx = sx
        if p <= 13:
            self.q = q_enum(p, max(sx, 8))
        else:
            self.q = {s: q_from_counts(p, s, q_counts_dp(p, s)) for s in range(1, sx + 1)}
        self.S = S if S is not None else (8 if p <= 13 else 4)

    def qb(self, d):
        if d in self.q:
            return self.q[d]
        top = max(self.q)
        return self.q[top] * Fraction(self.p) ** (d - top)

    def qt(self, s):
        S = self.S
        return self.q[s] if s <= S else self.q[S] * Fraction(self.p) ** (s - S)


# ------------------------------------------------------------------ Lemma Q right-hand side (per u)
def lemmaQ_rhs(p, gl, k, f, C, variant=None):
    """gl = [(g_r, s_r)] gates of u in [1,t] (relative positions), k <= V_t, f integer or None.
    variant: None (the lemma), 'half2D', 'noq' (q_s -> 1), 'noM' (drop k - M clause)."""
    g1, s1 = gl[0]
    b = P0(p, g1, min(s1, k))
    L, M, r = s1, s1, 1
    while L < k:
        s2 = gl[r][1]
        L2, M2 = L + s2, max(M, s2)
        lim = (f if f is not None else -10 ** 9)
        if variant != 'noM':
            lim = min(lim, k - M2)
        if f is not None and s2 == 1 and L2 <= lim:
            fac = C.q[2] / p ** 2
            if variant == 'half2D':
                fac /= 2
        else:
            d = min(s2, k - L)
            fac = (Fraction(1) if variant == 'noq' else C.qb(d)) / Fraction(p) ** d
        b *= fac
        L, M, r = L2, M2, r + 1
    return b


# ------------------------------------------------------------------ Props D / E, block (suffix) form
def propDE_block(p, gl, n, Np, K, C, fprime=None):
    """p^K [2^-H + sum_{a_c>=K} 2^{-c-1} + sum_{a_c<K} 2^{-c-1} P0 Suf_beta(c)]  (exact mpq).
    gl = [(G_b, s_b)] absolute gate positions in (n, Np], increasing; sum s_b = K.
    fprime None -> Prop D (all blocks 1D); else Prop E with 2D blocks where the end gate has depth 1 and
    end level <= fprime."""
    H = Np - n
    B = len(gl)
    G = [g for g, _ in gl]; S = [s for _, s in gl]
    lam = [0]
    for s in S:
        lam.append(lam[-1] + s)
    assert lam[-1] == K
    q2p2 = mpq(C.q[2].numerator, C.q[2].denominator) / (p * p)
    qcache = {}

    def q1d(d):
        if d not in qcache:
            x = C.qb(d)
            qcache[d] = mpq(x.numerator, x.denominator) / mpq(p) ** d
        return qcache[d]

    # Suf[b] for b = 1..B (1-based gate index): product over blocks b..B-1 (block b' ends at gate b'+1)
    Suf = [None] * (B + 2)
    Suf[B] = mpq(1)
    for b in range(B - 1, 0, -1):
        s_end = S[b]            # depth of gate b+1 (0-based index b)
        lam_end = lam[b + 1]
        if fprime is not None and s_end == 1 and lam_end <= fprime:
            fac = q2p2
        else:
            d = min(s_end, K - lam[b])
            fac = q1d(d)
        Suf[b] = Suf[b + 1] * fac
    tot = mpq(1, 2 ** H)
    # c with n+c >= G_B : a_c = K
    for pos in range(G[-1], Np):
        tot += mpq(1, 2 ** (pos - n + 1))
    prev = n
    for b in range(1, B + 1):
        a_c = lam[b - 1]
        w = mpq(0)
        for pos in range(prev, G[b - 1]):
            c = pos - n
            pz = P0(p, G[b - 1] - pos, min(S[b - 1], K - a_c))
            if pz:
                w += mpq(pz.numerator, pz.denominator) / mpz(2) ** (c + 1)
        tot += w * Suf[b]
        prev = G[b - 1]
    return mpq(p) ** K * tot


def propDE_literal(p, gl, n, Np, K, C, theta=None, MW=None):
    """the same bound computed literally per c by applying lemmaQ_rhs at u = x+n+c
    (relative gate lists), with f = theta - a_c; MW given -> Prop E (k - M_W in place of running max,
    implemented by passing gates with the running max replaced)."""
    H = Np - n
    tot = Fraction(1, 2 ** H)
    a = 0
    G = [g for g, _ in gl]; S = [s for _, s in gl]
    for c in range(H):
        pos = n + c
        a = sum(s for g, s in gl if g <= pos)
        if a >= K:
            tot += Fraction(1, 2 ** (c + 1))
            continue
        rel = [(g - pos, s) for g, s in gl if g > pos]
        k = K - a
        if theta is None:
            b = lemmaQ_rhs(p, rel, k, None, C)
        else:
            f = theta - a
            if MW is None:
                b = lemmaQ_rhs(p, rel, k, f, C)
            else:
                b = lemmaQ_rhs_MW(p, rel, k, f, C, MW)
        tot += Fraction(1, 2 ** (c + 1)) * b
    return Fraction(p) ** K * tot


def lemmaQ_rhs_MW(p, gl, k, f, C, MW):
    g1, s1 = gl[0]
    b = P0(p, g1, min(s1, k))
    L, r = s1, 1
    while L < k:
        s2 = gl[r][1]
        L2 = L + s2
        if s2 == 1 and L2 <= min(f, k - MW):
            fac = C.q[2] / p ** 2
        else:
            d = min(s2, k - L)
            fac = C.qb(d) / Fraction(p) ** d
        b *= fac
        L, r = L2, r + 1
    return b


# ------------------------------------------------------------------ Prop E' (closed form), my own evaluation
def eprime_constants(C, dps=50):
    import mpmath as mp
    mp.mp.dps = dps
    p, S = C.p, C.S
    lq = lambda s: mp.log(mp.mpf(C.qt(s).numerator) / C.qt(s).denominator)
    # Delta_s >= 0 for all s (needed by the derivation): check s <= S+1 explicitly; above S, Delta = log p
    for s in range(2, S + 2):
        assert C.qt(s) >= C.qt(s - 1), ("Delta_s < 0", s)
    rho1 = lq(1) + mp.fsum((lq(s) - lq(s - 1)) / mp.mpf(p) ** (s - 1) for s in range(2, S + 1)) \
        + mp.fsum(mp.log(p) / mp.mpf(p) ** (s - 1) for s in range(S + 1, S + 400))
    # tail beyond S+400 is < p^-(S+398) * log p * 2: add it explicitly as an upper bound
    rho1 += 2 * mp.log(p) / mp.mpf(p) ** (S + 398)
    gamma = lq(1) - (lq(2) - mp.log(p))
    kappa = (p - 1) * mp.log(2) - mp.log(p) + rho1 - gamma * mp.mpf(p - 1) ** 2 / p ** 2
    return dict(lq=lq, rho1=rho1, gamma=gamma, kappa=kappa)


def eprime_ln(C, E, K, H, sigma, fprime):
    """ln of Prop E' RHS:  p^K 2^-H (1+2^p) + 2^{p+sigma(p-1)} exp(K rho1 + ln(qt_sigma/q1) + gamma(2-1/p)
       - gamma (f'-sigma+1)(p-1)^2/p^2) e^-kappa/(1-e^-kappa)"""
    import mpmath as mp
    p = C.p
    assert E['kappa'] > 0
    t1 = K * mp.log(p) - H * mp.log(2) + mp.log(1 + mp.mpf(2) ** p)
    g = E['gamma']
    t2 = (p + sigma * (p - 1)) * mp.log(2) + K * E['rho1'] + (E['lq'](sigma) - E['lq'](1)) + g * (2 - mp.mpf(1) / p) \
        - g * (fprime - sigma + 1) * mp.mpf(p - 1) ** 2 / p ** 2 - E['kappa'] - mp.log(1 - mp.exp(-E['kappa']))
    hi = max(t1, t2)
    return hi + mp.log(mp.exp(t1 - hi) + mp.exp(t2 - hi))


# ------------------------------------------------------------------ exact signed DP with CRT (for tests)
CRT_Q = [2305843009213693951, 2305843009213693921, 2305843009213693907, 2305843009213693669]


def _crt(res, qs):
    x, M = 0, 1
    for r, q in zip(res, qs):
        t = ((r - x) * pow(M, -1, q)) % q
        x += M * t
        M *= q
    return x, M


class JointDP:
    """counts of (sum dt_c a_c mod p^ka, sum dt_c b_c mod p^kb); dt_0 = 1 if first_fixed, else signed.
    Counts kept modulo several primes < 2^61 (so 2A + roll + roll < 2^63)."""

    def __init__(self, p, ka, kb, nprimes):
        self.p, self.ka, self.kb = p, ka, kb
        self.qs = CRT_Q[:nprimes]
        self.qv = np.array(self.qs, dtype=np.int64).reshape(-1, 1, 1)
        self.A = np.zeros((nprimes, p ** ka, p ** kb), dtype=np.int64)
        self.ns = 0
        self.started = False

    def step(self, a, b, fixed=False):
        a %= self.p ** self.ka
        b %= self.p ** self.kb
        if fixed:
            assert not self.started
            self.A[:, a, b] = 1
            self.started = True
            return
        if not self.started:
            self.A[:, 0, 0] = 1
            self.started = True
        A = self.A
        self.A = (2 * A + np.roll(A, (a, b), axis=(1, 2)) + np.roll(A, (-a, -b), axis=(1, 2))) % self.qv
        self.ns += 1

    def count(self, k, f):
        """exact number (out of 4^ns) with first = 0 mod p^k, second = 0 mod p^f (f<=0: none)"""
        sk = self.p ** k
        sf = self.p ** f if (f is not None and f > 0) else 1
        sub = self.A[:, ::sk, ::sf]
        lo = (sub & ((1 << 31) - 1)).sum(axis=(1, 2))
        hi = (sub >> 31).sum(axis=(1, 2))
        res = [(int(hi[i]) * (1 << 31) + int(lo[i])) % self.qs[i] for i in range(len(self.qs))]
        x, M = _crt(res, self.qs)
        assert x <= 4 ** self.ns and 4 ** self.ns < M, "CRT range"
        return x
