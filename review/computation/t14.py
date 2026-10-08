# bonus probe: Cov(5,5,H), H=31..40, on a few classes K' (a single failing class refutes Cov(5,5,H))
from cov import ys, cover
from core import vfact
import random
random.seed(3)
for H in range(31,41):
    c=vfact(H-1,5); res=[]
    Ks=[1,2,3,4]+random.sample([k for k in range(5,5**c) if k%5],4)
    for K in Ks:
        M,x=ys(5,5,H,K); res.append((K,cover(M,x)))
    print("H=%d c=%d mod 5^%d: (K',missing) %s"%(H,c,5+c,res),flush=True)
