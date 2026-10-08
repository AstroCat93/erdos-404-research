"""Numerical checks of the structural lemmas (exact integer arithmetic).

(1) grouping: (pm+r)! = p^m m! W_m prod_{i<=r}(pm+i), W_m=(pm)!/(p^m m!) unit, W_m = (-1)^m mod p
(2) gate lemma: if v_p(m+1)=j then prod_{i<=r}(pm+i) == (-1)^r (p-1)!/(p-1-r)!  mod p^{j+1}
(3) approach lemma: if m = p^j t - 1 - i (0<=i), prod_{k<=r}(pm+k) == prod_{k<=r}(k-(1+i)p) mod p^{j+1}
(4) sanity of the DP against known small values.
"""
import sys
from math import factorial
from core import vp, vp_fact, f_exact_upto

ok = True
for p in (2, 3, 5, 7, 11):
    for m in range(0, 40):
        W = factorial(p * m) // (p ** m * factorial(m))
        assert factorial(p * m) % (p ** m * factorial(m)) == 0
        if W % p == 0 or (W - (-1) ** m) % p != 0:
            ok = False
            print("W fail", p, m)
        for r in range(p):
            P = 1
            for i in range(1, r + 1):
                P *= p * m + i
            if factorial(p * m + r) != p ** m * factorial(m) * W * P:
                ok = False
                print("group fail", p, m, r)
print("grouping identity + W_m unit, W_m=(-1)^m mod p:", ok)

ok = True
cnt = 0
for p in (3, 5, 7, 11, 13):
    for j in range(1, 4):
        for t in range(1, 30):
            if t % p == 0:
                continue
            for i in range(0, 12):
                m = p ** j * t - 1 - i
                if m < 0:
                    continue
                mod = p ** (j + 1)
                for r in range(p):
                    P = 1
                    L = 1
                    for k in range(1, r + 1):
                        P *= p * m + k
                        L *= k - (1 + i) * p
                    if (P - L) % mod:
                        ok = False
                        print("approach fail", p, j, t, i, r)
                    if i == 0:
                        G = (-1) ** r * factorial(p - 1) // factorial(p - 1 - r)
                        if (P - G) % mod:
                            ok = False
                            print("gate fail", p, j, t, r)
                    cnt += 1
print("gate lemma + approach lemma (", cnt, "cases):", ok)

# DP sanity vs. published small values (Kovac / Kitamura)
known = {(1, 2): 0, (2, 2): 254, (3, 2): 1, (4, 2): 6, (5, 2): 3, (3, 3): 3, (4, 7): 0, (6, 7): 0}
for (a, p), val in known.items():
    if val > 40:
        continue
    got = f_exact_upto(a, p, val + 2)
    print("f(%d,%d): DP=%s known=%d %s" % (a, p, got, val, "OK" if got == val else "MISMATCH"))
