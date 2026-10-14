"""t1: adversarial exact test of M4A Lemma Q:
    P(v(T_u)>=k, v(T_u')>=f) <= P0(g1,min(s1,k)) * prod_{r>=1, L_r<k} pi_r
for every u (not a negative integer), every t, 1<=k<=V_t(u), every f (f=None: no slope condition).
Exact probabilities by CRT DP over (T mod p^kmax, T' mod p^fmax).  Negative controls: stronger
(unproved) variants of the bound ('noM','half2D','depth2','noq') are also evaluated: a violation of
a control shows the test can see that feature of the bound.

usage: python3 t1_lemmaQ.py p SEED NU KIND kmax fmax tmax [a]
 KIND: rand  - Haar-random u
       neg   - u = -g + p^s w (deep gate at a small position g; near small negative integers)
       int   - u a small nonnegative integer
       scan  - all residues u mod p^a (random higher digits)
       dbl   - u near a p-adic double root of a random signed polynomial (high-slope paths)
       d1run - gates 2..(1+min(p-1,fmax+1)) of depth 1
       d1first - gates 1..min(p-1,fmax+1) of depth 1 (maximises consecutive 2D blocks)
"""
import sys, random
from fractions import Fraction
import numpy as np
import vf_lib as L

p = int(sys.argv[1]); seed = int(sys.argv[2]); NU = int(sys.argv[3]); KIND = sys.argv[4]
kmax = int(sys.argv[5]); fmax = int(sys.argv[6]); tmax = int(sys.argv[7])
a = int(sys.argv[8]) if len(sys.argv) > 8 else 3
random.seed(seed)
E = 60
CONTROLS = ("noM", "half2D", "depth2", "noq")


def gen_us():
    if KIND == "scan":
        for r in range(p ** a):
            yield (r + p ** a * random.randrange(p ** (E - a))) % p ** E
        return
    for _ in range(NU):
        if KIND == "rand":
            yield random.randrange(p ** E)
        elif KIND == "neg":
            g = random.randint(1, 2 * p + 1)
            s = random.randint(1, kmax + 2)
            w = random.randrange(1, p ** 10)
            while w % p == 0:
                w = random.randrange(1, p ** 10)
            yield (-g + p ** s * w) % p ** E
        elif KIND == "int":
            yield random.randint(0, 3 * p ** 2)
        elif KIND == "d1run":
            # gates 2..(1+min(p-1, fmax+1)) all of depth exactly 1 (at most p-1 consecutive gates can
            # have depth 1, since among p consecutive gates exactly one has depth >= 2)
            need = min(p - 1, fmax + 1)
            while True:
                u = random.randrange(p ** E)
                gl = L.gates(u, p, E, tmax)
                if len(gl) > need and all(s == 1 for _, s in gl[1:1 + need]):
                    yield u
                    break
        elif KIND == "d1first":
            # the first min(p-1, fmax+1) gates (g_1 included) all of depth 1: consecutive 2D blocks
            need = min(p - 1, fmax + 1)
            while True:
                u = random.randrange(p ** E)
                gl = L.gates(u, p, E, tmax)
                if len(gl) >= need and all(s == 1 for _, s in gl[:need]):
                    yield u
                    break
        elif KIND == "dbl":
            yield find_double_root()


