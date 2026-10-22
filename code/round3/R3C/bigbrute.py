#!/usr/bin/env python3
"""bigbrute.py (round 3, track R3C) -- independent brute-force reference for block coverage.

For a position N* = p^t K (K not divisible by p) and block length H, put N1 = N* - H and
M = v_p(N*!) - v_p(N1!) (Legendre).  The normalised block is {n!/N1! : N1 <= n < N*}; we compute each
ratio EXACTLY as a Python big integer (math.prod of the consecutive integers N1+1..n), reduce mod
Q = p^M, and form the set of all subset sums mod Q with a Python big-integer bitset:
    S <- S | rot(S, y)   (rot = cyclic rotation of a Q-bit integer).
Returns the number of residues mod Q that are NOT subset sums.  Shares no code with fibcov.c,
fibcov2.c, covchk.c, brute.py or brute_val.py (different arithmetic, different set representation).
usage: bigbrute.py p t H K [K ...]
"""
import math
import sys


def legendre(n, p):
    e = 0
    while n:
        n //= p
        e += n
    return e


def missing(p, t, H, K):
    Ns = p ** t * K
    N1 = Ns - H
    M = legendre(Ns, p) - legendre(N1, p)
    Q = p ** M
    mask = (1 << Q) - 1
    S = 1  # bit 0 set: empty sum
    for i in range(H):
        n = N1 + i
        y = math.prod(range(N1 + 1, n + 1)) % Q  # n!/N1!  (empty product = 1 for i = 0)
        if y:
            S = (S | (S << y) | (S >> (Q - y))) & mask
    return M, Q - bin(S).count('1')


if __name__ == '__main__':
    p, t, H = map(int, sys.argv[1:4])
    for K in map(int, sys.argv[4:]):
        M, m = missing(p, t, H, K)
        print(f"BB p={p} t={t} H={H} M={M} K={K} missing={m}")
