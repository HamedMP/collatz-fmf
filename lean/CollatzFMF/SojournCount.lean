import CollatzFMF.HarmonicBeta

/-!
# Sojourn count (Theorem S) with a rational base `q < 2`

Source: `notes/round6-nov2026/blind-H/REPORT.md` Theorem A (L1–L5), and
`notes/round6-nov2026/w2-delta/REPORT.md` section (b) Theorem S.

`count x K Y` is the number of indices `k < K` with `x k < Y`.

* `landing` (L2) : `x < 2^(j+1) → T^[j] x < 3^(a+1)`, `a = oddCount j x`.
* `class_card_le` (L4) : the class injection `k ↦ k + j`.
* `sojourn_abstract` : the induction, for abstract rational data `(P, Q, d, ν, κ, A)` with
  `3^Q ≤ 2^P` (so `P/Q ≥ log₂ 3`), Chernoff parameter `λ = ν^P`, and base `q = κ^Q`.
* `sojourn_39_20` : `count x K (2^L) ≤ 9 * (39/20)^L`.
* `sojourn_sharp` : `count x K (2^L) ≤ 10 * (9661/5000)^L`   (`2^0.94996 ≈ 1.93181`).

Everything in this file is complete (no `sorry`, no extra axioms).
-/

namespace CollatzFMF
namespace Sojourn

open KL (T)
open Harmonic

/-- Number of indices `k < K` with `x k < Y`. -/
def count (x : ℕ → ℕ) (K Y : ℕ) : ℕ := ((Finset.range K).filter fun k => x k < Y).card

/-- **L2 (landing bound).** A level-`≤ j` integer lands below `3^(a+1)` after `j` steps. -/
theorem landing (j x : ℕ) (hx : x < 2 ^ (j + 1)) : T^[j] x < 3 ^ (oddCount j x + 1) := by
  obtain ⟨r, h1, h2⟩ := lemma1 j x
  generalize oddCount j x = a at *
  generalize T^[j] x = y at *
  have hr : r < 3 ^ a * 2 ^ j := by
    have h3 : 0 < 2 ^ j * 2 ^ a := by positivity
    have h4 : r ≤ r * 2 ^ a := Nat.le_mul_of_pos_right _ (by positivity)
    omega
  have h5 : 3 ^ a * x < 3 ^ a * 2 ^ (j + 1) := Nat.mul_lt_mul_of_pos_left hx (by positivity)
  have h6 : 2 ^ j * y < 2 ^ j * 3 ^ (a + 1) := by
    rw [pow_succ] at h5
    rw [pow_succ]
    nlinarith
  exact Nat.lt_of_mul_lt_mul_left h6

/-- `⌈P (a+1) / Q⌉`: an exponent `i` with `3^(a+1) ≤ 2^i` when `3^Q ≤ 2^P`. -/
def idx (P Q a : ℕ) : ℕ := (P * (a + 1) + Q - 1) / Q

theorem idx_mul_le (P Q a : ℕ) : Q * idx P Q a ≤ P * (a + 1) + Q - 1 :=
  Nat.mul_div_le _ _

theorem idx_mul_ge (P Q a : ℕ) (hQ : 1 ≤ Q) : P * (a + 1) ≤ Q * idx P Q a := by
  unfold idx
  have h1 := Nat.div_add_mod (P * (a + 1) + Q - 1) Q
  have h2 := Nat.mod_lt (P * (a + 1) + Q - 1) hQ
  omega

theorem three_pow_le (P Q a : ℕ) (hQ : 1 ≤ Q) (hPQ : 3 ^ Q ≤ 2 ^ P) :
    3 ^ (a + 1) ≤ 2 ^ idx P Q a := by
  have h1 : (3 ^ (a + 1)) ^ Q ≤ (2 ^ idx P Q a) ^ Q := by
    calc (3 ^ (a + 1)) ^ Q = (3 ^ Q) ^ (a + 1) := by rw [← pow_mul, ← pow_mul, Nat.mul_comm]
      _ ≤ (2 ^ P) ^ (a + 1) := Nat.pow_le_pow_left hPQ _
      _ = 2 ^ (P * (a + 1)) := by rw [← pow_mul]
      _ ≤ 2 ^ (Q * idx P Q a) := Nat.pow_le_pow_right (by norm_num) (idx_mul_ge P Q a hQ)
      _ = (2 ^ idx P Q a) ^ Q := by rw [← pow_mul, Nat.mul_comm]
  exact (Nat.pow_le_pow_iff_left (by omega)).mp h1

