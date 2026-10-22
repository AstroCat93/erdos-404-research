# Check of round-4 track M4D, lens "numerical falsification": Lemma L, Theorem F, Corollary F1

Date: 2026-10-14. Track: `verify_M4D_falsify` (round 4).

**Claim under test** (data/round4/reports/M4D.md §1–2; status [proved]):
- **Lemma L.** The children's targets modulo p^{D′} are a bijective affine image of the parent's fibre lifts Lift(r) = {s ∈ Σ mod p^{D+D′} : s ≡ r mod p^D}.
- **Theorem F (θ-lifting).** Let G_ℓ = {r : |Lift_ℓ(r)| ≥ θ_{ℓ+1} p^{D_{ℓ+1}}}. Suppose (I) T_j meets G_j, and (II_ℓ) |G_ℓ| > (1−θ_ℓ) p^{D_ℓ} holds for every ℓ > j. Then x ∈ K_p.
  - Minimal θ gives Tao's block lemma.
  - θ = 1 gives R2b's fullness propagation (note Theorem 10.12).
- **Corollary F1.** μ(K_p ∩ A) ≥ μ(A ∩ I_j) − Σ_{ℓ>j} μ(A ∖ L_ℓ).
  - So μ(K_p) > 0 holds whenever the failure probabilities sum to less than μ(A ∩ I_j). That condition is hypothesis LIFT, which is not proved.

**Code, logs and budget.**
- **Code:** `code/round4/verify_M4D_falsify/` (README there). It was written from the definitions and shares no code with `code/round4/M4D/` or `code/round4/verify_M4D_logic/`.
- **Logs:** `data/round4/verify_M4D_falsify/t{1..5}_*.log`. Each run starts with its command line and start time and ends with its exit code and wall time.
- **Budget:** about 20 min of logged single-core wall time plus about 5 min of unlogged smoke tests. All runs used `nice -n 10`, one at a time. Peak memory was well below 1 GB.

## 0. Headline

**Verdict: confirmed. No counterexample was found, and the status labels are right.**
- Every step of the chain was tested in exact integer and rational arithmetic, at p = 3, 5, 7 and 11. The steps are (F1), the deletion step, (F2) with its converse and target formula, Lemma L, Theorem F, the two special cases, and Corollary F1.
- Test points include random x, x near −1 and −2, x within p^12 of small negative integers, gates at every position relative to the windows, and high-slope parents.
- **Lemma L:** 0 failures in 82,695 + 5,626 parents. Their child sets were found by brute force over all 2^H digit words, about 2.4·10^6 alive children in all.
- **Theorem F:** 0 failures at finite horizon over 44,945 θ-sequences. This is exhaustive over every θ ∈ (0,1]^L for 1,656 window chains. The hypotheses held in 8,797 cases, and the conclusion |T_ℓ| ≥ θ_ℓ p^{D_ℓ} was attained with equality 3,371 times, so the bound is sharp and an off-by-one would have shown.
- **Corollary F1:** 0 failures pointwise on all 179,413 determined cylinders of 20 exhaustive Haar enumerations. This covers 87,571 (cylinder, θ-schedule) pairs where the hypotheses held. In every run the integrated inequality holds in exact rationals on the determined mass. With the undetermined mass U (≤ 0.037) counted against it, it still holds except in the INCONCLUSIVE(U) lines of §1.4. In those lines the margin on the determined mass is non-negative but smaller than U.

What numerics cannot test:
- the passage from "alive at every n_ℓ" to x ∈ K_p, which needs infinitely many windows;
- the union bound over infinitely many windows in Corollary F1.

Both are elementary: (F1) and (F2) plus König's lemma (note Prop 1.2), and countable subadditivity. I tested every finite ingredient: V_n ≥ v_p(n!), the deletion step, prefix-aliveness, and locality, which is what makes the events Borel. The logic itself is the subject of the separate logic check (`data/round4/checks/M4D_logic.md`).

Two presentational remarks follow. Neither is an error in M4D.md.
1. "θ = 1 recovers R2b's Theorem 10.12" holds only in a narrower sense. It is the chained direction (ii)⇒(i), in the case where the incoming fullness modulus equals the window's jump (D = δ in Theorem 10.12's notation). M4D.md §2 itself says exactly this ("the chained form of its implication (ii)⇒(i)"). The one-line summary of the claim is looser.
2. Theorem F needs x not to be a negative integer, since otherwise targets are undefined. M4D.md §1 states this; the one-line claim omits it. The excluded set is null, so Corollary F1 is unaffected.

