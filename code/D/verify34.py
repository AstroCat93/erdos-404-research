#!/usr/bin/env python3
# Exact computation of f(34,2) with the reference c-recursion (big ints), cap 18440 > 18412.
import time, sys
from gref import g_capped
from sumdp_check import vp_fact
t0 = time.time()
a = int(sys.argv[1]); cap = int(sys.argv[2])
g, _ = g_capped(a, 2, cap)
print(f"a={a} cap={cap} g={g} f={g + vp_fact(a, 2)} {'(exact)' if g < cap else '(lower bound)'} time={time.time()-t0:.1f}s", flush=True)
