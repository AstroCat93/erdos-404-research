import Mathlib

/-!
# Erdős #404: the block-lifting lemma and the "first failure" reduction (machine-checked logic)

`P p a N` : there is a finite `T ⊆ [a, N)` with `a ∈ T` and `p ^ v_p(N!) ∣ ∑_{n ∈ T} n!`.
`f(a,p) ≥ v_p(N!)` iff `P p a N` (for `N > a`).

* `block_lift` (Tao's lemma, un-normalized form): if every multiple `p^{v(N1)} * s` can be
  completed by a subset of `[N1, N2)` to a multiple of `p^{v(N2)}`, then `P N1 → P N2`.
* `first_failure`: if the block lemma is available at every `N` with `1 ≤ v_p(N) ≤ T`
  (block length `≤ H`), then the least `N > a + H` with `¬ P p a N` is divisible by `p^(T+1)`.
The finite coverage computations (cov.c / cov_check.py) are what supply the hypothesis `hstep`;
that link (elements depend only on `N/p^t mod p^c`) is NOT formalized here.
-/

open Finset

namespace E404

/-- `v p N = v_p(N!)`. -/
noncomputable def v (p N : ℕ) : ℕ := padicValNat p N.factorial

def P (p a N : ℕ) : Prop :=
  ∃ T : Finset ℕ, a ∈ T ∧ (∀ n ∈ T, a ≤ n ∧ n < N) ∧ p ^ v p N ∣ ∑ n ∈ T, n.factorial

theorem block_lift {p a N1 N2 : ℕ} (h12 : N1 ≤ N2) (hP : P p a N1)
    (hcov : ∀ s : ℕ, ∃ U ⊆ Finset.Ico N1 N2,
      p ^ v p N2 ∣ p ^ v p N1 * s + ∑ n ∈ U, n.factorial) :
    P p a N2 := by
  obtain ⟨T, haT, hT, hdiv⟩ := hP
  obtain ⟨s, hs⟩ := hdiv
  obtain ⟨U, hU, hdivU⟩ := hcov s
  have hdisj : Disjoint T U := by
    rw [Finset.disjoint_left]
    intro n hnT hnU
    have h1 := (hT n hnT).2
    have h2 := (Finset.mem_Ico.mp (hU hnU)).1
    omega
  refine ⟨T ∪ U, Finset.mem_union_left _ haT, ?_, ?_⟩
  · intro n hn
    rcases Finset.mem_union.mp hn with h | h
    · exact ⟨(hT n h).1, lt_of_lt_of_le (hT n h).2 h12⟩
    · have hm := Finset.mem_Ico.mp (hU h)
      have := (hT a haT).2
      exact ⟨by omega, hm.2⟩
  · rw [Finset.sum_union hdisj, hs]
    exact hdivU

/-- If `p ∤ N` and `N ≥ 1` then `v p N = v p (N-1)`. -/
theorem v_succ_of_not_dvd {p N : ℕ} (hp : p.Prime) (hN : 1 ≤ N) (hpN : ¬ p ∣ N) :
    v p N = v p (N - 1) := by
  have := Fact.mk hp
  unfold v
  obtain ⟨M, rfl⟩ : ∃ M, N = M + 1 := ⟨N - 1, by omega⟩
  simp only [Nat.add_sub_cancel]
  rw [Nat.factorial_succ, padicValNat.mul (by omega) (Nat.factorial_ne_zero M)]
  have : padicValNat p (M + 1) = 0 := padicValNat.eq_zero_of_not_dvd hpN
  omega

theorem P_mono_of_eq {p a N N' : ℕ} (hle : N ≤ N') (hv : v p N' = v p N) (h : P p a N) :
    P p a N' := by
  obtain ⟨T, haT, hT, hdiv⟩ := h
  exact ⟨T, haT, fun n hn => ⟨(hT n hn).1, lt_of_lt_of_le (hT n hn).2 hle⟩, hv ▸ hdiv⟩

/-- First-failure reduction. `hstep` is the (computer-certified) block lemma at depths `1..T`. -/
theorem first_failure {p a T H : ℕ} (hp : p.Prime) (hH : 1 ≤ H)
    (hstep : ∀ N, a + H < N → 1 ≤ padicValNat p N → padicValNat p N ≤ T →
      (∀ M, a < M → M < N → P p a M) → P p a N)
    (N : ℕ) (haN : a + H < N) (hmin : ∀ M, a < M → M < N → P p a M) (hfail : ¬ P p a N) :
    p ^ (T + 1) ∣ N := by
  have := Fact.mk hp
  have hN0 : N ≠ 0 := by omega
  by_cases hdvd : p ∣ N
  · by_contra hcon
    have hle : padicValNat p N ≤ T := by
      by_contra hgt
      exact hcon ((padicValNat_dvd_iff_le hN0).mpr (by omega))
    have h1 : 1 ≤ padicValNat p N := one_le_padicValNat_of_dvd hN0 hdvd
    exact hfail (hstep N haN h1 hle hmin)
  · exfalso
    apply hfail
    have hprev := hmin (N - 1) (by omega) (by omega)
    exact P_mono_of_eq (by omega) (v_succ_of_not_dvd hp (by omega) hdvd) hprev

/-- Global consequence: with the block lemma at depths `1..T` (block length `≤ H`) and the base
range `(a, a+H]`, `P p a N` holds for every `a < N < p^(T+1)`; hence `f(a,p) ≥ v_p((p^(T+1)-1)!)`. -/
theorem all_below {p a T H : ℕ} (hp : p.Prime) (hH : 1 ≤ H)
    (hstep : ∀ N, a + H < N → 1 ≤ padicValNat p N → padicValNat p N ≤ T →
      (∀ M, a < M → M < N → P p a M) → P p a N)
    (hbase : ∀ N, a < N → N ≤ a + H → P p a N) :
    ∀ N, a < N → N < p ^ (T + 1) → P p a N := by
  intro N
  induction N using Nat.strong_induction_on with
  | _ N ih =>
    intro haN hNlt
    by_cases hsmall : N ≤ a + H
    · exact hbase N haN hsmall
    · by_contra hfail
      have hmin : ∀ M, a < M → M < N → P p a M :=
        fun M haM hMN => ih M hMN haM (lt_trans hMN hNlt)
      have hdvd := first_failure hp hH hstep N (by omega) hmin hfail
      have hpos : 0 < N := by omega
      exact absurd (Nat.le_of_dvd hpos hdvd) (by omega)

end E404

#print axioms E404.block_lift
#print axioms E404.first_failure
#print axioms E404.all_below
