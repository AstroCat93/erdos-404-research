#!/usr/bin/env python3
"""Exact test of Lemma 5 (one-step identity) of the R3Q report. For e alive at n with slope lam,
m = V_n(x), D = v(x+n+1), under  lam + D <= m - M_n  and  lam < m - M_n :
  avg_{w mod 2^R} sum_{f: (e,f) alive at n+1 at x'} rho_{n+1}^{(lam')}(tau_{n+1} mod 2^lam') = 2^{1-D} rho_n^{(lam)}(tau_n mod 2^lam),
x' = x + 2^m w, R = D + lam; aliveness, slopes lam' (must equal lam), targets and rho recomputed at x'.
Control: the same average with rho replaced by 1 (should differ for some parents with lam >= 2).
usage: test_step.py seed samples nlo nhi Rmax"""
import sys, random, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from common import *
def main():
    seed, S, nlo, nhi, Rmax = map(int, sys.argv[1:6]); rnd = random.Random(seed)
    tested = bad = ctrl_diff = big = skipped = 0
    for t in range(S):
        if t % 2: x = (-2 + (2 * rnd.getrandbits(60) + 1) * 2 ** rnd.randrange(2, 9)) % MOD
        else: x = 2 * rnd.getrandbits(P - 2)
        n = rnd.randrange(nlo, nhi + 1); pop = alive_paths(x, n)
        if not pop: continue
        m, Mn = env(x, n); D = v2(x + n + 1)
        for e, Sv, S1, S2 in pop:
            lam = v2(S1)
            if not (lam + D <= m - Mn and lam < m - Mn): continue
            R = D + lam
            if R > Rmax: skipped += 1; continue
            rhs = Fraction(2) ** (1 - D) * rho(x, n, lam, target(x, n, Sv))
            acc = Fraction(0); acc1 = Fraction(0)
            for w in range(1 << R):
                xp = (x + (w << m)) % MOD
                p0, p1, _ = taylor_pis(xp, n + 1); Vn1 = env(xp, n + 1)[0]
                Se = sum(p0[i] for i in range(n) if e[i]); Sp = sum(p1[i] for i in range(n) if e[i])
                for f in (0, 1):
                    Sc = (Se + f * p0[n]) % MOD
                    if v2(Sc) < Vn1: continue
                    lc = v2(Sp + f * p1[n])
                    if lc != lam: bad += 1; print("slope changed", n, lam, lc)
                    acc += rho(xp, n + 1, lc, target(xp, n + 1, Sc)); acc1 += 1
            acc /= (1 << R); acc1 /= (1 << R); tested += 1; big += lam >= 3
            if acc != rhs: bad += 1; print("FAIL", n, lam, D, acc, rhs)
            if lam >= 2 and acc1 != Fraction(2) ** (1 - D): ctrl_diff += 1
    print(f"parents tested={tested} (lam>=3: {big}) skipped={skipped} failures={bad} control(rho:=1) differs in {ctrl_diff}")
main()
