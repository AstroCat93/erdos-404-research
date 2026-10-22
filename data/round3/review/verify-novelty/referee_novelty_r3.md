# Round-3 novelty/credit referee report (AI referee; 2026-10-21)

Scope: §0 round-3 block and §11 of e404r3/note/note_v3.md, novelty/credit lens, plus internal consistency (§0 vs §11, §11 vs §4.7).
No mathematics here has been checked by a human. Labels: [checked] = re-derived or recomputed here; [searched] = literature/web check.

## 1. Fresh searches performed (2026-10-21, read-only)

| source | query | result |
|---|---|---|
| erdosproblems.com/404 (WebFetch) | status | open; last edited 29 Sep 2025; 7 comments; 0 proof claims; no new refs |
| Web (extended) | "Erdős problem 404 sums of distinct factorials divisible by prime powers" | only AstroCat93/erdos-404-research (this project), erdosproblems pages, Yudin 2610.01899, Abramov 2604.26429 (already listed) |
| Web (extended) | "sums of distinct factorials" p-adic Hausdorff dimension / uncountable / perfect set | nothing on K_p; real factorial-expansion fractals (arXiv:1706.01546), p-adic dims of integer sets (arXiv:2408.02967), Abram–Lagarias JFG 2014 — none overlap |
| Web (extended) | p-adic Bernoulli convolutions / random series in Z_p absolutely continuous | nothing p-adic; real Bernoulli-convolution L^2 literature only |
| Web | Evans "expected number of zeros of a random system of p-adic polynomials" | Evans, Electron. Commun. Probab. 11 (2006), arXiv:math/0602478 — adjacent (annealed root counts) |
| GitHub (gh search repos "erdos 404", "erdos-404") | recent activity | only AstroCat93 (2026-10-12), KitaKen1 x2 (2026-07-07/08), vibemathing template (2026-09-06) |
| GitHub KitaKen1/erdos-404-odd-prime-landscape issues | | #1 (this project's), open, 0 comments, last update 2026-10-12 |
| GitHub KitaKen1 repos by push date | | active on other problems to 2026-10-21; nothing on #404 since July |
| GitHub KitaKen1/erdos-404-p2-landscape tree + code search "2210" | | a=2210 appears only inside witness index lists; Kitamura's record table (README appendix) has 34, 8190, 1102, 3456, 14, 2 and f(594,2)>=66126; f(2210,2) is NOT in Kitamura's repo |
| gh code search "sums of distinct factorials" | | przchojecki/agentic-erdos notes/ep404.md (last commit 2026-05-09): problem restatement, Tao/Kovač comments, finite searches; no structural overlap |
| formal-conjectures PR #6936 | | still open, last update 2026-10-11; no ErdosProblems/404.lean on main |
| arXiv API (abs:"distinct factorials"; abs:factorials AND abs:adic) | newest first | nothing new on #404 after Yudin 2610.01899; adjacent: "Explicit results for Euler's factorial series ... under GRH" (2022) |
| MathOverflow (StackExchange API) | "distinct factorials", "sum of factorials adic" | MO 509609 (2026-03-28) on p-adic roots of the Mahler expansion of S_n = sum (-1)^{floor(k/p)} (pk)!/(p^k k!) — different object; MO 476702 already cited |
| Agresti 1975 | bibliographic | confirmed: J. Appl. Probab. 12(1) (1975) 39–46 |
| Kersting 2020 | bibliographic | confirmed: J. Appl. Probab. 57(1) (2020) 196–220, doi:10.1017/jpr.2019.84; arXiv:1703.01960 (earlier title "A general approach to branching processes in varying environment"); abstract covers a.s. extinction criteria and **square integrability of the normalised martingale** |
| arXiv:2509.20181 | abstract | R. Balka, K. Héra, G. Kiss, "Signed null sequences and Hausdorff dimension" (24 Sep 2025): dimension of the set of SIGN SEQUENCES for which a ±a_n series converges / has sum L. The note's description "on real achievement sets" is inaccurate. |
| arXiv:1210.2478 | abstract | Abram–Lagarias, "p-adic path set fractals and arithmetic", J. Fractal Geom. 1 (2014) 45–81 (journal ref missing in note) |
| Cobeli–Vâjâitu–Zaharescu | bibliographic | J. Ramanujan Math. Soc. 15(2) (2000) 135–154 per most indexes (one CV says 71–90) |

Gaps: Google Scholar and zbMATH not queried directly (only via general web search); Kitamura's forum posts not paged.

Conclusion of the searches: no prior or concurrent public work found that overlaps any §11 result (perfect kernel / uncountability / Hausdorff dimension of K_p, explicit rate at p=2, quenched martingale at odd p, L^2 carry cocycle, f(1,19) bound, f(2210,2)).

## 2. Recomputations [checked]

