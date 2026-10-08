from core import *
import math, sympy
def Phi(p):
    out=[]
    for r in range(p):
        m=p-r  # in [1,p]
        if m==2: continue
        # gamma_p(m)==0 iff no subset B of [1,m-1] with p | S_B(-m); do set DP mod p
        vals={1%p}; pr=1
        for b in range(1,m):
            pr=pr*(b-m)%p; vals|={(y+pr)%p for y in vals}
        if 0 not in vals: out.append(r)
    return out
claimed={3:[2],5:[2,4],7:[4,6],11:[7,8,10],13:[9,10,12],17:[12,13,14,16],19:[14,15,16,18],23:[19,20,22]}
for p,c in claimed.items():
    print(p,Phi(p),"OK" if Phi(p)==c else "DIFF claimed %s"%c)
# p-1 and p-3 membership, p-2 non-membership, lower bound
bad=[]
for p in sympy.primerange(5,60):
    F=set(Phi(p))
    if (p-1) not in F or (p-3) not in F or (p-2) in F: bad.append(p)
    lb=sum(1 for m in [1]+list(range(3,min(p,12)+1)) if sum(math.factorial(m-1)//math.factorial(k) for k in range(m))<p)
    if len(F)<lb: bad.append(('lb',p))
print("membership/lower-bound violations p<350:",bad)
# check Phi_p against true g: for a in class r, g(a)==0 iff r in Phi
for p in (3,5,7,11,13):
    F=set(Phi(p))
    for a in range(1,400):
        assert (g_exact(a,p,1)==0)==((a%p) in F),(p,a)
print("Phi_p consistent with g_exact for p<=13, a<400")
# Thm 3.5: Hensel construction for r not in Phi
def S_and_dS(T,r,p):
    x=sympy.symbols("x"); S=sympy.Integer(1)
    for b in T:
        pr=1
        for i in range(1,b+1): pr*=(x+i)
        S+=pr
    return int(S.subs(x,r))%p, int(sympy.diff(S,x).subs(x,r))%p
nh=0
for p in (3,5,7,11,13,17,19,23):
    F=set(Phi(p))
    for r in range(p):
        if r in F: continue
        ks=next(k for k in range(1,p+1) if (r+k)%p==0)
        T0=None
        for mask in range(1<<(ks-1)):
            T=[b for b in range(1,ks) if mask>>(b-1)&1]
            if S_and_dS(T,r,p)[0]==0: T0=T;break
        assert T0 is not None,(p,r)
        ok=any(S_and_dS(T,r,p)==(0,S_and_dS(T,r,p)[1]) and S_and_dS(T,r,p)[1]!=0 for T in (T0,T0+[ks]))
        assert ok,(p,r); nh+=1
print("Hensel construction succeeded for",nh,"classes")
