"""fz_lib.py -- independent exact-arithmetic library for the numerical falsification
of Theorem B1 / B1' (round-4 track M4B).  Written from the definitions in R3M section 1
and M4B section 2; it shares no code with code/round4/M4B or code/round3.

A p-adic point is represented by a nonnegative Python integer X (an honest element of Z_p),
so every valuation v(X+i) is exact.  An atom (cylinder) is a pair (r, m): the class r mod p^m.

Conventions (R3M section 1):
  pi_j(x) = (x+1)...(x+j), pi_0 = 1;  V_n = v(pi_n(x));  M_n = max_{i<=n} v(x+i);
  c_n = 2^{-n} p^{V_n};  a path of length n is e in {0,1}^n with e_0 = 1,
  S_e = sum_{j<n} e_j pi_j;  e is alive at n iff v(S_e(x)) >= V_n;  slope = v(S_e'(x)).
  Z0_n = number of slope-0 paths alive at n.
"""
from fractions import Fraction
import itertools
import numpy as np

INF = 10 ** 9


def vp(a, p):
    """p-adic valuation of the integer a (INF for a == 0)."""
    if a == 0:
        return INF
    v = 0
    while a % p == 0:
        a //= p
        v += 1
    return v


def vals(X, p, T):
    """[None, v(X+1), ..., v(X+T)]"""
    return [None] + [vp(X + i, p) for i in range(1, T + 1)]


def prefix(vl):
    """V[k] = sum_{i<=k} v_i, M[k] = max_{i<=k} v_i (V[0] = M[0] = 0)."""
    T = len(vl) - 1
    V = [0] * (T + 1)
    M = [0] * (T + 1)
    for k in range(1, T + 1):
        V[k] = V[k - 1] + vl[k]
        M[k] = max(M[k - 1], vl[k])
    return V, M


def c_n(n, Vn, p):
    return Fraction(p ** Vn, 2 ** n)


