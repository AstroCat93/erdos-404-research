# Track R3N (round 3, 2026-10-13): Kitamura's test case a = 594 at p = 2

*Edited by the lead after the adversarial check (`data/round3/checks/R3N.md`): the a = 17662 result (§4.3, Proposition R3N.4) was completed after the track agent was cut off by an external spending limit, and the check's wording and label fixes were applied. Edits are marked.*

## Headline

**f(594,2) = 90394 exactly**, i.e. g_2(594) = 90394 − v_2(594!) = 90394 − 590 = **89804**. [computer-assisted]

- **Upper bound.** No sum of distinct factorials with smallest term 594! is divisible by 2^90395. Two independently written exhaustive searches show this (program B, GMP, 1001 s; program C, hand-written limb arithmetic, 181 s). They share no code. Each enumerates every "alive" partial sum, and each reports 90394 as the largest 2-adic valuation over all such sums. The two programs agree exactly on the size of the search tree, through the identity steps_B = 3 + (3/2)·nodes_C (Lemma 5), with 8 306 671 179 = 3 + 1.5 · 5 537 780 784. Program C also gives the same result with target K = 131662, and the node count is identical, as it must be.
- **Lower bound.** An explicit set A ⊂ [594, 90397] with min A = 594 and |A| = 44801 satisfies v_2(Σ_{n∈A} n!) = 90394. Two exact big-integer verifiers check this independently, one in plain Python and one in GMP. Neither reduces modulo anything: each builds the full 1 357 890-bit sum. The witness ships as `data/round3/R3N/witness_594_K90394.txt.gz`.
- **Consequences.** f(594,2) is finite, so the live test case of the note (§2, §5, Remark 10.8.5, §10.6) is resolved. By the halving lemma (Cor. 3.7.1(i)), f(a,2) = v_2(a!) + 89804 for every a ≡ 594 (mod 2^89804). No exact value of f(594,2) had been published. Kitamura's repository (HEAD 3269719, 2026-07-08, unchanged on 2026-10-13) gives f(594,2) ≥ 66126 and no witness. Our ≥ 66126 witness (outcome 3, 32640 terms) is also shipped and verified.
- **Speed.** The method is a windowed depth-first search (§3). It reproduces Kitamura's g_2(594) ≥ 65536 in 33 s; Kitamura reports 3.5 h for that ladder step (implementation not stated; Kitamura's published scripts are Python). The machines and languages differ, so this is not a like-for-like comparison. It is also much faster than our own breadth-first search with deduplication (program A, which follows track D's design). On a = 34, K = 18445 the times are 0.9 s against 8.6 s. On a = 594, K = 66126, program A needed 340 s to reach only stage N = 10596, while C finished the whole search in 33 s.
- **Secondary results** [computer-assisted]:
  - **Exact f(a,2) for all 16384 even a ≤ 32768 except a = 17662**, each certified by two programs plus an exactly verified witness (§4.1). Odd a are trivial.
    - Among a ≤ 16384 the largest excess is at 594.
    - The next largest excesses are at a = 17534 (g = 59527), 16846 (44786), 26274 (42347), 27142 (26746), 10578 (24271) and 34 (18412).
  - **a = 17662 is a deeper survivor than 594: f(17662,2) = 221465 exactly, i.e. g_2(17662) = 203812** (§4.3). *(Lead, after the check:)* the upper bound rests on two independently written exhaustive programs (this track's `dfsW4` and the checker's program D, with identical tree size), and the lower bound on a 101480-term witness verified exactly by three verifiers.
  - Shadow family 2^t − 2: f(16382,2) = 20215, f(32766,2) = 37403, f(65534,2) = 90619 and f(131070,2) = 135292. These extend Kitamura's table, which stops at t = 13.
  - A population profile of the a = 594 search tree (§5).
  - [heuristic] Over even a ≤ 32768, G·P(g_2 ≥ G) stays between 8 and 12 for 256 ≤ G ≤ 131072 (§6). This is consistent with Kitamura's ≈ 11.5/G, and it suggests how the note's 0.7/√G fit (small G) and the 1/G law (large G) fit together.

Nothing here bears on Q3 or on Q1 for all a. The result is one more finite value, of the kind Theorem 3.6 allows (finite-depth certificates exist for finiteness, never for f = ∞).

---

## 1. Setting, and the two lemmas every program relies on [proved]

Throughout, a ≥ 2 is even (for odd a, f(a,2) = v_2(a!), see note §2) and v = v_2. For a finite set A ⊂ ℤ with min A = a and N > a, put

  S_N(A) = Σ_{n∈A, n<N} n!,  Σ_A = Σ_{n∈A} n!.

Say that A is **alive at N** if v(S_N(A)) ≥ v(N!). Note that S_N(A) depends only on the prefix A ∩ [a, N). By definition f(a,2) = sup_A v(Σ_A) over finite A with min A = a.

**Lemma 1 (stages).**
- (i) A is alive at a+1.
- (ii) If N is even and A is alive at N, then A is alive at N+1.
- (iii) If A is alive at N > a+1, then A is alive at every N' with a < N' ≤ N.
- (iv) The **death stage** N_d(A) = min{N > a : A not alive at N} exists. It is even, N_d ≥ a+2, and v(Σ_A) = v(S_{N_d}(A)) < v(N_d!).

*Proof.*
- (i) S_{a+1} = a!, and v((a+1)!) = v(a!) because a+1 is odd.
- (ii) S_{N+1} = S_N + e·N! with e ∈ {0,1}. Both terms have valuation ≥ v(N!), and v(N!) = v((N+1)!) because N+1 is odd.
- (iii) S_N − S_{N'} = Σ_{n∈A, N'≤n<N} n! is divisible by N'!, so v(S_{N'}) ≥ min(v(S_N), v(N'!)) ≥ v(N'!), using v(S_N) ≥ v(N!) ≥ v(N'!).
- (iv) For N > max A, S_N(A) = Σ_A is a fixed positive integer, while v(N!) → ∞. So a non-alive stage exists. By (i) and (ii) the first one is even and ≥ a+2. Finally Σ_A − S_{N_d} = Σ_{n∈A, n≥N_d} n! ≡ 0 (mod 2^{v(N_d!)}). Since v(S_{N_d}) < v(N_d!), this gives v(Σ_A) = v(S_{N_d}). ∎

**Pair steps and candidates.** Let N ≥ a+2 be even, and let P be a prefix (P ⊂ [a,N), min P = a) alive at N. Its four **candidates** are S_N(P) + d with d ∈ {0, N!, (N+1)!, N!+(N+1)!}, which are exactly the possible values of S_{N+2}. The **initial candidates** are a! and a! + (a+1)!, the possible values of S_{a+2}. A candidate is **alive** if its valuation is ≥ v((N+2)!); otherwise it is a **death candidate**. Fix the target K > v(a!), and let N_K = min{N : v(N!) ≥ K}. This N_K is even, since v((2m+1)!) = v((2m)!). The pair step ending at N_K is the **final step**, and its candidates are **final candidates**.

**Lemma 2 (decision and exact value).**
- (a) f(a,2) ≥ K iff some final candidate (of some alive prefix at N_K − 2, or an initial candidate if N_K = a+2) is ≡ 0 (mod 2^K).
- (b) Suppose no final candidate is ≡ 0 (mod 2^K). Then f(a,2) = max{v(c) : c a death candidate at a stage ≤ N_K, or a final candidate}, and this maximum is < K. Every such v(c) is < K, so it can be read off c mod 2^K.

*Proof.*
- (a) ⇐: a candidate is Σ_B for a finite set B with min B = a.
- (a) ⇒: let v(Σ_A) ≥ K. Replace A by A ∩ [a, N_K); the deleted terms are divisible by N_K!, hence by 2^K. For every N < N_K, S_{N_K} − S_N is divisible by N!, and v(S_{N_K}) ≥ K > v(N!). So A is alive at every N < N_K, and S_{N_K}(A) is a final candidate (of the alive prefix A ∩ [a, N_K−2)) with valuation ≥ K.
- (b): every listed c is a sum Σ_B with min B = a, so f ≥ max. Conversely, let A be finite with min A = a and death stage N_d.
  - If N_d < N_K, then S_{N_d}(A) is a death candidate (of the prefix at N_d − 2, alive by Lemma 1(iii), or an initial candidate). By Lemma 1(iv), v(Σ_A) equals its valuation.
  - If N_d ≥ N_K, then A is alive at N_K − 2, and S_{N_K}(A) is a final candidate. By hypothesis it has valuation < K ≤ v(N_K!). So N_d = N_K, and again v(Σ_A) = v(S_{N_K}(A)) by Lemma 1(iv).
  - The bound v(c) < K holds for non-final death candidates because v(c) < v((N+2)!) < K. For final candidates it holds by hypothesis. ∎

So deciding f(a,2) ≥ K means enumerating the alive prefixes at the even stages a+2 ≤ N ≤ N_K − 2. The enumeration can proceed stage by stage, extending only alive prefixes. By Lemma 1(iii), applied to the prefix itself as a finite set, a prefix alive at N restricts to an alive prefix at every earlier even stage, so stage-by-stage extension reaches every alive prefix. When the answer is no, the same enumeration gives f(a,2) exactly, provided we record the largest death valuation. This is the procedure of Kitamura (`determining_exact_values.md`) and of track D's `sumform_big.c`, written in the language of note §1.4. Our contribution is the way the enumeration is organised (§3).

**Remark (deduplication is useless here).** Two different alive prefixes with equal residues mod 2^K have identical futures. A breadth-first search can merge them, as track D and Kitamura do. In every run of program A (§3.1), however, deduplication merged at most 2 states in total; for example, 1 out of 15 866 376 children for a = 34, K = 18444. So in practice the number of distinct residues equals the number of alive prefixes. This is what makes a search without deduplication, but with memory O(K), efficient. [computer-assisted; logs in `data/round3/R3N/validate_deep_rows.log`]

## 2. Main result

**Theorem R3N.1 [computer-assisted].** f(594,2) = 90394, i.e. g_2(594) = 89804. Moreover:
- every finite A with min A = 594 has death stage ≤ 90400;
- the last stage at which some prefix is alive is N = 90398 (v(90398!) = 90390);
- the maximum 90394 is attained, for example by the shipped 44801-term witness, whose largest element is 90397.

**Corollary R3N.2 [proved from R3N.1, note Cor. 3.7.1(i) and note Theorem 3.1(a)].** f(a,2) = v_2(a!) + 89804 for every a ≡ 594 (mod 2^89804). In particular K_2 ∩ (594 + 2^89804 ℤ_2) = ∅.

*Proof of the corollary.* Cor. 3.7.1(i) (halving lemma, proved and in Lean) says that g_2(a) = G ≥ 1 implies g_2 ≡ G on the integers of a + 2^G ℤ. Combine this with Lemma 1.1 of the note for the integer statement. *(Fix after the check:)* for the ℤ_2 statement, also use Theorem 3.1(a) (locality): for y ∈ 594 + 2^89804 ℤ_2, the events g_2 ≥ G and g_2 ≥ G+1 are decided by y mod 2^{G+1}, so y has the same g_2 as an integer y' ≡ y (mod 2^{89805}) in the same class. ∎

### 2.1 Computational record for Theorem R3N.1

Programs are in `code/round3/R3N/`, binaries were built in `/tmp/r3_R3N` (commands in `code/round3/R3N/README.md`), and logs are in `data/round3/R3N/`. Every log starts with its command line. All runs used `nice -n 10`, on one core each, on the shared 4-core machine.

| what | program | command | result | wall time | log |
|---|---|---|---|---|---|
| upper bound | C (`dfsW.c`) | `dfsW 594 131662` | reachable=0; EXACT f=90394; nodes=5 537 780 784; survivors=13 566 171 | 275.8 s | `C_594_K131662.log` |
| upper bound | C | `dfsW 594 90395` | reachable=0; EXACT f=90394; **same** nodes and survivors | 181.0 s | `C_594_K90395.log` |
| upper bound | B (`dfsB.c`) | `dfsB 594 90395` | reachable=0; EXACT f=90394; steps=8 306 671 179 | 1001.4 s | `B_594_K90395.log` |
| lower bound | C | `dfsW 594 90394 w594_90394.txt` | reachable=1; witness 44801 terms, max element 90397 | 140.3 s | `C_594_K90394.log` |
| lower bound | B | `dfsB 594 90394 wB594_90394.txt` | reachable=1; its own witness, 44804 terms, max element 90399 (differs from C's witness in the last terms) | 320.3 s | `B_594_K90394.log` |
| B's witness | both verifiers | as above | v_2(sum) = 90394: VERIFIED (both) | 5.4 s | `verify_B_witness_594_90394.log` |
| witness check 1 | `verify_witness.py` (plain Python ints) | `python3 -I verify_witness.py w594_90394.txt 594 90394` | 44801 terms, min 594, strictly increasing, v_2(sum) = 90394, sum has 1 357 890 bits: VERIFIED | 2.8 s | `verify_py_594_90394.log` |
| witness check 2 | `verify_witness_gmp.c` (GMP) | `verify_witness_gmp w594_90394.txt 594 90394` | v_2(sum) = 90394: VERIFIED | < 2 s | `verify_gmp_594_90394.log` |
| profile | C' (`dfsWp.c`) | `dfsWp 594 90395 - profile_594.txt` | identical nodes and EXACT; deepest alive stage 90398 | 267.4 s | `Cp_594_K90395.log`, `profile_594.txt` |
| robustness | C compiled by clang with 512-bit windows (`-DWL=8`) | `dfsW8c 594 90395` | reachable=0; EXACT f=90394; nodes=5 537 780 784 (identical), but 176 levels instead of 352 and 2 283 824 survivors | 202.8 s | `C_WL8clang_594_K90395.log` |
| Kitamura's bound | C | `dfsW 594 66126 w594_66126.txt` | reachable=1, witness 32640 terms | 32.8 s | `C_594_K66126.log` |
| its witness | both verifiers | as above with 66126 | v_2(sum) = 66126: VERIFIED (both) | 1.3 s | `verify_py_594_66126.log`, `verify_gmp_594_66126.log` |

Witness files are `witness_594_K90394.txt.gz` (98 KB, from C), `witnessB_594_K90394.txt.gz` (from B) and `witness_594_K66126.txt.gz` (72 KB). Their SHA-256 sums, of the uncompressed text, are in `witness_sha256.txt`.

Validation before the 594 runs:
- **Kitamura's full table.** Programs B and C were run against K. Kitamura's exact table `p2_exact_table_1_256.csv`, for all 128 even a ≤ 256 and in both directions: K = f gives reachable, and K = f+1 gives unreachable with EXACT = f. Result: ALL_OK, 512 runs (`validate_table.log`; `validate_table.py`).
- **Deeper rows.** Programs A, B and C all reproduce f(2,2)=254, f(14,2)=1533, f(38,2)=828, f(34,2)=18444, f(1102,2)=12633, f(3456,2)=8275 and f(8190,2)=16396, in both directions. That is 42 runs, all agreeing (`validate_deep_rows.log`).
- **Profile against BFS.** The DFS profile of a = 34 agrees with the BFS populations of program A at the sampled boundaries N = 294, 550, 806 and 1060 (92, 214, 450, 97 states).
- **Witness verifiers.** Both verifiers return v_2 = 254 and 18444 on the C-witnesses for f(2,2) and f(34,2). The first has 119 terms, the same count as Kitamura's Lean-checked list; the second has 9216 terms, the same count as Kitamura's shipped list.

Total CPU for the 594 certification is about 30 core-minutes.

### 2.2 Why the two upper-bound programs are independent

| | program C (`dfsW.c`) | program B (`dfsB.c`) |
|---|---|---|
| arithmetic | hand-written 64-bit limbs, `unsigned __int128` carries | GMP `mpz` |
| normal form | unshifted, X = S_N mod 2^K | shifted, T_N = S_N/2^{v(N!)} mod 2^{K−v(N!)}, update T_{N+1} = (T_N + e·U_N)/2^{v(N+1)}, U_N = odd part of N! |
| step | pair steps N → N+2, 4 candidates | single steps N → N+1, 2 candidates |
| window | 256 bits at fixed alignment v(M_j!), boundaries where v grows by ≤ 256 | low 128 bits, right-shifted each step, window ends after ≥ 64 consumed bits |
| full-precision update | prefix-sharing add/subtract between consecutive survivors | each survivor rebuilt from scratch (sum of all its window terms) |
| exact value | max death valuation, lo_j + ctz(window) | max death valuation, v(n!) + ctz(128-bit value) |

Both programs share the mathematics of Lemmas 1–2 (which is proved) and nothing else. Neither deduplicates states, so neither depends on hashing.

### 2.3 Why each program is correct [proved]

**Lemma 3 (window lemma, program C).** Let M be even, lo = v(M!), and W = 256. For an integer 0 ≤ Z < 2^K with 2^lo | Z, put w(Z) = ⌊Z/2^lo⌋ mod 2^W. If 2^lo divides Z_1 and Z_2, then w((Z_1+Z_2) mod 2^K) ≡ w(Z_1) + w(Z_2) (mod 2^{min(W, K−lo)}).

*Proof.* Write Z_i = 2^lo z_i with 0 ≤ z_i < 2^{K−lo}. Then (Z_1+Z_2) mod 2^K = 2^lo · ((z_1+z_2) mod 2^{K−lo}), and reducing mod 2^{min(W,K−lo)} gives the claim. ∎

Now take an alive state X at a window start M_j. It satisfies 2^lo | X, and every factorial n! with n ≥ M_j is divisible by 2^lo. By Lemma 3, the window value tracked by the program agrees with w(S_N) on the low min(W, K−lo) bits, for every stage N in the window. The window end M_{j+1} is chosen so that v(M_{j+1}!) ≤ lo + W, or, in the last window, so that K − lo ≤ W. Hence every test "v(c) ≥ v((N+2)!)" (or "≥ K" at the final step) only inspects bits below min(W, K−lo). Every death valuation is lo + ctz(window value), with ctz below the target.

At the window end the program materialises the full state. It keeps an invariant: the working copy X_w equals X plus the option values of the currently included path `inc`, mod 2^K. For a new survivor path `chosen`, it subtracts the terms of `inc` from the first index where the two paths differ, and adds those of `chosen`; this preserves the invariant. A run-time assertion checks that the window of X_w equals the tracked window value. It never fired.

The recursion enters level j+1 with X_w for every survivor, so every alive prefix at every even stage is expanded exactly once, which is the enumeration of Lemma 2.

**Lemma 4 (window lemma, program B).** Fix a window start n_w with full state T = T_{n_w} mod 2^{R_w}, where R_w = K − v(n_w!). Let c_n = v(n!) − v(n_w!) be the number of bits consumed by stage n. Then the program's 128-bit value ℓ_n satisfies ℓ_n ≡ T_n (mod 2^{min(128−c_n, R_n)}), where R_n = K − v(n!).

*Proof.* By induction on n. ℓ_{n_w} = T mod 2^128. If ℓ_n ≡ T_n mod 2^m with m = min(128−c_n, R_n), then x = ℓ_n + e·(U_n mod 2^128) ≡ T_n + e·U_n (mod 2^m). Since 2^t | x exactly when 2^t | T_n + eU_n (t = v(n+1) ≤ 18 ≤ m, see below), we get x ≫ t ≡ T_{n+1} (mod 2^{m−t}), and m − t = min(128 − c_{n+1}, R_{n+1}). ∎

Each test needs t = v(n+1) valid bits, and t ≤ 18 because every stage used is below 2^19 = 524 288 (the largest is about 280 000; *hypothesis made explicit after the check*). A non-final window ends as soon as c ≥ 64, so every step inside it has at least 65 valid bits. The final window has R_w ≤ 128, so the final test "x ≡ 0 mod 2^{K−v(n!)}" uses K − v(n!) = R_n ≤ 128 − c_n bits.

At the window end, a survivor is rebuilt from the definition: T_end = ((T + Σ_{n∈window, e_n=1} n!/2^{v(n_w!)}) mod 2^{R_w}) / 2^{c_end}. The program asserts that the low c_end bits vanish and that the result agrees with ℓ on its valid bits. Neither assertion ever fired.

**Lemma 5 (exact tree-size identity between B and C).** Let α(N) be the number of alive prefixes at stage N. Suppose all prefixes die at or before the final step, as happens in the runs above. Then nodes_C = 4·Σ_{N even, N≥a+2} α(N), and steps_B = 3 + 6·Σ_{N even, N≥a+2} α(N) = 3 + (3/2)·nodes_C.

*Proof.*
- Program C evaluates 4 candidates for each alive prefix at each even stage ≥ a+2. Its initial step is done outside the counter.
- Program B evaluates 1 candidate at n = a (e forced) and 2 at n = a+1 (α(a+1) = 1). At each even N ≥ a+2 it evaluates 2α(N). At the following odd stage there are α(N+1) = 2α(N) prefixes, by Lemma 1(ii) and the fact that the two choices of e_N give different prefixes; there it evaluates 2α(N+1) = 4α(N).
- Summing gives the stated count. ∎

For a = 594, K = 90395, the identity holds exactly: 3 + 1.5 × 5 537 780 784 = 8 306 671 179. It also holds for every validation run we checked: a = 34 (95 198 259), 1102 (68 380 257) and 8190 (45 918 939). So the two programs enumerate trees of exactly the same size. Hence Σ_N α(N) = 1 384 445 196 alive (prefix, even stage) pairs for a = 594.

### 2.4 Adversarial re-check of the main claim

R3N.1 does not settle Q1 for all a or Q3, so the obstruction checklist of the task rules is not triggered. It was still re-checked against each way it could be wrong:

1. *Wrong problem.* The sets must have minimum exactly 594. Both programs force e_594 = 1 (C in `main`, B by `emin` at n = a). The witness verifiers check min A = 594 and strict increase.
2. *Search not exhaustive.* Lemma 2 needs every alive prefix at every even stage below N_K. Both programs expand all of them: there is no deduplication and no pruning other than the aliveness test.
   - The tree is K-independent (aliveness at N < N_K does not involve K), so C's node count must be the same for K = 90395 and K = 131662. It is. It is also the same with 512-bit windows under a different compiler (clang), where the window boundaries and the materialisation pattern are completely different.
   - B and C agree on the tree size through the exact identity of Lemma 5.
3. *Precision errors.* C's materialisation is checked against its window at every survivor. B rebuilds every survivor from scratch and checks it against its window. A high-bit error in C would propagate into later windows and would almost surely change the node count, which differs neither between the two K values nor from B.
4. *Exact value.* Lemma 2(b) needs all death valuations to be < K; the runs used K = 90395 > 90394. The value 90394 is reached by an explicit witness, verified twice from the definition. The value 90395 is excluded by two programs.
5. *Odd-stage deaths.* Lemma 1(ii) shows these do not occur. Program B, which processes odd stages explicitly, would have caught one.
6. *Consistency with note theorems.* The values f(a,2) obtained all have g ∈ {0,3} ∪ [6,∞) (Cor. 3.7.1(iii)); for 594, g = 89804. Over all 16385 exact survey rows, g never takes the values 1, 2, 4 or 5, and g = 3 occurs exactly for a ≡ 4 (mod 8) (§4.1).

## 3. Method: the windowed depth-first search [proved correct above; performance computer-assisted]

### 3.1 Program A (breadth-first, failed as a route to 594) [failed attempt]

Program A (`bfsA.c`) is track D's `sumform_big` in the unshifted normal form, with pair steps, a two-limb survivor filter and hash deduplication. It is correct (validated above) but memory-bound: each step streams the whole population of R-bit states through memory, about 9 ns per limb on this machine.

For a = 594 and K = 66126, the population was 222 270 states by N = 8596, at 1.7 GB, and the run had reached only N = 10596 after 6 CPU-minutes. The DFS profile (§5) shows populations up to 392 640 at N ≈ 63446. A BFS at K = 90395 would therefore need about 4 GB and 2–3 hours. We stopped the run (`A_594_K66126.log`). The lead's probe with a 2^22 cap is consistent with this.

### 3.2 Program C (windowed DFS)

Split the stages into windows [M_j, M_{j+1}) in which v(N!) grows by at most 256. Inside a window, only 4 limbs per state are tracked, by Lemma 3. A depth-first search over the 4 options per pair step finds all survivors at M_{j+1} at a cost of a few nanoseconds per candidate. Only survivors are lifted to full precision, about 11 full-length additions per survivor thanks to prefix sharing, and the search recurses.

Memory is O(K²/16) bytes for the cached factorial tables (n! mod 2^K for all n in the range, about 0.5 GB at K = 90395) plus O(K) for the stack. There is no population storage. For a = 594, K = 90395 the run handled 1.38·10^9 alive (prefix, even stage) pairs, that is 5.5·10^9 candidate evaluations, in 181 s: about 33 ns per candidate, including all full-precision work (1.46·10^8 full-length additions or subtractions).

Window sizes of 128, 256 and 512 bits were tried on a = 34, K = 18445 (1.0 s, 0.9 s, 1.1 s); 256 was kept. The design works because, in a critical branching tree, most subtrees die within one window, so their high bits are never computed. Full-precision work scales with the number of survivors at window boundaries, about 1/100 of all nodes for a = 594.

## 4. Secondary results [computer-assisted]

### 4.1 Exact f(a,2) for all even a ≤ 32768, except 594 (R3N.1) and 17662 (§4.3)

Command: `survey.py A0 A1 GMAX /tmp/r3_R3N OUT.csv`. For each even a:
1. program C is run with K = v(a!) + G for G = 64, 128, 256, … until the run is unreachable, which gives EXACT f;
2. program B is run at K = f (must be reachable) and at K = f+1 (must be unreachable with the same EXACT);
3. C writes a witness at K = f, and the GMP verifier must return v_2(sum) = f exactly.

All three checks pass for all 16384 even a ≤ 32768 except two capped rows:
- a = 594, capped at G = 65536 in the first file and superseded by R3N.1;
- a = 17662, capped at G = 131072 (§4.3).

| file | range | rows | wall time |
|---|---|---|---|
| `survey_2_4096.csv` (+ `.log`) | even 2..4096, cap G = 65536 | 2048 | ≈ 8 min |
| `survey_4098_16384.csv` (+ `.log`) | even 4098..16384, cap 131072 | 6144 | ≈ 6 min |
| `survey_16386_32768.csv`, `survey_24578_32768.csv` (+ logs), merged as **`survey_16386_32768_merged.csv`** | even 16386..32768, cap 131072 | 8192 | ≈ 75 min (two processes) |
| `shadow_t15_17.csv` (+ `.log`) | a = 32766, 65534, 131070 | 3 | ≈ 1.5 min |

The first 16386..32768 process was stopped after a = 24636. Its 30 rows overlapping with the second process are identical, field by field.

Cross-checks:
- The 128 values for a ≤ 256 agree with Kitamura's table, and 1102, 3456 and 8190 agree with Kitamura's deeper rows.
- Over all 16385 exact rows, g never takes the values 1, 2, 4 or 5, and g = 3 exactly when a ≡ 4 (mod 8). This matches Cor. 3.7.1(iii) and Kitamura's classification.

Largest g among even a ≤ 32768, plus Kitamura's rows (f = v(a!) + g):

| a | f(a,2) | g_2(a) | note |
|---|---|---|---|
| 17662 | 221465 | 203812 | §4.3 |
| 594 | 90394 | 89804 | R3N.1 |
| 17534 | 77053 | 59527 | new |
| 16846 | 61625 | 44786 | new |
| 26274 | 68614 | 42347 | new |
| 27142 | 53882 | 26746 | new |
| 10578 | 34843 | 24271 | new |
| 34 | 18444 | 18412 | Kitamura |
| 32494 | 50505 | 18023 | new |
| 22050 | 38672 | 16628 | new |
| 16510 | 31226 | 14723 | new |
| 9934 | 24580 | 14654 | new |
| 20736 | 32765 | 12032 | new |
| 25170 | 36861 | 11697 | new |
| 1102 | 12633 | 11536 | Kitamura |
| 12706 | 22969 | 10269 | new |
| 8190 | 16396 | 8218 | Kitamura (shadow t = 13) |
| 3456 | 8275 | 4823 | Kitamura |
| 25774 | 34813 | 9047 | new (row added after the check) |
| 26974 | 35481 | 8516 | new (row added after the check) |

("New" means: not listed in `KitaKen1/erdos-404-p2-landscape` at HEAD 3269719. Kitamura may have computed values that were not published.)

**Answer to the task's secondary question.** Among a ≤ 4096 the largest g_2(a) is at a = 594, followed by 34, 1102, 2210 (g = 6261), 3456, 1438 (3948), 574 (3526), 1602 (3486), 640 (3196) and 2662 (3129). Among a ≤ 16384, 594 is still the largest. In (16384, 32768] there is a larger survivor, a = 17662 (§4.3).

Every exact value pins a whole residue class (Cor. 3.7.1(i)): for example, f(a,2) = v_2(a!) + 59527 for all a ≡ 17534 (mod 2^59527).

**Shadow family a = 2^t − 2** (Kitamura's table stops at t = 13, with g = 8218):

| t | a | f(a,2) | g_2(a) |
|---|---|---|---|
| 14 | 16382 | 20215 | 3846 |
| 15 | 32766 | 37403 | 4651 |
| 16 | 65534 | 90619 | 25100 |
| 17 | 131070 | 135292 | 4238 |

All four are consistent with the cube bound g ≥ 3t. *(Updated after §4.3 was completed:)* the largest exact value of f(a,2) and the largest exact excess known here are both at a = 17662 (f = 221465, g = 203812). Among the other exact values, f(131070,2) = 135292 and f(65534,2) = 90619 are large mainly because v_2(a!) is large.

### 4.2 Validation of the half-memory variant `dfsW3.c`

`dfsW3.c` differs from `dfsW.c` in two ways:
- it stores only N! for even N in each window, half the table memory;
- it applies the three options as multiply-adds N!·m with m = 1, N+1, N+2.

Its output (RESULT and EXACT lines, including the node and survivor counts) is identical to `dfsW`'s on 262 runs: all even a ≤ 256 plus 1102, 3456 and 8190, at K = f and f+1 (`validate_dfsW3.log`). On a = 594, K = 90395 it gives the same nodes (5 537 780 784), the same survivors and EXACT f = 90394 (`C3_594_K90395.log`, 390 s).

### 4.3 a = 17662: a deeper survivor than 594 [computer-assisted lower bound]

**Proposition R3N.3 [computer-assisted; superseded by R3N.4].** f(17662,2) ≥ 148725, i.e. g_2(17662) ≥ 131072 (v_2(17662!) = 17653).
- *Witness:* 65459 terms in [17662, 148730], `witness_17662_K148725.txt.gz`.
- *Exact check:* v_2 of the 2 340 967-bit sum is 148725, by both exact verifiers (`verify_17662_148725.log`; 20 s in Python).
- *Search run:* `dfsW 17662 148725 w17662_148725.txt` (`C_17662_K148725.log`, 172 s).

**Proposition R3N.4 [computer-assisted] (completed by the lead after the agent was cut off).** f(17662,2) = 221465 exactly, i.e. g_2(17662) = 203812.
- *Upper bound and exact maximum, program C variant `dfsW4`* (checkpointing; tested on a = 34 and 594 under interruption): `dfsW4 17662 279797 ... -c ck17662 -i 600 -b best17662`, interrupted once by the external stop and resumed with `-r` from the 2400 s checkpoint. RESULT reachable=0, nodes 23 711 623 284, survivors 56 152 623, EXACT f = 221465 (`C4_17662_K279797.log`, 2400 s + 3167.5 s).
- *Independent upper bound, program D* (written by the checker, sharing no code with B, C or `dfsW4`): `dfsD 17662 221466`, split into subtrees at window level 120, unreachable, maximum death valuation 221465, total alive_even 5 927 905 821 = nodes_dfsW4 / 4 exactly (`data/round3/check_R3N/D_17662_K221466_chain.log`). The tree-size agreement also checks dfsW4's resume bookkeeping.
- *Witness:* `dfsW4 17662 221465 w17662_221465.txt` (reachable, 592.7 s; `C4_17662_K221465_witness.log`), 101480 terms in [17662, 221465], shipped as `witness_17662_K221465.txt.gz` (SHA-256 in `witness_sha256.txt`). v_2 of the 3 612 996-bit sum is exactly 221465 by three verifiers: the track's GMP and Python verifiers and the checker's `verify_w.py` (Horner and odd-part methods) (`verify_17662_221465.log`).
- Earlier intermediate witnesses (148725, 212995) remain shipped; they are superseded.

## 5. Population profile of a = 594 [computer-assisted data; interpretation heuristic]

`profile_594.txt` lists, for each of the 351 window boundaries M_j, the exact number of alive prefixes at stage M_j; `profile_594_summary.txt` is a digest. The sum of all boundary populations is 13 566 171, which equals C's survivor count.

| boundary M (last below 2^k) | alive | mean-field 2^{s(M)−s(594)−1} | first boundary above 2^k | alive | mean-field |
|---|---|---|---|---|---|
| 3922 | 2466 | 4 | 4174 | 276 | 1 |
| 8010 | 13416 | 8 | 8262 | 814 | 0.5 |
| 16186 | 135974 | 32 | 16436 | 2561 | 0.5 |
| 32538 | 92882 | 32 | 32786 | 816 | 0.25 |
| 65490 | 381806 | 128 | 65738 | 3018 | 1 |

- **Peak.** The overall maximum is 392 640 alive prefixes at M = 63446.
- **End of the tree.** The last boundaries are M = 90010 with 3328 alive and M = 90262 with 16 alive. The drop comes after the stage passes 90112 = 2^16 + 2^14 + 2^13, where the binary digit sum falls from 15 (at 90111) to 3. The last alive stage is 90398, and every prefix dies at 90400 (v(90400) = 5).

[heuristic] Compare log2(alive) with the mean-field exponent W(M) = s(M) − s(594) − 1. The excess log2(alive) − W(M), averaged over the boundaries in each octave [2^k, 2^{k+1}), is:

| k | 10 | 11 | 12 | 13 | 14 | 15 | 16 (M ≤ 90262) |
|---|---|---|---|---|---|---|---|
| mean | 5.9 | 8.2 | 10.1 | 11.6 | 11.8 | 11.2 | 9.4 |
| range | 5.3–6.7 | 6.7–9.8 | 8.1–11.1 | 10.7–12.2 | 11.3–12.7 | 10.1–12.0 | 2.0–11.9 |

So the surviving tree follows the environment walk with a nearly constant excess of 10–12 bits from N ≈ 4000 to N ≈ 65000. The excess then collapses in the last octave, falling to 2 bits at M = 90262.

[heuristic] The profile shows the critical branching process of note §5 (H1) and Remark 10.8.2, with Kitamura's critical-branching picture:
- The population grows by a large factor between powers of two, roughly tracking the mean-field 2^{W}, and crashes by 1–2 orders of magnitude just after each 2^k.
- For natural a the environment walk is bounded below (W_N ≥ 1 − s(a)), so each crash is survivable with positive probability. The process nevertheless dies, here at a non-power-of-two dip (90112 has three ones in binary).

## 6. The survival law over natural numbers [heuristic]

Let c(G) = #{even a ≤ 32768 : g_2(a) ≥ G}, out of 16384 values. This uses g_2(594) = 89804, and g_2(17662) ≥ 131072, which suffices for G ≤ 131072.

| G | 64 | 128 | 256 | 512 | 1024 | 2048 | 4096 | 8192 | 16384 | 32768 | 65536 | 131072 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c(G) | 2077 | 1244 | 656 | 367 | 174 | 94 | 43 | 19 | 10 | 5 | 2 | 1 |
| G·c(G)/16384 | 8.1 | 9.7 | 10.3 | 11.5 | 10.9 | 11.8 | 10.8 | 9.5 | 10.0 | 10.0 | 8.0 | 8.0 |

(Source: the survey files of §4.1.)

- **A c/G law.** Over three decades, 256 ≤ G ≤ 131072, the product G·P(g_2(a) ≥ G) for even a stays between 8 and 12. This is numerically consistent with Kitamura's measured "≈ 11.5/G" (Kitamura does not state the normalisation; the figure comes from the class census), provided that figure refers to even a (or, equivalently, ≈ 5.7/G over all a).
- **Haar densities.** For G ≤ 256 the natural-number fractions also agree with the Haar Monte Carlo densities of note §5, once those are doubled for even a: 2077/16384 = 0.127 vs 2·0.0644; 1244/16384 = 0.076 vs 2·0.0379; 656/16384 = 0.040 vs 2·0.0208 (note §5 gives 0.0208 for δ_254, not δ_256).
- **Possible reconciliation.** This suggests a way to reconcile the "0.7/√G" and "11.5/G" fits that the note left open (Remark 10.8.4). The local decay exponent rises from about 0.5 at small G (note §5: from 0.58 to 0.88 at G = 254) to about 1 for G ≳ 256. The 0.7/√G fit describes the small-G regime only. This is a heuristic reading of finite data, not a theorem.
- **Expected counts.** Under this law, the expected number of even a ≤ 32768 with g ≥ 89804 is about 16384·10/89804 ≈ 1.8, and with g ≥ 131072 about 1.25. The observed 2 and 1 (594 and 17662) are typical, not anomalous.
- **A c/G law is no evidence for f = ∞.** If P(g ≥ G) ≍ 1/G, then each fixed a has g_2(a) < ∞ with "probability 1", but survivors to any depth G occur among about G even integers. Computation can therefore keep finding deeper survivors, as it did with 17662, without this saying anything about Conjecture 5.1. Conversely, the extinction of 594 is exactly what the law predicts.

## 7. Failed attempts and limitations

- **[failed attempt] BFS with deduplication (program A) for a = 594.** It is memory-bound and was stopped at N = 10596, as described in §3.1. Deduplication buys nothing here, because duplicates are essentially absent.
- **[limitation] Size of the factorial tables.** Program C caches all n! mod 2^K, about G²/16 bytes for G = K − v(a!). `dfsW3` halves this to about G²/32 bytes, which allows G ≈ 3.5·10^5 within 7 GB. Beyond that, one would need to recompute tables (an LRU cache over levels), or to store only every other N! and use multipliers below 2^57.
- **[limitation] Upper-bound certification at large K.** Program B keeps GMP tables of about G²/16 bytes. A death of 17662 at G ≈ 2.6·10^5 could therefore not be certified by B within 7 GB without first halving B's tables in the same way.
- **[limitation] No third exhaustive check of R3N.1.** A run of program A at K = 90395 would need about 4 GB and 2–3 h, so it was not done. The upper bound rests on programs B and C, tied together by the exact identity of Lemma 5. The lower bound rests on the explicit witness and two exact verifiers.

## 8. Open issues

1. **Human check.** The upper bound in R3N.1 is a computation. It is reproducible in about 3 minutes (C) or 17 minutes (B) on one core, and an independent re-run by the computational referee, ideally with a third implementation, would add confidence.
2. **Q1 at p = 2 for all a** is untouched. R3N.1 removes the natural number the note named as a live test case, but a = 17662 (§4.3) takes its place. The c/G law of §6 predicts [heuristic] that deeper survivors keep appearing, about one with g ≥ 10^5 per 10^4 even a, so the hunt for "champions" has no natural end.
3. **Rate statement.** The survival law of §6 is empirical. A proof of P_{a≤X}(g_2(a) ≥ G) ≪ 1/G^θ for natural numbers would be a quantitative form of Conjecture 5.1 for integers.

## 9. Recommended next steps

1. Fold R3N.1 and Cor. R3N.2 into the note (§2, §5, Remark 10.8.5, §10.6), replacing "a = 594 remains a live test case". Credit Kitamura for the case, the 66126 bound and the exact-value pipeline.
2. Have the computational referee re-run `dfsB 594 90395` and the two witness verifiers. All are short.
3. Extend the certified table to a ≤ 2^16. This costs about an hour of wall time per 16384 values with the current driver, which is dominated by process start-up and could be batched. The deep cases dominate the CPU.
4. Use the profile data to test the survival heuristic quantitatively. For example, check whether log(alive) follows the environment walk W_N = s(a+N) − s(a) between crashes, which would support a quantitative version of H1 for integers.

## Credits

- **P. Erdős and R. L. Graham** posed the problem.
- **S. Lin** proved f(2,2) = 254.
- **K. Kitamura** (`KitaKen1/erdos-404-p2-landscape`, July 2026) contributed:
  - the normal form g = f − v_2(a!) and the determinacy lemma;
  - the exact-value pipeline (exhaustive DP plus witness; our Lemma 2 is that pipeline written out);
  - the exact table for a ≤ 256 and the deeper rows 1102, 3456 and 8190, which we used for validation;
  - the shadow family;
  - the critical-branching picture with the ≈ 11.5/G survival law;
  - the identification of a = 594 as the live champion, with f(594,2) ≥ 66126.
- **Track D** (round 1) wrote `sumform_big.c`, whose sum normal form program A reuses.
- The halving lemmas and Cor. 3.7.1 are from note §3.4.
- **T. Tao**'s predicate and block notation (note §1.4) underlie Lemma 1.
