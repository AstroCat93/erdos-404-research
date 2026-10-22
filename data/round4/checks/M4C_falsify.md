# Check of track M4C (Theorem M): numerical falsification and independent recomputation

Date: 2026-10-14. Object: `data/round4/reports/M4C.md`, Theorem M (§7): for every prime 11 ≤ p ≤ 97, μ(K_p ∩ p³ℤ_p) ≥ c_p p⁻³, with c₁₁ ≥ 1.25·10⁻⁴ (also printed as 1.254·10⁻⁴), c₁₃ ≥ 0.572, and c_p ≥ 0.69 for 17 ≤ p ≤ 97.
Lens: numerical falsification and independent recomputation. R3M's Theorem C3 is taken as given; its hypotheses are checked.
Code: `code/round4/verify_C_falsify/`. Logs: `data/round4/verify_C_falsify/` (each run starts with `### command:` and `### start:`, and ends with `### wall:`).
Independence: none of this code imports, copies or reads `code/round4/M4C/`. Everything was implemented from the text of M4C.md and R3M.md §5. Only the M4C logs (`assemble.log`, `check_assemble.log`, `qtable.log`) were read, for comparison.

## Verdict: **confirmed-with-fixes** (numerical lens)

- Every number in Theorem M was reproduced by an independent implementation, for all 21 primes, not only the five requested: the constants q₁, q₂, q₃, the greedy schedules, every s_k, Π_A, δ_A, c_p, μ(K_p), ℓ*−k₀ and κ_p. The printed c_p and μ(K_p) are valid lower bounds, rounded down, and the printed log Π_A and δ_A in the report are valid upper bounds.
- None of the lemmas I tested failed, in exact arithmetic, anywhere. That covers Lemmas H2, P, Q and L, the identity inside Prop H′, Props P1 and W, Lemma T′ ≥ T, and the far-tail rate. Each test includes controls, which do fail, so the tests can detect errors.
- **The fix is cosmetic only.** In `assemble.log`, the lines "delta_A <= …" print δ_A rounded to nearest at 10 significant digits. For 11 of the 21 primes the printed value is below the true δ_A, by less than 10⁻¹³ (see "Discrepancies" below). The report's §7.3 table is correctly rounded up, and no c_p is affected.
- **Limits of this lens.**
  - Lemma T is the bound actually used for the phase-2 windows. Its inequality could not be tested at the real window sizes, where K ≳ 40 makes ε impossible to compute exactly. Only its ingredients (H2, the H′ identity, Lemma Q) were tested, at small sizes, together with three small ball-averaged analogues of the whole chain.
  - The proofs of Lemmas Q and T were not re-derived line by line. That is the logic check's job.
  - At p = 11 the certificate has a thin margin (Π_A δ_A = 0.928; see "Sensitivity at p = 11").

## (1) The constants q₁, q₂, q₃: independent exact recomputation

Script: `qconst_indep.py`. Log: `qconst_indep.log`.

**Method 1, exact.**
- For q₁ and q₃, a weighted count DP over the residues mod p and mod p³ (weights 2, 1, 1 for the digits 0, +1, −1).
- For q₂, the state is A − pB mod p², with B = Σδ_r·(r!H_r mod p). This encodes the pair (A mod p, ⌊A/p⌋ − B mod p) bijectively.
- The DP runs modulo up to 10 word-size primes, with CRT reconstruction of the **whole** count vector. The program asserts that the counts sum to 4^p and that the maximum is attained at residue 0, as the autocorrelation argument of §4.1 says.

**Method 2, independent floating point.** q − 1 = Σ_{ξ≠0} Π_r cos²(πξc_r/m) is a sum of nonnegative terms, so it is accurate in relative terms.

**Method 3, brute force (p = 11, 13).** All 3^p signed vectors are enumerated, with the integer A and Python floor division. This checks the reading of ⌊A/p⌋ for negative A.

