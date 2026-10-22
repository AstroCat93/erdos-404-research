#!/usr/bin/env python3
"""ck_gate_kill.py -- exact test of an observation of the second check_R3M instance (round 3):

  Observation G.  Let p be odd, x in Z_p, 1 <= i <= n, s := v(x+i) >= 1, and V_n(x) > s.  If e is a
  path of length n alive at n with slope 0 (v(S_e'(x)) = 0), then v(S_{e|i}(-i)) = s, where
  S_{e|i}(-i) = sum_{j<i} e_j pi_j(-i) is an integer with |S_{e|i}(-i)| < e*(i-1)!.
  Proof: Taylor at x, S_e(-i) = S_e(x) - (x+i) S_e'(x) + (x+i)^2 R with R in Z_p; the three terms have
  valuations >= V_n > s, exactly s, and >= 2s > s.  And pi_j(-i) = 0 for j >= i.
  Consequences: P^0_n(x) is empty when v(x+1) >= 1 or v(x+2) >= 1 (S_e(-1) = 1, S_e(-2) = 1 - e_1),
  and whenever some i <= n has p^{v(x+i)} > e*(i-1)! (a deep gate), as soon as V_n(x) > v(x+i).

usage: ck_gate_kill.py p seed nx n
  x random; 2/3 of the samples get a forced gate v(x+i) = s (i, s random).  For every slope-0 path
  alive at n (DFS, ck_lib) and every i <= n with s = v(x+i) >= 1 and V_n > s, checks v(S_{e|i}(-i)) == s
  (exact integers).  Also counts samples with a deep gate (p^s > e*(i-1)!, V_n > s) and checks that
  their slope-0 population is empty, and checks that x = 1, 2 mod p... i.e. v(x+1)>=1 or v(x+2)>=1
  gives an empty slope-0 population when V_n > v(x+1) resp. v(x+2).
"""
import math
import random
import sys

from ck_lib import PAdic, products, alive_from_scratch


def vint(a, p):
    if a == 0:
        return 10 ** 9
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def main():
    p, seed, nx, n = (int(t) for t in sys.argv[1:5])
    P = PAdic(p, 3 * n + 120)
    rnd = random.Random(seed)
    pij = {}
    for i in range(1, n + 1):
        row = [1]
        q = 1
        for j in range(1, i):
            q *= (j - i)
            row.append(q)
        pij[i] = row  # pi_j(-i), j < i
    tests = fails = 0
    deep = deep_f = 0
    low = low_f = 0
    for it in range(nx):
        x = rnd.randrange(P.mod)
        if it % 3:
            i0 = rnd.randrange(1, n + 1)
            s0 = rnd.randrange(1, 3 * n // 2)
            x = (-i0 + p ** s0 * (rnd.randrange(1, p) + p * rnd.randrange(p ** 60))) % P.mod
        pi, dpi, vals = products(P, x, n)
        Vn = sum(vals[1:n + 1])
        al = alive_from_scratch(P, pi, dpi, vals, n)
        slope0 = [b for (b, S, dS) in al if P.v(dS) == 0]
        for i in range(1, n + 1):
            s = vals[i]
            if s < 1 or not Vn > s:
                continue
            for b in slope0:
                T = sum(pij[i][j] for j in range(i) if (b >> j) & 1)
                tests += 1
                fails += vint(T, p) != s
            if p ** s > math.e * math.factorial(i - 1):
                deep += 1
                deep_f += len(slope0) > 0
            if i <= 2:
                low += 1
                low_f += len(slope0) > 0
    print(f"RESULT gatekill p={p} n={n} samples={nx}: v(S_e|i(-i)) == v(x+i) fails {fails}/{tests}; "
          f"deep gates (p^s > e(i-1)!, V_n > s) with nonempty slope-0 population {deep_f}/{deep}; "
          f"v(x+1)>=1 or v(x+2)>=1 (V_n > s) with nonempty slope-0 population {low_f}/{low}")


if __name__ == "__main__":
    main()
