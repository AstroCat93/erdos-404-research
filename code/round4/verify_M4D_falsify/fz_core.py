"""Exact-arithmetic core for the numerical falsification of M4D's Lemma L,
Theorem F and Corollary F1 (round 4, track verify_M4D_falsify).

Written from the definitions only (note.md sec. 1.2-1.4, M4D report sec. 1-2);
it shares no code with code/round4/M4D/ or with other checkers.

Conventions.
  * x is always a NATURAL number (a legitimate point of Z_p that is not a
    negative integer).  All polynomials are evaluated exactly with Python
    integers, so S_e(x), pi_n(x) are exact; reductions mod p^k are applied
    only at the very end of a computation.
  * A path of length n is a 0/1 tuple e = (e_0,...,e_{n-1}) with e_0 = 1;
    S_e = sum_{j<n} e_j pi_j(x).  It is alive at n iff p^{V_n} | S_e.
  * target tau_n(e,x) = -S_e / pi_n  (a p-adic integer when e is alive).
"""
import random

import numpy as np


# ---------------------------------------------------------------- valuations
def vp(n, p):
    """p-adic valuation of a nonzero integer."""
    if n == 0:
        raise ValueError("vp(0)")
    n = abs(n)
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def vp_fact(n, p):
    """v_p(n!) by Legendre."""
    s, q = 0, p
    while q <= n:
        s += n // q
        q *= p
    return s


def pis(x, n):
    """[pi_0(x), ..., pi_n(x)] exactly."""
    out = [1]
    for j in range(1, n + 1):
        out.append(out[-1] * (x + j))
    return out


def dpis(x, n):
    """[pi_0'(x), ..., pi_n'(x)] exactly (derivative of the polynomial)."""
    P = [1]
    dP = [0]
    for j in range(1, n + 1):
        dP.append(dP[-1] * (x + j) + P[-1])
        P.append(P[-1] * (x + j))
    return dP


def Vlist(x, n, p):
    """[V_0, ..., V_n] with V_m = v(pi_m(x)) = sum_{i<=m} v(x+i)."""
    out = [0]
    for i in range(1, n + 1):
        out.append(out[-1] + vp(x + i, p))
    return out


def Mval(x, n, p):
    """M_n = max_{1<=i<=n} v(x+i) (0 if n = 0)."""
    return max([vp(x + i, p) for i in range(1, n + 1)] or [0])


# ---------------------------------------------------------------- targets
def target(S, pin, p, k):
    """-S/pin mod p^k, for S with v(S) >= v(pin).  Exact."""
    V = vp(pin, p)
    q = p ** V
    if S % q:
        raise ValueError("not alive")
    a = S // q
    b = pin // q
    mod = p ** k
    if mod == 1:
        return 0
    return (-a * pow(b, -1, mod)) % mod


# ---------------------------------------------------------------- alive paths
def alive_paths_bruteforce(x, n, p):
    """All alive paths at n by enumerating all 2^(n-1) paths (no pruning)."""
    P = pis(x, n)
    q = p ** vp(P[n], p)
    out = []
    for mask in range(1 << (n - 1)):
        e = (1,) + tuple((mask >> (j - 1)) & 1 for j in range(1, n))
        S = sum(P[j] for j in range(n) if e[j])
        if S % q == 0:
            out.append((e, S))
    return out


def alive_paths_dfs(x, n, p, P=None, V=None, cap=None):
    """All alive paths at n, by depth-first growth with exact integers.

    Pruning uses only: (e,b) alive at m+1  =>  e alive at m  (the converse in
    (F2)); alive_paths_bruteforce validates this pruning on small n.
    Returns list of (e, S_e).  If cap is given and some level exceeds it,
    returns None.
    """
    if n < 1:
        raise ValueError
    if P is None:
        P = pis(x, n)
    if V is None:
        V = Vlist(x, n, p)
    level = [((1,), 1)] if 1 % (p ** V[1]) == 0 else []
    for m in range(1, n):
        q = p ** V[m + 1]
        nxt = []
        for e, S in level:
            if S % q == 0:
                nxt.append((e + (0,), S))
            S1 = S + P[m]
            if S1 % q == 0:
                nxt.append((e + (1,), S1))
        level = nxt
        if cap is not None and len(level) > cap:
            return None
    return level


