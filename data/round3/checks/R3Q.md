# Adversarial check of track R3Q (round 3, 2026-10-13): an explicit rate for δ_G(2)

Checker: check_R3Q. Code: `code/round3/check_R3Q/` (see its README). Logs: `data/round3/check_R3Q/`. Scratch: `/tmp/r3_check_R3Q/`.
Track material read (read-only): `data/round3/reports/R3Q.md` (all 481 lines), `code/round3/R3Q/v2/` (bounds.py, rule.py, rule_K0.py, rule_A.py, common.py, run_logs.sh), the earlier instance's scripts where the report refers to them, `data/round3/R3Q/*.log`, and note.md §10.1 (Lemma 10.2–Prop. 10.7, proof of Theorem 10.1), §4.7, §10.1.4.
CPU used: about 19 core-minutes on one core (all jobs `nice -n 10`, strictly sequential; nothing else touched).
Every program of this check was written from the statements in the track report and shares no code with `code/round3/R3Q/`.

## 0. Verdicts

| id (as in the track report) | claim | verdict |
|---|---|---|
| Lemma 1 | valuation facts (a)–(e): V_{n+i}−V_n ≥ max(i−s(i), ⌊i/2⌋); truncated sum bound; V_n−M_n ≥ β(n), monotonicity; Taylor valuations; walk drop | **confirmed** (line by line; 90 000 random exact checks, §2) |
| Lemma 2 | truncation g_2 ≥ G, V_N ≤ G ⇒ P_N ≠ ∅; backward integrality; M_T ≤ G−T+2 ⇒ V_T ≤ G | **confirmed** |
| Lemma 3 | uniform slopes 1, 3, 3 on C_0, C_2, C_6; g_2 ≤ 6 on 10+16ℤ_2, ≤ 3 on 4+8ℤ_2 | **confirmed** [computer-assisted]: reduction checked line by line; third, independent certificate (dual numbers) gives the same 4/32/128 qualifying words, 0 violations, 0 words in (d),(e), also with 1 and 2 extra bits of x |
| Lemma 4 | Z_n ≤ 2^{⌈n/2⌉−1} | **confirmed** (proof; 3000 random populations) |
| Lemma 5 | one-step identity E Σ_f ρ_{n+1} = 2^{1−D} ρ_n under λ+D ≤ m−M_n, λ < m−M_n | **confirmed** (line by line; 15 051 parents, 12 103 with λ ≥ 3, every child recomputed from scratch at every x' = x+2^m w, w mod 2^{D+λ+1}; 0 failures; negative control ρ := 1 fails for 3976). Minor citation fix in Prop. 7 (§1.5) |
| Lemma 6 | weights: mean 1; ρ ≤ 2^{min(λ−1, ⌊(λ+M̃)/2⌋−1)}; ρ ≥ 2^{−⌊log₂2λ⌋} on paths surviving 2λ steps | **confirmed** (line by line; 3000 upper-bound checks, bound attained 739 times; 1335 lower-bound checks) |
| Prop. 7 | stopped martingale bound with digit split | **confirmed** (line by line; filtration, stopping time, integrability, digit split all checked; one citation should be made precise, §1.5) |
| Thm A | explicit bound on C_0, C_2, C_6 | **confirmed** [computer-assisted only through Lemma 3]; every table entry re-derived exactly by an independent evaluator |
| Thm A′ | μ(C ∩ {g_2 ≥ 2^K}) ≤ 2^{−K/7}, K ≥ 1024 | **confirmed-with-fixes**: proof and constants correct; closed-form check reproduced on [1024, 4·10⁶] (min margin 4.52 bits); exact rule values reproduced. Fix: the §4 heading says "[proved, given Lemma 3]" but the proof rests on a computer check over K ∈ [1024, 4·10⁶]; use [computer-assisted] as in §0 |
| Lemma 8 | v(S_e) ≥ 3j+1 ⇒ v(S_e') ≤ 2j or v(S_e^{[2]}) ≤ j (x ≡ 2 mod 4, j = v(x+2)) | **confirmed** (proof checked line by line, including the coefficient table m! mod 16 and the parity of α_{m,2}; 17 019 random checks, 6897 with slope > 2j, 0 failures) |
| Remark after Lemma 8 | on Ω: multiplicity 1 on 8ℤ_2, ≤ 2 on 2+4ℤ_2; K^{k,L} = ∅ for k ≥ 3 | **confirmed** (side remark, not used) |
| Lemma 9 | U-window bound on coarse atoms x+2^{V_n−M_n}ℤ_2 | **confirmed** (line by line; 5425 random windows, 418 with U_n ≠ ∅, (a),(b),(c) and the Taylor congruence of (d) checked at every w (5.6·10⁶ checks), κ ≤ j in 5018 cases, bound attained (ratio 1.000), 7 non-empty windows with the decay factor active, 0 failures) |
| Cor. 9′ | (W1)–(W3) ⇒ (H1)–(H4) with Θ_t = β(t); factor 2^{φ_j} | **confirmed** |
| Prop. 10 | μ(C_14 ∩ {U_{n_t} ≠ ∅, M_{n_t} ≤ M*}) ≤ B_3 | **confirmed** |
| Thm B | explicit bound on C_14 | **confirmed** (one harmless slack: ⌈(Λ+M_f)/2⌉ where Lemma 6(b) gives ⌊·⌋) |
| Cor. D | staircase table for δ_G(2) | **confirmed-with-fixes**: all 30 rows reproduced exactly by an independent evaluator (worst relative difference 4·10⁻⁴, i.e. rounding of the printed values), all hypotheses re-checked. Fix: several prose bounds are rounded *down*, so they are slightly false as stated: "≤ 0.1005" (exact 0.100506), "≤ 0.0910"/"≤ 0.091" (0.091033), "≤ 4.9·10⁻⁶" (4.9359·10⁻⁶), "≤ 0.0285" (0.028533); see §4 F1 |
| Thm C | δ_{2^K}(2) ≤ 2^{−K/80} for all K ≥ 3072 | **confirmed-with-fixes**: proof and every constant checked; closed form reproduced (largest failing K in [2400, 4·10⁶] is 3071; min margin on [3072, 4·10⁶] is 0.625 bits at K = 3135); exact rule values ≤ 2^{−K/80} at every K ∈ [3072, 3264] and at the worst K of every M-block up to K = 25 663 (margin ≥ 2.25 bits). Fix: the §7 heading label "[proved, given Lemma 3]" and "fully proved rate" in §8 should be [computer-assisted], as in the headline and §0 |
| §11 failed attempt | single digit-sum drop caps the method near G^{−0.227} | **confirmed** (arithmetic: q = 1−H(q) at q ≈ 0.2272) |
| §11 obstruction "large slopes" | per-slope accounting cannot work | **label-too-strong**: the decay rate 2^{−λ/2} it relies on is a numerical observation (4000 samples); relabel [heuristic] |
| §11 heuristic "weights" | median/max of max_s ρ | label correct; **unverified** (not re-run) |

Nothing here bears on Q3 or on whether f(a,2) < ∞ for every a, as the track report says.

## 1. Line-by-line check

Notation as in the track report and note §10.1.

### 1.1 Lemma 1 [confirmed]
- (a) Standard counting; the ⌊i/2⌋ part uses that x+n+t is even iff n+t is even. Correct.
- (b) The bound ⌈L/2^ℓ⌉ ≤ (L−1)/2^ℓ + 1 is right (⌈L/q⌉ = ⌊(L−1)/q⌋+1). The strict inequality needs L ≥ 2 and μ_L ≥ 1, as stated; for L = 1 the bound L−1+μ_L is an equality. The truncated version is correct because Σ_i min(v,c) = Σ_{ℓ≤c} #{2^ℓ | y+i}. Correct.
- (c) V_n − M_n = Σ_ℓ (c_ℓ−1)^+ is right (M_n = #{ℓ : c_ℓ ≥ 1}), and the sum over ℓ ≤ ⌊log₂n⌋ of ⌊n/2^ℓ⌋−1 is n−s(n)−⌊log₂n⌋. Both monotonicity arguments are correct (β(n+1)−β(n) = t − [n+1 = 2^a] with t the number of trailing ones of n).
- (d) Correct (needs x+t ≠ 0, i.e. x not a negative integer; excluded globally).
- (e) Both cases r = 0 and r > 0 recomputed; V_{n_0+N_K} − V_{n_0} ≥ N_K − 1 + s(r). Correct.

### 1.2 Lemma 2 [confirmed]
(a) uses that a sup of integers ≥ G is attained by some finite B (G integer). (c) is Lemma 1(b) with T ≥ 2. Correct.

### 1.3 Lemma 3 [confirmed, computer-assisted]
- Reduction: re-derived the valuation patterns (C_0: V_6 = 4, M_6 = 2; C_2: V_8 = 7, M_8 = 3; C_6: V_10 = 7+v(x+10) ≥ 11, V_10 − M_10 = 7; C_10: V_6 ≥ 7; C_4: V_4 ≥ 4), and confirmed them by brute force over x mod 2^20 (`cert3.log`). The propagation step uses v(π_j') ≥ V_j − M_j ≥ V_{n_0} − M_{n_0} > λ (Lemma 1(c),(d)). For (iv) the report correctly uses the *proof* of Lemma 2(a) (v(S_e) ≥ min(7, V_6) = 7) rather than its statement, since V_6 may exceed 7. Correct.
- Finite checks: `cert3.py` carries (π_j, π_j') mod 2^c as dual numbers and enumerates all words by subset-sum tables (a different method from both track programs). Result: (a) 4, (b) 32, (c) 128 qualifying (word, residue) pairs, 0 violations; (d), (e) no qualifying word. Re-run with x mod 2^{c+1} and 2^{c+2}: same verdicts (counts ×2, ×4). The certificate size 128·512 = 2^16 matches the headline.

### 1.4 Lemmas 4–6 [confirmed]
- Lemma 4: the levels V_1 < V_2 ≤ … with strict increase at even indices give 1 + ⌊(n−1)/2⌋ distinct levels, of which at most the top one (n odd, V_{n−1} = V_n) is not < V_n; so r ≥ ⌊n/2⌋ and Z_n ≤ 2^{n−1−⌊n/2⌋}. Correct.
- Lemma 5: every step re-derived. (a) M_n < m and D < m follow from λ ≥ 1 (or λ = 0 with the strict hypothesis). (b) is Lemma 10.5(b) with base point x; the bracket is integral and (1+E)^{-1} ≡ 1 mod 2^{m−M_n}. (c): the substitution t = f + 2^D y, the constancy of u = (x'+n+1)/2^D mod 2^λ (needs D+λ ≤ m) and of ρ^{(λ)}_{n+1} on C (needs λ ≤ m), and Q_n = g_0 + (x+n+1)Q' are all correct; both sides equal 2^{λ−D} Σ_f P(2^D u Q' ≡ τ_0 − f mod 2^λ). The λ = 0 case also holds (t is then uniform mod 2^D).
- Lemma 6: (b) the r ≥ ⌈I/2⌉ distinct levels and the truncated Lemma 1(b) with L = I ≤ 2λ (μ ≥ 1 because I ≥ 2) give r ≥ ⌈(λ+2−M̃)/2⌉, i.e. ρ ≤ 2^{⌊(λ+M̃)/2⌋−1}; the I = 1 case is covered. (c) the digit-sum claim "every integer in [0, 2λ−1] has digit sum ≤ ⌊log₂(2λ)⌋" is true (the only integer below 2^{a+1} with digit sum a+1 is 2^{a+1}−1 ≥ 2λ when 2^a ≤ 2λ < 2^{a+1}, since 2λ is even). Correct.

### 1.5 Proposition 7 [confirmed; one citation to make precise]
- Non-failing step ⇒ Lemma 5 hypotheses for every e ∈ Q_n: λ + D ≤ Λ + D ≤ m − M_n and λ ≤ Λ < β(n) ≤ m − M_n. Correct.
- Filtration: atoms x + 2^{V_{min(n,σ)}}; uses M_n < V_n (n ≥ n_s ≥ 4, x even) so that V_n, M_n and "step n fails" are functions of x mod 2^{V_n}. Nesting and the frozen definition are consistent. σ and τ̂ = min(τ, σ) are stopping times (v(x+t) ≤ M_t < V_t is decided on the atom). Correct.
- Martingale: children of slope-≤Λ paths keep their slope; children of slope > Λ paths have slope ≥ Λ+1 because v(π_n') ≥ β(n) ≥ Λ+1. Correct. Integrability: Y_{n_s} need not be integrable over C (2^{V_{n_s}} has infinite mean), but the argument is atom-by-atom with non-negative variables and a bounded stopping time, so optional stopping holds on each atom of F_{n_s}; nothing else is used. Correct.
- *Citation to make precise.* "Ŷ_n is constant on atoms of A_n" cites Lemma 5(a),(b). At a time n = σ (a failing step) the hypothesis λ + D ≤ m − M_n of Lemma 5 is false, so the lemma as stated does not apply; its proof of (a) (first two claims) and (b) uses only M_n < m and λ ≤ m − M_n, which do hold. Suggest stating Lemma 5(a),(b) under these weaker hypotheses, or citing note Lemma 10.5(b). No mathematical gap.
- Survival forces weight, digit split, conditioning on F_{n_s} (m_1 ≤ n_s − s(n_s) ≤ V_{n_s}), and ∫_C 2^{−s_lo} = μ(C)2^{−ℓ_0}(3/4)^{m_1−a}: all correct. The m_1 = 0 variant: correct.

### 1.6 Theorems A and A′ [confirmed]
- Theorem A: Prop. 7's hypothesis n_s − s(n_s) ≥ a is not listed but follows from n_s ≥ n_C ≥ 6 (6 − s(6) = 4 ≥ a). R/ρ_* = 2^{z(n_s)+ℓ_C} with ρ_max = 4, ρ_* = 1/4 for λ = 3. The formula for μ(C ∩ {v(x+i) ≥ b}) and the A_4 tail (term ≤ 2^{λ+1}(i−1)²2^{−i}; ratio (88/87)²/2 = 0.51156 ≤ 0.5116; 1/(1−0.5116) = 2.0475 ≤ 2.05) are correct.
- Theorem A′: K_t = K−1; A_1 ≤ 2^{−K−15}; A_4 ≤ 2.05·8·n_s²2^{−n_s} ≤ 0.9111 K²2^{−K/6}; k−1 ≤ K/4+5, q ≤ (K/4+5)/(K−5) ≤ 0.2561; 1 − H(0.26) = 0.17325. The K > 4·10⁶ argument is correct.

### 1.7 Lemma 8 and the remark [confirmed]
Every valuation in the expansions of c_0, c_1, c_2, c_3 re-derived (using j ≥ 2). π_j = (h−1)h P_{j−2}(h) and the coefficients 1−α_0, α_0−α_1, α_1−α_2 are right. m! ≡ 1,1,2,6,8,8,0,… (mod 16); P_m ≡ (h+1)^{⌈m/2⌉}h^{⌊m/2⌋} (mod 2) gives α_{m,2} odd exactly for m ∈ {2,4,5}. The chain mod 2, 4, 16 is correct and the contradiction is genuine. The remark follows from Lemma 3(i), Lemma 8 and note Lemma 10.3. (The cube identity S_{1,3} = (x+2)³ is consistent: v(S) = 3j < 3j+1, so it is outside the lemma.)

### 1.8 Lemma 9, Corollary 9′, Proposition 10 [confirmed]
- Lemma 9: (a) uses Θ_n ≥ M_n (i = 1 term) and m' ≥ M_n (i ≥ 2 terms); the symmetric inclusion is legitimate because all hypotheses depend only on v(x+i), i ≤ N, which are unchanged. (c): min(m'+Θ_n, 2m') ≥ m+D from (H1), and 2m'−m = m−2M_n ≥ m'−M_N ≥ D from (H2); π_{n+k}(x') ≡ π_{n+k}(x) mod 2^{m+m'−M_N} with m'−M_N ≥ D. The count ⌊(L−1)/2⌋ of levels below V_N is right (only the top level can equal V_N). (d): Lemma 8 gives κ ≤ j; v(π^{[2]}_{n+k}) ≥ m − 2M_N > j keeps v(S_c^{[2]}) = κ; Θ_N ≤ 2m' makes the Taylor congruence mod 2^{2m'} sufficient. Correct.
- Corollary 9′: (H1)–(H4) and m' ≤ n−2 re-derived from (W1)–(W3) and M* ≥ M_N. Correct.
- Proposition 10: atoms x + 2^{V_{n_i}−M_{n_i}} partition C_J ∩ {M_{n_i} ≤ M*} (valuations ≤ M* < β(n_i) ≤ m'); the indicator 1{M_{n_{i+1}} ≤ M*} is constant on atoms (m' > M*); integration atom by atom needs no nesting. μ(C_J) = 2^{−J−1}. Correct.

### 1.9 Theorem B [confirmed]
- Slopes after n_U: a prefix of slope < β(n_U) is inherited (v(π_j') ≥ β(n_U) for j ≥ n_U), so on {U_{n_U} = ∅} every alive path at t ≥ n_U has slope ≤ Λ. Correct.
- G_f depends on x mod 2^Λ and Λ < β(n_s) < V_{n_s}; the five-set decomposition is exhaustive; G_f^c ⊆ ∪_{n_s<i≤n_s+2Λ}{v(x+i) ≥ M_f+1} ⊆ the second B_2 sum. Correct.
- R: on G_f, M̃ ≤ M_f for every λ ≤ Λ, and ρ is monotone in λ. The report uses ⌈(Λ+M_f)/2⌉−1 where Lemma 6(b) gives ⌊(Λ+M_f)/2⌋−1; a larger R is valid, only slightly weaker.

### 1.10 Corollary D and Theorem C [confirmed; label and rounding fixes]
- Every constant of the Theorem C proof re-derived: chain bounds 13.5M−0.5 ≤ n_3 ≤ 13.5M, 20.25M−1.25 ≤ n_U ≤ 20.25M; (W1)–(W3) for M ≥ 22; B_2 ≤ (2M+1)2^{−M} (at most 3.92M+1 indices ≡ 2 mod 16); B_3 exponent −2.125M + 2.04 + 6log₂(20.25M) (report: 2.05); B_4 ≤ 2^{−2M+2log₂(22.25M+1)}; k−1 ≤ 22.75M − 3 + log₂(40.5M) (report uses the weaker −1.5); 1 − H(0.36) = 0.05731; 1 − H(0.04) = 0.7577; Σ_C A_4, Σ_C A_5, A_1 + B_1 ≤ 2^{−K+1}. The K > 4·10⁶ argument is correct (q → 22.75/64 and K/320 − 1 ≫ log₂(K/32+1) + 4).
- The track's `rule.py` majorant differs from the text in two negligible terms (A_4: −2M−7+2log₂(2M+17); A_5 binomial: −0.5(K−5)−2, with a code comment "q ≤ 0.25, H(0.25) < 0.82" that does not justify −0.5; it is justified by q ≤ 0.04). Both are larger than the text's terms, so the program's check implies the text's. My check uses the text's terms and gives the same values (−39.81, −49.16, −56.98, −119.99, −247.00 at K = 3072, 3584, 4096, 8192, 16384, as in the report's table).

## 2. Random tests of the key inequalities (`lemma_tests.py 1`, exact arithmetic mod 2^600, 853 s)

x is a random 2-adic integer: uniform even, near −2 with planted v(x+2) = j ∈ [2,9], or with a planted large v(x+i). Own helpers: Taylor triples (π, π^{[1]}, π^{[2]}), breadth-first alive populations, and ρ computed from the note's definition with exactly 2λ terms.

| test | instances | failures |
|---|---|---|
| Lemma 1(c) V_n−M_n ≥ β(n), 1(b) V_n ≤ n+M_n−2, 2(c) | 66 000 | 0 |
| Lemma 1(a) | 12 000 | 0 |
| Lemma 1(e) walk drop (N_K found by search) | 6000 | 0 |
| Lemma 1(b) truncated | 6000 | 0 |
| Lemma 4 | 3000 populations | 0 |
| Lemma 3 slopes on random x ∈ C_0, C_2, C_6, n up to 44 | 5238 paths | 0 |
| Lemma 3(iv): P_n = ∅ on C_10 (n ≥ 6), C_4 (n ≥ 4) | 466 + 507 | 0 |
| Lemma 6(b) upper bound (λ ≤ 11), mean = 1 | 3000 (bound attained 739×) | 0 |
| Lemma 6(c) lower bound | 1335 | 0 |
| Lemma 8 | 17 019 (6897 with slope > 2j) | 0 |
| Lemma 5 one-step identity (exact Fractions, all w mod 2^{D+λ+1}) | 15 051 parents (12 103 with λ ≥ 3) | 0; control ρ := 1 differs for 3976 |
| Lemma 9 (a),(b),(c) at every w; (d) exact average | 5425 windows, 418 with U_n ≠ ∅, 7 with decay active | 0; max ratio avg/bound = 1.000 |
| Lemma 9 Taylor congruence S_c'(x') ≡ S_c'(x) + 2^{m'+1}wS_c^{[2]}(x) mod 2^{2m'} | 5 597 248 | 0 |
| κ = v(S_c^{[2]}(x)) ≤ j for children of U_n | 5018 | 0 |

## 3. Exact recomputation of the numbers (`bounds_check.py`)

Own evaluator: failure sums exact for the first 6000 terms, then a dyadic-block tail (β(i−1) ≥ i−1−2t−1 on 2^t ≤ i−1 < 2^{t+1}), which differs from the track's ratio tail; exact binomial tails; every hypothesis of Theorems A and B (windows, β(n_s) ≥ Λ+1, n_s−s(n_s) ≥ a, ranges of m_1, K_t, n_s+2^{K_t}+2Λ ≤ T) re-checked with integers.

- **Corollary D table** (`table.log`, 8 s): all 30 rows reproduced from the logged parameters, e.g. K = 37: 0.1005059; K = 40: 0.0910330; K = 448: 0.0455551; K = 1024: 4.935928·10⁻⁶; K = 2048: 6.494454·10⁻¹³; K = 3072: 4.022777·10⁻²⁰. Worst relative difference to the printed table 4.1·10⁻⁴ (rounding). The staircase is non-increasing. The §4 per-class Theorem A entries agree to the printed digits.
- **Theorem A′** (`ruleA.log`): exact log₂ values −161.99, −159.00, −170.91 at K = 1024 (report: −162.0, −159.0, −170.9); also K = 1536, 2048, 4096 as in the track's log. Closed form ≤ 2^{−K/7} on all K ∈ [1024, 4·10⁶], min margin 4.52 bits at K = 1024; integer side conditions hold (`closed_and_ruleC.log`).
- **Theorem C** (`closed_and_ruleC.log`, `ruleC_blocks.log`): the text's nine-term closed form is ≤ 2^{−K/80} on [3072, 4·10⁶] (largest failing K in [2400, 4·10⁶]: 3071; min margin 0.625 bits at K = 3135, so float rounding is irrelevant); the integer side conditions of the rule hold for every K ≤ 30 000 and every 1009th K beyond. The exact bound under R(K) is ≤ 2^{−K/80} for every K ∈ [3072, 3264] and at K = 64M+63 for M = 48..400 (the worst K of each block, since only −K/80 and the B_5 binomial move inside a block): 357 values, worst margin 2.25 bits at K = 3135. Exact values at K = 3072, 3584, 4096, 8192, 16384: 2^{−41.443}, 2^{−49.224}, 2^{−57.027}, 2^{−120.028}, 2^{−247.030}, as in the report.

## 4. Fixes requested

- **F1 (must fix; rounding direction).** Upper bounds must be rounded up. As stated, the following are slightly false:
  - headline, §7 parenthetical, §8 and "In plain words": "δ_G(2) ≤ 0.1005 for G ≥ 2^37" (exact bound 0.1005059) → "≤ 0.10051";
  - headline and §8: "≤ 0.0910 for G ≥ 2^40", "at most 0.091" (0.0910330) → "≤ 0.09104";
  - headline, §6, §7, §8: "≤ 4.9·10⁻⁶ for G ≥ 2^1024" (4.935928·10⁻⁶) → "≤ 4.94·10⁻⁶";
  - headline (Theorem A′ bullet): "≤ 0.0285 in total at G = 2^40" (0.0285330) → "≤ 0.02854".
  The tables round to nearest (e.g. 0.1352 for 0.1352409, 8.04e-3 for 8.0414e-3); either round every entry up or say "rounded to nearest; exact values in `verify.log`". None of this changes any conclusion: 0.10051 still beats the census value 0.101636.
- **F2 (must fix; labels).** The §4 heading of Theorem A′ and the §7 headings of Corollary D and Theorem C say "[proved, given Lemma 3]". Theorem A′ and Theorem C rest on a computer check of a closed-form inequality over K ∈ [1024, 4·10⁶] (resp. [3072, 4·10⁶]) and Corollary D's numbers are computed; use [computer-assisted], as the headline and §0 already do. For the same reason, §8 "In plain words" should not call the rate "fully proved"; say "computer-assisted (an exhaustive 2^16-case certificate and a closed-form check)". (The checks are float evaluations; state the margins, ≥ 4.5 and ≥ 0.62 bits, so that rounding is visibly irrelevant.)
- **F3 (should fix; label).** §11 "[obstruction for this method] Large slopes": the 2^{−λ/2} decay of the slope tail is a numerical observation; relabel [heuristic].
- **F4 (minor).** Prop. 7 cites Lemma 5(a),(b) at failing times, where Lemma 5's D-hypothesis fails; state Lemma 5(a) (first two claims) and (b) under M_n < m and λ ≤ m − M_n only (§1.5).
- **F5 (minor).** Theorem A should list Prop. 7's hypothesis n_s − s(n_s) ≥ a (implied by n_s ≥ n_C); Theorem B could use ⌊(Λ+M_f)/2⌋ (§1.9).
- **F6 (minor).** "The census is better for every G < 2^37": the evaluation was at G = 2^K with a heuristic parameter search; say "for every evaluated G = 2^K, K ≤ 36". Also, "In plain words" says the bounds go below the census value "from G = 2^40 on"; elsewhere (correctly) from 2^37.
- **F7 (minor, code).** `rule.py` comment for the A_5 binomial term ("q ≤ 0.25, H(0.25) < 0.82") does not justify the exponent −0.5(K−5); the justification is q ≤ 0.04, which `rule_K0.py` checks.

## 5. Credits and wording
Kitamura (normal form, critical-branching picture, ≈ 11.5/G, cube identity), track R1b (martingale weights, Theorem 10.1), track R1a (Claim 10.9, correctly called unverified), R3N (c/G survey: 8–12 over even a, i.e. 4–6 over all a, as stated), the earlier R3Q instance (map of lemmas; its logged 0.086 at K = 1024 confirmed in `earlier_instance/thmC_scan.log`), Smith–Wilkinson, Athreya–Karlin, Afanasyev–Geiger–Kersting–Vatutin: all as in the note. The numbers quoted from the note (Monte Carlo 0.0644, 0.0379, 0.0208; δ_32(2) = 0.101636; Claim 10.9's 0.662G^{−0.2075}) match note §4.7, §5 and §10.1.4. No gendered pronouns or model names found in the report.

## 6. Reproduction

```sh
cd code/round3/check_R3Q
nice -n 10 python3 -I cert3.py                       # Lemma 3, < 1 s
nice -n 10 python3 -I lemma_tests.py 1               # random tests, about 14 min
nice -n 10 python3 -I bounds_check.py table          # Corollary D / Theorem A tables, 8 s
nice -n 10 python3 -I bounds_check.py ruleA 1024 1536 2048 4096
nice -n 10 python3 -I bounds_check.py closed 4000000 # closed forms of Theorems A', C, 19 s
nice -n 10 python3 -I bounds_check.py ruleC 3072 3264 1
sh run_ruleC_blocks.sh                               # 75 s
```
