# Check of round-4 track M4D, lens "numerical falsification": Theorem W6 with Lemmas W1–W3, Proposition W4 and Corollary W5

Date: 2026-10-14. Job: `D_W6_falsify` (round 4). Adversarial verifier; I did not write the work under check.

**Claim under test** (`data/round4/reports/M4D.md` §3, headline item 2, table §0):
- **W1–W3, W4.** R3M's window martingale, one-window variance identity, fresh-randomness lemma and two-window inequality (note Props 11.10, 11.11, 11.13; R3M Cor A′, Prop B, Lemma C1, Prop C2) hold for arbitrary adapted probability weights on the window digit strings. M4D labels these [proved].
- **W6.** Theorem 11.14 (R3M Theorem C3) holds with ε_ℓ replaced by the weighted fine-scale mass. M4D labels it [proved; the hypothesis is unproved].
- **Cor W5.** The minimum over q of the fine-scale mass is the harmonic mean m(W;D′) of the missing-lift ratios. A complete coset gives exactly zero variance. M4D labels it [proved].

**Code, logs, budget.**
- **Code:** `code/round4/verify_D_W6_falsify/` (README there).
  - It was written from the definitions in M4D.md §3 and R3M.md §1–§5.
  - It shares no code with `code/round4/M4D/`, `code/round4/verify_M4D_logic/` or the interrupted `code/round4/verify_M4D_falsify/`. I read the last of these but did not use it.
- **Logs:** `data/round4/verify_D_W6_falsify/*.log`. Each run starts with its command line and start time and ends with its exit code and wall time.
- **Budget:** about 45 min of logged single-core wall time plus about 10 min of smoke tests.
  - All runs used `nice -n 10`, a 30-minute timeout and a 3 GB address-space limit, one at a time.

## 0. Headline

**Verdict: confirmed-with-fixes.** I found no counterexample to W1, W2, W3, W4, W5 or the finite-horizon content of W6, at p = 3, 5, 7. The fixes concern how the result is quoted, not any statement or proof.

- **What was tested.** 184 cylinders (p = 3: 83, p = 5: 57, p = 7: 44) and 253 chain runs on 30 admissible atoms.
  - In total there were about 591,000 checks of claims, every one passed, plus 82,000 control checks.
  - Every identity and every inequality between rationals was checked in exact rational arithmetic. Only three checks are in floating point: the per-frequency form of W3(b) (float64 FFT) and the literal complex-exponential forms of W2 and of the sharp ε^{q,q′}. Their exact summed or Parseval forms were also checked.
- **The tests can see an error.**
  - The single-parent cases attain W2, W3(b) and W4 with exact equality, as the proofs predict. This happened in 3,864 W4 cases, 1,288 W2 cases and 2,856 W3(b) cases, so any wrong constant would have shown up.
  - W5(b) holds with exact equality ε̃^{q*} = m(W;D′) in 184 of 184 cylinders.
  - The finite-horizon Paley–Zygmund bound of W6 is attained with equality in some chains.
  - Four negative controls, each a deliberately broken hypothesis or constant, fail as they should (§5).
- **No exact counterexample exists to report.**
- **Wording fixes.** These agree with fixes F1, F2 and F6 of the logic check `data/round4/checks/M4D_logic_W6.md`.
  1. **"The minimum over weights of the fine-scale mass is m(W;D′)" is true only for the q′-free mass ε̃^q.** In W6's predictable form the sharp mass ε^{q,q′} is used, and it is often strictly smaller.
     - With q = q* and q′ uniform over the residues of W′ mod p^{D′}, it was strictly below m in 11 of the 13 adversarial-run cylinders with m > 0.
     - In one of them (p = 5, m = 1) it was 0, because W′ covers ℤ/p^{D′}.
     - This does not contradict Cor W5(a), which is stated for ε̃^q. It does make the headline wording ("For every window, the minimum over weights of the fine-scale mass equals…") imprecise. It also slightly strengthens M4D's remark that the weighted FE is at most the uniform one.
  2. **"Exact balance / zero variance" is a property of the q*-weighted functional only.**
     - All 333 tested cases had a complete coset and D′ ≥ 1, with uniform or random q. In every one of them, M_{N′} was non-constant on some sub-cylinder C′.
     - With q* it was constant on every C′ in all 3,010 cases tested.
  3. **Scope.** Everything here, like W1–W6 themselves, is the slope-0 case (R3M Cor A′ with L = 0). The frozen-weight slope-≤L identity of Prop 11.10 was not reweighted by M4D, and I did not test it.
