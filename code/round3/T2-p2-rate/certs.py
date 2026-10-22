# Finite checks behind Proposition 2.2 (exact rational arithmetic). Prints the maximal 2-adic valuation in each case.
from fractions import Fraction
from itertools import product
def v2(q):
    q=Fraction(q)
    if q==0: return float('inf')
    a,b=q.numerator,q.denominator; v=0
    while a%2==0: a//=2; v+=1
    while b%2==0: b//=2; v-=1
    return v
def pi(k,y):
    p=1
    for i in range(1,k+1): p*=(y+i)
    return p
# (a) S_e(-4) = sum_{j<4} e_j pi_j(-4), e_0=1
vals=[1+e1*pi(1,-4)+e2*pi(2,-4)+e3*pi(3,-4) for e1,e2,e3 in product((0,1),repeat=3)]
print('(a) S_e(-4) values',vals,'max v2 =',max(v2(q) for q in vals))
# Phi_e(y) = e2 - 1/(1-y) + sum_{k>=1} e_{k+2} pi_k(y); at y=-m only k<m contribute
def Phi(m,e2,es):   # es = (e3, e4, ..., e_{m+1}) i.e. coefficients of pi_1..pi_{m-1}
    y=-m
    return Fraction(e2)-Fraction(1,1-y)+sum(es[k-1]*pi(k,y) for k in range(1,m))
for (m,e2,e3,label) in [(4,1,0,'(c)/(d) e2=1 at y=-4'),(4,0,1,'(c) e2=0 at y=-4'),(8,0,1,'(d) e2=0 at y=-8')]:
    rng=[ (e3,)+t for t in product((0,1),repeat=m-2) ]
    vs=[v2(Phi(m,e2,es)) for es in rng]
    print(label,': cases',len(rng),' max v2(Phi(-m)) =',max(vs),' histogram',{v:vs.count(v) for v in sorted(set(vs))})
