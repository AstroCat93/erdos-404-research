# Gap-hunt: Corollary 11.19 of note_v3 (section 11.2), round 3, 2026-10-21

Verdict: NOT refuted. No fatal or serious gap found. Two minor presentation issues.

## Chain checked line by line
Cor 11.19(a) <- Thm 11.17 (+ Lemma 11.18, mass distribution principle) <- Prop 11.13(a) <- Lemma 11.12(a),(b) <- Thm 11.11(a),(b); extension to closure of S_p via Thm 11.14(iv) and Prop 11.13(b); L_p from Thm 3.9(b),(c).

1. Cor (a) proof. w=1, P=p: among tau+1..tau+p (tau in pZ) only t=p is divisible by p, so G=min(K,v(tau+p))=J. Mod p^J, tau = -p, so q_s = prod_{t=1}^s (t-p) = (-1)^s (p-1)!/(p-1-s)!; for odd p (-1)^s=(-1)^u, u=p-1-s, giving (p-1)! E_p (Thm 3.9(b) set). Unit multiple preserves covering, so sums cover Z/p^{min(J,L_p)} and N >= p^{min(J,L_p)} (if J>=L_p, distinct mod p^J >= distinct mod p^{L_p}). With tau=py, J=min(K,1+v(y+1)) and K=L_p+1: E min(1+v(y+1),L_p) = sum_{s<L_p} P(v(y+1)>=s) = sum_{s<L_p} p^{-s} (valid since s<=K-1). Multiply by (p-1)/p: 1-p^{-L_p}. p=2: set {1,-1}, N>=2, L_2=1. Correct. Using a lower bound L<=L_p (p>=37) is also valid (argument works for any L with covering).
2. Thm 11.17 hypotheses used: alpha simple zero of a finite-support word, alpha != -2, p not dividing w (w=1). Approximation of any point of closure(S_p) by such alpha: 11.14(iv) (truncation e|_n = e^J, J={j>=n: e_j=1}, Prop 11.13(a) applies) and, near -2, 11.13(b) (x_c != -2 since v(x_c+2)=v(c!)<inf). OK.
3. Prop 11.13(a): v(c_0)>=2lambda+2>2lambda, v(Delta_J')>=2lambda+1>lambda, coefficients in Z_p by 11.11(a),(b); zero h* has v>lambda>=0 so lies in pZ_p where the expansion is valid. Lemma 11.12(a) contraction factor needs V-2lambda>=1: OK.
4. Distances (11.2): bracket v=d<G_k (distinct sums mod p^{G_k}; q^z_s = q_s(tau_k) mod p^K since z=alpha mod p^{P0}, P0>=K+1); tail >= L_{k+1}(z) = L_k+g_k >= L_k+G_k because v(z+a_k+t) >= min(v(tau_k+t),K). Lemma 11.12(b) applied with base z' (slope lambda, v(z-z')>=P0>lambda). OK.
5. Cylinder/ball identification and constancy of rho_k on a cylinder: for n<=a_k, v(z+n) <= L_k - floor(a_k/p)+1 <= L_k-2lambda-1 < rho_k. OK; disjointness by ultrametric nesting. OK.
6. (11.3), numerator equidistribution (tau_m/p = y+i0+mw mod p^{K-1}, p not dividing w), denominator bound sum v(z+n) <= T/(p-1)+max. OK.
7. Lemma 11.18 Steps A-C: Borel-Cantelli bounds correct (at most P cylinder balls contain the fixed points -n; F1 converts growth bound on L_k into ball-measure bound; exponents summable). OK.

## Minor issues (not refutations)
- M1 (off-by-one, harmless): g_k sums v(z+a_k+t) for t=1..P, i.e. positions a_k+1..a_{k+1}, but (F2)/Step A/B/C take "max over window k" = positions a_k..a_k+P-1. Replace "window k" by {a_k+1,...,a_{k+1}} in Lemma 11.18 (still P fixed integers per k); all bounds unchanged.
- M2: mass distribution principle cited as "standard, proved in track report"; fine, but the cited form should be the local (pointwise lower density, mu-a.e.) version, e.g. Falconer, Techniques in Fractal Geometry, Prop. 2.3(a).

## Independent recomputation [computer-assisted]
Own C code `dimcheck.c` (this dir): enumerates y mod p^{K-1}, G, q_s, counts distinct subset sums by Gray-code walk + bitmap, long-double log sum. Not derived from wdim.c. Results (run1.log, run_*.log; 1 core each):

| p | (w,K) | D (mine) | note table | secs |
|---|---|---|---|---|
| 2 | (1,2) | 0.646240625 | 0.6462 | 0 |
| 2 | (3,16) | 0.754308851 | 0.7543 | 0 |
| 2 | (5,16) | 0.805446118 | 0.8054 | 0 |
| 2 | (7,22) | 0.833392955 | 0.8333 | 44 |
| 2 | (9,22) | 0.853045340 | 0.8530 | 950 |
| 3 | (1,8) | 0.806873279 | 0.8068 | 0 |
| 3 | (2,10) | 0.859186460 | 0.8591 | 0 |
| 3 | (4,12) | 0.911156522 | 0.9111 | 1 |
| 3 | (5,13) | 0.924735670 | 0.9247 | 21 |
| 5 | (1,7) | 0.923694746 | 0.9236 | 0 |
| 5 | (2,8) | 0.954843005 | 0.9548 | 0 |
| 5 | (3,8) | 0.969113107 | 0.9691 | 3 |
| 7 | (1,5) | 0.985556826 | 0.9855 | 0 |
| 7 | (2,6) | 0.992137617 | 0.9921 | 0 |
| 11 | (1,5) | 0.998268316 | 0.9982 | 0 |
| 13 | (1,5) | 0.999656750 | 0.9996 | 0 |
| 17,19,23 | (1,4) | 0.9999634, 0.9999906, 0.9999964 | 0.99996, 0.99999, 0.99999 | 1,3,103 |

All rounding-down margins exceed 1e-5, far above double/long-double error over <= 2^21 summands.
