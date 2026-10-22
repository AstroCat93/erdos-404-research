# Round-3 adversarial referee report, LOGIC lens (track verify-logic)

Date: 2026-10-21. Referee: an AI instance (Claude), not a human. Scope: the round-3 block of §0 and §11 of
`e404r3/note/note_v3.md` (2502 lines; §11 = lines 1821–2462), with spot checks against §§1–3 and §10 where §11 cites them.
Method: every proof labelled [proved] in §11 was read line by line against its cited lemmas; every finite or
numerical claim that a proof relies on was recomputed with code written for this report (no track code was
imported; one track script, `p2k2.py`, was re-run as is). No file outside this directory was modified.

Labels used below: **OK** = proof complete as written (possibly after trivial repairs noted); **GAP** = a step is
missing; **FALSE** = a statement is wrong. Severity: fatal / serious / minor.

## 1. Findings (most severe first)

### F1 [serious; GAP] "H′(p) ⇒ μ(K_p) > 0" is not proved (§0 item 22, §11.0 headline 3, Conjecture 11.10, §11.7 Q1)

Theorem 11.7 as displayed is correct: *for a given atom* A of G_j with M_j(A) > 0, the uniform bound
κ·r^max ≤ K gives (E1) with Λ = 1 + p^L K S_j / M_j(A), and then μ(K_p ∩ A) > 0 **provided**
μ_A(σ_j < ∞) < 1/Λ. Conjecture 11.10 then states H′(p) only as "κ r^max stays bounded on the unfrozen atoms"
and asserts "By Theorem 11.7 this would give μ(K_p) > 0"; §0 item 22 and §11.7 say μ(K_p) > 0 "is reduced to"
H′(p). The missing step is the **existence of an atom A with M_j(A) > 0 and μ_A(σ_j<∞) < 1/Λ(A)**.

Why it is not automatic:
- Theorem 11.3(d) only says that the atoms with μ_A(σ_j<∞) ≥ ε have total measure ≤ μ(σ_j<∞)/ε → 0. That is
  useless unless the atoms with M_j(A) > 0 have total measure much larger than μ(σ_j<∞).
- With the note's own Λ, S_j/M_j(A) is not small on atoms where M_j(A) is near its minimum
  2^{-n_j} p^{m_j}·(p/2^p)^L (S_j/M_j(A) can be as large as poly(n_j)). A sharper bookkeeping (sum the
  per-window increments p^L K·2^{-n_ℓ}p^{m_ℓ} M_ℓ with the actual 2^{-n_ℓ}p^{m_ℓ}, which decays
  super-geometrically along the windows) does give a uniform Λ_0 = 1 + K p^L (2^p/p)^L (1+o(1)) over all atoms
  with M_j(A)>0 for large j. Then summing Theorem 11.4 over atoms gives only
  μ(K_p) ≥ μ(M_j>0)/Λ_0 − μ({σ_j<∞} ∩ {M_j>0}).
  With C′ (M_{n_ℓ} ≤ 3 log_p n_ℓ), μ(σ_j<∞) is of order n_j^{-2}, while the only proved lower bound for
  μ(M_j > 0) ≈ δ_{V_{n_j}}(p) is exponentially small (Corollary 11.20). So the inequality closes only under
  an unproved polynomial lower bound on δ_G(p), or an unproved near-independence of {M_j>0} and {σ_j<∞}.
  (These events are plausibly correlated: x near a negative integer −i with i > n_j has a large shadow value
  γ_p(i) and also a deep future gate at i.)
- Choosing atoms A_j(z) shrinking to a point z ∈ K_p does not help either: nothing proved says any z ∈ K_p has
  σ_j(z) = ∞ (Lemma 11.18 gives only 𝔐_k = o(k) for code-measure-typical z, far weaker than 3 log n), and even
  then the conditional failure probability at the first "unknown" gate i ≡ −z (mod p^{m_j}) is of order 1 when
  i ≈ p^{m_j/3}.