/-- **L4 (class injection).** Indices `k` of level `j`, class `a`, with `k + j < K` inject via
`k ↦ k + j` into indices whose term is below `3^(a+1) ≤ 2^i`. -/
theorem class_card_le (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K j a i : ℕ)
    (hi : 3 ^ (a + 1) ≤ 2 ^ i) :
    ((Finset.range K).filter
        fun k => Nat.log 2 (x k) = j ∧ oddCount j (x k) = a ∧ k + j < K).card
      ≤ count x K (2 ^ i) := by
  unfold count
  apply Finset.card_le_card_of_injOn (fun k => k + j)
  · intro k hk
    simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_range] at hk ⊢
    obtain ⟨-, hlog, ha, hkj⟩ := hk
    refine ⟨hkj, ?_⟩
    rw [seq_iterate hx]
    have h1 : x k < 2 ^ (j + 1) := by
      rw [← hlog]; exact Nat.lt_pow_succ_log_self (by norm_num) _
    have h2 := landing j (x k) h1
    rw [ha] at h2
    omega
  · intro k _ k' _ h
    simpa using h

/-! ### High classes: Chernoff via the Terras generating function -/

/-- Chernoff weight: `≥ 1` exactly on the "high" classes `Q j ≤ P a + d`. -/
noncomputable def w (P Q d : ℕ) (ν : ℝ) (m : ℕ) : ℝ :=
  ν ^ (P * oddCount (Nat.log 2 m) m + d) / ν ^ (Q * Nat.log 2 m)

theorem sum_w_block (P Q d : ℕ) (ν κ : ℝ) (hν : 1 ≤ ν)
    (hch : 1 + ν ^ P ≤ κ ^ Q * ν ^ Q) (j : ℕ) :
    ∑ m ∈ Finset.Ico (2 ^ j) (2 ^ (j + 1)), w P Q d ν m ≤ ν ^ d * (κ ^ Q) ^ j := by
  have hν0 : (0 : ℝ) < ν := lt_of_lt_of_le zero_lt_one hν
  have hcongr : ∀ m ∈ Finset.Ico (2 ^ j) (2 ^ (j + 1)),
      w P Q d ν m = ν ^ d / ν ^ (Q * j) * (ν ^ P) ^ oddCount j m := by
    intro m hm
    obtain ⟨h1, h2⟩ := Finset.mem_Ico.mp hm
    have hlog : Nat.log 2 m = j := Nat.log_eq_of_pow_le_of_lt_pow h1 h2
    unfold w; rw [hlog, pow_add, pow_mul]; ring
  rw [Finset.sum_congr rfl hcongr, ← Finset.mul_sum, sum_pow_oddCount_block]
  have h1 : (1 + ν ^ P) ^ j ≤ (κ ^ Q) ^ j * ν ^ (Q * j) := by
    rw [pow_mul, ← mul_pow]
    exact pow_le_pow_left₀ (by positivity) hch j
  have h2 : (0 : ℝ) < ν ^ (Q * j) := by positivity
  have h3 : (0 : ℝ) ≤ ν ^ d := by positivity
  calc ν ^ d / ν ^ (Q * j) * (1 + ν ^ P) ^ j
      = ν ^ d * ((1 + ν ^ P) ^ j / ν ^ (Q * j)) := by ring
    _ ≤ ν ^ d * (κ ^ Q) ^ j :=
        mul_le_mul_of_nonneg_left ((div_le_iff₀ h2).mpr h1) h3

theorem sum_w_total (P Q d : ℕ) (ν κ : ℝ) (hν : 1 ≤ ν)
    (hch : 1 + ν ^ P ≤ κ ^ Q * ν ^ Q) (L : ℕ) :
    ∑ m ∈ Finset.Ico 1 (2 ^ L), w P Q d ν m
      ≤ ν ^ d * ∑ j ∈ Finset.range L, (κ ^ Q) ^ j := by
  induction L with
  | zero => simp
  | succ L ih =>
    rw [← Finset.sum_Ico_consecutive _ (Nat.one_le_two_pow (n := L))
      (Nat.pow_le_pow_right (by norm_num) (Nat.le_succ L)), Finset.sum_range_succ, mul_add]
    exact add_le_add ih (sum_w_block P Q d ν κ hν hch L)

