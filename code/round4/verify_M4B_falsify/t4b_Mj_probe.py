"""t4b_Mj_probe.py -- probe of the remark in the proof of B1' that M_j = c_{n_j} Z0_{n_j} is bounded.
The bound p^{V}/2 <= p^{n/(p-1) + log_p(e(n-1)!)}/2 holds for each fixed n; this probe looks for points
with a deep gate (depth s close to the Observation-G cutoff) where the slope-0 population is nonempty,
and reports the largest M_n found for each n. If max M_n grows with n, then sup_x M_j(x) is finite
only when n_j takes finitely many values (true for n_0, n_1 and for rules with bounded range).
Usage: python3 t4b_Mj_probe.py SEED NTRY"""
import sys, random, math
from fz_lib import *
seed, NTRY = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
p = 7
for n in (14, 21, 28, 35):
    best = Fraction(0); bestinfo = None; found = 0; maxs = 0
    for _ in range(NTRY):
        i = rng.randrange(max(3, n // 2), n + 1)
        smax = 1
        while p ** (smax + 1) <= math.e * math.factorial(i - 1):
            smax += 1
        s = rng.randrange(1, smax + 1)
        X = (-i + p ** s * (1 + p * rng.randrange(p ** 30)))
        X %= p ** 60
        vl = vals(X, p, n); V, M = prefix(vl)
        if V[n] > 20 or vl[i] != s:
            continue
        Z0, _ = dp_profile(X, p, n)
        if Z0[n] > 0:
            found += 1
            Mn = c_n(n, V[n], p) * Z0[n]
            maxs = max(maxs, s)
            if Mn > best:
                best = Mn; bestinfo = (i, s, V[n], Z0[n])
    print(f"RESULT p={p} n={n}: {found} deep-gate points with Z0>0 out of {NTRY}; deepest gate with Z0>0: s = {maxs}; max M_n = {float(best):.4g} at (gate i, depth s, V_n, Z0) = {bestinfo}")
