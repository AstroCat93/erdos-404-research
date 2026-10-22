#!/usr/bin/env python3
"""Definition-level check of a published witness for f(a,2) >= K (exact big integers, no modular shortcuts).

A witness file (K. Kitamura's format) lists the indices n > a whose factorials join a!.
We form B = {a} U indices, check that B is strictly increasing with minimum a, compute the
exact integer S = sum_{n in B} n! and its exact 2-adic valuation, and compare with the claim.

Usage: python3 -I verify_witness_bigint.py A CLAIMED_F WITNESS_FILE
"""
import sys
import time


def main():
    a, claimed, path = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    t0 = time.time()
    idx = [int(line) for line in open(path) if line.strip() and not line.startswith("#")]
    B = [a] + idx
    assert all(x < y for x, y in zip(B, B[1:])), "indices must be strictly increasing and > a"
    want = set(B)
    S, fact = 0, 1
    for n in range(1, B[-1] + 1):
        fact *= n
        if n in want:
            S += fact
    assert a >= 1
    v =(S & -S).bit_length() - 1
    print(f"a={a}: |B|={len(B)} terms, max index {B[-1]}, exact v_2(sum) = {v}, claimed f >= {claimed}: "
          f"{'OK' if v >= claimed else 'FAIL'} ({time.time() - t0:.1f} s)")
    sys.exit(0 if v >= claimed else 1)


if __name__ == "__main__":
    main()
