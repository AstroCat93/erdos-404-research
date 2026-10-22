# Independent recomputation of theta_p and theta_p^set (Cor 11.39 / Thm 11.38), exact rationals + mpmath
import sys, math
from fractions import Fraction as Fr
from itertools import product
import mpmath as mp
mp.mp.dps=50
def es(p):
    f=math.factorial(p-1); return [(-1)**u*f//math.factorial(u) for u in range(p)]
def counts_W(p,jmax):
    # exact weights for W=sum eta_u e_u, eta weights 1,2,1 (total 4^p); dict W->weight
    d={0:1}
    for e in es(p):
        nd={}
        for w,c in d.items():
            for s,wt in ((-1,1),(0,2),(1,1)):
                nd[w+s*e]=nd.get(w+s*e,0)+c*wt
        d=nd
    return d
def subsums(p):
    S={0}
    for e in es(p): S|={s+e for s in S}
    return S
for p in [2,3,5,7,11,13]:
    d=counts_W(p,0); S=subsums(p)
    assert len(S)==3*2**(p-2) or p==2
    tot=4**p
    def Gam(j): return Fr(p**j*sum(c for w,c in d.items() if w%(p**j)==0),tot)-1
    def dist(j): return len({s%(p**j) for s in S})
    P0=Fr(d[0],tot); J0=1
    while Fr(sum(c for w,c in d.items() if w%(p**J0)==0),tot)!=P0: J0+=1
    # theta = (p-1)/p * sum_j (1-1/p) p^-j f(j); f(j)=log_p(1+Gam(j+1)); affine for j+1>=J0
    def series(fun, aff):
        s=mp.mpf(0)
        for j in range(0,J0+5): s+=(1-mp.mpf(1)/p)*mp.mpf(p)**(-j)*fun(j)
        # tail j>=J0+5 with fun(j)= aff(j) = j+1 + c
        c=aff
        jt=J0+5; q=mp.mpf(1)/p
        # sum_{j>=jt} (1-q) q^j (j+1+c)
        tail=(1-q)*sum(q**j*(j+1+c) for j in range(jt,jt+400))
        return (p-1)*mp.mpf(1)/p*(s+tail)
    f=lambda j: mp.log(mp.mpf(1+Gam(j+1).numerator/ Gam(j+1).denominator) if False else mp.mpf((1+Gam(j+1)).numerator)/ (1+Gam(j+1)).denominator)/mp.log(p)
    cG=mp.log(mp.mpf(3)/2/2**p)/mp.log(p)   # 1+Gam(j)=3/2 p^j 2^-p for j>=J0
    fs=lambda j: mp.log(mp.mpf(p)**(j+1)/dist(j+1))/mp.log(p)
    cS=-mp.log(3*2**(p-2))/mp.log(p) if p>2 else -mp.log(3)/mp.log(2)
    # sanity: affine check
    for j in range(J0,J0+4):
        assert abs(f(j)-(j+1+cG))<mp.mpf(10)**-40, (p,j)
        assert abs(fs(j)-(j+1+cS))<mp.mpf(10)**-40, (p,j)
    th=series(f,cG); ths=series(fs,cS)
    print(p,"J0",J0,"Gam1",Gam(1),"dist",[dist(j) for j in range(1,J0+1)],"theta",mp.nstr(th,8),"1-theta_set",mp.nstr(1-ths,10))
