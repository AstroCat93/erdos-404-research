"""m4a_lib.py -- small exact helpers for track M4A (round 4).

Conventions (note.md section 10.1 at an odd prime p; data/round3/reports/R3M.md section 1):
  pi_c(y) = (y+1)...(y+c),  V_t(y) = v_p(pi_t(y)),  M_t(y) = max_{i<=t} v_p(y+i).
  Signed path delta = (delta_0, ..., delta_{t-1}) in {-1,0,1}^t, weights P(0)=1/2, P(+-1)=1/4
  (the law of the difference of two fair bits).  Integer weights: w(0)=2, w(+-1)=1, total 4 per digit.
  T_delta(y) = sum_c delta_c pi_c(y);  T'_delta(y) = sum_c delta_c pi_c'(y).
All arithmetic is with Python integers (exact); valuations are read modulo p^PREC.
The valuation helper follows the conventions of code/round3/check_R3M/ck_lib.py (written by the round-3 checker).
"""
from fractions import Fraction


def vp(a, p, cap=10 ** 9):
    """p-adic valuation of the integer a (cap if a == 0)."""
    if a == 0:
        return cap
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def pis(y, t, mod):
    """lists pi[c], dpi[c] (c = 0..t) of pi_c(y), pi_c'(y) modulo mod (y an integer representative)."""
    pi = [1] * (t + 1)
    dpi = [0] * (t + 1)
    for c in range(1, t + 1):
        pi[c] = pi[c - 1] * (y + c) % mod
        dpi[c] = (dpi[c - 1] * (y + c) + pi[c - 1]) % mod
    return pi, dpi


def Vt(y, t, p, cap=10 ** 9):
    return sum(vp(y + i, p, cap) for i in range(1, t + 1))


def Mt(y, t, p, cap=10 ** 9):
    return max(vp(y + i, p, cap) for i in range(1, t + 1)) if t >= 1 else 0
