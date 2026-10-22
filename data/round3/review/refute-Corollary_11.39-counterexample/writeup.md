# Counterexample hunt: Corollary 11.39 (note_v3.md §11.4) — 2026-10-21

Target: Corollary 11.39 (a) collision bound, (b) Hausdorff-dimension bounds incl. "≥0.99966 at p=13", (c) T_p(k) ≤ p^{(1+θ_p)k/2+O(log²k)}; and the lemmas it rests on (Lemma 11.35(c), Thm 11.36(ii),(iv), Lemma 11.37(a),(c), Thm 11.38 product bound).

## Verdict
No counterexample to the mathematics. Two numerical misroundings in the wrong direction (concrete, reproducible):

1. **Cor 11.39(b) / §0 item 23: "dim_H E_{N0} ≥ 0.99966 at p=13".** The proved bound is 1−θ^set_13 = 0.999656751178… < 0.99966. The Thm 11.38 table itself correctly says 0.999656. The constant 0.99966 is not established by the proof (it may still be true, but it is not proved). Fix: write "≥ 0.999656" (or "> 0.99965").
2. **Thm 11.38 table: "θ_3 ≤ 0.22940".** Exact value θ_3 = 0.229400028286… > 0.22940. Closed form (hand-checkable): θ_3 = (4/9)[log_3(33/32) + 7/4 − 2·log_3 2]. The stated upper bound is false by 2.8e-8. Fix: "θ_3 ≤ 0.22941". The T3a writeup (not the note) also has θ_5 ≤ 0.11013 (true 0.1101338); the note's 0.11014 is correct.
   All other table entries are correct in the right direction (θ_5, θ_7, θ_11, θ_13 ≥ values ≤ stated; 1−θ^set ≥ stated for p=2..13). θ_2 = log_2 3/4 exact (hand-verified, closed form).

These do not affect the asymptotic statements of Cor 11.39, which use θ_p symbolically. Severity: minor.

## Independent checks [computer-assisted, float64 unless stated]
- `constants.py` (exact rationals for Γ_p(j), dist_p(j) from the integer law of W; closed-form tail; mpmath 50 digits): reproduces J0(p), Γ_p(1), dist rows, L_p, θ_p, θ^set_p for p = 2,3,5,7,11,13; asserts P(W=0)=3/2^{p+1}, #subset sums = 3·2^{p−2}, and the affine tail from J0 on. Output `constants.log`. Agrees with T3a `data/theta.txt` to all printed digits.
- `l2check.py` + `run_l2.sh` (exact distribution of Z mod p^K by convolution, float64): 18 factorial cases (p=2: N0=1,2,5,8, K≤20; p=3: N0=1,3,4,9; p=5: N0=1,5,7; p=7: N0=1,7,10; p=11: N0=1,11; p=13: N0=1,13), incl. N0 not divisible by p (partial first block), plus 20 random-x cases (same valuations, random units). Checked: Thm 11.36(iv) 1 ≤ C_{a+j}/C_a ≤ 1+Γ_{G_a}(j) for every level and every j ≤ J; Lemma 11.37(a) Γ_block(j)=Γ_p(j) on every full block; Thm 11.38 product bound C_k ≤ (partial-block factor p^j)·Π(1+Γ_p(min(J_m,k−a_m))) (stronger than the proof's) for every k; Parseval C_k−C_{k−1} = Σ_{ord p^k} Π cos²; Lemma 11.35(c) both inequalities (k ≤ 7). Zero violations. (One initial flag at p=13, k=5 was float cancellation in C_k−C_{k−1}≈1e-18; recomputed from the direct Fourier sum: T=7.36e-9 ≤ 5.59e-7.) T_13(k), N0=13, reproduces §10.4.1 (7.7952e-3, 1.4997e-3, 3.7507e-6, 1.0362e-7, 8.8918e-9). C_k−1 values agree with Computation 11.43 (e.g. p=7,N0=1: 0.0193292; p=13,N0=13: 2.25377e-5).
- `setcheck.py`: Lemma 11.37(a) congruence P_m(r) ≡ ε_p e_{p−1−r} mod p^{J_m} for all m < 4000/3000/2000/1000/400/300 (p=2..13): 0 failures. θ^set construction: block residue counts equal dist_p(J_m) with the true factorials, and the exact collision mass of the "one subset per residue" measure at block levels equals Π p^J/dist_p(J) (equality: conditional on a collision mod p^J the two chosen subsets coincide, so the carry is 0) — consistent with the claimed block factor.

## Proof read (no gap found)
(a) is C_k p^{−k} with Thm 11.38. (b) Markov + Borel–Cantelli + local-dimension/mass-distribution principle on ultrametric balls: standard and correct; the set-measure is supported in E_{N0}, and Thm 11.36 with |μ̂|² replaces cos² verbatim. Last partial block costs ≤ p^{J_M} = p^{O(log k)}. (c) Cauchy–Schwarz over the p^k(1−1/p) frequencies of exact order p^k; T_p(k) of §10.4 equals Σ_{ord p^k}|ν̂| for N0=p. Thm 11.38 bookkeeping (M+1 ≤ (p−1)/p(k+e0+log_p k+O(1)), count of v_p(i)=j, f_p(j) ≤ j+1) re-derived.

## Commands / timings
constants.py 1.0 s; run_l2.sh (all cases) < 10 min single core; l2check p=13 reruns < 1 min; setcheck.py 0.2 s. Memory < 200 MB.
