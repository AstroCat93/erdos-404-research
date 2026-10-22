#!/usr/bin/env python3
"""selfsim_check.py -- exact checks of the self-similarity identity for windows of length H = p^D
ending at N* = p^t K' (Theorem S1 of writeup.md):
  y_i(K') = i! * A_i * B_i(K'),  A_i = (-1)^i binom(p^D-1, i) = prod_{s<=i}(1 - p^D/s),
  B_i(K') = prod_{s<=i} (1 + p^t K'/(s - p^D)).
and the digit-spread bounds (a) v(A_i - 1) >= D - floor(log_p i),  (b) v(B_i - 1) >= t - floor(log_p i),
(c) v(A_i - 1 + p^D H_i) >= 2(D - floor(log_p i)),  (d) v(y_i - i! A_i) >= t + v(i!) - floor(log_p i).
Reports the MINIMUM over i of (LHS - RHS) for each bound (>= 0 means the bound holds), and whether it is attained (=0)."""
from fractions import Fraction
from math import comb, factorial, floor, log
import sys
def vp(x, p):
    x = Fraction(x)
    if x == 0: return 10**9
    n, d = x.numerator, x.denominator; v = 0
    while n % p == 0: n //= p; v += 1
    while d % p == 0: d //= p; v -= 1
    return v
def flog(i, p):
    return 0 if i == 0 else int(floor(log(i)/log(p) + 1e-12)) if p**int(floor(log(i)/log(p)+1e-12)) <= i else int(floor(log(i)/log(p)+1e-12))-1
def flog_exact(i, p):
    k = 0
    while p**(k+1) <= i: k += 1
    return k
for (p, D, t, Kp) in [(13,2,3,1),(13,2,5,7),(13,3,4,5),(13,3,6,170),(7,2,3,3),(7,3,5,2),(11,2,4,9),(19,2,3,4),(5,3,4,1),(3,4,5,2)]:
    H = p**D; X = p**t * Kp
    worst = {k: None for k in 'abcd'}
    for i in range(H):
        y = 1
        for s in range(1, i+1): y *= (X - (H - s))
        A = Fraction((-1)**i * comb(H-1, i))
        B = Fraction(1)
        for s in range(1, i+1): B *= (1 + Fraction(p**t * Kp, s - H))
        assert y == factorial(i) * A * B, (p, D, t, Kp, i)
        L = flog_exact(i, p)
        Hi = sum(Fraction(1, s) for s in range(1, i+1))
        slack = {'a': vp(A - 1, p) - (D - L), 'b': vp(B - 1, p) - (t - L),
                 'c': vp(A - 1 + p**D * Hi, p) - 2*(D - L), 'd': vp(y - factorial(i)*A, p) - (t + vp(factorial(i), p) - L)}
        for k, v in slack.items():
            if i == 0 and k in 'abc': continue
            if worst[k] is None or v < worst[k]: worst[k] = v
    print(f"p={p} D={D} t={t} K'={Kp}: identity OK for all i<{H}; min slack a={worst['a']} b={worst['b']} c={worst['c']} d={worst['d']}")
print("ALL IDENTITY CHECKS PASSED")
