import random, time
from common import *
rng = random.Random(1)
t=time.time()
for k in range(1,9):
    cnt=0
    for r in range(1<<k):
        x = (r + (rng.getrandbits(200)<<k)) % MOD
        cnt += g_at_least(x,k)
    print(k,cnt)
# census delta_G for G=32 by Monte Carlo
N=4000; c=0
for _ in range(N):
    x=rng.getrandbits(P); c+=g_at_least(x,32)
print("delta_32 MC", c/N, "(note: 0.1016)")
# check alive_paths count consistency with g_at_least-like set
x=rand_in_class("C2",rng)
ps,Vs=alive_paths(x,25)
print("alive at 25:",len(ps),"V25",Vs[25])
print("time",time.time()-t)
