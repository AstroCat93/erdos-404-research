#!/usr/bin/env python3
"""budgets.py -- random-model budgets (round 3, track R3F; targets (b), (d)).

U_d = min{i : v_p(i!) >= d},  N_d = p^d - p^{d-1}.
  Lambda_p   = sum_d N_d (2/pi)^{U_d}        (L^1 random model; note Thm 10.16)
  Lambda'_p  = sum_d N_d 2^{-U_d/2}          (Cauchy-Schwarz/collision-count budget, this report)
  Lambda2_p  = sum_d N_d 2^{-U_d}            (L^2 random-model mass)
  tau_p(3)   = p^{3+c} (2/pi)^{p^2},  tau'_p(3) = p^{3+c} 2^{-p^2/2},  c = v_p((p^2-1)!)
Evaluation: mpmath interval arithmetic for d <= D; the tail d > D is bounded with U_d >= (p-1)d + 1:
  sum_{d>D} p^d q^{(p-1)d+1} = q r^{D+1}/(1-r),  r = p q^{p-1}  (q = 2/pi, 2^{-1/2}, 1/2), valid when r < 1.
usage: budgets.py [D]
"""
import sys
from mpmath import iv


def vfact(n, p):
    s = 0
    while n:
        n //= p; s += n
    return s


def U(d, p):
    # smallest i with v_p(i!) >= d; v_p(i!) >= d needs i >= (p-1)d+1, search upward
    i = (p - 1) * d + 1
    while vfact(i, p) < d:
        i += 1
    return i


def budget(p, q, D):
    tot = iv.mpf(0)
    for d in range(1, D + 1):
        tot += (iv.mpf(p) ** d - iv.mpf(p) ** (d - 1)) * q ** U(d, p)
    r = p * q ** (p - 1)
    if r.b >= 1:
        return tot, None
    tail = q * r ** (D + 1) / (1 - r)
    return tot, tot + tail


def main():
    iv.prec = 100
    D = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    print("# p  Lambda_p (L1)  Lambda'_p (C-S)  Lambda2_p (L2 mass)  tau_p(3)  tau'_p(3)   [upper endpoints; 'div' = series not bounded by the geometric tail]")
    for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        out = []
        for q in (2 / iv.pi, 1 / iv.sqrt(iv.mpf(2)), iv.mpf(1) / 2):
            part, full = budget(p, q, D)
            out.append(f"{float(full.b):.6g}" if full is not None else f"div(>{float(part.a):.4g})")
        c = vfact(p * p - 1, p)
        t1 = iv.mpf(p) ** (3 + c) * (2 / iv.pi) ** (p * p)
        t2 = iv.mpf(p) ** (3 + c) * iv.mpf(2) ** (-(p * p) / iv.mpf(2))
        print(f"{p:3d}  {out[0]:>12}  {out[1]:>14}  {out[2]:>14}  {float(t1.b):.3e}  {float(t2.b):.3e}")


if __name__ == "__main__":
    main()
