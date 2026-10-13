#!/usr/bin/env python3
"""summarize_a.py -- certified per-level ratios for single gate blocks (round 3, R3F, target (a)).

Reads   data/round3/R3F/a_gate_ivshell_p{p}_d*.log   (ivshell file mode: interval enclosures of S_d)
        data/round3/R3F/a_gate_d_p{p}.log            (gate_d: independent upper bounds of S_d)
        data/round3/R3F/a_jrel_p{p}_C10000.log       (jrel: enclosure of J_p)
and prints, for each d, the certified upper bound of rho_d = S_d / (N_d (2/pi)^p) (the larger of the two programs'
upper bounds is used; it is a valid upper bound as soon as either program is correct), the
analytic bound J_p^+ + dev_d (Theorem A4(iii), alias_bound.py) for d beyond the computed range, and the resulting
certified sup_d rho_d.
Printed decimals of S_d upper bounds are rounded up by one unit in the 13th significant digit before use.
usage: summarize_a.py DATA_DIR p d_exact_max d_analytic_from
"""
import sys, re, glob, math
from fractions import Fraction
from mpmath import iv, mpf
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from alias_bound import bounds

iv.prec = 120


def up13(x_str):
    """rational upper bound for a %.12e-printed nonnegative decimal (add one unit in the last place)"""
    m, e = x_str.lower().split('e')
    q = Fraction(m) * Fraction(10) ** int(e)
    ulp = Fraction(1, 10 ** 12) * Fraction(10) ** int(e)
    return q + ulp


def main():
    D, p, dex, dan = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    Sup = {}
    partial = {}   # d -> {t0: upper bound}  (chunked runs: lowest digit u_0 = t0 only)
    for f in glob.glob(f"{D}/a_gate_ivshell_p{p}_d*.log"):
        lines = open(f).read().splitlines()
        m = [re.search(r"PARTIAL RUN: shells (\d+)\.\.(\d+), lowest digit u_0 in \[(\d+),(\d+)\]", l) for l in lines]
        m = [x for x in m if x]
        for line in lines:
            if line.startswith('#') or not line.strip():
                continue
            w = line.split()
            d = int(w[0]); hi = up13(w[2])
            if m:
                lo_t, hi_t = int(m[0].group(3)), int(m[0].group(4))
                assert lo_t == hi_t
                partial.setdefault(d, {})[lo_t] = hi
            else:
                Sup.setdefault(d, []).append(('ivshell', hi))
    for d, ch in partial.items():
        if sorted(ch) == list(range(1, (p - 1) // 2 + 1)):
            Sup.setdefault(d, []).append(('ivshell(chunks)', sum(ch.values())))
        else:
            print(f"# warning: incomplete chunk set for d={d}: {sorted(ch)}")
    for f in glob.glob(f"{D}/a_gate_d_p{p}.log"):
        for line in open(f):
            m = re.search(r"d=(\d+) .*S_d_upper=([0-9.e+-]+)", line)
            if m:
                Sup.setdefault(int(m.group(1)), []).append(('gate_d', up13(m.group(2))))
    J = None
    for f in glob.glob(f"{D}/a_jrel_p{p}_C*.log"):
        for line in open(f):
            m = re.search(r"J_p in \[([0-9.]+), ([0-9.]+)\]", line)
            if m:
                J = (Fraction(m.group(1)), Fraction(m.group(2)) + Fraction(1, 10 ** 10))
    rm = (2 / iv.pi) ** p                 # interval enclosure of (2/pi)^p
    print(f"# p={p}: per-level certified upper bounds of rho_d = S_d/(N_d (2/pi)^p)")
    best = Fraction(0)
    for d in sorted(Sup):
        if d > dex:
            continue
        hi = max(v for (_, v) in Sup[d])
        N = p ** d - p ** (d - 1)
        r = (iv.mpf(hi.numerator) / hi.denominator) / (iv.mpf(N) * rm)
        progs = ",".join(sorted(set(s for (s, _) in Sup[d])))
        print(f"d={d:2d}  rho_d <= {float(r.b):.6f}   (programs: {progs})")
        best = max(best, Fraction(str(float(r.b))) + Fraction(1, 10 ** 6))
    if J is not None:
        alpha, beta = bounds(p)
        pi = iv.pi
        worst = mpf(0)
        for d in range(dan, dan + 60):
            M = iv.mpf(p) ** d
            E = lambda MM: pi ** 2 / 3 * alpha / MM ** 2
            N = iv.mpf(p) ** d - iv.mpf(p) ** (d - 1)
            dev = (iv.mpf(p) ** d * E(M) + iv.mpf(p) ** (d - 1) * E(M / p)) / N
            val = iv.mpf(J[1].numerator) / J[1].denominator + dev
            worst = max(worst, val.b)
        print(f"J_p in [{float(J[0]):.10f}, {float(J[1]):.10f}];  for all d >= {dan}: rho_d <= J_p^+ + dev_d <= {float(worst):.6f}  "
              f"(dev_d decreasing in d; maximum over d >= {dan} attained at d = {dan})")
        best = max(best, Fraction(str(float(worst))) + Fraction(1, 10 ** 6))
        missing = [d for d in range(1, dan) if d not in Sup or d > dex]
        print(f"levels covered by computation: 1..{dex}; analytic: >= {dan}; uncovered: {missing}")
        print(f"CERTIFIED: sup_d rho_d <= {float(best):.6f}" if not missing else "NOT all levels covered")


if __name__ == "__main__":
    main()
