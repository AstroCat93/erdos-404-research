# Adversarial check of track R3N (round 3, 2026-10-13): Kitamura's test case a = 594 at p = 2

Checker: check_R3N. Code: `code/round3/check_R3N/`. Logs: `data/round3/check_R3N/`. Binaries and scratch: `/tmp/r3_check_R3N/`.
Track material read (read-only): `data/round3/reports/R3N.md`, `code/round3/R3N/`, `data/round3/R3N/`.
CPU used: about 87 core-minutes on one core (all jobs `nice -n 10`, strictly sequential). The track's dfsW4 job (PID 515) was not touched; it finished on its own during this check (see §6).

## 0. Verdicts

| id (as in the track report) | claim | verdict |
|---|---|---|
| Lemma 1 | stages: aliveness facts, death stage even, v(Σ_A) = v(S_{N_d}) | **confirmed** (checked line by line) |
| Lemma 2 | decision and exact value via death/final candidates | **confirmed** (checked line by line) |
| Lemma 3 + correctness of C | 256-bit window lemma; dfsW.c enumerates every alive prefix | **confirmed** (lemma and code read line by line) |
| Lemma 4 + correctness of B | 128-bit shifted window lemma; dfsB.c enumerates every alive prefix | **confirmed-with-fixes** (an unstated hypothesis n < 2^19; see §1.4) |
| Lemma 5 | steps_B = 3 + (3/2)·nodes_C | **confirmed** (proof checked; identity reproduced; extended by a third program) |
| Theorem R3N.1 | f(594,2) = 90394 | **confirmed** [computer-assisted]: B and C rebuilt and re-run with identical output; a third, independently written exhaustive program (D, this check) gives the same EXACT value and the same tree size; all 594 witnesses re-verified by an own two-method verifier |
| Corollary R3N.2 | f(a,2) = v_2(a!) + 89804 on a ≡ 594 (mod 2^89804); K_2 ∩ (594 + 2^89804 ℤ_2) = ∅ | **confirmed-with-fixes** (the ℤ_2 form needs Theorem 3.1(a) as well, not only Cor. 3.7.1(i); §1.6) |
| Proposition R3N.3 | f(17662,2) ≥ 148725 | **confirmed** (own verifier). Also confirmed: the later shipped witness f(17662,2) ≥ 212995, and two unshipped witnesses 217088, 221186 (files only in `/tmp/r3_R3N`). The report text still contains the unfilled placeholders `STATUS-HEADLINE` and `STATUS-17662` (must fix) |
| (new, not in the report) dfsW4 EXACT f(17662,2) = 221465 | the resumed dfsW4 run finished: reachable=0 at K = 279797, EXACT 221465 | **confirmed-with-fixes**: the upper bound f ≤ 221465 and the exact maximum 221465 are confirmed by program D (independent; identical tree size 5 927 905 821 = nodes/4). **Fix: no explicit witness at 221465 exists yet** (largest verified witness 221186, unshipped); produce, ship and verify one before stating the exact value (§6) |
| §4.1 exact values | exact f(a,2) for all even a ≤ 32768 except 17662 | **confirmed** (all 16382 exact survey rows re-certified by program D in both directions with own-verified witnesses; 594 by R3N.1). Minor fixes: the "largest g" table omits two rows; survey.py robustness (§4.1 of this check) |
| §4.1 shadow family | f(2^t−2,2) for t = 14..17: 20215, 37403, 90619, 135292 | **confirmed** (program D, both directions, own-verified witnesses) |
| §4.2 dfsW3 validation | dfsW3 output identical to dfsW on 262 runs and on 594 | **unverified** (not re-run; logs are consistent) |
| §3.1 program A | [failed attempt] BFS with deduplication | label correct; **unverified** (not re-run) |
| §1 Remark (deduplication useless) | at most 2 merges in every program-A run | **confirmed-with-fixes**: the label "[observation, computer-assisted]" is not in the label set; use [computer-assisted]. The a = 34 count (15 866 376 children) agrees with program D's independent alive_even count |
| §5 profile | population profile of the 594 tree; interpretation [heuristic] | **confirmed** as data (sum of boundary populations 13 566 171 = C's survivor count; peak 392 640 at M = 63446; arithmetic of 90111/90112/90400 checked); interpretation correctly labelled heuristic |
| §6 survival law | G·P(g ≥ G) ∈ [8, 12] for 256 ≤ G ≤ 131072 [heuristic] | **confirmed-with-fixes** as a heuristic: every number re-computed from the CSVs; labelled heuristic throughout; two wording fixes (§5) |
| §1 Speed claim | 33 s against Kitamura's 3.5 h "in Python" | **confirmed-with-fixes**: the Kitamura excerpt gives 3.5 h but does not say which implementation or language produced it |
| Credits | Kitamura, Lin, Erdős–Graham, Tao, track D | **confirmed** (Kitamura's repository HEAD 32697193 still unchanged at 15:21 UTC today) |

Nothing found here bears on Q1 for all a or on Q3; R3N.1 is one more finite value, as the track report says.

## 1. Line-by-line check of the lemmas and of the correctness arguments

Notation as in the track report: a ≥ 2 even, v = v_2, S_N(A) = Σ_{n∈A, n<N} n!, alive at N iff v(S_N) ≥ v(N!).

### 1.1 Lemma 1 [confirmed]
- (i) S_{a+1} = a! and v((a+1)!) = v(a!) since a+1 is odd. Correct.
- (ii) For even N, S_{N+1} = S_N + e·N!, both summands have valuation ≥ v(N!) = v((N+1)!). Correct.
- (iii) S_{N'} = S_N − Σ_{n∈A, N'≤n<N} n!, the subtracted sum is a multiple of N'!, and v(S_N) ≥ v(N!) ≥ v(N'!). Correct. (The hypothesis N > a+1 is not needed.)
- (iv) Existence: for N > max A, S_N = Σ_A > 0 is fixed while v(N!) → ∞. Evenness: if N_d were odd then N_d ≥ a+3 (by (i)), N_d − 1 is even and alive by minimality, so N_d is alive by (ii), a contradiction. The tail Σ_{n∈A, n≥N_d} n! is divisible by 2^{v(N_d!)} > 2^{v(S_{N_d})}, so v(Σ_A) = v(S_{N_d}). Correct.

### 1.2 Lemma 2 [confirmed]
- N_K is even because v((2m+1)!) = v((2m)!); N_K ≥ a+2 because v((a+1)!) = v(a!) < K. Correct.
- (a) ⇐ is immediate. ⇒: truncating A to [a, N_K) removes multiples of N_K!, hence of 2^K; for a < N < N_K, S_{N_K} − S_N is a multiple of N! and v(S_{N_K}) ≥ K > v(N!) (minimality of N_K), so the truncated set is alive at every such N and S_{N_K} is a final candidate (an initial candidate when N_K = a+2). Correct.
- (b) "≥": every listed c is Σ_B with min B = a. "≤": case N_d < N_K gives a death candidate of the prefix at N_d − 2 (alive by minimality of N_d; the report cites Lemma 1(iii), which also works), with v(Σ_A) = v(c) by Lemma 1(iv). Case N_d ≥ N_K: alive at N_K − 2, the final candidate has valuation < K ≤ v(N_K!) by hypothesis, so N_d = N_K. The bound v(c) < K holds for non-final death candidates since v(c) < v((N+2)!) ≤ v((N_K−2)!) < K. Correct.
- The enumeration paragraph (stage-by-stage extension reaches every alive prefix, by Lemma 1(iii) applied to the prefix as a finite set) is correct.

### 1.3 Lemma 3 and program C (`dfsW.c`) [confirmed]
- Lemma 3: write Z_i = 2^lo z_i with 0 ≤ z_i < 2^{K−lo}; then (Z_1+Z_2) mod 2^K = 2^lo((z_1+z_2) mod 2^{K−lo}) and the claim follows. Correct (it needs lo ≤ K, which holds at every window start used).
- Code, read line by line:
  - `make_level`: non-final windows end at the largest even M' with v(M'!) ≤ lo + 256 < K, so M' < N_K and every target v((N+2)!) − lo ≤ 256 = min(W, K − lo); the final window has K − lo ≤ 256 and its last target is clamped to K, with a run-time check that the clamp happens only at the last step of the final level.
  - The factorial tables are a running product mod 2^K (limbs below `base` are zero and are checked), so option windows are exact by Lemma 3; option 3 is the 256-bit sum of options 1 and 2, valid by Lemma 3.
  - DFS: a candidate is alive iff its low `tgt` window bits vanish; deaths record lo + ctz < target, which is exact; success only at the last step of the final level.
  - Materialisation: the invariant X_w = X + Σ_{inc} options (mod 2^K) is preserved by subtracting `inc` and adding `chosen` from the first differing index; the 256-bit window comparison is a valid full check in non-final windows (K − lo > 256); the final level never materialises.
  - Each level owns its X_w, inc, chosen, ys; the child copies its input; ancestors' `chosen` arrays describe the current path, so the witness writer is correct.
  - main: initial candidates a!, a! + (a+1)! are tested against v((a+2)!) (or K if N_K = a+2), deaths recorded.

