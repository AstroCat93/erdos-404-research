#!/usr/bin/env python3
"""Independent check (sum form, no c-recursion): is there A with min A = a and
p^K | sum_{n in A} n! ?  DP over n with partial sums mod p^K, pruned by the
necessary condition S_N == 0 mod p^{min(K, v_p(N!))} (all later terms are
divisible by p^{v_p(N!)}).  Exact decision procedure."""
import sys
from math import factorial


def vp_fact(n, p):
    s, q = 0, p
    while q <= n:
        s += n // q
        q *= p
    return s


def reachable(a, p, K):
    mod = p ** K
    S = {factorial(a) % mod}
    N = a + 1
    fN = factorial(a + 1) % mod  # N! mod p^K
    while True:
        need = min(K, vp_fact(N + 0, p))  # condition at stage N+... handled below
        # include/exclude N!
        newS = set()
        nxt_need = min(K, vp_fact(N + 1, p))
        m = p ** nxt_need
        for s in S:
            for t in (s, (s + fN) % mod):
                if t % m == 0:
                    newS.add(t)
        S = newS
        if not S:
            return False
        if nxt_need >= K:
            return True  # all S are 0 mod p^K already
        N += 1
        fN = (fN * N) % mod


if __name__ == "__main__":
    p = 2
    for a, K in [(0, 254), (0, 255), (2, 254), (2, 255), (6, 133), (6, 134), (4, 6), (4, 7)]:
        print(a, K, reachable(a, p, K), flush=True)
