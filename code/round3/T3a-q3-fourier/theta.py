#!/usr/bin/env python3
"""theta.py -- rigorous (interval-arithmetic) evaluation of the exponents of Theorem 3 of the T3a round-3 writeup.

Input: data/gamma_enum.txt (exact integer counts from gamma_enum.c).
  Gamma_p(J) = p^J cnt(J)/4^p - 1                         (exact rational)
  theta_p     = ((p-1)/p) * sum_{J>=1} (1-1/p) p^{-(J-1)} log_p(1 + Gamma_p(J))       (fair-coin measure nu)
  theta_set_p = ((p-1)/p) * sum_{J>=1} (1-1/p) p^{-(J-1)} log_p(p^J / dist_p(J))      (best per-block measure)
For J beyond the enumerated range, or once cnt(J) has reached weight(W=0) (resp. dist(J) has reached 3*2^(p-2)),
the summand is J + log_p(3*2^(-p-1)) (resp. J - log_p(3*2^(p-2))) for all larger J (Lemma 2 of the writeup), and the
tail is summed in closed form.  All arithmetic in mpmath interval arithmetic (iv, 80 bits); the printed upper
endpoints are rigorous upper bounds (lower endpoints for 1-theta are rigorous lower bounds).
Usage: python3 theta.py   -> writes data/theta.txt
"""
import os, re
from fractions import Fraction
from mpmath import iv, mpf
iv.prec = 100
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

def load():
    D = {}
    for line in open(os.path.join(BASE, 'data', 'gamma_enum.txt')):
        m = re.match(r'p=(\d+)\s+Sigma_p=(\d+)\s+total_weight=4\^p=(\d+)\s+weight\(W=0\)=(\d+)', line)
        if m:
            p = int(m.group(1)); D.setdefault(p, {'J': {}})
            D[p]['W0'] = int(m.group(4)); D[p]['tot'] = int(m.group(3)); continue
        m = re.match(r'p=(\d+) J=(\d+)\s+p\^J=(\d+)\s+cnt=(\d+)\s+dist=(\d+)', line)
        if m:
            p, J = int(m.group(1)), int(m.group(2))
            D[p]['J'][J] = (int(m.group(4)), int(m.group(5)))
    return D

def logp(x, p):
    return iv.log(iv.mpf(x)) / iv.log(iv.mpf(p))

def tail(p, J0, a):
    """sum_{J>=J0} (1-1/p) p^{-(J-1)} (J + a), a an interval."""
    x = iv.mpf(1) / p
    S0 = x ** (J0 - 1) / (1 - x)
    S1 = x ** (J0 - 1) * (J0 / (1 - x) + x / (1 - x) ** 2)
    return (1 - x) * (S1 + a * S0)

def main():
    D = load(); out = []
    def pr(s):
        print(s); out.append(s)
    pr("# p  theta_p(fair coins) upper   1-theta_p lower   theta_set_p upper   1-theta_set lower   1-p^-L_p   (J0 closed-form start)")
    for p in sorted(D):
        d = D[p]; tot = d['tot']; W0 = d['W0']; Js = sorted(d['J'])
        dist0 = 3 * 2 ** (p - 2)
        # fair coins
        F = iv.mpf(0); J0 = None
        for J in Js:
            cnt, dist = d['J'][J]
            if cnt == W0:
                J0 = J; break
            onepG = Fraction(p ** J * cnt, tot)
            F += (1 - iv.mpf(1) / p) * iv.mpf(p) ** (-(J - 1)) * logp(onepG.numerator, p) - (1 - iv.mpf(1) / p) * iv.mpf(p) ** (-(J - 1)) * logp(onepG.denominator, p)
        assert J0 is not None, "closed form not reached for p=%d" % p
        a = logp(Fraction(W0, tot).numerator, p) - logp(Fraction(W0, tot).denominator, p)   # log_p(W0/4^p) = log_p(3*2^(-p-1))
        F += tail(p, J0, a)
        theta = F * (p - 1) / p
        # best per-block measure (set version)
        G = iv.mpf(0); J1 = None; L = 0
        for J in Js:
            cnt, dist = d['J'][J]
            if dist == p ** J: L = J
            if dist == dist0 and J >= 1:
                J1 = J; break
            G += (1 - iv.mpf(1) / p) * iv.mpf(p) ** (-(J - 1)) * (J - logp(dist, p))
        assert J1 is not None
        G += tail(p, J1, -logp(dist0, p))
        tset = G * (p - 1) / p
        pr("p=%2d  theta=%.9e  1-theta>=%.12f   theta_set=%.9e  1-theta_set>=%.12f   1-p^-L=%.9f (L_p=%d)   J0=%d J1=%d" % (
            p, float(theta.b), float((1 - theta).a), float(tset.b), float((1 - tset).a), 1 - p ** (-L), L, J0, J1))
    open(os.path.join(BASE, 'data', 'theta.txt'), 'w').write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
