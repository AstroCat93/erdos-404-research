#!/usr/bin/env python3
"""Independent verifier (pure Python big integers, no shared code with the C builder).

usage: verify.py p a K witness_file [extra]
Checks: the list is strictly increasing integers, first element == a, and
        sum_{n in list} n!  == 0  (mod p^K).
Also reports the exact v_p of the sum, capped at K+extra (default extra=30).
"""
import sys

def main():
    p, a, K = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    fn = sys.argv[4]
    extra = int(sys.argv[5]) if len(sys.argv) > 5 else 30
    xs = [int(l) for l in open(fn) if l.strip() and not l.startswith('#')]
    assert xs, "empty witness"
    assert xs[0] == a, f"first element {xs[0]} != a={a}"
    assert all(x < y for x, y in zip(xs, xs[1:])), "not strictly increasing"
    M = p ** (K + extra)
    s = 0
    fact = 1
    n = 0
    j = 0
    last = xs[-1]
    while n <= last:
        if n > 0:
            fact = fact * n % M
        if xs[j] == n:
            s += fact
            j += 1
            if j == len(xs):
                break
        n += 1
    s %= M
    v = 0
    t = s
    if t == 0:
        v = K + extra
    else:
        while t % p == 0:
            t //= p
            v += 1
    ok = v >= K
    print(f"p={p} a={a} K={K} terms={len(xs)} max={last} v_p(sum)>= {v}{' (cap)' if s == 0 else ''}  -> {'VERIFIED' if ok else 'FAILED'}")
    sys.exit(0 if ok else 1)

main()
