import random, sys
from fractions import Fraction
from lemmaT_test import v2, gamma_and_B, vf, valid, paths_valid
rnd = random.Random(int(sys.argv[1])); n = int(sys.argv[2]); trials = int(sys.argv[3])
nT = bad = nS = 0
for t in range(trials):
    tau0 = rnd.randrange(4, 16)
    x = -(n + 1) + ((rnd.getrandbits(200) | 1) << tau0)
    if x % 2: continue
    for p in paths_valid(x, n):
        S, pi, B = gamma_and_B(x, p)
        kap = vf(B); M = max(v2(x + l) for l in range(1, n + 1))
        sig = v2(pi) - kap
        if not (sig >= kap + M + 1): continue
        if v2(x + n + 1) < sig: continue
        if sig > 11: continue
        nS += 1
        Sm, pim, _ = gamma_and_B(-(n + 1), p)
        g = Fraction(Sm, pim)
        assert vf(g) >= 0  # -(n+1) valid through n (Lemma S)
        for en in (0, 1):
            c = g + en
            if c == 0: print("c=0 case"); continue
            tau = sig + vf(c)
            good = [u for u in range(1, 1 << sig, 2)
                    if valid(-(n + 1) + (u << tau) + (rnd.getrandbits(50) << (tau + sig)), p + (en,))]
            other = 0
            for tp in range(sig, sig + 8):
                if tp == tau: continue
                for _ in range(6):
                    if valid(-(n + 1) + ((rnd.getrandbits(40) | 1) << tp), p + (en,)): other += 1
            nT += 1
            if len(good) != 1 or other: bad += 1; print("FAIL", n, sig, kap, tau, len(good), other)
print("n", n, "case(ii) stable paths", nS, "tests", nT, "failures", bad)
