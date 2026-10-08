# End-to-end test of Thm 3.12(b) dichotomy using Cov certificates for p=5 (T=4,H*=25) and p=7 (T=3,H*=19)
from core import *
import random, sys
random.seed(1)
p,T,Hs,amax=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
big=vfact(p**(T+1)-1,p)
early=0; deep_ok=0; deep_inconcl=[]
for a in range(1,amax+1):
    K0=vfact(a+Hs,p)-vfact(a,p)
    g=g_exact(a,p,K0)
    if g<K0: early+=1; continue
    r=g_exact(a,p,big-vfact(a,p),maxstates=(p,4,2))
    if r>=big-vfact(a,p): deep_ok+=1
    else: deep_inconcl.append((a,r))
print("p=%d: a<=%d early-failure %d, deep (f>=%d certified by sampled DP) %d, inconclusive %s"%(p,amax,early,big,deep_ok,deep_inconcl))
