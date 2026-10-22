# F~(y) = -1/(1-y) + sum_{k>=1} f_k pi_k(y), f_1=1 ; F(y) = -y/(1-y) + sum_{k>=1} f_k pi_k(y)
# max over f of v2(F(-m)) (rational), m>=3
from fractions import Fraction
def v2q(q):
    if q==0: return 10**9
    a,b=q.numerator,q.denominator; v=0
    while a%2==0: a//=2; v+=1
    while b%2==0: b//=2; v-=1
    return v
for m in range(3,25):
    pis=[]; p=1
    for k in range(1,m):
        p*=(k-m); pis.append(p)
    for name,c0,force1 in (('Ft',Fraction(-1,1+m),True),('F',Fraction(m,1+m),False)):
        # c0 = value of -1/(1-y) at y=-m is -1/(1+m); -y/(1-y) at y=-m is m/(1+m)
        sums={c0+(pis[0] if force1 else 0)} if force1 else {c0}
        rng=pis[1:] if force1 else pis
        for q in rng:
            sums=sums|{s+q for s in sums}
        print(m,name,max(v2q(s) for s in sums), 'zero' if 0 in sums else '')
