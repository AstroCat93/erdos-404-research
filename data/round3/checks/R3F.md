# Adversarial check of track R3F (round 3, 2026-10-13): Fourier and equidistribution steps toward Q3

Checker: check_R3F. Code: `code/round3/check_R3F/`. Logs: `data/round3/check_R3F/`. Binaries, tables and scratch: `/tmp/r3_check_R3F/`.
Track material read (read-only): `data/round3/reports/R3F.md`, `code/round3/R3F/`, `data/round3/R3F/`, and note.md §§3.5–3.7, 10.2–10.6 for the cited statements.
CPU used: about 40 core-minutes. All jobs ran under `nice -n 10`, one after another. One incident: the first run of `jcheck.py` (C = 10⁴) used OpenBLAS's default threading and ran at about 2 cores for about 10 minutes, roughly 20 core-minutes. It was killed and re-run single-threaded in 15 s; the wrapper now exports `OPENBLAS_NUM_THREADS=1`. No process this check did not start was touched.

**Bottom line.** Every [proved] item was checked line by line and holds. Every number re-computed here agrees with the report. I recomputed numbers with my own programs, and they share no code with R3F. One proof needs no repair. The main computational gap in the report is the following. Theorem A5 at p = 13, level d = 9 rested on a single program (`gate_d`). Only 2 of the 6 `ivshell` chunks exist, and the report still says `TBD_P13D9`. This check supplies an independent second computation of that shell, so the certified value sup_d ρ_d ≤ 1.2064 at p = 13 now has two programs at every computed level.

