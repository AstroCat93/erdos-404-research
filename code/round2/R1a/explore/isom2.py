import random, sys
from fractions import Fraction
from isom import valid_paths, gamma_exact, Bval, vfrac, v2
rnd = random.Random(int(sys.argv[1])); n = int(sys.argv[2]); trials = int(sys.argv[3])
bad = 0; tot = 0; skipped = 0
for t in range(trials):
    x = rnd.getrandbits(400) & ~1
    M = max(v2(x + l) for l in range(1, n + 1))
    paths = valid_paths(x, n, 400)
    for path in paths[:6]:
        S, pi = gamma_exact(x, path)
        g = Fraction(S, pi)
        kap = vfrac(Bval(x, path))
        rho = v2(pi) - kap
        if rho <= M: skipped += 1; continue
        for _ in range(4):
            z = rnd.getrandbits(60) | 1
            j = rnd.randrange(0, 6)
            xp = x + (z << (rho + j))
            S2, pi2 = gamma_exact(xp, path)
            g2 = Fraction(S2, pi2)
            tot += 1
            ok = vfrac(g2) >= 0 and vfrac(g2 - g) == j
            if not ok:
                bad += 1
                if bad < 10: print("FAIL x%64=", x % 64, "n", n, "kap", kap, "rho", rho, "M", M, "j", j, "v(g2)", vfrac(g2), "v(diff)", vfrac(g2 - g))
print("n", n, "tests", tot, "failures", bad, "skipped(rho<=M)", skipped)
