#!/usr/bin/env python3
"""Round-4 novelty referee: small independent check of the constants q_s(p).

q_s(p) = p^s * max_z P( sum_{r<p} d_r * pi_r(-p) = z mod p^s ),
d_r i.i.d. with P(0)=1/2, P(+1)=P(-1)=1/4, pi_r(y) = (y+1)...(y+r).
(note.md section 12.1, M4A's normalisation.)

Exact rational arithmetic by a residue dynamic program (no code shared with
the tracks or verifiers). Also prints, for an OEIS look-up, the counts
N0(p) = #{S subset of {0,...,p-1}: sum_{r in S} r! = 0 mod p} and
C(p) = sum_z N_z^2, where N_z counts subsets with sum = z mod p
(so that q_1(p) = p * C(p) / 4^p).

Usage: python3 -I qconst_small.py [pmax]
"""
import sys
from fractions import Fraction


def primes(n):
    return [q for q in range(3, n + 1) if all(q % d for d in range(2, int(q ** .5) + 1))]


def q_s(p, s):
    m = p ** s
    vals = []
    acc = 1
    for r in range(p):
        if r > 0:
            acc *= (r - p)
        vals.append(acc % m)
    dist = {0: Fraction(1)}
    for a in vals:
        new = {}
        for z, w in dist.items():
            for d, pr in ((0, Fraction(1, 2)), (1, Fraction(1, 4)), (-1, Fraction(1, 4))):
                k = (z + d * a) % m
                new[k] = new.get(k, 0) + w * pr
        dist = new
    return m * max(dist.values())


def subset_counts(p):
    fac = [1]
    for r in range(1, p):
        fac.append(fac[-1] * r % p)
    N = [0] * p
    N[0] = 1
    for a in fac:
        N2 = N[:]
        for z in range(p):
            N2[(z + a) % p] += N[z]
        N = N2
    return N


def main():
    pmax = int(sys.argv[1]) if len(sys.argv) > 1 else 23
    for p in primes(pmax):
        q1 = q_s(p, 1)
        q2 = q_s(p, 2) if p <= 23 else None
        N = subset_counts(p)
        C = sum(x * x for x in N)
        assert Fraction(p * C, 4 ** p) == q1, (p, q1, C)
        line = "p=%2d q1=%s (q1-1=%.3e)" % (p, q1, float(q1 - 1))
        if q2 is not None:
            line += " q2=%s (q2-1=%.3e)" % (q2, float(q2 - 1))
        line += " N0=%d C=%d" % (N[0], C)
        print(line)
        sys.stdout.flush()


if __name__ == "__main__":
    main()