The required fixes are as follows:
- two unfilled placeholders (`TBD_P13D9`, `TBD_REPRO_TABLE`);
- one numerical value stated as a value although it is an upper bound (Λ'_7);
- several wording overstatements in heuristic observations (B2, B3, D3).

Nothing in R3F settles Q1 or Q3, and the report says so correctly.

## 0. Verdicts

| id (as in the track report) | claim | verdict |
|---|---|---|
| Fact F1 | Fourier inversion, Parseval = collision count, missed fraction ≤ Σ Q_d | **confirmed** (proof checked) |
| Fact F2 | S_d ≤ √(N_d Q_d) | **confirmed** |
| Lemma A1 | gate-block shells depend only on (p,d) for d ≤ j+1 | **confirmed** (proof checked; congruence y_i ≡ σ_i mod p^{j+1} verified as an integer identity for 31 actual gate blocks: p = 5, 7 with j = 1, 2 and p = 13 with j = 1) |
| Theorem A2 | exact L² shells; only relation ±(e_{p−2}+e_{p−1}); ratio exactly 3/2 when p^{d−1} > R_p = ⌊e(p−1)!⌋ | **confirmed** (proof checked; exhaustive enumeration of {−1,0,1}^p for p = 3, 5, 7, 11, 13 with exact rationals; brute-force cos² sums agree; independently, the frequency-side L² shell at p = 13, d = 9 encloses (3/2)N_9 2^{−13} = 1 792 377.07251) |
| Corollary A3 | uniform L¹ bound; C^CS_p = 2.0705, 2.5543, 4.5460, 5.2089 | **confirmed** (all four constants reproduced exactly) |
| Theorem A4 | Poisson/carry formula, ρ_d → J_p, error ≤ (π²α_{p−1}/3)(p^{−d}+p^{−d+1})/N_d | **confirmed** (every step checked, including the partial-fraction value of κ_m and the (1+1/η, 1+η) splitting; κ_m class-0 maximality checked by direct summation; α_{p−1}/((p−1)!)² ≤ 5.6106, 11.858, 31.803, 45.614, 81.127 reproduced in interval arithmetic; the Poisson identity A(M) = (2/π)^p Σ_j Ψ_p(jM) checked numerically) |
| Theorem A5 | certified sup_d ρ_d ≤ 1.320222, 1.175992, 1.837654, 1.206366 (p = 5, 7, 11, 13) | **confirmed-with-fixes**. A third program independently reproduces every computed level (p = 5: d ≤ 10; 7: d ≤ 9; 11: d ≤ 9; 13: d ≤ 9) and the analytic tails. My bounds: 1.3202205, 1.1759905, 1.8376527, 1.2063652. Fix: `TBD_P13D9` is unfilled, and in R3F's own material the level p = 13, d = 9 rests on `gate_d` alone (only 2/6 `ivshell` chunks were run); cite this check's computation (§2) or finish the chunks |
| Rigorous J_p (`jrel.c`) | J_p enclosures, p = 3…23 | **confirmed**: an independent implementation of the truncated carry recursion, with its own error derivation, gives enclosures inside or overlapping jrel's for all eight primes. For p = 5, 7, 11 it is also checked by a different method (the grid identity with the A4(iii) envelope), which gives J_5 to 10⁻¹⁰, J_7 to 2·10⁻⁸ and J_11 to 3·10⁻⁴ |
| Proposition A6 | J_p converges; \|J_{p'} − J_p\| ≤ 2.266/(p−1) | **confirmed** (proof checked; ∏_{m≥2} κ_m ∈ [1.67422, 1.67430], β^abs_∞ ≤ 2.06559, (π²/9)β^abs_∞ ≤ 2.26517) |
| A7 | what (a) does and does not imply | **confirmed-with-fixes** (correct; one loose phrase: "RMF restricted to windows of length H = p", see §3.1) |
| Proposition B1 | L2 = collision count; positive Haar measure from finite L² mass | **confirmed** (proof checked) |
| B2 | budgets Λ_p, Λ'_p, Λ2_p; Λ'_p < 1 exactly for p ≥ 11 | **confirmed-with-fixes**. All constants are reproduced, but Λ'_7 = 2.04957, not 2.0509: 2.0509 is the D = 60 partial sum plus the geometric tail bound, i.e. an upper bound. Also reword "fullness only for p ≥ 7" (§3.2) |
| B3 | exact small-level L² shells (table) | **confirmed-with-fixes**. Every tabulated value is reproduced by a different exact method (int64 DP with limb-split squares, no CRT), and for N₀ = 0 and p = 11, 13 also from the frequency side. Two observations are worded too strongly: "grows only at gate levels" and "shrinking jumps" (§3.3) |
| Proposition B4 | levels d ≤ t−1 of every RMF window equal the factorial-measure shells | **confirmed** (proof checked) |
| B4-data | certified T_fact(d); totals 0.286, 0.0668, 0.00830; coverage of all classes mod 7⁹, 11⁷, 13⁷ | **confirmed**. The shells were recomputed independently: totals ≤ 0.286433, 0.0667911, 0.00830168, with the same per-level ratios. The by-product was checked directly by subset-sum DP: 0 missing residues mod 7⁹, 11⁷ and 13⁷ |
| Corollary B4' | RMF(p,C) with CΛ_p < 1 forces full support of ν_fact | **confirmed** |
| Theorem B5 | collision-count version of Thm 10.16 (conditional); C < 11.7 (p = 11), C < 41.7 (p = 13) | **confirmed** (proof checked, including n_d = U_d for d ≤ c_t, c_{t+1} − c_t = p^{t−1} − 1, and the τ' ratio; thresholds 11.732 and 41.720 reproduced; the hypothesis is unproved, as labelled) |
| Proposition B6 | L² barrier lemma | **confirmed** (proof checked; the "any bound derived only from …" sentence is a meta-statement of the same kind as Theorem 3.10's consequence; it applies to the RMF windows, which are block-aligned runs ending at a level-(t−1) gate) |
| Proposition B7 | exact L² renormalisation; sup H^(2) = H^(2)(0) ≥ 1 | **confirmed** (proof checked; the identity (i) verified to relative 10⁻²⁵ at p = 5, 7, W = 1, k = 2, 3; sup over a 20 000-point grid equals H^(2)(0) = 1 + L²(bottom)) |
| B8 | exact gate identity; requirement = reformulation | **confirmed** (identity derived independently, and checked exactly on the first level-1 gate of the tail from p, p = 5, 7; the "requirement" part is a reformulation, as labelled) |
| C1 | linearisation mod p^{t+c} | **confirmed** (proof checked; verified for every class in 20 (p,t,H) cases) |
| C2 | K'-averaged L² = 2D collision counts | **confirmed** (proof checked; identity verified exactly, all s = 0..c, in 16 cases (14 with c ≥ 1) including p = 11, 13, where R3F had checked only p = 7) |
| C3 | proportion of non-covering classes ≤ Σ_d √(N_d E Q_d) | **confirmed** |
| C4 | table of exact failing counts, C3 bounds, C–S certificates | **confirmed** (20 of the 23 rows re-computed with my own code; every entry agrees; not re-run: (7,3,28), (13,4,32), (13,4,39)) |
| C5 | averaging cannot by itself feed Prop 10.10 / Thm 10.16 | **confirmed** (correctly labelled [negative]; the sizing "H ≳ 2M log₂ p" is a random-model heuristic, as the text implies) |
| D1 | Poisson decomposition; continuous transfer = j = 0 term | **confirmed** (identity proved as in A4; the transfer-operator identification checked: (L_m g)^(k) = ĝ(mk)) |
| D2 | the whole deviation from the random model is aliasing (illustration) | **confirmed** as an illustration: Ψ(0) re-computed with my own carry transfer (p = 13: [0.99991, 1.00013]; p = 11: [0.99978, 1.00005]), and the certified factors 0.06–4.2 reproduced from my own shells. It stays floating point, as labelled |
| D3 | Σ_k √(N_k Q(k)) ≤ 0.0252427 (p = 13), ≤ 0.143641 (p = 11) | **confirmed-with-fixes** (sums reproduced from independent L² bounds: 0.025242693 and 0.14364067; the phrase "in line with (π/(2√2))^{n_k}" overstates: the observed loss at k = 7 is 626, the random-model loss is 1.11^{91} ≈ 1.4·10⁴) |
| D4 | positive-definite majorants lose ≥ 16/15 per element; best constant in [0.6791, 0.7072] | **confirmed** (proof checked; budgets 0.800082 (p = 7), 0.167695 (p = 11), divergence at p = 5 (r = 1.063) reproduced) |
| (e) | Σ_{k≤7} T_13(k) ∈ [9.29878581106e-3, 9.29878581108e-3]; Σ_{k≤8} T_11(k) ∈ [6.68544967910e-2, 6.68544967911e-2] | **confirmed** [computer-assisted]: all 15 shells were recomputed by a third, independent implementation. My enclosures are [9.2987858110636e-3, 9.2987858110729e-3] and [6.6854496791039e-2, 6.6854496791104e-2], both inside the claimed ones. R3F's `ivshell` and `jrel` were also rebuilt and reproduce their logs digit for digit |
| Failed attempts 1–4 | as stated | **confirmed** (labels correct; minor: `gate_d` at p = 13, d = 9 took about 20 min, not "about 11 minutes"; its log shows 1409 s for d ≤ 9, of which d = 9 is about 12/13) |
| Headline / Q3 statements | "Nothing here settles Q1 or Q3" | **confirmed-with-fixes** (correct; the placeholders must be filled before integration) |
| Reproduction | commands and logs | **confirmed-with-fixes**: the placeholder `TBD_REPRO_TABLE` is unfilled |

## 1. Method of this check

All code is new and shares no code with `code/round3/R3F/`.

**Shells (A5, B4-data, (e), D3): `shellchk.c` + `gen_tables.py` + `shells.py`.**
- *Cosine evaluation.* cos(πr/M) is evaluated by the addition formula from four tables (cos and sin of πhB/M and of πl/M, with B = 2¹⁷). The tables are generated with arb ball arithmetic (python-flint `cos_pi_fmpq`/`sin_pi_fmpq` at 128 bits) and rounded to the nearest double. The generator certifies e_t = max |table − true| and an absolute per-factor bound eps = 10⁻¹⁵ ≥ 4e_t + 2.0001u + u(1+eps) (u = 2⁻⁵³). Each factor is replaced by min(1, |c̃|+eps) for the upper bound and max(0, |c̃|−eps) for the lower bound.
- *Arithmetic.* Round-to-nearest, `-ffp-contract=off`. The final sums are multiplied by explicit γ-type factors: (1−u)^{−(2n−1)} for the products, γ_{4095} for the block sums, n_blocks·2⁻⁶⁴ for the long-double accumulation, and 10⁻¹⁹ for the decimal print.
- *Enumeration.* u runs incrementally over 1..(M−1)/2, and non-units are skipped.

This differs from R3F's three methods: `ivshell` (Taylor enclosures in FE_UPWARD), `gate_d` (Taylor in FE_UPWARD, incremental residues) and `shells_mpfr.py` (MPFR table plus a numpy a-posteriori factor).

*Validation* (`validate_shellchk_brute.log`). Brute force in mpmath (40 digits) on 9 small cases (gate p = 5, d ≤ 3 and p = 7, d = 3; tails from 5, 11, 13; factorial measure p = 7 and 13, d = 2). All 9 brute values lie inside the enclosures.

**J_p and A4 constants: `jcheck.py`.**
- *Constants.* α_m, β_m, κ_m in mpmath interval arithmetic; κ_m also by direct summation.
- *Truncated forward carry recursion.* Dense float64 with single-threaded BLAS. The error bound was derived here: for each step m, β_{m−1}·‖ṽ_m‖₁·(2/(3m(m−1)C)) for the mass dropped outside |s'| ≤ C, plus β_{m−1}κ_m‖ṽ_m‖₁(γ_{2C+1}+2u) for rounding.
- *Overlap with `jrel.c`.* The same mathematical series is summed, but the code, the arithmetic and the bookkeeping are independent. The grid identity in `summ.py` gives a genuinely different second method for p = 5, 7, 11:

  J_p = (π/2)^p(1 + Σ_{d≤D} S_d)/p^D − E'(p^D), with |E'(p^D)| ≤ (π²/3)α_{p−1}/p^{2D}.

**Exact checks.**
- `a2check.py`: A1 and A2.
- `kavgcheck.py`: C1–C4, with per-class int64 DP and a joint (A, B) lazy walk for C2.
- `b3check.py`: B3, exact counts with limb-split squares.
- `covercheck.py`: direct subset-sum coverage.
- `identcheck.py`: A4(i), B7, B8.
- `budgetcheck.py`: B2, D4 and the B5 thresholds.
- `dcheck.py`: D2.

## 2. Theorem A5: the certified suprema, including the gap at p = 13, d = 9

Per-level certified upper bounds of ρ_d = S_d/(N_d(2/π)^p) (`summary.log`):

| p | ρ_1 | ρ_2 | ρ_3 | ρ_4 | ρ_5 | ρ_6 | ρ_7 | ρ_8 | ρ_9 | ρ_10 |
|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 0.668243 | **1.320221** | 1.069891 | 1.167283 | 1.167007 | 1.166976 | 1.166975 | 1.166975 | 1.166975 | 1.166975 |
| 7 | 0.798824 | 0.627502 | 1.173215 | **1.175991** | 1.169807 | 1.170438 | 1.170443 | 1.170443 | 1.170443 | |
| 11 | 0.867229 | **1.837653** | 1.068908 | 1.172620 | 1.171714 | 1.172171 | 1.172558 | 1.172524 | 1.172524 | |
| 13 | 0.230253 | 1.127194 | 1.015621 | **1.206365** | 1.170272 | 1.172852 | 1.172957 | 1.172950 | 1.172950 | |

*p = 13, d = 9.* S_9 ∈ [32 392 835.6659466, 32 392 835.6659821] (`a_gate_p13_d9.log`, 362 s, six chunks).
- R3F's `gate_d` gives S_9 ≤ 3.239283592·10⁷, consistent.
- The two `ivshell` chunks that exist (lowest digit u₀ = 1, 2) sum to [10 797 611.82, 10 797 612.55]. This is consistent with one third of S_9, but is not a check of the total.
- The L² enclosure from the same run, [1 792 377.072509, 1 792 377.072511], contains the exact value (3/2)N_9 2^{−13} of Theorem A2. This is a strong internal test of the program at this modulus (M ≈ 1.06·10¹⁰).

*Analytic tails* (Theorem A4(iii), α from my interval code):

| p | J_p enclosure used | tail bound | sup_d ρ_d (this check) | R3F |
|---|---|---|---|---|
| 5 | grid: 1.16697534 ± 1.1·10⁻¹⁰ | d ≥ 11: ≤ 1.1669753 | **≤ 1.3202205** (d = 2) | 1.320222 |
| 7 | grid: [1.170442982, 1.170443007] | d ≥ 10: ≤ 1.1704430 | **≤ 1.1759905** (d = 4) | 1.175992 |
| 11 | carry: [1.172434207, 1.172613790] | d ≥ 10: ≤ 1.1726408 | **≤ 1.8376527** (d = 2) | 1.837654 |
| 13 | carry: [1.172857510, 1.173041444] | d ≥ 10: ≤ 1.2005188 | **≤ 1.2063652** (d = 4) | 1.206366 |

So at every prime the certified supremum is reproduced by an independent program, at every level that is computed, together with an independent J_p enclosure.

At p = 13 the tail d ≥ 10 needs J_13^+. Here two independent codes are available (`jrel.c` and `jcheck.py`), but only one method, the truncated carry recursion. The grid identity is useless at p = 13 for D ≤ 9, since |E'(13⁹)| ≤ 0.31. This is adequate (J_13^+ ≤ 1.1789 would suffice; both codes give ≤ 1.17305), but it is worth saying in the report.

## 3. Wording and value fixes (none affects a proved statement)

### 3.1 A7, item "Proved"

"This is RMF restricted to windows of length H = p."
- RMF (Theorem 10.16) is defined only for H = p^{t−1} at depth t, and its right-hand side is a total, not a per-level, bound.
- What (a) proves is an RMF-type **per-level** random-model bound for single length-p windows (gate blocks) at **every** depth t = j+1. It does so with the constants of A5.
- Suggested wording: "This is an RMF-type per-level bound for single gate blocks (windows of length p) at every depth."

### 3.2 B2

*Value.* "Λ'_7 = 2.0509 (computed, with a rigorous geometric tail bound)". The value is Λ'_7 = 2.049567. The quoted number is the upper end of the enclosure [2.04957, 2.0509] obtained with D = 60, where the tail bound is 0.0013. `budgetcheck.py` uses D = 400, and the width is then below 10⁻²⁰. The conclusion Λ'_7 > 1 is unaffected. The same remark applies in a negligible way to the other B2 entries, which are upper ends: for example Λ'_11 = 0.291932 against the printed 0.2920.

*Wording.* "So in the random model, positive Haar measure of the tails is expected at every odd p, but fullness only for p ≥ 7." This is too strong.
- Λ_5 > 1 only means that the L¹ Fourier criterion cannot certify fullness at p = 5, even under the random model.
- It does not make non-fullness "expected" at p = 5. The note leaves UC(5) open: Conjecture 5.3 says "possibly p ≥ 5".
- Suggested wording: "…but the L¹ criterion can certify fullness only for p ≥ 7."

### 3.3 B3 observations and the headline (b)

*"Grows only at gate levels."* The L² mass grows at every level.
- At p = 3 from 3, the non-gate-owned levels contribute about 0.047 of L2(15) = 0.3312: k = 1 gives 0.031, k = 4 gives 0.0056, k = 5 gives 0.0036, and so on.
- The gate-owned levels k = 3, 7, 11, 12 contribute about 0.284.
- "Mainly at gate-owned levels" is accurate.

*"Shrinking jumps."* The gate jumps are 0.2329, 0.0289, 0.01089 and 0.01142 at k = 3, 7, 11, 12. The last is not smaller than the one before. Both observations are labelled heuristic, so this is a wording fix.

*Open issues, "positive measure and non-fullness would coexist".* This silently uses the following step:
- λ(E_3) > 0 implies λ(E_N) > 0 for every N, because E_3 is a finite union of translates of E_N.
- Theorem 3.11 concerns E_N with 81 | N, not E_3.

Worth one sentence.

### 3.4 D3

"The per-level loss grows with the level … in line with (π/(2√2))^{n_k}." The observed losses (2.1 at k = 1, 626 at k = 7) grow, but stay well below the random-model value (π/(2√2))^{n_k}: that is 3.9 at n = 13 and about 1.4·10⁴ at n = 91. Say "grows roughly geometrically in n_k (but stays below the random-model factor (π/(2√2))^{n_k})".

### 3.5 Placeholders

`TBD_P13D9` (§A5, twice) and `TBD_REPRO_TABLE` (Reproduction) must be filled before anything is integrated into the note.
- For the first, the honest statement from R3F's own logs is: "`ivshell` chunks u₀ = 1, 2 of 6 only (incomplete); the level is covered by `gate_d` and, independently, by check_R3F's `shellchk`."
- Alternatively, finish the 4 remaining `ivshell` chunks, at about 13 min each.

## 4. Proof review notes

Each item below was checked line by line. Only points where something needed care are listed.
- **A2(ii).** The downward induction is correct: u | u!/w! for w < u, so δ'_u P_u ≡ 0 (mod uP_u), hence u | δ'_u and δ'_u = 0 for u ≥ 2. The final step δ'_1 = −δ'_0 uses P_1 = P_0 and the sign convention, and gives δ_{p−2} = δ_{p−1}. The weight of the relation is 2·2^{p−2}/4^p = 2^{−p}/2. The identity R_p = ⌊e(p−1)!⌋ is classical, since 0 < Σ_{w≥p}(p−1)!/w! < 1.
- **A4(iii).**
  - *Class-0 sum.* With z = 1/(2m), Σ_{i≥1} 1/(4m²i²−1) = (1−πz cot πz)/2, so the class-0 sum is 2 − (π/(2m))cot(π/(2m)) as claimed. Every other residue class sums to at most 1, which was checked numerically to be below the class-0 value.
  - *Envelope.* The envelope recursion uses |b_k|k² ≤ 1/3 (equality at |k| = 1), Σ_{s'≠0}s'^{−2} = π²/3, and the optimal η = (π/3)/(m√κ_m). These give (π/3 + m√κ_m)².
  - *Start and decrease.* G_1 is supported on {−1,0,1}, so α_1 = π²/16. The bound on |ρ_d − J_p| is decreasing in d, which justifies the gluing in A5.
- **A6.** The completion of a relation with top index U is Σ over relations of (U−1)!/w!-weights equal to s'. Bounding it by G^abs_{U−1}(s') ≤ (π²/8)∏κ is valid, because (|b|∗|b|)(s) ≤ Σb² = π²/8 by Cauchy–Schwarz, and Σ_k b_k² = 1 + (π²−8)/8 = π²/8. Also |b_{Us'}| ≤ 1/(3U²s'²) and Σ_{U≥p} U^{−2} ≤ 1/(p−1).
- **B1(iii).** Plancherel on ℤ_p and uniqueness of Fourier–Stieltjes transforms give ν = f dλ. λ(supp ν) = inf_K |supp ν_K|/p^K because supp ν is closed, and the projection of supp ν mod p^K is supp ν_K by compactness.
- **B5.** All three ingredients check:
  - n_d = U_d for d ≤ c_t, since U_d ≤ p^{t−1} − 1 when d ≤ v_p((p^{t−1}−1)!);
  - n_d = p^{t−1} for c_t < d ≤ t + c_t;
  - c_{t+1} − c_t = p^{t−1} − 1, so τ'_p(t+1)/τ'_p(t) = (p·2^{−(p−1)/2})^{p^{t−1}}.

  (H1)–(H3) then give Cov(p,t,p^{t−1}) for all t ≥ 3 by Fact F1, with p^{t−1} + 1 < p^t, and Theorem 3.12(c) applies. τ'_11(3) = 2.1·10⁻⁵ and τ'_13(3) = 1.9·10⁻⁹ are negligible in the C thresholds.
- **B6.**
  - *Support bound.* X ≤ p(p^c−1)(p^{w_max+1}−1)/(p−1) < p^a/(p−1), with a = w_max + c + 2. So the support has at most 2p^a/(p−1) points. Reduction mod p^D only merges atoms, so Σν² ≥ (p−1)/(2p^a), and D − a = j − c − 1.
  - *Tail from p.* For M₀ = 1 the block after a level-j gate starts at level w_max + j + 1 = D, so the elements of level < D are exactly W.
  - *RMF windows.* These windows are block-aligned runs ending at a level-(t−1) gate, with w_max = c_t and demand t + c_t = w_max + j + 1. So B6 applies to them, which supports the remark under Theorem B5.
- **B8.** The identity follows from independence of the gate coins, from E e(ξD_Γ) = ∏cos²(πξσ_r) = F_p(ξ)², and from the gate block being p^e·U·(σ_r mod p^{j+1}) with one common unit U. That last fact is A1 together with the common factor (pm)!/p^{level}. The exact check (§0) confirms it.
- **C2.** For d = t+s, the count of K' mod p^c with A + p^tK'B ≡ 0 (mod p^{t+s}) is p^{c−s+v_s}·1(p^{t+v_s} | A), with v_s = min(v_p(B), s). This reproduces the stated formula. The Fourier form E_{K'} e(uK'B/p^s) = 1(p^s | B) for unit u is correct.
- **D4(ii).** mean(g·(1−cos4x)) = A₀ − A₂/2 ≤ A₀, and mean(|cos x|(1−cos4x)) = 2/π + 2/(15π). The tangent-line majorant 2^{−1/2}(1 + cos2x/2) ≥ |cos x| follows from AM–GM.

## 5. What R3F does and does not imply for Q3

Checked against Theorem 3.10 (barrier lemma), Corollary 10.20 (sup-type renormalisation), Theorems 10.16 and 10.18, and §10.6.
- **(a)** uses only the fixed residues σ_i, i.e. shallow digits. So by Theorem 3.10 it cannot be part of an argument that crosses deep gates, and it claims nothing of the kind (A7.4). Its Σ_{d≤j+1} S_d grows like J_p p^{j+1}(2/π)^p, consistent with Theorem 3.9(c).
- **B5** is a conditional reduction with the same logical status as Theorem 10.16. It is labelled "[proved; the hypothesis is unproved]". This is correct.
- **B6** is a quantitative L² strengthening of Theorem 3.10. The truncated model has large L² mass, not merely a missed class. It applies to the RMF windows themselves, so (H2) cannot be proved from boundedly many unit digits.
- **B7** is the exact L² analogue of Proposition 10.19 and Corollary 10.20, with the supremum attained at θ = 0 (checked numerically).
- **D1/D2.** D1 sharpens Corollary 10.20 in the stated sense. Supported by D2's floating-point data, it shows that the j = 0 (continuous) term equals the random model to about 2·10⁻⁴, so any MI-13-type statement is a statement about aliasing sums. This is a correct reading of an exact identity plus an uncertified illustration, and it is labelled as such.
- **B4/B4'** show that RMF already contains a fullness statement for ν_fact. The report correctly calls this "a structural remark, not a reduction".
- Nothing in R3F is claimed as progress on Q3 beyond reductions and obstructions. The headline sentence "Nothing here settles Q1 or Q3. No new unconditional statement about any f(a,p) is claimed" is accurate.
- The one unconditional new fact about factorial sums (every class mod 7⁹, 11⁷, 13⁷ is a finite sum of distinct factorials 0!, 1!, …) is confirmed here by a direct DP. It says nothing about f(a,p).

## 6. Reproduction

Build (outputs in `/tmp/r3_check_R3F/bin/`):

```
gcc -O2 -ffp-contract=off -fno-fast-math -o /tmp/r3_check_R3F/bin/shellchk code/round3/check_R3F/shellchk.c -lm
```

Every log starts with its command line and ends with its wall time. All jobs ran under `code/round3/check_R3F/run_logged.sh` (`nice -n 10`, single-threaded BLAS). The batches are `batch1.sh` (shells), `batch2.sh` (exact checks) and `batch3.sh` (B3, after a fix of an int64 overflow in the first version of `b3check.sumsq`; the faulty p = 11 output was discarded and every B3 log re-run).

| log (`data/round3/check_R3F/`) | command (in `code/round3/check_R3F/`) | wall |
|---|---|---|
| `e_tail_p13_k1-7.log` | `shells.py tail 13 13 k`, k = 1..7 | 23 s |
| `e_tail_p11_k1-8.log` | `shells.py tail 11 11 k`, k = 1..8 | 76 s |
| `a_gate_p5_d1-10.log`, `a_gate_p7_d1-9.log` | `shells.py gate 5 d` / `gate 7 d` | 5 s, 5 s |
| `a_gate_p11_d1-9.log` | `shells.py gate 11 d`, d = 1..9 | 63 s |
| `a_gate_p13_d1-8.log` | `shells.py gate 13 d`, d = 1..8 | 26 s |
| `a_gate_p13_d9.log` | `shells.py gate 13 9 --chunks 6` | 362 s |
| `b4_fact_p{7,11,13}_d*.log` | `shells.py fact p d` | 10 s, 8 s, 22 s |
| `a_jcheck_C10000.log` | `jcheck.py 10000 5 7 11 13` | 15 s |
| `a_jcheck_C10000_p3_17_19_23.log` | `jcheck.py 10000 3 17 19 23` | 25 s |
| `summary.log` | `summ.py data/round3/check_R3F` | <1 s |
| `a1_a2_a3_exact.log` | `a2check.py` | <1 s |
| `ident_poisson_b7_b8.log` | `identcheck.py` | 22 s |
| `b2_budgets.log` | `budgetcheck.py` | <1 s |
| `b4_cover_direct.log` | `covercheck.py 7 9 11 7 13 7` | 3 s |
| `c4_kavg.log` | `kavgcheck.py` with 20 (p,t,H) triples (see log) | 80 s |
| `b3_l2_p*_N*.log` | `b3check.py p N0 K` (7 cases) | 9 s total |
| `d2_psi0.log` | `dcheck.py 13 7 {100,300}`, `dcheck.py 11 8 300` | 8 s |
| `validate_shellchk_brute.log` | `shells.py … --brute` on 9 small cases | 3 s |
| `rerun_r3f_programs.log` | R3F's own `ivshell fact 13 13 6`, `jrel 13 10000`, `gate_d 7 d` (rebuilt from `code/round3/R3F/` into `/tmp/r3_check_R3F/r3f_bin/`); output identical to R3F's logs | 19 s |

Software: gcc 13.3, Python 3.13 with numpy 2.5.3, mpmath 1.3.0, python-flint 0.9.0 (arb).

## 7. Credit

The objects checked here come from the R3F track report and from note.md. Those are:
- the round-1 covering framework and gate congruence;
- round-2 Theorems 10.16 and 10.18, Proposition 10.19, Corollary 10.20 and Proposition 10.21 (tracks R2a, R2b);
- the period mean and the factorial-digit recursion (the round-2 computational referee and lead);
- Tao's block lemma and programme;
- K. Kitamura's normal form;
- the problem itself, due to Erdős and Graham.

Classical tools used in this check: Poisson summation, Parseval/Plancherel, Cauchy–Schwarz, Higham's γ_n bounds, and arb ball arithmetic (python-flint) for the certified tables. Nothing here was checked by a human.
