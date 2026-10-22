"""vF.py -- checker library for the logic check of M4D Lemma L / Theorem F / Corollary F1.

Written from scratch for this check; it shares no code with code/round4/M4D/.

Test points.  Every test point x is a NONNEGATIVE INTEGER (a genuine point of Z_p, never a negative
integer), drawn at random below p^prec, optionally with forced gates v(x+i) = s exactly.  All
quantities are then computed in exact integer arithmetic: pi_j(x) is an exact (big) integer, valuations
are exact, and targets tau = -S/pi_n are reduced modulo p^R through exact division by p^{V_n} and a
modular inverse of the unit part.

Conventions (note.md sec. 1.2; R3M sec. 1; M4D sec. 1):
  pi_j(x) = (x+1)...(x+j), pi_0 = 1;  V_n = v(pi_n(x));  a path of length n is e in {0,1}^n with e_0 = 1,
  S_e = sum_{j<n} e_j pi_j(x);  alive at n iff v(S_e) >= V_n;  target tau_n(e) = -S_e/pi_n.
  Window W=[n,N): y_i = pi_{n+i}/pi_n (0 <= i < N-n), Q_f = sum f_i y_i, jump D = V_N - V_n,
  unit u = pi_N/(p^D pi_n).
"""
import random

import numpy as np


def vp(a, p):
    """exact p-adic valuation of a nonzero integer"""
    if a == 0:
        raise ValueError("vp(0)")
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def make_x(rng, p, prec, forced=()):
    """random nonnegative integer x < p^prec (roughly), with v(x+i) = s exactly for each (i, s) in forced.
    Forced positions are imposed one after another by CRT-free rejection: x = -i + p^s * w, w unit."""
    mod = p ** prec
    if not forced:
        return rng.randrange(mod)
    for _ in range(100000):
        (i0, s0) = forced[0]
        w = rng.randrange(1, mod)
        while w % p == 0:
            w = rng.randrange(1, mod)
        x = (-i0 + p ** s0 * w) % (p ** (prec + s0))
        if all(vp(x + i, p) == s for (i, s) in forced):
            return x
    raise RuntimeError("could not force gates")


def valuations(x, p, N):
    """vals[i] = v(x+i) for 1 <= i <= N (vals[0] = 0); Vcum[n] = V_n"""
    vals = [0] * (N + 1)
    for i in range(1, N + 1):
        vals[i] = vp(x + i, p)
    Vcum = [0] * (N + 1)
    for i in range(1, N + 1):
        Vcum[i] = Vcum[i - 1] + vals[i]
    return vals, Vcum


def products(x, N):
    """exact integers pi_j(x), 0 <= j <= N"""
    pi = [1] * (N + 1)
    for j in range(1, N + 1):
        pi[j] = pi[j - 1] * (x + j)
    return pi


def unit_part(a, p, k):
    """a / p^k for an integer a with p^k | a (checked)"""
    q, r = divmod(a, p ** k)
    assert r == 0
    return q


def target_mod(S, pin, Vn, p, R):
    """tau = -S/pi_n modulo p^R, for exact integers S, pi_n with v(S) >= Vn = v(pi_n)"""
    if R <= 0:
        return 0
    m = p ** R
    a = unit_part(-S, p, Vn) % m
    b = unit_part(pin, p, Vn) % m
    return a * pow(b, -1, m) % m


def alive_bruteforce(x, p, n, pi, Vcum):
    """ALL paths of length n (2^(n-1) of them, e_0 = 1) by direct evaluation, no pruning.
    Returns list of (mask, S) with v(S) >= V_n."""
    out = []
    Vn = Vcum[n]
    for mask in range(1 << (n - 1)):
        S = 1
        for j in range(1, n):
            if (mask >> (j - 1)) & 1:
                S += pi[j]
        if S == 0 or vp(S, p) >= Vn:
            out.append(((mask << 1) | 1, S))
    return out


def alive_dfs(x, p, n, pi, Vcum):
    """paths of length n alive at n, by DFS with prefix pruning (prefix of an alive path is alive:
    M4D (F2) converse).  Validated against alive_bruteforce in t2."""
    out = []
    stack = [(1, 1, 1)] if Vcum[1] == 0 else []  # (mask, S, length); the length-1 path is alive iff v(x+1)=0
    while stack:
        mask, S, k = stack.pop()
        if k == n:
            out.append((mask, S))
            continue
        for bit in (0, 1):
            S2 = S + pi[k] if bit else S
            if S2 == 0 or vp(S2, p) >= Vcum[k + 1]:
                stack.append((mask | (bit << k), S2, k + 1))
    return out


