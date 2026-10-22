# Gap-hunt: Theorem 11.14 (note_v3.md §11.2) — 2026-10-21

Verdict: NOT refuted. No step was found that fails. Two minor presentational points only.

## Line-by-line
- Definitions: word e (e_0=1), F_e=sum e_j pi_j; K_p = union of Z(F_e) by Prop 1.2 (König). Simple zero: F_e(x)=0≠F_e'(x), with F_e'=F_e^{[1]} by Thm 11.11(b).
- Thm 11.11(a),(b) re-derived: pi_j^{[i]} is the h^i coefficient; v ≥ floor(j/p)-i; the double family e_j pi_j^{[i]}(x)h^i, h in pZ_p, has v ≥ max(floor(j/p), i), so it is summable and can be rearranged. OK.
- Lemma 11.12(a) re-derived: D=p^{V-λ}Z_p; T(D)⊆D needs 2(V-λ)-λ ≥ V-λ, i.e. V ≥ 2λ (holds). Contraction factor p^{-(V-2λ)}, with V-2λ ≥ 1. Uniqueness: the bracket has valuation exactly λ, since each extra term has v ≥ (i-1)(λ+1) > λ. If c_0=0, then D={0} and h*=0. v(G'(h*))=λ. OK.
- Prop 11.13(a): J ⊆ [p(2λ+2),∞) gives v(c_0) ≥ 2λ+2 > 2λ and v(Δ_J') ≥ 2λ+1 > λ. A single flip needs pi_j(α)≠0, which holds for every α that is not a negative integer (this includes the nonnegative integers). e^J keeps e_0=1. The child converges to α as j→∞. OK.
- Prop 11.13(b): re-derived F=y^2+(y-1)y pi_c(y)=yH(y), H(0)=-c!, H'(0)=1+c!-sum c!/i ≡ 1 (mod p) for c ≥ 2p. Then v(y_c)=v(c!) and F'(x_c)=y_c H'(y_c)≠0. -2 is itself simple for x+2=F_{{0,1}}. OK.
- (i): K_p is closed (Thm 3.1(b)). S_p ⊆ K_p via Prop 1.2. S_p has no isolated points, so its closure is perfect. OK.
- (ii): ⇒ direction: Cor 3.3 is stated for natural a, but locality at level 1 (Thm 3.1(a), valid on Z_p) extends g_p≡0 to the whole class. This is implicit in the note (MINOR). ⇐ direction: Thm 3.5 gives a simple root of the polynomial S_T=F_e with a finite word. Checked that k*=p-r (or p if r=0) matches the range [1,p-r-1] in the definition of Φ_p. OK.
- (iii): S̄_p ∩ (clopen class) is perfect and nonempty. A nonempty perfect subset of Z_p has cardinality 2^{ℵ0}. Since p-2 ∉ Φ_p (and -2 ∈ S_p), the hypothesis is never vacuous. OK.
- (iv): truncation e|_n = e^J with J ⊆ [n,∞), n ≥ p(2λ+2). The distance bound is ≥ floor(n/p)-λ. If Δ_J(α)=0, α itself is a finite-word zero. OK.
- Theorems 11.11(c), 11.15 and 11.17 are not used by 11.14.

## Minor points
1. Proof of (ii) cites Cor 3.3 for "g_p≡0 on the class". The corollary is phrased for natural a, so one should add "and by locality at level 1 (Thm 3.1(a))".
2. "Perfect" includes the empty set. Nonemptiness comes from (ii) and (iii), which is fine.

## Numerics [computer-assisted sanity only, not proof]
check_11_14.py (exact integer arithmetic mod p^N):
- 11.13(b) for p=2,3,5 and c ∈ {2p, 2p+1, 3p}: v(x_c+2)=v(c!) and v(F')=v(c!) (as predicted, since F'(x_c)=y_c H'(y_c)).
- Single-flip children of a simple zero (p=3, base word {0,2,5}): v(α_j-α)=v(pi_j(α))-λ for j=12..17, and each child is simple with slope 0.
Output: check_11_14.out. Runtime < 1 s.
