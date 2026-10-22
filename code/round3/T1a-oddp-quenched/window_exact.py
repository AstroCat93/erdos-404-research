#!/usr/bin/env python3
"""Exact one-window computations for the odd-p quenched martingale (track T1a, round 3).

Setting (note.md Sec. 10.1 transferred to odd p; see writeup.md Sec. 2-4):
  x in Z_p (we use x mod p^P), pi_j(x) = (x+1)...(x+j), V_n = v_p(pi_n(x)), M_n = max_{i<=n} v_p(x+i).
  A path e = (e_0=1, e_1, ..., e_{n-1}) is alive at n iff p^{V_n} | S_e(x), S_e = sum e_j pi_j.
  Target tau_n(e) = -S_e(x)/pi_n(x); slope lambda_e = v_p(S_e'(x)).
  Frozen-state weight rho_n(e) = p^lambda * a_n^{(lambda)}(tau_n(e) mod p^lambda), where
  a_n^{(lambda)}(t) = P_{f in {0,1}^{p lambda}} ( sum_{i<p lambda} f_i pi_{n+i}/pi_n == t mod p^lambda ).
  Martingale value  M_n = 2^{-n} p^{V_n} sum_{e alive, lambda_e <= L} rho_n(e).

For a window [n, N) on the atom C = x + p^m Z_p (m = V_n, D = V_N - V_n), with x_w = x with digits
m..m+D-1 replaced by w (w = 0..p^D-1), this script computes EXACTLY (Fractions):
  (1) X_e(w) = sum_{children (e,f) alive at N for x_w} rho_N((e,f))   for every parent e with lambda_e <= L;
  (2) checks the first-moment identity  avg_w X_e(w) == 2^{N-n} p^{-D} rho_n(e)  (Prop. A(iii));
  (3) checks slope inheritance and constancy of the parent set / frozen states on the atom;
  (4) checks the affine-target representation X_e(w) = psi^{(lambda)}_{s_e}(theta_e - beta_e w)  (Prop. C),
      with psi built from the window map alone;
  (5) the second moment: E_w Sigma, E_w Sigma^2, Var_w Sigma, sum_e Var_w X_e, the correlation ratio,
      and the Fourier/Weyl-sum form of Var (Theorem C), checked numerically.
Usage: window_exact.py p seed trials n N P L [atomdigits]
"""
import sys, random, cmath, math
from fractions import Fraction
from collections import defaultdict

def vp(a, p, cap=10**9):
    if a == 0:
        return cap
    k = 0
    while a % p == 0:
        a //= p; k += 1
    return k

