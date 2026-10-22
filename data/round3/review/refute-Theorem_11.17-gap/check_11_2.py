# Numerical sanity check of distance formula (11.2) in proof of Theorem 11.17.
import random, itertools, sys
p=int(sys.argv[1]) if len(sys.argv)>1 else 3
N=400; MOD=p**N
def v(a):
    a%=MOD
    if a==0: return N
    c=0
    while a%p==0: a//=p; c+=1
    return c
def F(word,x):  # word: set of j (incl 0)
    s=0; pi=1; m=max(word)
    for j in range(m+1):
        if j>0: pi=pi*(x+j)%MOD
        if j in word: s=(s+pi)%MOD
    return s
def dF(word,x):
    s=0; pi=1; d=0; m=max(word)
    for j in range(m+1):
        if j>0:
            d=(d*(x+j)+pi)%MOD; pi=pi*(x+j)%MOD
        if j in word: s=(s+d)%MOD
    return s
def newton(word,x,lam):
    for _ in range(60):
        f=F(word,x); 
        if f==0: break
        d=dF(word,x); u=d//p**lam; inv=pow(u%MOD,-1,MOD)
        x=(x-(f//p**lam)*inv)%MOD
    assert F(word,x)==0, "no conv"
    return x
random.seed(1)
# find simple zero of a finite word with slope 0
found=None
for trial in range(2000):
    word={0}|{j for j in range(1,7) if random.random()<.5}
    for r in range(p**6):
        lm=v(dF(word,r))
        if lm<=2 and v(F(word,r))>2*lm:
            a=newton(word,r,lm)
            if (a+2)%MOD!=0 and v(dF(word,a))==lm: found=(word,a,lm); break
    if found: break
word,alpha,lam=found
print("p",p,"word",sorted(word),"lam",lam)
w,K=1,3; P=w*p
l0=next(l for l in range(1,p+1) if (alpha+l)%p==0)
i0=next(i for i in range(200) if l0+p*i>max(max(word),p*(2*lam+2)) and v(F({0}|set(range(0)),0) if False else 1)>=0 and sum(v(alpha+n) for n in range(1,l0+p*i+1))-lam>=max(K+1,v(alpha+2)+1))
W=4
a=[l0+p*(i0+k*w) for k in range(W)]
Lk=lambda z,k: sum(v(z+n) for n in range(1,a[k]+1))
bad=0;tests=0
for t in range(300):
    c=[set(s for s in range(P) if random.random()<.5) for k in range(W)]
    c2=[set(x) for x in c]; k=random.randrange(W)
    while c2[k]==c[k]: c2[k]=set(s for s in range(P) if random.random()<.5)
    for m in range(k+1,W): c2[m]=set(s for s in range(P) if random.random()<.5)
    J=set().union(*[{a[m]+s for s in c[m]} for m in range(W)])
    J2=set().union(*[{a[m]+s for s in c2[m]} for m in range(W)])
    z=newton(word|J,alpha,lam); z2=newton(word|J2,alpha,lam)
    tau=(alpha+a[k])%p**K
    q=lambda s,x: __import__('math').prod([(x+tt) for tt in range(1,s+1)])
    br=sum(q(s,z+a[k]) for s in c[k])-sum(q(s,z+a[k]) for s in c2[k])
    d=v(br)
    G=min(K,sum(min(v((tau+tt)%p**K) if (tau+tt)%p**K else K,K) for tt in range(1,P+1)))
    lhs=v(z-z2); tests+=1
    if d<G:
        if lhs!=Lk(z,k)-lam+d: bad+=1; print("MISMATCH",k,lhs,Lk(z,k),d,G)
    else:
        if lhs< Lk(z,k)-lam+G: bad+=1; print("BOUND FAIL",k,lhs,Lk(z,k),G)
print("tests",tests,"bad",bad)
