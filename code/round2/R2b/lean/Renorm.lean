import Mathlib

/-!
# Erdős #404, round 2 (R2b): two small lemmas on the renormalisation route

1. `worst_case_iff`: in a finite additive group `G` with subgroup `K`, a set `B` has the
   property "for every `A` meeting every coset of `K`, the sumset `A + B` contains a given
   nonempty target `T`" iff `B` contains a full coset `c + K`.
   (Fullness-only propagation of carry sets: note.md Thm 3.12 setting.)

2. `window_succ`: the window recursion `y_{H+1, i+1}(X) = (X - H) * y_{H,i}(X)` for
   `y_{H,i}(X) = ∏_{s<i} (X - (H - (s+1)))`.
-/

open Set Pointwise

section WorstCase

variable {G : Type*} [AddCommGroup G]

/-- `A` meets every coset of `K`. -/
def MeetsAllCosets (K : AddSubgroup G) (A : Set G) : Prop :=
  ∀ g : G, ∃ a ∈ A, a - g ∈ K

theorem worst_case_iff (K : AddSubgroup G) (B T : Set G) (hT : T.Nonempty) :
    (∀ A : Set G, MeetsAllCosets K A → T ⊆ A + B) ↔
      ∃ c : G, ∀ k ∈ K, c + k ∈ B := by
  constructor
  · intro h
    by_contra hne
    push Not at hne
    obtain ⟨t0, ht0⟩ := hT
    -- adversarial set
    let A : Set G := {a | t0 - a ∉ B}
    have hA : MeetsAllCosets K A := by
      intro g
      obtain ⟨k, hk, hkB⟩ := hne (t0 - g)
      refine ⟨g - k, ?_, ?_⟩
      · show t0 - (g - k) ∉ B
        have : t0 - (g - k) = t0 - g + k := by abel
        rw [this]; exact hkB
      · have : g - k - g = -k := by abel
        rw [this]; exact K.neg_mem hk
    have := h A hA ht0
    obtain ⟨a, ha, b, hb, hab⟩ := this
    have hab' : a + b = t0 := hab
    apply ha
    have : t0 - a = b := by rw [← hab']; abel_nf
    rw [this]; exact hb
  · rintro ⟨c, hc⟩ A hA t ht
    obtain ⟨a, ha, hak⟩ := hA (t - c)
    refine ⟨a, ha, t - a, ?_, by abel_nf⟩
    have : t - a = c + -(a - (t - c)) := by abel
    rw [this]
    exact hc _ (K.neg_mem hak)

end WorstCase

section Window

variable {R : Type*} [CommRing R]

/-- `y H i X = ∏_{s < i} (X - (H - (s+1)))`, the normalised window element of note.md Thm 3.12. -/
def ywin (H : ℕ) (i : ℕ) (X : R) : R :=
  ∏ s ∈ Finset.range i, (X - ((H : R) - ((s : R) + 1)))

theorem ywin_zero (H : ℕ) (X : R) : ywin H 0 X = 1 := by
  simp [ywin]

theorem window_succ (H i : ℕ) (X : R) :
    ywin (H + 1) (i + 1) X = (X - (H : R)) * ywin H i X := by
  unfold ywin
  rw [Finset.prod_range_succ']
  rw [mul_comm]
  congr 1
  · push_cast; ring
  · apply Finset.prod_congr rfl
    intro s _
    push_cast; ring

end Window

/-- Abstract monotonicity: if the subset sums of a list `L` cover a ring `R` and `u` is a
unit, then the subset sums of `1 :: (u • L)` cover `R`. -/
theorem cover_extend {R : Type*} [CommRing R] (L : List R) (u : Rˣ)
    (h : ∀ x : R, ∃ S : List R, S.Sublist L ∧ S.sum = x) :
    ∀ x : R, ∃ S : List R, S.Sublist (1 :: L.map (fun z => (u : R) * z)) ∧ S.sum = x := by
  intro x
  obtain ⟨S, hS, hsum⟩ := h ((↑u⁻¹ : R) * x)
  refine ⟨S.map (fun z => (u : R) * z), ?_, ?_⟩
  · exact List.Sublist.cons _ (hS.map _)
  · rw [List.sum_map_mul_left]
    simp only [List.map_id']
    rw [hsum, ← mul_assoc, Units.mul_inv, one_mul]

#print axioms worst_case_iff
#print axioms window_succ
#print axioms cover_extend
