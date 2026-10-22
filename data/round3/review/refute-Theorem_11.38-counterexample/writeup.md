# Counterexample hunt: Theorem 11.38 (note_v3.md §11.4), round 3, 2026-10-21

All code written from scratch in this directory (no reuse of T3a code). Runs: single core, <3 s each, <0.5 GB.

## Commands and timings
- `python3 gamma_theta.py` (0.8 s) -> gamma_theta.log: Gamma_p(1), J_0(p), dist_p(j), covering depth, theta_p, 1-theta^set_p for p in {2,...,19} by meet-in-the-middle over the 3^p weighted sign vectors (exact Fractions), series summed to j=400 in mpmath (40 digits).
- `python3 ck_check.py` (1.6 s) -> ck_check.log: C_k for 24 (p,N0) cases incl. p not dividing N0 (float64 DP mod p^k, p^k <= 4.2e6), checked level by level against Thm 11.36(iv) (C_{a+j}/C_a <= 1+Gamma_group(j)) and Lemma 11.37(a) (full-block Gamma equals Gamma_p(j)), and the full product bound.
- `python3 sum_check.py <dir>` -> sum_check.log: the counting step S(k) = sum_{blocks below level k} f_p(J_m - 1) versus theta_p k, k up to 10^6, p in {2,3,5,7,13}.
- `python3 theta3_closed.py` -> theta3_closed.log: closed form theta_3 = (4/9)[log_3(33/32) + 7/4 - 2 log_3 2] in mpmath interval arithmetic (50 digits).

## Results
1. [computer-assisted] Lemma 11.37 table reproduced exactly (Gamma_p(1), J_0, covering depth) for all eight primes.
2. [computer-assisted] theta_p values agree with the note to all printed digits: 0.3962406252, 0.2294000283, 0.1101338076, 0.02660793049, 0.00623569904, 9.076755152e-4, 8.410653547e-5, 3.406650642e-5; 1-theta^set: 0.64624062518, 0.806873278571, 0.923694745532, 0.985556825536, 0.998268316014, 0.999656751178, 0.999965432719, 0.99999322551.
3. [computer-assisted] No violation of Thm 11.36(iv) or Lemma 11.37(a) in any group of any of the 24 cases; log_p C_k always well below the product bound (e.g. p=3,N0=8,k=13: 1.508 vs 3.490). C_k values agree with Computation 11.43 where depths overlap.
4. [computer-assisted] S(k) - theta_p k < 0 for every level up to 10^6 (max of (S-theta k)/log_p^2 k is negative), consistent with the proof's counting step.
5. Proof re-read: P_m(r) = prod_{i<=r}(p(m+1)-(p-i)) == (-1)^r (p-1)!/(p-1-r)! mod p^{J_m} gives Lemma 11.37(a) (eps_2 = -1 checked); block jumps J_m = 1+v_p(m+1); M < (p-1)/p (k+e_0) + s_p(M)/p. No logical gap found.

## Concrete defects (rounding direction of stated constants)
- **theta_3 <= 0.22940 is false.** Interval arithmetic: theta_3 in [0.22940002828619378726, 0.22940002828619378727] > 0.2294. The table entry rounds *down*; the excess 2.8e-8 k is not absorbed by O(log^2 k), so "log_3 C_k <= 0.2294 k + O(log^2 k)" is not what was proved. Fix: write 0.229401 (or 0.22941).
- **"dim_H E_{N0} >= 0.99966 at p=13" (Corollary 11.39(b), line 2251, and §0 item 23, line 126) is false as a consequence of the proof:** 1-theta^set_13 = 0.99965675... < 0.99966. The table's own entry 0.999656 is correct. Fix: 0.999656.
- Cosmetic: "log_2 3/4 = 0.39624" in the theta_p <= row rounds down (true value 0.3962406); harmless because the exact value is stated, but write 0.396241 for consistency.
All other table entries are valid upper/lower bounds.
