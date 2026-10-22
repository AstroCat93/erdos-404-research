# Referee check: Lemma 11.37 (gate-block law), theta_p and theta_set_p (Thm 11.38),
# Prop 11.41(b) conditional law, and exact C_k for small depths (Computation 11.43),
# written independently of track T3a's code.
import math, itertools
from fractions import Fraction
import numpy as np
from mpmath import mp, mpf, log
mp.dps = 30

def vp(z, p):
    if z == 0: return 10**9
    k = 0
    while z % p == 0: z //= p; k += 1
    return k

def gate_dist(p):
    e = [(-1) ** u * math.factorial(p - 1) // math.factorial(u) for u in range(p)]
    d = {0: 1}
    for x in e:
        nd = {}
        for w, c in d.items():
            for s, wt in ((-1, 1), (0, 2), (1, 1)):
                nd[w + s * x] = nd.get(w + s * x, 0) + c * wt
        d = nd
    return e, d  # weights sum to 4^p

def subset_sums(e):
    s = {0}
    for x in e: s = s | {y + x for y in s}
    return s

def analyse(p, jmax=60):
    e, d = gate_dist(p)
    tot = 4 ** p
    P0 = Fraction(d.get(0, 0), tot)
    assert P0 == Fraction(3, 2 ** (p + 1)), (p, P0)
    ss = subset_sums(e)
    assert len(ss) == 3 * 2 ** max(p - 2, 0), (p, len(ss))
    Gam = {}; J0 = None; dist = {}
    for j in range(1, jmax + 1):
        mod = p ** j
        Pj = Fraction(sum(c for w, c in d.items() if w % mod == 0), tot)
        Gam[j] = p ** j * Pj - 1
        if J0 is None and Pj == P0: J0 = j
        dist[j] = len({s % mod for s in ss})
    Lp = max(j for j in range(1, jmax + 1) if dist[j] == p ** j)
    # monotonicity of Gamma
    assert all(Gam[j] <= Gam[j + 1] for j in range(1, jmax))
    # closed form after J0
    assert all(Gam[j] == Fraction(3, 2) * p ** j / 2 ** p - 1 for j in range(J0, jmax + 1))
    th = mpf(0); ths = mpf(0)
    for j in range(0, jmax):
        w = (1 - mpf(1) / p) * mpf(p) ** (-j)
        th += w * log(1 + mpf(Gam[j + 1].numerator) / Gam[j + 1].denominator, p)
        ths += w * log(mpf(p) ** (j + 1) / dist[j + 1], p)
    th *= mpf(p - 1) / p; ths *= mpf(p - 1) / p
    return Gam[1], J0, Lp, th, ths

for p in [2, 3, 5, 7, 11, 13]:
    g1, J0, Lp, th, ths = analyse(p)
    print(f"p={p} Gamma_p(1)={g1} J0={J0} Lp={Lp} theta={mp.nstr(th, 12)} 1-theta_set={mp.nstr(1 - ths, 12)}")

# Prop 11.41(b): conditional law of Y/p^J on {p^J | Y} for an actual gate block, p=5, m with v(m+1) large
for p, m in [(5, 124), (5, 624), (7, 342)]:
    J = 1 + vp(m + 1, p)
    pm = p * m
    # x_{pm+r}/p^a = U*P_m(r); use exact P_m(r) and U = (pm)!/p^{e_m} reduced mod p^(J+3)
    mod = p ** (J + 3)
    f = 1; e_m = 0
    for i in range(1, pm + 1):
        z = i
        while z % p == 0: z //= p; e_m += 1
        f = f * z % mod
    U = f
    P = [1]
    for i in range(1, p): P.append(P[-1] * (pm + i))
    cnt = {}
    for eta in itertools.product((-1, 0, 1), repeat=p):
        wt = 1
        for t in eta: wt *= 2 if t == 0 else 1
        Y = sum(t * U * P[r] for t, r in zip(eta, range(p)))
        if Y % p ** J == 0:
            q = (Y // p ** J) % p ** 3
            cnt[q] = cnt.get(q, 0) + wt
    totc = sum(cnt.values())
    Up = U * P[p - 2] * ((m + 1) // p ** vp(m + 1, p)) % p ** 3
    print(f"p={p} m={m} J={J} conditional law of Y/p^J mod p^3:",
          {k: Fraction(c, totc) for k, c in cnt.items()}, " U' mod p^3 =", Up, " -U' =", (-Up) % p ** 3)

# exact C_k for small depth, N0 = 1, integer DP (weights 1,2,1)
def Ck(p, k, N0=1):
    mod = p ** k
    e0 = sum(vp(i, p) for i in range(1, N0 + 1))
    a = np.zeros(mod, dtype=object); a[0] = 1
    n = N0; fact = math.factorial(N0)
    out = None; terms = 0
    while True:
        if vp(fact, p) - e0 >= k: break
        x = (fact // p ** e0) % mod
        a = 2 * a + np.roll(a, x) + np.roll(a, -x)
        terms += 1
        n += 1; fact *= n
    return Fraction(int(a[0]) * mod, 4 ** terms)

for p, ks in [(2, range(1, 15)), (3, range(1, 10)), (5, range(1, 6)), (7, range(1, 5))]:
    print(p, [round(float(Ck(p, k)), 7) for k in ks])
