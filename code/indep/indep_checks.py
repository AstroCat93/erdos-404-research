#!/usr/bin/env python3
"""Independent re-checks for the Erdos #404 research note (written from scratch by the lead
author's assistant; shares no code with the track programs in ../A .. ../F).

Normal form used throughout.  For x in Z_p and finite B subset {1,2,...} put
    S_B(x) = 1 + sum_{b in B} (x+1)(x+2)...(x+b),
    g_p(x) = sup_B v_p(S_B(x)).
For a natural number a:  a! * S_B(a) = a! + sum_{b in B} (a+b)!, hence
    f(a,p) = v_p(a!) + g_p(a).
The decision procedure g_ge(x,p,G) ("is g_p(x) >= G?") is an exact residue-set DP:
the terms P_b(x) = (x+1)...(x+b) have nondecreasing valuation in b, so before term b is
considered every partial sum must already be 0 mod p^min(G, v_p(P_b(x))); once
v_p(P_b(x)) >= G all remaining terms vanish mod p^G.

usage: python3 indep_checks.py [witness_file p K ...]   (extra witness checks are optional)
"""
import sys, time, itertools
from math import factorial

def vp(n, p):
    if n == 0:
        return 10**9
    v = 0
    while n % p == 0:
        n //= p; v += 1
    return v

def vfact(n, p):
    s = 0
    while n:
        n //= p; s += n
    return s

def g_ge(x, p, G):
    """exact: is there finite B with p^G | S_B(x)?  (x any integer)"""
    if G <= 0:
        return True
    M = p ** G
    states = {1 % M}
    prod = 1
    b = 0
    while True:
        b += 1
        prod = (prod * (x + b)) % M
        vb = min(G, vp(prod, p))
        q = p ** vb
        states = {s for s in states if s % q == 0}
        if not states:
            return False
        if vb >= G:
            return 0 in states
        states |= {(s + prod) % M for s in states}

def g_val(x, p, cap):
    """exact min(g_p(x), cap)"""
    G = 0
    while G < cap and g_ge(x, p, G + 1):
        G += 1
    return G

def f_val(a, p, cap):
    return vfact(a, p) + g_val(a, p, cap)

def subset_sums_mod(elems, M):
    """bitset of subset sums mod M (bit r set iff r is a subset sum mod M)"""
    mask = (1 << M) - 1
    S = 1
    for x in elems:
        x %= M
        if x:
            S |= ((S << x) | (S >> (M - x))) & mask
    return S

def popcount(S):
    return bin(S).count("1")

ok_all = True
def report(name, ok, detail=""):
    global ok_all
    ok_all &= bool(ok)
    print(f"[{'OK ' if ok else 'BAD'}] {name}  {detail}", flush=True)

t0 = time.time()

# 1. known exact values (Lin, Kovac, Kitamura) -------------------------------------------
known = [(1,2,0),(2,2,254),(3,2,1),(4,2,6),(5,2,3),(6,2,133),(14,2,1533),
         (3,3,3),(39,3,25),(700,3,363),(110,5,30),(236,5,61),(42,7,7),(4,7,0),(6,7,0),
         (113,11,11),(163,13,13)]
for a, p, fv in known:
    g = fv - vfact(a, p)
    ok = g_ge(a, p, g) and not g_ge(a, p, g + 1)
    report(f"f({a},{p}) = {fv}", ok, f"(g = {g}: >=g reachable, >=g+1 not)")

# 2. the disputed value g(12,3) and g(26,5) ---------------------------------------------
g12 = g_val(12, 3, 30); g26 = g_val(26, 5, 16)
report("g_3(12) >= 20 (brief's '10' is not exact)", g12 >= 20, f"min(g_3(12),30) = {g12}")
report("g_5(26) >= 12", g26 >= 12, f"min(g_5(26),16) = {g26}")
report("g_3(3) = 2 exactly", g_val(3, 3, 10) == 2)

# 3. negative integers: E_p cap Z_{<0} = {-2}; shadows -m -------------------------------
def gamma_enum(m, p):
    """max_B v_p(S_B(-m)), B subset [1,m-1], by explicit enumeration of all 2^(m-1) subsets"""
    terms = []
    pr = 1
    for b in range(1, m):
        pr *= (-m + b)
        terms.append(pr)
    best = -1
    for mask in range(1 << len(terms)):
        s = 1 + sum(terms[i] for i in range(len(terms)) if mask >> i & 1)
        if s == 0:
            return None  # infinite
        best = max(best, vp(s, p))
    return best

