import CollatzFMF.ConstH

/-!
# Theorem H with constant 27.93: reciprocal sums of distinct integers in a block

Source: `notes/round6-nov2026/w2-delta/REPORT.md` section (b): the bad mass uses, per level,
`min(b_L/2^L, 2^(-L) + ln(1 + b_L/2^L))` (a bound for the reciprocal sum of `b_L` distinct
integers of `[2^L, 2^(L+1))`). Here the logarithm is replaced by a rational step function with
eight steps: on `[8c, 16c)` one has `1/n ≤ 1/((8+i)c)` for `(8+i)c ≤ n`.

* `inv_le_chunkH` : `1/n ≤ chunkH c n` on `[8c, 16c)`.
* `chunk_block` : `b` distinct integers of `[8c, 16c)` have reciprocal sum
  `≤ chunkNum c b / (360360 c)`.
* `exact_mass_chunk_run` : bad integers of levels `m+3, …, m+f+2`: kernel-evaluable bound.
* `theoremH_2793` : every distinct stretch has harmonic sum `≤ 27.93` (refereed: `27.163`).

Everything in this file is complete (no `sorry`, no extra axioms, no `native_decide`).
-/

namespace CollatzFMF
namespace Const

open KL (T)
open Harmonic

/-- `1/((8+j)c)`: the value of the step function on `[(8+j)c, (9+j)c)`. -/
noncomputable def chunkVal (c j : ℕ) : ℝ := 1 / (((8 : ℝ) + j) * c)

/-- The step function dominating `1/n` on `[8c, 16c)`, written as a sum of indicators. -/
noncomputable def chunkH (c n : ℕ) : ℝ :=
  chunkVal c 7
    + ∑ j ∈ Finset.range 7, if n < (9 + j) * c then chunkVal c j - chunkVal c (j + 1) else 0

theorem chunkVal_step_nonneg (c j : ℕ) (hc : 0 < c) : 0 ≤ chunkVal c j - chunkVal c (j + 1) := by
  have hc' : (0 : ℝ) < c := by exact_mod_cast hc
  have hj : (0 : ℝ) ≤ j := Nat.cast_nonneg j
  unfold chunkVal
  rw [sub_nonneg]
  apply one_div_le_one_div_of_le (by positivity)
  push_cast
  nlinarith

theorem sum_Ico_telescope (g : ℕ → ℝ) (i : ℕ) : ∀ m,
    ∑ j ∈ Finset.Ico i (i + m), (g j - g (j + 1)) = g i - g (i + m) := by
  intro m
  induction m with
  | zero => simp
  | succ m ih =>
    rw [show i + (m + 1) = i + m + 1 by omega, Finset.sum_Ico_succ_top (Nat.le_add_right i m), ih]
    ring

