# Check of round-4 track M4A, lens "numerical falsification"

This file holds two checks by the same track, with separate code:
- **Part II (below, 2026-10-14):** Corollary M′, μ(K_p) > 0 for p ∈ {11, 13, 17, 19, 23}.
- **Part I (further below, 2026-10-14, earlier session):** Theorem M, μ(K₇) > 0. It is kept unchanged.

Code: `code/round4/verify_M4A_falsify/`.
- Part II uses the files `cm_*.py`. They share no code with `code/round4/M4A/` and none with Part I's `vf_lib.py`, and where possible they use different algorithms (§II.6).
- Logs: `data/round4/verify_M4A_falsify/` (Part II: `cm*.log`). Each log starts with `=== command:` and ends with `=== exit:` and the wall time.

---

# Part II. Corollary M′ (p = 11, 13, 17, 19, 23)

**Claim under test** (M4A.md §6, Corollary M′, status [computer-assisted]). The verification of Theorem M, run with n₀ = 300, r = 27/20, ℓ₁ = 6 and the explicit atoms `data/round4/M4A/atom_p{11,13,17,19,23}.txt`, gives μ(K_p ∩ A_p)/μ(A_p) ≥ 1.06·10⁻⁴ (p = 11), 4.90·10⁻² (13), 3.48·10⁻³ (17), 1.09·10⁻¹ (19), 2.07·10⁻¹ (23). Hence μ(K_p) > 0 for these five primes.

## II.0 Headline

**Verdict: confirmed with one fix. No counterexample was found.** The conclusion μ(K_p) > 0 for p = 11, 13, 17, 19, 23 stands as a computer-assisted result, resting on R3M's Theorem C3 exactly as Theorem M does.

**The fix.** Three of the five printed lower bounds are rounded *up*, so the stated inequalities are slightly stronger than what the certificate proves:

