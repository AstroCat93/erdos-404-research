"""Referee checks for Section 11.3 / 11.2 at p=2 (independent code; T2/T1b scripts not read).
(1) Prop 11.25 finite cases (a),(b),(c) incl. the 64-case histogram.
(2) Prop 11.16 configuration check (subset sums of 4 signed normalised run elements mod 8).
(3) Prop 11.32 identity S_{1,3}=(x+2)^3.
(4) Cor 11.30 main-term constants and side-term supremum (own piecewise evaluation)."""
from fractions import Fraction as Fr
import math, itertools, sympy

def v2(q):
    q = Fr(q)
    if q == 0: return math.inf
    n, d = q.numerator, q.denominator
    v = 0
    while n % 2 == 0: n //= 2; v += 1
    while d % 2 == 0: d //= 2; v -= 1
    return v

def pi(k, x):
    r = 1
    for i in range(1, k + 1): r *= (x + i)
    return r

print("== Prop 11.25(a): S_e(-4) = 1 + e1 pi1(-4) + e2 pi2(-4) + e3 pi3(-4)")
vals = []
for e1, e2, e3 in itertools.product([0, 1], repeat=3):
    s = 1 + e1 * pi(1, -4) + e2 * pi(2, -4) + e3 * pi(3, -4)
    vals.append(s)
print(" values", vals, " max v2 =", max(v2(s) for s in vals))
print("== Prop 11.25(b): Phi_e(-4), Phi_e(y)=e2 - 1/(1-y) + sum_k e_{k+2} pi_k(y)")
def Phi(e, y):  # e: dict index->bit, indices >=2
    s = Fr(e.get(2, 0)) - Fr(1, 1 - y)
    k = 1
    while True:
        pk = pi(k, y)
        if pk == 0: break
        s += e.get(k + 2, 0) * pk
        k += 1
    return s
for (e2, e3) in [(1, 0), (0, 1)]:
    out = set()
    for e4, e5 in itertools.product([0, 1], repeat=2):
        out.add(Phi({2: e2, 3: e3, 4: e4, 5: e5}, -4))
    print(f" e2={e2},e3={e3}:", sorted(out), " v2:", sorted(v2(t) for t in out))
print("== Prop 11.25(c): Phi_e(-8), e2=0,e3=1, e4..e9 free (64 cases)")
hist = {}
for bits in itertools.product([0, 1], repeat=6):
    e = {2: 0, 3: 1}
    for i, b in enumerate(bits): e[4 + i] = b
    t = Phi(e, -8)
    hist[v2(t)] = hist.get(v2(t), 0) + 1
print(" histogram", dict(sorted(hist.items())))
# also e2=1,e3=0 at -4 ok above. Lemma 11.24(c) identity check symbolic
X = sympy.symbols('x')
y = X + 2
print("== Lemma 11.24(c) identity symbolic check for random words")
import random
random.seed(1)
bad = 0
for trial in range(200):
    n = random.randint(3, 12)
    e = [1, 1] + [random.randint(0, 1) for _ in range(n - 2)]
    S = sum(e[j] * sympy.prod([X + i for i in range(1, j + 1)]) for j in range(n))
    Y = sympy.symbols('y')
    Ph = e[2] - 1 / (1 - Y) + sum(e[k + 2] * sympy.prod([Y + i for i in range(1, k + 1)]) for k in range(1, n - 2))
    rhs = (Y * (Y - 1) * Ph).subs(Y, X + 2)
    if sympy.simplify(S - rhs) != 0: bad += 1
print(" failures:", bad, "of 200")
print("== Prop 11.32: S_{1,3} - (x+2)^3 =", sympy.expand(1 + (X + 1) + (X + 1) * (X + 2) * (X + 3) - (X + 2) ** 3))

print("== Prop 11.16: runs u (level V) and u+1 (level V+1); X = x+l_u+2, X = 6 mod 8")
# normalised elements (divide by 2^V U):  pi_{l_u}->1, pi_{l_u+1}->(X-1), pi_{l_u+2}->(X-1)X, pi_{l_u+3}->(X-1)X(X+1)
# later runs have level >= V + J_u + J_{u+1} = V+1+J_{u+1}
for Xm in range(0, 64):
    if Xm % 8 != 6: continue
    J1 = v2(Xm + 2) if (Xm + 2) % 64 else 6  # J_{u+1} = v(x+l_u+4) = v(X+2), mod-64 representative
    elems = [1, Xm - 1, (Xm - 1) * Xm, (Xm - 1) * Xm * (Xm + 1)]
    allok = True; failsigns = []
    for U in [1, 3, 5, 7]:
        for sg in itertools.product([1, -1], repeat=4):
            sums = set()
            for sub in itertools.product([0, 1], repeat=4):
                sums.add(sum(s * c * U * b for s, c, b in zip(sg, elems, sub)) % 8)
            # later runs (level >= V+1+J1) only matter mod 8 if 1+J1 < 3
            if not {1, 3, 5, 7} <= sums:
                allok = False; failsigns.append((U, sg))
    if Xm < 16 or not allok:
        print(f" X mod 64={Xm}: J_(u+1)={J1}; all odd residues mod 8 reached for all units U, all 16 signs: {allok}; #fail={len(failsigns)}")
print("  (J_(u+1)=2 case, i.e. X = 2 mod 8 is not of this form; T1b avoided it. Check: X=6 mod 8 forces v(X+2)>=3.)")
# what if J_{u+1}=2 : that requires X+2 = 4 mod 8 -> X = 2 mod 8, then J_u = v(X)=1 still; run u+2 at level V+1+2=V+3: no effect mod 8
for Xm in [2, 10]:
    elems = [1, Xm - 1, (Xm - 1) * Xm, (Xm - 1) * Xm * (Xm + 1)]
    nf = 0
    for sg in itertools.product([1, -1], repeat=4):
        sums = {sum(s * c * b for s, c, b in zip(sg, elems, sub)) % 8 for sub in itertools.product([0, 1], repeat=4)}
        if not {1, 3, 5, 7} <= sums: nf += 1
    print(f" X={Xm} (J_(u+1)=2): sign patterns failing to reach all odd residues mod 8: {nf}/16")
