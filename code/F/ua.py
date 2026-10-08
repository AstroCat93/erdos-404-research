import sys
p,A,B=map(int,sys.argv[1:4])
def vp(n):
    v=0
    while n%p==0: n//=p; v+=1
    return v
E=sum(vp(k) for k in range(A+1,B+1))
M=p**E; U=1
for n in range(1,A+1):
    m=n
    while m%p==0: m//=p
    U=U*m%M
print(U)
