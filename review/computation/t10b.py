from core import *
import random, math
random.seed(5)
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
