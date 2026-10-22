#!/usr/bin/env python3
"""audit_external_pairs.py -- check a third-party smooth-pairs file "n fact(n) fact(n+1)".

Usage:  python3 -I audit_external_pairs.py PAIRSFILE [LMAX]

The file is treated as data.  For every non-comment line with n <= LMAX it checks that
fact(n) multiplies out to n and fact(n+1) to n+1, that the bases are distinct primes in
increasing order, and that the exponents are >= 1.  ("1" stands for the empty product.)
It also reports how many n <= LMAX whose n(n+1) is smooth over the file's primes are
missing; missing pairs do not affect soundness, only strength.  Standard library only.
"""
import sys
from math import isqrt


def main():
    path = sys.argv[1]
    LMAX = int(sys.argv[2]) if len(sys.argv) > 2 else None
    rows = []
    maxv = 0
    with open(path) as fh:
        for line in fh:
            if line.startswith('#'):
                continue
            t = line.split()
            if len(t) != 3:
                sys.exit(f"bad line: {line!r}")
            n = int(t[0])
            if LMAX is not None and n > LMAX:
                continue
            rows.append((n, t[1], t[2]))
            maxv = max(maxv, n + 1)
    N = maxv
    spf = list(range(N + 1))
    for i in range(2, isqrt(N) + 1):
        if spf[i] == i:
            for j in range(i * i, N + 1, i):
                if spf[j] == j:
                    spf[j] = i
    bases = set()
    prev = 0
    for n, a, b in rows:
        if n <= prev:
            sys.exit(f"not strictly increasing at n={n}")
        prev = n
        for m, s in ((n, a), (n + 1, b)):
            if s == '1':
                if m != 1:
                    sys.exit(f"n={n}: empty factorisation for {m}")
                continue
            prod, last = 1, 1
            for tok in s.split(','):
                q, e = tok.split('^')
                q, e = int(q), int(e)
                if e < 1 or q <= last or q > N or spf[q] != q:
                    sys.exit(f"n={n}: bad factor {tok} of {m}")
                last = q
                bases.add(q)
                prod *= q ** e
            if prod != m:
                sys.exit(f"n={n}: factorisation {s} multiplies to {prod}, not {m}")
    P = max(bases)
    top = rows[-1][0] if LMAX is None else LMAX
    have = set(n for n, _, _ in rows)
    def smooth(m):
        while m > 1:
            if spf[m] > P:
                return False
            m //= spf[m]
        return True
    missing = [n for n in range(1, top + 1) if n not in have and smooth(n) and smooth(n + 1)]
    print(f"{path}: {len(rows)} pairs with n <= {top} audited, all factorisations correct; "
          f"largest base prime {P}; {len(bases)} distinct primes; "
          f"{P}-smooth pairs n <= {top} missing from the file: {len(missing)}")


if __name__ == '__main__':
    main()
