# Monte Carlo of Prop 11.26 (int_{C cap Gamma_*} Z_n <= 2^{L-1+max(0,L+1-k)}) and E[Y_0 1_C] <= E_C.
# Reported as unnormalised Haar integrals (= mu(C) * conditional mean).  Also: max over samples of Z_n, rho.
import random, time, sys, math
from fractions import Fraction
from common import *
rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 3)
NS=int(sys.argv[2]) if len(sys.argv)>2 else 3000
t0=time.time()
for cls in ("C0","C2","C6"):
    k,r0,L,l0,sL,EC,Vc=CLASSES[cls]
    bound26=2**(L-1+max(0,L+1-k))
    for n in (19,24,30):
        sz=0.0; sy=0.0; sz2=0.0; maxrho=0; lamhist={}
        for _ in range(NS):
            x=rand_in_class(cls,rng)
            m=V(x,n); Mn=Mx(x,n)
            gstar = m>=max(Vc,2*L+1,L+k) and m-L>Mn
            g0 = 2*Mx(x,n+l0)+3*L+3<=m
            if g0: assert gstar, "Gamma_0 not subset of Gamma_*"
            if not gstar: continue
            ps,Vs=alive_paths(x,n)
            Z=len(ps)*2.0**(m-n)
            sz+=Z; sz2+=Z*Z
            if g0:
                tot=Fraction(0)
                for bits,S,dS in ps:
                    r,lam=rho(x,n,S,dS); tot+=r; maxrho=max(maxrho,r)
                    lamhist[lam]=lamhist.get(lam,0)+1
                    assert lam<=L
                sy+=float(tot)*2.0**(m-n)
        mu=2.0**-k
        ez=mu*sz/NS; se=mu*math.sqrt(max(sz2/NS-(sz/NS)**2,0)/NS)
        print(f"{cls} n={n}: int_(C∩Γ*) Z_n ≈ {ez:.4f} ± {se:.4f} (bound {bound26});  E[Y0 1_C] ≈ {mu*sy/NS:.4f} (E_C={EC}); max rho {float(maxrho)}; slopes {dict(sorted(lamhist.items()))}")
print("time %.1fs"%(time.time()-t0))
