# Sanity checks for Prop 11.13 / Thm 11.14 (numerical, not proofs). Exact integer arithmetic mod p^N.
import math,sys
def v(n,p):
    if n==0: return 10**9
    k=0
    while n%p==0: n//=p;k+=1
    return k
def F(word,x,M):  # word: set of j (incl 0); returns F and F' mod M
    s=0;d=0;pi=1;dpi=0;mx=max(word)
    for j in range(0,mx+1):
        if j>0:
            dpi=(dpi*(x+j)+pi)%M; pi=pi*(x+j)%M
        if j in word: s=(s+pi)%M; d=(d+dpi)%M
    return s,d
def newton(word,x0,p,N,lam):
    M=p**(N+2*lam+4); x=x0
    for _ in range(200):
        f,d=F(word,x,M)
        if f==0: break
        # p-adic Newton: x -= f/d ; d = p^lam*u
        u=d//p**lam; inv=pow(u,-1,M); x=(x-(f//p**lam)*inv)%M
    f,d=F(word,x,M); return x%p**N, v(f,p), v(d,p)
N=40
for p in (2,3,5):
    for c in (2*p,2*p+1,3*p):
        w={0,1,2,c+2}
        M=p**(N+10); y=0
        for _ in range(100):
            pc=1;dpc=0
            for l in range(1,c+1): dpc=(dpc*(y+l)+pc)%M; pc=pc*(y+l)%M
            H=(y+(y-1)*pc)%M; dH=(1+pc+(y-1)*dpc)%M
            if H==0: break
            y=(y-H*pow(dH,-1,M))%M
        x=(y-2)%M; f,d=F(w,x,M); vf,vd=v(f,p),v(d,p); x%=p**N
        print("p",p,"c",c,"v(F)",vf,"v(F')",vd,"v(x+2)",v((x+2)%p**N,p),"v(c!)",v(math.factorial(c),p))
N=150
# single-flip children of a Theorem-3.5 simple zero; check v(alpha_j-alpha)=v(pi_j(alpha))-lam
for p in (3,5):
    w={0,1}  # x+2, root -2, lam=0 ; use another: S_{1,2}? find simple zero via r search
    base={0,2,5}
    for r in range(p):
        f,d=F(base,r,p)
        if f==0 and d!=0:
            a,vf,vd=newton(base,r,p,N,0)
            for j in range(2*p*(2*vd+2),2*p*(2*vd+2)+6):
                M=p**N; pij=1
                for l in range(1,j+1): pij=pij*(a+l)%(p**(N+10))
                b,vf2,vd2=newton(base|{j},a,p,N,vd)
                print("p",p,"alpha mod p",r,"lam",vd,"j",j,"v(diff)",v((b-a)%M,p),"pred",v(pij,p)-vd,"slope child",vd2,"vF",vf2)
            break