- Gamma_p(1) for p=2,3,5,7,11 (exact rationals, own DP): 0, 1/32, 9/256, 117/8192, 753/2^19 — match the Lemma 11.37 table. Distinct subset sums mod p^j give max{j: dist=p^j} = 1,1,1,2,2 and 3·2^{p-2} saturation (6, 24, 96) — match.
- theta_2 = log2(3)/4 by hand (f_2(0)=0, f_2(j)=j-2+log2 3).
- D_2(1,2) = (1/4)(1+log2 3) = 0.6462 by hand.
- v_19((19^9-1)!) = 17,927,094,312; v_19((19^8-1)!) = 943,531,272.
- 1 - H_2(0.227) = 0.22726 > 0.227; 0.61·2^{-2.27} = 0.1265 >= 1/8.
- Exact fractions: delta_11(5) = 0.52160227..., delta_9(7) = 0.62391872..., delta_28(2)=0.11640248, delta_17(3)=0.36329325.
- Proposition 11.13(b): F_e = y·(y + (y-1)π_c(y)), H(0) = -c!, H'(0) = 1 + c! - Σ c!/i ≡ 1 (mod p) re-derived.

## 3. Findings

### 3.1 [serious] §0 item 22, Conjecture 11.10 and §11.7 claim more than Theorem 11.7 proves
Theorem 11.7 (correctly) concludes mu(K_p ∩ A) > 0 only for an atom A with M_j(A) > 0 AND mu_A(sigma_j < inf) < 1/Lambda(A), Lambda(A) = 1 + p^L K S_j / M_j(A). Hypothesis H(p) of Corollary 11.5 also includes such an atom. But Conjecture 11.10 defines H'(p) only as "kappa·r^max bounded on unfrozen atoms" and says "By Theorem 11.7 this would give mu(K_p)>0"; §0 item 22 says "If [H'(p)] ..., then mu(K_p)>0"; §11.7 says "mu(K_p)>0 is reduced to H'(p)". The existence of a suitable atom does not follow from the bounded-ratio condition: since 2^{-n}p^{m} ~ (p^{1/(p-1)}/2)^n up to poly(n), S_j/M_j(A) ~ poly(n_j)/(weighted population of A), so one needs an atom at some level j with weighted population >> n_j^4 (constants p^{L+1}K) and freezing probability < 2/3, which is a population-growth statement on non-frozen atoms. If no such atom exists at any level the inequality mu_A(sigma_j<inf) >= 1/Lambda_A is consistent on every atom and the theorem gives nothing. The remark after Theorem 11.7 ("Lambda tends to 1 on atoms with M_j(A) bounded below") assumes such atoms carry non-negligible mass. Fix: add the atom condition to H'(p) (as in H(p)), or prove it; it is a single finite, checkable condition for one atom (exact freezing probability is essentially determined by x mod p^{m_j} for the early windows), so it may be certifiable computationally — but the shallow data (|P^L| <= 89,168 at n <= 86, p=3, vs 86^4 ≈ 5.5e7) do not yet reach it.

### 3.2 [minor] Corollary 11.39(b) and §0 item 23: "dim_H E_N0 >= 0.99966 at p=13" rounds a lower bound UP
1 - theta^set_13 = 0.99965675 (Computation 11.59; table "≥ 0.999656"). 0.99966 > 0.9996568, so the stated bound is not proved. Use 0.99965 (or 0.999656).

### 3.3 [minor] §4.7 / §0 item 10 odd-prime density bounds are rounded up; exposed by Computation 11.55
Exact archived values (T4 t4b_final.out): delta_10(5) = 0.5216163 → 1-delta = 0.47838 < stated 0.4784; delta_8(7) = 0.6239378 → 0.37606 < stated 0.3761; delta_5(13) = 0.75454 → 0.24546 < stated 0.2455. Computation 11.55 calls 1-delta_11(5) = 0.4783977 and 1-delta_9(7) = 0.3760813 "small improvements of §4.7", but both are numerically BELOW the §4.7 figures as printed. Fix §4.7/§0 to 0.4783, 0.3760, 0.2454 (round down), and state the improvements as 0.4783837 → 0.4783977 and 0.3760622 → 0.3760813. Also delta_11(5) = 0.52160227 should be printed 0.5216023 (or as an upper bound 0.5216023) rather than truncated 0.5216022.

### 3.4 [minor] §0 item 20: "dim_H K_p >= D_p(w,K) >= 1 - p^{-L_p}"
The second inequality holds for (w,K) = (1, L_p+1) (Corollary 11.19(a)), not for arbitrary (w,K) (e.g. K=1). Say "≥ max_{w,K} D_p(w,K) ≥ D_p(1,L_p+1) ≥ 1-p^{-L_p}". §0 item 20 also omits p=11 (0.9982) — harmless.