**Results:**
- All three methods agree for every prime. Methods 1 and 2 agree to a relative 3·10⁻¹⁴ or better, and brute force equals method 1 as rationals at p = 11 and 13.
- Exact values at p = 11: q₁ = 525041/524288, q₂ = 1165593/1048576, q₃ = 1888689/1048576.
- Exact values at p = 13: q₁ = 33555171/33554432, q₂ = 1057095/1048576, q₃ = 10002941/8388608.
- `compare.py` (log `compare.log`) compares all 21 × 3 values with the §4.3 table: **0 mismatches beyond the 3-digit rounding.**
- The 4-digit values in `qtable.log` also agree.
- The statement of §9.2 (AC(p) holds for every 13 ≤ p ≤ 97 and fails at p = 11) is confirmed.

| p | q₁−1 | q₂−1 | q₃−1 |
|---|---|---|---|
| 11 | 1.436234e-3 | 1.115961e-1 | 8.011942e-1 |
| 13 | 2.202392e-5 | 8.124352e-3 | 1.924435e-1 |
| 17 | 6.093178e-7 | 2.898074e-4 | 2.256895e-2 |
| 23 | 5.423033e-9 | 2.262841e-6 | 1.157882e-3 |
| 31 | 7.455405e-11 | 1.234945e-7 | 2.145758e-5 |
| 43 | 8.355892e-13 | 8.755455e-13 | 1.712836e-9 |
| 97 | 2.093613e-43 | 4.069334e-34 | 3.094217e-29 |

(The full list for all 21 primes is in the log.)

## (2) Exact tests of Lemmas H2, P, Q, Prop H′, Prop P1, and Lemma L

All probabilities below are exact rationals: CRT-reconstructed integer counts over 4^t.

| object | script / log | setting | trials | result |
|---|---|---|---|---|
| Lemma H2 | `test_H2.py` / `test_H2.log` | p = 7, 11, 13; balls b + p^rℤ_p with 2r ≤ D < K. Five families of F: signed window sums (half of them with B near a gate), planted near-double roots, planted near-triple roots, the (y+2)² path near −2, random polynomials | 2342 / 1171 / 605 | **0 failures in 4118**. Left side > 0 in 740 trials. Max left/right 0.9932, 0.9924, 0.9970. Control (2v(F′) ≥ D+2) violated 77, 62 and 27 times |
| identity inside Prop H′ (first-nonzero index, both signs, derivative threshold) | `test_identity.py` / `test_identity.log` | random z with random gate offsets, 30% with a deep gate, (2.2) imposed; both sides exact | p = 7: 25, p = 11: 25, p = 13: 20 points | **70/70 exact equalities** |
| Lemma P | `test_PQ.py` (random and J modes) / `test_PQ.log` | random y with planted deep gates, k up to 5, δ₀ lazy or fixed to 1 | p = 11: 51, p = 13: 6 | 0 violations. Max ratio ≤ 1; equality occurs, as expected when only block 0 counts |
| Lemma Q | `test_PQ.py` (edge grid, J mode, random mode) / `test_PQ.log` | grid over g₁ ∈ {1, 2, p−1, p}; deep gate (depth 2 or 3) at gate 1, 2, 3, 4 or none; f ≤ 5; k ∈ {f+d_max, f+d_max+1}; δ₀ lazy or fixed; full or partial last block; every test has J ≠ ∅ | p = 3: 780, p = 5: 560, p = 7: 272, p = 11: 32 (+17 with J = ∅), p = 13: 6 | **0 violations in 1650 J-tests**. Max ratio 0.9559 (p = 3), 0.9906 (p = 5), 0.9911 (p = 7), 0.9989 (p = 11), 0.9989 (p = 13). Control (q₂/p³ per J-block) violated in 303, 248, 146, 17 and 2 tests |
| Prop H′ + Lemma P/Q chain (ball average) | `test_Hball.py` / `test_Hball.log` | p = 7, balls of radius p², D = 4 = 2r, K = 5: exact E_B[ε] against c_{L+L′} + Σ_j (c_j/2)·E_B[Lemma Q/P bound] | 3 balls (343 points each) | holds. E_B ε ≈ 10⁻⁸–10⁻⁶ against bounds 0.27–5.1. This is a weak test; see below |
| Prop P1 (i) and (ii) | `test_P1.py` / `test_P1.log` | own greedy schedule; random x = p³u with extra p-power and sign; exact valuations; exact ε = p^K Coll_K − p^D Coll_D for every phase-1 window with K ≤ 7 (p = 7) or K ≤ 5 (p = 11, 13) | lin: 120 / 144 / 130; ε: 60 / 48 / 40 | 0 failures. Every ε ≤ 0.091 × bound (the bound is very loose). The windows with a depth-2 end gate (n₂ = 1) were included: p = 7, k = 3, 4 and p = 11, k = 4. 1 + χ²_{W₀} = q₁ exactly at p = 7, 11, 13 |
| Lemma L(b) and the identity of L(a) | `test_L.py` / `test_L.log` | the actual phase-2 windows with b_{ℓ+1} ≤ 6000 at p = 11, 13, 17; x ∈ G_ℓ either random or adversarial (a planted gate of the maximal depth s allowed in G_ℓ inside the window) | 119 / 120 / 72 points in G_ℓ | **0 lin failures**. v(x+jp) = 3 + v(ξ′ + j/p²) in every case. M4C's own §8 table lists Lemma L as untested |

