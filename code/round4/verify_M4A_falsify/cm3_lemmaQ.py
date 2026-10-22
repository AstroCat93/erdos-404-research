"""cm3: Lemma Q (quenched anti-concentration) at p = 7, 11, 13, 17, 19, 23, exact.
For each test point u and every t <= TMAX, every k <= min(KMAX, V_t(u)) and f in {none, 1..FMAX}:
   P( v(T_u) >= k, v(T_u') >= f )  <=  P0(g_1, min(s_1,k)) prod_r pi_r          (M4A Lemma Q)
with T_u = sum_{c<t} dt_c pi_c(u), dt_0 = 1, other dt_c signed.  Exact joint DP over
(T mod p^KMAX, T' mod p^FMAX), counts kept modulo 2-3 primes < 2^61 and reconstructed by CRT.
Point kinds (all near the dangerous places named in the brief):
  rand    random u
  neg     u = -g + p^s w: deep gate (depth s) at g = 1, 2, 3, p-1, p, p+1, p+2, 2p+1 (near -1, -2, ...)
  int     u a small non-negative integer (factorial gate pattern), or u = -1 + p^j (gate at 1 of depth j)
  d1first u + g_1 = p*mu with mu, mu+1, mu+2 units: runs of depth-1 gates, so 2D blocks occur
  dbl     u at a near-double root of a random signed polynomial (high-slope paths)
Controls (expected to FAIL somewhere if the corresponding feature of the bound is sharp):
  half2D (2D factor halved), noq (q_s -> 1), noM (k - M_{r+1} clause dropped).
usage: python3 cm3_lemmaQ.py p SEED NPERKIND KMAX FMAX TMAX KINDS(comma list)
"""
import sys, random, time
from fractions import Fraction
import cm_lib as L

p, seed, NPK, KMAX, FMAX, TMAX = map(int, sys.argv[1:7])
kinds = sys.argv[7].split(",")
random.seed(seed)
E = KMAX + FMAX + 40
PE = p ** E
C = L.Consts(p, sx=(5 if p > 13 else 6))


def unit():
    while True:
        w = random.randrange(1, PE)
        if w % p:
            return w


def make_points(kind):
    pts = []
    if kind == "rand":
        pts = [random.randrange(PE) for _ in range(NPK)]
    elif kind == "neg":
        gs = [1, 2, 3, p - 1, p, p + 1, p + 2, 2 * p + 1]
        for i in range(NPK):
            g = gs[i % len(gs)]
            s = 1 + (i // len(gs)) % (KMAX + 2)
            pts.append((-g + p ** s * unit()) % PE)
    elif kind == "int":
        base = [0, 1, 2, p - 1, p, 2 * p - 1, p * p - 1, p * p - 2]
        for i in range(NPK):
            if i < len(base):
                pts.append(base[i] % PE)
            else:
                j = 1 + (i - len(base)) % (KMAX + 2)
                pts.append((-1 + p ** j) % PE)
    elif kind == "d1first":
        for i in range(NPK):
            g1 = 1 + i % min(p, 4)
            while True:
                mu = random.randrange(PE // p)
                if all((mu + j) % p for j in range(3)):
                    break
            pts.append((p * mu - g1) % PE)
    elif kind == "dbl":
        for i in range(NPK):
            best = None
            for _ in range(30):
                tt = random.randrange(3, p + 4)
                dl = [1] + [random.choice((-1, 0, 0, 1)) for _ in range(tt - 1)]
                for u0 in range(p * p):
                    Pv, Pd, S, Sd = 1, 0, 0, 0
                    for c in range(tt):
                        if c >= 1:
                            Pd = Pd * (u0 + c) + Pv
                            Pv = Pv * (u0 + c)
                        S += dl[c] * Pv; Sd += dl[c] * Pd
                    if S % (p * p) == 0 and Sd % p == 0:
                        best = u0
                        break
                if best is not None:
                    break
            if best is None:
                best = random.randrange(p * p)
            pts.append((best + p * p * random.randrange(PE // (p * p))) % PE)
    return pts


def vq(a):
    a %= PE
    assert a != 0, "precision"
    return L.vp(a, p)


tot = {"cases": 0, "fail": 0, "eq": 0, "twoD": 0, "half2D": 0, "noq": 0, "noM": 0}
maxratio = Fraction(0)
T0 = time.time()
for kind in kinds:
    kc = dict(cases=0, fail=0, twoD=0)
    for u in make_points(kind):
        # gate list and pi_c, pi_c' mod p^KMAX / p^FMAX
        gl = []
        tmax = TMAX
        # number of CRT primes: need 4^(t-1) < product
        npr = 2 if 2 * (tmax - 1) < 120 else 3
        dp = L.JointDP(p, KMAX, FMAX, npr)
        Pv, Pd = 1, 0
        for t in range(1, tmax + 1):
            c = t - 1
            if c >= 1:
                Pd = (Pd * (u + c) + Pv) % PE
                Pv = (Pv * (u + c)) % PE
            dp.step(Pv, Pd, fixed=(c == 0))
            if (u + t) % p == 0:
                gl.append((t, vq(u + t)))
            Vt = sum(s for _, s in gl)
            for k in range(1, min(KMAX, Vt) + 1):
                for f in [None] + list(range(1, FMAX + 1)):
                    cntv = dp.count(k, f if f is not None else 0)
                    P = Fraction(cntv, 4 ** dp.ns)
                    b = L.lemmaQ_rhs(p, gl, k, f, C)
                    kc["cases"] += 1
                    if P > b:
                        kc["fail"] += 1
                        print(f"LEMMA Q FAIL p={p} kind={kind} u={u} t={t} k={k} f={f} P={P} bound={b} gates={gl}")
                    if P == b:
                        tot["eq"] += 1
                    if b > 0:
                        maxratio = max(maxratio, P / b)
                    # was a 2D block used?
                    if f is not None and L.lemmaQ_rhs(p, gl, k, f, C, variant='noq') != L.lemmaQ_rhs(p, gl, k, None, C, variant='noq'):
                        kc["twoD"] += 1
                    for var in ("half2D", "noq", "noM"):
                        if P > L.lemmaQ_rhs(p, gl, k, f, C, variant=var):
                            tot[var] += 1
    print(f"p={p} kind={kind}: {kc['cases']} cases, {kc['fail']} failures, {kc['twoD']} cases with a 2D block  [{time.time() - T0:.1f} s]", flush=True)
    tot["cases"] += kc["cases"]; tot["fail"] += kc["fail"]; tot["twoD"] += kc["twoD"]
print(f"TOTAL p={p}: {tot['cases']} cases, {tot['fail']} failures; equality in {tot['eq']}; max P/bound = {float(maxratio):.6f}; "
      f"cases with a 2D block: {tot['twoD']}")
print(f"controls (violations; >0 means that feature of the bound is needed): half2D {tot['half2D']}, noq {tot['noq']}, noM {tot['noM']}")
