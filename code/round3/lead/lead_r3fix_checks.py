# Lead's own re-derivations for the round-3 referee fixes (written from the note's definitions).
from fractions import Fraction
from math import factorial, log
import mpmath as mp
mp.mp.dps=40
def v(n,p):
    if n==0: return 10**9
    k=0
    while n%p==0: n//=p;k+=1
    return k
# (1) theta_3 closed form
t3=mp.mpf(4)/9*(mp.log(mp.mpf(33)/32,3)+mp.mpf(7)/4-2*mp.log(2,3))
print("theta_3 =",mp.nstr(t3,15))
# direct truncated sum from the definition
def Gam3(j):
    # Gamma_3(j)=3^j P(W==0 mod 3^j)-1, W=sum eta_u e_u, e=(2,-2,1)  ((-1)^u 2!/u!)
    from itertools import product
    e=[2,-2,1]; pr={-1:Fraction(1,4),0:Fraction(1,2),1:Fraction(1,4)}
    P=Fraction(0)
    for s in product([-1,0,1],repeat=3):
        W=sum(a*b for a,b in zip(s,e))
        if W%3**j==0:
            q=Fraction(1)
            for a in s:q*=pr[a]
            P+=q
    return 3**j*P-1
print("Gamma_3(1..4)=",[Gam3(j) for j in range(1,5)])
S=mp.mpf(0)
for j in range(0,200):
    S+=(mp.mpf(2)/3)*mp.mpf(3)**(-j)*mp.log(1+mp.mpf(Gam3(min(j+1,6)) if j+1<=6 else (mp.mpf(3)/16)*3**(j+1)-1+1-1),3) if False else 0
# simpler: closed form for j+1>=J0=2
S=(mp.mpf(2)/3)*mp.log(1+mp.mpf(Gam3(1).numerator)/Gam3(1).denominator,3)
for j in range(1,400):
    g=mp.mpf(3)/16*mp.mpf(3)**(j+1)-1
    S+=(mp.mpf(2)/3)*mp.mpf(3)**(-j)*mp.log(1+g,3)
print("theta_3 direct =",mp.nstr(mp.mpf(2)/3*S,15), " check Gamma_3(2..4) vs closed:",[Gam3(j)==Fraction(3,16)*3**j-1 for j in (2,3,4)])
print("log2(3)/4 =",mp.nstr(mp.log(3,2)/4,12))
# (2) Theorem 11.45 'Consequence' counterexample
def y(i,p,t,H,K):
    X=p**t*K; r=1
    for s in range(1,i+1): r*=X-(H-s)
    return r
for (p,t) in [(3,3),(5,3),(7,3),(3,4),(3,5)]:
    H=p**(t-1); c=v(factorial(H-1),p); M=t+c
    hits=[]
    for K in range(1,p**2):
        if K%p==0: continue
        for i in range(1,H):
            if (y(i,p,t,H,K)-factorial(i))%p**M==0: hits.append((K,i))
    print(f"p={p} t={t} H={H} c={c} M={M}: #(K',i) with y_i==i! mod p^M: {len(hits)}; first: {hits[:8]}")
print("v3(y_8-8!) at K'=1,2,4,5:",[v(y(8,3,3,9,K)-factorial(8),3) for K in (1,2,4,5)])
# (3) density fractions
for (num,p,G) in [(25468861,5,11),(25177371,7,9)]:
    d=Fraction(num,p**G); print(p,G,mp.nstr(mp.mpf(d.numerator)/d.denominator,12),"1-d=",mp.nstr(1-mp.mpf(d.numerator)/d.denominator,12))
