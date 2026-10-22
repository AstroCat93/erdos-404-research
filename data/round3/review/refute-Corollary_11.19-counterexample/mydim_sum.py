"""Combine histogram files from mydim (possibly several chunks) into D_p(w,K) with mpmath (40 digits),
and give a rigorous-ish enclosure: each log is computed at 40 digits, so error << 1e-30."""
import sys, mpmath as mp
mp.mp.dps = 40
p, w, K = map(int, sys.argv[1:4])
hist = {}
for fn in sys.argv[4:]:
    for line in open(fn):
        if line.startswith('N '):
            _, n, c = line.split(); hist[int(n)] = hist.get(int(n), 0) + int(c)
tot = sum(hist.values())
assert tot == p**(K-1), (tot, p**(K-1))
S = mp.fsum(c*mp.log(n)/mp.log(p) for n, c in hist.items())
D = mp.mpf(p-1)/(w*p) * S / tot
print(f"p={p} w={w} K={K} types={tot} D={mp.nstr(D,20)} minN={min(hist)} maxN={max(hist)}")
