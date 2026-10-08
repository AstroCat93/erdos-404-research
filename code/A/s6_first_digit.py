# s6_first_digit.py -- residues r mod p with g(a,p)=0 (i.e. f(a,p)=v_p(a!)) for all a = r mod p.
# g(a,p) >= 1 iff 0 in B_a mod p, B_a mod p = { sum_{j in J, 0 in J, J subset [0,t]} (-1)^j t!/(t-j)! } mod p,
# where t = p-1-r  (products prod_{l<=j}(a+l) vanish mod p for j>t).
# Theorem check: for t>=2 the integer sums are all nonzero (sum = 1 mod t), so if p > max|sum| then g=0.
from itertools import combinations
from sympy import primerange
from math import factorial

def sums_t(t):
    terms = [(-1) ** j * factorial(t) // factorial(t - j) for j in range(1, t + 1)]
    S = {1}
    for x in terms:
        S |= {s + x for s in S}
    return S

maxabs = {t: max(abs(s) for s in sums_t(t)) for t in range(0, 9)}
print("t : max|sum| over subsets J ∋ 0 :", maxabs)
print("t : is 0 an integer sum? ", {t: (0 in sums_t(t)) for t in range(0, 9)})
for p in primerange(3, 60):
    zero_cls = []
    for r in range(p):
        t = p - 1 - r
        S = sums_t(t) if t <= 20 else None
        if S is None:  # large t: brute-force mod p via DP
            vals = {1 % p}; c = 1
            for j in range(1, t + 1):
                c = c * (r + j) % p
                vals |= {(v + c) % p for v in vals}
            hit = 0 in vals
        else:
            hit = any(s % p == 0 for s in S)
        if not hit: zero_cls.append(r)
    pred = sorted((p - 1 - t) for t in range(0, p) if (t == 0 or (t >= 2 and maxabs.get(t, 10**18) < p)))
    print(f"p={p}: residues r with f(a,p)=v_p(a!) for all a=r mod p: {zero_cls}  "
          f"(as -1-t: t={[p-1-r for r in zero_cls]});  theorem guarantees r in {pred}: "
          f"{'OK' if set(pred) <= set(zero_cls) else 'FAIL'}")
