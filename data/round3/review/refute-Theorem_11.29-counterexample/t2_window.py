# Exact test of the window identity (11.4) (both unweighted and rho-weighted) on random atoms.
import random, time, sys
from fractions import Fraction
from common import *
rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 11)
maxD=int(sys.argv[2]) if len(sys.argv)>2 else 12
def children(xp, e_bits, n, N):
    pi,dpi=pis(xp,N)
    Vs=[0]
    for j in range(1,N+1): Vs.append(Vs[-1]+v(xp+j))
    S=sum(b*pi[j] for j,b in enumerate(e_bits))%MOD
    dS=sum(b*dpi[j] for j,b in enumerate(e_bits))%MOD
    assert v(S)>=Vs[n]
    cur=[(S,dS)]
    for j in range(n,N):
        nxt=[]
        for S1,d1 in cur:
            for f in (0,1):
                S2=(S1+f*pi[j])%MOD
                if v(S2)>=Vs[j+1]: nxt.append((S2,(d1+f*dpi[j])%MOD))
        cur=nxt
    return cur
tested=0; t0=time.time(); maxdev=0
CL=sys.argv[3].split(",") if len(sys.argv)>3 else ["C0","C2","C6"]
NLO,NHI=(int(sys.argv[4]),int(sys.argv[5])) if len(sys.argv)>5 else (19,30)
NAT=int(sys.argv[6]) if len(sys.argv)>6 else 25
for cls in CL:
    k,r0,L,l0,sL,EC,Vc=CLASSES[cls]
    done=0; tries=0
    while done<NAT and tries<20000:
        tries+=1
        x=rand_in_class(cls,rng)
        n=rng.randint(NLO,NHI); N=n+l0
        m=V(x,n); MN=Mx(x,N)
        if not (2*MN+3*L+3<=m): continue
        D=V(x,N)-m
        if D>maxD: continue
        x0=x%(1<<m)
        ps,Vs=alive_paths(x,n)
        if not ps: continue
        Wn=n-m; WN=N-(m+D)
        for bits,S,dS in ps:
            r,lam=rho(x,n,S,dS)
            assert lam<=L
            cnt=0; wsum=Fraction(0)
            for w in range(1<<D):
                xp=(x0+(w<<m))%MOD
                ch=children(xp,bits,n,N)
                cnt+=len(ch)
                for S2,d2 in ch:
                    assert v(d2)==lam, "child slope differs"
                    r2,l2=rho(xp,N,S2,d2); wsum+=r2
            lhs1=Fraction(cnt,1<<D); lhs2=wsum/(1<<D)
            rhs=Fraction(2)**(WN-Wn)*r
            if lhs1!=rhs or lhs2!=rhs:
                print("MISMATCH",cls,hex(x%(1<<64)),n,bits,lam,lhs1,lhs2,rhs); sys.exit(1)
            tested+=1
        done+=1
    print(cls,"atoms",done,"tries",tries)
print("paths tested",tested,"all exact equalities hold; time %.1fs"%(time.time()-t0))
