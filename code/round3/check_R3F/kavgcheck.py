"""kavgcheck.py -- independent re-computation of R3F C1-C4 (check of R3F, round 3).  Shares no code with kavg_l2.py.

For (p, t, H): c = v_p((H-1)!), M = t + c, classes K' mod p^c (units only; one class if c = 0).
 per class: y_i(K') = prod_{s<=i} (p^t K' - (H-s)) mod p^M; exact subset-sum counts mod p^M (numpy int64 DP);
            failing = some residue has count 0; Coll_d = sum_r c_d(r)^2 (exact, split into 20-bit halves);
            Q_d = (p^d Coll_d - p^{d-1} Coll_{d-1}) / 4^H  (Fraction);  CS(K') = sum_d sqrt(N_d Q_d(K'));
            L2(K') = sum_d Q_d.
 C3 bound = sum_d sqrt(N_d * mean_units Q_d).
 C1 check: y_i(K') == sigma_i + p^t K' tau_i  (mod p^{t+c}) for all classes (sigma, tau by the recursion
           sigma_i = -(H-i) sigma_{i-1}, tau_i = sigma_{i-1} - (H-i) tau_{i-1}).
 C2 check (H <= 30 only, int64 range): for every s = 0..c, with d = t+s,
           mean over ALL K' mod p^c of p^d P(sum delta_i y_i(K') = 0 mod p^d)   [per-class collision counts]
        == p^t E_delta[ p^{v_s} 1(p^{t+v_s} | A) ],  v_s = min(v_p(B), s)          [joint lazy walk (A, B)]
usage: python3 -I kavgcheck.py p t H [p t H ...]
"""
import sys
import time
from fractions import Fraction
from math import gcd

import numpy as np
import mpmath


def vp_fact(n, p):
    s, q = 0, p
    while q <= n:
        s += n // q
        q *= p
    return s


def window(p, t, H, Kp, M):
    mod = p ** M
    X = p ** t * Kp
    ys, y = [], 1
    for i in range(H):
        if i > 0:
            y = y * (X - (H - i)) % mod
        ys.append(y % mod)
    return ys


def subset_counts(ys, mod):
    c = np.zeros(mod, dtype=np.int64)
    c[0] = 1
    for y in ys:
        c = c + np.roll(c, y % mod)
    return c


def sumsq(c):
    hi = c >> 20
    lo = c & ((1 << 20) - 1)
    tot = 0
    for a in range(0, len(c), 1 << 18):
        h, l = hi[a:a + (1 << 18)], lo[a:a + (1 << 18)]
        tot += (int((h * h).sum()) << 40) + (int((h * l).sum()) << 21) + int((l * l).sum())
    return tot


def per_class(p, t, H, Kp, M):
    mod = p ** M
    c = subset_counts(window(p, t, H, Kp, M), mod)
    fail = bool((c == 0).any())
    coll = {M: sumsq(c)}
    for d in range(M - 1, -1, -1):
        cd = c.reshape(-1, p ** d).sum(axis=0) if d > 0 else np.array([c.sum()])
        coll[d] = sumsq(cd)
    Q = {d: Fraction(p ** d * coll[d] - p ** (d - 1) * coll[d - 1], 4 ** H) for d in range(1, M + 1)}
    return fail, Q


