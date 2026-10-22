"""b2_t5_r3m_compare.py -- cross-check of this library against the round-3 log
data/round3/R3M/eps_gate_depth.log (p = 3, windows [16,26) split 21, [24,40) split 32, [32,52) split 42,
gate at distance d in {1,4}, depth s), in the range where Cor B2' applies (d=1: s>=1; d=4: s>=3).
For each (window, d, s): NREP random cylinders x = -(n+d) + 3^s u; exact eps (this library), its median
and mean; the Cor B2' prediction (c_{n+d}/c_n)[eps_post + Delta(r*)/2] (d>=2) or (3^s/2) eps_post (d=1),
checked exactly per sample; and kappa = eps/3^s against the round-3 heuristic p^{v_pre}2^{-d}eps_post.
usage: b2_t5_r3m_compare.py SEED NREP
"""
import random
import statistics
import sys
from fractions import Fraction as Fr

from b2_lib import SignedLaw, Vrel, elems, forced_x

R3M = {  # medians from data/round3/R3M/eps_gate_depth.log (s = 1..6)
    (16, 1): [0.333, 0.307, 0.436, 4.59, 13.8, 41.3], (16, 4): [2.64, 0.0735, 0.221, 0.662, 1.99, 5.96],
    (24, 1): [0.193, 0.961, 0.344, 4.12, 12.5, 38], (24, 4): [0.261, 1.38, 0.41, 2.35, 7.19, 21.6],
    (32, 1): [0.322, 0.393, 0.192, 0.511, 1.82, 4.75], (32, 4): [0.469, 0.0961, 0.332, 2.08, 6.32, 19.4],
}
WIN = {16: (21, 26), 24: (32, 40), 32: (42, 52)}


def main():
    seed, NREP = int(sys.argv[1]), int(sys.argv[2])
    rnd = random.Random(seed)
    p = 3
    fails = 0
    for n in (16, 24, 32):
        N, Np = WIN[n]
        for d in (1, 4):
            for s in range(1, 7):
                hyp = (s >= 1) if d == 1 else (s >= 3)
                vals, kap_ratio = [], []
                for _ in range(NREP):
                    x = forced_x(p, n + d, s, rnd)
                    g = Vrel(x, n, n + d, p)
                    D, K = Vrel(x, n, N, p), Vrel(x, n, Np, p)
                    law = SignedLaw(elems(x, n, Np), p, K)
                    e = p ** K * law.prob(K) - p ** D * law.prob(D)
                    vals.append(e)
                    if hyp:
                        plaw = SignedLaw(elems(x, n + d, Np), p, K - g)
                        ep = p ** (K - g) * plaw.prob(K - g) - p ** (D - g) * plaw.prob(D - g)
                        if d == 1:
                            pred = Fr(p ** s, 2) * ep
                        else:
                            r = pow(x + n + d - 1, -1, p ** (K - g)) if K > g else 0
                            Dl = (plaw.rho(K - g, r) - plaw.rho(D - g, r)) if K > g else 0
                            pred = Fr(p ** g, 2 ** d) * (ep + Fr(Dl) / 2)
                        if pred != e:
                            fails += 1
                            print("FAIL", n, d, s, x % p ** 30)
                        # kappa = eps/p^s vs heuristic p^{v_pre} 2^{-d} eps_post, v_pre = g - s
                        if ep > 0:
                            kap_ratio.append(float((e / p ** s) / (Fr(p ** (g - s), 2 ** d) * ep)))
                med = statistics.median(float(v) for v in vals)
                mean = statistics.mean(float(v) for v in vals)
                r3 = R3M[(n, d)][s - 1]
                kr = (f" kappa/heur in [{min(kap_ratio):.4f},{max(kap_ratio):.4f}]" if kap_ratio else "")
                print(f"[{n},{Np}) split {N} d={d} s={s} hyp={'Y' if hyp else 'n'}: median {med:.4g} mean {mean:.4g} "
                      f"(R3M median {r3}){kr}", flush=True)
    print(f"RESULT r3m_compare: identity failures {fails}")


if __name__ == "__main__":
    main()
