#!/usr/bin/env python3
"""cpJ.py -- block constants for Theorem D / Theorem C of the T3a writeup.

For a prime p and J >= 1 let e_u = (p-1)! (-1)^u / u!  (u = 0..p-1), the gate-block pattern
(note Theorem 3.9(b): every block of level >= J-1 is, mod p^J, a unit times (e_u)).
  c_p(J)   = max_{xi != 0 mod p^J} prod_u |cos(pi xi e_u / p^J)|        (sup of the block's Fourier coefficient)
  Gam_p(J) = sum_{xi != 0 mod p^J} prod_u cos^2(pi xi e_u / p^J)        (block L^2 sum)
  A_p      = sum_{xi != 0 mod p} prod_{r<p} |cos(pi xi r!/p)|           (= Gam-type L^1 sum at J=1; Theorem C)
For J=1, c_p(1) is the c_p of track T4 (checked against T4's values).
Double precision; max is taken over all p^J - 1 residues (no pruning).
"""
import sys
import numpy as np
from math import factorial

def pattern(p):
    return [factorial(p - 1) * (-1) ** u // factorial(u) for u in range(p)]

def main():
    ps = [int(a) for a in sys.argv[1:]] or [3, 5, 7, 11, 13]
    LIM = 6_000_000
    for p in ps:
        e = pattern(p)
        # A_p and c_p(1) with the r! pattern (same set mod p as e_u up to a unit; use r! directly)
        xi = np.arange(1, p)
        prod = np.ones(p - 1)
        for r in range(p):
            prod *= np.abs(np.cos(np.pi * xi * (factorial(r) % p) / p))
        print("p=%d  A_p=%.10f  c_p(1)[r!]=%.10e" % (p, prod.sum(), prod.max()))
        J = 1
        while p ** J <= LIM:
            m = p ** J
            xi = np.arange(1, m, dtype=np.float64)
            pr = np.ones(m - 1)
            pr2 = np.ones(m - 1)
            for u in range(p):
                c = np.abs(np.cos(np.pi * xi * (e[u] % m) / m))
                pr *= c
            arg = int(np.argmax(pr)) + 1
            gam = float((pr * pr).sum())
            print("p=%d J=%d  c_p(J)=%.10e  at xi=%d  Gam_p(J)=%.6e  (p^J-1)c^2=%.6e  rm:p^J(1-1/p)2^-p=%.4e" % (
                p, J, pr.max(), arg, gam, (m - 1) * pr.max() ** 2, m * (1 - 1 / p) / 2 ** p))
            J += 1
        sys.stdout.flush()

if __name__ == '__main__':
    main()
