"""Theorem F (finiteness families) -- tables of tau(k,p) and independent DP checks.

Claim: p prime, 1<=k<=p, k != 2, a = p*m + (p-k), j = v_p(m+1).
 If j >= tau(k,p) then f(a,p) = v_p(a!) + tau(k,p).
 (k=1: tau=0 -> classical a = -1 mod p.)
Here tau(k,p) = max_{k-1 in S subset [0,k-1]} v_p( sum_{u in S} (-1)^u/u! ), finite for k != 2.
"""
import sys
from core import vp_fact, f_exact_upto, tau

primes = [3, 5, 7, 11, 13]
print("tau(k,p) table (k=1..p), '*' = some Q_S is exactly 0 (only k=2)")
TAU = {}
for p in primes:
    row = []
    for k in range(1, p + 1):
        t, S, z = tau(k, p)
        TAU[(k, p)] = (t, z)
        row.append(("%d" % t) + ("*" if z else ""))
    print("p=%2d:" % p, " ".join(row))

nchk = nbad = 0
for p in primes:
    for k in range(1, p + 1):
        t, z = TAU[(k, p)]
        if k == 2:
            continue
        assert not z
        r = p - k
        # m with v_p(m+1) >= t : m+1 = p^t * s
        ms = []
        for s in range(1, 6):
            m = p ** t * s - 1
            ms.append(m)
        ms = sorted(set(ms))[:4]
        for m in ms:
            a = p * m + r
            if a < 1:
                continue
            pred = vp_fact(a, p) + t
            if pred > 60:
                continue
            got = f_exact_upto(a, p, pred + 1)
            nchk += 1
            if got != pred:
                nbad += 1
                print("MISMATCH p=%d k=%d a=%d pred=%d got=%d" % (p, k, a, pred, got))
            else:
                print("ok p=%d k=%d tau=%d a=%d f=%d=v_p(a!)+%d" % (p, k, t, a, got, t))
print("checked", nchk, "cases, mismatches", nbad)
