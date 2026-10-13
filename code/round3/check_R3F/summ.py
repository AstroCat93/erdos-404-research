"""summ.py -- summaries of the check_R3F logs (check of R3F, round 3).
Printed shell bounds (15 significant digits) are widened outward by a relative 1e-14 before use.
 (A5)  per-level upper bounds of rho_d = S_d/(N_d (2/pi)^p) from shellchk; J_p enclosures (i) from jcheck.py
       (carry recursion) and (ii) from the grid identity  J_p = (pi/2)^p (1 + sum_{d<=D} S_d)/p^D - E'(p^D),
       |E'(M)| <= (pi^2/3) alpha_{p-1}/M^2  (Theorem A4(i),(iii)); analytic tail rho_d <= J^+ + dev_d,
       dev_d = (pi^2/3) alpha_{p-1} (p^-d + p^-(d-1))/N_d (decreasing in d); certified sup_d rho_d.
 (e)   totals of the tail shells T_13(k), k <= 7 and T_11(k), k <= 8; D3 sums  sum_k sqrt(N_k Q(k)).
 (B4)  factorial-measure shells and ratios to N_d (2/pi)^{U_d}.
usage: python3 -I summ.py LOGDIR
"""
import os
import re
import sys

import mpmath
from mpmath import iv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jcheck import constants  # noqa: E402

iv.dps = 30
mpmath.mp.dps = 30
W = mpmath.mpf('1e-14')
pat = re.compile(r'^(gate|tail|fact) p=(\d+) N0=(\S+) k=(\d+) n=(\d+)\s+S1 in \[(\S+), (\S+)\]\s+S2 in \[(\S+), (\S+)\]')


def read(logdir, fname):
    out = {}
    with open(os.path.join(logdir, fname)) as f:
        for line in f:
            m = pat.match(line)
            if m:
                k = int(m.group(4))
                out[k] = dict(n=int(m.group(5)), S1=(mpmath.mpf(m.group(6)) * (1 - W), mpmath.mpf(m.group(7)) * (1 + W)),
                              S2=(mpmath.mpf(m.group(8)) * (1 - W), mpmath.mpf(m.group(9)) * (1 + W)))
    return out


def jlog(logdir):
    J = {}
    fn = os.path.join(logdir, 'a_jcheck_C10000.log')
    if os.path.exists(fn):
        for line in open(fn):
            m = re.match(r'p=(\d+) C=\d+: .*J_p in \[(\S+), (\S+)\]', line)
            if m:
                J[int(m.group(1))] = (mpmath.mpf(m.group(2)) - mpmath.mpf('1e-9'), mpmath.mpf(m.group(3)) + mpmath.mpf('1e-9'))  # widen printed digits
    return J


