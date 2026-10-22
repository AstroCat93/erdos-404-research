# Prop 11.13(b): Newton root of H(y)=y+(y-1)pi_c(y) mod p^K, check v(y_c)=v(c!) and H'(y_c) unit.
# Theorem 11.45: y_i(K') = i! A_i B_i with stated congruences (a)-(d), random parameters.
import math, random
def v(z,p):
    if z==0: return 10**9
    c=0
    while z%p==0: z//=p; c+=1
    return c
def pic(c,y): 
    r=1
    for i in range(1,c+1): r*=(y+i)
    return r
out=[]
for p in [2,3,5,7]:
    for c in [2*p,2*p+1,3*p+2,5*p]:
        K=v(math.factorial(c),p)+30; m=p**K
        H=lambda y: y+(y-1)*pic(c,y)
        def Hp(y):
            # derivative of y+(y-1)pi_c(y)
            s=sum(math.prod(y+i for i in range(1,c+1) if i!=j) for j in range(1,c+1))
            return 1+pic(c,y)+(y-1)*s
        y=0
        for _ in range(60): y=(y-H(y)*pow(Hp(y)%m,-1,m))%m
        assert H(y)%m==0
        out.append((p,c,v(y,p)==v(math.factorial(c),p) or y%m==0, v(Hp(y),p)==0))
print("Prop 11.13(b) (p,c,v(y_c)=v(c!),H'(y_c) unit):",out)
bad=0;tests=0
for trial in range(300):
    p=random.choice([3,5,7,11,13]); D=random.randint(1,3); t=random.randint(D+1,D+4); H=p**D
    Kp=random.randint(1,p**3); X=p**t*Kp; vK=v(Kp,p)
    for i in range(H):
        y=math.prod(X-(H-s) for s in range(1,i+1))
        A=(-1)**i*math.comb(p**D-1,i); l=0 if i==0 else int(math.floor(math.log(i,p)+1e-12))
        # B_i = y/(i! A_i)
        from fractions import Fraction as F
        Bi=F(y,math.factorial(i)*A)
        Hi=sum(F(1,s) for s in range(1,i+1))
        def vf(q): return v(q.numerator,p)-v(q.denominator,p) if q!=0 else 10**9
        tests+=1
        ok = vf(F(A)-1)>=D-l and vf(Bi-1)>=t+vK-l and vf(F(A)-1+p**D*Hi)>=2*(D-l) and v(y-math.factorial(i)*A,p)>=t+vK+v(math.factorial(i),p)-l
        if not ok: bad+=1
print("Theorem 11.45 (a)-(d) congruences: tests",tests,"failures",bad)
