# Re-check of note_v3.md after the round-3 revision (2026-10-21, AI instance; not human)

Scope: confirm that S1, S2 and M1-M12 plus the presentational points were addressed; check that §0 (round-3 block), §11.7 status and §11.9 are consistent; look for new errors. About 30 min, single core.

## Commands
- `python3 check_1145.py` (this dir; <1 s): lists i<H=p^(t-1) with y_i == i! mod p^(t+c) for 8 unit K'.
  Output: (3,3): i=6,8 for all units; (5,3): 20,24; (7,3): 42,48; (3,4): 20,25 for some units only; (3,5): 76 for some units only. Matches the note's list and the lead's log `data_r3/lead/lead_r3fix_checks.log`.
- mpmath: theta_3 closed form (4/9)[log_3(33/32)+7/4-2log_3 2] = 0.229400028286... = direct 400-term sum of the definition; log2(3)/4 = 0.3962406252.
- Exact fractions: delta_11(5)=25468861/5^11=0.5216022733 (1-d=0.4783977267); delta_9(7)=25177371/7^9=0.6239187243 (1-d=0.3760812757); delta_17(3)=0.3632932537; p=2 1-delta_29=0.8865867, 1-delta_32=0.8983639.
- Census data (e404/E-behaviour/data/density_tables.txt): delta_6(11)=0.6997574 (1-d=0.3002426), delta_5(13)=0.7545443 (1-d=0.2454557). All §0 item 10 / §4.7 lower bounds now round down correctly (0.6367, 0.4783, 0.3760, 0.3002, 0.2454).
- `stat` on PREDICTIONS_registered_T1b.txt: birth 2026-10-21 17:18:27 CDT = 22:18:27Z, modified 17:37:02 CDT = 22:37:02Z. The lead's verdict (label correct) holds.

## Checklist (all addressed)
S1: Conj 11.10 now has part (b); Remark after Thm 11.7; §0 item 22, §11.0 headline 3, sentence after Thm 11.4, §11.7 Q1 and item 3 all corrected. The Remark's sum-over-atoms bound is a valid inequality (terms where (E2) fails are <= 0).
S2: Consequence withdrawn; counterexamples reproduced independently; Thm 11.45(a)-(d) kept as lower bounds; credit for (a) added.
M1 theta_3 <= 0.229401 (valid); log2(3)/4 <= 0.396241 (valid). M2 0.999656 (valid; true 0.99965675). M3 values valid. M4 qualified in §0 item 26, headline 6, §11.6. M5 Thm 11.48(b) correct, with a correct proof (1-p^{-m} factor). M6 §0 item 20 chain correct. M7 Comp 11.43 explained. M8 Comp 11.55 explained. M9 Comp 11.57 descriptive. M10 Conj 11.44 reworded (1.2989 vs 1.3105; excess 3.7% low, consistent with the table C_17-1=0.310525). M11 references fixed. M12 dates fixed. Presentational points: all present (Thm 11.14(ii) cites 3.1(a); Thm 11.17 "every w with p∤w, every K>=1"; Lemma 11.18 window; Cor 11.20 sup; Cor 11.19 p=23 note; Cor 11.39(b) scaled copy; A_p independence).
§11.9 counts (2/5, 0/6, 1/7, 4 refuted) match the three reports; 2 serious + 12 minor distinct is consistent.

## Remaining problems (all minor)
R1. §11.7 "What remains" item 3, last sentence: the alternative "a lower bound on mu{M_j >= c n_j^4 S_j} that is not exponentially small" is mis-stated. (i) Lambda is bounded once M_j(A) >= c S_j; the n_j^4 factor belongs to the *population* form (population >> n_j^4 is the same as M_j >> S_j, by the Remark after Thm 11.7). With n_j^4 S_j the condition is sufficient but needlessly strong and inconsistent with the Remark. (ii) "Not exponentially small" is not enough. Summing Thm 11.4 gives mu(K_p) >= mu{M_j >= cS_j}/(1+p^L K/c) - mu(sigma_j<inf), and mu(sigma_j<inf) is only polynomially small (about n_j^{-2} from the Borel-Cantelli bound). So the measure must beat (1+p^L K/c) mu(sigma_j<inf). Fix: "a lower bound on mu{M_j(A) >= c S_j} exceeding (1+p^L K/c) mu(sigma_j<inf)".
R2. §11.1, paragraph "The route mu{x:-1 in A'_x}>0" (just before Conj 11.10) still says the annealed second moment "diverges at every prime (Proposition 11.53); this is why the criterion above is quenched". Divergence of E Z^2 alone does not defeat the method; the M4 qualification (needs E Z_G = o(p^{G/2}), numerics only; truncated moments not excluded) was applied in §0, §11.0 and §11.6 but not here. Fix: add "[heuristic: together with the linear growth of E Z_G seen numerically, Computation 11.55]".
R3. Dates: the front matter says "Revision 3: 2026-10-21 ... referee corrections applied 2026-10-21", while §11.0 says "The lead compiled this section on 2026-10-21/22" and §11.8 "Lead re-runs (2026-10-21/22)". The lead's files are all stamped 2026-10-21 18:56-21:17 CDT. "/22" is true only in UTC, and the note otherwise gives CDT times. Use one convention, e.g. "2026-10-21 (CDT)".
R4 (optional nit, pre-existing proof wording). In the Theorem 11.38 constants sentence the bound (log_p(k+e_0)+2)^2 is applied, but the proof's X satisfies X <= (p-1)/p (k+e_0+log_p k+O(1)). So log_p X can exceed log_p(k+e_0) by O(log k / k). The conclusion (A_p independent of N_0) is unaffected; write log_p X <= log_p k + log_p(1+e_0) + O(1).
R5 (optional). Theorem 11.17's proof still defines "Window k" as a_k+[0,P), while Lemma 11.18 redefines it as a_k+1..a_k+P. The Lemma states this explicitly, so nothing is wrong, but readers meet two meanings of one term. Rename the Lemma's set (e.g. "the g-window of k").
R6 (optional, pre-existing). Computation 11.55 says that "survivor counts reproduce every delta_G(p) of §4.7", but §4.7's p=2 row includes G=29 and 32, beyond the annealed G<=28. Say "every delta_G(p) of §4.7 with G<=28, 17, 11, 9".

No new mathematical error found. No [proved] statement is affected. Q3 is still correctly stated as open everywhere.
