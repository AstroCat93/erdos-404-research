#!/usr/bin/env python3
"""qconst.py -- exact anti-concentration constants of one full gate block (M4C report, section 6):

  q1(p) = p * max_a P( A = a mod p ),                      A = sum_{r<p} d_r r!
  q2(p) = p^2 * max_{a,b} P( A = a mod p, B - floor(A/p) = b mod p ),   B = sum_{r<p} d_r r! H_r  (H_r mod p)
with d_r i.i.d. lazy signed (P(0)=1/2, P(+-1)=1/4).  Also chi^2(p) = p*P(A=0 mod p) - 1 (the mod-p shell of a
full block, cf. note Prop 11.12) and the 'Wilson' flag.  q1 >= 1 and q2 >= 1 always; the random model predicts
q1, q2 -> 1.  Exact rational arithmetic (integer weights 1,2,1 per digit), printed as floats with 9 digits.
usage: qconst.py MODE pmin pmax       MODE = 1 (q1 only), 2 (q1 and q2), 3 (mod-p^2 block constants q2A, q2B)
"""
import sys
from math import factorial


def primes(a, b):
    out = []
    for n in range(max(a, 2), b + 1):
        if all(n % d for d in range(2, int(n ** 0.5) + 1)):
            out.append(n)
    return out


def q1(p):
    dist = [0] * p
    dist[0] = 1
    f = 1
    for r in range(p):
        if r > 0:
            f = f * r % p
        new = [2 * x for x in dist]
        for t in range(p):
            if dist[t]:
                new[(t + f) % p] += dist[t]
                new[(t - f) % p] += dist[t]
        dist = new
    W = 4 ** p
    return p * max(dist) / W, p * dist[0] / W - 1


def q2(p):
    """joint law of (A mod p^2, B mod p); then fold to (A mod p, B - floor(A/p) mod p)."""
    mod = p * p
    Hm = [0]
    h = 0
    for j in range(1, p):
        h = (h + pow(j, -1, p)) % p
        Hm.append(h)
    dist = {(0, 0): 1}
    f = 1
    for r in range(p):
        if r > 0:
            f = f * r
        a = f % mod
        bb = f * Hm[r] % p
        new = {}
        for (x, y), w in dist.items():
            for d, m in ((0, 2), (1, 1), (-1, 1)):
                key = ((x + d * a) % mod, (y + d * bb) % p)
                new[key] = new.get(key, 0) + w * m
        dist = new
    fold = {}
    for (x, y), w in dist.items():
        key = (x % p, (y - x // p) % p)
        fold[key] = fold.get(key, 0) + w
    W = 4 ** p
    return p * p * max(fold.values()) / W


def main():
    mode, a, b = (int(t) for t in sys.argv[1:4])
    for p in primes(max(a, 5), b):
        wil = ((factorial(p - 1) + 1) // p) % p == 0
        Q1, chi2 = q1(p)
        line = f"p={p:4d} wilson={int(wil)} q1={Q1:.9f} chi2={chi2:.3e}"
        if mode >= 2:
            line += f" q2={q2(p):.9f}"
        print(line, flush=True)


if __name__ == "__main__" and sys.argv[1] in ("1", "2"):
    main()


def q2deep(p):
    """1D constants of a full block mod p^2 (report, Lemma P, early phase):
      qA = p^2 max_a P(sum_r d_r r! = a mod p^2)                 (block starting at a gate of depth >= 2)
      qB(w) = p^2 max_a P(sum_r d_r r!(1 + p w H_r) = a mod p^2) (block starting at a depth-1 gate, unit w mod p)
    returns (qA, max_w qB(w), qB(-1)) as exact Fractions."""
    import numpy as np
    from fractions import Fraction
    m2 = p * p
    Hm = [0]
    h = 0
    for j in range(1, p):
        h = (h + pow(j, -1, p)) % p
        Hm.append(h)
    fact = [1]
    for r in range(1, p):
        fact.append(fact[-1] * r)

    def maxlaw(elems):
        dist = np.zeros(m2, dtype=object)
        dist[0] = 1
        for a in elems:
            a %= m2
            dist = 2 * dist + np.roll(dist, a) + np.roll(dist, -a)
        return Fraction(m2 * int(max(dist)), 4 ** len(elems))

    qA = maxlaw([fact[r] for r in range(p)])
    qBs = {}
    for w in range(1, p):
        qBs[w] = maxlaw([fact[r] * (1 + p * w * Hm[r]) for r in range(p)])
    return qA, max(qBs.values()), qBs[p - 1]


def main_deep():
    a, b = (int(t) for t in sys.argv[2:4])
    for p in primes(max(a, 5), b):
        qA, qBmax, qBm1 = q2deep(p)
        print(f"p={p:4d} q2A-1={float(qA-1):.3e} max_w q2B(w)-1={float(qBmax-1):.3e} q2B(-1)-1={float(qBm1-1):.3e}",
              flush=True)


if __name__ == "__main__" and sys.argv[1] == "3":
    main_deep()
