#!/usr/bin/env python3
"""lead_checks.py -- small independent checks by the lead author for note_v2.md Section 10 (2026-10-12).

1. rho_0(p) (Lemma 10.11): least rho such that subset sums of {(-1)^u/u! : u <= rho} cover Z/p.
2. Ownership tiling of Theorem 10.18 (p = 13): around many multiples N* of 13 of every valuation
   t = 1..10, the kept windows are disjoint and their owned level ranges
   [v((N*-H)!)-1, v(N*!)-1) tile the integers without gaps or overlaps.
3. The level 67,977,551 of Theorem 10.18 and the Legendre values of Section 10.2.
4. D_13 = min{D : 13^D >= e*12!} (Corollary 10.13).
5. Lambda_p and tau_p(3) (Theorem 10.16), recomputed independently with mpmath.
"""
from math import factorial, e
from mpmath import mp, mpf, pi as mpi

mp.dps = 40


def vp(n, p):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def vfact(n, p):
    s = 0
    while n:
        n //= p
        s += n
    return s


# 1. rho_0
print("== rho_0(p)")
for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
    for rho in range(0, p):
        sums = {0}
        for u in range(rho + 1):
            val = ((-1) ** u * pow(factorial(u), -1, p)) % p
            sums |= {(s + val) % p for s in sums}
        if len(sums) == p:
            print(f"p={p} rho0={rho} H1={rho + 1}")
            break

# 2. ownership tiling at p = 13
print("== ownership tiling, p=13 (Theorem 10.18)")
p = 13
Ht = {1: 6, 2: 10, 3: 19, 4: 24, 5: 32, 6: 35, 7: 39}


def H_of(t):
    return Ht.get(t, 13)


def kept_windows(lo, hi):
    """kept windows (start, end) for multiples N* of 13 in [lo, hi], N* >= 26."""
    mults = [N for N in range(lo - lo % p, hi + 1, p) if N >= 26]
    wins = {N: (N - H_of(vp(N, p)), N) for N in mults}
    kept = {}
    for N, (s, en) in wins.items():
        drop = False
        for j in (1, 2):
            M = N + p * j  # window at N is dropped if it overlaps the window of N+13 or N+26 with t>=3
            if M in wins and vp(M, p) >= 3:
                ms, me = wins[M]
                if s < me and ms < en:
                    drop = True
        if not drop:
            kept[N] = (s, en)
    return kept


bad = 0
checked = 0
centres = [26, 39, 169, 2197]
for t in range(1, 11):
    for K in (1, 2, 5, 12, 14, 27):
        if K % p:
            centres.append(p ** t * K)
for C in centres:
    lo, hi = max(26, C - 13 * 8), C + 13 * 8
    kept = kept_windows(lo - 13 * 4, hi + 13 * 4)
    Ns = sorted(N for N in kept if lo <= N <= hi)
    # disjointness
    for a, b in zip(Ns, Ns[1:]):
        if kept[a][1] > kept[b][0]:
            bad += 1
            print("overlap", a, b)
    # tiling of owned levels: end level of window a == start level of next kept window b
    for a, b in zip(Ns, Ns[1:]):
        end_a = vfact(kept[a][1], p) - 1
        start_b = vfact(kept[b][0], p) - 1
        checked += 1
        if end_a != start_b:
            bad += 1
            print("gap/overlap in levels", a, b, end_a, start_b)
s26 = kept_windows(26, 26 + 13 * 3)[26]
print(f"first window {s26}, owns levels [{vfact(s26[0], p) - 1}, {vfact(26, p) - 1})")
print(f"tiling: {checked} consecutive pairs checked around {len(centres)} centres, failures={bad}")

# 3. levels and Legendre values
N8 = 13 ** 8
print("== Theorem 10.18 first uncertified window owns levels",
      [vfact(N8 - 13, 13) - 1, vfact(N8, 13) - 1])
for (pp, D) in [(7, 9), (11, 9), (13, 9), (17, 8), (17, 9), (19, 8), (23, 8), (13, 8), (11, 8)]:
    print(f"v_{pp}(({pp}^{D}-1)!) = {vfact(pp ** D - 1, pp)}")

# 4. D_13
D = 0
while 13 ** D < e * factorial(12):
    D += 1
print("== D_13 =", D)

# 5. Lambda_p, tau_p(3)
print("== Lambda_p, tau_p(3)")
q = mpf(2) / mpi
for p in [5, 7, 11, 13, 17, 19, 23]:
    lam = mpf(0)
    i = 0
    for d in range(1, 400):
        while vfact(i, p) < d:
            i += 1
        lam += (mpf(p) ** d - mpf(p) ** (d - 1)) * q ** i
    c = vfact(p ** 2 - 1, p)
    tau3 = mpf(p) ** (3 + c) * q ** (p ** 2)
    print(f"p={p} Lambda={float(lam):.6g} tau(3)={float(tau3):.4g} 1/(Lambda+tau3)={float(1 / (lam + tau3)):.4g}"
          f"  p(2/pi)^(p-1)={float(p * q ** (p - 1)):.4f}")
