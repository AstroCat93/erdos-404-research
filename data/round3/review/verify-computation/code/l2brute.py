# brute force C_k for tiny cases: enumerate all eta in {-1,0,1}^M with weights
import sys, itertools
from fractions import Fraction as F
p,N0,k=map(int,sys.argv[1:4]); m=p**k
def v(n):
    c=0
    while n%p==0: n//=p; c+=1
    return c
import math
e0=sum(v(i) for i in range(1,N0+1))
xs=[]
n=N0
while True:
    vn=sum(v(i) for i in range(1,n+1))
    if vn-e0>=k: break
    xs.append((math.factorial(n)//p**e0)%m); n+=1
dist={0:F(1)}
for x in xs:
    nd={}
    for r,pr in dist.items():
        for d,w in ((0,F(1,2)),(x,F(1,4)),(-x,F(1,4))):
            nd[(r+d)%m]=nd.get((r+d)%m,0)+pr*w
    dist=nd
print(f"p={p} N0={N0} k={k} M={len(xs)} C_k-1={p**k*dist.get(0,0)-1} ~ {float(p**k*dist.get(0,0)-1):.12g}")
