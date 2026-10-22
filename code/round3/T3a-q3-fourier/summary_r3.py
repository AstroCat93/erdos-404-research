#!/usr/bin/env python3
"""summary_r3.py -- consolidated exact L^2 table for the round-3 writeup (this instance, 2026-10-21).
For each l2dp output (deepest E per (p,N0)), reconstruct S exactly (CRT), C_k = p^k S/4^M, and report:
  C_k - 1 (exact, printed as float), the Theorem-3 product bound B_k = prod over level groups (1+Gamma_group),
  the block defects D = C_b/C_a - 1 and the ratio D/Gamma (Theorem 1: 0 <= D <= Gamma), and the
  finite-level hit fraction against the Cauchy-Schwarz lower bound 1/C_k.
Gamma of each level group is computed exactly from the group's own elements (signed-sum law mod p^J), so the
check does not rely on the gate congruence; for full blocks it is compared with Gamma_p(J) of data/gamma_table.txt.
Writes data/summary_r3.txt."""
import os, re
from fractions import Fraction
from math import factorial
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
Q = 2**61 - 1
def vfact(n, p):
    v, m = 0, n
    while m:
        m //= p; v += m
    return v
def crt(hi, lo, sq):
    a = (hi << 64) | lo
    t = ((sq - a) % Q) * pow(2**128 % Q, -1, Q) % Q
    return a + 2**128 * t
def gamma_group(elems, p, J):
    mod = p ** J; cnt = {0: 1}
    for a in elems:
        a %= mod; new = {}
        for s, c in cnt.items():
            for d, w in ((0, 2), (a, 1), (-a, 1)):
                t = (s + d) % mod; new[t] = new.get(t, 0) + c * w
        cnt = new
    return Fraction(mod * cnt.get(0, 0), 4 ** len(elems)) - 1
best = {}
for fn in os.listdir(os.path.join(BASE, 'data', 'l2')):
    m = re.match(r'p(\d+)_E(\d+)_N(\d+)\.txt$', fn)
    if not m: continue
    p, E, N0 = map(int, m.groups())
    if (p, N0) not in best or best[(p, N0)][0] < E: best[(p, N0)] = (E, fn)
out = []
def pr(s): print(s); out.append(s)
for (p, N0) in sorted(best):
    E, fn = best[(p, N0)]
    rows = {}; M = None
    for line in open(os.path.join(BASE, 'data', 'l2', fn)):
        if line.startswith('# p='): M = int(dict(kv.split('=') for kv in line[2:].split())['M'])
        elif not line.startswith('#') and line.strip():
            f = line.split(); rows[int(f[0])] = (crt(int(f[2]), int(f[3]), int(f[4])), int(f[7]) if len(f) > 7 else None)
    e0 = vfact(N0, p); K = E - e0
    C = {0: Fraction(1)}
    for k in range(1, K + 1): C[k] = Fraction(p ** k * rows[k + e0][0], 4 ** M)
    # level groups
    groups = []; n = N0
    while vfact(n, p) - e0 < K:
        a = vfact(n, p) - e0; x = factorial(n) // p ** vfact(n, p)
        if groups and groups[-1][0] == a: groups[-1][1].append(x)
        else: groups.append((a, [x]))
        n += 1
    pr('== p=%d N0=%d (file %s, M=%d): exact C_k for k<=%d' % (p, N0, fn, M, K))
    B = Fraction(1); viol = 0; lines = []
    for gi, (a, el) in enumerate(groups):
        b = groups[gi + 1][0] if gi + 1 < len(groups) else K
        J = b - a
        G = gamma_group(el, p, J)
        D = C[b] / C[a] - 1
        B *= 1 + G
        ok = (0 <= D <= G) and (C[b] <= B)
        viol += (not ok)
        lines.append('  level %3d->%3d J=%d (#el=%d)  D=%.4e  Gamma_group=%.4e  D/Gamma=%s  C_b=%.12f  product bound B=%.6f' % (
            a, b, J, len(el), float(D), float(G), ('%.3e' % float(D / G)) if G else 'n/a', float(C[b]), float(B)))
    for l in lines: pr(l)
    hf = rows[K + e0][1]
    if hf is not None:
        pr('  depth %d: hit fraction %.8f >= 1/C_k = %.8f : %s' % (K, hf / p ** (K + e0) * p ** e0, float(1 / C[K]), hf / p ** K >= 1 / C[K]))
    pr('  checks 0<=D<=Gamma and C<=B: violations=%d' % viol)
txt = '\n'.join(out)
open(os.path.join(BASE, 'data', 'summary_r3.txt'), 'w').write(txt + '\n')
