import Mathlib

/-!
# Erdős #404, prime 2: the residue lemma and the halving lemma

For `x : ℤ` put `P b x = (x+1)(x+2)⋯(x+b)` and, for a finite `B ⊆ ℕ`,
`S B x = 1 + ∑_{b ∈ B} P (b+1) x`.
For a natural number `a ≥ 1` we have `a! * S B a = a! + ∑_{b∈B} (a+b+1)!`
(lemma `factorial_mul_S`), so with `g(a) := sup_B v_2(S B a)` one has
`f(a,2) = v_2(a!) + g(a)`, and `g(a) ≥ G ↔ ∃ B, 2^G ∣ S B a`.

* `residue_lemma`: `∃ B, m ∣ S B x` depends only on `x mod m` (any modulus `m`).
* `halving`: for `G ≥ 2`, `(∃ B, 2^G ∣ S B a) ↔ (∃ B, 2^G ∣ S B (a + 2^(G-1)))`,
  i.e. at `p = 2` the property `g(a) ≥ G` depends only on `a mod 2^(G-1)`.
* `g_eq_three`: for `a ≡ 4 (mod 8)`, `8 ∣ S {0,2} a` and `16 ∤ S B a` for every `B`,
  i.e. `f(a,2) = v_2(a!) + 3`.
* `halving2`: for `G ≥ 6` and `a ≡ 2 (mod 4)`,
  `(∃ B, 2^G ∣ S B a) ↔ (∃ B, 2^G ∣ S B (a + 2^(G-3)))`, i.e. on `a ≡ 2 (mod 4)` the property
  `g(a) ≥ G` depends only on `a mod 2^(G-3)`.
Checked with Lean 4.34.1 / Mathlib v4.34.1 (`lake env lean E404Halving.lean` inside the `formal/`
project); no `sorry`, only the standard axioms.
-/

open Finset

namespace E404

/-- `P b x = (x+1)(x+2)⋯(x+b)`. -/
def P (b : ℕ) (x : ℤ) : ℤ := ∏ i ∈ range b, (x + i + 1)

/-- A companion of `P` playing the role of the derivative `P'`. -/
def D : ℕ → ℤ → ℤ
  | 0, _ => 0
  | b + 1, x => D b x * (x + b + 1) + P b x

/-- Normalised factorial sum: `S B x = 1 + ∑_{b ∈ B} P (b+1) x`. -/
def S (B : Finset ℕ) (x : ℤ) : ℤ := 1 + ∑ b ∈ B, P (b + 1) x

lemma P_zero (x : ℤ) : P 0 x = 1 := by simp [P]

lemma P_succ (b : ℕ) (x : ℤ) : P (b + 1) x = P b x * (x + b + 1) := by
  simp [P, prod_range_succ]

/-- Link with factorials: `(a+b)! = a! * P b a`. -/
lemma factorial_add_eq (a b : ℕ) : (((a + b).factorial : ℕ) : ℤ) = (a.factorial : ℤ) * P b (a : ℤ) := by
  induction b with
  | zero => simp [P]
  | succ b ih =>
    rw [P_succ, ← add_assoc, Nat.factorial_succ]
    push_cast
    rw [ih]
    ring

/-- `a! * S B a = a! + ∑_{b ∈ B} (a+b+1)!`. -/
lemma factorial_mul_S (a : ℕ) (B : Finset ℕ) :
    (a.factorial : ℤ) * S B (a : ℤ) = (a.factorial : ℤ) + ∑ b ∈ B, (((a + (b + 1)).factorial : ℕ) : ℤ) := by
  simp only [S, mul_add, mul_one, mul_sum]
  congr 1
  refine sum_congr rfl (fun b _ => ?_)
  rw [factorial_add_eq]

/-! ### Residue lemma -/

lemma P_modEq {m x y : ℤ} (h : x ≡ y [ZMOD m]) (b : ℕ) : P b x ≡ P b y [ZMOD m] := by
  unfold P
  exact Int.ModEq.prod (fun i _ => (h.add_right _).add_right _)

lemma S_modEq {m x y : ℤ} (h : x ≡ y [ZMOD m]) (B : Finset ℕ) : S B x ≡ S B y [ZMOD m] := by
  unfold S
  exact Int.ModEq.add_left _ (Int.ModEq.sum (fun b _ => P_modEq h _))

/-- **Residue lemma.** Whether some `B` gives `m ∣ S B x` depends only on `x mod m`. -/
theorem residue_lemma {m x y : ℤ} (h : x ≡ y [ZMOD m]) :
    (∃ B : Finset ℕ, m ∣ S B x) ↔ (∃ B : Finset ℕ, m ∣ S B y) := by
  constructor
  · rintro ⟨B, hB⟩
    exact ⟨B, (Int.ModEq.dvd_iff (S_modEq h B)).mp hB⟩
  · rintro ⟨B, hB⟩
    exact ⟨B, (Int.ModEq.dvd_iff (S_modEq h B)).mpr hB⟩

/-! ### First-order Taylor expansion -/

lemma P_shift (b : ℕ) (x h : ℤ) : h ^ 2 ∣ P b (x + h) - (P b x + h * D b x) := by
  induction b with
  | zero => simp [P, D]
  | succ b ih =>
    obtain ⟨k, hk⟩ := ih
    refine ⟨k * (x + h + b + 1) + D b x, ?_⟩
    have e : P b (x + h) = P b x + h * D b x + h ^ 2 * k := by linarith
    rw [P_succ, P_succ, e]
    simp only [D]
    ring

