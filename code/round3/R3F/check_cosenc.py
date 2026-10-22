"""check_cosenc.py -- validate ivshell's cos(pi r/M) enclosures against mpmath (60 digits).
usage: python3 check_cosenc.py BINARY NPOINTS SEED"""
import sys, random, subprocess
from mpmath import mp, mpf, cos, pi
mp.dps = 60
binary, npts, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
random.seed(seed)
bad = 0; tot = 0; maxw = 0.0
Ms = [3, 5, 7, 13, 11**8, 13**7, 13**8, 7**12, 11**9, 2**52 - 1, 5**22]
for M in Ms:
    rs = sorted(set(r for r in [0, 1, 2, M // 2, max(0, M // 2 - 1), M // 4, M // 3, M // 6] +
                    [random.randrange(0, M // 2 + 1) for _ in range(npts)] if r <= M // 2))
    for i in range(0, len(rs), 200):
        chunk = rs[i:i + 200]
        out = subprocess.run([binary, "test", str(M)] + [str(r) for r in chunk], capture_output=True, text=True, check=True).stdout.split("\n")
        for line in out:
            if not line.strip(): continue
            Mm, r, lo, hi = line.split()
            lo = float.fromhex(lo); hi = float.fromhex(hi); r = int(r)
            tv = cos(pi * mpf(r) / M)
            tot += 1
            if not (mpf(lo) <= tv <= mpf(hi)): bad += 1; print("FAIL", M, r, lo, hi, tv)
            maxw = max(maxw, hi - lo)
print(f"binary={binary} points={tot} failures={bad} max_width={maxw:.3e}")
