from core import *
from collections import Counter
for p,Hs,big in ((11,33,vfact(11**7-1,11)),(13,39,vfact(13**8-1,13)),(7,35,vfact(7**7-1,7)),(5,25,vfact(5**5-1,5))):
    early=Counter(); deep=0; blocked=0
    for a in range(1,1001):
        if (a+1)%p==0: blocked+=1
        K0=vfact(a+Hs,p)-vfact(a,p)
        g=g_exact(a,p,K0)
        if g<K0: early[g]+=1
        else: deep+=1
    print("p=%d H*=%d: blocked(a=-1 mod p)=%d, early-failure g-values %s, deep (=> f>=%d) %d"%(p,Hs,blocked,dict(early),big,deep))
