import Mathlib

/-!
# Subset sums of nonzero residues mod p (Cauchy–Davenport), used for Erdős #404

`subsetSums l` is the set of all subset sums of the list `l` in `ZMod p`.
If all entries are nonzero then `#(subsetSums l) ≥ min p (length l + 1)`; in particular
`p - 1` nonzero residues already have subset sums covering all of `ZMod p`.

Application in the #404 notes: the `p` factorials `(pm)!, ..., (pm+p-1)!` all have the same
`p`-adic valuation `e` and nonzero unit parts mod `p`, so their subset sums hit every class of
`p^e Z / p^{e+1} Z`.  This is the "one-block window" step used without computer search when
`v_p(G) = 1` (Tao's gate lemma with H = p).
-/

open Finset
open scoped Pointwise

variable {p : ℕ}

/-- All subset sums of a list, as a finset of `ZMod p`. -/
def subsetSums : List (ZMod p) → Finset (ZMod p)
  | [] => {0}
  | x :: xs => subsetSums xs + ({0, x} : Finset (ZMod p))

theorem card_subsetSums (hp : p.Prime) :
    ∀ (l : List (ZMod p)), (∀ x ∈ l, x ≠ 0) → min p (l.length + 1) ≤ (subsetSums l).card
  | [], _ => by
    simp [subsetSums]
  | x :: xs, hl => by
    have hx : x ≠ 0 := hl x (by simp)
    have hxs : ∀ y ∈ xs, y ≠ 0 := fun y hy => hl y (by simp [hy])
    have ih := card_subsetSums hp xs hxs
    have hne : (subsetSums xs).Nonempty := by
      rcases Nat.eq_zero_or_pos (subsetSums xs).card with h | h
      · have h2 : 2 ≤ p := hp.two_le
        omega
      · exact card_pos.mp h
    have ht : ({0, x} : Finset (ZMod p)).Nonempty := ⟨0, by simp⟩
    have hcard2 : ({0, x} : Finset (ZMod p)).card = 2 := by
      rw [card_insert_of_notMem (by simpa [eq_comm] using hx)]
      simp
    have cd := ZMod.cauchy_davenport hp hne ht
    rw [hcard2] at cd
    show min p (xs.length + 1 + 1) ≤ (subsetSums xs + ({0, x} : Finset (ZMod p))).card
    omega

/-- `p - 1` (or more) nonzero residues: subset sums cover `ZMod p`. -/
theorem subsetSums_eq_univ (hp : p.Prime) (l : List (ZMod p)) (hl : ∀ x ∈ l, x ≠ 0)
    (hlen : p - 1 ≤ l.length) :
    haveI : NeZero p := ⟨hp.ne_zero⟩
    subsetSums l = Finset.univ := by
  have : NeZero p := ⟨hp.ne_zero⟩
  have h := card_subsetSums hp l hl
  have hp2 := hp.two_le
  have hle : (subsetSums l).card ≤ p := by
    simpa [ZMod.card] using (Finset.card_le_univ (subsetSums l))
  apply Finset.eq_univ_of_card
  rw [ZMod.card]
  omega

#print axioms card_subsetSums
#print axioms subsetSums_eq_univ
