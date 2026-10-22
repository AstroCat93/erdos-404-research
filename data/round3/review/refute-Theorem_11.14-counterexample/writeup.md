# Adversarial check of Theorem 11.14 (note_v3 §11.2) — counterexample hunter, 2026-10-21

Verdict: NOT refuted. No counterexample; proof re-read line by line.

## Proof audit (by hand)
- (i) S_p ⊆ K_p (zero of F_e with e_0=1 gives g=∞ by Prop 1.2); closure ⊆ K_p as K_p closed.
  Non-isolation: for α≠-2 simple, α∉Z_{<0} (K_p∩Z_{<0}={-2}), single flip j≥p(2λ+2): Lemma 11.12(a)
  hypotheses hold (V=v(π_j(α))≥⌊j/p⌋≥2λ+2>2λ; v(π_j'(α))≥⌊j/p⌋-1≥2λ+1>λ), distance v(π_j(α))-λ finite
  and →∞. At -2: Prop 11.13(b) identity F=y·H(y), H(0)=-c!, H'(0)=1+c!-Σc!/i ≡1 mod p (c≥2p) checked.
  Closure of a set without isolated points is perfect; nonempty since -2∈S_p.
- Lemma 11.12(a): contraction constant V-2λ≥1, uniqueness on v(h)>λ, derivative valuation — all correct.
  Coefficients F^{[i]}(x) lie in Z_p (integer polynomials), Taylor double series summable for v(h)≥1.
- (ii) Φ_p definition matches γ_p(p-r)=0 via level-1 locality; Thm 3.5 Hensel construction correct
  (k*=p-r, π_{k*}' ≡ Π_{l<k*}(r+l) ≢0).
- (iii) nonempty perfect subset of Z_p has cardinality 2^ℵ0; clopen slice of perfect set is perfect.
- (iv) truncation e|_n = e^J, J⊆[n,∞), n≥p(2λ+2)≥2p≥1 so e_0 preserved; Δ_J(x)=0 case gives α_J=x, harmless.
Minor (not an error): (iv) is stated for S_p as a whole; fine since S_p dense in its closure.

## Numerics [computer-assisted], script test1114.py (seeds 1,2,3; <1 s each; p∈{2,3,5,7,11,13}, precision p^25..p^40)
- Φ_p recomputed: matches note for p=3,5,7,11,13.
- Thm 3.5 construction yields a simple zero exactly in classes r∉Φ_p (all r, all p).
- Random finite words (≤5 terms in [1,4p)): every simple zero found lies in a class ∉Φ_p.
- Prop 11.13(a) single flips j∈[p(2λ+2), p(2λ+2)+6p): new zero is simple, same slope λ, distance exactly v(π_j(x))-λ.
- Prop 11.13(b) c∈[2p,2p+5]: x_c zero of 1+π1+π2+π_{c+2}, v(x_c+2)=v(c!)=slope.
Totals: 377/421/413 tests, 0 failures.
