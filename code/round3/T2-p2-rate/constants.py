# Explicit constants for Theorem 7 (rate off the class 14 mod 16). Exact rational/float arithmetic of the bound terms.
import math
from fractions import Fraction
ALPHA=0.227
def H(a): return -a*math.log2(a)-(1-a)*math.log2(1-a)
assert 1-H(ALPHA) > ALPHA
classes={ 'C0=8Z2':dict(k=3,r0=0,L=1,EC=1), 'C2=2+8Z2':dict(k=3,r0=2,L=3,EC=2**3*2**(3-1+1)),
          'C6=6+16Z2':dict(k=4,r0=6,L=6,EC=2**6*2**(6-1+3)) }
def s(n): return bin(n).count('1')
def smax(L): return max(s(d) for d in range(0,2*L+2))
def h(n,L): return (n-math.log2(n)-3*L-4)/2
def Bbad(n0,L):
    l0=2*L+2; tot=0.0
    tot+=(n0+l0)*2.0**(-(math.floor(h(n0,L))+1))
    i=n0+l0+1
    while True:
        term=2.0**(-(math.floor(h(i-l0,L))+1))
        tot+=term; i+=1
        if term<1e-300 or i>n0+l0+20000: break
    return tot
def n0_of(G,L): return math.ceil(4*math.log2(G))+3*L+40
def bound(G,c):
    k,r0,L,EC=c['k'],c['r0'],c['L'],c['EC']; l0=2*L+2
    T=G//2; K=math.floor(math.log2(T-l0+1)); n0=n0_of(G,L)
    if n0+l0>T or K<=k: return None
    cc=math.floor(ALPHA*(K-k))-smax(L)+s(r0)
    walk=2.0**(-k)*2.0**(-(K-k)*(1-H(ALPHA)))
    return Bbad(n0,L)+n0*2.0**(-K)+2.0**(-cc)*EC+walk
for name,c in classes.items():
    k,r0,L,EC=c['k'],c['r0'],c['L'],c['EC']
    main=(2**(1+smax(L)-s(r0))*EC+2.0**(-k))*2**(ALPHA*k)*8**ALPHA
    side=max(G**ALPHA*(Bbad(n0_of(G,L),L)+8*n0_of(G,L)/G) for G in [2**j for j in range(10,400)])
    worst=max(bound(G,c)*G**ALPHA for G in list(range(2**10,2**14,7))+[2**j+d for j in range(14,200) for d in (0,1,3)] if bound(G,c) is not None)
    # smallest G at which the explicit bound drops below mu(C)=2^-k
    Gmin=next(G for G in (2**j for j in range(6,400)) if bound(G,c) is not None and bound(G,c)<2.0**(-k))
    print(f"{name}: L={L} E_C<= {EC}  s_max={smax(L)}  analytic C = {main:.4g} + side {side:.3g};  sup_G bound*G^a (numeric) = {worst:.4g};  bound < mu(C) from G ~ 2^{int(math.log2(Gmin))}")