/-! ### Parity facts for even `a` -/

lemma P_dvd_P {m n : ℕ} (hmn : m ≤ n) (x : ℤ) : P m x ∣ P n x := by
  induction n with
  | zero =>
    have : m = 0 := by omega
    subst this; exact dvd_rfl
  | succ n ih =>
    rcases Nat.eq_or_lt_of_le hmn with h | h
    · rw [h]
    · rw [P_succ]
      exact Dvd.dvd.mul_right (ih (by omega)) _

lemma P_one (x : ℤ) : P 1 x = x + 1 := by
  unfold P; rw [prod_range_one]; push_cast; ring
lemma P_two (x : ℤ) : P 2 x = (x + 1) * (x + 2) := by
  unfold P; simp only [prod_range_succ, prod_range_zero]; push_cast; ring
lemma P_three (x : ℤ) : P 3 x = (x + 1) * (x + 2) * (x + 3) := by
  unfold P; simp only [prod_range_succ, prod_range_zero]; push_cast; ring
lemma P_four (x : ℤ) : P 4 x = (x + 1) * (x + 2) * (x + 3) * (x + 4) := by
  unfold P; simp only [prod_range_succ, prod_range_zero]; push_cast; ring

lemma D_one (x : ℤ) : D 1 x = 1 := by
  simp only [D, P_zero]; ring
lemma D_two (x : ℤ) : D 2 x = 2 * x + 3 := by
  simp only [D, P, prod_range_succ, prod_range_zero]; push_cast; ring
lemma D_three (x : ℤ) : D 3 x = 3 * x ^ 2 + 12 * x + 11 := by
  simp only [D, P, prod_range_succ, prod_range_zero]; push_cast; ring
lemma D_four (x : ℤ) : D 4 x = 4 * x ^ 3 + 30 * x ^ 2 + 70 * x + 50 := by
  simp only [D, P, prod_range_succ, prod_range_zero]; push_cast; ring

/-- `P (b+1) x` is a multiple of `x + 1`. -/
lemma P_succ_dvd (b : ℕ) (x : ℤ) : (x + 1) ∣ P (b + 1) x := by
  have := P_dvd_P (show 1 ≤ b + 1 by omega) x
  rw [P_one] at this
  exact this

/-- For `b ≥ 4`, `(x+2)(x+4) ∣ P b x`. -/
lemma P_dvd_big {b : ℕ} (hb : 4 ≤ b) (x : ℤ) : (x + 2) * (x + 4) ∣ P b x := by
  have h4 := P_dvd_P hb x
  rw [P_four] at h4
  exact Dvd.dvd.trans ⟨(x + 1) * (x + 3), by ring⟩ h4

lemma P_even {a : ℤ} (ha : Even a) {b : ℕ} (hb : 2 ≤ b) : Even (P b a) := by
  have h2 := P_dvd_P hb a
  rw [P_two] at h2
  obtain ⟨m, rfl⟩ := ha
  exact (even_iff_two_dvd.mpr (Dvd.dvd.trans ⟨(m + m + 1) * (m + 1), by ring⟩ h2))

lemma D_even {a : ℤ} (ha : Even a) : ∀ b : ℕ, 4 ≤ b → Even (D b a) := by
  intro b hb
  induction b with
  | zero => omega
  | succ b ih =>
    rcases Nat.eq_or_lt_of_le hb with h | h
    · -- b + 1 = 4
      have hb3 : b = 3 := by omega
      subst hb3
      rw [D_four]
      obtain ⟨m, rfl⟩ := ha
      exact ⟨2 * (m + m) ^ 3 + 15 * (m + m) ^ 2 + 35 * (m + m) + 25, by ring⟩
    · simp only [D]
      exact Even.add (Even.mul_right (ih (by omega)) _) (P_even ha (by omega))

/-- An integer that is odd. -/
lemma isCoprime_two_pow_of_odd {w : ℤ} (hw : Odd w) (G : ℕ) : IsCoprime ((2 : ℤ) ^ G) w := by
  apply IsCoprime.pow_left
  obtain ⟨k, rfl⟩ := hw
  exact ⟨-k, 1, by ring⟩

/-- The sum over `B` split at 3. -/
lemma sum_split (B : Finset ℕ) (F : ℕ → ℤ) :
    ∑ b ∈ B, F b = ((if 0 ∈ B then F 0 else 0) + (if 1 ∈ B then F 1 else 0) + (if 2 ∈ B then F 2 else 0))
      + ∑ b ∈ B.filter (fun b => ¬ b < 3), F b := by
  rw [← sum_filter_add_sum_filter_not B (fun b => b < 3) F]
  congr 1
  have : B.filter (fun b => b < 3) = (range 3).filter (fun b => b ∈ B) := by
    ext b; simp only [mem_filter, mem_range]; tauto
  rw [this, sum_filter]
  simp only [sum_range_succ, sum_range_zero, zero_add]

/-- If `a` is even and `0 ∉ B` then `S B a` is odd. -/
lemma S_odd_of_not_mem {a : ℤ} (ha : Even a) {B : Finset ℕ} (h0 : 0 ∉ B) : Odd (S B a) := by
  unfold S
  have : Even (∑ b ∈ B, P (b + 1) a) := by
    apply Finset.even_sum
    intro b hb
    have : b ≠ 0 := fun h => h0 (h ▸ hb)
    exact P_even ha (by omega)
  rw [add_comm]
  exact this.add_one

