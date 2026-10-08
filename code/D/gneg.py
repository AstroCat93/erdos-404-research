#!/usr/bin/env python3
"""g_p(-m) for negative integers -m (m >= 1).

g_p(x) := sup over finite B subset Z_{>=1} of v_p(1 + sum_{b in B} P_b(x)),  P_b(x) = (x+1)...(x+b).
For x = a >= 1 this is f(a,p) - v_p(a!).  For x = -m, P_b(-m) = 0 for b >= m, so the sup is a max
over the 2^{m-1} integers 1 + sum_{b in B, b<m} P_b(-m); none of them is 0 when m != 2
(denominator argument), so g_p(-m) < infinity for m != 2 and g_p(-2) = infinity.

Consequence (residue lemma): f(a,p) = v_p(a!) + g_p(-m) for every a >= 1 with a == -m (mod p^{g_p(-m)+1}).
"""
import sys


def vp(n, p):
    if n == 0:
        return 10 ** 9
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def weights(m):
    w = []
    P = 1
    for b in range(1, m):
        P *= (b - m)
        w.append(P)
    return w  # P_1(-m) .. P_{m-1}(-m)


def reachable(m, p, K):
    """Is there B subset [1,m-1] with 1 + sum_B P_b(-m) == 0 mod p^K ?"""
    w = weights(m)
    mod = p ** K
    vals = [vp(x, p) for x in w] + [10 ** 9]
    S = {1 % mod}
    # before adding w[0], need S == 0 mod p^{min(K, v(w[0]))}
    need = min(K, vals[0])
    S = {s for s in S if s % (p ** need) == 0}
    for i, x in enumerate(w):
        need = min(K, vals[i + 1])
        m2 = p ** need
        S2 = set()
        for s in S:
            for t in (s, (s + x) % mod):
                if t % m2 == 0:
                    S2.add(t)
        S = S2
        if not S:
            return False
    return any(s % mod == 0 for s in S)


def g_neg(m, p, cap=400):
    if m == 2:
        return float('inf')
    K = 0
    while K < cap and reachable(m, p, K + 1):
        K += 1
    return K


def brute(m, p):
    w = weights(m)
    best = 0
    from itertools import product
    for bits in product((0, 1), repeat=len(w)):
        s = 1 + sum(x for x, e in zip(w, bits) if e)
        assert s != 0 or m == 2
        best = max(best, vp(s, p))
    return best


if __name__ == "__main__":
    # sanity: brute force for small m
    for p in (2, 3, 5):
        for m in range(1, 15):
            if m == 2:
                continue
            assert g_neg(m, p) == brute(m, p), (m, p)
    print("brute-force agreement OK for m<15, p in {2,3,5}")
    for p in (2, 3, 5, 7):
        row = []
        for m in range(1, 41):
            row.append((m, g_neg(m, p)))
        print("p=%d: " % p + " ".join("%d:%s" % (m, g) for m, g in row))
