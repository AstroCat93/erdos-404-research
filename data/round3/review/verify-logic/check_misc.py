# Referee check (verify-logic, round 3): assorted finite claims of Section 11, recomputed independently.
import math, itertools, cmath
from fractions import Fraction

def v(z, p):
    z = Fraction(z)
    if z == 0: return 10**9
    a, b = z.numerator, z.denominator; k = 0
    while a % p == 0: a //= p; k += 1
    while b % p == 0: b //= p; k -= 1
    return k

def pi(x, k):
    r = 1
    for i in range(1, k + 1): r *= (x + i)
    return r

print("== Prop 11.25 finite cases ==")
# (a) S_e(-4) for e1,e2,e3
vals = sorted({1 - 3 * a + 6 * b - 6 * c for a in (0, 1) for b in (0, 1) for c in (0, 1)})
print(" S_e(-4) values", vals, "max v2 =", max(v(t, 2) for t in vals))
# (b) Phi_e(-4) with e2=1,e3=0 and e2=0,e3=1, depending on e4,e5
def Phi(y, e2, tail):  # tail = e_3, e_4, ...
    return e2 - Fraction(1, 1 - y) + sum(t * pi(y, k) for k, t in enumerate(tail, start=1))
A = sorted({Phi(-4, 1, (0, a, b)) for a in (0, 1) for b in (0, 1)}); B = sorted({Phi(-4, 0, (1, a, b)) for a in (0, 1) for b in (0, 1)})
print(" family e2=1:", A, [v(t, 2) for t in A]); print(" family e3=1:", B, [v(t, 2) for t in B])
hist = {}
for tail in itertools.product((0, 1), repeat=6):
    val = Phi(-8, 0, (1,) + tail)
    assert val != 0
    hist[v(val, 2)] = hist.get(v(val, 2), 0) + 1
print(" Phi_e(-8), e2=0,e3=1, histogram of v2:", dict(sorted(hist.items())))
# identity S_e(x) = y(y-1)Phi_e(y), y=x+2, on random paths
import random; random.seed(5)
for _ in range(500):
    x = random.randrange(-10**6, 10**6) * 4 + 2
    e = [1, 1] + [random.randrange(2) for _ in range(10)]
    S = sum(e[j] * pi(x, j) for j in range(len(e)))
    y = x + 2
    assert S == y * (y - 1) * Phi(y, e[2], e[3:]), "identity fails"
print(" identity S_e = y(y-1)Phi_e(y): 500 random cases OK;  S_{1,3} =", [1 + pi(x, 1) + pi(x, 3) - (x + 2) ** 3 for x in range(-5, 5)])

print("== Prop 11.13(b): F_e = y H(y), H(0)=-c!, H'(0) unit ==")
for p in (2, 3, 5, 7):
    for c in range(2 * p, 2 * p + 4):
        H0 = -math.factorial(c); dH0 = 1 + math.factorial(c) - sum(math.factorial(c) // i for i in range(1, c + 1))
        assert dH0 % p != 0, (p, c)
print(" H'(0) is a p-unit for p in {2,3,5,7}, 2p<=c<2p+4")

print("== Thm 11.15 Step 0(b): f(u)=u+v(u!) hits every residue mod k with p|u ==")
def vfact(u, p):
    s = 0; q = p
    while q <= u: s += u // q; q *= p
    return s
bad = []
for p in (2, 3, 5, 7):
    for k in range(1, 40):
        hit = set()
        for u in range(0, p ** 7, p):
            hit.add((u + vfact(u, p)) % k)
            if len(hit) == k: break
        if len(hit) < k: bad.append((p, k))
print(" failures:", bad)

print("== c_p (Remark 11.9 / Computation 11.58) and Lemma 11.54 ==")
for p in (3, 5, 7, 11, 13):
    prods = [math.prod(abs(math.cos(math.pi * xi * math.factorial(r) / p)) for r in range(p)) for xi in range(1, p)]
    gm = math.exp(sum(math.log(t) for t in prods) / (p - 1))
    # worst incomplete block: units (p-2)!, (p-1)!
    wib = max(abs(math.cos(math.pi * xi * math.factorial(p - 2) / p) * math.cos(math.pi * xi * math.factorial(p - 1) / p)) for xi in range(1, p))
    print(f" p={p} c_p={max(prods):.7g} geo-mean*2^p={gm * 2 ** p:.12f} worst-incomplete={wib:.6f} cos^2(pi/p)={math.cos(math.pi / p) ** 2:.6f}")

print("== Thm 11.48(c): c_1(13,rho) ==")
p = 13
c1 = []
for rho in range(p):
    tot = 0.0
    for xi in range(1, p):
        pr = 1.0
        for u in range(rho + 1):
            pr *= math.cos(math.pi * xi * (-1) ** rho * math.factorial(rho) * (-1) ** u / (math.factorial(u) * p)) ** 2
        tot += pr
    c1.append(tot)
print(" min_rho c_1(13,rho) =", min(c1), " 13^4*min =", 13 ** 4 * min(c1), " 13^5*max =", 13 ** 5 * max(c1))

print("== Thm 11.50 Legendre values ==")
for D in (8, 9):
    n = 19 ** D - 1
    print(" v_19((19^%d-1)!) =" % D, vfact(n, 19))

print("== Prop 11.53: N_G(-2) = 2^{M_G-1} ==")
for p, G in [(2, 6), (3, 3), (5, 2), (7, 2), (3, 4)]:
    MG = max(b for b in range(1, p * G + 2) if vfact(b, p) < G)
    x = -2
    cnt = 0
    for B in itertools.product((0, 1), repeat=MG):
        S = 1 + sum(pi(x, b + 1) for b in range(MG) if B[b])
        if S % p ** G == 0: cnt += 1
    print(f" p={p} G={G} M_G={MG} N_G(-2)={cnt} 2^(M_G-1)={2 ** (MG - 1)}")

print("== Cor 11.30 main constants ==")
al = 0.227
H2 = lambda a: -a * math.log2(a) - (1 - a) * math.log2(1 - a)
print(" 1-H2(0.227) =", 1 - H2(al))
for name, k, r0, L, l0, sL, EC in [("C0", 3, 0, 1, 4, 2, 1), ("C2", 3, 2, 3, 8, 3, 64), ("C6", 4, 6, 6, 14, 3, 16384)]:
    sr0 = bin(r0).count('1')
    assert sL == max(bin(d).count('1') for d in range(l0))
    const = (2 ** (1 + sL - sr0) * EC + 2 ** -k) * 2 ** (al * k) * 8 ** al
    print(f" {name}: main constant {const:.6g}")
