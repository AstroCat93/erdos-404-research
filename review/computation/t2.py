from core import *
import time
t=time.time()
print("g2(0) via a=2^400:", g_exact(2**400,2,600))
for k in range(3,14):
    print("g2(2^%d)="%k, g_exact(2**k,2,2000))
print("g2(254)=",g_exact(254,2,2000))
g=g_exact(34,2,18500); print("f(34,2)=",vfact(34,2)+g, time.time()-t)