theorem inv_le_chunkH (c n : ℕ) (hc : 0 < c) (h1 : 8 * c ≤ n) (h2 : n < 16 * c) :
    1 / (n : ℝ) ≤ chunkH c n := by
  have hc' : (0 : ℝ) < c := by exact_mod_cast hc
  obtain ⟨i, hi7, hlo, hhi⟩ : ∃ i, i ≤ 7 ∧ (8 + i) * c ≤ n ∧ n < (9 + i) * c := by
    have hq1 : 8 ≤ n / c := (Nat.le_div_iff_mul_le hc).mpr h1
    have hq2 : n / c < 16 := (Nat.div_lt_iff_lt_mul hc).mpr h2
    refine ⟨n / c - 8, by omega, ?_, ?_⟩
    · rw [show 8 + (n / c - 8) = n / c by omega]
      exact Nat.div_mul_le_self n c
    · rw [show 9 + (n / c - 8) = n / c + 1 by omega, Nat.mul_comm]
      exact Nat.lt_mul_div_succ n hc
  have hstep : chunkVal c i - chunkVal c 7
      ≤ ∑ j ∈ Finset.range 7,
          if n < (9 + j) * c then chunkVal c j - chunkVal c (j + 1) else 0 := by
    have ht := sum_Ico_telescope (chunkVal c) i (7 - i)
    rw [show i + (7 - i) = 7 by omega] at ht
    rw [← ht]
    calc ∑ j ∈ Finset.Ico i 7, (chunkVal c j - chunkVal c (j + 1))
        = ∑ j ∈ Finset.Ico i 7,
            if n < (9 + j) * c then chunkVal c j - chunkVal c (j + 1) else 0 := by
          refine Finset.sum_congr rfl fun j hj => ?_
          have hij := (Finset.mem_Ico.mp hj).1
          have hle : (9 + i) * c ≤ (9 + j) * c := Nat.mul_le_mul_right c (by omega)
          rw [if_pos (lt_of_lt_of_le hhi hle)]
      _ ≤ _ := by
          apply Finset.sum_le_sum_of_subset_of_nonneg
          · intro j hj
            exact Finset.mem_range.mpr (Finset.mem_Ico.mp hj).2
          · intro j _ _
            split
            · exact chunkVal_step_nonneg c j hc
            · exact le_refl _
  have hn : 1 / (n : ℝ) ≤ chunkVal c i := by
    unfold chunkVal
    apply one_div_le_one_div_of_le (by positivity)
    have : (((8 + i) * c : ℕ) : ℝ) ≤ (n : ℝ) := by exact_mod_cast hlo
    push_cast at this
    exact this
  unfold chunkH
  linarith

/-- Integer numerator of the eight-step bound (common denominator `360360 = lcm(8..15)`). -/
def chunkNum (c b : ℕ) : ℕ :=
  24024 * b + 5005 * min b c + 4004 * min b (2 * c) + 3276 * min b (3 * c)
    + 2730 * min b (4 * c) + 2310 * min b (5 * c) + 1980 * min b (6 * c) + 1716 * min b (7 * c)

/-- **Reciprocal sum of at most `b` distinct integers of `[8c, 16c)`.** -/
theorem chunk_block (c b : ℕ) (hc : 0 < c) (S : Finset ℕ) (hS : ∀ n ∈ S, 8 * c ≤ n ∧ n < 16 * c)
    (hb : S.card ≤ b) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ (chunkNum c b : ℝ) / (360360 * c) := by
  have hc' : (0 : ℝ) < c := by exact_mod_cast hc
  have hv7 : (0 : ℝ) ≤ chunkVal c 7 := by unfold chunkVal; positivity
  have hcardj : ∀ j, (((S.filter (fun n => n < (9 + j) * c)).card : ℕ) : ℝ)
      ≤ ((min b ((j + 1) * c) : ℕ) : ℝ) := by
    intro j
    have h1 : (S.filter (fun n => n < (9 + j) * c)).card ≤ b :=
      (Finset.card_le_card (Finset.filter_subset _ _)).trans hb
    have h2 : (S.filter (fun n => n < (9 + j) * c)).card ≤ (j + 1) * c := by
      have hsub : S.filter (fun n => n < (9 + j) * c) ⊆ Finset.Ico (8 * c) ((9 + j) * c) := by
        intro n hn
        obtain ⟨a1, a2⟩ := Finset.mem_filter.mp hn
        exact Finset.mem_Ico.mpr ⟨(hS n a1).1, a2⟩
      have h3 := Finset.card_le_card hsub
      rw [Nat.card_Ico, ← Nat.sub_mul, show 9 + j - 8 = j + 1 by omega] at h3
      exact h3
    exact_mod_cast le_min h1 h2
  calc ∑ n ∈ S, (1 / (n : ℝ)) ≤ ∑ n ∈ S, chunkH c n :=
        Finset.sum_le_sum fun n hn => inv_le_chunkH c n hc (hS n hn).1 (hS n hn).2
    _ = (S.card : ℝ) * chunkVal c 7
          + ∑ j ∈ Finset.range 7, ((S.filter (fun n => n < (9 + j) * c)).card : ℝ)
              * (chunkVal c j - chunkVal c (j + 1)) := by
        unfold chunkH
        rw [Finset.sum_add_distrib, Finset.sum_const, nsmul_eq_mul, Finset.sum_comm]
        congr 1
        refine Finset.sum_congr rfl fun j _ => ?_
        rw [Finset.sum_ite, Finset.sum_const, Finset.sum_const_zero, add_zero, nsmul_eq_mul]
    _ ≤ (b : ℝ) * chunkVal c 7
          + ∑ j ∈ Finset.range 7, ((min b ((j + 1) * c) : ℕ) : ℝ)
              * (chunkVal c j - chunkVal c (j + 1)) := by
        apply add_le_add
        · apply mul_le_mul_of_nonneg_right _ hv7
          exact_mod_cast hb
        · apply Finset.sum_le_sum
          intro j _
          exact mul_le_mul_of_nonneg_right (hcardj j) (chunkVal_step_nonneg c j hc)
    _ = (chunkNum c b : ℝ) / (360360 * c) := by
        simp only [Finset.sum_range_succ, Finset.sum_range_zero, chunkVal, chunkNum]
        push_cast
        field_simp
        ring

