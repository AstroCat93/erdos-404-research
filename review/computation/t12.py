from core import *
import random
random.seed(7)
bad=0;n=0
for _ in range(400):
    p=random.choice([2,3,5,7,11,13]); m=random.choice([1]+list(range(3,16 if p>2 else 26)))
    gam=gamma2(m,p)
    if p**(gam+1)>10**40: continue
    k=random.randint(1,50)
    a=k*p**(gam+1)-m
    if a<1: continue
    g=g_exact(a,p,gam+3)
    n+=1
    if g!=gam: bad+=1; print("FAIL",p,m,a,g,gam)
print("Thm 3.2(c) random spot checks:",n,"failures",bad)
