"""bounds.py -- explicit upper bounds of track M4A (round 4), data/round4/reports/M4A.md:

  qconsts(p, S)            universal block constants q_s = p^s max_z P(sum_{k<p} delta_k pi_k(-p) == z mod p^s)
  lemmaQ_logbound(...)     Lemma Q: upper bound for G = p^k P(v(T_u) >= k, v(T_u') >= f)
  propE_bound(...)         Proposition E: upper bound for E_B[eps] (B a ball with constant gate pattern)
  propD_bound(...)         Proposition D: pointwise upper bound for eps(x) (and for p^K Coll_K)
All bounds are returned as exact Fractions (small cases) -- the large-scale evaluator (fe_eval.py) re-implements
the same formulas in outward-rounded interval arithmetic.
Positions are absolute: depth[i] = v_p(x+i) for i = 1..N' is the gate pattern of x.
"""
import itertools
from fractions import Fraction


def qconsts(p, S):
    w = {-1: 1, 0: 2, 1: 1}
    pk = [1]
    for k in range(1, p):
        pk.append(pk[-1] * (k - p))
    mod = p ** S
    L = {}
    for d in itertools.product((-1, 0, 1), repeat=p):
        wt = 1
        for x in d:
            wt *= w[x]
        z = sum(a * b for a, b in zip(d, pk)) % mod
        L[z] = L.get(z, 0) + wt
    out = [Fraction(1)]
    for s in range(1, S + 1):
        m = p ** s
        F = {}
        for z, c in L.items():
            F[z % m] = F.get(z % m, 0) + c
        out.append(Fraction(m * max(F.values()), 4 ** p))
    return out


def qconsts_dp(p, S):
    """Same constants as qconsts, computed by a residue DP modulo p^S (no enumeration of the 3^p configurations);
    used for large p.  Validated against qconsts for p <= 13 (code/round4/M4A/qdp_check.py)."""
    mod = p ** S
    law = {0: 1}
    val = 1
    for k in range(p):
        if k > 0:
            val = val * (k - p)
        a = val % mod
        new = {}
        for z, c in law.items():
            new[z] = new.get(z, 0) + 2 * c
            new[(z + a) % mod] = new.get((z + a) % mod, 0) + c
            new[(z - a) % mod] = new.get((z - a) % mod, 0) + c
        law = new
    out = [Fraction(1)]
    for s_ in range(1, S + 1):
        m = p ** s_
        F = {}
        for z, c in law.items():
            F[z % m] = F.get(z % m, 0) + c
        out.append(Fraction(m * max(F.values()), 4 ** p))
    return out


def block0_table_dp(p, S):
    """Same table as block0_table (P0[g][s], s <= S), by a residue DP modulo p^S."""
    mod = p ** S
    P0 = {}
    for g in range(1, p + 1):
        law = {1 % mod: 1}
        val = 1
        for c in range(1, g):
            val = val * (c - g)
            a = val % mod
            new = {}
            for z, cc in law.items():
                new[z] = new.get(z, 0) + 2 * cc
                new[(z + a) % mod] = new.get((z + a) % mod, 0) + cc
                new[(z - a) % mod] = new.get((z - a) % mod, 0) + cc
            law = new
        T = 4 ** (g - 1)
        P0[g] = [Fraction(sum(cc for z, cc in law.items() if z % p ** s_ == 0), T) for s_ in range(S + 1)]
    return P0


def block0_table(p, S):
    """P0[g][s] = P(sum_{c<g} delta_c pi_c(-g) == 0 mod p^s), delta_0 = 1, delta_1.. signed, for 1 <= g <= p,
    0 <= s <= S.  If u + g == 0 mod p^s then pi_c(u) == pi_c(-g) mod p^s, so this is exactly the probability of
    the block-0 event {T_{<g}(u) == 0 mod p^s} (first gate of u at g, with depth >= s)."""
    w = {-1: 1, 0: 2, 1: 1}
    P0 = {}
    for g in range(1, p + 1):
        vals = [1]
        for c in range(1, g):
            vals.append(vals[-1] * (c - g))  # pi_c(-g) = (1-g)(2-g)...(c-g)
        dist = {}
        for d in itertools.product((-1, 0, 1), repeat=g - 1):
            wt = 1
            for xx in d:
                wt *= w[xx]
            z = 1 + sum(a * b for a, b in zip(d, vals[1:]))
            dist[z] = dist.get(z, 0) + wt
        T = 4 ** (g - 1)
        P0[g] = [Fraction(sum(c for z, c in dist.items() if z % p ** s_ == 0), T) for s_ in range(S + 1)]
    return P0