- **Two notes on the record.**
  - The logic check `M4D_logic_W6.md` still contains the unfilled placeholders `__HEADLINE__`, `__TESTS__` and `__RECORD__` (lines 21, 216, 247).
  - The interrupted earlier falsification run left `data/round4/verify_M4D_falsify/w1_validate.log` with two `RESULT FAIL` lines. They come from a comparison between that harness's own "engine" and its own brute force (`mismatchN2`). That harness's later log `w2_cyl.log` ends `RESULT OK`.
  - My brute-force populations are computed directly from S_{(e,f,f′)}(x′) and never use such an engine. Nothing in my runs reproduces a mismatch. I did not diagnose the old harness.

## 1. Method

### 1.1 Two independent sides

**Points.** Every x is a natural number, so a genuine point of ℤ_p that is not a negative integer. A cylinder is C = x + p^m ℤ_p with m = V_n(x), and its points are x′ = x0 + p^m w.

**Brute side** (`wf_core.Cyl`):
- All paths alive at n come from a pruned BFS on exact residues of S_e. This BFS is complete, because a prefix of an alive path is alive. It was checked against exhaustive enumeration of all 2^(n−1) paths in 90 random cases: 0 mismatches.
- At every point x′ with w ∈ ℤ/p^{Ken} (Ken = D + D′, or more for W3), I evaluate directly:
  - S_e(x′), S_{(e,f)}(x′) and S_{(e,f,f′)}(x′);
  - their derivatives modulo p;
  - the child targets −S/π_N.
  - Ken > D + D′ is used to test W3 at levels k > D′, when (5.1) allows it.
- This gives the weighted functionals M_N(x′) = p^{V_N} Σ w(e)q(f) and M_{N′}(x′) = p^{V_{N′}} Σ w(e)q(f)q′_{C′}(f′) **pointwise**.
- Nothing on this side uses Lemma 2, Prop B, Lemma C1 or any formula under test.

**Formula side:** the right-hand sides of the statements, computed from the window sums Q_f(x) and Q′_{f′}(x):
- μ^q_k, χ²_q, ε̃^q = p^{K}Coll_K − p^D Coll_D, F^q(ξ);
- ε^{q,q′}, from the composite sums Q_f + (π_N/π_n)Q′_{f′};
- m(W;D′) and q*.

**Exactness and locality.**
- Weights are integer vectors, and every expectation over C is an exact rational.
- Locality was checked: for sampled w, a second lift w + p^{Ken}r gives an identical alive structure (184/184).

### 1.2 Samplers (edge cases included)

- **rand:** x uniform modulo p^40.
- **gate_hist:** a gate v(x+i) = s ∈ {2,3,4} at a random i ≤ n.
- **gate_win:** a gate inside W or W′. This is possible only at p = 3, 5, because at p = 7 it breaks (5.2).
- **tight:** D + D′ = m − M_{N′} exactly.
- **D0** (D = 0) and **D20** (D′ = 0). The second gives trivially complete classes.
- **near2:** x ≡ −2 mod p^s. At p = 3 and p = 5, 3,000 tries each never gave a nonempty slope-0 population. This is consistent with the double root of S_{1,2} = (x+2)², so this sampler contributed no cylinders.

### 1.3 Weights

- **Parent weights w:** all ones; random integers 0–50 with about 20% zeros; a single parent; all parents of one β-class mod p^{D′}; all zero.
- **q on W:** uniform; random; sparse (3 words); a point mass; q* of Cor W5; uniform over the residues of Σ mod p^K; all mass on one class mod p^D.
- **q′ on W′, constant on C:** uniform; random; a point mass; uniform over residues mod p^{D′}.
- **q′ varying with the sub-cylinder C′:**
  - random;
  - random point masses;
  - **adversarial:** for each C′, the point mass that maximises Var_{C′}(M_{N′}), chosen by exact comparison. Var_{C′} is a convex quadratic in q′, so this is the worst adapted q′.
- **Adversarial search** (`t_adv.py`): exact-objective hill climbing over w, q and q′ (§4).

### 1.4 Configurations (p, n, H, H′)

