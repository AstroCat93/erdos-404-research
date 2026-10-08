import sys
sys.path.insert(0, '.')
from gref import g_capped
# a = 0 ("0!" included) and a = 2^K for several K; also a = 2^K - m
for a in [0]:
    print("a=0 g=", g_capped(0, 2, 3000)[0], flush=True)
for K in range(3, 14):
    a = 2**K
    print("a=2^%d g=%d" % (K, g_capped(a, 2, 3000)[0]), flush=True)