/-- Guard: the bound is attained up to the step approximation: for `c = 1`, `b = 8` the true
maximum is `1/8 + … + 1/15 = 0.7254`, and the bound is exactly that (each step is one integer);
for `b = 1` it is `1/8`. -/
example : (chunkNum 1 8 : ℚ) / 360360 = 1/8 + 1/9 + 1/10 + 1/11 + 1/12 + 1/13 + 1/14 + 1/15 := by
  norm_num [chunkNum]
example : (chunkNum 1 1 : ℚ) / 360360 = 1 / 8 := by norm_num [chunkNum]

/-- Bad integers of level `l + 3`: eight-step bound with `b = b_{l+3}`. -/
theorem block_mass_chunk (s l : ℕ) (S : Finset ℕ)
    (hS : ∀ n ∈ S, 2 ^ (l + 3) ≤ n ∧ n < 2 ^ (l + 3 + 1) ∧ ¬ Good s n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ (chunkNum (2 ^ l) (bcount s (l + 3)) : ℝ) / (360360 * 2 ^ l) := by
  have hsub : S ⊆ (Finset.Ico (2 ^ (l + 3)) (2 ^ (l + 3 + 1))).filter (fun n => ¬ Good s n) := by
    intro n hn
    obtain ⟨a1, a2, a3⟩ := hS n hn
    exact Finset.mem_filter.mpr ⟨Finset.mem_Ico.mpr ⟨a1, a2⟩, a3⟩
  have hcard : S.card ≤ bcount s (l + 3) := by
    rw [← card_bad_block]; exact Finset.card_le_card hsub
  have h := chunk_block (2 ^ l) (bcount s (l + 3)) (by positivity) S (by
    intro n hn
    obtain ⟨a1, a2, -⟩ := hS n hn
    have e1 : 2 ^ (l + 3) = 8 * 2 ^ l := by rw [pow_add]; ring
    have e2 : 2 ^ (l + 3 + 1) = 16 * 2 ^ l := by rw [pow_add, pow_add]; ring
    rw [e1] at a1
    rw [e2] at a2
    exact ⟨a1, a2⟩) hcard
  simpa using h

/-- Bad integers of the levels `m+3, …, m+f+2`: sum of the eight-step bounds. -/
theorem exact_mass_chunk (s m : ℕ) : ∀ (f : ℕ) (S : Finset ℕ),
    (∀ n ∈ S, 2 ^ (m + 3) ≤ n ∧ n < 2 ^ (m + f + 3) ∧ ¬ Good s n) →
    ∑ n ∈ S, (1 / (n : ℝ))
      ≤ ∑ i ∈ Finset.range f,
          (chunkNum (2 ^ (m + i)) (bcount s (m + i + 3)) : ℝ) / (360360 * 2 ^ (m + i)) := by
  intro f
  induction f with
  | zero =>
    intro S hS
    have : S = ∅ := by
      apply Finset.eq_empty_of_forall_notMem
      intro n hn
      obtain ⟨a1, a2, -⟩ := hS n hn
      rw [Nat.add_zero] at a2
      omega
    rw [this]; simp
  | succ f ih =>
    intro S hS
    rw [Finset.sum_range_succ,
      ← Finset.sum_filter_add_sum_filter_not S (fun n => n < 2 ^ (m + f + 3))]
    apply add_le_add
    · apply ih
      intro n hn
      obtain ⟨h1, h2⟩ := Finset.mem_filter.mp hn
      exact ⟨(hS n h1).1, h2, (hS n h1).2.2⟩
    · apply block_mass_chunk
      intro n hn
      obtain ⟨h1, h2⟩ := Finset.mem_filter.mp hn
      exact ⟨not_lt.mp h2, (hS n h1).2.1, (hS n h1).2.2⟩

/-- `runC s f l (prow (l+3)) A = 2^f A + 2^(l+f) Σ_{i<f} chunkNum(2^(l+i), b_{l+i+3}) / 2^(l+i+1)`. -/
def runC (s : ℕ) : ℕ → ℕ → List ℕ → ℕ → ℕ
  | 0, _, _, A => A
  | f + 1, l, r, A =>
      runC s f (l + 1) (pnext 0 r) (2 * A + chunkNum (2 ^ l) (bsum s (l + 3) 0 r))

theorem runC_spec (s : ℕ) : ∀ f l A,
    (runC s f l (prow (l + 3)) A : ℝ)
      = 2 ^ f * (A : ℝ)
        + 2 ^ (l + f) * ∑ i ∈ Finset.range f,
            (chunkNum (2 ^ (l + i)) (bcount s (l + i + 3)) : ℝ) / 2 ^ (l + i + 1) := by
  intro f
  induction f with
  | zero => intro l A; simp [runC]
  | succ f ih =>
    intro l A
    have e : runC s (f + 1) l (prow (l + 3)) A
        = runC s f (l + 1) (prow (l + 1 + 3))
            (2 * A + chunkNum (2 ^ l) (bsum s (l + 3) 0 (prow (l + 3)))) := rfl
    rw [e, ih, bsum_prow, Finset.sum_range_succ']
    have hidx : ∀ i, l + 1 + i = l + (i + 1) := fun i => by omega
    simp only [hidx, Nat.add_zero]
    push_cast
    have h2 : (2 : ℝ) ^ (l + (f + 1)) = 2 ^ (l + 1) * 2 ^ f := by
      rw [← pow_add]; congr 1; omega
    have h3 : (2 : ℝ) ^ (l + 1) ≠ 0 := by positivity
    rw [h2]
    generalize ((chunkNum (2 ^ l) (bcount s (l + 3)) : ℕ) : ℝ) = cn
    have h4 : (2 : ℝ) ^ (l + 1) * 2 ^ f * (cn / 2 ^ (l + 1)) = 2 ^ f * cn := by
      field_simp
    generalize (∑ x ∈ Finset.range f,
      ((chunkNum (2 ^ (l + (x + 1))) (bcount s (l + (x + 1) + 3)) : ℕ) : ℝ)
        / 2 ^ (l + (x + 1) + 1)) = Sg
    rw [mul_add (2 ^ (l + 1) * 2 ^ f : ℝ), h4]
    ring

/-- Bad integers of the levels `m+3, …, m+f+2`: reciprocal sum
`≤ runC s f m (prow (m+3)) 0 · 2 / (360360 · 2^(m+f))`. -/
theorem exact_mass_chunk_run (s m f : ℕ) (S : Finset ℕ)
    (hS : ∀ n ∈ S, 2 ^ (m + 3) ≤ n ∧ n < 2 ^ (m + f + 3) ∧ ¬ Good s n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ (runC s f m (prow (m + 3)) 0 : ℝ) * 2 / (360360 * 2 ^ (m + f)) := by
  refine (exact_mass_chunk s m f S hS).trans (le_of_eq ?_)
  rw [runC_spec]
  have h3 : (2 : ℝ) ^ (m + f) ≠ 0 := by positivity
  push_cast
  rw [mul_zero, zero_add, Finset.mul_sum, Finset.sum_mul, Finset.sum_div]
  refine Finset.sum_congr rfl fun i _ => ?_
  have h4 : (2 : ℝ) ^ (m + i + 1) = 2 ^ (m + i) * 2 := pow_succ _ _
  have h5 : (2 : ℝ) ^ (m + i) ≠ 0 := by positivity
  rw [h4]
  field_simp

/-- Kernel evaluation (`s = 3`, levels `3 … 299`, eight-step bound): the refined mass is
`16.94259998… ≤ 16.9426` (Python: `crosscheck.py`). -/
theorem runC0 :
    runC 3 297 0 (prow 3) 0 * 2 * 10000 ≤ 169426 * (360360 * 2 ^ (0 + 297)) := by
  decide +kernel

/-- Guard: tight to the stated digit. -/
theorem runC0_lower :
    169425 * (360360 * 2 ^ (0 + 297)) ≤ runC 3 297 0 (prow 3) 0 * 2 * 10000 := by
  decide +kernel

theorem run0_small : run 3 3 0 (prow 0) 0 = 3 * 2 ^ (0 + 3) := by decide +kernel

/-- Bad mass (`s = 3`) of all positive integers, refined: `≤ 19.9472`
(source: `β_all(0) = 19.3719` with the logarithm). -/
theorem bad_mass_0_refined (S : Finset ℕ) (hS : ∀ n ∈ S, 2 ^ 0 ≤ n ∧ ¬ Good 3 n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ 199472 / 10000 := by
  rw [← Finset.sum_filter_add_sum_filter_not S (fun n => n < 2 ^ 3)]
  have h1 : ∑ n ∈ S.filter (fun n => n < 2 ^ 3), (1 / (n : ℝ)) ≤ 3 := by
    have h := exact_mass_run 3 0 3 (S.filter (fun n => n < 2 ^ 3)) (by
      intro n hn
      obtain ⟨a1, a2⟩ := Finset.mem_filter.mp hn
      exact ⟨(hS n a1).1, a2, (hS n a1).2⟩)
    rw [run0_small] at h
    refine h.trans (le_of_eq ?_)
    norm_num
  rw [← Finset.sum_filter_add_sum_filter_not (S.filter (fun n => ¬ n < 2 ^ 3))
    (fun n => n < 2 ^ 300)]
  have h2 : ∑ n ∈ (S.filter (fun n => ¬ n < 2 ^ 3)).filter (fun n => n < 2 ^ 300),
      (1 / (n : ℝ)) ≤ (runC 3 297 0 (prow 3) 0 : ℝ) * 2 / (360360 * 2 ^ (0 + 297)) := by
    have h := exact_mass_chunk_run 3 0 297
      ((S.filter (fun n => ¬ n < 2 ^ 3)).filter (fun n => n < 2 ^ 300)) (by
        intro n hn
        obtain ⟨a1, a2⟩ := Finset.mem_filter.mp hn
        obtain ⟨a3, a4⟩ := Finset.mem_filter.mp a1
        exact ⟨not_lt.mp a4, a2, (hS n a3).2⟩)
    rw [show (0 : ℕ) + 3 = 3 from rfl] at h
    exact h
  have h3 : ∑ n ∈ (S.filter (fun n => ¬ n < 2 ^ 3)).filter (fun n => ¬ n < 2 ^ 300),
      (1 / (n : ℝ)) ≤ 2 ^ (1 + 1) * 30 * (29 / 30 : ℝ) ^ 300 := by
    apply bad_mass_tail_odd 1 300
    intro n hn
    obtain ⟨a1, a2⟩ := Finset.mem_filter.mp hn
    obtain ⟨a3, -⟩ := Finset.mem_filter.mp a1
    exact ⟨not_lt.mp a2, (hS n a3).2⟩
  have hr : (runC 3 297 0 (prow 3) 0 : ℝ) * 2 / (360360 * 2 ^ (0 + 297))
      ≤ 169426 / 10000 := by
    have hC := runC0
    generalize runC 3 297 0 (prow 3) 0 = R at hC ⊢
    rw [div_le_div_iff₀ (by positivity) (by norm_num)]
    exact_mod_cast hC
  exact (add_le_add h1 (add_le_add (h2.trans hr) (h3.trans tail300))).trans (by norm_num)

/-- **Theorem H with constant 27.93** (refereed value `27.163`; previous kernel-checked value
`162`). Every pairwise distinct stretch of a `T`-trajectory has harmonic sum `≤ 2793/100`. -/
theorem theoremH_2793 (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k))
    (K : ℕ) (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) :
    ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) ≤ 2793 / 100 := by
  rcases Nat.eq_zero_or_pos (x 0) with h0 | h0
  · have hz : ∀ k, x k = 0 := by
      intro k
      induction k with
      | zero => exact h0
      | succ k ih => rw [hx, ih]; decide
    have hsum : ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) = 0 := by simp [hz]
    rw [hsum]; norm_num
  · have hbig : ∀ k < K, 2 ^ 0 ≤ x k := by
      intro k _
      have := iterate_pos h0 k
      rw [← Sharp.seq_eq_iterate hx k] at this
      rw [pow_zero]; exact this
    refine (theoremH_ge 3 (by norm_num) 0 _ bad_mass_0_refined x hx K hinj hbig).trans ?_
    norm_num

/-- Residue bound with `exp(931/100)` (`≈ 1.1e4`): the unconditional consequence of
`theoremH_2793`. -/
theorem residue_bound_931 (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (k : ℕ) (hk : k ≤ K) :
    (x 0 : ℝ) * 3 ^ oddCount k (x 0) ≤ (x k : ℝ) * 2 ^ k ∧
      (x k : ℝ) * 2 ^ k ≤ Real.exp (931 / 100) * ((x 0 : ℝ) * 3 ^ oddCount k (x 0)) := by
  have h := Sharp.residue_bound_of_sum x hx k (2793 / 100)
    (theoremH_2793 x hx k fun i hi j hj h => hinj i (by omega) j (by omega) h)
  rwa [show (2793 : ℝ) / 100 / 3 = 931 / 100 by norm_num] at h

/-! ## Guards: the new theorems instantiated on concrete data -/

/-- `theoremH_2793` on the first five terms `27, 41, 62, 31, 47` of the trajectory of `27`. -/
example : ∑ k ∈ Finset.range 5, (1 / ((T^[k] 27 : ℕ) : ℝ)) ≤ 2793 / 100 :=
  theoremH_2793 (fun k => T^[k] 27) (fun k => Function.iterate_succ_apply' T k 27) 5 (by decide)

/-- `harmonic_ge_71` on the stretch `2^72, 2^71` (its hypotheses are satisfiable). -/
example : ∑ k ∈ Finset.range 2, (1 / ((T^[k] (2 ^ 72) : ℕ) : ℝ)) ≤ 69 / 50 :=
  harmonic_ge_71 (fun k => T^[k] (2 ^ 72)) (fun k => Function.iterate_succ_apply' T k (2 ^ 72)) 2
    (by decide +kernel) (by decide +kernel)

/-- `Sharp.residue_bound_of_sum` + `theoremH_2793` at `27`, `k = 5` (`T^[5] 27 = 71`, `a = 4`). -/
example : (71 : ℝ) * 2 ^ 5 ≤ Real.exp (931 / 100) * (27 * 3 ^ 4) := by
  have h := (residue_bound_931 (fun k => T^[k] 27)
    (fun k => Function.iterate_succ_apply' T k 27) 5 (by decide) 5 (le_refl 5)).2
  have e1 : T^[5] 27 = 71 := by decide
  have e2 : oddCount 5 27 = 4 := by decide
  simp only [e1, e2, Function.iterate_zero, id_eq] at h
  exact_mod_cast h

end Const
end CollatzFMF
