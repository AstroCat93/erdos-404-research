# Optimised (exact binomial tail, best c) version of the Theorem 7 bound; same terms otherwise.
import math
from constants import classes, s, smax, Bbad, n0_of
def binom_cdf(N,u):
    if u<0: return 0.0
    return sum(math.comb(N,j) for j in range(0,min(N,u)+1))/2**N
def bound_opt(G,c):
    k,r0,L,EC=c['k'],c['r0'],c['L'],c['EC']; l0=2*L+2
    T=G//2; K=math.floor(math.log2(T-l0+1)); n0=n0_of(G,L)
    if n0+l0>T or K<=k: return None
    best=min(2.0**(-cc)*EC+2.0**(-k)*binom_cdf(K-k,cc+smax(L)-s(r0)) for cc in range(0,K+1))
    return Bbad(n0,L)+n0*2.0**(-K)+best
for name,c in classes.items():
    out=[]
    for j in (20,30,40,60,80,100,150,200):
        b=bound_opt(2**j,c); out.append(f"2^{j}:{b:.3g}")
    print(name,'mu(C)=',2.0**-c['k'],' '.join(out))
