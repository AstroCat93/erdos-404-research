# Referee's independent two-block window check: gate m with m+1 = p^j t (1<=t<p), window [p(m-1), p(m+1)),
# elements n!/(p(m-1))! = prod_{s=1}^{n-A}(A+s) (unit factor dropped), demand p^(j+2).
import sys, subprocess
from core import vfact
def cover(M,xs):
    out=subprocess.run(["./rcover"],input=f"{M} {len(xs)} "+" ".join(map(str,xs)),capture_output=True,text=True).stdout
    return int(out.split()[1])
p,j=int(sys.argv[1]),int(sys.argv[2])
ts=[int(x) for x in sys.argv[3:]] or list(range(1,p))
res=[]
for t in ts:
    m=p**j*t-1; A=p*(m-1)
    D=vfact(p*(m+1),p)-vfact(A,p); assert D==j+2
    M=p**D; xs=[1]; pr=1
    for s in range(1,2*p):
        pr=pr*(A+s)%M; xs.append(pr)
    miss=cover(M,xs); res.append((t,miss))
    print("p=%d j=%d t=%d missing=%d"%(p,j,t,miss),flush=True)
print("SUMMARY p=%d j=%d: %d/%d FULL"%(p,j,sum(1 for t,mm in res if mm==0),len(res)))