/-- High part: distinct terms below `2^L` in high classes are few. -/
theorem high_card (P Q d : ℕ) (ν : ℝ) (hν : 1 ≤ ν) (x : ℕ → ℕ) (hpos : ∀ k, 0 < x k) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (L : ℕ) :
    (((Finset.range K).filter fun k => x k < 2 ^ L ∧
        Q * Nat.log 2 (x k) ≤ P * oddCount (Nat.log 2 (x k)) (x k) + d).card : ℝ)
      ≤ ∑ m ∈ Finset.Ico 1 (2 ^ L), w P Q d ν m := by
  set S := (Finset.range K).filter fun k => x k < 2 ^ L ∧
        Q * Nat.log 2 (x k) ≤ P * oddCount (Nat.log 2 (x k)) (x k) + d with hS
  have hν0 : (0 : ℝ) < ν := lt_of_lt_of_le zero_lt_one hν
  have hinjS : Set.InjOn x (S : Set ℕ) := by
    intro i hi j hj hij
    have hi' := Finset.mem_range.mp (Finset.mem_filter.mp hi).1
    have hj' := Finset.mem_range.mp (Finset.mem_filter.mp hj).1
    exact hinj i hi' j hj' hij
  have hcard : S.card = (S.image x).card := (Finset.card_image_of_injOn hinjS).symm
  have hsub : S.image x ⊆ Finset.Ico 1 (2 ^ L) := by
    intro m hm
    obtain ⟨k, hk, rfl⟩ := Finset.mem_image.mp hm
    exact Finset.mem_Ico.mpr ⟨hpos k, (Finset.mem_filter.mp hk).2.1⟩
  have hwnn : ∀ m, 0 ≤ w P Q d ν m := fun m => by unfold w; positivity
  calc (S.card : ℝ) = ∑ _m ∈ S.image x, (1 : ℝ) := by rw [hcard]; simp
    _ ≤ ∑ m ∈ S.image x, w P Q d ν m := by
        apply Finset.sum_le_sum
        intro m hm
        obtain ⟨k, hk, rfl⟩ := Finset.mem_image.mp hm
        have hh := (Finset.mem_filter.mp hk).2.2
        unfold w
        rw [one_le_div (by positivity)]
        exact pow_le_pow_right₀ hν hh
    _ ≤ ∑ m ∈ Finset.Ico 1 (2 ^ L), w P Q d ν m :=
        Finset.sum_le_sum_of_subset_of_nonneg hsub fun m _ _ => hwnn m

/-! ### Low classes: geometric sum of the induction hypothesis -/

/-- The constant multiplying `A * q^j` in the low part. -/
noncomputable def G (P Q d : ℕ) (κ : ℝ) : ℝ :=
  κ ^ (P + Q - 1) * κ ^ P / ((κ ^ P - 1) * κ ^ (d + 1))

theorem G_nonneg (P Q d : ℕ) (κ : ℝ) (hκ : 1 < κ) (hP : 1 ≤ P) : 0 ≤ G P Q d κ := by
  have h1 : (1 : ℝ) < κ ^ P := one_lt_pow₀ hκ (by omega)
  have h2 : (0 : ℝ) < κ ^ P - 1 := by linarith
  have h0 : (0 : ℝ) < κ := by linarith
  unfold G; positivity