def target_sets_dp(x, times, p, Vtop):
    """Independent DP for the alive-target sets.

    Carries the set of targets tau_m mod p^(Vtop - V_m) of alive paths via
    tau_{m+1} = (tau_m - e_m)/(x+m+1)  (alive iff v(tau_m - e_m) >= v(x+m+1)),
    starting from tau_0 = 0 with e_0 = 1 forced.  Returns {t: set of
    targets mod p^(Vtop - V_t)} for t in times.  Requires Vtop >= V_max(times).
    """
    times = sorted(times)
    N = times[-1]
    out = {}
    prec = Vtop  # precision of tau_0 = 0
    cur = {0}
    for m in range(0, N):
        y = x + m + 1
        d = vp(y, p)
        w = y // p ** d
        newprec = prec - d
        if newprec < 0:
            raise ValueError("precision exhausted")
        modn = p ** newprec
        winv = pow(w, -1, modn) if modn > 1 else 0
        pd = p ** d
        digits = (1,) if m == 0 else (0, 1)
        nxt = set()
        for t in cur:
            for b in digits:
                z = t - b
                if z % pd == 0:
                    nxt.add(((z // pd) * winv) % modn)
        cur = nxt
        prec = newprec
        if (m + 1) in times:
            out[m + 1] = set(cur)
    return out


# ---------------------------------------------------------------- windows
class Window:
    """Window W = [n, N) at x: elements y_i = prod_{s=1}^i (x+n+s), i<H."""

    def __init__(self, x, n, N, p):
        self.x, self.n, self.N, self.p = x, n, N, p
        self.H = N - n
        ys = [1]
        for s in range(1, self.H + 1):
            ys.append(ys[-1] * (x + n + s))
        self.y = ys[: self.H]          # y_0..y_{H-1}
        yH = ys[self.H]                # = pi_N / pi_n
        self.D = vp(yH, p)
        self.unit = yH // p ** self.D  # u = pi_N/(p^D pi_n), exact integer unit

    def sums_mask(self, K):
        """Boolean array of length p^K: True at residues of the 2^H sums Q_f."""
        M = self.p ** K
        arr = np.zeros(M, dtype=bool)
        arr[0] = True
        for yi in self.y:
            sh = yi % M
            if sh:
                arr = arr | np.roll(arr, sh)
        return arr

    def sums_list_exact(self):
        """All 2^H exact window sums Q_f, indexed by f encoded as an int."""
        Q = [0]
        for i, yi in enumerate(self.y):
            Q = Q + [q + yi for q in Q]
        return Q  # index bit i <-> f_i


def lift_counts(win, Dn):
    """|Lift(r)| for r in Z/p^D, with band Dn: counts of residues of
    Sigma = {Q_f mod p^(D+Dn)} that are = r mod p^D."""
    p, D = win.p, win.D
    arr = win.sums_mask(D + Dn)
    return arr.reshape(p ** Dn, p ** D).sum(axis=0).astype(np.int64)


# ---------------------------------------------------------------- samplers
def rand_unit(p, rng, lo=1, hi=None):
    hi = hi or p ** 6
    while True:
        u = rng.randrange(lo, hi)
        if u % p:
            return u


def x_with_gate(p, rng, i, s, extra=40):
    """A natural x with v(x+i) = s exactly (i >= 1, s >= 0)."""
    if s == 0:
        while True:
            x = rng.randrange(p ** 10, p ** extra)
            if vp(x + i, p):
                continue
            return x
    u = rand_unit(p, rng, p ** 3, p ** (extra - s if extra > s + 4 else s + 4))
    return u * p ** s - i


def sample_x(p, rng, kind, nmax):
    """Edge-case samplers.  Returns (x, label)."""
    if kind == "rand":
        return rng.randrange(p ** 8, p ** 40), "rand"
    if kind == "near-1":
        s = rng.randint(1, 6)
        return x_with_gate(p, rng, 1, s), "x=-1 mod p^%d" % s
    if kind == "near-2":
        s = rng.randint(1, 6)
        return x_with_gate(p, rng, 2, s), "x=-2 mod p^%d" % s
    if kind == "negint":
        m = rng.randint(3, max(3, nmax + 3))
        s = rng.randint(1, 6)
        return x_with_gate(p, rng, m, s), "x=-%d mod p^%d" % (m, s)
    raise ValueError(kind)
