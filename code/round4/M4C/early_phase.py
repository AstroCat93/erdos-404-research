#!/usr/bin/env python3
"""early_phase.py -- deterministic phase of the M4C proof on the atom A = p^3 Z_p (x = p xi, xi = 0 mod p^2).

On A, for j < p^2 the gate x + jp has depth 1 + v_p(j) (deterministic), every other x+i is a unit.
Block schedule n_k = b_k p.  For every k with b_{k+1} < p^2 this script checks EXACTLY (integers):
  (lin_k)  D_{k-1} + D_k <= m_{k-1} - M_{n_{k+1}}  and  M_{n_{k+1}} < m_{k-1}      (R3M (5.2); constant on A)
and computes the pointwise bound of Lemma P (report section 4):
  eps_k <= ebar_k := q1^{n1(k)} q2^{n2(k)} - 1,
  n1 = number of blocks of the composite [n_{k-1}, n_{k+1}) ending at a depth-1 gate,
  n2 = number ending at a depth-2 gate (their start gate has depth 1 and unit = -1 mod p, so the block law
       mod p^2 is that of A - pB, whose max is q2/p^2).
It prints log Pi_early = log(1 + chi^2_{W_0}) + sum_k log(1 + ebar_k) (outward-rounded floats from exact rationals).
usage: early_phase.py p [b0 b1 ...]     (default: greedy schedule, largest b_{k+1} with lin_k, up to < p^2)
"""
import sys
from fractions import Fraction
from math import factorial, log

sys.path.insert(0, __file__.rsplit("/", 1)[0])


def vp(n, p):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def q1_exact(p):
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
    return Fraction(p * max(dist), 4 ** p)


def q2_exact(p):
    m2 = p * p
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
        a = f % m2
        bb = f * Hm[r] % p
        new = {}
        for (x, y), w in dist.items():
            for d, m in ((0, 2), (1, 1), (-1, 1)):
                key = ((x + d * a) % m2, (y + d * bb) % p)
                new[key] = new.get(key, 0) + w * m
        dist = new
    fold = {}
    for (x, y), w in dist.items():
        key = (x % p, (y - x // p) % p)
        fold[key] = fold.get(key, 0) + w
    return Fraction(p * p * max(fold.values()), 4 ** p)


def env(p, b):
    """depth of the gate at block j (position j p) on A, for 1 <= j < p^2."""
    return 1 + vp(b, p)


def V(p, b):
    return sum(env(p, j) for j in range(1, b + 1))


def M(p, b):
    return max(env(p, j) for j in range(1, b + 1))


def lin(p, bm, bk, bp):
    m = V(p, bm)
    K = V(p, bp) - m
    return K <= m - M(p, bp) and M(p, bp) < m


def greedy(p):
    b = [3, 4]
    while True:
        bm, bk = b[-2], b[-1]
        best = None
        for c in range(bk + 1, min(2 * bm + 1, p * p)):
            if lin(p, bm, bk, c):
                best = c
        if best is None:
            return b
        b.append(best)


def main():
    p = int(sys.argv[1])
    b = [int(t) for t in sys.argv[2:]] or greedy(p)
    q1 = q1_exact(p)
    q2 = q2_exact(p)
    logsum = log(float(q1)) * (1 + 1e-12) + 1e-300   # log(1+chi^2_{W_0}), chi^2 = q1 - 1
    rows = []
    for k in range(1, len(b) - 1):
        bm, bk, bp = b[k - 1], b[k], b[k + 1]
        assert bp < p * p
        if not lin(p, bm, bk, bp):
            print(f"lin_{k} FAILS for blocks {bm},{bk},{bp}")
            return
        n1 = sum(1 for j in range(bm + 1, bp + 1) if env(p, j) == 1)
        n2 = sum(1 for j in range(bm + 1, bp + 1) if env(p, j) == 2)
        ebar = q1 ** n1 * q2 ** n2 - 1
        # outward rounding: log(1+ebar) <= n1 log q1 + n2 log q2, evaluated with a relative safety factor
        l = (n1 * log(float(q1)) + n2 * log(float(q2))) * (1 + 1e-12) + 1e-300
        logsum += l
        rows.append((k, bm, bk, bp, n1, n2, float(ebar)))
    print(f"# early_phase p={p} blocks={b}")
    print(f"RIGOROUS q1 = {float(q1):.12f} (q1-1 = {float(q1-1):.4e}), q2 = {float(q2):.12f} (q2-1 = {float(q2-1):.4e})")
    for r in rows:
        print(f"  k={r[0]:2d} composite blocks ({r[1]},{r[3]}] : lin ok, n1={r[4]}, n2={r[5]}, ebar <= {r[6]:.4e}")
    print(f"RIGOROUS log Pi_early <= {logsum:.6f}  (Pi_early <= {2.718281828459046 ** logsum * (1 + 1e-9):.6f}); "
          f"last block of the deterministic phase b = {b[-1]} (p^2 = {p*p})")


if __name__ == "__main__":
    main()


def q3_exact(p):
    """p^3 max_a P(sum_{r<p} d_r F_r = a mod p^3), F_r = prod_{s=1}^r (s - p): the law mod p^3 of a block that starts
    at a depth-1 gate with unit w = -1 mod p^2 (on A = p^3 Z_p: every block ending at a gate jp with p^2 | j)."""
    import numpy as np
    m3 = p ** 3
    F = [1]
    for r in range(1, p):
        F.append(F[-1] * (r - p))
    dist = np.zeros(m3, dtype=object)
    dist[0] = 1
    for a in F:
        a %= m3
        dist = 2 * dist + np.roll(dist, a) + np.roll(dist, -a)
    return Fraction(m3 * int(max(dist)), 4 ** p)
