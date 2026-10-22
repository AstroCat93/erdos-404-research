#!/usr/bin/env python3
"""Exact test of M4C Proposition P1 (report §6) and of the admissibility data.

For p in {7, 11, 13}: greedy phase-1 schedule (own implementation, cert.phase1),
random x = p^3 u (exact integers, u random with random extra p-divisibility),
and every phase-1 window k whose K = V(b_{k+1}) - V(b_{k-1}) is small enough:
  (i)  lin_k by direct valuations of x:  D_{k-1}+D_k <= m_{k-1} - M_{n_{k+1}},
       M_{n_{k+1}} < m_{k-1}; and V_{bp}(x) = V(b), M_{bp}(x) = Mx(b);
  (ii) eps_k(x) = p^K Coll_K - p^D Coll_D  (exact, CRT)  <=  q1^{n1} q2^{n2} - 1.
Also the first window: 1 + chi^2_{W_0} = p Coll_1([3p,4p)) = q1 exactly.
"""
import sys, random, time
from fractions import Fraction
sys.path.insert(0, __import__('os').path.dirname(__file__))
from vlib import vp, pis, prob_zero
from qconst_indep import q_exact
from cert import phase1


def main():
    p = int(sys.argv[1]); nx = int(sys.argv[2]); maxK = int(sys.argv[3])
    rng = random.Random(9000 + p)
    q1, _, _ = q_exact(p, 1); q2, _, _ = q_exact(p, 2)
    b, k0, wins = phase1(p)
    P2 = p * p
    d = [0] + [1 + vp(j, p) for j in range(1, P2)]
    Vc = [0] * P2; Mxc = [0] * P2
    for j in range(1, P2):
        Vc[j] = Vc[j - 1] + d[j]; Mxc[j] = max(Mxc[j - 1], d[j])
    print("p=%d phase-1 schedule %s, k0=%d" % (p, b, k0), flush=True)
    t0 = time.time()
    nlin = 0; nlinfail = 0; neps = 0; nepsfail = 0; worst = {}
    for it in range(nx):
        u = rng.randrange(1, p ** 30) * p ** rng.choice([0, 0, 0, 1, 2, 5])
        if rng.random() < 0.3:
            u = -u
        x = p ** 3 * u
        # admissibility / chi^2 of W_0
        if it == 0:
            P0, _ = pis(x + 3 * p, p)
            c1 = prob_zero([v % p for v in P0], 1, p)
            print("  1+chi^2_{W_0} = p Coll_1 = %s ; q1 = %s ; equal: %s" % (p * c1, q1, p * c1 == q1), flush=True)
        # valuations along all of phase 1
        nmax = b[-1] * p
        vals = [0] + [vp(x + i, p) for i in range(1, nmax + 1)]
        Vx = [0] * (nmax + 1); Mx = [0] * (nmax + 1)
        for i in range(1, nmax + 1):
            Vx[i] = Vx[i - 1] + vals[i]; Mx[i] = max(Mx[i - 1], vals[i])
        for bb in b:
            assert Vx[bb * p] == Vc[bb] and Mx[bb * p] == Mxc[bb], (p, bb)
        for (k, lo, hi, n1, n2) in wins:
            mid = b[k]
            m_km1 = Vx[lo * p]; Dk1 = Vx[mid * p] - Vx[lo * p]; Dk = Vx[hi * p] - Vx[mid * p]
            Mn = Mx[hi * p]
            nlin += 1
            if not (Dk1 + Dk <= m_km1 - Mn and Mn < m_km1):
                nlinfail += 1
                print("  LIN FAILS", p, k, lo, mid, hi)
            K = Dk1 + Dk; D = Dk1
            if K > maxK:
                continue
            z = x + lo * p
            t = (hi - lo) * p
            Pz, _ = pis(z, t)
            a = [v % p ** K for v in Pz]
            collK = prob_zero(a, K, p)
            collD = prob_zero([v % p ** D for v in a], D, p)
            eps = p ** K * collK - p ** D * collD
            bound = q1 ** n1 * q2 ** n2 - 1
            neps += 1
            r = float(eps / bound) if bound > 0 else float('inf')
            w = worst.setdefault(k, [lo, mid, hi, K, n1, n2, 0.0, 0.0, 1e9])
            w[6] = max(w[6], r); w[7] = max(w[7], float(eps)); w[8] = min(w[8], float(eps))
            if eps > bound or eps < 0:
                nepsfail += 1
                print("  P1(ii) FAILS", dict(p=p, k=k, lo=lo, hi=hi, K=K, eps=float(eps), bound=float(bound)), flush=True)
    for k in sorted(worst):
        lo, mid, hi, K, n1, n2, r, emax, emin = worst[k]
        print("  window k=%d blocks (%d,%d,%d] K=%d n1=%d n2=%d: eps in [%.4e, %.4e], bound q1^n1 q2^n2 - 1 = %.4e, max eps/bound %.4f" % (
            k, lo, mid, hi, K, n1, n2, emin, emax, float(q1 ** n1 * q2 ** n2 - 1), r))
    print("p=%d: %d random x in A; lin checks %d (failures %d); eps checks %d (failures %d)  [%.0fs]" % (
        p, nx, nlin, nlinfail, neps, nepsfail, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