def c2_check(p, t, H):
    c = vp_fact(H - 1, p)
    M = t + c
    # sigma, tau
    sig, tau = [1], [0]
    for i in range(1, H):
        sig.append(-(H - i) * sig[-1])
        tau.append(sig[-2] - (H - i) * tau[-1])
    # C1
    ok1 = True
    for Kp in range(p ** c):
        ys = window(p, t, H, Kp, M)
        for i in range(H):
            if (ys[i] - sig[i] - p ** t * Kp * tau[i]) % p ** M != 0:
                ok1 = False
    res = {'C1': ok1}
    if H > 30:
        return res
    # LHS: mean over all K' mod p^c of p^d P(... = 0 mod p^d), via lazy-walk distribution mod p^M per class
    lhs = {}
    for s in range(0, c + 1):
        lhs[s] = Fraction(0)
    for Kp in range(p ** c):
        ys = window(p, t, H, Kp, M)
        w = np.zeros(p ** M, dtype=np.int64); w[0] = 1
        for y in ys:
            w = 2 * w + np.roll(w, y) + np.roll(w, -y)
        for s in range(0, c + 1):
            d = t + s
            hit = int(w.reshape(-1, p ** d)[:, 0].sum())
            lhs[s] += Fraction(p ** d * hit, 4 ** H)
    for s in lhs:
        lhs[s] /= p ** c
    # RHS: joint lazy walk (A mod p^M, B mod p^c)
    PA, PB = p ** M, p ** c
    J = np.zeros((PA, PB), dtype=np.int64); J[0, 0] = 1
    for i in range(H):
        a, b = sig[i] % PA, tau[i] % PB
        J = 2 * J + np.roll(np.roll(J, a, axis=0), b, axis=1) + np.roll(np.roll(J, -a, axis=0), -b, axis=1)
    rhs = {}
    Bs = np.arange(PB)
    vB = np.array([c if b == 0 else min(c, next(k for k in range(c + 1) if b % p ** (k + 1) != 0)) for b in Bs])
    for s in range(0, c + 1):
        tot = Fraction(0)
        vs = np.minimum(vB, s)
        for v in range(0, s + 1):
            cols = (vs == v)
            mask_rows = (np.arange(PA) % p ** (t + v) == 0)
            cnt = int(J[np.ix_(mask_rows, cols)].sum())
            tot += Fraction(p ** v * cnt, 4 ** H)
        rhs[s] = p ** t * tot
    res['C2'] = all(lhs[s] == rhs[s] for s in lhs)
    res['C2_values'] = {s: (float(lhs[s]), float(rhs[s])) for s in lhs}
    return res


def main():
    args = [int(a) for a in sys.argv[1:]]
    for j in range(0, len(args), 3):
        p, t, H = args[j:j + 3]
        t0 = time.time()
        c = vp_fact(H - 1, p)
        M = t + c
        classes = [K for K in range(p ** c) if K % p != 0] if c > 0 else [1]
        Qs, fails = [], 0
        for K in classes:
            f, Q = per_class(p, t, H, K, M)
            fails += f
            Qs.append(Q)
        N = {d: p ** d - p ** (d - 1) for d in range(1, M + 1)}
        meanQ = {d: sum(Q[d] for Q in Qs) / len(Qs) for d in range(1, M + 1)}
        C3 = sum(mpmath.sqrt(N[d] * mpmath.mpf(meanQ[d].numerator) / meanQ[d].denominator) for d in N)
        cs = [sum(mpmath.sqrt(N[d] * mpmath.mpf(Q[d].numerator) / Q[d].denominator) for d in N) for Q in Qs]
        cert = sum(1 for x in cs if x < 1)
        L2 = [sum(Q.values()) for Q in Qs]
        mL2 = max(L2)
        line = (f'(p,t,H)=({p},{t},{H}) c={c} M={M} classes={len(classes)} failing={fails} C3={mpmath.nstr(C3, 4)} '
                f'CS-cert={cert}/{len(classes)} maxL2={float(mL2):.3g} vs p^-M={p ** -M:.3g} '
                f'parseval-cert={sum(1 for x in L2 if x < Fraction(1, p ** M))}/{len(classes)}')
        c2 = c2_check(p, t, H)
        line += f'  C1={c2["C1"]}' + (f' C2={c2["C2"]}' if 'C2' in c2 else ' C2=(skipped, H>30)')
        print(line + f'  ({time.time() - t0:.1f}s)', flush=True)


if __name__ == '__main__':
    main()
