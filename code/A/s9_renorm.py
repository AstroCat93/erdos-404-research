# s9_renorm.py -- check (p^t m)! = p^{alpha_t m} m! prod_{i=1}^t P(p^i m), alpha_t=(p^t-1)/(p-1),
# and the level-t carry recursion xi_{m+1} = (xi_m + y_m)/(p^{alpha_t}(m+1)) on random sets A.
import math, random
from fractions import Fraction
def P(n,p):
    r=1
    for j in range(1,n+1):
        if j%p: r*=j
    return r
ok=True
for p in [2,3,5]:
    for t in [1,2,3]:
        al=(p**t-1)//(p-1)
        for m in range(0,12):
            Pi=1
            for i in range(1,t+1): Pi*=P(p**i*m,p)
            if math.factorial(p**t*m)!=p**(al*m)*math.factorial(m)*Pi: ok=False; print("fail",p,t,m)
        random.seed(p*10+t)
        A=set(n for n in range(1,p**t*8) if random.random()<0.4)
        S=lambda N: sum(math.factorial(n) for n in A if n<N)
        for m in range(0,7):
            xi_m=Fraction(S(p**t*m),p**(al*m)*math.factorial(m))
            xi_n=Fraction(S(p**t*(m+1)),p**(al*(m+1))*math.factorial(m+1))
            Pi=1
            for i in range(1,t+1): Pi*=P(p**i*m,p)
            y=Pi*sum(math.prod(range(p**t*m+1,p**t*m+j+1)) for j in range(p**t) if p**t*m+j in A)
            if xi_n!=(xi_m+y)/(p**al*(m+1)): ok=False; print("rec fail",p,t,m)
print("renormalization identities:",ok)
