#!/usr/bin/env python3
"""Per-parent exact check of the one-window identity (p = 2).

For x (even, random 2-adic digits), time n, window end N, with m = V_n(x), D = V_N - V_n:
for every path e alive at n with lambda_e = v(S_e'(x)) <= D, check (exactly, with Fractions)
   avg_{w mod 2^D}  sum_{children e' of e alive at N}  rho_N(e')  ==  2^{W_N - W_n} * rho_n(e),
where x_w = (x mod 2^m) + 2^m w + (x >> (m+D)) << (m+D), and also check
   * lambda_{e'} == lambda_e for every child (inheritance),
   * the alive set at n and tau_n(e) mod 2^lambda_e do not depend on w,
   * the children's states tau_N(e') mod 2^lambda are equidistributed in expectation.
Usage: mart_check2.py seed trials n N P
"""
import random, sys
from fractions import Fraction
from collections import defaultdict

def v2(a):
    if a == 0:
        return 10**9
    return (a & -a).bit_length() - 1

def pis(x, n, MOD):
    p = [1]; dp = [0]
    for j in range(1, n + 1):
        p.append(p[-1] * (x + j) % MOD)
        dp.append((dp[-1] * (x + j) + p[-2]) % MOD)
    return p, dp

def alive_paths(x, n, P):
    """List of bitmasks e (bit j = e_j) alive at n, via DFS on tau."""
    ds = [v2(x + j + 1) for j in range(n)]
    us = [((x + j + 1) >> ds[j]) for j in range(n)]
    out = []
    stack = [(0, 0, P, 0)]
    while stack:
        j, tau, prec, mask = stack.pop()
        if j == n:
            out.append(mask); continue
        d = ds[j]
        for e in ((1,) if j == 0 else (0, 1)):
            t = (tau - e) % (1 << prec)
            if d and (t & ((1 << d) - 1)):
                continue
            np_ = prec - d
            assert np_ > 0
            nt = ((t >> d) * pow(us[j], -1, 1 << np_)) % (1 << np_)
            stack.append((j + 1, nt, np_, mask | (e << j)))
    return out

def S_val(mask, p, n, MOD):
    s = 0
    for j in range(n):
        if (mask >> j) & 1:
            s += p[j]
    return s % MOD

def V(x, n):
    return sum(v2(x + i) for i in range(1, n + 1))

def mu(x, n):
    return max(v2(x + i) for i in range(1, n + 1))

def tail_dist(x, n, lam):
    """distribution of Q_f mod 2^lam, Q_f = sum_{j>=n} f_j (x+n+1)...(x+j)."""
    mod = 1 << lam
    terms = []; prod = 1
    for j in range(n, n + 2 * lam):
        terms.append(prod % mod); prod = prod * (x + j + 1) % mod
    dist = defaultdict(int)
    k = len(terms)
    for f in range(1 << k):
        s = 0
        for i in range(k):
            if (f >> i) & 1:
                s += terms[i]
        dist[s % mod] += 1
    return {r: Fraction(c, 1 << k) for r, c in dist.items()}

def rho(x, n, lam, tau):
    if lam == 0:
        return Fraction(1)
    return (1 << lam) * tail_dist(x, n, lam).get(tau % (1 << lam), Fraction(0))

def tau_of(mask, x, n, P):
    MOD = 1 << P
    p, dp = pis(x, n, MOD)
    S = S_val(mask, p, n, MOD); Sp = S_val(mask, dp, n, MOD)
    Vn = v2(p[n])
    assert v2(S) >= Vn
    prec = P - Vn
    tau = (-(S >> Vn) * pow(p[n] >> Vn, -1, 1 << prec)) % (1 << prec)
    return tau, v2(Sp)

def check(x, n, N, P, DMAX):
    m = V(x, n); VN = V(x, N); D = VN - m
    if D > DMAX or D < 1:
        return None
    mun = mu(x, n); muN = mu(x, N)
    Wn = n - m; WN = N - VN
    parents = alive_paths(x, n, P)
    if not parents:
        return None
    x0 = x % (1 << m); rest = x >> (m + D)
    pinfo = {}
    for e in parents:
        tau, lam = tau_of(e, x, n, P)
        if lam <= D:
            pinfo[e] = (lam, tau % (1 << lam), rho(x, n, lam, tau))
    if not pinfo:
        return None
    acc = defaultdict(Fraction)
    states = defaultdict(lambda: defaultdict(int))
    ok_inherit = True; ok_const = True
    for w in range(1 << D):
        xw = x0 + (w << m) + (rest << (m + D))
        if w < 3:
            if sorted(alive_paths(xw, n, P)) != sorted(parents):
                ok_const = False
        kids = alive_paths(xw, N, P)
        for c in kids:
            e = c & ((1 << n) - 1)
            if e not in pinfo:
                continue
            lam, tmod, rh = pinfo[e]
            tauN, lamN = tau_of(c, xw, N, P)
            if lamN != lam:
                ok_inherit = False
            acc[e] += rho(xw, N, lam, tauN)
            states[e][tauN % (1 << lam) if lam else 0] += 1
        if w < 3:
            for e, (lam, tmod, rh) in pinfo.items():
                t2, l2 = tau_of(e, xw, n, P)
                if l2 != lam or (lam and t2 % (1 << lam) != tmod):
                    ok_const = False
    res = []
    for e, (lam, tmod, rh) in pinfo.items():
        lhs = acc[e] / (1 << D)
        rhs = Fraction(2) ** (WN - Wn) * rh
        st = states[e]
        unif = (len(set(st.values())) <= 1 and (len(st) == (1 << lam) or len(st) == 0))
        res.append((lam, lhs == rhs, unif, lhs, rhs))
    conds = dict(lin=D + max(l for l, _, _ in pinfo.values()) <= m - mun,
                 inherit=max(l for l, _, _ in pinfo.values()) < m - muN, env=muN < m)
    return dict(n=n, N=N, m=m, D=D, mun=mun, muN=muN, res=res, ok_inherit=ok_inherit,
                ok_const=ok_const, conds=conds)

if __name__ == "__main__":
    seed, trials, n, N, P = (int(a) for a in sys.argv[1:6])
    DMAX = int(sys.argv[6]) if len(sys.argv) > 6 else 10
    rnd = random.Random(seed)
    tot = good = 0; lamhist = defaultdict(int); allconds = 0
    done = 0; tries = 0
    while done < trials and tries < 100000:
        tries += 1
        x = rnd.getrandbits(P) & ~1
        r = check(x, n, N, P, DMAX)
        if r is None:
            continue
        done += 1
        for lam, eq, unif, lhs, rhs in r['res']:
            tot += 1; good += eq; lamhist[lam] += 1
            if not eq or not unif:
                print("MISMATCH/NONUNIF", r['n'], r['N'], r['m'], r['D'], lam, eq, unif, lhs, rhs, r['conds'])
        print(f"x#{done}: m={r['m']} D={r['D']} mu_n={r['mun']} mu_N={r['muN']} parents(lam<=D)={len(r['res'])} "
              f"lams={sorted(set(l for l,_,_,_,_ in r['res']))} all_eq={all(q for _,q,_,_,_ in r['res'])} "
              f"inherit={r['ok_inherit']} G-meas={r['ok_const']} conds={r['conds']}", flush=True)
    print(f"TOTAL parent identities exact: {good}/{tot}; lambda histogram {dict(lamhist)}")
