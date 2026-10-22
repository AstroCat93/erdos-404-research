# Round 3, track R3F: rigorous Fourier and equidistribution steps (2026-10-13)

*Two placeholders left when the track agent was cut off by an external spending limit were filled in by the lead after the adversarial check (`data/round3/checks/R3F.md`); the check's other wording fixes are listed there and applied in note.md §11.*

Track R3F of round 3 (AI-assisted). Scope: the analytic route to Q3 (note.md §6, §10.3–10.6), targets (a)–(e) of the round-3 task. All code is in `code/round3/R3F/`. All logs are in `data/round3/R3F/`; every log starts with its command line and ends with the wall time. Scratch files are in `/tmp/r3_R3F/`.

## Headline

**Nothing here settles Q1 or Q3. No new unconditional statement about any f(a,p) is claimed.** What is new is the following.

- **(a) Single gate blocks, uniformly in the level (proved + certified).**
  - Each Fourier shell of a single gate block depends only on (p, d). It does not depend on the gate's level, its position, or K' (Lemma A1).
  - Its L² shells are exact collision counts. There is exactly one integer relation, so the L² ratio is exactly 3/2 at every level d with p^{d-1} > ⌊e(p−1)!⌋ (Theorem A2). This gives a uniform L¹ bound by Cauchy–Schwarz (Corollary A3).
  - An exact Poisson/"carry" formula (Theorem A4) shows that the per-level ratio ρ_d = S_d/(N_d(2/π)^p) tends to an explicit constant J_p at rate O(((p−1)!/p^d)²), with explicit constants.
  - Combined with interval-arithmetic shell sums at small levels, this certifies sup_{d≥1} ρ_d (Theorem A5): **sup_d ρ_d ≤ 1.3203 (p=5), 1.1760 (p=7), 1.8377 (p=11), 1.2064 (p=13)**. The maximum is attained at d = 2 or 4, and ρ_d → J_p ≈ 1.17 for large d.
  - The ratio "≈1.17 at every p" that round 2 observed numerically is J_p (J_13 ∈ [1.17285, 1.17305]). J_p converges as p→∞ (Proposition A6).
  - This is the "first, insufficient step" of note §10.6 item 1. Why it is insufficient: §A7.