def main():
    d = sys.argv[1]
    alpha, beta, kap = constants(14)
    twopi_lo = mpmath.mpf((iv.mpf(2) / iv.pi).a)
    pihalf = iv.pi / 2
    Jc = jlog(d)
    print('# (A5) certified upper bounds of rho_d (shellchk), J_p enclosures, analytic tail, sup')
    for p, fn in ((5, 'a_gate_p5_d1-10.log'), (7, 'a_gate_p7_d1-9.log'), (11, 'a_gate_p11_d1-9.log'), (13, 'a_gate_p13_d1-8.log')):
        g = read(d, fn)
        if p == 13 and os.path.exists(os.path.join(d, 'a_gate_p13_d9.log')):
            g.update(read(d, 'a_gate_p13_d9.log'))
        D = max(g)
        rho = {}
        for k in sorted(g):
            N = p ** k - p ** (k - 1)
            rho[k] = g[k]['S1'][1] / (N * twopi_lo ** p)
        a = mpmath.mpf(alpha[p - 1].b)
        K = mpmath.mpf((iv.pi ** 2 / 3).b)
        E = K * a / mpmath.mpf(p) ** (2 * D)
        tot_lo = 1 + mpmath.fsum(g[k]['S1'][0] for k in g)
        tot_hi = 1 + mpmath.fsum(g[k]['S1'][1] for k in g)
        Jg = (mpmath.mpf((pihalf ** p).a) * tot_lo / mpmath.mpf(p) ** D - E,
              mpmath.mpf((pihalf ** p).b) * tot_hi / mpmath.mpf(p) ** D + E)
        print(f'p={p}: computed levels 1..{D};  rho_d upper: ' + ', '.join(f'd={k}: {mpmath.nstr(rho[k], 8)}' for k in sorted(rho)))
        print(f'   J_p (grid identity, D={D}, |E\'| <= {mpmath.nstr(E, 3)}): [{mpmath.nstr(Jg[0], 10)}, {mpmath.nstr(Jg[1], 10)}]'
              + (f';  J_p (carry recursion, jcheck C=1e4): [{mpmath.nstr(Jc[p][0], 10)}, {mpmath.nstr(Jc[p][1], 10)}]' if p in Jc else ''))
        cands = [x for x in (Jg if Jg[1] - Jg[0] < 0.5 else None, Jc.get(p)) if x is not None]
        Jhi = min(x[1] for x in cands)
        for d0 in (D, D - 1, D - 2):
            dev = K * a * (mpmath.mpf(p) ** (-(d0 + 1)) + mpmath.mpf(p) ** (-d0)) / (p ** (d0 + 1) - p ** d0)
            print(f'   analytic tail for d >= {d0 + 1}: rho_d <= J^+ + dev_{d0 + 1} = {mpmath.nstr(Jhi, 10)} + {mpmath.nstr(dev, 4)} = {mpmath.nstr(Jhi + dev, 8)}')
        dev = K * a * (mpmath.mpf(p) ** (-(D + 1)) + mpmath.mpf(p) ** (-D)) / (p ** (D + 1) - p ** D)
        sup = max(max(rho.values()), Jhi + dev)
        arg = max(rho, key=lambda k: rho[k])
        print(f'   CERTIFIED (this check): sup_d rho_d <= {mpmath.nstr(sup, 8)}  (max computed level d={arg})')
    print('\n# (e) tail shells of note 10.4.1 and D3 sums')
    for p, fn, K in ((13, 'e_tail_p13_k1-7.log', 7), (11, 'e_tail_p11_k1-8.log', 8)):
        g = read(d, fn)
        lo = mpmath.fsum(g[k]['S1'][0] for k in range(1, K + 1))
        hi = mpmath.fsum(g[k]['S1'][1] for k in range(1, K + 1))
        d3 = mpmath.fsum(mpmath.sqrt((p ** k - p ** (k - 1)) * g[k]['S2'][1]) for k in range(1, K + 1))
        print(f'p={p}: sum_(k<={K}) T(k) in [{mpmath.nstr(lo, 14)}, {mpmath.nstr(hi, 14)}];  D3: sum sqrt(N_k Q(k)) <= {mpmath.nstr(d3, 8)}')
        for k in range(1, K + 1):
            print(f'   k={k}: T in [{mpmath.nstr(g[k]["S1"][0], 13)}, {mpmath.nstr(g[k]["S1"][1], 13)}]  Q(k) <= {mpmath.nstr(g[k]["S2"][1], 8)}')
    print('\n# (B4-data) factorial-measure shells T_fact(d) (upper) and ratio to N_d (2/pi)^{U_d}')
    for p, fn in ((7, 'b4_fact_p7_d1-9.log'), (11, 'b4_fact_p11_d1-7.log'), (13, 'b4_fact_p13_d1-7.log')):
        g = read(d, fn)
        tot = mpmath.fsum(g[k]['S1'][1] for k in g)
        rnd = mpmath.fsum((p ** k - p ** (k - 1)) * mpmath.mpf((iv.mpf(2) / iv.pi).b) ** g[k]['n'] for k in g)
        cells = ', '.join(f'd={k}: {mpmath.nstr(g[k]["S1"][1], 4)} ({mpmath.nstr(g[k]["S1"][1] / ((p ** k - p ** (k - 1)) * twopi_lo ** g[k]["n"]), 3)})' for k in sorted(g))
        print(f'p={p}: {cells};  total <= {mpmath.nstr(tot, 6)}  random total = {mpmath.nstr(rnd, 6)}')


if __name__ == '__main__':
    main()
