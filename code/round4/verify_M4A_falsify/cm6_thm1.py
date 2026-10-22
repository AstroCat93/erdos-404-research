"""cm6: Theorem 1 (exact identity), Lemma F, Props D and E on balls B = x0 + p^b Z_p, exact, at
p = 7, 11, 13 (small levels).  B is chosen so that the gate pattern of (n, N'] is constant on B
(b > M_W) and theta = min(ceil(D/2), D-b+1) >= 1.  All x in B mod p^R (R = max(K, theta)) enumerated.
Point kinds: 'rand', 'neg2' (x0 near -(n+2): a gate at distance 2 from the window start), 'neg1'.
usage: python3 cm6_thm1.py p SEED NB KMAX
"""
import sys, random
from fractions import Fraction
import cm_lib as L

p, seed, NB, KMAX = map(int, sys.argv[1:5])
random.seed(seed)
EP = 40
PE = p ** EP
C = L.Consts(p, sx=(5 if p > 13 else 6))


def ycs(x, n, H, mod_a, mod_b):
    """y_c(x) = prod_{i<=c}(x+n+i) and d/dx, reduced mod mod_a / mod_b"""
    Y, Yd = [1], [0]
    for c in range(1, H):
        Yd.append((Yd[-1] * (x + n + c) + Y[-1]) % PE)
        Y.append(Y[-1] * (x + n + c) % PE)
    return [a % mod_a for a in Y], [a % mod_b for a in Yd]


def G_exact(u, t, k, f):
    """p^k P(v(T_u) >= k, v(T_u') >= f), dt_0 = 1"""
    ff = max(f, 0)
    dp = L.JointDP(p, k, ff, 2 if 2 * t < 118 else 3)
    Pv, Pd = 1, 0
    for c in range(t):
        if c >= 1:
            Pd = (Pd * (u + c) + Pv) % PE
            Pv = Pv * (u + c) % PE
        dp.step(Pv, Pd, fixed=(c == 0))
    return Fraction(p ** k * dp.count(k, ff), 4 ** dp.ns)


stats = dict(balls=0, thm1=0, lemF=0, propD=0, propE=0, eqF=0)
tries = 0
while stats["balls"] < NB and tries < 50 * NB:
    tries += 1
    kind = ["rand", "neg2", "neg1"][tries % 3]
    n = random.randrange(1, 4 * p)
    x0 = random.randrange(PE)
    if kind != "rand":
        dist = 2 if kind == "neg2" else 1
        x0 = (-(n + dist) + p ** random.randrange(1, 3) * random.randrange(1, PE)) % PE
    K = random.randrange(2, KMAX + 1)
    gl, lev, Np = [], 0, n
    while lev < K:
        Np += 1
        if (x0 + Np) % p == 0:
            s = L.vp((x0 + Np) % PE, p)
            gl.append((Np, s)); lev += s
    if lev != K or len(gl) < 2:
        continue
    # D = level after some gate before the last; N anywhere in [that gate, next gate)
    jg = random.randrange(len(gl) - 1)
    D = sum(s for _, s in gl[:jg + 1])
    N = random.randrange(gl[jg][0], gl[jg + 1][0])
    MW = max(s for _, s in gl)
    b = MW + 1 + random.randrange(2)
    theta = min(-(-D // 2), D - b + 1)
    if theta < 1:
        continue
    H = Np - n
    R = max(K, theta, b)
    xs = [(x0 + p ** b * w) % PE for w in range(p ** (R - b))]
    # every x in B has the same gate pattern on (n, N']
    assert all([(i, L.vp((x + i) % PE, p)) for i in range(n + 1, Np + 1) if (x + i) % p == 0] == gl for x in xs[:5])
    lhs = Fraction(0); hs = Fraction(0); hsD = Fraction(0)
    propD_ok = True
    PDb = L.propDE_block(p, gl, n, Np, K, C)
    PDF = Fraction(int(PDb.numerator), int(PDb.denominator))
    for x in xs:
        Y, Yd = ycs(x, n, H, p ** K, p ** theta)
        dp = L.JointDP(p, K, theta, 2 if 2 * H < 118 else 3)
        for c in range(H):
            dp.step(Y[c], Yd[c])
        tot = 4 ** H
        cK0, cD0 = dp.count(K, 0), dp.count(D, 0)
        cKt, cDt = dp.count(K, theta), dp.count(D, theta)
        eps = Fraction(p ** K * cK0 - p ** D * cD0, tot)
        lhs += eps
        hs += Fraction(p ** K * (cKt - 2 ** H), tot)
        hsD += Fraction(p ** D * (cDt - 2 ** H), tot)
        if Fraction(p ** K * cK0, tot) > PDF:
            propD_ok = False
            print(f"PROP D FAIL p={p} x={x} n={n} N'={Np} K={K}")
    nx = len(xs)
    lhs /= nx; hs /= nx; hsD /= nx
    rhs = Fraction(p ** K - p ** D, 2 ** H) + hs - hsD
    t1 = (lhs == rhs)
    # Lemma F (needs M_W <= K - theta)
    lf = None
    if MW <= K - theta:
        bound = Fraction(0)
        a = 0
        for c in range(H):
            a = sum(s for g, s in gl if g <= n + c)
            if a >= K:
                bound += Fraction(p ** K, 2 ** (c + 1))
                continue
            sup = max(G_exact((x + n + c) % PE, H - c, K - a, theta - a) for x in xs)
            bound += Fraction(p ** a, 2 ** (c + 1)) * sup
        lf = hs <= bound
        stats["eqF"] += (hs == bound)
        fp = min(theta, K - MW)
        PEb = L.propDE_block(p, gl, n, Np, K, C, fprime=fp)
        pe = lhs <= Fraction(int(PEb.numerator), int(PEb.denominator))
        stats["propE"] += pe
        if not pe:
            print(f"PROP E FAIL p={p} n={n} N={N} N'={Np} D={D} K={K} b={b}")
    stats["balls"] += 1
    stats["thm1"] += t1
    stats["lemF"] += (lf is not False)
    stats["propD"] += propD_ok
    if not t1:
        print(f"THEOREM 1 FAIL p={p} kind={kind} n={n} N={N} N'={Np} D={D} K={K} b={b} theta={theta}: lhs {lhs} rhs {rhs}")
    if lf is False:
        print(f"LEMMA F FAIL p={p} kind={kind} n={n} N={N} N'={Np} D={D} K={K} b={b} theta={theta}")
    print(f"ball {stats['balls']}: kind={kind} n={n} N={N} N'={Np} gates={gl} D={D} K={K} b={b} theta={theta} |B mod p^R|={nx}: "
          f"E_B eps = {float(lhs):.6g}, Thm1 identity {t1}, high-slope terms {float(hs):.4g} / {float(hsD):.4g}, LemmaF {lf}", flush=True)
print(f"RESULT p={p}: {stats['balls']} balls; Theorem 1 exact {stats['thm1']}/{stats['balls']}; Lemma F holds {stats['lemF']}/{stats['balls']} "
      f"(equality {stats['eqF']}); Prop D (every x) {stats['propD']}/{stats['balls']}; Prop E {stats['propE']} ok")