**Edge-case coverage of Lemma Q.** The tests include:
- J-blocks that start at a deep gate (d_i = 2 or 3; the ε_i = 0 branch of the proof): p = 3, 5, 7 (32 tests at p = 7 with 7⁸ states);
- J-blocks followed by a deep gate at i+2;
- consecutive J-blocks, with up to |J| = 3;
- f = k − d_max exactly;
- a fixed δ₀ = 1, which is the case of Λ.

Deep starting gates could only be reached at p ≤ 7, because the state space p^{k+f} becomes too large at p ≥ 11.

**Observation: Lemma Q is essentially sharp.**
- The maximal ratio 0.9989 at p = 11 and 13 occurs for all-depth-1 gates, g₁ = 1, J = {1}, k = 3, f = 2 and δ₀ lazy. Block 0 then forces δ₀ = 0, the prescribed value of Φ₁ is the mode, and the 1D blocks are almost uniform (q₁ ≈ 1).
- M4C's own test reports a maximal ratio of 0.4996 at p = 11, so it did not sample these configurations.
- Sharpness means the tests are sensitive, and the lemma still held in every case.

**Limits.**
- The ball-averaged chain test is weak: at these sizes the Lemma Q/P bounds are far above E_B ε.
- The exact H′ right-hand side (E_B Λ^{(λ)}) was too expensive at p ≥ 5 within the budget. H′ is covered instead by its two exact components: H2 for each fixed δ, and the pointwise identity.

## (3) Proposition W

Script: `test_W.py`. Log: `test_W.log`.

**Method.** For every prime 7 ≤ p ≤ 97 I took 40 random x = p³u, with u up to p²⁵, some with extra p-divisibility and some negative. For each x:
- the first block is {0, p−1}, or the explicit block at p = 13;
- the second block is a **random** solution of the stated congruence Σe_{p+u}u! ≡ w_p/(ξ+1), or (k_e + ξλ_e)/(ξ+1) for a general first block;
- the third block is a random subset that cancels the p² digit;
- S_e(x) and S′_e(x) are then evaluated as exact integers.

**Results:**
- In 40/40 cases for every prime: V_{3p}(x) = 3, M_{3p} = 1, v(x+4p) = 1 and M_{4p} = 1 (the admissibility data). S_e ≡ 0 mod p² after the second block, the path is alive at 3p, and S′_e ≡ −w_p/(ξ+1) mod p.
- The slope is 0 in 40/40 cases for every non-Wilson prime.
- At the Wilson prime 13 the block {0, 12} gives slope 0 in 0/40 cases, as predicted. The explicit block {0, 1, 2, 3, 4, 8, 9} gives slope 0 in 40/40. I recomputed Σj! = 403234 = 13·31018, k_e ≡ 0 and λ_e ≡ 12 (mod 13), as stated.
- The general criterion "slope 0 iff λ_e ≢ k_e" was tested on 60 random admissible first blocks per prime. It agrees in 60/60 every time, and both directions occur.

