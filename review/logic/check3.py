import sys,time
def pi_list(x,n,M):
    out=[1%M]; r=1
    for l in range(1,n): r=r*(x+l)%M; out.append(r)
    return out
def full(p,k,N):
    M=p**k; s=1; mask=(1<<M)-1
    for t in pi_list(N,p*k+p,M):
        if t: s|= ((s<<t)|(s>>(M-t))) & mask
        if s==mask: return True
    return s==mask
p=3; surv=[N for N in range(81) if full(p,4,N)]
for k in range(5,int(sys.argv[1])+1):
    t0=time.time()
    surv=[c+j*3**(k-1) for c in surv for j in range(3) if full(p,k,c+j*3**(k-1))]
    print(k,len(surv),len(surv)/3**k,sorted(set(N%81 for N in surv)),round(time.time()-t0,1),flush=True)
