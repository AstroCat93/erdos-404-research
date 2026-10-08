from cov import ys, cover
from core import vfact
for H in range(36,43):
    c=vfact(H-1,7)
    r=[(K,cover(*ys(7,7,H,K))) for K in (1,2)]
    print("t=7 H=%d c=%d mod 7^%d: (K'',missing) %s"%(H,c,7+c,r),flush=True)
    if all(m==0 for _,m in r): break
