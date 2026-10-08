"""Collect certified results into tables (reads the .out files produced by ecover / tau / win2 runs).

f(1,p) lower bounds:
  Theorem C  (single block):  L = L_p (Sigma(E_p) covers Z/p^L)  =>  f(1,p) >= p + p^2 + ... + p^L
  Theorem C' (+ two-block windows for gate levels L..J2, all t mod p certified FULL):
             f(1,p) >= e_{M*} + L,  M* = p^{J2+1} - 1,  e_M = M + v_p(M!).
Rigorous density lower bound for {a : f(a,p) < oo} from Theorem F with K in {1,3,...,p}
(disjoint residue classes mod p):  delta(p) >= sum over K with exact tau of p^{-(tau(K,p)+1)}.
"""
import re, glob, os
from core import e_block

here = os.path.dirname(os.path.abspath(__file__))
L, Lexact = {}, {}
for line in open(os.path.join(here, "ecover_table.out")).readlines() + open(os.path.join(here, "ecover_big.out")).readlines():
    m = re.match(r"p=(\d+) L=(\d+) p\^L=\d+ covered=\d+ (FULL|partial)", line)
    if m:
        p, l, st = int(m[1]), int(m[2]), m[3]
        if st == "FULL":
            L[p] = max(L.get(p, 0), l)
        else:
            Lexact[p] = True
LEV = {}
for fn in glob.glob(os.path.join(here, "win2*.out")):
    for line in open(fn):
        m = re.match(r"LEVEL p=(\d+) j=(\d+) : ALL t FULL", line)
        if m:
            LEV.setdefault(int(m[1]), set()).add(int(m[2]))
J2 = {}
for p in L:
    j = L[p]
    while j in LEV.get(p, set()):
        j += 1
    J2[p] = j - 1   # all gate levels L..J2 certified by two-block windows (J2 = L-1: none)

print("p | L_p | f(1,p) >= (Thm C) | J2 | f(1,p) >= (Thm C')")
for p in sorted(L):
    l = L[p]
    b1 = sum(p ** i for i in range(1, l + 1))
    tag = "" if Lexact.get(p) else "+"
    # J2 is only meaningful if levels L..J2 are all certified
    j2 = J2[p]
    b2 = e_block(p ** (j2 + 1) - 1, p) + l if j2 >= l else b1
    print("%3d | %d%s | %d | %d | %d" % (p, l, tag, b1, j2, b2))

print()
print("p | rigorous density lower bound for {a: f(a,p) < oo} (Theorem F, K<=p, exact tau only)")
for line in open(os.path.join(here, "tau_table.out")):
    m = re.match(r"p=(\d+) tau:(.*)\|", line)
    if not m:
        continue
    p = int(m[1])
    toks = m[2].split()
    dens = 0.0
    nzero = 0
    for k, t in enumerate(toks, start=1):
        if t == "*" or t.endswith("+"):
            continue
        dens += p ** (-(int(t) + 1))
        if int(t) == 0:
            nzero += 1
    print("%3d | %.6f | #{K<=p: tau=0} = %d" % (p, dens, nzero))
