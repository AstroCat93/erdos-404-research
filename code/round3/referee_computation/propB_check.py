#!/usr/bin/env python3
"""Round-3 computational referee: exact re-check of R3M Proposition B (note Proposition 11.11)
at p = 5 on small windows.  Written from the statement in data/round3/reports/R3M.md section 3;
no R3M or checker code is used.

For a configuration (x0, n, N) with m = V_n(x0), D = V_N(x0) - m, (W2') D <= m - M_n, (W3') M_N < m:
  * P = P^0_n(x0): all paths e (e_0 = 1, length n) alive at n with slope v(S_e'(x0)) = 0.
  * BRUTE FORCE, from scratch: for every integer w in [0, p^(D+1)) and x' = x0 + p^m w, count
    children #{f in {0,1}^(N-n): v(S_(e,f)(x')) >= V_N(x')} for every e in P (exact integers).
  * (i)  the count equals m_W(tau0_e - beta_e w mod p^D), with m_W(r) = #{f : Q_f(x0) = r mod p^D},
         tau0_e = -S_e(x0)/pi_n(x0) mod p^D, beta_e = omega^-1 S_e'(x0) mod p^D, omega = pi_n(x0)/p^m;
         and it depends on w only mod p^D.
  * (ii) E_C Y = |P| T p^-D  (exact),   E_C[Y^2] = p^-2D sum_eta |A(eta)|^2  (A by an explicit DFT
         in 50-digit mpmath; the left side is an exact rational), and
         Var_C(c_N Y) = c_n^2 sum_{eta != 0} |sum_e muhat(eta/beta_e) e(eta phi_e / p^D)|^2 <= M^2 chi_W^2.
"""
import sys, itertools, time, random
from fractions import Fraction as Fr
import mpmath as mp

mp.mp.dps = 50
p = 5


def vp(x):
    if x == 0:
        return 10 ** 9
    k = 0
    while x % p == 0:
        x //= p
        k += 1
    return k


def pi_list(x, n):
    out, q = [1], 1
    for i in range(1, n + 1):
        q *= (x + i)
        out.append(q)
    return out           # out[j] = pi_j(x), j = 0..n


def deriv_pi(x, j):
    """pi_j'(x) by the product rule, exact."""
    tot = 0
    for k in range(1, j + 1):
        prod = 1
        for i in range(1, j + 1):
            if i != k:
                prod *= (x + i)
        tot += prod
    return tot


