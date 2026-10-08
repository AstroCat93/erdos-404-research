"""Faster constructive witness for Theorem C + two-block windows (a = 1), using unit parts.

For n in block m (pm <= n < pm+p): n! = p^{e_m} * u(n), u(n) = n!/p^{v_p(n!)} a unit.
Carry c_m = (sum_{n in A, n < pm} n!) / p^{e_m}.  Block step: c_{m+1} = (c_m + sum_R u)/p^{d_m}.
Two-block window at (m, m+1) with m+1 a gate of level j in [L, J2]:
   c_m + sum_{R1} u(pm+r) + p * sum_{R2} u(p(m+1)+r) == 0 mod p^{j+2}.
Final step at M* = p^{J2+1}-1: single block to precision L.
Independent final check: sum_{n in A} n! mod p^target recomputed from a plain running factorial.
usage: python3 build_witness3.py p L J2 [outfile]
"""
import sys
from core import e_block, vp

p, L, J2 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
out = sys.argv[4] if len(sys.argv) > 4 else None
Mstar = p ** (J2 + 1) - 1
target = e_block(Mstar, p) + L
T = target + 2
MOD = p ** T

ustate = [1, 0]  # u(n) mod p^T for n = ustate[1]


def block_units(M):
    u, n = ustate
    res = []
    for r in range(p):
        N = p * M + r
        while n < N:
            n += 1
            k = n
            while k % p == 0:
                k //= p
            u = u * k % MOD
        res.append(u)
    ustate[0], ustate[1] = u, n
    return res


def sums_mod(vals, q, allowed, start):
    reach = {start % q: ()}
    for r in allowed:
        new = dict(reach)
        for v, R in reach.items():
            w = (v + vals[r]) % q
            if w not in new:
                new[w] = R + (r,)
        reach = new
    return reach


A = []
c = 0
M = 0
while M <= Mstar:
    jn = vp(M + 2, p) if M + 1 < Mstar else 0
    if M >= 1 and L <= jn <= J2:
        q = p ** (jn + 2)
        u1 = block_units(M); u2 = block_units(M + 1)
        S1 = sums_mod([x % q for x in u1], q, range(p), c)
        S2 = sums_mod([(p * x) % q for x in u2], q, range(p), 0)
        found = None
        for v, R1 in S1.items():
            if (-v) % q in S2:
                found = (R1, S2[(-v) % q]); break
        if found is None:
            raise SystemExit("FAILED window at M=%d level %d" % (M, jn))
        tot = c + sum(u1[r] for r in found[0]) + p * sum(u2[r] for r in found[1])
        d = jn + 2
        assert tot % (p ** d) == 0
        c = (tot // p ** d) % MOD
        A += [p * M + r for r in sorted(found[0])] + [p * (M + 1) + r for r in sorted(found[1])]
        M += 2
        continue
    u = block_units(M)
    if M == Mstar:
        d = L
    else:
        d = e_block(M + 1, p) - e_block(M, p)
    q = p ** d
    if M == 0:
        reach = sums_mod([x % q for x in u], q, range(2, p), c + u[1]); forced = (1,)
    else:
        reach = sums_mod([x % q for x in u], q, range(p), c); forced = ()
    if 0 not in reach:
        raise SystemExit("FAILED block M=%d d=%d" % (M, d))
    R = sorted(reach[0] + forced)
    tot = c + sum(u[r] for r in R)
    assert tot % q == 0
    c = (tot // q) % MOD
    A += [p * M + r for r in R]
    M += 1

print("p=%d L=%d J2=%d: |A|=%d max A=%d target=%d" % (p, L, J2, len(A), A[-1], target), flush=True)
Aset = set(A)
assert A[0] == 1 and len(Aset) == len(A)
PT = p ** target
f, tot = 1, 0
for n in range(1, A[-1] + 1):
    f = f * n % PT
    if n in Aset:
        tot += f
print("independent check: sum_{n in A} n! == 0 mod p^%d : %s" % (target, tot % PT == 0))
if out:
    with open(out, "w") as fh:
        fh.write("# a=1 p=%d : sum_{n in A} n! == 0 mod p^%d (L=%d; two-block windows for gate levels %d..%d)\n" % (p, target, L, L, J2))
        fh.write(" ".join(map(str, A)) + "\n")
