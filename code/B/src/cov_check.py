#!/usr/bin/env python3
"""Independent re-check of block-coverage certificates Cov(p,t,H) (Python big-int bitsets, shares no code with cov.c).

For a class representative K' (unit mod p^c, c = v_p((H-1)!)), take an ACTUAL position
N* = p^t * K'' with K'' == K' (mod p^c) (K'' = K' + p^c * r, r random), set N1 = N* - H and
compute directly from the definition
    M  = v_p(N*!) - v_p(N1!)          (Legendre, no closed formula used)
    e_i = (N1+i)! / N1!  mod p^M,   i = 0..H-1   (product of consecutive integers)
then checks that the 2^H subset sums cover Z/p^M with a big-integer bitset DP.
usage: cov_check.py p t H [maxclasses]   (maxclasses>0: random sample of that many classes)
"""
import sys, random
import numpy as np

def vf(n, p):
    s = 0
    while n:
        n //= p; s += n
    return s

def main():
    p, t, H = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    maxc = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    rnd = random.Random(404 + 1000 * p + 10 * t + H)
    c = vf(H - 1, p)
    pc = p ** c
    classes = [k for k in range(1, max(pc, 2)) if (c == 0 or k % p)]
    if c == 0:
        classes = [1]
    if maxc and len(classes) > maxc:
        classes = rnd.sample(classes, maxc)
    ok_all = True
    for k in classes:
        Kpp = k + pc * rnd.randrange(1, 10**6)
        if Kpp % p == 0:
            Kpp += pc
        Ns = p ** t * Kpp
        N1 = Ns - H
        M = vf(Ns, p) - vf(N1, p)
        Q = p ** M
        els = []
        y = 1
        for i in range(H):
            if i > 0:
                y = y * (N1 + i) % Q
            els.append(y)
        # bitset as a Python integer: bit r set  <=>  residue r is a subset sum
        mask = (1 << Q) - 1
        B = 1
        for x in els:
            x %= Q
            if x:
                B |= ((B << x) & mask) | (B >> (Q - x))
        cov = (B == mask)
        if not cov:
            ok_all = False
            print(f"  class K'={k} (N*={Ns}): NOT covered, missing {Q - bin(B).count('1')}")
    print(f"cov_check p={p} t={t} H={H} c={c} M={M} classes_checked={len(classes)}/{len([1] if c==0 else [k for k in range(1,pc) if k%p])} -> {'ALL COVERED' if ok_all else 'FAILURES'}")

main()
