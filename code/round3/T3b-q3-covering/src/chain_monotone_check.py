#!/usr/bin/env python3
"""chain_monotone_check.py (2026-10-20) -- sanity check of the reach of note Prop. 10.14 from a certified Cov(p,t,H0):
(a) p !| H: Cov(H) => Cov(H+1);  (b) 1 <= v_p(H) <= L_p, H+p < p^t: Cov(H) => Cov(H+p).
Reach(H0) is computed literally; then small cases are decided EXACTLY (numpy DP over Z/p^M, all unit classes K' mod p^c)
to show that an H outside the reach may fail although H0 holds (so 'every H in [H0, p^{L_p+1}]' is not a consequence)."""
import numpy as np
def vf(n,p):
    s=0
    while n: n//=p; s+=n
    return s
def vp(n,p):
    v=0
    while n%p==0: n//=p; v+=1
    return v
def reach(p,t,H0,Lp):
    R={H0}; stack=[H0]
    while stack:
        H=stack.pop()
        if H%p and H+1<=p**t and H+1 not in R: R.add(H+1); stack.append(H+1)
        if H%p==0 and 1<=vp(H,p)<=Lp and H+p<p**t and H+p not in R: R.add(H+p); stack.append(H+p)
    return R
def cov(p,t,H):
    c=vf(H-1,p); M=t+c; Q=p**M; pc=p**c; bad=[]
    for Kp in range(1,pc) if c else [1]:
        if Kp%p==0: continue
        y=[1]
        for i in range(1,H): y.append(y[-1]*(p**t*Kp-(H-i))%Q)
        S=np.zeros(Q,dtype=bool); S[0]=True
        for a in y: S=S|np.roll(S,a%Q)
        if not S.all(): bad.append((Kp,int((~S).sum())))
    return bad
for (p,t,H0,Lp) in [(7,3,19,2),(13,3,19,2),(13,2,10,2)]:
    R=reach(p,t,H0,Lp)
    print(f"p={p} t={t} from Cov({p},{t},{H0}), L_p={Lp}: reach = {sorted(R)[:12]} ... (size {len(R)}, max {max(R)}); multiples of p reached up to {max(h for h in R if h%p==0) if any(h%p==0 for h in R) else None}")
    for H in sorted(set(range(H0,H0+p+3))|{h for h in [p**2,p**2+1,p**2+p] if h<p**t}):
        if p**(t+vf(H-1,p))>4*10**6: continue
        bad=cov(p,t,H)
        print(f"   Cov({p},{t},{H}): {'HOLDS' if not bad else 'FAILS at '+str(bad[:3])}   in reach: {H in R}")
