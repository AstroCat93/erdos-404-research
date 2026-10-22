# independent brute-force check of D_p(w,K) (writeup Theorem 3.1); exact subset enumeration
import sys, math, itertools
def v(a,p,K):
    a%=p**K
    if a==0: return K
    c=0
    while a%p==0: a//=p; c+=1
    return c
def D(p,w,K):
    P=w*p; M=p**K; tot=0.0
    for y in range(p**(K-1)):
        tau=p*y
        G=min(K,sum(v(tau+t,p,K) for t in range(1,P+1)))
        m=p**G
        q=[math.prod(tau+t for t in range(1,s+1))%m for s in range(P)]
        sums=set()
        for mask in range(1<<P):
            sums.add(sum(q[s] for s in range(P) if mask>>s&1)%m)
        tot+=math.log(len(sums),p)
    return (p-1)/(w*p)*tot/p**(K-1)
for a in sys.argv[1:]:
    p,w,K=map(int,a.split(','))
    print(p,w,K,"%.10f"%D(p,w,K))