Repair (any one): (a) state H′(p) like H(p) of Corollary 11.5, i.e. *including* "there is an atom A of some
G_j with M_j(A) > 0 and μ_A(σ_j<∞) < 1/Λ"; or (b) state the conclusion as "H′(p) implies μ(K_p ∩ A) > 0 for every
atom A with M_j(A) > 0 and μ_A(σ_j<∞) < 1/Λ"; and correct §0 item 22, §11.0 headline 3, Conjecture 11.10 and the
§11.7 status line accordingly. The odd-p "reduction" is then to H′(p) **plus** a good starting atom.

### F2 [serious (false statement labelled [proved]); low importance] The "Consequence [proved]" after Theorem 11.45 is false

Text: "for the family H = p^{t−1} ... no element of that window is congruent to its factorial at the top digit
t+c of the demand (since c ≥ v(i!) ... would require v(i!) ≥ c+1+ℓ(i))". This only shows that the **lower bound**
(d) does not reach the top digit; it does not show non-congruence, and non-congruence is false.
Exact counterexample (`check_selfsim_units.py`, also by hand): p = 3, t = 3, H = 9, c = v_3(8!) = 2, demand 3^5,
unit position K′ = 1 (X = 27):
- y_8 = ∏_{j=1}^{8}(27 − j) satisfies v_3(y_8 − 8!) = 5 (= t + c) for K′ = 1, 2, 4, 5;
- y_6 = ∏_{j=3}^{8}(27 − j) satisfies v_3(y_6 − 6!) = 5;
- y_i ≡ i!A_i (mod 3^5) for i = 6, 7, 8.
Same phenomenon at p = 5, t = 3 (i = 20..24 agree with i!A_i mod 5^7; i = 20, 24 agree with i!), p = 7, t = 3
(i = 42..48), and y_i ≡ i! (mod p^{t+c}) for p = 3, t = 4 (i = 20, 25) and p = 3, t = 5 (i = 75..77).
Cause: near i = p^D − 1 the sum Σ_{s≤i} 1/(s − p^D) = −H_{p^D−1}+… cancels (Wolstenholme-type), so the loss ℓ(i)
in (b),(d) does not occur and the true valuation exceeds the bound. Theorem 11.45(a)–(d) themselves are correct as
lower bounds (checked on 6 parameter sets, 30 positions each). Repair: delete the "Consequence" or restate it as
"the bound (d) does not by itself reach digit t+c"; drop the conclusion about "not implied by any covering statement
about the factorials" or label it [heuristic].

### F3 [minor; over-claim] Proposition 11.53: "the annealed second-moment route is closed"

E Z_G^2 ≥ p^G/4 is proved (and N_G(−2) = 2^{M_G−1} was re-checked by brute force for (p,G) = (2,6), (3,3), (3,4),
(5,2), (7,2)). But the conclusion "E Z_G^2/(E Z_G)^2 → ∞, so the annealed second moment cannot prove μ(K_p)>0"
needs E Z_G = o(p^{G/2}), which is supported only by the numerics of Computation 11.55 (linear growth, [heuristic]);
and truncated annealed moments are not excluded by a proof. Label the "route closed" sentence [heuristic] or add
the needed bound.

### F4 [minor; numerical] Two rounded bounds point the wrong way
- Corollary 11.39(b) and §0 item 23: "dim_H E_{N0} ≥ 1 − θ^set_p (e.g. ≥ 0.99966 at p = 13)". The value is
  1 − θ^set_13 = 0.99965675…, so "≥ 0.99966" is false; write ≥ 0.99965 (the table of Theorem 11.38 correctly has
  0.999656).
