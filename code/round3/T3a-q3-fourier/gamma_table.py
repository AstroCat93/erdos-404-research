#!/usr/bin/env python3
"""gamma_table.py -- exact Gamma_p(J) = p^J cnt(J)/4^p - 1 as fractions (from data/gamma_enum.txt), up to the first J0
with cnt(J0) = weight(W=0); cross-checks against data/gamma_exact.txt (previous instance, independent Python DP).
Writes data/gamma_table.txt."""
import os, re
from fractions import Fraction
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
D = {}
for line in open(os.path.join(BASE, 'data', 'gamma_enum.txt')):
    m = re.match(r'p=(\d+)\s+Sigma_p=(\d+)\s+total_weight=4\^p=(\d+)\s+weight\(W=0\)=(\d+)', line)
    if m: D[int(m.group(1))] = dict(Sig=int(m.group(2)), tot=int(m.group(3)), W0=int(m.group(4)), J={})
    m = re.match(r'p=(\d+) J=(\d+)\s+p\^J=(\d+)\s+cnt=(\d+)\s+dist=(\d+)', line)
    if m: D[int(m.group(1))]['J'][int(m.group(2))] = (int(m.group(4)), int(m.group(5)))
prev = {}
fn = os.path.join(BASE, 'data', 'gamma_exact.txt')
if os.path.exists(fn):
    for line in open(fn):
        m = re.match(r'p=(\d+) J=(\d+)\s+Gamma_p\(J\)=(\S+)', line)
        if m: prev[(int(m.group(1)), int(m.group(2)))] = Fraction(m.group(3))
out = []
for p in sorted(D):
    d = D[p]; s = []
    assert Fraction(d['W0'], d['tot']) == Fraction(3, 2 ** (p + 1)), p
    for J in sorted(d['J']):
        cnt, dist = d['J'][J]
        G = Fraction(p ** J * cnt, d['tot']) - 1
        chk = prev.get((p, J))
        flag = '' if chk is None else (' [=prev]' if chk == G else ' [MISMATCH prev %s]' % chk)
        s.append('J=%d: Gamma=%s (%.6e), dist=%d%s' % (J, G, float(G), dist, flag))
        if cnt == d['W0']:
            s.append('  -> for all J>=%d: Gamma_p(J) = (3/2) p^J 2^-p - 1, dist = 3*2^(p-2) = %d' % (J, 3 * 2 ** (p - 2)) if dist == 3 * 2 ** (p - 2) else '  -> cnt closed form from J=%d (dist not yet saturated)' % J)
            if dist == 3 * 2 ** (p - 2): break
    out.append('p=%d (Sigma_p=%d, weight(W=0)/4^p = 3/2^(p+1)):\n  ' % (p, d['Sig']) + '\n  '.join(s))
txt = '\n'.join(out); print(txt)
open(os.path.join(BASE, 'data', 'gamma_table.txt'), 'w').write(txt + '\n')
