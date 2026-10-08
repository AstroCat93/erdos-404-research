"""Constructive check of Theorem C' (single-block E-coverage for gate levels < L, two-block Tao
windows for gate levels L..J2) for a = 1.

Blocks M = 0..M*-1 with M* = p^(J2+1) - 1; at M* single block to valuation e_{M*} + L.
 - block M+1 a gate of level j in [L, J2]: choose blocks M, M+1 jointly (meet in the middle)
   so that the partial sum is 0 mod p^{e_{M+2}};
 - otherwise single block (Cauchy-Davenport / E-coverage).
Raises if any step is impossible (would contradict the computer-verified coverage claims).
Final check: sum_{n in A} n! == 0 mod p^{target}, with n! computed exactly mod p^{target+1}.

usage: python3 build_witness2.py p L J2 [outfile]
"""
import sys
from core import e_block, vp

p, L, J2 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
out = sys.argv[4] if len(sys.argv) > 4 else None
Mstar = p ** (J2 + 1) - 1
target = e_block(Mstar, p) + L
T = target + 1
MOD = p ** T

# running factorial mod p^T, generated block by block
fact_state = [1, 0]  # (n! mod MOD for n = fact_state[1])


def block_facts(M):
    """return [ (pM+r)! mod MOD for r in 0..p-1 ], advancing the running factorial."""
    f, n = fact_state
    res = []
    for r in range(p):
        N = p * M + r
        while n < N:
            n += 1
            f = f * n % MOD
        res.append(f)
    fact_state[0], fact_state[1] = f, n
    return res


def subset_sums(vals, q, allowed, forced_sum=0):
    """dict residue -> list of chosen indices (one representative) for subsets of `allowed`."""
    reach = {forced_sum % q: ()}
    for r in allowed:
        new = dict(reach)
        for v, R in reach.items():
            w = (v + vals[r]) % q
            if w not in new:
                new[w] = R + (r,)
        reach = new
    return reach


A = []
s = 0
M = 0
while M <= Mstar:
    em = e_block(M, p)
    base = p ** em
    assert s % base == 0
    nxt = M + 1
    jn = vp(nxt + 1, p) if nxt <= Mstar else 0
    if M >= 1 and nxt < Mstar and L <= jn <= J2:
        # two-block window: blocks M (non-gate) and M+1 (gate of level jn)
        need = e_block(M + 2, p)
        D = need - em
        q = p ** D
        x1 = block_facts(M)
        x2 = block_facts(M + 1)
        c = (s // base) % q
        y1 = [(x // base) % q for x in x1]
        y2 = [(x // base) % q for x in x2]
        S2 = subset_sums(y2, q, range(p))
        found = None
        S1 = subset_sums(y1, q, range(p), forced_sum=c)
        for v, R1 in S1.items():
            w = (-v) % q
            if w in S2:
                found = (R1, S2[w])
                break
        if found is None:
            raise SystemExit("FAILED two-block window at M=%d (gate level %d)" % (M, jn))
        for r in sorted(found[0]):
            A.append(p * M + r); s = (s + x1[r]) % MOD
        for r in sorted(found[1]):
            A.append(p * (M + 1) + r); s = (s + x2[r]) % MOD
        assert s % (p ** need) == 0
        M += 2
        continue
    need = target if M == Mstar else e_block(M + 1, p)
    D = need - em
    q = p ** D
    xs = block_facts(M)
    c = (s // base) % q
    ys = [(x // base) % q for x in xs]
    if M == 0:
        reach = subset_sums(ys, q, range(2, p), forced_sum=c + ys[1])
        forced = (1,)
    else:
        reach = subset_sums(ys, q, range(p), forced_sum=c)
        forced = ()
    if 0 not in reach:
        raise SystemExit("FAILED single block at M=%d (d=%d)" % (M, D))
    for r in sorted(reach[0] + forced):
        A.append(p * M + r); s = (s + xs[r]) % MOD
    assert s % (p ** need) == 0
    M += 1

print("p=%d L=%d J2=%d: constructed |A|=%d, max A=%d, min A=%d, target=%d" % (p, L, J2, len(A), A[-1], A[0], target))
# independent re-check: recompute n! mod p^T from scratch and sum over A
Aset = set(A)
f, tot = 1, 0
for n in range(0, A[-1] + 1):
    if n:
        f = f * n % MOD
    if n in Aset:
        tot = (tot + f) % MOD
assert A[0] == 1 and len(Aset) == len(A)
print("re-check: sum == 0 mod p^%d : %s" % (target, tot % (p ** target) == 0))
if out:
    with open(out, "w") as fh:
        fh.write("# a=1 p=%d : sum_{n in A} n! == 0 mod p^%d  (L=%d, two-block windows for levels %d..%d)\n" % (p, target, L, L, J2))
        fh.write(" ".join(map(str, A)) + "\n")