### 1.4 Lemma 4 and program B (`dfsB.c`) [confirmed-with-fixes]
- The induction is correct: if ℓ_n ≡ T_n mod 2^m with m = min(128 − c_n, R_n) and t = v(n+1) ≤ m, then x ≫ t ≡ T_{n+1} mod 2^{m−t}, and m − t = min(128 − c_{n+1}, R_{n+1}).
- Non-final windows stop at the first n with c_n ≥ 64, so every step inside has c_n ≤ 63 and m ≥ 65 (also R_n = R_w − c_n > 65), which covers any t ≤ 18. The report's phrase "at least 128 − 63 − 18 > 18 valid bits" garbles this. The right statement is "at least 65 valid bits, and each test needs t = v(n+1) of them".
- **Unstated hypothesis.** t = v(n+1) ≤ 18 holds only for n < 2^19 = 524 288. All runs satisfy this (the largest stage used anywhere is about 280 000), but the lemma should state it, or the program should assert t ≤ 64 (it has no such check). Without it, a run with K above about 5·10^5 could silently test unchecked bits. This does not affect any result in the report.
- Final window: R_w ≤ 128, so the final test uses R_n = R_w − c_n ≤ 128 − c_n bits, all valid. Correct.
- Rebuild: T_end = ((T + Σ_{e_n=1} n!/2^{v(n_w!)}) mod 2^{R_w}) / 2^{c_end} is the definition. The code asserts that the low c_end bits vanish and that the result agrees with the window on its 128 − c_end valid bits. The table G[i] = U_n·2^{v(n!)−v(n_w!)} mod 2^{R_w} is correct, and the 128-bit odd-part table is cross-checked against the GMP value at each window. `path`/`ech` are set on descent and describe the current branch. Correct.