| p | configurations |
|---|---|
| 3 | (20,5,4), (26,6,5), (30,6,6); edges (21,2,4) and (22,5,2) |
| 5 | (20,5,5), (25,5,5); edges (20,3,5) and (20,5,3) |
| 7 | (21,7,7), (28,7,7); edges (21,3,7) and (21,7,3) |

At p = 7, and in the p = 5 n = 25 and p = 3 n = 30 runs, 20–60 random slope-0 parents are followed (the others get weight 0, which the lemmas allow). The W1(a) slope checks then run on those lines. A separate p = 7 run (`full`) evaluates the children of **all** parents at every point.

## 2. Results on cylinders (W1–W5)

Totals over all completed `t_cyl` runs, from `aggregate.py`. The core checks are listed below; all have 0 failures.

| statement | what is compared | checks (p=3 / 5 / 7) | failures |
|---|---|---|---|
| **W1(a)** | children of slope-0 parents are slope 0; children of slope>0 parents are not; grandchildren have slope 0 iff the line does | 184 cylinders, every point, every parent or line | 0 |
| Lemma 2(a) | parents' aliveness and slope constant on C; BFS at sampled x′ gives the same alive set | 184 + 184 | 0 |
| **W1(b)** | E_C[M_N] = M_n exactly | 17,862 / 13,065 / 5,270 | 0 |
| W1 on each C′ (W4 step 1) | E_{C′}[M_{N′}] = M_N(C′), and M_N constant on C′ | 36,197 + 36,197 | 0 |
| **W2** pointwise | brute M_N(x′) = p^{V_N} Σ_e w(e) μ^q_D(τ⁰_e − β_e w) | 5,150 | 0 |
| **W2** identity | Var_C(M_N) = p^{2m} Σ_{η≠0} \|A(η)\|², in its exact Parseval form | 5,150 | 0 |
| W2 literal | the complex-exponential A(η) as written, float64, rel. tol. 10⁻⁹ | 1,015 | 0 |
| **W2** bound | Var ≤ M_n² χ²_q; **equality** for a single weighted parent | 5,150; equality 1,288/1,288 | 0 |
| **W3(a)** | E_C Ψ(ξ) = 0 for all ξ ≢ 0: the weighted child mass per target class mod p^k is flat in the class (exact), at every k ≤ k3 | 9,677 | 0 |
| W3, F^q | Σ_{ξ≠0} F^q(ξ) = ε̃^q at level (D,k) | 9,677 | 0 |
| **W3(b)** summed | Σ_{ξ≠0} E\|p^{V_N}Ψ\|² ≤ (p^m W)² Σ F^q, exact; **equality** for a single parent | 9,677; equality 2,856/2,856 | 0 |
| **W3(b)** per ξ | E\|p^{V_N}Ψ(ξ)\|² ≤ (p^m W)² F^q(ξ) with ζ ≡ ξu⁻¹, float64 FFT, rel. tol. 10⁻⁹ | 199,420 / 53,452 / 5,766 | 0 |
| **W4** adapted | E_C M_{N′}² − E_C M_N² ≤ ε̃^q M_n², with q′ constant, varying, or adversarial per C′ | 17,794 / 13,020 / 5,236 | 0 |
| W4 equality case | single parent and point-mass q′ (any, varying with C′): LHS = ε̃^q M_n² **exactly** | 3,864/3,864 | 0 |
| **W4** sharp | LHS ≤ ε^{q,q′} M_n², with q′ constant on C | 20,600 | 0 |
| W4 identification | ε^{q,q′} (composite-collision form) = Σ_{ξ≠0}\|μ̂^{q′}(ξ)\|² F^q(ξ) (float); and ε^{q,q′} ≤ ε̃^q (exact) | 2,479; 20,600 | 0 |
| **W5** | m(W;D′) = 0 iff some class is complete | 184 | 0 |
| **W5(a)** | ε̃^q ≥ m for the 7 named q, all 2^H point masses, 10 random, 10 perturbed q*, 3 gradient-descent minimisers per cylinder | 14,396 | 0 |
| **W5(b)** | ε̃^{q*} = m(W;D′), exactly | 184/184 | 0 |
| **W5(c)** | complete coset and q = q*: M_{N′} constant on **every** C′ and LHS = 0, for every parent weight and every q′ (including varying and adversarial q′) | 3,010 + 3,010 | 0 |