theorem geom_filter (P Q d : ℕ) (κ : ℝ) (hκ : 1 < κ) (hP : 1 ≤ P) (n M : ℕ) :
    ∑ a ∈ (Finset.range n).filter (fun a => P * a + d < M), κ ^ (Q * idx P Q a)
      ≤ G P Q d κ * κ ^ M := by
  have h0 : (0 : ℝ) < κ := by linarith
  have hρ1 : (1 : ℝ) < κ ^ P := one_lt_pow₀ hκ (by omega)
  have hr : (0 : ℝ) < κ ^ P - 1 := by linarith
  set F := (Finset.range n).filter (fun a => P * a + d < M) with hF
  rcases F.eq_empty_or_nonempty with he | hne
  · rw [he, Finset.sum_empty]
    exact mul_nonneg (G_nonneg P Q d κ hκ hP) (by positivity)
  set m := F.max' hne with hm
  have hmF : P * m + d < M := (Finset.mem_filter.mp (F.max'_mem hne)).2
  have hgeom : (∑ a ∈ Finset.range (m + 1), (κ ^ P) ^ a) * (κ ^ P - 1) = (κ ^ P) ^ (m + 1) - 1 :=
    geom_sum_mul _ _
  have hgeom' : ∑ a ∈ Finset.range (m + 1), (κ ^ P) ^ a ≤ (κ ^ P) ^ (m + 1) / (κ ^ P - 1) := by
    rw [le_div_iff₀ hr, hgeom]; linarith
  have hED : κ ^ (P * m) * κ ^ (d + 1) ≤ κ ^ M := by
    rw [← pow_add]; exact pow_le_pow_right₀ hκ.le (by omega)
  calc ∑ a ∈ F, κ ^ (Q * idx P Q a)
      ≤ ∑ a ∈ F, κ ^ (P + Q - 1) * (κ ^ P) ^ a := by
        apply Finset.sum_le_sum
        intro a _
        rw [← pow_mul, ← pow_add]
        apply pow_le_pow_right₀ hκ.le
        have h1 := idx_mul_le P Q a
        have h2 : P * (a + 1) = P * a + P := by ring
        omega
    _ ≤ ∑ a ∈ Finset.range (m + 1), κ ^ (P + Q - 1) * (κ ^ P) ^ a := by
        apply Finset.sum_le_sum_of_subset_of_nonneg
        · intro a ha
          exact Finset.mem_range.mpr (Nat.lt_succ_of_le (F.le_max' a ha))
        · intro a _ _; positivity
    _ = κ ^ (P + Q - 1) * ∑ a ∈ Finset.range (m + 1), (κ ^ P) ^ a := by rw [Finset.mul_sum]
    _ ≤ κ ^ (P + Q - 1) * ((κ ^ P) ^ (m + 1) / (κ ^ P - 1)) :=
        mul_le_mul_of_nonneg_left hgeom' (by positivity)
    _ = G P Q d κ * (κ ^ (P * m) * κ ^ (d + 1)) := by
        unfold G
        rw [pow_succ, ← pow_mul]
        field_simp
    _ ≤ G P Q d κ * κ ^ M := mul_le_mul_of_nonneg_left hED (G_nonneg P Q d κ hκ hP)

/-- Low part at a fixed level `j`, given the induction hypothesis at the landing scales. -/
theorem low_level (P Q d : ℕ) (κ A : ℝ) (hκ : 1 < κ) (hP : 1 ≤ P) (hQ : 1 ≤ Q)
    (hPQ : 3 ^ Q ≤ 2 ^ P) (hA : 0 ≤ A)
    (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K j : ℕ)
    (hIH : ∀ a, P * a + d < Q * j →
      (count x K (2 ^ idx P Q a) : ℝ) ≤ A * κ ^ (Q * idx P Q a)) :
    (((Finset.range K).filter fun k => Nat.log 2 (x k) = j ∧
        P * oddCount j (x k) + d < Q * j ∧ k + j < K).card : ℝ)
      ≤ A * G P Q d κ * (κ ^ Q) ^ j := by
  set F := (Finset.range K).filter fun k => Nat.log 2 (x k) = j ∧
        P * oddCount j (x k) + d < Q * j ∧ k + j < K with hF
  have hfib := Finset.card_eq_sum_card_fiberwise (s := F) (t := Finset.range (j + 1))
    (f := fun k => oddCount j (x k))
    (fun k _ => Finset.mem_range.mpr (Nat.lt_succ_of_le (oddCount_le j (x k))))
  have hterm : ∀ a ∈ Finset.range (j + 1),
      (((F.filter fun k => oddCount j (x k) = a).card : ℕ) : ℝ)
        ≤ if P * a + d < Q * j then A * κ ^ (Q * idx P Q a) else 0 := by
    intro a _
    split_ifs with hlow
    · refine le_trans ?_ (hIH a hlow)
      have hsub : (F.filter fun k => oddCount j (x k) = a) ⊆
          (Finset.range K).filter
            fun k => Nat.log 2 (x k) = j ∧ oddCount j (x k) = a ∧ k + j < K := by
        intro k hk
        obtain ⟨hk1, hk2⟩ := Finset.mem_filter.mp hk
        obtain ⟨hk3, hk4, -, hk6⟩ := Finset.mem_filter.mp hk1
        exact Finset.mem_filter.mpr ⟨hk3, hk4, hk2, hk6⟩
      exact_mod_cast (Finset.card_le_card hsub).trans
        (class_card_le x hx K j a _ (three_pow_le P Q a hQ hPQ))
    · have hempty : (F.filter fun k => oddCount j (x k) = a) = ∅ := by
        apply Finset.filter_eq_empty_iff.mpr
        intro k hk hka
        obtain ⟨-, -, hk5, -⟩ := Finset.mem_filter.mp hk
        rw [hka] at hk5
        exact hlow hk5
      rw [hempty]; simp
  calc (F.card : ℝ)
      = ∑ a ∈ Finset.range (j + 1), (((F.filter fun k => oddCount j (x k) = a).card : ℕ) : ℝ) := by
        rw [hfib]; push_cast; rfl
    _ ≤ ∑ a ∈ Finset.range (j + 1),
          (if P * a + d < Q * j then A * κ ^ (Q * idx P Q a) else 0) :=
        Finset.sum_le_sum hterm
    _ = A * ∑ a ∈ (Finset.range (j + 1)).filter (fun a => P * a + d < Q * j),
          κ ^ (Q * idx P Q a) := by
        rw [Finset.mul_sum, Finset.sum_filter]
    _ ≤ A * (G P Q d κ * κ ^ (Q * j)) :=
        mul_le_mul_of_nonneg_left (geom_filter P Q d κ hκ hP _ _) hA
    _ = A * G P Q d κ * (κ ^ Q) ^ j := by rw [pow_mul]; ring

/-! ### The induction -/

/-- **Sojourn count, abstract rational form.** Data: naturals `P, Q, d` with `3^Q ≤ 2^P`,
`P ≤ d + 1`; reals `ν ≥ 1`, `κ > 1`, `A ≥ 0` with the Chernoff condition
`1 + ν^P ≤ κ^Q ν^Q` and the closing condition `1 + ν^d + A G ≤ A (κ^Q - 1)`.
Then every `T`-sequence with `x 0 ≥ 1` whose first `K` terms are pairwise distinct has at most
`A (κ^Q)^L` indices `k < K` with `x k < 2^L`. -/
theorem sojourn_abstract (P Q d : ℕ) (ν κ A : ℝ) (hQ : 1 ≤ Q) (hPQ : 3 ^ Q ≤ 2 ^ P)
    (hd : P ≤ d + 1) (hν : 1 ≤ ν) (hκ : 1 < κ) (hA0 : 0 ≤ A)
    (hch : 1 + ν ^ P ≤ κ ^ Q * ν ^ Q)
    (hA : 1 + ν ^ d + A * G P Q d κ ≤ A * (κ ^ Q - 1))
    (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (hx0 : 1 ≤ x 0) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (L : ℕ) :
    (count x K (2 ^ L) : ℝ) ≤ A * (κ ^ Q) ^ L := by
  have hP : 1 ≤ P := by
    by_contra h
    have hP0 : P = 0 := by omega
    subst hP0
    have : 3 ^ 1 ≤ 3 ^ Q := Nat.pow_le_pow_right (by norm_num) hQ
    omega
  have hpos : ∀ k, 0 < x k := fun k => by
    have := iterate_pos (x := x 0) (by omega) k
    rwa [← seq_iterate hx, Nat.zero_add] at this
  have hq1 : (1 : ℝ) < κ ^ Q := one_lt_pow₀ hκ (by omega)
  induction L using Nat.strong_induction_on with
  | _ L IH =>
  set q := κ ^ Q with hq
  set g := ∑ j ∈ Finset.range L, q ^ j with hg
  have hgq : g * (q - 1) = q ^ L - 1 := geom_sum_mul _ _
  have hLg : (L : ℝ) ≤ g := by
    have : ∑ _j ∈ Finset.range L, (1 : ℝ) ≤ g :=
      Finset.sum_le_sum fun j _ => one_le_pow₀ hq1.le
    simpa using this
  -- the three parts
  set SH := (Finset.range K).filter fun k => x k < 2 ^ L ∧
    Q * Nat.log 2 (x k) ≤ P * oddCount (Nat.log 2 (x k)) (x k) + d with hSH
  set SL := (Finset.range K).filter fun k => x k < 2 ^ L ∧
    P * oddCount (Nat.log 2 (x k)) (x k) + d < Q * Nat.log 2 (x k) ∧
    k + Nat.log 2 (x k) < K with hSL
  set SE := (Finset.range K).filter fun k => x k < 2 ^ L ∧ ¬ k + Nat.log 2 (x k) < K with hSE
  have hloglt : ∀ k, x k < 2 ^ L → Nat.log 2 (x k) < L := fun k hk =>
    Nat.log_lt_of_lt_pow (hpos k).ne' hk
  have hcover : ((Finset.range K).filter fun k => x k < 2 ^ L) ⊆ SH ∪ SL ∪ SE := by
    intro k hk
    obtain ⟨hk1, hk2⟩ := Finset.mem_filter.mp hk
    simp only [Finset.mem_union, hSH, hSL, hSE, Finset.mem_filter]
    by_cases h1 : Q * Nat.log 2 (x k) ≤ P * oddCount (Nat.log 2 (x k)) (x k) + d
    · exact Or.inl (Or.inl ⟨hk1, hk2, h1⟩)
    · by_cases h2 : k + Nat.log 2 (x k) < K
      · exact Or.inl (Or.inr ⟨hk1, hk2, by omega, h2⟩)
      · exact Or.inr ⟨hk1, hk2, h2⟩
  have hcount : count x K (2 ^ L) ≤ SH.card + SL.card + SE.card := by
    unfold count
    exact (Finset.card_le_card hcover).trans
      ((Finset.card_union_le _ _).trans (Nat.add_le_add_right (Finset.card_union_le _ _) _))
  -- end terms
  have hE : SE.card ≤ L := by
    have hsub : SE ⊆ Finset.Ico (K - L) K := by
      intro k hk
      obtain ⟨hk1, hk2, hk3⟩ := Finset.mem_filter.mp hk
      have := hloglt k hk2
      have := Finset.mem_range.mp hk1
      exact Finset.mem_Ico.mpr ⟨by omega, by omega⟩
    have := Finset.card_le_card hsub
    rw [Nat.card_Ico] at this
    omega
  -- high terms
  have hH : (SH.card : ℝ) ≤ ν ^ d * g :=
    (high_card P Q d ν hν x hpos K hinj L).trans (sum_w_total P Q d ν κ hν hch L)
  -- low terms
  have hL : (SL.card : ℝ) ≤ A * G P Q d κ * g := by
    have hfib := Finset.card_eq_sum_card_fiberwise (s := SL) (t := Finset.range L)
      (f := fun k => Nat.log 2 (x k))
      (fun k hk => Finset.mem_range.mpr (hloglt k (Finset.mem_filter.mp hk).2.1))
    rw [hfib, hg, Finset.mul_sum]
    push_cast
    apply Finset.sum_le_sum
    intro j hj
    have hjL := Finset.mem_range.mp hj
    have hsub : (SL.filter fun k => Nat.log 2 (x k) = j) ⊆
        (Finset.range K).filter fun k => Nat.log 2 (x k) = j ∧
          P * oddCount j (x k) + d < Q * j ∧ k + j < K := by
      intro k hk
      obtain ⟨hk1, hk2⟩ := Finset.mem_filter.mp hk
      obtain ⟨hk3, -, hk5, hk6⟩ := Finset.mem_filter.mp hk1
      rw [hk2] at hk5 hk6
      exact Finset.mem_filter.mpr ⟨hk3, hk2, hk5, hk6⟩
    refine le_trans (Nat.cast_le.mpr (Finset.card_le_card hsub)) ?_
    apply low_level P Q d κ A hκ hP hQ hPQ hA0 x hx K j
    intro a ha
    have hidx : idx P Q a < L := by
      have h1 := idx_mul_le P Q a
      have h2 : P * (a + 1) = P * a + P := by ring
      have h3 : Q * idx P Q a < Q * (j + 1) := by
        have : Q * (j + 1) = Q * j + Q := by ring
        omega
      have := Nat.lt_of_mul_lt_mul_left h3
      omega
    have := IH (idx P Q a) hidx
    rwa [hq, ← pow_mul] at this
  -- assemble
  have hG := G_nonneg P Q d κ hκ hP
  have hcountR : (count x K (2 ^ L) : ℝ) ≤ (SH.card : ℝ) + (SL.card : ℝ) + (SE.card : ℝ) := by
    exact_mod_cast hcount
  have hER : (SE.card : ℝ) ≤ g := le_trans (by exact_mod_cast hE) hLg
  have hg0 : 0 ≤ g := le_trans (Nat.cast_nonneg L) hLg
  have h1 : (count x K (2 ^ L) : ℝ) ≤ (1 + ν ^ d + A * G P Q d κ) * g := by nlinarith
  have h2 : (1 + ν ^ d + A * G P Q d κ) * g ≤ A * (q - 1) * g :=
    mul_le_mul_of_nonneg_right hA hg0
  have h3 : A * (q - 1) * g = A * (q ^ L - 1) := by rw [← hgq]; ring
  have h4 : A * (q ^ L - 1) ≤ A * q ^ L := by nlinarith
  linarith

/-! ### Instances -/

/-- **Sojourn count, base `39/20`.** (`P/Q = 8/5`, `ν = 16/15`, `κ = 8/7`, `d = 24`.)
On any distinct stretch of a `T`-trajectory started at `x 0 ≥ 1`, at most `9 * (39/20)^L`
indices have a term below `2^L`. -/
theorem sojourn_39_20 (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (hx0 : 1 ≤ x 0) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (L : ℕ) :
    (count x K (2 ^ L) : ℝ) ≤ 9 * (39 / 20 : ℝ) ^ L := by
  have h := sojourn_abstract 8 5 24 (16 / 15) (8 / 7) 9 (by norm_num) (by norm_num)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    (by unfold G; norm_num) x hx hx0 K hinj L
  refine h.trans (mul_le_mul_of_nonneg_left ?_ (by norm_num))
  exact pow_le_pow_left₀ (by norm_num) (by norm_num) L

/-- **Sojourn count, base `1.9322`.** (`P/Q = 65/41`, `ν = 126/125`, `κ = 251/247`,
`d = 211`.) At most `10 * 1.9322^L` indices of a distinct stretch have a term below `2^L`.
The true exponent base of Theorem S is `2^0.949956 ≈ 1.93181`; the best base this
parametrization can reach with `P/Q = 65/41` is `≈ 1.93197`. -/
theorem sojourn_sharp (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (hx0 : 1 ≤ x 0) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (L : ℕ) :
    (count x K (2 ^ L) : ℝ) ≤ 10 * (9661 / 5000 : ℝ) ^ L := by
  have h := sojourn_abstract 65 41 211 (126 / 125) (251 / 247) 10 (by norm_num) (by norm_num)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    (by unfold G; norm_num) x hx hx0 K hinj L
  refine h.trans (mul_le_mul_of_nonneg_left ?_ (by norm_num))
  exact pow_le_pow_left₀ (by norm_num) (by norm_num) L

/-! ### Guards -/

/-- Guard: `count` on the trajectory of 27 (cross-checked in Python): among the first 71
terms (`27, 41, …, 2, 1`, pairwise distinct), exactly 10 are below `2^5`. -/
example : count (fun k => T^[k] 27) 71 (2 ^ 5) = 10 := by decide

/-- Guard: the hypotheses are satisfiable — the theorem applies to the first 71 terms of the
trajectory of 27. (At `L = 5` the bound reads `10 ≤ 10 * 1.9322^5 ≈ 269`: true, but weaker
than the trivial bound `2^5 - 1`; see the next guard.) -/
example : ((10 : ℕ) : ℝ) ≤ 10 * (9661 / 5000 : ℝ) ^ 5 := by
  have hinj : ∀ i < 71, ∀ j < 71, T^[i] 27 = T^[j] 27 → i = j := by decide
  have h := sojourn_sharp (fun k => T^[k] 27) (fun k => Function.iterate_succ_apply' T k 27)
    (by decide) 71 hinj 5
  have hc : count (fun k => T^[k] 27) 71 (2 ^ 5) = 10 := by decide
  rwa [hc] at h

/-- Guard (non-vacuity): the bound beats the trivial count `2^L - 1` of all positive integers
below `2^L` from `L = 67` on, and by a factor `> 3` at `L = 100`; it is weaker than the
trivial bound for `L ≤ 66`. -/
example : 10 * (9661 / 5000 : ℝ) ^ 67 < 2 ^ 67 - 1 := by norm_num
example : 3 * (10 * (9661 / 5000 : ℝ) ^ 100) < 2 ^ 100 - 1 := by norm_num
example : (2 : ℝ) ^ 66 - 1 < 10 * (9661 / 5000 : ℝ) ^ 66 := by norm_num

end Sojourn
end CollatzFMF
