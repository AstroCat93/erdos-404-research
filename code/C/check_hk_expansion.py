"""Check: for N = p^J s and 0 <= u < p^J,
  (N-1-u)! = (N-1)! (-1)^u/u! * sum_{k>=0} N^k h_k(1, 1/2, ..., 1/u)
truncated at k <= K0 the error has v_p >= (K0+1)*(J - floor(log_p u)) (relative)."""
from fractions import Fraction
from math import factorial
from core import vp

def hks(u, K0):
    # complete homogeneous symmetric polys of 1/1..1/u up to degree K0
    h = [Fraction(1)] + [Fraction(0)] * K0
    for i in range(1, u + 1):
        x = Fraction(1, i)
        for k in range(1, K0 + 1):
            h[k] = h[k] + x * h[k - 1]
    return h

bad = cnt = 0
for p in (3, 5, 7):
    for J in (1, 2, 3):
        for s in (1, 2, p + 1):
            N = p ** J * s
            if N > 500: continue
            for u in range(1, min(N, p ** J)):
                exact = Fraction(factorial(N - 1 - u), factorial(N - 1)) * factorial(u) * (-1) ** u
                lg = 0
                while p ** (lg + 1) <= u: lg += 1
                for K0 in (0, 1, 2):
                    h = hks(u, K0)
                    approx = sum(Fraction(N) ** k * h[k] for k in range(K0 + 1))
                    err = exact - approx
                    cnt += 1
                    if err != 0 and vp(err, p) < (K0 + 1) * (J - lg):
                        bad += 1
                        print("FAIL", p, J, s, u, K0, vp(err, p))
print("cases", cnt, "failures", bad)