/-- **Key lemma.** If `a` is even, `2^(G-1) ∤ a + 2` and `2^G ∣ S B a` (with `G ≥ 1`), then
`∑_{b∈B} D (b+1) a` is even. -/
lemma key {G : ℕ} (hG : 1 ≤ G) {a : ℤ} (ha : Even a) (hnd : ¬ (2 : ℤ) ^ (G - 1) ∣ a + 2)
    {B : Finset ℕ} (hB : (2 : ℤ) ^ G ∣ S B a) : Even (∑ b ∈ B, D (b + 1) a) := by
  have h2G : (2 : ℤ) ∣ (2 : ℤ) ^ G := dvd_pow_self 2 (by omega)
  have h0 : 0 ∈ B := by
    by_contra h0
    exact (Int.not_even_iff_odd.mpr (S_odd_of_not_mem ha h0)) (even_iff_two_dvd.mpr (h2G.trans hB))
  -- the tail of the sums
  set T := B.filter (fun b => ¬ b < 3) with hT
  have tailP : (a + 2) * (a + 4) ∣ ∑ b ∈ T, P (b + 1) a := by
    apply dvd_sum
    intro b hb
    rw [hT, mem_filter] at hb
    exact P_dvd_big (by omega) a
  have tailD : Even (∑ b ∈ T, D (b + 1) a) := by
    apply Finset.even_sum
    intro b hb
    rw [hT, mem_filter] at hb
    exact D_even ha (b + 1) (by omega)
  obtain ⟨K, hK⟩ := tailP
  have hS : S B a = 1 + (((if 0 ∈ B then P 1 a else 0) + (if 1 ∈ B then P 2 a else 0)
      + (if 2 ∈ B then P 3 a else 0)) + (a + 2) * (a + 4) * K) := by
    unfold S
    rw [sum_split B (fun b => P (b + 1) a)]
    rw [← hT, hK]
  rw [sum_split B (fun b => D (b + 1) a), ← hT]
  apply Even.add _ tailD
  obtain ⟨m, rfl⟩ := ha
  -- `(2:ℤ)^G ∣ (a+2) * w` with `w` odd forces `2^(G-1) ∣ a+2`: contradiction.
  have bad : ∀ w : ℤ, Odd w → ¬ (2 : ℤ) ^ G ∣ (m + m + 2) * w := by
    intro w hw hdiv
    have := (isCoprime_two_pow_of_odd hw G).dvd_of_dvd_mul_right hdiv
    exact hnd (Dvd.dvd.trans (pow_dvd_pow 2 (by omega)) this)
  rw [hS] at hB
  by_cases h1 : 1 ∈ B <;> by_cases h2 : 2 ∈ B <;>
    simp only [h0, h1, h2, ite_true, ite_false, zero_add, Nat.reduceAdd, add_zero] at hB ⊢ <;>
    (try simp only [P_one, P_two, P_three, D_one, D_two, D_three] at hB ⊢)
  · -- B ∩ {0,1,2} = {0,1,2}: S = (a+2)(a^2+5a+5 + (a+4)K)
    exfalso
    apply bad ((m + m) ^ 2 + 5 * (m + m) + 5 + (m + m + 4) * K)
    · exact ⟨2 * m ^ 2 + 5 * m + 2 + (m + 2) * K, by ring⟩
    · convert hB using 1; ring
  · -- {0,1}: D 1 + D 2 = 4m + 4
    exact ⟨2 * m + 2, by ring⟩
  · -- {0,2}: D 1 + D 3 = 12 m^2 + 24 m + 12
    exact ⟨6 * m ^ 2 + 12 * m + 6, by ring⟩
  · -- {0}: S = (a+2)(1 + (a+4)K)
    exfalso
    apply bad (1 + (m + m + 4) * K)
    · exact ⟨(m + 2) * K, by ring⟩
    · convert hB using 1; ring

/-- `S B a` is odd when `a` is odd. -/
lemma S_odd_of_odd {a : ℤ} (ha : Odd a) (B : Finset ℕ) : Odd (S B a) := by
  unfold S
  have : Even (∑ b ∈ B, P (b + 1) a) := by
    apply Finset.even_sum
    intro b _
    have h := P_succ_dvd b a
    obtain ⟨k, rfl⟩ := ha
    exact even_iff_two_dvd.mpr (Dvd.dvd.trans ⟨k + 1, by ring⟩ h)
  rw [add_comm]
  exact this.add_one

lemma S_01 (x : ℤ) : S {0, 1} x = (x + 2) ^ 2 := by
  simp [S, P, prod_range_succ]; ring

