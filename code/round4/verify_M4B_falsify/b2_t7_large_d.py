"""b2_t7_large_d.py -- Cor B2' at large distances d (10..16), where the hypothesis p^s > e(d-1)!
forces deep gates (e.g. p = 7, d = 16: s >= 15).  The pre-window law is handled by meet in the middle
(3^d pre-vectors are not enumerated one by one).  Checks (a), (b) [Coll^pre_g = (3/2)2^{-d},
P(A == 0 mod p^K) = 2^{-d}], (c) [exact identity], and the band [1/2, 3/2].
usage: b2_t7_large_d.py SEED NCASES
"""
import math
import random
import sys
from fractions import Fraction as Fr

from b2_lib import SignedLaw, Vrel, elems, forced_x, hyp_deep, vp, vx


def main():
    seed, NC = int(sys.argv[1]), int(sys.argv[2])
    rnd = random.Random(seed)
    st = dict(cases=0, fail=0, K_eq_g=0)
    rmin, rmax = Fr(10), Fr(0)
    while st["cases"] < NC:
        p = rnd.choice((3, 5, 7))
        d = rnd.randint(10, 16)
        s0 = next(s for s in range(1, 999) if hyp_deep(p, s, d))
        s = s0 + rnd.randint(0, 3)
        n = rnd.randint(0, 25)
        N = n + d + rnd.randint(0, 3)
        Np = N + rnd.randint(1, 24 - (N - n)) if 24 - (N - n) >= 1 else N + 1
        if Np - n > 25:
            continue
        x = forced_x(p, n + d, s, rnd)
        bad = []
        if any(vx(x, n + i, p) != vp(d - i, p) for i in range(1, d)):
            bad.append("(a)")
        g = Vrel(x, n, n + d, p)
        if g != vp(math.factorial(d - 1), p) + s:
            bad.append("(a) g")
        D, K = Vrel(x, n, N, p), Vrel(x, n, Np, p)
        ys = elems(x, n, Np)
        prelaw = SignedLaw(ys[:d], p, K)
        if prelaw.prob(g) != Fr(3, 2) / 2 ** d:
            bad.append(f"(b) Coll^pre_g = {prelaw.prob(g)}")
        if K > g and prelaw.prob(K) != Fr(1, 2 ** d):
            bad.append("(b) P(A=0 mod p^K)")
        law = SignedLaw(ys, p, K)
        e = p ** K * law.prob(K) - p ** D * law.prob(D)
        plaw = SignedLaw(elems(x, n + d, Np), p, K - g)
        ep = p ** (K - g) * plaw.prob(K - g) - p ** (D - g) * plaw.prob(D - g)
        if K > g:
            r = pow(x + n + d - 1, -1, p ** (K - g))
            Dl = plaw.rho(K - g, r) - plaw.rho(D - g, r)
        else:
            Dl = Fr(0)
            st["K_eq_g"] += 1
        cr = Fr(p ** g, 2 ** d)
        if e != cr * (ep + Dl / 2):
            bad.append("(c)")
        if ep > 0:
            ratio = e / (cr * ep)
            rmin, rmax = min(rmin, ratio), max(rmax, ratio)
            if not Fr(1, 2) <= ratio <= Fr(3, 2):
                bad.append("band")
        st["cases"] += 1
        if bad:
            st["fail"] += 1
            print(f"FAIL p={p} [{n},{N},{Np}) d={d} s={s}: {bad}", flush=True)
        if st["cases"] % 50 == 0:
            print("progress", st, flush=True)
    print(f"ratio range [{float(rmin):.6f}, {float(rmax):.6f}]")
    print("RESULT large_d:", st)


if __name__ == "__main__":
    main()