- Theorem 11.38 table: "θ_3 ≤ 0.22940", but θ_3 = 0.2294000283 (T3a's `theta.txt` and my recomputation). Write
  ≤ 0.229401. (All other θ_p and 1 − θ^set_p entries are correctly rounded.)

### F5 [minor] Theorem 11.48(b): "L^1(Y) < √L^2(Y)" fails when L^2(Y) = 0 (e.g. Y = {1} in Z/2: both are 0).
Write ≤, strict when L^2 > 0. The consequence "L^2 < 1 ⇒ L^1 < 1" is unaffected.

### F6 [minor; wording] §0 item 20: "dim_H K_p ≥ D_p(w,K) ≥ 1 − p^{−L_p}". The second inequality holds for
w = 1, K ≥ L_p + 1 (Corollary 11.19(a)), not for all (w,K): e.g. D_7(1,1) = 6/7 < 1 − 7^{−2}.

### F7 [minor; data/text inconsistency] Computation 11.43 says Theorem 11.36(iv) "holds on all 12 data sets", but
`data_r3/T3a-q3-fourier/data/l2_summary.txt` prints "TheoremD checks=12 viol=1" for p = 3, N0 = 1. The flagged step
is 0→1, ratio 1.125 against "bound" 1.031 = 1 + Γ_3(1): the archived checker compared the *partial* first group
{1!, 2!} with the full-block Γ_3(1). For that group D = 1/8 equals its own Γ_{G_0}(1) = 1/8 (carry 0), so
Theorem 11.36(iv) is not violated. Add a sentence, or fix the diagnostic, so a reader of the data is not misled.

(No fatal error was found.)

## 2. Verdict on every numbered result of §11

| id | verdict | notes (what was checked) |
|---|---|---|
| Lemma 11.1 | OK | (a)–(g) re-derived; (b) strict since Σ_{k≤M}p^{-k}<1/(p−1); (g)(ii) expansion and (1+E)^{-1}≡1 mod p^{m−M_n} checked. |
| Prop 11.2 | OK | D ≥ L+1 from (W1); slope preservation from v(π′_j) ≥ m−M_N > L; constancy of q_f (D+λ ≤ m), u (λ < m−M_N), a_N^{(λ)} (depends on x mod p^λ); count in (iv). **Brute force** from the definitions (paths, aliveness, slopes, frozen weights; no use of the proposition's formulas): 14 windows at p=3 (L=0,1) and p=5 (L=0); per-parent identity E_wX_e = 2^{N−n}p^{−D}ρ_n(e) exact in rationals; child slope = parent slope always; child sums independent of digits above m+D. |
| Thm 11.3 | OK | (a) atoms/ENV measurability; (b) measurability of ρ at ℓ=j via (W2), at ℓ>j via (W3) of window ℓ−1; martingale identity **verified exactly** E[M_{ℓ+1}|atom] = M_ℓ in the 14 brute-force windows; zero absorbing; (c) König; (d) Borel–Cantelli with K_ℓ=⌈3log_p n_ℓ⌉. |
| Thm 11.4 | OK | L²-bounded martingale, Cauchy–Schwarz, zero absorbing. |
| Cor 11.5 | OK | (11.1) re-derived; H(p) correctly includes the atom condition. |
| Thm 11.6 | OK | Fourier substitution and Parseval; class form and Jensen. Parseval form of Var_wΣ checked numerically on the 14 windows (agreement to 1e−9). |
| Thm 11.7 | OK as stated; **implication to μ(K_p)>0 has a GAP (F1)** | Chain M²R ≤ (2^{−N}p^{V_N})²κ r^max Σμ_e² ≤ p^L K 2^{−n}p^m M_ℓ re-derived, and checked numerically on the 14 windows (equality when L=0 and all parents share one profile, as expected); p^m < p^{n/(p−1)}n³ from Lemma 11.1(b) with n=0. |
| Prop 11.8 | sketch (not refereed as proved) | — |
| Remark 11.9 | facts OK | c_3..c_13 = 1/8, 0.1323771, 0.0823662, 0.0266813, 0.0032999 recomputed; worst incomplete block = cos²(π/p) confirmed; p ≥ 7 threshold for p^{D} vs 2^{(N−n)/2} correct (p²<2^{p−1}). |
| Thm 11.11 | OK | (a) coefficient formula and bounds; (b) double-series summability for h ∈ pZ_p; (c) nonvanishing via F_e(−m) ≡ 1 mod (m−1), Strassmann. |
| Lemma 11.12 | OK | contraction constant V−2λ ≥ 1; uniqueness bracket of valuation λ; (b) distance formula. |
| Prop 11.13 | OK | (a) v(c_0) ≥ 2λ+2, v(Δ′_J) ≥ 2λ+1; (b) F_e = y·H(y), H(0) = −c!, H′(0) ≡ 1 (re-checked numerically for p ≤ 7, 2p ≤ c < 2p+4). |
| Thm 11.14 | OK | relies on Thm 3.2(a) (K_p∩Z_{<0}={−2}), Cor 3.3, Thm 3.5 (simple roots), all checked in earlier rounds. |
| Thm 11.15 | OK | Step 0: f(u)=Σd_iR_{i+1}, R_n ≡ R_a (p^a), pure periodicity mod k′; checked numerically that every residue mod k ≤ 60 is hit with p∣u (p=2,3,5; p=7 except k=49, where the construction needs digits beyond the search range p^8 — consistent with the proof, which uses ≥ c digits ≥ a+2). Step 1 records argument (consecutive records ≥ p^{M*} apart). Step 2 Cauchy–Davenport digit by digit. Step 3 rescaled Hensel: all valuation estimates re-derived (b_i, i<k: ≥ i(s−M) ≥ w; b_k ≡ θ; i>k: ≥ (i−k)s−γ ≥ w), v(H′(1)) = κ < w. |
| Prop 11.16 | computer-assisted, OK | `p2k2.py` re-run: 64 configurations, the 16 bad ones all have J_{u+1}=2 (avoided by u ≡ 2 mod 4); levels mod k: f(u) = 3+Σ_{i≥2}d_iR_{i+1} re-derived. |
| Thm 11.17 | OK | codes, (11.2) (bracket valuation < G_k ≤ g_k, tail ≥ L_{k+1}), cylinder ⇔ ball, constancy of ρ_k on balls (v(z+n) ≤ L_k−2λ−1 for n ≤ a_k), ρ_{k+1} > ρ_k (G ≥ w ≥ 1), mass-distribution estimate (11.3), equidistribution of types (p∤w). |
| Lemma 11.18 | OK | (F1),(F2); Steps A–C (ball around a deep gate is a ball around −n; summable bounds k^{−2} and stretched-exponential). |
| Cor 11.19 | (a) OK; values reproduced | (a): q_s ≡ (p−1)!(−1)^u/u! mod p^J, E min(J,L_p) = Σ_{s<L_p}p^{−s}. **Independent recomputation of D_p(w,K)** (`check_wdim.py`, own code) for 18 cases: (2,1,2) 0.6462406, (2,3,16) 0.7543089, (2,5,16) 0.8054461, (2,7,22) 0.8333930, (3,1,8) 0.8068733, (3,2,10) 0.8591865, (3,4,12) 0.9111565, (3,5,13) 0.9247357, (5,1,7) 0.9236947, (5,2,8) 0.9548430, (5,3,8) 0.9691131, (7,1,5) 0.9855568, (7,2,6) 0.9921376, (11,1,5) 0.9982683, (13,1,5) 0.9996567, (17,1,4) 0.9999634, (19,1,4) 0.9999906, (23,1,4) 0.9999964, (2,9,22) 0.8530453 (1101 s) — every table entry, including the headline 0.8530, is a correct round-down. |
| Cor 11.20 | OK | dim_H ≤ lower box; locality. |
| Prop 11.21 | OK | density of finite sums; 1-Lipschitz. |
| Lemma 11.23 | OK | (a)–(e) re-derived. |
| Lemma 11.24 | OK | (b) mod 2^{t+1} computation; (c) identity S_e = y(y−1)Φ_e(y) checked on 500 random paths. |
| Prop 11.25 | OK | finite cases recomputed: S_e(−4) ∈ {−8,−5,−2,1,4,7}; Φ_e(−4) families; Φ_e(−8) histogram {1:32,3:16,4:8,5:3,6:4,7:1} identical to the note. Numerical: max slope of alive paths = 1 on C_0 (n=10) and 3 on C_2 (n=12), exhaustive mod 2^22. |
| Prop 11.26 | OK | strong Hensel + root separation; |R_e| ≤ 2^{max(0,L+1−k)}. Numerically ∫_{C∩Γ*}Z_n = 0.0625 (C_0, n=10; bound 1) and 0.125 (C_2, n=12; bound 8), i.e. E[Z_n|C∩Γ] ≈ 0.51, 1.07, consistent with the note's 0.52, 0.97. |
| Lemma 11.27 | OK | Γ_L(n) is F_n-measurable (decided by x mod 2^m); (W1)–(W3) from Γ_L; (11.4) both identities. |
| Prop 11.28 | OK | optional stopping for a bounded stopping time on a nonnegative supermartingale. |
| Thm 11.29 | OK | bad-window union bound (h_L monotone, μ{v(x+i)>h} = 2^{−⌊h⌋−1}); V_N < 2N ≤ G on Γ; walk term (n_{ℓ+1} ≤ 2^K+ℓ_0−1 ≤ T). |
| Cor 11.30 | OK | 1−H_2(0.227) = 0.227255; main constants recomputed 20.885, 1316.37, 1.97159e5; side-term suprema recomputed on a dense sample of G ∈ [2^10,2^60]: 1.5844, 1.7005, 1.8755 (lead: 1.585, 1.701, 1.876). |
| Prop 11.31 | OK (conditional) | F_0-measurable level c(x): 2^{−c(x)}Y_ℓ is still a supermartingale. |
| Prop 11.32 | OK | S_{1,3} = (x+2)³ checked; Taylor-minimum at i=3 re-derived. |
| Lemma 11.35 | OK | — |
| Thm 11.36 | OK | (i)–(iv) re-derived; (ii) uses that no level lies strictly between a and a+J and level-(a+J) terms vanish mod p^{a+J}. |
| Lemma 11.37 | OK; table reproduced | Γ_p(1), J_0(p), L_p for p = 2,3,5,7,11,13 recomputed exactly (own enumeration of 3^p sign vectors); P(W=0) = 3/2^{p+1}, 3·2^{p−2} distinct subset sums, closed form for j ≥ J_0 and monotonicity asserted in code. |
| Thm 11.38 | OK; constants reproduced (one rounding, F4) | proof re-derived (block factors ≤ 1+Γ_p(J_m); count of v_p(i)=j; e_M formula). θ_p, 1−θ^set_p recomputed for p ≤ 13 to 12 digits, identical to T3a; θ_2 = log_2 3/4 by hand. |
| Cor 11.39 | OK (rounding F4) | (b) set version: block factor p^{J}/dist_p(J); last partial block trivially O(log k). |
| Prop 11.40 | OK | φ_W(t/p) = φ_p(U t/p). |
| Prop 11.41 | OK | (a) pigeonhole, M^s < p^d; (b) conditional law **reproduced exactly** for actual gate blocks (p,m) = (5,124), (5,624), (7,342): 2/3 δ_0 + 1/6 δ_{±U′} with U′ as stated. |
| Prop 11.42 | OK | — |
| Comp 11.43 | small depths reproduced | own exact DP: C_k for p=2 (k ≤ 14), 3 (k ≤ 9), 5 (k ≤ 5), 7 (k ≤ 4) identical to T3a's archived lists. See F7. |
| Thm 11.45 | (a)–(d) OK as lower bounds; **"Consequence" FALSE (F2)** | identity y_i = i!A_iB_i and bounds asserted exactly on 6 parameter sets × 30 positions. |
| Thm 11.46 | OK | **fibre identity checked**: direct miss count = Σ_T fibre miss counts on 212 positions over 6 (p,t,H) configurations (p = 3,5,7; covering and non-covering cases). |
| Cor 11.47 | OK | (b) via the coset criterion; V_p elements pairwise incongruent mod p^{D_p}. |
| Thm 11.48 | OK (strictness F5) | (c) c_1(13,ρ) ≥ 2.2024e−5 recomputed (13^4·c_1 < 1 < 13^5·c_1). |
| Remark 11.49 | OK | Cov(13,3,H) recomputed exhaustively over unit K′: holds H = 19..26, fails 27..31, holds 32. |
| Thm 11.50 | computational (not re-run) | Legendre values 943 531 272 and 17 927 094 312 recomputed. Logic: rests on Prop 10.10 (round 2). |
| Lemma 11.52 | OK | (c) indexing ("last candidates") is terse but correct once candidates include both choices of e_n. |
| Prop 11.53 | inequality OK; interpretation over-claimed (F3) | N_G(−2) brute force, 5 cases. |
| Lemma 11.54 | OK | geometric mean × 2^p = 1 numerically (p ≤ 13). |
| Comp 11.59 | OK, and the identity is exact | D_p(1,K) → (p−1)/p·E log_p dist_p(1+v(y+1)) = 1−θ^set_p since Σ_j(1−1/p)p^{−j}(j+1) = p/(p−1). |

Heuristics/conjectures (11.10, 11.22, 11.33, 11.34, 11.44) are correctly labelled; no proof claimed.
Arithmetic inside Heuristic 11.33 ((3/4)^K(2/3)^K = 2^{−K}) and Remark 11.9 checked.

## 3. Reproduction of this report's checks (single core each, all < 1 GB)

All scripts are in this directory (`verify-logic/`), logs in `verify-logic/logs/`. Python 3.9, numpy 2.0.2, mpmath 1.3.0.

| script | what | wall |
|---|---|---|
| `check_window.py 3 12 15 0 4 1`, `3 16 22 1 6 2`, `5 16 21 0 4 3` | brute-force Prop 11.2, Thm 11.3(b), Thm 11.6 (Parseval), Thm 11.7 chain; logs `check_window_*.log` | 0.4 s, 6 s, 4 s |
| `check_wdim.py p w K` | D_p(w,K), 19 cases; logs `check_wdim*.log` | ≤ 1 s each; (3,5,13) 6 s; (2,7,22) 77 s; (2,9,22) 1101 s |
| `check_gate_theta.py` | Lemma 11.37 table, θ_p, θ^set_p, Prop 11.41(b), small C_k | 3 s |
| `check_misc.py` | Prop 11.25 finite cases, Lemma 11.24(c) identity, Prop 11.13(b), c_p, Lemma 11.54, c_1(13,ρ), Legendre values, N_G(−2), Cor 11.30 main constants | < 1 s |
| `check_step0.py` | Thm 11.15 Step 0(b) | 40 s |
| `check_cov.py` | Thm 11.45 bounds, Thm 11.46(b) fibre identity, Remark 11.49 | 132 s |
| `check_selfsim_units.py` | counterexample to the Thm 11.45 "Consequence" (F2) | 3 s |
| `check_t2_side.py` | Cor 11.30 side terms | ~60 s |
| `check_p2_firstmoment.py 22` | Prop 11.25/11.26 numerics at p = 2 | 59 s |
| `python3 -I note/code_r3/T1b-Kp-structure/p2k2.py` (track script, re-run unchanged) | Prop 11.16 | < 1 s |