/-- Forward direction of the halving lemma. -/
lemma halving_fwd {G : ℕ} (hG : 2 ≤ G) {a : ℤ} (h : ∃ B : Finset ℕ, (2 : ℤ) ^ G ∣ S B a) :
    ∃ B : Finset ℕ, (2 : ℤ) ^ G ∣ S B (a + 2 ^ (G - 1)) := by
  obtain ⟨B, hB⟩ := h
  rcases Int.even_or_odd a with ha | ha
  · by_cases hnd : (2 : ℤ) ^ (G - 1) ∣ a + 2
    · -- near -2: use B = {0,1}, S = (x+2)^2
      refine ⟨{0, 1}, ?_⟩
      rw [S_01]
      have h1 : (2 : ℤ) ^ (G - 1) ∣ a + 2 ^ (G - 1) + 2 := by
        have : a + 2 ^ (G - 1) + 2 = (a + 2) + 2 ^ (G - 1) := by ring
        rw [this]; exact dvd_add hnd dvd_rfl
      have h2 : ((2 : ℤ) ^ (G - 1)) ^ 2 ∣ (a + 2 ^ (G - 1) + 2) ^ 2 := pow_dvd_pow_of_dvd h1 2
      refine Dvd.dvd.trans ?_ h2
      rw [← pow_mul]
      exact pow_dvd_pow 2 (by omega)
    · have hev := key (by omega) ha hnd hB
      refine ⟨B, ?_⟩
      -- S B (a+h) - S B a = ∑ (P(b+1)(a+h) - P(b+1) a) = h * ∑ D + h^2 * (...)
      have hdiff : (2 : ℤ) ^ G ∣ S B (a + 2 ^ (G - 1)) - S B a := by
        have e : S B (a + 2 ^ (G - 1)) - S B a
            = ∑ b ∈ B, (P (b + 1) (a + 2 ^ (G - 1)) - (P (b + 1) a + 2 ^ (G - 1) * D (b + 1) a))
              + 2 ^ (G - 1) * ∑ b ∈ B, D (b + 1) a := by
          simp only [S, mul_sum, ← sum_add_distrib]
          rw [add_sub_add_left_eq_sub, ← sum_sub_distrib]
          refine sum_congr rfl (fun b _ => by ring)
        rw [e]
        apply dvd_add
        · apply dvd_sum
          intro b _
          refine Dvd.dvd.trans ?_ (P_shift (b + 1) a (2 ^ (G - 1)))
          rw [← pow_mul]
          exact pow_dvd_pow 2 (by omega)
        · obtain ⟨k, hk⟩ := hev
          rw [hk]
          have : (2 : ℤ) ^ G = 2 ^ (G - 1) * 2 := by
            rw [← pow_succ]; congr 1; omega
          rw [this]
          exact ⟨k, by ring⟩
      have := dvd_add hdiff hB
      simpa using this
  · exfalso
    have hodd := S_odd_of_odd ha B
    have h2 : (2 : ℤ) ∣ S B a := Dvd.dvd.trans (dvd_pow_self 2 (by omega)) hB
    exact (Int.not_even_iff_odd.mpr hodd) (even_iff_two_dvd.mpr h2)

/-- **Halving lemma (p = 2).** For `G ≥ 2`, whether `2^G ∣ S B a` for some `B` depends only on
`a mod 2^(G-1)`. Equivalently `g(a,2) ≥ G` depends only on `a mod 2^(G-1)`. -/
theorem halving {G : ℕ} (hG : 2 ≤ G) (a : ℤ) :
    (∃ B : Finset ℕ, (2 : ℤ) ^ G ∣ S B a) ↔ (∃ B : Finset ℕ, (2 : ℤ) ^ G ∣ S B (a + 2 ^ (G - 1))) := by
  constructor
  · exact halving_fwd hG
  · intro h
    have h2 := halving_fwd hG h
    have hm : a + 2 ^ (G - 1) + 2 ^ (G - 1) ≡ a [ZMOD 2 ^ G] := by
      have : a + 2 ^ (G - 1) + 2 ^ (G - 1) = a + 2 ^ G := by
        have : (2 : ℤ) ^ G = 2 ^ (G - 1) * 2 := by rw [← pow_succ]; congr 1; omega
        rw [this]; ring
      rw [this]
      exact Int.add_modEq_right
    exact (residue_lemma hm).mp h2

/-! ### The class `a ≡ 4 (mod 8)`: `g(a,2) = 3` exactly -/

lemma S_02 (x : ℤ) : S {0, 2} x = (x + 2) ^ 3 := by
  simp only [S]
  rw [sum_pair (by norm_num)]
  simp only [P_one, P_three, zero_add, Nat.reduceAdd]
  ring

lemma no16_at (x : ℤ) (hx : x = 4 ∨ x = 12) (B : Finset ℕ) : ¬ (16 : ℤ) ∣ S B x := by
  set T := B.filter (fun b => ¬ b < 3) with hT
  have tail : (16 : ℤ) ∣ ∑ b ∈ T, P (b + 1) x := by
    apply dvd_sum
    intro b hb
    rw [hT, mem_filter] at hb
    refine Dvd.dvd.trans ?_ (P_dvd_big (by omega) x)
    rcases hx with rfl | rfl <;> norm_num
  obtain ⟨K, hK⟩ := tail
  unfold S
  rw [sum_split B (fun b => P (b + 1) x), ← hT, hK]
  rcases hx with rfl | rfl <;>
  by_cases h0 : 0 ∈ B <;> by_cases h1 : 1 ∈ B <;> by_cases h2 : 2 ∈ B <;>
    simp only [h0, h1, h2, ite_true, ite_false, zero_add, Nat.reduceAdd, P_one, P_two, P_three] <;>
    norm_num <;> omega

/-- **`g(a,2) = 3` for `a ≡ 4 (mod 8)`**: some `B` gives `8 ∣ S B a` (namely `B = {0,2}`, i.e.
`a! + (a+1)! + (a+3)! = a!(a+2)^3`), and no `B` gives `16 ∣ S B a`. -/
theorem g_eq_three (a : ℤ) (ha : a % 8 = 4) :
    (∃ B : Finset ℕ, (8 : ℤ) ∣ S B a) ∧ ∀ B : Finset ℕ, ¬ (16 : ℤ) ∣ S B a := by
  constructor
  · refine ⟨{0, 2}, ?_⟩
    rw [S_02]
    have : (2 : ℤ) ∣ a + 2 := by omega
    obtain ⟨k, hk⟩ := this
    rw [hk]
    exact ⟨k ^ 3, by ring⟩
  · intro B hB
    have h16 : a ≡ a % 16 [ZMOD 16] := (Int.mod_modEq a 16).symm
    have hB' : (16 : ℤ) ∣ S B (a % 16) := (Int.ModEq.dvd_iff (S_modEq h16 B)).mp hB
    have : a % 16 = 4 ∨ a % 16 = 12 := by omega
    exact no16_at (a % 16) this B hB'

