"""t5: Prop D at the real geometry of the p=7 atom, at exactly computable scales.
For a window start n = n_{l-1} (l = 0..LMAX) and a scale j <= JMAX, let N'_j be the first position
with V_{N'_j} - V_n >= j.  If V_{N'_j} - V_n == j exactly, then, since the composite-window elements
beyond N'_j vanish mod p^j, p^j Coll_j(x) of the full window equals that of [n, N'_j), and Prop D
(with K = j) must bound it.  x ranges over x_A and random points of the atom A = x_A + 7^51 Z_7
(all have the same gate pattern there).  Exact DP mod p^j (all digits signed).
usage: python3 t5_atom_lowscale.py ATOMFILE LMAX JMAX NPTS SEED
"""
import sys, random
from fractions import Fraction
import vf_lib as L

atomfile, LMAX, JMAX, NPTS, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
random.seed(seed)
cfg = dict(l.strip().split("=", 1) for l in open(atomfile) if "=" in l)
p = int(cfg["p"]); m = int(cfg["m"]); xA = int(cfg["xA"])
E = 120
times = [int(cfg["n0"])]
while len(times) < LMAX + 3:
    times.append(-(-27 * times[-1] // 20))
pts = [xA] + [(xA + p ** m * random.randrange(p ** (E - m))) % p ** E for _ in range(NPTS - 1)]
ok = bad = skipped = 0
maxr = 0.0
for l in range(0, LMAX + 1):
    n = times[l]
    for j in range(1, JMAX + 1):
        # find N'_j
        lev = 0; Np = n
        while lev < j:
            Np += 1
            if (xA + Np) % p == 0:
                lev += L.vmod(xA + Np, p, E)
        if lev != j:
            skipped += 1
            continue
        gl = [(i, L.vmod(xA + i, p, E)) for i in range(n + 1, Np + 1) if (xA + i) % p == 0]
        bound = L.block_bound(p, gl, n, Np, j, None)
        bF = Fraction(int(bound.numerator), int(bound.denominator))
        # extend the window by a few more elements (they must not change Coll_j)
        Hext = Np - n + 3 * p
        for x in pts:
            dp = L.coll_counts(p, x, n, Hext, j)
            c, tot = dp.count_zero_fast(j, 0)
            val = Fraction(p ** j * c, tot)
            dp2 = L.coll_counts(p, x, n, Np - n, j)
            c2, tot2 = dp2.count_zero_fast(j, 0)
            assert Fraction(c2, tot2) == Fraction(c, tot), "extension changed Coll_j"
            if val <= bF:
                ok += 1
            else:
                bad += 1
                print(f"PROP D FAIL at atom: l={l} n={n} Np={Np} j={j} p^j Coll_j={float(val)} bound={float(bF)}")
            maxr = max(maxr, float(val / bF))
        print(f"l={l} n={n} j={j} N'_j={Np}: p^j Coll_j(x_A) = {float(Fraction(p**j*L.coll_counts(p, xA, n, Np-n, j).count_zero_fast(j,0)[0], 4**(Np-n))):.6f}  Prop D = {float(bF):.6f}", flush=True)
print(f"checks: {ok} ok, {bad} violations, {skipped} (l,j) skipped (level jumps past j); max ratio {maxr:.4f}")