- **(b) The L² analogue for tail measures.**
  - Proved: L² mass = collision count. Finite L² mass gives absolute continuity of the tail measure and an explicit Haar lower bound for the tail set (Proposition B1).
  - The random-model L² mass is finite at every odd p, including p = 3, 5, where the L¹ budget fails (B2). Exact small-level L² shells are tabulated (B3). At p = 3 the L² mass of the tail from 3 reaches only 0.331 at level 15 and grows only at gate levels, by shrinking jumps: numerical evidence [heuristic] for positive Haar measure of a non-full tail.
  - The levels d ≤ t−1 of every RMF window are exactly the shells of the full factorial measure law(Σ_{i≥0}ε_i i!) (Proposition B4). So RMF(p,C) with CΛ_p<1 already forces that measure to have full support (Corollary B4'). Certified L¹ shells of that measure lie within a factor 3.75 of the random model on all computed levels (p = 7: d ≤ 9; p = 11, 13: d ≤ 7), with totals 0.286, 0.0668 and 0.00830 (B4-data).
  - A collision-count version of Theorem 10.16 holds (Theorem B5). Its budget is Λ'_p = Σ_d N_d 2^{−U_d/2}, which is < 1 exactly when p ≥ 11 (Λ'_11 = 0.2920, Λ'_13 = 0.1549).
  - Two obstructions are proved: an L² barrier lemma (B6, the L² form of Theorem 3.10), and an exact L² renormalisation identity whose profile satisfies sup H^{(2)} = H^{(2)}(0) ≥ 1 (B7, the L² form of Corollary 10.20).
  - **No uniform L² bound is proved.**
- **(c) Averaging over K'.**
  - Proved: for c ≤ t the window is linear in K' modulo p^{t+c} (C1). K'-averaged L² shells are exact collision counts of the 2D lazy walk (Σδ_iσ_i, Σδ_iτ_i), so averaging projects onto the sublattice where the twist vanishes (C2). The proportion of non-covering classes is ≤ Σ_d √(N_d E_{K'}Q_d) (C3).
  - Small cases are certified (C4).
  - **Negative (C5):** at the minimal lengths H_t where Cov actually holds, these bounds are vacuous. Pure collision-count certificates appear only at H ≈ 2–2.6·H_t; for example they certify every class of (p,t,H) = (13,2,26), (13,2,39), and 154/156 classes of (13,3,39). An averaged statement can feed Proposition 10.10 or Theorem 10.16 only by certifying every class.
- **(d) Factorial-base transfer.**
  - Proved: the continuous transfer operator computes exactly the j = 0 term of a Poisson decomposition of each grid sum. The p-adic grid adds aliasing terms j ≠ 0 (D1).
  - For the tail shells of §10.4 the j = 0 term is the random model to within 2.2·10⁻⁴, while the certified shells differ from it by factors 0.06–4.2. All of the deviation is aliasing (D2).
  - Rigorous non-sup bound: Cauchy–Schwarz per level with exact collision counts (D3).
  - **Obstruction (D4):** any bound that replaces |cos| by a positive-definite trigonometric majorant loses a factor ≥ 16/15 per element against the L¹ random model. Such a replacement turns the L¹ sum into a positive count, and the best majorant constant lies in [0.6791, 0.7072].
- **(e) Interval-arithmetic re-run of all certified shells of §10.4.1 (computer-assisted).** Two independent implementations with directed rounding were run, plus a brute-force reference:
  - **Σ_{k≤7} T_13(k) ∈ [9.29878581106·10⁻³, 9.29878581108·10⁻³]**;
  - **Σ_{k≤8} T_11(k) ∈ [6.68544967910·10⁻², 6.68544967911·10⁻²]**.

  Every shell is now in interval arithmetic. This confirms round 2's values.

Throughout, "proved" means a complete proof is written below. Nothing here was checked by a human.

---

## 0. Notation and two standard facts

- p is an odd prime, e(x) = exp(2πix), N_d = p^d − p^{d−1}, U_d = min{i : v_p(i!) ≥ d}.
- For a finite family y = (y_i) of p-adic integers, ν_y is the law of Σ ε_i y_i with independent fair coins ε_i (the uniform measure on the subset sums).
- For ξ = u/p^d with u a unit: |ν̂_y(ξ)| = ∏_i |cos(π u y_i / p^d)| (phases read mod 1; only y_i mod p^d matters).
- Level-d shells:
  - S_d(y) = Σ_{u∈(Z/p^d)^×} ∏_i |cos(π u y_i/p^d)| (L¹);
  - Q_d(y) = Σ_{u∈(Z/p^d)^×} ∏_i cos²(π u y_i/p^d) (L²).

**Fact F1 (Fourier inversion / Parseval; note Prop. 3.13(b)).**
- If Σ_{d=1}^{D} S_d(y) < 1, then every class mod p^D is a subset sum of y.
- Σ_{d=1}^{D} Q_d(y) = p^D·Coll_D(y)/4^n − 1, where n = #y and Coll_D(y) = #{(S,S') : Σ_S y ≡ Σ_{S'} y (mod p^D)}.
- The fraction of classes mod p^D that are missed is ≤ Σ_{d≤D} Q_d(y).

*Proof.* Inversion on Z/p^D gives ν(r) ≥ p^{−D}(1 − Σ_{ξ≠0}|ν̂(ξ)|). Grouping ξ ≠ 0 by exact order p^d gives the shells. Parseval gives Σ_ξ|ν̂(ξ)|² = p^D Σ_r ν(r)², and ν(r) = c(r)/2^n with Σ_r c(r)² = Coll_D. Finally Σ_r(p^Dν(r) − 1)² = p^D(p^DΣ_rν(r)² − 1) = p^D Σ_{d≤D}Q_d. If ν vanishes on a set Z of residues, the left side is ≥ |Z|. ∎

**Fact F2 (Cauchy–Schwarz per level).** S_d(y) ≤ √(N_d Q_d(y)).

---

## (a) Single gate blocks, uniformly in the level

**Setting.** A gate block of level j ≥ 0 is block m = {pm, …, pm+p−1} with v_p(m+1) = j. In the window form of note §3.7 it is the window of length H = p ending at N* = p(m+1) = p^t K' (t = j+1, K' a unit). Its normalised elements are y_i(K') = ∏_{s=1}^{i}(p^tK' − (p−s)), 0 ≤ i < p. Here c = v_p((p−1)!) = 0, so the demand is p^t. Write β_{j,K'} := ν_{y(K')}.

**Lemma A1 (shells are level-, position- and K'-independent) [proved].** For 1 ≤ d ≤ t, y_i(K') ≡ σ_i := (−1)^i (p−1)!/(p−1−i)! (mod p^d). Hence, for every d ≤ j+1,
  S_d(β_{j,K'}) = S_d(p) := Σ_{u∈(Z/p^d)^×} F_p(u/p^d),  F_p(θ) := ∏_{i<p} |cos(π θ σ_i)|,
and the same holds for Q_d. These quantities depend only on (p, d).

*Proof.* p^tK' ≡ 0 (mod p^d), and ∏_{s≤i}(s − p) = (−1)^i (p−1)(p−2)⋯(p−i) = σ_i (Lemma 10.11(a) with H = p). ∎

(This is the Fourier form of the gate congruence, Theorem 3.9(b).)

**Theorem A2 (exact L² shells) [proved].** Let A₂(M) = (1/M)Σ_{r mod M} F_p(r/M)², and let R_p = Σ_i|σ_i| = Σ_{w=0}^{p−1}(p−1)!/w! = ⌊e(p−1)!⌋.
- (i) A₂(M) = 4^{−p} Σ_{δ∈{−1,0,1}^p, M | ⟨δ,σ⟩} 2^{z(δ)}, where z(δ) = #{i : δ_i = 0}. Also Q_d(p) = p^d A₂(p^d) − p^{d−1}A₂(p^{d−1}).
- (ii) The only δ ∈ {−1,0,1}^p∖{0} with ⟨δ,σ⟩ = 0 are ±(e_{p−2} + e_{p−1}).
- (iii) If M > R_p, then A₂(M) = (3/2)·2^{−p}. Hence Q_d(p) = (3/2)·N_d·2^{−p} whenever p^{d−1} > R_p.

*Proof.*
- (i) Use cos²(πx) = (2 + e(x) + e(−x))/4. Then F_p(θ)² = 4^{−p}Σ_δ 2^{z(δ)} e(θ⟨δ,σ⟩), and (1/M)Σ_{r mod M} e(rn/M) = 1[M|n]. In the shell, the non-units u = pu' (u' mod p^{d−1}) satisfy F_p(pu'/p^d) = F_p(u'/p^{d−1}).
- (ii) Put P_w = (p−1)!/w! (0 ≤ w ≤ p−1), so σ_i = (−1)^i P_{p−1−i}, and δ'_w := (−1)^{p−1−w}δ_{p−1−w}. Then ⟨δ,σ⟩ = Σ_w δ'_w P_w. Suppose this vanishes and δ'_w = 0 for all w > u, for some u ≥ 2. For w < u, P_w = P_u·u!/w! and u | u!/w!. So δ'_u P_u ≡ 0 (mod u P_u), i.e. u | δ'_u, and then δ'_u = 0 because |δ'_u| ≤ 1 < u. Downward induction from u = p−1 to u = 2 gives δ'_w = 0 for all w ≥ 2. Then (δ'_1 + δ'_0)(p−1)! = 0, since P_1 = P_0. For odd p, δ'_1 = −δ_{p−2} and δ'_0 = δ_{p−1}, so δ_{p−2} = δ_{p−1}.
- (iii) |⟨δ,σ⟩| ≤ R_p < M, so M | ⟨δ,σ⟩ iff ⟨δ,σ⟩ = 0. By (ii) the weight is 2^p + 2·2^{p−2} = (3/2)·2^p. ∎

So, in the archimedean regime, the collision excess of a gate block over the random model is exactly the factor 3/2 coming from the single relation σ_{p−2} + σ_{p−1} = 0 (i.e. (p−1)!/1! = (p−1)!/0!).

**Corollary A3 (uniform L¹ bound) [proved; the finite table is computer-assisted].** For every gate block of every level j and every d ≤ j+1,
  S_d ≤ √(N_d Q_d(p)) ≤ C^{CS}_p · N_d (2/π)^p,  C^{CS}_p := max_d √(Q_d(p)/N_d)(π/2)^p.
For p^{d−1} > R_p the maximand equals √(3/2)(π/(2√2))^p. Exact values (`gate_l2.py`, exact rational arithmetic; logs `a_gate_l2_p{5,7,11,13}.log`, which list Q_d/(N_d2^{−p}) for every d ≤ 12):
- C^{CS}_5 = 2.0705 (attained for all d ≥ 4);
- C^{CS}_7 = 2.5543;
- C^{CS}_11 = 4.5460 (d = 2);
- C^{CS}_13 = 5.2089 (d = 4).

*Proof.* Fact F2 and Theorem A2. ∎

**Theorem A4 (Poisson formula; limit; rate) [proved].** Let b_k := (−1)^{k+1}/(4k²−1) for k ∈ Z (so b_0 = 1, b_{±1} = 1/3, b_{±2} = −1/15, …). Put
  Ψ_p(n) := Σ_{k∈Z^p : Σ_w k_w P_w = n} ∏_w b_{k_w}  (n ∈ Z).
- (i) F̂_p(n) = (2/π)^p Ψ_p(n). For every M ≥ 1, A(M) := (1/M)Σ_{r mod M} F_p(r/M) = (2/π)^p Σ_{j∈Z} Ψ_p(jM).
- (ii) J_p := Ψ_p(0) = (π/2)^p ∫₀¹ F_p. Moreover
  ρ_d := S_d(p)/(N_d(2/π)^p) = J_p + (p^d E'(p^d) − p^{d−1}E'(p^{d−1}))/N_d,  E'(M) := Σ_{j≠0} Ψ_p(jM).
- (iii) |E'(M)| ≤ (π²/3)·α_{p−1}/M². The constants are defined by
  - α₁ = π²/16, β₁ = π²/8;
  - κ_m = 2 − (π/(2m))cot(π/(2m)), β_m = κ_m β_{m−1};
  - α_m = β_{m−1}/3 + α_{m−1}(π/3 + m√κ_m)².

  In particular ρ_d → J_p, with |ρ_d − J_p| ≤ (π²α_{p−1}/3)(p^{−d} + p^{−d+1})/N_d.

*Proof.*
- (i) For real x, |cos πx| = (2/π)Σ_k b_k e(kx). The series converges absolutely, with Σ_k|b_k| = 1 + 2Σ_{k≥1}1/(4k²−1) = 2.
  - b is even, so the signs of the σ_i do not matter. Multiplying the p series evaluated at x = θP_w gives F_p(θ) = (2/π)^p Σ_{k∈Z^p} ∏_w b_{k_w} e(θ Σ_w k_wP_w).
  - This sum converges absolutely (total mass 2^p). Grouping by n = Σk_wP_w gives F̂_p(n).
  - Summing e(rn/M) over r mod M gives M·1[M|n]. The interchange is justified by absolute convergence.
- (ii) J_p = Ψ_p(0) = (π/2)^p F̂_p(0) = (π/2)^p ∫F_p by (i). The formula for ρ_d follows from (i) and S_d = p^dA(p^d) − p^{d−1}A(p^{d−1}) (as in A2(i)), since (p^d − p^{d−1})J_p = N_d J_p.
- (iii) *Carry recursion.* For 1 ≤ m ≤ p−1 put Ψ_m(s) := Σ_{(k_0,…,k_m): Σ_{w≤m} k_w m!/w! = s} ∏ b_{k_w}, so that Ψ_{p−1} = Ψ_p.
  - For m ≥ 2, the w = m coefficient is 1 and all other coefficients are multiples of m. So k_m = s − m s' with s' = Σ_{w<m}k_w (m−1)!/w! ∈ Z, and Ψ_m(s) = Σ_{s'∈Z} b_{s−ms'} Ψ_{m−1}(s').
  - Ψ₁(s) = Σ_{k₀+k₁=s} b_{k₀}b_{k₁} = (b∗b)(s). These are the Fourier coefficients of ((π/2)|cos πx|)² = (π²/8)(1 + cos 2πx), so Ψ₁(0) = π²/8, Ψ₁(±1) = π²/16, and Ψ₁(s) = 0 otherwise.
  - Put G₁ = |Ψ₁| and G_m(s) = Σ_{s'}|b_{s−ms'}| G_{m−1}(s'). By induction |Ψ_m| ≤ G_m.
  - *Bound by β_m.* κ_m := sup_s Σ_{s'}|b_{s−ms'}| is the largest residue-class sum of |b| mod m. The class of 0 has sum 1 + 2Σ_{i≥1}1/(4m²i²−1) = 2 − (π/(2m))cot(π/(2m)) (partial fractions: Σ_{i≥1}1/(i²−z²) = (1 − πz cot πz)/(2z²) at z = 1/(2m)). Every other class sums to at most Σ_{k≠0}|b_k| = 1 ≤ κ_m. Hence G_m ≤ κ_mβ_{m−1} = β_m.
  - *Bound by α_m/s², for s ≠ 0.*
    - The term s' = 0 contributes |b_s|G_{m−1}(0) ≤ β_{m−1}/(4s²−1) ≤ β_{m−1}/(3s²).
    - For s' ≠ 0 put k = s − ms'. For every η > 0, s² ≤ (1+1/η)k² + (1+η)m²s'². Using |b_k|k² ≤ 1/3, Σ_{s'≠0}s'^{−2} = π²/3 and Σ_{s'}|b_{s−ms'}| ≤ κ_m, this gives s² Σ_{s'≠0}|b_{s−ms'}|/s'² ≤ (1+1/η)π²/9 + (1+η)m²κ_m.
    - Choosing η = (π/3)/(m√κ_m) gives (π/3 + m√κ_m)². With G_{m−1}(s') ≤ α_{m−1}/s'², this yields G_m(s) ≤ α_m/s².
  - *Start.* G₁ vanishes for |s| ≥ 2, so α₁ = π²/16 and β₁ = π²/8.
  - Hence |E'(M)| ≤ Σ_{j≠0} G_{p−1}(jM) ≤ α_{p−1}Σ_{j≠0}(jM)^{−2}. ∎

*Constants* (`alias_bound.py`, mpmath intervals). α_{p−1}/((p−1)!)² ≤ 5.61, 11.86, 31.80, 45.61, 81.13 for p = 5, 7, 11, 13, 17. The resulting bounds on |ρ_d − J_p| are ≤ 8.2·10⁻³ (p=5, d=5), ≤ 1.4·10⁻² (p=7, d=6), ≤ 3.3·10⁻³ (p=11, d=9) and ≤ 2.8·10⁻² (p=13, d=10). They decrease by a factor ≥ p² per level. (The recursion is crude. The cheapest aliasing mechanism, one large carry jump at the last step, suggests a true constant of about 0.15·((p−1)!)² [heuristic], so roughly two orders of magnitude are lost at p = 13. This only shifts the level from which the analytic bound takes over.)

**Theorem A5 (certified sup over all levels) [computer-assisted].** For every gate block of every level, and every d ≥ 1 (with d ≤ j+1):

| p | ρ_1 | ρ_2 | ρ_3 | ρ_4 | ρ_5 | ρ_6 | ρ_7 | ρ_8 | ρ_9 | J_p ∈ | analytic bound, all d ≥ d₀+1 | **sup_d ρ_d ≤** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 0.6683 | **1.3203** | 1.0699 | 1.1673 | 1.1671 | 1.1670 | 1.1670 | 1.1670 | 1.1670 | [1.16690, 1.16705] | d ≥ 6: ≤ 1.16738 | **1.320222** (d = 2) |
| 7 | 0.7989 | 0.6276 | 1.1733 | **1.1760** | 1.1699 | 1.1705 | 1.1705 | 1.1705 | 1.1705 | [1.17036, 1.17053] | d ≥ 7: ≤ 1.17081 | **1.175992** (d = 4) |
| 11 | 0.8673 | **1.8377** | 1.0690 | 1.1727 | 1.1718 | 1.1722 | 1.1726 | 1.1726 | 1.1726 | [1.17243, 1.17262] | d ≥ 9: ≤ 1.17589 | **1.837654** (d = 2) |
| 13 | 0.2303 | 1.1272 | 1.0157 | **1.2064** | 1.1703 | 1.1729 | 1.1730 | 1.1730 | 1.1730 | [1.17285, 1.17305] | d ≥ 10: ≤ 1.20053 | **1.206366** (d = 4) |

Entries are certified upper bounds of ρ_d, rounded up in the 4th decimal; the exact bounds are in `a_summary_p{5,7,11,13}.log`. Coverage of the levels:
- p = 5: d ≤ 10 by both programs, d = 11, 12 by `gate_d`, d ≥ 6 analytically.
- p = 7: d ≤ 8 by both programs, d = 9, 10 by `gate_d`, d ≥ 7 analytically.
- p = 11: d ≤ 8 by both programs, d = 9 by `gate_d` and analytically.
- p = 13: d ≤ 8 by both programs, d ≥ 10 analytically. d = 9 by `gate_d` (S₉ ≤ 3.239283592·10⁷, ratio 1.172950) and by `ivshell` in six chunks, of which only chunks u0 = 1, 2 were run before the track agent was cut off by an external spending limit. *(Filled in by the lead after the check:)* the level is covered independently by the checker's program `shellchk` (arb-certified tables, sharing no code with R3F), which gives S₉ ∈ [32392835.6659466, 32392835.6659821] (`data/round3/checks/R3F.md`). Independently of both, Cauchy–Schwarz with the exact Q₉ (`a_gate_l2_p13.log`) gives ρ₉ ≤ 4.7963.

So every level is covered by two independent methods (for p = 13, d = 9: `gate_d` and the checker's `shellchk`). For d ≥ 10 at p = 13 the analytic bound uses J_13 from one method (the truncated carry recursion, implemented twice: `jrel` and the checker's `jcheck`); the grid identity gives no independent check there.

The sup is attained at a small level (d = 2 or 4), in the modular regime p^d < (p−1)!. The asymptotic value J_p is approached from d ≈ log_p((p−1)!) + 1 on. The analytic bound uses J_p from `jrel.c`. As an independent check, the directly computed ρ_d at the largest computed level lies inside the J_p enclosure (p = 5, 7, 11, 13: 1.166975, 1.170443, 1.172524, 1.172950).

*Certificate.*
- For d ≤ d₀, ρ_d is bounded by the larger of two independent rigorous upper bounds for S_d:
  - `ivshell.c` in file mode: interval arithmetic with directed rounding;
  - `gate_d.c`: incremental residues and its own Taylor enclosure, sharing no code with `ivshell.c`.

  The two agree to ≤ 3·10⁻⁸ relative.
- For d > d₀, Theorem A4(iii) is used with the rigorous enclosure of J_p from `jrel.c` (below).
- The levels are glued as follows. A4's bound is decreasing in d, so its value at d₀+1 bounds all larger d.
- Logs: `a_gate_ivshell_p*_d*.log`, `a_gate_d_p*.log`, `a_jrel_p*_C10000.log`. Summaries: `a_summary_p{5,7,11,13}.log` (`summarize_a.py`).

**Rigorous J_p (`jrel.c`) [computer-assisted].** J_p = Σ_s v₁(s)(b∗b)(s), where v is the forward carry vector:
- v_{p−1} = δ₀;
- v_{m−1}(s') = Σ_s v_m(s) b_{s−ms'}.

The computation keeps carries |s| ≤ C at each step. The error of this truncation is at most Σ_m β_{m−1}‖v_m‖₁·(2/3)/(m(m−1)C), because Σ_{|s'|>C}|b_{s−ms'}| ≤ (2/3)/(m(m−1)C) for |s| ≤ C. The arithmetic is mid-radius: directed-rounding radii plus Higham's γ_n bound for the rounding of dot products. Results with C = 10⁴ (`a_jrel_p*_C10000.log`, total wall time 215 s):

| p | 3 | 5 | 7 | 11 | 13 | 17 | 19 | 23 |
|---|---|---|---|---|---|---|---|---|
| J_p ≥ | 1.151412 | 1.166902 | 1.170358 | 1.172429 | 1.172852 | 1.173323 | 1.173465 | 1.173658 |
| J_p ≤ | 1.151495 | 1.167049 | 1.170528 | 1.172619 | 1.173047 | 1.173525 | 1.173669 | 1.173866 |
| truncated sum | 1.1514538 | 1.1669753 | 1.1704430 | 1.1725240 | 1.1729495 | 1.1734239 | 1.1735672 | 1.1737621 |

The width comes entirely from the truncation bound (≈10⁻⁴). The arithmetic error is below 10⁻¹⁰. Cross-checks:
- J_5 and J_7 agree with the brute-force grid ratios at large d (1.166975 at p = 5, d = 10, and 1.170443 at p = 7, d = 8; ivshell gate logs);
- J_13 agrees with round 2's diagnostic ratio 1.173 (`fwin2_gate_p13_t7_H13.log`, levels d = 5–7).

**Proposition A6 (J_p converges as p → ∞) [proved].** J_∞ := lim J_p exists, and
  |J_{p'} − J_p| ≤ (π²/9)·β^{abs}_∞/(p−1)  for p' > p,
where β^{abs}_∞ = (π²/8)∏_{m≥2}κ_m < ∞.

*Proof.*
- Since 1/w! = (p−1)!^{−1}P_w, J_p is the sum of ∏_w b_{k_w} over k ∈ Z^{p} with Σ_{w<p} k_w/w! = 0.
- Since b_0 = 1, J_{p'} − J_p = Σ_{U=p}^{p'−1} R_U, where R_U is the sum over relations whose largest index with k_w ≠ 0 is U.
- Multiplying such a relation by U! gives k_U ≡ 0 (mod U), so k_U = −Us' with s' ≠ 0. The remaining coordinates form a relation Σ_{w<U}k_w(U−1)!/w! = s'.
- Bounding the remaining weights by absolute values: the completion is G^{abs}_{U−1}(s'), defined like G but with final pair (|b|∗|b|) ≤ Σb_k² = π²/8. So it is ≤ β^{abs}_{U−1} ≤ β^{abs}_∞.
- Hence |R_U| ≤ β^{abs}_∞ Σ_{s'≠0}|b_{Us'}| ≤ β^{abs}_∞·(2/(3U²))(π²/6). Summing over U ≥ p gives the claim.
- ∏κ_m converges because κ_m − 1 ≤ 2/(4m²−1) + 2/(3m²). ∎

(The bound is crude: ∏_{m≥2}κ_m ≤ 1.6744 and β^{abs}_∞ ≤ 2.0657 (interval arithmetic), so |J_p − J_∞| ≤ 2.266/(p−1).) Numerically the truncated sums increase with p (1.15145, 1.16698, 1.17044, 1.17252, 1.17295, 1.17342, 1.17357, 1.17376 for p = 3, …, 23). This suggests J_∞ ≈ 1.174–1.175 [heuristic extrapolation; the rigorous bound only gives |J_23 − J_∞| ≤ 0.103].

**This explains round 2's numerics.** Track R2b found a per-level ratio of about 1.17 for single gate blocks at every p tested (Conjecture 10.23, evidence). That ratio is J_p.

### A7. What (a) proves, and what it does not imply

*Proved.* Single gate blocks satisfy the random-model Fourier bound level by level, uniformly in the level, the position and K', with the constants of A5. This is RMF restricted to windows of length H = p.

*Not implied.* (Each item below is a proved statement or a direct consequence of one.)
1. **Windows of length p^{t−1}.** RMF concerns windows of length H = p^{t−1}. Their Fourier coefficient is a product over p^{t−2} blocks, evaluated at frequencies that differ from block to block by p-adic units (the unit parts U(n)). Per-block bounds on Σ_ξ of each factor do not bound Σ_ξ of the product. That is exactly the decorrelation problem of Corollary 10.20.
2. **The archimedean regime.** The asymptotic regime of A4, p^d ≫ (p−1)!, is what makes (a) provable. For a window of fixed length H, Lemma A1 extends verbatim: y_i ≡ σ^{(H)}_i = (−1)^i(H−1)!/(H−1−i)! (mod p^d) for d ≤ t. So the analogues of A2–A4 hold once p^d exceeds R^{(H)} = Σ_i|σ^{(H)}_i| ≤ e(H−1)!, i.e. d ≳ H log_p H. (Here (p−1)! is replaced by (H−1)!, and A2(ii) by the relation lattice of σ^{(H)}.) The RMF windows need d ≤ t + c with H = p^{t−1}, and there d ≪ H log_p H. **So for the RMF windows the archimedean regime is never reached.** All of their levels are in the modular regime, where the residues σ^{(H)}_i mod p^d are not the integers themselves.
3. **No crossing.** A single gate block cannot cover beyond L_p (Theorem 3.9(c)). Consistently, Σ_{d≤j+1}S_d ≈ J_p p^{j+1}(2/π)^p → ∞.
4. **Theorem 3.10.** (a) uses only the K'-independent residues σ_i. These are fixed integers, i.e. shallow information, which by the barrier lemma cannot carry a covering argument across deep gates. (a) does not attempt to.

---

## (b) The L² analogue for tail measures

Here ν = ν_{N₀} is the law of X = Σ_{n≥N₀} ε_n x_n with x_n = n!/p^{e₀} and e₀ = v_p(N₀!). Write l_n = v_p(x_n) and n_k = #{n : l_n < k}. The shells are T(k) (L¹, as in §10.4) and Q(k) (L²). ν_fact := ν₀ (N₀ = 0, elements 0!, 1!, 2!, …) is the *factorial measure*.

**Proposition B1 (L² = collision count; positive measure) [proved].**
- (i) L2(K) := Σ_{k≤K} Q(k) = p^K Coll_K/4^{n_K} − 1, where Coll_K = #{(S,S') ⊆ {n : l_n<K}² : Σ_S x ≡ Σ_{S'} x (mod p^K)}.
- (ii) At least p^K/(1 + L2(K)) residues mod p^K are finite subset sums.
- (iii) If L2(∞) := sup_K L2(K) < ∞, then ν is absolutely continuous with density in L²(Z_p), and the tail set E_{N₀} has Haar measure ≥ p^{−e₀}/(1 + L2(∞)).

*Proof.*
- (i) is Fact F1: elements of level ≥ K vanish mod p^K.
- (ii) If ν_K denotes the law mod p^K, then by Cauchy–Schwarz 1 ≤ |supp ν_K|·Σ_r ν_K(r)² = |supp ν_K|(1 + L2(K))/p^K.
- (iii) By Plancherel on Z_p, Σ_{ξ∈Q_p/Z_p}|ν̂(ξ)|² < ∞ gives an f ∈ L² with f̂ = ν̂, so ν = f dλ.
  - supp ν is closed, so λ(supp ν) = lim_K |supp ν_K|/p^K ≥ 1/(1 + L2(∞)).
  - supp ν_K is the set of residues of finite subset sums, and E_{N₀} = p^{e₀} supp ν. ∎

By Proposition 3.13(c), ν is of pure type. So "L2(∞) < ∞" decides the dichotomy in favour of absolute continuity. Positive measure does not imply fullness. At p = 3 the tails E_N with 81 | N miss classes (Theorem 3.11), while B3 suggests that the L² mass of the tail from 3 stays bounded [heuristic].

**B2 (random-model budgets; constants computed with intervals) [the constants are proved bounds; their relevance is heuristic].** Replacing each factor by its mean (E cos² = 1/2, E|cos| = 2/π) gives budgets with U_d as above (`budgets.py`):

| p | 3 | 5 | 7 | 11 | 13 | 17 | 19 | 23 |
|---|---|---|---|---|---|---|---|---|
| Λ_p = Σ N_d(2/π)^{U_d} (L¹, Thm 10.16) | ∞ | 1.2437 | 0.3632 | 0.07538 | 0.03514 | 0.007473 | 0.003393 | 0.000679 |
| Λ'_p = Σ N_d 2^{−U_d/2} (Cauchy–Schwarz) | ∞ | ∞ | 2.0496 | 0.2920 | 0.1549 | 0.04638 | 0.02553 | 0.007657 |
| Λ2_p = Σ N_d 2^{−U_d} (L² mass) | 0.5881 | 0.1486 | 0.04959 | 0.004910 | 0.001468 | 1.22e-4 | 3.43e-5 | 2.62e-6 |

Since v_p(i!) = (i − s_p(i))/(p−1) ≤ (i−1)/(p−1), we have U_d ≥ (p−1)d + 1. Hence:
- the L² series converges for every p ≥ 3 (ratio p/2^{p−1} < 1);
- Λ'_p ≤ 2^{−1/2} r/(1−r) with r = p·2^{−(p−1)/2}. Since r is decreasing for p ≥ 3 and r ≤ 11/32 for p ≥ 11, this gives Λ'_p ≤ 0.371 < 1 for every p ≥ 11;
- for p = 3, 5 the series Λ'_p diverges. Indeed s_p(i) ≤ (p−1)(1 + log_p i) gives U_d ≤ (p−1)(d + 2 + log_p(pd)), so the terms are ≥ c·r^d·d^{−O(1)}, and r = p·2^{−(p−1)/2} > 1 for these p;
- Λ'_7 = 2.0496 (2.04957; 2.0509 is the upper end of the D = 60 enclosure; corrected after the check).

**So Λ'_p < 1 exactly for p ≥ 11 [proved].** The L¹ series diverges at p = 3, and its sum exceeds 1 at p = 5. **So in the random model, positive Haar measure of the tails is expected at every odd p, but fullness only for p ≥ 7.** That is consistent with Theorem 3.11 at p = 3.

**B3 (certified L² shells at small levels) [computer-assisted].** Exact collision counts were computed by subset-sum counting modulo two 62-bit primes with Chinese remaindering (`l2_dp.py`). The L² shells were also enclosed independently on the frequency side (`ivshell.c`, column T2). Where both exist they agree to all printed digits.

| p | N₀ | levels K | L2(K_max) | max_k Q(k)/(N_k 2^{−n_k}) (level) | random-model mass Σ_k N_k 2^{−n_k} over the same levels |
|---|---|---|---|---|---|
| 3 | 3 | 1–15 | 0.33121 | 1.55 (k = 11) | 0.895 |
| 3 | 0 | 1–15 | 0.18474 | 2.58 (k = 12) | 0.585 |
| 5 | 5 | 1–10 | 0.041554 | 2.12 (k = 7) | 0.151 |
| 5 | 0 | 1–10 | 0.057244 | 3.27 (k = 8) | 0.149 |
| 7 | 7 | 1–8 | 0.014957 | 4.84 (k = 7) | 0.0496 |
| 7 | 0 | 1–8 | 0.014904 | 2.47 (k = 8) | 0.0496 |
| 11 | 11 | 1–7 | 1.44014e-3 | 0.50 (k = 5) | 4.9e-3 |
| 11 | 0 | 1–7 | 1.43847e-3 | 0.29 (k = 1) | 4.9e-3 |
| 13 | 13 | 1–6 | 2.25377e-5 | 0.22 (k = 2) | 1.5e-3 |
| 13 | 0 | 1–6 | 2.20604e-5 | 0.12 (k = 3) | 1.5e-3 |

Logs: `b_l2dp_p{p}_N{N0}.log` (per-level n_K, L2(K), Q(K), Q/random, √(N_KQ(K))). Total wall time 524 s. The exact counts agree with I1's T2 enclosures wherever both exist: N₀ = p in `e_ivshell_*`, and N₀ = 0 in `b_ivshell_fact_p*_N0.log`.

*Observations* [the values are certified; the extrapolations are heuristic]:
- The L² mass grows only at gate-owned levels. These are the levels k with n_k = n_{k−1}, e.g. p = 3, k = 3, 7, 11, 12, and p = 5, 7, k = 7. In between it is essentially constant.
- At p = 3 the jumps shrink: +0.233, +0.029, +0.011, +0.011 at k = 3, 7, 11, 12. L2(15) = 0.331 for the tail from 3. This is consistent with L2(∞) < ∞, i.e. with positive Haar measure of the tail set at p = 3. If L2(∞) is close to the computed 0.33, then B1(iii) gives λ(E_3) ≥ 3^{−1}/1.34 or so, even though tails E_N with 81 | N are never full (Theorem 3.11).
- At p = 11 and 13, every computed level of the factorial measure ν_fact lies below the random model (ratio ≤ 0.29 and ≤ 0.13). So the low-level part of (H2) in Theorem B5 holds with C = 1 on all computed levels. At p = 5 and 7 the gate levels exceed the random model by factors up to 3.3 and 4.8.

**Proposition B4 (the low levels of every RMF window are the factorial measure) [proved].** Let t ≥ 2, H = p^{t−1}, K' arbitrary, and W = W_t(K') the window of length H ending at p^tK'. For 1 ≤ d ≤ t−1:
  S_d(W) = T_fact(d) := Σ_{u∈(Z/p^d)^×} ∏_{i≥0, v_p(i!)<d} |cos(π u i!/p^d)|,  Q_d(W) = Q_fact(d).

*Proof.*
- By Lemma 10.11(a), y_i ≡ ∏_{s≤i}(s − p^{t−1}) ≡ i! (mod p^d), because p^d | p^{t−1}.
- Factors with p^d | i! equal 1.
- Every i with v_p(i!) < d satisfies i < U_d ≤ pd ≤ p^{t−1} = H, so it belongs to the window. ∎

**B4-data (certified shells of the factorial measure) [computer-assisted].** `ivshell.c` (mode `fact p 0 k`; logs `b_ivshell_fact_p{7,11,13}_N0.log`) gives the L¹ shells T_fact(d) with interval enclosures. Its L² column agrees with the exact counts of `l2_dp.py` (N₀ = 0) to all printed digits. Upper bounds, and the ratio to the random model N_d(2/π)^{U_d}:

| p | d = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | Σ (computed levels) | random Σ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 7 | 0.2031 (0.80) | 0.0554 (0.73) | 0.0124 (0.55) | 0.0113 (1.70) | 6.93e-4 (0.35) | 8.80e-4 (1.51) | 2.79e-4 (1.61) | 1.89e-3 (1.56) | 5.20e-4 (1.44) | 0.28644 | 0.36303 |
| 11 | 0.06037 (0.87) | 6.11e-3 (1.15) | 2.84e-4 (0.69) | 2.25e-5 (0.72) | 1.83e-6 (0.77) | 6.87e-7 (3.75) | 1.27e-8 (0.90) | | | 0.066792 | 0.07538 |
| 13 | 7.80e-3 (0.23) | 4.40e-4 (0.35) | 6.64e-5 (1.46) | 1.09e-7 (0.065) | 6.28e-9 (0.10) | 5.18e-10 (0.23) | 5.16e-11 (0.63) | | | 0.0083017 | 0.03514 |

By B4, these numbers bound the levels d ≤ min(t−1, d_max) of every RMF window, for every t and every K'. For example, at p = 13 the levels d ≤ min(t−1, 7) of any window of length 13^{t−1} carry L¹ mass ≤ 8.302·10⁻³. So the K'-free part of RMF holds on all computed levels, with per-level constant ≤ 1.70 (p = 7), ≤ 3.75 (p = 11) and ≤ 1.46 (p = 13). The overall ratio is 0.79, 0.89 and 0.24 respectively. As a by-product, by Fact F1, every residue class mod 7⁹, 11⁷ and 13⁷ has the form Σ_{i∈B} i! for a finite B ⊆ Z_{≥0}.

**Corollary B4' (RMF already contains a fullness statement) [proved].** If RMF(p,C) of Theorem 10.16 holds with CΛ_p < 1, then Σ_{d≥1}T_fact(d) ≤ CΛ_p < 1. Hence ν_fact has full support: every x ∈ Z_p is Σ_{i∈B} i! for some B ⊆ N.

The same conclusion follows from the L² hypothesis of Theorem B5, with √C Λ'_p < 1.

*Proof.*
- RMF bounds Σ_{ξ≠0} of the window by C(Λ_p + τ_p(t)). By B4, the part over levels d ≤ t−1 equals Σ_{d≤t−1}T_fact(d).
- Let t → ∞. Note τ_p(t) → 0 for p ≥ 5 (Theorem 10.16's proof).
- Fact F1 at every modulus, and compactness (as in Theorem 10.18), give full support. ∎

So the hypothesis of Theorem 10.16 contains an MI-type inequality (Conjecture 10.22) for the measure started at 0! instead of 13!. Theorems 10.16 and 10.18 therefore rest on the same kind of inequality. Is fullness of ν_fact alone useful for Q3? Not by itself, since 0 is not a natural starting point. This is a structural remark, not a reduction.

**Theorem B5 (collision-count version of Theorem 10.16) [proved; the hypothesis is unproved].** Let p ≥ 7. Assume:
- **(H1)** Cov(p,1,H₁) and Cov(p,2,H₂) hold with H_t + 1 < p^t.
- **(H2)** For some C, every t ≥ 3 and every unit K' mod p^{c_t} (c_t = v_p((p^{t−1}−1)!)), the window W = W_t(K') of length p^{t−1} satisfies Q_d(W) ≤ C·N_d·2^{−n_d} for 1 ≤ d ≤ t + c_t, where n_d = #{i < p^{t−1} : v_p(i!) < d}.
- **(H3)** √C·(Λ'_p + τ'_p(3)) < 1, where τ'_p(t) := p^{t+c_t}·2^{−p^{t−1}/2}.

Then UC(p) holds. Hence f(1,p) = ∞, and Q3 has a positive answer.

(H3) can hold only for p ≥ 11, since Λ'_7 = 2.05. It allows C < 11.7 at p = 11 and C < 41.7 at p = 13. For comparison, Theorem 10.16 allows C < 13.3 and C < 28.5 for its L¹ ratio.

*Proof.*
- By Fact F2 and (H2), Σ_{ξ≠0}|ν̂_W(ξ)| ≤ Σ_d √(N_d Q_d) ≤ √C Σ_{d≤t+c} N_d 2^{−n_d/2}.
- As in Theorem 10.16, n_d = U_d for d ≤ c_t and n_d = p^{t−1} for c_t < d ≤ t + c_t. (By Proposition 10.15(i), v_p(y_i) = v_p(i!).) So the sum is ≤ √C(Λ'_p + τ'_p(t)).
- τ'_p(t+1)/τ'_p(t) = (p·2^{−(p−1)/2})^{p^{t−1}} < 1 for p ≥ 7, because c_{t+1} − c_t = p^{t−1} − 1. So τ'_p(t) ≤ τ'_p(3) for t ≥ 3.
- By Fact F1, Cov(p,t,p^{t−1}) holds for all t ≥ 3, and H_t := p^{t−1} satisfies H_t + 1 < p^t.
- Theorem 3.12(c) now gives UC(p), f(1,p) = ∞ and Q3. ∎

*How this sits with the obstructions.*
- Theorem B5 is a reduction, like Theorem 10.16. It proves nothing about Q3 unless (H2) is proved.
- By B4, (H2) at levels d ≤ t−1 is a single K'-free family of counting statements: the factorial measure's L² shells are bounded by C·N_d2^{−U_d}. The K'-dependent part lives at levels t ≤ d ≤ t+c_t.
- By B6, no proof of (H2) can use only boundedly many digits of the unit parts (Theorem 3.10).
- By B7, no proof of (H2) can go through a supremum-type renormalisation bound (Corollary 10.20).

**Proposition B6 (L² barrier lemma) [proved].** Let W = [pM₀, pM₁) be a run of full blocks whose last block is a gate of level j. Use the notation of Theorem 3.10: weights w_n ≤ w_max, demand D = w_max + j + 1, and truncations y_n = p^{w_n}ρ_n with ρ_n ∈ [1, p^c) the unit part reduced mod p^c. Then the uniform measure on subset sums of (y_n) mod p^D has
  Σ_{0≠ξ mod p^D} |ν̂_y(ξ)|² ≥ ((p−1)/2)·p^{j−c−1} − 1.

In particular, take M₀ = 1, so W runs from p to a level-j gate. Then any bound for the L² mass of the tail measure ν_p that is derived only from the valuations and c digits of the unit parts is ≥ ((p−1)/2)p^{j−c−1} − 1. This is unbounded as j → ∞. **A uniform L² bound needs unboundedly many digits of the unit parts (of Morita's Γ_p).**

*Proof.*
- Every subset sum is an integer in [0, X] with X ≤ (p^c−1)·p·(p^{w_max+1}−1)/(p−1) < p^{a}/(p−1), where a = w_max + c + 2. (Each block has p elements of one weight, and distinct blocks have distinct weights.)
- So the support has at most X + 1 ≤ 2p^a/(p−1) points.
- By Cauchy–Schwarz, Σ_r ν_y(r)² ≥ (p−1)/(2p^a). Hence p^DΣν_y² − 1 ≥ ((p−1)/2)p^{D−a} − 1, and D − a = j − c − 1.
- For M₀ = 1, the elements of the tail ν_p of level < D are exactly the elements of W: the block after the gate starts at level w_max + j + 1 = D. ∎

**Proposition B7 (exact L² renormalisation; supremum-type L² bounds) [proved].** Assume W is attained, as in Proposition 10.19, and keep its notation (N_W, a, x'_n = n!/N₀!). Put
  G(θ)² = ∏_{N₀≤n<N_W} cos²(πθx'_n),  H^{(2)}_W(θ) = Σ_{s mod p^W} G(θ+s/p^W)².
Then:
- (i) Q_{N₀}(k) = Σ_{w∈(Z/p^{k−W})^×} |ν̂_{N_W}(w/p^{k−W})|² · H^{(2)}_W(w a^{−1}/p^k).
- (ii) H^{(2)}_W(θ) = p^W 4^{−n} Σ_{(S,S'): p^W | Δ} e(θΔ), where Δ = Σ_S x' − Σ_{S'} x' and n = N_W − N₀. This is a trigonometric polynomial with nonnegative coefficients, so sup H^{(2)}_W = H^{(2)}_W(0) = p^W·P(p^W | Z_bot) = 1 + (L² mass of the bottom W levels) ≥ 1.
- (iii) Consequently the supremum-type bound Q_{N₀}(k) ≤ (sup H^{(2)}_W)·Q_{N_W}(k−W) has step factor ≥ 1 and cannot give decay when iterated.
- (iv) Expanding H^{(2)} in (i) gives the exact positive formula
  Q_{N₀}(k) = p^W 4^{−n} Σ_{(S,S'): p^W|Δ} [q·P(Z_top ≡ −a^{−1}Δ/p^W (mod q)) − (q/p)·P(Z_top ≡ −a^{−1}Δ/p^W (mod q/p))],
  where q = p^{k−W} and Z_top is the lazy difference for the tail from N_W.

So in L² the "decorrelation" that Corollary 10.20 requires is the following: the bottom near-collisions Δ/p^W must not concentrate where the top collision density is large.

*Proof.* (i) is the proof of Proposition 10.19 with cos² in place of |cos|; that proof uses nothing else about the factor. (ii) follows from cos²(πx) = (2+e(x)+e(−x))/4 and Σ_{s mod p^W} e(sΔ/p^W) = p^W 1[p^W|Δ]. For (iv), substitute (ii) into (i) and use Σ_{w mod q}|ν̂_top(w/q)|² e(wm/q) = q·P(Z_top ≡ −m mod q); the non-unit w are subtracted as in A2(i). ∎

In L² the supremum is attained exactly at 0. In L¹ (Corollary 10.20) it was reached only in the limit, by continuity.

**B8 (exact gate identity, and what a proof of bounded L² must show) [identity proved; the requirement is a reformulation].**
- Let a level-j gate block sit at relative level e, and condition on p^e | Z_< (the elements below the gate collide mod p^e).
- Let χ be the conditional law of the collision carry C = Z_</p^e mod p^{j+1}.
- Let D_Γ = Σ_r δ_r σ_r be the gate block's lazy difference; by Lemma A1 its law mod p^{j+1} is fixed, up to a unit U.

Then
  p^{e+j+1}P(p^{e+j+1} | Z_{≤gate}) = p^e P(p^e | Z_<) · [1 + Σ_{0≠w mod p^{j+1}} F_p(wU/p^{j+1})² χ̂(w)].

By Theorem A2, Σ_{w≠0}F_p² ≈ (3/2)2^{−p}p^{j+1}. So if C is concentrated (χ̂ ≈ 1), the bracket is of order 2^{−p}p^{j+1}, which is unbounded in j. By Cauchy–Schwarz the bracket is ≤ 1 + (Σ_{w≠0}F_p⁴)^{1/2}·(L² mass of χ)^{1/2}. A uniform L² bound therefore requires the collision carry entering every deep gate to be equidistributed mod p^{j+1} in L², with an error that decays with j. That carry is determined by the lower shells, so the requirement is circular. By B6 it cannot be established from boundedly many unit digits.

---

## (c) Averaging over K'

Fix (p, t, H) with c = v_p((H−1)!) ≤ t and M = t + c. Let y_i(K') = ∏_{s≤i}(p^tK' − (H−s)), σ_i = y_i(0) = (−1)^i(H−1)!/(H−1−i)!, and τ_i = y_i'(0) = −σ_i Σ_{s≤i} 1/(H−s) ∈ Z.

**C1 (linearisation) [proved].** y_i(K') ≡ σ_i + p^tK'τ_i (mod p^{t+c}).

*Proof.* In the expansion of y_i as a polynomial in X = p^tK' with integer coefficients, the terms with X^k, k ≥ 2, are divisible by p^{2t}, and p^{t+c} | p^{2t}. (`kavg_l2.py` also checks this for every class.) ∎

**C2 (K'-averaged L² = 2D collision counts) [proved].** Let δ ∈ {−1,0,1}^H be the lazy difference (P(0) = 1/2, P(±1) = 1/4), A = Σδ_iσ_i and B = Σδ_iτ_i. Let K' be uniform mod p^c. Then for d ≤ t,
  E_{K'}[p^d P(Σδ_iy_i(K') ≡ 0 (mod p^d))] = p^d P(p^d | A),
which is K'-independent. For d = t + s with 1 ≤ s ≤ c,
  E_{K'}[p^{t+s} P(Σδ_iy_i(K') ≡ 0 (mod p^{t+s}))] = p^t E_δ[p^{v_s} 1(p^{t+v_s} | A)],  v_s = min(v_p(B), s).

Equivalently, on Fourier transforms, E_{K'}|ν̂_{K'}(u/p^{t+s})|² = E_δ[e(uA/p^{t+s})·1(p^s | B)]. **Averaging over K' projects the twisted walk onto the sublattice where the twist B vanishes mod p^s.** For L¹ there is no such identity. One only has E_{K'}S_d ≤ √(N_d E_{K'}Q_d), by Fact F2 and Jensen.

*Proof.* Expand E_{K'}e(ξ(A + p^tK'B)) = e(ξA)·1[p^s | B] for ξ of order p^{t+s} (K' runs over all residues mod p^c ⊇ mod p^s). Then sum over ξ of order ≤ p^{t+s}. Alternatively, count K' mod p^c with A + p^tK'B ≡ 0 (mod p^{t+s}): there are p^{c−s+v_s}·1(p^{t+v_s}|A) of them. ∎

`kavg_l2.py` checks the full-sum version of C2 exactly, against per-class enumeration, in every case where both were computed (identity "equal: True" in `c_kavg_p7.log`).

**C3 (proportion of non-covering classes) [proved].** Let φ = #{unit classes}. Then
  #{unit K' : the window does not cover}/φ ≤ Σ_{d=1}^{M} √(N_d · E_{K' unit} Q_d(K')),
and E_{unit} ≤ (p^c/φ)E_{all K'}, which is computable from C2 alone.

*Proof.*
- For each K', L¹(K') ≤ Σ_d √(N_dQ_d(K')) by Fact F2. If L¹(K') < 1, then K' covers (Fact F1).
- So #fail ≤ Σ_{K'} L¹(K') ≤ Σ_d √N_d Σ_{K'}√(Q_d(K')) ≤ Σ_d √N_d √(φ Σ_{K'}Q_d(K')), by Cauchy–Schwarz over K'. ∎

**C4 (tables) [computer-assisted; exact integer counts].** `kavg_l2.py`: per-class subset-sum counts mod p^M (int64, exact, H ≤ 61), exact sums of squares with 16-bit limbs, and per-level folding.

Logs: `c_kavg_p{p}_t{t}_H{H}.log` (total wall time 1130 s). Columns: c = v_p((H−1)!); "units" is the number of unit classes K' mod p^c; "failing" is the exact number of non-covering classes; "C3" is the bound of C3 on the proportion of failing classes; "C–S cert." is the number of classes with Σ_d √(N_dQ_d(K')) < 1; the last column compares max_{K'} L2(K') with p^{−M}, the Parseval certificate threshold. Minimal covering lengths (note §10.2): H₂ = 7, H₃ = 19 at p = 7; H₂ = 10, H₃ = 19, H₄ = 24 at p = 13.

| p | t | H | c | units | failing (exact) | C3 bound | C–S cert. | max L2 vs p^{−M} |
|---|---|---|---|---|---|---|---|---|
| 7 | 2 | 7 | 0 | 1 | 0 | 2.32 | 0/1 | 0.113 vs 0.0204 |
| 7 | 2 | 12 | 1 | 6 | 0 | 3.29 | 0/6 | 0.062 vs 0.0029 |
| 7 | 2 | 14 | 1 | 6 | 0 | 1.64 | 0/6 | 0.026 vs 0.0029 |
| 7 | 2 | 20 | 2 | 42 | 0 | 1.94 | 0/42 | 0.028 vs 4.2e-4 |
| 7 | 2 | 21 | 2 | 42 | 0 | 1.49 | 10/42 | 0.021 vs 4.2e-4 |
| 7 | 3 | 19 | 2 | 42 | 0 | 22.3 | 0/42 | 0.089 vs 6.0e-5 |
| 7 | 3 | 21 | 2 | 42 | 0 | 11.2 | 0/42 | 0.034 vs 6.0e-5 |
| 7 | 3 | 28 | 3 | 294 | 0 | 7.19 | 0/294 | 0.018 vs 8.5e-6 |
| 11 | 3 | 18 | 1 | 10 | 0 | 30.9 | 0/10 | 0.094 vs 6.8e-5 |
| 13 | 2 | 10 | 0 | 1 | 0 | 4.22 | 0/1 | 0.112 vs 0.0059 |
| 13 | 2 | 19 | 1 | 12 | 0 | 2.87 | 0/12 | 0.056 vs 4.6e-4 |
| 13 | 2 | **26** | 1 | 12 | 0 | **0.179** | **12/12** | **5.9e-5 vs 4.6e-4** |
| 13 | 2 | 30 | 2 | 156 | **156** | 2.84 | 0/156 | 0.42 vs 3.5e-5 |
| 13 | 2 | **35** | 2 | 156 | 0 | **0.142** | **156/156** | 1.6e-4 vs 3.5e-5 |
| 13 | 2 | **39** | 2 | 156 | 0 | **0.051** | **156/156** | **2.4e-5 vs 3.5e-5** |
| 13 | 3 | 19 | 1 | 12 | 0 | 35.2 | 0/12 | 0.104 vs 3.5e-5 |
| 13 | 3 | 26 | 1 | 12 | 0 | 3.27 | 0/12 | 1.0e-3 vs 3.5e-5 |
| 13 | 3 | 30 | 2 | 156 | **156** | 12.5 | 0/156 | 0.42 vs 2.7e-6 |
| 13 | 3 | 35 | 2 | 156 | 0 | 1.89 | 0/156 | 2.2e-4 vs 2.7e-6 |
| 13 | 3 | 39 | 2 | 156 | 0 | 0.442 | 154/156 | 2.8e-5 vs 2.7e-6 |
| 13 | 4 | 24 | 1 | 12 | 0 | 129 | 0/12 | 0.100 vs 2.7e-6 |
| 13 | 4 | 32 | 2 | 156 | 0 | 92.8 | 0/156 | 0.057 vs 2.1e-7 |
| 13 | 4 | 39 | 2 | 156 | 0 | 8.46 | 0/156 | 1.0e-4 vs 2.1e-7 |

(Also run: (7,3,20) and (7,3,26), with the same pattern; see the logs.)

*What the table shows.*
- **(i)** The averaged identity C2 holds exactly ("equal: True" in all 10 p = 7 runs, where the 2D-walk formula was evaluated independently).
- **(ii)** The exact failing counts reproduce the layer obstruction of Lemma 10.11. H = 30 at p = 13 has (H−1) mod 13 = 3 < ρ₀(13) = 5, and all 156 classes fail at t = 2 and t = 3.
- **(iii)** At the minimal covering lengths H_t, every averaged or L² bound is vacuous (C3 ≥ 2.3).
- **(iv)** Pure collision-count certificates do work once H is about 2–2.6 times H_t.
  - At p = 13, t = 2, H = 26, all 12 classes are certified by per-class Cauchy–Schwarz, and also by Parseval (max L2 < p^{−M}). The averaged C3 bound alone gives proportion ≤ 0.179.
  - At H = 35 and 39, all 156 classes are certified. At H = 39, Parseval certifies them too, and C3 alone gives ≤ 0.051.
  - At t = 3, H = 39 (≈ 2H₃), 154 of 156 classes are certified.
  - At t = 4, H ≤ 39 (≤ 1.6H₄), none are.
- At (13,4,32) the bottleneck is visible at level 1: E Q₁ = 0.054, because only ρ+1 = 6 of the elements are units (Lemma 10.11(d)). At large H the top level is the bottleneck: at (13,4,39), √(N₆EQ₆) ≈ 7.8.

**C5 (what averaging can and cannot feed) [negative].**
- Proposition 10.10 needs a covering window at *every* first-failure position p^tK''. Theorem 10.16 needs its Fourier bound for *every* K'.
- An averaged statement "all but a proportion ε_t of classes" says nothing about a prescribed position unless ε_tφ < 1, i.e. unless it certifies every class.
- The C3/C2 bounds certify a class only if Σ_d √(N_dQ_d) < 1. At the top level (d = M, n_M = H) this needs N_M 2^{−H/2} ≲ 1, i.e. H ≳ 2M log₂ p: about twice the counting threshold of Cov.
- In C4, every averaged or L² bound is vacuous at the actual minimal covering lengths H_t. Collision-count certificates appear only at H ≈ 2–2.6·H_t: all classes at (13,2,26), (13,2,35) and (13,2,39); 154/156 at (13,3,39); none at t = 4 for H ≤ 39.
- The averaged L² of C2 does give exact access to the K'-structure. The twist τ enters only through the event p^s | B.

So, in the precise sense above, averaging over K' cannot by itself feed Proposition 10.10 or Theorem 10.16. A measure-theoretic use (positive measure of K_p, note §10.6 item 4) would need a population argument, which was not attempted.

---

## (d) The factorial-base transfer picture

**D1 (Poisson decomposition; the continuous transfer operator is the j = 0 term) [proved].** Let x₀ | x₁ | ⋯ | x_{n−1} be positive integers with ratios m_i = x_i/x_{i−1}, and F(θ) = ∏_i |cos(π θ x_i)|. Then for every M ≥ 1,
  (1/M)Σ_{r mod M} F(r/M) = (2/π)^n Σ_{j∈Z} Ψ(jM),
where Ψ(s) = Σ_{k: Σk_ix_i = s}∏b_{k_i}. Ψ is computed by the carry recursion of A4 (start from the element with coefficient 1; at each step k = s − m s').

The j = 0 term is (2/π)^nΨ(0) = ∫₀¹F. It is exactly what the continuous factorial-base transfer operator computes: Proposition 10.21's recursion θ_{m} = (d + θ_{m+1})/(m+1), as used in `lead_hmean.py` and by the round-2 computational referee. Indeed, on Fourier coefficients, (L_m g)(y) = (1/m)Σ_{a<m} g((y+a)/m) acts by ĝ ↦ ĝ(m·), and multiplication by (π/2)|cos πy| acts by convolution with b. So the forward carry recursion is the transfer operator in Fourier variables.

On the grid G_M = M^{−1}Z/Z with gcd(m, M) = 1, multiplication by m is a bijection. So the discrete operator selects one preimage (y + a)/m instead of averaging over all m preimages: for y = v/M one needs m | aM + v, i.e. a ≡ −v·M^{−1} (mod m). The difference is the aliasing Σ_{j≠0}.

*Proof.* As in Theorem A4(i),(iii). ∎

**D2 (for the tail shells, the whole deviation from the random model is aliasing) [computer-assisted illustration].** `cont_vs_grid.py` computes Ψ(0) for the chains x'_n = n!/N₀!, N₀ ≤ n < N_k. Results:
- p = 13, k ≤ 7: Ψ(0) ∈ [0.99991, 1.00013];
- p = 11, k ≤ 8: Ψ(0) ∈ [0.99978, 1.00005].

So the continuous transfer value (p^k−p^{k−1})∫F_k equals the random model N_k(2/π)^{n_k} to within 2.2·10⁻⁴ relative. The certified shells T(k) of (e) differ from it by the following factors.
- p = 13, k = 1…7: 0.230, 1.208, 0.0824, 0.0620, 0.145, 0.519, 0.0728.
- p = 11, k = 1…8: 0.867, 1.160, 0.661, 0.718, 4.16, 0.655, 2.37, 3.01.

(Ψ(0) is computed in floating point with carries truncated at 300. With multipliers ≥ 12 the neglected mass is negligible, but this computation is not interval-certified, and only the illustration depends on it.)

*Consequence.*
- For the tail measures the grid modulus p^k is minute compared with the oscillation scale N_k!/N₀!. The archimedean main term is the random model.
- Whether MI-13 (Conjecture 10.22) holds is decided entirely by the aliasing sums Σ_{j≠0}Ψ(jp^k). These are signed weighted counts of integer relations Σk_n x'_n = j p^k with j ≠ 0, a p-adic quantity.
- This sharpens Corollary 10.20. Supremum-type transfer bounds fail, and moreover even the exact continuous transfer value carries no information beyond the random model. Single gate blocks (A4) are the opposite regime: there the aliasing vanishes as d → ∞.

**D3 (a rigorous bound without a supremum over phases) [proved; numbers computer-assisted].** By Fact F2, Σ_{ξ≠0} ∏_j|cos(πξy_j/p^M)| ≤ Σ_{d=1}^{M} √(N_d Q_d), where Q_d = p^d P_d − p^{d−1}P_{d−1} and P_d is the probability that the lazy difference walk hits 0 mod p^d. This is an exact collision count, and no phase supremum is taken. For the tail from 13 it gives Σ_{k≤7}√(N_kQ(k)) ≤ 0.0252427, against the certified L¹ value 0.0092988 (factor 2.71). For the tail from 11 it gives Σ_{k≤8} ≤ 0.143641, against 0.0668545 (factor 2.15) (`d3_cs_p13.log`, `d3_cs_p11.log`; the Q(k) are I1's certified T2 upper bounds). So L² shells alone, with no phase supremum, prove the equidistribution of Corollary 10.17 with |θ_y| ≤ 0.0253 (p = 13) and ≤ 0.144 (p = 11). For p = 13, k ≤ 6, these L² shells are also exact collision counts (B3). The per-level loss grows with the level: at p = 13 it is 2.1 at k = 1 and 626 at k = 7, in line with (π/(2√2))^{n_k}.

**D4 (limits of counting bounds) [proved].**
- (i) (Lyapunov) (E|cos πU|^{2m})^{1/(2m)} ≥ (E cos²)^{1/2} = 2^{−1/2} > 2/π for every m ≥ 1. So, measured in the random model, any Hölder or even-moment bound loses at least (π/(2√2))^{n_d} ≈ 1.111^{n_d} at level d against the L¹ random model. Cauchy–Schwarz loses exactly this.
- (ii) More generally, let g(x) = A₀ + Σ_{k≥1}A_k cos(2kx) be a trigonometric polynomial with A_k ≥ 0 for all k (positive definite) and g ≥ |cos x| on R. Replacing |cos| by g turns the L¹ shell into a positive weighted relation count:
  Σ_ξ ∏_i g(πξy_i/p^M) = p^M Σ_{k: Σk_iy_i≡0} ∏ ĝ(k_i).

  Every such g has A₀ ≥ 2/π + 2/(15π) = (16/15)(2/π) ≈ 0.6791. The tangent-line majorant g = 2^{−1/2}(1 + cos(2x)/2) has A₀ = 2^{−1/2} ≈ 0.7071, and it corresponds to Cauchy–Schwarz.

*Proof of (ii).* Let φ(x) = 1 − cos 4x ≥ 0, with mean 1 over a period. Then mean(gφ) = A₀ − A₂/2 ≤ A₀. Since g ≥ |cos| and φ ≥ 0, mean(gφ) ≥ mean(|cos|φ) = 2/π − (1/2)·(4/π)(−1)/15 = 2/π + 2/(15π). (Here (4/π)(−1)^{k+1}/(4k²−1) is the cos(2kx) coefficient of |cos x|.) ∎

*Consequence.*
- The best per-element constant of positive-definite majorant methods lies in [0.6791, 0.7072], strictly above 2/π = 0.6366.
- With 0.7071 the budget Λ'_p is < 1 only for p ≥ 11 (B2). With the lower-bound constant 0.6791, the corresponding budget Σ_d N_d·0.6791^{U_d} would be 0.800 at p = 7, still diverges at p = 5, and is 0.168 at p = 11 (interval evaluation with `budgets.budget`). So D4(ii) does not exclude the counting route at p = 7. Whether some positive-definite majorant actually reaches a constant with budget < 1 at p = 7 is open.
- The L¹ random model itself, i.e. the constant 2/π, is out of reach of every positive-count method of this type.

---

## (e) Interval-arithmetic re-run of all certified shell sums of §10.4.1 [computer-assisted]

**Cost estimate (done first).** Round 2's `fl1` ran in 8 s (p=13, k≤7) and 20 s (p=11, k≤8). `iv_shells.py` (mpmath iv) was too slow beyond k = 4 or 5. An interval version in C with directed rounding was estimated at 5–10× `fl1`; it took 35 s and 101 s. A Python/MPFR implementation was estimated at about 3 and 10 minutes; it took 190 s and 661 s. The budget allowed every shell, so every shell was certified.

**Implementation I1: `ivshell.c`.**
- C, entirely in FE_UPWARD. Downward operations are written as negated upward operations. A start-up self-test checks the rounding mode.
- π is enclosed by the two doubles adjacent to it. The phase is r/M with r ≤ M/2 exact.
- cos is enclosed via alternating Taylor partial sums S₁₀ ≥ cos ≥ S₁₁, valid on [0, 1.58] because the terms decrease. Even and odd terms are rounded in opposite directions.
- Products and sums of lower and upper bounds use directed rounding. The program uses a depth-first search over p-adic digits as in `fl1`, without pruning, and outputs enclosures [lo, hi] of T1 (L¹) and T2 (L²).
- Built twice: gcc 13.3 `-O2 -frounding-math -fno-fast-math`, and clang 18.1 `-O2 -frounding-math -ffp-model=strict`. Both builds give identical output.
- A later revision added an optional restriction to a range of shells and of lowest digits u₀ (file mode), used to split the p = 13, d = 9 gate shell into six checkpointed chunks. With default arguments its output is byte-identical to the earlier build (checked with `fact 13 13 5`).
- The cos enclosures were validated against mpmath at 60 digits on 21 071 points per build, including the extremes r = 0, 1, M/2: 0 failures, maximal width 2.0·10⁻¹⁵ (`check_cosenc.log`).

**Implementation I2: `shells_mpfr.py`.** It shares no code with I1.
- Python big-integer factorials and full residues x_n mod p^k.
- One table of cosine upper bounds, computed by MPFR via gmpy2: correctly rounded cos with RoundUp, at a RoundDown-enclosed argument, using cos decreasing on [0, π/2].
- numpy float64 products and sums, with the a-posteriori factor (1−2^{−53})^{−(N+n)}, multiplied in exact rationals. Partial products are floored at 2^{−900}, which only increases them and prevents underflow.
- Plain enumeration of units.

**Reference I3: `brute_shells.py`.** mpmath, 40 digits, brute force; used for small cases.

**Validation** (`e_validate_small.log`). On (p,N₀,k_max) = (5,5,5), (7,7,4), (11,11,3), (13,13,3) and (3,3,7), I1's enclosures contain I3's values, I2's upper bounds lie above them, and all three agree to 12–13 significant digits.

**Results** (`e_ivshell_{gcc,clang}_p13_k7.log`, `e_ivshell_{gcc,clang}_p11_k8.log`, `e_mpfr_p13_k7.log`, `e_mpfr_p11_k8.log`):

| k | T_13(k): I1 lower (rounded down) | I1 upper | I2 upper (MPFR) | certified upper |
|---|---|---|---|---|
| 1 | 7.79521409915e-3 | 7.795214099155e-3 | 7.795214099155e-3 | 7.79521409916e-3 |
| 2 | 1.49970737362e-3 | 1.499707373628e-3 | 1.499707373628e-3 | 1.49970737363e-3 |
| 3 | 3.75065312870e-6 | 3.750653128703e-6 | 3.750653128703e-6 | 3.75065312871e-6 |
| 4 | 1.03621943840e-7 | 1.036219438411e-7 | 1.036219438413e-7 | 1.03621943842e-7 |
| 5 | 8.89178677055e-9 | 8.891786770624e-9 | 8.891786770928e-9 | 8.89178677093e-9 |
| 6 | 1.16542593370e-9 | 1.165425933986e-9 | 1.165425934393e-9 | 1.16542593440e-9 |
| 7 | 6.00075987569e-12 | 6.000759881729e-12 | 6.000759916357e-12 | 6.00075991636e-12 |
| **Σ k≤7** | **9.29878581106e-3** | | | **9.29878581108e-3** |

| k | T_11(k): I1 lower (rounded down) | I1 upper | I2 upper (MPFR) | certified upper |
|---|---|---|---|---|
| 1 | 6.03691747281e-2 | 6.036917472815e-2 | 6.036917472815e-2 | 6.03691747282e-2 |
| 2 | 6.18281247616e-3 | 6.182812476169e-3 | 6.182812476169e-3 | 6.18281247617e-3 |
| 3 | 2.69963737679e-4 | 2.699637376799e-4 | 2.699637376798e-4 | 2.69963737680e-4 |
| 4 | 2.24372925073e-5 | 2.243729250739e-5 | 2.243729250741e-5 | 2.24372925075e-5 |
| 5 | 9.95208365731e-6 | 9.952083657409e-6 | 9.952083657521e-6 | 9.95208365753e-6 |
| 6 | 1.20035199814e-7 | 1.200351998220e-7 | 1.200351998394e-7 | 1.20035199840e-7 |
| 7 | 3.31990322869e-8 | 3.319903233566e-8 | 3.319903236666e-8 | 3.31990323667e-8 |
| 8 | 3.23868109389e-9 | 3.238681108484e-9 | 3.238681166924e-9 | 3.23868116693e-9 |
| **Σ k≤8** | **6.68544967910e-2** | | | **6.68544967911e-2** |

(`e_summary_p13.log`, `e_summary_p11.log`, produced by `summarize_e.py`. It asserts that the gcc and clang builds of I1 print identical output, and it rounds the printed decimals outward.) Round 2's table (§10.4.1, floating point with margins) gave upper bounds rounded up in the 5th digit, with totals 9.2988e-3 and 6.6855e-2. Every round-2 entry is ≥ the corresponding certified upper bound here, so every entry of that table is now confirmed in interval arithmetic.

Each certified upper bound in the last row is the larger of I1 and I2, rounded up in the 12th digit. It holds as soon as either implementation is correct. The interval widths of I1 are below 10⁻¹⁶ absolute for the dominant shells. The deepest shells have relative widths up to 1.0·10⁻⁹ (p = 13, k = 7) and 4.5·10⁻⁹ (p = 11, k = 8). These are far from any threshold. **Corollary 10.17 now rests entirely on interval arithmetic: |θ_y| ≤ 0.0093 (p = 13, K ≤ 7) and ≤ 0.0669 (p = 11, K ≤ 8).**

---

## Failed attempts

1. **Level-by-level conditioning for L² (supremum over carries).** Conditioning on everything below a level and taking the supremum over the incoming carry gives P_{l+1}/P_l ≤ max_r P(block sum ≡ r). Each factor is ≥ 1/p, so the normalised factor is ≥ 1. At a level-j gate the factor is ≥ p^{j+1}·P(D_Γ ≡ 0) = p^{j+1}(3/2)2^{−p} for large j, by A2. That is unbounded. *Where it breaks:* it is a supremum-type bound. B7 and B8 show that the needed input is averaging over the carry, which is circular.
2. **Analytic aliasing bound at p = 13, d = 9.** The crude envelope of A4(iii) gives |E'(13⁸)| ≤ 52. That is useless for S₉, so S₉ at p = 13 had to be computed (`gate_d`, about 11 minutes). A sharper envelope that tracks the residue class of the carry would close this gap. The true aliasing at M = 13⁹ is about 10⁻³, estimated from the "pay at the bottom" mechanism [heuristic].
3. **Positive-definite majorants approaching 2/π.** The aim was a family of positive counting bounds converging to the L¹ random model. It fails: D4(ii) gives the barrier 0.6791. The best constant in [0.6791, 0.7072] was not computed, because no LP solver was available (scipy is not installed).
4. **L² covering certificates at the minimal lengths.** Certifying Cov by L²(K') < p^{−M} (Parseval), or by per-level Cauchy–Schwarz, needs H about twice the counting threshold. It fails at every minimal H_t tried (C4). It succeeds only at about 2–2.6·H_t, e.g. for all classes at (p,t,H) = (13,2,26).

## Open issues

- **No uniform-in-level L² or L¹ bound** is known for any factorial tail measure or window. B4 shows that the low levels of RMF are a single counting problem, for the factorial measure ν_fact. B6–B8 show that any proof must use unboundedly many unit digits, and must control carry equidistribution at deep gates by averaging.
- The certified sup in A5 depends on finite computations up to d₀ and on the crude envelope A4(iii) beyond. A sharper envelope would make the computational part trivial.
- B3 suggests L2(∞) < ∞ for the tail from 3 (L2(15) = 0.331, with shrinking jumps at the gates) [heuristic]. If true, that tail set has positive Haar measure. Tails E_N with 81 | N are not full (Theorem 3.11), so at p = 3 positive measure and non-fullness would coexist.
- The best positive-definite majorant constant in D4(ii), and whether it rescues the counting route at p = 7.

## Recommended next steps

1. **The counting problem for ν_fact.** Prove, or refute numerically to higher levels, Q_fact(d) ≤ C N_d 2^{−U_d} uniformly in d. By B4 and B5 this, plus the K'-dependent top levels, is the L² route to UC(p) for p ≥ 11. A natural first case is levels that straddle one level-1 gate: p = 13, d ≈ 12–14, which is beyond exact DP. A Monte Carlo collision estimator would be the tool there.
2. **An annealed L² statement** (average over x ∈ Z_p instead of K'). For x ∈ Z_p let μ_x be the law of Σ_{j≥1}ε_jπ_j(x), and L2_K(x) its L² mass up to level K. Then
   ∫L2_K(x)dx = Σ_δ P(δ)·#{x mod p^K : S_δ(x) ≡ 0 (mod p^K)} − 1,  S_δ = Σ_j δ_jπ_j,
   which is a root-counting problem for the integer polynomials S_δ.
   - If sup_K ∫L2_K < ∞, then L2_K(x) is nondecreasing in K, and Fatou gives sup_K L2_K(x) < ∞ for Haar-a.e. x. Then μ_x has an L² density, and the achievement set {Σ_{j≥1}e_jπ_j(x)} has positive Haar measure, for a.e. x.
   - The §10.1 conditioning on x mod p^{V_n} ("slopes", Lemma 10.5) is the natural tool, as it was for p = 2. This is the L² version of §10.6 item 4, and it sees no particular natural number.
3. **Close A5's gap analytically,** with a residue-class-aware envelope in A4(iii).
4. **Use D4** to look for an optimal positive-definite majorant. If its constant is ≤ about 0.68, the counting route may extend to p = 7.

## Reproduction

All commands were run on 2026-10-13 on the shared machine (4 cores), using one core, under `nice -n 10` (wrapper `code/round3/R3F/run_logged.sh`). Builds (outputs in `/tmp/r3_R3F/`):

```
gcc   -O2 -frounding-math -fno-fast-math -o ivshell_gcc  code/round3/R3F/ivshell.c -lm
clang -O2 -frounding-math -ffp-model=strict -o ivshell_clang code/round3/R3F/ivshell.c -lm
gcc   -O2 -frounding-math -fno-fast-math -o gate_d code/round3/R3F/gate_d.c -lm
gcc   -O2 -frounding-math -fno-fast-math -o jrel   code/round3/R3F/jrel.c -lm
```

*(Lead's note: the track agent was cut off before writing the reproduction table.)* Every log in `data/round3/R3F/` begins with its exact command line and ends with its wall time, so the logs themselves are the reproduction record; the adversarial check rebuilt `ivshell`, `jrel` and `gate_d` and reproduced their logs (`data/round3/checks/R3F.md`).

Software: Python 3 with numpy 2.3.2, gmpy2 2.3.2 (GMP 6.3.0, MPFR 4), mpmath 1.3.0, sympy (primality checks of the CRT moduli).

## Credit

- The problem is due to Erdős and Graham.
- The block lemma and the position-independent programme are due to T. Tao.
- The covering framework (§3.7, Theorem 3.12) and the gate congruence (Theorem 3.9) come from round 1. Theorems 10.16 and 10.18 (and the shell sums of §10.4.1) are from round-2 tracks R2b and R2a. The renormalisation identity (Proposition 10.19, Corollary 10.20) and the factorial-base formula (Proposition 10.21) are from round-2 track R2a.
- The period mean and the factorial-digit transfer recursion are due to the round-2 computational referee and the round-2 lead.
- K. Kitamura's normal form underlies the whole setting.
- S. Lin (f(2,2) = 254) and V. Kovač (corrected statement) are credited as in note.md.
- Classical tools used here: Poisson summation and Fejér-type positivity, the Jessen–Wintner purity dichotomy (via Proposition 3.13(c)), Plancherel on Z_p, Cauchy–Schwarz, and Higham's floating-point error bounds.
- The interval code relies on the correct rounding of MPFR (via gmpy2) in I2, and on IEEE-754 directed rounding in I1.
