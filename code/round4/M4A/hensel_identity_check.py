#!/usr/bin/env python3
"""hensel_identity_check.py -- exact test of Theorem 1 of data/round4/reports/M4A.md (track M4A, round 4):

For a ball B = xB + p^b Z_p on which the valuations v(x+i), n < i <= N', are constant, a composite window
[n, N) u [N, N') with D = V_N - V_n, K = V_N' - V_n, H = N' - n, and floor(D/2) + 1 >= b:

   E_B[eps] = 2^-H (p^K - p^D)
             + E_delta[ 1{delta != 0} ( p^K mu_B(v(S_delta) >= K, v(S_delta') >= th)
                                      - p^D mu_B(v(S_delta) >= D, v(S_delta') >= th) ) ],
   th = min(ceil(D/2), D-b+1)  (= ceil(D/2) when floor(D/2)+1 >= b),

where eps(x) = p^K Coll_K - p^D Coll_D is R3M's fine-scale mass of the composite window (Prop C2),
S_delta(x) = sum_{c<H} delta_c y_c(x), y_c = (x+n+1)...(x+n+c), delta i.i.d. P(0)=1/2, P(+-1)=1/4.

LHS: average of eps over x = xB + p^b w, w mod p^(K-b) (eps depends on x mod p^K only), exact Fractions.
RHS: per x, exact integer DP over (S mod p^K, S' mod p^th), th = ceil(D/2).
Also reports the two-sided bound  -p^D HS_D <= E_B eps - 2^-H(p^K-p^D) <= p^K HS_K.
With FORCE=1 the condition floor(D/2)+1 >= b is dropped and the general threshold th = min(ceil(D/2), D-b+1)
of Lemma H is used (the identity is claimed for every b).
usage: hensel_identity_check.py p SEED NB n H1 H2 b KMAX [FORCE]
"""
import random
import sys
from fractions import Fraction

import numpy as np

from m4a_lib import vp


def coll_counts(elems, p, K):
    """numpy int64 counts of the 2^len subset sums mod p^K."""
    mod = p ** K
    dist = np.zeros(mod, dtype=np.int64)
    dist[0] = 1
    for y in elems:
        dist = dist + np.roll(dist, int(y % mod))
    return dist


def fold(dist, p, j):
    return dist.reshape(-1, p ** j).sum(axis=0) if j < 50 else dist


def eps_exact(elems, p, D, K):
    dist = coll_counts(elems, p, K)
    T2 = 4 ** len(elems)
    cK = int(np.dot(dist, dist))
    fD = dist.reshape(-1, p ** D).sum(axis=0) if D > 0 else np.array([dist.sum()])
    cD = int(np.dot(fD, fD))
    return Fraction(p ** K * cK - p ** D * cD, T2)


def signed_joint(ys, dys, p, K, th):
    """integer weights (total 4^H) of (S mod p^K, S' mod p^th) for S = sum delta_c y_c."""
    m1, m2 = p ** K, p ** th
    st = np.zeros((m1, m2), dtype=np.int64)
    st[0, 0] = 1
    for y, dy in zip(ys, dys):
        a, bb = int(y % m1), int(dy % m2)
        st = 2 * st + np.roll(np.roll(st, a, axis=0), bb, axis=1) + np.roll(np.roll(st, -a, axis=0), -bb, axis=1)
    return st


def main():
    p, seed, NB, n, H1, H2, b, KMAX = (int(a) for a in sys.argv[1:9])
    FORCE = len(sys.argv) > 9 and sys.argv[9] == '1'
    N, N2 = n + H1, n + H1 + H2
    H = N2 - n
    rnd = random.Random(seed)
    done = ok = tries = 0
    bound_ok = 0
    while done < NB and tries < 200000:
        tries += 1
        xB = rnd.randrange(p ** b)
        # valuations constant on B: no i in (n, N'] with xB + i == 0 mod p^b  (then v(x+i) = v(xB+i) < b)
        if any((xB + i) % p ** b == 0 for i in range(1, N2 + 1)):
            continue
        vals = [vp(xB + i, p) for i in range(N2 + 1)]
        D = sum(vals[n + 1:N + 1])
        K = sum(vals[n + 1:N2 + 1])
        if D < 1 or K > KMAX or K <= D:
            continue
        if not FORCE and D // 2 + 1 < b:
            continue
        th = min((D + 1) // 2, D - b + 1)   # Lemma H threshold: min(ceil(D/2), D-b+1)
        if th < 0:
            th = 0
        done += 1
        nw = p ** max(0, K - b)
        lhs = Fraction(0)
        hsK = Fraction(0)
        hsD = Fraction(0)
        T2 = 4 ** H
        for w in range(nw):
            x = xB + p ** b * w
            ys, dys = [], []
            y, dy = 1, 0
            for c in range(H):
                ys.append(y)
                dys.append(dy)
                f = x + n + c + 1
                y, dy = y * f, dy * f + y
            lhs += eps_exact(ys, p, D, K)
            st = signed_joint(ys, dys, p, K, th)
            # delta = 0 has weight 2^H and S = S' = 0: exclude it
            z = 2 ** H
            colK = int(st[0, 0]) - z
            stD = st.reshape(p ** (K - D), p ** D, p ** th).sum(axis=0)
            colD = int(stD[0, 0]) - z
            hsK += Fraction(colK, T2)
            hsD += Fraction(colD, T2)
        lhs /= nw
        hsK /= nw
        hsD /= nw
        base = Fraction(p ** K - p ** D, 2 ** H)
        rhs = base + p ** K * hsK - p ** D * hsD
        good = (lhs == rhs)
        ok += good
        bnd = (-p ** D * hsD <= lhs - base <= p ** K * hsK)
        bound_ok += bnd
        print(f"B#{done}: xB={xB} b={b} D={D} K={K} th={th} nw={nw}  E_B eps={float(lhs):.6e}  RHS={float(rhs):.6e} "
              f"exact_equal={good}  p^K*HS_K={float(p**K*hsK):.3e} p^D*HS_D={float(p**D*hsD):.3e} "
              f"base={float(base):.3e} bound_ok={bnd}  cond={D//2+1>=b}", flush=True)
    print(f"RESULT p={p} n={n} H1={H1} H2={H2} b={b} FORCE={FORCE}: identity exact in {ok}/{done} balls; "
          f"two-sided bound in {bound_ok}/{done}")


if __name__ == "__main__":
    main()
