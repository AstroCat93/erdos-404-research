#!/usr/bin/env python3
"""summarize.py -- consolidated table of the exact L^2 Fourier masses C_k(p,N0) from data/l2/*.txt,
random-model tails beyond the computed depth, and a check of the block-recursion inequality
(Theorem D):  C_{e_{m+1}} / C_{e_m} <= 1 + (p^J - 1) c_p(J)^2,  J = e_{m+1} - e_m,
using c_p(J) from data/cpJ.txt (sup over all nonzero xi mod p^J).  Writes data/l2_summary.txt and .json.
"""
import glob, json, os, re, sys
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from l2post import read, crt, vfact

def rm_tail(p, N0, e0, kmax, K=3000):
    """sum_{k>kmax} p^k (1-1/p) 2^{-m_k}, m_k = #{n>=N0: v(n!)<k+e0}, as a float."""
    # m_k: count elements; n ranges up to where v(n!) >= kmax+K+e0
    tail = 0.0
    n = N0; v = vfact(N0, p); counts = {}
    # precompute v(n!) increasing
    vs = []
    while v < K + kmax + e0 + 1:
        vs.append(v); n += 1
        m = n
        while m % p == 0:
            m //= p; v += 1
    # vs[i] = v((N0+i)!)
    import bisect
    for k in range(kmax + 1, kmax + K):
        mk = bisect.bisect_left(vs, k + e0)
        from math import exp, log
        t = (k * log(p) + log(1 - 1 / p) - mk * log(2))
        tail += exp(t) if t > -700 else 0.0
    return tail

def main():
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    cp = {}; gam = {}
    for line in open(os.path.join(base, 'data', 'cpJ.txt')):
        m = re.match(r'p=(\d+) J=(\d+)\s+c_p\(J\)=([0-9.e+-]+)\s+at xi=\d+\s+Gam_p\(J\)=([0-9.e+-]+)', line)
        if m: cp[(int(m.group(1)), int(m.group(2)))] = float(m.group(3)); gam[(int(m.group(1)), int(m.group(2)))] = float(m.group(4))
    from math import cos, pi, factorial
    out = []; js = {}
    files = sorted(glob.glob(os.path.join(base, 'data', 'l2', 'p*_E*_N*.txt')),
                   key=lambda f: [int(x) for x in re.findall(r'\d+', os.path.basename(f))])
    for fn in files:
        p, E, N0, M, rows = read(fn)
        e0 = vfact(N0, p)
        S = {Ep: (crt(hi, lo, sq), Mp, hit) for Ep, Mp, hi, lo, sq, sd, hit in rows}
        Ck = {0: Fraction(1)}
        for Ep in range(1, E + 1):
            k = Ep - e0
            if k >= 1: Ck[k] = Fraction(p) ** k * Fraction(S[Ep][0], 4 ** M)
        kmax = E - e0
        # block structure: attained levels (relative) = {v(n!)-e0 : n>=N0}
        attained = set()
        n = N0
        while vfact(n, p) - e0 <= kmax:
            attained.add(vfact(n, p) - e0); n += 1
        viol = []
        prev = 0
        checks = []
        for k in range(1, kmax + 1):
            if k in attained or k == kmax:
                pass
            # the top block ending at level k: previous attained level below k
        levels = sorted(a for a in attained if a <= kmax)
        # Theorem D applies between consecutive attained levels e_m -> e_{m+1}
        first_block_identity = None
        for a, b in zip(levels, levels[1:]):
            J = b - a
            ratio = float(Ck[b] / Ck[a])
            if N0 == 1 and a == 0:
                # partial first block {1,...,p-1}: exact identity C_1 = 1 + Gamma'_p, Gamma'_p = sum_{s!=0} prod_{r=1}^{p-1} cos^2(pi s r!/p)
                gp = sum(eval('*'.join(['1.0'] + ['cos(pi*%d*%d/%d)**2' % (s, factorial(r) % p, p) for r in range(1, p)])) for s in range(1, p))
                first_block_identity = (float(Ck[1]), 1 + gp, abs(float(Ck[1]) - 1 - gp) < 1e-12)
                continue
            bsup = 1 + (p ** J - 1) * cp[(p, J)] ** 2 if (p, J) in cp else None
            bgam = 1 + gam[(p, J)] if (p, J) in gam else None
            bound = min(x for x in (bsup, bgam) if x is not None) if (bsup or bgam) else None
            ok = (bound is None) or (ratio <= bound * (1 + 1e-12))
            checks.append((a, b, J, ratio, bound, ok))
            if not ok: viol.append((a, b))
        hitfrac = {Ep - e0: S[Ep][2] / p ** Ep for Ep in S if Ep - e0 >= 1}
        tail = rm_tail(p, N0, e0, kmax)
        last = float(Ck[kmax])
        out.append("p=%d N0=%d e0=%d M=%d depth k=%d : C_k=%.10f  C_k-1=%.6e  hit fraction=%.8f  1/C_k=%.6f  rm tail beyond=%.3e  TheoremD checks=%d viol=%d" % (
            p, N0, e0, M, kmax, last, last - 1, hitfrac[kmax], 1 / last, tail, len(checks), len(viol)))
        out.append("   C_k by k: " + " ".join("%d:%.8g" % (k, float(Ck[k])) for k in range(1, kmax + 1)))
        out.append("   hit/p^k : " + " ".join("%d:%.6f" % (k, hitfrac[k]) for k in range(1, kmax + 1)))
        if first_block_identity: out.append("   first partial block identity C_1 = 1+Gamma'_p : %.12f vs %.12f  ok=%s" % first_block_identity)
        out.append("   Theorem D ratios (a->b,J,ratio,bound): " + " ".join("%d->%d,%d,%.6g,%s" % (a, b, J, r, ("%.4g" % bd) if bd else "n/a") for a, b, J, r, bd, ok in checks))
        js["p%d_N%d" % (p, N0)] = dict(p=p, N0=N0, e0=e0, M=M, kmax=kmax,
            C_k={k: str(Ck[k]) for k in range(1, kmax + 1)}, C_k_float={k: float(Ck[k]) for k in range(1, kmax + 1)},
            hit_fraction={k: hitfrac[k] for k in range(1, kmax + 1)}, rm_tail_beyond=tail,
            theoremD_checks=[dict(a=a, b=b, J=J, ratio=r, bound=bd, ok=ok) for a, b, J, r, bd, ok in checks])
    txt = "\n".join(out)
    print(txt)
    open(os.path.join(base, 'data', 'l2_summary.txt'), 'w').write(txt + "\n")
    json.dump(js, open(os.path.join(base, 'data', 'l2_summary.json'), 'w'), indent=1)

if __name__ == '__main__':
    main()