### 3.5 [minor] Credit / citation corrections
- arXiv:2509.20181 is Balka–Héra–Kiss, "Signed null sequences and Hausdorff dimension" (2025): it concerns the dimension of sets of sign sequences (in sequence space) giving convergence / a prescribed sum, not "real achievement sets". Correct the description in §11.9 and References; it is arguably closer to the word-space side of §11.2 than to K_p.
- Abram–Lagarias: add journal reference J. Fractal Geom. 1 (2014) 45–81.
- Agresti (1975) J. Appl. Probab. 12(1) 39–46 and Kersting (2020) J. Appl. Probab. 57(1) 196–220, doi:10.1017/jpr.2019.84, are now bibliographically verified; drop "not verified" for the records (contents still from abstract only).
- Kersting (2020) treats square integrability of the normalised martingale for branching processes in varying environment; this is the closest classical analogue of the L^2 criterion of Theorems 11.4/11.7 (quenched = varying environment). §11.9 lists Kersting only for Heuristic 11.33; add it to the template credit of §11.1.
- Theorem 11.48(a)/(b) (Chebyshev covering from the L^2 mass; L^1 < sqrt(L^2) by Cauchy–Schwarz) are standard Fourier facts; label "standard" in the credit list.
- Theorem 11.45(a): the congruence (-1)^i binom(p^D-1,i) ≡ 1 (mod p^{D-floor(log_p i)}) is classical (binomial coefficients modulo prime powers; e.g. Granville's survey). Credit as classical.
- Proposition 11.21 restates the compactness reformulation (Proposition 1.2, credited in §2 to neelsomani / erichou1 / AItoBit); say so.
- Proposition 11.53 is the -2 shadow (Kitamura's cube identity/shadow family; Theorem 3.2); a one-line credit would be appropriate.
- Theorem 11.38 / Corollary 11.39(b): the method is the p-adic analogue of the classical L^2 (correlation-dimension / energy) method for Bernoulli convolutions (Garsia; Peres–Schlag–Solomyak). No p-adic precedent found; a pointer to the real analogue would help readers.
- Optional adjacent: Evans (2006, ECP 11, arXiv:math/0602478) on expected numbers of p-adic polynomial zeros (cf. the annealed first moment and Proposition 11.26); p-adic Euler factorial series literature (values of sum n! t^n) as adjacent to §11.4.

### 3.6 [minor] "Annealed route closed" (§0 item 26, §11.0 headline 6)
Proposition 11.53 proves only that the untruncated second moment ratio diverges. The statement about truncated moments (Paley–Zygmund "at best (log G)^2/G") is a heuristic reading in Computation 11.55. The headline "the annealed route is closed" should be qualified as "the untruncated annealed second moment".

### 3.7 [minor] Dating/labelling inconsistencies
- §0 heading "Round 3 additions (2026-10-12; §11; AI-refereed, not human-refereed)" while the body and §11.9 say the AI referee reports are pending; "AI-refereed" is premature (update after this round's reports) and the date 2026-10-12 conflicts with tracks running 2026-10-20/21.
- "## 11. Round 3, 2026-10-12": same.
- Front matter "Date: ... Revision 2: 2026-10-12." lacks a Revision 3 date.
- Corollary 11.20's comparison "beats p^{-ceil(G/3)}" holds for all p with D > 2/3; fine as stated (D ≥ 0.853 at p=2).

### 3.8 Credit checks that PASS
- f(2210,2) = 8467 is new relative to Kitamura's repositories (searched tree, README record table, witness gallery, code search); 2206 + 6261 = 8467 with v_2(2210!) = 2210 - s_2(2210) = 2206 [checked].
- Kitamura's "~11.5/G": Kitamura's README/determining_exact_values.md/witness_gallery.md give no definition; the context is the classification of even classes, so the "fraction among even a" reading (= 2 delta_G) is plausible and correctly labelled [heuristic reading].
- f(1,19) >= 17,927,094,312: no competing public bound (Kitamura covers p <= 13; erdosproblems lists none).
- Uncountability/perfect kernel/Hausdorff dimension of K_p, the explicit rate at p=2 off 14 mod 16, the L^2 carry cocycle and theta_p bounds: no prior or concurrent public work found.
- Classical tools (Hensel, Strassmann, Cauchy–Davenport, mass distribution, Chernoff, Paley–Zygmund, Kesten–Stigum/LPP/Tanny templates) are credited in §11.9.

## 4. Commands log (2026-10-21; single core; all < 1 min)
- sed/grep reads of note_v3.md (§0, §2, §4.7, §11), Kitamura local copies under e404r3/T4-computations/kitamura/ (read as data).
- gh api repos/KitaKen1/erdos-404-p2-landscape/git/trees/HEAD?recursive=1; gh api search/code 2210; gh search repos "erdos 404"; gh api .../issues; gh api users/KitaKen1/repos; gh api repos/przchojecki/agentic-erdos/contents/notes/ep404.md; gh api repos/google-deepmind/formal-conjectures/pulls/6936.
- curl arXiv API (two queries), StackExchange API (three queries).
- WebSearch x6, WebFetch x3 (erdosproblems.com/404, arXiv abs 2509.20181, 1210.2478).
- python3 gam.py (Gamma_p, distinct sums), python3 one-liners (Legendre, Chernoff, fractions). Scripts in scratchpad r3-verify-novelty/.
