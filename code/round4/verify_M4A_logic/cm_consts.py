#!/usr/bin/env python3
"""cm_consts.py -- independent block constants for the check of M4A Corollary M' (verify_M4A_logic, round 4).

Shares no code with code/round4/M4A/.  Three independent ways to get the constants of M4A section 4:
  (1) numpy residue DP modulo p^S (arrays, np.roll), exact int64 counts (4^p <= 4^23 < 2^63);
  (2) full enumeration of the 3^p digit vectors (vl_lib.q_consts / vl_lib.P0_table), p <= 13 only;
  (3) Fourier formula  P(Z == z mod p^s) = p^-s sum_xi e(-xi z/p^s) prod_k cos^2(pi xi a_k/p^s)
      in 60-digit mpmath (s = 1, 2 only), as a check of q_1, q_2 at the large primes.
  q_s  = p^s max_z P(Z == z mod p^s),  Z = sum_{k<p} zeta_k pi_k(-p), zeta i.i.d. signed (P(0)=1/2, P(+-1)=1/4);
  P0(g,s) = P(sum_{c<g} zeta_c pi_c(-g) == 0 mod p^s), zeta_0 = 1.
Also prints rho_1, gamma, kappa (M4A section 5) for the truncation level S used by M4A (S=8 for p<=13, S=4 else)
and for the largest S computed by the DP (memory cap p^S <= 2e7).
usage: cm_consts.py p [p ...]
"""
import sys
from fractions import Fraction

import mpmath
import numpy as np

from vl_lib import q_consts, P0_table


def dp_dist(vals, mod, first_fixed):
    cur = np.zeros(mod, dtype=np.int64)
    if first_fixed:
        cur[vals[0] % mod] = 1
        rest = vals[1:]
    else:
        cur[0] = 1
        rest = vals
    for a in rest:
        a %= mod
        cur = 2 * cur + np.roll(cur, a) + np.roll(cur, -a)
    return cur, 4 ** len(rest)


def q_dp(p, S):
    vals = [1]
    for k in range(1, p):
        vals.append(vals[-1] * (k - p))
    dist, tot = dp_dist(vals, p ** S, False)
    assert int(dist.sum()) == tot
    out = {}
    for s in range(1, S + 1):
        red = dist.reshape(-1, p ** s).sum(axis=0)     # index j -> residue j mod p^s (p^s divides p^S)
        out[s] = Fraction(p ** s * int(red.max()), tot)
    return out


def P0_dp(p, S0):
    P0 = {}
    for g in range(1, p + 1):
        vals = [1]
        for c in range(1, g):
            vals.append(vals[-1] * (c - g))
        dist, tot = dp_dist(vals, p ** S0, True)
        row = [Fraction(1)]
        for s in range(1, S0 + 1):
            red = dist.reshape(-1, p ** s).sum(axis=0)
            row.append(Fraction(int(red[0]), tot))
        P0[g] = row
    return P0


def q_fourier(p, s):
    mpmath.mp.dps = 60
    vals = [1]
    for k in range(1, p):
        vals.append(vals[-1] * (k - p))
    m = p ** s
    a = [v % m for v in vals]
    phi = []
    for xi in range(m):
        pr = mpmath.mpf(1)
        for ak in a:
            pr *= mpmath.cos(mpmath.pi * xi * ak / m) ** 2
        phi.append(pr)
    best = mpmath.mpf(0)
    for z in range(m):
        tot = mpmath.mpf(0)
        for xi in range(m):
            tot += phi[xi] * mpmath.cos(2 * mpmath.pi * xi * z / m)
        best = max(best, tot / m)
    return m * best


def derived(p, q, S):
    lq = {s: mpmath.log(mpmath.mpf(q[s].numerator) / q[s].denominator) for s in range(1, S + 1)}
    rho1 = lq[1] + sum((lq[s] - lq[s - 1]) / mpmath.mpf(p) ** (s - 1) for s in range(2, S + 1)) \
        + mpmath.log(p) * mpmath.mpf(p) ** (-S) / (1 - mpmath.mpf(1) / p)
    gamma = lq[1] - mpmath.log((mpmath.mpf(q[2].numerator) / q[2].denominator) / p)
    kappa = (p - 1) * mpmath.log(2) - mpmath.log(p) + rho1 - gamma * mpmath.mpf(p - 1) ** 2 / p ** 2
    return rho1, gamma, kappa


def main():
    mpmath.mp.prec = 256
    for p in (int(a) for a in sys.argv[1:]):
        Sdp = max(s for s in range(1, 9) if p ** s <= 2 * 10 ** 7)       # memory cap for the numpy DP
        q = q_dp(p, Sdp)
        P0 = P0_dp(p, Sdp)
        print(f"== p={p}: q_s by numpy DP mod p^{Sdp}:")
        for s in range(1, Sdp + 1):
            print(f"   q_{s} = {q[s]} = {float(q[s]):.9f}")
        mono = all(q[s] >= q[s - 1] for s in range(2, Sdp + 1)) and all(q[s] <= p * q[s - 1] for s in range(2, Sdp + 1))
        print(f"   q_(s-1) <= q_s <= p q_(s-1) for s <= {Sdp}: {mono}")
        qS, SS_m4a = q, Sdp
        if p <= 13:
            qe = q_consts(p, 8)
            P0e = P0_table(p, 12)
            eqq = all(qe[s] == q[s] for s in range(1, Sdp + 1))
            eqP = all(P0e[g][s] == P0[g][s] for g in range(1, p + 1) for s in range(Sdp + 1))
            print(f"   enumeration (3^p digit vectors) agrees with the DP for s <= {Sdp}: q_s {eqq}, P0 table {eqP}")
            print("   enumeration q_s, s <= 8: " + ", ".join(f"q_{s}={float(qe[s]):.9f}" for s in range(1, 9)))
            qS, SS_m4a = qe, 8
        else:
            SS_m4a = 4
        if p >= 11:
            for s in (1, 2):
                qf = q_fourier(p, s)
                print(f"   Fourier check q_{s}: {mpmath.nstr(qf, 20)} vs DP {float(q[s]):.15f}; "
                      f"|diff| = {mpmath.nstr(abs(qf - mpmath.mpf(q[s].numerator) / q[s].denominator), 3)}")
        print(f"   P0(g,s) s=1..{min(Sdp, 4)}: " + "; ".join(
            f"g={g}:" + ",".join(str(P0[g][s]) for s in range(1, min(Sdp, 4) + 1)) for g in range(1, p + 1)))
        nz = [g for g in range(1, p + 1) if P0[g][Sdp] > 0]
        print(f"   g with P0(g,{Sdp}) > 0: {nz}  (P0(2,s) = 1/4 for all s <= {Sdp}: "
              f"{all(P0[2][s] == Fraction(1, 4) for s in range(1, Sdp + 1))})")
        for SS in sorted({SS_m4a, Sdp}):
            src = qS if SS <= max(k for k in qS if isinstance(k, int)) else q
            r, g, k = derived(p, src, SS)
            print(f"   S={SS}{' (M4A choice)' if SS == SS_m4a else ''}: rho_1 = {mpmath.nstr(r, 10)}, "
                  f"gamma = {mpmath.nstr(g, 10)}, kappa = {mpmath.nstr(k, 10)}")


if __name__ == "__main__":
    main()
