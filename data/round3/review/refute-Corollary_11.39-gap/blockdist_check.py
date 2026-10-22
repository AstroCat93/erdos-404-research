# Check dist_13(J) from actual factorial blocks, and recompute 1-theta_set_13 in float (independent formula)
import math
p=13
def v(n):
    c=0
    while n%p==0: n//=p; c+=1
    return c
def blockdist(m):
    J=1+v(m+1); mod=p**J
    f=math.factorial(p*m); a=0
    while f%p==0: f//=p; a+=1
    xs=[]; cur=math.factorial(p*m)
    for r in range(p):
        if r>0: cur*= (p*m+r)
        xs.append((cur//p**a)%mod)
    S={0}
    for x in xs: S|={(s+x)%mod for s in S}
    return J,len(S)
for m in [1,2,12,25,168,337,2196]:
    print("m",m,"J,dist",blockdist(m))
dist={1:13,2:169,3:2163,4:5178,5:6136}
D=lambda j: dist.get(j,6144)
th=sum((p-1)/p*(1-1/p)*p**-j*math.log(p**(j+1)/D(j+1),p) for j in range(200))
print("1-theta_set_13 =",1-th, " >= 0.99966 ?", 1-th>=0.99966)
