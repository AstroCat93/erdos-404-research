# convert l2ref output (S_k) to C_k = p^k S_k / 4^M exactly; print C_k with 10 digits
import sys, re
from fractions import Fraction as F
cur=None
for line in open(sys.argv[1]):
    m=re.match(r"p=(\d+) N0=(\d+) kmax=(\d+) e0=(\d+) M=(\d+)",line)
    if m: p,N0=int(m.group(1)),int(m.group(2)); cur=(p,N0); rows=[]; continue
    m=re.match(r"k=(\d+) M=(\d+) S=(\d+)",line)
    if m and cur:
        k,M,S=int(m.group(1)),int(m.group(2)),int(m.group(3))
        C=F(p**k*S,4**M)
        print(f"p={p} N0={N0} k={k} C_k={float(C):.10f} C_k-1={float(C-1):.6e}")