/-! ### Second halving lemma: for `a ≡ 2 (mod 4)`, `g(a) ≥ G` depends only on `a mod 2^(G-3)` -/

lemma sum_split5 (B : Finset ℕ) (F : ℕ → ℤ) :
    ∑ b ∈ B, F b = ((if 0 ∈ B then F 0 else 0) + (if 1 ∈ B then F 1 else 0) + (if 2 ∈ B then F 2 else 0)
      + (if 3 ∈ B then F 3 else 0) + (if 4 ∈ B then F 4 else 0))
      + ∑ b ∈ B.filter (fun b => ¬ b < 5), F b := by
  rw [← sum_filter_add_sum_filter_not B (fun b => b < 5) F]
  congr 1
  have : B.filter (fun b => b < 5) = (range 5).filter (fun b => b ∈ B) := by
    ext b; simp only [mem_filter, mem_range]; tauto
  rw [this, sum_filter]
  simp only [sum_range_succ, sum_range_zero, zero_add]

lemma P_five (x : ℤ) : P 5 x = (x + 1) * (x + 2) * (x + 3) * (x + 4) * (x + 5) := by
  unfold P; simp only [prod_range_succ, prod_range_zero]; push_cast; ring

lemma P_six_dvd {b : ℕ} (hb : 6 ≤ b) (x : ℤ) :
    (x + 1) * (x + 2) * (x + 3) * (x + 4) * (x + 5) * (x + 6) ∣ P b x := by
  have h := P_dvd_P hb x
  have e : P 6 x = (x + 1) * (x + 2) * (x + 3) * (x + 4) * (x + 5) * (x + 6) := by
    unfold P; simp only [prod_range_succ, prod_range_zero]; push_cast; ring
  rw [e] at h; exact h

/-- Shape (i)+(ii) of a witness: `0 ∈ B` and exactly one of `1, 2` lies in `B`. -/
lemma shape12 {G : ℕ} (hG : 1 ≤ G) {a : ℤ} (ha : Even a) (hnd : ¬ (2 : ℤ) ^ (G - 1) ∣ a + 2)
    {B : Finset ℕ} (hB : (2 : ℤ) ^ G ∣ S B a) : 0 ∈ B ∧ (1 ∈ B ↔ 2 ∉ B) := by
  have h2G : (2 : ℤ) ∣ (2 : ℤ) ^ G := dvd_pow_self 2 (by omega)
  have h0 : 0 ∈ B := by
    by_contra h0
    exact (Int.not_even_iff_odd.mpr (S_odd_of_not_mem ha h0)) (even_iff_two_dvd.mpr (h2G.trans hB))
  refine ⟨h0, ?_⟩
  set T := B.filter (fun b => ¬ b < 3) with hT
  have tailP : (a + 2) * (a + 4) ∣ ∑ b ∈ T, P (b + 1) a := by
    apply dvd_sum; intro b hb; rw [hT, mem_filter] at hb; exact P_dvd_big (by omega) a
  obtain ⟨K, hK⟩ := tailP
  have hS : S B a = 1 + (((if 0 ∈ B then P 1 a else 0) + (if 1 ∈ B then P 2 a else 0)
      + (if 2 ∈ B then P 3 a else 0)) + (a + 2) * (a + 4) * K) := by
    unfold S; rw [sum_split B (fun b => P (b + 1) a)]; rw [← hT, hK]
  obtain ⟨m, rfl⟩ := ha
  have bad : ∀ w : ℤ, Odd w → ¬ (2 : ℤ) ^ G ∣ (m + m + 2) * w := by
    intro w hw hdiv
    have := (isCoprime_two_pow_of_odd hw G).dvd_of_dvd_mul_right hdiv
    exact hnd (Dvd.dvd.trans (pow_dvd_pow 2 (by omega)) this)
  rw [hS] at hB
  by_cases h1 : 1 ∈ B <;> by_cases h2 : 2 ∈ B
  · exfalso
    simp only [h0, h1, h2, ite_true, P_one, P_two, P_three] at hB
    apply bad ((m + m) ^ 2 + 5 * (m + m) + 5 + (m + m + 4) * K)
    · exact ⟨2 * m ^ 2 + 5 * m + 2 + (m + 2) * K, by ring⟩
    · convert hB using 1; ring
  · tauto
  · tauto
  · exfalso
    simp only [h0, h1, h2, ite_true, ite_false, P_one, add_zero] at hB
    apply bad (1 + (m + m + 4) * K)
    · exact ⟨(m + 2) * K, by ring⟩
    · convert hB using 1; ring

