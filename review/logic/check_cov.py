import sys,time,math
def vfact(n,p):
    s=0
    while n: n//=p; s+=n
    return s
def cov(p,t,H,stop_on_fail=True):
    c=vfact(H-1,p); M=p**(t+c); mask=(1<<M)-1; pc=p**c
    fails=[]
    for K in range(pc if c>0 else 1):
        if c>0 and K%p==0: continue
        X=p**t*K
        s=1; y=1
        for i in range(H):
            if i>0: y=y*(X-(H-i))%M
            t_=y%M
            if t_: s|=((s<<t_)|(s>>(M-t_)))&mask
            if s==mask: break
        if s!=mask:
            fails.append(K)
            if stop_on_fail: break
    return c,M,fails
jobs=[(5,1,3),(5,2,10),(5,3,20),(5,4,25),(7,1,4),(7,2,7),(7,3,19),(7,4,26),(7,5,28),
      (11,1,5),(11,2,10),(11,3,18),(11,4,22),(11,5,30),(13,1,6),(13,2,10),(13,3,19),(13,4,24),(13,5,32)]
if len(sys.argv)>1: jobs=[tuple(map(int,a.split(','))) for a in sys.argv[1:]]
for (p,t,H) in jobs:
    t0=time.time(); c,M,f=cov(p,t,H)
    print((p,t,H),"c=",c,"H+1<p^t:",H+1<p**t,"HOLDS" if not f else "FAILS at K=%s"%f[:3],round(time.time()-t0,1),flush=True)
