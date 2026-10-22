# Test of the BPVE/Agresti predictor on natural numbers in the regime G = lambda * a (G >> a for lambda >> 1),
# using T4's exact capped table g_2(a), a <= 4096, cap 4094 (file surv_cap4094.txt). kappa = 2.6 fitted on Haar MC (G>=512).
import sys, math
from agresti import agresti
g={}
for line in open(sys.argv[1]):
    if line.startswith('#'): continue
    a,v=line.split()[:2]; g[int(a)]=int(v)
cap=4094; kap=2.6
print('lambda  #a  observed  predicted(kappa=2.6)  Poisson-sd')
for lam in [0.25,0.5,1,2,4,8,16,32,64]:
    As=[a for a in g if a%2==0 and lam*a<=cap and a>=16]
    obs=sum(1 for a in As if g[a]>=lam*a)
    pred=sum(min(1.0,kap/agresti(a,math.ceil(lam*a))) for a in As)
    print(f"{lam:6} {len(As):5} {obs:6} {pred:10.2f} {math.sqrt(pred):8.2f}")
