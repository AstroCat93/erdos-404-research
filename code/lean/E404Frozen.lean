/-
Erdős #404 — frozen residue classes for general primes (Lean 4 + Mathlib).
Self-contained (repeats the basic definitions of E404Behaviour.lean).

  GoodP p x K  :≡  ∃ T ∋ 0, p^K ∣ ∑_{k∈T} (x+1)⋯(x+k)       ("g(x,p) ≥ K")
  goodP_iff_fact : for a : ℕ and p prime, GoodP p a K ↔ ∃ T ∋ 0, p^(v_p(a!)+K) ∣ ∑_{k∈T} (a+k)!
                   i.e. GoodP p a K ↔ f(a,p) ≥ v_p(a!) + K.
  good1_iff_small : if p ∣ x + j (j ≥ 1) then GoodP p x 1 only depends on T ⊆ [0,j)  (finite check).
  frozen_m1 : every prime p, every x ≡ -1 (mod p):            ¬ GoodP p x 1
  frozen_m3 : every prime p ≠ 3, every x ≡ -3 (mod p):        ¬ GoodP p x 1
  frozen_m4 : every prime p ∉ {2,5,7}, every x ≡ -4 (mod p):  ¬ GoodP p x 1
  Hence f(a,p) = v_p(a!) on these infinite families (frozen_f).
-/
import Mathlib

open Finset

namespace E404F

def rp (x : ℤ) : ℕ → ℤ
  | 0 => 1
  | k + 1 => rp x k * (x + (k + 1))

def P (T : Finset ℕ) (x : ℤ) : ℤ := ∑ k ∈ T, rp x k

def GoodP (p : ℕ) (x : ℤ) (K : ℕ) : Prop := ∃ T : Finset ℕ, 0 ∈ T ∧ (p : ℤ) ^ K ∣ P T x

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

lemma rp_modEq {x y m : ℤ} (h : x ≡ y [ZMOD m]) (k : ℕ) : rp x k ≡ rp y k [ZMOD m] := by
  induction k with
  | zero => rfl
  | succ k ih =>
    simp only [rp]
    exact ih.mul (h.add_right _)

theorem locality (T : Finset ℕ) {x y m : ℤ} (h : x ≡ y [ZMOD m]) : P T x ≡ P T y [ZMOD m] := by
  unfold P
  exact Int.ModEq.sum fun k _ => rp_modEq h k

lemma dvd_rp_of_le (x : ℤ) {j k : ℕ} (hj : 1 ≤ j) (hjk : j ≤ k) : (x + j) ∣ rp x k := by
  induction k with
  | zero => omega
  | succ k ih =>
    simp only [rp]
    rcases Nat.lt_or_ge k j with h | h
    · have : j = k + 1 := by omega
      subst this; push_cast; exact dvd_mul_left _ _
    · exact (ih h).mul_right _

theorem good1_iff_small (p : ℕ) (x : ℤ) (j : ℕ) (hj : 1 ≤ j) (hdiv : (p : ℤ) ∣ x + j) :
    GoodP p x 1 ↔ ∃ T ⊆ Finset.range j, 0 ∈ T ∧ (p : ℤ) ∣ P T x := by
  classical
  constructor
  · rintro ⟨T, h0, hT⟩
    refine ⟨T.filter (· < j), fun k hk => Finset.mem_range.mpr (Finset.mem_filter.mp hk).2,
      Finset.mem_filter.mpr ⟨h0, by omega⟩, ?_⟩
    have hsplit : P T x = P (T.filter (· < j)) x + ∑ k ∈ T.filter (fun k => ¬ k < j), rp x k := by
      unfold P; rw [Finset.sum_filter_add_sum_filter_not]
    have hbig : (p : ℤ) ∣ ∑ k ∈ T.filter (fun k => ¬ k < j), rp x k :=
      Finset.dvd_sum fun k hk =>
        dvd_trans hdiv (dvd_rp_of_le x hj (by have := (Finset.mem_filter.mp hk).2; omega))
    rw [pow_one, hsplit] at hT
    exact (dvd_add_left hbig).mp hT
  · rintro ⟨T, -, h0, hT⟩
    exact ⟨T, h0, by rw [pow_one]; exact hT⟩

