# Counterexample hunt: Corollary 11.20 (note_v3 §11.2)

Round 3 refutation track, 2026-10-21. All code here was written from the note's statements only; no code from T1b was used.
Machine use: 1 core; longest run 249 s; memory < 50 MB.

## Target
Corollary 11.20: lower box dim K_p >= dim_H K_p >= D := max_{w,K} D_p(w,K); delta_G(p) >= p^{-(1-D+eps)G} for large G; at p=2, delta_G(2) >= 2^{-(0.147+o(1))G}.

## Verdict
No counterexample was found, and no logical gap was found in the corollary's own proof. **Not refuted.**

## 1. Constants: independent exact recomputation of D_p(w,K) [computer-assisted]
`mydim.c` computes D_p(w,K) directly from the definition. It groups the types tau by G = G_K(tau). For G < K, the types with G_K = G are the classes mod p^{G+1} with sum_t min(v(tau+t), G+1) = G. Each such class has p^{K-G-1} lifts. For G = K it enumerates mod p^K. A weight check (the lift counts sum to p^{K-1}) passes in every run. Subset sums use a byte array, or a 64-bit bitset for p = 2. The two DP versions agree on every case they share.

| (p,w,K) | mine | note table |
|---|---|---|
| (2,1,2) | 0.6462406 | 0.6462 |
| (2,3,16) | 0.7543089 | 0.7543 |
| (2,5,16) | 0.8054461 | 0.8054 |
| (2,7,22) | 0.8333930 | 0.8333 |
| (2,9,22) | **0.8530453** | **0.8530** |
| (3,1,8) | 0.8068733 | 0.8068 |
| (3,2,10) | 0.8591865 | 0.8591 |
| (3,5,13) | 0.9247357 | 0.9247 |
| (5,1,7) | 0.9236947 | 0.9236 |
| (5,3,8) | 0.9691131 | 0.9691 |
| (7,1,5) | 0.9855568 | 0.9855 |
| (7,2,6) | 0.9921376 | 0.9921 |

So 1 - D_2(9,22) = 0.146955 < 0.147, and the stated constant 0.147 is valid as an upper bound on 1 - D. A Monte Carlo cross-check with 30 000 arc4random samples gave 0.85338 +- 0.00024 for (2,9,22) and 0.83285 +- 0.00030 for (2,7,22). Both are consistent with the exact values. An early run with 600 samples used macOS `rand()%2` and gave 0.8494 +- 0.0017; I discarded it because of poor low-bit randomness and replaced it with arc4random.

The values are computed in double precision and are not interval-certified, the same status the note states. The margin, 0.8530453 - 0.8530 = 4.5e-5, is far larger than the rounding error.

## 2. Intermediate lemmas tested on explicit zeros [computer-assisted]
`codes_test.py` builds Theorem 11.17's code family explicitly.
- The base word is e_0 = e_1 = e_2 = e_{c+2} = 1 with c = 2p (Prop 11.13(b)).
- Its simple zero alpha is found by p-adic Newton to precision p^600.
  - p = 2: v(alpha+2) = 3 and slope lambda = 3. This is consistent with F'(x_c) = y_c H'(y_c).
- Windows a_k, types tau_k, G_k and the families F_k are built exactly as in the proof.
- For 150 to 180 codes truncated to 4 to 7 windows, the program computes the zeros z(c) by Newton from alpha. It then checks:
  - (i) the slope is lambda and v(z - alpha) >= P_0;
  - (ii) the distance formula (11.2), v(z - z') = L_k(z) - lambda + d with d < G_k, on every pair;
  - (iii) the cylinder/ball correspondence: c' agrees with c on windows 0..k iff v(z - z') >= rho_k(z).

Results:

| run | pairs | (11.2) failures | slope/P_0 failures | cylinder failures |
|---|---|---|---|---|
| p=2,w=3,K=6, 5 windows | 12 720 | 0 | 0 | 0 |
| p=2,w=1,K=3, 7 windows | 16 290 | 0 | 0 | 0 |
| p=3,w=1,K=4, 6 windows | 15 400 | 0 | 0 | 0 |
| p=3,w=2,K=5, 4 windows (c=7) | all | 0 | 0 | 0 |

`gcheck.py` checks the locality step of the Corollary directly. For a zero z of the word {0,1,2,6} ∪ {16,18,19,22,25,30,33}, the class z mod 2^G has g_2 >= G for G = 8, 12, 14, 16, 18. The check is a brute-force subset-sum DP on S_B, using the definition and not Theorem 3.1. Random classes pass at roughly the rate delta_G predicts.

## 3. Logic of the Corollary (re-derived)
- dim_H <= lower box dim holds for any set.
- N_G := #{classes mod p^G meeting K_p}. Then lower box dim >= D gives N_G >= p^{(D-eps)G} for large G.
- If x is in K_p and y ≡ x (mod p^G), then g_p(y) >= G (Theorem 3.1(a), or Prop 11.21). So delta_G = p^{-G} #{c : g_p(c) >= G} >= p^{-(1-D+eps)G}.
- Theorem 11.17 needs a simple zero alpha ≠ -2 of a finite word. Prop 11.13(b) supplies one, which I also computed explicitly. The theorem also needs p ∤ w; w = 9 is odd.
- I re-checked the denominator bound in (11.3): the sum of v(z+n) over T consecutive n is at most T/(p-1) + max v. I also re-checked the Borel–Cantelli steps A to C of Lemma 11.18. I found no error in either.
- 0.147 < 1/3, so the bound beats 2^{-ceil(G/3)} for large G.

## 4. Minor remarks (no effect on correctness)
- "max_{w,K}" is not shown to be attained. Read it as sup; with the eps already in the statement nothing changes.
- The bound is numerically very weak. The exact delta_32(2) = 0.1016, and Monte Carlo gives about 5.5/G, both far above 2^{-0.147G}. So numerics cannot falsify the bound, and only the constant and the lemmas could be tested.
- Provenance, which concerns Cor 11.19 rather than 11.20: `T1b-Kp-structure/PREDICTIONS_registered_T1b.txt` says it was "written 2026-10-21T22:18:27Z". Its directory mtime is 17:18:27 local, and the machine is UTC-7, so the true UTC is 2026-10-22 00:18:27. The "Z" label appears to be wrong. The order of events is still consistent: registration at 17:18:27, batch1.log from 17:18:57 to 17:36:31, outcomes appended at 17:37:02. The note's "22:18:27 UTC" should be corrected.

## Files
- `mydim.c`, `mydim` (exact and MC D_p(w,K)); `run_log.txt` (outputs); `run_2_9_22.err` (per-G class counts)
- `codes_test.py`, `codes_p2_w3.log`, `codes_p2_w1.log`, `codes_p3_w1.log`, `codes_p3_w2.log`
- `gcheck.py`

Commands: `clang -O2 -o mydim mydim.c -lm; ./mydim p w K` (exact), `./mydim p w K nsamples` (MC); `python3 codes_test.py p w K kmax [c] [nsamples]`; `python3 gcheck.py codes_test.py`.