## 1. What was tested, and how

Conventions:
- **x.** Every x is a natural number. These are genuine points of ℤ_p, so all polynomials are evaluated exactly: S_e(x), π_n(x) and the window elements y_i = ∏_{s≤i}(x+n+s) are exact integers. I reduce modulo p^k only at the end.
- **Edge cases.** Near −m, x = u·p^s − m (u a unit), which forces v(x+m) = s exactly.
- **Alive paths.** These are computed three independent ways, which agree:
  1. brute force over all 2^{n−1} paths;
  2. pruned DFS on exact S_e;
  3. the carry recursion τ_{m+1} = (τ_m − e_m)/(x+m+1), which is alive iff v(τ_m − e_m) ≥ v(x+m+1). It carries the targets modulo p^{V_top − V_m}.
- **Window sums Σ.** These are kept as numpy boolean bitsets modulo p^K, built by rotate-or from the exact y_i. In t5 they are cross-checked against Python sets (1,099 windows, 0 mismatches).

### 1.1 Standing facts (t1_basics, 7 runs, p = 3, 5, 7, 11)

| check | what | checks | failures |
|---|---|---|---|
| F1a | V_n(x) ≥ v_p(n!) | 45,600 | 0 |
| DEL | v(S_B) ≥ V_n ⇒ v(S_{B∩[1,n)}) ≥ V_n, over **all** B ⊆ [1, n+h) | 262,986 | 0 |
| DFS | pruned DFS = brute force over all 2^{n−1} paths | 2,280 | 0 |
| DP | carry-recursion target sets = targets of DFS paths | 9,120 | 0 |
| F2conv | (e,f) alive at N ⇒ e alive at n, over **all** parents e, alive or not | 132,925 | 0 |
| F2iff | e alive: (e,f) alive at N ⇔ Q_f ≡ τ mod p^D | 1,607,776 | 0 |
| F2tau | τ_N((e,f)) = u^{−1}(τ − Q_f)/p^D mod p^k | 132,925 | 0 |
| LOC | V's, T_ℓ mod p^{D_ℓ} and Σ_ℓ mod p^{D_ℓ+D_{ℓ+1}} agree at a, at a + t·p^k and at x, whenever k ≥ V_N and k > M_N | 2,280 | 0 |

LOC is the locality fact behind "the events are countable unions of cylinders, hence Borel" (Cor F1), and behind the exhaustive enumeration of §1.4.

### 1.2 Lemma L (t2_lemmaL: 5 runs, p = 3, 5, 7, 11, H ≤ 15; t5_deep_highslope: 4 runs)

For each window pair W = [n, N), W′ = [N, N′) and each alive parent e:
1. I computed C(e) = {τ_N((e,f)) mod p^{D′} : (e,f) alive at N} by **brute force**. That means all 2^H words f, aliveness from the definition p^{V_N} | S_e + Σ_i f_i π_{n+i}, and the target from −S/π_N. Neither Q_f, nor u, nor (F2) is used.
2. Separately, I computed λ(Lift(r)) from the bitset Σ mod p^K and the unit u = π_N/(p^D π_n).

| | t2 (random, near −1, −2, −m; gates at start, middle or end of W and of W′) | t5 (v(x+m) = 6, 9, 12; windows before, straddling, after, or starting at m) |
|---|---|---|
| parents tested | 82,695 (13,932 with complete lift; 40,363 childless) | 5,426, plus 200 cube-path parents |
| alive children found by brute force | 2,395,714 | — |
| windows outside R3M's linear regime | 6,748 of 7,398 | all (moduli up to p^18) |
| parents of slope v(S_e′) ≥ 2 | 17,790 (5,209 at p = 7) | 200 cube-path parents, slope 2s (2s+1 at p = 3) |
| windows with D = 0 / D′ = 0 / D or D′ ≥ 3 | 1,400 / 1,457 / 4,523 | — |
| **failures**: λ(Lift(r)) ≠ C(e); λ not injective; \|C(e)\| ≠ \|Lift(r)\|; "C(e) = ℤ/p^{D′} ⇔ r complete"; lift-count helper | **0** | **0** |

