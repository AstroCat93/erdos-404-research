#!/usr/bin/env python3
"""Independent cross-check of |S_k| = #{a in [1,2^k] : g(a,2) >= k} using the sum-form DP
(sumdp_check.reachable: partial sums of factorials mod 2^K, no c-recursion)."""
import sys
from sumdp_check import reachable, vp_fact
K = int(sys.argv[1])
cnt = 0
for a in range(1, 2 ** K + 1):
    if reachable(a, 2, vp_fact(a, 2) + K):
        cnt += 1
print(f"k={K} |S_k|={cnt} density={cnt / 2 ** K:.6f}")
