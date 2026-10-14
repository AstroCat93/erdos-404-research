"""Exact-arithmetic core for the numerical falsification of M4D section 3
(Lemmas W1-W3, Prop W4, Cor W5, Thm W6: the weighted R3M machinery).

Written from the definitions (R3M report sec. 1-5, M4D report sec. 3).  It
shares no code with code/round4/M4D/ or code/round4/verify_M4D_logic/, and
not with this directory's fz_core.py either (that file serves the Lemma L /
Theorem F check).

Conventions
-----------
* x is a NATURAL number, hence a genuine point of Z_p that is not a negative
  integer.  Points of the cylinder C = x + p^m Z_p are x' = x + p^m * w with
  w a natural number; every x' is again a natural number.
* A path of length n is a 0/1 tuple e with e_0 = 1; S_e(X) = sum_j e_j pi_j(X).
  Alive at n: p^{V_n(x)} | S_e(x).  Target tau_n(e,x) = -S_e(x)/pi_n(x).
  Slope: v(S_e'(x)).
* Window W = [n,N): elements y_i = prod_{s=1}^{i}(x+n+s), 0 <= i < H; the
  digit string f in {0,1}^H is encoded as an int whose bit i is f_i;
  Q_f = sum_i f_i y_i.
* Every quantity that is a function of x' is recomputed AT x' from exact
  integers (S_e(x'), pi_n(x'), window elements at x').  Nothing uses the
  linearisation of R3M Lemma 2(b) except the tests that test it.
* Weights are integer numerators over an explicit integer denominator, so
  every mean and second moment below is an exact rational.
"""
import random
from fractions import Fraction

import numpy as np


# ------------------------------------------------------------------ basics
def vp(a, p):
    if a == 0:
        raise ValueError("vp(0)")
    a = abs(a)
    v = 0
    while a % p == 0:
        a //= p
        v += 1
    return v


def V_upto(x, N, p):
    """[V_0..V_N], V_t = v(pi_t(x)) = sum_{i<=t} v(x+i)."""
    out = [0]
    for i in range(1, N + 1):
        out.append(out[-1] + vp(x + i, p))
    return out


def M_upto(x, N, p):
    return max([vp(x + i, p) for i in range(1, N + 1)] or [0])


def exact_pis(x, n):
    out = [1]
    for j in range(1, n + 1):
        out.append(out[-1] * (x + j))
    return out


def exact_dpis(x, n):
    P, dP = [1], [0]
    for j in range(1, n + 1):
        dP.append(dP[-1] * (x + j) + P[-1])
        P.append(P[-1] * (x + j))
    return dP


def S_of(e, pis):
    return sum(pis[j] for j, b in enumerate(e) if b)


def slope(e, x, p, cap=60):
    """v(S_e'(x)), capped at cap (returns cap if divisible by p^cap)."""
    dP = exact_dpis(x, len(e))
    s = sum(dP[j] for j, b in enumerate(e) if b)
    if s == 0:
        return cap
    return min(vp(s, p), cap)


# ------------------------------------------------------------------ paths
def alive_paths(x, n, p, cap=None):
    """All alive paths of length n at x (prefix-pruned DFS; the pruning is
    the converse of (F2): a prefix of an alive path is alive).  Exact mod
    p^{V_n}.  Returns list of tuples, or None if a level exceeds cap."""
    V = V_upto(x, n, p)
    mod = p ** V[n]
    P = [t % mod for t in exact_pis(x, n)]
    if V[1] > 0:
        return []
    level = [((1,), 1 % mod)]
    for m in range(1, n):
        q = p ** V[m + 1]
        nxt = []
        for e, S in level:
            if S % q == 0:
                nxt.append((e + (0,), S))
            S1 = (S + P[m]) % mod
            if S1 % q == 0:
                nxt.append((e + (1,), S1))
        level = nxt
        if cap is not None and len(level) > cap:
            return None
    return [e for e, _ in level]


def random_alive_path(x, n, p, rng, max_nodes=200000):
    """One alive path of length n by randomised DFS with backtracking."""
    V = V_upto(x, n, p)
    mod = p ** V[n]
    P = [t % mod for t in exact_pis(x, n)]
    if V[1] > 0:
        return None
    stack = [((1,), 1 % mod)]
    nodes = 0
    while stack:
        e, S = stack.pop()
        nodes += 1
        if nodes > max_nodes:
            return None
        m = len(e)
        if m == n:
            return e
        q = p ** V[m + 1]
        kids = []
        for b in (0, 1):
            S1 = (S + b * P[m]) % mod
            if S1 % q == 0:
                kids.append((e + (b,), S1))
        rng.shuffle(kids)
        stack.extend(kids)
    return None


