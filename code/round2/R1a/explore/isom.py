# Test the scaled-isometry claim: for a path e valid through n at x, with kappa=v(B_n(x,x)),
# rho = v(pi_n(x)) - kappa: for x' = x + 2^rho z, is e valid at x' and v(gamma_n(x')-gamma_n(x)) = v(z)?
import random, sys
from fractions import Fraction
def v2(n):
    if n == 0: return 10**9
    return (n & -n).bit_length() - 1
def valid_paths(x, n, M):
    # return list of (path tuple) valid through step n (gamma_n integral), via DP tracking gamma mod 2^Mcur
    Mcur = M
    if v2(x+1) > 0: return []
    pop = [((1,), pow(x+1, -1, 1 << M))]
    for k in range(2, n+1):
        d = v2(x + k); Mnew = Mcur - d
        inv = pow(((x + k) >> d) % (1 << Mnew), -1, 1 << Mnew)
        new = []
        for (p, g) in pop:
            for e in (0, 1):
                y = (g + e) % (1 << Mcur)
                if d and (y & ((1 << d) - 1)): continue
                new.append((p + (e,), ((y >> d) * inv) % (1 << Mnew)))
        pop = new; Mcur = Mnew
        if len(pop) > 2000: pop = pop[:2000]
    return [p for (p, g) in pop]
def gamma_exact(x, path):
    # exact rational gamma_n = S/pi_n
    S = 0; pi = 1
    for i, e in enumerate(path):
        if e: S += pi
        pi *= (x + i + 1)
    return S, pi
def Bval(x, path):
    # B_n = sum_{i=1}^n gamma_i(x) pi_{i-1}(x) as exact rational
    S = 0; pi = 1; B = Fraction(0)
    pis = [1]
    for i, e in enumerate(path):
        if e: S += pi
        pi_next = pi * (x + i + 1)
        gam = Fraction(S, pi_next)
        B += gam * pi
        pi = pi_next
    return B
def vfrac(q):
    if q == 0: return 10**9
    return v2(q.numerator) - v2(q.denominator)
rnd = random.Random(int(sys.argv[1])); n = int(sys.argv[2]); trials = int(sys.argv[3])
bad = 0; tot = 0
for t in range(trials):
    x = rnd.getrandbits(400) & ~1
    paths = valid_paths(x, n, 400)
    for path in paths[:5]:
        S, pi = gamma_exact(x, path)
        g = Fraction(S, pi)
        assert vfrac(g) >= 0
        kap = vfrac(Bval(x, path))
        rho = v2(pi) - kap
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
                if bad < 10: print("FAIL x%64=", x % 64, "n", n, "kap", kap, "rho", rho, "j", j, "v(g2)", vfrac(g2), "v(diff)", vfrac(g2 - g))
print("tests", tot, "failures", bad)
