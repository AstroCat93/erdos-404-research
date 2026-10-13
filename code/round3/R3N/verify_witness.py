#!/usr/bin/env python3
"""Independent exact verifier for a p=2 witness file (track R3N, round 3).

Reads a list of integers (one per line, '#' comments allowed), checks that it is a strictly
increasing list of distinct positive integers with the claimed minimum a, computes the exact
integer  S = sum_{n in A} n!  with plain Python big integers (running product, no modular
reduction at all), and prints v_2(S) exactly.

Usage: python3 -I verify_witness.py WITNESSFILE a [K]
Exit code 0 iff the list is valid, min = a, and (if K is given) v_2(S) >= K.
"""
import sys
import time


def main():
    path, a = sys.argv[1], int(sys.argv[2])
    K = int(sys.argv[3]) if len(sys.argv) > 3 else None
    A = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            A.append(int(line))
    ok = True
    if not A or A[0] != a:
        print(f"FAIL: first element {A[0] if A else None} != a={a}")
        ok = False
    if any(x >= y for x, y in zip(A, A[1:])):
        print("FAIL: list not strictly increasing")
        ok = False
    t0 = time.time()
    members = set(A)
    P = 1
    S = 0
    for n in range(1, A[-1] + 1):
        P *= n
        if n in members:
            S += P
    v = (S & -S).bit_length() - 1
    print(f"terms={len(A)} min={A[0]} max={A[-1]} v2(sum)={v} bits(sum)={S.bit_length()} time={time.time()-t0:.1f}s")
    if K is not None:
        print(f"check v2(sum) >= {K}: {v >= K}")
        ok = ok and v >= K
    # v_2(a!) and the excess g = v2(sum) - v2(a!)
    va = 0
    m = a
    while m:
        m //= 2
        va += m
    print(f"v2(a!)={va} => f({a},2) >= {v}, g >= {v - va}")
    print("VERIFIED" if ok else "NOT VERIFIED")
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
