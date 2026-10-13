#!/usr/bin/env python3
"""Exact test of the undetermined-population window bound (R3Q report, Lemma 7).

For x in 2+4Z_2, j = v(x+2), times n < N, m = V_n(x), D = V_N(x) - m, and thresholds
Th_n <= Th_N, let U_n = {e alive at n : v(S_e'(x)) >= Th_n}.  If the hypotheses
  (U0) m >= max(4,3j+1); (U1) D <= min(Th_n, m - M_N), D <= m; (U2) j < m - 2 M_N;
  (U3) Th_n > 2j; (U4) Th_N <= 2m; (U5) Th_n <= min(Th_N, m - M_N); (U6) M_N < m
hold, the lemma asserts, for x' = x + 2^m w (w uniform):
  (a) U_n is the same at every x'; every member of U_N(x') has its length-n prefix in U_n;
  (b) every e in U_n has v(S_e^[2](x)) <= j;
  (c) the set F_0(e) of f with (e,f) alive at N does not depend on w, and |F_0| <= 2^{N-n-r},
      r = floor((N-n-1)/2);
  (d) avg_w |U_N(x')| <= |U_n| * 2^{(N-n) - r - max(0, Th_N - m - 1 - j)}.
Everything at x' is recomputed by direct evaluation.  Thresholds are instantiated as
Th_n = m - c1, Th_N = V_N - c2 with small constants (the lemma allows any thresholds satisfying (U0)-(U6)).
usage: check_U_window.py seed samples res modu nlo nhi gapmax [gen|beta]
  (mode beta: Th_n = beta(n) = n - s(n) - floor(log2 n), the threshold used in Theorem C)
"""
import random, sys

def v2(a):
    return (a & -a).bit_length() - 1 if a else 10**9

def evals(x, N, P):
    MOD = 1 << P
    p0, p1, p2 = [1], [0], [0]
    for j in range(1, N + 1):
        a = x + j
        p2.append((p2[-1] * a + p1[-1]) % MOD)
        p1.append((p1[-1] * a + p0[-1]) % MOD)
        p0.append(p0[-1] * a % MOD)
    return p0, p1, p2

def alive_bits(x, n, P):
    pop = [((), 0, P)]
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
        if len(pop) > 20000:
            return None
    return [b for b, _, _ in pop]

MODE = "gen"
def main():
    global MODE
    seed, S, res, modu, nlo, nhi, gapmax = (int(a) for a in sys.argv[1:8])
    if len(sys.argv) > 8: MODE = sys.argv[8]
    P = 600
    MOD = 1 << P
    rnd = random.Random(seed)
    tests = 0; fails = 0; nonempty_U = 0
    for s in range(S):
        x = (res + modu * rnd.getrandbits(P)) % MOD
        j = v2(x + 2)
        n = rnd.randrange(nlo, nhi + 1)
        N = n + rnd.randrange(2, gapmax + 1)
        V = lambda t, y=x: sum(v2(y + i) for i in range(1, t + 1))
        m = V(n); VN = V(N); D = VN - m
        MN = max(v2(x + i) for i in range(1, N + 1))
        bits = alive_bits(x, n, P)
        if bits is None:
            continue
        p0, p1, p2 = evals(x, N, P)
        slopes = {}
        for e in bits:
            slopes[e] = v2(sum(p1[t] for t in range(n) if e[t]) % MOD)
        # choose thresholds: Th_n as large as allowed by (U5) but test only if some path qualifies
        def beta(t): return t - bin(t).count("1") - (t.bit_length() - 1)
        for c1 in ((0, 1, 2, 3) if MODE == "gen" else ("beta",)):
            if MODE == "gen":
                Thn = min(m - MN, m - c1)
                ThN = min(2 * m, VN - c1)
            else:
                Thn, ThN = beta(n), beta(N)
            hyp = (m >= max(4, 3 * j + 1) and D <= min(Thn, m - MN) and D <= m and j < m - 2 * MN
                   and Thn > 2 * j and ThN <= 2 * m and Thn <= min(ThN, m - MN) and MN < m)
            if not hyp:
                continue
            Un = [e for e in bits if slopes[e] >= Thn]
            if not Un:
                continue
            nonempty_U += 1
            r = (N - n - 1) // 2
            # (b)
            for e in Un:
                k2 = v2(sum(p2[t] for t in range(n) if e[t]) % MOD)
                if k2 > j:
                    fails += 1; print("FAIL(b)", x % 1024, n, e, k2, j)
            R = max(1, ThN - m + 1)
            R = min(R, 10)
            # F0 at x (w = 0)
            F0 = {}
            for e in Un:
                Se = sum(p0[t] for t in range(n) if e[t])
                F0[e] = [f for f in range(1 << (N - n))
                         if v2((Se + sum(p0[n + t] for t in range(N - n) if (f >> t) & 1)) % MOD) >= VN]
                if len(F0[e]) > 2 ** (N - n - r):
                    fails += 1; print("FAIL(c-size)", n, N, len(F0[e]), N - n - r)
            tot = 0
            for w in range(1 << R):
                xp = (x + (w << m)) % MOD
                q0, q1, q2 = evals(xp, N, P)
                Vp = sum(v2(xp + i) for i in range(1, N + 1))
                assert Vp == VN
                # (a) U_n unchanged at x'
                for e in bits:
                    Sx = sum(q0[t] for t in range(n) if e[t]) % MOD
                    if v2(Sx) < m:
                        fails += 1; print("FAIL(a-alive)")
                    if (v2(sum(q1[t] for t in range(n) if e[t]) % MOD) >= Thn) != (e in set(Un)):
                        fails += 1; print("FAIL(a-U)")
                cnt = 0
                for e in bits:
                    Se = sum(q0[t] for t in range(n) if e[t]); Spe = sum(q1[t] for t in range(n) if e[t])
                    for f in range(1 << (N - n)):
                        Sc = (Se + sum(q0[n + t] for t in range(N - n) if (f >> t) & 1)) % MOD
                        if v2(Sc) < VN:
                            if e in F0 and f in F0[e]:
                                fails += 1; print("FAIL(c-w-dependence)")
                            continue
                        if e in F0 and f not in F0[e]:
                            fails += 1; print("FAIL(c-w-dependence2)")
                        lamc = v2((Spe + sum(q1[n + t] for t in range(N - n) if (f >> t) & 1)) % MOD)
                        if lamc >= ThN:
                            cnt += 1
                            if e not in F0:
                                fails += 1; print("FAIL(a-closure)", n, N, slopes[e], Thn)
                tot += cnt
            avg = tot / (1 << R)
            bound = len(Un) * 2.0 ** ((N - n) - r - max(0, ThN - m - 1 - j))
            tests += 1
            if avg > bound + 1e-12:
                fails += 1; print("FAIL(d)", n, N, m, D, j, len(Un), avg, bound)
    print(f"class {res} mod {modu}: window tests with nonempty U_n = {tests} failures = {fails}")

if __name__ == "__main__":
    main()
