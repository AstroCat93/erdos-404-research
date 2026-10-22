#!/usr/bin/env python3
"""check_R3N: own exact witness verifier for p = 2 (independent of the track's two verifiers).

The track's verifiers (code/round3/R3N/verify_witness.py, verify_witness_gmp.c) both form
S = sum_{n in A} n! as a running product of n! that is added term by term.  This file uses two
different methods and requires them to agree:

  (H) Horner nesting, exact integers, no reduction.  For A = {a_1 < ... < a_m},
        S = a_1! * (1 + P(a_1+1, a_2) * (1 + P(a_2+1, a_3) * ( ... (1 + P(a_{m-1}+1, a_m)) ... ))),
      with P(x, y) = x (x+1) ... y, evaluated from the inside out.  Then
        v_2(S) = v_2(a_1!) + v_2(inner),  and also v_2(S) is read off the full product
      a_1! * inner (gmpy2.fac(a_1) * inner), as a cross-check.
  (M) Modular, via odd parts.  n! = 2^{v(n!)} * U(n) with v(n!) = n - s_2(n) (Legendre) and
      U(n) = prod_{m <= n} odd(m).  With R = K + 64 it computes
        S mod 2^R = sum_{n in A} (U(n) mod 2^R) * 2^{v(n!)}  mod 2^R,
      and v_2(S) = position of the lowest set bit, provided it is < R (otherwise "v >= R").

The file format is one integer per line; lines starting with '#' and blank lines are ignored.
It also checks: every entry is an integer, the list is strictly increasing, min = a.
Accepts plain or .gz files.  Prints the SHA-256 of the (decompressed) text.

Usage: python3 -I verify_w.py FILE a K       (K = the claimed exact valuation)
Exit 0 iff the list is valid, min A = a, and both methods give v_2(S) = K exactly.
"""
import gzip
import hashlib
import sys
import time

import gmpy2
from gmpy2 import mpz


def legendre2(n):
    return n - bin(n).count('1')


def odd(m):
    while m % 2 == 0:
        m //= 2
    return m


def read_list(path):
    raw = gzip.open(path, 'rb').read() if path.endswith('.gz') else open(path, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    A = []
    for line in raw.decode('ascii').splitlines():
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        if not s.isdigit():
            raise ValueError(f"non-integer line: {s!r}")
        A.append(int(s))
    return A, sha


def method_H(A):
    inner = mpz(1)
    for i in range(len(A) - 1, 0, -1):
        P = 1
        for j in range(A[i - 1] + 1, A[i] + 1):
            P *= j
        inner = 1 + inner * P
    v_inner = gmpy2.bit_scan1(inner)
    S = gmpy2.fac(A[0]) * inner
    vS = gmpy2.bit_scan1(S)
    if vS != legendre2(A[0]) + v_inner:
        raise AssertionError("method H: inconsistent valuations")
    return vS, S.bit_length()


def method_M(A, R):
    Aset = set(A)
    U = mpz(1)
    Smod = mpz(0)
    for n in range(1, A[-1] + 1):
        U = gmpy2.f_mod_2exp(U * odd(n), R)
        if n in Aset:
            e = legendre2(n)
            if e < R:
                Smod += U << e
    Smod = gmpy2.f_mod_2exp(Smod, R)
    if Smod == 0:
        return None  # v >= R
    return gmpy2.bit_scan1(Smod)


def main():
    path, a, K = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    A, sha = read_list(path)
    ok = True
    if not A or A[0] != a:
        print(f"FAIL: min A = {A[0] if A else None} != a = {a}")
        ok = False
    if any(x >= y for x, y in zip(A, A[1:])):
        print("FAIL: not strictly increasing")
        ok = False
    print(f"file={path} sha256(text)={sha} terms={len(A)} min={A[0]} max={A[-1]}")
    t0 = time.time()
    vH, bits = method_H(A)
    t1 = time.time()
    vM = method_M(A, K + 64)
    t2 = time.time()
    print(f"method H (Horner, exact): v2(S)={vH} bits(S)={bits} time={t1 - t0:.1f}s")
    print(f"method M (mod 2^(K+64), odd parts): v2(S)={'>=K+64' if vM is None else vM} time={t2 - t1:.1f}s")
    if vH != vM:
        print("FAIL: methods disagree")
        ok = False
    if vH != K:
        print(f"FAIL: v2(S) = {vH} != claimed K = {K}")
        ok = False
    va = legendre2(a)
    print(f"v2(a!)={va}; claimed f({a},2) >= {K}, g >= {K - va}")
    print("VERIFIED (both methods, v2(S) = K exactly)" if ok else "NOT VERIFIED")
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
