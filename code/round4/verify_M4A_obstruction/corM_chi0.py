"""corM_chi0.py -- the first-window chi^2 on the atoms of M4A's Corollary M', bracketed exactly:

    p P(S == 0 mod p) - 1   <=   chi^2_0   <=   M4A's Prop D bound,     and  chi^2_0 >= (p-1) 4^-p  (Prop 11.12).

chi^2_W = p^D Coll_D - 1, Coll_j = P(S == 0 mod p^j), S = sum_{c<H} delta_c y_c, y_c = (x+n+1)...(x+n+c),
delta i.i.d. signed, W = W_0 = [300, 405).  The lower bound is the mod-p level of the Fourier sum
chi^2 = sum_{xi != 0} |mu^(xi)|^2 (the terms with xi in p^(D-1) Z / p^D Z), i.e. Prop 11.12's mechanism.
When p^D <= 3e5 (only p = 23 here) chi^2_0 itself is computed exactly.  The values depend only on
x mod p^(D + M_W), hence are constant on A (D_0 + M_405 <= m is asserted).
Exact: integer weights (total 4^H) as Python ints in numpy object arrays.

Usage: python3 corM_chi0.py ATOMFILE PROPD_BOUND
"""
import os
import sys
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vo_lib import vp  # noqa: E402


def law(ys, mod):
    cnt = np.zeros(mod, dtype=object)
    cnt[0] = 1
    for y in ys:
        a = y % mod
        cnt = 4 * cnt if a == 0 else 2 * cnt + np.roll(cnt, a) + np.roll(cnt, -a)
    return cnt


def main():
    kv = dict(line.split('=', 1) for line in open(sys.argv[1]).read().split() if '=' in line)
    p, n0, xA, m = int(kv['p']), int(kv['n0']), int(kv['xA']), int(kv['m'])
    bound = Fraction(sys.argv[2])
    n, N = n0, -(-27 * n0 // 20)
    dep = [vp(xA + i, p) for i in range(n + 1, N + 1)]
    D, MW = sum(dep), max(dep)
    assert D + MW <= m
    H = N - n
    tot = 4 ** H
    ys, y = [], 1
    for c in range(H):
        ys.append(y)
        y *= xA + n + c + 1
    first_gate = next(i for i in range(1, H + 1) if dep[i - 1] > 0)
    c1 = law(ys, p)
    lowp = p * Fraction(int(c1[0]), tot) - 1
    floor = Fraction(p - 1, 4 ** p)
    print(f"p={p} W_0=[{n},{N}) H={H} D_0={D} M_W={MW}; first gate at n+{first_gate} (depth {dep[first_gate - 1]})")
    print(f"   exact mod-p level  p P(S == 0 mod p) - 1 = {float(lowp):.7g}   (lower bound for chi^2_0)")
    print(f"   Prop 11.12 floor (p-1)4^-p = {float(floor):.4g} <= mod-p level: {floor <= lowp}")
    print(f"   M4A's Prop D bound {float(bound):.7g} >= mod-p level: {bound >= lowp};  ratio = {float(lowp / bound):.5f}")
    if p ** D <= 3 * 10 ** 5:
        cD = law(ys, p ** D)
        assert sum(cD) == tot
        chi2 = p ** D * Fraction(int(cD[0]), tot) - 1
        print(f"   exact chi^2_0 = {float(chi2):.7g}:  mod-p level <= chi^2_0 <= Prop D: {lowp <= chi2 <= bound};  "
              f"chi^2_0 / Prop D = {float(chi2 / bound):.4f}")


if __name__ == '__main__':
    main()
