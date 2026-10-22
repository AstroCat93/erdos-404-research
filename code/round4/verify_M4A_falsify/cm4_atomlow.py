"""cm4: Prop D at the real geometry of the Cor M' atoms (p = 11..23), at exactly computable scales.
For each window start n = n_l (l = 0..LMAX) and scale j <= JMAX: N'_j = first N' with V_N' - V_n >= j.
If the level is exactly j, the composite window [n, N'_j) gives p^j Coll_j(x), computed exactly
(signed DP mod p^j over all H = N'_j - n elements, CRT counts) at x_A and at NPTS-1 random x in A;
it must be <= Prop D (K = j), evaluated by cm_lib.propDE_block.  The extension of the window by 2p more
elements must not change Coll_j (they vanish mod p^j) -- also checked.
usage: python3 cm4_atomlow.py ATOMFILE LMAX JMAX NPTS SEED
"""
import sys, random
from fractions import Fraction
import cm_lib as L

atomfile, LMAX, JMAX, NPTS, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
random.seed(seed)
cfg = dict(l.strip().split("=", 1) for l in open(atomfile) if "=" in l)
p, m, xA, n0 = int(cfg["p"]), int(cfg["m"]), int(cfg["xA"]), int(cfg["n0"])
C = L.Consts(p)
times = [n0]
while len(times) < LMAX + 3:
    times.append(-(-27 * times[-1] // 20))
pts = [xA] + [xA + p ** m * random.randrange(1, p ** 30) for _ in range(NPTS - 1)]


def coll_count(x, n, H, j):
    npr = 2 if 2 * H < 118 else (3 if 2 * H < 178 else 4)
    dp = L.JointDP(p, j, 0, npr)
    y = 1
    mod = p ** j
    for c in range(H):
        if c >= 1:
            y = y * (x + n + c) % mod
        dp.step(y, 0)
    return Fraction(p ** j * dp.count(j, 0), 4 ** dp.ns)


ok = bad = skipped = 0
maxr = Fraction(0)
for l in range(0, LMAX + 1):
    n = times[l]
    for j in range(1, JMAX + 1):
        lev, Np = 0, n
        while lev < j:
            Np += 1
            if (xA + Np) % p == 0:
                lev += L.vp(xA + Np, p)
        if lev != j:
            skipped += 1
            continue
        gl = [(i, L.vp(xA + i, p)) for i in range(n + 1, Np + 1) if (xA + i) % p == 0]
        b = L.propDE_block(p, gl, n, Np, j, C)
        bF = Fraction(int(b.numerator), int(b.denominator))
        vals = []
        for x in pts:
            val = coll_count(x, n, Np - n, j)
            if x == xA:
                assert coll_count(x, n, Np - n + 2 * p, j) == val, "extension changed Coll_j"
            vals.append(val)
            if val <= bF:
                ok += 1
            else:
                bad += 1
                print(f"PROP D FAIL p={p} l={l} n={n} N'={Np} j={j}: p^j Coll_j = {val} > {bF}")
            maxr = max(maxr, val / bF)
        exb = bF - 1
        print(f"p={p} l={l} n={n} j={j} N'_j={Np} gates={gl}: p^j Coll_j - 1 in [{float(min(vals) - 1):.6e}, {float(max(vals) - 1):.6e}], Prop D - 1 = {float(exb):.6e}"
              + (f", max excess ratio {float((max(vals) - 1) / exb):.6f}" if exb > 0 else ""), flush=True)
print(f"RESULT p={p}: {ok} checks ok, {bad} violations, {skipped} (l,j) skipped (level jumps past j); max ratio {float(maxr):.6f}")
