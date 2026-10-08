# Referee's independent Cov(p,t,H) checker.  Cov(p,t,H): for every unit K' mod p^c, c=v_p((H-1)!),
# subset sums of y_i(K') = prod_{s=1}^{i} (p^t K' - (H-s)), 0<=i<H, cover Z/p^(t+c).
import sys, subprocess
from core import vfact
def ys(p,t,H,K):
    c=vfact(H-1,p); M=p**(t+c); X=p**t*K
    out=[1%M]; pr=1
    for i in range(1,H):
        pr=pr*(X-(H-i))%M; out.append(pr)
    return M,out
def cover(M,xs):
    out=subprocess.run(["./rcover"],input=f"{M} {len(xs)} "+" ".join(map(str,xs)),capture_output=True,text=True).stdout
    return int(out.split()[1])
def classes(p,c,part=0,nparts=1):
    if c==0: return [1]
    return [K for K in range(1,p**c) if K%p and K%nparts==part]
if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="pos":   # pos p t H [part nparts]
        p,t,H=map(int,sys.argv[2:5]); part,np_=(int(sys.argv[5]),int(sys.argv[6])) if len(sys.argv)>5 else (0,1)
        c=vfact(H-1,p); bad=[]; n=0
        for K in classes(p,c,part,np_):
            M,x=ys(p,t,H,K); n+=1
            m=cover(M,x)
            if m: bad.append((K,m))
        print("Cov(%d,%d,%d) c=%d mod p^%d classes=%d failing=%s"%(p,t,H,c,t+c,n,bad[:5]),flush=True)
    elif mode=="neg": # neg p t Hmax : for each H<=Hmax report a failing class (or counting bound)
        p,t,Hmax=map(int,sys.argv[2:5])
        for H in range(1,Hmax+1):
            c=vfact(H-1,p)
            if 2**H < p**(t+c): print("H=%d fails by counting"%H); continue
            f=None
            for K in classes(p,c):
                M,x=ys(p,t,H,K)
                m=cover(M,x)
                if m: f=(K,m); break
            print("H=%d c=%d: %s"%(H,c,"FAILS at K'=%d (missing %d)"%f if f else "HOLDS (all classes covered)"),flush=True)