**Ratios.** For W2 (Var/bound), W3(b) (summed and per ξ) and W4 (adapted and sharp), the largest ratio LHS/RHS is exactly 1 at each prime. It is attained only in the single-parent equality cases.

**Gradient descent.** The projected-gradient minimiser of ε̃^q over the simplex never went below m. Its smallest ratio ε̃/m was 1.0000 (rounding of the minimiser to 10⁻⁹-integer weights). Where m = 0, it reached ε̃ = 0 exactly in 40 cylinders.

**Complete cosets.** These are common: 86 of the 184 cylinders had a complete class. 37 of them have D′ = 0, which is trivial. The other 49 have D′ = 1, at all three primes. So W5(c) was exercised well beyond the trivial case.

## 3. Theorem W6 at finite horizon (`t_chain.py`)

**Setting.**
- Deterministic times n_ℓ = n_0 + ℓH for ℓ = 0..L+2, with L = 3 windows after j = 0.
- p = 3: (n_0, H) = (24, 5) and (20, 5). p = 5: (25, 5). p = 7: (35, 7).
- An admissible atom A of G_0 is drawn at random or with a history gate.
- **Every** G_ℓ-atom below A is enumerated exactly while the process is not stopped. A stopped atom keeps its frozen value M̃ = M_{min(ℓ,τ)}.
- Populations are recomputed by brute force at a representative of each atom.

**Schedules.**
- U: uniform, predictable.
- R: random, adapted.
- RP: random, predictable.
- S: q* of Cor W5 for (W_ℓ; D_{ℓ+1}) on the regime event, uniform off it. This is the schedule of Remark 2 with fix F4.
- P: random point masses, adapted.
- M: mixtures, adapted.

**Stopping thresholds ε̄.** ε̄ = ∞; the median or lower quartile of ε̃_ℓ over active atoms; and 0. Both w_0 ≡ 1 (W6 as stated) and single-parent starts were used.

**Size.** 253 runs (atom × schedule × ε̄), with about 372,000 atoms visited in total.

| check (W6 proof step it tests) | checks | failures |
|---|---|---|
| weighted martingale E[M_{ℓ+1} \| G_ℓ] = M_ℓ on every non-stopped atom (W1) | 20,579 | 0 |
| first window E_A[M̃_1²] ≤ M_0²(1 + χ²_{q_0}(A)) (W2) | 253 | 0 |
| per G_{ℓ−1}-atom C ⊂ {τ > ℓ}: E_C[M_{ℓ+1}² − M_ℓ²] ≤ ε̃_ℓ M_{ℓ−1}(C)² (W4) | 1,950 | 0 |
| … ≤ ε̄_ℓ M_{ℓ−1}(C)² | 1,454 | 0 |
| predictable schedules: … ≤ ε^{q_{ℓ−1},q_ℓ} M_{ℓ−1}(C)² (sharp W4); q_ℓ constant on the G_{ℓ−1}-atom; ε ≤ ε̃ | 638 × 3 | 0 |
| single weighted path at C with point-mass q_ℓ: **equality** LHS = ε̃_ℓ M_{ℓ−1}² | 89/89 | 0 |
| recursion a_{ℓ+1} − a_ℓ ≤ ε̄_ℓ a_{ℓ−1}; a_{ℓ+1} ≤ M_0² Π_{A,ℓ}; a_ℓ nondecreasing | 338 + 338 + 253 | 0 |
| Paley–Zygmund steps: E[Y_L²] ≤ M_0²Π and E[Y_L] ≥ M_0(1 − √(Πδ)), with Y_L = 1_{τ>L} M̃_L | 161 + 161 | 0 |
| **conclusion** μ_A(Y_L > 0) ≥ (1 − √(Πδ))²/Π, where Πδ < 1 | 102 | 0 |
| Remark 2: under the q* schedule ε̃_ℓ = m(W_{ℓ−1};D_ℓ) | 410 | 0 |
| Remark 2 / W5(c): m = 0 ⇒ M_{ℓ+1} = M_ℓ on every G_ℓ-atom (occurs at p = 5, 7) | 136 | 0 |
| measurability: regime R_{ℓ+1}, q*, and ε̃_{ℓ+1} recomputed at a second representative of the G_ℓ-atom agree (so τ is predictable) | 184 + 184 + 916 | 0 |
| measurability and W1(a): the weighted population at a second representative equals the full P⁰_{n_ℓ} (independent BFS), or each weighted path is alive with slope 0 there (exact big integers); survival M_ℓ > 0 ⇒ an alive path (BFS) | 559 + 776 + 559 | 0 |

