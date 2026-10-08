import subprocess
from core import gamma2, vp
Lp={3:1,5:1,7:2,11:2,13:2,17:3,19:3}
for p in (17,19):
    Kmax=Lp[p]+(4 if p<17 else 2)
    out=subprocess.run(["./census2",str(p),str(Kmax),"glist","1500"],capture_output=True,text=True).stdout.split("\n")
    bad=0;n=0;exact=0
    for line in out:
        if not line: continue
        a,g=map(int,line.split()); n+=1
        k=p-(a%p); m0=(a-(p-k))//p
        tau=gamma2(k,p) if k!=2 else 10**9
        if tau<=vp(m0+1,p):
            exact+=1
            if g!=tau: bad+=1; print("exact fail",p,a,g,tau)
        elif g<Lp[p]+1: bad+=1; print("lower fail",p,a,g,tau)
    print("gap theorem p=%d (C DP): %d a's (%d in exact branch), %d failures"%(p,n,exact,bad),flush=True)
