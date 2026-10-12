#!/usr/bin/env python3
"""bottleneck.py -- multiplicity profile of the low layers of a Cov block (HEURISTIC diagnostics;
the multiplicities themselves are exact integer counts).

Block y_i = prod_{s<=i} (p^t K - (H-s)), 0 <= i < H; c = v_p((H-1)!), M = t + c.
L_k = {i : v_p(y_i) < k},  U_k = complement.  For k <= t the residues y_i mod p^k do not depend on K.
m_k(r) = #{ S subset L_k : sum_{i in S} y_i == r (mod p^k) }        (exact, numpy DP)
Bottleneck ratio at level k:   R_k = min_r m_k(r) * 2^{|U_k|} / p^{M-k};   R_0 = 2^H/p^M.
R*(levels <= kmax) = min_k R_k.   (R_M = min over residues of the true representation count.)
usage: bottleneck.py p t H [kmax] [K]
"""
import sys
import numpy as np


def vf(n, p):
    s = 0
    while n:
        n //= p
        s += n
    return s


def profile(p, t, H, kmax=None, K=1, maxsize=3 * 10**7):
    c = vf(H - 1, p)
    M = t + c
    if kmax is None:
        kmax = c
    Q = p ** M
    y = [1]
    for i in range(1, H):
        y.append(y[-1] * (p ** t * K - (H - i)) % Q)
    v = [vf(H - 1, p) - vf(H - 1 - i, p) for i in range(H)]
    out = {'c': c, 'M': M, 'rho': (H - 1) % p, 'R0': 2.0 ** H / p ** M, 'levels': {}}
    for k in range(1, min(kmax, M) + 1):
        mod = p ** k
        if mod > maxsize:
            break
        L = [y[i] % mod for i in range(H) if v[i] < k]
        nU = H - len(L)
        cnt = np.zeros(mod, dtype=np.float64)   # exact while counts < 2^53
        cnt[0] = 1.0
        for a in L:
            if a:
                cnt = cnt + np.roll(cnt, a)
            else:
                cnt = 2 * cnt
        assert len(L) < 53
        mn = float(cnt.min())
        arg = np.flatnonzero(cnt == mn)
        out['levels'][k] = dict(nL=len(L), nU=nU, min=mn, avg=2.0 ** len(L) / mod,
                                Rk=mn * 2.0 ** nU / p ** (M - k), argmin=[int(x) for x in arg[:16]], nargmin=len(arg))
    out['Rstar'] = min([out['R0']] + [d['Rk'] for d in out['levels'].values()])
    return out


def main():
    p, t, H = map(int, sys.argv[1:4])
    kmax = int(sys.argv[4]) if len(sys.argv) > 4 else None
    K = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    o = profile(p, t, H, kmax, K)
    print(f"p={p} t={t} H={H} c={o['c']} M={o['M']} rho={o['rho']} R0={o['R0']:.4g} R*={o['Rstar']:.4g}")
    for k, d in o['levels'].items():
        print(f"  k={k}: |L_k|={d['nL']} |U_k|={d['nU']} min m_k={d['min']:.0f} avg={d['avg']:.4g} R_k={d['Rk']:.4g} "
              f"#argmin={d['nargmin']} argmin={d['argmin']}")


if __name__ == '__main__':
    main()