| p | certified bound (my recomputation = M4A's own log) | stated in Cor M′ | correct rounding |
|---|---|---|---|
| 11 | 1.05875·10⁻⁴ | ≥ 1.06·10⁻⁴ (too strong) | ≥ 1.05·10⁻⁴ |
| 13 | 4.89550·10⁻² | ≥ 4.90·10⁻² (too strong) | ≥ 4.89·10⁻² |
| 17 | 3.48258·10⁻³ | ≥ 3.48·10⁻³ | correct |
| 19 | 1.09096·10⁻¹ | ≥ 1.09·10⁻¹ | correct |
| 23 | 2.06713·10⁻¹ | ≥ 2.07·10⁻¹ (too strong) | ≥ 2.06·10⁻¹ |

M4A's own log `fe_verify_final.log` prints 1.0587e−04, 4.8954e−02 and 2.0671e−01. The report's table (§6) and the claim rounded these to the nearest value rather than down. The positivity statement is unaffected. The table's log₁₀ δ_A column is rounded the same way (−24.74 for −24.737 at p = 11), which matters only as a presentation point.

**What was done.**
1. An independent recomputation of the whole FE certificate for all five atoms, from the statements in M4A.md (§II.1). Every printed number is reproduced: χ²₀, the six ε̄_ℓ, E_A ε_ℓ for ℓ = 7..14 (to the printed 3 decimals of log₁₀), the phase sums, μ_A(G′ᶜ), the phase-4 tail, Π_A, δ_A and the Paley–Zygmund bound. For ℓ = 15, 16 (ℓ = 16 only at p = 23), M4A prints the cap ≈ 10^−210.5 from its truncated c-sum, while my full sums are smaller (10^−222 to 10^−376). Theirs is the weaker bound, so the two are consistent; these windows contribute nothing visible to δ_A.
2. The p-specific constants (q_s, P₀, ρ₁, γ, κ, the phase-4 rate), by two or three methods each (§II.2).
3. Exact tests of every lemma in the chain at the new primes, and again at p = 7 (and p = 3, 5 where cheap), with the edge cases the lens asks for (§II.3):
   - Lemma Q: 75,521 cases at p = 7..23, 0 failures;
   - Theorem 1, Lemma F, Props D and E on balls;
   - Lemma H;
   - Prop D pointwise at the real atom geometry and on random windows at the largest exact levels;
   - Prop E′ ≥ Prop E with M4A's choice S = 4 for p > 13.

## II.1 Independent recomputation of the certificate (`cm2_cert.py`, logs `cm2_cert_p{11,13,17,19,23}.log`)

Method, per atom:
- **Atom and path.** V₃₀₀(x_A) is computed three ways: the valuation of the big integer π₃₀₀(x_A), Legendre's formula v((x_A+300)!) − v(x_A!), and a gate scan. The stored path e is evaluated as big integers, both at x_A and at five random x ∈ A: v(S_e(x)) ≥ m = V₃₀₀(x) and S_e′(x) is a unit mod p. So Z⁰₃₀₀ ≠ 0 on A.
- **Digit formulas.** For N < i_A, V_N on A is computed as v((x_A+N)!) − v(x_A!), and M over (a, b] from ⌊(x_A+b)/p^s⌋ − ⌊(x_A+a)/p^s⌋. This is a different formula from M4A's; both were checked against a direct scan up to N = 40000 (0 mismatches).
- **Phases 0–2** are exact rationals (gmpy2). Props D and E use my block (suffix-product) form. For W₀ and ℓ = 1, 2 it was also evaluated literally per c through a separate Lemma Q evaluator; the two forms agree exactly.
- **Phase 2.** θ = min(⌈D/2⌉, D − m + 1) (Theorem 1 with the ball A, b = m). The Lemma F hypothesis M_W ≤ K − θ is asserted for every window.
- **Phase 3** uses Prop E′ (mpmath, 60 digits) with exact D, K and M_W. E′ ≥ exact E is checked on every phase-2 window.
- **Phase 4** has two parts.
  - My own per-ℓ worst case on G′, for 300 windows, with deterministic digit counts for the levels ≤ m.
  - My own analytic majorant for all ℓ ≥ ℓ₄, built from Legendre-type bounds only. Each of its two branches has the form −a·n + b·ln n + c₀; its value and slope are checked at n* = n_{ℓ₄−1}, and so are the side conditions D ≥ 2σ + 1 and the linear regime (§II.4).

| p | m | i_A | last ℓ before i_A | χ²₀ | ε̄₁ … ε̄₆ | first Markov window ℓ = 7: D, K, θ, M_W; log₁₀ E_A ε₇ |
|---|---|---|---|---|---|---|
| 11 | 30 | 5.730·10³⁰ | 215 | 3.63828 | 4.24547, 0.453086, 0.635356, 2.76092, 2.8053, 3.78773 | 62, 149, 31, 3; −25.038 |
| 13 | 26 | 8.120·10²⁸ | 201 | 0.422094 | 0.433964, 1.47852, 0.457808, 0.0598492, 0.0431679, 0.0517123 | 52, 124, 26, 3; −23.528 |
| 17 | 18 | 1.359·10²² | 149 | 7.50249 | 7.50253, 3.01·10⁻⁴, 2.40·10⁻³, 0.594706, 8.97·10⁻⁴, 0.0409166 | 39, 93, 20, 2; −20.861 |
| 19 | 16 | 4.043·10¹⁹ | 130 | 1.4437·10⁻³ | 1.444·10⁻³, 0.0720314, 4.66·10⁻⁴, 4.75·10⁻⁴, 2.56747, 1.412·10⁻³ | 34, 83, 17, 3; −17.893 |
| 23 | 14 | 3.793·10¹⁸ | 122 | 2.22478·10⁻⁸ | 5.48·10⁻⁸, 0.0621592, 0.796879, 2.41·10⁻⁶, 8.83·10⁻⁴, 0.0621617 | 28, 68, 14, 2; −17.702 |

| p | phase 2 sum (ℓ = 7..16) | phase 3 sum | μ_A(G′ᶜ) | phase-4 tail (all ℓ ≥ ℓ₄) | log₁₀ Π_A | δ_A | log₁₀(Π_A δ_A) | PZ bound | M4A log |
|---|---|---|---|---|---|---|---|---|---|
| 11 | 1.83184·10⁻²⁵ | 4.7·10⁻⁴⁷⁹ | 1.38·10⁻⁷² | 10^(−2.19·10²⁸) | 3.97521 | 1.83184·10⁻²⁵ | −20.7619 | 1.05875·10⁻⁴ | 1.0587·10⁻⁴ |
| 13 | 5.93041·10⁻²⁴ | 2.7·10⁻⁴⁷⁷ | 2.52·10⁻⁶⁹ | 10^(−3.25·10²⁶) | 1.31020 | 5.93041·10⁻²⁴ | −21.9167 | 4.89550·10⁻² | 4.8954·10⁻² |
| 17 | 2.75731·10⁻²¹ | 1.4·10⁻⁴¹² | 6.81·10⁻⁵⁷ | 10^(−4.71·10¹⁹) | 2.45810 | 2.75731·10⁻²¹ | −18.1014 | 3.48258·10⁻³ | 3.4825·10⁻³ |
| 19 | 2.55669·10⁻¹⁸ | 4.5·10⁻³⁸² | 1.03·10⁻⁵² | 10^(−1.47·10¹⁷) | 0.962191 | 2.55669·10⁻¹⁸ | −16.6301 | 1.09096·10⁻¹ | 1.0909·10⁻¹ |
| 23 | 3.97099·10⁻¹⁸ | 2.9·10⁻³³³ | 1.97·10⁻⁵¹ | 10^(−1.19·10¹⁶) | 0.684632 | 3.97099·10⁻¹⁸ | −16.7165 | 2.06713·10⁻¹ | 2.0671·10⁻¹ |

Further checks:
- **Admissibility.** W₀ = [300, 405) satisfies D₀ ≤ m − M₄₀₅ and M₄₀₅ < m for every atom: (D₀, M) = (11, 3), (8, 3), (8, 2), (6, 2), (4, 2).
- **Linear regime.** It holds on all of A for every composite window ending before i_A (ℓ ≤ 215, 201, 149, 130, 122).
- **Phase boundaries.** ℓ₄ = 216, 202, 150, 131, 123, the same as M4A's log.
- **Regression at p = 7** (`cm2_cert_p7.log`, ℓ₁ = 8). The new code reproduces Theorem M exactly: 1.8434438·10⁻²⁶, log₁₀ Π_A = 25.73437, δ_A = 1.0005204·10⁻⁴⁵. This is a third implementation agreeing with M4A and with Part I.

## II.2 Constants (`cm1_consts.py`, log `cm1_consts.log`)

| p | q₁ | q₂ | q₃ | S used in E′ | ρ₁ | γ | κ | phase-4 rate c (r = 27/20) |
|---|---|---|---|---|---|---|---|---|
| 11 | 525041/524288 | 1165593/1048576 | 1888689/1048576 | 8 | 0.0164478 | 2.29353 | 2.65454 | 0.031818 |
| 13 | 33555171/33554432 | 1057095/1048576 | 10002941/8388608 | 8 | 0.00252215 | 2.55688 | 3.57670 | 0.031599 |
| 17 | 1.00000061 | 1.00028981 | 1.02256895 | 4 | 2.614·10⁻⁴ | 2.83292 | 5.74796 | 0.027434 |
| 19 | 1.00000010 | 1.00046337 | 1.01075071 | 4 | 1.144·10⁻⁴ | 2.94398 | 6.89009 | 0.025683 |
| 23 | 1.00000001 | 1.00000226 | 1.00115788 | 4 | 1.752·10⁻⁵ | 3.13549 | 9.24499 | 0.022819 |

(Exact fractions for p = 17..23 are in the log.)
- **q_s.** Computed by an exact int64 residue DP (every count is < 4²³ = 2⁴⁶). This agrees with full enumeration of the 3^p digit vectors (p ≤ 13, s ≤ 6), and with an FFT of the characteristic function Π_k(½ + ½cos(2πξπ_k(−p)/p^s)) to within 1.4·10⁻¹⁷ (all p, p^s ≤ 7·10⁶).
- **P₀(g, s).** Computed by exact meet-in-the-middle for every s; equal to a residue DP for all g ≤ p and p^s ≤ 30000.
- **Monotonicity.** q_s ≤ q_{s+1} ≤ p·q_s holds at every computed s. This is the Δ_s ≥ 0 that Prop E′ needs, and it also makes M4A's q̃_s = q₄p^{s−4} (p > 13) a valid majorant.
- **Agreement with M4A.** All constants agree with M4A's printed values to within 5·10⁻⁷ (they print 6 decimals). They also agree with the report's (q₁, q₂, q₃) at p = 11 and 13.
- **Rates.** κ > 0 and c > 0 at all five primes, while c < 0 at p = 3 and 5 (−0.132 and −0.018), as M4A §8 says.
- **Deep-gate factor.** P₀(2, s) = 1/4 for every s at every p: the double root of (y+2)². Also P₀(1, ·) = 0, and P₀(3, s) = 0 for s ≥ 1 when p ≥ 7.

## II.3 Exact tests of the lemmas at the new primes

| claim | test | size | result |
|---|---|---|---|
| **Lemma Q** | `cm3_lemmaQ.py`: own CRT-exact joint DP over (T mod p^k, T′ mod p^f), every t ≤ t_max and every k ≤ min(k_max, V_t); f ∈ {none, 1, .., f_max}. Points: random; u = −g + p^s w with g ∈ {1, 2, 3, p−1, p, p+1, p+2, 2p+1} and s up to k_max+2 (deep gates at −1, −2, …); small integers and −1 + p^j; runs of depth-1 gates starting at g₁ ≤ 4 (2D blocks); near double roots of random signed polynomials | p = 7 (k ≤ 4, f ≤ 3), 11, 13, 17, 19, 23 (k ≤ 3, f ≤ 2) | **75,521 cases, 0 failures**; 3,145 cases contain a 2D block; equality in 39,498 (max P/bound = 1 exactly) |
| ↳ controls | 2D factor halved; q_s → 1; the k − M_{r+1} clause dropped | same | violated 1,319, 7,931 and 24 times (at every prime except "noM" at p = 13). So the 2D factor is sharp to within a factor 2 at every prime, the q_s are needed, and the k − M clause is needed. |
| **Prop D at the real atom geometry** | `cm4_atomlow.py`: for each window start n₀..n₆ and scale j ≤ 3 with a window of exact level j, exact p^j Coll_j at x_A and 3 random x ∈ A against Prop D (K = j). Extending the window by 2p elements does not change Coll_j (checked). | p = 11, 13, 17, 19, 23 | **404/404**; max ratio 1.000000 (attained). The tiny excesses that make phase 1 cheap are reproduced exactly: e.g. p = 23, n₀, j = 1: p Coll₁ − 1 = 5.978677·10⁻⁹ = Prop D − 1; p = 17, n₀: the gate at n₀ + 1 gives exactly p/2 − 1 = 7.5, which is the χ²₀ ≈ 7.50 of the table |
| **Prop D pointwise, larger levels** | `cm8_propD_window.py`: composite windows of exact level K (up to 6 at p = 7, 5 at p = 11, 4 at p ≥ 13), with deep gates (depth ≤ 5) at n+1, n+2, n+3 and at n+p+2, integer x, random x; p^K Coll_K, ε = p^K Coll_K − p^D Coll_D and the χ² form of [n, N), all exact | p = 7 (60 windows), 11 (50), 13 (40), 17 (40), 19 (30), 23 (30) | **250/250 in all three forms**; max (p^K Coll_K − 1)/(Prop D − 1) = 1.000000 (attained). The true ε is often far below Prop D − 1 (e.g. at p = 23, ε = 5.9·10⁻¹⁴ against 263.5, when a gate of depth 2 sits at n + 1), as expected from dropping p^D Coll_D ≥ 1 |
| **Theorem 1 (identity), Lemma F, Props D, E** | `cm6_thm1.py`: balls B = x₀ + p^b ℤ_p with constant gate pattern and θ ≥ 1; all x ∈ B mod p^R enumerated; Lemma F's sup computed exactly by DP at every x and c; x₀ random or near −(n+1), −(n+2) | p = 7 (40 balls, K ≤ 4, θ ∈ {1, 2}), 11 (30, K ≤ 3), 13 (20, K ≤ 3) | **Theorem 1 exact in 90/90**; Lemma F 90/90 (equality in 83); Prop D at every x 90/90; Prop E 90/90 |
| **Lemma H** | `cm7_lemmaH.py`: random polynomials, (X−z₀)² + p^j c, (X−z₀)²(X−z₁), (X+2)², cubes, signed carry polynomials centred at a double root mod p² | p = 7, 11, 13 (k′ ≤ 4), 17, 19, 23 (k′ ≤ 3); 3,573 cases (760 with θ ≤ 0) | **3,573/3,573 exact**; the control θ+1 breaks the identity 350 times, so the threshold ⌈k/2⌉ is used sharply at every prime |
| **Prop E′ ≥ Prop E** | `cm5_eprime.py`: 120 windows [n, ⌈rn⌉, ⌈r²n⌉) per prime, r ∈ {6/5, 27/20, 3/2}, n ≤ 3000; 3/4 of them with a planted deep gate (depth 2..10) at n+1..n+2, just after N, or mid-window; σ ∈ {M_W, M_W+3}; M4A's S (8 for p ≤ 13, 4 above) | p = 3, 5, 7, 11, 13, 17, 19, 23 | **1,920/1,920**; min ln(E′/E) = 12.6 nats (p = 7). Block form = literal per-c form (Props D and E) in 76/76 small windows |
| Lemma Q proof algebra at deep levels | Part I's `t6_deep_algebra.py` (this track's code), run at the new primes | p = 13, 17, 19, 23; 10 points each (half with a planted gate of depth 5–25), t ≤ 1500, levels L up to 147 | Step 0(a) 10,422/10,422; Step 3 congruence 3,435/3,435; Step 4 congruence and history cancellation 3,226/3,226 2D blocks; the controls one digit stronger fail in all 3,435 and 3,226 (logs `cm9_t6_deep_p*.log`) |

