"""Independent exact-arithmetic library for the adversarial (numerical falsification) check of
round-4 track M4A.  Written from the statements in data/round4/reports/M4A.md only; it shares no
code with code/round4/M4A/.

Conventions
-----------
* p odd prime, v = v_p.  A p-adic integer u is represented by an integer representative modulo
  p**E (E large).  Valuations v(u+i) are only trusted when they are < E (checked).
* signed digit: P(0)=1/2, P(+1)=P(-1)=1/4.  Exact probabilities are kept as integer counts with
  weights (1,2,1) per digit, i.e. a count over 4**(#signed digits).
* Exact DP: counts are kept modulo several primes ~2^60 (int64 numpy arrays) and reconstructed
  by CRT; the reconstructed count is checked to be <= the total weight, so it is the true count.
"""
from fractions import Fraction
from functools import lru_cache
import numpy as np

CRT_PRIMES = [1152921504606846883, 1152921504606846869, 1152921504606846803]


# ----------------------------------------------------------------------------- valuations
def vp(n, p):
    n = int(n)
    if n == 0:
        raise ValueError("v_p(0)")
    n = abs(n)
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def vmod(a, p, E):
    """valuation of a residue a mod p^E, requiring a != 0 mod p^E"""
    a %= p ** E
    if a == 0:
        raise ValueError("valuation >= E: precision exhausted")
    return vp(a, p)


def gates(u, p, E, t):
    """list of (i, depth) for 1<=i<=t with p | u+i"""
    out = []
    for i in range(1, t + 1):
        if (u + i) % p == 0:
            out.append((i, vmod(u + i, p, E)))
    return out


def V(u, p, E, t):
    return sum(s for _, s in gates(u, p, E, t))


# ----------------------------------------------------------------------------- constants
def signed_value_dist(coeffs, first_fixed):
    """exact distribution of sum_c zeta_c*coeffs[c] over the integers, zeta signed i.i.d.
    (zeta_0 = 1 if first_fixed).  Returns dict value -> integer weight, and total weight."""
    dist = {}
    if first_fixed:
        dist = {coeffs[0]: 1}
        rest = coeffs[1:]
    else:
        dist = {0: 1}
        rest = coeffs
    for a in rest:
        nd = {}
        for val, w in dist.items():
            for d, wd in ((-1, 1), (0, 2), (1, 1)):
                key = val + d * a
                nd[key] = nd.get(key, 0) + w * wd
        dist = nd
    return dist, 4 ** len(rest)


def pi_at(y, k):
    r = 1
    for i in range(1, k + 1):
        r *= (y + i)
    return r


@lru_cache(maxsize=None)
def q_consts(p, smax):
    """q_s = p^s max_z P(Z = z mod p^s), Z = sum_{k<p} zeta_k pi_k(-p), zeta signed (zeta_0 signed)."""
    coeffs = [pi_at(-p, k) for k in range(p)]
    dist, tot = signed_value_dist(coeffs, first_fixed=False)
    q = {}
    for s in range(1, smax + 1):
        mod = p ** s
        agg = {}
        for val, w in dist.items():
            agg[val % mod] = agg.get(val % mod, 0) + w
        q[s] = Fraction(mod * max(agg.values()), tot)
    return q


@lru_cache(maxsize=None)
def P0(p, g, s):
    """P( sum_{c<g} zeta_c pi_c(-g) = 0 mod p^s ), zeta_0 = 1, others signed."""
    if s <= 0:
        return Fraction(1)
    coeffs = [pi_at(-g, c) for c in range(g)]
    dist, tot = signed_value_dist(coeffs, first_fixed=True)
    mod = p ** s
    w = sum(wt for val, wt in dist.items() if val % mod == 0)
    return Fraction(w, tot)


def q_of(p, d, q):
    """q_d with q given up to some smax; beyond, the exact value is computed on demand"""
    if d in q:
        return q[d]
    return q_consts(p, d)[d]