- **Cube path.** At x = u·p^s − 2 the parent (1,1,0,1,0,…,0) has S_e = (x+2)^3 exactly (checked). Its slope is v(3(x+2)^2) = 2s, or 2s+1 at p = 3. Lemma L held for it in all 200 cases.
- **Negative controls.** Both show the test can fail.
  - Unit 2u in place of u: λ ≠ C(e) for 28,083 of 35,166 eligible parents. The rest are parents with complete lift or a symmetric image.
  - Divisor p^{D+1} in place of p^D: λ ≠ C(e) for 23,656 of 23,736.
- **No regime needed.** Lemma L uses no slope or linear-regime condition. Accordingly, almost all tested windows lie outside R3M's regime D + D′ ≤ V_n − M_{N′}, and the lemma held there.

### 1.3 Theorem F, finite horizon (t3_thmF: 6 runs, p = 3, 5, 7, 11)

**Why the θ-enumeration is exhaustive.**
- Take a chain n_0 < ⋯ < n_{L+1}, with L+1 = 3 to 5 windows of length 3 to 16, and a start j. Then θ_ℓ enters only through two places: G_{ℓ−1} = {r : |Lift_{ℓ−1}(r)| ≥ θ_ℓ p^{D_ℓ}}, and the terms (1−θ_ℓ)p^{D_ℓ} and θ_ℓ p^{D_ℓ}.
- On each interval of θ_ℓ where G_{ℓ−1} is constant, the largest θ_ℓ makes (II_ℓ) easiest and the conclusion hardest. That largest value is θ_ℓ = c/p^{D_ℓ}, with c one of the distinct positive lift counts of W_{ℓ−1}.
- So a counterexample with any θ ∈ (0,1]^{L−j} yields one at these critical values. I enumerated **all** critical combinations. The code would fall back to 6,000 random ones if there were more, but that never happened (log: no "sampled" line), so the enumeration was complete in every case. 14 chains of the long-window p = 7 run were skipped because a modulus exceeded 2·10^7.
- To validate this integer reformulation, I also re-evaluated the literal statement with `Fraction` θ's: random critical values, and random non-critical θ ∈ (0,1].

**Independence.** T_ℓ comes from the carry-recursion DP (independent of Lemma L), cross-checked against exact DFS 3,191 times with 0 mismatches. The lift counts come from bitsets of the exact y_i.

| quantity | total over 6 runs |
|---|---|
| chains / θ-sequences evaluated | 1,656 / 44,945 |
| θ-sequences with (I) and all (II_ℓ) true | 8,797 (plus 13,833 literal-`Fraction` cases) |
| conclusion instances \|T_ℓ\| ≥ θ_ℓ p^{D_ℓ}, of which with equality | 16,646, of which 3,371 |
| (chain, j) where some θ works / only an intermediate θ works (neither θ = p^{−D} nor θ = 1) | 1,728 / 321 |
| **failures of Theorem F** (critical and literal) | **0** |

**Special cases and side statements** (0 failures each):
- Tao (θ_ℓ = p^{−D_ℓ}): (II_ℓ) ⇔ W_ℓ covers ℤ/p^{D_ℓ}. Checked on every window pair, together with the block lemma itself (T_ℓ ≠ ∅ and W_ℓ covers ⇒ T_{ℓ+1} ≠ ∅; 1,186 instances).
- θ = 1:
  - T_ℓ full and a complete class exists ⇒ T_{ℓ+1} full (550 instances);
  - R2b's Theorem 10.12 (ii)⇒(i) on random full carry sets;
  - (i)⇒(ii) through the proof's construction (if no class is complete, one lift per class outside Σ misses target 0). 4,555 window pairs.
- Prop F2(a): (1−θ_ℓ)θ_{ℓ+1}p^{D_ℓ+D_{ℓ+1}} < 2^{H_ℓ} and θ_{ℓ+1}p^{D_{ℓ+1}} ≤ 2^{H_ℓ}, whenever the hypotheses hold.
- F2(b), key step: a gate of depth s at distance d into W_ℓ gives |Σ_ℓ mod p^s| ≤ 2^d (199 forced gates). When p^s > 2^d + 2^{H_{ℓ−1}}, no θ-sequence satisfies the hypotheses for any j ≤ ℓ−1 (2,735 θ-sequences).

