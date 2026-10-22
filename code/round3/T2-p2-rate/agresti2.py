import random, sys
from agresti import agresti
random.seed(11)
Gs=[16,32,64,128,256,512,1024,2048]
mc={16:0.15166,32:0.101594,64:0.064165,128:0.037699,256:0.020518,512:0.010682,1024:0.005623,2048:0.00266}
xs=[random.getrandbits(200)&~1 for _ in range(3000)]
A={G:[agresti(x,G) for x in xs] for G in Gs}
for kap in [1.0,2.0,2.6,3.0]:
    row=[]
    for G in Gs:
        p=sum(min(1.0,kap/a) for a in A[G])/len(xs)/2
        row.append('%d:%.4f(%.2f)'%(G,p,p/mc[G]))
    print('kappa',kap,' '.join(row))
# natural numbers: predicted N(A,G) vs observed (T4 survivors_NAG)
obs={256:{256:5,512:5,1024:2,2048:1,4094:1},1024:{256:15,512:11,1024:6,2048:4,4094:2},4096:{256:85,512:40,1024:20,2048:13,4094:5}}
for kap in [2.0,2.6]:
  for Amax in [256,1024,4096]:
    out=[]
    for G in [64,128,256,512,1024,2048,4094]:
        pred=sum(min(1.0,kap/agresti(a,G)) for a in range(2,Amax+1,2))
        out.append('%d:%.1f/%s'%(G,pred,obs[Amax].get(G,'-')))
    print('kappa',kap,'A',Amax,' '.join(out))
