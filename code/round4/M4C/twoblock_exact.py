#!/usr/bin/env python3
"""twoblock_exact.py -- exact (rational) annealed band mass of the two-block composite window (Proposition Q of
the M4C report), computed in two independent ways:

 (direct)  E[eps] = average over zeta in Z/p minus {-1,-2} of eps(z), z = p*zeta, where
           eps(z) = p^2 Coll_2 - p Coll_1 for the 2p elements y_c = (z+1)...(z+c), c < 2p  (exact integer counts;
           eps depends on z only through zeta mod p, so this is E over Haar z in pZ_p conditioned on
           v(z+p) = v(z+2p) = 1);
 (formula) Proposition Q: with N = sum_{u<p} d_u u!, k = N/p mod p (when p | N), Lam = sum d_u u! H_u mod p,
           s = sum d'_u u! mod p (d, d' independent lazy signed vectors of length p):
           E[eps] = p^2/(p-2) * E[ 1_{p|N} * cnt(k, Lam, s) ] - p q_p,
           cnt = 1 - [k=Lam] - [s=2Lam-k]  if Lam != s,   cnt = (p-2)[k = s]  if Lam = s.
Also prints q_p = P(sum d_u u! = 0 mod p) and 1 + chi^2 = p q_p.
usage: twoblock_exact.py p1 p2 ...
"""
import sys
from fractions import Fraction
from math import factorial


def direct(p):
    mod = p * p
    tot = Fraction(0)
    nz = 0
    for zeta in range(p):
        if (zeta + 1) % p == 0 or (zeta + 2) % p == 0:
            continue
        z = p * zeta
        elems = []
        y = 1
        for c in range(2 * p):
            elems.append(y % mod)
            y = y * (z + c + 1) % mod
        # signed law with weights (1,2,1)/4 per element -> collision probabilities
        dist = [0] * mod
        dist[0] = 1
        for a in elems:
            new = [0] * mod
            for t in range(mod):
                if dist[t]:
                    new[t] += 2 * dist[t]
                    new[(t + a) % mod] += dist[t]
                    new[(t - a) % mod] += dist[t]
            dist = new
        W = 4 ** (2 * p)
        coll2 = Fraction(dist[0], W)
        coll1 = Fraction(sum(dist[t] for t in range(0, mod, p)), W)
        tot += p * p * coll2 - p * coll1
        nz += 1
    return tot / nz


def formula(p):
    H = [Fraction(0)]
    for j in range(1, p):
        H.append(H[-1] + Fraction(1, j))
    Hm = [h.numerator * pow(h.denominator, -1, p) % p for h in H]
    # joint law of (N mod p^2, Lam mod p) for d, weights (1,2,1)
    mod = p * p
    dist = {(0, 0): 1}
    for u in range(p):
        a = factorial(u) % mod
        l = factorial(u) * Hm[u] % p
        new = {}
        for (n, lam), w in dist.items():
            for d, mult in ((0, 2), (1, 1), (-1, 1)):
                key = ((n + d * a) % mod, (lam + d * l) % p)
                new[key] = new.get(key, 0) + w * mult
        dist = new
    W = 4 ** p
    # law of s mod p
    sl = [0] * p
    sl[0] = 1
    for u in range(p):
        a = factorial(u) % p
        new = [0] * p
        for t in range(p):
            if sl[t]:
                new[t] += 2 * sl[t]
                new[(t + a) % p] += sl[t]
                new[(t - a) % p] += sl[t]
        sl = new
    q = Fraction(sl[0], W)
    acc = 0
    for (n, lam), w in dist.items():
        if n % p:
            continue
        k = (n // p) % p
        for s in range(p):
            if not sl[s]:
                continue
            if lam != s:
                cnt = 1 - (1 if k == lam else 0) - (1 if s == (2 * lam - k) % p else 0)
            else:
                cnt = (p - 2) * (1 if k == s else 0)
            acc += w * sl[s] * cnt
    E = Fraction(p * p, p - 2) * Fraction(acc, W * W) - p * q
    return E, q


def main():
    for p in (int(a) for a in sys.argv[1:]):
        E2, q = formula(p)
        E1 = direct(p) if p <= 23 else None
        agree = (E1 == E2) if E1 is not None else "not run"
        print(f"p={p}: q_p={float(q):.6e} (1+chi^2 = p q_p = {float(p*q):.6f}); E[eps_2block] formula = {float(E2):.6e}; "
              f"direct = {float(E1) if E1 is not None else float('nan'):.6e}; exact agreement: {agree}")


if __name__ == "__main__":
    main()
