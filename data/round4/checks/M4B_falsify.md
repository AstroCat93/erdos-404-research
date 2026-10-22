# Check of M4B Theorem B1 / B1′ (adaptive window times): numerical falsification

> **Part II** (appended below, 2026-10-14) is a separate check, by the same lens, of M4B **Lemma B2a + Corollary B2′** (deep gate at distance d). Its verdict is *confirmed, with wording fixes*. Part I (this headline and §§1–7) concerns Theorem B1/B1′ only.

Date: 2026-10-14. Lens: numerical falsification with exact arithmetic. Code: `code/round4/verify_M4B_falsify/`, written from the definitions and sharing no code with `code/round4/M4B/` or `code/round3/`. Logs: `data/round4/verify_M4B_falsify/`; each log starts with its command line.

## Headline

**Verdict: confirmed, with three small fixes.** No counterexample was found to any step of the chain behind Theorem B1 / B1′. Every exact identity and inequality the proof uses was tested at p = 7, and also at p = 3 and 5. The tests used random cylinders, x close to −1, −2 and −k, deep lifts, and three different two-step-predictable rules (`lin`, `ladder`, `hash`). There were 0 failures.

The sharpest tests are these:
- The single-parent **equality** cases of Prop C2 and Prop B hold exactly in 443/443 cases with random window times.
- An exhaustive exact computation over all of ℤ_p confirms the global stopped process of B1′ to horizon 3–5 in 13 configurations: martingale, second-moment recursion, and the finite-horizon Paley–Zygmund bound.
- The B1′ bound is non-vacuous in 4 of these runs (all at p = 7). For example, μ(Y₄ > 0) = 0.228 ≥ 5.2·10⁻⁴.

The three fixes:
1. **(F1, a small gap in the written proof of B1′.)** The bullet "Q_j < ∞ … M_j is bounded" holds only if n_j takes finitely many values. That is true for j ≤ 1 and for the bounded-range example rule of M4B §2. For j ≥ 2, a general two-step-predictable rule may have unbounded n_j, and sup M_n grows with n: the largest M_n found at deep gates is 3.1, 3.5, 14.7, 29.8 at n = 14, 21, 28, 35. The theorem statement is unaffected: if Q_j = ∞ its hypothesis fails, or its conclusion is trivial. The bullet should say "if n_j is bounded", or B1′ should assume Q_j < ∞.
2. **(F2, wording.)** M4B says two-step predictability "is required". It is what the proof uses for B_ℓ, defined with the realised ε_ℓ: a one-step-predictable n_{ℓ+1} breaks the realised-ε bound in 16/16 single-parent atoms (adversary B). It is not strictly necessary, though. Remark R2 below [proved] shows that a one-step choice bounded by a two-step-predictable N* satisfies the C2 bound with ε(N*); adversary A gave 0/16 violations, as R2 predicts.
3. **(F3, headline of M4B.)** M4B states that B1 and B1′ "have no numerical content to test". They have exact finite consequences, and these are now tested (§2).

## 1. The claim and the chain checked

Claim (M4B Thm B1 / B1′, labelled [proved]): R3M Theorem C3 (= note Thm 11.14) holds verbatim when n₀ < n₁ are deterministic, n₀ ≥ 2p, and each n_{ℓ+1} (ℓ ≥ 1) is a function of x mod p^{V_{n_{ℓ−1}}(x)}. The global form is μ(K_p) ≥ (m*_j − √(ΠQ_jδ))²/(ΠQ_j).

The steps of the proof, and the test of each:

| step | statement used | test | result |
|---|---|---|---|
| S1 | Lemma B1a: n₀..n_{ℓ+1} and m_ℓ constant on A_ℓ(x); M_{n_ℓ} < m_ℓ; A_ℓ ⊆ A_{ℓ−1} | t1 (random and deep lifts, x ≈ −k), t1b | 172 683 lifts, 0 failures |
| S2 | B_ℓ is G_{ℓ−1}-measurable; ε_ℓ depends only on x mod p^{m_{ℓ−1}} on the linear-regime event | t1 | 65 280 B-checks (11 677 with the event true), 46 708 ε-constancy checks, 0 failures |
| S3 | martingale step: Cor A′ on atoms of G_ℓ with adaptive n_{ℓ+1} | t2 (exact means over all p^{D_ℓ} sub-cylinders) | 282 atoms (93 at p = 7), 0 failures |
| S4 | L² step: Prop C2 on atoms of G_{ℓ−1} with adaptive n_{ℓ+1}; Prop B at ℓ = j | t3: full populations, single explicit parents (equality), parent subsets | 229 atoms, 443 single parents (exact equality in both C2 and B), 182 subsets, 0 failures |
| S5 | recursion a_{ℓ+1} ≤ a_ℓ + ε̄_ℓ a_{ℓ−1}, Cauchy–Schwarz, Paley–Zygmund | t5 (global, exhaustive), t6 (per atom, random j) | 13 global configurations, 5 per-atom runs (170 atoms), 0 failures |
| S6 | survival ⇒ K_p: Prop A(i) at slope 0, (F1), (F2) | t2 (cross counts of prefix slope against final slope) | 0 violations (see R1: at slope 0 this is unconditional) |
| S7 | B1′: Q_j < ∞ through Observation G | t4 (Observation G at path level), t4b (probe) | Observation G: 124 084 (path, gate) pairs, 0 failures; "M_j bounded" needs n_j bounded (F1) |

## 2. Numerical tests

Exact means Python integers and `Fraction`. Slope-0 counts are int64 (at most 2^60), checked against brute force. Floats appear only in the Fourier cross-check of ε and in the square roots of the final Paley–Zygmund comparison, which uses a relative tolerance of 10⁻¹².

