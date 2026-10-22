"""t3: independent re-computation of the FE certificate of M4A Theorem M (p=7 atom), from the
statements in M4A.md only (no code shared with code/round4/M4A/).

 (a) atom: V_300(xA), M_300, the stored path e (v(S_e(xA)) >= m, S_e'(xA) unit), admissibility of W_0;
 (b) window times n_{l+1} = ceil(27 n_l / 20); digit formula for V_N, M_N (checked against direct
     valuations up to 70000);
 (c) linear regime for every composite window with n_{l+1} < i_A (exact, digit formula);
 (d) phase 0/1: Prop D (exact rationals, block form) -> chi^2_0 and eps_bar_l, l=1..L1;
 (e) phase 2: Prop E (exact rationals, block form) for l = L1+1..LE; Markov with eps_bar=2^{-(l-L1)};
 (f) phase 3: Prop E' (closed form, mpmath 60 digits) for the remaining l with n_{l+1} < i_A;
     also Prop E (exact) vs Prop E' for l in phase-3 range up to LX (E' must dominate);
 (g) phase 4: l with n_{l+1} >= i_A: worst-case Prop E' on G' (sigma_l = m + ceil(2 log_7 n_{l+1}) + 11),
     evaluated for l = first..LMAX4, with side conditions (D >= 2 sigma, linear regime);
 (h) Pi_A, delta_A, Pi_A*delta_A, Paley-Zygmund lower bound.
usage: python3 t3_atom_fe.py ATOMFILE L1 LE LX LMAX4
"""
import sys, math
import mpmath as mp
import gmpy2
from gmpy2 import mpq
import vf_lib as L

mp.mp.dps = 60
atomfile, L1, LE, LX, LMAX4 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
cfg = {}
for line in open(atomfile):
    if "=" in line:
        k, v = line.strip().split("=", 1)
        cfg[k] = v
p = int(cfg["p"]); n0 = int(cfg["n0"]); m = int(cfg["m"]); xA = int(cfg["xA"]); path = cfg["path"].strip()
print(f"atom: p={p} n0={n0} m={m} xA={xA} len(path)={len(path)}")


def vdirect(i):
    return L.vp(xA + i, p) if (xA + i) % p == 0 else 0


# (a) atom checks ------------------------------------------------------------------------
V300 = sum(vdirect(i) for i in range(1, n0 + 1))
M300 = max(vdirect(i) for i in range(1, n0 + 1))
assert path[0] == "1" and len(path) == n0
S = 0; Sd = 0; P = 1; Pd = 0
for j in range(n0):
    if j >= 1:
        Pd = Pd * (xA + j) + P
        P = P * (xA + j)
    if path[j] == "1":
        S += P; Sd += Pd
vS = L.vp(S, p) if S != 0 else 10 ** 9
print(f"(a) V_300(xA)={V300} (claimed m={m}): {V300 == m};  M_300={M300} < m: {M300 < m}")
print(f"    v_p(S_e(xA))={vS} >= m: {vS >= m};  S_e'(xA) mod p = {Sd % p} (slope 0: {Sd % p != 0})")
print(f"    xA < p^m: {xA < p ** m}")

