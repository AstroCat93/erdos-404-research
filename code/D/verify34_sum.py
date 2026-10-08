#!/usr/bin/env python3
# Independent (sum-form) exact check of f(34,2) = 18444: is 2^K | sum of distinct factorials with min 34?
import time
from sumdp_check import reachable
for K in (18444, 18445):
    t0 = time.time()
    print(f"a=34 K={K} reachable={reachable(34, 2, K)} time={time.time()-t0:.1f}s", flush=True)
