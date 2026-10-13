#!/usr/bin/env python3
"""gate_l2.py -- exact L^2 (collision) shell sums of a single gate block, and the Cauchy-Schwarz L^1 bound
(round 3, track R3F, target (a)).

Gate block of level j (any position): normalised elements, modulo p^d for every d <= j+1, are
   sigma_i = (-1)^i (p-1)!/(p-1-i)!,   0 <= i < p           (note Thm 3.9(b), Lemma 10.11(a))
Level-d L^2 shell:  Q_d = sum_{u unit mod p^d} prod_i cos^2(pi u sigma_i / p^d)
                        = p^d A2(p^d) - p^{d-1} A2(p^{d-1}),
   A2(M) = (1/M) sum_{u mod M} prod_i cos^2(pi u sigma_i/M) = 4^{-p} sum_{delta in {-1,0,1}^p, M | <delta,sigma>} 2^{z(delta)}
   (z = number of zero coordinates).  This is an exact rational; computed here by exact enumeration
   (meet in the middle over two halves of the coordinates, Python integers).
Random model value per level: N_d 2^{-p}, N_d = p^d - p^{d-1}.
Cauchy-Schwarz:  S_d := sum_{u unit} prod |cos| <= sqrt(N_d Q_d).
Also checks the claim: the only delta != 0 with <delta, sigma> = 0 exactly are +-(e_{p-2} + e_{p-1}).
usage: gate_l2.py p dmax
"""
import sys, math
from fractions import Fraction
from collections import defaultdict
from itertools import product


def sigma(p):
    f = math.factorial(p - 1)
    return [(-1) ** i * f // math.factorial(p - 1 - i) for i in range(p)]


def half_table(vals, mod):
    """dict residue -> sum of 2^{zeros} over delta in {-1,0,1}^len(vals)"""
    t = defaultdict(int)
    for dl in product((-1, 0, 1), repeat=len(vals)):
        s = sum(a * b for a, b in zip(dl, vals))
        w = 1 << sum(1 for a in dl if a == 0)
        t[s % mod if mod else s] += w
    return t


def coll(vals, mod):
    """sum over delta with mod | <delta,vals> (mod=0: exact zero) of 2^{z(delta)}"""
    h = len(vals) // 2
    A = half_table(vals[:h], mod)
    B = half_table(vals[h:], mod)
    tot = 0
    for r, w in A.items():
        key = (-r) % mod if mod else -r
        tot += w * B.get(key, 0)
    return tot


def main():
    p, dmax = int(sys.argv[1]), int(sys.argv[2])
    s = sigma(p)
    R = sum(abs(x) for x in s)
    print(f"# gate_l2 p={p} sigma={s}")
    print(f"# R = sum|sigma_i| = {R} (= floor(e (p-1)!) : {R == math.floor(math.e * math.factorial(p-1)) if p < 15 else 'n/a'})")
    # exact relations
    if p <= 13:
        rel = [dl for dl in product((-1, 0, 1), repeat=p) if any(dl) and sum(a * b for a, b in zip(dl, s)) == 0]
        print(f"# nonzero delta in {{-1,0,1}}^p with <delta,sigma>=0 exactly: {rel}")
    c_inf = coll(s, 0)
    print(f"# exact-integer collision weight sum_(<delta,sigma>=0) 2^z = {c_inf} = 2^p * {Fraction(c_inf, 2**p)}")
    A2 = {0: Fraction(1)}
    for d in range(1, dmax + 1):
        M = p ** d
        c = coll(s, M) if M <= R else c_inf
        A2[d] = Fraction(c, 4 ** p)
    print("# d  N_d  Q_d/(N_d 2^-p) [exact]  CS ratio sqrt(N_d Q_d)/(N_d (2/pi)^p)   (A2 exact-integer regime: p^d > R)")
    for d in range(1, dmax + 1):
        N = p ** d - p ** (d - 1)
        Q = p ** d * A2[d] - p ** (d - 1) * A2[d - 1]
        rq = Q / (N * Fraction(1, 2 ** p))
        cs = math.sqrt(N * Q) / (N * (2 / math.pi) ** p)
        print(f"{d:2d} {N} {float(rq):.10f} ({rq}) {cs:.6f} {'(exact-int regime)' if p**d > R else ''}")
    lim = math.sqrt(1.5) * (math.pi / (2 * math.sqrt(2))) ** p
    print(f"# limiting C-S ratio sqrt(3/2) (pi/(2 sqrt 2))^p = {lim:.6f}")


if __name__ == "__main__":
    main()
