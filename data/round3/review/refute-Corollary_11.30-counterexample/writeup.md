# Counterexample hunt: Corollary 11.30 (note_v3 §11.3), 2026-10-21

Verdict: **not refuted.** No counterexample to the corollary or to any lemma it uses was found. All code was written independently from the definitions in §10.1/§11.3; no T2 or lead code was reused.

## What the corollary can and cannot be tested against
The bound beats the trivial bound μ(C) only for G ≥ 2^18 (C0) up to G ≥ 2^44 (C6). So a direct numerical refutation at computable G is impossible. Testing therefore targets (i) every intermediate lemma on small cases, and (ii) the constants.

## Tests (code in `code/`, logs in `logs/`, ≤ 3 cores, all runs < 5 min except an aborted duplicate)
| test | what | result |
|---|---|---|
| A `testA_slopes.py 2 70 20000` (19 s) | Prop 11.25 on random points and on points 2-adically close to negative integers in each class (n ≤ 70); Lemma 11.24(b); Lemma 11.23(a)–(c); Lemma 10.2(d); finite certificate values; identity S_e(−m−2)=(−m)(−m−1)Φ_e(−m) (500 random words) | 0 violations. Largest slopes seen 1, 3, 3 (certified bounds 1, 3, 6). Certificate valuations reproduced exactly: C0 {0,0,0,0,1,1,2,3}; C2 family A {2,1,1,2}, B {4,1,1,4}; C6 family B histogram {1:32,3:16,4:8,5:3,6:4,7:1}. |
| B `testB_window.py` (L=1: 300 trials; L=3: 150; L=6: 12 trials, D ≤ 13; 17 s / 3.6 min / 4.5 min) | **exact** check of both identities (11.4) on whole cylinders C_n(x): all w mod 2^D, two random high tails each; also Prop 10.6(i) (child slope = parent slope; no slope ≤ L child of a slope > L parent), constancy of V_n, V_N, parent set on the cylinder, and independence from bits beyond m+D | 0 failures; unweighted and ρ-weighted sums equal 2^D·2^{W_N−W_n}ρ_n(e) exactly for every parent |
| C `testC_mc.py` (Monte Carlo) | Prop 11.26; E[Y_ℓ 1_C] nonincreasing; barrier inequality Prop 11.28 for c=−2..3 | ∫Z ≈ 0.060, 0.127, 0.137 vs bounds 1, 8, 256; E[Y_ℓ] flat or decreasing within MC error; barrier LHS ≤ 2^{−c}E[Y_0] with large margin |
| D `testD_constants.py 120` (95 s, mpmath 60 digits) | exact RHS of Theorem 11.29 with the corollary's n0, c, at every breakpoint of (n0, K) for 2^10 ≤ G ≤ 2^120, exact binomial tail; 1−H2(0.227); assertion 2^K > G/8 and all hypotheses of Thm 11.29 | sup RHS·G^0.227 = 17.52 (C0), 1119.8 (C2), 1.6776e5 (C6); side terms 1.584, 1.701, 1.875 (lead: 1.585, 1.701, 1.876); 1−H2(0.227)=0.227255>0.227; all below 29, 1325, 1.98e5; sum 199354 ≤ 2.0e5 |

## Hand checks of the proof chain (no error found)
- Main-term constants: (2^{1+s_L−s(r0)}E_C + 2^{−k})·2^{αk}·8^α = 20.88, 1316.4, 1.9716e5. ✓
- s_L values 2, 3, 3 for ℓ0 = 4, 8, 14. ✓ E_C = 2^L·2^{L−1+max(0,L+1−k)} = 1 (L=1 uses ρ≡1), 64, 16384. ✓
- Γ_L(n) ⇒ (W1)–(W3); Γ_0 ⊆ Γ*(n0); Γ_ℓ is F_{n_ℓ}-measurable; V_N < 2N ≤ G on Γ_ℓ. ✓
- Bad-window union bound and monotonicity of h_L; walk term (W_{N_K+δ} formula; ℓ ≤ ℓ*; N_K ≤ n0 has measure n0·2^{−K}). ✓
- Partition of Z_2: odd, 4 mod 8, C0, C2, C6, 14 mod 16. Density transfer by Theorem 3.1(c). ✓
- For G ≤ 2^10 the claimed bounds exceed μ(C) (6.0, 274.7, 41051 at G = 2^10). ✓

## Remarks (not errors)
- My breakpoint sup for C2 (1119.8) is slightly below the lead's 1121. It may be a grid difference, and it is immaterial.
- For C6 the certificate allows slope 6, but no slope above 3 was observed, even at adversarial points. The constant E_C is therefore very loose, as the note says.
- Test B for L=6 used D ≤ 13 only. A run with D ≤ 17 was stopped after 18 min as redundant.
