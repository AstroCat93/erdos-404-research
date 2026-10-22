# Exact check of window identity (11.4), Prop 11.25 slope bounds, and W-walk facts on random cylinders.
import random, sys
from fractions import Fraction
P=400; MOD=1<<P
def v(a):
    a%=MOD
    if a==0: return P
    return (a & -a).bit_length()-1
def alive_paths(x,n):
    # returns list of (e tuple, S mod MOD, Sprime mod MOD); DFS keeping prefixes alive at each length
    # pi_j and pi_j' as integers mod MOD
    pis=[1]; dps=[0]
    for j in range(1,n+1):
        pis.append(pis[-1]*(x+j)%MOD); dps.append((dps[-1]*(x+j)+pis[-2])%MOD)
    V=[0]*(n+1)
    for j in range(1,n+1): V[j]=V[j-1]+v(x+j)
    cur=[((1,),1,0)]
    for j in range(1,n):
        nxt=[]
        for e,S,Sp in cur:
            for b in (0,1):
                S2=(S+b*pis[j])%MOD; Sp2=(Sp+b*dps[j])%MOD
                if v(S2)>=V[j+1]: nxt.append((e+(b,),S2,Sp2))
        cur=nxt
    return cur,V,pis
def a_lam(x,n,lam):
    # distribution of sum_{i<2lam} f_i pi_{n+i}/pi_n mod 2^lam
    cnt=[0]*(1<<lam)
    q=[1]
    for i in range(1,2*lam): q.append(q[-1]*(x+n+i))
    for mask in range(1<<(2*lam)):
        s=sum(q[i] for i in range(2*lam) if mask>>i&1)
        cnt[s%(1<<lam)]+=1
    return [Fraction(c,1<<(2*lam)) for c in cnt]
def rho(x,n,e,S,Sp,pis,lam):
    if lam==0: return Fraction(1)
    tau=(-S//1)  # need tau = -S/pi_n in Z_2 mod 2^lam
    # compute -S/pi_n mod 2^lam: S and pi_n mod MOD, divide by 2^{v(pi_n)}
    m=v(pis[n]); odd=(pis[n]>>m)%MOD
    t=((-S)>>m) * pow(odd,-1,1<<lam) % (1<<lam)
    return (1<<lam)*a_lam(x,n,lam)[t]
classes={'C0':(0,3,1),'C2':(2,3,3),'C6':(6,4,6)}
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
tests=0; maxslope={}; fails=0
for name,(r0,k,L) in classes.items():
    l0=2*L+2; done=0; tries=0
    while done<int(sys.argv[2]) if len(sys.argv)>2 else 6:
        tries+=1
        n=random.randint(19,34)
        x=r0+(1<<k)*random.getrandbits(P-k)
        paths,V,pis=alive_paths(x,n)
        m=V[n]; N=n+l0
        MN=max(v(x+i) for i in range(1,N+1))
        for e,S,Sp in paths:
            maxslope[name]=max(maxslope.get(name,0),v(Sp))
            if v(Sp)>L: print("SLOPE VIOLATION",name,n,e); fails+=1
        if not (2*MN+3*L+3<=m) or not paths: continue
        Vn=m; VN=Vn+sum(v(x+i) for i in range(n+1,N+1)); D=VN-Vn
        if D>12: continue
        x0=x%(1<<m)
        WN=N-VN; Wn=n-Vn
        # LHS: exact average over w mod 2^D of #alive at N and rho-weighted
        tot=0; totw=Fraction(0)
        for w in range(1<<D):
            xp=x0+(w<<m)
            pN,VV,pisN=alive_paths(xp,N)
            assert VV[N]==VN
            tot+=len(pN)
            for e,S,Sp in pN: totw+=rho(xp,N,e,S,Sp,pisN,v(Sp))
        lhs=Fraction(tot,1<<D); lhsw=totw/(1<<D)
        rhs=Fraction(2)**(WN-Wn)*sum(rho(x,n,e,S,Sp,pis,v(Sp)) for e,S,Sp in paths)
        st="OK" if (lhs==rhs and lhsw==rhs) else "MISMATCH"
        if st!="OK": fails+=1
        print(name,"n",n,"m",m,"D",D,"|P_n|",len(paths),"E#",lhs,"Ew",lhsw,"pred",rhs,st)
        done+=1
print("maxslope",maxslope,"fails",fails)