def alive_paths(x, n, p, P):
    """Bitmasks e (bit j = e_j, e_0 = 1) alive at n, by DFS on targets tau_j mod p^{P - V_j}."""
    ds = [vp(x + j + 1, p) for j in range(n)]
    us = [(x + j + 1) // p**ds[j] for j in range(n)]
    out = []
    stack = [(0, 0, P, 0)]
    while stack:
        j, tau, prec, mask = stack.pop()
        if j == n:
            out.append(mask); continue
        d = ds[j]
        assert prec - d > 0, "precision exhausted"
        mod_new = p ** (prec - d)
        for e in ((1,) if j == 0 else (0, 1)):
            t = (tau - e) % (p ** prec)
            if d and t % (p ** d):
                continue
            nt = ((t // p**d) * pow(us[j], -1, mod_new)) % mod_new
            stack.append((j + 1, nt, prec - d, mask | (e << j)))
    return out

def pis(x, n, MOD):
    """pi_j and pi_j' for j = 0..n, mod MOD."""
    pi = [1]; dpi = [0]
    for j in range(1, n + 1):
        pi.append(pi[-1] * (x + j) % MOD)
        dpi.append((dpi[-1] * (x + j) + pi[-2]) % MOD)
    return pi, dpi

def S_val(mask, arr, n, MOD):
    return sum(arr[j] for j in range(n) if (mask >> j) & 1) % MOD

def V(x, n, p):
    return sum(vp(x + i, p) for i in range(1, n + 1))

def Mx(x, n, p):
    return max(vp(x + i, p) for i in range(1, n + 1))

_adist_cache = {}
def a_dist(x, n, lam, p):
    """Distribution (dict residue -> Fraction) of sum_{i<p lam} f_i pi_{n+i}/pi_n mod p^lam."""
    key = (x % p**(lam + 1) if lam else 0, n, lam, p)   # products mod p^lam depend on x mod p^lam; keep safe margin
    # NOTE: the terms prod_{k=1}^{i}(x+n+k) mod p^lam depend only on x mod p^lam; key by x mod p^(lam+1) for safety.
    if key in _adist_cache:
        return _adist_cache[key]
    mod = p ** lam
    cnt = defaultdict(int); cnt[0] = 1
    prod = 1
    for i in range(p * lam):
        term = prod % mod               # pi_{n+i}/pi_n = prod_{k=1}^{i} (x+n+k)
        new = defaultdict(int)
        for r, c in cnt.items():
            new[r] += c
            new[(r + term) % mod] += c
        cnt = new
        prod = prod * (x + n + i + 1)
    tot = 2 ** (p * lam)
    res = {r: Fraction(c, tot) for r, c in cnt.items()}
    _adist_cache[key] = res
    return res

def rho(x, n, lam, tau, p):
    if lam == 0:
        return Fraction(1)
    return p**lam * a_dist(x, n, lam, p).get(tau % p**lam, Fraction(0))

def tau_lam(mask, x, n, p, P):
    """(tau_n(e,x) mod p^{P-V_n}, lambda_e) with lambda capped at P."""
    MOD = p ** P
    pi, dpi = pis(x, n, MOD)
    S = S_val(mask, pi, n, MOD); Sp = S_val(mask, dpi, n, MOD)
    Vn = vp(pi[n], p)
    assert vp(S, p, cap=P) >= Vn
    prec = P - Vn
    mod = p ** prec
    tau = (-(S // p**Vn) * pow(pi[n] // p**Vn, -1, mod)) % mod
    return tau, vp(Sp, p, cap=P)

def replace_digits(x, m, D, w, p):
    """x with p-adic digits m..m+D-1 replaced by the digits of w (0 <= w < p^D)."""
    low = x % p**m
    high = x // p**(m + D)
    return low + p**m * w + p**(m + D) * high

def window_check(x, n, N, p, P, L, rnd=None, verbose=True):
    m = V(x, n, p); VN = V(x, N, p); D = VN - m
    if D < 1 or VN + L + 2 > P:
        return None
    Mn = Mx(x, n, p); MN = Mx(x, N, p)
    conds = dict(W1=(N - n >= p * L), W2=(D + L <= m - Mn), W3=(L < m - MN), env=(MN < m))
    parents = alive_paths(x, n, p, P)
    if not parents:
        return None
    pinfo = {}
    for e in parents:
        tau, lam = tau_lam(e, x, n, p, P)
        if lam <= L:
            pinfo[e] = (lam, tau, rho(x, n, lam, tau, p))
    if not pinfo:
        return None
    x0 = x % p**m  # base point of the atom (representative with zero digits above m)
    # --- window map data at the base point x0 ---
    MODw = p ** (D + L)
    # y_j = pi_j(x0)/pi_n(x0) = prod_{i=n+1}^{j} (x0+i), j = n..N-1, as integers mod p^{D+L}
    ys = []; prod = 1
    for j in range(n, N):
        ys.append(prod % MODw)
        prod = prod * (x0 + j + 1)
    # window fibre counts q_f mod p^{D+L}: dict residue -> count (DP)
    cnt = defaultdict(int); cnt[0] = 1
    for y in ys:
        new = defaultdict(int)
        for r, c in cnt.items():
            new[r] += c; new[(r + y) % MODw] += c
        cnt = new
    # unit u = pi_N(x0)/(p^D pi_n(x0)) mod p^L  (needs L <= m - M_N for constancy on the atom)
    piN_over_pin = 1
    for i in range(n + 1, N + 1):
        piN_over_pin *= (x0 + i)
    assert vp(piN_over_pin, p) == D
    u_full = piN_over_pin // p**D
    # omega = pi_n(x0)/p^m
    pin0 = 1
    for i in range(1, n + 1):
        pin0 *= (x0 + i)
    omega = pin0 // p**m
    # --- brute force X_e(w) ---
    X = {e: [Fraction(0)] * p**D for e in pinfo}
    ok_inherit = True; ok_const = True
    for w in range(p ** D):
        xw = replace_digits(x, m, D, w, p)
        if w < 2:
            # parent set and frozen states constant on the atom
            if sorted(alive_paths(xw, n, p, P)) != sorted(parents):
                ok_const = False
            for e, (lam, tau, rh) in pinfo.items():
                t2, l2 = tau_lam(e, xw, n, p, P)
                if l2 != lam or (lam and (t2 - tau) % p**lam):
                    ok_const = False
        kids = alive_paths(xw, N, p, P)
        for c in kids:
            e = c % 2**n
            if e not in pinfo:
                continue
            lam = pinfo[e][0]
            tauN, lamN = tau_lam(c, xw, N, p, P)
            if lamN != lam:
                ok_inherit = False
            X[e][w] += rho(xw, N, lam, tauN, p)
    # --- (2) first-moment identity ---
    fm_ok = []
    for e, (lam, tau, rh) in pinfo.items():
        lhs = sum(X[e]) / p**D
        rhs = Fraction(2**(N - n), p**D) * rh
        fm_ok.append(lhs == rhs)
    # --- (4) affine representation X_e(w) = Psi^{(lam)}(tau0_e - p^lam beta_e w mod p^{D+lam}) ---
    # Psi^{(lam)}(t) = sum_f [t == q_f mod p^D] p^lam a_N(u^{-1}(t-q_f)/p^D mod p^lam)
    aN = {lam: a_dist(x0, N, lam, p) for lam in set(v[0] for v in pinfo.values())}
    def Psi(lam, t):
        modD = p ** D; modDl = p ** (D + lam)
        tot = Fraction(0)
        t %= modDl
        for r, c in cnt.items():
            r2 = r % modDl
            if (t - r2) % modD == 0:
                if lam == 0:
                    tot += c
                else:
                    z = ((t - r2) // modD) % p**lam
                    st = (z * pow(u_full, -1, p**lam)) % p**lam
                    tot += c * p**lam * aN[lam].get(st, Fraction(0))
        return tot
    aff_ok = True
    MODP = p ** P
    pi0, dpi0 = pis(x0, n, MODP)
    parent_data = {}
    for e, (lam, tau, rh) in pinfo.items():
        # tau0 = tau_n(e, x0) mod p^{D+lam}; beta = omega^{-1} S_e'(x0)/p^lam mod p^D
        S0 = S_val(e, pi0, n, MODP); Sp0 = S_val(e, dpi0, n, MODP)
        tau0 = (-(S0 // p**m) * pow(omega, -1, p**(P - m))) % p**(P - m)
        assert vp(Sp0, p, cap=P) == lam
        beta = ((Sp0 // p**lam) * pow(omega, -1, p**D)) % p**D
        modDl = p ** (D + lam)
        s_e = tau0 % p**lam
        theta = ((tau0 - s_e) // p**lam) % p**D
        parent_data[e] = (lam, s_e, theta, beta)
        for w in range(p ** D):
            t = (tau0 - p**lam * beta * w) % modDl
            if Psi(lam, t) != X[e][w]:
                aff_ok = False
    # --- (5) second moment ---
    pD = p ** D
    Sigma = [sum(X[e][w] for e in pinfo) for w in range(pD)]
    ES = sum(Sigma) / pD
    ES2 = sum(s * s for s in Sigma) / pD
    VarS = ES2 - ES * ES
    sumVar = Fraction(0)
    for e in pinfo:
        me = sum(X[e]) / pD
        sumVar += sum(v * v for v in X[e]) / pD - me * me
    # Fourier form: Var = p^{-2D} sum_{eta != 0} | sum_e Xhat_e(eta) |^2
    fourier_var = 0.0
    for eta in range(1, pD):
        tot = 0j
        for e in pinfo:
            tot += sum(float(X[e][w]) * cmath.exp(-2j * math.pi * eta * w / pD) for w in range(pD))
        fourier_var += abs(tot) ** 2
    fourier_var /= pD ** 2
    # per-order breakdown of the variance: order p^d  <->  eta with v_p(eta) = D - d
    by_order = defaultdict(float)
    for eta in range(1, pD):
        d = D - vp(eta, p)
        tot = 0j
        for e in pinfo:
            tot += sum(float(X[e][w]) * cmath.exp(-2j * math.pi * eta * w / pD) for w in range(pD))
        by_order[d] += abs(tot) ** 2 / pD ** 2
    # Weyl sums of parent 'Newton roots' w*_e = theta_e/beta_e at order p^d, slope-0 parents only
    weyl = {}
    slope0 = [e for e in pinfo if parent_data[e][0] == 0]
    for d in range(1, D + 1):
        best = 0.0
        for eta in range(1, p ** d):
            if eta % p == 0:
                continue
            s = sum(cmath.exp(2j * math.pi * eta * (parent_data[e][2] * pow(parent_data[e][3], -1, p**d)) / p**d) for e in slope0)
            best = max(best, abs(s))
        weyl[d] = best / max(1, len(slope0))
    res = dict(n=n, N=N, m=m, D=D, Mn=Mn, MN=MN, conds=conds, nparents=len(parents), nL=len(pinfo),
               lams=sorted(set(v[0] for v in pinfo.values())), fm_ok=all(fm_ok), n_fm=len(fm_ok),
               inherit=ok_inherit, const=ok_const, aff_ok=aff_ok,
               Mn_val=Fraction(p**m, 2**n) * sum(v[2] for v in pinfo.values()),
               EMN=Fraction(p**VN, 2**N) * ES, ES=ES, VarS=VarS, sumVar=sumVar,
               relvar=(VarS / (ES * ES) if ES else None), fourier_var=fourier_var,
               by_order=dict(by_order), weyl=weyl, nslope0=len(slope0))
    return res

if __name__ == "__main__":
    p = int(sys.argv[1]); seed = int(sys.argv[2]); trials = int(sys.argv[3])
    n = int(sys.argv[4]); N = int(sys.argv[5]); P = int(sys.argv[6]); L = int(sys.argv[7])
    atom = sys.argv[8] if len(sys.argv) > 8 else None   # e.g. "0mod3" : force x = r mod p^k
    rnd = random.Random(seed)
    done = 0; tries = 0
    tot_fm = 0; tot_ok = 0
    while done < trials and tries < 20000:
        tries += 1
        x = rnd.randrange(p ** P)
        if atom:
            r, k = atom.split("mod"); r = int(r); k = int(k)
            x = x - x % k + r
        if x % p == p - 1:
            continue  # g = 0 class (Phi_p contains p-1): no alive paths
        res = window_check(x, n, N, p, P, L)
        if res is None:
            continue
        done += 1
        tot_fm += res['n_fm']; tot_ok += res['n_fm'] if res['fm_ok'] else 0
        print(f"x#{done} x%p^4={x % p**4} m={res['m']} D={res['D']} M_n={res['Mn']} M_N={res['MN']} conds={res['conds']} "
              f"parents={res['nparents']} (lam<=L: {res['nL']}, slope0: {res['nslope0']}) lams={res['lams']} "
              f"firstmoment={res['fm_ok']} inherit={res['inherit']} const={res['const']} affine={res['aff_ok']}")
        print(f"    M_n={float(res['Mn_val']):.6f} E[M_N]={float(res['EMN']):.6f} (equal: {res['Mn_val']==res['EMN']})  "
              f"E Sigma={float(res['ES']):.4f} Var Sigma={float(res['VarS']):.4f} sum_e Var X_e={float(res['sumVar']):.4f} "
              f"corr-ratio={float(res['VarS']/res['sumVar']) if res['sumVar'] else float('nan'):.4f} "
              f"relvar={float(res['relvar']) if res['relvar'] is not None else float('nan'):.5f} 1/nL={1/res['nL']:.5f} "
              f"fourier={res['fourier_var']:.6f} (exact {float(res['VarS']):.6f})")
        print(f"    Var by order p^d: " + ", ".join(f"d={d}:{v:.4f}" for d, v in sorted(res['by_order'].items())) +
              "   | normalised Weyl sums of slope-0 Newton roots: " + ", ".join(f"d={d}:{v:.3f}" for d, v in sorted(res['weyl'].items())))
    print(f"TOTAL first-moment identities exact: {tot_ok}/{tot_fm}")
