"""vl_lib.py -- independent helpers for the LOGIC check of round-4 track M4A (verify_M4A_logic).

Written from the statements in data/round4/reports/M4A.md (sections 1-5); it shares no code with
code/round4/M4A/.  Conventions:
  pi_c(y) = (y+1)...(y+c);  V_t(y) = v(pi_t(y));  signed digit law P(0)=1/2, P(+-1)=1/4 (integer weights 2,1,1 of 4).
  Composite window [n, N'): y_c(x) = pi_{n+c}(x)/pi_n(x) = prod_{i=1}^{c} (x+n+i), 0 <= c < H = N'-n.
Exact arithmetic: python ints / Fractions; numpy int64 only for counts bounded by 4^H with H <= 31.
"""
import itertools
from fractions import Fraction

import numpy as np


def vp(a, p):
    if a == 0:
        raise ValueError("valuation of 0")
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


# ---------------------------------------------------------------- universal constants (Lemma Q)
def q_consts(p, S):
    """q_s = p^s max_z P(Z == z mod p^s), Z = sum_{k<p} zeta_k pi_k(-p), zeta i.i.d. signed. Returns dict s->Fraction."""
    pik = [1]
    for k in range(1, p):
        pik.append(pik[-1] * (k - p))
    cnt = {}
    for z in itertools.product((-1, 0, 1), repeat=p):
        w = 1
        for zz in z:
            w *= 2 if zz == 0 else 1
        val = sum(a * b for a, b in zip(z, pik))
        cnt[val] = cnt.get(val, 0) + w
    out = {}
    for s in range(1, S + 1):
        m = p ** s
        red = {}
        for v_, c in cnt.items():
            red[v_ % m] = red.get(v_ % m, 0) + c
        out[s] = Fraction(m * max(red.values()), 4 ** p)
    out['atom'] = Fraction(max(cnt.values()), 4 ** p)   # max_z P(Z = z): q_s = p^s * this for s large
    return out


def qt(q, p, s, S):
    """q~_s: q_s for s <= S, q_S p^(s-S) beyond (an upper bound for q_s since q_s <= p q_{s-1})."""
    return q[s] if s <= S else q[S] * Fraction(p) ** (s - S)


def P0_table(p, Smax):
    """P0[g][s] = P(sum_{c<g} zeta_c pi_c(-g) == 0 mod p^s), zeta_0 = 1, 1 <= g <= p, 0 <= s <= Smax."""
    P0 = {}
    for g in range(1, p + 1):
        vals = [1]
        for c in range(1, g):
            vals.append(vals[-1] * (c - g))
        cnt = {}
        for z in itertools.product((-1, 0, 1), repeat=g - 1):
            w = 1
            for zz in z:
                w *= 2 if zz == 0 else 1
            val = 1 + sum(a * b for a, b in zip(z, vals[1:]))
            cnt[val] = cnt.get(val, 0) + w
        tot = 4 ** (g - 1)
        P0[g] = [Fraction(sum(c for v_, c in cnt.items() if v_ % p ** s == 0), tot) for s in range(Smax + 1)]
    return P0


# ---------------------------------------------------------------- exact signed-sum DPs
def signed_dp_0(vals, mod, first_fixed=False):
    """Weighted count (weights 2,1,1 per digit) of digit vectors with sum_c d_c vals[c] == 0 mod `mod`.
    If first_fixed, d_0 = 1 (weight 1).  Returns (count, total weight)."""
    assert len(vals) - (1 if first_fixed else 0) <= 31, "int64 overflow: more than 31 free digits"
    cur = np.zeros(mod, dtype=np.int64)
    start = 0
    if first_fixed:
        cur[vals[0] % mod] = 1
        start = 1
    else:
        cur[0] = 1
    tot = 1
    for c in range(start, len(vals)):
        a = vals[c] % mod
        cur = 2 * cur + np.roll(cur, a) + np.roll(cur, -a)
        tot *= 4
    return int(cur[0]), tot


def signed_dp_joint(vals, dvals, mod1, mod2, first_fixed=False):
    """Weighted counts array over (sum d_c vals[c] mod mod1, sum d_c dvals[c] mod mod2). Returns (array, total)."""
    assert len(vals) - (1 if first_fixed else 0) <= 31, "int64 overflow: more than 31 free digits"
    cur = np.zeros((mod1, mod2), dtype=np.int64)
    start = 0
    if first_fixed:
        cur[vals[0] % mod1, dvals[0] % mod2] = 1
        start = 1
    else:
        cur[0, 0] = 1
    tot = 1
    for c in range(start, len(vals)):
        a, b = vals[c] % mod1, dvals[c] % mod2
        cur = 2 * cur + np.roll(cur, (a, b), axis=(0, 1)) + np.roll(cur, (-a, -b), axis=(0, 1))
        tot *= 4
    return cur, tot


