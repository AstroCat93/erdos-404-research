#!/usr/bin/env python3
"""summarize_e.py -- certified table for target (e) from the ivshell (I1, two builds) and shells_mpfr (I2) logs.

Per shell k: I1 enclosure [lo, hi] (both builds must print identical numbers; checked), I2 upper bound,
certified upper = max(I1 hi, I2 hi) rounded up by one unit in the 13th significant digit (printed values are
rounded to nearest at 13 digits), certified lower = I1 lo rounded down likewise.  Cumulative sums in exact rationals.
usage: summarize_e.py DATA_DIR p kmax
"""
import sys, re
from fractions import Fraction
from decimal import Decimal, getcontext, ROUND_FLOOR, ROUND_CEILING


def fmt(q, mode, digits=12):
    """decimal string of the rational q rounded down (mode='dn') or up ('up') to `digits` significant digits"""
    getcontext().prec = 60
    x = Decimal(q.numerator) / Decimal(q.denominator)
    e = x.adjusted()
    quant = Decimal(1).scaleb(e - digits + 1)
    return str(x.quantize(quant, rounding=ROUND_FLOOR if mode == 'dn' else ROUND_CEILING))


def dec(x):
    m, e = x.lower().split('e')
    return Fraction(m) * Fraction(10) ** int(e), Fraction(1, 10 ** 12) * Fraction(10) ** int(e)


def read_iv(path):
    out = {}
    for line in open(path):
        if line.startswith('#') or not line.strip():
            continue
        w = line.split()
        out[int(w[0])] = (w[1], w[2], w[3], w[4])
    return out


def read_mpfr(path):
    out = {}
    for line in open(path):
        m = re.match(r"k=\s*(\d+) .*T1_upper=([0-9.e+-]+)", line)
        if m:
            out[int(m.group(1))] = m.group(2)
    return out


def main():
    D, p, kmax = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    g = read_iv(f"{D}/e_ivshell_gcc_p{p}_k{kmax}.log")
    c = read_iv(f"{D}/e_ivshell_clang_p{p}_k{kmax}.log")
    mp = read_mpfr(f"{D}/e_mpfr_p{p}_k{kmax}.log")
    assert g == c, "gcc and clang builds differ"
    cl, cu = Fraction(0), Fraction(0)
    print(f"# p={p}: shells T_{p}(k) of the tail measure from N0={p}")
    print("# k  I1 lower (rounded down)   I1 upper   I2 upper   certified upper (rounded up)   rel.width(I1)")
    for k in range(1, kmax + 1):
        lo, ulo = dec(g[k][0]); hi, uhi = dec(g[k][1]); m2, um = dec(mp[k])
        L = lo - ulo
        U = max(hi + uhi, m2 + um)
        cl += L; cu += U
        print(f"{k:2d}  {fmt(L,'dn')}  {g[k][1]}  {mp[k]}  {fmt(U,'up')}  {float((hi-lo)/hi):.1e}")
    print(f"SUM k<={kmax}:  certified enclosure [{fmt(cl,'dn')}, {fmt(cu,'up')}]")


if __name__ == "__main__":
    main()
