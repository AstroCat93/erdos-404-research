import sys
def chk(p,t,H,K):
    c=sum(1 for i in range(1,H) for _ in iter(lambda i=[i]: (i[0]%p==0) and not i.__setitem__(0,i[0]//p), False))
    # simpler valuation
    c=0
    for i in range(1,H):
        x=i
        while x%p==0: c+=1; x//=p
    M=t+c; N=p**M; X=p**t*K
    ys=[]; y=1
    for i in range(H):
        if i>0: y=y*(X-(H-i))
        ys.append(y%N)
    S={0}
    for v in ys: S|={(s+v)%N for s in S}
    return N-len(S)
for a in [(5,2,10,1),(5,2,9,1),(7,3,19,1),(7,3,18,3),(3,2,9,1),(5,3,14,2),(7,2,6,1)]:
    print(a,chk(*a))
