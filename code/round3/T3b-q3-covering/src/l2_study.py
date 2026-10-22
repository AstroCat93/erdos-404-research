#!/usr/bin/env python3
"""l2_study.py -- exact L^1 / L^2 Fourier diagnostics for certified Cov windows (small moduli).
For the window y_i = prod_{s<=i}(p^t K' - (H-s)), i<H, mod p^M (M = t+c):
  N(r) = exact number of subsets with sum == r (numpy DP, exact below 2^53),
  nu-hat(xi) = (1/2^H) sum_r N(r) e(xi r / p^M)  (FFT),
  L1 = sum_{xi != 0} |nu-hat(xi)|,   L2 = p^M sum_{xi != 0} |nu-hat(xi)|^2 = sum_r (N(r)/mean - 1)^2  (Parseval),
  random-model budgets: L1rm = sum_d (p^d-p^{d-1}) (2/pi)^{n_d},  L2rm = p^M sum_d (p^d-p^{d-1}) 2^{-n_d},
  fibre-hybrid at k=c: Hyb = max_T (F/|B_T| - 1) * sum_{eta != 0} |nu_U-hat(eta)|^2  (F = p^{M-c}; B_T = fibre SET of low sums).
Full covering is guaranteed by L1<1 (Fourier inversion), by L2<1 (Chebyshev), or by Hyb<1 (Cauchy-Schwarz on fibres).
"""
import sys, math
import numpy as np
def vf(n,p):
    s=0
    while n: n//=p; s+=n
    return s
def study(p,t,H,Kp):
    c=vf(H-1,p); M=t+c; Q=p**M
    y=[1]
    for i in range(1,H): y.append(y[-1]*(p**t*Kp-(H-i))%Q)
    v=[vf(H-1,p)-vf(H-1-i,p) for i in range(H)]
    N=np.zeros(Q); N[0]=1.0
    for a in y:
        N = N + np.roll(N, a%Q)
    assert abs(N.sum()-2.0**H) < 1e-3*2.0**H
    mean=2.0**H/Q
    nz=int((N==0).sum()); mn=N.min()
    L2=float(((N/mean-1.0)**2).sum())
    nh=np.fft.fft(N)/2.0**H
    L1=float(np.abs(nh[1:]).sum())
    # random model budgets
    nd=lambda d: sum(1 for i in range(H) if v[i]<d)
    L1rm=sum((p**d-p**(d-1))*(2/math.pi)**nd(d) for d in range(1,M+1))
    L2rm=Q*sum((p**d-p**(d-1))*2.0**(-nd(d)) for d in range(1,M+1))
    # fibre hybrid at k=c (if c>=1)
    hyb=None
    if c>=1:
        k=c; PK=p**k; F=Q//PK
        lo=[y[i] for i in range(H) if v[i]<k]; hi=[(y[i]//PK)%F for i in range(H) if v[i]>=k]
        # low sums (set) bucketed by residue mod PK
        S=np.zeros(Q,dtype=bool); S[0]=True
        for a in lo: S = S | np.roll(S,a%Q)
        idx=np.flatnonzero(S)
        NU=np.zeros(F); NU[0]=1.0
        for w in hi: NU = NU + np.roll(NU,w)
        nuh=np.fft.fft(NU)/2.0**len(hi)
        s2=float((np.abs(nuh[1:])**2).sum())
        worst=0.0; minB=None
        for T in range(PK):
            B=idx[idx%PK==T]
            if len(B)==0: worst=float('inf'); continue
            val=(F/len(B)-1.0)*s2
            worst=max(worst,val); minB=len(B) if minB is None else min(minB,len(B))
        hyb=(worst,s2,minB,F,len(lo),len(hi))
    return dict(p=p,t=t,H=H,Kp=Kp,c=c,M=M,Q=Q,minN=mn,zeros=nz,mean=mean,L1=L1,L2=L2,L1rm=L1rm,L2rm=L2rm,hyb=hyb)
cases=[(13,3,19,[1,5,12]),(13,3,18,[1]),(13,4,24,[1,7]),(13,4,23,[1]),(11,4,22,[1,3]),(11,3,18,[1,2]),(7,4,26,[1,2]),(7,5,28,[1]),(11,5,30,[1]),(7,3,19,[1,4])]
print("p t H K' | c M | minN zeros(covered?) | L1 L1rm | L2 L2rm | Hyb(k=c) [sum|nuU|^2, min|B_T|, F, nlo, nhi]")
for (p,t,H,Ks) in cases:
    for Kp in Ks:
        r=study(p,t,H,Kp)
        h=r['hyb']
        hs = "n/a" if h is None else f"{h[0]:.3g} [{h[1]:.3g}, {h[2]}, {h[3]}, {h[4]}, {h[5]}]"
        print(f"{p} {t} {H} {Kp} | c={r['c']} M={r['M']} | minN={r['minN']:.0f} zeros={r['zeros']} {'COVERED' if r['zeros']==0 else 'NOT'} | L1={r['L1']:.4g} L1rm={r['L1rm']:.4g} | L2={r['L2']:.4g} L2rm={r['L2rm']:.4g} | Hyb={hs}")
