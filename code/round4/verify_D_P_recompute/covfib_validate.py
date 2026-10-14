#!/usr/bin/env python3
"""Validate covfib.c against covchk.c (itself validated against numpy brute force):
per-class missing counts must agree exactly, for several fibre levels k."""
import subprocess, sys
CF, CC = sys.argv[1], sys.argv[2]
def parse(out):
    r = {}
    for l in out.splitlines():
        if l.startswith("K="):
            f = dict(kv.split("=") for kv in l.split() if "=" in kv)
            r[int(f["K"])] = int(f["missing"])
    return r
cases = [(7,3,18,[1,2]),(7,3,19,[1,2]),(7,4,25,[1,2,3]),(7,4,26,[2]),(5,3,19,[1,2]),(5,4,25,[2,3]),(13,2,14,[1]),
         (13,5,32,[1,2]),(11,5,30,[1,2]),(13,6,35,[2]),(3,3,26,[1,2])]
ok = True
for p,t,H,ks in cases:
    base = parse(subprocess.run([CC,str(p),str(t),str(H)],capture_output=True,text=True,check=True).stdout)
    for k in ks:
        r = parse(subprocess.run([CF,str(p),str(t),str(H),str(k)],capture_output=True,text=True,check=True).stdout)
        mism = sum(1 for K in base if r.get(K) != base[K])
        nf = sum(1 for K in base if base[K])
        print(f"Cov({p},{t},{H}) k={k}: classes {len(base)}, failing classes {nf}, total missing {sum(base.values())}, mismatches {mism}")
        ok &= (mism == 0 and len(r) == len(base))
# single classes at the largest modulus covchk can do: the known failing class and two covered ones
for (p,t,H,K) in [(7,6,33,5),(7,6,34,5),(7,6,33,1),(13,7,38,1) if False else (11,6,32,1)]:
    a = parse(subprocess.run([CC,str(p),str(t),str(H),"one",str(K)],capture_output=True,text=True,check=True).stdout)
    for k in (1,2):
        b = parse(subprocess.run([CF,str(p),str(t),str(H),str(k),"one",str(K)],capture_output=True,text=True,check=True).stdout)
        print(f"Cov({p},{t},{H}) K={K} k={k}: covchk missing {a[K]}, covfib missing {b[K]}")
        ok &= (a[K] == b[K])
print("VALIDATION", "OK" if ok else "FAILED")
