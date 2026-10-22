# Sanity checks (not proofs): (1) slope bounds per class for all alive paths, (2) Hensel first-moment bound E[Z_n 1_C].
# usage: python3 check_cert.py SEED NMAX SAMPLES
import random, sys
B=300; MOD=1<<B
def v2(z):
    z%=MOD
    return B if z==0 else (z & -z).bit_length()-1
def pops(x,nmax,cap=400000):
    """BFS over all alive paths; returns list of (n, V_n, |P_n|, max slope over P_n)."""
    P=[(1,0)]; pi=1; dpi=0; V=0; res=[]
    for n in range(1,nmax+1):
        if n>1:
            P=[q for (S,Sd) in P for q in ((S,Sd),((S+pi)%MOD,(Sd+dpi)%MOD))]
        dpi=(dpi*(x+n)+pi)%MOD; pi=(pi*(x+n))%MOD; V+=v2(x+n)
        P=[(S,Sd) for (S,Sd) in P if v2(S)>=V]
        if len(P)>cap: return res,False
        res.append((n,V,len(P),max([v2(Sd) for S,Sd in P],default=-1)))
        if not P: break
    return res,True
def main():
    random.seed(int(sys.argv[1]))
    classes={'0mod8':(0,8,1,4),'2mod8':(2,8,3,7),'6mod16':(6,16,6,11)}
    nmax=int(sys.argv[2]); S=int(sys.argv[3])
    for name,(r0,mod,L,Vmin) in classes.items():
        worst=-1; viol=0; sumZ={n:0.0 for n in (16,24,32,40) if n<=nmax}; cnt=0; overflow=0
        for s in range(S):
            x=(random.getrandbits(B)//mod)*mod+r0
            res,ok=pops(x,nmax)
            if not ok: overflow+=1; continue
            cnt+=1
            for (n,V,np_,ms) in res:
                if V>=Vmin and np_>0:
                    worst=max(worst,ms)
                    if ms>L: viol+=1
                if n in sumZ: sumZ[n]+=2.0**(V-n)*np_
        print(name,'L=',L,'samples',cnt,'overflow',overflow,'max slope seen',worst,'violations',viol,
              'E[Z_n|C]:',{n:round(v/cnt,3) for n,v in sumZ.items()})
if __name__=="__main__":
    main()
