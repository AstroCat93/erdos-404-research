# Counterexample hunt: Theorem 11.29 (note_v3 §11.3) — round 3, 2026-10-21

Target: Theorem 11.29, mu(C ∩ {g_2>=G}) <= B_L(n0) + n0 2^{-K} + 2^{-c} E_C + 2^{-k} P(Bin(K-k,1/2) <= c+s_L-s(r0)), for C in {C0=8Z_2, C2=2+8Z_2, C6=6+16Z_2}.

Verdict: **not refuted.** No counterexample to the theorem or to any intermediate lemma was found. The proof was re-read step by step and every step checked out (see §3). All code is independent and new in this directory. It does not import any other track's code.

## 1. Code (all in this directory; Python 3.9, at most 3 cores, each run under 3 min, under 200 MB)

- `common.py`: 2-adic arithmetic at precision 2^600. It provides alive-path enumeration with S_e and S_e', the frozen-state weights a_n^{(λ)} and ρ_n, the targets τ_n, and an exact test for g_2(x) >= G (it tracks alive S_e mod 2^G).
- `t0_sanity.py`: |{g>=k} mod 2^k| restricted to even classes = 1,2,4,6,12,24,(34,62) for k=1..8, which matches §3.4. MC δ_32 = 0.0975 ± 0.005, against the note's 0.1016.
- `t1_certs_slopes.py`: Prop 11.25.
- `t2_window.py`: exact test of identity (11.4).
- `t3_firstmoment.py`: Prop 11.26 and E[Y_0 1_C] <= E_C.
- `t4_chain.py`: pointwise test of each deterministic step of the proof of Thm 11.29, plus Monte Carlo of the probabilistic steps. Outputs are in `t4_out_seed{21,31,32,33_bias}.txt`.
- `t5_lemmas.py`: Lemma 10.2(a)–(d), Lemma 11.23(a)–(e).

Commands: `python3 t1_certs_slopes.py 7|99`; `python3 t2_window.py 11 12`, `python3 t2_window.py 12 16 C6 28 45 4`, `python3 t2_window.py 13 13 C0,C2 19 60 60`; `python3 t3_firstmoment.py 3 3000`; `python3 t4_chain.py 21 300`, `python3 t4_chain.py 31|32 1500`, `python3 t4_chain.py 33 1500 bias`; `python3 t5_lemmas.py 5`. Each run took between 2 s and 135 s.

## 2. Results

All results in this section are [computer-assisted] (finite checks) or Monte Carlo. They are evidence, not proof.

1. **Certificates (Prop 11.25), exact rational arithmetic.**
   - S_e(-4) ∈ {1,-5,7,1,-2,-8,4,-2}, with max valuation 3.
   - Φ_e(-4), family A: {4/5,-26/5,34/5,4/5}, valuations ≤ 2. Family B: {-16/5,-46/5,14/5,-16/5}, valuations ≤ 4.
   - Φ_e(-8), family B, over all 64 choices of (e4..e9): never 0. The valuation histogram is {1:32,3:16,4:8,5:3,6:4,7:1}, identical to the note.
   - The identity S_e = y(y-1)Φ_e(y) holds at 200 random rational points.
