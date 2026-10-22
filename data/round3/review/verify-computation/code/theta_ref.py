"""Referee re-derivation of Lemma 11.37 table and Theorem 11.38 constants
(theta_p, theta_p^set) from gblock.c output, using exact rationals + mpmath.
Independent of T3a's gamma_enum.c/theta.py (not read).
Usage: python3 theta_ref.py OUTDIR"""
import sys, itertools
from fractions import Fraction as F
import mpmath as mp
mp.mp.dps = 40
OUT = sys.argv[1]

def load(p):
    cnt = {}
    wz = None
    for line in open(f"{OUT}/gblock_{p}.txt"):
        if line.startswith("p="):
            wz = int(line.split("weight=")[1].split()[0])
        elif line.startswith("j="):
            a, b = line.split()
            cnt[int(a[2:])] = int(b[4:])
    return wz, cnt

def eu(p):
    f = 1
    for i in range(1, p): f *= i
    out = []; uf = 1
    for u in range(p):
        if u > 0: uf *= u
        out.append((-1) ** u * (f // uf))
    return out

def dist(p, j):
    e = eu(p); m = p ** j
    s = {0}
    for x in e:
        s = s | {(y + x) % m for y in s}
    return len(s)

def distinct_int(p):
    e = eu(p); s = {0}
    for x in e:
        s = s | {y + x for y in s}
    return len(s)

res = {}
for p in [2, 3, 5, 7, 11, 13, 17, 19]:
    wz, cnt = load(p)
    assert cnt[0] == 4 ** p
    PW0 = F(wz, 4 ** p)
    ok_b = (PW0 == F(3, 2 ** (p + 1)))
    Gam = {j: F(p ** j * cnt[j], 4 ** p) - 1 for j in cnt}
    J0 = min(j for j in cnt if cnt[j] == wz)
    # distinct sums
    nint = distinct_int(p) if p <= 19 else None
    dl = {}
    j = 1
    while True:
        dl[j] = dist(p, j)
        if j >= J0 + 2 and dl[j] == nint and p ** j > 0: break
        j += 1
        if j > 16: break
    Lp = max(j for j in dl if dl[j] == p ** j) if any(dl[j] == p ** j for j in dl) else 0
    # theta_p = (p-1)/p * sum_{j>=0} (1-1/p) p^{-j} f_p(j), f_p(j)=log_p(1+Gamma(j+1))
    # for j+1 >= J0: 1+Gamma = (3/2) p^{j+1} 2^{-p}  -> f = (j+1) + log_p(3/2^{p+1})
    def theta(fun, jstar):
        s = mp.mpf(0)
        for jj in range(0, jstar):
            s += (1 - mp.mpf(1) / p) * mp.mpf(p) ** (-jj) * fun(jj)
        # tail jj>=jstar with f = (jj+1) + c ; sum_{jj>=J} q^jj (jj+1) and q^jj
        q = mp.mpf(1) / p
        c = tailc
        # sum_{jj>=J} q^jj = q^J/(1-q); sum_{jj>=J} (jj+1) q^jj = q^J (J+1 - J q)/(1-q)^2
        J = jstar
        s += (1 - q) * (q ** J * (J + 1 - J * q) / (1 - q) ** 2 + c * q ** J / (1 - q))
        return (mp.mpf(p) - 1) / p * s
    tailc = mp.log(mp.mpf(3) / 2 ** (p + 1)) / mp.log(p)
    jstar = J0  # f_p(j) uses Gamma(j+1); affine from j+1>=J0 i.e. j>=J0-1; safe to start tail at J0
    # check affinity numerically for j+1 in [J0, max computed]
    for jj in range(J0, max(cnt)):
        assert Gam[jj] == F(3, 2) * p ** jj / 2 ** p - 1, (p, jj)
    def fgam(jj):
        g = Gam[jj + 1]
        return mp.log(mp.mpf(g.numerator + g.denominator) / g.denominator) / mp.log(p)
    th = theta(fgam, jstar)
    # theta_set: log_p(p^{j+1}/dist(j+1)); for large j, dist = nint (constant) => (j+1) - log_p(nint)
    tailc = -mp.log(nint) / mp.log(p)
    jset = min(j for j in dl if dl[j] == nint)  # dist constant from here
    def fset(jj):
        return (jj + 1) - mp.log(dl[jj + 1]) / mp.log(p)
    ths = theta(fset, max(jset - 1, 0))
    res[p] = (Gam[1], J0, Lp, th, 1 - ths)
    print(f"p={p}: P(W=0)=3/2^(p+1)? {ok_b}; #distinct int sums={nint} (3*2^(p-2)={3*2**(p-2) if p>=2 else None}); "
          f"Gamma(1)={Gam[1]}; J0={J0}; maxj dist=p^j: {Lp}; dist={dl}")
    print(f"     theta_p={mp.nstr(th, 12)}  1-theta_set={mp.nstr(1 - ths, 13)}")
print("theta_2 vs log2(3)/4:", mp.nstr(res[2][3] - mp.log(3, 2) / 4, 5))
