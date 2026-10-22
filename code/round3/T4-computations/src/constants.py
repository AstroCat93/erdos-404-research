# c_p = max_{xi in (Z/p)^x} prod_{r=0}^{p-1} |cos(pi xi r!/p)|  and its geometric mean over xi, primes p <= 53.
# mpmath, 30 digits.  Also the argmax xi and the number of xi attaining the max (up to 1e-20).
from mpmath import mp, mpf, cos, pi, fabs, log, exp
import sys
mp.dps = 30
def primes(n):
    return [q for q in range(2, n+1) if all(q % d for d in range(2, int(q**0.5)+1))]
print("# p  c_p  geomean_xi  argmax_xi  n_argmax  (2/pi)^p  c_p^(1/p)")
for p in primes(53):
    fac = [1]*p
    for r in range(1, p): fac[r] = fac[r-1]*r % p
    best = mpf(0); arg = None; nbest = 0; logsum = mpf(0)
    for xi in range(1, p):
        pr = mpf(1)
        for r in range(p):
            pr *= fabs(cos(pi*mpf(xi*fac[r] % p)/p))
        if pr > 0: logsum += log(pr)
        else: logsum = mpf('-inf')
        if pr > best + mpf(10)**-20: best = pr; arg = xi; nbest = 1
        elif fabs(pr-best) <= mpf(10)**-20: nbest += 1
    gm = exp(logsum/(p-1)) if logsum > mpf('-inf') else mpf(0)
    print(p, mp.nstr(best, 15), mp.nstr(gm, 15), arg, nbest, mp.nstr((mpf(2)/pi)**p, 10), mp.nstr(best**(mpf(1)/p), 10))
