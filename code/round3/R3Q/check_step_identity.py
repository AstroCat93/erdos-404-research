#!/usr/bin/env python3
"""Exact test of the per-step weighted identity (R3Q report, Lemma 5), independent of note.md code.

For random even x and a time n, every path e alive at n with slope lam = v(S_e'(x)) satisfying
   lam + D <= m - M_n,  lam <= m - M_n - 1,     m = V_n(x), D = v(x+n+1), M_n = max_{i<=n} v(x+i),
should satisfy
   avg_{w mod 2^R} sum_{f in {0,1}: (e,f) alive at n+1 for x'} rho_{n+1}^{(lam')}(tau_{n+1}((e,f),x') mod 2^lam')
        = 2^{1-D} rho_n^{(lam)}(tau_n(e,x) mod 2^lam),
where x' = x + 2^m w, lam' = slope of the child at x' (should equal lam), and
   rho_n^{(lam)}(s) = 2^lam * P( sum_{i>=0} g_i pi_{n+i}(x)/pi_n(x) == s mod 2^lam ),  g_i iid fair bits.
Everything at x' is recomputed from scratch (aliveness, slope, target, rho) by direct evaluation.
usage: check_step_identity.py seed samples n_lo n_hi Rmax [res modu]   (x uniform in res + modu*Z_2)
"""
import random, sys
from fractions import Fraction

def v2(a):
    return (a & -a).bit_length() - 1 if a else 10**9

def rho(x, n, lam, s):
    """2^lam * P(Q == s mod 2^lam), exact Fraction."""
    if lam == 0:
        return Fraction(1)
    mod = 1 << lam
    dist = {0: 1}
    tot = 1
    c = 1   # c_{n+i} = pi_{n+i}/pi_n
    i = 0
    while v2(c) < lam:
        cm = c % mod
        nd = {}
        for t, k in dist.items():
            nd[t] = nd.get(t, 0) + k
            u = (t + cm) % mod
            nd[u] = nd.get(u, 0) + k
        dist = nd; tot *= 2
        i += 1
        c *= (x + n + i)
    return Fraction(dist.get(s % mod, 0) * mod, tot)

def alive_paths(x, n, P):
    """Return list of bit-tuples e (length n, e0=1) alive at n, via BFS on targets."""
    pop = [((), 0, P)]   # (bits, tau mod 2^prec, prec)
    for j in range(n):
        d = v2(x + j + 1); u = (x + j + 1) >> d
        new = []
        for bits, tau, prec in pop:
            for e in ((1,) if j == 0 else (0, 1)):
                t = (tau - e) % (1 << prec)
                if d and (t & ((1 << d) - 1)):
                    continue
                npr = prec - d
                new.append((bits + (e,), ((t >> d) * pow(u, -1, 1 << npr)) % (1 << npr), npr))
        pop = new
    return [b for b, _, _ in pop]

def evals(x, N, P):
    """pi_j(x), pi_j'(x) mod 2^P for j = 0..N."""
    MOD = 1 << P
    pis, dps = [1], [0]
    for j in range(1, N + 1):
        pis.append(pis[-1] * (x + j) % MOD)
        dps.append((dps[-1] * (x + j) + pis[-2]) % MOD)
    return pis, dps

def Vn(x, n):
    return sum(v2(x + i) for i in range(1, n + 1))

def main():
    seed, S, nlo, nhi, Rmax = (int(a) for a in sys.argv[1:6])
    res, modu = (int(sys.argv[6]), int(sys.argv[7])) if len(sys.argv) > 7 else (0, 2)
    P = 400
    rnd = random.Random(seed)
    tested = 0; fails = 0; lam_gt_D = 0; skipped = 0
    for s in range(S):
        x = (res + modu * rnd.getrandbits(P)) % (1 << P)
        n = rnd.randrange(nlo, nhi + 1)
        m = Vn(x, n); Mn = max(v2(x + i) for i in range(1, n + 1)); D = v2(x + n + 1)
        paths = alive_paths(x, n, P)
        if not paths:
            continue
        pis, dps = evals(x, n + 1, P)
        for e in paths:
            Se = sum(pis[j] for j in range(n) if e[j]) % (1 << P)
            Sp = sum(dps[j] for j in range(n) if e[j]) % (1 << P)
            lam = v2(Sp)
            if not (lam + D <= m - Mn and lam <= m - Mn - 1):
                continue
            R = D + lam + 1
            if R > Rmax:
                skipped += 1
                continue
            tau = (-Se * pow(pis[n] >> m, -1, 1 << P)) >> 0
            tau = ((-Se) >> m) * pow(pis[n] >> m, -1, 1 << (P - m)) % (1 << (P - m))
            lhs_target = Fraction(2) ** (1 - D) * rho(x, n, lam, tau % (1 << max(lam, 1)) if lam else 0)
            acc = Fraction(0)
            for w in range(1 << R):
                xp = (x + (w << m)) % (1 << P)
                pp, dp = evals(xp, n + 1, P)
                Vn1 = Vn(xp, n + 1)
                Sx = sum(pp[j] for j in range(n) if e[j]) % (1 << P)
                Spx = sum(dp[j] for j in range(n) if e[j]) % (1 << P)
                for f in (0, 1):
                    Sc = (Sx + f * pp[n]) % (1 << P)
                    if v2(Sc) < Vn1:
                        continue
                    lamc = v2((Spx + f * dp[n]) % (1 << P))
                    if lamc != lam:
                        print("SLOPE CHANGE", x, n, e, lam, lamc); fails += 1
                    tc = ((-Sc) >> Vn1) * pow(pp[n + 1] >> Vn1, -1, 1 << (P - Vn1)) % (1 << (P - Vn1))
                    acc += rho(xp, n + 1, lamc, tc % (1 << lamc) if lamc else 0)
            acc /= (1 << R)
            tested += 1
            lam_gt_D += (lam > D)
            if acc != lhs_target:
                fails += 1
                print("FAIL", n, lam, D, m, Mn, acc, lhs_target)
    print(f"tested parents={tested} (with lam>D: {lam_gt_D}) skipped(R>Rmax)={skipped} failures={fails}")

if __name__ == "__main__":
    main()
