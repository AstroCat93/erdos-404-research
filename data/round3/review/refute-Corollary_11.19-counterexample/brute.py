# brute-force oracle straight from the definition: enumerate all 2^P subsets
import sys, math
def v(x,p,K):
    if x==0: return K
    c=0
    while x%p==0: x//=p; c+=1
    return min(c,K)
def D(p,w,K):
    P=w*p; pK=p**K; tot=0.0
    for y in range(p**(K-1)):
        tau=p*y
        G=min(K,sum(v((tau+t)%pK,p,K) for t in range(1,P+1))); M=p**G
        q=[];cur=1
        for s in range(P):
            if s>0: cur*=tau+s
            q.append(cur%M)
        sums={0}
        for a in q: sums|={(x+a)%M for x in sums}
        tot+=math.log(len(sums),p)
    return (p-1)/(w*p)*tot/p**(K-1)
for arg in sys.argv[1:]:
    p,w,K=map(int,arg.split(','))
    print(p,w,K,"%.10f"%D(p,w,K))
