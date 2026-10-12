# Direct numerical test of Lemma S / Lemma T (stability balls, exact one-class transitions).
import random, sys
def v2(n):
    if n == 0: return 10**9
    return (n & -n).bit_length() - 1
def gamma_and_B(x, path):
    """exact: returns (S, pi_n, Bnum, Bden) with gamma_n = S/pi_n and B_n(x,x) = sum gamma_i pi_{i-1} as fraction"""
    from fractions import Fraction
    S = 0; pi = 1; B = Fraction(0)
    for i, e in enumerate(path):
        if e: S += pi
        pin = pi * (x + i + 1)
        B += Fraction(S * pi, pin)
        pi = pin
    return S, pi, B
def vf(q):
    if q == 0: return 10**9
    return v2(q.numerator) - v2(q.denominator)
def valid(x, path):
    S = 0; pi = 1
    for i, e in enumerate(path):
        if e: S += pi
        pi *= (x + i + 1)
    return v2(S) >= v2(pi) if S != 0 else True
def paths_valid(x, n, cap=50):
    out = [(1,)] if v2(x + 1) == 0 else []
    for k in range(2, n + 1):
        new = []
        for p in out:
            for e in (0, 1):
                q = p + (e,)
                if valid(x, q[:k]) and valid(x, q): new.append(q)
        out = new[:cap]
    return out
rnd = random.Random(int(sys.argv[1])); n = int(sys.argv[2]); trials = int(sys.argv[3])
nT = 0; badT = 0; nS = 0; caseii = 0
for t in range(trials):
    x = rnd.getrandbits(300) & ~1
    if rnd.random() < 0.3:   # force some case (ii): put -(n+1) near x
        x = (-(n + 1) + (rnd.getrandbits(250) << rnd.randrange(8, 40))) % (1 << 300)
        if x % 2: continue
    for p in paths_valid(x, n):
        S, pi, B = gamma_and_B(x, p)
        kap = vf(B); M = max(v2(x + l) for l in range(1, n + 1))
        sig = v2(pi) - kap
        if not (sig >= kap + M + 1): continue
        nS += 1
        d = v2(x + n + 1)
        if d < sig:
            # case (i): classes x + 2^sig * j, j < 2^d; for each e_n exactly one j valid
            for en in (0, 1):
                good = []
                for j in range(1 << d):
                    xp = x + (j << sig) + (rnd.getrandbits(60) << (sig + d))
                    if valid(xp, p + (en,)): good.append(j)
                nT += 1
                if len(good) != 1:
                    badT += 1; print("case(i) FAIL", n, d, sig, kap, good)
        else:
            caseii += 1
            # case (ii): c = gamma_n(-(n+1)) + e_n ; predicted tau = sig + v(c)
            from fractions import Fraction
            Sm, pim, _ = gamma_and_B(-(n + 1), p)
            for en in (0, 1):
                c = Fraction(Sm, pim) + en
                tau = sig + vf(c)
                # count valid classes among x' = -(n+1) + 2^tau*u, u odd mod 2^sig
                good = []
                for u in range(1, 1 << sig, 2) if sig <= 12 else []:
                    xp = -(n + 1) + (u << tau) + (rnd.getrandbits(60) << (tau + sig))
                    if valid(xp, p + (en,)): good.append(u)
                # also check other spheres tau' != tau give nothing (sample)
                other = 0
                for tp in range(sig, sig + 6):
                    if tp == tau: continue
                    for _ in range(8):
                        u = rnd.getrandbits(40) | 1
                        xp = -(n + 1) + (u << tp)
                        if valid(xp, p + (en,)): other += 1
                if sig <= 12:
                    nT += 1
                    if len(good) != 1 or other:
                        badT += 1; print("case(ii) FAIL", n, sig, kap, tau, len(good), other)
print("n", n, "stable paths tested", nS, "transition tests", nT, "failures", badT, "caseii", caseii)