/-- Shape (iii): for `a ≡ 2 (mod 4)`, a witness contains `3` iff it contains `4`. -/
lemma shape34 {G : ℕ} (hG : 1 ≤ G) {a : ℤ} (ha : a % 4 = 2) (hnd : ¬ (2 : ℤ) ^ (G - 1) ∣ a + 2)
    {B : Finset ℕ} (hB : (2 : ℤ) ^ G ∣ S B a) : (3 ∈ B ↔ 4 ∈ B) := by
  have hev : Even a := ⟨a / 2, by omega⟩
  obtain ⟨h0, h12⟩ := shape12 hG hev hnd hB
  set T := B.filter (fun b => ¬ b < 5) with hT
  have tailP : (a + 1) * (a + 2) * (a + 3) * (a + 4) * (a + 5) * (a + 6) ∣ ∑ b ∈ T, P (b + 1) a := by
    apply dvd_sum; intro b hb; rw [hT, mem_filter] at hb; exact P_six_dvd (by omega) a
  obtain ⟨K, hK⟩ := tailP
  have hS : S B a = 1 + (((if 0 ∈ B then P 1 a else 0) + (if 1 ∈ B then P 2 a else 0)
      + (if 2 ∈ B then P 3 a else 0) + (if 3 ∈ B then P 4 a else 0) + (if 4 ∈ B then P 5 a else 0))
      + (a + 1) * (a + 2) * (a + 3) * (a + 4) * (a + 5) * (a + 6) * K) := by
    unfold S; rw [sum_split5 B (fun b => P (b + 1) a)]; rw [← hT, hK]
  obtain ⟨k, rfl⟩ : ∃ k, a = 4 * k + 2 := ⟨a / 4, by omega⟩
  have bad : ∀ w : ℤ, Odd w → ¬ (2 : ℤ) ^ G ∣ (8 * k + 8) * w := by
    intro w hw hdiv
    have h1 := (isCoprime_two_pow_of_odd hw G).dvd_of_dvd_mul_right hdiv
    apply hnd
    have e : (2 : ℤ) ^ G = 2 ^ (G - 1) * 2 := by rw [← pow_succ]; congr 1; omega
    rw [e] at h1
    obtain ⟨c, hc⟩ := h1
    exact ⟨c, by linarith⟩
  -- odd and even building blocks
  have o1 : Odd (4 * k + 3) := ⟨2 * k + 1, by ring⟩
  have o2 : Odd (4 * k + 5) := ⟨2 * k + 2, by ring⟩
  have o3 : Odd (2 * k + 3) := ⟨k + 1, by ring⟩
  have o4 : Odd (4 * k + 7) := ⟨2 * k + 3, by ring⟩
  have oP : Odd ((4 * k + 3) * (4 * k + 5) * (2 * k + 3)) := (o1.mul o2).mul o3
  have oP5 : Odd ((4 * k + 3) * (4 * k + 5) * (2 * k + 3) * (4 * k + 7)) := oP.mul o4
  have eT : Even ((4 * k + 3) * (4 * k + 5) * (2 * k + 3) * (4 * k + 7) * (4 * k + 8) * K) :=
    ⟨(4 * k + 3) * (4 * k + 5) * (2 * k + 3) * (4 * k + 7) * (2 * k + 4) * K, by ring⟩
  rw [hS] at hB
  by_cases h1 : 1 ∈ B <;> by_cases h3 : 3 ∈ B <;> by_cases h4 : 4 ∈ B
  all_goals first
    | tauto
    | (exfalso
       have h2 : (2 ∈ B ↔ 1 ∉ B) := by tauto
       simp only [h0, h1, h2, h3, h4, ite_true, ite_false, not_true, not_false_eq_true,
         P_one, P_two, P_three, P_four, P_five, add_zero, zero_add] at hB
       first
         | (apply bad ((2 * k + 2) + (4 * k + 3) * (4 * k + 5) * (2 * k + 3)
              + (4 * k + 3) * (4 * k + 5) * (2 * k + 3) * (4 * k + 7) * (4 * k + 8) * K)
            · exact ((Even.add_odd ⟨k + 1, by ring⟩ oP).add_even eT)
            · convert hB using 1; ring)
         | (apply bad ((2 * k + 2) + (4 * k + 3) * (4 * k + 5) * (2 * k + 3) * (4 * k + 7)
              + (4 * k + 3) * (4 * k + 5) * (2 * k + 3) * (4 * k + 7) * (4 * k + 8) * K)
            · exact ((Even.add_odd ⟨k + 1, by ring⟩ oP5).add_even eT)
            · convert hB using 1; ring)
         | (apply bad (8 * (k + 1) ^ 2 + (4 * k + 3) * (4 * k + 5) * (2 * k + 3)
              + (4 * k + 3) * (4 * k + 5) * (2 * k + 3) * (4 * k + 7) * (4 * k + 8) * K)
            · exact ((Even.add_odd ⟨4 * (k + 1) ^ 2, by ring⟩ oP).add_even eT)
            · convert hB using 1; ring)
         | (apply bad (8 * (k + 1) ^ 2 + (4 * k + 3) * (4 * k + 5) * (2 * k + 3) * (4 * k + 7)
              + (4 * k + 3) * (4 * k + 5) * (2 * k + 3) * (4 * k + 7) * (4 * k + 8) * K)
            · exact ((Even.add_odd ⟨4 * (k + 1) ^ 2, by ring⟩ oP5).add_even eT)
            · convert hB using 1; ring))

lemma P_four_dvd8 {a : ℤ} (ha : a % 4 = 2) : (8 : ℤ) ∣ P 4 a := by
  obtain ⟨k, rfl⟩ : ∃ k, a = 4 * k + 2 := ⟨a / 4, by omega⟩
  rw [P_four]; exact ⟨(4 * k + 3) * (k + 1) * (4 * k + 5) * (2 * k + 3), by ring⟩

