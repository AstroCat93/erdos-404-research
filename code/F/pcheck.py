#!/usr/bin/env python3
"""P(a,p,N): exists a = a_1 < ... < a_k < N with p^{v_p(N!)} | sum a_i!.  Exact DP over residues
(sets of residues mod p^{e(N)}), returns a witness set for each a < N for which P holds."""
import sys, math
def vp(n,p):
    v=0
    while n%p==0: n//=p; v+=1
    return v
def P(a,p,N):
    e=sum(vp(k,p) for k in range(1,N+1)); M=p**e
    reach={math.factorial(a)%M:(a,)}
    for n in range(a+1,N):
        f=math.factorial(n)%M
        new=dict(reach)
        for r,w in reach.items():
            s=(r+f)%M
            if s not in new: new[s]=w+(n,)
        reach=new
    return e, reach.get(0)
p,N=int(sys.argv[1]),int(sys.argv[2])
for a in range(1,N):
    e,w=P(a,p,N)
    print(f"p={p} N={N} e(N)={e} a={a}: P={'yes' if w else 'no'}" + (f" witness={w} v_p(sum)={vp(sum(math.factorial(x) for x in w),p)}" if w else ""))
