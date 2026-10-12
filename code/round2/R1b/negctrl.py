"""Negative controls for the window identity: (a) replace rho by 1 (drop the frozen-state weight);
(b) use rho but with the WRONG parity of the tail (shift tau by 1).  Both should FAIL on some parents
with lambda >= 2, showing the exact check in mart_check2.py is not vacuous."""
import random, sys
from fractions import Fraction
from collections import defaultdict
import mart_check2 as mc
rnd = random.Random(int(sys.argv[1])); n, N, P = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
fails_a = fails_b = tot = 0; done = 0
while done < int(sys.argv[5]):
    x = rnd.getrandbits(P) & ~1
    m = mc.V(x, n); D = mc.V(x, N) - m
    if D > 10 or D < 1: continue
    parents = mc.alive_paths(x, n, P)
    info = {}
    for e in parents:
        tau, lam = mc.tau_of(e, x, n, P)
        if 2 <= lam <= D: info[e] = (lam, tau)
    if not info: continue
    done += 1
    x0 = x % (1 << m); rest = x >> (m + D)
    acc_a = defaultdict(Fraction); acc_b = defaultdict(Fraction)
    for w in range(1 << D):
        xw = x0 + (w << m) + (rest << (m + D))
        for c in mc.alive_paths(xw, N, P):
            e = c & ((1 << n) - 1)
            if e in info:
                lam, _ = info[e]
                tauN, _ = mc.tau_of(c, xw, N, P)
                acc_a[e] += 1
                acc_b[e] += mc.rho(xw, N, lam, tauN + 1)
    WnN = (N - mc.V(x, N)) - (n - m)
    for e, (lam, tau) in info.items():
        tot += 1
        rhs_a = Fraction(2) ** WnN * 1
        rhs_b = Fraction(2) ** WnN * mc.rho(x, n, lam, tau)
        fails_a += (acc_a[e] / (1 << D) != rhs_a)
        fails_b += (acc_b[e] / (1 << D) != rhs_b)
print(f"parents with lambda>=2: {tot}; control (a) rho:=1 fails on {fails_a}; control (b) shifted state fails on {fails_b}")
