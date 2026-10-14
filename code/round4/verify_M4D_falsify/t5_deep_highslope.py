"""t5: Lemma L at very deep gates and on explicitly high-slope parents.

  * x = u p^s - m with s in {6, 9, 12} (x extremely close to the negative
    integer -m), windows before, straddling, and after the gate at index m.
    Moduli p^K are huge here, so Sigma is kept as a Python set of the 2^H
    residues (independent of the numpy bitset used elsewhere); this also
    cross-checks Window.sums_mask where p^K is small.
  * x = u p^s - 2: the path (1,1,0,1) has S = (x+2)^3 (cube identity, checked
    exactly), slope v(S') = 2s.  It and its zero-extensions are used as the
    parent explicitly (when alive), plus all other alive parents (capped).
Usage: python3 t5_deep_highslope.py p seed nsamples
"""
import random
import sys
import time
from collections import Counter

from fz_core import (Vlist, Window, alive_paths_dfs, dpis, pis, rand_unit,
                     target, vp)


def check_parent(p, x, n, N, N2, Se, P, V, PS, Sig, W, stat, fails, tag):
    D, D2 = V[N] - V[n], V[N2] - V[N]
    K = D + D2
    pD, pD2 = p ** D, p ** D2
    tau = target(Se, P[n], p, K)
    r = tau % pD
    lift = [s_ for s_ in Sig if s_ % pD == r]
    uinv = pow(W.unit, -1, pD2) if pD2 > 1 else 0
    lam = {(((tau - s_) // pD) * uinv) % pD2 if pD2 > 1 else 0 for s_ in lift}
    qN = p ** V[N]
    C = set()
    for z in PS:
        Sc = Se + z
        if Sc % qN == 0:
            C.add(target(Sc, P[N], p, D2))
    stat["parents (" + tag + ")"] += 1
    if lift:
        stat["parents with children (" + tag + ")"] += 1
    if lam != C or len(lam) != len(lift):
        fails["Lemma L (" + tag + ")"] += 1
        print("FAIL", tag, p, x, n, N, N2)


def main():
    p = int(sys.argv[1])
    seed = int(sys.argv[2])
    ns = int(sys.argv[3])
    rng = random.Random(seed)
    t0 = time.time()
    stat = Counter()
    fails = Counter()
    maxK = 0
    for it in range(ns):
        s = rng.choice([6, 9, 12])
        if it % 2 == 0:
            m = 2
        else:
            m = rng.randint(2, 12)
        u = rand_unit(p, rng, p ** 2, p ** 8)
        x = u * p ** s - m
        assert vp(x + m, p) == s
        where = rng.choice(["before", "straddle", "after", "start-at-m"])
        H = rng.randint(1, 10)
        H2 = rng.randint(1, 8)
        if where == "before":
            N = rng.randint(m - 1, m + 3)  # window ends near m; W' may contain m
            N = max(N, 2)
            n = max(1, N - H)
        elif where == "straddle":
            n = rng.randint(max(1, m - H), max(1, m - 1))
            N = n + H
            if N < m:
                N = m
        elif where == "start-at-m":
            n = m
            N = n + H
        else:
            n = m + rng.randint(1, 6)
            N = n + H
        N2 = N + H2
        P = pis(x, N2)
        V = Vlist(x, N2, p)
        D, D2 = V[N] - V[n], V[N2] - V[N]
        K = D + D2
        maxK = max(maxK, K)
        W = Window(x, n, N, p)
        modK = p ** K
        Sig = {0}
        for yi in W.y:
            Sig |= {(z + yi) % modK for z in Sig}
        if p ** K <= 10 ** 6:
            arr = W.sums_mask(K)
            stat["Sigma set vs bitset cross-checks"] += 1
            if set(int(z) for z in arr.nonzero()[0]) != Sig:
                fails["Sigma set vs bitset"] += 1
        PS = [0]
        for i in range(N - n):
            PS = PS + [z + P[n + i] for z in PS]
        stat["windows (" + where + ")"] += 1
        # explicit high-slope parent for m = 2
        if m == 2 and n >= 4:
            e = (1, 1, 0, 1) + (0,) * (n - 4)
            Se = sum(P[j] for j in range(n) if e[j])
            if Se != (x + 2) ** 3:
                fails["cube identity"] += 1
            dP = dpis(x, n)
            sl = vp(sum(dP[j] for j in range(n) if e[j]), p)
            stat["cube-path slope == 2s"] += int(sl == 2 * s)
            if Se % p ** V[n] == 0:
                check_parent(p, x, n, N, N2, Se, P, V, PS, Sig, W, stat, fails,
                             "cube path (1,1,0,1,0..)")
            else:
                stat["cube path dead at n"] += 1
        parents = alive_paths_dfs(x, n, p, P=P, V=V, cap=100000)
        if parents is None:
            stat["skipped parents (cap)"] += 1
            continue
        if len(parents) > 25:
            parents = rng.sample(parents, 25)
        for e, Se in parents:
            check_parent(p, x, n, N, N2, Se, P, V, PS, Sig, W, stat, fails, "all")
    print("p=%d seed=%d samples=%d  max K=%d  time=%.1fs" % (p, seed, ns, maxK, time.time() - t0))
    for k in sorted(stat):
        print("  %-44s %d" % (k, stat[k]))
    print("  failures:", dict(fails))
    print("TOTAL FAILURES", sum(fails.values()))


if __name__ == "__main__":
    main()
