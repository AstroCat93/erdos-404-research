#!/usr/bin/env python3
"""brute.py -- reference coverage checker (R3-frontier).  Exact, numpy boolean array of size p^M.
Elements are computed from actual factorials: n!/N1! for N1 = p^t K - H <= n < p^t K, using Python
big integers for N1 and Legendre for M.  Prints the number of residues mod p^M NOT covered.
usage: brute.py p t H K [K ...]      or      brute.py p t H all [lift]
"""
import sys
import numpy as np


def vfact(n, p):
    s = 0
    while n:
        n //= p
        s += n
    return s


def missing(p, t, H, K):
    Ns = p**t * K
    N1 = Ns - H
    M = vfact(Ns, p) - vfact(N1, p)
    Q = p**M
    S = np.zeros(Q, dtype=bool)
    S[0] = True
    e = 1
    for i in range(H):
        if i > 0:
            e = (e * (N1 + i)) % Q
        if e % Q:
            S = S | np.roll(S, e % Q)
    return M, int(Q - S.sum())


def main():
    p, t, H = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    c = vfact(H - 1, p)
    if sys.argv[4] == 'all':
        lift = int(sys.argv[5]) if len(sys.argv) > 5 else 0
        pc = p**c
        Ks = [1 + lift * p] if c == 0 else [K + lift * pc for K in range(1, pc) if K % p]
    else:
        Ks = [int(x) for x in sys.argv[4:]]
    tot_fail = 0
    for K in Ks:
        M, m = missing(p, t, H, K)
        assert M == t + c
        print(f"R p={p} t={t} H={H} M={M} K={K} missing={m}")
        tot_fail += (m > 0)
    print(f"SUMMARY R p={p} t={t} H={H} n={len(Ks)} fail={tot_fail}")


if __name__ == '__main__':
    main()