# ----------------------------------------------------------------------------- Lemma Q bound
def lemmaQ_bound(p, u, E, t, k, f, mode="Q", MW=None):
    """Right-hand side of Lemma Q for P(v(T_u)>=k, v(T_u')>=f), T_u=sum_{c<t} dt_c pi_c(u).
    f=None means no slope condition (f=-infinity).
    mode 'Q'  : the statement of Lemma Q (running max M_{r+1}).
    mode 'MW' : Prop E variant, running max replaced by MW (>= every M_{r+1}).
    Control modes (stronger, unproved variants used as negative controls):
    'noM'     : drop the k-M_{r+1} constraint in the 2D condition.
    'half2D'  : 2D factor q_2/(2p^2).
    'depth2'  : allow end gates of depth <=2 to count as 2D (factor q_2/p^2).
    'noq'     : exact block-0 factor, but 1D factor 1/p^d instead of q_d/p^d (pretend q_s = 1).
    Returns Fraction."""
    gl = gates(u, p, E, t)
    Vt = sum(s for _, s in gl)
    assert 1 <= k <= Vt, (k, Vt)
    g1, s1 = gl[0]
    q = q_consts(p, 10)
    b = P0(p, g1, min(s1, k))
    L = s1
    Mrun = s1
    r = 0
    while L < k:
        r += 1
        # block r = [g_r, g_{r+1}); its end gate is gl[r]
        gi, s_next = gl[r]
        Lnext = L + s_next
        Mnext = max(Mrun, s_next)
        Mused = MW if mode == "MW" else Mnext
        ff = -10 ** 9 if f is None else f
        if mode == "noM":
            twoD = (s_next == 1 and Lnext <= ff)
        elif mode == "depth2":
            twoD = (s_next <= 2 and Lnext <= min(ff, k - Mused))
        else:
            twoD = (s_next == 1 and Lnext <= min(ff, k - Mused))
        if twoD:
            fac = q[2] / p ** 2
            if mode == "half2D":
                fac = fac / 2
        else:
            d = min(s_next, k - L)
            fac = (q_of(p, d, q) if mode != "noq" else Fraction(1)) / Fraction(p) ** d
        b *= fac
        L = Lnext
        Mrun = Mnext
    return b


# ----------------------------------------------------------------------------- exact DP
def crt(res, primes):
    x, M = 0, 1
    for r, q in zip(res, primes):
        # solve x' = x mod M, x' = r mod q
        t = ((int(r) - x) * pow(M, -1, q)) % q
        x = x + M * t
        M *= q
    return x, M


class SignedDP:
    """Joint law of (sum dt_c A_c mod p^ka, sum dt_c B_c mod p^kb) for signed digits dt_c,
    with dt_0 = 1 if first_fixed.  Counts mod CRT primes (int64)."""

    def __init__(self, p, ka, kb, first_fixed, nprimes=2):
        self.p, self.ka, self.kb = p, ka, kb
        self.ma, self.mb = p ** ka, p ** kb
        self.primes = CRT_PRIMES[:nprimes]
        self.q = np.array(self.primes, dtype=np.int64).reshape(-1, 1, 1)
        self.A = np.zeros((nprimes, self.ma, self.mb), dtype=np.int64)
        self.first_fixed = first_fixed
        self.nsigned = 0
        self.started = False

    def step(self, a, b):
        a %= self.ma
        b %= self.mb
        if not self.started:
            self.started = True
            if self.first_fixed:
                self.A[:, a, b] = 1
                return
            self.A[:, 0, 0] = 1
        A = self.A
        A = (2 * A + np.roll(A, (a, b), axis=(1, 2)) + np.roll(A, (-a, -b), axis=(1, 2))) % self.q
        self.A = A
        self.nsigned += 1

    def count_zero_fast(self, k, f):
        """same as count_zero, summing in int64 via a 30-bit hi/lo split (exact)."""
        sk = self.p ** max(k, 0)
        sf = self.p ** f if (f is not None and f > 0) else 1
        sub = self.A[:, ::sk, ::sf]
        lo = (sub & ((1 << 30) - 1)).sum(axis=(1, 2))
        hi = (sub >> 30).sum(axis=(1, 2))
        res = [(int(hi[i]) * (1 << 30) + int(lo[i])) % self.primes[i] for i in range(len(self.primes))]
        x, M = crt(res, self.primes)
        tot = 4 ** self.nsigned
        assert x <= tot, "CRT overflow: add primes"
        return x, tot

    def count_zero(self, k, f):
        """exact count of configurations with first coord = 0 mod p^k and second = 0 mod p^f
        (k<=ka, f<=kb; f<=0 means no condition).  Total weight 4**nsigned."""
        sk = self.p ** max(k, 0)
        sf = self.p ** max(f, 0) if f is not None and f > 0 else 1
        sub = self.A[:, ::sk, ::sf]
        res = [int(sub[i].astype(object).sum()) % self.primes[i] for i in range(len(self.primes))]
        x, M = crt(res, self.primes)
        tot = 4 ** self.nsigned
        assert x <= tot, "CRT overflow: add primes"
        return x, tot


