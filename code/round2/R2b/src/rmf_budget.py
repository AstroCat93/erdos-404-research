# Random-model Fourier budget S(p,t,H=p^D) = sum_d (p^d-p^{d-1}) (2/pi)^{n_d}, exact n_d.
# Under hypothesis RMF(p,C): sum_{xi!=0} prod|cos| <= C*S, so C*S<1 certifies Cov(p,t,p^D).
import math, sys
from mpmath import mp, mpf, log
mp.dps=30
def vfact(n,p):
    s=0
    while n: n//=p; s+=n
    return s
def U(d,p,limit):
    # number of i < limit with v(i!) < d
    i=0
    while i<limit and vfact(i,p)<d: i+=1
    return i
def budget(p,t,D):
    H=p**D; c=vfact(H-1,p); q=mpf(2)/mp.pi
    low=mpf(0)
    for d in range(1,c+1):
        nd=U(d,p,H); low+= (mpf(p)**d-mpf(p)**(d-1))*q**nd
    # top: d=c+1..t+c, n_d=H
    top=(mpf(p)**(t+c)-mpf(p)**c)*q**H
    return low, top, c
for p in [5,7,11,13,17]:
    rho=p*(2/math.pi)**(p-1); kap=math.log(math.pi/2)-math.log(p)/(p-1)
    print(f"p={p} rho~={rho:.4f} kappa_p={kap:.4f}")
    for D in range(1,5):
        if p**D>40000: break
        low,top1,c=budget(p,D+1,D)
        # largest t with top <= low (i.e., top(t) small): top(t)=p^{t+c}(2/pi)^H approx
        H=p**D
        # t_max(C): C*(low+top)<1
        res=[]
        for C in [1,2,3,5,10]:
            if C*low>=1: res.append((C,None)); continue
            eps=1/mpf(C)-low
            # p^{t+c} q^H <= eps  -> t <= (log eps - H log q)/log p - c
            tm=int(math.floor(float((log(eps)-H*log(mpf(2)/mp.pi))/log(p)) - c))
            res.append((C,tm))
        print(f"   D={D} H={H} c={c} low={float(low):.4g}  t_max for C in [1,2,3,5,10] (need D<t<=t_max): {res}")
