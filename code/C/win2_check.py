"""Independent check of win2: window elements computed from exact factorials (big ints)."""
import sys
from math import factorial
from core import vp_fact
p, j = int(sys.argv[1]), int(sys.argv[2])
for t0 in range(1, p):
    for t in (t0, t0 + p, t0 + 2 * p):
        m = p ** j * t - 1
        N, H = p * (m - 1), 2 * p
        D = vp_fact(N + H, p) - vp_fact(N, p)
        assert D == j + 2
        M = p ** D
        F = factorial(N)
        els = [(factorial(n) // F) % M for n in range(N, N + H)]
        S = {0}
        for x in els:
            S |= {(s + x) % M for s in S}
        print("t=%d (t0=%d) covered=%d of %d %s" % (t, t0, len(S), M, "FULL" if len(S) == M else "partial"))
