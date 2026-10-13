# Round 4 brief (2026-10-13): prove μ(K_p) > 0 for one odd prime p ≥ 7

This round has one target: **prove Conjecture 5.2 for at least one prime p ≥ 7** (or for all p ≥ p₀ with p₀ explicit), i.e. that
K_p = {x ∈ ℤ_p : g_p(x) = ∞} has positive Haar measure.

This would not answer Q3, because K_p is nowhere dense (Theorem 3.6) and a measure statement cannot place a natural number in K_p. It would still be a genuine new theorem: the round-1 numerics give μ(K_7) ≈ 0.62.

## Where round 3 stopped (note.md §11.3; full proofs in data/round3/reports/R3M.md; check in data/round3/checks/R3M.md)

Notation follows note.md §10.1 at an odd prime p:
- π_j(x) = (x+1)⋯(x+j);
- V_n = v_p(π_n(x)) and M_n = max_{i≤n} v_p(x+i);
- c_n = 2^{-n} p^{V_n}, which tends to 0 exponentially for almost every x (supercritical);
- a path e of length n is *alive* if v(S_e(x)) ≥ V_n, where S_e = Σ_{j<n} e_j π_j with e_0 = 1;
- the slope of e is λ_e = v(S_e′(x));
- P⁰_n is the slope-0 alive population, Z⁰_n = |P⁰_n|, and M_ℓ = c_{n_ℓ} Z⁰_{n_ℓ};
- a window W = [n, N) has jump D = V_N − V_n;
- survival of the population for all n implies x ∈ K_p (König; note Prop 1.2).

Results already proved (all checked by an independent instance and by a referee):
- **Prop 11.10** (R3M Prop A): odd-p window identity; c_n Σ ρ is a martingale on window cylinders.
- **Prop 11.11** (R3M Prop B): exact conditional second moment. The children of a slope-0 parent e at x′ = x₀ + p^m w are counted by m_W(β_e(φ_e − w)), where φ_e is the Hensel root of S_e in the cylinder.
- **Prop 11.12** (R3M Prop N): every window has χ²_W ≥ (p−1)4^{−p}, so per-window Cauchy–Schwarz can never give L²-boundedness.
- **Prop 11.13** (R3M Prop C2, two-window inequality). On C = x + p^{V_n}ℤ_p, under D + D′ ≤ V_n − M_{N′} and M_{N′} < V_n:
  E_C[(c_{N′}Z⁰_{N′})²] − E_C[(c_N Z⁰_N)²] ≤ ε(W,W′)·(c_n Z⁰_n)²,
  with ε(W,W′) = p^{D+D′}Coll_{D+D′} − p^D Coll_D, the L² mass of the composite window law in the frequency band (p^D, p^{D+D′}].
- **Theorem 11.14** (R3M Theorem C3; conditional). Take deterministic times 2p ≤ n₀ < n₁ < ⋯, a summable sequence (ε̄_ℓ), and an admissible atom A (a cylinder with a nonempty slope-0 population and the linear window conditions). Let τ be the first ℓ at which the linear-regime condition fails or ε_ℓ(x) > ε̄_ℓ, and put Π_A = (1+χ²_j) Π_ℓ (1+ε̄_ℓ).
  If (FE) δ_A := μ_A(τ < ∞) < 1/Π_A, then μ(K_p ∩ A)/μ(A) ≥ (1 − √(Π_A δ_A))²/Π_A > 0.
- **Lemma C4** (R3M): explicit union bound for the deep-gate (linear-regime) part of τ. It is small for n_j large.
- **Lemma C5 / Prop 11.15(a)** (R3M). ε(W,W′) is an explicit combination of the densities
  Λ_t(y) = p^{V_t(y)} · P(1 + Σ_{1≤c<t} δ_c π_c(y) ≡ 0 mod p^{V_t(y)})
  of a **signed carry process**, with δ_c i.i.d., P(0) = ½ and P(±1) = ¼:
  ε = (c_{N′}−c_N)/c_n + Σ_{n≤j<N} (c_j/2c_n)[Λ_{N′−j}(x+j) − Λ_{N−j}(x+j)] + Σ_{N≤j<N′} (c_j/2c_n) Λ_{N′−j}(x+j).
