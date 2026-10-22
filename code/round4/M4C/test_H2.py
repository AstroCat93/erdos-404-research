#!/usr/bin/env python3
"""test_H2.py -- exact test of Lemma H2 (multi-scale Hensel increment bound) of the M4C report:
for F in Z_p[X], a ball B = b + p^r Z_p and integers D < K with D >= 2r,
   I_B := p^K mu_B(v(F) >= K) - p^D mu_B(v(F) >= D)  <=  p^K mu_B{ v(F) >= K, 2 v(F') >= D }.
Polynomials: (a) random integer coefficients; (b) signed window sums T(z) = sum_c d_c (z+1)...(z+c), d_c in
{-1,0,1} with P(0)=1/2; (c) products with a planted double root (z+a)^2 * G(z).  Everything exact (integers).
Negative control: the same inequality with the derivative threshold raised by 2 (should fail sometimes).
usage: test_H2.py p SEED NTRIALS [KRMAX]  (trials with K - r > KRMAX are skipped)
"""
import random
import sys


def val(a, p, cap):
    if a % p ** cap == 0:
        return cap
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def peval(coef, y, mod):
    s = 0
    for c in reversed(coef):
        s = (s * y + c) % mod
    return s


def deriv(coef):
    return [i * coef[i] for i in range(1, len(coef))]


def polymul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def rand_poly(kind, rnd, p):
    if kind == 0:
        deg = rnd.randint(1, 7)
        return [rnd.randint(-p ** 2, p ** 2) for _ in range(deg + 1)]
    if kind == 1:
        t = rnd.randint(2, 3 * p)
        coef = [0]
        pic = [1]  # coefficients of pi_c(z)
        for c in range(t):
            d = rnd.choice((0, 0, 1, -1))
            if c == 0:
                d = 1
            while len(coef) < len(pic):
                coef.append(0)
            for i, a in enumerate(pic):
                coef[i] += d * a
            pic = polymul(pic, [c + 1, 1])
        return coef
    a = rnd.randint(0, p ** 3)
    G = [rnd.randint(-p, p) for _ in range(rnd.randint(1, 4))]
    if all(g == 0 for g in G):
        G[0] = 1
    return polymul(polymul([a, 1], [a, 1]), G)


def main():
    p, seed, NT = (int(a) for a in sys.argv[1:4])
    KRMAX = int(sys.argv[4]) if len(sys.argv) > 4 else 99
    rnd = random.Random(seed)
    st = dict(trials=0, fail=0, nonzero_lhs=0, ctrl_fail=0, max_ratio=0.0)
    for _ in range(NT):
        kind = rnd.randrange(3)
        F = rand_poly(kind, rnd, p)
        dF = deriv(F)
        r = rnd.randint(0, 2)
        D = rnd.randint(max(1, 2 * r), 2 * r + 4)
        K = rnd.randint(D + 1, D + 3)
        if K - r > KRMAX:
            continue
        b = rnd.randrange(p ** r) if r else 0
        mK = p ** K
        h = -(-D // 2)
        cntK = cntD = rhs = ctrl = 0
        for u in range(p ** (K - r)):
            y = b + p ** r * u
            fy = peval(F, y, mK)
            if fy % p ** D == 0 and u < p ** (D - r):
                cntD += 1
            if fy == 0:
                cntK += 1
                dv = val(peval(dF, y, mK), p, K)
                if dv >= h:
                    rhs += 1
                if dv >= h + 2:
                    ctrl += 1
        # mu_B(v>=K) = cntK / p^(K-r);  mu_B(v>=D) = cntD / p^(D-r)
        lhs_num = p ** r * (cntK - cntD)       # = p^K mu_K - p^D mu_D, times 1
        rhs_num = p ** r * rhs
        st["trials"] += 1
        if lhs_num != 0:
            st["nonzero_lhs"] += 1
        if lhs_num > rhs_num:
            st["fail"] += 1
            print("FAIL", kind, F[:6], r, b, D, K, lhs_num, rhs_num)
        if lhs_num > p ** r * ctrl:
            st["ctrl_fail"] += 1
        if rhs_num > 0 and lhs_num > 0:
            st["max_ratio"] = max(st["max_ratio"], lhs_num / rhs_num)
    print(f"# test_H2 p={p} seed={seed} NT={NT}")
    print("RESULT", st)


if __name__ == "__main__":
    main()
