#!/usr/bin/env python3
"""test_Hprime.py -- exact test of Proposition H' of the M4C report:
for an environment ball B = z0 + p^r Z_p (r = M+1, all v(z+i), i <= L+L', constant on B) with D >= 2r and
ceil(D/2) <= K - M,
   E_B[eps] <= c_{L+L'} + sum_{j < L+L'} (c_j/2) E_B[ Lambda^{(lambda_j)}_{L+L'-j}(z+j) ],  lambda_j = ceil(D/2) - V_j,
where eps(z) = p^K Coll_K - p^D Coll_D of the composite law of y_c = (z+1)...(z+c), c < L+L',
Lambda^{(lam)}_t(y) = p^{V_t(y)} P(v(R(y)) >= V_t(y), v(R'(y)) >= lam), R = 1 + sum_{1<=c<t} d_c pi_c(y).
Both sides are computed exactly (rationals): the average over z in B runs over all z mod p^Q (Q large enough
that every quantity is determined), the signed laws by exact DP (weights 1,2,1).
usage: test_Hprime.py p SEED NBALLS LTOT            (ball-averaged inequality)
       test_Hprime.py p SEED NZ LTOT pointwise        (pointwise first-nonzero-index identity)
"""
import random
import sys
from fractions import Fraction

import numpy as np


def v(a, p, cap=60):
    a %= p ** cap
    if a == 0:
        return cap
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def signed_count(elems, dels, mod1, mod2, forced0):
    """number (weights 1,2,1; first digit forced to +1 if forced0) of signed vectors with
    sum d_c elems_c = 0 mod mod1 and sum d_c dels_c = 0 mod mod2."""
    dist = np.zeros((mod1, mod2), dtype=object)
    start = 0
    if forced0:
        dist[elems[0] % mod1, dels[0] % mod2] = 1
        start = 1
    else:
        dist[0, 0] = 1
    for a, b in zip(elems[start:], dels[start:]):
        a %= mod1
        b %= mod2
        dist = 2 * dist + np.roll(np.roll(dist, a, 0), b, 1) + np.roll(np.roll(dist, -a, 0), -b, 1)
    return int(dist[0, 0])


def main():
    p, seed, NB, LT = (int(a) for a in sys.argv[1:5])
    rnd = random.Random(seed)
    st = dict(balls=0, fail=0, max_ratio=0.0, nonzero=0)
    for _ in range(NB):
        z0 = rnd.randrange(p ** 12)
        L = rnd.randint(2, LT - 1)
        vals = [v(z0 + i, p) for i in range(1, LT + 1)]
        M = max(vals)
        r = M + 1
        D = sum(vals[:L])
        K = sum(vals)
        if not (D >= 2 * r and -(-D // 2) <= K - M and K > D):
            continue
        Vc = [0]
        for i in range(LT):
            Vc.append(Vc[-1] + vals[i])
        Q = K  # every quantity used depends only on z mod p^K (polynomials mod p^K; V, M fixed on B)
        lhs = Fraction(0)
        rhs = Fraction(0)
        nz = p ** (Q - r)
        lam_all = [-(-D // 2) - Vc[j] for j in range(LT)]
        for u in range(nz):
            z = (z0 % p ** r) + p ** r * u
            mod = p ** Q
            pi = [1]
            for c in range(1, LT):
                pi.append(pi[-1] * (z + c) % mod)
            # eps(z)
            W = 4 ** LT
            cK = signed_count(pi, [0] * LT, p ** K, 1, False)
            cD = signed_count(pi[:L], [0] * L, p ** D, 1, False)
            # Coll_D uses the elements below level D only (others vanish mod p^D): extend by 4^{LT-L}
            eps = Fraction(p ** K * cK, W) - Fraction(p ** D * cD, 4 ** L)
            lhs += eps
            # right side
            rh = Fraction(p ** K, 2 ** LT)  # c_{L+L'}
            for j in range(LT):
                t = LT - j
                y = z + j
                pij = [1]
                dpij = [0]
                for c in range(1, t):
                    dpij.append((dpij[-1] * (y + c) + pij[-1]) % mod)
                    pij.append(pij[-1] * (y + c) % mod)
                Vt = K - Vc[j]
                lam = lam_all[j]
                mf = p ** max(lam, 0)
                cnt = signed_count(pij, dpij, p ** Vt, mf, True)
                Lam = Fraction(p ** Vt * cnt, 4 ** (t - 1))
                cj = Fraction(p ** Vc[j], 2 ** j)
                rh += cj / 2 * Lam
            rhs += rh
        lhs /= nz
        rhs /= nz
        st["balls"] += 1
        if lhs > 0:
            st["nonzero"] += 1
            st["max_ratio"] = max(st["max_ratio"], float(lhs / rhs))
        if lhs > rhs:
            st["fail"] += 1
            print("FAIL", z0 % p ** r, L, LT, float(lhs), float(rhs))
    print(f"# test_Hprime p={p} seed={seed} NBALLS={NB} LTOT={LT}")
    print("RESULT", st)


if __name__ == "__main__" and len(sys.argv) <= 5:
    main()


def pointwise(p, seed, NZ, LT):
    """exact pointwise check of the first-nonzero-index identity behind Prop H':
    sum_d P(d) p^K 1[v(T_d(z)) >= K, v(T_d'(z)) >= h] = c_{L+L'} + sum_j (c_j/2) Lambda^{(h - V_j)}_{LT-j}(z+j),
    h = ceil(D/2), valid when h <= K - M (M = max_{i<=LT} v(z+i))."""
    rnd = random.Random(seed)
    st = dict(points=0, fail=0, nonzero=0)
    for _ in range(NZ):
        z = rnd.randrange(p ** 30)
        L = rnd.randint(2, LT - 1)
        vals = [v(z + i, p) for i in range(1, LT + 1)]
        M = max(vals)
        D = sum(vals[:L])
        K = sum(vals)
        h = -(-D // 2)
        if not (h <= K - M and K > D and K <= 9 and h >= 1):
            continue
        Vc = [0]
        for i in range(LT):
            Vc.append(Vc[-1] + vals[i])
        mod = p ** (K + 2)
        pi = [1]
        dpi = [0]
        for c in range(1, LT):
            dpi.append((dpi[-1] * (z + c) + pi[-1]) % mod)
            pi.append(pi[-1] * (z + c) % mod)
        lhs = Fraction(p ** K * signed_count(pi, dpi, p ** K, p ** h, False), 4 ** LT)
        rhs = Fraction(p ** K, 2 ** LT)
        for j in range(LT):
            t = LT - j
            y = z + j
            pij = [1]
            dpij = [0]
            for c in range(1, t):
                dpij.append((dpij[-1] * (y + c) + pij[-1]) % mod)
                pij.append(pij[-1] * (y + c) % mod)
            Vt = K - Vc[j]
            lam = h - Vc[j]
            cnt = signed_count(pij, dpij, p ** Vt, p ** max(lam, 0), True)
            rhs += Fraction(p ** Vc[j], 2 ** j) / 2 * Fraction(p ** Vt * cnt, 4 ** (t - 1))
        st["points"] += 1
        st["nonzero"] += (lhs > 0)
        if lhs != rhs:
            st["fail"] += 1
            print("IDENTITY FAIL", z % p ** 8, L, float(lhs), float(rhs))
    print(f"# test_Hprime pointwise identity p={p} seed={seed} NZ={NZ} LTOT={LT}")
    print("RESULT", st)


if __name__ == "__main__" and len(sys.argv) > 5 and sys.argv[5] == "pointwise":
    pointwise(*(int(a) for a in sys.argv[1:5]))
