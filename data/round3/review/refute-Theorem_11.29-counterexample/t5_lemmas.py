# Random tests of Lemma 11.23(a)-(e), Lemma 10.2(a)-(d) on x in 2Z_2 (random and near negative integers).
import random, sys, time
from common import *
rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 5); t0=time.time(); nt=0
for it in range(4000):
    if it%2: x=(rng.getrandbits(P-1)<<1)%MOD
    else:
        m=2*rng.randint(1,200); x=(-m+(rng.getrandbits(P-60)<<rng.randint(1,40)))%MOD
        if x%2: continue
    nmax=rng.randint(4,300)
    Vs=[0]; Ms=[0]
    for i in range(1,nmax+1):
        Vs.append(Vs[-1]+v(x+i)); Ms.append(max(Ms[-1],v(x+i)))
    for n in range(1,nmax+1):
        assert Vs[n]>=n-s(n)                     # 10.2(a)
        assert Vs[n]<=n+Ms[n]                    # 10.2(b)
        if n>=4: assert Vs[n]>=Ms[n]+1           # 11.23(b)
    for n in range(1,nmax):
        for N in range(n+1,min(nmax,n+40)+1):
            D=Vs[N]-Vs[n]; assert D<=(N-n)+Ms[N]   # 11.23(c)
            assert D>=(N-n)//2                     # 10.2(c)
    for K in range(1,9):
        r=x%(1<<K); NK=(1<<K)-r if r else (1<<K)
        if NK+(1<<K)>nmax: continue
        for d in range(0,1<<K):
            assert (NK+d-Vs[NK+d])==(NK-Vs[NK])+s(d)   # 11.23(a)
        assert NK-Vs[NK]<=1-s(r)                        # 10.2(d)
    nt+=1
print("lemma tests passed on",nt,"points; %.1fs"%(time.time()-t0))
# 11.23(e): constancy of P_n, W_n on cylinders x+2^{V_n} Z_2
for it in range(300):
    x=(rng.getrandbits(P-1)<<1)%MOD; n=rng.randint(4,22)
    ps,Vs=alive_paths(x,n); m=Vs[n]
    y=(x+(rng.getrandbits(200)<<m))%MOD
    ps2,Vs2=alive_paths(y,n)
    assert Vs2[n]==m and sorted(b for b,_,_ in ps)==sorted(b for b,_,_ in ps2)
print("11.23(e) cylinder constancy ok")
