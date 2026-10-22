#!/usr/bin/env python3
"""plateau_bounds.py -- the explicit lower bounds of Corollary P (data/round4/reports/M4D.md), exact rationals.

Inputs (cited, computer-assisted, not recomputed here):
  * census values delta_{G0}(p) = mu{g_p >= G0} (note.md section 4.7; 5 decimals, so we subtract 1e-5);
  * uniform covering certificates Cov(p,t,H_t), t <= T (note.md section 10.2; two programs each).
For each p: n0 = max_t H_t;  mu{V_{n0} > G0} <= n0 * p^{-k0} where k0 is the least valuation forced by
V_{n0} > G0 (computed below from the multiplicity bound N_1 <= ceil(n0/p), N_k <= 1 for p^k > n0);
  B_p := delta_{G0} - 1e-5 - n0 p^{-k0}  <=  mu{P(x,n0)};
  delta_{v_p(N!)}(p) >= B_p - (N - n0) p^{-(T+1)}   for N >= n0.
Also prints, for eps in {0.01, 0.05, 0.1}, the largest N with loss <= eps and G = v_p(N!).
usage: plateau_bounds.py
"""
from fractions import Fraction

DATA = {
    # p: (G0, delta_G0 (5 decimals), [H_1..H_T])
    7: (8, Fraction(62394, 10 ** 5), [4, 7, 19, 26, 28, 34]),
    11: (6, Fraction(69976, 10 ** 5), [5, 10, 18, 22, 30, 33]),
    13: (5, Fraction(75454, 10 ** 5), [6, 10, 19, 24, 32, 35, 39]),
    17: (4, Fraction(75692, 10 ** 5), [5, 11, 16, 25, 30, 34, 43]),
    19: (4, Fraction(77792, 10 ** 5), [5, 12, 17, 27, 31, 35]),
    23: (3, Fraction(85617, 10 ** 5), [7, 12, 18, 23, 33, 37]),
}


def vfact(n, p):
    s, q = 0, p
    while q <= n:
        s += n // q
        q *= p
    return s


def main():
    print("TABLE p | T | n0 | G0 | k0 | n0*p^-k0 | B_p (lower bound for mu{P(x,n0)}) | p^(T+1) | "
          "N, G=v_p(N!) with loss <= 0.01 / 0.05 / 0.1")
    for p, (G0, dG0, Hs) in DATA.items():
        T = len(Hs)
        assert all(Hs[t - 1] + 1 < p ** t for t in range(1, T + 1))
        n0 = max(Hs)
        # V_{n0} = sum_k N_k with N_1 <= ceil(n0/p), N_k <= ceil(n0/p^k); for p^k > n0, N_k <= 1.
        # V_{n0} > G0 forces some x+i (i <= n0) with v(x+i) >= k0: find the least such k0.
        caps = []
        k = 1
        while p ** k <= n0:
            caps.append(-(-n0 // p ** k))
            k += 1
        k1 = k          # first level with N_k <= 1
        base = sum(caps)  # max contribution of levels < k1
        # with max valuation m >= k1: V <= base + (m - k1 + 1); V >= G0+1 forces m >= G0 + 1 - base + k1 - 1
        assert base <= G0
        k0 = max(k1, G0 + 1 - base + k1 - 1)
        tail = Fraction(n0, p ** k0)
        B = dG0 - Fraction(1, 10 ** 5) - tail
        P = p ** (T + 1)
        outs = []
        for eps in (Fraction(1, 100), Fraction(5, 100), Fraction(1, 10)):
            N = n0 + int(eps * P)
            outs.append(f"N={N}, G={vfact(N, p)}")
        print(f"TABLE {p} | {T} | {n0} | {G0} | {k0} | {float(tail):.3e} | {float(B):.5f} | {P} | " + " / ".join(outs))
    print("SUMMARY delta_G(p) >= B_p - eps for all G <= the listed G (eps = 0.01, 0.05, 0.1).")


if __name__ == "__main__":
    main()
