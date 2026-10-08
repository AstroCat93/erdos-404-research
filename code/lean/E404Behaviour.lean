/-
Erdős Problem #404 — behaviour of f(a,p).  Machine-checked lemmas (Lean 4 + Mathlib).

Notation.  rp x k = (x+1)(x+2)...(x+k)  (rising product, rp x 0 = 1),
           P T x  = ∑_{k ∈ T} rp x k     (T a finite set of offsets, 0 ∈ T).
For a ≥ 0 and T ∋ 0 :  ∑_{k∈T} (a+k)! = a! · P T a   (normal_form), so
  f(a,p) = v_p(a!) + g(a,p),   g(a,p) = sup_{T ∋ 0} v_p(P T a).

Main results proved here:
  * normal_form   : ∑_{k∈T} (a+k)! = a! * P T a.
  * locality      : x ≡ y [ZMOD m] → P T x ≡ P T y [ZMOD m]
                    (so "g(a,p) ≥ G" depends only on a mod p^G).
  * cube          : P {0,1,3} x = (x+2)^3   (Kitamura's identity).
  * taylor_P      : h^2 ∣ P T (x+h) - P T x - h * DP T x.
  * sibling       : (p = 2) for every even x ∈ ℤ and G ≥ 1,
                    Good x (G+1) ↔ Good (x + 2^G) (G+1),
                    where Good x K :≡ ∃ T, 0 ∈ T ∧ 2^K ∣ P T x   ("g(x,2) ≥ K").
  * constancy     : if x is even, G ≥ 1, g(x,2) = G exactly (Good x G ∧ ¬Good x (G+1)),
                    and y ≡ x [ZMOD 2^G], then g(y,2) = G exactly.
  * good_iff_fact : for a : ℕ, Good a K ↔ ∃ T ∋ 0, 2^(v_2(a!) + K) ∣ ∑_{k∈T} (a+k)!,
                    i.e. Good a K ↔ f(a,2) ≥ v_2(a!) + K  (with v_2 = Nat.factorization · 2).
  * constancy_f   : the same constancy statement phrased with factorial sums.
-/
import Mathlib

open Finset

namespace E404

/-- rising product (x+1)(x+2)⋯(x+k) -/
def rp (x : ℤ) : ℕ → ℤ
  | 0 => 1
  | k + 1 => rp x k * (x + (k + 1))

/-- P_T(x) = ∑_{k ∈ T} (x+1)⋯(x+k) -/
def P (T : Finset ℕ) (x : ℤ) : ℤ := ∑ k ∈ T, rp x k

/-- "derivative" of the rising product, defined by the product rule -/
def D (x : ℤ) : ℕ → ℤ
  | 0 => 0
  | k + 1 => D x k * (x + (k + 1)) + rp x k

def DP (T : Finset ℕ) (x : ℤ) : ℤ := ∑ k ∈ T, D x k

/-! ### normal form -/

lemma rp_nat (a k : ℕ) : ((a + k).factorial : ℤ) = (a.factorial : ℤ) * rp a k := by
  induction k with
  | zero => simp [rp]
  | succ k ih =>
    rw [← add_assoc, Nat.factorial_succ]
    push_cast
    rw [ih]
    simp only [rp]
    ring

theorem normal_form (a : ℕ) (T : Finset ℕ) :
    (∑ k ∈ T, ((a + k).factorial : ℤ)) = (a.factorial : ℤ) * P T a := by
  simp only [P, Finset.mul_sum, rp_nat]

/-! ### locality -/

lemma rp_modEq {x y m : ℤ} (h : x ≡ y [ZMOD m]) (k : ℕ) : rp x k ≡ rp y k [ZMOD m] := by
  induction k with
  | zero => rfl
  | succ k ih =>
    simp only [rp]
    exact ih.mul (h.add_right _)

theorem locality (T : Finset ℕ) {x y m : ℤ} (h : x ≡ y [ZMOD m]) : P T x ≡ P T y [ZMOD m] := by
  unfold P
  exact Int.ModEq.sum fun k _ => rp_modEq h k

/-! ### the cube identity -/

lemma rp1 (x : ℤ) : rp x 1 = x + 1 := by simp [rp]
lemma rp2 (x : ℤ) : rp x 2 = (x + 1) * (x + 2) := by simp [rp]; try ring
lemma rp3 (x : ℤ) : rp x 3 = (x + 1) * (x + 2) * (x + 3) := by simp [rp]; try ring

theorem cube (x : ℤ) : P {0, 1, 3} x = (x + 2) ^ 3 := by
  simp [P, rp]
  ring

/-! ### Taylor expansion to first order -/

lemma taylor_rp (x h : ℤ) (k : ℕ) : h ^ 2 ∣ rp (x + h) k - rp x k - h * D x k := by
  induction k with
  | zero => simp [rp, D]
  | succ k ih =>
    obtain ⟨q, hq⟩ := ih
    refine ⟨D x k + q * (x + h + (k + 1)), ?_⟩
    simp only [rp, D]
    linear_combination (x + h + ((k : ℤ) + 1)) * hq

theorem taylor_P (T : Finset ℕ) (x h : ℤ) : h ^ 2 ∣ P T (x + h) - P T x - h * DP T x := by
  have : P T (x + h) - P T x - h * DP T x = ∑ k ∈ T, (rp (x + h) k - rp x k - h * D x k) := by
    simp only [P, DP, Finset.sum_sub_distrib, Finset.mul_sum]
  rw [this]
  exact Finset.dvd_sum fun k _ => taylor_rp x h k

/-! ### parity of D at even points -/

lemma rp_even_of_two_le {x : ℤ} (hx : Even x) : ∀ k, 2 ≤ k → Even (rp x k) := by
  intro k hk
  induction k with
  | zero => omega
  | succ k ih =>
    simp only [rp]
    rcases Nat.lt_or_ge k 2 with h | h
    · have hk1 : k = 1 := by omega
      subst hk1
      apply Even.mul_left
      have : x + ((1 : ℕ) + 1 : ℤ) = x + 2 := by push_cast; ring
      rw [this]
      exact hx.add even_two
    · exact (ih h).mul_right _

lemma D_parity {x : ℤ} (hx : Even x) :
    ∀ k, (k ∈ ({1, 2, 3} : Finset ℕ) → Odd (D x k)) ∧
      (k ∉ ({1, 2, 3} : Finset ℕ) → Even (D x k)) := by
  obtain ⟨r, rfl⟩ := hx
  intro k
  induction k with
  | zero => simp [D]
  | succ k ih =>
    rcases Nat.lt_or_ge k 3 with hk | hk
    · interval_cases k
      · refine ⟨fun _ => ?_, fun h => by simp at h⟩
        simp [D, rp]
      · refine ⟨fun _ => ?_, fun h => by simp at h⟩
        simp only [D, rp]; push_cast
        exact ⟨2 * r + 1, by ring⟩
      · refine ⟨fun _ => ?_, fun h => by simp at h⟩
        simp only [D, rp]; push_cast
        exact ⟨6 * r ^ 2 + 12 * r + 5, by ring⟩
    · rcases Nat.lt_or_ge k 4 with hk4 | hk4
      · have hk3 : k = 3 := by omega
        subst hk3
        refine ⟨fun h => by simp at h, fun _ => ?_⟩
        simp only [D, rp]; push_cast
        exact ⟨16 * r ^ 3 + 60 * r ^ 2 + 70 * r + 25, by ring⟩
      · refine ⟨fun h => by simp at h; omega, fun _ => ?_⟩
        have h1 : Even (D (r + r) k) := ih.2 (by simp; omega)
        have h2 : Even (rp (r + r) k) := rp_even_of_two_le ⟨r, rfl⟩ k (by omega)
        simp only [D]
        exact (h1.mul_right _).add h2

lemma DP_even {x : ℤ} (hx : Even x) (T : Finset ℕ) (hT : (T ∩ {1, 2, 3}).card = 2) :
    Even (DP T x) := by
  classical
  unfold DP
  rw [← Finset.sum_filter_add_sum_filter_not T (fun k => k ∈ ({1, 2, 3} : Finset ℕ))]
  have hA : Even (∑ k ∈ T.filter (fun k => k ∈ ({1, 2, 3} : Finset ℕ)), D x k) := by
    have hf : T.filter (fun k => k ∈ ({1, 2, 3} : Finset ℕ)) = T ∩ {1, 2, 3} := by
      ext k; simp
    rw [hf]
    obtain ⟨i, j, hij, hs⟩ := Finset.card_eq_two.mp hT
    rw [hs, Finset.sum_pair hij]
    have hi : i ∈ T ∩ {1, 2, 3} := by rw [hs]; simp
    have hj : j ∈ T ∩ {1, 2, 3} := by rw [hs]; simp
    exact Odd.add_odd ((D_parity hx i).1 (Finset.mem_inter.mp hi).2)
      ((D_parity hx j).1 (Finset.mem_inter.mp hj).2)
  have hB : Even (∑ k ∈ T.filter (fun k => k ∉ ({1, 2, 3} : Finset ℕ)), D x k) := by
    apply Finset.even_sum
    intro k hk
    exact (D_parity hx k).2 (Finset.mem_filter.mp hk).2
  exact hA.add hB

/-! ### the low-level forcing lemma -/

lemma rp_dvd_rp (x : ℤ) {j k : ℕ} (h : j ≤ k) : rp x j ∣ rp x k := by
  induction k with
  | zero =>
    have : j = 0 := by omega
    subst this; exact dvd_rfl
  | succ k ih =>
    rcases Nat.lt_or_ge k j with hk | hk
    · have : j = k + 1 := by omega
      subst this; exact dvd_rfl
    · exact (ih hk).mul_right _

lemma two_coprime_of_odd {m : ℤ} (hm : Odd m) (n : ℕ) : IsCoprime ((2 : ℤ) ^ n) m := by
  apply IsCoprime.pow_left
  obtain ⟨s, rfl⟩ := hm
  exact ⟨-s, 1, by ring⟩

/-- If 2^w ∥ (x+2), x even, 0 ∈ T and 2^(w+1) ∣ P T x, then exactly two of 1,2,3 lie in T
    (namely 1, and exactly one of 2, 3). -/
lemma forcing {x : ℤ} (hx : Even x) {w : ℕ} (hw : (2 : ℤ) ^ w ∣ x + 2)
    (hw' : ¬ (2 : ℤ) ^ (w + 1) ∣ x + 2)
    (T : Finset ℕ) (h0 : 0 ∈ T) (hT : (2 : ℤ) ^ (w + 1) ∣ P T x) : (T ∩ {1, 2, 3}).card = 2 := by
  classical
  obtain ⟨r, hr⟩ := hx
  have hbig : ∀ k, 4 ≤ k → (2 : ℤ) ^ (w + 1) ∣ rp x k := by
    intro k hk
    refine dvd_trans ?_ (rp_dvd_rp x hk)
    have e4 : rp x 4 = ((x + 2) * (x + 4)) * ((x + 1) * (x + 3)) := by simp [rp]; ring
    rw [e4, pow_succ]
    have h4 : (2 : ℤ) ∣ x + 4 := ⟨r + 2, by rw [hr]; ring⟩
    exact (mul_dvd_mul hw h4).mul_right _
  have hsplit : P T x = (∑ k ∈ T.filter (fun k => k < 4), rp x k)
      + ∑ k ∈ T.filter (fun k => ¬ k < 4), rp x k := by
    unfold P; rw [Finset.sum_filter_add_sum_filter_not]
  have hbigsum : (2 : ℤ) ^ (w + 1) ∣ ∑ k ∈ T.filter (fun k => ¬ k < 4), rp x k :=
    Finset.dvd_sum fun k hk => hbig k (by simp at hk; omega)
  have hsmall : (2 : ℤ) ^ (w + 1) ∣ ∑ k ∈ T.filter (fun k => k < 4), rp x k := by
    rw [hsplit] at hT; exact (dvd_add_left hbigsum).mp hT
  have hfilt : T.filter (fun k => k < 4) = (Finset.range 4).filter (fun k => k ∈ T) := by
    ext k; simp [and_comm]
  have hsm : ∑ k ∈ T.filter (fun k => k < 4), rp x k
      = 1 + (if 1 ∈ T then x + 1 else 0) + (if 2 ∈ T then (x + 1) * (x + 2) else 0)
        + (if 3 ∈ T then (x + 1) * (x + 2) * (x + 3) else 0) := by
    rw [hfilt, Finset.sum_filter]
    simp only [Finset.sum_range_succ, Finset.sum_range_zero, h0, ite_true]
    rw [rp1, rp2, rp3]
    simp [rp]
  rw [hsm] at hsmall
  have odd_nd : ∀ m : ℤ, Odd m → ¬ (2 : ℤ) ^ (w + 1) ∣ m := fun m hm hd => by
    have h2 : (2 : ℤ) ∣ m := dvd_trans (dvd_pow_self 2 (Nat.succ_ne_zero w)) hd
    exact (Int.not_even_iff_odd.mpr hm) (even_iff_two_dvd.mpr h2)
  have key : ∀ m : ℤ, Odd m → ¬ (2 : ℤ) ^ (w + 1) ∣ (x + 2) * m := by
    intro m hm hdiv
    exact hw' ((two_coprime_of_odd hm (w + 1)).dvd_of_dvd_mul_right hdiv)
  subst hr
  by_cases h1 : 1 ∈ T <;> by_cases h2 : 2 ∈ T <;> by_cases h3 : 3 ∈ T <;>
    simp only [h1, h2, h3, ↓reduceIte] at hsmall
  · exact absurd (by convert hsmall using 1; ring :
      (2 : ℤ) ^ (w + 1) ∣ (r + r + 2) * ((r + r) ^ 2 + 5 * (r + r) + 5))
      (key _ ⟨2 * r ^ 2 + 5 * r + 2, by ring⟩)
  · have : T ∩ {1, 2, 3} = {1, 2} := by
      ext k; simp only [Finset.mem_inter, Finset.mem_insert, Finset.mem_singleton]
      constructor
      · rintro ⟨hk, h | h | h⟩ <;> subst h <;> simp_all
      · rintro (h | h) <;> subst h <;> simp_all
    rw [this]; rfl
  · have : T ∩ {1, 2, 3} = {1, 3} := by
      ext k; simp only [Finset.mem_inter, Finset.mem_insert, Finset.mem_singleton]
      constructor
      · rintro ⟨hk, h | h | h⟩ <;> subst h <;> simp_all
      · rintro (h | h) <;> subst h <;> simp_all
    rw [this]; rfl
  · exact absurd (by convert hsmall using 1; ring : (2 : ℤ) ^ (w + 1) ∣ r + r + 2) hw'
  · exact absurd hsmall (odd_nd _ ⟨(2 * r + 1) * (r + 1) * (2 * r + 4), by ring⟩)
  · exact absurd hsmall (odd_nd _ ⟨(2 * r + 1) * (r + 1), by ring⟩)
  · exact absurd hsmall (odd_nd _ ⟨(2 * r + 1) * (r + 1) * (2 * r + 3), by ring⟩)
  · exact absurd hsmall (odd_nd _ ⟨0, by ring⟩)

/-! ### the p = 2 sibling theorem -/

/-- `Good x K` : some T ∋ 0 has 2^K ∣ P T x, i.e. g(x,2) ≥ K. -/
def Good (x : ℤ) (K : ℕ) : Prop := ∃ T : Finset ℕ, 0 ∈ T ∧ (2 : ℤ) ^ K ∣ P T x

lemma good_of_cube {x : ℤ} {G : ℕ} (hG : 1 ≤ G) (h : (2 : ℤ) ^ G ∣ x + 2) : Good x (G + 1) := by
  refine ⟨{0, 1, 3}, by simp, ?_⟩
  rw [cube]
  have h1 : (2 : ℤ) ^ (G + 1) ∣ (2 ^ G) ^ 3 := by
    rw [← pow_mul]; exact pow_dvd_pow 2 (by omega)
  exact dvd_trans h1 (pow_dvd_pow_of_dvd h 3)

lemma transfer {x : ℤ} (hx : Even x) {G w : ℕ} (hG : 1 ≤ G) (hwG : w < G)
    (hw : (2 : ℤ) ^ w ∣ x + 2) (hw' : ¬ (2 : ℤ) ^ (w + 1) ∣ x + 2)
    (h : ℤ) (hh : h = 2 ^ G ∨ h = -2 ^ G) : Good x (G + 1) → Good (x + h) (G + 1) := by
  rintro ⟨T, h0, hT⟩
  refine ⟨T, h0, ?_⟩
  have hc := forcing hx hw hw' T h0 (dvd_trans (pow_dvd_pow 2 (by omega)) hT)
  obtain ⟨d, hd⟩ := DP_even hx T hc
  obtain ⟨q, hq⟩ := taylor_P T x h
  have hh2 : h ^ 2 = 2 ^ (2 * G) := by
    rcases hh with rfl | rfl
    · rw [← pow_mul, mul_comm]
    · rw [neg_sq, ← pow_mul, mul_comm]
  have expand : P T (x + h) = P T x + h * (d + d) + h ^ 2 * q := by
    rw [← hd]; linear_combination hq
  rw [expand]
  refine dvd_add (dvd_add hT ?_) ?_
  · rcases hh with rfl | rfl
    · exact ⟨d, by ring⟩
    · exact ⟨-d, by ring⟩
  · rw [hh2]; exact dvd_mul_of_dvd_left (pow_dvd_pow 2 (by omega)) q

theorem sibling (x : ℤ) (hx : Even x) (G : ℕ) (hG : 1 ≤ G) :
    Good x (G + 1) ↔ Good (x + 2 ^ G) (G + 1) := by
  by_cases hdiv : (2 : ℤ) ^ G ∣ x + 2
  · constructor <;> intro _
    · apply good_of_cube hG
      have e : x + 2 ^ G + 2 = (x + 2) + 2 ^ G := by ring
      rw [e]; exact dvd_add hdiv dvd_rfl
    · exact good_of_cube hG hdiv
  · have hex : ∃ w, ¬ (2 : ℤ) ^ (w + 1) ∣ x + 2 :=
      ⟨G - 1, by rw [Nat.sub_add_cancel hG]; exact hdiv⟩
    classical
    set w := Nat.find hex with hwdef
    have hw' : ¬ (2 : ℤ) ^ (w + 1) ∣ x + 2 := Nat.find_spec hex
    have hwle : w ≤ G - 1 := Nat.find_min' hex (by rw [Nat.sub_add_cancel hG]; exact hdiv)
    have hwG : w < G := by omega
    have hw : (2 : ℤ) ^ w ∣ x + 2 := by
      rcases Nat.eq_zero_or_pos w with h0 | hpos
      · rw [h0]; simp
      · have := Nat.find_min hex (show w - 1 < w by omega)
        rw [Nat.sub_add_cancel hpos] at this
        exact not_not.mp this
    have hdivG : (2 : ℤ) ^ (w + 1) ∣ 2 ^ G := pow_dvd_pow 2 (by omega)
    have hx' : Even (x + 2 ^ G) := hx.add (Int.even_pow.mpr ⟨even_two, by omega⟩)
    have hw2 : (2 : ℤ) ^ w ∣ x + 2 ^ G + 2 := by
      have e : x + 2 ^ G + 2 = (x + 2) + 2 ^ G := by ring
      rw [e]; exact dvd_add hw (pow_dvd_pow 2 (by omega))
    have hw2' : ¬ (2 : ℤ) ^ (w + 1) ∣ x + 2 ^ G + 2 := by
      intro hc
      apply hw'
      have e : x + 2 = (x + 2 ^ G + 2) - 2 ^ G := by ring
      rw [e]; exact dvd_sub hc hdivG
    constructor
    · exact transfer hx hG hwG hw hw' (2 ^ G) (Or.inl rfl)
    · intro h
      have := transfer hx' hG hwG hw2 hw2' (-2 ^ G) (Or.inr rfl) h
      have e : x + 2 ^ G + -2 ^ G = x := by ring
      rwa [e] at this

theorem periodic (x : ℤ) (hx : Even x) (G : ℕ) (hG : 1 ≤ G) (c : ℤ) :
    Good x (G + 1) ↔ Good (x + c * 2 ^ G) (G + 1) := by
  have hev : ∀ n : ℤ, Even (x + n * 2 ^ G) := fun n =>
    hx.add ((Int.even_pow.mpr ⟨even_two, by omega⟩).mul_left n)
  induction c using Int.induction_on with
  | zero => simp
  | succ n ih =>
    have h1 := sibling (x + (n : ℤ) * 2 ^ G) (hev n) G hG
    have e : x + (n : ℤ) * 2 ^ G + 2 ^ G = x + ((n : ℤ) + 1) * 2 ^ G := by ring
    rw [e] at h1
    exact ih.trans h1
  | pred n ih =>
    have h1 := sibling (x + (-(n : ℤ) - 1) * 2 ^ G) (hev _) G hG
    have e : x + (-(n : ℤ) - 1) * 2 ^ G + 2 ^ G = x + -(n : ℤ) * 2 ^ G := by ring
    rw [e] at h1
    exact ih.trans h1.symm

lemma good_locality {x y : ℤ} {K : ℕ} (h : x ≡ y [ZMOD 2 ^ K]) : Good x K ↔ Good y K := by
  have tr : ∀ {u v : ℤ}, u ≡ v [ZMOD 2 ^ K] → Good u K → Good v K := by
    intro u v huv hu
    obtain ⟨T, h0, hT⟩ := hu
    refine ⟨T, h0, ?_⟩
    have hd := Int.ModEq.dvd (locality T huv)
    have e : P T v = (P T v - P T u) + P T u := by ring
    rw [e]; exact dvd_add hd hT
  exact ⟨tr h, tr h.symm⟩

/-- Constancy (Kitamura's observation, now a theorem): for p = 2, if g(x,2) = G ≥ 1 exactly
    then g(y,2) = G for every y ≡ x (mod 2^G). -/
theorem constancy (x y : ℤ) (hx : Even x) (G : ℕ) (hG : 1 ≤ G) (hxy : x ≡ y [ZMOD 2 ^ G])
    (h1 : Good x G) (h2 : ¬ Good x (G + 1)) : Good y G ∧ ¬ Good y (G + 1) := by
  refine ⟨(good_locality hxy).mp h1, ?_⟩
  obtain ⟨c, hc⟩ := (Int.modEq_iff_dvd.mp hxy)
  have hy : y = x + c * 2 ^ G := by linear_combination hc
  rw [hy, ← periodic x hx G hG c]
  exact h2

/-! ### link with the original problem -/

lemma dvd_cancel_odd {e K : ℕ} {u X : ℤ} (hu : Odd u) :
    (2 : ℤ) ^ (e + K) ∣ 2 ^ e * u * X ↔ (2 : ℤ) ^ K ∣ X := by
  constructor
  · intro h
    rw [pow_add, mul_assoc] at h
    have h' : (2 : ℤ) ^ K ∣ u * X :=
      (mul_dvd_mul_iff_left (pow_ne_zero e (by norm_num : (2 : ℤ) ≠ 0))).mp h
    exact (two_coprime_of_odd hu K).dvd_of_dvd_mul_left h'
  · intro h
    rw [pow_add, mul_assoc]
    exact mul_dvd_mul_left _ (dvd_mul_of_dvd_right h u)

/-- `Good a K` ⟺ some finite set A = a + T (min A = a) has 2^(v₂(a!)+K) ∣ ∑_{n∈A} n!,
    i.e. Good a K ⟺ f(a,2) ≥ v₂(a!) + K. -/
theorem good_iff_fact (a K : ℕ) :
    Good (a : ℤ) K ↔ ∃ T : Finset ℕ, 0 ∈ T ∧
      (2 : ℤ) ^ ((a.factorial).factorization 2 + K) ∣ ∑ k ∈ T, ((a + k).factorial : ℤ) := by
  set e := (a.factorial).factorization 2
  have hsplit : (a.factorial : ℤ) = 2 ^ e * ((a.factorial / 2 ^ e : ℕ) : ℤ) := by
    have := Nat.ordProj_mul_ordCompl_eq_self a.factorial 2
    exact_mod_cast this.symm
  have hodd : Odd ((a.factorial / 2 ^ e : ℕ) : ℤ) := by
    have hnd : ¬ 2 ∣ a.factorial / 2 ^ e :=
      Nat.not_dvd_ordCompl Nat.prime_two (Nat.factorial_ne_zero a)
    rw [Int.odd_coe_nat]
    exact Nat.odd_iff.mpr (Nat.two_dvd_ne_zero.mp hnd)
  constructor
  · rintro ⟨T, h0, hT⟩
    refine ⟨T, h0, ?_⟩
    rw [normal_form, hsplit]
    exact (dvd_cancel_odd hodd).mpr hT
  · rintro ⟨T, h0, hT⟩
    refine ⟨T, h0, ?_⟩
    rw [normal_form, hsplit] at hT
    exact (dvd_cancel_odd hodd).mp hT

/-- `Fge a K` : f(a,2) ≥ v₂(a!) + K, i.e. some A = a + T (T ∋ 0 finite) has 2^(v₂(a!)+K) ∣ ∑_{n∈A} n!. -/
def Fge (a K : ℕ) : Prop := ∃ T : Finset ℕ, 0 ∈ T ∧
  (2 : ℤ) ^ ((a.factorial).factorization 2 + K) ∣ ∑ k ∈ T, ((a + k).factorial : ℤ)

/-- Constancy phrased with factorial sums: if a is even, G ≥ 1, and f(a,2) = v₂(a!) + G exactly,
    then f(b,2) = v₂(b!) + G exactly for every b ≡ a (mod 2^G). -/
theorem constancy_f (a b G : ℕ) (ha : Even a) (hG : 1 ≤ G) (hab : (a : ℤ) ≡ b [ZMOD 2 ^ G])
    (h1 : Fge a G) (h2 : ¬ Fge a (G + 1)) : Fge b G ∧ ¬ Fge b (G + 1) := by
  have hx : Even (a : ℤ) := by exact_mod_cast ha
  rw [Fge, ← good_iff_fact] at h1 h2
  have := constancy (a : ℤ) (b : ℤ) hx G hG hab h1 h2
  rw [Fge, Fge, ← good_iff_fact, ← good_iff_fact]
  exact this

end E404

#print axioms E404.sibling
#print axioms E404.constancy
#print axioms E404.good_iff_fact
#print axioms E404.constancy_f
