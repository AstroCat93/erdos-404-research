# direct truncated summation of theta_p (no closed-form tail) as a cross-check of theta_ref.py
import mpmath as mp, sys
mp.mp.dps=30
for p in [3,5,13]:
    cnt={}; 
    for l in open(f"out/gblock_{p}.txt"):
        if l.startswith("j="): a,b=l.split(); cnt[int(a[2:])]=int(b[4:])
    s=mp.mpf(0)
    for j in range(0,23):
        g=mp.mpf(p)**(j+1)*cnt[j+1]/mp.mpf(4)**p
        s+=(1-mp.mpf(1)/p)*mp.mpf(p)**(-j)*mp.log(g)/mp.log(p)
    print(p, mp.nstr((p-1)*s/p,15), "(truncated at j=22; tail < p^-22*25)")
