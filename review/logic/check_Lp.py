import math,sys,time
def covers(p,L):
    M=p**L; mask=(1<<M)-1; s=1
    for u in range(p):
        t=((-1)**u*pow(math.factorial(u),-1,M))%M
        s|=((s<<t)|(s>>(M-t)))&mask
    return s==mask
claimed={3:1,5:1,7:2,11:2,13:2,17:3,19:3,23:4,29:5,31:5}
for p,L in claimed.items():
    t0=time.time()
    a=covers(p,L)
    b=covers(p,L+1) if p**(L+1)<3e7 else 'skip'
    print(p,L,"covers L:",a,"covers L+1:",b,round(time.time()-t0,1),flush=True)
# f(1,p) >= p+...+p^L and two-block numbers
def vfact(n,p):
    s=0
    while n: n//=p; s+=n
    return s
for p,L,J in [(17,3,6),(19,3,6),(23,4,6),(29,5,6),(31,5,6)]:
    m=p**J-1; print(p, m+vfact(m,p)+L)
print(vfact(13**8-1,13), vfact(11**7-1,11))
print(sum(37**i for i in range(1,7)), sum(53**i for i in range(1,7)))
