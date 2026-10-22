# Referee: direct check of Cov(p,t,H) (definition of note §3.7) by subset-sum DP over Z/p^{t+c},
# for every unit K' mod p^c.  Used for Remark 11.49 (p=13,t=3,H=19..32) and Theorem 11.48(c) constant.
import sys, math, numpy as np
def vfact(n,p):
    s=0
    while n: n//=p; s+=n
    return s
def cov(p,t,H):
    c=vfact(H-1,p); M=t+c; m=p**M
    Ks=[K for K in range(1,p**c+1) if K%p] if c>0 else [1]
    worst=0
    for K in Ks:
        X=p**t*K
        ys=[]; y=1
        for i in range(H):
            if i>0: y=y*(X-(H-i))%m
            ys.append(y%m)
        reach=np.zeros(m,dtype=bool); reach[0]=True
        for y in ys:
            reach=reach|np.roll(reach,y)
        miss=m-int(reach.sum())
        worst=max(worst,miss)
        if miss and worst==miss: badK=K
    return c,M,len(Ks),worst
p,t=int(sys.argv[1]),int(sys.argv[2])
for H in range(int(sys.argv[3]),int(sys.argv[4])+1):
    c,M,nK,worst=cov(p,t,H)
    print(f"Cov({p},{t},{H}): c={c} M={M} units={nK} max misses={worst} -> {'HOLDS' if worst==0 else 'FAILS'}",flush=True)
