import Mathlib

/-!
# Erdős #404, Theorem F (finiteness families): the no-exact-cancellation lemma

For d = k - 1 ≥ 2 and S ⊆ {0,…,d} with d ∈ S, the integer
  N_S = ∑_{u ∈ S} (-1)^u · ∏_{i ∈ (u, d]} i      ( = d! · ∑_{u∈S} (-1)^u / u! )
is ≡ (-1)^d (mod d), hence nonzero.  Consequently Q_S = ∑_{u∈S} (-1)^u/u! ≠ 0, so
τ(k,p) = max_S v_p(Q_S) is finite for every k ≥ 3.  (For k = 2, i.e. d = 1, the
set S = {0,1} gives Q_S = 0: this is the identity (N-2)! + (N-1)! = N·(N-2)!.)
-/

open Finset

/-- `N d S = ∑_{u∈S} (-1)^u ∏_{i ∈ Ioc u d} i`, i.e. `d! * ∑_{u∈S} (-1)^u/u!`. -/
def NS (d : ℕ) (S : Finset ℕ) : ℤ :=
  ∑ u ∈ S, (-1 : ℤ) ^ u * ∏ i ∈ Ioc u d, (i : ℤ)

theorem NS_dvd_sub (d : ℕ) (S : Finset ℕ) (hS : S ⊆ range (d + 1)) (hd : d ∈ S) :
    (d : ℤ) ∣ NS d S - (-1 : ℤ) ^ d := by
  unfold NS
  rw [← add_sum_erase S _ hd]
  simp only [Ioc_self, prod_empty, mul_one, add_sub_cancel_left]
  apply dvd_sum
  intro u hu
  have hu' : u ∈ S := mem_of_mem_erase hu
  have hne : u ≠ d := ne_of_mem_erase hu
  have hlt : u < d := by
    have := mem_range.mp (hS hu')
    omega
  apply Dvd.dvd.mul_left
  exact dvd_prod_of_mem (fun i : ℕ => (i : ℤ)) (mem_Ioc.mpr ⟨hlt, le_refl d⟩)

theorem NS_ne_zero (d : ℕ) (h2 : 2 ≤ d) (S : Finset ℕ) (hS : S ⊆ range (d + 1)) (hd : d ∈ S) :
    NS d S ≠ 0 := by
  intro h0
  have h := NS_dvd_sub d S hS hd
  rw [h0, zero_sub, dvd_neg] at h
  have hu : IsUnit ((-1 : ℤ) ^ d) := (isUnit_one.neg).pow d
  have hdu : IsUnit (d : ℤ) := isUnit_of_dvd_unit h hu
  rcases Int.isUnit_iff.mp hdu with h1 | h1 <;> omega

/-- Sanity instance (k = 3, p = 5): the start-block sums for a ≡ -3 (mod 5) are
  2!, 2!+3!, 2!+4!, 2!+3!+4! = 2, 8, 26, 32, none divisible by 5, so f(a,5) = v_5(a!). -/
example : ∀ s ∈ [2, 2 + 6, 2 + 24, 2 + 6 + 24], ¬ (5 ∣ s) := by decide

/-!
# Gate lemma (approach form)

If p^j ∣ m + 1 + i' (i.e. block m sits i' blocks before a gate of level ≥ j), then for every r,
  ∏_{k=1}^{r} (p m + k) ≡ ∏_{k=1}^{r} (k - (1+i') p)   (mod p^{j+1}).
With i' = 0 this says the gate block's partial products are ≡ (-1)^r (p-1)!/(p-1-r)!,
independent of the higher digits of m.
-/
theorem gate_factor (p j m i' k : ℕ) (h : p ^ j ∣ m + 1 + i') :
    ((p * m + k : ℕ) : ℤ) ≡ (k : ℤ) - (1 + i') * p [ZMOD (p : ℤ) ^ (j + 1)] := by
  obtain ⟨c, hc⟩ := h
  apply Int.ModEq.symm
  rw [Int.modEq_iff_dvd]
  refine ⟨(c : ℤ), ?_⟩
  have hc' : ((m : ℤ) + 1 + i') = (p : ℤ) ^ j * c := by exact_mod_cast hc
  push_cast
  have : (p : ℤ) * m + k - (k - (1 + i') * p) = p * (m + 1 + i') := by ring
  rw [this, hc']
  ring

theorem gate_prod (p j m i' : ℕ) (h : p ^ j ∣ m + 1 + i') (r : ℕ) :
    (∏ k ∈ Finset.Icc 1 r, ((p * m + k : ℕ) : ℤ)) ≡
      ∏ k ∈ Finset.Icc 1 r, ((k : ℤ) - (1 + i') * p) [ZMOD (p : ℤ) ^ (j + 1)] := by
  induction r with
  | zero => simp
  | succ n ih =>
    rw [Finset.prod_Icc_succ_top (by omega), Finset.prod_Icc_succ_top (by omega)]
    exact Int.ModEq.mul ih (gate_factor p j m i' (n + 1) h)

#print axioms NS_ne_zero
#print axioms gate_prod
