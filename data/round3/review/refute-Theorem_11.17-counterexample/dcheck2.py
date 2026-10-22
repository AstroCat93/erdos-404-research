import sys, time
sys.path.insert(0, sys.argv[1])
from dcheck import D
for (p,w,K) in [(2,3,16),(2,5,16),(3,2,10),(5,2,8),(7,2,6),(3,4,12),(5,3,8)]:
    t=time.time(); print(p,w,K,'%.10f'%D(p,w,K),'%.0fs'%(time.time()-t),flush=True)
