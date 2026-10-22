#!/usr/bin/env python3
"""Exact pointwise test of the first-nonzero-index identity inside Prop H' (M4C §2):
  sum_delta P(delta) p^K 1{v(T_delta(z)) >= K, v(T'_delta(z)) >= h}
      = c_{L+L'} + sum_j (c_j/2) Lambda^{(lambda_j)}_{L+L'-j}(z+j),
h = ceil(D/2), lambda_j = h - V_j, valid when h <= K - M (hypothesis (2.2)).
Random z (exact integers, random gate offsets and occasional deep gates)."""
import sys, random, time
from fractions import Fraction
sys.path.insert(0, __import__('os').path.dirname(__file__))
from vlib import vp, pis, prob_joint_zero, prob_zero


def main():
    p = int(sys.argv[1]); npts = int(sys.argv[2]); maxst = int(sys.argv[3])
    rng = random.Random(55 + p)
    n = 0; eq = 0; t0 = time.time()
    tries = 0
    while n < npts and tries < 50 * npts:
        tries += 1
        g1 = rng.randrange(1, p + 1)
        u = rng.randrange(p ** 25)
        if rng.random() < 0.3:
            u = -rng.randrange(1, 4) + p ** rng.randrange(1, 3) * rng.randrange(1, p ** 10)  # a deep gate
        z = -g1 + p * u
        L = g1 + p * rng.randrange(1, 3) + rng.randrange(0, p)
        Lp = rng.randrange(1, 2 * p)
        T = L + Lp
        vals = [vp(z + i, p) for i in range(1, T + 1)]
        D = sum(vals[:L]); K = sum(vals); M = max(vals)
        h = -(-D // 2)
        if not (h <= K - M) or p ** (K + h) > maxst or D == K:
            continue
        Pz, Dz = pis(z, T)
        lhs = p ** K * prob_joint_zero([x % p ** K for x in Pz], [x % p ** h for x in Dz], K, h, p)
        V = [0] * (T + 1)
        for c in range(1, T + 1):
            V[c] = V[c - 1] + vals[c - 1]
        rhs = Fraction(p ** K, 2 ** T)
        for j in range(T):
            y = z + j; t = T - j; k = K - V[j]; lam = h - V[j]
            Py, Dy = pis(y, t)
            if lam >= 1:
                pr = prob_joint_zero([x % p ** k for x in Py], [x % p ** lam for x in Dy], k, lam, p, fixed0=True)
            else:
                pr = prob_zero([x % p ** k for x in Py], k, p, fixed0=True)
            rhs += Fraction(p ** V[j], 2 ** j) / 2 * p ** k * pr
        n += 1
        eq += (lhs == rhs)
        if lhs != rhs:
            print("  IDENTITY FAILS", dict(p=p, g1=g1, L=L, Lp=Lp, D=D, K=K, M=M, lhs=float(lhs), rhs=float(rhs)), flush=True)
    print("p=%d: identity tested at %d points (D in window 1, K total, h=ceil(D/2) <= K-M), exact equality at %d  [%.0fs]" % (p, n, eq, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
