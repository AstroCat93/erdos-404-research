"""vlib.py -- helper library for the logic check of round-4 track M4B (Theorem B1 / B1').

The p-adic helpers PAdic, products, extend, alive_from_scratch, subset_sum_law and collision are
copied from code/round3/check_R3M/ck_lib.py (the independently validated library of the round-3
check of track R3M); that directory is read-only for this check, so they are copied here unchanged.
The window-time rules and the atom enumeration are new.

Conventions (R3M report section 1; M4B report section 2):
  pi_j(x) = (x+1)...(x+j), V_n = v(pi_n(x)), M_n = max_{i<=n} v(x+i), c_n = 2^-n p^{V_n}.
  A path of length n is a bitmask e with bit 0 set; S_e(x) = sum_{j<n} e_j pi_j(x);
  alive at n iff v(S_e(x)) >= V_n; slope = v(S_e'(x)).
  Random window times (M4B section 2): n_0 < n_1 deterministic, n_0 >= 2p; for l >= 1,
  n_{l+1} is a function of x mod p^{m_{l-1}(x)}, m_l := V_{n_l}(x)  ("two-step predictable").
"""
import math
from fractions import Fraction


# ----------------------------------------------------------------------------------------------
# copied from code/round3/check_R3M/ck_lib.py
class PAdic:
    """Fixed-precision context: integers mod p^prec."""

    def __init__(self, p, prec):
        self.p = p
        self.prec = prec
        self.mod = p ** prec

    def v(self, a):
        a %= self.mod
        if a == 0:
            return self.prec
        k = 0
        p = self.p
        while a % p == 0:
            a //= p
            k += 1
        return k


def products(P, x, N):
    mod = P.mod
    pi = [1] * (N + 1)
    dpi = [0] * (N + 1)
    vals = [None] * (N + 1)
    for j in range(1, N + 1):
        pi[j] = pi[j - 1] * (x + j) % mod
        dpi[j] = (dpi[j - 1] * (x + j) + pi[j - 1]) % mod
        vals[j] = P.v(x + j)
    return pi, dpi, vals


def extend(P, pi, dpi, vals, start, N, roots):
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
    root = (1, 1, 0)
    if P.v(1) < vals[1]:
        return []
    return extend(P, pi, dpi, vals, 1, n, [root])


def subset_sum_law(elems, modulus):
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
# end of copied part
# ----------------------------------------------------------------------------------------------


def vtrunc(a, p, m):
    """min(v_p(a), m), computed from a mod p^m only."""
    a %= p ** m
    if a == 0:
        return m
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def vfact(n, p):
    s, q = 0, p
    while q <= n:
        s += n // q
        q *= p
    return s


# ---------------------------------- window-time rules ------------------------------------------
# A rule is called as rule(p, xr, mprev, ns) where xr = x mod p^mprev and ns = [n_0, ..., n_l];
# it returns n_{l+1}.  TWO-STEP rules receive mprev = m_{l-1}; ONE-STEP (negative control) rules
# receive mprev = m_l.  Only xr (and the already constant n's) may be used.

def rule_ladder(r=1.25, R=12, T=24, Cp=1):
    """M4B section 2 example: least n >= ceil(r n_l) which is a C'-ladder point for horizon T,
    tested with truncated valuations min(v(x+i), mprev); fallback ceil(r n_l) + R."""
    def f(p, xr, mprev, ns):
        nl = ns[-1]
        base = math.ceil(r * nl)
        for n in range(base, base + R):
            s = 0
            ok = True
            for d in range(1, T + 1):
                s += vtrunc(xr + n + d, p, mprev)
                if p ** s > Cp * 2 ** d:
                    ok = False
                    break
            if ok:
                return n
        return base + R
    f.name = f"ladder(r={r},R={R},T={T},C'={Cp})"
    return f


def rule_hash(H=5):
    """an arbitrary ('wild') function of x mod p^mprev: n_{l+1} = n_l + 1 + hash % H."""
    def f(p, xr, mprev, ns):
        h = ((xr * 0x9E3779B1 + 1000003 * mprev + 7919 * ns[-1]) % (2 ** 61 - 1)) >> 7
        return ns[-1] + 1 + h % H
    f.name = f"hash(H={H})"
    return f


def window_times(p, x, n0, n1, rule, L, P, onestep=False):
    """n_0..n_L and m_0..m_L for x (an integer read mod p^prec).  If onestep, n_{l+1} is computed
    from x mod p^{m_l} (negative control) instead of x mod p^{m_{l-1}}."""
    ns = [n0, n1]
    ms = [sum(P.v(x + i) for i in range(1, n0 + 1)), sum(P.v(x + i) for i in range(1, n1 + 1))]
    for l in range(1, L):
        mprev = ms[l] if onestep else ms[l - 1]
        xr = x % p ** mprev
        nxt = rule(p, xr, mprev, ns)
        assert nxt > ns[-1]
        ns.append(nxt)
        ms.append(sum(P.v(x + i) for i in range(1, nxt + 1)))
    return ns, ms


def eps_composite(x, n, N, N2, p, D, K):
    """eps = p^K Coll_K - p^D Coll_D for the composite window [n, N2) (elements pi_j/pi_n)."""
    ys = []
    q = 1
    for k in range(N2 - n):
        ys.append(q)
        q *= x + n + k + 1
    return p ** K * collision(ys, p ** K) - p ** D * collision(ys, p ** D)


def chi2_window(x, n, N, p, D):
    """chi^2_W = p^D sum_r mu_W(r)^2 - 1 for W = [n, N) (uniform subset sums mod p^D)."""
    ys = []
    q = 1
    for k in range(N - n):
        ys.append(q)
        q *= x + n + k + 1
    return p ** D * collision(ys, p ** D) - 1
