# exact min(g_2(x), CAP) for a 2-adic integer x given mod 2^B (B >= CAP + 64 suffices if no valuation >= 64 occurs),
# carry recursion with deduplication (same algorithm as T4's p2add.c, independently written in Python).
import random, sys
def v2(z): return (z & -z).bit_length()-1
def gcap(x, CAP):
    # state: carries c = S_n / 2^{V_n} mod 2^r, r = CAP - V_n ; omega = pi_n/2^{V_n} mod 2^r
    r=CAP; cs={0}; om=1; n=0; V=0; first=True
    while True:
        m=x+n+1; t=v2(m) if m else 10**9
        mask=(1<<r)-1
        es=(1,) if first else (0,1)
        if t>=r:
            best=-1
            for c in cs:
                for e in es:
                    y=(c+e*om)&mask
                    if y==0: return CAP
                    best=max(best,v2(y))
            return V+best
        new=set(); best=-1
        for c in cs:
            for e in es:
                y=(c+e*om)&mask
                vy=v2(y) if y else r
                if vy<t: best=max(best,vy); continue
                new.add(y>>t)
        if not new: return V+best
        r-=t; om=(om*(m>>t))&((1<<r)-1); cs=new; V+=t; n+=1; first=False
if __name__=='__main__':
    seed,S,CAP=map(int,sys.argv[1:4]); random.seed(seed)
    from collections import Counter
    tot=Counter(); byc=Counter()
    for s in range(S):
        x=random.getrandbits(CAP+128)&~1
        g=gcap(x,CAP)
        cls = '0mod8' if x%8==0 else '4mod8' if x%8==4 else '2mod8' if x%8==2 else '6mod16' if x%16==6 else '14mod16'
        for G in (16,32,64,128,256,512):
            if G<=CAP and g>=G: byc[(cls,G)]+=1; tot[G]+=1
    for G in (16,32,64,128,256,512):
        if G>CAP: continue
        print(G,'delta=%.5f'%(tot[G]/S),' '.join('%s:%.3f'%(c,byc[(c,G)]/max(tot[G],1)) for c in ('0mod8','2mod8','6mod16','14mod16','4mod8')))
