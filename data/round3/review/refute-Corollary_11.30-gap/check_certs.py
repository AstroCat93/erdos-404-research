# Independent checks for Prop 11.25 finite cases, Cor 3.7.1(iii) mod 16, and random slope tests.
from fractions import Fraction as F
import itertools, random
def v2(q):
    q=F(q)
    if q==0: return 10**9
    a,b=q.numerator,q.denominator; c=0
    while a%2==0: a//=2; c+=1
    while b%2==0: b//=2; c-=1
    return c
def pi(k,x):
    r=1
    for i in range(1,k+1): r*=(x+i)
    return r
# (a) S_e(-4)
print("S(-4):",[(e,1-3*e[0]+6*e[1]-6*e[2]) for e in itertools.product([0,1],repeat=3)])
def Phi(y,e2,e3,rest,yv):
    # Phi_e(y)=e2-1/(1-y)+sum_{k>=1} e_{k+2} pi_k(y), rest = e4,e5,...
    s=F(e2)-F(1,1-yv)+e3*pi(1,yv)
    for j,b in enumerate(rest): s+=b*pi(j+2,yv)
    return s
for e2,e3 in [(1,0),(0,1)]:
    vals=[v2(Phi(None,e2,e3,r,-4)) for r in itertools.product([0,1],repeat=4)]
    print("Phi(-4) e2,e3=",e2,e3,"max val",max(vals))
hist={}
for r in itertools.product([0,1],repeat=8):
    q=Phi(None,0,1,r,-8); assert q!=0
    hist[v2(q)]=hist.get(v2(q),0)+1
print("Phi(-8) e2=0,e3=1 hist over e4..e11 (256, entries>=e10 vanish):",sorted(hist.items()))
# identity check S_e(x)=y(y-1)Phi_e(y), e1=1
for _ in range(200):
    n=random.randint(3,12); e=[1,1]+[random.randint(0,1) for _ in range(n-2)]
    x=random.randint(-50,50)*2
    if x in range(-n-2,0): continue
    S=sum(e[j]*pi(j,x) for j in range(n)); y=x+2
    if y==1: continue
    assert S==y*(y-1)*Phi(None,e[2],e[3] if n>3 else 0,e[4:],y) if n>3 else True
print("identity ok")
# Cor 3.7.1 mod 16: classes c mod 16 with g>=4
good=[]
for c in range(16):
    terms=[pi(b,c)%16 for b in range(1,16)]
    reach={1%16}
    for t in terms: reach|={(r+t)%16 for r in reach}
    if 0 in reach: good.append(c)
print("g>=4 classes mod16:",good)