lemma P_dvd8 {a : ℤ} (ha : a % 4 = 2) {b : ℕ} (hb : 4 ≤ b) : (8 : ℤ) ∣ P b a :=
  (P_four_dvd8 ha).trans (P_dvd_P hb a)

lemma D_five (x : ℤ) : D 5 x = D 4 x * (x + 5) + P 4 x := by
  simp only [D]; push_cast; ring

lemma D_dvd8 {a : ℤ} (ha : a % 4 = 2) : ∀ b : ℕ, 6 ≤ b → (8 : ℤ) ∣ D b a := by
  have hev : Even a := ⟨a / 2, by omega⟩
  intro b hb
  induction b with
  | zero => omega
  | succ b ih =>
    rcases Nat.eq_or_lt_of_le hb with h | h
    · have hb5 : b = 5 := by omega
      subst hb5
      -- D 6 = D 5 * (a+6) + P 5,  D 5 even, 4 ∣ a+6, 8 ∣ P 5
      have e6 : D 6 a = D 5 a * (a + 6) + P 5 a := by simp only [D]; push_cast; ring
      rw [e6]
      have hD5 : Even (D 5 a) := by
        rw [D_five]; exact Even.add (Even.mul_right (D_even hev 4 le_rfl) _) (P_even hev (by norm_num))
      obtain ⟨d, hd⟩ := hD5
      obtain ⟨k, hk⟩ : ∃ k, a = 4 * k + 2 := ⟨a / 4, by omega⟩
      apply dvd_add
      · rw [hd, hk]; exact ⟨d * (k + 2), by ring⟩
      · exact P_dvd8 ha (by norm_num)
    · simp only [D]
      exact dvd_add (Dvd.dvd.mul_right (ih (by omega)) _) (P_dvd8 ha (by omega))

/-- For `a ≡ 2 (mod 4)` and a witness of the shape forced above, `8 ∣ ∑_{b∈B} D (b+1) a`. -/
lemma Dsum8 {a : ℤ} (ha : a % 4 = 2) {B : Finset ℕ} (h0 : 0 ∈ B) (h12 : 1 ∈ B ↔ 2 ∉ B)
    (h34 : 3 ∈ B ↔ 4 ∈ B) : (8 : ℤ) ∣ ∑ b ∈ B, D (b + 1) a := by
  have hev : Even a := ⟨a / 2, by omega⟩
  rw [sum_split5 B (fun b => D (b + 1) a)]
  apply dvd_add
  · have e45 : D 4 a + D 5 a = D 4 a * (a + 6) + P 4 a := by rw [D_five]; ring
    have h45 : (8 : ℤ) ∣ D 4 a + D 5 a := by
      rw [e45]
      obtain ⟨d, hd⟩ := D_even hev 4 le_rfl
      obtain ⟨k, hk⟩ : ∃ k, a = 4 * k + 2 := ⟨a / 4, by omega⟩
      apply dvd_add
      · rw [hd, hk]; exact ⟨d * (k + 2), by ring⟩
      · exact P_four_dvd8 ha
    obtain ⟨k, hk⟩ : ∃ k, a = 4 * k + 2 := ⟨a / 4, by omega⟩
    have h12a : (8 : ℤ) ∣ D 1 a + D 2 a := by rw [D_one, D_two, hk]; exact ⟨k + 1, by ring⟩
    have h13a : (8 : ℤ) ∣ D 1 a + D 3 a := by rw [D_one, D_three, hk]; exact ⟨6 * (k + 1) ^ 2, by ring⟩
    by_cases h1 : 1 ∈ B <;> by_cases h3 : 3 ∈ B
    · have h2 : 2 ∉ B := h12.mp h1
      have h4 : 4 ∈ B := h34.mp h3
      simp only [h0, h1, h2, h3, h4, ite_true, ite_false, zero_add, Nat.reduceAdd, add_zero]
      have := dvd_add h12a h45
      convert this using 1; ring
    · have h2 : 2 ∉ B := h12.mp h1
      have h4 : 4 ∉ B := fun h => h3 (h34.mpr h)
      simp only [h0, h1, h2, h3, h4, ite_true, ite_false, zero_add, Nat.reduceAdd, add_zero]
      exact h12a
    · have h2 : 2 ∈ B := by tauto
      have h4 : 4 ∈ B := h34.mp h3
      simp only [h0, h1, h2, h3, h4, ite_true, ite_false, zero_add, Nat.reduceAdd, add_zero]
      have := dvd_add h13a h45
      convert this using 1; ring
    · have h2 : 2 ∈ B := by tauto
      have h4 : 4 ∉ B := fun h => h3 (h34.mpr h)
      simp only [h0, h1, h2, h3, h4, ite_true, ite_false, zero_add, Nat.reduceAdd, add_zero]
      exact h13a
  · apply dvd_sum
    intro b hb
    rw [mem_filter] at hb
    exact D_dvd8 ha (b + 1) (by omega)

lemma S_02' (x : ℤ) : S {0, 2} x = (x + 2) ^ 3 := S_02 x

