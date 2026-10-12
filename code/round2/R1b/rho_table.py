"""Exact table of the rank-one window operator's weight vector rho(s) = 2^lam * P_f(Q_f == s mod 2^lam),
Q_f = sum_{i<2 lam} f_i (y+1)...(y+i), y = x + n, as a function of y mod 2^(lam+?) (it depends on y mod 2^lam
only through the products; we tabulate y mod 2^(2*lam+1) and print the distinct vectors)."""
import sys
from fractions import Fraction
for lam in (1, 2, 3, 4):
    mod = 1 << lam
    vecs = {}
    for y in range(1 << (lam + 1)):
        terms = []; prod = 1
        for i in range(2 * lam):
            terms.append(prod % mod); prod = prod * (y + i + 1) % mod
        cnt = [0] * mod
        for f in range(1 << len(terms)):
            cnt[sum(terms[i] for i in range(len(terms)) if (f >> i) & 1) % mod] += 1
        vec = tuple(Fraction(c * mod, 1 << len(terms)) for c in cnt)
        vecs.setdefault(vec, []).append(y)
    print(f"lambda={lam}: {len(vecs)} distinct rho-vectors over y mod {1 << (lam+1)}")
    for vec, ys in vecs.items():
        print("   rho =", [str(v) for v in vec], " for y in", ys[:8], "..." if len(ys) > 8 else "")
