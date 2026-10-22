# Referee check (verify-logic, round 3): brute-force test of Prop 11.2, Thm 11.3(b),
# Thm 11.6 (Parseval form) and the inequality chain of Thm 11.7, directly from the
# definitions (paths, aliveness, slopes, frozen-state weights), at odd p.
# Written independently of the track code.  Usage: python3 check_window.py p n N L ntrials seed
import sys, random, itertools, cmath, math
from fractions import Fraction

def v(z, p):
    if z == 0: return 10**9
    k = 0
    while z % p == 0: z //= p; k += 1
    return k

def pis(x, N):
    pi = [1]; dpi = [0]
    for j in range(1, N + 1):
        pi.append(pi[-1] * (x + j)); dpi.append(dpi[-1] * (x + j) + pi[-2])
    return pi, dpi

def a_weight(x, n, lam, p, t):
    # a_n^{(lam)}(t) = P_{f in {0,1}^{p lam}} ( sum f_i pi_{n+i}/pi_n == t mod p^lam )
    if lam == 0: return Fraction(1)
    mod = p ** lam
    q = [1]
    for i in range(1, p * lam):
        q.append(q[-1] * (x + n + i))
    cnt = 0
    for f in itertools.product((0, 1), repeat=p * lam):
        if sum(fi * qi for fi, qi in zip(f, q)) % mod == t % mod: cnt += 1
    return Fraction(cnt, 2 ** (p * lam))

def population(x, n, L, p):
    """alive paths of length n with slope <= L: list of (e, lam, tau) ; plus V_n, M_n"""
    pi, dpi = pis(x, n)
    Vn = v(pi[n], p); Mn = max(v(x + i, p) for i in range(1, n + 1))
    out = []
    for bits in itertools.product((0, 1), repeat=n - 1):
        e = (1,) + bits
        S = sum(pi[j] for j in range(n) if e[j]); dS = sum(dpi[j] for j in range(n) if e[j])
        if v(S, p) >= Vn:
            lam = v(dS, p)
            if lam <= L:
                out.append((e, lam, taumod(S, pi[n], p, lam + 2), S, dS))
    return out, Vn, Mn, pi, dpi

def taumod(S, pin, p, k):
    V = v(pin, p); assert v(S, p) >= V
    u = pin // p ** V; mod = p ** k
    return (-(S // p ** V)) * pow(u, -1, mod) % mod

def rho(x, n, lam, tau, p):
    return p ** lam * a_weight(x, n, lam, p, tau % (p ** lam))

def main():
    p, n, N, L, ntr, seed = map(int, sys.argv[1:7])
    random.seed(seed)
    P = 60
    done = 0; tried = 0
    while done < ntr and tried < 20000:
        tried += 1
        x = random.randrange(p ** P)
        if (x + 1) % p == 0: continue
        pi, dpi = pis(x, N)
        m = v(pi[n], p); VN = v(pi[N], p); D = VN - m
        Mn = max(v(x + i, p) for i in range(1, n + 1)); MN = max(v(x + i, p) for i in range(1, N + 1))
        if not (N - n >= p * (L + 1) and D + L <= m - Mn and L < m - MN and MN < m): continue
        # parent population at the atom (computed at x0 = x mod p^m; check constancy at x too)
        x0 = x % p ** m
        par, Vn0, _, pi0, dpi0 = population(x0 + p ** (P - 5) * 7, n, L, p)  # some point of the atom
        if not par: continue
        parx, _, _, _, _ = population(x, n, L, p)
        assert sorted(e for e, *_ in par) == sorted(e for e, *_ in parx), "population not constant on atom"
        Mpar = Fraction(p ** m, 2 ** n) * sum(rho(x, n, lam, tau, p) for e, lam, tau, S, dS in parx)
        # children for each w
        tails = [random.randrange(p ** 20) for _ in range(2)]
        vals = []; perparent = {e: [] for e, *_ in par}
        for w in range(p ** D):
            res = []
            for z in tails:
                xp = x0 + p ** m * w + p ** (m + D) * z
                pi1, dpi1 = pis(xp, N)
                assert v(pi1[N], p) == VN and v(pi1[n], p) == m
                tot = Fraction(0); pp = {}
                for e, lam0, tau0, S0, dS0 in par:
                    Se = sum(pi1[j] for j in range(n) if e[j]); dSe = sum(dpi1[j] for j in range(n) if e[j])
                    assert v(Se, p) >= m and v(dSe, p) == lam0
                    Xe = Fraction(0)
                    for f in itertools.product((0, 1), repeat=N - n):
                        S = Se + sum(pi1[n + i] for i in range(N - n) if f[i])
                        if v(S, p) >= VN:
                            dS = dSe + sum(dpi1[n + i] for i in range(N - n) if f[i])
                            lam = v(dS, p)
                            assert lam == lam0, "child slope differs"
                            tauN = taumod(S, pi1[N], p, lam + 2)
                            Xe += rho(xp, N, lam, tauN, p)
                    pp[e] = Xe; tot += Xe
                res.append((tot, pp))
            assert res[0][0] == res[1][0], "child sum depends on digits above m+D"
            vals.append(res[0][0])
            for e in perparent: perparent[e].append(res[0][1][e])
        mean = sum(vals) / len(vals)
        Mnext_mean = Fraction(p ** (m + D), 2 ** N) * mean
        # Prop 11.2(iv) per parent
        for e, lam, tau, S, dS in parx:
            mu_e = sum(perparent[e]) / len(perparent[e])
            assert mu_e == Fraction(2 ** (N - n), p ** D) * rho(x, n, lam, tau, p), "11.2(iv) fails"
        # Thm 11.6 Parseval: Var = p^{-2D} sum_{eta != 0} |hat Sigma(eta)|^2
        Q = p ** D
        var = sum((vv - mean) ** 2 for vv in vals) / Q
        hat = [sum(float(vals[w]) * cmath.exp(-2j * math.pi * eta * w / Q) for w in range(Q)) for eta in range(Q)]
        var2 = sum(abs(h) ** 2 for h in hat[1:]) / Q ** 2
        # Thm 11.7 chain: M^2 R <= p^L kappa r_max 2^{-n} p^m M
        c = Fraction(p ** (m + D), 2 ** N)
        sumvar = Fraction(0); rmax = 0.0
        for e in perparent:
            arr = perparent[e]; mu = sum(arr) / Q
            ve = sum((a - mu) ** 2 for a in arr) / Q
            sumvar += ve
            if mu > 0: rmax = max(rmax, float(ve / mu ** 2))
        kappa = float(var / sumvar) if sumvar > 0 else 0.0
        lhs = float(c * c * var)
        rhs = p ** L * kappa * rmax * float(Fraction(p ** m, 2 ** n) * Mpar)
        print(f"p={p} n={n} N={N} L={L} m={m} D={D} Mn={Mn} MN={MN} |P|={len(par)} M_l={float(Mpar):.6g} "
              f"E[M_l+1]={float(Mnext_mean):.6g} equal={Mnext_mean == Mpar} Var={float(var):.6g} Parseval={var2:.6g} "
              f"M^2R={lhs:.4g} <= {rhs:.4g}: {lhs <= rhs * (1 + 1e-9)}")
        assert Mnext_mean == Mpar
        assert abs(float(var) - var2) <= 1e-9 * max(1.0, var2)
        assert lhs <= rhs * (1 + 1e-9) + 1e-300
        done += 1
    print("windows tested:", done, "of", tried, "draws")

main()
