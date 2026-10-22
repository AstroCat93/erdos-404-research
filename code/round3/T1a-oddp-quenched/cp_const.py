#!/usr/bin/env python3
"""Top-digit (order-p) contraction constants (writeup.md Sec. 5.3).

For a stretch of unit elements y_0=1, y_1=r0, y_2=r0(r0+1), ..., y_k = prod_{i<k}(r0+i) (k <= p-r0), i.e. the
elements pi_j(x)/pi_n(x) of a window starting at n when x+n+1 == r0 (mod p), r0 in 1..p-1, up to the next
multiple of p, the mod-p Fourier coefficient of the subset-sum distribution at a unit frequency xi is
      F(r0, xi) = prod_{k=0}^{p-r0} |cos(pi xi y_k / p)|.
  c_p(r0) = max_xi F(r0, xi);  c_p = c_p(1) = max_xi prod_{r<p} |cos(pi xi r!/p)|  (the full block 0!,...,(p-1)!).
Also printed: the order-p l^2 mass  sum_{xi != 0} F(r0,xi)^2  and the worst case over r0.
"""
import math, sys

def consts(p):
    rows = []
    for r0 in range(1, p):
        ys = []; prod = 1
        for k in range(0, p - r0 + 1):
            ys.append(prod % p)
            prod = prod * (r0 + k)
        best = 0.0; l2 = 0.0; argbest = None
        for xi in range(1, p):
            F = 1.0
            for y in ys:
                F *= abs(math.cos(math.pi * xi * y / p))
            if F > best:
                best, argbest = F, xi
            l2 += F * F
        rows.append((r0, len(ys), best, argbest, l2))
    return rows

if __name__ == "__main__":
    ps = [int(a) for a in sys.argv[1:]] or [3, 5, 7, 11, 13, 17, 19, 23]
    for p in ps:
        rows = consts(p)
        cp = rows[0][2]
        worst = max(r[2] for r in rows)
        worst_l2 = max(r[4] for r in rows)
        print(f"p={p}: c_p = c_p(1) = {cp:.6f} (xi={rows[0][3]}, {rows[0][1]} units 0!..{p-1}!);  "
              f"max_r0 c_p(r0) = {worst:.6f};  max_r0 sum_xi F^2 = {worst_l2:.6f};  cos^2(pi/p) = {math.cos(math.pi/p)**2:.6f}")
        for r0, k, best, xi, l2 in rows:
            print(f"    r0={r0:2d} units={k:2d} c_p(r0)={best:.6f} (xi={xi}) l2={l2:.6f}")