### 1.5 Lemma 5 [confirmed]
- C: 4 candidates per alive prefix at every even N, a+2 ≤ N ≤ N_K − 2. B: 1 step at n = a (forced), 2 at n = a+1, then 2α(N) at even N and 2α(N+1) = 4α(N) at the following odd stage (no death at odd stages by Lemma 1(ii); the two choices of e_N give distinct prefixes). The hypothesis is only that the search is not stopped by a success. Correct.
- Reproduced: 3 + 1.5 × 5 537 780 784 = 8 306 671 179 (both from the re-runs below).
- **Third program.** Program D (this check) counts its candidate steps and its alive prefixes at even stages a+2 ≤ N ≤ N_K − 2. The same counting gives steps_D = steps_B − 1 (D does not count the forced step at a) and alive_even = nodes_C/4. Both hold exactly for a = 594: 8 306 671 178 and 1 384 445 196. They also hold for a = 34 (95 198 258; 15 866 376) and a = 2 (alive_even 3246 = 12984/4). So three independently written programs enumerate trees of the same size.

### 1.6 Corollary R3N.2 [confirmed-with-fixes]
The statement is right, but the proof cites only Cor. 3.7.1(i). Note §3.4 states that corollary on a + 2^G ℤ (integers). The report's paraphrase says "on a + 2^G ℤ_2". To pass to ℤ_2, also cite Theorem 3.1(a) (locality: g ≥ G and g ≥ G+1 are decided by x mod 2^{G+1}): approximate y ∈ 594 + 2^89804 ℤ_2 by an integer y' ≡ y (mod 2^89805) in the same class. Alternatively, Theorem 3.1(b) alone gives the ℤ_2 statement on the smaller class mod 2^89805. One sentence fixes it.

