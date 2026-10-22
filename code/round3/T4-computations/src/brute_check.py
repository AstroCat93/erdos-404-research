import sys, itertools
def MG(p,G):
    b=0; v=0
    while True:
        y=b+1; w=0
        while y%p==0: y//=p; w+=1
        if v+w>=G: return b
        v+=w; b+=1
def N(p,G,x):
    M=p**G; m=MG(p,G)
    pis=[]; pr=1
    for b in range(1,m+1): pr=pr*(x+b)%M; pis.append(pr)
    # subset-sum count via dict DP
    cnt={1%M:1}
    for t in pis:
        new=dict(cnt)
        for r,c in cnt.items(): new[(r+t)%M]=new.get((r+t)%M,0)+c
        cnt=new
    return cnt.get(0,0)
for p,G in [(2,6),(2,8),(3,3),(3,4),(5,2),(7,2)]:
    M=p**G; m=MG(p,G); Ns=[N(p,G,x) for x in range(M)]
    S1=sum(Ns); S2=sum(n*n for n in Ns); surv=sum(1 for n in Ns if n)
    print(f"p={p} G={G} M_G={m} sumN={S1} sumN2={S2} surv={surv} maxN={max(Ns)} delta={surv/M:.6f}")
