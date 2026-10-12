#!/usr/bin/env python3
"""Brute-force test of Theorem 10.12 (worst-case propagation iff) on random small instances.
(i): for EVERY R full mod p^D, T(R) = {(x+s)/pi : x in R, s in Sigma, pi | x+s} meets every class
     mod p^D'.  Only R mod p^(delta+D') matters and shrinking R only shrinks T, so it suffices to
     range over all selections x_rho (one lift mod p^(delta+D') of each class rho mod p^D).
(ii): Sigma mod p^(delta+D') contains a full coset c + p^D Z / p^(delta+D') Z.
pi = p^delta * u with u a random unit."""
import itertools, random
random.seed(7)
def run(p, D, Dp, delta, trials):
    mod = p ** (delta + Dp)
    lifts = {r: [r + p ** D * j for j in range(p ** (delta + Dp - D))] for r in range(p ** D)}
    bad = 0; n_i = 0; n_ii = 0
    for _ in range(trials):
        size = random.randint(1, mod)
        Sig = set(random.sample(range(mod), size))
        u = random.choice([a for a in range(1, mod) if a % p])
        pi = p ** delta * u
        # (ii)
        ii = any(all((c + p ** D * j) % mod in Sig for j in range(p ** (delta + Dp - D))) for c in range(p ** D))
        # (i)
        i_holds = True
        for sel in itertools.product(*[lifts[r] for r in range(p ** D)]):
            T = set()
            for x in sel:
                for s in Sig:
                    z = (x + s) % mod
                    if z % p ** delta == 0:
                        # (x+s)/pi mod p^Dp
                        T.add(((z // p ** delta) * pow(u, -1, p ** max(Dp, 1))) % (p ** Dp) if Dp > 0 else 0)
            if len(T) < p ** Dp:
                i_holds = False; break
        n_i += i_holds; n_ii += ii
        if i_holds != ii:
            bad += 1
            print('COUNTEREXAMPLE', p, D, Dp, delta, sorted(Sig), u)
    print(f"p={p} D={D} D'={Dp} delta={delta}: trials={trials} (i)true={n_i} (ii)true={n_ii} disagreements={bad}")
for (p, D, Dp, delta) in [(3, 1, 0, 1), (3, 1, 1, 1), (3, 2, 1, 1), (3, 2, 0, 2), (3, 1, 1, 2), (3, 2, 1, 2),
                          (5, 1, 1, 1), (5, 1, 0, 1), (3, 2, 2, 1), (2, 2, 1, 1), (2, 3, 1, 2), (3, 3, 1, 2)]:
    if D > delta + Dp:
        continue
    run(p, D, Dp, delta, 300)
