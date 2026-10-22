#!/usr/bin/env python3
"""t2_recursion.py -- validates the two independent ways this checker computes alive targets.

For random integer x (optionally with a forced gate), and every n <= nmax:
  (a) the set of paths alive at n by BRUTE FORCE over all 2^(n-1) paths (no pruning) equals the DFS set
      (the DFS prunes with backward integrality, M4D (F2) converse -- so (a) also tests that converse);
  (b) the set of targets tau_n(e) mod p^R (R = V_Nmax - V_n) of the brute-force alive paths equals the set
      produced by the single-step carry recursion (both implementations: step_targets, step_targets_np);
  (c) (F1)-type bookkeeping: V_n >= v_p(n!) for every n (Legendre bound used in (F1)).
usage: t2_recursion.py p seed nx nmax [gate_pos gate_depth]
"""
import random
import sys
from math import factorial

from vF import make_x, valuations, products, alive_bruteforce, alive_dfs, target_mod, step_targets, \
    step_targets_np, vp


def main():
    p, seed, nx, nmax = (int(a) for a in sys.argv[1:5])
    forced = ()
    if len(sys.argv) > 6:
        forced = ((int(sys.argv[5]), int(sys.argv[6])),)
    rng = random.Random(seed)
    fails = dict(dfs=0, rec=0, recnp=0, legendre=0)
    checks = 0
    tot_alive = 0
    for _ in range(nx):
        x = make_x(rng, p, 30, forced)
        vals, V = valuations(x, p, nmax)
        pi = products(x, nmax)
        Nmax = nmax
        rec = step_targets(x, p, vals, V, Nmax, range(1, nmax + 1))
        recnp = step_targets_np(x, p, vals, V, Nmax, range(1, nmax + 1))
        for n in range(1, nmax + 1):
            if V[n] < vp(factorial(n), p):
                fails['legendre'] += 1
            bf = alive_bruteforce(x, p, n, pi, V)
            df = alive_dfs(x, p, n, pi, V)
            if sorted(m for m, _ in bf) != sorted(m for m, _ in df):
                fails['dfs'] += 1
            R = V[Nmax] - V[n]
            tset = {target_mod(S, pi[n], V[n], p, R) for _, S in bf}
            if tset != rec[n]:
                fails['rec'] += 1
            if tset != {int(t) for t in recnp[n]}:
                fails['recnp'] += 1
            checks += 1
            tot_alive += len(bf)
    print(f"RESULT t2 p={p} seed={seed} nx={nx} nmax={nmax} forced={forced}: (x,n) checks={checks}, "
          f"alive paths seen={tot_alive}; brute-force vs DFS mismatches={fails['dfs']}, "
          f"target-set (brute force) vs carry recursion mismatches: python={fails['rec']}, numpy={fails['recnp']}, "
          f"Legendre V_n>=v(n!) failures={fails['legendre']}")


if __name__ == "__main__":
    main()
