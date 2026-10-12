#!/usr/bin/env python3
"""Referee's independent small checks for note_v2 §10 (written from scratch)."""
import math
from fractions import Fraction
import mpmath as mp

def leg(n, p):
    s = 0
    while n:
        n //= p; s += n
    return s
def vp(n, p):
    s = 0
    while n % p == 0:
        n //= p; s += 1
    return s

print("== Legendre values of §10.2")
claims = {(7, 9): 6725592, (11, 9): 235794760, (13, 9): 883708272, (17, 9): 7411742272,
          (19, 8): 943531272, (23, 8): 3559590232, (17, 8): 435984832, (13, 8): 67977552, (11, 8): 21435880}
for (p, D), val in claims.items():
    got = leg(p ** D - 1, p)
    print(f"  v_{p}(({p}^{D}-1)!) = {got}  claimed {val}  {'OK' if got == val else 'MISMATCH'}")

print("== rho_0(p) (Lemma 10.11)")
def rho0(p):
    for rho in range(p):
        S = {0}
        for u in range(rho + 1):
            e = ((-1) ** u * pow(math.factorial(u), -1, p)) % p
            S = S | {(s + e) % p for s in S}
        if len(S) == p:
            return rho
    return None
r0 = {p: rho0(p) for p in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31)}
print("  ", r0, " claimed 1,2,3,4,5,4,4,6,6,6")

print("== L_p (cover depth of E_p) for p<=23, for Prop 10.14(b) and Cor 10.13")
def Lp(p, maxL=6):
    L = 0
    for Lc in range(1, maxL + 1):
        mod = p ** Lc
        S = {0}
        for u in range(p):
            e = ((-1) ** u * pow(math.factorial(u), -1, mod)) % mod
            S = S | {(s + e) % mod for s in S}
        if len(S) == mod:
            L = Lc
        else:
            break
    return L
print("  ", {p: Lp(p) for p in (5, 7, 11, 13, 17, 19, 23)})

print("== D_p = min{D: p^D >= e (p-1)!}")
for p in (7, 11, 13, 17):
    D = 0
    while p ** D < math.e * math.factorial(p - 1):
        D += 1
    print(f"  D_{p} = {D}")

print("== Lambda_p and tau_p(3) (Theorem 10.16)")
mp.mp.dps = 40
for p in (5, 7, 11, 13, 17, 19, 23):
    two_pi = 2 / mp.pi
    lam = mp.mpf(0)
    d = 1
    while True:
        U = 0
        while leg(U, p) < d:
            U += 1
        term = (p ** d - p ** (d - 1)) * two_pi ** U
        lam += term
        if d > 5 and term < mp.mpf(10) ** -30:
            break
        d += 1
    c3 = leg(p ** 2 - 1, p)
    tau3 = mp.mpf(p) ** (3 + c3) * two_pi ** (p ** 2)
    print(f"  p={p}: Lambda={mp.nstr(lam, 6)} tau(3)={mp.nstr(tau3, 4)} 1/(L+tau)={mp.nstr(1/(lam+tau3), 5)}")

print("== Claim 10.9 arithmetic")
A = 2 * 3 ** -1.5 + 1 / 9
ex = math.log2(3 / 4) / 2
print(f"  prefactor={A:.6f}  exponent log2(3/4)/2={ex:.5f}  A*(4/3)={A*4/3:.5f}")
G = 2 ** 40
print(f"  bound at G=2^40: {1/16 + 0.661 * G ** ex + G * 2 ** (-G / 4):.6f} (claimed 0.0646)")
# Worst case over G in [256, 2^20]: D = floor(log2 G) - 1, check 2^(D+1) <= G and D >= 7
worst = 0
for G in range(256, 1 << 20):
    D = G.bit_length() - 2
    assert 2 ** (D + 1) <= G and D >= 7
    lhs = A * (3 / 4) ** (D / 2) + 2.0 ** (D - 2 ** D)
    rhs = 0.661 * G ** ex + G * 2.0 ** (-G / 4)
    worst = max(worst, lhs / rhs)
print(f"  max over G in [256,2^20) of (claimed-bound pieces)/(stated formula) = {worst:.5f} (must be <=1)")

print("== Theorem 10.18 ownership tiling (referee's own script)")
Ht = {1: 6, 2: 10, 3: 19, 4: 24, 5: 32, 6: 35, 7: 39}
def Hof(N):
    t = vp(N, 13)
    return Ht.get(t, 13)
def check_tiling(lo, hi):
    # windows at multiples N>=26 of 13 in [lo,hi)
    ends = [N for N in range(max(26, lo - lo % 13), hi, 13) if N >= 26]
    win = {N: (N - Hof(N), N) for N in ends}
    deep = [N for N in ends if vp(N, 13) >= 3]
    kept = set(ends)
    for N in deep:
        for d in (13, 26):
            M = N - d
            if M in win and win[M][1] > win[N][0] and M not in deep:
                kept.discard(M)
    kept = sorted(kept)
    # disjointness
    bad = 0
    for a, b in zip(kept, kept[1:]):
        if win[a][1] > win[b][0]:
            bad += 1
    # ownership: levels [v((N-H)!)-1, v(N!)-1) consecutive
    for a, b in zip(kept, kept[1:]):
        if leg(win[b][0], 13) != leg(a, 13):
            bad += 1
    # dropped ones have valuation 1
    dropped = [N for N in ends if N not in kept]
    bad += sum(1 for N in dropped if vp(N, 13) != 1)
    return bad, len(kept), len(dropped), kept[0] if lo <= 26 else None
print("  start region:", check_tiling(0, 13 ** 4))
for t in range(3, 12):
    N = 13 ** t * 7
    print(f"  around 7*13^{t}:", check_tiling(N - 13 ** 3, N + 13 ** 3))
N = 13 ** 8
print("  first uncertified window owns", (leg(N - 13, 13) - 1, leg(N, 13) - 1), "claimed [67977551, 67977559)")
print("  first window at 26 owns", (leg(20, 13) - 1, leg(26, 13) - 1))
