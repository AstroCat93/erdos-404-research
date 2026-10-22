#!/usr/bin/env python3
"""b2a_exhaustive.py -- exhaustive test of M4B Lemma B2a (factorial cancellation).

Claim: eps_0..eps_{d-1} in {-1,0,1}, sum_k eps_k/k! = 0  ==>  eps_k = 0 (k>=2) and eps_0 = -eps_1.
Equivalently the integer T(eps) = sum_k eps_k (d-1)!/k! vanishes only at eps = 0 and
eps = +-(1,-1,0,...,0)  (3 solutions for d >= 2, 1 for d = 1).
Method: meet in the middle over {-1,0,1}^d (exact integers), for d = 1..DMAX; all solutions listed.
Also: (i) the tail bound sum_{k>k*} 1/k! < 1/k*! (k* = 2..60) checked with Fractions against the
proof's bound (k*+2)/((k*+1)(k*+1)!); (ii) negative control: digits in {-2..2} (lemma must fail);
(iii) for each (p, d, s) with p^s <= e (d-1)!, the number of eps with T(eps) == 0 mod p^s (shows
the depth hypothesis of Cor B2' is not vacuous).
usage: b2a_exhaustive.py DMAX
"""
import sys
import math
from collections import defaultdict
from fractions import Fraction
from itertools import product


def solutions(d, digits=(-1, 0, 1)):
    F = math.factorial(d - 1)
    c = [F // math.factorial(k) for k in range(d)]
    h = d // 2
    left = defaultdict(list)
    for e in product(digits, repeat=h):
        left[sum(a * b for a, b in zip(e, c[:h]))].append(e)
    sols = []
    for e in product(digits, repeat=d - h):
        t = sum(a * b for a, b in zip(e, c[h:]))
        for el in left.get(-t, ()):
            sols.append(el + e)
    return sols


def main():
    DMAX = int(sys.argv[1])
    allok = True
    for d in range(1, DMAX + 1):
        sols = sorted(solutions(d))
        expect = sorted({tuple([0] * d)} | ({tuple([1, -1] + [0] * (d - 2)), tuple([-1, 1] + [0] * (d - 2))} if d >= 2 else set()))
        ok = sols == expect
        # also check sum eps_k/k! == 0 exactly with Fractions for the solutions
        ok = ok and all(sum(Fraction(e, math.factorial(k)) for k, e in enumerate(s)) == 0 for s in sols)
        allok &= ok
        print(f"d={d:2d}: 3^d={3**d:>10d} zero-sum vectors={len(sols)} expected={len(expect)} {'OK' if ok else 'FAIL'}"
              + (f"  sols={sols}" if d <= 4 else ""), flush=True)
    # tail bound used in the proof
    tb_ok = True
    for ks in range(2, 61):
        tail = sum(Fraction(1, math.factorial(k)) for k in range(ks + 1, ks + 60))
        bound = Fraction(ks + 2, (ks + 1) * math.factorial(ks + 1))
        # the finite tail is a lower bound for the infinite tail; check the proof's bound and strictness
        # (infinite tail <= bound by the geometric comparison; we check bound < 1/ks! exactly)
        tb_ok &= (tail <= bound) and (bound < Fraction(1, math.factorial(ks)))
    print(f"tail bound sum_(k>k*) 1/k! <= (k*+2)/((k*+1)(k*+1)!) < 1/k*!, k*=2..60: {'OK' if tb_ok else 'FAIL'}")
    print(f"e-2 < 1: {math.e - 2:.6f}")
    # negative control: digits in {-2,...,2}
    for d in range(3, 7):
        s2 = solutions(d, digits=(-2, -1, 0, 1, 2))
        bad = [s for s in s2 if any(s[k] != 0 for k in range(2, d)) or s[0] != -s[1]]
        print(f"NEG digits in [-2,2], d={d}: zero-sum vectors={len(s2)}, violating the lemma's conclusion={len(bad)}"
              + (f", e.g. {bad[0]}" if bad else ""))
    # depth hypothesis: count eps with T == 0 mod p^s when p^s <= e (d-1)!
    for p in (3, 5, 7):
        for d in range(2, min(DMAX, 9) + 1):
            F = math.factorial(d - 1)
            c = [F // math.factorial(k) for k in range(d)]
            smin = 0
            while p ** smin <= math.e * F:
                smin += 1
            row = []
            for s in range(max(1, smin - 2), smin + 2):
                cnt = sum(1 for e in product((-1, 0, 1), repeat=d) if sum(a * b for a, b in zip(e, c)) % p ** s == 0)
                row.append(f"s={s}{'*' if s >= smin else ' '}:{cnt}")
            print(f"p={p} d={d} (threshold s_min={smin}): #eps with T==0 mod p^s: " + "  ".join(row))
    print(f"RESULT Lemma B2a exhaustive d=1..{DMAX}: {'ALL OK' if allok and tb_ok else 'FAILURES'}")


if __name__ == "__main__":
    main()
