import math, itertools, sympy as sp
def pi(b,x):
    r=1
    for l in range(1,b+1): r*=(x+l)
    return r
def vp(n,p):
    if n==0: return 10**9
    k=0
    while n%p==0: n//=p; k+=1
    return k
def gge(p,G,c):
    M=p**G; mask=(1<<M)-1; s=1<<(1%M)
    for b in range(1,p*G):
        t=pi(b,c)%M
        if t: s|=((s<<t)|(s>>(M-t)))&mask
    return bool(s&1)
def gmin(p,c,Gmax):
    g=0
    while g<Gmax and gge(p,g+1,c): g+=1
    return g
def gamma(p,m,cap=20):
    best=0
    for r in range(1,m):
        pass
    terms=[pi(b,-m) for b in range(1,m)]
    for mask in range(1<<len(terms)):
        s=1+sum(terms[i] for i in range(len(terms)) if mask>>i&1)
        best=max(best,min(vp(s,p),cap))
    return best
# gap theorem check
for p,L,Gmax,A in [(7,2,4,400),(11,2,3,400),(5,1,3,300),(13,2,3,300)]:
    gam={k:(gamma(p,k) if k!=2 else 10**9) for k in range(1,p+1)}
    bad=0
    for a in range(1,A+1):
        k=p-(a%p) if a%p else p
        m0=(a-(p-k))//p
        tau=gam[k]
        g=gmin(p,a,Gmax)
        if tau<=vp(m0+1,p):
            ok = (g==min(tau,Gmax))
        else:
            ok = (g>=min(L+1,Gmax))
        if not ok: bad+=1; print("GAP VIOLATION",p,a,g,tau)
    print("gap check p=%d a<=%d: violations=%d"%(p,A,bad), "gammas",gam)
print("g_3(3) =", gmin(3,3,5), " g_3(12)>=", gmin(3,12,9))
print("g_5(5^8-17)=", gmin(5,5**8-17,9))
# Prop 3.4(b): rational roots and multiplicity of -2 for B subset [1,8]
x=sp.symbols('x'); worst=0
for r in range(1,9):
    for B in itertools.combinations(range(1,9),r):
        S=1+sum(sp.prod([x+l for l in range(1,b+1)]) for b in B)
        P=sp.Poly(sp.expand(S),x)
        roots=[q for q in sp.roots(P,filter='Q').keys()] if False else None
        # rational roots via factor_list
        fl=sp.factor_list(P.as_expr())[1]
        for f,e in fl:
            if sp.degree(f,x)==1:
                rt=sp.solve(f,x)[0]
                if rt!=-2: print("OTHER RATIONAL ROOT",B,rt)
                else:
                    if e>worst: worst=e; wB=B
print("max multiplicity of -2 for B in [1,8]:",worst,wB)
