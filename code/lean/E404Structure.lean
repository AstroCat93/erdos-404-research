import Mathlib

/-!
# Erdős #404 — two small machine-checked lemmas (A-structure)

1. `sigma_ne_zero`: for `t ≥ 2` and any finite `J ⊆ ℕ` containing `0`,
   `∑_{j ∈ J} (-1)^j * t.descFactorial j ≠ 0` (here `t.descFactorial j = t!/(t-j)!` for `j ≤ t`).
   This is the integer fact behind the "near -1" theorem: for `a ≡ -1-t (mod p^k)` with
   `p^k > max |σ|`, `f(a,p) = v_p(a!) + max_σ v_p(σ)`; in particular for `k = 1`,
   `f(a,p) = v_p(a!)`.
   (`t = 1`, `J = {0,1}` is the unique exception: `1 - 1 = 0`, i.e. the point `x = -2`.)

2. `two_adic_never_full`: for every residue `r` mod 16, the subset sums of the products
   `∏_{l=1}^{j} (r + l)` (`j = 0..15`) do not cover `ZMod 16`.  Hence for every `x ∈ ℤ_2`
   the achievement set `A_x = {∑_j e_j ∏_{l≤j}(x+l)}` is not all of `ℤ_2`; in particular
   Tao's gate method can never certify `f(a,2) = ∞`.
-/

open Finset

/-- `t ∣ t.descFactorial j` for `j ≥ 1`. -/
lemma dvd_descFactorial_of_pos (t j : ℕ) (hj : 1 ≤ j) : t ∣ t.descFactorial j := by
  obtain ⟨i, rfl⟩ : ∃ i, j = i + 1 := ⟨j - 1, by omega⟩
  rcases Nat.eq_zero_or_pos t with h | h
  · subst h; simp
  · obtain ⟨s, rfl⟩ : ∃ s, t = s + 1 := ⟨t - 1, by omega⟩
    rw [Nat.succ_descFactorial_succ]
    exact Dvd.intro _ rfl

theorem sigma_ne_zero (t : ℕ) (ht : 2 ≤ t) (J : Finset ℕ) (h0 : 0 ∈ J) :
    (∑ j ∈ J, (-1 : ℤ) ^ j * (t.descFactorial j : ℤ)) ≠ 0 := by
  intro hsum
  have hsplit := Finset.add_sum_erase J (fun j => (-1 : ℤ) ^ j * (t.descFactorial j : ℤ)) h0
  simp only [pow_zero, Nat.descFactorial_zero, Nat.cast_one, mul_one] at hsplit
  have hdvd : (t : ℤ) ∣ ∑ j ∈ J.erase 0, (-1 : ℤ) ^ j * (t.descFactorial j : ℤ) := by
    apply Finset.dvd_sum
    intro j hj
    have hj1 : 1 ≤ j := by
      have := Finset.ne_of_mem_erase hj
      omega
    exact Dvd.dvd.mul_left (Int.natCast_dvd_natCast.mpr (dvd_descFactorial_of_pos t j hj1)) _
  have h1 : (t : ℤ) ∣ 1 := by
    have : (1 : ℤ) = -(∑ j ∈ J.erase 0, (-1 : ℤ) ^ j * (t.descFactorial j : ℤ)) := by
      linarith
    rw [this]; exact (dvd_neg).mpr hdvd
  have : (t : ℤ) ≤ 1 := Int.le_of_dvd one_pos h1
  omega

/-- the unique exceptional identity, `t = 1`: `1 - 1 = 0` (the p-adic point `x = -2`). -/
example : (∑ j ∈ ({0, 1} : Finset ℕ), (-1 : ℤ) ^ j * ((1 : ℕ).descFactorial j : ℤ)) = 0 := by
  decide

/-- subset sums (as a set of residues) of a list of elements of `ZMod n`. -/
def subsetSums {n : ℕ} : List (ZMod n) → Finset (ZMod n)
  | [] => {0}
  | x :: xs => let s := subsetSums xs; s ∪ s.image (· + x)

/-- the elements `∏_{l=1}^{j} (r + l)` for `j = 0, …, m-1`, in `ZMod n`. -/
def prods (n r : ℕ) : ℕ → List (ZMod n)
  | 0 => []
  | m + 1 => prods n r m ++ [((List.range m).map (fun l => ((r + l + 1 : ℕ) : ZMod n))).prod]

/-- For p = 2: no residue r mod 16 has A_r ≡ everything mod 16.
(All products with j ≥ 16 contain the 16 consecutive factors r+1..r+16, hence vanish mod 16,
so the first 16 products already give all of A_r mod 16.) -/
theorem two_adic_never_full : ∀ r : Fin 16, (subsetSums (prods 16 r.val 16)).card < 16 := by
  decide

#print axioms sigma_ne_zero
#print axioms two_adic_never_full
