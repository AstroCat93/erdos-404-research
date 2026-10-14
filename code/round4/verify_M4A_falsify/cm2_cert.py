"""cm2: independent recomputation of the FE certificate of M4A Corollary M' for one atom file.
Own code (cm_lib), no code shared with code/round4/M4A/ or with t3_atom_fe.py.
 (a) atom: V_300(x_A) three ways (big-integer product, Legendre, gate scan); M_300 < m;
     the stored path: v(S_e(x)) >= m and S_e'(x) a unit, at x_A AND at random x in A (big integers);
 (b) times n_{l+1} = ceil(27 n_l/20); i_A; V_N, M_N on A by Legendre (= direct scan, checked);
 (c) admissibility of W_0; linear regime for every composite window with n_{l+1} < i_A;
 (d) phase 0/1: Prop D (exact) -> chi^2_0 and eps_bar_l (l <= L1); block form vs literal per-c form;
 (e) phase 2: Prop E (exact) for L1 < l with n_{l+1} <= NMAX2, theta = min(ceil(D/2), D - m + 1) as in
     Theorem 1 with b = m, the Lemma F hypothesis M_W <= K - theta checked; Markov with 2^{-(l-L1)};
 (f) phase 3: Prop E' for the remaining l with n_{l+1} < i_A (exact D, K, M_W from Legendre);
     E' >= exact E checked on the phase-2 windows;
 (g) phase 4: mu_A(G'^c); per-l worst case on G' for l = l4 .. l4+NL4 with deterministic digit counts;
     analytic majorant for all l >= l4 (value and slope at n*);
 (h) Pi_A, delta_A, Pi_A delta_A, Paley-Zygmund bound; comparison with the M4A table.
usage: python3 cm2_cert.py ATOMFILE L1 NMAX2 NL4 [LITMAX]
"""
import sys, math, random, time
from fractions import Fraction
import mpmath as mp
from gmpy2 import mpq, mpz
import cm_lib as L

mp.mp.dps = 60
atomfile, L1, NMAX2, NL4 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
LITMAX = int(sys.argv[5]) if len(sys.argv) > 5 else 2
T0 = time.time()
cfg = dict(l.strip().split("=", 1) for l in open(atomfile) if "=" in l)
p, n0, m, xA, path = int(cfg["p"]), int(cfg["n0"]), int(cfg["m"]), int(cfg["xA"]), cfg["path"].strip()
C = L.Consts(p)
E = L.eprime_constants(C)
print(f"atom p={p} n0={n0} m={m} xA={xA}; Prop E' constants S={C.S} rho1={mp.nstr(E['rho1'],8)} gamma={mp.nstr(E['gamma'],8)} kappa={mp.nstr(E['kappa'],8)}")
LN2 = mp.log(2)
LN10 = mp.log(10)

# ---------------------------------------------------------------- (a) atom
assert 0 <= xA < p ** m and len(path) == n0 and path[0] == "1"
V_prod = L.vp(L.pi_int(xA, n0), p)
V_leg = L.legendre(xA + n0, p) - L.legendre(xA, p)
scan = [(i, L.vp(xA + i, p)) for i in range(1, n0 + 1) if (xA + i) % p == 0]
V_scan = sum(s for _, s in scan); M300 = max(s for _, s in scan)
print(f"(a) V_300(x_A): product {V_prod}, Legendre {V_leg}, scan {V_scan}; claimed m={m}: {V_prod == V_leg == V_scan == m}; M_300={M300} < m: {M300 < m}")
assert V_prod == V_leg == V_scan == m and M300 < m


def S_and_Sd(x):
    S = 0; Sd = 0; P = 1; Pd = 0
    for j in range(n0):
        if j >= 1:
            Pd = Pd * (x + j) + P
            P = P * (x + j)
        if path[j] == "1":
            S += P; Sd += Pd
    return S, Sd


random.seed(p)
ok_path = True
for trial in range(6):
    x = xA if trial == 0 else xA + p ** m * random.randrange(1, p ** 40)
    S, Sd = S_and_Sd(x)
    vS = L.vp(S, p) if S else 10 ** 9
    Vx = L.vp(L.pi_int(x, n0), p)
    good = (vS >= Vx == m) and (Sd % p != 0)
    ok_path &= good
    if trial == 0:
        print(f"    path at x_A: v(S_e)={vS} >= V_300={Vx}, S_e' mod p={Sd % p}")
print(f"    path alive with slope 0 at x_A and 5 random x in A (V_300(x) = m there too): {ok_path}")
assert ok_path