2. **Slopes.** About 9×10^4 alive paths were checked, at 9000 points that were random or adversarial (x ≡ −m mod 2^j, so that x+2, x+4, … are highly divisible). Depths ranged from the first n with V_n >= V_cert up to n = 19+. The maximum slopes found were 1, 3, 3 for C0, C2, C6, against the bounds 1, 3, 6. No violations.
3. **Window identity (11.4), exact.** For 2935 paths in 174 atoms satisfying Γ_L(n), the test enumerates every w mod 2^D in the atom x0+2^m w. Both the unweighted and the ρ-weighted child expectations equal 2^{W_N-W_n} ρ_n(e) exactly (as Fractions). The atoms were 170 in C0/C2 with n ∈ [19,60] and 4 in C6 with n ∈ [28,45], D <= 16. The children's slope always equals the parent's (Prop 10.6(i)).
4. **First moment (Prop 11.26).** The unnormalised ∫_{C∩Γ*} Z_n is about 0.06, 0.12, 0.13 for C0, C2, C6, against the bounds 1, 8, 256. E[Y_0 1_C] is at most about 0.17, against E_C = 1, 64, 16384. Γ_0 ⊆ Γ_* held in every sample, and max ρ = 2 <= 2^L.
5. **Proof chain (Thm 11.29).** The test covers G ∈ {128,256,512}, n0 ∈ {19,40,60,80,150} and c ∈ [−3,7], with about 3300 points per (class, G, n0) across 4 seeds, one of them biased toward extreme low-digit sums. The following held pointwise with zero violations:
   - (P1) ¬E_good ⇒ some i <= n_{ℓ*}+ℓ0 has v(x+i) > h_L(max(n0,i−ℓ0)).
   - (P2) On E_good: V_{n_{ℓ+1}} < G, and g>=G ⇒ P_{n_{ℓ+1}} ≠ ∅ for all ℓ <= ℓ*.
   - (P3) On C∩E_good∖Hit∩{N_K>n0}: s(x mod 2^K) <= c+s_L. This was exercised 81,657 times.
   - Lemma 10.2(d) held at every point.

   In the Monte Carlo, the barrier term's ratio to 2^{-c}E[Y0 1_C] was at most 0.11. The walk term's ratio to 2^{-k}P(Bin <= ·) was at most 0.58.
6. **Valuation lemmas.** These were tested on 4000 points, half of them near negative integers, with no failures.

**The final inequality cannot be tested numerically at accessible G.** At every G where μ(C∩{g>=G}) can be computed (G <= 512), the right-hand side is at least n0 2^{-K} >= 0.47 > μ(C). So the bound is vacuous there. The note itself says it beats μ(C) only from G ≈ 2^18, 2^29, 2^44. The meaningful falsification test is therefore the pointwise and identity checks above, and they all passed.

## 3. Proof re-check (by reading, not machine-checked)

These are my own re-derivations. No gap found.

- **Bad windows.** ¬Γ_ℓ means 2M > V_{n_ℓ}−3L−3 >= n_ℓ−log2 n_ℓ−3L−4, using V_n >= n−s(n) and s(n) <= log2 n+1. h_L is increasing for n >= 2, and n_ℓ >= max(n0, i−ℓ0). The union bound is valid. When h < −1 the terms exceed 1, which is harmless.
- **Barrier.** On Γ_ℓ, Lemma 10.2(b) gives V_N < 2N <= G. Lemma 11.23(d) is correct. The (W1)–(W3) derivation from Γ_L(n) checks out. Γ_ℓ and W_{n_{ℓ+1}} are F_ℓ-measurable on Γ_ℓ because M_N < m and the cylinders partition. Optional stopping applies with Y >= 0. And Y_0 <= 2^L Z_{n0} 1_{Γ0}, since ρ <= 2^λ.
- **Prop 11.26.** The count of 2^{n−1} paths is right. μ(B_r) = 2^{λ_r−V_n}. Root separation gives |R_e| <= 2^{L+1−k}. The constants are 1, 8, 256.
- **Walk.** n_{ℓ+1} <= 2^K+ℓ0−1 <= T follows from the definition of K. Lemma 11.23(a) needs δ < 2^K, which uses 2^K >= ℓ0. The integer c gives s(r) <= c+s_L. On C, s(x mod 2^K) = s(r0) + Bin(K−k, 1/2).

**Remark (not an error).** For C6 with n0 = 19, Γ_0 is empty. It needs V_19 >= 2M_33+21, but V_19 < 19+M_19 <= 19+M_33. So the theorem is vacuous for small n0 in C6, since B_L(19) ≈ 288. This is consistent with the hypotheses as stated; the corollary uses n0 >= 4 log2 G + 58.
- Extra run `t2_window.py 77 16 C6 28 50 6` (larger D) was stopped after 10 min for time; no output, so no result is claimed from it.