### 2.1 Library validation (`t0_validate.log`)
- The dynamic-programming counts of slope-0 and all alive paths (state: S mod p^{V_T}, S′ mod p) were compared with brute force over all 2^{n−1} paths.
  - Scope: p = 3, 5, 7, n ≤ 16, random x and x ≡ −k mod p^s (k ≤ 14, s ≤ 5).
  - Result: 840 comparisons, 0 failures. About one third have Z⁰ > 0.
- ε was computed two ways: by collisions, p^K Coll_K − p^D Coll_D (exact), and by the R3M Fourier-fibre definition Σ|μ̂_{W′}|²F_W (FFT). They agree in 87/87 cases, and χ² ≥ 0 and ε ≥ 0 throughout.

### 2.2 Partition and measurability (`t1_partition.log`, `t1b_n0_small.log`)
- *Setup.* Four rules (`lin`: the longest window keeping (5.2) under truncated valuations; `ladder`; `hash`, an arbitrary function of x mod p^{m_{ℓ−1}}; `det`), at p = 3, 5, 7 with n₀ ∈ {2p, 2p+3}, horizon 4.
- *Points.* Random x, and x = −k + p^s u for k ≤ n₁+9 and s ≤ 12.
- *Lifts.* For each ℓ, random lifts y ∈ A_ℓ(x), plus lifts that make some y+k divisible by p^{m_ℓ+e} (e = 1, 3, 9; 18 921 deep lifts).
- *Results.* 0 failures in:
  - constancy of n₀..n_{ℓ+1} and m₀..m_ℓ;
  - refinement, and M_{n_ℓ} < m_ℓ;
  - constancy of the linear-regime part of B_ℓ, and of the data (D_{ℓ−1}, D_ℓ, M_{n_{ℓ+1}}), on A_{ℓ−1}(x);
  - exact constancy of ε_ℓ on A_{ℓ−1}(x).
- *Negative control.* A one-step rule (n₂ read from x mod p^{m₁}) is non-constant on 119/240 atoms of G₀.
- *Sensitivity of the hypothesis n₀ ≥ 2p.* For n₀ < 2p, V_{n₀} is non-constant on its own cylinder in 44–691 of 2000 lifts. For n₀ ≥ 2p it is constant in 0/2000 failures.

### 2.3 Martingale step with adaptive times (`t2_martingale.log`)
- On atoms A of G_ℓ (ℓ = 0..3) where W_ℓ = [n_ℓ, n_{ℓ+1}) satisfies (W2′) and (W3′), with Z⁰_{n_ℓ} > 0, the test enumerates all p^{D_ℓ} sub-cylinders exactly. 30% of the sampled points are x ≈ −k.
- It checks E_A[c_{n_{ℓ+1}}Z⁰] = c_{n_ℓ}Z⁰_{n_ℓ}, that Z⁰_{n_ℓ} is constant on A, and that the rule returns the same n_{ℓ+1}, n_{ℓ+2} at every lift.
- It also checks Prop A(i) through a tagged DP: no slope-0 path at n_{ℓ+1} has a prefix of slope ≥ 1, and no alive child of a slope-0 parent has slope ≥ 1. This involved 7.6·10⁸ parent–child pairs.
- Result: 282 atoms (p = 3: 97, p = 5: 92, p = 7: 93), 0 failures.
- *Negative control.* A "peeking" rule picks N ∈ {N₁, N₂} from digits finer than m_ℓ, taking the pointwise maximum of c_N Z⁰_N. It raises E_A[M] strictly in 60/60 atoms (30 at p = 5, 30 at p = 7). So the mean test detects a violation of predictability.

### 2.4 Two-window step with adaptive times (`t3_twowindow.log`)
- On atoms C of G_{ℓ−1} with (5.2) for (W_{ℓ−1}, W_ℓ), where n_{ℓ+1} comes from the rule, the test enumerates all p^K lifts (p^K ≤ 400).
- *Full population.* C2 holds in 229/229 atoms. The ratio lhs/rhs over the 142 atoms with ε > 0 has median 0.044 and maximum exactly 1 (natural single parents). Prop B holds, and so does the martingale E_C[M_ℓ] = E_C[M_{ℓ+1}] = M_{ℓ−1}. The rule is constant on C, and ε by collisions equals ε by Fourier fibres.
- *Single explicit parent e* (descendants computed by a DP started from S_e). The proof loses nothing here, so equality is predicted:
  - E_C[(c_{N′}Y_{N′})²] − E_C[(c_N Y_N)²] = ε·c_n² **exactly** in 443/443 cases;
  - E_C[(c_N Y_N)²] = (1+χ²)c_n² **exactly** in 443/443 cases.
  - This would expose any error in the constant, the band, or the window identification under random times.
- *Random parent subsets (2–5 parents).* The inequalities hold in 182/182 cases.
- Per prime: p = 3: 76 atoms and 161 single parents; p = 5: 76 and 152; p = 7: 77 and 130.
- *Negative control* (outside the hypothesis of B1). n_{ℓ+1} is chosen one-step-predictably on each atom C′ of G_ℓ, among candidates N′ with distinct jumps that all satisfy (5.2). There are two adversaries:
  - **Adversary B** maximises the excess E_{C′}[(c_{N′}Y)²] − ε(N′)c_n². It violates the realised bound E[ΔM²] ≤ E[ε(N′(x))]M² in **16/16** single-parent atoms (8 at p = 5, 8 at p = 7).
  - **Adversary A** maximises E_{C′}[(c_{N′}Y)²]. It never exceeds max_{N′} ε(N′)·M² (0/16). Remark R2 explains why.