def find_double_root():
    """random signed polynomial T=sum_{c<t0} d_c pi_c (d_0=1); search z mod p^A maximising
    min(v(T(z)), 2 v(T'(z))) and return z + p^A * random."""
    A = 4 if p <= 5 else 3
    mod = p ** (2 * A)
    zs = np.arange(p ** A, dtype=object)
    best = None
    for _ in range(40):
        t0 = random.randint(3, 3 * p)
        d = [1] + [random.choice((-1, 0, 0, 1)) for _ in range(t0 - 1)]
        P = np.ones(p ** A, dtype=object); Dv = np.zeros(p ** A, dtype=object)
        T = np.ones(p ** A, dtype=object); Tp = np.zeros(p ** A, dtype=object)
        for c in range(1, t0):
            Dv = (Dv * (zs + c) + P) % mod
            P = (P * (zs + c)) % mod
            T = (T + d[c] * P) % mod
            Tp = (Tp + d[c] * Dv) % mod
        for z in range(p ** A):
            tv = int(T[z]); tp = int(Tp[z])
            vt = 2 * A if tv == 0 else L.vp(tv, p)
            vd = 2 * A if tp == 0 else L.vp(tp, p)
            sc = min(vt, 2 * vd)
            if best is None or sc > best[0]:
                best = (sc, z)
    sc, z = best
    return (z + p ** A * random.randrange(p ** (E - A))) % p ** E


stats = dict(cases=0, fails=0, maxratio=Fraction(0), max2D=0, cases2D=0, attained=0)
ctrl = {c: 0 for c in CONTROLS}
worst = None
for u in gen_us():
    gl = L.gates(u, p, E, tmax)
    Pv, Dv = L.pi_and_deriv(u, tmax, p ** 40)
    dp = L.SignedDP(p, kmax, fmax, first_fixed=True, nprimes=2 if tmax <= 58 else 3)
    Vt = 0
    gi = 0
    for t in range(1, tmax + 1):
        c = t - 1
        dp.step(Pv[c], Dv[c])
        while gi < len(gl) and gl[gi][0] <= t:
            Vt += gl[gi][1]; gi += 1
        if Vt == 0:
            continue
        for k in range(1, min(Vt, kmax) + 1):
            for f in [None] + list(range(1, fmax + 1)):
                x, tot = dp.count_zero_fast(k, f if f is not None else 0)
                P = Fraction(x, tot)
                b = L.lemmaQ_bound(p, u, E, t, k, f, mode="Q")
                stats["cases"] += 1
                if b == 0:
                    if P != 0:
                        stats["fails"] += 1
                        print("FAIL(b=0)", p, u, t, k, f, P)
                    continue
                r = P / b
                if r > 1:
                    stats["fails"] += 1
                    print(f"FAIL p={p} u={u} t={t} k={k} f={f} P={P} bound={b} ratio={float(r):.6f}")
                if r == 1:
                    stats["attained"] += 1
                if r > stats["maxratio"]:
                    stats["maxratio"] = r
                    worst = (u % p ** 12, t, k, f, P, b)
                # number of 2D blocks: ratio of 1D-only bound to this bound is (q1/p / (q2/p^2))^#2D
                if f is not None:
                    g = L.lemmaQ_bound(p, u, E, t, k, None, mode="Q")
                    ratio2 = g / b
                    unit = (L.q_consts(p, 2)[1] / p) / (L.q_consts(p, 2)[2] / p ** 2)
                    m2 = 0
                    while ratio2 >= unit:
                        ratio2 /= unit; m2 += 1
                    if m2 > 0:
                        stats["cases2D"] += 1
                        stats["max2D"] = max(stats["max2D"], m2)
                for cm in CONTROLS:
                    if f is None and cm in ("noM", "half2D", "depth2"):
                        continue
                    bc = L.lemmaQ_bound(p, u, E, t, k, f, mode=cm)
                    if P > bc:
                        ctrl[cm] += 1
print(f"p={p} KIND={KIND} kmax={kmax} fmax={fmax} tmax={tmax}")
print(f"cases={stats['cases']} FAILURES={stats['fails']} max P/bound={float(stats['maxratio']):.6f} "
      f"(attained with equality in {stats['attained']} cases)")
print(f"cases with >=1 2D block: {stats['cases2D']}, max #2D blocks in one case: {stats['max2D']}")
print("negative controls (violations of stronger unproved variants): " + ", ".join(f"{c}:{ctrl[c]}" for c in CONTROLS))
if worst:
    print("worst case (u mod p^12, t, k, f, P, bound):", worst[0], worst[1], worst[2], worst[3], worst[4], worst[5])
