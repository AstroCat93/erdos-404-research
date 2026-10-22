# Gap-hunt: Corollary 11.30 (note_v3 §11.3) — 2026-10-21

Verdict: NOT refuted. No unjustified step found. Labels: line-by-line check [proved-level reading by an AI referee, not human];
numerical checks [computer-assisted].

## Chain checked line by line
- Lemma 11.23(a)-(e): all verified (a: v(2^K u+i)=v(i); b: two even terms among x+2,x+4; c: count per level; d: truncation; e: V_n>M_n).
- Lemma 11.24(a)-(c): verified, incl. pi_j(x)=(y-1) y pi_{j-2}(y), the unit 1-y, and S'_e=(2y-1)Phi+y(y-1)Phi'.
- Prop 11.25: every Taylor-inequality case re-derived; valuations of h (2, >=3, 2, >=4) match the classes; the exclusions of i=0 and i>=2 are correct.
- Prop 11.26: strong Hensel + root separation argument correct; r stays in C and in the same V_n-cylinder; |R_e| bound; constants 1, 8, 256.
- Window identity: Gamma_L(n) implies (W1)-(W3) of Prop 10.6 and M_N<m (Lemma 10.5 setting); summing 10.6(iii) over 2^lambda states gives both identities (11.4); rho==1 for lambda<=1 checked.
- Lemma 11.27, Prop 11.28: measurability (Gamma_j decided mod 2^{V_{n_j}}, coarser than F_l), supermartingale, optional stopping at bounded time: correct.
- Thm 11.29: bad-window union bound (h_L monotone, i-l0<=n_l), barrier (V_N<2N<=2T<=G then Lemma 11.23(d)), walk term (N_K, delta<l0<=2^K, n_{l+1}<=T, Lemma 10.2(d)+11.23(a), integer c), binomial law of digits k..K-1 on C: correct. Gamma_0 subset Gamma_*(n_0) correct.
- Cor 11.30: Chernoff (1-H2(0.227)=0.227255>0.227), 2^K>G/8 for G>=4 l0, hypotheses for G>=2^10, trivial bound below 2^10 (0.125<=0.1265), class cover of R, Cor 3.7.1(iii) (g>=4 classes mod 16 = {0,2,6,8,10,14}), Thm 3.1(c).

## Independent computations (this directory)
- check_certs.py: S_e(-4) values {1,-5,7,1,-2,-8,4,-2}; max v(Phi(-4)) = 2 (e2=1) / 4 (e3=1); Phi(-8) never 0, histogram x4 of note's {1:32,3:16,4:8,5:3,6:4,7:1}; identity S=y(y-1)Phi on 200 random cases; g>=4 classes mod 16.
- check_slopes.py 7 200: 200 random 200-bit points per class, all alive paths with V_n>=V_cert: max slopes 1,3,3 (<= L=1,3,6).
- check_consts.py (exact integer n0,K; right endpoints of all constancy intervals, 2^10<=G<=2^190):
  sup side*G^a = 1.5844, 1.7005, 1.8755; sup(side+Chernoff main)*G^a = 22.469, 1318.07, 197161;
  sup min(mu(C),exact RHS)*G^a = 17.52, 1120.6, 1.657e5. Matches lead's 22.47/1318.1/1.97162e5 and 17.53/1121/1.680e5 (last differs slightly: 1.657e5 vs 1.680e5; both well below the claim; my grid stops at 2^190 and uses min with mu(C)=1/16 for C6 which the lead may treat differently). Timing: <3 s each.

## Cosmetic remarks (no effect on truth)
1. "n_0>=19 (so V_{n_0}>=13)": actually V_{n_0}>=16; fine.
2. Summary item 21 omits "G>=4"; harmless since the bound exceeds 1 for G<4.
3. Thm 11.29 first term written mu(E_good^c) (not intersected with C): valid upper bound.
4. Hit/A_l use W_{n_{l+1}}, F_l-measurable only on Gamma_l; A_l includes Gamma_l so OK, but worth one sentence.
