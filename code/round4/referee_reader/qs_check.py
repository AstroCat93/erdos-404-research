"""Fresh-reader referee (round 4): recompute q_s(p) as defined in note.md §12.1,
  q_s(p) = p^s max_z P( sum_{r<p} delta_r pi_r(-p) == z mod p^s ),
delta_r i.i.d. with P(0)=1/2, P(+1)=P(-1)=1/4, pi_r(y)=(y+1)...(y+r), pi_0=1.
Exact integer DP (weights 2,1,1; total 4^p). Usage: python3 -I qs_check.py p [p ...]"""
import sys
from fractions import Fraction

def qs(p, s):
    m = p ** s
    vals = []
    y = -p
    acc = 1
    for r in range(p):
        if r > 0:
            acc = acc * (y + r)
        vals.append(acc % m)
    dist = {0: 1}
    for v in vals:
        nd = {}
        for z, c in dist.items():
            for d, w in ((0, 2), (1, 1), (-1, 1)):
                t = (z + d * v) % m
                nd[t] = nd.get(t, 0) + c * w
        dist = nd
    mx = max(dist.values())
    return Fraction(m * mx, 4 ** p)

if __name__ == "__main__":
    for a in sys.argv[1:]:
        p = int(a)
        q1, q2 = qs(p, 1), qs(p, 2)
        print(f"p={p} q1={q1} ({float(q1):.10g}, q1-1={float(q1-1):.3g}) q2={q2} ({float(q2):.10g}, q2-1={float(q2-1):.3g})")