def pi_and_deriv(u, cmax, mod):
    """lists pi_c(u) mod `mod` and pi_c'(u) mod `mod` for 0<=c<cmax"""
    P = [1]
    Dv = [0]
    for c in range(1, cmax):
        P.append(P[-1] * (u + c) % mod)
        Dv.append((Dv[-1] * (u + c) + P[-2]) % mod)
    return P, Dv


# ----------------------------------------------------------------------------- windows
def window_elems(x, n, H, mod):
    """y_c(x) = prod_{i=1}^c (x+n+i) mod `mod` and its x-derivative, 0<=c<H"""
    Y = [1]
    Yd = [0]
    for c in range(1, H):
        Y.append(Y[-1] * (x + n + c) % mod)
        Yd.append((Yd[-1] * (x + n + c) + Y[-2]) % mod)
    return Y, Yd


def coll_counts(p, x, n, H, K, nprimes=2):
    """exact count for Coll_j(x), all j<=K: returns dp so that dp.count_zero(j,0)/4^H = Coll_j"""
    Y, _ = window_elems(x, n, H, p ** K)
    dp = SignedDP(p, K, 0, first_fixed=False, nprimes=nprimes)
    for c in range(H):
        dp.step(Y[c], 0)
    return dp


# ----------------------------------------------------------------------------- Prop D / E (via Lemma Q, per c)
def propDE_via_Q(p, x, E, n, Np, K, theta=None, MW=None, mode="Q"):
    """p^K [2^-H + sum_{a_c>=K} 2^{-c-1} + sum_{a_c<K} 2^{-c-1} * p^{-k}*... ] computed literally as
    2^-H p^K + sum_c 2^{-c-1} p^{a_c} * p^{K-a_c} * LemmaQ(u=x+n+c, t=H-c, k=K-a_c, f=theta-a_c).
    theta=None -> Prop D (no slope).  mode 'MW' -> Prop E's M_W variant."""
    H = Np - n
    tot = Fraction(1, 2 ** H) * p ** K
    a = 0  # a_c = V_{n+c}-V_n
    for c in range(H):
        if c >= 1 and (x + n + c) % p == 0:
            a += vmod(x + n + c, p, E)
        if a >= K:
            tot += Fraction(p ** K, 2 ** (c + 1))
            continue
        k = K - a
        f = None if theta is None else theta - a
        b = lemmaQ_bound(p, x + n + c, E, H - c, k, f, mode=mode, MW=MW)
        tot += Fraction(p ** K, 2 ** (c + 1)) * b
    return tot


