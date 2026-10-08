# Check Thm 3.12(a): at actual N*=p^t K'' (p∤K''), block {n!/p^{v((N*-H)!)}: N*-H<=n<N*} = U * y_i(K'' mod p^c) mod p^{t+c},
# and jump v(N*!)-v((N*-H)!) = t+c.
from core import vp, vfact
from cov import ys
import random
bad=0; cnt=0
for p in (3,5,7):
    for t in (1,2,3):
        for H in range(1,min(p**t,40)+1):
            c=vfact(H-1,p)
            for Kpp in random.sample([k for k in range(1,400) if k%p],12):
                N=p**t*Kpp
                if N-H<1: continue
                A=N-H
                jump=vfact(N,p)-vfact(A,p)
                if jump!=t+c: bad+=1; print("jump",p,t,H,Kpp); continue
                M=p**(t+c)
                # actual block normalized by A! (unit factor U(A) ignored): prod_{s=1}^{i}(A+s)
                act=[1];pr=1
                for i in range(1,H): pr*= (A+i); act.append(pr%M)
                Mr,y=ys(p,t,H,Kpp % (p**c) if c else 1)
                # with c=0 y doesn't depend on K at all mod p^t (K' only enters via p^t K')
                cnt+=1
                if act!=y: bad+=1; print("mismatch",p,t,H,Kpp)
print("Thm3.12(a) reduction: %d cases, %d failures"%(cnt,bad))
