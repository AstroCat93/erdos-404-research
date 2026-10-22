# max slope of alive paths vs depth t = v(x+2) for x in -2 + 2^t*odd (sanity data for Hypothesis H)
import random, sys
from check_cert import pops, v2, B
random.seed(int(sys.argv[1])); S=int(sys.argv[2]); nmax=int(sys.argv[3])
for t in range(4,13):
    mx=-1; nsurv=0; hist={}
    for s in range(S):
        u=random.getrandbits(B-t-1)*2+1
        x=(-2+(u<<t))%(1<<B)
        res,ok=pops(x,nmax,cap=200000)
        if not ok: continue
        # only times with V >= 3t+8 (slopes then reflect frozen structure)
        ms=[r[3] for r in res if r[1]>=3*t+8 and r[2]>0]
        if ms:
            nsurv+=1; m=max(ms); mx=max(mx,m); hist[m-t]=hist.get(m-t,0)+1
    print('t',t,'samples',S,'with alive paths at V>=3t+8:',nsurv,'max slope',mx,'max(slope)-t histogram',dict(sorted(hist.items())))
