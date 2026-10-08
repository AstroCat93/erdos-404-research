#!/usr/bin/env python3
"""First-moment experiment for p = 2 (NUMERICAL, not a proof).

For a 2-adic alpha (sampled as a random large even integer) and m >= 1, let r = alpha mod 2^m,
L = 2^m - r (L = 2^m if r = 0), so alpha + L is the first multiple of 2^m above alpha.
Z'_m(alpha) := number of eps-sequences (eps_0 = 1) that pass every gate of the c-recursion up to
stage L-1 and satisfy c_{L-1} + eps == 0 mod 2^m at the deep gate alpha + L.
Then g(alpha) >= v_2(P_{L-1}(alpha)) + m  ==>  Z'_m(alpha) >= 1, so mu(E_2) <= E_alpha[Z'_m] for all m.
The random-bits ('mean-field') prediction is E[Z'_m | r] = 2^{-s_2(r)}, whose average over r is
(1/2)(3/4)^{m-1} -> 0.  This script estimates E[Z'_m] and P(Z'_m >= 1) by sampling alpha.
"""
import random, sys
from collections import defaultdict


def v2(n):
    return (n & -n).bit_length() - 1


def Zprime(alpha, m):
    r = alpha % (1 << m)
    if r % 2 == 1:
        return 0, 0.0
    L = (1 << m) - r if r else (1 << m)
    ts = [v2(alpha + b + 1) for b in range(L - 1)]
    R = sum(ts) + m
    pop = {0: 1}
    for b in range(L - 1):
        t = ts[b]
        u = (alpha + b + 1) >> t
        Rn = R - t
        modR = 1 << R
        modn = 1 << Rn
        inv = pow(u, -1, modn) if Rn > 0 else 0
        new = defaultdict(int)
        for c, k in pop.items():
            for e in ((1,) if b == 0 else (0, 1)):
                x = (c + e) % modR
                if t and (x & ((1 << t) - 1)):
                    continue
                nc = ((x >> t) * inv) % modn if Rn > 0 else 0
                new[nc] += k
        pop = new
        R = Rn
        if not pop:
            return 0, 2.0 ** (-bin(r).count('1'))
    mask = (1 << m) - 1
    Z = 0
    for c, k in pop.items():
        for e in ((1,) if L == 1 else (0, 1)):
            if (c + e) & mask == 0:
                Z += k
    return Z, 2.0 ** (-bin(r).count('1'))


if __name__ == "__main__":
    ms = [int(x) for x in sys.argv[1].split(',')]
    ns = int(sys.argv[2]); seed = int(sys.argv[3])
    rnd = random.Random(seed)
    for m in ms:
        tot = 0; surv = 0; mf = 0.0; zmax = 0
        for i in range(ns):
            alpha = rnd.getrandbits(4096)
            Z, M = Zprime(alpha, m)
            tot += Z; surv += (Z > 0); mf += M if alpha % 2 == 0 else 0.0
            zmax = max(zmax, Z)
        print(f"m={m} samples={ns} E[Z']={tot/ns:.4f} P(Z'>=1)={surv/ns:.4f} meanfield={mf/ns:.4f} "
              f"(exact mean-field average {(0.5*(0.75)**(m-1)):.4f}) maxZ={zmax}", flush=True)
