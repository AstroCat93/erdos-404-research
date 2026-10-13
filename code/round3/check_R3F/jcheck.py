"""jcheck.py -- independent checks of R3F Theorem A4 constants, J_p, Proposition A6 (check of R3F, round 3).

(1) alpha_m, beta_m, kappa_m of A4(iii) in mpmath interval arithmetic; kappa_m also by direct summation.
(2) J_p = Psi_p(0) by the carry recursion, organised as dense truncated vectors on [-C, C] in float64
    (numpy dot products), with this file's own rigorous error accounting:
      J = sum_s v~_1(s) Psi_1(s) + sum_{m=2}^{p-1} (dropped_m + fp_m),
      |dropped_m| <= beta_{m-1} ||v~_m||_1 * 2/(3 m (m-1) C)          (tail of |b| beyond the window),
      |fp_m|      <= beta_{m-1} kappa_m ||v~_m||_1 * (gamma_{2C+1} + 2u)  (float64 dot products, rounded b_k).
(3) Proposition A6 constants: prod_{m>=2} kappa_m and beta^abs_inf (with a rigorous tail bound for the product).

usage: python3 -I jcheck.py C p [p ...]
"""
import sys
import time

import numpy as np
import mpmath
from mpmath import iv

iv.dps = 30


def kappa_iv(m):
    z = iv.pi / (2 * m)
    return 2 - z * iv.cos(z) / iv.sin(z)


def constants(pmax):
    """alpha[m], beta[m], kappa[m] (intervals) for 1 <= m <= pmax-1."""
    alpha = {1: iv.pi ** 2 / 16}
    beta = {1: iv.pi ** 2 / 8}
    kap = {}
    for m in range(2, pmax):
        k = kappa_iv(m)
        kap[m] = k
        beta[m] = k * beta[m - 1]
        alpha[m] = beta[m - 1] / 3 + alpha[m - 1] * (iv.pi / 3 + m * iv.sqrt(k)) ** 2
    return alpha, beta, kap


def kappa_direct(m, K=200000):
    """max residue-class sum of |b_k| mod m, by direct summation (|k| <= K) plus a tail bound."""
    ks = np.arange(-K, K + 1)
    b = 1.0 / (4.0 * ks.astype(float) ** 2 - 1.0)
    b = np.abs(b)
    sums = [b[(ks % m) == r].sum() for r in range(m)]
    return max(sums), int(np.argmax(sums)), 2.0 / (3.0 * K)


def J_trunc(p, C):
    u = 2.0 ** -53
    alpha, beta, kap = constants(p)
    ks = None
    v = np.zeros(2 * C + 1); v[C] = 1.0       # v_{p-1} = delta_0, index s + C
    err = mpmath.mpf(0)
    for m in range(p - 1, 1, -1):
        # v_{m-1}(s') = sum_s v_m(s) b_{s - m s'},  |s'| <= C
        Kmax = (m + 1) * C + 1
        kk = np.arange(-Kmax, Kmax + 1, dtype=np.float64)
        bk = ((-1.0) ** (np.abs(np.arange(-Kmax, Kmax + 1)) + 1)) / (4.0 * kk * kk - 1.0)
        off = Kmax                               # index of k = 0
        # row j' = 0..2C corresponds to s' = C - j'; entry (j', i) is b_{(i - C) - m (C - j')} = bk[off - C - mC + i + m j']
        base = off - C - m * C
        A = np.lib.stride_tricks.as_strided(bk[base:], shape=(2 * C + 1, 2 * C + 1),
                                            strides=(m * bk.strides[0], bk.strides[0]), writeable=False)
        assert base + m * (2 * C) + 2 * C < len(bk) and base >= 0
        nv_rev = np.empty(2 * C + 1)
        step = 512
        for j0 in range(0, 2 * C + 1, step):
            nv_rev[j0:j0 + step] = np.ascontiguousarray(A[j0:j0 + step]) @ v
        nv = nv_rev[::-1].copy()                 # index s' + C
        l1 = mpmath.mpf(float(np.abs(v).sum())) * (1 + mpmath.mpf('1e-9'))
        bm1 = mpmath.mpf(beta[m - 1].b)
        dropped = bm1 * l1 * mpmath.mpf(2) / (3 * m * (m - 1) * C)
        n = 2 * C + 1
        gam = n * u / (1 - n * u)
        fp = bm1 * mpmath.mpf(kap[m].b) * l1 * (gam + 2 * u)
        err += dropped + fp
        v = nv
    psi1 = {0: iv.pi ** 2 / 8, 1: iv.pi ** 2 / 16, -1: iv.pi ** 2 / 16}
    l1 = mpmath.mpf(float(np.abs(v).sum())) * (1 + mpmath.mpf('1e-9'))
    val = sum(iv.mpf(float(v[C + s])) * psi1[s] for s in (-1, 0, 1))
    err += l1 * 3 * u * mpmath.mpf(psi1[0].b)     # rounding of the three products/sum (crude)
    return val, err


