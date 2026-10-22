# Test A: Proposition 11.25 (slope certificates), Lemma 11.24(b), Lemma 11.23(a)-(d),
# and the finite certificate values, on random and adversarial points.
import sys, random, itertools
from fractions import Fraction
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from lib import *

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
NMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 40
TRIALS = int(sys.argv[3]) if len(sys.argv) > 3 else 300

CLASSES = {'C0': (0, 3, 1, 4), 'C2': (2, 3, 3, 7), 'C6': (6, 4, 6, 11)}

def vfrac(q):
    q = Fraction(q)
    if q == 0:
        return 10**9
    a, b = q.numerator, q.denominator
    return v(a, 10**6) - v(b, 10**6) if a else 10**9

def vint(a):
    a = abs(a)
    return (a & -a).bit_length() - 1 if a else 10**9

# --- finite certificate values (independent recomputation) ---
def pi_int(x, k):
    r = 1
    for i in range(1, k + 1):
        r *= (x + i)
    return r
print("S_e(-4) valuations (C0):", sorted(vint(1 - 3*a + 6*b - 6*c) for a, b, c in itertools.product((0,1), repeat=3)))
# C2: Phi_e(-4), families
for fam in ('A', 'B'):
    vals = []
    for e4, e5 in itertools.product((0, 1), repeat=2):
        e2, e3 = (1, 0) if fam == 'A' else (0, 1)
        Phi = e2 - Fraction(1, 1 + 4) + e3 * pi_int(-4, 1) + e4 * pi_int(-4, 2) + e5 * pi_int(-4, 3)
        vals.append(vfrac(Phi))
    print("C2 family", fam, "v(Phi_e(-4)) =", vals)
# C6 family B: Phi_e(-8)
hist = {}
for bits in itertools.product((0, 1), repeat=6):
    Phi = -Fraction(1, 9) + pi_int(-8, 1) + sum(bits[k] * pi_int(-8, k + 2) for k in range(6))
    hist[vfrac(Phi)] = hist.get(vfrac(Phi), 0) + 1
print("C6 family B v(Phi_e(-8)) histogram:", dict(sorted(hist.items())))
# Direct check of identity S_e(-m-2) = (-m)(-m-1) Phi_e(-m) for random words
for _ in range(500):
    m = rng.choice([4, 8, 6, 10, 12])
    L = rng.randint(3, 15)
    e = [1, 1] + [rng.randint(0, 1) for _ in range(L)]
    x = -m - 2
    S = sum(e[j] * pi_int(x, j) for j in range(len(e)))
    Phi = e[2] - Fraction(1, 1 + m) + sum(e[k + 2] * pi_int(-m, k) for k in range(1, len(e) - 2))
    assert S == (-m) * (-m - 1) * Phi, (m, e)
print("identity Lemma 11.24(c) at negative integers: ok")

# --- random / adversarial slope checks ---
worst = {c: 0 for c in CLASSES}
viol = []
lem_viol = []
for trial in range(TRIALS):
    for cname, (r0, k, L, Vc) in CLASSES.items():
        mode = trial % 3
        if mode == 0:
            x = rand_in_class(r0, k, rng)
        else:
            # adversarial: very close to a negative integer in the class
            m = rng.choice([mm for mm in range(2, 200, 2) if (-mm) % (1 << k) == r0])
            j = rng.randint(k + 4, 60)
            x = ((-m) + (rng.getrandbits(P) << j)) & MASK
            if (x % (1 << k)) != r0:
                continue
        n = rng.randint(6, NMAX)
        paths, V = alive_paths(x, n)
        if V[n] < Vc:
            continue
        for e, S, dS in paths:
            lam = v(dS)
            worst[cname] = max(worst[cname], lam)
            if lam > L:
                viol.append((cname, x % (1 << 64), n, e, lam))
            # Lemma 11.24(b) for C2, C6
            if cname != 'C0':
                t = v(x + 2)
                if n >= 4 and v(S) >= t + 1 and not (e[1] == 1 and e[2] + e[3] == 1):
                    lem_viol.append(('11.24b', cname, n, e))
        # Lemma 11.23 (a),(b),(c)
        if n >= 4 and V[n] < Mn(x, n) + 1:
            lem_viol.append(('11.23b', x, n))
        Nn = n + rng.randint(1, 20)
        D = Vn(x, Nn) - V[n]
        if D > (Nn - n) + Mn(x, Nn):
            lem_viol.append(('11.23c', x, n, Nn))
        K = rng.randint(1, 8)
        r = x % (1 << K)
        NK = (1 << K) - r if r else (1 << K)
        W = lambda N: N - Vn(x, N)
        for d in range(0, 1 << K, max(1, (1 << K) // 7)):
            if W(NK + d) != W(NK) + s(d):
                lem_viol.append(('11.23a', x, K, d))
        if W(NK) > 1 - s(r):
            lem_viol.append(('10.2d', x, K))
print("max slope seen per class:", worst)
print("slope violations:", len(viol), viol[:5])
print("lemma violations:", len(lem_viol), lem_viol[:5])
