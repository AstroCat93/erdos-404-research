# Prop 11.25: finite certificate values and random/adversarial slope tests.
import random, time, itertools, sys
from fractions import Fraction
from common import *
def piQ(y,k):
    r=Fraction(1)
    for i in range(1,k+1): r*= (y+i)
    return r
# (a) S_e(-4)
vals=[1-3*a+6*b-6*c for a,b,c in itertools.product((0,1),repeat=3)]
print("S_e(-4):",vals,"max v",max(vfrac(q) for q in vals))
# (b) Phi_e(-4) families
def Phi(y,e2,tail):  # tail = (e3,e4,...)
    r=Fraction(e2)-Fraction(1,1-y)
    for k,ek in enumerate(tail,1): r+=ek*piQ(y,k)
    return r
A=[Phi(-4,1,(0,a,b)) for a,b in itertools.product((0,1),repeat=2)]
B=[Phi(-4,0,(1,a,b)) for a,b in itertools.product((0,1),repeat=2)]
print("(b) famA",A,[vfrac(q) for q in A]); print("(b) famB",B,[vfrac(q) for q in B])
# (c) famB at -8 over e4..e9 ; also check pi_k(-8)=0 for k>=8
hist={}
for t in itertools.product((0,1),repeat=6):
    q=Phi(-8,0,(1,)+t); vv=vfrac(q); assert q!=0; hist[vv]=hist.get(vv,0)+1
print("(c) famB Phi(-8) valuation histogram",dict(sorted(hist.items())))
# identity check S_e(x)=y(y-1)Phi_e(y) at rational points
rng=random.Random(5)
for _ in range(200):
    n=rng.randint(4,12); e=[1,1]+[rng.randint(0,1) for _ in range(n-2)]
    xq=Fraction(rng.randint(-50,50)*2+1, 7)  # generic, never -1
    y=xq+2
    if y==1: continue
    S=sum(e[j]*piQ(xq,j) for j in range(n))
    assert S==y*(y-1)*Phi(y,e[2] if n>2 else 0,tuple(e[3:]))
print("identity S=y(y-1)Phi ok")
# random slope tests
L={"C0":1,"C2":3,"C6":6}
rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 7)
t0=time.time(); worst={c:0 for c in L}; npaths={c:0 for c in L}
for cls in L:
    k,r0,LL,l0,sL,EC,Vc=CLASSES[cls]
    for trial in range(3000):
        x=rand_in_class(cls,rng)
        if trial%3==1:  # adversarial: make x+2 (or x+4/x+8 etc) highly divisible within class
            m=rng.choice([2,4,6,8,10,12,14,16,18,20,22,26,30])
            x=(-m + (rng.getrandbits(P-40)<<rng.randint(k+1,30)))%MOD
            if x % (1<<k)!=r0: continue
        # smallest n with V_n >= Vcert, plus a few larger
        n=1
        while V(x,n)<Vc: n+=1
        for nn in (n,n+1,n+3,max(n,19)):
            ps,Vs=alive_paths(x,nn)
            for bits,S,dS in ps:
                lam=v(dS); npaths[cls]+=1
                worst[cls]=max(worst[cls],lam)
                if lam>LL: print("VIOLATION",cls,hex(x%2**64),nn,bits,lam); sys.exit(1)
print("max slopes seen",worst,"paths checked",npaths,"time %.1fs"%(time.time()-t0))
