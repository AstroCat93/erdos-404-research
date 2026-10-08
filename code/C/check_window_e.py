"""Window approach lemma (e^{-1} form): N = p^J s, 0 <= u < N:
   (N-1-u)! = (N-1)! * (-1)^u / u! * (1 + eps_u), v_p(eps_u) >= J - floor(log_p u) for 1 <= u < p^J (eps_0 = 0).
Exact rational check."""
from fractions import Fraction
from math import factorial
from core import vp
bad = 0; cnt = 0
for p in (2, 3, 5, 7):
    for J in (1, 2, 3):
        for s in (1, 2, 3, p + 1, 2 * p + 1):
            N = p ** J * s
            if N > 400:
                continue
            FN1 = factorial(N - 1)
            for u in range(0, min(N, p ** J)):
                lhs = Fraction(factorial(N - 1 - u))
                main = Fraction(FN1 * (-1) ** u, factorial(u))
                eps = lhs / main - 1
                cnt += 1
                if u == 0:
                    ok = eps == 0
                else:
                    lg = 0
                    while p ** (lg + 1) <= u:
                        lg += 1
                    ok = (eps == 0) or vp(eps, p) >= J - lg
                if not ok:
                    bad += 1
                    print("FAIL", p, J, s, u, vp(eps, p))
print("cases", cnt, "failures", bad)
