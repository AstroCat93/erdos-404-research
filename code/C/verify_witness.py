"""Standalone verifier (no project imports).  usage: python3 verify_witness.py p K file
Checks: the file's integers are strictly increasing, the first is the claimed a (printed),
and p^K divides sum_{n in A} n!  (computed with exact integers modulo p^K).
Also reports the exact p-adic valuation of the sum if it is < K + 5 (computed mod p^(K+5))."""
import sys
p, K, fn = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
nums = []
for line in open(fn):
    if line.startswith("#"):
        continue
    nums += [int(x) for x in line.split()]
assert all(x < y for x, y in zip(nums, nums[1:])), "not strictly increasing"
mod = p ** (K + 5)
S, f, i = 0, 1, 0
for n in range(0, nums[-1] + 1):
    if n:
        f = f * n % mod
    if i < len(nums) and nums[i] == n:
        S = (S + f) % mod
        i += 1
PK = p ** K
if S % PK != 0:
    v = 0
    while S % p ** (v + 1) == 0:   # only reached if the claim fails; v < K
        v += 1
else:
    v, T = K, S // PK
    while v < K + 5 and T % p == 0:
        T //= p
        v += 1
print("a=%d |A|=%d max=%d : v_p(sum) %s %d  -> claim p^%d | sum is %s" % (
    nums[0], len(nums), nums[-1], ">=" if v == K + 5 else "=", v, K, v >= K))