/-- transport along x ≡ -m (mod p) -/
lemma dvd_P_iff {p : ℕ} {x y : ℤ} (h : x ≡ y [ZMOD p]) (T : Finset ℕ) :
    (p : ℤ) ∣ P T x ↔ (p : ℤ) ∣ P T y := by
  have hm := locality T h
  constructor
  · intro hx
    have hd := Int.ModEq.dvd hm
    have e : P T y = (P T y - P T x) + P T x := by ring
    rw [e]; exact dvd_add hd hx
  · intro hy
    have hd := Int.ModEq.dvd hm.symm
    have e : P T x = (P T x - P T y) + P T y := by ring
    rw [e]; exact dvd_add hd hy

lemma subsets_range (j : ℕ) (T : Finset ℕ) (hT : T ⊆ Finset.range j) :
    T ∈ (Finset.range j).powerset := Finset.mem_powerset.mpr hT

/-- the finite tables P T (-m) for T ⊆ [0,m), 0 ∈ T  (m = 1, 3, 4) -/
lemma table_m1 : ∀ T ∈ (Finset.range 1).powerset, 0 ∈ T → P T (-1) = 1 := by decide
lemma table_m3 : ∀ T ∈ (Finset.range 3).powerset, 0 ∈ T →
    P T (-3) = 1 ∨ P T (-3) = -1 ∨ P T (-3) = 3 := by decide
lemma table_m4 : ∀ T ∈ (Finset.range 4).powerset, 0 ∈ T →
    P T (-4) = 1 ∨ P T (-4) = -5 ∨ P T (-4) = 7 ∨ P T (-4) = -2 ∨ P T (-4) = -8 ∨ P T (-4) = 4 := by
  decide

lemma prime_dvd_int {p : ℕ} (_hp : p.Prime) {v : ℤ} (h : (p : ℤ) ∣ v) : p ∣ v.natAbs :=
  Int.natCast_dvd.mp h

theorem frozen_m1 (p : ℕ) (hp : p.Prime) (x : ℤ) (hx : x ≡ -1 [ZMOD p]) : ¬ GoodP p x 1 := by
  have hdiv : (p : ℤ) ∣ x + (1 : ℕ) := by
    have := (Int.ModEq.dvd hx.symm); push_cast; simpa [sub_eq_add_neg, add_comm] using this
  rw [good1_iff_small p x 1 le_rfl hdiv]
  rintro ⟨T, hT, h0, hd⟩
  rw [dvd_P_iff hx T, table_m1 T (subsets_range 1 T hT) h0] at hd
  exact hp.one_lt.ne' (Nat.dvd_one.mp (prime_dvd_int hp hd))

theorem frozen_m3 (p : ℕ) (hp : p.Prime) (hp3 : p ≠ 3) (x : ℤ) (hx : x ≡ -3 [ZMOD p]) :
    ¬ GoodP p x 1 := by
  have hdiv : (p : ℤ) ∣ x + (3 : ℕ) := by
    have := (Int.ModEq.dvd hx.symm); push_cast; simpa [sub_eq_add_neg, add_comm] using this
  rw [good1_iff_small p x 3 (by norm_num) hdiv]
  rintro ⟨T, hT, h0, hd⟩
  rw [dvd_P_iff hx T] at hd
  rcases table_m3 T (subsets_range 3 T hT) h0 with h | h | h <;> rw [h] at hd <;>
    have hn := prime_dvd_int hp hd <;> simp at hn
  · exact hp.one_lt.ne' hn
  · exact hp.one_lt.ne' hn
  · exact hp3 ((Nat.prime_dvd_prime_iff_eq hp Nat.prime_three).mp hn)

theorem frozen_m4 (p : ℕ) (hp : p.Prime) (hp2 : p ≠ 2) (hp5 : p ≠ 5) (hp7 : p ≠ 7) (x : ℤ)
    (hx : x ≡ -4 [ZMOD p]) : ¬ GoodP p x 1 := by
  have hdiv : (p : ℤ) ∣ x + (4 : ℕ) := by
    have := (Int.ModEq.dvd hx.symm); push_cast; simpa [sub_eq_add_neg, add_comm] using this
  rw [good1_iff_small p x 4 (by norm_num) hdiv]
  rintro ⟨T, hT, h0, hd⟩
  rw [dvd_P_iff hx T] at hd
  have two_of : p ∣ 2 → False := fun h => hp2 ((Nat.prime_dvd_prime_iff_eq hp Nat.prime_two).mp h)
  rcases table_m4 T (subsets_range 4 T hT) h0 with h | h | h | h | h | h <;> rw [h] at hd <;>
    have hn := prime_dvd_int hp hd <;> simp at hn
  · exact hp.one_lt.ne' hn
  · exact hp5 ((Nat.prime_dvd_prime_iff_eq hp (by norm_num)).mp hn)
  · exact hp7 ((Nat.prime_dvd_prime_iff_eq hp (by norm_num)).mp hn)
  · exact two_of hn
  · exact two_of (hp.dvd_of_dvd_pow (show p ∣ 2 ^ 3 by norm_num; exact hn))
  · exact two_of (hp.dvd_of_dvd_pow (show p ∣ 2 ^ 2 by norm_num; exact hn))

