import math
from agresti import agresti
kap=2.6
def pred(Amax,G): return sum(min(1.0,kap/agresti(a,G)) for a in range(2,Amax+1,2))
for Amax in [256,4096]:
    prev=None
    for G in [4096,8192,16384,32768,65536,131072,262144] if Amax==4096 else [256,1024,4096,16384,65536,262144,1048576]:
        p=pred(Amax,G)
        le='' if prev is None else ' local exponent %.3f'%(-math.log(p/prev[1])/math.log(G/prev[0]))
        print('A',Amax,'G',G,'pred N %.3f'%p, le); prev=(G,p)
