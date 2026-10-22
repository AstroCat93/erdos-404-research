#!/usr/bin/env python3
"""qfourier.py -- independent evaluation of the block constants q_1, q_2, q_3 of track M4C (report section 4.1),
written by the obstruction verifier without using any M4C code.

Method (different from M4C's dynamic programmes).  A lazy signed digit has characteristic function
E e(t*delta) = 1/2 + cos(2 pi t)/2 = cos^2(pi t) >= 0.  Hence for X = sum_r delta_r c_r mod m the Fourier
coefficients are nonnegative, so P(X = a) <= P(X = 0) for every a (positive definiteness), and
    m * max_a P(X = a) = m * P(X = 0) = sum_{xi mod m} prod_r cos^2(pi xi c_r / m) = 1 + sum_{xi != 0} (...).
With F_r = prod_{s=1}^r (s - p):
  q_1 : m = p,   c_r = F_r = r!            (mod p);
  q_2 : m = p^2, c_r = F_r = r!(1 - p H_r) (mod p^2); (A mod p, digit_1(A) - B mod p) is a bijective image of
        (A - pB) mod p^2 = sum delta_r F_r mod p^2, so this is M4C's q_2;
  q_3 : m = p^3, c_r = F_r                 (mod p^3).
Every term of the xi != 0 sum is positive, so q_k - 1 is computed as a sum of positive terms (log-sum-exp in
float64; relative accuracy about 1e-12).  Output: q_k - 1 for each p, to compare with M4C's table and with the
values M4A computed independently (p = 7, 11, 13).
usage: qfourier.py p1 p2 ...
"""
import sys
import numpy as np


def F_list(p, m):
    F = [1]
    for s in range(1, p):
        F.append(F[-1] * (s - p))
    return [f % m for f in F]


def qminus1(p, k):
    m = p ** k
    c = F_list(p, m)
    xi = np.arange(1, m, dtype=np.int64)
    logprod = np.zeros(m - 1)
    for cr in c:
        t = (xi * cr) % m                      # exact integer phase numerator
        logprod += 2.0 * np.log(np.abs(np.cos(np.pi * t.astype(np.float64) / m)))
    mx = logprod.max()
    return float(np.exp(mx) * np.exp(logprod - mx).sum()), int(np.argmax(logprod)) + 1


def main():
    ps = [int(a) for a in sys.argv[1:]]
    print("p  wilson  q1-1  q2-1  q3-1   (largest single Fourier term index for q2)")
    for p in ps:
        f = 1
        for r in range(1, p):
            f = f * r % (p * p)
        wil = int((f + 1) % (p * p) == 0)
        q1, _ = qminus1(p, 1)
        q2, x2 = qminus1(p, 2)
        q3, _ = qminus1(p, 3)
        print(f"p={p:3d} wilson={wil} q1-1={q1:.6e} q2-1={q2:.6e} q3-1={q3:.6e}  (argmax xi for q2: {x2})", flush=True)


if __name__ == "__main__":
    main()