/-! ### link with f(a,p) -/

lemma dvd_cancel_unit {p e K : ℕ} (hp : p.Prime) {u : ℕ} (hu : ¬ p ∣ u) {X : ℤ} :
    (p : ℤ) ^ (e + K) ∣ (p : ℤ) ^ e * u * X ↔ (p : ℤ) ^ K ∣ X := by
  have hcop : IsCoprime ((p : ℤ) ^ K) (u : ℤ) := by
    have : Nat.Coprime (p ^ K) u := Nat.Coprime.pow_left K ((Nat.Prime.coprime_iff_not_dvd hp).mpr hu)
    exact_mod_cast Nat.isCoprime_iff_coprime.mpr this
  constructor
  · intro h
    rw [pow_add, mul_assoc] at h
    have h' : (p : ℤ) ^ K ∣ u * X :=
      (mul_dvd_mul_iff_left (pow_ne_zero e (by exact_mod_cast hp.ne_zero))).mp h
    exact hcop.dvd_of_dvd_mul_left h'
  · intro h
    rw [pow_add, mul_assoc]
    exact mul_dvd_mul_left _ (dvd_mul_of_dvd_right h _)

theorem goodP_iff_fact (p : ℕ) (hp : p.Prime) (a K : ℕ) :
    GoodP p (a : ℤ) K ↔ ∃ T : Finset ℕ, 0 ∈ T ∧
      (p : ℤ) ^ ((a.factorial).factorization p + K) ∣ ∑ k ∈ T, ((a + k).factorial : ℤ) := by
  set e := (a.factorial).factorization p
  have hsplit : (a.factorial : ℤ) = (p : ℤ) ^ e * ((a.factorial / p ^ e : ℕ) : ℤ) := by
    have := Nat.ordProj_mul_ordCompl_eq_self a.factorial p
    exact_mod_cast this.symm
  have hnd : ¬ p ∣ a.factorial / p ^ e := Nat.not_dvd_ordCompl hp (Nat.factorial_ne_zero a)
  constructor
  · rintro ⟨T, h0, hT⟩
    refine ⟨T, h0, ?_⟩
    rw [normal_form, hsplit]
    exact (dvd_cancel_unit hp hnd).mpr hT
  · rintro ⟨T, h0, hT⟩
    refine ⟨T, h0, ?_⟩
    rw [normal_form, hsplit] at hT
    exact (dvd_cancel_unit hp hnd).mp hT

/-- f(a,p) = v_p(a!) on the frozen families: no T reaches exponent v_p(a!) + 1. -/
theorem frozen_f (p : ℕ) (hp : p.Prime) (a : ℕ)
    (h : (a : ℤ) ≡ -1 [ZMOD p] ∨ ((a : ℤ) ≡ -3 [ZMOD p] ∧ p ≠ 3) ∨
      ((a : ℤ) ≡ -4 [ZMOD p] ∧ p ≠ 2 ∧ p ≠ 5 ∧ p ≠ 7)) :
    ¬ ∃ T : Finset ℕ, 0 ∈ T ∧
      (p : ℤ) ^ ((a.factorial).factorization p + 1) ∣ ∑ k ∈ T, ((a + k).factorial : ℤ) := by
  rw [← goodP_iff_fact p hp]
  rcases h with h | ⟨h, h3⟩ | ⟨h, h2, h5, h7⟩
  · exact frozen_m1 p hp _ h
  · exact frozen_m3 p hp h3 _ h
  · exact frozen_m4 p hp h2 h5 h7 _ h

end E404F

#print axioms E404F.frozen_f

#print axioms E404F.frozen_m1
#print axioms E404F.frozen_m3
#print axioms E404F.frozen_m4
