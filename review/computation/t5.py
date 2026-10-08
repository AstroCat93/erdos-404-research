import numpy as np
from core import vfact
def full_classes(k,p=3):
    M=p**k
    J=1
    while vfact(J,p)<k: J+=1   # pi_j with j>=J vanish mod p^k
    res=[]
    for N in range(M):
        arr=np.zeros(M,bool); arr[0]=True
        pr=1
        arr|=np.roll(arr,1)  # pi_0=1
        for j in range(1,J):
            pr=pr*(N+j)%M
            if pr: arr|=np.roll(arr,pr)
        if arr.all(): res.append(N)
    return res
import sys
for k in range(4,10):
    f=full_classes(k)
    print(k,len(f),sorted(set(N%81 for N in f)),flush=True)
