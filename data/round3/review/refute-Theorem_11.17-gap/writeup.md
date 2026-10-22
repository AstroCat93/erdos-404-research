# Gap-hunt of Theorem 11.17 (note_v3.md §11.2), 2026-10-21

Verdict: NOT refuted. No unjustified step found. Minor presentational points only.

## Line-by-line checks (all [proved] unless noted)
1. Setup: alpha != -2 in K_p, so not a negative integer (Thm 3.2(a): K_p ∩ Z_{<0} = {-2}); runs defined. i0 with l_{i0} >= p(2lambda+2), beyond supp(e), P_0 >= max(K+1, v(alpha+2)+1): exists since L_i -> infinity.
2. Windows: a_{k+1} = a_k + P, disjoint, contiguous. Flips are additions (e_j=0 beyond support).
3. z(c) via Prop 11.13(a) (J infinite allowed; J ⊆ [p(2lambda+2),∞) holds). v(z-alpha) >= L_{i0}-lambda = P_0 since v(pi_j) nondecreasing. z ≡ alpha mod p^{P_0} gives types, truncated valuations, v(z+2) preserved; z in K_p so not a negative integer.
4. (11.2): Lemma 11.12(b) applies with base z' (slope exactly lambda by 11.13(a)) and v(z-z') >= P_0 > lambda. Coefficients F^{[i]}(z) lie in Z_p trivially (the bound floor(j/p)-i in 11.11(a) may be negative but is not needed). Bracket: q^z_s ≡ q_s(tau_k) mod p^K, so distinct-sum family gives d < G_k <= K. Tail >= L_{k+1}(z) = L_k + g_k with g_k >= G_k because min(v(z+n),K) = min(v(tau_k+t),K) (with v(0):=K). Hence equality.
5. Cylinder characterisation: m<k: L_m+G_m <= L_{m+1} <= L_k; m>k: >= L_{k+1}-lambda >= rho_k. OK. rho_k constant on ball: v(z+n) <= L_k - floor(a_k/p) + 1 <= L_k - 2lambda - 1 < rho_k (G_k >= 1 since t=p term). Disjointness via ultrametric nesting. OK.
6. G_K(tau) >= 1 always, so rho_k strictly increasing; intervals (p^{-rho_{k+1}}, p^{-rho_k}] exhaust small r. (11.3) direction of inequality correct.
7. Numerator: alpha+a_m = p(y+i0+mw), p∤w gives exact equidistribution mod p^{K-1}; average = wp/(p-1) D. Denominator: sum v over (k+1)P consecutive integers <= (k+1)P/(p-1) + M. Ratio -> D given M_k = o(k).
8. Lemma 11.18: (F1),(F2) correct (two n with v>beta differ by multiple of p^{beta+1} > P). Step A: <= P cylinder balls contain some -n; Borel–Cantelli; L_k <= C2^k. Step B: ball B(-n,p^{-k^2}) measure bounded via (F1) at a point of E_k in Good; p^{-log_2 x} <= 1/x; summable. Step C: stretched-exponential bound summable. Countable unions fine.
9. Local mass distribution principle: standard (Falconer-type; works in any metric space via Egorov + covers). Cited, not proved in the note: minor.
10. Extension to closure of S_p: 11.14(iv) gives finite-support simple zeros densely; if the one found is -2, 11.13(b) supplies finite-support simple zeros x_c != -2 nearby. 11.14(ii) gives every class r ∉ Phi_p.

## Computation [computer-assisted sanity check, not part of proof]
check_11_2.py: for p=2 (lambda=1), 3,5,7 (lambda=0), w=1, K=3, 4 windows, 300 random code pairs each: v(z-z') = L_k(z) - lambda + d whenever d < G_k; 0 mismatches / 1200. Precision p^400, Newton lifting. Runtimes < 4 s each:
  python3 check_11_2.py {2,3,5,7}

## Minor points (not refutations)
- Statement leaves "for every w >= 1 with p∤w and every K >= 1" implicit; should be stated.
- Theorem 11.11(a) lower bound floor(j/p)-i is negative for small j; Lemma 11.12(b) only needs F^{[i]} in Z_p, which is trivial. Could be said.
- Mass distribution principle should be cited precisely (e.g. Falconer, Techniques in Fractal Geometry, Prop. 2.3) .