/-- Forward direction of the second halving lemma. -/
lemma halving2_fwd {G : ℕ} (hG : 6 ≤ G) {a : ℤ} (ha : a % 4 = 2)
    (h : ∃ B : Finset ℕ, (2 : ℤ) ^ G ∣ S B a) :
    ∃ B : Finset ℕ, (2 : ℤ) ^ G ∣ S B (a + 2 ^ (G - 3)) := by
  obtain ⟨B, hB⟩ := h
  by_cases hnd3 : (2 : ℤ) ^ (G - 3) ∣ a + 2
  · refine ⟨{0, 2}, ?_⟩
    rw [S_02]
    have h1 : (2 : ℤ) ^ (G - 3) ∣ a + 2 ^ (G - 3) + 2 := by
      have : a + 2 ^ (G - 3) + 2 = (a + 2) + 2 ^ (G - 3) := by ring
      rw [this]; exact dvd_add hnd3 dvd_rfl
    refine Dvd.dvd.trans ?_ (pow_dvd_pow_of_dvd h1 3)
    rw [← pow_mul]; exact pow_dvd_pow 2 (by omega)
  · have hnd : ¬ (2 : ℤ) ^ (G - 1) ∣ a + 2 := fun h =>
      hnd3 ((pow_dvd_pow 2 (by omega : G - 3 ≤ G - 1)).trans h)
    have hev : Even a := ⟨a / 2, by omega⟩
    obtain ⟨h0, h12⟩ := shape12 (by omega) hev hnd hB
    have h34 := shape34 (by omega) ha hnd hB
    obtain ⟨q, hq⟩ := Dsum8 ha h0 h12 h34
    refine ⟨B, ?_⟩
    have hdiff : (2 : ℤ) ^ G ∣ S B (a + 2 ^ (G - 3)) - S B a := by
      have e : S B (a + 2 ^ (G - 3)) - S B a
          = ∑ b ∈ B, (P (b + 1) (a + 2 ^ (G - 3)) - (P (b + 1) a + 2 ^ (G - 3) * D (b + 1) a))
            + 2 ^ (G - 3) * ∑ b ∈ B, D (b + 1) a := by
        simp only [S, mul_sum, ← sum_add_distrib]
        rw [add_sub_add_left_eq_sub, ← sum_sub_distrib]
        refine sum_congr rfl (fun b _ => by ring)
      rw [e]
      apply dvd_add
      · apply dvd_sum
        intro b _
        refine Dvd.dvd.trans ?_ (P_shift (b + 1) a (2 ^ (G - 3)))
        rw [← pow_mul]
        exact pow_dvd_pow 2 (by omega)
      · rw [hq]
        have : (2 : ℤ) ^ G = 2 ^ (G - 3) * 8 := by
          rw [show (8 : ℤ) = 2 ^ 3 by norm_num, ← pow_add]; congr 1; omega
        rw [this]
        exact ⟨q, by ring⟩
    have := dvd_add hdiff hB
    simpa using this

/-- **Second halving lemma (p = 2).** For `G ≥ 6` and `a ≡ 2 (mod 4)`,
`g(a,2) ≥ G` depends only on `a mod 2^(G-3)`. -/
theorem halving2 {G : ℕ} (hG : 6 ≤ G) {a : ℤ} (ha : a % 4 = 2) :
    (∃ B : Finset ℕ, (2 : ℤ) ^ G ∣ S B a) ↔ (∃ B : Finset ℕ, (2 : ℤ) ^ G ∣ S B (a + 2 ^ (G - 3))) := by
  have h8 : (2 : ℤ) ^ (G - 3) % 4 = 0 := by
    have : (2 : ℤ) ^ (G - 3) = 4 * 2 ^ (G - 5) := by
      rw [show (4 : ℤ) = 2 ^ 2 by norm_num, ← pow_add]; congr 1; omega
    rw [this]; simp
  constructor
  · exact halving2_fwd hG ha
  · intro h
    -- iterate the forward step 7 more times: a + 8 * 2^(G-3) = a + 2^G ≡ a
    have iter : ∀ n : ℕ, ∃ B : Finset ℕ, (2 : ℤ) ^ G ∣ S B (a + 2 ^ (G - 3) + n * 2 ^ (G - 3)) := by
      intro n
      induction n with
      | zero => simpa using h
      | succ n ih =>
        have hmod : (a + 2 ^ (G - 3) + n * 2 ^ (G - 3)) % 4 = 2 := by
          have : (a + 2 ^ (G - 3) + n * 2 ^ (G - 3)) = a + (n + 1) * 2 ^ (G - 3) := by ring
          rw [this, Int.add_emod, Int.mul_emod, h8]; simp [ha]
        have := halving2_fwd hG hmod ih
        push_cast
        have e : a + 2 ^ (G - 3) + (n + 1) * 2 ^ (G - 3) = a + 2 ^ (G - 3) + n * 2 ^ (G - 3) + 2 ^ (G - 3) := by ring
        rw [e]; exact this
    obtain ⟨B, hB⟩ := iter 7
    have hm : a + 2 ^ (G - 3) + ((7 : ℕ) : ℤ) * 2 ^ (G - 3) ≡ a [ZMOD 2 ^ G] := by
      have : a + 2 ^ (G - 3) + ((7 : ℕ) : ℤ) * 2 ^ (G - 3) = a + 2 ^ G := by
        have e : (2 : ℤ) ^ G = 2 ^ (G - 3) * 8 := by
          rw [show (8 : ℤ) = 2 ^ 3 by norm_num, ← pow_add]; congr 1; omega
        rw [e]; push_cast; ring
      rw [this]; exact Int.add_modEq_right
    exact (residue_lemma hm).mp ⟨B, hB⟩

end E404

#print axioms E404.halving
#print axioms E404.residue_lemma
#print axioms E404.factorial_mul_S
#print axioms E404.g_eq_three
#print axioms E404.halving2
