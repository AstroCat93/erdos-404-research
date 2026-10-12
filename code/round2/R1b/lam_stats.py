import random, sys
sys.path.insert(0,'.')
from mart_check import alive, V, mu, v2
rnd = random.Random(int(sys.argv[1])); n=int(sys.argv[2]); T=int(sys.argv[3]); P=400
from collections import Counter
cnt=Counter(); cntrel=Counter(); nonempty=0
for t in range(T):
    x = rnd.getrandbits(P) & ~1
    pops = alive(x, n, P)
    if pops: nonempty+=1
    m=mu(x,n)
    for tau,sp,prec in pops:
        l=v2(sp); cnt[min(l,60)]+=1; cntrel[min(l,60)-m]+=1
print("n",n,"nonempty",nonempty,"/",T)
print("lambda hist", sorted(cnt.items()))
print("lambda-mu hist", sorted(cntrel.items()))
