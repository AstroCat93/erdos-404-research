#!/usr/bin/env python3
"""predict.py (round 3, track R3C) -- HEURISTIC predictions from the bottleneck threshold law
(note.md Conjecture 10.24), using the round-2 profile code (code/round2/R3/src/bottleneck.py,
imported read-only).

  nu = R* / ln(p^M * n),  R* = min(R_0, min_{1<=k<=min(c,t,5)} R_k),  n = #classes or #positions.
  Bands (note.md Conj 10.24): nu < 1.17 -> FAIL,  nu > 1.47 -> HOLD,  otherwise MIXED.
Also applies the PROVED necessary condition of Lemma 10.11: (H-1) mod p >= rho0(p), and the counting
bound 2^H >= p^M.  Predicted minimal H_t = least H with H+1 < p^t, both necessary conditions, and nu > 1.47.

usage: predict.py p tmin tmax [pos:N for t=tmax]
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'round2', 'R3', 'src'))
from bottleneck import profile, vf  # noqa: E402


def rho0(p):
    # least rho such that subset sums of {(-1)^u/u! : u <= rho} cover Z/p
    inv = lambda a: pow(a, p - 2, p)
    fac = 1
    S = {0}
    for u in range(p):
        if u:
            fac = fac * u % p
        e = (-1) ** u * inv(fac) % p
        S = S | {(s + e) % p for s in S}
        if len(S) == p:
            return u
    return None


def nu_of(p, t, H, n=None):
    c = vf(H - 1, p)
    M = t + c
    if n is None:
        n = (p ** c - p ** (c - 1)) if c else 1
    o = profile(p, t, H, kmax=min(c, t, 5))
    R = o['Rstar']
    nu = R / math.log(p ** M * n) if R > 0 else 0.0
    return c, M, n, R, nu


def band(nu):
    return 'FAIL' if nu < 1.17 else ('HOLD' if nu > 1.47 else 'MIXED')


def main():
    p, t0, t1 = map(int, sys.argv[1:4])
    posmode = sys.argv[4] if len(sys.argv) > 4 else None
    r0 = rho0(p)
    print(f"# p={p} rho0={r0}")
    for t in range(t0, t1 + 1):
        n_override = int(posmode.split(':')[1]) if (posmode and t == t1) else None
        Hmin_pred = None
        rows = []
        for H in range(2, 2 * p + 1):
            if H + 1 >= p ** t:
                break
            c = vf(H - 1, p)
            M = t + c
            if 2 ** H < p ** M:
                continue
            if (H - 1) % p < r0:
                rows.append(f"  H={H}: (H-1) mod p = {(H-1) % p} < rho0 -> FAIL (proved, Lemma 10.11)")
                continue
            c, M, n, R, nu = nu_of(p, t, H, n_override)
            b = band(nu)
            rows.append(f"  H={H} c={c} M={M} n={n} R*={R:.4g} nu={nu:.3f} -> {b}")
            if b == 'HOLD' and Hmin_pred is None:
                Hmin_pred = H
            if Hmin_pred is not None and H >= Hmin_pred + 2:
                break
        mode = f"positions n={n_override}" if n_override else "uniform"
        print(f"p={p} t={t} [{mode}] predicted minimal H (first HOLD-band H) = {Hmin_pred}")
        for r in rows:
            print(r)


if __name__ == '__main__':
    main()
