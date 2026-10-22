# Lead-author independent spot checks for note section 11 (round 3).
# Written from the statements in the track writeups, sharing no code with the tracks.
# Usage: python3 -I lead_checks_r3.py   (pure Python 3, ~1 min)
from fractions import Fraction
from itertools import product
from math import comb, log2, cos, pi, prod, log
import random

def vp(n, p):
    if n == 0:
        return None
    n, v = abs(n), 0
    while n % p == 0:
        n //= p; v += 1
    return v

def vfact(n, p):
    s, q = 0, n
    while q:
        q //= p; s += q
    return s

print("== 1. Window-code dimension D_p(w,K) of T1b Thm 3.1, own brute force (definition re-implemented)")
def D(p, w, K):
    P, M = w * p, p ** K
    tot = 0.0
    for y in range(p ** (K - 1)):
        tau = p * y
        G = 0
        for t in range(1, P + 1):
            a = (tau + t) % M
            G += K if a == 0 else min(vp(a, p), K)
        G = min(G, K)
        mod = p ** G
        q, cur = [], 1
        for s in range(P):
            q.append(cur % mod)
            cur = cur * (tau + s + 1) % M
        sums = {0}
        for x in q:
            sums |= {(u + x) % mod for u in sums}
        tot += log(len(sums)) / log(p)
    return (p - 1) / (w * p) * tot / p ** (K - 1)
for (p, w, K, ref) in [(2, 3, 7, 0.7317424946), (3, 2, 5, 0.8550881683), (5, 1, 4, 0.9236947455), (7, 1, 3, 0.9855433782)]:
    d = D(p, w, K)
    print(f"  D_{p}({w},{K}) = {d:.10f}  track value {ref}  agree={abs(d-ref)<1e-9}")

print("== 2. Gate-block law, T3a Lemma 2(b),(c): brute force over all 3^p sign vectors")
for p in (3, 5, 7, 11):
    e = [(-1) ** u * prod(range(u + 1, p)) for u in range(p)]   # (p-1)!/u! * (-1)^u
    W0 = 0
    cnt = {}
    for eta in product((-1, 0, 1), repeat=p):
        wgt = prod(2 if x == 0 else 1 for x in eta)               # weights 1/4,1/2,1/4 -> 1,2,1 (/4^p)
        W = sum(a * b for a, b in zip(eta, e))
        if W == 0:
            W0 += wgt
        for J in range(1, 9):
            if W % p ** J == 0:
                cnt[J] = cnt.get(J, 0) + wgt
    sums = {sum(x for x, s in zip(e, S) if s) for S in product((0, 1), repeat=p)}
    PW0 = Fraction(W0, 4 ** p)
    J0 = min(J for J in range(1, 9) if cnt[J] == W0)
    G1 = Fraction(p * cnt[1], 4 ** p) - 1
    print(f"  p={p}: P(W=0)={PW0} (3/2^(p+1)={Fraction(3, 2**(p+1))}) ; #distinct sums={len(sums)} (3*2^(p-2)={3*2**(p-2)}) ; J0={J0} ; Gamma_p(1)={G1} ; weight counts 4^p*P(p^J | W), J=1..8: {[cnt[J] for J in range(1, 9)]}")

print("== 3. theta_2 = log2(3)/4 from the series of T3a Theorem 3")
# f_2(j) = log2(1+Gamma_2(j+1)); Gamma_2(1)=0, Gamma_2(J)=(3/2)2^J/4-1 for J>=2  => f_2(0)=0, f_2(j)=j+1+log2(3/8) for j>=1
F = sum((1 - 0.5) * 2.0 ** (-j) * (0 if j == 0 else (j + 1 + log2(3 / 8))) for j in range(200))
print(f"  theta_2 = {0.5*F:.12f} ; log2(3)/4 = {log2(3)/4:.12f}")

print("== 4. Legendre values for the p=19 bound")
for D_ in (8, 9):
    N = 19 ** D_ - 1
    print(f"  v_19((19^{D_}-1)!) = {vfact(N, 19)}")

