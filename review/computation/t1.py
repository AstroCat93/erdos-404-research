from core import *
# brute vs DP consistency on small cases
import random
bad=0
for p in (2,3,5,7):
    for a in range(1,60):
        for K in (1,2,3,4) if p>2 else (1,2,3,4,5,6,7,8):
            if p**K > 5000: continue
            x=g_exact(a,p,K); y=g_brute(a,p,K)
            if x!=y: bad+=1; print("MISMATCH",p,a,K,x,y)
print("brute-vs-dp mismatches",bad)
# known values f(a,p)=v(a!)+g
known=[(1,2,0),(2,2,254),(3,2,1),(4,2,6),(5,2,3),(6,2,133),(14,2,1533),(38,2,828),
       (3,3,3),(39,3,25),(700,3,363),(110,5,30),(236,5,61),(42,7,7),(4,7,0),(6,7,0),(113,11,11),(163,13,13),(949,3,488)]
for a,p,f in known:
    K=f-vfact(a,p)+2
    g=g_exact(a,p,K)
    print(a,p,"claimed f",f,"computed f",vfact(a,p)+g, "OK" if vfact(a,p)+g==f else "DIFF")
