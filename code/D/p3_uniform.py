#!/usr/bin/env python3
"""p = 3: test the 'uniform crossing' property U(j):
   for N == 0 mod 3^j with v_3(N + 3^j) = j, and EVERY c in Z_3 at stage N, is there a choice
   eps_N..eps_{N+3^j-1} with c_{M} in Z_3 for all N <= M <= N+3^j ?
   (c_{M+1} = (c_M + eps_M)/(M+1).)  Only c mod 3^{v((N+3^j)!/N!)} matters.
Also the one-step lemma at valuation-1 gates: from stage N == 0 mod 3 with v_3(N+3) = 1,
every c has >= 2 surviving continuations to stage N+3."""
import sys


def v3(n):
    v = 0
    while n % 3 == 0:
        n //= 3
        v += 1
    return v


def can_cross(N, H, c, prec):
    """DFS: from (N, c mod 3^prec) can we reach stage N+H with integral c?"""
    states = {c % 3 ** prec}
    r = prec
    for M in range(N, N + H):
        t = v3(M + 1)
        u = (M + 1) // 3 ** t
        new = set()
        if t > r:
            raise ValueError("precision too small")
        mod_new = 3 ** (r - t)
        inv = pow(u, -1, mod_new) if mod_new > 1 else 0
        for s in states:
            for e in (0, 1):
                x = (s + e) % 3 ** r
                if x % 3 ** t == 0:
                    new.add(((x // 3 ** t) * inv) % mod_new if mod_new > 1 else 0)
        states = new
        r -= t
        if not states:
            return False
    return True


def check_U(j, kmax):
    H = 3 ** j
    fails = []
    total = 0
    for k in range(1, kmax + 1):
        N = H * k
        if v3(N + H) != j:
            continue
        prec = sum(v3(N + i) for i in range(1, H + 1))
        for c in range(3 ** prec):
            total += 1
            if not can_cross(N, H, c, prec):
                fails.append((N, c))
    return total, fails


if __name__ == "__main__":
    for j, kmax in [(1, 60), (2, 60)]:
        total, fails = check_U(j, kmax)
        print(f"U({j}): tested {total} (N,c) pairs, failures: {len(fails)}; first few: {fails[:8]}")
