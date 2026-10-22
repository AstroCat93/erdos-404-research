#!/usr/bin/env python3
"""Implementation 2 of the Lemma 3 certificates (shares no code with cert_classes.py):
expands S_e(X) as an integer polynomial with sympy, reduces coefficients, evaluates by Horner,
and decides 2-adic valuations with gmpy2. Same five statements."""
import sympy as sp, gmpy2
from itertools import product
X=sp.symbols('X')
def polys(n):
    out=[sp.Integer(1)]
    for j in range(1,n): out.append(sp.expand(out[-1]*(X+j)))
    return [sp.Poly(q,X) for q in out]
def val(a): return 99 if a==0 else int(gmpy2.bit_scan1(gmpy2.mpz(a)))
def check(res,mod,n,k,slope):
    P=polys(n); viol=0; q=0
    for bits in product((0,1),repeat=n-1):
        S=P[0]
        for j,b in enumerate(bits,1):
            if b: S=S+P[j]
        Sd=S.diff(X)
        cs=[int(c) for c in S.all_coeffs()]; ds=[int(c) for c in Sd.all_coeffs()]
        for x in range(res,2**k,mod):
            h=0
            for c in cs: h=(h*x+c)%(2**k)
            if h==0:
                q+=1; t=0
                for c in ds: t=t*x+c
                if slope is None or val(t)!=slope: viol+=1
    return q,viol
for name,a in [("a",(0,8,6,4,1)),("b",(2,16,8,7,3)),("c",(6,16,10,11,3)),("d",(10,16,6,7,None)),("e",(4,8,4,4,None))]:
    q,vi=check(*a); print(name, "qualifying",q,"violations",vi, "OK" if vi==0 else "FAIL")
