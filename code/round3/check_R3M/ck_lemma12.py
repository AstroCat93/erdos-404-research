#!/usr/bin/env python3
"""ck_lemma12.py -- exact tests of R3M Lemma 1 (valuation facts) and Lemma 2 (linearisation).
Second check_R3M instance (round 3); uses ck_lib.py only.

usage: ck_lemma12.py p seed nx nmax
For x random (PREC p-adic digits; every 3rd sample with a forced deep gate v(x+i) >= s):
 Lemma 1 (a) V_n >= v(n!) = (n - s_p(n))/(p-1);  (b) V_n < n/(p-1) + M_n;
         (c) V_j - V_n >= floor((j-n)/p)  (j >= n);
         (d) v(pi_j^[i](x)) >= V_j - i M_j, with pi_j^[i](x) = sum_k c_k binom(k,i) x^(k-i) computed
             from the integer coefficients c_k of pi_j(X) (independent of the product formula);
         (e) S(y+h) = sum_i S^[i](y) h^i for S = pi_j (exact integer identity at random y, h).
 Lemma 2 (n < N with M_N < m = V_n): for every path e alive at n (DFS) and random w:
         (a) aliveness at n of every alive e is unchanged at x' = x0 + p^m w;
         (b) tau_n(e,x') == tau_n(e,x0) - omega^-1 S_e'(x0) w  (mod p^(m - M_n)),  omega = pi_n(x0)/p^m;
         also counted: how often the congruence still holds mod p^(m - M_n + 1) (sharpness, informative).
"""
import math
import random
import sys

from ck_lib import PAdic, products, alive_from_scratch, target


def poly_pi(j):
    """integer coefficients of prod_{k=1}^j (X + k), lowest degree first."""
    c = [1]
    for k in range(1, j + 1):
        new = [0] * (len(c) + 1)
        for d, a in enumerate(c):
            new[d] += a * k
            new[d + 1] += a
        c = new
    return c


def taylor_coeff(c, i, x):
    return sum(c[k] * math.comb(k, i) * x ** (k - i) for k in range(i, len(c)))


def sp(n, p):
    s = 0
    while n:
        s += n % p
        n //= p
    return s


def main():
    p, seed, nx, nmax = (int(a) for a in sys.argv[1:5])
    prec = 3 * nmax + 80
    P = PAdic(p, prec)
    rnd = random.Random(seed)
    polys = {j: poly_pi(j) for j in range(0, nmax + 1)}
    f = {k: 0 for k in "abcde"}
    t = {k: 0 for k in "abcde"}
    l2a = l2a_f = l2b = l2b_f = l2b_sharp = 0
    for it in range(nx):
        x = rnd.randrange(P.mod)
        if it % 3 == 2:
            i0 = rnd.randrange(1, nmax + 1)
            s = rnd.randrange(2, 9)
            x = (-i0 + p ** s * rnd.randrange(1, p ** 40)) % P.mod
        vals = [None] + [P.v(x + i) for i in range(1, nmax + 1)]
        V = [0] * (nmax + 1)
        M = [0] * (nmax + 1)
        for j in range(1, nmax + 1):
            V[j] = V[j - 1] + vals[j]
            M[j] = max(M[j - 1], vals[j])
        for n in range(1, nmax + 1):
            t["a"] += 1
            f["a"] += not (V[n] >= (n - sp(n, p)) // (p - 1) and (n - sp(n, p)) % (p - 1) == 0)
            t["b"] += 1
            f["b"] += not (V[n] * (p - 1) < n + (p - 1) * M[n])
            for j in range(n, nmax + 1):
                t["c"] += 1
                f["c"] += not (V[j] - V[n] >= (j - n) // p)
        for _ in range(4):
            j = rnd.randrange(1, nmax + 1)
            i = rnd.randrange(0, min(j, 6) + 1)
            tc = taylor_coeff(polys[j], i, x)
            t["d"] += 1
            f["d"] += not (P.v(tc) >= V[j] - i * M[j])
            y = rnd.randrange(-10 ** 6, 10 ** 6)
            h = rnd.randrange(-10 ** 6, 10 ** 6)
            lhs = 1
            for k in range(1, j + 1):
                lhs *= y + h + k
            rhs = sum(taylor_coeff(polys[j], ii, y) * h ** ii for ii in range(0, j + 1))
            t["e"] += 1
            f["e"] += lhs != rhs
        # Lemma 2 on a few (n, N)
        for _ in range(3):
            n = rnd.randrange(2 * p, nmax)
            N = rnd.randrange(n + 1, nmax + 1)
            m = V[n]
            if not (M[N] < m) or m > 60:
                continue
            pi, dpi, _ = products(P, x, n)
            alive = alive_from_scratch(P, pi, dpi, vals, n)
            if not alive:
                continue
            if len(alive) > 200:
                alive = rnd.sample(alive, 200)
            x0 = x % p ** m
            pi0, dpi0, _ = products(P, x0, n)
            omega = pi0[n] // p ** m
            md = p ** (m - M[n])
            md1 = p ** (m - M[n] + 1)
            for _w in range(3):
                w = rnd.randrange(p ** 40)
                xp = x0 + p ** m * w
                pi2, dpi2, _ = products(P, xp, n)
                for (b, _S, _dS) in alive:
                    S0 = sum(pi0[j] for j in range(n) if (b >> j) & 1) % P.mod
                    dS0 = sum(dpi0[j] for j in range(n) if (b >> j) & 1) % P.mod
                    S2 = sum(pi2[j] for j in range(n) if (b >> j) & 1) % P.mod
                    l2a += 1
                    if P.v(S2) < m or P.v(S0) < m:
                        l2a_f += 1
                        continue
                    lhs = target(P, S2, pi2[n], m)
                    pred = target(P, S0, pi0[n], m) - pow(omega, -1, p ** (prec - m)) * dS0 * w
                    l2b += 1
                    l2b_f += (lhs - pred) % md != 0
                    l2b_sharp += (lhs - pred) % md1 == 0
    print(f"RESULT lemma1 p={p} nmax={nmax}: (a) fails {f['a']}/{t['a']}; (b) fails {f['b']}/{t['b']}; "
          f"(c) fails {f['c']}/{t['c']}; (d) fails {f['d']}/{t['d']}; (e) fails {f['e']}/{t['e']}")
    print(f"RESULT lemma2 p={p}: (a) aliveness changes {l2a_f}/{l2a}; (b) congruence mod p^(m-M_n) fails "
          f"{l2b_f}/{l2b}; holds also mod p^(m-M_n+1) in {l2b_sharp}/{l2b} (informative)")


if __name__ == "__main__":
    main()