### 2.5 Observation G, the bound behind Q_j < ∞, and the ladder rule (`t4_obsG_ladder.log`, `t4b_Mj_probe.log`)
- *Observation G* (checker of R3M) was tested on explicit slope-0 path lists, at forced gates x = −i + p^s u in 80% of samples. The identity v(S_{e|i}(−i)) = s held for **124 084** (path, gate) pairs over 49 358 paths, with 0 failures.
- Z⁰_n = 0 at every point with p^s > e·(i−1)! (297 points, 0 failures).
- The bound M_n ≤ log_p(e(n−1)!) and c_nZ⁰_n ≤ p^{V_n}/2 on {Z⁰ ≠ 0} holds in 59/59 cases.
- *The example rule of M4B §2* (a C′-ladder start for horizon T_max, found with truncated valuations min(v(x+i), m_{ℓ−1})) behaves as claimed:
  - it is a function of x mod p^{m_{ℓ−1}} (450 tests);
  - on {M_{n_{ℓ+1}+T_max} < m_{ℓ−1}} the truncated ladder property equals the true one (321/321).
- *Probe for F1* (p = 7): at deep gates with depth up to the Observation-G cutoff, the largest M_n = c_nZ⁰_n found was:

  | n | 14 | 21 | 28 | 35 |
  |---|---|---|---|---|
  | largest M_n | 3.08 | 3.48 | 14.7 | 29.8 |
  | gate depth | 4 | 4 | 8 | 8 |

  So sup_x M_n grows with n. A bound on M_j uniform over x requires n_j to be bounded.

### 2.6 Exhaustive finite-horizon test of B1′ and B1 (`t5_*.log`, `t6_*.log`)
- *Method.* `t5_global.py` enumerates **all** atoms of G₀. Classes x = −i + O(p^s) with p^s > e(i−1)! are cut, because Observation G makes the slope-0 population empty there; a DP at a representative of each cut class confirms Z⁰ = 0. The total mass check (atoms plus cut classes) gives exactly 1 in every run.
- From each admissible atom it recursively refines through G₁, G₂, …, applying B_ℓ with the adaptive n_{ℓ+1} and the threshold ε̄. It then computes exactly m*, Q, a_k = E[M̃_k²], E[M̃_k], δ_L and Y_L = M̃_L·1{τ > L}.
- Results (0 failures in every run):

| p | n₀, n₁ | rule | L | ε̄ | adm atoms | nodes | (G1) E M̃_k = m* | B1′ finite-horizon bound | per-atom B1: non-vacuous / adm, min ratio |
|---|---|---|---|---|---|---|---|---|---|
| 7 | 14, 21 | lin | 3 | 1/5 | 58 | 17 992 | exact | 0.2400 ≥ 0.00625 | 50/58, 1.46 |
| 7 | 14, 21 | lin | 4 | 1/5 | 58 | 34 946 | exact | 0.2284 ≥ 0.00052 | 50/58, 1.75 |
| 7 | 14, 21 | ladder | 3 | 1/5 | 58 | 2 018 | exact | 0.2417 ≥ 0.00658 | 42/58, 1.46 |
| 7 | 14, 21 | ladder | 4 | 1/5 | 58 | 4 076 | exact | 0.2417 ≥ 0.00152 | 42/58, 1.75 |
| 7 | 14, 21 | hash | 3 | 1 | 58 | 1 634 | exact | vacuous | 20/58, 4.06 |
| 7 | 15, 22 | lin | 3 | 1/10 | 58 | 10 628 | exact | vacuous | 29/58, 1.23 |
| 7 | 14, 17 | lin | 3 | 1/20 | 62 | 341 | exact | vacuous | 0/62 |
| 5 | 10, 15 | lin | 3 | 1/5 | 17 | 1 802 | exact | vacuous | 13/17, 1.49 |
| 5 | 10, 15 | lin | 5 | 1/5 | 17 | 1 927 | exact | vacuous | 0/17 |
| 5 | 10, 15 | hash | 3 | 1 | 17 | 249 | exact | vacuous | 7/17, 4.14 |
| 5 | 12, 17 | ladder | 3 | 1/2 | 17 | 17 | exact | vacuous | 0/17 |
| 3 | 6, 9 | lin | 3 | 1/2 | 2 | 14 | exact | vacuous | 0/2 |
| 3 | 8, 11 | hash | 3 | 1 | 2 | 2 | exact | vacuous | 0/2 |

- In every run these hold, exactly:
  - (G2) a₀ ≤ a₁ ≤ Q;
  - (G3) a_{k+1} ≤ a_k + ε̄ a_{k−1};
  - (G4) a_L ≤ ΠQ;
  - (G5) E Y_L ≥ m* − √(a_Lδ_L), and μ(Y_L>0)·E Y_L² ≥ (E Y_L)²;
  - the per-node C2 check, 3 228 nodes in all.
- "Vacuous" means m* ≤ √(ΠQδ_L), so the bound says nothing; the inequalities (G1)–(G5) were still checked.
- `t6_atom_j.py` tests B1 per atom at a **random** starting time j = 1, 2. There the atom of G_j and n_{j+1} are themselves adaptive, and there were 170 admissible atoms in 5 configurations at p = 3, 5, 7. Results: the per-atom martingale is exact, a_j ≤ a_{j+1} ≤ (1+χ²_j)M_j² holds, the recursion holds, and μ_A(Y_L > 0) ≥ (1−√(Π_Aδ_A))²/Π_A on all 73 atoms where it is non-vacuous (min ratio 1.44). 0 failures.
- Two identical rows of numbers are genuine identities, not bugs. The pairs (n₀ = 14, 15 at p = 7), (10, 12 at p = 5) and (6, 8 at p = 3) give identical m* and a₀ because M_{n+1} = M_n whenever v(x+n+1) = 0. The added elements x+n+1 ≡ x+1, x+2 (mod p) lie in the classes that Observation G kills.

