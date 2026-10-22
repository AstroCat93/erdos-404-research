"""t4: Corollary F1 by EXHAUSTIVE Haar enumeration (finite horizon).

Deterministic chain n_0 < ... < n_{L+1}, start j = 0, theta schedules fixed in
advance (constant Fractions, or the x-dependent minimal one p^{-D_l}).
Z_p is partitioned into cylinders a + p^k Z_p (a natural), refined until the
cylinder determines every quantity: k > M_{n_{L+1}}(a) and k >= V_{n_{L+1}}(a)
(then V_m, T_l mod p^{D_l}, Sigma_l mod p^{D_l+D_{l+1}} are constant on it; this
locality is itself tested in t1/LOC).  Cylinders still undetermined at k = kcap
are counted as unknown mass U.

Per determined cylinder (pointwise form of Theorem F, finite horizon):
     I_0 and L_1 ... L_{L-1}   =>   |T_L| >= theta_L p^{D_L}   (=> alive at n_L)
Integrated (Corollary F1, finite horizon, A = Z_p and A = each class mod p):
     mu(A & alive at n_L) >= mu(A & I_0) - sum_{l=1}^{L-1} mu(A \\ L_l)
checked with exact Fractions as  lower(LHS) >= upper(RHS)  (U counted adversely).

The base set is a cylinder B = x0 + p^m Z_p (m = 0: B = Z_p); A ranges over
B itself and its p sub-classes mod p^{m+1}.  All masses are normalised by
mu(B) (i.e. they are mu_B).

Usage: python3 t4_corF1.py p kcap m x0 n_0 H_0 H_1 ... H_L
"""
import sys
import time
from collections import defaultdict
from fractions import Fraction

from fz_core import Mval, Vlist, Window, lift_counts, target_sets_dp


def main():
    p = int(sys.argv[1])
    kcap = int(sys.argv[2])
    m0 = int(sys.argv[3])
    x0 = int(sys.argv[4])
    n0 = int(sys.argv[5])
    Hs = [int(a) for a in sys.argv[6:]]
    L = len(Hs) - 1
    times = [n0]
    for h in Hs:
        times.append(times[-1] + h)
    NT = times[-1]
    schedules = {"min(p^-D)": None}
    for th in [Fraction(1, 7), Fraction(1, 3), Fraction(1, 2), Fraction(2, 3),
               Fraction(6, 7), Fraction(1)]:
        schedules["const %s" % th] = th
    t0 = time.time()
    k0 = m0 + 1
    base = x0 % (p ** m0)
    stack = [(base + t * p ** m0, k0) for t in range(p)]
    mass = defaultdict(Fraction)   # (schedule, A, quantity) -> mass
    U = Fraction(0)
    ncyl = 0
    pt_fail = 0
    pt_hyp = defaultdict(int)
    alive_mass = defaultdict(Fraction)
    while stack:
        a, k = stack.pop()
        x = a if a > 0 else p ** k  # natural representative
        V = Vlist(x, NT, p)
        M = Mval(x, NT, p)
        if not (k > M and k >= V[NT]):
            if k >= kcap:
                U += Fraction(p ** m0, p ** k)
                continue
            for t in range(p):
                stack.append((a + t * p ** k, k + 1))
            continue
        ncyl += 1
        w = Fraction(p ** m0, p ** k)
        Acls = (a // p ** m0) % p
        Ds = [V[times[l + 1]] - V[times[l]] for l in range(L + 1)]
        pw = [p ** d for d in Ds]
        Ts = []
        for l in range(L + 1):
            dp = target_sets_dp(x, [times[l]], p, V[times[l + 1]])
            Ts.append({z % pw[l] for z in dp[times[l]]})
        cnts = [lift_counts(Window(x, times[l], times[l + 1], p), Ds[l + 1])
                for l in range(L)]
        aliveL = bool(Ts[L])
        for A in ("all", "cls%d" % Acls):
            alive_mass[A] += w if aliveL else 0
        for name, th in schedules.items():
            theta = {l: (Fraction(1, pw[l]) if th is None else th)
                     for l in range(1, L + 1)}
            G = {l: {r for r in range(pw[l])
                     if Fraction(int(cnts[l][r]), pw[l + 1]) >= theta[l + 1]}
                 for l in range(0, L)}
            I0 = bool(Ts[0] & G[0])
            Ll = {l: len(G[l]) > (1 - theta[l]) * pw[l] for l in range(1, L)}
            concl = len(Ts[L]) >= theta[L] * pw[L]
            if I0 and all(Ll.values()):
                pt_hyp[name] += 1
                if not (concl and aliveL):
                    pt_fail += 1
                    print("POINTWISE FAIL", name, a, k)
            for A in ("all", "cls%d" % Acls):
                if I0:
                    mass[(name, A, "I0")] += w
                for l in range(1, L):
                    if not Ll[l]:
                        mass[(name, A, "notL%d" % l)] += w
                if concl:
                    mass[(name, A, "concl")] += w
    print("base cylinder B = %d + %d^%d Z_p" % (base, p, m0))
    print("p=%d chain=%s kcap=%d  determined cylinders=%d  unknown mass U=%s (~%.3g)  time=%.1fs"
          % (p, times, kcap, ncyl, U, float(U), time.time() - t0))
    print("pointwise: hypotheses held on (cylinders) %s ; failures %d" % (dict(pt_hyp), pt_fail))
    nfail = pt_fail
    for name in schedules:
        for A in ["all"] + ["cls%d" % c for c in range(p)]:
            mA = Fraction(1) if A == "all" else Fraction(1, p)
            I0 = mass[(name, A, "I0")]
            nots = sum((mass[(name, A, "notL%d" % l)] for l in range(1, L)), Fraction(0))
            rhs_upper = I0 + U - nots
            lhs_lower = alive_mass[A]
            ok = lhs_lower >= rhs_upper
            ok_concl = mass[(name, A, "concl")] >= rhs_upper
            if A == "all" or not ok:
                print("  %-12s A=%-5s mu(A&alive n_L)=%.6f  mu(A&|T_L|>=th p^D)=%.6f  "
                      "mu(A&I0)=%.6f  sum mu(A\\L_l)=%.6f  RHS=%.6f  %s"
                      % (name, A, float(lhs_lower), float(mass[(name, A, 'concl')]),
                         float(I0), float(nots), float(I0 - nots),
                         "OK" if (ok and ok_concl) else ("INCONCLUSIVE(U)" if lhs_lower >= I0 - nots else "FAIL")))
            if not (lhs_lower >= I0 - nots and mass[(name, A, "concl")] >= I0 - nots):
                nfail += 1
    print("TOTAL FAILURES", nfail)


if __name__ == "__main__":
    main()
