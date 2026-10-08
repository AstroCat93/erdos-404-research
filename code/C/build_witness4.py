"""Witness builder for a = 1 with a 3-block 'flex' window at deep gates (levels L..J2):
blocks M-1 (any subset meeting its own mod-p condition; alternatives tried in turn),
then the exact 2-block MITM on (M, M+1) where M+1 is the gate.  Gates of level < L use the
single-block E-coverage; non-gates use Cauchy-Davenport.  Unit-part bookkeeping as in
build_witness3.py.  Independent final check from a plain running factorial mod p^target.
usage: python3 build_witness4.py p L J2 [outfile]
"""
import sys
from itertools import combinations
from core import e_block, vp

p, L, J2 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
out = sys.argv[4] if len(sys.argv) > 4 else None
Mstar = p ** (J2 + 1) - 1
target = e_block(Mstar, p) + L
T = target + 2
MOD = p ** T
ustate = [1, 0]


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


def all_subsets_hitting(vals, q, start):
    """all subsets R of range(p) with start + sum vals[R] == 0 mod q (generator)."""
    for k in range(p + 1):
        for R in combinations(range(p), k):
            if (start + sum(vals[r] for r in R)) % q == 0:
                yield R


A = []
c = 0
M = 0
retries = 0
while M <= Mstar:
    jg = vp(M + 3, p) if M + 2 < Mstar else 0   # is block M+2 a deep gate?
    if M >= 1 and L <= jg <= J2:
        # flex window: blocks M (alternatives), M+1, M+2 (gate of level jg)
        u0 = block_units(M); u1 = block_units(M + 1); u2 = block_units(M + 2)
        q = p ** (jg + 2)
        S2 = sums_mod([(p * x) % q for x in u2], q, range(p), 0)
        done = False
        for R0 in all_subsets_hitting([x % p for x in u0], p, c % p):
            tot0 = c + sum(u0[r] for r in R0)
            c1 = (tot0 // p) % MOD
            S1 = sums_mod([x % q for x in u1], q, range(p), c1)
            for v, R1 in S1.items():
                w = (-v) % q
                if w in S2:
                    R2 = S2[w]
                    tot = c1 + sum(u1[r] for r in R1) + p * sum(u2[r] for r in R2)
                    assert tot % q == 0
                    c = (tot // q) % MOD
                    A += [p * M + r for r in R0] + [p * (M + 1) + r for r in sorted(R1)] + [p * (M + 2) + r for r in sorted(R2)]
                    done = True
                    break
            if done:
                break
            retries += 1
        if not done:
            raise SystemExit("FAILED flex window at M=%d (gate level %d)" % (M, jg))
        M += 3
        continue
    u = block_units(M)
    d = L if M == Mstar else e_block(M + 1, p) - e_block(M, p)
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

print("p=%d L=%d J2=%d: |A|=%d max A=%d target=%d (flex retries=%d)" % (p, L, J2, len(A), A[-1], target, retries), flush=True)
Aset = set(A)
assert A[0] == 1 and len(Aset) == len(A) and A == sorted(A)
PT = p ** target
f, tot = 1, 0
for n in range(1, A[-1] + 1):
    f = f * n % PT
    if n in Aset:
        tot += f
print("independent check: sum_{n in A} n! == 0 mod p^%d : %s" % (target, tot % PT == 0))
if out:
    with open(out, "w") as fh:
        fh.write("# a=1 p=%d : sum_{n in A} n! == 0 mod p^%d\n" % (p, target))
        fh.write(" ".join(map(str, A)) + "\n")