# ----------------------------------------------------------------------------- block form (efficient, for big windows)
def block_bound(p, gl, n, Np, K, fprime=None, exact=True):
    """Block (Suf) form of Prop D (fprime=None) / Prop E (fprime = min(theta, K - M_W)).
    gl: list of (position i, depth) of the gates of x in (n, Np], increasing.
    Returns p^K*[2^-H + sum ...] as gmpy2 mpq if exact."""
    import gmpy2
    from gmpy2 import mpq
    H = Np - n
    q = q_consts(p, 12)
    Q = {d: mpq(q[d].numerator, q[d].denominator) for d in q}
    G = [g for g, _ in gl]
    S = [s for _, s in gl]
    nb = len(G)
    lam = [0] * (nb + 1)  # lam[b] = level after gate b (1-based), lam[0]=0
    for b in range(1, nb + 1):
        lam[b] = lam[b - 1] + S[b - 1]
    assert lam[nb] == K, (lam[nb], K)
    # block factor for block b (1-based, = [G_b, G_{b+1})), defined when lam[b] < K
    pq2 = Q[2] / (p * p)

    def fac(b):
        s_next = S[b]          # depth of gate b+1
        if fprime is not None and s_next == 1 and lam[b + 1] <= fprime:
            return pq2
        d = min(s_next, K - lam[b])
        qd = Q[d] if d in Q else mpq(q_consts(p, d)[d].numerator, q_consts(p, d)[d].denominator)
        return qd / mpq(p) ** d

    # w_b = sum over c with beta(c)=b of 2^{-c-1} P0(g1(c), min(s_b, K - a_c)), a_c = lam[b-1]
    # total = sum_b w_b Suf_b with Suf_b = prod_{b'=b}^{nb-1} fac(b')  (lam[b'] < K iff b' < nb)
    # forward Horner: acc = (((w_1 f_1 + w_2) f_2 + ...) + w_{nb-1}) f_{nb-1} + w_nb
    acc = mpq(0)
    for b in range(1, nb + 1):
        lo = n if b == 1 else G[b - 2]      # c ranges over n+c in [G_{b-1}, G_b)
        w = mpq(0)
        a_c = lam[b - 1]
        for pos in range(lo, G[b - 1]):
            c = pos - n
            g1 = G[b - 1] - pos
            pz = P0(p, g1, min(S[b - 1], K - a_c))
            if pz:
                w += mpq(pz.numerator, pz.denominator) / mpq(2) ** (c + 1)
        if b < nb:
            assert lam[b] < K
            acc = (acc + w) * fac(b)
        else:
            acc = acc + w
    # terms with a_c >= K: c with no gate in (n+c, Np], i.e. n+c >= G_last
    tail = mpq(0)
    for pos in range(G[-1], Np):
        c = pos - n
        tail += mpq(1) / mpq(2) ** (c + 1)
    return mpq(p) ** K * (mpq(1) / mpq(2) ** H + tail + acc)


# ----------------------------------------------------------------------------- Prop E' closed form
def eprime_consts(p, S=8, prec=60):
    import mpmath as mp
    mp.mp.dps = prec
    q = q_consts(p, S)
    qf = {s: mp.mpf(q[s].numerator) / q[s].denominator for s in q}
    lq = {s: mp.log(qf[s]) for s in qf}
    rho1 = lq[1] + sum((lq[s] - lq[s - 1]) / mp.mpf(p) ** (s - 1) for s in range(2, S + 1)) \
        + mp.log(p) * mp.mpf(p) ** (-S) / (1 - mp.mpf(1) / p)
    gamma = lq[1] - mp.log(qf[2] / p)
    kappa = (p - 1) * mp.log(2) - mp.log(p) + rho1 - gamma * mp.mpf((p - 1) ** 2) / p ** 2
    return dict(q=qf, lq=lq, rho1=rho1, gamma=gamma, kappa=kappa, S=S)


def log_qtilde(p, s, C):
    import mpmath as mp
    S = C["S"]
    if s <= S:
        return C["lq"][max(s, 1)]
    return C["lq"][S] + (s - S) * mp.log(p)


def eprime_log(p, K, H, sigma, fprime, C):
    """natural log of the Prop E' right-hand side (requires kappa>0)."""
    import mpmath as mp
    assert C["kappa"] > 0
    t1 = K * mp.log(p) - H * mp.log(2) + mp.log(1 + mp.mpf(2) ** p)
    g = C["gamma"]
    t2 = (p + sigma * (p - 1)) * mp.log(2) + K * C["rho1"] + (log_qtilde(p, sigma, C) - C["lq"][1]) \
        + g * (2 - mp.mpf(1) / p) - g * (fprime - sigma + 1) * mp.mpf((p - 1) ** 2) / p ** 2 \
        + (-C["kappa"]) - mp.log(1 - mp.exp(-C["kappa"]))
    m = max(t1, t2)
    return m + mp.log(mp.exp(t1 - m) + mp.exp(t2 - m))
