import sys,time
def elems(p,j,t,M):
    m=p**j*t-1; start=p*(m-1); out=[1%M]; r=1
    for n in range(start+1,p*(m+1)):
        r=r*n%M; out.append(r)
    return out
def full(vals,M):
    mask=(1<<M)-1; s=1
    for v in vals:
        if v: s|=((s<<v)|(s>>(M-v)))&mask
        if s==mask: return True
    return s==mask
for p,j in [tuple(map(int,a.split(','))) for a in sys.argv[1:]]:
    M=p**(j+2); t0=time.time()
    dep_ok=all(elems(p,j,t,M)==elems(p,j,t+p*k,M) for t in range(1,p) for k in (1,2,5))
    res=[full(elems(p,j,t,M),M) for t in range(1,p)]
    print(p,j,"depends only on t mod p:",dep_ok,"FULL",sum(res),"/",p-1,round(time.time()-t0,1),flush=True)
