#!/usr/bin/env python3
"""defect_table.py -- from the exact L^2 masses C_k (data/l2_summary.json) build
 (1) the block-defect table: for consecutive attained levels a -> b (J = b - a), D = C_b/C_a - 1 against the
     worst case Gamma_p(J) = p^J P(W == 0 mod p^J) - 1 (Theorem B), with the exact Gamma from gamma_exact.py;
 (2) the shell table T2(j) = C_j - C_{j-1} against the random model rm(j) = p^j (1-1/p) 2^{-m_j};
 (3) for p = 2: the random-model partial sums and the exponent of divergence.
Writes data/defect_table.txt.  Pure python, exact rationals for C and Gamma, floats for display.
"""
import json, os, sys
from fractions import Fraction
from math import factorial, log
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gamma_exact import gamma, pattern
from l2post import vfact

def main():
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    js = json.load(open(os.path.join(base, 'data', 'l2_summary.json')))
    out = []
    def pr(s):
        print(s); out.append(s)
    gcache = {}
    def G(p, J, first_partial=False):
        key = (p, J, first_partial)
        if key not in gcache:
            if first_partial:   # N0 = 1: the level-0 block is {1!,...,(p-1)!}
                gcache[key] = gamma(p, 1, [factorial(r) for r in range(1, p)])
            elif p == 2:
                gcache[key] = None  # gate congruence is for odd p only; computed per block below
            else:
                gcache[key] = gamma(p, J)
        return gcache[key]
    for key in sorted(js, key=lambda s: [int(x) for x in s[1:].replace('_N', ' ').split()]):
        d = js[key]; p, N0, e0, kmax = d['p'], d['N0'], d['e0'], d['kmax']
        Ck = {0: Fraction(1)}
        Ck.update({int(k): Fraction(v) for k, v in d['C_k'].items()})
        # attained levels and the elements of each level
        levels = {}
        n = N0
        while vfact(n, p) - e0 <= kmax:
            levels.setdefault(vfact(n, p) - e0, []).append(n); n += 1
        att = sorted(levels)
        pr("== p=%d N0=%d e0=%d depth %d : C_%d = %.10f" % (p, N0, e0, kmax, kmax, float(Ck[kmax])))
        pr("   block defects D = C_b/C_a - 1 between consecutive attained levels a->b (J=b-a), worst case Gamma_p(J):")
        for a, b in zip(att, att[1:]):
            if b > kmax: break
            J = b - a
            D = Ck[b] / Ck[a] - 1
            if p == 2:
                ys = [factorial(m) // p ** (e0 + a) for m in levels[a]]
                gam = gamma(p, J, ys)
                tag = "p=2 block %s" % levels[a]
            elif N0 == 1 and a == 0:
                gam = G(p, 1, True); tag = "partial first block"
            else:
                gam = G(p, J); tag = "gate level %d" % (J - 1) if J > 1 else "non-gate"
            pr("   %3d->%3d J=%d  D=%.6e  Gamma=%.6e  D/Gamma=%.3e  [%s, elements %d..%d]" % (
                a, b, J, float(D), float(gam), float(D / gam) if gam else float('nan'), tag, levels[a][0], levels[a][-1]))
        pr("   shells T2(j) = C_j - C_{j-1} vs random model rm(j) = p^j (1-1/p) 2^-m_j  (m_j = #elements with v<j):")
        rmsum = 0.0
        for j in range(1, kmax + 1):
            mj = sum(len(levels[a]) for a in att if a < j)
            rm = p ** j * (1 - 1 / p) / 2.0 ** mj
            rmsum += rm
            T2 = Ck[j] - Ck[j - 1]
            pr("   j=%2d m_j=%3d  T2=%.6e  rm=%.6e  T2/rm=%.4f   cum: C_j-1=%.6e  sum rm=%.6e" % (
                j, mj, float(T2), rm, float(T2) / rm if rm else float('nan'), float(Ck[j] - 1), rmsum))
        if p == 2:
            # random-model growth: continue rm(j) far beyond the data
            pr("   p=2 random model continued: partial sums S(K) = sum_{j<=K} rm(j) and local exponent d log S / d log K")
            vs = []; v = e0; n = N0
            K = 1 << 14
            while v < K + e0 + 2:
                vs.append(v); n += 1
                m = n
                while m % p == 0:
                    m //= p; v += 1
            import bisect
            S = 0.0; prev = None
            for j in range(1, K + 1):
                mj = bisect.bisect_left(vs, j + e0)
                S += 2.0 ** (j - 1 - mj)
                if j in (28, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384):
                    pr("      K=%5d  S(K)=%.4f  %s" % (j, S, ("exponent vs previous = %.3f" % (log(S / prev[1]) / log(j / prev[0]))) if prev else ""))
                    prev = (j, S)
            pr("      (mean of 2^-s_2(n) over n<2^L is (3/4)^L, so rm(j) ~ j^(log2(3/4)) = j^-0.415 on average and S(K) ~ K^0.585 [heuristic])")
    open(os.path.join(base, 'data', 'defect_table.txt'), 'w').write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
