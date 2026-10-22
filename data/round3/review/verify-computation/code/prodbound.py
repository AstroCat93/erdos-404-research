# product bound prod (1+Gamma_p(J_m)) over full blocks up to depth k (Theorem 11.38 proof), with the
# first (partial or full) group's factor taken as its exact value (C at its jump), as a guess of the
# note's "product bound" column.
import sys
from fractions import Fraction as F
from math import factorial
def vp(n,p):
    c=0
    while n%p==0: n//=p; c+=1
    return c
def vfact(n,p):
    s=0
    while n: n//=p; s+=n
    return s
def gam(p,j):
    cnt={}
    for l in open(f"out/gblock_{p}.txt"):
        if l.startswith("j="): a,b=l.split(); cnt[int(a[2:])]=int(b[4:])
    return F(p**j*cnt[j],4**p)-1
def exact_first(p,N0,elems,J):
    # exact C-factor of first group: p^J P(sum eta x = 0 mod p^J) for the group's normalised elements
    m=p**J; d={0:F(1)}
    for x in elems:
        nd={}
        for r,pr in d.items():
            for dd,w in ((0,F(1,2)),(x,F(1,4)),(-x,F(1,4))): nd[(r+dd)%m]=nd.get((r+dd)%m,0)+pr*w
        d=nd
    return p**J*d.get(0,0)
for (p,N0,k) in [(2,1,28),(3,1,17),(5,1,12),(7,1,10),(11,1,7),(13,1,7),(13,13,6)]:
    e0=vfact(N0,p)
    # groups by level
    n=N0; groups=[]
    while True:
        a=vfact(n,p)-e0
        if a>=k: break
        g=[n]; n+=1
        while vfact(n,p)-e0==a: g.append(n); n+=1
        groups.append((a,g))
    prod=F(1); out=[]
    for i,(a,g) in enumerate(groups):
        anext=groups[i+1][0] if i+1<len(groups) else None
        J=(anext-a) if anext is not None else None
        j=min(J,k-a) if J is not None else k-a
        if len(g)<p:   # partial group: exact
            elems=[(factorial(x)//p**(e0+a))%p**j for x in g]
            fct=exact_first(p,N0,elems,j)
        else:
            fct=1+gam(p,j)
        prod*=fct
    print(f"p={p} N0={N0} k={k}: product bound = {float(prod):.6f}")