def random_alive_paths(x, n, p, k, rng, tries=None):
    out = set()
    tries = tries or 4 * k
    for _ in range(tries):
        e = random_alive_path(x, n, p, rng)
        if e is None:
            break
        out.add(e)
        if len(out) >= k:
            break
    return sorted(out)


# ------------------------------------------------------------------ windows
def welems(x, n, N):
    """Exact window elements y_0..y_{H-1} and y_H = pi_N/pi_n."""
    ys = [1]
    for s in range(1, N - n + 1):
        ys.append(ys[-1] * (x + n + s))
    return ys[: N - n], ys[N - n]


def wsums(x, n, N, mod):
    """int64 array of length 2^H: Q_f(x) mod `mod`, bit i of f <-> y_i."""
    ys, _ = welems(x, n, N)
    Q = np.zeros(1, dtype=np.int64)
    for y in ys:
        Q = np.concatenate([Q, (Q + (y % mod)) % mod])
    return Q


def wsums_exact(x, n, N):
    ys, _ = welems(x, n, N)
    Q = [0]
    for y in ys:
        Q = Q + [q + y for q in Q]
    return Q


# ------------------------------------------------------------------ cylinder
class Cyl:
    """Cylinder C = x + p^m Z_p (m = V_n(x)) with windows W=[n,N), W'=[N,N2)."""

    def __init__(self, p, x, n, N, N2):
        self.p, self.x, self.n, self.N, self.N2 = p, x, n, N, N2
        V = V_upto(x, N2, p)
        self.V = V
        self.m = V[n]
        self.D = V[N] - V[n]
        self.D2 = V[N2] - V[N]
        self.K = self.D + self.D2
        self.Mn = M_upto(x, n, p)
        self.MN = M_upto(x, N, p)
        self.MN2 = M_upto(x, N2, p)
        m = self.m
        self.W2p = self.D <= m - self.Mn          # (W2')
        self.W3p = self.MN < m                     # (W3')
        self.r52 = (self.K <= m - self.MN2) and (self.MN2 < m)   # (5.2)
        _, yH = welems(x, n, N)
        assert vp(yH, p) == self.D
        self.u_exact = yH // p ** self.D           # pi_N/(p^D pi_n), exact unit

    def u_mod(self, k):
        return self.u_exact % (self.p ** k)

    # ------------------------------------------------------------ targets
    def parent_targets(self, parents, K, npts=None, check_windows=True):
        """tau[w, i] = tau_n(parents[i], x + p^m w) mod p^K for w < p^K
        (or the first npts values), computed from exact S_e(x'), pi_n(x').
        Also verifies, at every point, that V_n, V_N, V_{N2} and M_{N2} are
        the same as at x, that every parent is alive at x', and (if
        check_windows) that Q_f(x') mod p^K and Q'_{f'}(x') mod p^{D2} and
        u(x') mod p^{D2} equal their values at x."""
        p, x, n, N, N2, m = self.p, self.x, self.n, self.N, self.N2, self.m
        Kc = max(K, 1)
        mod = p ** (m + Kc)
        modK = p ** K
        E = np.array([list(e) for e in parents], dtype=np.int64)
        assert E.shape[1] == n
        assert mod * n < 2 ** 62
        npts = npts or p ** K
        tau = np.zeros((npts, len(parents)), dtype=np.int64)
        QK0 = wsums(x, n, N, modK) if check_windows else None
        Q20 = wsums(x, N, N2, p ** self.D2) if check_windows else None
        u0 = self.u_mod(self.D2)
        bad = 0
        for w in range(npts):
            xp = x + p ** m * w
            pis = exact_pis(xp, n)
            pn = pis[n]
            if vp(pn, p) != m:
                bad += 1
            if check_windows and w % max(1, npts // 64) == 0:
                Vp = V_upto(xp, N2, p)
                if (Vp[n], Vp[N], Vp[N2], M_upto(xp, N2, p)) != (
                        self.V[n], self.V[N], self.V[N2], self.MN2):
                    bad += 1
                if not np.array_equal(wsums(xp, n, N, modK), QK0):
                    bad += 1
                if not np.array_equal(wsums(xp, N, N2, p ** self.D2), Q20):
                    bad += 1
                _, yH = welems(xp, n, N)
                if (yH // p ** self.D) % (p ** self.D2) != u0 or vp(yH, p) != self.D:
                    bad += 1
            pv = np.array([t % mod for t in pis[:n]], dtype=np.int64)
            S = (E @ pv) % mod
            if np.any(S % (p ** m)):
                bad += 1
            unit = (pn // p ** m) % (p ** Kc)
            inv = pow(int(unit), -1, p ** Kc)
            tau[w] = ((-(S // p ** m)) % modK * inv) % modK if K > 0 else 0
        return tau, bad


# ------------------------------------------------------------------ laws
def law(Q, qnum, mod):
    """Exact law (list of Fractions) of Q_f mod `mod` under integer weights."""
    A = sum(int(t) for t in qnum)
    cnt = [0] * mod
    for i, wt in zip((Q % mod).tolist(), qnum):
        cnt[i] += int(wt)
    return [Fraction(c, A) for c in cnt]


def coll(mu):
    return sum(t * t for t in mu)


def coarsen(mu, p, k):
    """Law mod p^k from a law mod p^K (K >= k)."""
    mod = p ** k
    out = [Fraction(0)] * mod
    for s, t in enumerate(mu):
        if t:
            out[s % mod] += t
    return out


def chi2(mu_D, p, D):
    return p ** D * coll(mu_D) - 1


def eps_tilde(mu_K, p, D, D2):
    """p^{D+D2} Coll_{D+D2}(mu) - p^D Coll_D(mu)."""
    return p ** (D + D2) * coll(mu_K) - p ** D * coll(coarsen(mu_K, p, D))


def composite_law(mu_K, mu2, p, D, D2, u):
    """Law of Q_f + p^D u Q'_{f'} mod p^{D+D2} (independent f ~ mu, f' ~ mu2)."""
    K = D + D2
    mod = p ** K
    out = [Fraction(0)] * mod
    for t, b in enumerate(mu2):
        if not b:
            continue
        sh = (p ** D * u * t) % mod
        for s, a in enumerate(mu_K):
            if a:
                out[(s + sh) % mod] += a * b
    return out


def lifts(QK, p, D, D2):
    """Lift(r) for each class r mod p^D: residues mod p^{D+D2} attained."""
    K = D + D2
    att = sorted(set((QK % (p ** K)).tolist()))
    L = {r: [] for r in range(p ** D)}
    for s in att:
        L[s % (p ** D)].append(s)
    return L


def harmonic_m(L, p, D, D2):
    """m(W;D') = p^D / sum_r a_r^{-1}, a_r = p^{D'}/|Lift(r)| - 1."""
    P2 = p ** D2
    inv_sum = Fraction(0)
    for r, lst in L.items():
        k = len(lst)
        if k == 0:
            continue
        if k == P2:
            return Fraction(0)
        inv_sum += Fraction(k, P2 - k)       # a_r^{-1} = k/(P2-k)
    return Fraction(p ** D) / inv_sum


def qstar(QK, L, p, D, D2):
    """M4D's optimal weights q* as exact Fractions per f (list)."""
    K = D + D2
    P2 = p ** D2
    Qr = (QK % (p ** K)).tolist()
    cnt = {}
    for s in Qr:
        cnt[s] = cnt.get(s, 0) + 1
    complete = [r for r, lst in L.items() if len(lst) == P2]
    nu = {}
    if complete:
        for r in complete:
            nu[r] = Fraction(1, len(complete))
    else:
        tot = sum(Fraction(len(l), P2 - len(l)) for l in L.values() if l)
        for r, l in L.items():
            if l:
                nu[r] = Fraction(len(l), P2 - len(l)) / tot
    q = []
    for s in Qr:
        r = s % (p ** D)
        if r in nu:
            q.append(nu[r] / len(L[r]) / cnt[s])
        else:
            q.append(Fraction(0))
    return q


def frac_to_int_weights(qf):
    """Common-denominator integer numerators for a list of Fractions."""
    from math import lcm
    den = 1
    for t in qf:
        den = lcm(den, t.denominator)
    return [int(t * den) for t in qf], den
