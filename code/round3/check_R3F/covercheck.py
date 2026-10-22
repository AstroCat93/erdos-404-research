"""covercheck.py -- direct check of the B4-data by-product (check of R3F, round 3):
"every residue class mod 7^9, 11^7 and 13^7 is sum_{i in B} i! for a finite B".
Direct subset-sum reachability DP mod p^K (numpy boolean array), elements i! for all i with v_p(i!) < K
(elements with v_p(i!) >= K are 0 mod p^K and do not matter).  Independent of any Fourier argument.
usage: python3 -I covercheck.py p K [p K ...]
"""
import sys
import time
from math import factorial

import numpy as np


def vp_fact(n, p):
    s, q = 0, p
    while q <= n:
        s += n // q
        q *= p
    return s


def main():
    a = [int(x) for x in sys.argv[1:]]
    for j in range(0, len(a), 2):
        p, K = a[j], a[j + 1]
        t0 = time.time()
        mod = p ** K
        reach = np.zeros(mod, dtype=bool); reach[0] = True
        n = 0
        i = 0
        while vp_fact(i, p) < K:
            x = factorial(i) % mod
            reach |= np.roll(reach, x)
            n += 1
            i += 1
        missing = int((~reach).sum())
        print(f'p={p} K={K} modulus={mod} elements=0!..{i - 1}! ({n})  missing residues: {missing}  ({time.time() - t0:.1f}s)', flush=True)


if __name__ == '__main__':
    main()
