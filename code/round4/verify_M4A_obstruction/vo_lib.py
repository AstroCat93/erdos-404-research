"""vo_lib.py -- exact helpers for track verify_M4A_obstruction (round 4).

Written for this check; shares no code with code/round4/M4A/ (which is imported read-only only where
the M4A bound itself is the object under test).

Conventions (note.md section 10.1, data/round3/reports/R3M.md section 1, data/round4/reports/M4A.md section 1):
  pi_c(y) = (y+1)...(y+c);  V_t(y) = v_p(pi_t(y));  composite window [n,N) u [N,N'), H = N'-n,
  y_c(x) = (x+n+1)...(x+n+c) (0 <= c < H), D = V_N - V_n, K = V_N' - V_n.
  Coll_j = P(sum_c delta_c y_c == 0 mod p^j), delta_c i.i.d. signed (P(0)=1/2, P(+-1)=1/4).
  eps = p^K Coll_K - p^D Coll_D (fine-scale band mass);  chi^2_W = p^D Coll_D(W) - 1 for W=[n,N).
All results are exact rationals: the signed law is propagated with integer weights (2,1,1), total 4^H,
in numpy int64 (exact as long as 4^H < 2^63, i.e. H <= 31; asserted).
"""
from fractions import Fraction
import numpy as np


def vp(a, p, cap=10 ** 9):
    if a == 0:
        return cap
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def depths(x, upto, p):
    """depth[i] = v_p(x+i) for i = 0..upto (x a nonnegative integer, so x+i > 0 for i >= 1)."""
    return [0] + [vp(x + i, p) for i in range(1, upto + 1)]


def window(x, n, N, N2, p):
    dep = depths(x, N2, p)
    V = [0] * (N2 + 1)
    for i in range(1, N2 + 1):
        V[i] = V[i - 1] + dep[i]
    D = V[N] - V[n]
    K = V[N2] - V[n]
    MW = max(dep[n + 1:N2 + 1])
    return dep, D, K, MW


def signed_law(elems, mod):
    """integer weights of sum delta_c e_c mod `mod`; total weight 4^len(elems)."""
    assert len(elems) <= 31
    cnt = np.zeros(mod, dtype=np.int64)
    cnt[0] = 1
    for e in elems:
        a = int(e % mod)
        if a == 0:
            cnt = 4 * cnt
            continue
        cnt = 2 * cnt + np.roll(cnt, a) + np.roll(cnt, -a)
    return cnt


def coll_pair(x, n, N, N2, p):
    """exact (p^K Coll_K, p^D Coll_D, D, K, M_W) of the composite window at the integer point x."""
    dep, D, K, MW = window(x, n, N, N2, p)
    H = N2 - n
    mod = p ** K
    ys = []
    y = 1
    for c in range(H):
        ys.append(y % mod)
        y = y * (x + n + c + 1) % mod
    cnt = signed_law(ys, mod)
    tot = 4 ** H
    collK = Fraction(int(cnt[0]), tot)
    collD = Fraction(int(cnt[0::p ** D].sum()), tot)
    return p ** K * collK, p ** D * collD, D, K, MW


def chi2_window(x, n, N, p):
    """exact chi^2 of the single window W=[n,N) modulo p^D (Prop 11.12's quantity)."""
    dep, D, K, MW = window(x, n, N, N, p)
    H = N - n
    mod = p ** D
    ys = []
    y = 1
    for c in range(H):
        ys.append(y % mod)
        y = y * (x + n + c + 1) % mod
    cnt = signed_law(ys, mod)
    return p ** D * Fraction(int(cnt[0]), 4 ** H) - 1, D
