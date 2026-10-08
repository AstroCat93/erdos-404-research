def pi(b,x):
    r=1
    for l in range(1,b+1): r*=(x+l)
    return r
def full(p,k,N):
    M=p**k; s=0  # bitmask
    s=1
    for j in range(0,p*k+p):
        t=pi(j,N)%M
        s|= ((s<<t)|(s>>(M-t))) & ((1<<M)-1)
    return s==(1<<M)-1
for k in [4,5,6,7]:
    M=3**k
    fl=[N for N in range(M) if full(3,k,N)]
    print(k,len(fl),sorted(set(N%81 for N in fl)))