report("S_{1}(-2) = 0 (the point -2 is in E_p for every p)", 1 + (-2 + 1) == 0)
bad = []
for p in (2, 3, 5, 7, 11, 13):
    for m in [1] + list(range(3, 15)):
        gm = gamma_enum(m, p)
        if gm is None:
            bad.append((p, m, "zero")); continue
        # oracle at the p-adic point -m (finite B suffice since P_b(-m)=0 for b>=m)
        if g_val(-m, p, gm + 2) != gm:
            bad.append((p, m, "oracle")); continue
        # shadows: a = p^(gm+1)*y - m, y=1..3, natural numbers: g(a) must equal gm exactly
        K = gm + 1
        for y in (1, 2, 3):
            a = p ** K * y - m
            while a < 1:
                a += p ** K
            if g_val(a, p, gm + 2) != gm:
                bad.append((p, m, "shadow", a))
report("shadow theorem: g(a,p) = gamma(m,p) on a = -m mod p^(gamma+1), m in {1,3..14}, p<=13",
       not bad, f"failures: {bad[:5]}")
print("    gamma(m,2), m=3..14:", [gamma_enum(m, 2) for m in range(3, 15)])
print("    gamma(m,3), m=3..14:", [gamma_enum(m, 3) for m in range(3, 15)])

# 4. frozen classes Phi_p = {r mod p : g = 0 on r + pZ} -----------------------------------
expected = {2:[1],3:[2],5:[2,4],7:[4,6],11:[7,8,10],13:[9,10,12],17:[12,13,14,16],
            19:[14,15,16,18],23:[19,20,22]}
for p, exp in expected.items():
    phi = [r for r in range(p) if not g_ge(r, p, 1)]
    report(f"Phi_{p}", phi == exp, f"{phi}")

# 5. Tao-type covering obstructions --------------------------------------------------------
# 5a: subset sums of {0!,...,8!} mod 81 miss exactly {68,77}
S = subset_sums_mod([factorial(t) for t in range(9)], 81)
miss = [r for r in range(81) if not S >> r & 1]
report("{0!,...,8!} mod 81 misses exactly {68,77}", miss == [68, 77], f"{miss}")
# 5b: p=2, every r mod 16: subset sums of P_j(r), j=0..15, do not cover Z/16
allfail = True
for r in range(16):
    el, pr = [1], 1
    for j in range(1, 16):
        pr *= (r + j); el.append(pr)
    if popcount(subset_sums_mod(el, 16)) == 16:
        allfail = False
report("p=2: A_x mod 16 != Z/16 for all x (so Tao covering never works at p=2)", allfail)

# 6. L_p = max L with subset sums of {(-1)^u/u! : u<p} covering Z/p^L ----------------------
expL = {3:1, 5:1, 7:2, 11:2, 13:2, 17:3, 19:3, 23:4}
for p, L in expL.items():
    def covers(Lev):
        M = p ** Lev
        el = [((-1) ** u * pow(factorial(u), -1, M)) % M for u in range(p)]
        return popcount(subset_sums_mod(el, M)) == M
    okL = covers(L) and not covers(L + 1)
    report(f"L_{p} = {L}", okL)

# 7. gate congruence (lemma behind Theorem C): if p^j | m+1, then
#    P_m(r) := prod_{i=1..r}(pm+i) == prod_{i=1..r}(i-p) (mod p^(j+1))
badg = 0
for p in (3, 5, 7, 11):
    for j in (1, 2, 3):
        for t in range(1, 30):
            m = p ** j * t - 1
            for r in range(p):
                A = 1; Bv = 1
                for i in range(1, r + 1):
                    A *= p * m + i; Bv *= i - p
                if (A - Bv) % p ** (j + 1):
                    badg += 1
report("gate congruence P_m(r) == prod(i-p) mod p^(j+1) when p^j | m+1", badg == 0)

