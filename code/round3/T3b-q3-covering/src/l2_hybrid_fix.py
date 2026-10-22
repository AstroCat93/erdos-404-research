#!/usr/bin/env python3
"""l2_hybrid_fix.py (2026-10-20) -- CORRECTION of the fibre-hybrid column of l2_study.py.
For a window y_i mod p^M, fibre level k=c, F=p^{M-k}: B_T = SET of carries (low subset sums == T mod p^k, divided by p^k),
nu_U = subset-sum law of the high elements / p^k on Z/F.  Exact (Chebyshev, PROVED):
   misses in fibre T  <=  Cheb_T := F * sum_{eta != 0} |B_T-hat(eta)|^2 |nu_U-hat(eta)|^2,
   B_T-hat = transform of the uniform measure on B_T.  Two rigorous relaxations and the heuristic of l2_study.py:
   CS_T  := F * (F/|B_T| - 1) * sup_{eta != 0} |nu_U-hat(eta)|^2    (Cauchy-Schwarz with Parseval sum_{eta!=0}|B_T-hat|^2 = F/|B_T|-1)  [proved, >= Cheb_T]
   Hyb_T := (F/|B_T| - 1) * sum_{eta != 0} |nu_U-hat(eta)|^2        (l2_study.py; equals E Cheb_T for a RANDOM set B_T; NOT an upper bound in general)
Prints max over T of each, and the number of fibres T where Hyb_T < Cheb_T (i.e. where the old 'criterion' would be unsound)."""
import math, numpy as np
def vf(n,p):
    s=0
    while n: n//=p; s+=n
    return s
def study(p,t,H,Kp):
    c=vf(H-1,p); M=t+c; Q=p**M
    y=[1]
    for i in range(1,H): y.append(y[-1]*(p**t*Kp-(H-i))%Q)
    v=[vf(H-1,p)-vf(H-1-i,p) for i in range(H)]
    k=c; PK=p**k; F=Q//PK
    lo=[y[i] for i in range(H) if v[i]<k]; hi=[(y[i]//PK)%F for i in range(H) if v[i]>=k]
    S=np.zeros(Q,dtype=bool); S[0]=True
    for a in lo: S = S | np.roll(S,a%Q)
    idx=np.flatnonzero(S)
    NU=np.zeros(F); NU[0]=1.0
    for w in hi: NU = NU + np.roll(NU,w)
    nuh=np.fft.fft(NU)/2.0**len(hi); a2=np.abs(nuh)**2; a2[0]=0.0
    s2=float(a2.sum()); sup2=float(a2.max())
    # exact miss count per fibre for cross-check
    N=np.zeros(Q); N[0]=1.0
    for a in y: N = N + np.roll(N,a%Q)
    worstC=worstCS=worstH=0.0; unsound=0; worstmiss=0
    for T in range(PK):
        B=idx[idx%PK==T]//PK
        if len(B)==0: return None
        ind=np.zeros(F); ind[B]=1.0/len(B)
        bh=np.abs(np.fft.fft(ind))**2; bh[0]=0.0
        cheb=F*float((bh*a2).sum()); cs=F*(F/len(B)-1.0)*sup2; assert cheb<=cs*(1+1e-9)+1e-9; hyb=(F/len(B)-1.0)*s2
        miss=int((N[T::PK]==0).sum())
        assert miss<=cheb+1e-6, (T,miss,cheb)
        worstC=max(worstC,cheb); worstCS=max(worstCS,cs); worstH=max(worstH,hyb); worstmiss=max(worstmiss,miss)
        if hyb<cheb: unsound+=1
    return dict(c=c,M=M,F=F,nlo=len(lo),nhi=len(hi),Cheb=worstC,CS=worstCS,Hyb=worstH,sup2=sup2,s2=s2,unsound=unsound,PK=PK,miss=worstmiss)
cases=[(13,3,19,1),(13,3,18,1),(13,4,24,1),(11,4,22,1),(11,3,18,1),(7,4,26,1),(7,5,28,1),(11,5,30,1),(7,3,19,1)]
print("p t H K' | c M F nlo nhi | max misses/fibre | max_T Cheb_T (proved bound) | max_T CS_T (proved) | max_T Hyb_T (old column, heuristic) | sup|nuU|^2 sum|nuU|^2 | #fibres with Hyb_T < Cheb_T / p^c")
for (p,t,H,Kp) in cases:
    r=study(p,t,H,Kp)
    if r is None: print(p,t,H,Kp,'empty fibre'); continue
    print(f"{p} {t} {H} {Kp} | {r['c']} {r['M']} {r['F']} {r['nlo']} {r['nhi']} | {r['miss']} | {r['Cheb']:.4g} | {r['CS']:.4g} | {r['Hyb']:.4g} | {r['sup2']:.3g} {r['s2']:.3g} | {r['unsound']}/{r['PK']}")
