#!/usr/bin/env python3
"""carry_check.py -- exact check of the block recursion (Theorem B of the T3a writeup) on small cases.

Elements x'_n = n!/p^{e0}, n >= N0, e0 = v_p(N0!).  Fix a block level k0 (= relative valuation of a block)
and the jump J to the next attained level.  'lower' = elements with v < k0, 'block' = elements with v == k0.
  Y = sum_{lower} eta_n x'_n,  W = sum_{block} eta_n (x'_n / p^{k0}),  eta iid in {-1,0,1} w.p. 1/4,1/2,1/4.
  q(z)  = P(p^{k0} | Y and Y/p^{k0} == z mod p^J)        (carry law on the divisibility event)
  b(z)  = P(W == z mod p^J)                               (block signed-sum law)
Theorem B:  C_{k0+J} = p^{k0+J} sum_z q(z) b(-z),  C_{k0} = p^{k0} sum_z q(z),
            C_{k0+J} - C_{k0} = p^{k0} sum_z q(z) (p^J b(-z) - 1)  <=  C_{k0} * Gamma,  Gamma = p^J b(0) - 1,
with equality iff q is concentrated on z = 0.  We verify the identity against a direct DP for C (all elements
with v < k0+J mod p^{k0+J}), report the defect D = C_{k0+J}/C_{k0} - 1, Gamma, the ratio D/Gamma, and the
total-variation distance of q/|q| from uniform.  Exact rationals throughout.
Usage: python3 -I carry_check.py p N0 k0 J
"""
import sys
from fractions import Fraction
from math import factorial

def vfact(n, p):
    v = 0; m = n
    while m:
        m //= p; v += m
    return v

def signed_sum_counts(elems, mod):
    cnt = {0: 1}
    for a in elems:
        a %= mod
        new = {}
        for s, c in cnt.items():
            for d, w in ((0, 2), (a, 1), (mod - a, 1)):
                t = (s + d) % mod
                new[t] = new.get(t, 0) + c * w
        cnt = new
    return cnt

def main():
    p, N0, k0, J = map(int, sys.argv[1:5])
    e0 = vfact(N0, p)
    lower, block, allk = [], [], []
    n = N0
    while vfact(n, p) - e0 < k0 + J:
        v = vfact(n, p) - e0
        x = factorial(n) // p ** e0
        allk.append(x)
        if v < k0: lower.append(x)
        elif v == k0: block.append(x // p ** k0)
        else: raise SystemExit("level %d is attained between k0 and k0+J: J is not the jump" % v)
        n += 1
    print("p=%d N0=%d e0=%d k0=%d J=%d  #lower=%d  #block=%d  block units mod p^J: %s" % (
        p, N0, e0, k0, J, len(lower), len(block), [y % p ** J for y in block]))
    mod = p ** (k0 + J)
    # direct C values
    cntA = signed_sum_counts(allk, mod)
    C_top = Fraction(mod * cntA.get(0, 0), 4 ** len(allk))
    cntL = signed_sum_counts(lower, p ** k0)
    C_k0 = Fraction(p ** k0 * cntL.get(0, 0), 4 ** len(lower))
    # carry law q and block law b
    cntY = signed_sum_counts(lower, mod)
    q = {}
    for r, c in cntY.items():
        if r % p ** k0 == 0:
            z = (r // p ** k0) % p ** J
            q[z] = q.get(z, 0) + Fraction(c, 4 ** len(lower))
    cntW = signed_sum_counts(block, p ** J)
    b = {z: Fraction(c, 4 ** len(block)) for z, c in cntW.items()}
    pJ = p ** J
    rhs_top = p ** (k0 + J) * sum(q[z] * b.get((-z) % pJ, 0) for z in q)
    rhs_k0 = p ** k0 * sum(q.values())
    print("C_%d direct = %s = %.10f ; via Theorem B = %s ; equal: %s" % (k0 + J, C_top, float(C_top), rhs_top, C_top == rhs_top))
    print("C_%d direct = %s = %.10f ; via q = %s ; equal: %s" % (k0, C_k0, float(C_k0), rhs_k0, C_k0 == rhs_k0))
    D = C_top / C_k0 - 1
    Gam = pJ * b.get(0, 0) - 1
    tot = sum(q.values())
    tv = sum(abs(q.get(z, 0) / tot - Fraction(1, pJ)) for z in range(pJ)) / 2
    print("defect D = C_%d/C_%d - 1 = %.6e ; worst case Gamma = p^J b(0) - 1 = %.6e ; D/Gamma = %.4e" % (
        k0 + J, k0, float(D), float(Gam), float(D / Gam) if Gam else float('nan')))
    print("carry law q/|q|: TV distance from uniform mod p^J = %.6e ; max_z q/|q| = %.6e (uniform %.6e) ; #support = %d of %d" % (
        float(tv), float(max(q.values()) / tot), 1 / pJ, len(q), pJ))
    print("block law: b(0) = %s = %.6e (uniform %.6e)" % (b.get(0, 0), float(b.get(0, 0)), 1 / pJ))

if __name__ == '__main__':
    main()
