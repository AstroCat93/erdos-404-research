#!/usr/bin/env python3
"""vcl_H2direct.py -- independent exact test of M4C Lemma H2 for single polynomials (verify_C_logic track).

Lemma H2: F in Z_p[X], B = b + p^r Z_p, D < K, D >= 2r:
   p^K mu_B{v(F) >= K} - p^D mu_B{v(F) >= D}  <=  p^K mu_B{v(F) >= K, 2 v(F') >= D}.
Everything depends on z mod p^K only, so both sides are exact rationals (counts over z in B mod p^K).
F types: random integer polynomials; planted double roots (X-a)^2 G; planted near-double roots
(X-a)(X-a-p^m u) G; signed window sums sum_c delta_c pi_c(X) with random lazy signed delta (delta_0 = 1).
Control: the right side with 2v(F') >= D+2 instead of >= D (must fail sometimes).
usage: vcl_H2direct.py p ntrials seed
"""
import random
import sys
from fractions import Fraction


def polymul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def ev(F, z, m):
    r = 0
    for c in reversed(F):
        r = (r * z + c) % m
    return r


def deriv(F):
    return [i * F[i] for i in range(1, len(F))] or [0]


def v(n, p, cap):
    if n == 0:
        return cap
    k = 0
    while n % p == 0 and k < cap:
        n //= p
        k += 1
    return k


def make_F(p, rng):
    t = rng.randrange(4)
    G = [rng.randrange(-p ** 3, p ** 3) for _ in range(rng.randrange(1, 4))]
    if t == 0:
        return [rng.randrange(-p ** 4, p ** 4) for _ in range(rng.randrange(2, 7))], "random"
    if t == 1:
        a = rng.randrange(p ** 4)
        return polymul(polymul([-a, 1], [-a, 1]), G), "double"
    if t == 2:
        a = rng.randrange(p ** 4)
        m = rng.randrange(1, 4)
        u = rng.randrange(1, p)
        return polymul(polymul([-a, 1], [-a - p ** m * u, 1]), G), "near-double"
    # signed window sum
    n = rng.randrange(3, 3 * p)
    F = [1]
    pi = [1]
    for c in range(1, n):
        pi = polymul(pi, [c, 1])
        d = rng.choice([0, 0, 1, -1])
        if d:
            F = [x + d * y for x, y in zip(F + [0] * (len(pi) - len(F)), pi)]
    return F, "window"


def main():
    p = int(sys.argv[1])
    ntr = int(sys.argv[2])
    rng = random.Random(int(sys.argv[3]))
    Kmax = {3: 9, 5: 6, 7: 5}[p]
    fails = ctrl = pos = 0
    worst = Fraction(0)
    bytype = {}
    for _ in range(ntr):
        F, typ = make_F(p, rng)
        if all(c == 0 for c in F):
            continue
        Fd = deriv(F)
        r = rng.randrange(0, 3)
        D = rng.randrange(max(2 * r, 1), Kmax)
        K = rng.randrange(D + 1, Kmax + 1)
        b = rng.randrange(p ** r)
        m = p ** K
        nK = nD = nR = nC = 0
        N = p ** (K - r)
        for w in range(N):
            z = b + p ** r * w
            vF = v(ev(F, z, m), p, K)
            vFd = v(ev(Fd, z, m), p, K)
            if vF >= K:
                nK += 1
                if 2 * vFd >= D:
                    nR += 1
                if 2 * vFd >= D + 2:
                    nC += 1
            if vF >= D:
                nD += 1
        L = Fraction(p ** K * nK - p ** D * nD, N)
        R = Fraction(p ** K * nR, N)
        C = Fraction(p ** K * nC, N)
        bytype[typ] = bytype.get(typ, 0) + 1
        if L > R:
            fails += 1
            print(f"FAIL type={typ} F={F} r={r} b={b} D={D} K={K}: L={L} R={R}")
        if L > C:
            ctrl += 1
        if L > 0:
            pos += 1
            worst = max(worst, L / R)
    print(f"p={p}: {ntr} trials {bytype}; failures {fails}; left side > 0 in {pos}; max left/right {float(worst):.4f}; "
          f"control (2v(F') >= D+2) violated {ctrl} times")


if __name__ == "__main__":
    main()
