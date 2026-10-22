"""identcheck.py -- numerical checks of exact identities in R3F (check of R3F, round 3).

(1) Theorem A4(i) (Poisson formula): A(M) = (1/M) sum_{r mod M} F_p(r/M) == (2/pi)^p sum_j Psi_p(jM), with Psi_p
    computed by the carry recursion on a window |s| <= S (truncation error O(1/S); a sanity check, not a proof).
(2) Proposition B7(i),(ii): exact L^2 renormalisation identity for the tail from N0 = p with W = 1 (attained),
    k = 2, 3: Q_{N0}(k) == sum_{w unit mod p^{k-W}} |nu^_{N_W}(w/p^{k-W})|^2 H2_W((w a^{-1} mod p^{k-W})/p^k),
    and sup H2_W = H2_W(0) = 1 + (L^2 mass of the bottom W levels) on a fine grid.
(3) B8 identity on the same data: p^{e+j+1} P(p^{e+j+1} | Z_{<=gate}) == p^e P(p^e | Z_<) [1 + sum_{w != 0} F_p(wU/p^{j+1})^2 chi^(w)]
    for the first level-1 gate block of the tail from p (block m = p-1 at p = 5, 7), by exact enumeration.
usage: python3 -I identcheck.py
"""
from fractions import Fraction
from math import factorial, gcd

import mpmath
import numpy as np

mpmath.mp.dps = 30


def vp_fact(n, p):
    s, q = 0, p
    while q <= n:
        s += n // q
        q *= p
    return s


def b(k):
    return (-1) ** (abs(k) + 1) / (4.0 * k * k - 1.0)


def psi_vector(p, S):
    """Psi_{p-1}(s) for |s| <= S, via Psi_m(s) = sum_{s'} b_{s-ms'} Psi_{m-1}(s'), Psi_1 = b*b."""
    idx = np.arange(-S, S + 1)
    psi = np.zeros(2 * S + 1)
    psi[S] = np.pi ** 2 / 8; psi[S + 1] = psi[S - 1] = np.pi ** 2 / 16
    K = (p + 1) * S + 2
    kk = np.arange(-K, K + 1, dtype=float)
    bk = ((-1.0) ** (np.abs(np.arange(-K, K + 1)) + 1)) / (4 * kk * kk - 1)
    for m in range(2, p):
        new = np.empty(2 * S + 1)
        sp = np.arange(-S, S + 1)
        for j, s in enumerate(idx):
            new[j] = np.dot(bk[s - m * sp + K], psi)
        psi = new
    return psi


