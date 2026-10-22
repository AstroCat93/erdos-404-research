# Recheck of the withdrawn Consequence of Thm 11.45: list i<H=p^(t-1) with y_i == i! mod p^(t+c)
from math import factorial
def v(n,p):
    if n==0: return 10**9
    k=0
    while n%p==0: n//=p;k+=1
    return k
for p,t in [(3,3),(5,3),(7,3),(3,4),(3,5)]:
    H=p**(t-1); c=v(factorial(H-1),p); mod=p**(t+c)
    units=[k for k in range(1,p*p*2) if k%p][:8]
    alli=[];somei=[];AiOK=[]
    for i in range(H):
        res=[]
        for K in units:
            y=1
            for s in range(1,i+1): y=y*(p**t*K-(H-s))%mod
            res.append((y-factorial(i))%mod==0)
        if all(res): alli.append(i)
        elif any(res): somei.append(i)
    print(p,t,"H",H,"c",c,"all-units:",alli,"some-units:",somei)
