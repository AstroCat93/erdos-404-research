# Independent recomputation of Gamma_p(j), J_0(p), dist_p(j), theta_p, theta_set_p (Lemma 11.37, Thm 11.38).
# Meet-in-the-middle over the 3^p weighted sign vectors (weights 1,2,1 for eta=-1,0,1).
import sys, math
from fractions import Fraction
from collections import Counter
import mpmath as mp
mp.mp.dps = 40

def evals(p):
    return [(-1)**u * math.factorial(p-1)//math.factorial(u) for u in range(p)]

def half(es):
    c = Counter({0:1})
    for e in es:
        n = Counter()
        for s, w in c.items():
            n[s] += 2*w; n[s+e] += w; n[s-e] += w
        c = n
    return c

def subset_half(es):
    s = {0}
    for e in es:
        s = s | {x+e for x in s}
    return s

def stats(p, jmax):
    e = evals(p); h = p//2
    A = half(e[:h]); B = half(e[h:])
    SA = subset_half(e[:h]); SB = subset_half(e[h:])
    Pzero = Fraction(3, 2**(p+1))
    G = {}; dist = {}; J0 = None
    for j in range(1, jmax+1):
        q = p**j
        Am = Counter()
        for s, w in A.items(): Am[s % q] += w
        cnt = 0
        for s, w in B.items(): cnt += w*Am.get((-s) % q, 0)
        P = Fraction(cnt, 4**p)
        G[j] = q*P - 1
        if J0 is None and P == Pzero: J0 = j
        # distinct subset sums mod q
        if q <= 10**7 or True:
            ra = {x % q for x in SA}
            dist[j] = len({(x+y) % q for x in ra for y in SB}) if len(ra)*len(SB) < 5*10**7 else None
    return e, G, dist, J0

def theta(p, G, dist, J0, jmax):
    # f_p(j)=log_p(1+Gamma(j+1)); affine for j+1>=J0: 1+Gamma(j+1)= (3/2) p^{j+1} 2^{-p}
    lp = mp.log(p)
    w = lambda j: (1-mp.mpf(1)/p)*mp.mpf(p)**(-j)
    F = mp.mpf(0); Fs = mp.mpf(0)
    for j in range(0, 400):
        jj = j+1
        if jj in G: g = 1+G[jj]
        else: g = Fraction(3, 2)*Fraction(p**jj, 2**p)
        F += w(j)*mp.log(mp.mpf(g.numerator)/g.denominator)/lp
        if jj in dist and dist[jj] is not None: d = dist[jj]
        else: d = 3*2**(p-2)  # all integer subset sums distinct mod p^jj once jj large (check validity below)
        Fs += w(j)*mp.log(mp.mpf(p)**jj/d)/lp
    return (p-1)*F/p, (p-1)*Fs/p

if __name__ == '__main__':
    for p in [2,3,5,7,11,13,17,19]:
        jmax = 9 if p < 11 else 8
        e, G, dist, J0 = stats(p, jmax)
        th, ths = theta(p, G, dist, J0, jmax)
        print(p, 'Gamma1=', G[1], 'J0=', J0, 'dist=', [dist[j] for j in range(1, 5)],
              'maxfull=', max([j for j in dist if dist[j] == p**j], default=0),
              'theta=', mp.nstr(th, 10), '1-theta_set=', mp.nstr(1-ths, 12), flush=True)