def poisson(p, Ms, S=4000):
    f = factorial(p - 1)
    sig = [(-1) ** i * (f // factorial(p - 1 - i)) for i in range(p)]
    psi = psi_vector(p, S)
    out = []
    for M in Ms:
        A = mpmath.fsum(mpmath.fprod(abs(mpmath.cospi(mpmath.mpf(r * x % M) / M)) for x in sig) for r in range(M)) / M
        js = np.arange(-(S // M), S // M + 1)
        rhs = (2 / np.pi) ** p * psi[js * M + S].sum()
        out.append((M, float(A), rhs, float(A) - rhs))
    return out


def b7(p, kmax=3):
    N0, W = p, 1
    NW = N0
    while vp_fact(NW, p) - vp_fact(N0, p) < W:
        NW += 1
    assert vp_fact(NW, p) - vp_fact(N0, p) == W  # attained
    a = (factorial(NW) // factorial(N0)) // p ** W
    assert a % p != 0
    res = []
    for k in range(W + 1, kmax + 1):
        M = p ** k
        q = p ** (k - W)
        # tail elements x'_n = n!/N0!, levels < k
        n, xs = N0, []
        while vp_fact(n, p) - vp_fact(N0, p) < k or n < NW:
            xs.append(factorial(n) // factorial(N0))
            n += 1
        lhs = mpmath.fsum(mpmath.fprod(mpmath.cospi(mpmath.mpf(u * x % M) / M) ** 2 for x in xs)
                          for u in range(1, M) if u % p)
        bottom = [factorial(n) // factorial(N0) for n in range(N0, NW)]
        top = [factorial(n) // factorial(NW) for n in range(NW, n)]

        def H2(theta):
            return mpmath.fsum(mpmath.fprod(mpmath.cospi((theta + mpmath.mpf(s) / p ** W) * x) ** 2 for x in bottom)
                               for s in range(p ** W))
        ainv = pow(a, -1, q)
        rhs = mpmath.fsum(mpmath.fprod(mpmath.cospi(mpmath.mpf(w * y % q) / q) ** 2 for y in top) *
                          H2(mpmath.mpf(w * ainv % q) / M) for w in range(1, q) if w % p)
        res.append((k, lhs, rhs))
    # (ii)
    grid = [mpmath.mpf(i) / 20000 / p ** W for i in range(20000)]
    Hs = [H2(t) for t in grid]
    l2bottom = mpmath.fsum(mpmath.fprod(mpmath.cospi(mpmath.mpf(s * x % p ** W) / p ** W) ** 2 for x in bottom)
                           for s in range(1, p ** W))
    return res, max(Hs), H2(0), 1 + l2bottom


def b8(p):
    """first level-1 gate of the tail from p: block m = p-1 (elements n = p(p-1) .. p^2-1), relative level e."""
    N0 = p
    e0 = vp_fact(N0, p)
    m = p - 1
    j = 1
    below = [factorial(n) // p ** e0 for n in range(N0, p * m)]
    gate = [factorial(n) // p ** e0 for n in range(p * m, p * m + p)]
    e = vp_fact(p * m, p) - e0
    Dm = p ** (e + j + 1)
    # exact lazy-difference distributions mod p^{e+j+1}
    def lazy(xs, mod):
        w = np.zeros(mod, dtype=object); w[0] = 1
        for x in xs:
            w = 2 * w + np.roll(w, x % mod) + np.roll(w, -(x % mod))
        return w
    wb = lazy(below, Dm)
    wg = lazy(gate, Dm)
    tot_b = 4 ** len(below); tot_g = 4 ** len(gate)
    # LHS
    conv = sum(wb[r] * wg[(-r) % Dm] for r in range(Dm))
    lhs = Fraction(Dm * conv, tot_b * tot_g)
    # RHS
    pe = Fraction(p ** e * sum(wb[r] for r in range(0, Dm, p ** e)), tot_b)
    # chi: law of C = Z_</p^e mod p^{j+1} conditioned on p^e | Z_<
    q = p ** (j + 1)
    chi = [0] * q
    for r in range(0, Dm, p ** e):
        chi[(r // p ** e) % q] += wb[r]
    Z = sum(chi)
    # gate block = p^e * U * y_i with y_i = sigma_i mod p^{j+1}: U = (gate[0]/p^e) mod p^{j+1}
    U = (gate[0] // p ** e) % q
    f = factorial(p - 1)
    sig = [(-1) ** i * (f // factorial(p - 1 - i)) for i in range(p)]
    assert all((gate[i] // p ** e - U * sig[i]) % q == 0 for i in range(p))
    s = mpmath.mpf(0)
    for w in range(1, q):
        F2 = mpmath.fprod(mpmath.cospi(mpmath.mpf(w * U * x % q) / q) ** 2 for x in sig)
        chihat = mpmath.fsum(mpmath.mpf(chi[c]) / Z * mpmath.expjpi(2 * mpmath.mpf(w * c) / q) for c in range(q))
        s += F2 * chihat
    rhs = pe * (1 + s)
    return float(lhs), rhs


def main():
    print('# (1) Theorem A4(i): A(M) direct vs (2/pi)^p sum_j Psi_p(jM) (carry recursion, window S = 4000)')
    for p, Ms in ((5, [5, 25, 125]), (7, [7, 49, 343])):
        for M, A, rhs, diff in poisson(p, Ms):
            print(f'  p={p} M={M}: A(M)={A:.12f}  Poisson={rhs:.12f}  diff={diff:.2e}')
    print('# (2) Proposition B7 (L^2 renormalisation), tail from N0 = p, W = 1')
    for p in (5, 7):
        res, supH, H0, onepl = b7(p, kmax=3 if p == 5 else 3)
        for k, l, r in res:
            print(f'  p={p} k={k}: Q_N0(k) direct={mpmath.nstr(l, 15)}  identity RHS={mpmath.nstr(r, 15)}  rel.diff={mpmath.nstr(abs(l - r) / l, 3)}')
        print(f'  p={p}: max over 20000-point grid of H2 = {mpmath.nstr(supH, 12)};  H2(0) = {mpmath.nstr(H0, 12)};  1 + L2(bottom) = {mpmath.nstr(onepl, 12)}')
    print('# (3) B8 gate identity (first level-1 gate of the tail from p), exact enumeration')
    for p in (5, 7):
        l, r = b8(p)
        print(f'  p={p}: LHS={l:.15g}  RHS={mpmath.nstr(mpmath.re(r), 15)} (imag {mpmath.nstr(mpmath.im(r), 2)})')


if __name__ == '__main__':
    main()