## (4) The certificate (Π_A, δ_A, c_p): independent recomputation

Script: `cert.py`. Log: `cert.log`. Comparison: `compare.py`, log `compare.log`.

**What was implemented, from the report text alone.**
- The greedy phase 1 under (6.1).
- The phase-2 rules: the s-rule, b_{k+1} as the (T1)-maximal value capped by 2b_{k−1} and by b_k + ⌈1.6(b_k − b_{k−1})⌉, the far-tail rule ⌊5b_k/4⌋, and the switch at b_{k−1} > 3000.
- Lemma T term by term for N ≤ 6000, and Lemma T′ otherwise.
- The remainder η2^{−(ℓ*−k₀)+1} + 10⁻¹⁰⁰⁰.
- c_p = (1 − √(Π_Aδ_A))²/Π_A.

(T1), (T2) and N ≥ p are asserted in integer arithmetic for every window. As a by-product, Lemma T′ ≥ Lemma T was checked on every window with N ≤ 6000: 0 failures, with a minimum log-margin of 13.4. I ran all 21 primes.

| p | log Π_A | δ_A | c_p (recomputed) | printed c_p | μ(K_p) ≥ (recomputed) | printed | ℓ*−k₀ |
|---|---|---|---|---|---|---|---|
| 11 | 2.36257158730 | 0.0874274367768 | 1.25497932·10⁻⁴ | 1.254·10⁻⁴ (headline 1.25·10⁻⁴) | 9.42885·10⁻⁸ | 9.42·10⁻⁸ | 595 |
| 13 | 0.199392226400 | 0.0219904749557 | 0.572777376 | 0.572 | 2.60709·10⁻⁴ | 2.60·10⁻⁴ | 595 |
| 17 | 0.00839859350143 | 0.00938686440007 | 0.808063776 | 0.808 | 1.64475·10⁻⁴ | 1.64·10⁻⁴ | 592 |
| 23 | 1.00147708·10⁻⁴ | 0.00858747917805 | 0.823159312 | 0.823 | 6.76551·10⁻⁵ | 6.76·10⁻⁵ | 591 |
| 97 | 7.2434153·10⁻³² | 0.021615897385 | 0.727568980 | 0.727 | 7.97185·10⁻⁷ | 7.96·10⁻⁷ | 581 |

**Comparison with the report (all 21 primes, `compare.log`).**
- The phase-1 schedules and k₀ coincide with `assemble.log` for all 21 primes.
- All 81 explicit phase-2 windows have identical integer data (ℓ, blocks, s, N_W, N, I), and their μ(G^c) and ε̄ = √𝔅 agree to the printed precision.
- Π_A agrees to all 15 printed digits, δ_A to all 10 printed digits, and c_p to all 10 digits printed by `check_assemble.log`.
- Every §7.3 entry passes: log Π_A and δ_A are upper bounds, c_p and μ(K_p) are lower bounds, and ℓ*−k₀ is equal.
- The headline's c₁₁ ≥ 1.25·10⁻⁴ and the table's 1.254·10⁻⁴ are both valid roundings down of 1.25498·10⁻⁴. The minimum c_p over 17 ≤ p ≤ 97 is 0.69200 (p = 41), so "c_p ≥ 0.69" holds.
- In the μ(K_p) column four entries are rounded down further than necessary (p = 31, 47, 53, 97: for example 2.91 against the true 2.920·10⁻⁵). They are still valid lower bounds.

