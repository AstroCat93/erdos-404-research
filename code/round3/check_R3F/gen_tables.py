"""gen_tables.py -- certified cosine/sine tables for shellchk.c (check of R3F, round 3).

Tables for modulus M:  Ch[h] = cos(pi h B/M), Sh[h] = sin(pi h B/M) (0 <= h < nhi = ceil(M/B)),
                       Cl[l] = cos(pi l/M),   Sl[l] = sin(pi l/M)   (0 <= l < B),
B = min(2^17, next power of two >= M).  Values: arb balls at 128 bits (python-flint, cos_pi_fmpq / sin_pi_fmpq
with exact rational arguments), converted to the nearest double.  e_t = max over all entries of an arb upper bound
for |double - true value|.

Error of the evaluated cosine c~ = fl(fl(Ch*Cl) - fl(Sh*Sl)) (round to nearest, no FMA), u = 2^-53:
  |c~ - cos(pi r/M)| <= 4 e_t + 2 e_t^2 + 2u(1+u)(1+2e_t)^2 =: E.
(|Ch Cl - C~h C~l| <= e_t(1+e_t) + e_t, same for the sine product; |P1|+|P2| <= (1+2e_t)^2 by Cauchy-Schwarz,
 so the two product roundings and the subtraction cost <= u(1+u)(1+2e_t)^2 + u(1+2e_t)^2.)
The C code uses a_i = fl(|c~| + eps) and b_i = fl(|c~| - eps); fl(|c~| + eps) >= |c~| + eps - u(1+eps) and
fl(|c~| - eps) <= |c~| - eps + u.  So eps >= E + u(1+eps) makes a_i >= |cos| >= b_i.  We require
eps = 1e-15 and assert E + 1.0001 u <= eps.

usage: python3 -I gen_tables.py M OUTFILE
"""
import sys
import numpy as np
from flint import arb, fmpq, ctx

U = 2.0 ** -53


def gen(M, out):
    ctx.prec = 128
    B = 1
    while B < M and B < (1 << 17):
        B <<= 1
    nhi = -(-M // B)
    et = 0.0

    def tab(nums, den):
        cs = np.empty(len(nums)); ss = np.empty(len(nums))
        nonlocal et
        for j, a in enumerate(nums):
            q = fmpq(a, den)
            c = arb.cos_pi_fmpq(q); s = arb.sin_pi_fmpq(q)
            fc = float(c.mid()); fs = float(s.mid())
            ec = float((arb(fc) - c).abs_upper().upper()) * (1 + 1e-12)
            es = float((arb(fs) - s).abs_upper().upper()) * (1 + 1e-12)
            et = max(et, ec, es)
            cs[j] = fc; ss[j] = fs
        return cs, ss

    Ch, Sh = tab([h * B for h in range(nhi)], M)
    Cl, Sl = tab(list(range(B)), M)
    eps = 1e-15
    e_t = et
    E = 4 * e_t + 2 * e_t * e_t + 2 * U * (1 + U) * (1 + 2 * e_t) ** 2
    assert E + 1.0001 * U <= eps, (e_t, E)
    with open(out, 'wb') as f:
        np.array([M, B, nhi], dtype='<u8').tofile(f)
        np.array([eps], dtype='<f8').tofile(f)
        for a in (Ch, Sh, Cl, Sl):
            a.astype('<f8').tofile(f)
    return dict(M=M, B=B, nhi=nhi, e_t=e_t, E=E, eps=eps)


if __name__ == '__main__':
    M = int(sys.argv[1])
    print(gen(M, sys.argv[2]))
