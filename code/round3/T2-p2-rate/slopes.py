# explore slopes of alive paths for random even x (B-bit truncation), BFS over paths
import random, sys
B=400; MOD=1<<B
def v2(z):
    z%=MOD
    if z==0: return B
    return (z & -z).bit_length()-1
def run(x,nmax,cap=200000):
    # state per path: S, S' at x mod 2^B ; pi_n, pi_n'
    pops=[(1,0)]  # e_0=1: S=1, S'=0
    pi=1; dpi=0; V=0
    out=[]
    for n in range(1,nmax+1):
        # extend paths with e_{n-1}? convention: path length n uses pi_0..pi_{n-1}; we already have pi_{n-1}
        # current pi corresponds to pi_{n-1}; after adding choose e_{n-1}
        if n==1:
            newp=[(1,0)]
        else:
            newp=[]
            for (S,Sd) in pops:
                newp.append((S,Sd)); newp.append(((S+pi)%MOD,(Sd+dpi)%MOD))
        # advance pi to pi_n
        dpi=(dpi*(x+n)+pi)%MOD; pi=(pi*(x+n))%MOD
        V+=v2(x+n)
        pops=[(S,Sd) for (S,Sd) in newp if v2(S)>=V]
        if len(pops)>cap: return out,'cap'
        out.append((n,V,len(pops),sorted(v2(Sd) for S,Sd in pops)))
        if not pops: break
    return out,'ok'
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
cls=sys.argv[2] if len(sys.argv)>2 else 'all'
nmax=int(sys.argv[3]) if len(sys.argv)>3 else 60
cnt=0
for trial in range(4000):
    x=random.getrandbits(B)&~1
    if cls=='0mod8' and x%8: continue
    if cls=='2mod4' and x%4!=2: continue
    out,st=run(x,nmax)
    last=out[-1]
    if last[0]==nmax and last[2]>0:
        cnt+=1
        vx=[v2(x+i) for i in range(1,nmax+1)]
        print('x%64=',x%64,'v(x+2)=',v2(x+2),'M=',max(vx),'argmax',vx.index(max(vx))+1,'pop',last[2],'slopes',sorted(set(last[3]))[:12], 'st',st)
    if cnt>=25: break
