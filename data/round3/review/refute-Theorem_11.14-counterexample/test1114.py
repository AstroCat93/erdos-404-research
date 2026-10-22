# Counterexample hunt for Theorem 11.14 / Prop 11.13 / Lemma 11.12 / Thm 3.5 (note_v3 §11.2)
import random, itertools, sys
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
def v(n,p,cap=10**6):
    if n==0: return cap
    k=0
    while n%p==0: n//=p; k+=1
    return k
def pi(b,x,M):
    r=1
    for l in range(1,b+1): r=r*(x+l)%M
    return r
def dpi(b,x,M):  # derivative of pi_b at x mod M
    s=0
    for d in range(1,b+1):
        r=1
        for l in range(1,b+1):
            if l!=d: r=r*(x+l)%M
        s+=r
    return s%M
def F(B,x,M): return (1+sum(pi(b,x,M) for b in B))%M
def dF(B,x,M): return sum(dpi(b,x,M) for b in B)%M
def Phi(p):
    out=set()
    for r in range(p):
        m=p-r; ok=True
        for k in range(m):
            for B in itertools.combinations(range(1,m),k):
                if F(B,-m,p)==0: ok=False;break
            if not ok: break
        if ok: out.add(r)
    return out
def hensel_simple(B,p,N):
    """all roots x mod p^N of F_B with v(F'(x)) = lam, lifted by Newton from roots mod p^(2lam+1). Returns list (x,lam)."""
    M=p**N; res=[]
    # brute roots mod p^K for small K, with v(F')<=lamcap
    K=3
    for x0 in range(p**K):
        val=F(B,x0,p**K); 
        if val!=0: continue
        lam=v(dF(B,x0,p**K),p,cap=K)
        if 2*lam+1>K or lam>=K: continue
        # Newton
        x=x0
        for _ in range(4*N):
            fx=F(B,x,M); 
            if fx==0: break
            d=dF(B,x,M); vd=v(d,p)
            u=(d//p**vd)
            x=(x - (fx//p**vd)*pow(u,-1,M))%M
        if F(B,x,M)==0 and v(dF(B,x,M),p,cap=N)==lam:
            res.append((x,lam))
    # dedupe by distance > lam
    out=[]
    for x,l in res:
        if not any(v((x-y)%M,p,cap=N)>l for y,_ in out): out.append((x,l))
    return out
fails=0; tests=0
for p in [2,3,5,7,11,13]:
    ph=Phi(p)
    print("p",p,"Phi",sorted(ph))
    N=40 if p<=3 else 25
    M=p**N
    # (ii): simple zero exists in every class r not in Phi (Thm 3.5 construction) and none in Phi classes
    for r in range(p):
        m=p-r; found=None
        for k in range(m):
            for T0 in itertools.combinations(range(1,m),k):
                if F(T0,r,p)==0:
                    for T in (T0,T0+(m,)):
                        if F(T,r,p)==0 and dF(T,r,p)%p!=0: found=T;break
                if found: break
            if found: break
        tests+=1
        if (found is None)!=(r in ph): fails+=1; print("FAIL (ii) construction",p,r,found)
    # random finite words: simple zeros must lie in classes not in Phi; test Prop 11.13(a) single flips
    for trial in range(60 if p<=5 else 25):
        B=tuple(sorted(random.sample(range(1,4*p),random.randint(1,5))))
        roots=hensel_simple(B,p,N)
        for x,lam in roots:
            tests+=1
            if x%p in ph: fails+=1; print("FAIL simple zero in Phi class",p,B,x)
            # single flips at j >= p(2lam+2)
            for j in random.sample(range(p*(2*lam+2), p*(2*lam+2)+6*p),3):
                B2=tuple(sorted(set(B)^{j}))
                # find zero near x: Newton from x
                y=x
                for _ in range(6*N):
                    fy=F(B2,y,M)
                    if fy==0: break
                    d=dF(B2,y,M); vd=v(d,p); y=(y-(fy//p**vd)*pow(d//p**vd,-1,M))%M
                tests+=1
                pj=v(pi(j,x,M),p,cap=N)
                pred=pj-lam
                got=v((y-x)%M,p,cap=N)
                lam2=v(dF(B2,y,M),p,cap=N)
                ok = F(B2,y,M)==0 and lam2==lam and (got==pred or (pred>=N-lam and got>=N-2*lam-1)) and got>lam
                if not ok:
                    fails+=1; print("FAIL 11.13a",p,B,x,lam,j,pred,got,lam2)
    # Prop 11.13(b)
    for c in range(2*p,2*p+6):
        B=(1,2,c+2); y=(-2)%M
        # find zero x_c with v(x_c+2)=v(c!) : Hensel on H
        import math
        vc=v(math.factorial(c),p)
        # Newton on H(y)=y+(y-1)pi_c(y) from y=0 (H'(0) unit), then x=y-2
        def H(yy): return (yy+(yy-1)*pi(c,yy,M))%M
        def dH(yy): return (1+pi(c,yy,M)+(yy-1)*dpi(c,yy,M))%M
        yy=0
        for _ in range(8*N):
            h=H(yy)
            if h==0: break
            yy=(yy-h*pow(dH(yy),-1,M))%M
        x=(yy-2)%M
        ok = F(B,x,M)==0 and v((x+2)%M,p,cap=N)==vc and v(dF(B,x,M),p,cap=N)==vc and vc<N
        if not ok: fails+=1; print("FAIL 11.13b",p,c,vc,F(B,x,M),v((x+2)%M,p,cap=N),v(dF(B,x,M),p,cap=N))
print("tests",tests,"fails",fails)
