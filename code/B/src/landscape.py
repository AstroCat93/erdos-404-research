#!/usr/bin/env python3
"""Dichotomy landscape for odd p: classify every start a in [1, A] as
   BLOCKED   a == -1 mod p                       f(a,p) = v_p(a!)            (trivial)
   EXACT     exhaustive DP (exact_g)             f(a,p) = v_p(a!) + g         (proved)
   GE        witness (search) + independent check f(a,p) >= v_p(a!) + G       (proved)
   OPEN      neither succeeded
usage: landscape.py p A G outcsv [state_cap]
"""
import subprocess, sys, os, time

BASE = os.path.dirname(os.path.abspath(__file__)) + "/.."
p, A, Gt, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
cap = sys.argv[5] if len(sys.argv) > 5 else "100000"
tmpdir = f"{BASE}/data/landscape_tmp_p{p}"
os.makedirs(tmpdir, exist_ok=True)

def vf(n):
    s = 0
    while n:
        n //= p; s += n
    return s

rows = []
t0 = time.time()
with open(out, "w") as fo:
    fo.write("p,a,v_p(a!),status,value,detail\n")
    for a in range(1, A + 1):
        va = vf(a)
        if a % p == p - 1:
            row = (p, a, va, "BLOCKED", 0, "a==-1 mod p; f=v_p(a!)")
        else:
            r = subprocess.run([f"{BASE}/exact_g", str(p), str(a), "40", cap], capture_output=True, text=True).stdout.split()
            st, val, mx = r[3], int(r[4]), r[5]
            if st == "EXACT":
                row = (p, a, va, "EXACT", val, f"DP maxstates={mx}")
            else:
                K = va + Gt
                wf = f"{tmpdir}/w_{a}.txt"
                s = subprocess.run([f"{BASE}/search{p}", str(a), str(K), wf, "96", "12", "8", "20000000", "400"],
                                   capture_output=True, text=True)
                v = subprocess.run([f"{BASE}/verify_bin", str(p), str(a), str(K), wf], capture_output=True, text=True)
                if v.returncode == 0 and "VERIFIED" in v.stdout:
                    row = (p, a, va, "GE", Gt, f"DP {st} at G={val}; witness K={K} verified")
                else:
                    row = (p, a, va, "OPEN", val, f"DP {st} at G={val}; search failed")
                try:
                    os.remove(wf)
                except OSError:
                    pass
        fo.write(",".join(map(str, row)) + "\n")
        fo.flush()
        rows.append(row)
from collections import Counter
c = Counter(r[3] for r in rows)
ex = [r for r in rows if r[3] == "EXACT"]
print(f"p={p} A={A} G={Gt}: {dict(c)}  max exact g = {max((r[4] for r in ex), default=None)}  time {time.time()-t0:.0f}s")
