# brute-force D_p(w,K) by explicit enumeration of all 2^P subset sums (tiny cases only)
import sys, math, itertools
p,w,K=map(int,sys.argv[1:4]); P=w*p; pK=p**K
def v(z):
    z%=pK
    if z==0: return K
    c=0
    while z%p==0: z//=p; c+=1
    return c
tot=0.0
for y in range(p**(K-1)):
    tau=p*y
    G=min(K,sum(v(tau+t) for t in range(1,P+1))); m=p**G
    q=[1]
    for s in range(1,P): q.append(q[-1]*(tau+s))
    sums={0}
    for x in q: sums|={(a+x)%m for a in sums}
    tot+=math.log(len(sums))/math.log(p)
print(f"p={p} w={w} K={K} D={(p-1)/(w*p)*tot/p**(K-1):.12f}")