# ---------------------------------------------------------------- (b) times, i_A, digit formulas
times = [n0]
while len(times) < 5000:
    times.append(-(-27 * times[-1] // 20))
iA = (-xA) % p ** m
if iA == 0:
    iA = p ** m
lastA = max(l for l in range(1, len(times) - 1) if times[l + 1] < iA)


def Vleg(N):
    """V_N(x) for x in A, valid for N < i_A"""
    assert N < iA
    return L.legendre(xA + N, p) - L.legendre(xA, p)


def cnt(a, b, s):
    """#{a < i <= b : p^s | x_A + i}"""
    return (xA + b) // p ** s - (xA + a) // p ** s


def Mmax(a, b, smax):
    best = 0
    for s in range(1, smax + 1):
        if cnt(a, b, s) > 0:
            best = s
    return best


# check digit formulas against a direct scan up to 40000
acc = 0; mx = 0; bad = 0
for N in range(1, 40001):
    if (xA + N) % p == 0:
        d = L.vp(xA + N, p); acc += d; mx = max(mx, d)
    if N % 499 == 0 or N in times[:15]:
        if acc != Vleg(N) or mx != Mmax(0, N, m - 1):
            bad += 1
print(f"(b) i_A = {iA} = {float(iA):.5e}; last l with n_(l+1) < i_A: {lastA} (n_(l+1)={float(times[lastA+1]):.4e}, next {float(times[lastA+2]):.4e});"
      f" Legendre/floor digit formulas vs scan (N <= 40000): {bad} mismatches")
assert bad == 0

# ---------------------------------------------------------------- (c) admissibility and linear regime
D0 = Vleg(times[1]) - Vleg(times[0]); M1 = Mmax(0, times[1], m - 1)
adm = D0 <= m - M1 and M1 < m
print(f"(c) W_0 = [{times[0]},{times[1]}): D_0={D0}, M_(n_1)={M1}; D_0 <= m - M: {D0 <= m - M1}; admissible: {adm}")
assert adm
linbad = 0
for l in range(1, lastA + 1):
    n, Np = times[l - 1], times[l + 1]
    Vn = Vleg(n); K = Vleg(Np) - Vn; Mx = Mmax(0, Np, m - 1)
    if not (K <= Vn - Mx and Mx < Vn):
        linbad += 1
        print(f"    linear regime FAILS at l={l}")
print(f"    linear regime holds on all of A for l = 1..{lastA}: {linbad == 0}")


def gates(a, b):
    return [(i, L.vp(xA + i, p)) for i in range(a + 1, b + 1) if (xA + i) % p == 0]


def l10(x):
    return mp.log10(mp.mpf(int(x.numerator))) - mp.log10(mp.mpf(int(x.denominator)))


# ---------------------------------------------------------------- (d) phases 0/1
gl0 = gates(times[0], times[1])
PD0 = L.propDE_block(p, gl0, times[0], times[1], D0, C)
chi0 = PD0 - 1
lit = L.propDE_literal(p, gl0, times[0], times[1], D0, C)
print(f"(d) chi^2_0 <= {float(chi0):.6g}   [block == literal per-c: {Fraction(int(PD0.numerator), int(PD0.denominator)) == lit}]")
epsbar = {}
for l in range(1, L1 + 1):
    n, N, Np = times[l - 1], times[l], times[l + 1]
    gl = gates(n, Np)
    K = sum(s for _, s in gl); D = sum(s for i, s in gl if i <= N)
    assert K == Vleg(Np) - Vleg(n) and D == Vleg(N) - Vleg(n)
    PD = L.propDE_block(p, gl, n, Np, K, C)
    epsbar[l] = PD - 1
    extra = ""
    if l <= LITMAX:
        lit = L.propDE_literal(p, gl, n, Np, K, C)
        extra = f"  [block == literal: {Fraction(int(PD.numerator), int(PD.denominator)) == lit}]"
    MW = max(s for _, s in gl)
    print(f"    l={l} [{n},{N},{Np}) D={D} K={K} M_W={MW} eps_bar = {float(epsbar[l]):.6g}{extra}", flush=True)

# ---------------------------------------------------------------- (e) phase 2
fail = {}
exactE = {}
l = L1 + 1
while times[l + 1] <= NMAX2:
    n, N, Np = times[l - 1], times[l], times[l + 1]
    gl = gates(n, Np)
    K = sum(s for _, s in gl); D = sum(s for i, s in gl if i <= N); MW = max(s for _, s in gl)
    theta = min(-(-D // 2), D - m + 1)
    lemF = MW <= K - theta
    fp = min(theta, K - MW)
    PE = L.propDE_block(p, gl, n, Np, K, C, fprime=fp)
    exactE[l] = (l10(PE), K, Np - n, MW, fp)
    fail[l] = l10(PE) + (l - L1) * mp.log10(2)
    print(f"(e) l={l} [{n},{N},{Np}) D={D} K={K} theta={theta} (=ceil(D/2): {theta == -(-D // 2)}) M_W={MW} Lemma F hyp: {lemF}"
          f"  log10 E_A eps <= {mp.nstr(exactE[l][0], 7)}  log10 fail <= {mp.nstr(fail[l], 7)}", flush=True)
    assert lemF and theta >= 1
    l += 1
LE = l - 1
# E' >= E on the same windows
dom = all(L.eprime_ln(C, E, K, H, MW, fp) / LN10 >= e for (e, K, H, MW, fp) in exactE.values())
print(f"    Prop E' >= exact Prop E on all {len(exactE)} phase-2 windows: {dom}")

# ---------------------------------------------------------------- (f) phase 3
sum3 = mp.mpf(0)
lin3 = True
for l in range(LE + 1, lastA + 1):
    n, N, Np = times[l - 1], times[l], times[l + 1]
    Vn = Vleg(n); D = Vleg(N) - Vn; K = Vleg(Np) - Vn; H = Np - n
    MW = Mmax(n, Np, m - 1)
    theta = min(-(-D // 2), D - m + 1)
    assert theta >= 1 and MW <= K - theta
    fp = min(theta, K - MW)
    lf = L.eprime_ln(C, E, K, H, MW, fp) + (l - L1) * LN2
    fail[l] = lf / LN10
    sum3 += mp.exp(lf)
    if l in (LE + 1, LE + 2, LE + 5, 50, 100, lastA):
        print(f"(f) l={l} D={D} K={K} M_W={MW} theta={theta} log10 fail <= {mp.nstr(fail[l], 8)}")
sum2 = mp.fsum(mp.mpf(10) ** fail[l] for l in range(L1 + 1, LE + 1))
print(f"    phase 2 (l={L1+1}..{LE}) sum = {mp.nstr(sum2, 8)};  phase 3 (l={LE+1}..{lastA}) sum = {mp.nstr(sum3, 6)}")

# ---------------------------------------------------------------- (g) phase 4
l4 = lastA + 1
muGc = mp.mpf(p) ** -10 * (mp.mpf(iA) ** -2 + mp.mpf(p) ** (-2 * m) * mp.pi ** 2 / 6)


def floorlog(N2):
    """largest e with p^e <= N2"""
    e = 0
    while p ** (e + 1) <= N2:
        e += 1
    return e


sum4 = mp.mpf(0); side_bad = 0; worst = -mp.inf; minrate = mp.inf
for l in range(l4, l4 + NL4 + 1):
    n, N, Np = times[l - 1], times[l], times[l + 1]
    H = Np - n
    sig = m + 10 + floorlog(Np * Np)            # every gate <= Np has depth <= sig on G'
    Kdet = sum(cnt(n, Np, s) for s in range(1, m + 1))
    Kup = Kdet + (sig - m) * cnt(n, Np, m)
    Dlow = sum(cnt(n, N, s) for s in range(1, m + 1))
    Vnlow = sum(cnt(0, n, s) for s in range(1, m + 1))
    ok = (Dlow // 2 >= sig) and (Kup <= Vnlow - sig) and (sig < Vnlow)
    side_bad += (not ok)
    fp = min(-(-Dlow // 2), Dlow - sig)
    lf = L.eprime_ln(C, E, Kup, H, sig, fp) + (l - L1) * LN2
    sum4 += mp.exp(lf)
    worst = max(worst, lf); minrate = min(minrate, -lf / n)
print(f"(g) phase 4 from l={l4} (n*={float(times[l4-1]):.5e}); mu_A(G'^c) <= {mp.nstr(muGc, 6)}")
print(f"    per-l worst case on G', l={l4}..{l4+NL4}: side conditions fail for {side_bad}; max ln fail = {mp.nstr(worst, 6)}; min (-ln fail)/n_(l-1) = {mp.nstr(minrate, 6)}; sum = 10^{mp.nstr(mp.log10(sum4), 6)}")

# analytic majorant for every l >= l4 (n = n_(l-1) >= n*)
r = mp.mpf(27) / 20
rate = E['gamma'] * (p - 1) * (r - 1) / (2 * p ** 2) - (r ** 2 - 1) * E['rho1'] / (p - 1)
cpr = rate / 2
lp = mp.log(p); lq1 = E['lq'](1); lqS = E['lq'](C.S); g_ = E['gamma']; k_ = E['kappa']; rho = E['rho1']


def maj(nn):
    nn = mp.mpf(nn)
    sig = m + 10 + 2 * mp.log(2 * nn) / lp
    Hlo = (r ** 2 - 1) * nn; Hup = Hlo + r + 1
    Kup = Hup / (p - 1) + sig
    Dlo = (r - 1) * nn / (p - 1) - mp.log(nn) / lp - 1
    Vlo = nn / (p - 1) - mp.log(nn) / lp - 1
    lnT1 = mp.log(1 + mp.mpf(2) ** p) + Hlo * (lp / (p - 1) - LN2) + sig * lp
    lnT2 = (p + sig * (p - 1)) * LN2 + Kup * rho + (lqS - lq1) + (sig - C.S) * lp + g_ * (2 - mp.mpf(1) / p) \
        - g_ * (Dlo / 2 - sig + 1) * mp.mpf(p - 1) ** 2 / p ** 2 - k_ - mp.log(1 - mp.exp(-k_))
    lpen = (1 + mp.log(nn / n0) / mp.log(r) - L1) * LN2 + LN2
    return [lnT1 + lpen + cpr * nn, lnT2 + lpen + cpr * nn, Dlo - 2 * sig - 1, Vlo - Kup - sig - 1]


nstar = times[l4 - 1]
v0 = maj(nstar)
hstep = mp.mpf(nstar) * mp.mpf('1e-20')
v1 = maj(nstar + hstep)
der = [(b - a) / hstep for a, b in zip(v0, v1)]
okmaj = v0[0] < 0 and v0[1] < 0 and der[0] < 0 and der[1] < 0 and v0[2] > 0 and v0[3] > 0 and der[2] > 0 and der[3] > 0
print(f"    analytic majorant (each branch = -a n + b ln n + c0, so its slope -a + b/n is monotone): at n*: branch1 {mp.nstr(v0[0],6)}, branch2 {mp.nstr(v0[1],6)};"
      f" slopes {mp.nstr(der[0],6)}, {mp.nstr(der[1],6)}; side margins D-2sig-1 = {mp.nstr(v0[2],6)}, V_n-K-sig-1 = {mp.nstr(v0[3],6)} (slopes {mp.nstr(der[2],4)}, {mp.nstr(der[3],4)})")
print(f"    rate c = {mp.nstr(rate, 8)}, used c' = c/2 = {mp.nstr(cpr, 8)}; all l >= {l4}: ln fail_l <= -c' n_(l-1): {okmaj}")
tail4 = mp.log10(2) - cpr * nstar / LN10
print(f"    => sum_(l >= {l4}) fail_l <= 2 exp(-c' n*) = 10^{mp.nstr(tail4, 6)}")
assert okmaj

# ---------------------------------------------------------------- (h) totals
lnPi = mp.log(mp.mpf(int(chi0.numerator)) / int(chi0.denominator) + 1)
for l in range(1, L1 + 1):
    e = epsbar[l]
    lnPi += mp.log(mp.mpf(int(e.numerator)) / int(e.denominator) + 1)
pr = mp.mpf(1)
for i in range(1, 201):
    pr *= 1 + mp.mpf(2) ** -i
lnPi += mp.log(pr) + mp.mpf(2) ** -200
Pi = mp.exp(lnPi)
delta = sum2 + sum3 + mp.mpf(10) ** tail4 + muGc
prod = Pi * delta
lb = (1 - mp.sqrt(prod)) ** 2 / Pi
print(f"(h) log10 Pi_A <= {mp.nstr(lnPi / LN10, 8)};  delta_A <= {mp.nstr(delta, 8)} (log10 {mp.nstr(mp.log10(delta), 7)});  log10(Pi_A delta_A) <= {mp.nstr(mp.log10(prod), 7)};  FE: {prod < 1}")
print(f"RESULT p={p}: mu(K_p cap A)/mu(A) >= {mp.nstr(lb, 8)}   (log10 {mp.nstr(mp.log10(lb), 6)});  mu(A) = p^-{m};  mu(K_p) >= 10^{mp.nstr(mp.log10(lb) - m * mp.log10(p), 6)}")
print(f"[{time.time() - T0:.1f} s]")
