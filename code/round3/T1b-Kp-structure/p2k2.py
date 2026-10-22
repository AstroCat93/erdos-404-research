# p=2,k=2: for each local configuration, which odd residues mod 8 of delta/2^V are reachable
# using runs u (J=1) and u+1 (J>=2), all sign patterns sigma in {+-1}^4.
from itertools import product
def v2(n):
    if n==0: return 99
    c=0
    while n%2==0: n//=2; c+=1
    return c
res={}
for X in range(0,2**10,2):   # X = x+l_u+2 mod 2^10 (even), positions l_u=l, l+1 ; next run l+2,l+3
    # run u: elements pi_l * {1, (x+l+1)} ; x+l = X-2
    if v2(X)!=1: continue
    xl=X-2
    for Xp_off in [0]:
        Xp=xl+4  # x+l+4 = start of run u+2 ; jump J_{u+1}=v(Xp)
        J1=v2(Xp)
        if J1<2: continue
        q1=(xl+1)
        # level of run u+1 relative: v(pi_{l+2}/pi_l)=v((xl+1)(xl+2))=1
        w1=(xl+1)*(xl+2)//2   # unit part of pi_{l+2}/pi_l /2  (times 2)
        q1p=(xl+3)
        for sig in product([1,-1],repeat=4):
            R=set()
            for a in product([0,1],repeat=4):
                s=a[0]*sig[0]*1+a[1]*sig[1]*q1+2*w1*(a[2]*sig[2]*1+a[3]*sig[3]*q1p)
                if s%2: R.add(s%8)
            key=(X%16,min(J1,4),sig)
            res.setdefault(key,set()).update([frozenset(R)])
bad={k:v for k,v in res.items() if any(len(r)<4 for r in v)}
good={k for k in res if k not in bad}
print("configs",len(res),"bad",len(bad))
for k in sorted(bad): print(k,[sorted(r) for r in bad[k]])