def main():
    C = int(sys.argv[1])
    ps = [int(a) for a in sys.argv[2:]]
    alpha, beta, kap = constants(max(max(ps), 17) + 1)
    print('# A4(iii) constants (mpmath iv, upper ends):  alpha_{p-1}/((p-1)!)^2  and beta_{p-1}')
    for p in ps:
        f = mpmath.factorial(p - 1)
        print(f'p={p}: alpha_(p-1)/((p-1)!)^2 <= {mpmath.nstr(mpmath.mpf(alpha[p - 1].b) / f ** 2, 8)}   '
              f'beta_(p-1) <= {mpmath.nstr(mpmath.mpf(beta[p - 1].b), 8)}', flush=True)
    print('# kappa_m: closed form vs direct summation (|k| <= 2e5; tail <= 3.4e-6)')
    for m in (2, 3, 4, 7, 12):
        kd, r, tail = kappa_direct(m)
        print(f'  m={m}: closed form {mpmath.nstr(mpmath.mpf(kap[m].mid), 12)}  direct {kd:.12f} (max class {r}, tail <= {tail:.1e})', flush=True)
    # Proposition A6: prod_{m>=2} kappa_m, with tail bound prod_{m>M} kappa_m <= exp(sum_{m>M} (kappa_m - 1)),
    # kappa_m - 1 <= 2/(4m^2-1) + (2/(3m^2))(pi^2/6 - 1) <= (1/2 + (2/3)(pi^2/6-1)) / (m^2 - 1/4)... use crude 1.0/(m(m-1)) * c
    Mt = 20000
    prod = iv.mpf(1)
    for m in range(2, Mt + 1):
        prod *= kappa_iv(m)
    # sum_{m>Mt} (kappa_m - 1) <= sum_{m>Mt} [2/(4m^2-1) + 2(pi^2/6-1)/(3m^2)] <= (1/2 + 2(pi^2/6-1)/3)/(Mt) * 1.01
    tail = (mpmath.mpf(1) / 2 + 2 * (mpmath.pi ** 2 / 6 - 1) / 3) / Mt * mpmath.mpf('1.01')
    prod_hi = mpmath.mpf(prod.b) * mpmath.exp(tail)
    print(f'# Prop A6: prod_(m>=2) kappa_m in [{mpmath.nstr(mpmath.mpf(prod.a), 8)}, {mpmath.nstr(prod_hi, 8)}];  '
          f'beta_abs_inf <= {mpmath.nstr(prod_hi * mpmath.pi ** 2 / 8, 8)};  (pi^2/9) beta_abs_inf <= '
          f'{mpmath.nstr(prod_hi * mpmath.pi ** 4 / 72, 8)}', flush=True)
    for p in ps:
        t0 = time.time()
        val, err = J_trunc(p, C)
        lo = mpmath.mpf(val.a) - err; hi = mpmath.mpf(val.b) + err
        print(f'p={p} C={C}: J_trunc = {mpmath.nstr(mpmath.mpf(val.mid), 12)}  total error <= {mpmath.nstr(err, 4)}  '
              f'=> J_p in [{mpmath.nstr(lo, 10)}, {mpmath.nstr(hi, 10)}]   ({time.time() - t0:.1f}s)', flush=True)


if __name__ == '__main__':
    main()