## 2. Re-runs of programs B and C (rebuilt from source)

Sources: `dfsW.c` sha256 341f47e3…9e00, `dfsB.c` sha256 225d144d…9231. Built with gcc 13.3.0, `-O3 -march=native` (B with `-lgmp`), in `/tmp/r3_check_R3N`. Driver: `code/round3/check_R3N/rerun_594.sh`.

| run | result | wall | log |
|---|---|---|---|
| C `dfsW 594 90395` | reachable=0; nodes 5 537 780 784; surv 13 566 171; fulladds 146 314 113; EXACT f = 90394 (identical to the track's log) | 176.1 s | `rerun_W_594_K90395.log` |
| C `dfsW 594 90394 w.txt` | reachable=1; nodes 3 645 409 494; witness 44801 terms, **byte-identical** to the shipped `witness_594_K90394.txt.gz` (sha256 ea44330f…80f5) | 122.7 s | `rerun_W_594_K90394.log` |
| B `dfsB 594 90395` | reachable=0; steps 8 306 671 179; surv 56 569 314; windows 1381; EXACT f = 90394 (identical) | 739.2 s | `rerun_B_594_K90395.log` |

Smoke tests of the rebuilt binaries: f(2,2) = 254 and f(34,2) = 18444 in both programs (identity 95 198 259 = 3 + 1.5 × 63 465 504).

## 3. Own witness verifier and own exhaustive solver

### 3.1 Verifier `verify_w.py` (gmpy2)
Both of the track's verifiers build S = Σ n! as a running product of n! that is added term by term. Mine uses two other methods and requires them to agree:
- (H) backward Horner nesting, S = a_1!·(1 + P(a_1+1, a_2)·(1 + … (1 + P(a_{m−1}+1, a_m)))), exact integers;
- (M) S mod 2^{K+64}, assembled from the odd parts of n! and Legendre's v_2(n!) = n − s_2(n).

It also checks that the file is all integers, strictly increasing, with min = a, and it requires v_2(S) = K **exactly**.

Validation (`test_verifier.py`, log `test_verifier.log`):
- 300 random small sets against a direct v_2 of Σ math.factorial: 0 mismatches;
- the 594 witness is rejected when the claim is K = 90393 or K = 90395, when a = 592, when one line is duplicated, and when one line is dropped; the unchanged file is accepted;
- in addition, 128 + 16382 + 26 witnesses with known values (§3.3) all verify.

Results (`verify_all.sh`, log `verify_own.log`; every SHA-256 equals `witness_sha256.txt`):

| witness | terms | max | v_2(S) by H and by M | wall |
|---|---|---|---|---|
| `witness_594_K90394.txt.gz` (C) | 44801 | 90397 | 90394 = 90394 | 1.9 s |
| `witnessB_594_K90394.txt.gz` (B) | 44804 | 90399 | 90394 = 90394 | 1.1 s |
| `witness_594_K66126.txt.gz` | 32640 | 66130 | 66126 = 66126 | 0.8 s |
| `witness_17662_K148725.txt.gz` | 65459 | 148730 | 148725 = 148725 | 3.2 s |
| `witness_17662_v212995.txt.gz` | 97664 | 212992 | 212995 = 212995 | 6.1 s |
| `/tmp/r3_R3N/best17662_217088.txt` (not shipped; sha256 5bbe141f…a9be) | 99252 | 217091 | 217088 = 217088 | 5.9 s |
| `/tmp/r3_R3N/best17662_221186.txt` (not shipped; sha256 84121490…ce66) | 101329 | 221188 | 221186 = 221186 | 6.1 s |

So f(594,2) ≥ 90394 and f(17662,2) ≥ 221186 are verified exactly by a third method. The last two files exist only in `/tmp/r3_R3N`. They must be copied (gzipped, with SHA-256) into `data/round3/R3N/` before 217088 or 221186 is cited.

### 3.2 Program D (`dfsD.c`): design and independence
Written from scratch for this check; it shares no code with B, C or dfsW4. It also differs from both in design:
- single steps n → n+1 on the **unshifted** sum S_n mod 2^K (C: pair steps, unshifted; B: single steps, shifted);
- 128-bit windows in `unsigned __int128` at offset lo = v(s!), with the window end at the last stage t with v(t!) − lo ≤ 128 (C: 256-bit, 4 limbs; B: shifted 128-bit, ends after 64 consumed bits);
- full precision with GMP `mpn` limb functions (C: hand-written limbs; B: `mpz`);
- a survivor is updated by adding or subtracting n! **only at positions whose choice changed** (C subtracts and re-adds every position after the first difference; B rebuilds from scratch);
- the running factorial mod 2^K is cross-checked against `mpz_fac_ui` mod 2^K at every 8th window (89 checks for 594);
- every materialised survivor is checked against the window value and for full-precision aliveness (low v(t!) bits zero).

Its mathematics (written out in the file header) is Lemma 2 in single-step form, re-derived independently.

The partition option `-p L START END TLIMIT` (§6) was added after the 594, Kitamura, sample and full-survey runs. The final source (sha256 84b799ef…8400) leaves the unpartitioned path unchanged, apart from propagating the recursion's return code. Regression with the final binary: Kitamura's table ALL_OK again (`validate_D_kitamura_final_binary.log`), and a = 34 gives identical counters.

### 3.3 Validation of D

| test | result | time | log |
|---|---|---|---|
| Kitamura's `p2_exact_table_1_256.csv`, all 256 rows. Odd a: value = v_2(a!). Even a: K = f reachable (witness verified by `verify_w.py`, v_2 = f exactly) and K = f+1 unreachable with EXACT = f | ALL_OK: 128 + 128 rows, 128 witnesses verified | 13 s | `validate_D_kitamura.log` |
| seeded random sample: 400 rows of the survey CSVs + shadow CSV (seed 20261013), both directions, witnesses verified when g ≤ 20000 | ALL_OK | 46 s | `validate_D_survey.log` |
| explicit deep rows, both directions, all witnesses verified: 131070, 32766, 65534, 10578, 27142, 26274, 16846, **17534** (g = 59527), 32494, 22050, 1102, 3456, 8190, 16510, 9934, 20736, 25170, 12706, 25774, 26974, 2210, 1438, 574, 1602, 640, 2662 | ALL_OK (26 rows) | 27 + 135 + 11 s | `validate_D_deep1.log`, `validate_D_deep2.log`, `validate_D_deep3.log` |
| **full re-certification of every exact survey row** (16382 rows: all even a ≤ 32768 except 594 and 17662). D at K = f (witness, checked in-process by methods H and M: v_2 = f exactly, min = a, increasing; the witness file is blanked after each row) and at K = f+1 (unreachable, EXACT = f) | ALL_OK, 0 failures | 106 s + 449 s | `full_recert_2_16384.log`, `full_recert_16386_32768.log` |

### 3.4 Program D on a = 594 (third independent upper bound)

| run | result | wall | log |
|---|---|---|---|
| `dfsD 594 90395` | reachable=0; **EXACT f = 90394**; steps 8 306 671 178 (= steps_B − 1); alive_even 1 384 445 196 (= nodes_C/4); surv 51 825 254; updates 210 608 143; windows 705; faccheck 89 | 177.1 s | `D_594_K90395.log` |
| `dfsD 594 90394 w` | reachable=1; witness 44804 terms (same set as B's shipped witness: both search single steps in the order e = 0, 1); steps 3 169 957 294 = B's 3 169 957 295 − 1; witness VERIFIED by both methods (v_2 = 90394 exactly; sha256 c34a5088…c956) | 60.5 s | `D_594_K90394.log` |

So the upper bound f(594,2) ≤ 90394 now rests on three independently written exhaustive programs (B, C, D) with the same EXACT value and the same tree size. The lower bound rests on three witnesses (C's, B's = D's) checked by three verifiers (the track's two and mine).

## 4. CSV-level checks of §4.1 and §6 (`check_csv.py`, log `check_csv.log`)
- The three survey CSVs contain every even a in [2, 32768] exactly once. 16382 rows are exact and 2 are capped (594 at g ≥ 65536, 17662 at g ≥ 131072). Every exact row has the correct v_2(a!), g = f − v_2(a!), certB = 1 and witness_v2 = f.
- g ∉ {1, 2, 4, 5} and (g = 3 ⇔ a ≡ 4 mod 8) on all exact rows. The 128 values for even a ≤ 256 equal Kitamura's table. 1102, 3456, 8190 (and 2, 14, 34) equal Kitamura's rows.
- The 30 overlapping rows 24578..24636 of the two 16386..32768 processes are identical.
- The ranking claims hold: the a ≤ 4096 top ten are as stated, and 594 has the largest g for a ≤ 16384.
- **Minor fix (§4.1 table).** The table headed "Largest g among even a ≤ 32768" omits a = 25774 (f = 34813, g = 9047) and a = 26974 (f = 35481, g = 8516). Both exceed the listed 8190 (8218) and 3456 (4823). Either add them or retitle the table (e.g. "largest g, plus Kitamura's rows"). Program D confirms both values.
- §6 table re-computed: c(G) = 2077, 1244, 656, 367, 174, 94, 43, 19, 10, 5, 2, 1, and G·c/16384 = 8.1, 9.7, 10.25, 11.5, 10.9, 11.8, 10.8, 9.5, 10.0, 10.0, 8.0, 8.0. These match the report (it prints 10.3 for 10.25).
- §5: `profile_594.txt` has 351 boundaries with population sum 13 566 171 (= C's survivor count) and peak 392 640 at M = 63446. 90111 has binary digit sum 15, 90112 has 3, and v_2(90400) = 5.

### 4.1 Robustness of the track's survey driver (minor)
`survey.py` takes `v2(sum)=` from the GMP verifier's output without checking `VERIFIED` (which includes min A = a). It also ignores C's return status at K = f. If C ever failed to write the witness, the previous row's file would be re-verified. That would go unnoticed exactly when f(a) = f(a−2), which happens for **1141** survey rows. This cannot have happened silently in the shipped data: B independently confirmed reachability at K = f, so C must have succeeded unless it crashed. Program D's full re-certification checks min A = a and blanks the witness file after each row, so it closes the gap for all 16382 rows. The script should still be fixed before reuse.

## 5. Heuristic labels and credit
- §5 is labelled "[computer-assisted data; interpretation heuristic]", §6 "[heuristic]", the headline bullet "[heuristic]" and §8.2 "[heuristic]". Every survival-law statement is labelled heuristic, and §6 ends by saying that the c/G law is no evidence for f = ∞. Correct.
- §6 wording fixes:
  - (a) "This agrees well with Kitamura's measured ≈ 11.5/G" should add that Kitamura does not state the normalisation (Kitamura's figure comes from the class census; see S0's report, Remark 10.8.4). The report's conditional "provided that figure refers to even a" is good, but "agrees well" is stronger than an unknown normalisation allows; "is numerically consistent with" is safer.
  - (b) The "Haar densities" bullet compares c(256)/16384 with 2·0.0208, but note §5 gives 0.0208 for **δ_254**, not δ_256.
- Speed claim (§0): the excerpt (`witness_gallery.md` §9) gives "g(594,2) ≥ 65536 3.5 h" without naming the implementation. Kitamura's published search scripts are Python, so "in Python" is plausible but not stated by Kitamura. Suggest "Kitamura reports 3.5 h for that ladder step (implementation not stated; Kitamura's published scripts are Python)".
- Credit to Kitamura is correct and complete for what the report uses:
  - the normal form and determinacy lemma;
  - the exact-value pipeline (`determining_exact_values.md` §4–5);
  - the a ≤ 256 table and the rows 1102, 3456, 8190;
  - the shadow family (table to t = 13);
  - the critical-branching picture and ≈ 11.5/G;
  - a = 594 as the open champion with f(594,2) ≥ 66126 and no shipped witness (consistent with note §2, line 238).
- Kitamura's repository HEAD is 32697193 (`git ls-remote`, 2026-10-13 15:21 UTC), still the commit the excerpts quote. So "no exact value of f(594,2) had been published" holds as of today.
- Erdős–Graham, Lin, Tao (predicate/blocks, note §1.4) and track D (`sumform_big.c`) are credited correctly. No gendered pronouns and no model names were found in the report.

## 6. The finished dfsW4 run on a = 17662 (not yet in the report)

**What the track's log shows.** `data/round3/R3N/C4_17662_K279797.log` ends with:
- `RESULT a=17662 K=279797 reachable=0 nodes=23711623284 surv=56152623 fulladds=445378655 levels=444 time=3167.5s`;
- `EXACT a=17662 f=221465 g=203812`.

The run was interrupted once and resumed from the 2400 s checkpoint (level 92, depth 128) at 15:08:49 UTC. On its own, this is one program whose result depends on checkpoint/resume code. The track tested that code on a = 34 and a = 594, but it is still a single implementation, so rule 3 is not met by the track alone.

**Independent check by program D (this check)** (`chain_17662.sh`, log `D_17662_K221466_chain.log`). `dfsD 17662 221466` (N_K = 221472; 2.6 GB of tables) was split over the 20 000 subtrees rooted at window L = 120, in two sequential jobs (`-p 120 0 inf 1000`, then `-p 120 3019 inf 1000`):

| job | subtrees | deep steps | deep alive_even | best | wall |
|---|---|---|---|---|---|
| 1 | [0, 3019) | 27 708 712 172 | 4 618 117 689 | 221465 | 1214 s |
| 2 | [3019, 20000) (+ complete shallow part: 1 004 795 800 steps, 167 472 633 alive_even) | 6 853 926 956 | 1 142 315 499 | 131070 | 429 s |

- No job found S_{N_K} ≡ 0 mod 2^221466. So f(17662,2) ≤ 221465, and the maximum death valuation over the complete tree is 221465, i.e. EXACT f(17662,2) = 221465 (Lemma 2(b), valid because K = 221466 > 221465).
- **Tree size.** Total alive_even = 167 472 633 + 4 618 117 689 + 1 142 315 499 = **5 927 905 821 = 23 711 623 284 / 4 = nodes_dfsW4 / 4**. Total steps = 35 567 434 928 = 3 + 1.5 × 23 711 623 284 − 1. Both agree exactly with the Lemma-5 counting.
  - The comparison is legitimate. A prefix alive at stage 221472 would have valuation ≥ v_2(221472!) = 221466 at its death. dfsW4 says no death exceeds 221465, so its tree at K = 279797 and D's tree at K = 221466 must coincide.
  - The exact agreement also checks dfsW4's checkpoint/resume bookkeeping: its node counter after the resume is right.
- The partition option was tested on a = 34 before use: shallow + Σ deep reproduced 95 198 258 steps and 15 866 376 alive_even exactly. A time-limited stop produced a correct NEXT.

**Status.** EXACT f(17662,2) = 221465 (g = 203812) is **confirmed** as an upper bound and exact maximum by two independently written exhaustive programs (dfsW4 and D) with identical tree size [computer-assisted]. The lower bound needs an explicit verified witness; see the next paragraph. If it holds, f(17662,2) = 221465 is the largest exact value of f(a,2) known here, larger than both 594's g and f(131070,2) = 135292. Two report sentences then need updating: "the largest exact excess g is the one at a = 594" (§4.1) and "f(131070,2) = 135292 and f(65534,2) = 90619 are the largest exact values of f(a,2) we know".

**Lower bound (witness).** No witness file at 221465 exists: dfsW4 writes "best" witnesses only when the best crosses a multiple of 4096. The largest verified witness is 221186 (§3.1; file only in `/tmp/r3_R3N`). A time-boxed run `dfsD 17662 221465 W` (hard cap 840 s) stopped before reaching the success (best 214614 at the stop; `D_17662_K221465.log`), and my CPU budget did not allow a longer one.
- The exact value is reported by two independent programs as the maximum death valuation of a complete enumeration. That meets rule 3 ("two implementations sharing no code").
- It does not meet the project's own standard for exact values (an explicit witness verified from the definition), which the track applies everywhere else.
- **Required before the note states f(17662,2) = 221465:** produce the witness, e.g. `dfsW4 17662 221465 w.txt` (or D at the same K, uncapped). Ship it gzipped with its SHA-256, and verify it with `verify_w.py` (about 6 s) and the track's two verifiers.
- Until then, the safe statement is: 221186 ≤ f(17662,2) ≤ 221465, with 221465 the exact value according to two independent exhaustive programs [computer-assisted].

## 7. Required and suggested changes to the track report
1. **Must fix.** Replace the placeholders `STATUS-HEADLINE` (headline list) and `STATUS-17662` (§4.3). Record the shipped 212995 witness and the outcome of the dfsW4 run (§6 here), with the labels given in §6.
2. Ship `best17662_217088.txt` and `best17662_221186.txt` (gzipped, with SHA-256) if 217088 or 221186 is cited. Both verify exactly (§3.1).
2a. For the new dfsW4 result: produce, ship and verify a witness at 221465 before stating f(17662,2) = 221465 (§6). Then cite program D (this check) as the second, independent exhaustive program for the upper bound. Update the two "largest exact value" sentences of §4.1, and note in §7 (limitations) that the upper bound for 17662 now has a second program after all (B could not run there; D did, in two jobs).
3. Lemma 4: state n < 2^19 (or add `assert(t <= 64)` to dfsB); fix the "128 − 63 − 18" sentence.
4. Corollary R3N.2: cite Theorem 3.1(a) for the passage from ℤ to ℤ_2.
5. §4.1 table: add 25774 and 26974, or retitle.
6. §1 Remark: use the label [computer-assisted].
7. §6: the two wording fixes of §5 (normalisation of 11.5/G; δ_254 vs G = 256).
8. Speed claim: do not attribute "in Python" to Kitamura's 3.5 h figure.
9. survey.py: check `VERIFIED` and C's return status, and delete the witness file between rows.
10. Optional: cite program D (this check) as a third independent upper bound for R3N.1, and its full re-certification of §4.1.

## 8. Commands and logs (all in `data/round3/check_R3N/`; one core, `nice -n 10`)
- `code/round3/check_R3N/rerun_594.sh` → `rerun_W_594_K90395.log`, `rerun_W_594_K90394.log`, `rerun_B_594_K90395.log` (176 s, 123 s, 739 s).
- `gcc -O3 -march=native -o /tmp/r3_check_R3N/dfsD code/round3/check_R3N/dfsD.c -lgmp`; `dfsD 594 90395` → `D_594_K90395.log` (177 s); `dfsD 594 90394 W` + `verify_w.py` → `D_594_K90394.log` (61 s + 1 s).
- `code/round3/check_R3N/verify_all.sh` → `verify_own.log` (25 s in total).
- `python3 -I code/round3/check_R3N/test_verifier.py …` → `test_verifier.log`.
- `python3 -I code/round3/check_R3N/validate_D.py kitamura|survey|full …` → `validate_D_kitamura.log`, `validate_D_survey.log`, `validate_D_deep{1,2,3}.log`, `full_recert_2_16384.log`, `full_recert_16386_32768.log`.
- `python3 -I code/round3/check_R3N/check_csv.py data/round3/R3N data/round3/S0/kitamura_excerpts/p2_exact_table_1_256.csv` → `check_csv.log`.
- §6 runs: `chain_17662.sh` → `D_17662_K221466_chain.log` (1214 s + 429 s); `D_17662_K221466_stopped_at_146s.log` (first, unsplit attempt, stopped by me after 146 s because its projected length exceeded the 30-minute job limit); `D_17662_K221465.log` (witness run).
