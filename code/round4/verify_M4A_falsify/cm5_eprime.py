"""cm5: Prop E' (closed form) >= Prop E (exact block form) on random and adversarial composite windows,
with the constants used by M4A for Cor M' (S = 8 for p <= 13, S = 4 for p > 13); plus Props D/E block
form == literal per-c form (through the Lemma Q evaluator) on small windows.
Windows [n, ceil(r n), ceil(r^2 n)), r in {6/5, 27/20, 3/2}; x random mod p^E with, in 3/4 of the
cases, a planted deep gate (depth 2..DMAX) just after n, at n+2, just after N, or mid-window.
theta = ceil(D/2) (a ball of radius >= p^-(floor(D/2)+1)); Lemma F hypothesis M_W <= K - theta required.
sigma in {M_W, M_W + 3}.
usage: python3 cm5_eprime.py p SEED NW nmin nmax DMAX NLIT
"""
import sys, random
from fractions import Fraction
import mpmath as mp
import cm_lib as L

p, seed, NW, nmin, nmax, DMAX, NLIT = map(int, sys.argv[1:8])
random.seed(seed)
mp.mp.dps = 40
C = L.Consts(p)
E = L.eprime_constants(C)
EP = 60
PE = p ** EP
rs = [Fraction(6, 5), Fraction(27, 20), Fraction(3, 2)]
done = dom = 0
minmargin = mp.inf
lit_ok = lit_n = 0
skipped = 0
for w in range(NW):
    r = rs[w % 3]
    n = random.randrange(nmin, nmax)
    N = -(-r.numerator * n // r.denominator)
    Np = -(-r.numerator * N // r.denominator)
    x = random.randrange(PE)
    mode = w % 4
    if mode:
        pos = {1: n + 1 + random.randrange(2), 2: N + 1 + random.randrange(p), 3: (n + Np) // 2}[mode]
        d = random.randrange(2, DMAX + 1)
        x = (-pos + p ** d * random.randrange(1, PE)) % PE
    gl = [(i, L.vp((x + i) % PE, p)) for i in range(n + 1, Np + 1) if (x + i) % p == 0]
    K = sum(s for _, s in gl); D = sum(s for i, s in gl if i <= N); MW = max(s for _, s in gl)
    theta = -(-D // 2)
    if not (MW <= K - theta and theta >= 1):
        skipped += 1
        continue
    fp = min(theta, K - MW)
    PEb = L.propDE_block(p, gl, n, Np, K, C, fprime=fp)
    lE = mp.log(mp.mpf(int(PEb.numerator))) - mp.log(mp.mpf(int(PEb.denominator)))
    for sig in (MW, MW + 3):
        fps = min(theta, K - sig)
        lEp = L.eprime_ln(C, E, K, Np - n, sig, fps)
        done += 1
        if lEp >= lE:
            dom += 1
        else:
            print(f"E' < E: p={p} n={n} N={N} N'={Np} D={D} K={K} M_W={MW} sigma={sig}: ln E' = {mp.nstr(lEp, 10)} < ln E = {mp.nstr(lE, 10)}")
        minmargin = min(minmargin, lEp - lE)
    if lit_n < NLIT and Np - n <= 400:
        lit_n += 1
        PD = L.propDE_block(p, gl, n, Np, K, C)
        a = Fraction(int(PD.numerator), int(PD.denominator)) == L.propDE_literal(p, gl, n, Np, K, C)
        b = Fraction(int(PEb.numerator), int(PEb.denominator)) == L.propDE_literal(p, gl, n, Np, K, C, theta=theta, MW=MW)
        lit_ok += (a and b)
print(f"RESULT p={p} (S={C.S}): E' >= E in {dom}/{done} (window, sigma) pairs; min ln(E'/E) = {mp.nstr(minmargin, 6)}; "
      f"{skipped} windows skipped (Lemma F hypothesis fails); block == literal (D and E) in {lit_ok}/{lit_n}")
