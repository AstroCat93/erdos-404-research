"""Counterexample hunt for the intermediate steps of Theorem 11.17 / Corollary 11.19 (note_v3 §11.2).
Builds the actual window code of the proof around a simple zero alpha = x_c (Prop 11.13(b)),
computes the zeros z(c) by p-adic Newton to high precision, and checks on random code pairs:
  (i)  z(c) is a zero of F_{e^{J(c)}}, simple with slope lambda, z = alpha mod p^{P0};
  (ii) formula (11.2): v(z-z') = L_k(z) - lambda + d with d = v(bracket), 0 <= d < G_k;
  (iii) the cylinder criterion: agree on windows 0..k  <=>  v(z'-z) >= rho_k(z);
  (iv)  rho_k constant on cylinders (L_k(z') = L_k(z) when z' in the cylinder of z).
Usage: python3 test_1117_codes.py p w K c nwin npairs seed"""
import sys, random, itertools
p, w, K, c, NW, NPAIRS, seed = map(int, sys.argv[1:8])
random.seed(seed)
P = w*p
R = 400  # working p-adic precision (digits)
MOD = p**R
def v(x):
    x %= MOD
    if x == 0: return R
    k = 0
    while x % p == 0: x //= p; k += 1
    return k
def F_and_dF(x, word):  # word: sorted list of j with e_j=1
    m = max(word); pi, dpi = 1, 0; F, dF = 0, 0; ws = set(word)
    for j in range(0, m+1):
        if j > 0:
            dpi = (dpi*(x+j) + pi) % MOD; pi = (pi*(x+j)) % MOD
        if j in ws: F = (F+pi) % MOD; dF = (dF+dpi) % MOD
    return F, dF
def newton(x, word, lam):
    for _ in range(200):
        F, dF = F_and_dF(x, word)
        if F % MOD == 0: return x
        a = v(F); assert v(dF) == lam, ("slope changed", v(dF), lam)
        assert a > 2*lam, ("not in Hensel range", a, lam)
        u = (dF // p**lam); b = F // p**a  # both exact (we only need mod p^R)
        step = (p**(a-lam) * b * pow(u, -1, MOD)) % MOD
        x = (x - step) % MOD
    raise RuntimeError("newton")
def pi_val(x, j):
    r = 1
    for l in range(1, j+1): r = r*(x+l) % MOD
    return r
# base word and simple zero alpha = x_c, slope lambda = v(c!)
base = [0, 1, 2, c+2]
import math
lam = v(math.factorial(c))
alpha = newton((-2 + 0) % MOD, base, lam) if False else None
# start: y = x+2 with v(y)=v(c!): use Hensel on H(y)=y+(y-1)pi_c(y) from y=0
def H_dH(y):
    pc, dpc = 1, 0
    for i in range(1, c+1):
        dpc = (dpc*(y+i) + pc) % MOD; pc = pc*(y+i) % MOD
    return (y + (y-1)*pc) % MOD, (1 + pc + (y-1)*dpc) % MOD
y = 0
for _ in range(200):
    h, dh = H_dH(y)
    if h == 0: break
    y = (y - h*pow(dh, -1, MOD)) % MOD
alpha = (y-2) % MOD
F0, dF0 = F_and_dF(alpha, base)
assert F0 == 0 and v(dF0) == lam, (v(F0), v(dF0), lam)
assert v(alpha+2) == v(math.factorial(c))
# runs of alpha
l0 = next(l for l in range(1, p+1) if (alpha+l) % p == 0)
def L_at(x, n): return v(pi_val(x, n))
# choose i0
i0 = 0
while True:
    li = l0 + p*i0
    if li >= p*(2*lam+2) and li > c+2 and L_at(alpha, li)-lam >= max(K+1, v(alpha+2)+1): break
    i0 += 1
a = [l0 + p*(i0 + k*w) for k in range(NW+1)]
P0 = L_at(alpha, a[0]) - lam
def vK(x): return min(v(x), K)
types = [(alpha + a[k]) % p**K for k in range(NW)]
def Gk(tau): return min(K, sum(min(v((tau+t) % p**K) if (tau+t) % p**K else K, K) for t in range(1, P+1)))
def qs(tau, M):
    out = []; cur = 1 % M
    for s in range(P):
        if s > 0: cur = cur*(tau+s) % M
        out.append(cur)
    return out
fams, Gs = [], []
for k in range(NW):
    G = Gk(types[k]); M = p**G; q = qs(types[k], M)
    seen = {};
    subs = list(itertools.chain.from_iterable(itertools.combinations(range(P), r) for r in range(P+1)))
    random.shuffle(subs)
    for S in subs:
        sm = sum(q[s] for s in S) % M
        if sm not in seen: seen[sm] = S
    fams.append(list(seen.values())); Gs.append(G)
print(f"p={p} w={w} K={K} c={c} lambda={lam} l0={l0} i0={i0} P0={P0} windows={NW} N_k={[len(f) for f in fams]} G_k={Gs}")
def word_of(code):
    J = sorted(a[k]+s for k in range(NW) for s in code[k])
    return base + J
cache = {}
def zero_of(code):
    key = tuple(code)
    if key not in cache:
        z = newton(alpha, word_of(code), lam)
        F, dF = F_and_dF(z, word_of(code))
        assert F == 0 and v(dF) == lam
        assert v(z-alpha) >= P0, ("z not = alpha mod p^P0", v(z-alpha), P0)
        cache[key] = z
    return cache[key]
def Lk(z, k): return L_at(z, a[k])
fails = 0; checked = 0
for t in range(NPAIRS):
    c1 = [random.choice(f) for f in fams]
    k = random.randrange(NW)
    c2 = list(c1);
    alt = [S for S in fams[k] if S != c1[k]]
    c2[k] = random.choice(alt)
    for m in range(k+1, NW):
        if random.random() < 0.5: c2[m] = random.choice(fams[m])
    z1, z2 = zero_of(c1), zero_of(c2)
    dist = v(z1-z2)
    br = (sum(pi_val(z1, a[k]+s)//1 for s in c1[k]) - sum(pi_val(z1, a[k]+s) for s in c2[k])) % MOD
    Lz = Lk(z1, k)
    d = v(br) - Lz
    pred = Lz - lam + d
    ok = (dist == pred) and (0 <= d < Gs[k])
    # cylinder criterion and rho constancy
    for kk in range(NW):
        rho = Lk(z1, kk) + Gs[kk] - lam
        agree = all(c1[m] == c2[m] for m in range(kk+1))
        ok = ok and (agree == (dist >= rho))
        if agree: ok = ok and (Lk(z2, kk) == Lk(z1, kk))
    checked += 1
    if not ok:
        fails += 1; print("FAIL", k, dist, pred, d, Gs[k])
print(f"pairs checked {checked} failures {fails}")
