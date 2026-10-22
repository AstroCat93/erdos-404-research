# Independent re-check of the finite certificates of Prop 11.25 used by Thm 11.29
from fractions import Fraction as F
from itertools import product
def v2(q):
    q=F(q); 
    if q==0: return None
    a,b=q.numerator,q.denominator; c=0
    while a%2==0: a//=2;c+=1
    while b%2==0: b//=2;c-=1
    return c
def pi(k,x):
    r=1
    for i in range(1,k+1): r*=(x+i)
    return r
# (a)
va=[v2(1-3*e1+6*e2-6*e3) for e1,e2,e3 in product([0,1],repeat=3)]
print("(a) vals",[1-3*e1+6*e2-6*e3 for e1,e2,e3 in product([0,1],repeat=3)],"max v",max(va))
def Phi(e2,rest,y):  # rest = (e3,e4,...)
    s=F(e2)-F(1,1-y)
    for k,ek in enumerate(rest,1): s+=ek*pi(k,y)
    return s
print("(b) e2=1,e3=0:",[ (Phi(1,(0,a,b),-4),v2(Phi(1,(0,a,b),-4))) for a,b in product([0,1],repeat=2)])
print("(b) e2=0,e3=1:",[ (Phi(0,(1,a,b),-4),v2(Phi(0,(1,a,b),-4))) for a,b in product([0,1],repeat=2)])
from collections import Counter
h=Counter(); zero=0
for t in product([0,1],repeat=6):
    val=Phi(0,(1,)+t+(0,0,0),-8)
    if val==0: zero+=1
    else: h[v2(val)]+=1
print("(c) e2=0,e3=1 hist",dict(sorted(h.items())),"zeros",zero)
# identity check S_e(x) = y(y-1)Phi_e(y) for e1=1, random
import random
ok=True
for _ in range(2000):
    n=random.randint(4,12); e=[1,1]+[random.randint(0,1) for _ in range(n-2)]
    x=random.randint(-50,50)*2
    y=x+2
    if y in (0,1): continue
    S=sum(e[j]*pi(j,x) for j in range(n))
    ok &= (S==y*(y-1)*Phi(e[2],e[3:],y))
print("identity",ok)
