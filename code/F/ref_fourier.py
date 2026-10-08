# brute-force reference: distribution of sum_{n>=N} eps_n n!/p^e(N) mod p^s via exact enumeration, then DFT
import sys, itertools, cmath, math
def vp(n,p):
    v=0
    while n%p==0: n//=p; v+=1
    return v
def run(p,N,S):
    e=sum(vp(k,p) for k in range(1,N+1))
    fac=math.factorial(N)
    out=[]
    for s in range(1,S+1):
        M=p**s
        ws=[]; n=N; f=fac
        while vp(f,p)-e < s:
            ws.append((f//p**e)%M); n+=1; f*=n
        dist={0:1.0}
        for w in ws:
            nd={}
            for r,pr in dist.items():
                for t in (r,(r+w)%M):
                    nd[t]=nd.get(t,0)+pr/2
            dist=nd
        T=Q=0
        for u in range(1,M):
            if u%p==0: continue
            c=sum(pr*cmath.exp(2j*math.pi*u*r/M) for r,pr in dist.items())
            T+=abs(c); Q+=abs(c)**2
        out.append((s,len(ws),T,Q))
    return out
p,N,S=map(int,sys.argv[1:4])
for row in run(p,N,S): print(row)
