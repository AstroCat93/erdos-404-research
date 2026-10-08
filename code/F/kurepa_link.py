#!/usr/bin/env python3
"""Kurepa link: S_p := sum_{n>=1} n! in Z_p (converges p-adically).  S_p == !p - 1 (mod p).
For primes p < LIM with p | sum_{k=1}^{p-1} k!, compute v_p(S_p) exactly (mod p^3 suffices unless >= 3).
f(1,p) >= v_p(S_p) trivially (take A = [1, N] with N large)."""
import sys
from sympy import primerange
LIM=int(sys.argv[1]) if len(sys.argv)>1 else 20000
hits=[]
for p in primerange(3,LIM):
    s=0; f=1
    for k in range(1,p):
        f=f*k%p; s=(s+f)%p
    if s==0: hits.append(p)
print("primes p<%d with p | 1!+...+(p-1)!:"%LIM, hits)
for p in hits:
    K=4; M=p**K
    s=0; f=1
    # n! == 0 mod p^K once n >= K*p
    for n in range(1,K*p):
        f=f*n%M; s=(s+f)%M
    v=0; t=s
    while t%p==0 and v<K: t//=p; v+=1
    print(f"p={p}: v_p(sum_(n>=1) n!) = {v if v<K else '>= %d'%K}")
