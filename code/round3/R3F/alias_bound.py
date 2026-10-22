#!/usr/bin/env python3
"""alias_bound.py -- rigorous aliasing (Poisson) bound for single gate blocks (round 3, track R3F, target (a)).

F(theta) = prod_{u<p} |cos(pi theta P_u)|, P_u = (p-1)!/u!.  Fourier coefficients: hat F(n) = (2/pi)^p Psi(n),
Psi(n) = sum_{k: sum_u k_u P_u = n} prod b_{k_u},  b_k = (-1)^{k+1}/(4k^2-1).
Backward absolute completion weights: G_1(s) = |(b*b)(s)| (pi^2/8 at 0, pi^2/16 at +-1, else 0),
  G_m(s) = sum_{s'} |b_{s - m s'}| G_{m-1}(s'),  m = 2..p-1;   |Psi(n)| <= G_{p-1}(n).
Envelopes (proved in the report):  G_m(s) <= beta_m for all s,  G_m(s) <= alpha_m / s^2 for s != 0, with
  beta_1 = pi^2/8, alpha_1 = pi^2/16,
  beta_m = kappa_m beta_{m-1},
  alpha_m = beta_{m-1}/3 + alpha_{m-1} (pi/3 + m sqrt(kappa_m))^2,
  kappa_m = 2 - (pi/(2m)) cot(pi/(2m))  (= max residue-class sum of |b_k| mod m).
Then  sum_{j != 0} |Psi(j M)| <= (pi^2/3) alpha_{p-1} / M^2  =: E(M).
Consequence for the gate shells: with rho_d = S_d / (N_d (2/pi)^p),
  |rho_d - J_p| <= (p^d E(p^d) + p^{d-1} E(p^{d-1})) / N_d.
All quantities evaluated in mpmath interval arithmetic (upper endpoints reported).
usage: alias_bound.py p [dmin dmax]
"""
import sys
from mpmath import iv, mpf

iv.prec = 120


def bounds(p):
    pi = iv.pi
    beta = pi ** 2 / 8
    alpha = pi ** 2 / 16
    for m in range(2, p):
        x = pi / (2 * m)
        kappa = 2 - x * iv.cot(x)
        alpha = beta / 3 + alpha * (pi / 3 + m * iv.sqrt(kappa)) ** 2
        beta = kappa * beta
    return alpha, beta


def main():
    p = int(sys.argv[1])
    dmin = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    dmax = int(sys.argv[3]) if len(sys.argv) > 3 else 14
    alpha, beta = bounds(p)
    import math
    fac = math.factorial(p - 1)
    print(f"# p={p}: alpha_(p-1) <= {float(alpha.b):.6e}  (= {float(alpha.b)/fac**2:.4f} * ((p-1)!)^2),  beta_(p-1) <= {float(beta.b):.6f}")
    pi = iv.pi
    for d in range(max(dmin, 1), dmax + 1):
        M = iv.mpf(p) ** d
        E = lambda MM: pi ** 2 / 3 * alpha / MM ** 2
        N = iv.mpf(p) ** d - iv.mpf(p) ** (d - 1)
        dev = (iv.mpf(p) ** d * E(M) + iv.mpf(p) ** (d - 1) * E(M / p)) / N
        print(f"d={d:2d}  E(p^d) <= {float(E(M).b):.4e}   |rho_d - J_p| <= {float(dev.b):.4e}")


if __name__ == "__main__":
    main()
