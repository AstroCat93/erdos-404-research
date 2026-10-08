from core import *
for p in (2,3,5,7,11,13):
    for m in range(1,17):
        if m==2: continue
        assert gamma(m,p)==gamma2(m,p),(m,p)
print("gamma == gamma2 for m<=16, p<=13")
print("gamma2:",[ (m,gamma2(m,2)) for m in (4,6,8,10,12,14,18,24,26,30,34)])
print("gamma2 odd m nonzero?",[m for m in range(1,40,2) if gamma2(m,2)!=0])
print("gamma3:",[(m,gamma2(m,3)) for m in (3,5,6,8,9,11)])
print("gamma5:",[(m,gamma2(m,5)) for m in (4,5,7,17)])
print("gamma7(4)=",gamma2(4,7)," gamma13(13)=",gamma2(13,13))
import math
for m in range(2,20):
    terms=[];pr=1
    for b in range(1,m): pr*=(b-m); terms.append(pr)
    vals={1}
    for t in terms: vals|={y+t for y in vals}
    mx=max(abs(v) for v in vals)
    bound=sum(math.factorial(m-1)//math.factorial(k) for k in range(m))
    assert mx<=bound, m
    if m!=2: assert 0 not in vals
print("bound (b) ok and nonvanishing for m<=19")
for p in (2,3,5,7):
    out=[]
    for k in range(1,8):
        m=p**k+2
        if m>40: break
        out.append((m,gamma2(m,p),3*k))
    print("p=%d (m,gamma,3k):"%p,out)
