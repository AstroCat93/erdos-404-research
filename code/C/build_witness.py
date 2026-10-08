"""Constructive check of Theorem C (E-coverage => f(1,p) >= p+p^2+...+p^L).

Follows the proof literally: blocks m = 0..p^L-1, block m = {pm,...,pm+p-1}.
 * non-gate block (p does not divide m+1): need partial sum == 0 mod p^{e_{m+1}};
   guaranteed by Cauchy-Davenport;
 * gate block of level j (1<=j<=L-1): need == 0 mod p^{e_{m+1}}; guaranteed by
   Sigma(E_p) covering Z/p^{j+1};
 * final block m* = p^L - 1: need == 0 mod p^{e_{m*}+L}.
If any step fails the script raises (that would refute the theorem / coverage claim).
Then the resulting set A is checked INDEPENDENTLY with exact big-integer arithmetic.

usage: python3 build_witness.py p L [outfile]
"""
import sys
from core import e_block, vp_fact

p = int(sys.argv[1]); L = int(sys.argv[2])
out = sys.argv[3] if len(sys.argv) > 3 else None
mstar = p ** L - 1
target = e_block(mstar, p) + L
assert target == sum(p ** i for i in range(1, L + 1)), (target,)
T = target + 2
MOD = p ** T

A = []
s = 0             # partial sum mod p^T
fact = 1          # running n! mod p^T
for m in range(0, mstar + 1):
    em = e_block(m, p)
    need = target if m == mstar else e_block(m + 1, p)
    d = need - em
    base = p ** em
    xs = []
    for r in range(p):
        n = p * m + r
        if n > 0:
            fact = fact * n % MOD
        xs.append(fact)
    assert s % base == 0
    q = p ** d
    c = (s // base) % q
    ys = [(x // base) % q for x in xs]
    allowed = list(range(p))
    forced = []
    if m == 0:           # a = 1: 1 in A, 0 not in A
        allowed = list(range(2, p))
        forced = [1]
        c = (c + ys[1]) % q
    # subset-sum DP over Z/q with back-pointers
    reach = {c: None}
    for r in allowed:
        new = dict(reach)
        for v in reach:
            w = (v + ys[r]) % q
            if w not in new:
                new[w] = (v, r)
        reach = new
    if 0 not in reach:
        raise SystemExit("FAILED at block m=%d (d=%d)" % (m, d))
    R = []
    v = 0
    while reach[v] is not None:
        v, r = reach[v]
        R.append(r)
    R = sorted(R + forced)
    for r in R:
        A.append(p * m + r)
        s = (s + xs[r]) % MOD
    assert s % (p ** need) == 0
print("constructed |A| =", len(A), "max A =", A[-1], "target valuation =", target)

# independent exact check
tot = 0
f = 1
Aset = set(A)
for n in range(0, A[-1] + 1):
    if n > 0:
        f *= n
    if n in Aset:
        tot += f
assert tot > 0
v = 0
pt = p ** target
assert tot % pt == 0, "exact check FAILED"
x = tot // pt
while x % p == 0:
    x //= p
    v += 1
print("exact v_p(sum) = %d >= %d : OK  (min A = %d)" % (target + v, target, A[0]))
if out:
    with open(out, "w") as fh:
        fh.write("# p=%d L=%d witness for f(1,p) >= %d ; exact v_p(sum)=%d\n" % (p, L, target, target + v))
        fh.write(" ".join(map(str, A)) + "\n")
