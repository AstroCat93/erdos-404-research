#!/usr/bin/env python3
"""test_base.py -- exact check of Proposition W of the M4C report (an explicit slope-0 path alive at 3p).

Claim: let p >= 7 be prime, x = p*xi with xi + i != 0 mod p (i = 1..4).  Let the first block be {0, p-1}
(e_0 = e_{p-1} = 1), choose second-block bits e_{p+u} (u<p) with sum_u e_{p+u} u! = w_p/(xi+1) mod p
(w_p = ((p-1)!+1)/p the Wilson quotient) and third-block bits e_{2p+u} making S_e(x) = 0 mod p^3.  Then e is
alive at 3p (V_{3p}(x) = 3) and its slope is 0 iff p is not a Wilson prime (w_p != 0 mod p).
More generally, for a first block e (e_0=1, sum e_j j! = p k_e), the slope is 0 iff lambda_e != k_e mod p,
lambda_e = sum e_j j! H_j.  For Wilson primes the script searches such a first block.
Everything is checked by direct exact evaluation of S_e(x), S_e'(x) mod p^PREC for random x in each class.
usage: test_base.py SEED NX [atom] p1 p2 ...     ('atom': sample x in A = p^3 Z_p)
"""
import random
import sys
from fractions import Fraction
from math import factorial


def v(a, p, cap):
    a %= p ** cap
    if a == 0:
        return cap
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def subset_with_sum(vals, target, p):
    """indices I with sum_{i in I} vals[i] = target mod p (DP); None if impossible."""
    reach = {0: []}
    for i, a in enumerate(vals):
        new = dict(reach)
        for s, I in reach.items():
            t = (s + a) % p
            if t not in new:
                new[t] = I + [i]
        reach = new
    return reach.get(target % p)


def check_path(p, x, bits, n, prec):
    mod = p ** prec
    pi, dpi, S, dS, V = 1, 0, 0, 0, 0
    for j in range(n):
        if bits[j]:
            S = (S + pi) % mod
            dS = (dS + dpi) % mod
        dpi = (dpi * (x + j + 1) + pi) % mod
        pi = pi * (x + j + 1) % mod
        V += v(x + j + 1, p, prec)
    return v(S, p, prec) >= V, v(dS, p, prec), V


def build(p, x, first, prec):
    """complete a first block (list of bits of length p, first[0]=1) to a path of length 3p alive at 3p."""
    mod = p ** prec
    n = 3 * p
    bits = list(first) + [0] * (2 * p)
    pi = [1] * (n + 1)
    for j in range(1, n + 1):
        pi[j] = pi[j - 1] * (x + j) % mod
    for blk, lev in ((1, 1), (2, 2)):
        S = sum(pi[j] for j in range(n) if bits[j]) % mod
        assert S % p ** lev == 0
        need = (-(S // p ** lev)) % p
        vals = [(pi[blk * p + u] // p ** lev) % p for u in range(p)]
        I = subset_with_sum(vals, need, p)
        if I is None:
            return None
        for u in I:
            bits[blk * p + u] = 1
    return bits


ATOM = False


def main():
    global ATOM
    seed, NX = int(sys.argv[1]), int(sys.argv[2])
    args = sys.argv[3:]
    if args and args[0] == "atom":
        ATOM = True
        args = args[1:]
    primes = [int(a) for a in args]
    rnd = random.Random(seed)
    prec = 12
    for p in primes:
        wq = (factorial(p - 1) + 1) // p
        wilson = (wq % p == 0)
        H = [Fraction(0)]
        for j in range(1, p):
            H.append(H[-1] + Fraction(1, j))
        first = [1] + [0] * (p - 2) + [1]
        firsts = [first]
        if wilson:
            # search a first block with sum e_j j! = 0 mod p and lambda_e != k_e mod p
            found = None
            for _ in range(200000):
                e = [1] + [rnd.randrange(2) for _ in range(p - 1)]
                s = sum(factorial(j) for j in range(p) if e[j])
                if s % p:
                    continue
                lam = sum(factorial(j) * H[j] for j in range(p) if e[j])
                lam = lam.numerator * pow(lam.denominator, -1, p) % p
                if (lam - (s // p)) % p:
                    found = e
                    break
            firsts.append(found)
            if found is not None:
                print(f"p={p}: Wilson prime; first block found: indices {[j for j in range(p) if found[j]]}")
        res = []
        for fi, fb in enumerate(firsts):
            if fb is None:
                res.append(("first-block-%d" % fi, "none found"))
                continue
            ok_alive = slope0 = tot = 0
            for _ in range(NX):
                if ATOM:
                    x = p ** 3 * rnd.randrange(p ** (prec - 3))  # x in A = p^3 Z_p
                else:
                    while True:
                        xi = rnd.randrange(p ** (prec - 1))
                        if all((xi + i) % p for i in range(1, 5)):
                            break
                    x = p * xi
                bits = build(p, x, fb, prec)
                if bits is None:
                    continue
                alive, slope, V = check_path(p, x, bits, 3 * p, prec)
                tot += 1
                ok_alive += alive and V == 3
                slope0 += (slope == 0)
            res.append(("first-block-%d" % fi, f"alive&V=3: {ok_alive}/{tot}, slope0: {slope0}/{tot}"))
        print(f"p={p} wilson_quotient_mod_p={wq % p} wilson={wilson} :: {res}")


if __name__ == "__main__":
    main()