## 3. Observations with proofs

**R1 [proved]. Prop A(i) at slope 0 needs no window hypothesis once n ≥ 2p.** Let n ≥ 2p, x not a negative integer, e alive at n, f ∈ {0,1}^{N−n}. Then S′_{(e,f)}(x) ≡ S′_e(x) (mod p). So an alive child of a slope-0 parent has slope 0, and (with (F2)) every slope-0 path alive at N has a slope-0 prefix alive at n.
*Proof.*
- S′_{(e,f)} = S′_e + Σ_{n≤j<N} f_{j−n} π′_j, and π′_j(x) = Σ_{i≤j} π_j(x)/(x+i).
- Each term has valuation V_j − v(x+i) ≥ V_j − M_j.
- For j ≥ n ≥ 2p, at least two of x+1, …, x+j are divisible by p, so V_j − M_j ≥ 1.

This explains why the (W3′)-violating sensitivity run in t2 (270 points) could not fail. It is not a defect of the test.

**R2 [proved]. One-step choice below a two-step bound.** Setting:
- Let C be an atom of G_{ℓ−1}. Put n = n_{ℓ−1}, N = n_ℓ and m = V_n, all constant on C.
- Let N* > N be constant on C, with (5.2) holding for (n, N, N*).
- Let ν be a function of x mod p^{V_N(x)} with N < ν ≤ N*.

Then E_C[(c_νZ⁰_ν)²] − E_C[(c_NZ⁰_N)²] ≤ ε(n, N, N*)·(c_nZ⁰_n)².

*Proof.*
- By (5.2), M_{N*} < m, so all valuations up to N* are constant on C. The atoms C′ of G_ℓ inside C are the classes mod p^{V_N}, and ν is constant on each of them.
- Split C′ into the classes C″ mod p^{V_ν}. On C″, c_νZ⁰_ν is constant.
- Cor A′ (L = 0) applies on C″ to the window [ν, N*):
  - (W2′): V_{N*} − V_ν ≤ V_{N*} − V_n ≤ m − M_{N*} ≤ V_ν − M_ν, by (5.2), m ≤ V_ν and M_ν ≤ M_{N*};
  - (W3′): M_{N*} < m ≤ V_ν;
  - ν ≥ 2p.
- So E_{C″}[c_{N*}Z⁰_{N*}] = c_νZ⁰_ν, and Jensen gives E_{C″}[(c_{N*}Z⁰_{N*})²] ≥ (c_νZ⁰_ν)².
- Averaging over C″ ⊆ C′ ⊆ C gives E_C[(c_νZ⁰_ν)²] ≤ E_C[(c_{N*}Z⁰_{N*})²].
- Prop C2 for (n, N, N*) on C finishes the proof. ∎

So two-step predictability is a sufficient condition that the proof of B1 uses (with B_ℓ defined through the realised ε_ℓ), not a necessary one. Adversary A (0/16) matches R2, and adversary B (16/16) shows that the realised-ε form genuinely needs it. A full one-step variant of B1 along these lines is plausible but is not written out here [not claimed].

## 4. Falsification attempts that did not break the claim
1. Deep lifts inside atoms (y + k ≡ 0 mod p^{m_ℓ+9}) and starting points x ≈ −1, −2, −k with s ≤ 12. Lemma B1a and the measurability of B_ℓ survived (§2.2).
2. Windows chosen adversarially among admissible rules (`hash` is an arbitrary function of x mod p^{m_{ℓ−1}}). The martingale and C2 survived (§2.3, §2.4).
3. Single parents, where every inequality in the C2/B proofs must be an equality. The equalities are exact (§2.4).
4. Global accounting through deep atoms (gates up to the Observation-G cutoff). (G1) is exact to the last digit (§2.6).
5. Attempts that break only **outside** the hypotheses, as they should: n₀ < 2p (§2.2), peeking rules (§2.3), and one-step rules against the realised ε (§2.4).

