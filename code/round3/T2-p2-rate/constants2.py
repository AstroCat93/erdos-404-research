# sup_G min(mu(C), bound(G)) * G^alpha over a dense grid, with the Theorem 5.3 bound and the Cor. 5.4 parameter choice.
import math
from constants import classes, s, smax, Bbad, n0_of, H, ALPHA
def bound(G,c):
    k,r0,L,EC=c['k'],c['r0'],c['L'],c['EC']; l0=2*L+2
    T=G//2
    if T-l0+1<2: return None
    K=math.floor(math.log2(T-l0+1)); n0=n0_of(G,L)
    if n0+l0>T or K<=k or 2**K<l0: return None
    cc=math.floor(ALPHA*(K-k))-smax(L)+s(r0)
    return Bbad(n0,L)+n0*2.0**(-K)+2.0**(-cc)*EC+2.0**(-k)*2.0**(-(K-k)*(1-H(ALPHA)))
for name,c in classes.items():
    mu=2.0**(-c['k']); best=0; arg=None
    Gs=list(range(2,1<<16))+[int(2**(j+i/256)) for j in range(16,300) for i in range(256)]
    for G in Gs:
        b=bound(G,c); b=mu if b is None else min(mu,b)
        val=b*G**ALPHA
        if val>best: best,arg=val,G
    # analytic limit of the main term for G->infinity:
    k,r0,L,EC=c['k'],c['r0'],c['L'],c['EC']
    main=(2**(1+smax(L)-s(r0))*EC+2.0**(-k))*2**(ALPHA*k)*8**ALPHA
    print(f"{name}: sup over grid of min(mu,bound)*G^0.227 = {best:.4g} at G={arg};  analytic main-term constant = {main:.4g}")
