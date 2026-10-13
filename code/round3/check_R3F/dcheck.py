"""dcheck.py -- re-computation of R3F D2 (illustration): Psi(0) for the tail chains x'_n = n!/N0!, N0 <= n < N_k.
Psi(0) = sum over integer relations sum_i k_i x_i = 0 of prod b_{k_i}, b_k = (-1)^{k+1}/(4k^2-1).
With x_i = x_{i-1} m_i (m_i = N0 + i), relations are parametrised by carries: k_0 = -m_1 c_1,
k_i = c_i - m_{i+1} c_{i+1} (1 <= i <= n-2), k_{n-1} = c_{n-1}.  Transfer over c with |c| <= C (float64; not certified:
this item is an illustration in R3F as well).  Written independently of cont_vs_grid.py.
usage: python3 -I dcheck.py p kmax C
"""
import sys

import numpy as np


def vp_fact(n, p):
    s, q = 0, p
    while q <= n:
        s += n // q
        q *= p
    return s


def b(k):
    k = np.asarray(k, dtype=float)
    return np.where(np.abs(k) % 2 == 1, 1.0, -1.0) / (4 * k * k - 1)


def psi0(ms, C):
    cs = np.arange(-C, C + 1)
    v = b(-ms[0] * cs)                       # weight of c_1 from k_0
    for i in range(1, len(ms)):
        # v_new(c_{i+1}) = sum_{c_i} v(c_i) b(c_i - m_{i+1} c_{i+1})
        K = cs[:, None] - ms[i] * cs[None, :]
        v = v @ b(K)
    return float(v @ b(cs))                 # k_{n-1} = c_{n-1}


def main():
    p, kmax, C = (int(a) for a in sys.argv[1:4])
    N0 = p
    e0 = vp_fact(N0, p)
    for k in range(1, kmax + 1):
        n = N0
        while vp_fact(n, p) - e0 < k:
            n += 1
        ms = list(range(N0 + 1, n))         # x'_{N0} = 1, ratios m = N0+1, ..., n-1
        print(f'p={p} k={k}: elements {n - N0}, Psi(0) = {psi0(ms, C):.8f} (C={C})', flush=True)


if __name__ == '__main__':
    main()