## 5. What was not tested, and what remains open
- The infinite-horizon part of the proof (Doob's L² convergence, the event τ = ∞, K_p membership through (F1)) cannot be tested numerically. It was checked by reading and is the verbatim R3M argument, which the round-3 checker audited. Nothing in it uses determinism of the times beyond n_ℓ → ∞, which holds because the n_ℓ are strictly increasing integers.
- Sizes tested: p ∈ {3, 5, 7}, n ≤ 60, horizons L ≤ 5, composite jumps with p^K ≤ 2500. The B1′ bound was non-vacuous only in 4 runs at p = 7. At p = 3 only 2 atoms of G₀ are admissible (Observation G kills x ≢ 0 mod 3 and most of the rest).
- F1: whether Q_j < ∞ for every two-step-predictable rule with unbounded range is open. It is not needed for the truth of B1′.
- Hypothesis FE (or (S_B)) and the initial-phase gap of M4B §7 are outside this claim and untouched. μ(K_p) > 0 remains unproved.

## 6. Reproduction
Each log in `data/round4/verify_M4B_falsify/` starts with its command line. The drivers are `batch_t5.sh` and `batch_t6.sh`. The other runs are:
- `run.sh LOG python3 t0_validate.py 1 30`
- `t1_partition.py 2 80 8`
- `t1b_n0_small.py 31 400`
- `t2_martingale.py 4 30 400`
- `t3_twowindow.py 7 25 400 2500`
- `t4_obsG_ladder.py 8 150`
- `t4b_Mj_probe.py 12 1500`

Total wall time was about 4 minutes on one core under `nice -n 10`.

## 7. Credit
- Theorem C3, Lemma 2, Prop A, Cor A′, Prop B and Prop C2 are track R3M's (round 3). Observation G is the round-3 checker's.
- Theorem B1/B1′, Lemma B1a and the ladder rule are track M4B's (round 4).
- The quenched p = 2 martingale is track R1b's (round 2).
- Classical tools: the Paley–Zygmund inequality, Doob's L² martingale convergence theorem, Jensen's and the Cauchy–Schwarz inequalities. The second-moment method on trees follows Lyons.
- The double root (x+2)² is note Prop 3.4.
- This check was produced in an AI-assisted session (verification track verify_M4B_falsify of round 4). No human has checked it.

---

# Part II. Check of M4B Lemma B2a + Corollary B2′ (deep gate at distance d): numerical falsification

Date: 2026-10-14. Lens: numerical falsification, exact arithmetic. Code: `code/round4/verify_M4B_falsify/b2_*.py`, written from the definitions in M4B §1, §3 and R3M Prop C2. It shares no code with `code/round4/M4B/`, `code/round3/`, or Part I of this check. Logs: `data/round4/verify_M4B_falsify/b2_*.log`; each starts with its command line.

## II.0 Headline

**Verdict: confirmed, with wording fixes.** No counterexample was found. Every identity and inequality in the chain was tested exactly at p = 7, and also at p = 3 and p = 5: Lemma B2a → (B2.1), (B2.3) → Cor B2′(a), (b), (c) and the band [½, 3/2].

The cases cover:
- random cylinders and random windows;
- x close to −1, −2 and −k, including window start n = 0;
- gate depths s up to 60, so that K reaches 67;
- a second deep gate inside the post window;
- an empty first post window (d = N − n);
- the degenerate case K = g;
- distances up to d = 16.

| test | scope | result |
|---|---|---|
| Lemma B2a, exhaustive | all 3^d sign vectors, d ≤ 24, in both the ε_k/k! form and the falling-factorial form A₀ used in B2′(b) | exactly the 3 predicted solutions for every d ≥ 2; **0 failures** |
| Prop B2 (B2.1)–(B2.5) | 2 500 random windows, every split point: 17 158 (sample, split) pairs; all r mod p^{K−g} for (B2.3) | **0 failures**; negative control (u⁻¹ → 1) differs in 12 610/15 443 |
| Cor B2′ (a), (b), (c) and band | 4 000 forced-gate cases (2 016 at p = 7), 5 families | **0 failures** |
| Cor B2′, exhaustive over residues | 360 configurations, every unit w mod p^R (R = 3 at p = 5, 7; R = 4 at p = 3): 53 760 cases | **0 failures** |
| direct decomposition of ε by pre-digits | same 53 760 cases; 473 088 non-solution pre-vectors checked to contribute exactly 0 | **0 failures** |
| large distance | d = 10..16, s ≥ s_hyp(d): 300 cases | **0 failures** |
| comparison with round 3 | R3M `eps_gate_depth.log` (p = 3, d = 1, 4) | medians agree to 3 digits wherever ε is deterministic in x |

**Fixes.** All are about the statement as summarised. The written Cor B2′ in M4B §3 is correct.
1. **(W1) d = 1 must be excluded from the first clause.** The summary reads: "for a gate … at distance d with p^s > e(d−1)!: Coll^pre_g = (3/2)2^{−d} exactly, and ε = (c_{n+d}/c_n)[ε^post + ½Δ(1/(x+n+d−1))]". Read literally, that includes d = 1, where it is false:
   - Coll^pre_g = ½, not ¾ (600/600 cases);
   - the d ≥ 2 formula holds in only 62 of 600 cases (exactly those with Δ(1/(x+n)) = 0).
   
   M4B §3 states (b) and (c) correctly for d ≥ 2, with d = 1 separately. The summary should say "for 2 ≤ d ≤ N−n".
2. **(W2) The gate must be in the first window: 1 ≤ d ≤ N − n.** This is stated in the setting of M4B §3 but not in the summary.
   - With the gate in the second window, g > D in 600/600 tested cases. Then ε^post = ε([n+d,N),[N,N′)) is undefined, and the split identity has no meaning.
   - Coll^pre_g = (3/2)2^{−d} and the Prop B5 bound p^K Coll_K ≤ (3/2)(c_{n+d}/c_n)p^{K−g} still hold there (600/600, 0 failures).
3. **(W3, minor)** The M4B headline says B2a has "no numerical content to test". It has finite exact content, now checked exhaustively for d ≤ 24.
4. **(W4, reading.)** "The correction is the (y+2)² double root" is an interpretation, not a separate statement. The correction comes from the pre-pair δ_{n+d−2} = δ_{n+d−1} = ±1, which gives the *simple* factor A = ±y_{n+d−2}(x+n+d).
   - The double root (Y+2)², with Y = x+n+d−2, appears only when the pair is continued by δ_{n+d} = ±1. The identity y_{n+d−2} + y_{n+d−1} + y_{n+d} = y_{n+d−2}(x+n+d)² was verified 600/600.
   - This is consistent with r* = 1/(x+n+d−1) ≡ −1 (mod p^s).

## II.1 The claim and the chain

Claim (M4B Lemma B2a and Cor B2′, labelled [proved]).
- **B2a.** If ε_k ∈ {−1, 0, 1} and Σ_{k<d} ε_k/k! = 0, then ε_k = 0 for k ≥ 2 and ε₀ = −ε₁.
- **B2′.** Let 1 ≤ d ≤ N−n, s = v(x+n+d), p^s > e(d−1)!, and K > g. Then:
  - (a) v(x+n+i) = v(d−i) for 1 ≤ i < d, and g = v((d−1)!) + s;
  - (b) for d ≥ 2, Coll^pre_g = (3/2)2^{−d} and P(A ≡ 0 mod p^K) = 2^{−d}; for d = 1 both equal ½;
  - (c) for d ≥ 2, ε = (c_{n+d}/c_n)[ε^post + ½Δ(1/(x+n+d−1))]; for d = 1, ε = (p^s/2)ε^post for every s ≥ 1;
  - hence ½ ≤ ε / ((c_{n+d}/c_n)ε^post) ≤ 3/2.

| step | what is used | test (log) | result |
|---|---|---|---|
| S1 | Lemma B2a | exhaustive by meet in the middle, d ≤ 24 (`b2_t1_lemmaB2a.log`) | 0 failures |
| S2 | the reduction A ≡ 0 (mod p^g) ⇒ A₀ = 0, via y_{n+i} ≡ (−1)^i(d−1)_i (mod p^s) and \|A₀\| < e(d−1)! < p^s | explicit enumeration of all 3^d pre-vectors as exact p-adic integers, d ≤ 9 (`b2_t3`); MITM for d ≤ 16 (`b2_t7`) | the solution set {δ : p^g \| A} is exactly {0, ±(e_{d−2}+e_{d−1})} in every case |
| S3 | (a): pre-gate valuations are factorial | `b2_t3`, `b2_t7` | 0 failures |
| S4 | (B2.1): the split identity | `b2_t2` (all splits, random x) | 0 / 17 158 |
| S5 | (B2.3): \|Δ(r)\| ≤ Δ(0), Δ even, for **all** r | `b2_t2` | 0 / 17 158 |
| S6 | (B2.2): Δ(0) = ε^post, with ε^post computed from scratch on [n+d, N, N′) | `b2_t2`, `b2_t3` | 0 failures |
| S7 | (c): the exact identity, with ε computed directly from the composite law and no splitting | `b2_t3`, `b2_t6`, `b2_t7`, `b2_t5` | 0 failures |
| S8 | the mechanism of (c): pre = 0 contributes (c_{n+d}/c_n)ε^post; each sign of the pair contributes (c_{n+d}/c_n)Δ(r*)/4; every other pre-vector contributes exactly 0 | `b2_t6`, computed with the post digits relative to n (no division by y_{n+d}) | 0 failures |
| S9 | the band [½, 3/2] | `b2_t3`, `b2_t7` | observed range for d ≥ 2: [0.6144, 1.4360] (`b2_t3`), [0.75, 1.375] (`b2_t7`); d = 1: exactly 1 |

## II.2 Numerical tests

Exact arithmetic throughout:
- Python integers and `Fraction`;
- numpy int64 counts with at most 4^31 total weight, asserted;
- meet-in-the-middle dictionaries of Python integers for deep gates.

x is an integer representing the cylinder x + p^400 ℤ_p. Every valuation used is asserted to be determined by that cylinder.

### II.2.1 Lemma B2a (`b2_t1_lemmaB2a.log`, 11 s)
- *Exhaustive check.* For d = 1..24 (up to 3^24 ≈ 2.8·10^11 vectors, by meet in the middle on exact integers):
  - Σ ε_k (d−1)!/k! = 0 has exactly the solutions 0, (1,−1,0,…), (−1,1,0,…);
  - A₀ = Σ δ_i(−1)^i(d−1)!/(d−1−i)! = 0 has exactly 0 and ±(e_{d−2}+e_{d−1}).
- *The two numerical inequalities of the written proof* (tail Σ_{k>k*}1/k! ≤ (k*+2)/((k*+1)(k*+1)!) < 1/k*!) checked for k* ≤ 60.
- *Sharpness of p^s > e(d−1)!.* The hypothesis is sufficient but not necessary. For p = 3, 5, 7 and d ≤ 16, the least s for which A₀ ≡ 0 (mod p^s) has only the 3 trivial solutions is often below s_hyp. Examples: p = 7, d = 10 needs s = 5, against s_hyp = 8; p = 3, d = 16 needs s = 14, against s_hyp = 27. Cor B2′(b) itself needs only A ≡ 0 (mod p^g), with g = v((d−1)!) + s ≥ s, so it holds even more often (control C1 below). This does not affect the claim.

### II.2.2 Proposition B2 (`b2_t2_propB2.log`, 45 s)
- *Samples.* 2 500 random windows: n ∈ [0, 40] (n = 0, 1, 2 over-weighted), both window lengths in [1, 13].
  - 55% of x are Haar-random; 45% are x = −k + p^s w with k ≤ N′+3 and s ≤ 4.
  - Range of K (p^K ≤ 3^11, 5^7, 7^6): up to 11 at p = 3, 7 at p = 5, 6 at p = 7.
- *ε three ways.* Signed collisions by meet in the middle, signed collisions from a full numpy law, and the R3M definition Σ_r ν_k(r)² with the unsigned subset-sum law. They agree in all samples; the R3M definition was compared in 625 of them.
- *Results.* (B2.1)–(B2.5) hold at every split point: **17 158 pairs, 0 failures**, with ε > 0 in 2 150 samples.
- *Negative control.* (B2.1) with u⁻¹ replaced by 1 fails in 12 610 of the 15 443 pairs where u ≢ 1.

### II.2.3 Corollary B2′, random families (`b2_t3_corB2p.log`, 61 s)
- *Cases.* 4 000 in all (p = 7: 2 016, p = 5: 963, p = 3: 1 021), with d ≤ 9 at p = 7, d ≤ 8 at p = 5 and d ≤ 7 at p = 3. Composite windows have at most 22 elements.
- *Depths.* s ∈ [s_hyp(d), s_hyp(d)+4], and with probability 0.15 s ∈ [s_hyp, 60]. The largest values reached are s = 60 and K = 67.
- *Families:*
  - `rand` (1 477): random windows;
  - `negk` (739): x = −k + p^s w with n ∈ [0, k−1], d = k−n. This includes n = 0 with x ≈ −1, −2, −3 and very deep s.
  - `two` (232): a second gate x + n + d + t·p^s of depth s + s₂ (s₂ ≤ 12) inside the post window;
  - `end` (795): d = N − n, so the first post window is empty;
  - `short` (757): N′ − (n+d) < p, so K = g is possible (1 134 cases, where ε = ε^post = 0 and the claim is trivially true).
- *Spread of K − g:* {0: 1134, 1: 1498, 2: 684, 3: 133, 4: 176, 5: 115, 6: 84, 7: 18, 8: 35, 9: 23, ≥10: 100}.
- *Per-case checks:* (a), (b) by explicit enumeration of all 3^d pre-vectors, (c) exactly, evenness of Δ at r*, \|Δ(r*)\| ≤ ε^post, and the band. **0 failures.**
- *The band is not trivially tight.* For d ≥ 2 with ε^post > 0 (1 998 cases), the ratio ε/((c_{n+d}/c_n)ε^post) ranges over [0.6144, 1.4360], and differs from 1 in 1 988 cases. For d = 1 it is exactly 1.

### II.2.4 Controls and boundary cases (`b2_t4_controls.log`, 12 s; 600 cases each)
- **C1, hypothesis violated** (1 ≤ s, p^s < e(d−1)!, d = 3..8). These failures show that the hypothesis is used:
  - (b) fails in 496/600;
  - (c) fails in 341/600;
  - the band [½, 3/2] fails in 96/600;
  - (a) fails in 31/600.
  
  The per-(p, d, s) table in the log shows (b) and (c) holding exactly where A ≡ 0 (mod p^g) happens to have only the trivial solutions, for example (3, 4, 2), (5, 6, 3) and (7, 8, 4).
- **C2, d = 1.** Coll^pre_g = ½ in 600/600, and ε = (p^s/2)ε^post in 600/600 (s = 1..8). The d ≥ 2 formula with ½Δ(1/(x+n)) holds in only 62/600 (see W1).
- **C3, argument of Δ.** With r* the identity holds in 600/600. With r = 0 (i.e. factor 3/2) it holds in 47/600. With r = 1 it holds in 542/600, because r* ≡ −1 (mod p^s), Δ is even, and K − g ≤ s in most cases. The identity is therefore sharp, not a loose bound.
- **C4, gate in the second window** (d > N − n, d ≤ 8). The results:
  - Coll^pre_g = (3/2)2^{−d}: 600/600;
  - P(A ≡ 0 mod p^K) = 2^{−d}: 600/600;
  - the B5 bound: 600/600;
  - g > D in 600/600 (see W2).
- **C5.** y_{n+d−2} + y_{n+d−1} + y_{n+d} = y_{n+d−2}(x+n+d)²: 600/600.

### II.2.5 Exhaustive over residues, and direct decomposition (`b2_t6_exhaustive.log`, 46 s)
- *Configurations.* p ∈ {7, 5, 3}, n ∈ {0, 3, 2p}, d = 1..5, s ∈ {s_hyp, s_hyp+1}, N − n − d ∈ {0, 4}, N′ − N ∈ {p−1, 2p−2}: 360 configurations in all.
- *Points.* x = −(n+d) + p^s w for **every** unit w mod p^R (R = 3 at p = 7, 5; R = 4 at p = 3), with random higher digits: 53 760 cases.
- *Check 1.* The exact identity (c) holds in every case.
- *Check 2: direct decomposition.* For each pre-vector δ_pre, the contribution T(δ_pre) to ε is computed from the composite law conditioned on δ_pre. The post digits are taken relative to n, so the computation uses neither y_{n+d}⁻¹ nor Prop B2. In every case:
  - T(0) = (c_{n+d}/c_n)ε^post;
  - T(±pair) = (c_{n+d}/c_n)Δ(r*)/4 each;
  - T = 0 for all other pre-vectors (all of them for d ≤ 3, and 6 random ones for d = 4, 5; 473 088 in total);
  - Σ T = ε (d ≤ 3).
  
  **0 failures in 53 760 cases.**

### II.2.6 Large distances (`b2_t7_large_d.log`, 21 s)
- *Cases.* 300, with d = 10..16 and s ∈ [s_hyp, s_hyp+3]; for example p = 7, d = 16 forces s ≥ 15. Coll^pre_g and P(A ≡ 0 mod p^K) were computed by meet in the middle over the 3^d pre-vectors.
- *Results.* (a), (b), (c) and the band: **0 failures**. The ratio range was [0.75, 1.375], and K = g in 72 cases.

### II.2.7 Comparison with round 3 (`b2_t5_r3m_compare.log`, 2 s)
- *Setup.* Windows [16,26) split 21, [24,40) split 32 and [32,52) split 42 at p = 3, with d ∈ {1, 4}, s = 1..6, and 8 cylinders per point (fresh random digits, not the round-3 ones).
- *Agreement.* Wherever ε is essentially independent of x (large s), the medians agree with `data/round3/R3M/eps_gate_depth.log` to 3 digits. Examples (this check / R3M):
  - d = 1: 4.587/4.59, 13.76/13.8, 41.28/41.3, 4.146/4.12, 12.46/12.5, 38.03/38;
  - d = 4: 0.2206/0.221, 0.6619/0.662, 1.986/1.99, 5.957/5.96, 2.349/2.35, 7.192/7.19, 21.58/21.6, 2.081/2.08, 6.32/6.32, 19.36/19.4.
- *The κ reading.* With κ := ε/p^s (R3M's definition) and v_pre = g − s = v((d−1)!), the ratio κ/(p^{v_pre}2^{−d}ε^post) is:
  - exactly 1 for d = 1;
  - for d = 4: 0.9495 on [16,26), 0.974–1.358 on [24,40), and 0.910–1.357 on [32,52).
  
  So "the round-3 heuristic holds up to a factor in [½, 3/2]" is confirmed, where ε^post means the post-window mass at the same x. The Cor B2′ identity held exactly in every sample in the hypothesis range.

## II.3 Line-by-line re-check of the written proofs (supporting the numerics)

- **B2a.** Let k* ≥ 2 be the least index with ε_{k*} ≠ 0.
  - Then \|ε_{k*}/k*!\| = 1/k*! exceeds Σ_{k>k*} 1/k!, which is ≤ (k*+2)/((k*+1)(k*+1)!) < 1/k*!. So the tail sum is nonzero.
  - It is also at most e − 2 < 1 in absolute value.
  - But ε₀ + ε₁ is an integer equal to minus the tail. Contradiction.
  - Hence all ε_k = 0 for k ≥ 2, and ε₀ = −ε₁. Correct.
- **B2′(a).** v(x+n+i) = v((x+n+d) − (d−i)) = v(d−i), since 0 < d−i ≤ d−1 < p^s. Correct.
- **B2′(b).** Mod p^s, y_{n+i} = ∏_{k≤i}(k − d + p^s w) ≡ (−1)^i(d−1)!/(d−1−i)!.
  - If p^g \| A then, since g ≥ s, p^s \| A₀.
  - \|A₀\| ≤ Σ_{k<d}(d−1)!/k! < e(d−1)! < p^s, so A₀ = 0.
  - The substitution k = d−1−i, ε_k = (−1)^k δ_{n+d−1−k} turns A₀ = 0 into Lemma B2a.
  - The pair solutions give A = ±y_{n+d−2}(x+n+d), of valuation v((d−1)!) + s = g, so A ≢ 0 (mod p^K) when K > g.
  - Weights: 2^{−d} for δ_pre = 0, and 2·(¼)²·(½)^{d−2} = ½·2^{−d} for the pairs. Correct.
- **B2′(c).** In (B2.1), r_a = −a/y_{n+d} = ∓y_{n+d−2}(x+n+d)/(y_{n+d−2}(x+n+d−1)(x+n+d)) = ∓1/(x+n+d−1), a unit. Δ is even (B2.3), so ε = p^g 2^{−d}[Δ(0) + ½Δ(r*)].
  - For d = 1, A = δ_n and p^g \| δ_n forces δ_n = 0, since g = s ≥ 1.
  - The band follows from \|Δ\| ≤ Δ(0) = ε^post. Correct.
- **Hypotheses used.** p odd. 1 ≤ d ≤ N−n, so that g ≤ D and both collision events force p^g \| A. p^s > e(d−1)! (or s ≥ 1 for d = 1). K > g, needed only for the value 2^{−d} of P(A ≡ 0 mod p^K); if K = g, then ε = ε^post = Δ = 0. No other hypothesis is needed. In particular the claim does not need n ≥ 2p, admissibility, or the absence of further gates after n+d (family `two`).

## II.4 What was not tested / remains open
- Everything in the claim is a finite exact identity, and every step was tested. The tested sizes:
  - composite windows have at most 22 elements (25 in `b2_t7`);
  - full-array tests use p^K ≤ 3^11, 5^7, 7^6;
  - meet-in-the-middle tests reach K = 67;
  - distances reach d ≤ 16, with Lemma B2a itself checked to d ≤ 24.
  
  Nothing in the proofs depends on size, so the tests and the re-check together leave no gap.
- The claim does not bear on (S)/(S_B), on FE, or on the initial-phase gap of M4B §7. μ(K_p) > 0 remains unproved for every odd p.

## II.5 Reproduction
Each command was run with `code/round4/verify_M4B_falsify/run.sh LOG python3 …` from `code/round4/verify_M4B_falsify/` (nice −n 10, 30-minute limit):

| script | command |
|---|---|
| `b2_t1_lemmaB2a.py` | `24 16` |
| `b2_t2_propB2.py` | `20261014 2500` |
| `b2_t3_corB2p.py` | `20261014 4000 22` |
| `b2_t4_controls.py` | `41 600` |
| `b2_t5_r3m_compare.py` | `91 8` |
| `b2_t6_exhaustive.py` | `5 4 3 3` |
| `b2_t7_large_d.py` | `77 300` |

The library is `b2_lib.py`. Total wall time was about 4.5 minutes on one core.

## II.6 Credit
- Lemma B2a, Prop B2, Cor B2′ and Prop B5 are track M4B's (round 4).
- Prop C2, Lemma C5 and the κ heuristic of §7.3 are track R3M's (round 3). The round-3 values compared in II.2.7 come from R3M's `eps_gate_depth.log`.
- The double root (x+2)² is note Prop 3.4.
- Classical tools: Fourier inversion on ℤ/p^k, and Parseval.
- This check was produced in an AI-assisted session (verification track verify_M4B_falsify of round 4). No human has checked it.
