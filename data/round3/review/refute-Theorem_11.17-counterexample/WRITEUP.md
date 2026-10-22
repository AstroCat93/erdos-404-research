# Counterexample hunt: Theorem 11.17 (note_v3 §11.2), 2026-10-21

Track: refute-Theorem_11.17-counterexample (round 3). Work dir empty at start (no prior instance files).
All code written from scratch here; 1 core; every run < 5 s, < 100 MB.

## Verdict
No counterexample, no numerical discrepancy. Not refuted. [computer-assisted checks + line-by-line re-reading]

## 1. D_p(w,K) recomputed from the definition (dcheck.py, dcheck2.py; logs dcheck.log, dcheck2.log)
Bitset DP over distinct subset sums mod p^{G_K(tau)}, averaged over tau = p*y, y mod p^{K-1}; independent of wdim.c.
| (p,w,K) | ours | note |
|---|---|---|
| (2,1,2) | 0.6462406252 | 0.6462 |
| (2,3,16) | 0.7543088505 | 0.7543 |
| (2,5,16) | 0.8054461177 | 0.8054 |
| (3,1,8) | 0.8068732786 | 0.8068 (11.59: 0.8068732786) |
| (3,2,10) | 0.8591864596 | 0.8591 |
| (3,4,12) | 0.9111565224 | 0.9111 |
| (5,1,7) | 0.9236947455 | 0.9236 (11.59: 0.9236947455) |
| (5,2,8) | 0.9548430047 | 0.9548 |
| (5,3,8) | 0.9691131074 | 0.9691 (headline) |
| (7,1,5) | 0.9855568255 | 0.9855 (11.59: 0.9855568255) |
| (7,2,6) | 0.9921376170 | 0.9921 (headline) |
Not recomputed: (2,7,22), (2,9,22) [0.8530 headline], (3,5,13) [0.9247 headline] (larger; already double-run by track and lead).
Observed: D_p(1,K) constant in K once K >= L_p+1-ish, as Cor 11.19(a) predicts; all D < 1.

## 2. Stress test of the proof's mechanism (zcheck.py, zcheck2.py; logs zcheck.log, zcheck2.log)
Exact p-adic integers mod p^N (N = 90..260). For p in {2,3,5,7}, random finite words B subset [1,10],
simple zeros alpha found by Hensel from random residues (slopes lambda in {0,1,3} occurred), alpha far from -2.
Construction exactly as in the proof: runs l_i, i_0 with l_{i_0} >= p(2lambda+2), beyond supp e, P_0 >= max(K+1, v(alpha+2)+1);
windows a_k + [0,wp); random (not only distinct-sum) subsets S_k in 2-3 windows; z(c) by Newton on e + 1_J.
Checked, for every code and every pair (about 19,000 pairs in total, 0 skipped for precision):
- Prop 11.13(a): Newton converges, child slope = lambda, v(z - alpha) = v(Delta_J(alpha)) - lambda. 0 failures.
- (11.2): v(z(c)-z(c')) = L_k(z) - lambda + d whenever d = v(bracket) < g_k(z). 0 failures.
- cylinder <=> ball: c,c' agree on windows 0..kk iff v(z-z') >= rho_kk(z) (tested whenever d < G_k). 0 failures.
- rho_kk constant on cylinders. 0 failures.
Parameters: (p,w,K) in {(2,1,2),(2,3,4),(2,1,6),(2,5,6),(3,1,3),(3,2,3),(3,1,5),(3,4,4),(5,1,2),(5,2,4),(7,1,2)}.

## 3. Proof re-read (no gap found)
- Tail valuation >= L_{k+1} = L_k + g_k >= L_k + G_k > L_k + d: correct since windows tile (a_{k+1} = a_k + wp) and
  v(z+a_k+t) >= min(v(tau_k+t),K) because z = alpha mod p^{P_0}, P_0 >= K+1.
- Lemma 11.12(b) applies: both zeros simple with slope lambda (11.13(a), J subset [p(2lambda+2), oo)), v(z-z') >= P_0 > lambda.
- (11.3) and the density bound sum_{T consecutive} v(z+n) <= T/(p-1) + max v: correct; type equidistribution needs p !| w (assumed).
- Lemma 11.18: Steps A-C re-derived; Borel-Cantelli sums are k^{-2} and p^{-c k^{1/3}}; F2 uses p^{beta+1} > P. OK.
- Only external input: the local mass distribution principle (standard; Falconer, Techniques, Prop. 2.3) and
  K_p cap Z_{<0} = {-2} (Theorem 3.2(a), not re-checked here).
Minor presentational point: the statement should say "for every w with p !| w and every K >= 1" explicitly (it is implicit).

## Commands
python3 dcheck.py (0.1 s); python3 dcheck2.py <dir> (4 s); python3 zcheck.py (1 s); python3 zcheck2.py <dir> (1 s).