## II.4 Points specific to Corollary M′ that were attacked

1. **The slope threshold at the first Markov window.** Theorem 1 on the ball A gives θ = min(⌈D/2⌉, D − m + 1), and this equals ⌈D/2⌉ only when D ≥ 2m − 2. With ℓ₁ = 6 the first Markov window is ℓ = 7. The margins (D against 2m − 2) are:
   - p = 11: 62 against 58;
   - p = 13: 52 against 50;
   - p = 17: 39 against 34;
   - p = 19: 34 against 30;
   - p = 23: 28 against 26.

   So θ = ⌈D/2⌉ holds, narrowly at p = 13 and 23. My code computes θ from the min and does not assume it, and asserts M_W ≤ K − θ (Lemma F) for every phase-2 and phase-3 window. A smaller ℓ₁ would have needed the weaker θ; it is not used.
2. **S = 4 for p > 13 in Prop E′.** Exact q₅ is below q₄p at p = 17, 19, 23 (16.72 < 33.17, 8.26 < 24.88, 2.35 < 24.03), so q̃_s ≥ q_s holds. E′ with S = 4 dominates exact Prop E in 720/720 window–σ pairs at these primes.
3. **Phase-4 rate at large p.** The rate c falls from 0.0318 (p = 11) to 0.0228 (p = 23); half of it is used. My majorant has its own constants:
   - σ ≤ m + 10 + 2 log_p(2n);
   - D ≥ (r−1)n/(p−1) − log_p n − 1;
   - K ≤ H/(p−1) + σ;
   - V_n ≥ n/(p−1) − log_p n − 1.

   With these, both branches are negative with negative slope at n*, and the margins D − 2σ − 1 and V_n − K − σ − 1 are positive with positive slope at n*, at every prime. Over the 300 evaluated windows, the smallest value of −ln(fail)/n_{ℓ−1} equals the full rate c to six digits (0.0318181, 0.031599, 0.0274336, 0.0256832, 0.0228191). So the per-window bounds decay at the asymptotic rate, twice the rate the majorant uses.
