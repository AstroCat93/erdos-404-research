#!/usr/bin/env python3
"""n4_infinite_mean_check.py -- exact test of the mechanism of Proposition N4 (E_Haar[eps] = +infinity).

Claim: if v(x+n+1) = s, then eps(W,W') = (p^s/2) * eps_post exactly (Prop B2 with d = 1), and if moreover
s >= s0 := K_fact + v((N'-n-1)!) + 1 (K_fact = v((N'-n-1)!)), the post window [n+1,N') is position-independent
modulo p^{K_post}, so eps_post = eps_fact(N-n-1, N'-N) = the fine-scale mass of the factorial window
0!, 1!, ..., (N'-n-2)! with split after N-n-1 elements (D_f = v((N-n-1)!), K_f = v((N'-n-1)!)).
Hence eps = (p^s/2) eps_fact for all s >= s0, each shell {v(x+n+1)=s} has Haar measure (1-1/p)p^-s, and
E[eps] >= sum_{s>=s0} (1-1/p) eps_fact / 2 = +infinity as soon as eps_fact > 0 (which holds when K_f > D_f).
The program checks eps == (p^s/2) eps_fact exactly for random x in each shell s0 <= s <= s0+3.
usage: n4_infinite_mean_check.py p SEED NREP n H H2
"""
import random
import sys
from fractions import Fraction

from m4b_lib import Ctx, valuations, window_elems, eps_composite, forced_gate_x, unsigned_dist, fold, sumsq


def vfact(n, p):
    s, q = 0, p
    while q <= n:
        s += n // q
        q *= p
    return s


def main():
    p, seed, NREP, n, H, H2 = (int(a) for a in sys.argv[1:7])
    C = Ctx(p, 300)
    rnd = random.Random(seed)
    N, N2 = n + H, n + H + H2
    Lp, L2 = H - 1, H2                    # post window lengths
    Df, Kf = vfact(Lp, p), vfact(Lp + L2, p)
    fact = [1]
    for c in range(1, Lp + L2):
        fact.append(fact[-1] * c)
    m = unsigned_dist(fact, p ** Kf)
    eps_fact = p ** Kf * Fraction(sumsq(m), 4 ** (Lp + L2)) - p ** Df * Fraction(sumsq(fold(m, p ** Df)), 4 ** (Lp + L2))
    s0 = Kf + vfact(Lp + L2, p) + 1
    ok = tot = 0
    for s in range(s0, s0 + 4):
        for _ in range(NREP):
            x = forced_gate_x(C, rnd, n + 1, s)
            vals, V = valuations(C, x, N2)
            D, K = V[N] - V[n], V[N2] - V[n]
            y = window_elems(C, x, n, N2)
            eps = eps_composite(y, p, D, K)
            good = (eps == Fraction(p ** s, 2) * eps_fact)
            ok += good
            tot += 1
            if not good:
                print(f"MISMATCH s={s} eps={float(eps)} predicted={float(Fraction(p**s,2)*eps_fact)}")
        print(f"  s={s}: D={D} K={K} eps={float(eps):.6g} = p^s/2 * eps_fact ? {good}", flush=True)
    print(f"RESULT p={p} n={n} H={H} H2={H2}: eps_fact={float(eps_fact):.6g} (D_f={Df}, K_f={Kf}, s0={s0}); "
          f"identity eps = (p^s/2) eps_fact exact in {ok}/{tot}; shell contribution (1-1/p) eps_fact/2 = "
          f"{float((1 - Fraction(1, p)) * eps_fact / 2):.4g} per s >= s0")


if __name__ == "__main__":
    main()
