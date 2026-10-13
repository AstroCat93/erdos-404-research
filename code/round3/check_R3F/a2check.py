"""a2check.py -- independent checks of R3F Lemma A1, Theorem A2, Corollary A3 (check of R3F, round 3).

A1: for actual gate blocks (block m with p^j || m+1, several cofactors), the normalised elements
    y_i = (pm+i)!/(pm)! satisfy y_i = sigma_i mod p^{j+1} exactly (integer check), and generally not mod p^{j+2}.
A2: enumerate all delta in {-1,0,1}^p (3^p vectors), n = <delta, sigma>, weight 2^{z(delta)}.
    (ii) list the nonzero delta with n = 0;  (iii)/(i) exact A_2(p^d) = 4^{-p} sum_{p^d | n} 2^z as fractions,
    Q_d = p^d A_2(p^d) - p^{d-1} A_2(p^{d-1}); report Q_d/(N_d 2^{-p}) and the C-S ratio sqrt(N_d Q_d)/(N_d (2/pi)^p).
    Also a brute-force cross-check of Q_d against direct summation of cos^2 for small p^d.
usage: python3 -I a2check.py
"""
from fractions import Fraction
from math import factorial, isqrt
import numpy as np
import mpmath


def sigma(p):
    f = factorial(p - 1)
    return [(-1) ** i * (f // factorial(p - 1 - i)) for i in range(p)]


def a1(p, j, Kps):
    out = []
    s = sigma(p)
    for Kp in Kps:
        if Kp % p == 0:
            continue
        m = p ** j * Kp - 1
        base = factorial(p * m)
        ys = [factorial(p * m + i) // base for i in range(p)]
        ok = all((ys[i] - s[i]) % p ** (j + 1) == 0 for i in range(p))
        nxt = all((ys[i] - s[i]) % p ** (j + 2) == 0 for i in range(p))
        out.append((Kp, ok, nxt))
    return out


def a2(p, dmax):
    s = sigma(p)
    vals = np.array([0], dtype=np.int64)
    zs = np.array([0], dtype=np.int64)
    for x in s:
        vals = np.concatenate([vals, vals + x, vals - x])
        zs = np.concatenate([zs + 1, zs, zs])
    w = np.left_shift(np.int64(1), zs)  # 2^z
    R = sum(abs(x) for x in s)
    e_fl = int(mpmath.floor(mpmath.e * factorial(p - 1)))
    zero_nontriv = []
    idx = np.nonzero(vals == 0)[0]
    # decode delta for the zero entries other than delta = 0
    for t in idx:
        if t == 0:
            continue
        d = []
        tt = int(t)
        # construction order: index = block * 3^... ; decode base-3 digits from the last element
        for i in range(p - 1, -1, -1):
            blk = 3 ** i
            q, tt = divmod(tt, blk)
            d.append({0: 0, 1: 1, 2: -1}[q])
        zero_nontriv.append(tuple(reversed(d)))
    A2 = {}
    for d in range(0, dmax + 1):
        M = p ** d
        A2[d] = Fraction(int(w[vals % M == 0].sum()), 4 ** p)
    rows = []
    two = mpmath.mpf(2) / mpmath.pi
    for d in range(1, dmax + 1):
        N = p ** d - p ** (d - 1)
        Q = p ** d * A2[d] - p ** (d - 1) * A2[d - 1]
        ratio = Q / (Fraction(N, 2 ** p))
        cs = mpmath.sqrt(N * mpmath.mpf(Q.numerator) / Q.denominator) / (N * two ** p)
        rows.append((d, N, ratio, cs, p ** (d - 1) > R))
    return R, e_fl, zero_nontriv, rows


def brute_Q(p, d):
    s = sigma(p)
    M = p ** d
    tot = mpmath.mpf(0)
    for u in range(1, M):
        if u % p == 0:
            continue
        pr = mpmath.mpf(1)
        for x in s:
            pr *= mpmath.cospi(mpmath.mpf(u * x % M) / M) ** 2
        tot += pr
    return tot


def main():
    mpmath.mp.dps = 30
    print('# Lemma A1: gate blocks m = p^j K\' - 1, elements (pm+i)!/(pm)!  vs sigma_i')
    for p, j in ((5, 1), (5, 2), (7, 1), (7, 2), (13, 1)):
        print(f'p={p} j={j}:', [(Kp, ok, nxt) for Kp, ok, nxt in a1(p, j, range(1, 8))], ' (K\', = mod p^{j+1}, = mod p^{j+2})')
    for p, dmax in ((3, 8), (5, 8), (7, 9), (11, 11), (13, 12)):
        R, efl, z, rows = a2(p, dmax)
        print(f'\n# p={p}: sigma={sigma(p)}  R=sum|sigma|={R}  floor(e (p-1)!)={efl}  equal={R == efl}')
        print(f'  nonzero delta with <delta,sigma>=0: {z}')
        cmax = max(r[3] for r in rows)
        for d, N, ratio, cs, arch in rows:
            print(f'  d={d:2d} Q_d/(N_d 2^-p) = {str(ratio):>14s} = {float(ratio):.10f}   CS ratio = {mpmath.nstr(cs, 8)}'
                  f'{"   (p^(d-1) > R)" if arch else ""}')
        print(f'  max_d CS ratio (d <= {dmax}) = {mpmath.nstr(cmax, 8)};  sqrt(3/2)(pi/(2 sqrt2))^p = '
              f'{mpmath.nstr(mpmath.sqrt(1.5) * (mpmath.pi / (2 * mpmath.sqrt(2))) ** p, 8)}')
    print('\n# brute-force cross-check of Q_d (mpmath, direct cos^2 sums)')
    for p, d in ((5, 1), (5, 2), (5, 3), (7, 2), (11, 2), (13, 2)):
        R, efl, z, rows = a2(p, d)
        Q = rows[d - 1][2] * Fraction(p ** d - p ** (d - 1), 2 ** p)
        b = brute_Q(p, d)
        print(f'  p={p} d={d}: exact Q_d = {float(Q):.15g}  brute = {mpmath.nstr(b, 15)}  agree: {abs(b - mpmath.mpf(Q.numerator) / Q.denominator) < 1e-20}')


if __name__ == '__main__':
    main()