4. **μ_A(G′ᶜ) ≤ p⁻¹⁰(i_A⁻² + p⁻²ᵐπ²/6).** Re-derived: for i = i_A + p^m j, v(x+i) − m is distributed as v of a Haar-random element of ℤ_p, so P(v(x+i) > m + 2 log_p i + 10) ≤ p⁻¹⁰ i⁻². Evaluated independently (table above).
5. **Deep gates at the atoms' window starts.**
   - At p = 17 the gate at n₀ + 1 makes p Coll₁ = p/2 exactly. This drives χ²₀ ≈ ε̄₁ ≈ 7.5 and Π_A ≈ 10^2.46, and Prop D reproduces it exactly.
   - At p = 23 a depth-1 gate lies at distance 9 from both n₁ and n₅ (which differ by 41·23). It gives ε̄₂ ≈ ε̄₆ ≈ 0.0622.

   These are the near-start gate effects that the brief and R3M (Prop N3 and the discussion after it) warn about. They are priced exactly and are finite.
6. **Integer and near-integer points, high-slope paths.** The Lemma Q, Lemma H and Prop D tests include small integers, the shadows −g + p^s w of the negative integers −1, −2, −3, …, and near double roots. There was no failure, and the bounds are attained at P₀(2, s) = 1/4.
7. **Is μ(K_p ∩ A)/μ(A) ≥ 0.2 at p = 23 plausible?** The note's numerical values are μ(K₁₁) ≈ 0.70 and μ(K₁₃) ≈ 0.75 (note §5). The bounds here are conditional on atoms carrying a slope-0 path, and none exceeds those values. A direct Monte Carlo falsification of the lower bound is not feasible: on A the population at n₀ = 300 has about 2³⁰⁰p⁻ᵐ alive paths (≈ 10⁷¹ at p = 23), so {g_p ≥ G} has measure ≈ 1 on A until G is far above m, out of exact reach.

## II.5 What was not tested, and what remains open

1. **R3M Theorem C3** (with Props A, B, C2 and Corollary A′) is the frame and is not re-tested; it was checked in round 3 by an independent instance and a referee. Cor M′ uses it with no p-specific hypothesis beyond n₀ ≥ 2p (300 ≥ 46).
2. **Lemma Q at the scale used.** The certificate applies Lemma Q at levels in the hundreds (K = 68..149 at ℓ = 7). The exact tests reach k ≤ 3 at p ≥ 11, so at most one 2D block in a row there. The deep-level algebra of the proof was tested separately (table). As in Part I, the evidence at the scale used is the proof plus local tests, not a direct evaluation.
3. **Prop D at the actual phase-1 levels.** These are K = 10..110, which is out of exact reach (the DP state space is p^K). It was tested at the atom geometry for levels ≤ 3 and on random windows for levels ≤ 4–6.
4. **Arithmetic.** Phase 3 E′ and phase 4 are mpmath at 60 digits, not interval arithmetic. The margins exceed 10³⁰⁰ in phase 3 and are doubly exponential in phase 4. M4A's evaluation uses outward rounding.
5. **Human refereeing** of the whole chain has not happened.

