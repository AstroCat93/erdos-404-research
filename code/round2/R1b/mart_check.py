#!/usr/bin/env python3
"""Exact numerical check of the window martingale identity (p = 2).

Notation (see notes in this directory):
  x in Z_2 even, represented by an integer mod 2^P (P large).
  pi_j(x) = (x+1)...(x+j), V_n = v(pi_n(x)), W_n = n - V_n.
  A path e in {0,1}^n with e_0 = 1 is alive at n iff 2^{V_n} | S_e(x) = sum_{j<n} e_j pi_j(x).
  tau_n(e) = -S_e(x)/pi_n(x) in Z_2;  lambda_e = v(S_e'(x)), S_e' = sum_j e_j pi_j'(x).
  rho_n(e) = 2^lambda * P_f( Q_f(x) == tau_n(e) mod 2^lambda ),
     Q_f = sum_{j>=n} f_j (x+n+1)...(x+j)   (only the first 2*lambda terms matter mod 2^lambda).
  M_n = 2^{-W_n} * sum_{e alive at n, lambda_e <= L} rho_n(e).

Claim checked: with m = V_n, D = V_N - V_n, conditioning on x mod 2^m and averaging over the
digits w = (x >> m) mod 2^D, the average of M_N equals M_n exactly (Fractions), provided the
window conditions hold (D >= L, D + L <= m - mu_n, L < V_n - mu_N, mu_N < m).
"""
import random, sys
DMAX = 11
from fractions import Fraction

def v2(a):
    if a == 0:
        return 10**9
    return (a & -a).bit_length() - 1

def alive(x, n, P):
    """Return list of (tau_n mod 2^{P-V_n}, Sprime mod 2^P) over alive paths at time n."""
    MOD = 1 << P
    # precompute pi_j, pi'_j mod 2^P for j < n
    pis = [1]; dps = [0]
    for j in range(1, n):
        pis.append(pis[-1] * (x + j) % MOD)
        dps.append((dps[-1] * (x + j) + pis[-2]) % MOD)
    ds = [v2(x + j + 1) for j in range(n)]          # ds[j] = v(x+j+1)
    us = [((x + j + 1) >> ds[j]) for j in range(n)]
    out = []
    # DFS: state (j, tau_j mod 2^prec, prec, Sprime)
    stack = [(0, 0, P, 0)]
    while stack:
        j, tau, prec, sp = stack.pop()
        if j == n:
            out.append((tau, sp, prec))
            continue
        d = ds[j]
        for e in ((1,) if j == 0 else (0, 1)):
            t = (tau - e) % (1 << prec)
            if d > 0 and (t & ((1 << d) - 1)):
                continue
            nprec = prec - d
            if nprec <= 0:
                raise RuntimeError("precision exhausted")
            nt = ((t >> d) * pow(us[j], -1, 1 << nprec)) % (1 << nprec)
            nsp = (sp + e * dps[j]) % MOD
            stack.append((j + 1, nt, nprec, nsp))
    return out

def V(x, n):
    return sum(v2(x + i) for i in range(1, n + 1))

def mu(x, n):
    return max(v2(x + i) for i in range(1, n + 1))

def rho(x, n, lam, tau):
    if lam == 0:
        return Fraction(1)
    mod = 1 << lam
    terms = []
    prod = 1
    for j in range(n, n + 2 * lam):
        terms.append(prod % mod)
        prod = prod * (x + j + 1) % mod
    cnt = 0
    k = len(terms)
    for f in range(1 << k):
        s = 0
        for i in range(k):
            if (f >> i) & 1:
                s += terms[i]
        if (s - tau) % mod == 0:
            cnt += 1
    return Fraction(cnt * (1 << lam), 1 << k)

def Mval(x, n, L, P):
    pops = alive(x, n, P)
    Wn = n - V(x, n)
    tot = Fraction(0)
    nlow = 0; nhigh = 0
    lams = []
    for tau, sp, prec in pops:
        lam = v2(sp)
        lams.append(lam)
        if lam <= L:
            nlow += 1
            tot += rho(x, n, lam, tau)
        else:
            nhigh += 1
    return tot / Fraction(2) ** Wn if Wn >= 0 else tot * 2 ** (-Wn), nlow, nhigh, lams

def check(x, n, N, L, P, verbose=True):
    m = V(x, n); VN = V(x, N); D = VN - m
    mun = mu(x, n); muN = mu(x, N)
    if D > DMAX:
        raise RuntimeError(f"D={D} too large")
    conds = dict(D_ge_L=D >= L, lin=D + L <= m - mun, inherit=L < m - muN, env=muN < m)
    Mn, nlow, nhigh, lams = Mval(x, n, L, P)
    x0 = x % (1 << m)
    rest = x >> (m + D)
    acc = Fraction(0)
    Mn_vals = set()
    for w in range(1 << D):
        xw = x0 + (w << m) + (rest << (m + D))
        MN, _, _, _ = Mval(xw, N, L, P)
        acc += MN
        if w < 4:
            Mn_vals.add(Mval(xw, n, L, P)[0])
    avg = acc / (1 << D)
    if verbose:
        print(f"n={n} N={N} m=V_n={m} D={D} mu_n={mun} mu_N={muN} conds={conds} "
              f"alive(lam<=L)={nlow} alive(lam>L)={nhigh} lam-hist={sorted(set(lams))}")
        print(f"   M_n={Mn} (={float(Mn):.6f})  avg_w M_N={avg} (={float(avg):.6f})  "
              f"equal={Mn == avg}  M_n const over w: {len(Mn_vals) == 1}")
    return Mn == avg, all(conds.values())

if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    N = int(sys.argv[4]) if len(sys.argv) > 4 else 48
    L = int(sys.argv[5]) if len(sys.argv) > 5 else 3
    rnd = random.Random(seed)
    P = int(sys.argv[6]) if len(sys.argv) > 6 else 256
    ok = 0; tot = 0; okc = 0
    for t in range(trials):
        x = rnd.getrandbits(P) & ~1
        try:
            eq, conds = check(x, n, N, L, P)
        except RuntimeError as ex:
            print("skip", ex); continue
        tot += 1; ok += eq; okc += (eq or not conds)
    print(f"equalities {ok}/{tot}")
