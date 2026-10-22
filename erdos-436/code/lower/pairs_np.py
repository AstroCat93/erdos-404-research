#!/usr/bin/env python3
"""Independent re-implementation of pairs.c with a different algorithm.

f(n) = sum_{q^e || n} e*R(q) mod k is computed by an additive prime-power sieve:
for every prime q <= N and every power q^j <= N, add R(q) to all multiples of q^j.
Primes come from a plain Eratosthenes sieve (numpy).  Factorisations of the first
pair are re-derived by trial division in pure Python.

Usage: pairs_np.py K VECFILE N [--default D] [--unit U] [--sha]
Prints the first n with f(n) = f(n+1) = 0 (n+1 <= N), and optionally the SHA-256 of
f(1..N) as bytes, for byte-for-byte comparison with `pairs -o`.
"""
import sys, hashlib, time
import numpy as np


def load_vector(path, k):
    R = {}
    with open(path) as fh:
        for line in fh:
            if not line.strip() or line.startswith('#'):
                continue
            q, v = line.split()
            q = int(q)
            if q in R:
                raise SystemExit(f"duplicate {q}")
            R[q] = int(v) % k
    return R


def primes_upto(N):
    s = np.ones(N + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.nonzero(s)[0]


def f_array(k, R, N, default=None, unit=1):
    """returns (f as uint8 array indexed 0..N with f[0] unused, primes, n_defaulted)."""
    P = primes_upto(N)
    f = np.zeros(N + 1, dtype=np.uint16)
    nd = 0
    for q in P.tolist():
        v = R.get(q)
        if v is None:
            if default is None:
                raise SystemExit(f"prime {q} <= N has no value and no default")
            v = default % k
            nd += 1
        v = (v * unit) % k
        if v == 0:
            continue
        qq = q
        while qq <= N:
            f[qq::qq] += v
            if qq > N // q:
                break
            qq *= q
    f %= k
    return f.astype(np.uint8), P, nd


def first_pair(f, N):
    z = (f == 0)
    z[0] = False
    both = z[1:N] & z[2:N + 1]          # index i <-> pair (i+1, i+2)
    idx = np.flatnonzero(both)
    return (int(idx[0]) + 1 if idx.size else None), int(idx.size), int(z[1:].sum())


def factor(n):
    out = []
    d = 2
    while d * d <= n:
        e = 0
        while n % d == 0:
            n //= d
            e += 1
        if e:
            out.append((d, e))
        d += 1 if d == 2 else 2
    if n > 1:
        out.append((n, 1))
    return out


def main():
    a = sys.argv[1:]
    k, path, N = int(a[0]), a[1], int(a[2])
    default = None
    unit = 1
    sha = '--sha' in a
    if '--default' in a:
        default = int(a[a.index('--default') + 1])
    if '--unit' in a:
        unit = int(a[a.index('--unit') + 1])
    t0 = time.time()
    R = load_vector(path, k)
    f, P, nd = f_array(k, R, N, default, unit)
    Pset_ok = all(int(q) in R for q in P.tolist()) if default is None else True
    n, npairs, nz = first_pair(f, N)
    print(f"[np] k={k} N={N} entries={len(R)} primes<=N={len(P)} defaulted={nd} unit={unit} all_primes_listed={Pset_ok}")
    print(f"[np] zeros on [1,N]={nz} zero-pairs={npairs}")
    if n is None:
        print(f"[np] FIRST_PAIR none with n+1<={N}")
    else:
        print(f"[np] FIRST_PAIR n={n} n+1={n+1}")
        for t in (n, n + 1):
            fs = factor(t)
            s = sum(e * ((R.get(q, default) * unit) % k) for q, e in fs) % k
            print("    ", t, "=", " * ".join(f"{q}^{e}[R={(R.get(q, default) * unit) % k}]" for q, e in fs), " f =", s)
    if sha:
        print("[np] sha256(f[1..N]) =", hashlib.sha256(f[1:N + 1].tobytes()).hexdigest())
    print(f"[np] time {time.time() - t0:.2f}s")


if __name__ == '__main__':
    main()