print("== 5. T1b Lemma 2.2: simple zero x_c of 1+pi_1+pi_2+pi_{c+2} with v(x_c+2)=v(c!)")
def F_val(x, c):
    return 1 + (x + 1) + (x + 1) * (x + 2) + prod(x + i for i in range(1, c + 3))
def F_der(x, c, mod):
    # derivative of the polynomial at x, mod 'mod' (product rule, exact)
    terms = [x + i for i in range(1, c + 3)]
    d = 0
    for i in range(len(terms)):
        d += prod(terms[:i] + terms[i + 1:])
    return (1 + (2 * x + 3) + d) % mod
for p, c in [(3, 6), (3, 7), (3, 9), (5, 10), (5, 12), (7, 14)]:
    Nn = 60; mod = p ** Nn
    # direct Newton on H(y) = y + (y-1) pi_c(y)
    def H(y): return y + (y - 1) * prod(y + i for i in range(1, c + 1))
    def Hd(y):
        ts = [y + i for i in range(1, c + 1)]
        d = sum(prod(ts[:i] + ts[i + 1:]) for i in range(len(ts)))
        return 1 + prod(ts) + (y - 1) * d
    y = 0
    for _ in range(200):
        hy = H(y) % mod
        if hy == 0:
            break
        y = (y - hy * pow(Hd(y) % mod, -1, mod)) % mod
    xc = (y - 2) % mod
    ok = F_val(xc, c) % mod == 0
    print(f"  p={p} c={c}: v(y_c)={vp(y, p)} v(c!)={vfact(c, p)} F(x_c)=0 mod p^{Nn}: {ok} ; v(F'(x_c))={vp(F_der(xc, c, mod), p)} (= v(y_c) expected)")

print("== 6. T4 Lemma 3: geometric mean over units xi of prod_{r<p}|cos(pi xi r!/p)| equals 2^-p")
for p in (3, 5, 7, 11, 13, 17):
    s = 0.0
    for xi in range(1, p):
        s += sum(log(abs(cos(pi * ((xi * prod(range(1, r + 1))) % p) / p))) for r in range(p))  # reduce mod p before floating point
    print(f"  p={p}: geometric mean * 2^p = {2**p * 2.718281828459045 ** (s/(p-1)):.12f}")

print("== 7. T4 Proposition 2: N_G(x) = 2^(M_G-1) on x = -2 mod p^G (brute force over subsets)")
for p, G in [(2, 6), (3, 3), (5, 2), (7, 2)]:
    MG = max(b for b in range(1, p * G + 1) if vfact(b, p) < G)
    x = (-2) % p ** G
    pis = [prod((x + i) for i in range(1, b + 1)) for b in range(0, MG + 1)]
    cntN = sum(1 for B in product((0, 1), repeat=MG) if (1 + sum(pis[b + 1] for b in range(MG) if B[b])) % p ** G == 0)
    print(f"  p={p} G={G}: M_G={MG}  N_G(-2)={cntN}  2^(M_G-1)={2**(MG-1)}")

print("== 8. Kitamura's exact table vs T4 capped g_2 (value column is f(a,2) = v_2(a!) + g_2(a))")
import csv, re, os, sys
base = os.environ.get("T4DIR")
if base and os.path.exists(base + "/kitamura/p2_exact_table_1_256.csv"):
    g = {}
    for l in open(base + "/data/surv_cap4094.txt"):
        m = re.match(r"\s*(\d+)\s+(-?\d+)", l)
        if m:
            g[int(m[1])] = int(m[2])
    kit = {int(r["a"]): int(r["value"]) for r in csv.DictReader(open(base + "/kitamura/p2_exact_table_1_256.csv"))}
    mm = [a for a in range(1, 257) if min(kit[a] - vfact(a, 2), 4094) != g[a]]
    print(f"  rows {len(kit)}; mismatches after conversion f->g: {mm}")
else:
    print("  skipped (set T4DIR to the T4-computations directory containing kitamura/ and data/)")
