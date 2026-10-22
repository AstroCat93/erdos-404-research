"""Concrete test of the window-code construction (Thm 11.17) and of the
distance formula (11.2), at p=2 and p=3, on explicit zeros z(c) computed by
p-adic Newton.  Independent code (written from the note's statements only).
Usage: python3 codes_test.py p w K kmax  [c]
"""
import sys, itertools, random
p = int(sys.argv[1]); w = int(sys.argv[2]); K = int(sys.argv[3]); kmax = int(sys.argv[4])
c0 = int(sys.argv[5]) if len(sys.argv) > 5 else 2 * p
PREC = 600
MOD = p ** (PREC + 60)

def v(x, cap=10**9):
    if x == 0: return cap
    n = 0
    while x % p == 0:
        x //= p; n += 1
        if n >= cap: return cap
    return n

def vm(x, M=MOD):  # valuation of x mod M (exactness up to log_p M)
    return v(x % M, cap=PREC + 50)

def F_and_dF(x, J):
    """J = sorted list of positions j>=0 with e_j=1. returns F, F' mod MOD."""
    s = 0; ds = 0; pi = 1; dpi = 0; jmax = max(J); Js = set(J)
    for j in range(0, jmax + 1):
        if j > 0:
            dpi = (dpi * (x + j) + pi) % MOD
            pi = pi * (x + j) % MOD
        if j in Js:
            s += pi; ds += dpi
    return s % MOD, ds % MOD

def newton(x, J):
    for _ in range(200):
        f, df = F_and_dF(x, J)
        lam = vm(df)
        if vm(f) >= PREC: return x % p ** PREC, lam
        u = df // p ** lam
        x = (x - (f // p ** lam) * pow(u, -1, MOD)) % MOD
    raise RuntimeError("no convergence")

def pi_val(x, j):
    r = 1
    for l in range(1, j + 1): r = r * (x + l) % MOD
    return r

# base word e: e0=e1=e2=e_{c+2}=1  (Prop 11.13(b)); zero near -2 with v(x+2)=v(c!)
base = [0, 1, 2, c0 + 2]
import math
alpha, lam = newton(-2 + math.factorial(c0), base)
f, df = F_and_dF(alpha, base)
print(f"p={p} base word {base}; alpha mod p^20 = {alpha % p**20}, v(F)={vm(f)}, slope lam={lam}, v(alpha+2)={vm(alpha+2)}")
assert vm(alpha + 2) == v(math.factorial(c0)) and lam == vm(alpha+2)

# runs
l0 = next(l for l in range(1, p + 1) if (alpha + l) % p == 0)
def L(i, z): return vm(pi_val(z, l0 + p * i))
i0 = 0
while True:
    li = l0 + p * i0
    if li >= p * (2 * lam + 2) and li > max(base) and L(i0, alpha) - lam >= max(K + 1, vm(alpha + 2) + 1):
        break
    i0 += 1
P = w * p
a = [l0 + p * (i0 + k * w) for k in range(kmax + 1)]
P0 = L(i0, alpha) - lam
print(f"l0={l0} i0={i0} a_k={a} P0={P0}")

def Gk(tau):
    return min(K, sum(min(vm(tau + t, p ** K), K) for t in range(1, P + 1)))
def qs(tau, s, M):
    r = 1
    for t in range(1, s + 1): r = r * (tau + t) % M
    return r

fams = []; taus = []; Gs = []
for k in range(kmax + 1):
    tau = (alpha + a[k]) % p ** K
    G = Gk(tau); M = p ** G
    q = [qs(tau, s, p ** K) for s in range(P)]
    seen = {}
    for bits in range(1 << P):
        S = tuple(s for s in range(P) if bits >> s & 1)
        r = sum(q[s] for s in S) % M
        if r not in seen: seen[r] = S
    fams.append(list(seen.values())); taus.append(tau); Gs.append(G)
    print(f"window {k}: tau={tau} G={G} N={len(seen)}")

# sample codes
random.seed(1)
NS = int(sys.argv[6]) if len(sys.argv) > 6 else 60
codes = set()
while len(codes) < NS:
    codes.add(tuple(random.randrange(len(fams[k])) for k in range(kmax + 1)))
codes = list(codes)
# add pairs sharing long prefixes
extra = []
for cc in codes[:20]:
    for k in range(kmax + 1):
        alt = list(cc); alt[k] = (alt[k] + 1) % len(fams[k]); extra.append(tuple(alt))
codes = list(set(codes + extra))
zs = {}
bad = 0
for cc in codes:
    J = sorted(set(base) | {a[k] + s for k in range(kmax + 1) for s in fams[k][cc[k]]})
    z, lz = newton(alpha, J)
    f, _ = F_and_dF(z, J)
    if lz != lam or vm(z - alpha) < P0: bad += 1; print("SLOPE/P0 FAIL", cc, lz, vm(z - alpha))
    zs[cc] = (z, J)
print(f"{len(codes)} zeros computed; slope/P0 failures: {bad}")

# distance formula check
fails = 0; checked = 0; bydepth = {}
items = list(zs.items())
for i in range(len(items)):
    for j in range(i + 1, len(items)):
        (c1, (z1, J1)), (c2, (z2, J2)) = items[i], items[j]
        k = next(m for m in range(kmax + 1) if c1[m] != c2[m])
        Lk = vm(pi_val(z1, a[k]))
        q = [qs(z1 + a[k], s, MOD) for s in range(P)]
        br = sum(q[s] for s in fams[k][c1[k]]) - sum(q[s] for s in fams[k][c2[k]])
        d = vm(br)
        dist = vm(z1 - z2)
        ok = (d < Gs[k]) and (dist == Lk - lam + d)
        # rho_k ordering: agree on windows 0..k  iff dist >= rho_k
        rho = Lk + Gs[k] - lam
        checked += 1
        if not ok:
            fails += 1
            if fails < 10: print("DIST FAIL", c1, c2, k, Lk, d, Gs[k], dist)
        bydepth.setdefault(k, []).append(dist)
print(f"pairs checked {checked}, distance-formula failures {fails}")
for k in sorted(bydepth): print(f"  first diff at window {k}: dist range {min(bydepth[k])}..{max(bydepth[k])}")
# rho_k disjointness: for each z and each k, the ball of radius p^-rho_k(z) contains exactly the codes agreeing on 0..k
rfails = 0
for c1, (z1, _) in items:
    for k in range(kmax):
        rho = vm(pi_val(z1, a[k])) + Gs[k] - lam
        for c2, (z2, _) in items:
            if c2 == c1: continue
            agree = c1[:k + 1] == c2[:k + 1]
            if agree != (vm(z1 - z2) >= rho): rfails += 1
print(f"cylinder/ball correspondence failures: {rfails}")
# box count of the finite family: distinct classes mod p^G
for G in range(P0, P0 + 40, 4):
    print(f"  G={G}: classes mod p^G hit by sampled zeros = {len({z % p**G for z,_ in zs.values()})}")
