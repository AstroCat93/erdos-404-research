#!/usr/bin/env python3
"""Round-3 computational referee: recompute rows of R3Q's Corollary D (note Cor. 11.8) from the
logged parameters, using only the statements of Theorems A and B and Proposition 10 in
data/round3/reports/R3Q.md (no R3Q or checker code is used).

Everything is exact rational arithmetic (fractions.Fraction); infinite sums are cut at
I0 explicit terms plus a rigorous tail majorant (also exact rational).

Rows done here (parameters as logged in data/round3/R3Q/scan_D*.log; T = 2^K - 2K - 12 as in
Theorem C / bounds.py):
  K=37, K=40     : C14 part is the trivial 1/16
  K=448          : C14 part from Theorem B with M*=8, Mf=13, chain [46,67,110,194], ns=202, k=209, m1=0
"""
from fractions import Fraction as Fr
from math import comb, floor
import sys

TAIL_TERMS = 6000


def s2(n):
    return bin(n).count("1")


def beta(n):
    return n - s2(n) - (n.bit_length() - 1)


def z(n):
    return -(-n // 2) - 1


def flog2(x):
    return x.bit_length() - 1


def mu_v(rC, a, i, b):
    """mu(C ∩ {v(x+i) >= b}) for C = rC + 2^a Z_2, computed from first principles."""
    if b <= 0:
        return Fr(1, 2 ** a)
    y = rC + i
    if b <= a:
        return Fr(1, 2 ** a) if y % (2 ** b) == 0 else Fr(0)
    return Fr(1, 2 ** b) if y % (2 ** a) == 0 else Fr(0)


def count_res(lo, hi, r, m):
    """#{i in [lo,hi] : i = r mod m}."""
    if hi < lo:
        return 0
    first = lo + ((r - lo) % m)
    return 0 if first > hi else (hi - first) // m + 1


def P_bin_lt(N, k):
    """P(Bin(N,1/2) < k), with P = 1 if N <= 0 < k."""
    if N <= 0:
        return Fr(1) if k > 0 else Fr(0)
    if k <= 0:
        return Fr(0)
    return Fr(sum(comb(N, i) for i in range(min(k, N + 1))), 2 ** N)


def tail_major(lam, i0):
    """Rigorous majorant of sum_{i>=i0} 2^-(beta(i-1)-lam+1).
    beta(n) >= n - 2 floor(log2 n) - 1, so each term <= 2^lam * (i-1)^2 * 2^-(i-1);
    for m >= i0-1 >= 100 the ratio of consecutive m^2 2^-m is <= (101/100)^2/2 < 0.511."""
    m0 = i0 - 1
    assert m0 >= 100
    return Fr(2 ** lam) * Fr(m0 * m0, 2 ** m0) / (1 - Fr(511, 1000))


def A1_sum(rC, a, T, b):
    """sum_{i=1}^T mu(C ∩ {v(x+i) >= b}) for b > a."""
    assert b > a
    return Fr(count_res(1, T, (-rC) % (2 ** a), 2 ** a), 2 ** b)


def theorem_A(cls, K, ns, k, m1):
    rC, a, lam, nC = {"C0": (0, 3, 1, 6), "C2": (2, 4, 3, 8), "C6": (6, 4, 3, 10)}[cls]
    G = 2 ** K
    T = G - 2 * K - 12
    ellC = 0 if lam == 1 else (lam - 1) + flog2(2 * lam)
    Kt = flog2(T - ns - 2 * lam)
    # hypotheses
    assert G >= 7 and T <= G and ns >= nC and beta(ns) >= lam + 1 and Kt >= a and k >= 1
    assert m1 == 0 or (a <= m1 <= min(ns - s2(ns), Kt)), "m1 out of range"
    A1 = A1_sum(rC, a, T, G - T + 3)
    I0 = ns + TAIL_TERMS
    A4 = sum(mu_v(rC, a, i, beta(i - 1) - lam + 1) for i in range(ns + 1, min(T, I0 - 1) + 1))
    A4 += tail_major(lam, I0) if T >= I0 else 0
    l0 = s2((rC + ns) % 2 ** a)
    if m1 >= a:
        A5 = Fr(1, 2 ** a) * (P_bin_lt(Kt - m1, k) + Fr(2) ** (1 - k + ellC + z(ns) - l0) * Fr(3, 4) ** (m1 - a))
    else:
        A5 = Fr(1, 2 ** a) * (P_bin_lt(Kt - a, k - l0) + Fr(2) ** (1 - k + ellC + z(ns)))
    tot = A1 + A4 + A5
    return min(tot, Fr(1, 2 ** a)), dict(A1=A1, A4=A4, A5=A5)


def windows_ok(chain, Ms):
    for n, N in zip(chain, chain[1:]):
        L = N - n
        if not (beta(n) >= 2 * Ms + 1 and L + 2 * Ms <= beta(n) + 1 and beta(N) <= 2 * beta(n)):
            return False
    return True


def phi(J, n, N):
    L = N - n
    return L - (L - 1) // 2 - max(0, beta(N) - n + 1 - J)


def theorem_B(K, Ms, Mf, chain, ns, k, m1):
    rC, a = 14, 4
    G = 2 ** K
    T = G - 2 * K - 12
    nU = chain[-1]
    Lam = beta(nU) - 1
    Kt = flog2(T - ns - 2 * Lam)
    assert Ms >= 4 and Mf >= Ms and windows_ok(chain, Ms)
    assert ns >= nU and ns - s2(ns) >= 4 and Kt >= 4 and k >= 1
    assert m1 == 0 or 4 <= m1 <= min(ns - s2(ns), Kt)
    B1 = A1_sum(rC, a, T, G - T + 3)
    B2 = sum(mu_v(rC, a, i, Ms + 1) for i in range(1, nU + 1)) + \
        sum(mu_v(rC, a, i, Mf + 1) for i in range(nU + 1, ns + 2 * Lam + 1))
    B3 = sum(Fr(1, 2 ** (J + 1)) * Fr(2) ** (z(chain[0]) + sum(phi(J, chain[i], chain[i + 1]) for i in range(len(chain) - 1)))
             for J in range(4, Ms + 1))
    I0 = ns + TAIL_TERMS
    B4 = sum(mu_v(rC, a, i, beta(i - 1) - Lam + 1) for i in range(ns + 1, min(T, I0 - 1) + 1))
    B4 += tail_major(Lam, I0) if T >= I0 else 0
    ellB = min(Lam - 1, -(-(Lam + Mf) // 2) - 1) + flog2(2 * Lam)
    l0 = s2((14 + ns) % 16)
    if m1 >= 4:
        B5 = Fr(1, 16) * (P_bin_lt(Kt - m1, k) + Fr(2) ** (1 - k + ellB + z(ns) - l0) * Fr(3, 4) ** (m1 - 4))
    else:
        B5 = Fr(1, 16) * (P_bin_lt(Kt - 4, k - l0) + Fr(2) ** (1 - k + ellB + z(ns)))
    tot = B1 + B2 + B3 + B4 + B5
    return min(tot, Fr(1, 16)), dict(B1=B1, B2=B2, B3=B3, B4=B4, B5=B5, Lam=Lam, Kt=Kt, ellB=ellB)


def fmt(x):
    return "%.6e" % float(x) if x > Fr(1, 10 ** 300) else "<1e-300"


ROWS = {
    37: dict(C0=(8, 10, 4), C2=(14, 13, 5), C6=(12, 10, 10), B=None, logged="1.0051e-01",
             logged_parts=dict(C0="6.6557e-03", C2="2.0503e-02", C6="1.0847e-02")),
    40: dict(C0=(16, 10, 10), C2=(14, 12, 9), C6=(12, 11, 9), B=None, logged="9.1033e-02",
             logged_parts=dict(C0="8.0414e-03", C2="1.3683e-02", C6="6.8087e-03")),
    448: dict(C0=(88, 88, 85), C2=(80, 91, 76), C6=(90, 90, 85),
              B=dict(Ms=8, Mf=13, chain=[46, 67, 110, 194], ns=202, k=209, m1=0), logged="4.5555e-02",
              logged_parts=dict(C0="9.8138e-25", C2="1.2223e-24", C6="4.4658e-24", C14="4.5555e-02",
                                B="B1=2.6e-141,B2=2.7e-02,B3=5.2e-03,B4=1.5e-05,B5=1.4e-02")),
}


def main():
    for K, row in ROWS.items():
        print("== K=%d (G=2^%d); logged bound %s" % (K, K, row["logged"]))
        total = Fr(0)
        for cls in ("C0", "C2", "C6"):
            ns, k, m1 = row[cls]
            val, parts = theorem_A(cls, K, ns, k, m1)
            total += val
            print("  %s (ns=%d,k=%d,m1=%d): %s   [A1=%s A4=%s A5=%s]  logged %s"
                  % (cls, ns, k, m1, fmt(val), fmt(parts["A1"]), fmt(parts["A4"]), fmt(parts["A5"]),
                     row["logged_parts"][cls]))
        if row["B"] is None:
            c14 = Fr(1, 16)
            print("  C14: trivial 1/16")
        else:
            c14, bp = theorem_B(K, **row["B"])
            print("  C14 (Theorem B %s): %s  [B1=%s B2=%s B3=%s B4=%s B5=%s; Lam=%d Kt=%d ellB=%d]  logged %s / %s"
                  % (row["B"], fmt(c14), fmt(bp["B1"]), fmt(bp["B2"]), fmt(bp["B3"]), fmt(bp["B4"]), fmt(bp["B5"]),
                     bp["Lam"], bp["Kt"], bp["ellB"], row["logged_parts"]["C14"], row["logged_parts"]["B"]))
        total += c14
        print("  TOTAL bound on delta_G(2) = %s  (exact rational; float %.10f)" % (fmt(total), float(total)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
