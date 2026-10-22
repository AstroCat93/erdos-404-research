#!/usr/bin/env python3
"""t4_corF1_exhaustive.py -- exact, exhaustive test of M4D Corollary F1 (finite horizon) on a cylinder A,
and of the local-constancy (Borel) claim in its proof.

Deterministic times n_0 < ... < n_{L+1}, j = 0, deterministic theta schedule (constant c), or the
locally constant schedule theta_l = p^{-D_l} ('tao').  Events (M4D sec. 2):
  I_0  = { T_0 meets G_0 },   L_l = { |G_l| > (1-theta_l) p^{D_l} }  (l = 1..L-1),
  ALIVE = { T_L nonempty } = { some path alive at n_L }   (finite-horizon stand-in for K_p; K_p is inside it).
Finite-horizon Corollary F1:   mu(A & ALIVE) >= mu(A & I_0) - sum_{l=1}^{L-1} mu(A \\ L_l).
Method: Haar measure on A = a + p^kA Z_p is split into cylinders c + p^k Z_p.  A cylinder is DETERMINED when
v(c+i) < k for all 1 <= i <= n_{L+1} and V_{n_{L+1}}(c) <= k; then every event above is constant on it
(the checker's argument; tested here by re-evaluating at random points x' = c + p^k w of a sample of
determined cylinders, with x' a large integer).  Undetermined cylinders are split, down to level kmax;
the remaining undetermined mass U is reported and charged against the inequality.
Every determined cylinder also gets the POINTWISE check  I_0 & all L_l  =>  ALIVE (Theorem F, finite form).
usage: t4_corF1_exhaustive.py p a kA kmax schedule n_0 ... n_{L+1}      (schedule: 1, 1/2, 1/4, tao)
"""
import random
import sys
from fractions import Fraction

import numpy as np

from vF import valuations, step_targets_np, subset_sums, window_elems


def events(x, p, times, sched):
    L = len(times) - 2
    vals, V = valuations(x, p, times[-1])
    D = [V[times[l + 1]] - V[times[l]] for l in range(L + 1)]
    tg = step_targets_np(x, p, vals, V, times[-1], times[:L + 1])
    T0 = set(int(t) % p ** D[0] for t in tg[times[0]])
    alive = len(tg[times[L]]) > 0
    if sched == 'tao':
        theta = [None] + [Fraction(1, p ** D[l]) for l in range(1, L + 1)]
    else:
        theta = [None] + [Fraction(sched)] * L
    G = []
    for l in range(L):
        m = p ** (D[l] + D[l + 1])
        s = subset_sums(window_elems(x, times[l], times[l + 1] - times[l], m), m)
        Lc = np.bincount(np.nonzero(s)[0] % p ** D[l], minlength=p ** D[l])
        thr = theta[l + 1] * p ** D[l + 1]
        G.append({r for r in range(p ** D[l]) if Lc[r] >= thr})
    I0 = bool(T0 & G[0])
    Ls = [len(G[l]) > (1 - theta[l]) * p ** D[l] for l in range(1, L)]
    return I0, tuple(Ls), alive


def main():
    p, a, kA, kmax = (int(t) for t in sys.argv[1:5])
    sched = sys.argv[5]
    times = [int(t) for t in sys.argv[6:]]
    L = len(times) - 2
    N = times[-1]
    rng = random.Random(12345)
    mu_alive = mu_I0 = mu_all = Fraction(0)
    mu_notL = [Fraction(0)] * (L - 1)
    U = Fraction(0)
    ncyl = pointwise_viol = lc_checked = lc_fail = 0
    stack = [(a % p ** kA if kA > 0 else 0, kA)]
    while stack:
        c, k = stack.pop()
        det = k > 0
        if det:
            vals, V = valuations(c if c > 0 else c + p ** k, p, N)  # c + i > 0 always; use c+p^k if c == 0
            xrep = c if c > 0 else c + p ** k
            det = all(v < k for v in vals[1:]) and V[N] <= k
        if not det:
            if k >= kmax:
                U += Fraction(1, p ** k)
                continue
            for j in range(p):
                stack.append((c + j * p ** k, k + 1))
            continue
        ncyl += 1
        w = Fraction(1, p ** k)
        I0, Ls, alive = events(xrep, p, times, sched)
        if rng.random() < 0.05:
            # local constancy: re-evaluate at a random far point of the same cylinder
            xp = xrep + p ** k * rng.randrange(1, p ** 30)
            lc_checked += 1
            if events(xp, p, times, sched) != (I0, Ls, alive):
                lc_fail += 1
        if I0 and all(Ls) and not alive:
            pointwise_viol += 1
        mu_alive += w * alive
        mu_I0 += w * I0
        mu_all += w * (I0 and all(Ls))
        for l in range(L - 1):
            if not Ls[l]:
                mu_notL[l] += w
    muA = Fraction(1, p ** kA)
    rhs_upper = mu_I0 + U - sum(mu_notL)
    ok = mu_alive >= rhs_upper
    print(f"RESULT t4 p={p} A={a}+{p}^{kA}Z_p kmax={kmax} schedule={sched} times={times}: determined cylinders={ncyl}, "
          f"undetermined mass U/mu(A)={float(U / muA):.3e}; mu(A&ALIVE)/mu(A)={float(mu_alive / muA):.6f}, "
          f"mu(A&I0)/mu(A)={float(mu_I0 / muA):.6f}, sum mu(A minus L_l)/mu(A)={[float(t / muA) for t in mu_notL]}, "
          f"mu(A&I0&all L)/mu(A)={float(mu_all / muA):.6f}; RHS (charged with U)/mu(A)={float(rhs_upper / muA):.6f}; "
          f"inequality holds: {ok}; pointwise (I)&(II)=>ALIVE violations={pointwise_viol}; "
          f"local-constancy re-evaluations={lc_checked}, mismatches={lc_fail}")


if __name__ == "__main__":
    main()
