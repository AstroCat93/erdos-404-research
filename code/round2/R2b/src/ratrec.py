import sys
def digits(r,p,M):
    d=[]
    for _ in range(M): d.append(r%p); r//=p
    return d
def ratrec(r,m):
    # find a/b == r mod m with |a|,|b| small via extended Euclid (half-gcd style list of all convergents)
    out=[]
    a0,a1=m,r%m; b0,b1=0,1
    while a1!=0:
        out.append((a1,b1))
        q=a0//a1; a0,a1=a1,a0-q*a1; b0,b1=b1,b0-q*b1
    return out
p=int(sys.argv[1]); M=int(sys.argv[2]); m=p**M
for s in sys.argv[3:]:
    r=int(s)%m
    best=min(ratrec(r,m), key=lambda ab: max(abs(ab[0]),abs(ab[1])))
    print(r, 'digits(lo->hi)=',digits(r,p,M),' best a/b=',best, ' v(r)=', next((i for i,x in enumerate(digits(r,p,M)) if x), M))
