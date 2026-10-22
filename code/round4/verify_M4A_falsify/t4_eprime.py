"""t4: Prop E' (closed form) >= Prop E (exact block form) on many random and adversarial windows,
and Prop D / Prop E block form == per-c Lemma Q form on smaller windows (two code paths).
Windows [n, N, N') with N = ceil(r n), N' = ceil(r N); ball radius b = M_W + 1 (theta =
min(ceil(D/2), D-b+1)); only windows with M_W <= K - theta and theta >= 1 are used.
Adversarial x: deep gate (depth s up to SMAX) at distance g from n or from N; x near -n-2.
Also tests sigma > M_W (E' is claimed for every sigma >= M_W).
usage: python3 t4_eprime.py p SEED NW nmin nmax SMAX
"""
import sys, random
import mpmath as mp
from fractions import Fraction
import vf_lib as L

p = int(sys.argv[1]); seed = int(sys.argv[2]); NW = int(sys.argv[3])
nmin = int(sys.argv[4]); nmax = int(sys.argv[5]); SMAX = int(sys.argv[6])
random.seed(seed)
mp.mp.dps = 40
C = L.eprime_consts(p)
E = 80
ok = bad = skipped = paths = paths_bad = 0
minmargin = mp.inf
kinds = {}
for w in range(NW):
    r = random.choice((Fraction(6, 5), Fraction(27, 20), Fraction(3, 2)))
    n = random.randint(nmin, nmax)
    N = -(-(r.numerator * n) // r.denominator)
    Np = -(-(r.numerator * N) // r.denominator)
    kind = random.choice(("rand", "deep_n", "deep_N", "neg2", "deep_mid"))
    if kind == "rand":
        x = random.randrange(p ** E)
    else:
        s = random.randint(2, SMAX)
        if kind == "deep_n":
            g = random.randint(1, 2 * p)
            base = n + g
        elif kind == "deep_N":
            g = random.randint(1, 2 * p)
            base = N + g
        elif kind == "neg2":
            base = n + 2
        else:
            base = random.randint(n + 1, Np)
        u = random.randrange(1, p ** 20)
        while u % p == 0:
            u = random.randrange(1, p ** 20)
        x = (-base + p ** s * u) % p ** E
    gl = [(i, L.vmod(x + i, p, E)) for i in range(n + 1, Np + 1) if (x + i) % p == 0]
    K = sum(s for _, s in gl); D = sum(s for i, s in gl if i <= N); MW = max(s for _, s in gl)
    b = MW + 1
    theta = min(-(-D // 2), D - b + 1)
    if theta < 1 or MW > K - theta:
        skipped += 1
        continue
    kinds[kind] = kinds.get(kind, 0) + 1
    fp = min(theta, K - MW)
    PE = L.block_bound(p, gl, n, Np, K, fp)
    lE = mp.log(mp.mpf(int(PE.numerator))) - mp.log(mp.mpf(int(PE.denominator)))
    for sig in (MW, MW + random.randint(1, 5)):
        lEp = L.eprime_log(p, K, Np - n, sig, min(theta, K - sig), C)
        if lEp >= lE:
            ok += 1
            minmargin = min(minmargin, lEp - lE)
        else:
            bad += 1
            print(f"E' < E: p={p} kind={kind} x mod p^15={x % p**15} n={n} N={N} Np={Np} D={D} K={K} MW={MW} sigma={sig} lnE={mp.nstr(lE,10)} lnE'={mp.nstr(lEp,10)}")
    # two code paths on small windows
    if Np - n <= 160 and paths < 60:
        paths += 1
        PE1 = L.propDE_via_Q(p, x, E, n, Np, K, theta=theta, MW=MW, mode="MW")
        PD1 = L.propDE_via_Q(p, x, E, n, Np, K)
        PD2 = L.block_bound(p, gl, n, Np, K, None)
        if PE1 != Fraction(int(PE.numerator), int(PE.denominator)) or PD1 != Fraction(int(PD2.numerator), int(PD2.denominator)):
            paths_bad += 1
            print("PATH MISMATCH", p, x, n, N, Np)
print(f"p={p}: windows tested {sum(kinds.values())} (kinds {kinds}), skipped {skipped}; E'>=E: {ok} ok, {bad} violations; "
      f"min ln(E'/E) = {mp.nstr(minmargin, 6)}; two-path checks {paths}, mismatches {paths_bad}")