**Far tail (`far_tail.py`, log `far_tail.log`).**
- From the Lemma T′ formula and the far-tail schedule (N_W ≥ b/4 − 1, N ≤ 9b/16 + 1, s = O(log b)) I derived the decay rate in b:
  κ_p = (1−1/p)|log ρ|/(8α) − (9/16)[log q₁ + (log q₂)/p + (log q₃)/p² + (log p)/(p²(p−1))].
  It reproduces every printed κ_p, e.g. 0.226719 at p = 11 and 0.560106 at p = 97; every printed value is at or below the analytic one.
- Continuing the explicit schedule from 10⁶⁰ to 10²⁰⁰ (about 1444 more windows each) at p = 11, 13 and 97:
  - (T1), (T2) and N ≥ p hold in every window;
  - s_k ≤ 3 + 10 ln b holds in every window;
  - max log(T′)/b equals −κ_p;
  - δ_A and c_p are unchanged.
- This supports the analytic remainder argument of §7.2.

**Sensitivity at p = 11.**
- Π_Aδ_A = 0.9283, so the slack is 1/Π_A − δ_A = 0.00675.
- The certificate would fail if the bound 𝔅 of the first phase-2 window, (105, 120, 144] with √𝔅 = 0.0592, were about 22% larger, or if log Π_A were 3.1% larger.
- So c₁₁ > 0 depends on Lemmas T and Q holding with essentially no loss on that window. Nothing in my tests suggests they fail, and the margin is a feature of the bound, not an error. For p ≥ 13 the margins are large: Π_Aδ_A ≤ 0.027.

## Hypotheses of Theorem C3 (R3M §5), checked numerically and exactly

- n₀ = 3p ≥ 2p.
- A = p³ℤ_p is an atom of 𝒢₀: m₀ = V_{3p}(x) = 3 on A (checked on random x).
- Admissibility: D₀ = v(x+4p) = 1 ≤ m₀ − M_{4p} = 2 and M_{4p} = 1 < 3 (checked). Z⁰_{3p} ≥ 1 on all of A (Prop W, checked).
- 1 + χ²_{W₀} = p·Coll₁([3p, 4p)) = q₁: exact equality at p = 7, 11, 13.
- The thresholds ε̄_ℓ are deterministic and nonnegative, with Π < ∞.
- B_ℓ ⊇ G_ℓ ∩ {ε_ℓ ≤ ε̄_ℓ} in phase 2 (Lemma L(b), checked on G_ℓ). In phase 1, lin and ε ≤ ε̄ hold everywhere (P1, checked).
- FE: Π_Aδ_A < 1 for every listed p (recomputed).

## Discrepancies found (exact)

1. **Cosmetic (fix recommended).** The lines `RESULT p=…: … delta_A <= X` in `assemble.log` print X rounded to nearest at 10 significant digits. For p = 17, 23, 29, 43, 47, 53, 59, 67, 71, 79 and 97, X is below the recomputed δ_A. For example, at p = 17 X = 0.0093868644 while δ_A = 0.00938686440007; the excess is at most 7·10⁻¹⁴. The δ_A in M4C.md §7.3 is correctly rounded up, and c_p is computed from the unrounded value, so no conclusion changes. `check_assemble.log` prints the same rounded values.
2. **Not a discrepancy.** M4C's log Π_A at p = 89 and 97 is larger than mine by about 10⁻³⁶. This comes from their deliberate outward rounding of q by a relative 10⁻⁴⁰, which is large compared with q₁(97) − 1 = 2·10⁻⁴³. It is conservative.
3. **Not a discrepancy.** The p = 7 phase-1 schedule (3, 4, 5, 6, 7, 9, 13, 16, 23, 30, 44, 48) was computed only for the P1 test. Theorem M does not claim p = 7.

## Resource note

About 80 core-minutes in total, at nice 10 and on one core at a time. About 35 of those were lost to a bug in my own test generator: it demanded more consecutive non-gate residues than exist modulo 3 and 5, and looped until killed. This is noted in `test_PQ.log` and `test_Hball.log`; the runs were fixed and rerun, except the p = 5 ball test.