**Negative controls.**
- Dropping (I) produces conclusion failures (6,316).
- Index slip, i.e. G_ℓ defined with θ_ℓ in place of θ_{ℓ+1}, also produces failures (140).
- Replacing ">" by "≥" in (II_ℓ) produced **no** failure in this sample. The borderline case |T_ℓ| + |G_ℓ| = p^{D_ℓ} with T_ℓ ∩ G_ℓ = ∅ never occurred, so strictness was not stressed numerically. It is needed logically (pigeonhole) and is used correctly in the proof.

### 1.4 Corollary F1 by exhaustive Haar enumeration (t4_corF1: 20 runs)

**Method.**
- Take a base set B: either ℤ_p, or a cylinder x_0 + p^m ℤ_p. Partition it into cylinders a + p^k ℤ_p, with a natural.
- Refine each cylinder until it determines every quantity, that is k > M_{n_{L+1}}(a) and k ≥ V_{n_{L+1}}(a) (locality, §1.1 LOC).
- Mass still undetermined at the cap k_cap is counted as unknown, U, and always against the inequality.
- θ-schedules: θ_ℓ = p^{−D_ℓ(x)} (x-dependent), and the constants 1/7, 1/3, 1/2, 2/3, 6/7, 1.

**What is checked.**
- *Pointwise* (the finite-horizon Theorem F, which with the union bound is Cor F1): on every determined cylinder, I_0 ∧ L_1 ∧ ⋯ ∧ L_{L−1} ⇒ |T_L| ≥ θ_L p^{D_L} ⇒ alive at n_L.
- *Integrated*, in exact rationals: μ_B(A ∩ alive at n_L) ≥ μ_B(A ∩ I_0) − Σ_{ℓ=1}^{L−1} μ_B(A ∖ L_ℓ), for A = B and for each class of B mod p^{m+1}.

**Totals.** 179,413 determined cylinders; 87,571 (cylinder, schedule) pairs with the hypotheses true. **0 pointwise failures; 0 integrated failures.**
- 149 (run, schedule, A) lines are marked INCONCLUSIVE(U). There the inequality holds on the determined mass, but the margin is smaller than U, so counting U adversely leaves it open. All of them lie in one of three places:
  - the two x ≡ −2 cylinders (θ ≥ 2/3), where both sides equal 0.997 on the determined mass;
  - the six dead-class cylinders;
  - single classes A with zero alive mass (A = class −1 of ℤ_7; three classes of 113 + 5^3).

  None has determined LHS < determined RHS.

| p | B | chain n_ℓ | U | μ_B(alive at n_L) | Cor F1 right-hand side, by schedule |
|---|---|---|---|---|---|
| 3 | ℤ_3 | 3, 6, 9, 12, 15 | 0.018 | 0.4033 | all < 0 (vacuous) |
| 3 | ℤ_3 | 4, 8, 12, 16 | 0.037 | 0.4033 | all < 0 |
| 5 | ℤ_5 | 5, 10, …, 25 | 0.008 | 0.5203 | all < 0 |
| 7 | ℤ_7 | 7, 14, 21, 28 | 0.0017 | **0.6235** | 0.029 to 0.187, all ≤ LHS |
| 7 | ℤ_7 | 7, 15, 23, 31 | 0.0072 | **0.6223** | 0.033 to 0.223, all ≤ LHS |
| 7 | 492 + 7^4 ℤ_7 | 14, 26, 38, 50 | 0 | 1 | 1 for θ ≤ 6/7 (certified on all of B); 0 for θ = 1 |
| 7 | 47 + 7^2 ℤ_7 and 341 + 7^3 ℤ_7 (x ≡ −2) | 7, 14, 21, 28 | 0.003 | 0.9971 | 0.997 for θ ≥ 2/3; 0 for θ ≤ 1/2 and for θ = p^{−D} |
| 7 | 30 + 7^2, 324 + 7^3 (v(x+19) ≥ 2 or 3: gate at the start of W_1) | 11, 18, 25, 32 | 0.003 | 0.989, 0.927 | ≤ 0: criterion certifies nothing |
| 7 | 22 + 7^2, 23 + 7^2 (v(x+27) ≥ 2, resp. v(x+26) ≥ 2: gate 2–3 steps into W_2) | 11, 18, 25, 32 / 9, 16, 23, 30 | 0.003 | 0.997 | ≤ 0 |
| 5 | 13 + 5^2, 113 + 5^3 (gate at the start of W_1) | 6, 11, …, 26 | 0.008 | 0.84, 0.20 | ≤ 0 |

