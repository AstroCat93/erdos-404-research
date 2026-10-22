# Independent evaluation of Corollary 11.30 constants from Theorem 11.29.
import math
from fractions import Fraction
a=0.227
cls={'C0':dict(k=3,r0=0,L=1,l0=4,sL=2,E=1),'C2':dict(k=3,r0=2,L=3,l0=8,sL=3,E=64),'C6':dict(k=4,r0=6,L=6,l0=14,sL=3,E=16384)}
def s(n): return bin(n).count('1')
def h(n,L): return 0.5*(n-math.log2(n)-3*L-4)
def BL(n0,L,l0):
    tot=(n0+l0)*2.0**(-math.floor(h(n0,L))-1)
    for n in range(n0+1,n0+4000): tot+=2.0**(-math.floor(h(n,L))-1)
    return tot*(1+1e-12)
def ilog2floor(m): return m.bit_length()-1
def n0of(G,L):
    # ceil(4 log2 G) exactly: smallest j with G^4 <= 2^j
    j=(G**4).bit_length()-1
    if G**4 != 1<<j: j+=1
    return j+3*L+40
def binom_cdf(N,t):
    if t<0: return 0.0
    return sum(math.comb(N,i) for i in range(0,min(t,N)+1))/2**N
def bound(G,c_):
    k,r0,L,l0,sL,E=c_['k'],c_['r0'],c_['L'],c_['l0'],c_['sL'],c_['E']
    T=G//2; K=ilog2floor(T-l0+1); n0=n0of(G,L)
    assert T>=n0+l0 and 2**K>=l0 and K>k and n0>=19
    c=math.floor(a*(K-k))-sL+s(r0)
    side=BL(n0,L,l0)+n0*2.0**(-K)
    mainChern=(2**(1+sL-s(r0))*E+2**-k)*2**(a*k)*(8/G)**a
    mainExact=2.0**(-c)*E+2**-k*binom_cdf(K-k,c+sL-s(r0))
    return side, mainChern, mainExact
for name,c_ in cls.items():
    L,l0=c_['L'],c_['l0']
    cands=set()
    for K in range(8,200): cands.add(2**(K+2)+2*l0-3)
    for j in range(40,800):
        # largest G with G^4<=2^j
        import math as _m
        g=_m.isqrt(_m.isqrt(2**j))
        cands.add(g)
    cands=sorted(G for G in cands if 2**10<=G<=2**190)
    sup_side=0; sup_tot=0; sup_ex=0
    for G in cands:
        sd,mc,me=bound(G,c_)
        sup_side=max(sup_side,sd*G**a); sup_tot=max(sup_tot,(sd+mc)*G**a); sup_ex=max(sup_ex,min(sd+me, 1/8 if name!='C6' else 1/16)*G**a)
    print(name,"sup side*G^a=%.4f  sup(side+chernoff main)*G^a=%.6g  sup exact min(mu,RHS)*G^a=%.6g"%(sup_side,sup_tot,sup_ex))
print("1-H(0.227)=",1-(-0.227*math.log2(0.227)-0.773*math.log2(0.773)))
print("small G: 0.125 vs 0.61*2^-2.27=",0.61*2**(-10*a))
