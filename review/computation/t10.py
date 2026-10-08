from core import *
import random, math
random.seed(5)
# Thm 3.7(a),(b) halving numerics
viol=0;n=0
for _ in range(3000):
    G=random.randint(2,14); x=random.randint(1,2**16)
    a=g_exact(x,2,G)>=G; b=g_exact(x+2**(G-1),2,G)>=G; n+=1
    if a!=b: viol+=1
    if G>=6 and x%4==2:
        b2=g_exact(x+2**(G-3),2,G)>=G; n+=1
        if a!=b2: viol+=1
# (b) restricted to x=2 mod 4 exhaustively for G=6..12 over x<2^G
for G in range(6,13):
    for x in range(2,2**G+2,4):
        n+=1
        if (g_exact(x,2,G)>=G)!=(g_exact(x+2**(G-3),2,G)>=G): viol+=1
print("halving tests",n,"violations",viol)
# Cor 3.7.1(iii): g_2 values for a<=3000
from collections import Counter
c=Counter(); bad=[]
for a in range(1,3001):
    g=g_exact(a,2,40); c[min(g,40)]+=1
    if g in (1,2,4,5): bad.append(a)
    if (g==0)!=(a%2==1) or (g==3)!=(a%8==4): bad.append(('iff',a))
print("p=2 a<=3000: forbidden/iff violations",bad[:10],"smallest values",sorted(c)[:6])
# Gap theorem 3.9(d) for p=5 (L=1), 7 (L=2), 11,13 (L=2)
Lp={5:1,7:2,11:2,13:2,3:1}
for p in (3,5,7,11,13):
    bad=0;cnt=0
    for a in range(1,1500):
        k=p-(a%p) # in [1,p]
        m0=(a-(p-k))//p
        assert a==p*m0+(p-k)
        tau=gamma2(k,p) if k!=2 else float('inf')
        K=Lp[p]+2+ (int(tau) if tau!=float('inf') else 0)+3
        g=g_exact(a,p,K)
        cnt+=1
        if tau<=vp(m0+1,p):
            if g!=tau: bad+=1; print("gap-thm exact fail",p,a,g,tau)
        else:
            if g<Lp[p]+1: bad+=1; print("gap-thm lower fail",p,a,g,tau)
    print("gap theorem p=%d: %d a's, %d failures"%(p,cnt,bad))
# first failures
def first_failure(a,p,Nmax):
    for N in range(a+1,Nmax):
        K=vfact(N,p)-vfact(a,p)
        if g_exact(a,p,K)<K: return N
print("first failure f(949,3):",first_failure(949,3,1100),"f(700,3):",first_failure(700,3,800), "v3(980!),v3(981!)=",vfact(980,3),vfact(981,3))
# Prop 3.14
def U(n,p): x=math.factorial(n); return x//p**vp(x,p)
def P(n,p):
    r=1
    for j in range(1,n+1):
        if j%p: r*=j
    return r
ok=True
for p in (2,3,5,7):
    for n in range(1,200): ok&= U(n,p)==P(n,p)*U(n//p,p)
    for k in (1,2,3):
        M=p**k
        eps = -1 if (p%2==1 or M==4) else 1
        for n in range(0,150): ok&= (P(n+M,p)-eps*P(n,p))%M==0
        if p%2==1:
            Pm=[1]
            for j in range(1,6*M): Pm.append(Pm[-1]*(j if j%p else 1)%M)
            per=[d for d in range(1,2*M+1) if all(Pm[n+d]==Pm[n] for n in range(0,3*M))]
            ok&= per[0]==2*M
    if p%2: 
        for j in range(0,6): ok&= (U(p**j,p)-(-1)**j)%p==0
print("Prop 3.14 checks:",ok)
# grouping identity 1.6
ok=True
for p in (2,3,5,7):
    for n in range(1,120):
        m,r=divmod(n,p)
        W=math.factorial(p*m)//(p**m*math.factorial(m))
        ok&= math.factorial(n)==p**m*math.factorial(m)*W*math.prod(p*m+j for j in range(1,r+1))
        ok&= (W-(-1)**m)%p==0 if p>2 else True
print("grouping identity:",ok)