def slope0_population(x0, n, m, pD):
    """All slope-0 paths alive at n.  Enumerated by depth-first search with pruning: by backward
    integrality (F2) a path alive at n is alive at every j <= n, i.e. v(S_{e|j}) >= V_j."""
    P = pi_list(x0, n)
    Vs = [vp(q) for q in P]
    dpi = [deriv_pi(x0, j) for j in range(n)]
    omega = P[n] // p ** m
    oinv = pow(omega, -1, pD)
    pop = []
    stack = [(1, (1,), P[0], dpi[0])]
    while stack:
        j, e, S, Sd = stack.pop()
        if j == n:
            if vp(S) >= m and Sd % p != 0:
                tau0 = (-(S // p ** m) * oinv) % pD
                beta = (oinv * Sd) % pD
                phi = (tau0 * pow(beta, -1, pD)) % pD
                pop.append((e, S, tau0, beta, phi))
            continue
        for b in (0, 1):
            S2 = S + b * P[j]
            if vp(S2) >= Vs[j + 1] or j + 1 == n and vp(S2) >= m:
                stack.append((j + 1, e + (b,), S2, Sd + b * dpi[j]))
    pop.sort()
    return pop


def find_configs(rng, want, per_D=2, maxpop=60):  # noqa: C901
    """Random search for windows satisfying (W2'), (W3') with D in want, a slope-0 population of
    size 2..maxpop, and at least two distinct beta_e mod p^D (so that Prop. B(ii) is not just (iii))."""
    out = []
    tries = 0
    while any(sum(1 for c in out if c[3] == D) < per_D for D in want) and tries < 60000:
        tries += 1
        n = rng.randrange(9, 22)
        N = n + rng.randrange(5, 11)
        x0 = rng.randrange(0, 5 ** 7)
        P = pi_list(x0, N)
        m = vp(P[n])
        D = vp(P[N]) - m
        Mn = max(vp(x0 + i) for i in range(1, n + 1))
        MN = max(vp(x0 + i) for i in range(1, N + 1))
        if not (D in want and D <= m - Mn and MN < m):
            continue
        if sum(1 for c in out if c[3] == D) >= per_D:
            continue
        x0 %= p ** m
        pop = slope0_population(x0, n, m, p ** D)
        if not (2 <= len(pop) <= maxpop) or len({b for (_, _, _, b, _) in pop}) < 2:
            continue
        if len(pop) * 2 ** (N - n) * p ** (D + 1) > 4_000_000:      # keep the brute force small
            continue
        out.append((x0, n, N, D))
    return out


def run(x0, n, N):
    t0 = time.time()
    P = pi_list(x0, N)
    m = vp(P[n]); D = vp(P[N]) - m
    Mn = max(vp(x0 + i) for i in range(1, n + 1)); MN = max(vp(x0 + i) for i in range(1, N + 1))
    assert 1 <= D <= m - Mn and MN < m
    pD = p ** D
    T = 2 ** (N - n)
    pop = slope0_population(x0, n, m, pD)
    if len(pop) == 0:
        return None
    # window law m_W
    mW = [0] * pD
    for f in itertools.product((0, 1), repeat=N - n):
        q = sum(P[n + k] // P[n] for k in range(N - n) if f[k]) % pD
        mW[q] += 1
    # brute-force child counts at x' = x0 + p^m w, w in [0, p^(D+1))
    mism_i = 0
    Yw = {}
    for w in range(p ** (D + 1)):
        xp = x0 + p ** m * w
        Pp = pi_list(xp, N)
        VN = vp(Pp[N])
        Y = 0
        for (e, _, tau0, beta, phi) in pop:
            Se = sum(Pp[j] for j in range(n) if e[j])
            cnt = 0
            for f in itertools.product((0, 1), repeat=N - n):
                s = Se + sum(Pp[n + k] for k in range(N - n) if f[k])
                if vp(s) >= VN:
                    cnt += 1
            pred = mW[(tau0 - beta * w) % pD]
            mism_i += (cnt != pred)
            Y += cnt
        Yw[w] = Y
    dep_ok = all(Yw[w] == Yw[w % pD] for w in Yw)
    Ys = [Yw[w] for w in range(pD)]
    EY = Fr(sum(Ys), pD)
    EY2 = Fr(sum(y * y for y in Ys), pD)
    ok_mean = EY == Fr(len(pop) * T, pD)
    # spectral side
    zeta = [mp.e ** (-2j * mp.pi * k / pD) for k in range(pD)]       # e(-k/p^D)
    mhat = [mp.fsum(mW[r] * zeta[(r * xi) % pD] for r in range(pD)) for xi in range(pD)]
    tot = mp.mpf(0)
    tot_nz = mp.mpf(0)
    for eta in range(pD):
        A = mp.mpc(0)
        for (_, _, _, beta, phi) in pop:
            A += mhat[(eta * pow(beta, -1, pD)) % pD] * zeta[(-eta * phi) % pD]     # e(+eta phi / p^D)
        a2 = abs(A) ** 2
        tot += a2
        if eta:
            tot_nz += a2
    rhs = tot / pD ** 2
    err2 = abs(rhs - mp.mpf(EY2.numerator) / EY2.denominator)
    # variance identity, with c_n = 2^-n p^m, c_N = 2^-N p^(m+D)
    cn = Fr(p ** m, 2 ** n); cN = Fr(p ** (m + D), 2 ** N)
    var_exact = cN ** 2 * (EY2 - EY ** 2)
    var_spec = (mp.mpf(cn.numerator) / cn.denominator) ** 2 * tot_nz / T ** 2
    err_var = abs(var_spec - mp.mpf(var_exact.numerator) / var_exact.denominator)
    chi2 = Fr(pD * sum(c * c for c in mW), T * T) - 1
    Mval = cn * len(pop)
    cs_ok = var_exact <= Mval ** 2 * chi2
    nbeta = len({b for (_, _, _, b, _) in pop})
    print("config x0=%d n=%d N=%d: m=%d D=%d M_n=%d M_N=%d |P^0_n|=%d distinct beta mod p^D=%d T=%d" %
          (x0, n, N, m, D, Mn, MN, len(pop), nbeta, T))
    print("  (i) child counts vs m_W(tau0 - beta w): %d mismatches over %d (e,w) pairs; Y depends on w mod p^D only: %s"
          % (mism_i, len(pop) * p ** (D + 1), dep_ok))
    print("  (ii) E_C Y = %s, |P| T p^-D = %s : %s" % (EY, Fr(len(pop) * T, pD), ok_mean))
    print("       E_C[Y^2] = %s (exact) ; p^-2D sum|A|^2 = %s ; |diff| = %s" % (EY2, mp.nstr(rhs, 30), mp.nstr(err2, 5)))
    print("       Var_C(c_N Y) = %s (exact = %.15g) ; spectral = %s ; |diff| = %s"
          % (var_exact, float(var_exact), mp.nstr(var_spec, 20), mp.nstr(err_var, 5)))
    print("       chi_W^2 = %s ; M^2 chi_W^2 = %.15g ; Var <= M^2 chi^2: %s ; ratio Var/(M^2 chi^2) = %.6f"
          % (chi2, float(Mval ** 2 * chi2), cs_ok, float(var_exact / (Mval ** 2 * chi2)) if chi2 else float('nan')))
    print("  time %.1fs" % (time.time() - t0), flush=True)
    return mism_i == 0 and dep_ok and ok_mean and err2 < mp.mpf(10) ** -30 and err_var < mp.mpf(10) ** -30 and cs_ok


# Configurations: the first four were found by find_configs(random.Random(5), {2, 3}) in two
# versions of the search (n ranges 9..16 and 9..21); the D = 3 one by a systematic scan over
# x0 < 5^5, 10 <= n < 22, n+4 <= N < n+10 (first hit).  All are re-validated in run().
CONFIGS = [(80, 15, 22), (565, 16, 25), (561, 17, 27), (335, 16, 25), (100, 20, 25)]


def main():
    allok = True
    for (x0, n, N) in CONFIGS:
        r = run(x0, n, N)
        if r is None:
            print("config x0=%d n=%d N=%d: empty slope-0 population, skipped" % (x0, n, N))
            continue
        allok &= r
    print("RESULT", "PASS" if allok else "FAIL")


if __name__ == "__main__":
    main()