The finite-horizon Paley–Zygmund bound is attained with **equality** in some runs. Examples are μ_A(Y_L>0) = 0.8 = 1/Π with Π = 1.25, δ = 0 (p = 5), and μ_A(Y_L>0) = 1 = 1/Π with Π = 1 (p = 7). These cases are two-valued M̃_L.

In the 4 runs with δ > 0 and Πδ < 1, the bound held with room, for example 0.571 ≥ 0.0071 at p = 7.

The per-atom ratio LHS/(ε̃M²) has a median between 10⁻⁴ and 10⁻² in the runs with many weighted parents (w_0 ≡ 1 or 6 parents). In the single-parent runs the median is 0.0145, 0.67 and 1. The maximum is exactly 1, attained in the single-path equality cases.

**C3's hypotheses after the substitution.** I checked the following against R3M's proof of Theorem C3:
- W6 keeps R3M's times n_0 ≥ 2p, the partitions G_ℓ, the admissible atom and the linear-regime part of B_ℓ.
- It replaces Cor A′, Prop B and Prop C2 by W1, W2 and W4, and ε_ℓ by ε̃_ℓ (or by the sharp ε_ℓ for predictable schedules).

Each replaced step was tested above on exact atoms. The stopping time stayed predictable: ε̃_{ℓ+1} and the regime were constant on G_ℓ-atoms in every sample. So the hypotheses that C3's proof uses are met exactly in all tested instances.

## 4. Adversarial search (`t_adv.py`)

**Method.** Hill climbing with an exact rational objective, starting from 2–3 weighted parents and moving the parent weights, q and q′. Configurations: 16 cylinders × 4 objectives at p = 3, 5, 7, with 100–250 steps each.

**Best values found:**

| objective (must be ≤ 1) | p = 3 | p = 5 | p = 7 |
|---|---|---|---|
| Var_C(M_N) / (M_n² χ²_q) | 1.0000 to 8 digits (6 parents) | 1.0000 to 8 digits (6 parents) | 0.865 |
| W4 adapted, with q′ the worst per C′ | 0.874 | 0.928 | 0.919 |
| W4 sharp | 0.795 | 0.971 | 0.902 |
| m(W;D′) / ε̃^q | 0.919 | 0.956 | 0 (m = 0) |

Violations: 0; no value exceeded 1 in exact arithmetic.
- For W2, values within 10⁻⁸ of 1 with 6 weighted parents are consistent with Prop N's equality case (all β_e and all τ⁰_e equal mod p^D). I did not inspect those parents individually.
- For W4 (both forms) and for W5, the search stayed at or below 0.971.

**Sharp mass against m.** In 11 of the 13 cylinders with m > 0, ε^{q*, q′_res} < m(W;D′). In one of them (p = 5, W′ covering ℤ/p^{D′}) it was 0 while m = 1. This is wording fix 1 of §0.

## 5. Negative controls: the tests have power

All four controls fail as they should. The fourth set, the complete-coset control, behaves as predicted.

- **NC1 (W1 needs q fixed on C).** q is made to vary with C′ inside C. E_C[M_N] = M_n fails in 147/147 cylinders.
- **NC2 (the sharp W4 needs q′ constant on C).** q′ varies with C′, but ε^{q,q′(C′_0)} is used in place of ε̃. The bound fails in 397 of 15,450 cases, mostly single-parent ones.
- **NC3 (the unit in F^q).** ζ ≡ ξu is used instead of ξu⁻¹. W3(b) per ξ fails in 9,026 of 65,596 cases. The test cannot see this at p = 3, k = 1, where u ≡ ±1.
- **NC4 (constant in W4).** ε̃ is taken at level K−1, dropping the top shell. The single-parent equality case then fails in 147/147.
- **Complete coset with q ≠ q*.** M_{N′} is non-constant on some C′ in 333/333 cases with D′ ≥ 1. With D′ = 0 it is trivially constant (345 cases).

## 6. What numerics cannot test

- **The infinite-horizon steps of W6:** Doob's L² convergence, the limit Y = 1_{τ=∞}M̃_∞, and "M_ℓ > 0 for all ℓ ⇒ x ∈ K_p" (König; F1/F2).
  - I tested the finite-horizon analogue exactly, including the Paley–Zygmund conclusion with δ_L = μ_A(τ ≤ L).
  - I also tested the finite ingredients: prefix aliveness and survival by BFS.
  - The limit steps are standard and were checked by the logic check (§2.6 there).