def qs(q, p, s):
    """q_s for any s >= 1 (q_s <= p q_{s-1}, so beyond the table use the last entry times p^excess)."""
    if s < len(q):
        return q[s]
    return q[-1] * p ** (s - (len(q) - 1))


def lemmaQ_bound(depth, start, t, k, f, p, q, P0=None):
    """Upper bound for G = p^k P(v(T_u) >= k, v(T_u') >= f), u = x + start, T_u = sum_{c<t} delta_c pi_c(u),
    delta_0 = 1, where depth[i] = v(x+i).  Requires k <= V_t(u).  f <= 0 means no slope condition.
    Returns a Fraction.  (Lemma Q; block 0 is bounded by the exact table P0 if given, else by 1.)"""
    if k <= 0:
        return Fraction(p) ** k if k == 0 else Fraction(1, p ** (-k))
    gates = []  # (relative position g, depth s, relative level L_g = V_g(u))
    V = 0
    for g in range(1, t + 1):
        s = depth[start + g]
        V += s
        if s > 0:
            gates.append((g, s, V))
    assert V >= k, (V, k)
    prob = Fraction(1)
    Mrun = 0
    for r in range(len(gates)):
        g, s, L = gates[r]
        Mrun = max(Mrun, s)
        if r == 0:
            if P0 is not None:  # block 0 = [0, g_1): exact probability of T_{<g_1} == 0 mod p^min(s_1,k)
                prob *= P0[g][min(s, k, len(P0[g]) - 1)]
            continue
        Lr = gates[r - 1][2]  # level of block r-1 = [g_{r-1}, g_r)
        if Lr >= k:
            break
        # block r-1 has end gate g = g_r with depth s and level L_{r} = L
        if s == 1 and L <= min(f, k - Mrun):
            prob *= q[2] / p ** 2
        else:
            d = min(s, k - Lr)
            prob *= qs(q, p, d) / p ** d
    return p ** k * prob


def window_data(depth, n, N, N2):
    V = [0] * (N2 + 1)
    for i in range(1, N2 + 1):
        V[i] = V[i - 1] + depth[i]
    D = V[N] - V[n]
    K = V[N2] - V[n]
    a = [V[n + c] - V[n] for c in range(N2 - n)]
    MW = max(depth[n + 1:N2 + 1])
    return D, K, a, MW


def propE_bound(depth, n, N, N2, b, p, q, P0=None):
    """Upper bound for E_B[eps] for the composite window [n,N) u [N,N'), B a ball of radius p^-b on which the
    gate pattern depth[n+1..N'] is constant (all depths < b).  Theorem 1 + Lemma F + Lemma Q.
    Returns (bound, theta).  Requires K - M_W >= theta (checked)."""
    D, K, a, MW = window_data(depth, n, N, N2)
    H = N2 - n
    th = min((D + 1) // 2, D - b + 1)
    assert max(depth[n + 1:N2 + 1]) < b
    if th > 0:
        assert K - MW >= th, (K, MW, th)
    tot = Fraction(p ** K, 2 ** H)
    for c in range(H):
        w = Fraction(1, 2 ** (c + 1))
        if a[c] >= K:
            tot += w * p ** K
        else:
            f = th - a[c] if th > 0 else 0
            tot += w * p ** a[c] * lemmaQ_bound(depth, n + c, H - c, K - a[c], f, p, q, P0)
    return tot, th


def propD_bound(depth, n, N, N2, p, q, which='K', P0=None):
    """Pointwise upper bound for p^K Coll_K (which='K') or p^D Coll_D of the window [n,N) (which='D')
    for the composite window; eps <= p^K Coll_K - 1 and chi^2_W = p^D Coll_D(W) - 1."""
    D, K, a, MW = window_data(depth, n, N, N2)
    if which == 'K':
        H, top = N2 - n, K
    else:
        H, top = N - n, D
    tot = Fraction(p ** top, 2 ** H)
    for c in range(H):
        w = Fraction(1, 2 ** (c + 1))
        if a[c] >= top:
            tot += w * p ** top
        else:
            tot += w * p ** a[c] * lemmaQ_bound(depth, n + c, H - c, top - a[c], 0, p, q, P0)
    return tot
