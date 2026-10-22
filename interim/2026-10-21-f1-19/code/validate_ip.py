#!/usr/bin/env python3
"""validate_ip.py -- cross-validate A' (fibcov_ip) and C' (covchk_ip) against the brute-force
reference publish-erdos404/code/round2/R3/src/brute.py on small instances, all fibre levels k,
comparing the exact number of uncovered residues for each position K. Run with -I."""
import os, sys, subprocess, random
R3 = os.environ.get("ERDOS404_R3_SRC", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "code", "round2", "R3", "src"))  # repo: publish-erdos404/code/round2/R3/src
sys.path.insert(0, R3)
from brute import missing, vfact
BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bin')
def runA(p,t,H,k,Ks):
    out = subprocess.run([os.path.join(BIN,'fibcov_ip'),str(p),str(t),str(H),str(k),'pos']+[str(K) for K in Ks],capture_output=True,text=True).stdout
    res={}
    for line in out.splitlines():
        if line.startswith('A '):
            d=dict(x.split('=') for x in line.split() if '=' in x); res[int(d['K'])]=int(d['missing'])
    return res
def runC(p,t,H,k,Ks):
    out = subprocess.run([os.path.join(BIN,'covchk_ip'),str(p),str(t),str(H),str(k),'pos']+[str(K) for K in Ks],capture_output=True,text=True).stdout
    res={}
    for line in out.splitlines():
        if line.startswith('C '):
            d=dict(x.split('=') for x in line.split() if '=' in x); res[int(d['K'])]=int(d['miss'])
    return res
random.seed(20261012)
cases=[(3,2,9),(3,3,20),(3,3,27),(5,2,10),(5,3,14),(5,3,20),(5,4,22),(5,4,25),(7,2,5),(7,3,15),(7,3,19),(7,4,22),(7,4,26),
       (11,3,14),(11,3,18),(11,4,22),(13,3,16),(13,3,19),(13,4,21),(13,4,24),(17,3,20),(17,3,24),(19,3,22),(2,3,6),(2,4,9),
       (3,4,30),(5,5,30),(7,5,27),(11,5,28)]
nchk=nbad=nfail=0
for (p,t,H) in cases:
    c=vfact(H-1,p); M=t+c
    if p**M > 3*10**8: continue
    pc=p**c
    Ks=[K for K in range(1,p**(c+1)+p) if K%p] if c else [1,2,p+1,2*p+3]
    Ks=sorted(set(random.sample(Ks,min(len(Ks),6))+[1]))
    ref={K:missing(p,t,H,K)[1] for K in Ks}
    for k in range(0,M+1):
        # keep low enumeration bounded
        nlow=sum(1 for i in range(H) if vfact(H-1,p)-vfact(H-1-i,p)<k)
        if nlow>26: continue
        rA=runA(p,t,H,k,Ks); rC=runC(p,t,H,k,Ks)
        for K in Ks:
            nchk+=1
            if ref[K]>0: nfail+=1
            if rA.get(K)!=ref[K] or rC.get(K)!=ref[K]:
                nbad+=1; print("MISMATCH",p,t,H,k,K,"ref",ref[K],"A'",rA.get(K),"C'",rC.get(K))
    print(f"case p={p} t={t} H={H} M={M} done; ref misses {ref}")
print(f"TOTAL comparisons={nchk} failing_cases={nfail} mismatches={nbad}")