def step_targets(x, p, vals, Vcum, Nmax, want):
    """Single-step carry recursion for the set of alive targets.
    State at time n: the set of tau_n(e) mod p^{R(n)} over all e alive at n, R(n) = V_Nmax - V_n.
    Step n -> n+1 (window [n, n+1): y_0 = 1, Q_f = f in {0,1}, jump d = v(x+n+1), unit (x+n+1)/p^d):
        tau' = ((tau - f)/p^d) * ((x+n+1)/p^d)^{-1}   for f in {0,1} with tau = f mod p^d.
    Returns {n: set} for n in want (n >= 1)."""
    want = set(want)
    res = {}
    R = Vcum[Nmax] - Vcum[1]
    if vals[1] > 0:
        cur = set()
    else:
        m = p ** R
        cur = {(-pow((x + 1) % m, -1, m)) % m} if R > 0 else {0}
    if 1 in want:
        res[1] = cur
    for n in range(1, Nmax):
        d = vals[n + 1]
        R2 = Vcum[Nmax] - Vcum[n + 1]
        m2 = p ** R2
        pd = p ** d
        u = unit_part(x + n + 1, p, d)
        uinv = pow(u % m2, -1, m2) if R2 > 0 else 0
        nxt = set()
        for t in cur:
            for f in (0, 1):
                a = t - f
                if a % pd == 0:
                    nxt.add((a // pd) * uinv % m2 if R2 > 0 else 0)
        cur = nxt
        if n + 1 in want:
            res[n + 1] = cur
    return res


def window_elems(x, n, H, m):
    """y_i = prod_{s=1}^{i} (x+n+s) mod m, 0 <= i < H"""
    ys = []
    y = 1 % m
    for i in range(H):
        ys.append(y)
        y = y * (x + n + i + 1) % m
    return ys


def subset_sums(ys, m):
    """boolean array of residues mod m attained by subset sums of ys"""
    arr = np.zeros(m, dtype=bool)
    arr[0] = True
    for y in ys:
        arr = arr | np.roll(arr, int(y % m))
    return arr


def lift_counts(x, p, n, H, D, D2):
    """|Lift(r)| for every r mod p^D: number of residues s mod p^(D+D2) attained by the window sums
    of W = [n, n+H) with s = r mod p^D.  Returns numpy int array of length p^D."""
    K = D + D2
    m = p ** K
    sup = subset_sums(window_elems(x, n, H, m), m)
    idx = np.nonzero(sup)[0]
    return np.bincount(idx % (p ** D), minlength=p ** D)


def lift_sets(x, p, n, H, D, D2):
    """dict r -> sorted list of residues s mod p^(D+D2) in Lift(r) (pure python sets, small cases)"""
    K = D + D2
    m = p ** K
    sums = {0}
    for y in window_elems(x, n, H, m):
        sums |= {(s + y) % m for s in sums}
    out = {}
    for s in sums:
        out.setdefault(s % (p ** D), set()).add(s)
    return out


def unit_of_window(x, p, n, H, D):
    """u = pi_N/(p^D pi_n) = prod_{s=1}^{H}(x+n+s)/p^D, exact integer"""
    prod = 1
    for s in range(1, H + 1):
        prod *= x + n + s
    return unit_part(prod, p, D)


NP_LIMIT = 2 ** 31


def step_targets_np(x, p, vals, Vcum, Nmax, want):
    """Same recursion as step_targets, with numpy int64 arrays once the modulus p^R is below 2^31
    (products then stay below 2^62).  Returns {n: numpy array of distinct residues mod p^{R(n)}}.
    Validated against step_targets and brute force in t2."""
    want = set(want)
    res = {}
    R = Vcum[Nmax] - Vcum[1]
    if vals[1] > 0:
        cur = set()
    else:
        m = p ** R
        cur = {(-pow((x + 1) % m, -1, m)) % m} if R > 0 else {0}
    if 1 in want:
        res[1] = np.array(sorted(cur), dtype=object if p ** R >= NP_LIMIT else np.int64)
    for n in range(1, Nmax):
        d = vals[n + 1]
        R2 = Vcum[Nmax] - Vcum[n + 1]
        m2 = p ** R2
        pd = p ** d
        u = unit_part(x + n + 1, p, d)
        uinv = pow(u % m2, -1, m2) if R2 > 0 else 0
        if isinstance(cur, set):
            nxt = set()
            for t in cur:
                for f in (0, 1):
                    a = t - f
                    if a % pd == 0:
                        nxt.add((a // pd) * uinv % m2 if R2 > 0 else 0)
            cur = nxt
            if m2 < NP_LIMIT:
                cur = np.array(sorted(cur), dtype=np.int64)
        else:
            m = p ** (Vcum[Nmax] - Vcum[n])
            parts = []
            for f in (0, 1):
                a = (cur - f) % m
                sel = a[a % pd == 0] // pd
                parts.append((sel * uinv) % m2 if R2 > 0 else sel * 0)
            cur = np.unique(np.concatenate(parts))
        if n + 1 in want:
            if isinstance(cur, set):
                res[n + 1] = np.array(sorted(cur), dtype=object)
            else:
                res[n + 1] = cur.copy()
    return res