# 8. p=2 halving lemma, numerically: g>=G depends only on a mod 2^(G-1) -----------------
viol = 0
for G in range(2, 12):
    for a in range(0, 2 ** (G - 1)):
        if g_ge(a, 2, G) != g_ge(a + 2 ** (G - 1), 2, G):
            viol += 1
report("halving lemma numerics (G=2..11, all classes)", viol == 0)

# 9. class counts |S_k| = #{r mod p^k : g_p(r) >= k} -------------------------------------
exp2 = [1, 2, 4, 6, 12, 24, 34, 62, 120, 238, 426, 802, 1548, 2870]
cnt2 = [sum(1 for r in range(2 ** k) if g_ge(r, 2, k)) for k in range(1, 15)]
report("p=2 |S_k|, k=1..14 (matches tracks D and E)", cnt2 == exp2, f"{cnt2}")
cnt3 = [sum(1 for r in range(3 ** k) if g_ge(r, 3, k)) for k in range(1, 9)]
print("    p=3 |S_k|, k=1..8:", cnt3, " densities:", [round(c / 3 ** k, 4) for k, c in enumerate(cnt3, 1)])
cnt5 = [sum(1 for r in range(5 ** k) if g_ge(r, 5, k)) for k in range(1, 6)]
print("    p=5 |S_k|, k=1..5:", cnt5, " densities:", [round(c / 5 ** k, 4) for k, c in enumerate(cnt5, 1)])

# 10. Theorem A spot checks from actual factorials --------------------------------------
# Cov(p,t,H): for N* = p^t K'' (p !| K''), the normalised block n!/p^v((N*-H)!) , N*-H<=n<N*,
# has subset sums covering Z/p^(v(N*!)-v((N*-H)!)).  Check over one full period of K'' mod p^c.
def cov_actual(p, t, H, Kvals):
    for K2 in Kvals:
        N = p ** t * K2
        N0 = N - H
        D = vfact(N, p) - vfact(N0, p)
        M = p ** D
        el, pr = [], 1
        # n!/N0! = prod_{s=1}^{n-N0}(N0+s); normalise by p^v of (N0!) only through the unit part of N0!
        # (the unit part of N0! is a common unit factor and does not affect coverage)
        for i in range(H):
            if i > 0:
                pr *= N0 + i
            q = pr
            # reduce: element is p^{v(n!)-v(N0!)} * unit; we need it mod p^D
            el.append(q % M)
        if popcount(subset_sums_mod(el, M)) != M:
            return False, K2
    return True, None

for (p, t, H) in [(5, 2, 10), (5, 3, 20), (7, 3, 19), (11, 3, 18), (13, 3, 19), (5, 4, 25)]:
    c = vfact(H - 1, p)
    per = p ** c
    Kvals = [k for k in range(1, per + 1) if k % p]  # one representative per unit class mod p^c
    if len(Kvals) > 120:
        Kvals = Kvals[:120]
    okc, badK = cov_actual(p, t, H, Kvals)
    report(f"Cov({p},{t},{H}) at actual positions N*=p^t K'' ({len(Kvals)} classes)", okc, f"{badK or ''}")
okn, _ = cov_actual(3, 2, 9, [1])
report("Cov(3,2,9) FAILS at N*=9 (negative case)", not okn)

# 11. optional witness checks --------------------------------------------------------------
def check_witness(path, p, K):
    A = []
    with open(path) as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            A.extend(int(w) for w in line.split())
    inc = all(A[i] < A[i + 1] for i in range(len(A) - 1))
    M = p ** K
    s, fact, n, idx = 0, 1, 0, 0
    last = A[-1]
    Aset = A
    j = 0
    while n <= last:
        if n > 0:
            fact = fact * n % M
        if j < len(Aset) and Aset[j] == n:
            s += fact; j += 1
        n += 1
    return inc, A[0], len(A), s % M == 0

args = sys.argv[1:]
while len(args) >= 3:
    path, p, K = args[0], int(args[1]), int(args[2]); args = args[3:]
    tt = time.time()
    inc, first, nterms, zero = check_witness(path, p, K)
    report(f"witness {path.split('/')[-1]}: sum == 0 mod {p}^{K}", inc and zero,
           f"(a={first}, terms={nterms}, increasing={inc}, {time.time()-tt:.0f}s)")

print(f"ALL_OK={ok_all}  total {time.time()-t0:.0f}s")
