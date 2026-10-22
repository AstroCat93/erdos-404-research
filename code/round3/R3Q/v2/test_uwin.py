#!/usr/bin/env python3
"""Exact test of Lemma 8 (U-window on coarse atoms) of the R3Q report.
x in 2+4Z_2, j = v(x+2); n < N, L = N-n; M* := M_N(x) (>= j); hypotheses
  (C1) beta(n) >= 3M*+1,  (C2) L + 2M* <= beta(n)+1,  (C3) beta(N) <= 2 beta(n).
U_t(y) = {e alive at t for y : v(S_e'(y)) >= beta(t)}.  Atom C' = x + 2^{m'} Z_2, m' = V_n(x) - M_n(x).
Claims, for every x' = x + 2^{m'} w:
  (a) U_n(x') = U_n(x);  (b) every member of U_N(x') has its length-n prefix in U_n(x);
  (c) for e in U_n(x) the set F_0(e) = {f : (e,f) alive at N} is the same at x' as at x, |F_0| <= 2^{L - floor((L-1)/2)};
  (d) avg_w |U_N(x')| <= |U_n(x)| 2^{L - floor((L-1)/2) - max(0, beta(N) - m' - 1 - j)}
      (and the weaker exponent with m' -> n-2, j -> M*).
Control: with the coarser atom m'' = ceil(V_n/2) - 1 the constancy in (a)/(c) is reported (expected to fail sometimes).
usage: test_uwin.py seed samples nlo nhi Lmax Rcap [gen]
  gen: random thresholds Th_n, Th_N satisfying the general hypotheses (T1)-(T5) of Lemma 8 instead of beta."""
import sys, random, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
TH = {}
def Uset(y, t):
    pop = alive_paths(y, t)
    th = TH.get(t, beta(t))
    return None if pop is None else {q[0]: q for q in pop if v2(q[2]) >= th}
def main():
    seed, S, nlo, nhi, Lmax, Rcap = map(int, sys.argv[1:7]); rnd = random.Random(seed)
    global GEN; GEN = len(sys.argv) > 7 and sys.argv[7] == 'gen'
    tests = bad = nonvac = ctrl_fail = ctrl_tests = 0; tight = 0.0
    for t in range(S):
        x = (-2 + (2 * rnd.getrandbits(80) + 1) * 2 ** rnd.randrange(2, 8)) % MOD
        j = v2(x + 2); n = rnd.randrange(nlo, nhi + 1); N = n + rnd.randrange(1, Lmax + 1); L = N - n
        Vn, Mn = env(x, n); VN, MN = env(x, N); Ms = MN; D = VN - Vn; mp0 = Vn - Mn
        TH.clear()
        if GEN:   # general thresholds: (T1) max(M_n,2j+1,D+M_n) <= Th_n <= m', Th_n <= Th_N <= 2m'; (T2) D <= m'-M_N; (T4)
            lo = max(Mn, 2 * j + 1, D + Mn)
            if not (lo <= mp0 and D <= mp0 - MN and Vn >= 3 * j + 1 and Vn - 2 * MN > j and MN < mp0): continue
            TH[n] = rnd.randrange(lo, mp0 + 1); TH[N] = rnd.randrange(TH[n], 2 * mp0 + 1)
        elif not (beta(n) >= 3 * Ms + 1 and L + 2 * Ms <= beta(n) + 1 and beta(N) <= 2 * beta(n)): continue
        Un = Uset(x, n)
        if Un is None: continue
        tests += 1
        if not Un: continue
        nonvac += 1; mp = Vn - Mn
        p0, p1, _ = taylor_pis(x, N)
        F0 = {}
        for e in Un:
            Se = Un[e][1]; F0[e] = set()
            for fb in range(1 << L):
                Sc = (Se + sum(p0[n + k] for k in range(L) if fb >> k & 1)) % MOD
                if v2(Sc) >= VN: F0[e].add(fb)
            if len(F0[e]) > 2 ** (L - (L - 1) // 2): bad += 1; print("(c) size fail")
        phi = L - (L - 1) // 2 - max(0, TH.get(N, beta(N)) - mp - 1 - j)
        phiw = phi if GEN else L - (L - 1) // 2 - max(0, beta(N) - (n - 2) - 1 - Ms)
        R = min(Rcap, max(1, TH.get(N, beta(N)) - mp - 1 - j + 2)); tot = 0
        for w in range(1 << R):
            xp = (x + (w << mp)) % MOD
            if Uset(xp, n).keys() != Un.keys(): bad += 1; print("(a) fail")
            q0, _, _ = taylor_pis(xp, N)
            for e in Un:
                Se = sum(q0[i] for i in range(n) if e[i])
                Fw = {fb for fb in range(1 << L)
                      if v2(Se + sum(q0[n + k] for k in range(L) if fb >> k & 1)) >= VN}
                if Fw != F0[e]: bad += 1; print("(c) constancy fail")
            UN = Uset(xp, N)
            for e2 in UN:
                if e2[:n] not in Un: bad += 1; print("(b) closure fail")
            tot += len(UN)
        avg = tot / (1 << R)
        if avg > len(Un) * 2.0 ** phi + 1e-12 or phi > phiw: bad += 1; print("(d) fail", n, N, avg, len(Un), phi, phiw)
        tight = max(tight, avg / (len(Un) * 2.0 ** phi))
        # control: coarser atom
        mc = (Vn + 1) // 2 - 1
        if mc < mp:
            ctrl_tests += 1
            for w in range(1, 64):
                xp = (x + (w << mc)) % MOD
                if env(xp, N) != (VN, MN): continue
                if env(xp, n) != (Vn, Mn): continue
                if Uset(xp, n).keys() != Un.keys(): ctrl_fail += 1; break
    print(f"windows tested={tests} with U_n nonempty={nonvac} failures={bad} max(avg/bound)={tight:.3f} "
          f"control: coarser atom changed U_n in {ctrl_fail}/{ctrl_tests}")
main()
