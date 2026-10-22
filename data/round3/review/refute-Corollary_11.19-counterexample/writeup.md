# Adversarial check of Corollary 11.19 (note_v3 §11.2), counterexample-hunter track, 2026-10-21

Verdict: NOT refuted. No counterexample to Cor. 11.19(a), Thm 11.17 (as used), or the table values.

## Code (all written here from the definitions in note_v3 §11.2; wdim.c not used or read)
- `mydim.c` (clang -O3): exact N_{w,K}(tau) for every y mod p^{K-1}; byte-array subset-sum DP mod p^G
  (odd p) / rotating 64-bit bitset (p=2, M>=64). Outputs the exact histogram {N: count}.
- `mydim_sum.py`: D_p(w,K) from the exact histogram in mpmath (40 digits) -> no floating-point issue.
- `brute.py`: brute-force oracle (enumerates all 2^P subsets); agrees with mydim to 10 digits on
  (2,1,2),(2,3,7),(3,2,5),(5,1,4),(2,5,6),(7,1,3),(3,1,4),(2,3,9),(2,5,8) [last two exercise the bitset path].
- `lp_check.py`: L_p from Sigma(E_p) (own code); pointwise check of N_{1,K}(tau) >= p^{min(J,L_p)} and G=J
  for every tau, K in {L_p+1, L_p+2}; checks D_p(1,L_p+1) >= 1-p^{-L_p}.
- `test_1117_codes.py`: builds the actual window code of the proof of Thm 11.17 around the simple zero
  alpha=x_c of Prop 11.13(b) (slope lambda=v(c!)), finds z(c) by p-adic Newton (400 digits), and on random
  code pairs checks: z(c) simple zero with slope lambda, z=alpha mod p^{P0}; formula (11.2) exactly
  (v(z-z') = L_k(z)-lambda+d, 0<=d<G_k); the cylinder criterion v(z-z')>=rho_k <=> agreement on windows 0..k;
  constancy of L_k on cylinders.

## Results
- L_p (own): 1 for p=3,5; 2 for 7,11,13; 3 for 17,19; 4 for 23. Matches §3.5.
- Cor 11.19(a): 0 pointwise failures for p=2,3,5,7,11,13,17,19,23; D_p(1,L_p+1) >= 1-p^{-L_p} in all cases
  (out/lp_check.out). The proof's expectation computation E min(J,L_p)=sum_{s<L_p}p^{-s} re-derived by hand; correct.
- Window-code tests: 11 configurations (p=2,3,5,7; w=1,2,3,5), 3380 pairs, 0 failures (out/test_1117_codes.out).
- Table values, exact histograms + 20-digit sums (out/D_highprec.out):
  (2,9,22) 0.85304534032; (2,7,22) 0.83339295535; (2,5,16) 0.80544611775; (2,3,16) 0.75430885054;
  (3,5,13) 0.92473566952; (3,4,12) 0.91115652244; (3,2,10) 0.85918645955; (3,1,8) 0.80687327857;
  (5,3,8) 0.96911310738; (5,2,8) 0.95484300467; (5,1,7) 0.92369474553; (7,2,6) 0.99213761701;
  (7,1,5) 0.98555682554; (11,1,5) 0.99826831601; (13,1,5) 0.99965674991; (17,1,4) 0.99996339867;
  (19,1,4) 0.99999061855; (23,1,4) 0.99999642654 (= 1-23^{-4} exactly, since K=L_23 there).
  All agree with the note's log to every printed digit; every rounded-down table entry is correct, margins >= 1.3e-5.
  Deficit at p=2: 1-0.853045 = 0.146955 < 0.147, consistent with Cor 11.20.
- Proof re-read (Thm 11.17, Lemma 11.18, Cor 11.19(a)): no gap found. Cosmetic: Lemma 11.18 Step A/(F2) uses
  "window k" for n in a_k+[0,P) while g_k sums n in a_k+[1,P]; harmless (use a_k+[0,P]).
  Cosmetic: §0 item 20 lists p=13 but omits p=11 (0.9982); (17,19,23) row uses K=L_p+1 for 17,19 but K=L_p for 23.
- Not checked here: L_p for p>=29 (archived logs), used only for the 37<=p<=97 remark.

## Commands and timings (12-core machine, <=4 processes, <100 MB each)
- `./mydim p w K` for 16 cheap cases: each <=2 s.
- `./mydim 2 7 22`: 19.6 s. `./mydim 2 9 22` in 3 chunks: 85 s each (parallel).
- `python3 lp_check.py`: ~1 min. `python3 test_1117_codes.py ...`: <=5 s per configuration.
