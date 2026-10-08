"""Sanity checks for Theorems (frozen lower bound, dichotomy/Hensel construction, cube multiplicity)."""
import math, sys, itertools
sys.path.insert(0, '.')
from e404lib import frozen_set
import sympy as sp
# (1) lower bound: j in {0} U [2,inf) with e*j! < p  =>  p-1-j frozen
bad = 0; n = 0
for line in open('../data/frozen_upto30000.txt'):
    head, js = line.split(':'); p = int(head.split()[0]); js = set(int(x) for x in js.split())
    for j in [0] + list(range(2, 20)):
        if math.e * math.factorial(j) < p and j <= p - 1:
            n += 1
            if j not in js: bad += 1; print("LB FAIL", p, j)
print("(1) frozen lower bound checks:", n, "failures:", bad)
# (2) dichotomy: for r not frozen, T0 subset [0,k*-1] with P(r)=0 mod p, and T in {T0, T0+{k*}} with P'(r) != 0 mod p
x = sp.symbols('x')
def rising(k): 
    e = sp.Integer(1)
    for i in range(1, k + 1): e *= (x + i)
    return sp.expand(e)
R = [rising(k) for k in range(0, 60)]
dR = [sp.diff(e, x) for e in R]
bad = 0; cnt = 0
for p in list(sp.primerange(2, 40)):
    Phi = frozen_set(p)
    for r in range(p):
        if r in Phi: continue
        ks = p - r if r >= 1 else p
        found = None
        for size in range(0, ks):
            for S in itertools.combinations(range(1, ks), size):
                T0 = (0,) + S
                if sum(R[k].subs(x, r) for k in T0) % p == 0:
                    found = T0; break
            if found: break
        assert found is not None
        T = found if sum(dR[k].subs(x, r) for k in found) % p != 0 else found + (ks,)
        ok = sum(R[k].subs(x, r) for k in T) % p == 0 and sum(dR[k].subs(x, r) for k in T) % p != 0
        cnt += 1
        if not ok: bad += 1; print("DICHOTOMY FAIL", p, r, T)
print("(2) dichotomy/Hensel construction checks:", cnt, "failures:", bad)
# (3) multiplicity of (x+2) in P_T for all T subset [0,10] with 0 in T
best = 0; arg = None
y = sp.symbols('y')
for mask in range(1 << 10):
    T = [0] + [k for k in range(1, 11) if mask >> (k - 1) & 1]
    P = sp.Poly(sum(R[k] for k in T), x)
    m = 0
    while P.eval(-2) == 0:
        P = sp.Poly(sp.quo(P.as_expr(), x + 2), x); m += 1
    if m > best: best, arg = m, T
print("(3) max multiplicity of root -2 over T subset [0,10]:", best, "attained at", arg)
