#!/usr/bin/env python3
"""signed_slopes.py -- heuristic experiment (not a proof): for Haar-random y, the normalised alive mass
Lam_T(y) of the SIGNED carry process (digits -1,0,1 with weights 1/4,1/2,1/4, delta_0 = 1), split by the slope
lambda = v_p(S_delta'(y)) (bucket L+1 means slope >= L+1).  Dense numpy DP over (S mod p^V_T, S' mod p^(L+1)),
float64.  Samples with V_T(y) > 11 are skipped (memory).  usage: signed_slopes.py p T L NY SEED
"""
# heuristic: E_y[Lam_t^{(lambda)}(y)] for the signed process, by slope lambda (scratch experiment)
import numpy as np, random, sys
p=int(sys.argv[1]); T=int(sys.argv[2]); L=int(sys.argv[3]); NY=int(sys.argv[4]); seed=int(sys.argv[5])
rnd=random.Random(seed); PREC=60; MOD=p**PREC
def vp(a):
    a%=MOD
    if a==0: return PREC
    k=0
    while a%p==0: a//=p;k+=1
    return k
acc={}; cnt=0
for it in range(NY):
    y=rnd.randrange(MOD)
    V=sum(vp(y+i) for i in range(1,T+1))
    if V>11: continue
    cnt+=1
    m1=p**V; m2=p**(L+1)
    st=np.zeros((m1,m2)); st[1%m1,0]=1.0
    pc=1; dpc=0
    for c in range(1,T):
        dpc=(dpc*(y+c)+pc); pc=pc*(y+c)
        a=pc%m1; b=dpc%m2
        st=0.5*st+0.25*np.roll(np.roll(st,a,axis=0),b,axis=1)+0.25*np.roll(np.roll(st,-a,axis=0),-b,axis=1)
    row=st[0]*m1
    for s in range(m2):
        lam=0
        if s==0: lam=L+1
        else:
            t=s
            while t%p==0: t//=p; lam+=1
        acc[lam]=acc.get(lam,0)+row[s]
print(f"p={p} T={T} samples={cnt}: E[Lam_T by slope] (slope {L+1} means >={L+1}):", {k:round(v/cnt,4) for k,v in sorted(acc.items())}, "total", round(sum(acc.values())/cnt,4))
