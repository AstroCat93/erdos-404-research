#!/usr/bin/env python3
"""eprime_test.py -- does the closed form Prop E' dominate the block form Prop E? (verify_M4A_logic, round 4)

Random x in Z_p (truncated at p^40, with optionally a planted deep gate of depth s at distance d after n),
composite window [n, N, N'), theta = ceil(D/2) (a ball small enough), sigma = M_W, f' = min(theta, K - sigma).
Prop E evaluated block-wise with the full c-sum (statement of M4A section 5); Prop E' from its closed form.
Both in mpmath (256 bits).  usage: eprime_test.py p SEED NW NMIN NMAX
"""
import random
import sys
from fractions import Fraction

import mpmath
from mpmath import mpf

from vl_lib import vp, q_consts, P0_table
from fe_indep import propDE_mp

mpmath.mp.prec = 256


def main():
    p, seed, nw, nmin, nmax = (int(x) for x in sys.argv[1:6])
    rng = random.Random(seed)
    S = 8
    qF = q_consts(p, S)
    P0F = P0_table(p, 14)
    qmp = {s: mpf(qF[s].numerator) / qF[s].denominator for s in range(1, S + 1)}
    P0mp = {g: [mpf(x.numerator) / x.denominator for x in row] for g, row in P0F.items()}
    lq = {s: mpmath.log(qmp[s]) for s in range(1, S + 1)}
    rho1 = lq[1] + sum((lq[s] - lq[s - 1]) / mpf(p) ** (s - 1) for s in range(2, S + 1)) \
        + mpmath.log(p) * sum(mpf(p) ** (-(s - 1)) for s in range(S + 1, S + 400))
    gamma = lq[1] - mpmath.log(qmp[2] / p)
    kappa = (p - 1) * mpmath.log(2) - mpmath.log(p) + rho1 - gamma * mpf(p - 1) ** 2 / p ** 2
    assert kappa > 0
    ek = mpmath.exp(-kappa)
    worst = mpf(-1e9)
    bad = 0
    nev = 0
    for it in range(nw):
        n = rng.randint(nmin, nmax)
        r1 = 1 + rng.random() * 0.5
        r2 = 1 + rng.random() * 0.5
        N = int(n * r1) + 1
        N2 = int(N * r2) + 1
        x = rng.randrange(p ** 40)
        if it % 2 == 1:   # plant a deep gate at distance d after n
            d, s = rng.randint(1, 3 * p), rng.randint(3, 7)
            x = (-(n + d)) % p ** s + p ** s * rng.randrange(p ** 30)
        depth = [0] + [min(vp(x + i, p), 30) for i in range(1, N2 + 1)]
        V = [0] * (N2 + 1)
        for i in range(1, N2 + 1):
            V[i] = V[i - 1] + depth[i]
        D, K = V[N] - V[n], V[N2] - V[n]
        MW = max(depth[n + 1:N2 + 1])
        th = (D + 1) // 2
        if MW > K - th or th < 1:
            continue
        fpr = min(th, K - MW)
        nev += 1
        E = propDE_mp(depth, V, n, N2, K, p, qmp, S, P0mp, fprime=fpr)
        sig = MW
        lqt = lq[sig] if sig <= S else lq[S] + (sig - S) * mpmath.log(p)
        t1 = mpf(p) ** K * mpf(2) ** (-(N2 - n)) * (1 + mpf(2) ** p)
        t2 = mpf(2) ** (p + sig * (p - 1)) * mpmath.exp(K * rho1 + lqt - lq[1] + gamma * (2 - mpf(1) / p)
                                                           - gamma * (fpr - sig + 1) * mpf(p - 1) ** 2 / p ** 2) \
            * ek / (1 - ek)
        Ep = t1 + t2
        ratio = mpmath.log10(E) - mpmath.log10(Ep)
        worst = max(worst, ratio)
        if E > Ep:
            bad += 1
            print(f"  VIOLATION n={n} N={N} N'={N2} D={D} K={K} M_W={MW} log10 E={mpmath.nstr(mpmath.log10(E), 8)} "
                  f"log10 E'={mpmath.nstr(mpmath.log10(Ep), 8)}")
    print(f"EPRIME p={p} seed={seed}: windows drawn={nw} evaluated={nev} E'<E in {bad}; max log10(E/E') = {mpmath.nstr(worst, 6)}")


if __name__ == "__main__":
    main()