Six further runs fall in classes where nothing is alive (g_p ≡ 0): x ≡ −1 or −3 mod 7, and x ≡ −1 mod 5. They pass trivially and are flagged in the log as uninformative; this was my own choice of base points, not an effect of M4D's claims.

Readings. These are consistent with M4D's own statements, not defects.
- **p = 7.** μ(alive at 28) = 0.6235 ± 0.0017 and μ(alive at 31) = 0.6223 ± 0.0072. Both agree with the census δ_8(7) = 0.62394 and with μ(K_7) ≈ 0.62. Even at these short horizons, the Corollary F1 bound is strictly positive for every schedule (best 0.22), but far from sharp.
- **p = 3, 5.** The bound is vacuous, as Prop F2(a)'s counting threshold 2^{p−1} > p^2 predicts.
- **Deep gates.** A gate of depth ≥ 2 at or near the start of a window of length 7 makes the criterion certify **nothing**, for every schedule, on cylinders where 93–99.7 % of points are alive at n_L. This is the deep-gate cost of Prop F2(b),(c) and §7.2 (here s* = 2 at H = 7). Corollary F1 charges it as μ(A ∖ L_ℓ), exactly as stated.
- **Near −2.** On the cylinders x ≡ −2 mod 7^2 and 7^3, the Tao schedule fails everywhere, while θ ≥ 2/3 certifies the whole cylinder. The intermediate θ of Theorem F is genuinely used there.

## 2. Adversarial notes on the chain

1. **Lemma L.** It uses only that u is a unit and that τ − s̃ ≡ 0 mod p^D. It is insensitive to slope, to the linear regime, to D = 0 or D′ = 0, and to gates of any depth inside W or W′. All of these were exercised (§1.2), with moduli up to p^18 at x within p^12 of −m.
2. **Theorem F.** The induction uses only Lemma L, the inclusion "children of a parent alive at n_ℓ are alive at n_{ℓ+1}", and pigeonhole: |T_ℓ| ≥ θ_ℓ p^{D_ℓ} and |G_ℓ| > (1−θ_ℓ)p^{D_ℓ} force T_ℓ ∩ G_ℓ ≠ ∅. Each was tested. Taking θ_ℓ to depend on x is harmless, since the statement is pointwise.
3. **Corollary F1.** The bound is "1_{A∩I_j} − Σ_ℓ 1_{A∖L_ℓ} ≤ 1_{A∩K_p} pointwise", integrated. It needs no second moment and no independence, as claimed. Prop 11.12 and Prop 11.15(b) therefore do not touch it.
4. **Status label of LIFT.** The claim marks LIFT as unproved, and nothing here proves it. It is not touched by any test: the tests concern the implication, not its hypothesis.

## 3. What remains open

Nothing in the tested chain. Whether hypothesis LIFT holds for some p ≥ 7 is exactly the open problem stated in M4D.md §9. Numerically, at p = 7 with windows of length 7–8 (where the chains of §1.4 have a single (II)-window, ℓ = 1), the failure mass μ(∁L_1) of one window is 0.26–0.50, depending on the schedule (§1.4). LIFT needs these masses to be summable over infinitely many, growing windows.

## 4. Credit

- The machinery under test is track M4D (round 4).
- The θ = 1 case is the fullness propagation of track R2b (round 2; note Theorem 10.12).
- The minimal-θ case is Tao's block lemma (note Lemma 1.3(iii)).
- (F1) and (F2) are from R3M (round 3, §1).
- Census values are from round 1 (note §4.7).
- Classical tools: König's lemma; countable subadditivity.

*This check was produced in an AI-assisted session (round 4, track verify_M4D_falsify). It has not been checked by a human.*
