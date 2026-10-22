"""cm7: Lemma H (Hensel step) exactly, at p = 7, 11, 13, 17, 19, 23, on adversarial polynomials.
LHS = p^k' mu_B{v(S)>=k'} - p^k mu_B{v(S)>=k};  RHS = same with both sets intersected with
H = {v(S) >= k, v(S') >= theta},  theta = min(ceil(k/2), k-b+1).  All z in B mod p^R enumerated
(R = max(k', theta, b)).  Polynomials: random, (X-z0)^2 + p^j c, (X-z0)^2 (X-z1), (X+2)^2 (the
double root behind R3M Prop N3), signed carry polynomials 1 + sum d_c pi_c(X) (some with a planted
double root), cubes.  Balls often centred at the (near-)root.  Control: theta+1 must fail sometimes.
usage: python3 cm7_lemmaH.py p SEED NCASES KPMAX
"""
import sys, random
from fractions import Fraction
import cm_lib as L

p, seed, NC, KPMAX = map(int, sys.argv[1:5])
random.seed(seed)


def polymul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r


def ev(P, z, mod):
    v = 0
    for c in reversed(P):
        v = (v * z + c) % mod
    return v


def deriv(P):
    return [i * P[i] for i in range(1, len(P))] or [0]


def carry_poly(t, dl):
    P = [0]; cur = [1]
    for c in range(t):
        if c >= 1:
            cur = polymul(cur, [c, 1])
        if dl[c]:
            P = [a + dl[c] * b for a, b in zip(P + [0] * (len(cur) - len(P)), cur + [0] * (len(P) - len(cur)))]
    return P


def v_or_big(a, mod_exp):
    return L.vp(a, p) if a % p ** mod_exp else mod_exp


ok = bad = ctrl = trivial = 0
for case in range(NC):
    kind = case % 6
    z0 = random.randrange(p ** 6)
    if kind == 0:
        P = [random.randrange(-p ** 3, p ** 3) for _ in range(random.randrange(2, 7))]
    elif kind == 1:
        j = random.randrange(1, 6)
        P = polymul([-z0, 1], [-z0, 1]); P[0] += p ** j * random.randrange(1, p)
    elif kind == 2:
        P = polymul(polymul([-z0, 1], [-z0, 1]), [-(z0 + p ** random.randrange(0, 3)), 1])
    elif kind == 3:
        z0 = -2 + p ** random.randrange(1, 4) * random.randrange(p)
        P = [4, 4, 1]                     # (X+2)^2
    elif kind == 4:
        t = random.randrange(3, p + 3)
        dl = [1] + [random.choice((-1, 0, 0, 1)) for _ in range(t - 1)]
        P = carry_poly(t, dl)
        # try to centre at a near double root mod p^2
        for u in range(p * p):
            if ev(P, u, p * p) == 0 and ev(deriv(P), u, p) == 0:
                z0 = u; break
    else:
        P = polymul(polymul([-z0, 1], [-z0, 1]), [-z0, 1])
    if not any(P[1:]):
        continue
    Pd = deriv(P)
    b = random.randrange(0, 4)
    k = random.randrange(1, KPMAX + 1)
    kp = random.randrange(k, KPMAX + 1)
    theta = min(-(-k // 2), k - b + 1)
    if theta <= 0:
        trivial += 1
    R = max(kp, theta + 1, b)
    zs = [z0 + p ** b * w for w in range(p ** (R - b))]
    nz = len(zs)
    vals = [(v_or_big(ev(P, z, p ** R), R), v_or_big(ev(Pd, z, p ** R), R)) for z in zs]

    def side(th):
        A = sum(1 for vs, vd in vals if vs >= kp); Bc = sum(1 for vs, vd in vals if vs >= k)
        HA = sum(1 for vs, vd in vals if vs >= kp and vs >= k and vd >= th)
        HB = sum(1 for vs, vd in vals if vs >= k and vd >= th)
        return Fraction(p ** kp * A - p ** k * Bc, nz), Fraction(p ** kp * HA - p ** k * HB, nz)

    l, r = side(theta)
    if l == r:
        ok += 1
    else:
        bad += 1
        print(f"LEMMA H FAIL p={p} kind={kind} P={P} z0={z0} b={b} k={k} k'={kp} theta={theta}: {l} != {r}")
    l2, r2 = side(theta + 1)
    ctrl += (l2 != r2)
print(f"RESULT p={p}: Lemma H exact in {ok}/{ok + bad} cases ({trivial} with theta <= 0); control theta+1 fails in {ctrl}")
