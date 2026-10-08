import numpy as np, time
from core import vfact
p=3
def isfull(N,k):
    M=p**k; J=1
    while vfact(J,p)<k: J+=1
    arr=np.zeros(M,bool); arr[0]=True; arr|=np.roll(arr,1); pr=1
    for j in range(1,J):
        pr=pr*(N+j)%M
        if pr: arr|=np.roll(arr,pr)
    return bool(arr.all())
# exhaustive at k=8 as base (validated by t5), then lift
M8=3**8
cur=[N for N in range(M8) if isfull(N,8)]
print(8,len(cur),sorted(set(N%81 for N in cur)))
t=time.time()
for k in range(9,15):
    cand=[N+i*3**(k-1) for N in cur for i in range(3)]
    cur=[N for N in cand if isfull(N,k)]
    print(k,len(cur),sorted(set(N%81 for N in cur)),"density %.5f"%(len(cur)/3**k),"%.0fs"%(time.time()-t),flush=True)
    if not cur: break
