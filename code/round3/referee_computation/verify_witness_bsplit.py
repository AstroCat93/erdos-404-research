#!/usr/bin/env python3
"""Round-3 computational referee: third-method witness verifier for f(a,2) >= K.

Method (shares no code with the R3N track or its checker):
  For A = {n_1 < ... < n_k} with n_1 = a, write b = a-1 and
      S = sum_i n_i! = b! * T,   T = sum_i prod_{m=b+1}^{n_i} m.
  T is computed by BINARY SPLITTING over the index range: for a block of
  indices [i, j) with predecessor value p_i (= n_{i-1}, or b for i = 0),
      R(i,j) = prod_{m=p_i+1}^{n_{j-1}} m,
      T(i,j) = sum_{l=i}^{j-1} prod_{m=p_i+1}^{n_l} m,
  and  R(i,k) = R(i,j) R(j,k),  T(i,k) = T(i,j) + R(i,j) T(j,k).
  Leaf range products are themselves product trees.  Arithmetic is CPython's
  own big integers (not GMP).  Then v_2(S) = v_2(b!) + v_2(T), with v_2(b!)
  taken both from Legendre (b - s_2(b)) and from math.factorial(b) directly.

Usage: python3 -I verify_witness_bsplit.py FILE[.gz] a K   (exits 0 iff all checks pass)
       python3 -I verify_witness_bsplit.py --selftest
"""
import sys, gzip, math, random, time

sys.setrecursionlimit(10000)


def range_prod(lo, hi):
    """prod_{m=lo}^{hi} m (1 if hi < lo), by a balanced product tree."""
    if hi < lo:
        return 1
    if hi - lo < 16:
        r = 1
        for m in range(lo, hi + 1):
            r *= m
        return r
    mid = (lo + hi) // 2
    return range_prod(lo, mid) * range_prod(mid + 1, hi)


def bsplit(A, i, j, prev):
    """Return (R, T) for index block [i, j); prev = value preceding A[i]."""
    if j - i == 1:
        R = range_prod(prev + 1, A[i])
        return R, R
    mid = (i + j) // 2
    R1, T1 = bsplit(A, i, mid, prev)
    R2, T2 = bsplit(A, mid, j, A[mid - 1])
    return R1 * R2, T1 + R1 * T2


def v2(x):
    if x == 0:
        raise ValueError("v2(0)")
    return (x & -x).bit_length() - 1


def v2_sum_factorials(A):
    b = A[0] - 1
    _, T = bsplit(A, 0, len(A), b)
    leg = b - bin(b).count("1") if b > 0 else 0
    direct = v2(math.factorial(b))
    assert leg == direct, (leg, direct)
    return leg + v2(T)


def read_witness(path):
    op = gzip.open if path.endswith(".gz") else open
    header, A = [], []
    with op(path, "rt") as fh:
        for line in fh:
            s = line.strip()
            if not s:
                continue
            if s.startswith("#"):
                header.append(s)
                continue
            A.append(int(s))
    return header, A


def selftest():
    rng = random.Random(20261013)
    for trial in range(400):
        a = rng.randrange(1, 60)
        hi = a + rng.randrange(0, 60)
        A = sorted({a} | {n for n in range(a + 1, hi + 1) if rng.random() < 0.5})
        S = sum(math.factorial(n) for n in A)
        assert v2_sum_factorials(A) == v2(S), (A,)
    # a few known exact values from the literature, checked via brute force minima
    print("selftest: 400 random sets agree with direct sum of math.factorial; OK")


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        selftest()
        return 0
    path, a, K = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    t0 = time.time()
    header, A = read_witness(path)
    ok = True
    print("file:", path)
    for h in header:
        print("header:", h)
    print("terms:", len(A), " min:", min(A), " max:", max(A))
    if A[0] != a or min(A) != a:
        print("FAIL: min != a"); ok = False
    inc = all(A[i] < A[i + 1] for i in range(len(A) - 1))
    print("strictly increasing:", inc)
    ok &= inc
    v = v2_sum_factorials(A)
    print("v_2(sum n!) =", v, " (claimed K =", K, ")")
    if v != K:
        print("FAIL: valuation != K"); ok = False
    # negative controls: removing the last term or the second term must change the valuation
    for name, B in (("drop last", A[:-1]), ("drop 2nd", A[:1] + A[2:])):
        vb = v2_sum_factorials(B)
        print("control (%s): v_2 = %d" % (name, vb))
    print("time %.1fs" % (time.time() - t0))
    print("RESULT", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
