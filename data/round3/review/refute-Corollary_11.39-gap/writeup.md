# Gap-hunt: Corollary 11.39 (note_v3 §11.4) — 2026-10-21

## Verdict
Mathematics of (a), (b), (c) checks out step by step [proved, modulo Thm 11.36/11.38/Lemma 11.37 which were re-derived here].
One concrete defect: the numerical instance in (b) (and §0 item 23) "dim_H E_N0 >= 0.99966 at p=13" is NOT what the proof gives.
The proved bound is 1 - theta^set_13 = 0.99965675... < 0.99966 (a lower bound was rounded UP). The §11.4 table's
">= 0.999656" is correct. Fix: write ">= 0.999656" (or 0.99965) in Cor 11.39(b) and §0 item 23.

## Reproduction
- `theta_check.py` (exact rational enumeration of W over 3^p sign vectors for p<=13, subset-sum dist_p(j), mpmath series with
  verified affine tails): theta_p and 1-theta^set_p match the table for p=2..13; 1-theta^set_13 = 0.9996567512. Log: theta_check.log (~6 s, 1 core).
- `blockdist_check.py`: dist from actual factorial blocks n=13m..13m+12 (m=1,2,12,25,168,337,2196) equals dist_13(J_m) =13,169,2163,5178;
  float recomputation 1-theta^set_13 = 0.99965675117756 (< 0.99966). Log: blockdist_check.log.

## Step-by-step check (all passed)
- (a) = C_k p^{-k} with Thm 11.38; C_eps absorbs A log^2 k + B.
- Thm 11.38: block factor <= 1+Gamma_p(J_m) via 11.36(ii),(iv) + 11.37(a),(c) (monotone in j for last partial block); counting
  #{i<=X: v_p(i)=j} <= X(1-1/p)p^{-j}+1; X=M+1 <= (p-1)/p (k+e0) + O(log k) from e_M=(pM-s_p(M))/(p-1). p∤N0 partial block at level 0
  with factor <= p^{1+v_p(m0)}: constant. p=2 block structure (P_m(1)=2(m+1)-1 ≡ -1 mod 2^{J_m}) checked; theta_2 = log2(3)/4 re-derived.
- (b) Markov + Borel–Cantelli on ∫nu(B_k(x))dnu = C_k p^{-k}; ultrametric mass distribution principle on nu restricted to
  {nu(B_k(x)) <= p^{-sk}, k>=k0}: valid. "E_N0 charged by nu" is loose (supp nu = p^{-e0}E_N0); harmless since scaling by p^{e0} is a similarity.
- theta^set: per-block uniform law on one subset per residue mod p^{J_m}; still supported in p^{-e0}E_N0; generalised 11.36 with
  |mu_hat|^2 >= 0 keeps positivity; block factor p^J P(S≡S') = p^J/dist(J); dist constant 3*2^{p-2} for J>=J0 (from 11.37(c): events equal).
- (c) T_p(k) of §10.4 equals sum_{ord xi=p^k}|nu_hat(xi)| for N0=p; Lemma 11.35(c) Cauchy–Schwarz gives T <= (p^k C_k)^{1/2}.
