#!/usr/bin/env python3
"""ck_validate_lib.py -- validate ck_lib.alive_from_scratch against brute force over all paths.

For random x in Z_p (PREC digits) and small n, every path e of length n (2^(n-1) of them) is
evaluated directly: S_e(x) = sum_j e_j prod_{i<=j}(x+i) recomputed from scratch for each e,
and aliveness v(S_e(x)) >= v(pi_n(x)) decided; the set must equal the DFS output.  Also checks
the slope v(S_e'(x)) via a finite-difference-free formula (derivative of the product rule,
recomputed independently with sum_i prod_{k != i}).
usage: ck_validate_lib.py p seed nx n
"""
import random
import sys

from ck_lib import PAdic, products, alive_from_scratch


def main():
    p, seed, nx, n = (int(a) for a in sys.argv[1:5])
    prec = 40
    P = PAdic(p, prec)
    rnd = random.Random(seed)
    nfail = 0
    tot_alive = 0
    for _ in range(nx):
        x = rnd.randrange(P.mod)
        pi, dpi, vals = products(P, x, n)
        dfs = {b: (S, dS) for (b, S, dS) in alive_from_scratch(P, pi, dpi, vals, n)}
        Vn = sum(P.v(x + i) for i in range(1, n + 1))
        brute = {}
        for rest in range(2 ** (n - 1)):
            b = 1 | (rest << 1)
            S = 0
            dS = 0
            for j in range(n):
                if (b >> j) & 1:
                    prod = 1
                    for i in range(1, j + 1):
                        prod *= (x + i)
                    S += prod
                    # derivative of prod_{i<=j}(x+i): sum_i prod_{k!=i}
                    for i in range(1, j + 1):
                        q = 1
                        for k in range(1, j + 1):
                            if k != i:
                                q *= (x + k)
                        dS += q
            if P.v(S) >= Vn:
                brute[b] = (S % P.mod, dS % P.mod)
        tot_alive += len(brute)
        if set(brute) != set(dfs):
            nfail += 1
            continue
        for b in brute:
            if brute[b] != dfs[b]:
                nfail += 1
                break
    print(f"RESULT validate_lib p={p} n={n} samples={nx} alive paths compared={tot_alive} failures={nfail}")


if __name__ == "__main__":
    main()
