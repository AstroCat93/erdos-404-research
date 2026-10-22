# Independent implementation (refute-Theorem_11.29-counterexample track), p = 2.
# Notation as in note_v3 section 10.1 / 11.3.
import random
from fractions import Fraction

P = 600            # working 2-adic precision
MOD = 1 << P

def v(n):
    """2-adic valuation of an integer (n != 0); returns P for n == 0 mod 2^P."""
    n %= MOD
    if n == 0:
        return P
    return (n & -n).bit_length() - 1

def vfrac(q):
    q = Fraction(q)
    if q == 0:
        return None
    a, b = q.numerator, q.denominator
    return v(a) - v(b)

def s(n):
    return bin(n).count("1")

CLASSES = {  # name: (k, r0, L, l0, sL, E_C, Vcert)
    "C0": (3, 0, 1, 4, 2, 1, 4),
    "C2": (3, 2, 3, 8, 3, 64, 7),
    "C6": (4, 6, 6, 14, 3, 16384, 11),
}

def rand_in_class(cls, rng):
    k, r0 = CLASSES[cls][0], CLASSES[cls][1]
    return (r0 + (rng.getrandbits(P - k) << k)) % MOD

def V(x, n):
    return sum(v(x + i) for i in range(1, n + 1))

def Mx(x, n):
    return max(v(x + i) for i in range(1, n + 1))

def W(x, n):
    return n - V(x, n)

def pis(x, n):
    """pi_j(x) and pi_j'(x) mod 2^P for j = 0..n."""
    pi = [1]; dpi = [0]
    for j in range(1, n + 1):
        a = (x + j) % MOD
        dpi.append((dpi[-1] * a + pi[-1]) % MOD)
        pi.append((pi[-1] * a) % MOD)
    return pi, dpi

def alive_paths(x, n, want_slope=True):
    """All paths e (e_0=1) of length n alive at n: list of (bits tuple, S, S')."""
    pi, dpi = pis(x, n)
    Vs = [0]
    for j in range(1, n + 1):
        Vs.append(Vs[-1] + v(x + j))
    # level j: prefixes of length j alive at j (v(S) >= V_j)
    cur = [((1,), 1, 0)]  # length 1: S = pi_0 = 1, alive since V_1 = v(x+1) = 0 for even x
    assert Vs[1] == 0, "x must be even"
    for j in range(1, n):
        nxt = []
        for bits, S, dS in cur:
            for e in (0, 1):
                S2 = (S + e * pi[j]) % MOD
                if v(S2) >= Vs[j + 1]:
                    nxt.append((bits + (e,), S2, (dS + e * dpi[j]) % MOD))
        cur = nxt
    return cur, Vs

def inv_odd(u, prec):
    return pow(u, -1, 1 << prec)

def a_weights(x, n, lam):
    """a_n^{(lam)}(t), t mod 2^lam: law of sum_{i<2lam} f_i pi_{n+i}(x)/pi_n(x) mod 2^lam."""
    if lam == 0:
        return {0: Fraction(1)}
    m = 1 << lam
    # q_i = pi_{n+i}/pi_n = prod_{j=n+1}^{n+i} (x+j), integers
    qs = [1]
    for i in range(1, 2 * lam):
        qs.append(qs[-1] * (x + n + i) % MOD)
    dist = {0: 1}
    for q in qs:
        nd = {}
        for t, c in dist.items():
            for f in (0, 1):
                t2 = (t + f * q) % m
                nd[t2] = nd.get(t2, 0) + c
        dist = nd
    tot = 2 ** (2 * lam)
    return {t: Fraction(c, tot) for t, c in dist.items()}

def target_mod(x, n, S, prec):
    """tau_n = -S/pi_n(x) mod 2^prec (requires v(S) >= V_n)."""
    pi_n = 1
    for j in range(1, n + 1):
        pi_n = pi_n * (x + j) % MOD
    Vn = v(pi_n)
    num = (-S) % MOD
    assert v(num) >= Vn
    num >>= Vn
    u = pi_n >> Vn
    return num * inv_odd(u % (1 << prec), prec) % (1 << prec)

def rho(x, n, S, dS, ainfo=None):
    lam = v(dS)
    a = a_weights(x, n, lam)
    t = target_mod(x, n, S, lam) if lam > 0 else 0
    return (2 ** lam) * a.get(t, Fraction(0)), lam

def g_at_least(x, G, nmax=None):
    """True iff g_2(x) >= G. Tracks alive paths keyed by S mod 2^G (multiplicity irrelevant)."""
    mod = 1 << G
    Sset = {1 % mod}
    pi = 1; Vn = 0; n = 0
    # state: set of S_e mod 2^G for e alive at n (length n) ; start n=1 with S=1
    pi = 1  # pi_0
    n = 1
    pi = pi * (x + 1) % MOD; Vn = v(x + 1)   # V_1
    if Vn > 0:
        return G <= 0   # x odd: S=1 not alive at 1; g_2 = 0
    if Vn >= G:
        return True
    pi_prev = 1  # pi_{n-1}... we need pi_n when extending length n -> n+1 : add e_n*pi_n
    while True:
        # extend from length n to n+1: add e_n * pi_n
        new = set()
        pn = pi % mod
        Vn1 = Vn + v(x + n + 1)
        thr = min(Vn1, G)
        for S in Sset:
            for e in (0, 1):
                S2 = (S + e * pn) % mod
                if v(S2 if S2 else MOD) >= thr:
                    new.add(S2)
        n += 1
        pi = pi * (x + n) % MOD
        Vn = Vn1
        Sset = new
        if not Sset:
            return False
        if Vn >= G:
            return True

def alive_count_levels(x, ns, G):
    """For each n in ns (increasing), return number of distinct S mod 2^G alive at n (0 means P_n empty).
    Valid for 'nonempty' tests whenever V_n <= G."""
    mod = 1 << G
    Sset = {1}
    Vn = v(x + 1); pi = (x + 1) % MOD; n = 1
    out = {}
    target = set(ns)
    if 1 in target:
        out[1] = len(Sset)
    nmax = max(ns)
    while n < nmax:
        pn = pi % mod
        Vn1 = Vn + v(x + n + 1)
        thr = min(Vn1, G)
        new = set()
        for S in Sset:
            for e in (0, 1):
                S2 = (S + e * pn) % mod
                if v(S2 if S2 else MOD) >= thr:
                    new.add(S2)
        n += 1
        pi = pi * (x + n) % MOD
        Vn = Vn1
        Sset = new
        if n in target:
            out[n] = len(Sset)
    return out