- **The hypothesis of W6 (weighted FE).** It is unproved and not claimed. Nothing here bears on whether it holds, so W6 by itself proves nothing about μ(K_p).
- **Larger parameters.** Windows were limited to lengths H ≤ 7, three windows after j, and enumerations of up to 3^9 points. Per-ξ statements were tested in float64 at relative tolerance 10⁻⁹; their exact summed versions hold exactly.

## 7. Computational record

| log | runs (args) | result | wall |
|---|---|---|---|
| `cyl_p3.log` | `t_cyl.py 3 20 5 4 101 40 …` | 32 cylinders, OK | 683 s |
| | `t_cyl.py 3 26 6 5 102 15 …near2…` | **stopped by hand** after about 10 min (no exit line): near2 never yields a population at p = 3 and only used up attempts | — |
| | `t_cyl.py 3 30 6 6 103 6 … - 2 12` | **exit 1**: exceeded the 3 GB address-space limit while storing a 3^10-point enumeration (resource, not a test failure) | 202 s |
| | `t_cyl.py 3 26 6 5 102 15 … - 1 20` (batch3) | **exit 1**: hit my own int64 guard `p^R < 2^56` in `alive_all` for a cylinder with a deep gate (resource, not a test failure) | 214 s |
| | `t_cyl.py 3 30 6 6 103 6 … 40 1 12` (batch3) | **exit 1**: out of memory in the per-ξ FFT (3^10 × 3^6 table) | 48 s |
| | the two runs above again, with resource guards (batch4) | 15 cylinders (1 skipped by the guard), OK; 6 cylinders (52 W3 levels skipped as too large), OK | 235 s, 53 s |
| `cyl_p3_edge.log` | D = 0 (n=21, H=2) and D′ = 0 (n=22, H′=2) | 15 + 15 cylinders, OK | 13 s, 6 s |
| `cyl_p5.log` | (20,5,5) and (25,5,5) | 24 + 9 cylinders, OK | 72 s, 21 s |
| `cyl_p5_edge.log` | D = 0 and D′ = 0 | 12 + 12, OK | 32 s, 15 s |
| `cyl_p7.log` | (21,7,7), (28,7,7), (21,7,7) `full` | 16 + 4 + 4, OK | 27 s, 39 s, 4 s |
| `cyl_p7_edge.log` | D = 0 and D′ = 0 | 10 + 10, OK | 1 s, 2 s |
| `chain_p3.log` | 3 runs, 15 atoms, 145 chain runs | OK | 80 s, 4 s, 8 s |
| `chain_p5.log` | 2 runs, 7 atoms, 60 chain runs | OK | 112 s, 1 s |
| `chain_p7.log` | 2 runs, 8 atoms, 48 chain runs | OK | 79 s, 2 s |
| `adv.log` | 4 runs, 16 cylinders | 0 violations | 117 s total |

**Batches.** `batch.sh`, then `batch3.sh`, then `batch2.sh`, then `batch4.sh`. The resource guards were added to `t_cyl.py` and `wf_core.py` between batches. They only skip cylinders or W3 levels, and they report what they skip. They change no test.

**Reproduce.**
- For example, `./run.sh LOG python3 t_cyl.py 5 20 5 5 201 30 rand,gate_hist,gate_win,near2,tight - 1`.
- Then run `python3 aggregate.py ../../../data/round4/verify_D_W6_falsify` to get the totals in §2–§3.

## 8. Credit

- **Weighted machinery, Cor W5, Thm W6:** track M4D (round 4).
- **Unweighted machinery** (Lemma 2, Prop A/Cor A′, Prop B, Lemma C1, Prop C2, Theorem C3, Prop N): track R3M (round 3).
- **Complete-coset (fullness) condition:** track R2b (round 2), note Theorem 10.12.
- **Logic check of the same claim**, whose fixes F1, F2 and F6 the numerics here support: `data/round4/checks/M4D_logic_W6.md`.
- **Classical:** Parseval, Cauchy–Schwarz, Minkowski, the Paley–Zygmund inequality.

*This report was produced in an AI-assisted session (round 4, job D_W6_falsify). It has not been checked by a human.*