def pis_and_derivs(y, t):
    """exact integers pi_c(y), pi_c'(y) for c = 0..t-1."""
    pi, dpi = [1], [0]
    for c in range(1, t):
        dpi.append(dpi[-1] * (y + c) + pi[-1])
        pi.append(pi[-1] * (y + c))
    return pi, dpi


# ---------------------------------------------------------------- Lemma Q bound (from the statement)
def lemmaQ_bound(dep, k, f, p, q, S, P0):
    """Statement of Lemma Q.  dep[g] = v(u+g) for g = 1..t (dep[0] unused).  Returns the bound (Fraction) for
    P(v(T) >= k, v(T') >= f), T = sum_{c<t} d_c pi_c(u), d_0 = 1.  Requires 1 <= k <= V_t(u)."""
    t = len(dep) - 1
    gates = [g for g in range(1, t + 1) if dep[g] > 0]
    s = [None] + [dep[g] for g in gates]                 # s_1, s_2, ...
    L = [0]
    for r in range(1, len(gates) + 1):
        L.append(L[-1] + s[r])
    assert L[-1] >= k
    Mr = [0]
    for r in range(1, len(gates) + 1):
        Mr.append(max(Mr[-1], s[r]))
    g1 = gates[0]
    bound = P0[g1][min(s[1], k, len(P0[g1]) - 1)]
    r = 1
    while r < len(gates) + 1 and L[r] < k:
        # block r = [g_r, g_{r+1}); g_{r+1} exists because L_r < k <= V_t
        if s[r + 1] == 1 and L[r + 1] <= min(f, k - Mr[r + 1]):
            bound *= q[2] / Fraction(p ** 2)
        else:
            d = min(s[r + 1], k - L[r])
            bound *= qt(q, p, d, S) / Fraction(p ** d)
        r += 1
    return bound


# ---------------------------------------------------------------- Props D and E (from the statements)
def window_pattern(depth, n, N, N2):
    """depth[i] = v(x+i) for absolute i in (n, N2]. Returns D, K, H, a (list), gates (abs), lam (dict), MW."""
    H = N2 - n
    a = [0] * H
    acc = 0
    for c in range(1, H):
        acc += depth[n + c]
        a[c] = acc
    D = sum(depth[i] for i in range(n + 1, N + 1))
    K = sum(depth[i] for i in range(n + 1, N2 + 1))
    gates = [i for i in range(n + 1, N2 + 1) if depth[i] > 0]
    lam = {}
    acc = 0
    for i in range(n + 1, N2 + 1):
        acc += depth[i]
        if depth[i] > 0:
            lam[i] = acc
    MW = max(depth[i] for i in range(n + 1, N2 + 1))
    return D, K, H, a, gates, lam, MW


def propDE_bound(depth, n, N, N2, p, q, S, P0, top='K', theta=None):
    """Prop D (theta=None) or Prop E (theta given; f' = min(theta, K - M_W)) as an exact Fraction.
    top='K': bound for p^K Coll_K of the composite window (Prop D) or for E_B[eps] (Prop E);
    top='D': Prop D for p^D Coll_D of the window [n, N) alone (then pass N2 = N)."""
    D, K, H, a, gates, lam, MW = window_pattern(depth, n, N, N2)
    Kt = K if top == 'K' else D
    fpr = None
    if theta is not None and theta >= 1:
        fpr = min(theta, Kt - MW)
    # block factors pi_{beta'} for consecutive gates with lam < Kt
    fac = []
    for j in range(len(gates) - 1):
        G, G2 = gates[j], gates[j + 1]
        if lam[G] >= Kt:
            break
        if fpr is not None and depth[G2] == 1 and lam[G2] <= fpr:
            fac.append(q[2] / Fraction(p ** 2))
        else:
            d = min(depth[G2], Kt - lam[G])
            fac.append(qt(q, p, d, S) / Fraction(p ** d))
    suf = [Fraction(1)] * (len(gates) + 1)
    for j in range(len(fac) - 1, -1, -1):
        suf[j] = fac[j] * suf[j + 1]
    tot = Fraction(1, 2 ** H)
    gi = 0
    for c in range(H):
        w = Fraction(1, 2 ** (c + 1))
        if a[c] >= Kt:
            tot += w
            continue
        while gates[gi] <= n + c:
            gi += 1
        G = gates[gi]
        g1, s1 = G - n - c, depth[G]
        tot += w * P0[g1][min(s1, Kt - a[c], len(P0[g1]) - 1)] * suf[gi]
    return Fraction(p) ** Kt * tot


# ---------------------------------------------------------------- composite-window exact quantities
def window_vals(x, n, H, modS, modd=None):
    """y_c(x) mod modS and (optionally) y_c'(x) mod modd for c < H (exact integer recursion)."""
    ys, dys = [1], [0]
    for c in range(1, H):
        dys.append(dys[-1] * (x + n + c) + ys[-1])
        ys.append(ys[-1] * (x + n + c))
    return [y % modS for y in ys], ([d % modd for d in dys] if modd else None)