# (b) times and digit formula ---------------------------------------------------------------
times = [n0]
while len(times) < 3000:
    times.append(-(-27 * times[-1] // 20))
iS = {}
for s in range(1, m + 1):
    r = (-xA) % p ** s
    iS[s] = r if r != 0 else p ** s
iA = iS[m]
print(f"(b) i_A = {iA} ({float(iA):.4e});  n_l: {times[:12]}")


def Vdig(N):
    assert N < iA
    return sum((N - iS[s]) // p ** s + 1 for s in range(1, m) if iS[s] <= N)


def Mdig(N):
    assert N < iA
    return max([s for s in range(1, m) if iS[s] <= N] + [0])


def MWdig(n, Np):
    """exact max depth in (n, Np]"""
    best = 0
    for s in range(1, m):
        # first i > n with i = iS[s] mod p^s
        if iS[s] > n:
            i = iS[s]
        else:
            i = iS[s] + ((n - iS[s]) // p ** s + 1) * p ** s
        if i <= Np:
            best = s
    return best


bad = 0
acc = 0; mx = 0
for N in range(1, 70001):
    d = vdirect(N); acc += d; mx = max(mx, d)
    if N % 997 == 0 or N in times[:20]:
        if acc != Vdig(N) or mx != Mdig(N):
            bad += 1
print(f"    digit formula vs direct valuations at sampled N<=70000: {bad} mismatches")

# windows -------------------------------------------------------------------------------------
lastA = max(l for l in range(1, len(times) - 1) if times[l + 1] < iA)
print(f"    last l with n_(l+1) < i_A: {lastA};  n_(l+1) there = {times[lastA + 1]:.4e}; next n = {times[lastA + 2]:.4e}")
D0 = Vdig(times[1]) - Vdig(times[0]); M1 = Mdig(times[1])
print(f"    W_0=[{times[0]},{times[1]}): D_0={D0}, M_(n_1)={M1}: D_0<=m-M: {D0 <= m - M1}, M<m: {M1 < m}")

# (c) linear regime for l=1..lastA -------------------------------------------------------------
lin_bad = 0
for l in range(1, lastA + 1):
    n, N, Np = times[l - 1], times[l], times[l + 1]
    ml = Vdig(n); K = Vdig(Np) - ml; Mx = Mdig(Np)
    if not (K <= ml - Mx and Mx < ml):
        lin_bad += 1
print(f"(c) linear regime (D_(l-1)+D_l <= m_(l-1)-M_(n_(l+1)), M<m_(l-1)) fails for {lin_bad} of l=1..{lastA}")


def gates_direct(n, Np):
    return [(i, vdirect(i)) for i in range(n + 1, Np + 1) if (xA + i) % p == 0]


def log10q(x):
    return float(mp.log10(mp.mpf(int(x.numerator))) - mp.log10(mp.mpf(int(x.denominator))))


# (d) phase 0 / 1 -------------------------------------------------------------------------------
gl0 = gates_direct(times[0], times[1])
PD0 = L.block_bound(p, gl0, times[0], times[1], D0, None)
chi0 = PD0 - 1
print(f"(d) phase 0: chi^2_0 <= {float(chi0):.6f}   (report: 0.504642)")
epsbar = {}
for l in range(1, L1 + 1):
    n, N, Np = times[l - 1], times[l], times[l + 1]
    gl = gates_direct(n, Np)
    K = sum(s for _, s in gl); D = sum(s for i, s in gl if i <= N)
    assert K == Vdig(Np) - Vdig(n) and D == Vdig(N) - Vdig(n)
    PD = L.block_bound(p, gl, n, Np, K, None)
    epsbar[l] = PD - 1
    print(f"    l={l} [{n},{N},{Np}) D={D} K={K} eps_bar={float(epsbar[l]):.6g}")

# (e) phase 2 -----------------------------------------------------------------------------------
logfail = {}
for l in range(L1 + 1, LE + 1):
    n, N, Np = times[l - 1], times[l], times[l + 1]
    gl = gates_direct(n, Np)
    K = sum(s for _, s in gl); D = sum(s for i, s in gl if i <= N); MW = max(s for _, s in gl)
    b = m
    theta = min(-(-D // 2), D - b + 1)
    assert theta == -(-D // 2), "theta != ceil(D/2)"
    assert MW <= K - theta
    fp = min(theta, K - MW)
    PE = L.block_bound(p, gl, n, Np, K, fp)
    lE = log10q(PE)
    logfail[l] = lE + (l - L1) * math.log10(2)
    print(f"(e) l={l} [{n},{N},{Np}) D={D} K={K} theta={theta} M_W={MW} log10 E_A eps <= {lE:.3f}  log10 fail <= {logfail[l]:.3f}", flush=True)

# (f) phase 3 -----------------------------------------------------------------------------------
C = L.eprime_consts(p)
print(f"(f) constants rho1={float(C['rho1']):.6f} gamma={float(C['gamma']):.6f} kappa={float(C['kappa']):.6f}")
for l in range(LE + 1, LX + 1):
    # exact Prop E and closed form E' on the same windows (E' must dominate)
    n, N, Np = times[l - 1], times[l], times[l + 1]
    gl = gates_direct(n, Np)
    K = sum(s for _, s in gl); D = sum(s for i, s in gl if i <= N); MW = max(s for _, s in gl)
    theta = -(-D // 2)
    PE = L.block_bound(p, gl, n, Np, K, min(theta, K - MW))
    lE = log10q(PE)
    lEp = float(L.eprime_log(p, K, Np - n, MW, min(theta, K - MW), C) / mp.log(10))
    print(f"    l={l}: exact Prop E log10 = {lE:.3f};  Prop E' log10 = {lEp:.3f};  E' >= E: {lEp >= lE}", flush=True)
total3 = mp.mpf(0)
worst3 = None
for l in range(LE + 1, lastA + 1):
    n, N, Np = times[l - 1], times[l], times[l + 1]
    Vn = Vdig(n); D = Vdig(N) - Vn; K = Vdig(Np) - Vn; H = Np - n
    MW = MWdig(n, Np)
    theta = min(-(-D // 2), D - m + 1)
    assert theta == -(-D // 2) and MW <= K - theta
    lE = L.eprime_log(p, K, H, MW, min(theta, K - MW), C)
    lf = lE + (l - L1) * mp.log(2)
    total3 += mp.exp(lf)
    logfail[l] = float(lf / mp.log(10))
    if l in (LE + 1, LE + 2, 30, 100, 200, lastA):
        print(f"    l={l} D={D} K={K} M_W={MW} log10 fail <= {logfail[l]:.6g}")
s2 = sum(10 ** logfail[l] for l in range(L1 + 1, LE + 1))
print(f"    phase 2 sum = {s2:.6e}; phase 3 sum = {mp.nstr(total3, 6)}")

# (g) phase 4 -----------------------------------------------------------------------------------
l4 = lastA + 1
muGc = mp.mpf(p) ** -10 * (mp.mpf(iA) ** -2 + mp.mpf(p) ** (-2 * m) * mp.pi ** 2 / 6)
print(f"(g) phase 4 from l={l4}; mu_A(G'^c) <= {mp.nstr(muGc, 6)}")


def vfact(nn):
    s, q = 0, p
    while q <= nn:
        s += nn // q; q *= p
    return s


total4 = mp.mpf(0)
side_bad = 0
worst4 = -mp.inf
rate_min = mp.inf
for l in range(l4, LMAX4 + 1):
    n, N, Np = times[l - 1], times[l], times[l + 1]
    H = Np - n
    sig = m + int(mp.ceil(2 * mp.log(Np) / mp.log(p))) + 11
    # G' => every gate up to Np has depth <= m + 2 log_p i + 10 < sig
    Dlow = vfact(N - n)
    Kup = sum(-(-H // p ** j) for j in range(1, sig + 1))
    vn = vfact(n)
    ok = (Dlow >= 2 * sig) and (Kup <= vn - sig) and (sig < vn)
    if not ok:
        side_bad += 1
    fplow = min(-(-Dlow // 2), Dlow - sig)
    lE = L.eprime_log(p, Kup, H, sig, fplow, C)
    lf = lE + (l - L1) * mp.log(2)
    total4 += mp.exp(lf)
    worst4 = max(worst4, lf)
    rate_min = min(rate_min, -lf / n)
    if l in (l4, l4 + 1, l4 + 10, l4 + 100, LMAX4):
        print(f"    l={l} n={mp.nstr(mp.mpf(n), 6)} sigma={sig} D>={mp.nstr(mp.mpf(Dlow),6)} K<={mp.nstr(mp.mpf(Kup),6)} ln fail <= {mp.nstr(lf, 8)}  (-ln fail)/n = {mp.nstr(-lf / n, 6)}")
print(f"    side conditions (D>=2 sigma, linear regime on G_l) fail for {side_bad} of l={l4}..{LMAX4}")
print(f"    max ln fail over phase 4 range = {mp.nstr(worst4, 8)};  min (-ln fail)/n_(l-1) = {mp.nstr(rate_min, 6)}")
print(f"    phase 4 sum (l={l4}..{LMAX4}) = {mp.nstr(total4, 6)}")

# (g2) analytic tail for all l > LMAX4 (indeed for all l >= l4), my own majorant ----------------
#   n = n_{l-1} >= nstar;  N <= r n + 1, N' <= r^2 n + r + 1 <= 2n;  H in [(r^2-1)n, (r^2-1)n + r + 1]
#   sigma <= m + 2 log_p(2n) + 12;  D >= v((N-n)!) >= (r-1)n/(p-1) - log_p n - 2;  K <= H/(p-1) + sigma
#   f' >= D/2 - sigma (needs D >= 2 sigma);  l <= 1 + ln(n/300)/ln r
r = mp.mpf(27) / 20
cp = mp.mpf("0.03")
lq1 = C["lq"][1]; lq8 = C["lq"][8]; g_ = C["gamma"]; k_ = C["kappa"]; rho = C["rho1"]


def tails(nn):
    nn = mp.mpf(nn)
    sig = m + 2 * mp.log(2 * nn) / mp.log(p) + 12
    Hlo = (r ** 2 - 1) * nn
    Hup = Hlo + r + 1
    Kup = Hup / (p - 1) + sig
    Dlo = (r - 1) * nn / (p - 1) - mp.log(nn) / mp.log(p) - 2
    flo = Dlo / 2 - sig
    T1 = mp.log(1 + mp.mpf(2) ** p) + (Hlo / (p - 1) + sig) * mp.log(p) - Hlo * mp.log(2)
    T2 = (p + (p - 1) * sig) * mp.log(2) + Kup * rho + (lq8 + (sig - 8) * mp.log(p) - lq1) + g_ * (2 - mp.mpf(1) / p) \
        - g_ * (flo - sig + 1) * mp.mpf((p - 1) ** 2) / p ** 2 - k_ - mp.log(1 - mp.exp(-k_))
    lpen = (1 + mp.log(nn / n0) / mp.log(r) - L1) * mp.log(2)
    side = (Dlo >= 2 * sig)
    return T1 + lpen + cp * nn, T2 + lpen + cp * nn, side


nstar = times[l4 - 1]
a1, a2, sd = tails(nstar)
h = mp.mpf(nstar) * mp.mpf("1e-6")
b1, b2, _ = tails(nstar + h)
d1 = (b1 - a1) / h; d2 = (b2 - a2) / h
print(f"(g2) analytic majorant at n*={mp.nstr(mp.mpf(nstar),6)}: [T1 + l ln2 + 0.03 n] = {mp.nstr(a1,6)}, [T2 + l ln2 + 0.03 n] = {mp.nstr(a2,6)}, D>=2sigma: {sd}")
print(f"     slopes (numerical, each is -a + b/n with b>0, so maximal at n*): {mp.nstr(d1,6)}, {mp.nstr(d2,6)}")
print(f"     => for every l >= {l4}: ln fail_l <= ln2 + max(...) <= -0.03 n_(l-1) + ln 2: {a1 < 0 and a2 < 0 and d1 < 0 and d2 < 0}")
print(f"     => sum over l >= {l4} of fail_l <= sum_l 2 exp(-0.03 n_(l-1)) <= 4 exp(-0.03 n*) = 10^{mp.nstr(mp.log10(4) - cp * nstar / mp.log(10), 6)}")

# (h) totals ------------------------------------------------------------------------------------
lp = mp.mpf(0)
lp += mp.log(mp.mpf(int(chi0.numerator)) / int(chi0.denominator) + 1)
for l in range(1, L1 + 1):
    e = epsbar[l]
    lp += mp.log(mp.mpf(int(e.numerator)) / int(e.denominator) + 1)
# prod_{i>=1}(1+2^-i) <= prod_{i<=80}(1+2^-i) * exp(2^-80)
pr = mp.mpf(1)
for i in range(1, 81):
    pr *= 1 + mp.mpf(2) ** -i
lp += mp.log(pr) + mp.mpf(2) ** -80
Pi = mp.exp(lp)
delta = mp.mpf(s2) + total3 + total4 + muGc
print(f"(h) log10 Pi_A <= {mp.nstr(lp / mp.log(10), 8)}   (report: 25.7344)")
print(f"    delta_A <= {mp.nstr(delta, 8)} (phase 4 counted up to l={LMAX4})   (report: 1.0006e-45)")
print(f"    log10(Pi_A delta_A) <= {mp.nstr(mp.log10(Pi * delta), 8)}   (report: -19.265)")
lb = (1 - mp.sqrt(Pi * delta)) ** 2 / Pi
print(f"    PZ lower bound mu(K_p cap A)/mu(A) >= {mp.nstr(lb, 8)}   (report: 1.843e-26)")