## II.6 Code paths and commands

Differences from M4A's code, and from Part I's:
- q_s: residue DP, plus enumeration and FFT;
- P₀: meet-in-the-middle;
- V_N: Legendre's formula;
- Prop D/E: suffix-product form, plus a literal per-c form through a separate Lemma Q evaluator;
- the analytic phase-4 majorant: own constants;
- CRT primes: < 2⁶¹.

Commands (in `code/round4/verify_M4A_falsify/`; every log starts with its command line):
- `python3 cm1_consts.py 4`
- `python3 cm2_cert.py data/round4/M4A/atom_pP.txt 6 60000 300 2` for P = 11, 13, 17, 19, 23, and `… atom_p7.txt 8 60000 300 1`
- `batch_cm3.sh`: `cm3_lemmaQ.py p SEED NPERKIND KMAX FMAX TMAX rand,neg,int,d1first,dbl`
- `batch_cm4.sh`: `cm4_atomlow.py`, `cm5_eprime.py`, `cm6_thm1.py`, `cm7_lemmaH.py`, `cm8_propD_window.py` (parameters in the script and the logs)
- `t6_deep_algebra.py p 9p 10 1500` for p = 13, 17, 19, 23 (Part I's script; logs `cm9_t6_deep_p*.log`)

Budget: about 10.5 core-minutes of logged runs (613 s in total), plus about 1 minute of smoke tests; the longest single job took 219 s (Lemma Q at p = 23). One core at a time, under `nice -n 10`.

## II.7 Credit

- **Statements under test.** Track M4A of round 4: Corollary M′, with Lemma H, Theorem 1, Lemma F, Lemma Q, Props D/E/E′ and the FE certificate.
- **Machinery.** The conditional Theorem C3, Props A, B, C2 and Prop N3 are track R3M's (round 3).
- **Earlier work.** The p = 2 quenched martingale is track R1b's (round 2). The p = 2 quantitative machinery and the high-slope and deep-gate templates are track R3Q's (round 3).
- **Classical tools.** Hensel's lemma; Legendre's formula; Paley–Zygmund; Doob's L² convergence; the second-moment method for trees (Lyons); branching processes in random environments (Smith–Wilkinson, Athreya–Karlin, Afanasyev–Geiger–Kersting–Vatutin); Littlewood–Offord-type anti-concentration; the Chinese remainder theorem and meet-in-the-middle for the exact computations.
- This check was produced in an AI-assisted session and has not been reviewed by a human.

---

# Part I. Theorem M (μ(K₇) > 0)

*(Written in an earlier session of this track; unchanged except for this heading. Its code is `vf_lib.py` and `t*.py`, and its logs are `t*.log`.)*

Date: 2026-10-14. Code: `code/round4/verify_M4A_falsify/`, written from the statements in `data/round4/reports/M4A.md`, with no code shared with `code/round4/M4A/`. Logs: `data/round4/verify_M4A_falsify/`. Each log starts with `=== command:` and ends with `=== exit:` and the wall time.

## Headline

**Verdict: confirmed (as a computer-assisted result). No counterexample was found.** I tested every new identity and inequality in the chain of Theorem M exactly, at p = 3, 5, 7 (and 11 where cheap):
- Lemma H;
- Theorem 1;
- Lemma F;
- Lemma Q, including the algebra of its proof at levels up to 219;
- Props D and E, evaluated by two code paths, and Prop E′;
- the window-level bounds at the real geometry of the atom.

Every claimed bound holds in every case. The stronger control variants fail where they should, so the tests can see the features they probe.

I also recomputed the whole FE certificate for the p = 7 atom from scratch, in exact rationals for phases 0–2 (and for Prop E up to l = 20). It reproduces every printed number:
- χ²₀ ≤ 0.504642;
- all eight ε̄_l;
- E_A ε₉ ≤ 10^−45.301;
- δ_A ≤ 1.0005204·10^−45;
- log₁₀ Π_A ≤ 25.73437;
- log₁₀(Π_A δ_A) ≤ −19.2654;
- μ(K₇ ∩ A)/μ(A) ≥ 1.8434·10^−26.

For phase 4 (l ≥ 307) I built my own majorant from Legendre-type bounds only. It confirms that the tail is at most 10^(−2.99·10^40).

The claim rests on R3M Theorem C3 (with Props A, B and C2) from round 3. I did not re-test those numerically here; they were checked in round 3 by an independent instance and a referee. Within that frame, the label **[computer-assisted]** is appropriate, and I found nothing to fix in M4A's chain.

## 1. What was tested, and results

All probabilities are exact rationals. The signed-process DP keeps integer counts with weights (1,2,1) per digit, modulo two or three primes near 2^60. Counts are reconstructed by CRT and checked to lie below the total weight 4^(#digits), so they are the true counts. The DP was validated against brute-force enumeration of all signed paths: 807/807 comparisons agree (`t0_validate.log`).

| claim (M4A.md) | test (program) | size | result |
|---|---|---|---|
| constants q_s, P₀, ρ₁, γ, κ (§4, §5) | `t0_validate.py` | p = 3, 5, 7, 11, 13 | All agree with the report: q₁ = 8309/8192, q₂ = 4557/4096, q₃ = 33271/8192, q_s = 7^s·3/256 for s = 4..8; the P₀ table at p = 7; ρ₁ = 0.06041, γ = 1.85344, κ = 0.91167. q_s ≤ q_{s+1} ≤ p·q_s holds for s < 8 at all five primes, which is the Δ_s ≥ 0 that Prop E′ needs. |
| **Lemma Q**: P(v(T) ≥ k, v(T′) ≥ f) ≤ P₀·Π π_r (§4) | `t1_lemmaQ.py`; exact DP over (T mod p^k, T′ mod p^f), every t ≤ t_max, every k ≤ min(V_t, k_max), f ∈ {none, 1..f_max} | 23 configurations: p = 3 (k ≤ 9, f ≤ 5, t ≤ 45), p = 5 (k ≤ 6, f ≤ 4), p = 7 (k ≤ 4, f ≤ 3, t ≤ 50), p = 11 (k ≤ 3, f ≤ 2) | **1,525,715 cases, 0 failures.** Equality holds in 65,297 cases. 112,051 cases use at least one 2D block, and up to 3 consecutive 2D blocks occur (p = 5, `d1first`). |
| ↳ Lemma Q, edge cases | point types `neg` (u = −g + p^s w, g ≤ 2p+1, s ≤ k_max+2: near −1, −2, …), `int` (u a small integer), `dbl` (u at the best near-double root of a random signed polynomial: high-slope paths), `scan` (every residue mod p^a), `d1run`, `d1first` (runs of depth-1 gates) | in the counts above | 0 failures in each type |
| ↳ controls for Lemma Q | 2D factor halved; 1D factor 1/p^d in place of q_d/p^d; the k − M_{r+1} clause dropped; depth-2 end gates allowed as 2D | same cases | 9,612, 78,994, 6 and 0 violations respectively. The halved-2D and q_s → 1 controls are violated, so the 2D factor and q_s are both needed. The k − M clause is needed (6 violations at p = 7, 11). |
| Lemma Q, proof algebra at deep levels | `t6_deep_algebra.py`: exact p-adic arithmetic, levels L up to 219, a planted deep gate (depth 5–25) in half the points | p = 3, 5, 7, 11; t up to 1000 | Step 0(a), v(R_r − R_r^{<g_r}) ≥ L_r + 1: 24,735/24,735. Step 3 congruence: 8,186/8,186 (the control one digit stronger fails in all). Step 4: 6,423/6,423 2D blocks (control fails in all). The history cancels identically in all 6,423. |
| **Lemma H** (§2) | `t2a_lemmaH.py`: random polynomials, squares, cubes, near-double roots (X−z)² + p^j c, signed carry polynomials; balls often centred at roots | 6,000 cases at p = 3, 5, 7 | **6,000 exact equalities, 0 failures.** Of these, 1,501 have θ ≤ 0 and are trivial. Control θ+1 in place of θ: the identity fails 520 times, so θ = min(⌈k/2⌉, k−b+1) is where it stops. |
| **Theorem 1** (identity for E_B ε) | `t2b_chain.py`: ε(x) = p^K Coll_K − p^D Coll_D, exact for every x ∈ B mod p^K, against the high-slope form | 250 balls (p = 3: 160, p = 5: 60, p = 7: 30); kinds random, deep gate of depth 2–4 at distance 1, 2, 3, 4, p+2 from n, and integer x | **250/250 exact identities** (θ ≥ 1 in 129) |
| **Lemma F** | same, with the sup over a 4-point subset of B, which makes the test stronger | 129 balls with θ ≥ 1 and M_W ≤ K − θ | 129/129 hold; max LHS/RHS = 1 (equality occurs) |
| **Prop D** (pointwise; χ² form) | same; also `t5_atom_lowscale.py` at the real atom geometry (below) | 250 balls × all x | 250/250 for p^K Coll_K and ε ≤ (Prop D) − 1; 250/250 for p^D Coll_D ≤ Prop D(N′ = N); max ratio 1.0000 (attained) |
| **Prop E** (averaged) | same | 129 balls | 129/129; max E_B ε / Prop E = 0.13 |
| Props D/E, two code paths | per-c Lemma Q form against block (Suf) form | 379 (t2b) + 71 (t4) | exact equality in all 450 |
| **Prop E′ ≥ Prop E** | `t4_eprime.py`: windows [n, ⌈rn⌉, ⌈r²n⌉), r ∈ {6/5, 27/20, 3/2}, n up to 3000; x random or with a deep gate (depth ≤ 12) just after n, just after N, at n+2, or mid-window; σ = M_W and σ > M_W | 889 windows (p = 7: 394, p = 5: 197, p = 3: 199, p = 11: 99), two σ each | **1,778/1,778**; min ln(E′/E) = 9.88 nats |
| Prop D at the real atom geometry | `t5_atom_lowscale.py`: for each start n_{l−1} (l = 0..8) and scale j ≤ 6 with a window [n, N′_j) of exact level j (elements beyond vanish mod 7^j; checked), exact 7^j Coll_j at x_A and 2 random points of A | 135 checks | 135/135; max ratio 1.0000 |

## 2. Independent recomputation of the FE certificate (`t3_atom_fe.py`, log `t3_atom_fe.log`)

| item | my value | M4A.md |
|---|---|---|
| V₃₀₀(x_A), M₃₀₀ | 51, 4 | 51 |
| path: v₇(S_e(x_A)), S_e′(x_A) mod 7 | 51, 6 (big-integer evaluation) | 51, 6 |
| x_A < 7^51; i_A | true; 4.1065·10^42 | ≈ 4.1·10^42 |
| digit formula for V_N, M_N | 0 mismatches against direct valuations (N ≤ 70000, sampled) | — |
| W₀: D₀ = 17 ≤ m − M₄₀₅ = 47, M₄₀₅ = 4 < 51 | true | admissible |
| linear regime, l = 1..306 (all composite windows ending before i_A) | holds for all 306 | holds |
| last l with n_{l+1} < i_A | 306 (n₃₀₇ = 3.0956·10^42 < i_A < n₃₀₈ = 4.1791·10^42) | 306 |
| χ²₀ bound (Prop D, exact) | 0.504642 | 0.5046 |
| ε̄₁..ε̄₈ (Prop D, exact) | 1.63688, 12.9262, 98.6367, 137.821, 336.303, 3834.74, 464266, 4.95628·10^7 | 1.64, 12.9, 98.6, 138, 336, 3835, 4.64·10^5, 4.96·10^7 |
| log₁₀ E_A ε_l, l = 9..13 (Prop E, exact; θ = ⌈D/2⌉ checked; M_W ≤ K − θ checked) | −45.301, −61.003, −84.226, −113.998, −154.224 | same |
| l = 14, 15, 16 | −209.810, −284.978, −383.356 (full sums) | ≤ −209.76, −210.53, −210.44 (their truncated c-sum plus tail: weaker and consistent) |
| Prop E′ against exact Prop E, l = 11..20 | E′ dominates in all 10 (e.g. l = 17: −479.572 ≥ −517.140) | E′ used from l = 17 on |
| phase 2 + 3 sum | 1.000520·10^−45 (dominated by l = 9) | ≤ 1.0006·10^−45 |
| μ_A(G′^c) | 2.46676·10^−94 | ≤ 2.47·10^−94 |
| phase 4, evaluated l = 307..2000 (worst-case E′ on G′: σ_l = 51 + ⌈2 log₇ n_{l+1}⌉ + 11, D ≥ v((N−n)!), K ≤ Σ_{j≤σ} ⌈H/7^j⌉, f′ ≥ min(⌈D/2⌉, D−σ)) | side conditions (D ≥ 2σ, linear regime on G_l) hold for all l; ln fail_l ≤ −0.0314359·n_{l−1} for every l; largest −7.2·10^40 | ln fail ≤ −c′n, with c = 0.0314 |
| phase 4, all l ≥ 307 (my majorant Φ, §3) | Σ_{l≥307} fail_l ≤ 4e^{−0.03 n*} = 10^(−2.99·10^40) | ≤ 10^(−1.56·10^40) |
| log₁₀ Π_A | 25.73437 | ≤ 25.7344 |
| δ_A | 1.0005204·10^−45 | ≤ 1.0006·10^−45 |
| log₁₀(Π_A δ_A) | −19.265404 | ≤ −19.265 |
| (1 − √(Π_A δ_A))²/Π_A | 1.8434438·10^−26 | ≥ 1.843·10^−26 |

The same program applied to Corollary M′ at p = 11 and p = 13 (L₁ = 6) reproduces that table too (`t3_atom_fe_p11.log`, `t3_atom_fe_p13.log`):
- p = 11: log₁₀ Π_A = 3.975 and log₁₀ δ_A = −24.737, giving a bound of 1.0588·10^−4 (report: 1.06·10^−4);
- p = 13: log₁₀ Π_A = 1.310 and log₁₀ δ_A = −23.227, giving 0.04895 (report: 4.90·10^−2).

Corollary M′ is not the claim under test; this is a spot check only.

**Arithmetic.**
- Phases 0–2, and Prop E for l ≤ 20, are exact rationals (gmpy2 mpq).
- Phase 3 E′ and phase 4 use mpmath at 60 significant digits, without outward rounding. The rounding error (~10^−55 relative) is negligible against the margins: phase 3 contributes 10^−477 against the needed 10^−26.
- M4A's own evaluation was in interval arithmetic.

## 3. My phase-4 majorant (all l ≥ 307 at once)

Let n = n_{l−1} ≥ n* = n₃₀₆ = 2.29·10^42 and r = 27/20. Then:
- N ≤ rn + 1 and N′ ≤ r²n + r + 1 ≤ 2n;
- H ∈ [(r²−1)n, (r²−1)n + r + 1];
- σ ≤ 51 + 2 log₇(2n) + 12;
- D ≥ v((N−n)!) ≥ (r−1)n/6 − log₇n − 2, by Legendre with s₇(m) ≤ 6(log₇m + 1);
- K ≤ H/6 + σ (Lemma 1(b));
- f′ ≥ D/2 − σ;
- l ≤ 1 + ln(n/300)/ln r.

Insert these into the two terms T₁ (the base term p^K 2^−H (1+2^p)) and T₂ (the level sum) of Prop E′. E′ is increasing in K and σ and decreasing in f′ and H, so every substitution is in the safe direction. Each Tᵢ + (l−8) ln 2 + 0.03n has the form −aᵢn + O(log n) with aᵢ > 0. At n* the values are −6.3·10^41 and −3.3·10^39, and the slopes are −0.273 and −0.0014. Each slope is −a + b/n with b > 0, so it is largest at n*. Hence ln fail_l ≤ −0.03·n_{l−1} + ln 2 for every l ≥ 307, and the tail sum is ≤ 10^(−2.99·10^40). The linear regime K ≤ v(n!) − σ, σ < v(n!), and D ≥ 2σ hold with margins linear in n. This agrees with M4A's tangent-line argument (their rate c′ = c/2 = 0.0157 is more conservative than my 0.03).

## 4. Adversarial points that were specifically attacked

1. **Deep gates near window starts (R3M Prop N3: ∫Λ_t = ∞).**
   - Lemma Q at u near −2 with depth up to k_max+2 holds with equality: P₀(2,s) = 1/4 is attained, which is the double root of (y+2)².
   - t2b and t4 plant gates of depth 2–12 at distance 1, 2, 3, 4, p+2 from n, from N, and in mid-window. No violation of Props D, E or E′ occurs. E′ keeps a margin of at least 9.9 nats.
   - The exact block-0 factor P₀ is what makes these cases safe. With P₀ replaced by 1 the bound stays valid but becomes weak; it is not a control.
2. **High-slope signed paths.**
   - `dbl` points sit at the best near-double root, mod p^{2A}, of 40 random signed polynomials each.
   - Lemma H was run on squares, cubes and near-squares with balls centred at roots.
   - No failure. Lemma H fails as soon as θ is raised by 1 (520 times), which shows the threshold ⌈k/2⌉ is genuinely used.
3. **The 2D factor q₂/p², uniformly in the history.**
   - The halved factor is violated 9,612 times, so the factor is not loose by 2.
   - The Step-4 congruence π_{g+k′}(u)·Σ_{i=k′+1}^{p} p/(y+i) ≡ p^L(ω/α)π_{k′}(−p) (mod p^{L+2}) holds in all 6,423 deep 2D blocks, and fails mod p^{L+3} in all of them. So exactly two digits are pinned, as the lemma uses.
   - The history term cancels identically from the definitions, so the residue pinned for the block's digits is a function of the history alone. This is the uniformity in h.
4. **Integer-like points.** u a small integer (gate depths follow the factorial pattern), and x small integers in t2b: no failure.
5. **Real atom geometry.**
   - 7^j Coll_j ≤ Prop D at x_A and at random points of A, for every window start n₀..n₈ and every j ≤ 6 with an exact-level window: 135/135, with equality at j = 1.
   - All exact checks in §2 are at the atom itself.
6. **Consistency of the arithmetic of the certificate.** Two independent implementations, mine and M4A's, agree to every printed digit.

## 5. Observations (no effect on the verdict)

- The "depth-2 end gate counted as 2D" control was never violated in 1.5 million cases. Lemma Q may therefore hold with a stronger 2D condition. This is a possible slack, not a claim.
- Prop D is attained (ratio 1.0000) at the first scale, and Lemma F holds with equality in some balls. These are the cases where the bounds are tight.
- Prop E is loose on small windows (E_B ε / Prop E ≤ 0.13), as expected; its strength is the decay in D.
- A slip in the report's prose, not an error: the headline and §7 give μ(K₇) ≥ 1.4·10^−69, §6 gives ≈ 1.5·10^−69, and the exact value of the lower bound is 1.8434·10^−26 · 7^−51 = 1.465·10^−69. Both statements are correct.

## 6. Failed attempts in my own harness (transparency)

- The first version of the `d1run` point generator asked for up to 12 consecutive gates of depth 1. Among any p consecutive gates exactly one has depth ≥ 2, so the rejection loop could not terminate. One run hung for about 12 minutes and was killed.
  - Fixed: at most p−1 consecutive depth-1 gates are now required.
  - Added `d1first`, which puts the run at g₁ so that consecutive 2D blocks actually occur (3 consecutive at p = 5).
  - All `d1run` and `d1first` logs are from the fixed code.
- `t3_atom_fe.py` prints the p = 7 reference values ("report: …") even for p = 11 and 13. Those strings are labels only and do not enter any computation.

## 7. What was not tested, and what remains open

1. **R3M Theorem C3**, and through it Props A, B and C2 and Corollary A′. These are round-3 results (proved; checked by an independent instance and a referee; exact tests at p = 3, 5, 7 in round 3). They are the frame in which Theorem M is stated, and they are not re-tested here.
   - The identification ε(W,W′) = p^K Coll_K − p^D Coll_D, which M4A uses to connect to C3, is exact for every x. The composite transform factorises as μ̂_{W,K}(ζ)·μ̂_{W′}(ζu), and Parseval then gives the identity. So no extra hypothesis enters there.
2. **Lemma Q at the scale used.** At l = 9 the certificate uses Lemma Q with K = 456 and up to 70 2D blocks (counted from the first gate of the window, f′ = 97). Exact DP tests reach at most 3 consecutive 2D blocks and levels ≤ 9. Every per-block step of the proof was tested at levels up to 219: Step 0(a), the Step-3 and Step-4 congruences, and the history cancellation. The remaining step, the chain rule P(∩A_r) ≤ P(A₀)Π sup_h P(A_r | h), is elementary. I regard Lemma Q as tested as far as is possible, but at that scale the evidence is the proof plus these local tests, not a direct evaluation.
3. My evaluation of phases 3–4 is not in interval arithmetic. M4A's is. The margins are astronomically larger than any rounding error.
4. Human refereeing of the whole chain (R3M and M4A) has not happened.

## 8. Commands (all in `code/round4/verify_M4A_falsify/`; the logs contain them)

- `python3 t0_validate.py 1 60`
- `batch_t1.sh` and `batch_t2.sh`: `t1_lemmaQ.py p SEED NU KIND kmax fmax tmax [a]`, `t2a_lemmaH.py p SEED N`, `t2b_chain.py p SEED NB KIND Kmax maxpts statemax`, `t4_eprime.py p SEED NW nmin nmax SMAX`, `t5_atom_lowscale.py ATOM 8 6 3 501`, `t3_atom_fe.py ATOM 8 16 20 2000`, `t6_deep_algebra.py p SEED NU tmax`
- `t1_lemmaQ.py 5 403 8 d1first 5 4 45`, `t1_lemmaQ.py 7 404 20 d1first 4 3 50`
- `t3_atom_fe.py atom_p11.txt 6 12 14 600`, `t3_atom_fe.py atom_p13.txt 6 12 14 600`

Budget: about 17 core-minutes of logged runs, plus about 12.5 minutes in the killed hung run and about 2 minutes of smoke tests. One core at a time, under `nice -n 10`; the longest single job took 151 s.

## 9. Credit

- **Statements under test.** Track M4A of round 4: Lemma H, Theorem 1, Lemma F, Lemma Q, Props D/E/E′ and Theorem M.
- **Machinery.** The conditional Theorem C3, Props A, B and C2, Lemma C5 and Prop N3 are track R3M's (round 3).
- **Earlier work.** The p = 2 quenched martingale is track R1b's (round 2); the p = 2 quantitative machinery and the high-slope and deep-gate templates are track R3Q's (round 3).
- **Classical tools.** Hensel's lemma, Legendre's formula, Paley–Zygmund, Doob's L² convergence, the second-moment method for trees (Lyons), branching processes in random environments (Smith–Wilkinson, Athreya–Karlin, Afanasyev–Geiger–Kersting–Vatutin), Littlewood–Offord-type anti-concentration, and the Chinese remainder theorem for the exact DP.
- This check was produced in an AI-assisted session and has not been reviewed by a human.
