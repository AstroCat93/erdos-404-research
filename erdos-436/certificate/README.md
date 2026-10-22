# Certificates

Each `kK_LL.cert.xz` is an xz-compressed stream in the `pairtree-cert 1` format, specified completely
in [`FORMAT.md`](FORMAT.md). A valid certificate with no `U` lines proves the statement C(k, L, S2):
every assignment R of values in Z/k to the primes ≤ L+1 with R(2) in S2 has some n ≤ L with
f_R(n) ≡ f_R(n+1) ≡ 0 (mod k). The identity of a certificate is the SHA-256 of the decompressed
stream (`SHA256SUMS.decompressed`). The SHA-256 of a `.xz` file (`SHA256SUMS`) also depends on the
compressor; these files were made with `xz 5.4.5 -9 -T1`.

| k | L | R(2) values | internal nodes (B) | leaves (L) | deepest branching prime | leaves with n = L | decompressed bytes | `.xz` bytes |
|---|---|---|---|---|---|---|---|---|
| 2 | 9 | all | 3 | 4 | 5 | 1 | 63 | 116 |
| 3 | 77 | all | 21 | 43 | 13 | 2 | 286 | 192 |
| 4 | 1224 | all | 167 | 502 | 41 | 2 | 3,084 | 812 |
| 5 | 7888 | all | 5,965 | 23,861 | 101 | 60 | 154,700 | 26,236 |
| 6 | 202124 | all | 7,739 | 38,696 | 277 | 34 | 255,504 | 43,348 |
| 7 | 1649375 | all | 1,381,693 | 8,290,159 | 491 | 156 | 58,540,515 | 7,696,052 |
| **8** | **1508324** | **0, 2, 4, 6** | **2,000,473** | **14,003,308** | **283** | **976** | **101,385,765** | **11,635,028** |

Only three certificates are used in the proof of Λ(8,2) ≤ 1508324 (paper, Theorem 3.2):

* `k8_L1508324` covers the primes p ≡ 1 (mod 8) with p > 1508325. R(2) is even because 2 is a
  quadratic residue of such p.
* `k4_L1224` covers p ≡ 5 (mod 8) with p > 1225, since then the 8th powers are the 4th powers.
* `k2_L9` covers p ≡ 3 (mod 4) with p > 10, since then the 8th powers are the squares.

The primes up to 1508325 are handled directly ((H3) of the paper). The certificates for
k = 3, 5, 6, 7 are a calibration: with all values of R(2) allowed, the same generator closes exactly
at the classical values Λ(k,2) = 77, 7888, 202124 and 1649375.
