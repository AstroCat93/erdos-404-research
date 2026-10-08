# bonus: position-specific depth-7 coverage at p=11: N* = 11^7 K'', K''=1..10
from cov import ys, cover
from core import vfact
H0=None
for H in range(34,45):
    c=vfact(H-1,11); m=cover(*ys(11,7,H,1))
    print("p=11 t=7 H=%d c=%d K''=1 missing=%d"%(H,c,m),flush=True)
    if m==0: H0=H; break
if H0:
    r=[(K,cover(*ys(11,7,H0,K))) for K in range(2,11)]
    print("H=%d K''=2..10:"%H0,r,flush=True)
    print("v11((11^8-1)!)=",vfact(11**8-1,11))
