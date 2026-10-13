#!/usr/bin/env python3
"""Round-3 computational referee (extra item): independent evaluation of the closed-form majorant in
the proof of R3Q Theorem C (note Theorem 11.7), transcribed from data/round3/reports/R3Q.md §7 only.

Rule R(K): M = floor(K/64); chain n1 = 6M, n_{i+1} = n_i + floor(n_i/2) (i = 1,2,3), nU = n4;
Lam = beta(nU) - 1; ns = nU + 2M; m1 = 0; k = ellB + z(ns) + M with Mf = M;
Theorem A classes: ns_A = 2M + 16, k_A = ellC + z(ns_A) + M.
Majorant terms (log2 form):
  B2  <= (2M+1) 2^-M
  B3  <= 2^(-2.125M + 2.05 + 6 log2(20.25M))
  B4  <= 2^(-2M + 2 log2(22.25M+1))
  B5b  = 2^(-M-3)
  B5a <= 2^(-0.0573(K-5) - 4)                  [needs q = (k-1)/(K-5) <= 0.36]
  A5  <= (1/4)(2^(1-M) + 2^(-0.75(K-5)))        [needs q_A = (kA-1)/(K-1-a) <= 0.04]
  A4  <= 3 * 2.05 * 2^3 * (2M+16)^2 * 2^(-2M-16)
  A1+B1 <= 2^(-K+1)
Checks: majorant <= 2^(-K/80) for K in [3072, 4e6]; largest failing K in [2400, 3071];
minimum margin (bits); q and q_A computed EXACTLY from the rule for every K.
"""
import math, time


def s2(n):
    return bin(n).count("1")


def beta(n):
    return n - s2(n) - (n.bit_length() - 1)


def z(n):
    return -(-n // 2) - 1


def lse2(xs):
    mx = max(xs)
    return mx + math.log2(sum(2.0 ** (x - mx) for x in xs))


def main():
    t0 = time.time()
    worst_q = worst_qA = 0.0
    last_fail = None
    min_margin, argmin = 1e9, None
    for K in range(2400, 4_000_001):
        M = K // 64
        n = 6 * M
        for _ in range(3):
            n = n + n // 2
        nU = n
        Lam = beta(nU) - 1
        ns = nU + 2 * M
        ellB = min(Lam - 1, -(-(Lam + M) // 2) - 1) + ((2 * Lam).bit_length() - 1)
        k = ellB + z(ns) + M
        q = (k - 1) / (K - 5)
        worst_q = max(worst_q, q)
        for a, lam in ((3, 1), (4, 3)):
            ellC = 0 if lam == 1 else (lam - 1) + ((2 * lam).bit_length() - 1)
            kA = ellC + z(2 * M + 16) + M
            worst_qA = max(worst_qA, (kA - 1) / (K - 1 - a))
        terms = [math.log2(2 * M + 1) - M,
                 -2.125 * M + 2.05 + 6 * math.log2(20.25 * M),
                 -2 * M + 2 * math.log2(22.25 * M + 1),
                 -M - 3,
                 -0.0573 * (K - 5) - 4,
                 -2 + (1 - M), -2 - 0.75 * (K - 5),
                 math.log2(3 * 2.05 * 8) + 2 * math.log2(2 * M + 16) - 2 * M - 16,
                 -K + 1]
        lg = lse2(terms)
        margin = -K / 80 - lg
        if margin < 0:
            last_fail = K
        elif K >= 3072 and margin < min_margin:
            min_margin, argmin = margin, K
    print("largest K in [2400, 4e6] with majorant > 2^(-K/80):", last_fail)
    print("minimum margin on [3072, 4e6]: %.4f bits at K=%d" % (min_margin, argmin))
    print("max q = (k-1)/(K-5) over [2400, 4e6]: %.5f (report: <= 0.36)" % worst_q)
    print("max q_A over [2400, 4e6]: %.5f (report: <= 0.04)" % worst_qA)
    print("1 - H(0.36) = %.5f, 1 - H(0.04) = %.5f" % (1 - (-(0.36 * math.log2(0.36) + 0.64 * math.log2(0.64))),
                                                     1 - (-(0.04 * math.log2(0.04) + 0.96 * math.log2(0.96)))))
    print("time %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
