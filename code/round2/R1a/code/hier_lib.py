# Exact (rational) implementation of the carry hierarchy for p = 2.
#   u0_n = (u0_{n-1} + e_{n-1})/(y+n),   uj_n = (uj_{n-1} + u(j-1)_n)/(y+n)  (j >= 1),   all u_0 = 0.
from fractions import Fraction as Fr
def v2i(n):
    if n == 0: return 10**9
    return (n & -n).bit_length() - 1
def vf(q):
    if q == 0: return 10**9
    return v2i(q.numerator) - v2i(q.denominator)
JMAX = 5
def hier(y, path, jmax=JMAX):
    u = [Fr(0)] * jmax
    for k, e in enumerate(path):
        n = k + 1
        new = [Fr(0)] * jmax
        new[0] = (u[0] + e) / (y + n)
        for j in range(1, jmax): new[j] = (u[j] + new[j - 1]) / (y + n)
        u = new
    return u
def flat_order(u):
    m = 0
    while m < len(u) - 1 and vf(u[m]) >= 0: m += 1
    return m
def valid_paths(y, n, cap=40):
    paths = [()]
    for k in range(n):
        new = []
        for p in paths:
            for e in ((1,) if k == 0 else (0, 1)):
                q = p + (e,)
                if vf(hier(y, q, 1)[0]) >= 0: new.append(q)
        paths = new[:cap]
    return paths
def mflat(y, path, m):
    u = hier(y, path, m)
    return all(vf(u[j]) >= 0 for j in range(m))
def env(y, n):
    P = sum(v2i(y + l) for l in range(1, n + 1)); M = max(v2i(y + l) for l in range(1, n + 1))
    pin = 1
    for l in range(1, n + 1): pin *= (y + l)
    return P, M, pin
