#!/usr/bin/env python3
"""Independent exact verifier for the bounds printed by bounds.py (shares no code with it).
Parses the lines 'K=... delta<=... C0=...(ns=..,k=..,m1=..) ... C14=...(M*=..,Mf=..,chain=[..],ns=..,k=..,m1=..,...)'
and recomputes every term of Theorems A and B of the R3Q report from scratch:
  beta(n) via Legendre's formula for v(n!) and floor(log2 n) by halving; residue counts by explicit
  arithmetic-progression formulas checked against brute force for small ranges; binomial tails with gmpy2;
  all window hypotheses (W1)-(W3) and parameter constraints are re-checked.  Prints the recomputed total
  as an exact rational's log2 and the ratio to the logged value.
usage: verify_bounds.py logfile"""
import re, sys, math, gmpy2
from fractions import Fraction as F
def vfact(n):
    t, q = 0, n
    while q: q //= 2; t += q
    return t
def lg(n):
    c = 0
    while n > 1: n //= 2; c += 1
    return c
def bet(n): return vfact(n) - lg(n)            # n - s(n) - floor(log2 n)
def digsum(n): return n - vfact(n)
def zz(n): return -(-n // 2) - 1
def ap_count(lo, hi, c, mod):                   # #{lo <= i <= hi : i == c (mod mod)}
    if hi < lo: return 0
    first = lo + ((c - lo) % mod)
    return 0 if first > hi else (hi - first) // mod + 1
def tail(Kt, k):                                # P(Bin(Kt,1/2) <= k-1)
    if k <= 0: return F(0)
    if Kt <= 0: return F(1)
    return F(int(sum(gmpy2.bincoef(Kt, i) for i in range(0, min(k, Kt + 1)))), 2 ** Kt)
def m_one(r, a, i, b):
    if b <= 0: return F(1, 2 ** a)
    if b <= a: return F(1, 2 ** a) if (r + i) % 2 ** b == 0 else F(0)
    return F(1, 2 ** b) if (r + i) % 2 ** a == 0 else F(0)
def m_fail(r, a, lo, hi, lam):
    tot = F(0); i = lo; stop = lo + 2500
    while i <= hi and i < stop:
        tot += m_one(r, a, i, bet(i - 1) - lam + 1); i += 1
    if i <= hi:   # geometric tail: 2^{-(bet(t-1)-lam+1)} <= 2^{lam+1} (t-1)^2 2^{-t}, consecutive ratio <= 0.51
        assert i >= 100
        tot += F(41, 20) * (i - 1) ** 2 * F(2) ** (lam + 1 - i)
    return tot
def t5(muC, a, lowb, Kt, k, m1, lr, zs):
    if m1 == 0: return muC * (tail(Kt - a, k - lowb) + F(2) ** (1 - k + lr + zs))
    assert m1 >= a
    return muC * (tail(Kt - m1, k) + F(2) ** (1 - k + lr + zs - lowb) * F(3, 4) ** (m1 - a))
def lrm(lam): return -lg(2 * lam)
def thmA(G, KG, name, ns, k, m1):
    r, a, lam, nC = {"C0": (0, 3, 1, 6), "C2": (2, 4, 3, 8), "C6": (6, 4, 3, 10)}[name]
    T = G - 2 * KG - 12; assert ns >= nC and bet(ns) >= lam + 1
    assert m1 == 0 or a <= m1 <= ns - digsum(ns)
    Kt = lg(T - ns - 2 * lam); assert ns + 2 ** Kt + 2 * lam <= T
    lr = 0 if lam == 1 else (lam - 1) - lrm(lam)
    A1 = ap_count(1, T, (-r) % 2 ** a, 2 ** a) * F(1, 2 ** (G - T + 3))
    A4 = m_fail(r, a, ns + 1, T, lam)
    A5 = t5(F(1, 2 ** a), a, digsum((r + ns) % 2 ** a), Kt, k, m1, lr, zz(ns))
    return min(A1 + A4 + A5, F(1, 2 ** a))
def thmB(G, KG, Ms, Mf, ch, ns, k, m1):
    r, a = 14, 4; T = G - 2 * KG - 12; nU = ch[-1]; Lam = bet(nU) - 1
    for n, N in zip(ch, ch[1:]):
        assert N > n and bet(n) >= 2 * Ms + 1 and (N - n) + 2 * Ms <= bet(n) + 1 and bet(N) <= 2 * bet(n), (n, N)
    assert ns >= nU and bet(ns) >= Lam + 1 and Mf >= Ms and Ms + 1 > a and (m1 == 0 or a <= m1 <= ns - digsum(ns))
    Kt = lg(T - ns - 2 * Lam); assert ns + 2 ** Kt + 2 * Lam <= T
    B1 = ap_count(1, T, 2, 16) * F(1, 2 ** (G - T + 3))
    B2 = ap_count(1, nU, 2, 16) * F(1, 2 ** (Ms + 1)) + ap_count(nU + 1, ns + 2 * Lam, 2, 16) * F(1, 2 ** (Mf + 1))
    B3 = F(0)
    for J in range(4, Ms + 1):
        e = -J - 1 + zz(ch[0])
        for n, N in zip(ch, ch[1:]):
            L = N - n; e += L - (L - 1) // 2 - max(0, bet(N) - (n - 2) - 1 - J)
        B3 += F(2) ** e
    B4 = m_fail(r, a, ns + 1, T, Lam)
    lr = min(Lam - 1, -(-(Lam + Mf) // 2) - 1) - lrm(Lam)
    B5 = t5(F(1, 16), a, digsum((r + ns) % 16), Kt, k, m1, lr, zz(ns))
    return min(B1 + B2 + B3 + B4 + B5, F(1, 16))
def selftest():
    for lo in range(1, 40):
        for hi in range(lo - 1, 80):
            for mod in (8, 16):
                for c in range(mod):
                    assert ap_count(lo, hi, c, mod) == sum(1 for i in range(lo, hi + 1) if i % mod == c)
    for n in range(1, 3000): assert bet(n) == n - bin(n).count("1") - (n.bit_length() - 1)
    assert tail(10, 3) == F(1 + 10 + 45, 1024)
selftest()
for line in open(sys.argv[1]):
    if not line.startswith("K="): continue
    KG = int(re.match(r"K=(\d+)", line).group(1)); G = 2 ** KG
    logged = float(re.search(r"delta<=([0-9.e+-]+)", line).group(1))
    tot = F(0)
    for name in ("C0", "C2", "C6"):
        mm = re.search(name + r"=[0-9.e+-]+\(ns=(\d+),k=(\d+),m1=(\d+)\)", line)
        tot += thmA(G, KG, name, *map(int, mm.groups()))
    mm = re.search(r"C14=[0-9.e+-]+\(M\*=(\d+),Mf=(\d+),chain=\[([0-9, ]+)\],ns=(\d+),k=(\d+),m1=(\d+)", line)
    if mm:
        Ms, Mf = int(mm.group(1)), int(mm.group(2)); ch = [int(t) for t in mm.group(3).split(",")]
        tot += thmB(G, KG, Ms, Mf, ch, int(mm.group(4)), int(mm.group(5)), int(mm.group(6)))
    else: tot += F(1, 16)
    l2 = math.log2(tot.numerator) - math.log2(tot.denominator)
    print(f"K={KG}: recomputed delta bound = 2^{l2:.4f} = {2**l2:.6e}; logged {logged:.4e}; ratio {2**l2/logged:.6f}")
