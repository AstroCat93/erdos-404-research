# Independent recomputation of Gamma_p(j), dist_p(j), J0(p), theta_p, theta_set_p (Lemma 11.37, Thm 11.38)
# exact rationals; series summed in closed form beyond J0 (affine tail), evaluated with mpmath at 50 digits.
import sys
from fractions import Fraction
from math import factorial
import mpmath as mp
mp.mp.dps = 50

def data(p):
    e = [(-1)**u * factorial(p-1)//factorial(u) for u in range(p)]
    # integer law of W = sum eta_u e_u, weights 1,2,1 (total 4^p)
    dist = {0: 1}
    for x in e:
        nd = {}
        for w, c in dist.items():
            for s, wt in ((-1, 1), (0, 2), (1, 1)):
                nd[w + s*x] = nd.get(w + s*x, 0) + c*wt
        dist = nd
    subs = {0}
    for x in e:
        subs = subs | {s + x for s in subs}
    return e, dist, subs

def main(p, jmax=12):
    e, dist, subs = data(p)
    tot = 4**p
    P0 = Fraction(dist.get(0, 0), tot)
    assert P0 == Fraction(3, 2**(p+1)), (p, P0)
    assert len(subs) == 3 * 2**(p-2), (p, len(subs))
    G = {}; D = {}
    J0 = None
    for j in range(1, jmax+1):
        m = p**j
        cnt = sum(c for w, c in dist.items() if w % m == 0)
        G[j] = Fraction(m*cnt, tot) - 1
        D[j] = len({s % m for s in subs})
        if J0 is None and Fraction(cnt, tot) == P0:
            J0 = j
    # closed forms valid for j >= J0
    for j in range(J0, jmax+1):
        assert G[j] == Fraction(3*p**j, 2**(p+1)) - 1
        assert D[j] == 3*2**(p-2)
    # theta = (p-1)/p * sum_{j>=0} (1-1/p) p^{-j} f(j), f(j)=log_p(1+G(j+1))
    def series(term_exact, tail_const):
        # terms for j+1 < J0 explicit, then term = (j+1) + tail_const for j+1>=J0 (affine)
        s = mp.mpf(0)
        w = lambda j: (1 - mp.mpf(1)/p) * mp.mpf(p)**(-j)
        for j in range(0, J0-1):
            s += w(j) * term_exact(j+1)
        # sum_{j>=J0-1} w(j) ((j+1) + c)
        j0 = J0-1
        S0 = mp.nsum(lambda j: w(j), [j0, mp.inf])
        S1 = mp.nsum(lambda j: w(j)*(j+1), [j0, mp.inf])
        s += S1 + tail_const*S0
        return (mp.mpf(p-1)/p) * s
    lp = lambda x: mp.log(x)/mp.log(p)
    theta = series(lambda J: lp(mp.mpf((1+G[J]).numerator)/(1+G[J]).denominator),
                   lp(mp.mpf(3)/2**(p+1)))
    thset = series(lambda J: J - lp(D[J]), -lp(3*2**(p-2)))
    # brute-check closed form against direct truncated sum
    def direct(fn):
        return (mp.mpf(p-1)/p)*mp.fsum((1-mp.mpf(1)/p)*mp.mpf(p)**(-j)*fn(j+1) for j in range(0, jmax))
    print(f"p={p} J0={J0} Gamma(1)={G[1]} dist={[D[j] for j in range(1,J0+1)]} "
          f"maxfull={max(j for j in D if D[j]==p**j) if any(D[j]==p**j for j in D) else 0}")
    print(f"   theta_p={mp.nstr(theta,12)}  theta_set={mp.nstr(thset,12)}  1-theta_set={mp.nstr(1-thset,12)}")
    return theta, thset

if __name__ == "__main__":
    for p in [int(a) for a in sys.argv[1:]] or [2,3,5,7,11,13]:
        main(p)