# ----------------------------------------------------------------------------------------
# slope-0 population counts by dynamic programming over (S mod p^{V_T}, S' mod p)
# ----------------------------------------------------------------------------------------
def dp_profile(X, p, T, tag_at=None):
    """Exact counts for the point X:
       Z0[n] = #slope-0 paths alive at n, Zall[n] = #paths alive at n, for 1 <= n <= T.
       If tag_at = n0 (< T) is given, also returns cross[(tag, fin)] at time T, where tag = 1 iff the
       prefix of length n0 has slope 0 at X and fin = 1 iff the full path (length T) has slope 0.
       Exactness: counts are int64 (<= 2^T, T <= 60); residues modulo p^{V_T} with V_T <= 20."""
    vl = vals(X, p, T)
    V, M = prefix(vl)
    Vf = V[T]
    assert Vf <= 20 and T <= 60, (Vf, T)
    Z0 = [0] * (T + 1)
    Zall = [0] * (T + 1)
    cross = {}
    if vl[1] > 0:  # S = 1 for the length-1 path; nothing alive at any n >= 1
        if tag_at is not None:
            return Z0, Zall, cross
        return Z0, Zall
    MODF = p ** Vf
    # pi_k mod p^{Vf} and pi_k' mod p for k = 0..T-1
    pis = [1 % MODF]
    dpis = [0]
    for k in range(1, T):
        pis.append(pis[-1] * (X + k) % MODF)
        dpis.append((dpis[-1] * (X + k) + pis[-2]) % p)
    # state at length k = 1
    s = np.array([1 % MODF], dtype=np.int64)
    d = np.array([0], dtype=np.int64)
    tg = np.array([0], dtype=np.int64)
    cnt = np.array([1], dtype=np.int64)
    Z0[1] = 0
    Zall[1] = 1
    if tag_at == 1:
        tg = (d != 0).astype(np.int64)
    for k in range(1, T):
        # current: paths of length k alive at k; s = S/p^{V_k} mod p^{Vf-V_k}
        modk = p ** (Vf - V[k])
        if V[k] < Vf:
            sh = (pis[k] // (p ** V[k])) % modk if pis[k] != 0 else 0
        else:
            sh = 0
        # sanity: pi_k has valuation exactly V_k (when V_k < Vf)
        if V[k] < Vf:
            assert vp(pis[k], p) == V[k] or pis[k] == 0 and False, "valuation of pi_k"
        s2 = np.concatenate([s, (s + sh) % modk]) if modk > 1 else np.concatenate([s, s])
        d2 = np.concatenate([d, (d + dpis[k]) % p])
        t2 = np.concatenate([tg, tg])
        c2 = np.concatenate([cnt, cnt])
        delta = V[k + 1] - V[k]
        if delta > 0:
            pdl = p ** delta
            mask = (s2 % pdl) == 0
            s2 = s2[mask] // pdl
            d2 = d2[mask]
            t2 = t2[mask]
            c2 = c2[mask]
        if len(c2) == 0:
            s, d, tg, cnt = s2, d2, t2, c2
            break
        key = (s2 * p + d2) * 2 + t2
        uk, inv = np.unique(key, return_inverse=True)
        cn = np.zeros(len(uk), dtype=np.int64)
        np.add.at(cn, inv, c2)
        t3 = uk % 2
        rest = uk // 2
        d3 = rest % p
        s3 = rest // p
        s, d, tg, cnt = s3, d3, t3, cn
        if tag_at is not None and k + 1 == tag_at:
            tg = (d != 0).astype(np.int64)
            key = (s * p + d) * 2 + tg
            # no merge needed: tag is a function of d
        Z0[k + 1] = int(cnt[d != 0].sum())
        Zall[k + 1] = int(cnt.sum())
    if tag_at is not None:
        for t in (0, 1):
            for f in (0, 1):
                sel = (tg == t) & ((d != 0) == bool(f))
                cross[(t, f)] = int(cnt[sel].sum()) if len(cnt) else 0
        return Z0, Zall, cross
    return Z0, Zall


def brute_profile(X, p, n):
    """Brute force over all 2^{n-1} paths of length n: (#slope-0 alive at n, #alive at n)."""
    vl = vals(X, p, n)
    V, M = prefix(vl)
    pis = [1]
    dpis = [0]
    for k in range(1, n):
        pis.append(pis[-1] * (X + k))
        dpis.append(dpis[-1] * (X + k) + pis[-2])
    z0 = za = 0
    for bits in itertools.product((0, 1), repeat=n - 1):
        S = 1 + sum(pis[j] for j in range(1, n) if bits[j - 1])
        Sd = sum(dpis[j] for j in range(1, n) if bits[j - 1])
        if vp(S, p) >= V[n]:
            za += 1
            if Sd % p != 0:
                z0 += 1
    return z0, za


# ----------------------------------------------------------------------------------------
# window laws, chi^2 and the fine-scale mass eps (R3M Prop B, Prop C2)
# ----------------------------------------------------------------------------------------
def law_counts(elems, p, K):
    """counts[r] = #{f in {0,1}^L : sum f_i elems_i == r mod p^K} (int64 numpy array)."""
    mod = p ** K
    c = np.zeros(mod, dtype=np.int64)
    c[0] = 1
    for y in elems:
        c = c + np.roll(c, int(y % mod))
    return c


def reduce_counts(c, p, K, D):
    if D == K:
        return c
    return c.reshape(p ** (K - D), p ** D).sum(axis=0)


def sumsq(c):
    return sum(int(a) * int(a) for a in c)


def window_elems(X, p, n, N):
    """y_j = pi_j(X)/pi_n(X) = (X+n+1)...(X+j) for n <= j < N (exact integers)."""
    out = []
    y = 1
    for j in range(n, N):
        if j > n:
            y *= (X + j)
        out.append(y)
    return out


def chi2(X, p, n, N):
    """chi^2_W for W = [n,N): p^D sum mu^2 - 1 with D = V_N - V_n (exact Fraction)."""
    vl = vals(X, p, N)
    V, _ = prefix(vl)
    D = V[N] - V[n]
    el = window_elems(X, p, n, N)
    L = len(el)
    c = law_counts(el, p, D) if D > 0 else np.array([2 ** L], dtype=np.int64)
    return Fraction(p ** D * sumsq(c), 4 ** L) - 1


def eps_coll(X, p, n, N, Np):
    """eps(W,W') = p^K Coll_K - p^D Coll_D of the composite window [n,N') (exact Fraction)."""
    vl = vals(X, p, Np)
    V, _ = prefix(vl)
    D = V[N] - V[n]
    K = V[Np] - V[n]
    el = window_elems(X, p, n, Np)
    L = len(el)
    if K == 0:
        return Fraction(0)
    cK = law_counts(el, p, K)
    cD = reduce_counts(cK, p, K, D)
    return Fraction(p ** K * sumsq(cK) - p ** D * sumsq(cD), 4 ** L)


def eps_fourier(X, p, n, N, Np):
    """R3M definition: sum_{xi != 0 mod p^{D'}} |mu_W'(xi)|^2 F_W(xi) (float, FFT)."""
    vl = vals(X, p, Np)
    V, _ = prefix(vl)
    D = V[N] - V[n]
    Dp = V[Np] - V[N]
    K = D + Dp
    if Dp == 0:
        return 0.0
    elW = window_elems(X, p, n, N)
    elWp = window_elems(X, p, N, Np)
    cW = law_counts(elW, p, K).astype(float) / 2 ** len(elW)
    cWp = law_counts(elWp, p, Dp).astype(float) / 2 ** len(elWp)
    FW = np.abs(np.fft.fft(cW)) ** 2  # index zeta mod p^K
    FWp = np.abs(np.fft.fft(cWp)) ** 2  # index xi mod p^D'
    piN_over = 1
    for i in range(n + 1, N + 1):
        piN_over *= (X + i)
    u = (piN_over // p ** D) % p ** Dp
    uinv = pow(u, -1, p ** Dp)
    tot = 0.0
    for xi in range(1, p ** Dp):
        t = (xi * uinv) % p ** Dp
        fib = FW[t::p ** Dp].sum()
        tot += FWp[xi] * fib
    return tot


def cond52(V, M, n, N, Np):
    """(5.2) for the composite window [n,N) u [N,N')."""
    m = V[n]
    K = V[Np] - V[n]
    return K <= m - M[Np] and M[Np] < m


def condW(V, M, n, N):
    """(W2'), (W3') for the window [n,N)."""
    m = V[n]
    D = V[N] - V[n]
    return D <= m - M[n] and M[N] < m


# ----------------------------------------------------------------------------------------
# adaptive window times (M4B section 2)
# ----------------------------------------------------------------------------------------
def trunc_vals(r, m, p, T):
    """truncated valuations min(v(x+i), m), i = 1..T, for x in the class r mod p^m."""
    out = [None]
    for i in range(1, T + 1):
        a = (r + i) % (p ** m)
        out.append(m if a == 0 else min(vp(a, p), m))
    return out


def rule_next(rule, r, m, hist, p, H):
    """n_{l+1} as a function of (x mod p^{m_{l-1}}, m_{l-1}, n_0..n_l).
       r = x mod p^m (canonical residue), m = m_{l-1}; hist = [n_0, ..., n_l]."""
    nl = hist[-1]
    nlm1 = hist[-2]
    if rule == 'det':
        return nl + H
    if rule == 'hash':
        return nl + 1 + ((r * 1000003 + 7919 * m + 31 * nl) % H)
    tv = trunc_vals(r, m, p, nl + H + 3)
    if rule == 'lin':
        # largest n in [nl+1, nl+H] keeping (5.2) for [n_{l-1}, n_l, n) computed with truncated valuations
        best = nl + 1
        Ktr = sum(tv[i] for i in range(nlm1 + 1, nl + 1))
        Mtr = max(tv[1:nl + 1])
        for n in range(nl + 1, nl + H + 1):
            Ktr += tv[n]
            Mtr = max(Mtr, tv[n])
            if Ktr <= m - Mtr and Mtr < m:
                best = n
        return best
    if rule == 'ladder':
        # least n >= nl + 2 with no gate at distance 1 or 2 (truncated valuations), else nl + H
        for n in range(nl + 2, nl + H):
            if tv[n + 1] == 0 and tv[n + 2] == 0:
                return n
        return nl + H
    raise ValueError(rule)


def schedule(X, p, n0, n1, rule, H, L):
    """times n_0..n_{L+1} and m_0..m_L for the point X under an adaptive rule."""
    n = [n0, n1]
    m = []
    for l in range(0, L + 1):
        T = n[l]
        vl = vals(X, p, T)
        V, _ = prefix(vl)
        m.append(V[T])
        if l >= 1:
            r = X % (p ** m[l - 1])
            n.append(rule_next(rule, r, m[l - 1], n[:l + 1], p, H))
    return n, m


# ----------------------------------------------------------------------------------------
# explicit parents: enumeration of slope-0 alive paths and descendant counts of one parent
# ----------------------------------------------------------------------------------------
def enum_alive(X, p, n, limit=200000):
    """explicit list of (bits, S, S') for all paths of length n alive at n (DFS with pruning by
       backward integrality); bits = (e_0=1, e_1, ..., e_{n-1}); S, S' exact integers at X."""
    vl = vals(X, p, n)
    V, _ = prefix(vl)
    pis = [1]; dpis = [0]
    for k in range(1, n):
        pis.append(pis[-1] * (X + k))
        dpis.append(dpis[-1] * (X + k) + pis[-2])
    out = []
    stack = [((1,), 1, 0)]
    while stack:
        bits, S, Sd = stack.pop()
        k = len(bits)
        if vp(S, p) < V[k]:
            continue
        if k == n:
            out.append((bits, S, Sd))
            if len(out) > limit:
                raise RuntimeError("too many paths")
            continue
        stack.append((bits + (0,), S, Sd))
        stack.append((bits + (1,), S + pis[k], Sd + dpis[k]))
    return out


def dp_from_parent(X, p, T, bits):
    """descendant counts of the parent path 'bits' (length n): Z0[k], Zall[k] for n <= k <= T
       (counts of extensions of length k alive at k, with slope 0 / any slope), exact."""
    n = len(bits)
    vl = vals(X, p, T)
    V, _ = prefix(vl)
    Vf = V[T]
    assert Vf <= 20
    MODF = p ** Vf
    pisx = [1]; dpisx = [0]
    for k in range(1, T):
        pisx.append(pisx[-1] * (X + k))
        dpisx.append(dpisx[-1] * (X + k) + pisx[-2])
    S = sum(pisx[j] for j in range(n) if bits[j])
    Sd = sum(dpisx[j] for j in range(n) if bits[j])
    Z0 = [0] * (T + 1); Zall = [0] * (T + 1)
    if vp(S, p) < V[n]:
        return Z0, Zall
    modn = p ** (Vf - V[n])
    s = np.array([(S // p ** V[n]) % modn if V[n] < Vf else 0], dtype=np.int64) if True else None
    d = np.array([Sd % p], dtype=np.int64)
    cnt = np.array([1], dtype=np.int64)
    Z0[n] = int(Sd % p != 0); Zall[n] = 1
    for k in range(n, T):
        modk = p ** (Vf - V[k])
        sh = ((pisx[k] % MODF) // p ** V[k]) % modk if V[k] < Vf else 0
        s2 = np.concatenate([s, (s + sh) % modk]) if modk > 1 else np.concatenate([s, s])
        d2 = np.concatenate([d, (d + dpisx[k] % p) % p])
        c2 = np.concatenate([cnt, cnt])
        delta = V[k + 1] - V[k]
        if delta > 0:
            pdl = p ** delta
            mask = (s2 % pdl) == 0
            s2 = s2[mask] // pdl; d2 = d2[mask]; c2 = c2[mask]
        if len(c2) == 0:
            break
        key = s2 * p + d2
        uk, inv = np.unique(key, return_inverse=True)
        cn = np.zeros(len(uk), dtype=np.int64)
        np.add.at(cn, inv, c2)
        s, d, cnt = uk // p, uk % p, cn
        Z0[k + 1] = int(cnt[d != 0].sum()); Zall[k + 1] = int(cnt.sum())
    return Z0, Zall
