#!/usr/bin/env python3
"""Referee quick checks (independent code): rho_0(p), Legendre values of §10.2, Lambda_p, tau_p(3),
D_13, Claim 10.9 constant, small uniform Cov(p,t,H) minimality (t<=3) and the p=13,t=2 pattern."""
import math
import numpy as np

def vf(n, p):
    s = 0
    while n:
        n //= p; s += n
    return s

def inv(a, m):
    return pow(a, -1, m)

def rho0(p):
    # least rho such that subset sums of {(-1)^u/u! mod p : u<=rho} cover Z/p
    for rho in range(p):
        S = {0}
        for u in range(rho + 1):
            x = ((-1) ** u * inv(math.factorial(u) % p, p)) % p
            S = S | {(s + x) % p for s in S}
        if len(S) == p:
            return rho
    return None

print("rho0:", {p: rho0(p) for p in [3,5,7,11,13,17,19,23,29,31]})

for p, D, claim in [(7,9,6725592),(11,9,235794760),(13,9,883708272),(17,9,7411742272),
                    (19,8,943531272),(23,8,3559590232),(17,8,435984832),(13,8,67977552)]:
    v = vf(p**D - 1, p)
    print(f"v_{p}(({p}^{D}-1)!) = {v}  claim {claim}  {'OK' if v==claim else 'MISMATCH'}")

# Theorem 10.18 ownership of the first uncertified window
print("Thm10.18 levels:", vf(13**8-13,13)-1, vf(13**8,13)-1)

def U(d, p):
    i = 0
    while vf(i, p) < d:
        i += 1
    return i

def Lam(p, dmax=60):
    tot = 0.0
    for d in range(1, dmax):
        tot += (p**d - p**(d-1)) * (2/math.pi) ** U(d, p)
    return tot

def tau(p, t):
    c = vf(p**(t-1) - 1, p)
    return p**(t+c) * (2/math.pi) ** (p**(t-1))

for p in [5,7,11,13,17,19,23]:
    L = Lam(p, 40 if p < 11 else 12)
    print(f"p={p}: Lambda={L:.6g} tau3={tau(p,3):.3g} 1/(L+tau)={1/(L+tau(p,3)):.4g}")

# D_p
for p in [7, 11, 13]:
    D = 0
    while p**D < math.e * math.factorial(p-1):
        D += 1
    print("D_p", p, D)

# Claim 10.9 constant
c = (2*3**-1.5 + 1/9)
print("Claim10.9 constant (4/3)*c =", c*4/3, " exponent log2(3/4)/2 =", math.log2(0.75)/2)

# small Cov checks: Cov(p,t,H): for every unit K' mod p^c, subset sums of y_i cover Z/p^(t+c)
def cov(p, t, H):
    c = vf(H - 1, p)
    M = p ** (t + c)
    pc = p ** c
    Ks = [K for K in range(1, max(pc, 2)) if K % p] if c > 0 else [1]
    if 2 ** H < M:
        return False
    for K in Ks:
        X = p**t * K
        R = np.zeros(M, dtype=bool); R[0] = True
        y = 1
        for i in range(H):
            if i > 0:
                y = (y * (X - (H - i))) % M
            R = R | np.roll(R, y)
        if not R.all():
            return False
    return True

for p, tmax, Hmax in [(7,3,30),(11,3,30),(13,3,30),(17,3,30),(19,3,30),(23,3,30)]:
    row = []
    for t in range(1, tmax + 1):
        hmin = None
        for H in range(1, min(Hmax, p**t) + 1):
            if cov(p, t, H):
                hmin = H; break
        row.append(hmin)
    print(f"min H_t p={p} t=1..{tmax}:", row)

print("p=13,t=2 pattern:", [(H, cov(13, 2, H)) for H in range(9, 27)])
print("p=7,t=3:", [(H, cov(7, 3, H)) for H in range(18, 40)])
