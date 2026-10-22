# Independent recomputation of Gamma_p(j), J0, dist_p(j), theta_p, theta_set for Thm 11.38.
# Exact integer arithmetic for Gamma; theta via Fraction-based bounds with mpmath for logs (high precision).
import sys
from fractions import Fraction
from math import factorial
import mpmath as mp
mp.mp.dps=50
def run(p):
    e=[(-1)**u*factorial(p-1)//factorial(u) for u in range(p)]
    # distribution of W=sum eta_u e_u, weights 1,2,1 (total 4^p)
    dist={0:1}
    for x in e:
        nd={}
        for v,c in dist.items():
            for s,w in ((-1,1),(0,2),(1,1)):
                nd[v+s*x]=nd.get(v+s*x,0)+c*w
        dist=nd
    tot=4**p
    assert sum(dist.values())==tot
    # subset sums
    ss={0}
    for x in e: ss|={v+x for v in ss}
    G={}; J0=None
    for j in range(1,40):
        q=p**j
        c=sum(cnt for v,cnt in dist.items() if v%q==0)
        G[j]=Fraction(q*c,tot)-1
        if J0 is None and c==dist.get(0,0): J0=j
        if J0 is not None and j>=J0+2: break
    D={j:len({v%p**j for v in ss}) for j in range(1,J0+3)}
    # theta: sum_{j>=0} (1-1/p)p^{-j} f(j), f(j)=log_p(1+G(j+1)); for j+1>=J0: f=log_p(1.5*2^-p)+j+1
    c0=mp.log(mp.mpf(3)/2/2**p)/mp.log(p)
    F=mp.mpf(0)
    for j in range(0,J0-1):
        F+=(1-mp.mpf(1)/p)*mp.mpf(p)**(-j)*mp.log(mp.mpf((1+G[j+1]).numerator)/(1+G[j+1]).denominator)/mp.log(p)
    # tail j>=J0-1: sum (1-1/p)p^{-j}(c0+j+1)
    t=J0-1
    S0=sum((1-mp.mpf(1)/p)*mp.mpf(p)**(-j) for j in range(t,t+1))  # placeholder
    # closed forms: sum_{j>=t} (1-1/p)p^{-j} = p^{-t};  sum_{j>=t} (1-1/p) j p^{-j} = p^{-t}(t + 1/(p-1))
    F+=mp.mpf(p)**(-t)*(c0+1)+mp.mpf(p)**(-t)*(t+mp.mpf(1)/(p-1))
    theta=(1-mp.mpf(1)/p)*F
    # brute check of tail by direct sum
    Fb=mp.mpf(0)
    for j in range(0,400):
        g = G[j+1] if j+1 in G and j+1<J0 else None
        val = mp.log(mp.mpf(g.numerator+g.denominator)/g.denominator)/mp.log(p) if g is not None else c0+j+1
        Fb+=(1-mp.mpf(1)/p)*mp.mpf(p)**(-j)*val
    # theta_set
    Fs=mp.mpf(0)
    for j in range(0,400):
        dj = D[j+1] if j+1 in D else None
        if dj is None or j+1>=J0: dj_val = mp.mpf(3)*2**(p-2)  # all distinct once p^j exceeds range
        else: dj_val=mp.mpf(dj)
        if j+1 in D: dj_val=mp.mpf(D[j+1])
        Fs+=(1-mp.mpf(1)/p)*mp.mpf(p)**(-j)*(j+1-mp.log(dj_val)/mp.log(p))
    return G,J0,D,theta,(1-mp.mpf(1)/p)*Fb,(1-mp.mpf(1)/p)*Fs,max(j for j in D if D[j]==p**j) if any(D[j]==p**j for j in D) else 0
for p in [2,3,5,7,11,13,17,19]:
    G,J0,D,th,thb,ths,L=run(p)
    print(p,"G1=",G[1],"J0=",J0,"L=",L,"theta=",mp.nstr(th,8),"direct=",mp.nstr(thb,8),"1-theta_set=",mp.nstr(1-ths,8),flush=True)