- **Remark C6** (sketch). The signed process satisfies the window identity verbatim. On slope classes visible to the windows, p^{V_t} Σ P(δ)ρ is a martingale, so their expected increments vanish. **If (S) held** — the normalised mass of signed paths whose slope is comparable to V_t is small — then E_A[ε_ℓ] would reduce to boundary terms of size O(c_{n_ℓ}/c_{n_{ℓ−1}}) plus failure events, and Markov would give FE.
- **Prop 11.15(b)** (R3M Prop N3): ∫ Λ_t dμ = +∞ for t ≥ 3, because the signed path (1,1,1,0,…) has S = (y+2)² (a double root at −2). So any annealed bound must first truncate at deep gates near window starts.

Numerics (heuristic; R3M §7.3), with n_{ℓ+1} = ⌈1.25 n_ℓ⌉:
- Median ε_ℓ at p = 7 decays steadily: 0.014, 0.0048, 0.0021, 0.0017, 0.00053, 0.00017. It also decays at p = 5, but not visibly at p = 3.
- ε grows by about a factor p per extra level of the deepest gate in the window.
- A heuristic decomposition gives κ_ℓ ≈ p^{v_pre} 2^{−d} ε^post_ℓ for a gate of depth s at distance d from the window start, contributing about κ p^s.
- At p = 3, slopes ≥ 4 carry 16–71% of the sample mean of Λ_t, so (S) is not a formality there. At p = 5, slopes ≥ 3 carry 7%.

## The open sub-problems (R3M §10 item 1)

1. **(S):** a first-moment bound for the signed carry process restricted to paths whose slope exceeds a fraction of V_t, uniformly on cylinders. This is the odd-p, signed analogue of note Proposition 10.7 (multiplicity k ≥ 2, subcritical).
   - Hint from R3M: the distinct-valuation counting of Prop 10.7 transfers, because two different signed digits d ≠ d′ ∈ {−1,0,1} cannot agree modulo p (|d − d′| ≤ 2 < p), so each distinct-level index costs a factor ≤ ½.
2. **Truncation:** an event G_ℓ, "no gate deeper than a slowly growing threshold s_ℓ near the start of W_{ℓ−1}", with E_A[ε_ℓ 1_{G_ℓ}] exponentially small in n_{ℓ−1} and Σ_ℓ μ_A(G_ℓ^c) small (as in Lemma C4).
3. Then FE follows by Markov's inequality, and Theorem 11.14 gives μ(K_p) > 0.

Other freedoms worth using:
- The window times need not be deterministic, if measurability is handled. Windows could be chosen adaptively so that their starts avoid deep gates.
- One may work at large p, where supercriticality is overwhelming: the expected growth per block is about 2^{p−1}/p^{p/(p−1)}.
- One may use a different functional or a thinned sub-population, if survival still implies x ∈ K_p.

## Obstructions any proof must respect

- Theorem 3.6: K_p is nowhere dense, so there is no residue-class criterion.
- Prop 11.12: per-window Cauchy–Schwarz fails.
- Prop 11.15(b): the plain annealed mean is infinite.
- Theorem 3.10 / Prop 11.23 (barrier lemmas): **deterministic** covering or L² bounds need unboundedly many digits of factorial unit parts.

For Haar-random x, however, those digits are polynomial images of the digits of x itself, so averaging over x is available. This is the loophole a measure proof must exploit.

## Files
- note.md §10.1 (the p = 2 machinery: Lemma 10.2–10.5, Props 10.6–10.7, the k = 1 martingale and the k ≥ 2 subcritical case); §11.3 (round 3).
- data/round3/reports/R3M.md (full proofs, §5; numerics, §7; failed attempts, §9).
- code/round3/R3M/ (exact test scripts: oddp_window_check.py, spectral_check.py, twowin_check.py, lemma_c5_check.py, signed_slopes.py, epsilon_scan.py, eps_gate_depth.py, oddp_mc.c). code/round3/check_R3M/ has an independently validated library (ck_lib.py).
- data/round3/reports/R3Q.md: the p = 2 explicit-rate machinery. Its stopped-martingale bounds, its high-slope window bound on coarse atoms (Lemma 9 / Prop 10), and its Lemma 8 (no high slope with high second derivative near −2) are the closest existing analogues of (S) and of the deep-gate truncation.
