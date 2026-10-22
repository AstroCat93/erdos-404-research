# c_p (max over units xi of prod_{r<p}|cos(pi xi r!/p)|), Lemma 11.54 geometric mean, I_p/(2/pi)^p for p=5,7
import mpmath as mp, numpy as np, math
mp.mp.dps=30
def primes(n): return [q for q in range(3,n+1) if all(q%d for d in range(2,int(q**.5)+1))]
for p in primes(53):
    fr=[math.factorial(r)%p for r in range(p)]
    vals=[]
    for xi in range(1,p):
        prod=mp.mpf(1)
        for f in fr: prod*=abs(mp.cos(mp.pi*xi*f/p))
        vals.append(prod)
    cp=max(vals); gm=mp.exp(sum(mp.log(v) for v in vals)/(p-1))
    print(f"p={p} c_p={mp.nstr(cp,8)} c_p/(2/pi)^p={mp.nstr(cp/(2/mp.pi)**p,4)} geomean*2^p={mp.nstr(gm*2**p,15)}")
for p in [5,7]:
    e=[(-1)**u*math.factorial(p-1)//math.factorial(u) for u in range(p)]
    for Npts in [2*10**7, 4*10**7]:
        tot=0.0; chunk=10**6
        for s in range(0,Npts,chunk):
            th=(np.arange(s,min(s+chunk,Npts))+0.5)/Npts
            pr=np.ones_like(th)
            for x in e: pr*=np.abs(np.cos(np.pi*x*th))
            tot+=pr.sum()
        Ip=tot/Npts
        print(f"p={p} N={Npts} I_p={Ip:.10f} I_p/(2/pi)^p={Ip/(2/math.pi)**p:.6f}")
