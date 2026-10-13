#!/usr/bin/env python3
"""ck_indep_search.py -- tests the remark after R3M Prop B ("the offspring numbers X_e = m_W(beta_e(phi_e - w)) of
two parents are never independent when |P| >= 2 and chi^2_W > 0") in the abstract: searches F: Z/9 -> {0,1,2},
nonconstant with non-uniform mod-3 class sums (so the mod-p shell is nonzero), and an affine bijection
w -> b w + c of Z/9 such that F(w) and F(b w + c) are independent for uniform w.  Second check_R3M instance."""
import itertools
from fractions import Fraction
units=[1,2,4,5,7,8]
found=0
for F in itertools.product(range(3),repeat=9):
    if len(set(F))==1: continue
    cls=[F[a]+F[a+3]+F[a+6] for a in range(3)]
    if len(set(cls))==1: continue
    vals=sorted(set(F))
    pm={v:F.count(v) for v in vals}
    for b in units:
        for c in range(9):
            if b==1 and c==0: continue
            joint={}
            for w in range(9):
                k=(F[w],F[(b*w+c)%9]); joint[k]=joint.get(k,0)+1
            if all(joint.get((u,v),0)*9==pm[u]*pm[v] for u in vals for v in vals):
                found+=1
                if found<=3: print("example F=",F,"b=",b,"c=",c)
print("independent configurations found:",found)
