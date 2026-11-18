import CollatzFMF.ResidueProduct

/-!
# Exact counts of bad parity vectors, level by level

Source: `notes/round6-nov2026/w2-delta/REPORT.md` section (b) (definition of `b_L`);
`notes/round6-nov2026/lean-constants/REPORT.md`.

* `card_oddCount_block` : `#{n ∈ [2^L, 2^(L+1)) : oddCount L n = a} = C(L, a)`
  (coefficient form of `Harmonic.sum_pow_oddCount_block`).
* `BadA s L a` : the vector-level badness condition `3^a (2^a + 1) 2^s > 2^(L+a)`;
  `bcount s L = Σ_a [BadA s L a] C(L,a)` is the number `b_L` of bad vectors.
* `card_bad_block` : `#{n ∈ [2^L, 2^(L+1)) : ¬ Good s n} = bcount s L`.
* `exact_mass` : distinct bad integers in `[2^M, 2^(M+f))` have reciprocal sum
  `≤ Σ_{L=M}^{M+f-1} b_L / 2^L`.
* `run`, `prow`, `run_spec` : a kernel-evaluable Pascal-row computation of
  `2^(M+f) * Σ_{L=M}^{M+f-1} b_L / 2^L` (a natural number), with its correctness proof.

Everything in this file is complete (no `sorry`, no extra axioms, no `native_decide`).
-/

namespace CollatzFMF
namespace Const

open KL (T)
open Harmonic

/-! ## The count identity -/

/-- Terras, count form: exactly `C(L, a)` integers of the level-`L` block have `a` odd terms
among their first `L` iterates. -/
theorem card_oddCount_block (L a : ℕ) :
    ((Finset.Ico (2 ^ L) (2 ^ (L + 1))).filter (fun n => oddCount L n = a)).card
      = L.choose a := by
  have hpoly : (∑ n ∈ Finset.Ico (2 ^ L) (2 ^ (L + 1)),
      (Polynomial.X : Polynomial ℝ) ^ oddCount L n) = (1 + Polynomial.X) ^ L := by
    apply Polynomial.funext
    intro y
    simpa [Polynomial.eval_finsetSum] using sum_pow_oddCount_block y L
  have hc : (∑ n ∈ Finset.Ico (2 ^ L) (2 ^ (L + 1)),
      (Polynomial.X : Polynomial ℝ) ^ oddCount L n).coeff a
      = ((1 + Polynomial.X : Polynomial ℝ) ^ L).coeff a := by rw [hpoly]
  simp only [Polynomial.finsetSum_coeff, Polynomial.coeff_X_pow,
    Polynomial.coeff_one_add_X_pow] at hc
  rw [Finset.card_filter]
  have h2 : ((∑ n ∈ Finset.Ico (2 ^ L) (2 ^ (L + 1)), (if oddCount L n = a then 1 else 0) : ℕ) : ℝ)
      = (L.choose a : ℝ) := by
    rw [← hc]
    push_cast
    refine Finset.sum_congr rfl fun n _ => ?_
    by_cases h : oddCount L n = a
    · simp [h]
    · have h' : ¬ a = oddCount L n := fun e => h e.symm
      simp [h, h']
  exact_mod_cast h2

/-- Guard: the four integers of level 2 are `4, 5, 6, 7` with odd counts `0, 1, 1, 2`. -/
example : oddCount 2 4 = 0 ∧ oddCount 2 5 = 1 ∧ oddCount 2 6 = 1 ∧ oddCount 2 7 = 2 := by decide

/-! ## Bad vectors -/

/-- Vector-level badness: a parity vector of length `L` with `a` ones is bad for `s` iff
`3^a (2^a + 1) 2^s > 2^(L+a)` (negation of Lemma 2's hypothesis). -/
def BadA (s L a : ℕ) : Prop := ¬ (3 ^ a * (2 ^ a + 1) * 2 ^ s ≤ 2 ^ (L + a))

instance (s L a : ℕ) : Decidable (BadA s L a) := by unfold BadA; infer_instance

/-- `b_L`: the number of bad vectors of length `L`. -/
def bcount (s L : ℕ) : ℕ := ∑ a ∈ Finset.range (L + 1), if BadA s L a then L.choose a else 0

theorem not_good_iff {s L n : ℕ} (h1 : 2 ^ L ≤ n) (h2 : n < 2 ^ (L + 1)) :
    ¬ Good s n ↔ BadA s L (oddCount L n) := by
  have hlog : Nat.log 2 n = L := Nat.log_eq_of_pow_le_of_lt_pow h1 h2
  unfold Good BadA
  rw [hlog]

/-- The number of bad integers of level `L` is exactly `b_L`. -/
theorem card_bad_block (s L : ℕ) :
    ((Finset.Ico (2 ^ L) (2 ^ (L + 1))).filter (fun n => ¬ Good s n)).card = bcount s L := by
  have h1 : (Finset.Ico (2 ^ L) (2 ^ (L + 1))).filter (fun n => ¬ Good s n)
      = (Finset.Ico (2 ^ L) (2 ^ (L + 1))).filter (fun n => BadA s L (oddCount L n)) := by
    apply Finset.filter_congr
    intro n hn
    obtain ⟨a1, a2⟩ := Finset.mem_Ico.mp hn
    exact not_good_iff a1 a2
  rw [h1, Finset.card_eq_sum_card_fiberwise (f := oddCount L) (t := Finset.range (L + 1))
    (fun n _ => Finset.mem_range.mpr (Nat.lt_succ_of_le (oddCount_le L n)))]
  unfold bcount
  refine Finset.sum_congr rfl fun a _ => ?_
  by_cases hb : BadA s L a
  · rw [if_pos hb, ← card_oddCount_block L a]
    congr 1
    ext n
    simp only [Finset.mem_filter]
    constructor
    · rintro ⟨⟨h, -⟩, e⟩; exact ⟨h, e⟩
    · rintro ⟨h, e⟩; exact ⟨⟨h, by rw [e]; exact hb⟩, e⟩
  · rw [if_neg hb, Finset.card_eq_zero, Finset.filter_eq_empty_iff]
    rintro n hn e
    rw [Finset.mem_filter] at hn
    rw [e] at hn
    exact hb hn.2

/-- Bad integers of a single level: reciprocal sum `≤ b_L / 2^L`. -/
theorem block_mass (s L : ℕ) (S : Finset ℕ)
    (hS : ∀ n ∈ S, 2 ^ L ≤ n ∧ n < 2 ^ (L + 1) ∧ ¬ Good s n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ (bcount s L : ℝ) / 2 ^ L := by
  have hsub : S ⊆ (Finset.Ico (2 ^ L) (2 ^ (L + 1))).filter (fun n => ¬ Good s n) := by
    intro n hn
    obtain ⟨a1, a2, a3⟩ := hS n hn
    exact Finset.mem_filter.mpr ⟨Finset.mem_Ico.mpr ⟨a1, a2⟩, a3⟩
  have hcard : S.card ≤ bcount s L := by
    rw [← card_bad_block]; exact Finset.card_le_card hsub
  calc ∑ n ∈ S, (1 / (n : ℝ)) ≤ ∑ _n ∈ S, (1 / (2 : ℝ) ^ L) := by
        apply Finset.sum_le_sum
        intro n hn
        have h1 : ((2 : ℝ)) ^ L ≤ (n : ℝ) := by exact_mod_cast (hS n hn).1
        exact one_div_le_one_div_of_le (by positivity) h1
    _ = (S.card : ℝ) * (1 / (2 : ℝ) ^ L) := by rw [Finset.sum_const, nsmul_eq_mul]
    _ ≤ (bcount s L : ℝ) * (1 / (2 : ℝ) ^ L) := by
        apply mul_le_mul_of_nonneg_right _ (by positivity)
        exact_mod_cast hcard
    _ = (bcount s L : ℝ) / 2 ^ L := by ring

/-- **Exact bad mass on a range of levels.** Distinct bad integers in `[2^M, 2^(M+f))` have
reciprocal sum `≤ Σ_{i<f} b_{M+i} / 2^(M+i)`. -/
theorem exact_mass (s M : ℕ) : ∀ (f : ℕ) (S : Finset ℕ),
    (∀ n ∈ S, 2 ^ M ≤ n ∧ n < 2 ^ (M + f) ∧ ¬ Good s n) →
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ ∑ i ∈ Finset.range f, (bcount s (M + i) : ℝ) / 2 ^ (M + i) := by
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
    rw [Finset.sum_range_succ, ← Finset.sum_filter_add_sum_filter_not S (fun n => n < 2 ^ (M + f))]
    apply add_le_add
    · apply ih
      intro n hn
      obtain ⟨h1, h2⟩ := Finset.mem_filter.mp hn
      exact ⟨(hS n h1).1, h2, (hS n h1).2.2⟩
    · apply block_mass
      intro n hn
      obtain ⟨h1, h2⟩ := Finset.mem_filter.mp hn
      exact ⟨not_lt.mp h2, (hS n h1).2.1, (hS n h1).2.2⟩

/-! ## Kernel-evaluable computation of the exact mass (Pascal rows) -/

/-- One Pascal step: `pnext 0 [c_0, …, c_L] = [c_0, c_0 + c_1, …, c_{L-1} + c_L, c_L]`. -/
def pnext : ℕ → List ℕ → List ℕ
  | p, [] => [p]
  | p, c :: cs => (p + c) :: pnext c cs

/-- Row `L` of Pascal's triangle. -/
def prow : ℕ → List ℕ
  | 0 => [1]
  | L + 1 => pnext 0 (prow L)

/-- Sum of the entries of a row at bad positions (positions counted from `a`). -/
def bsum (s L : ℕ) : ℕ → List ℕ → ℕ
  | _, [] => 0
  | a, c :: cs => (if BadA s L a then c else 0) + bsum s L (a + 1) cs

/-- `run s f L (prow L) A = 2^f A + 2^(L+f) Σ_{i<f} b_{L+i} / 2^(L+i)` (see `run_spec`). -/
def run (s : ℕ) : ℕ → ℕ → List ℕ → ℕ → ℕ
  | 0, _, _, A => A
  | f + 1, L, r, A => run s f (L + 1) (pnext 0 r) (2 * A + 2 * bsum s L 0 r)

theorem pnext_spec (L : ℕ) : ∀ k a, L ≤ a + k →
    pnext (L.choose a) ((List.range' (a + 1) k).map L.choose)
      = (List.range' (a + 1) (k + 1)).map (L + 1).choose := by
  intro k
  induction k with
  | zero =>
    intro a h
    have h0 : L.choose (a + 1) = 0 := Nat.choose_eq_zero_of_lt (by omega)
    simp [pnext, Nat.choose_succ_succ, h0]
  | succ k ih =>
    intro a h
    have := ih (a + 1) (by omega)
    have hc : (L + 1).choose (a + 1) = L.choose a + L.choose (a + 1) := Nat.choose_succ_succ L a
    simp only [List.range'_succ, List.map_cons, pnext] at this ⊢
    rw [this, hc]

theorem prow_eq (L : ℕ) : prow L = (List.range' 0 (L + 1)).map L.choose := by
  induction L with
  | zero => rfl
  | succ L ih =>
    rw [prow, ih]
    have := pnext_spec L L 0 (by omega)
    simp only [List.range'_succ, List.map_cons, pnext, Nat.choose_zero_right, Nat.zero_add]
      at this ⊢
    rw [this]

theorem bsum_spec (s L : ℕ) : ∀ k a,
    bsum s L a ((List.range' a k).map L.choose)
      = ∑ i ∈ Finset.range k, if BadA s L (a + i) then L.choose (a + i) else 0 := by
  intro k
  induction k with
  | zero => intro a; simp [bsum]
  | succ k ih =>
    intro a
    rw [List.range'_succ, List.map_cons, bsum, ih (a + 1), Finset.sum_range_succ', Nat.add_zero,
      Nat.add_comm]
    congr 1
    refine Finset.sum_congr rfl fun i _ => ?_
    rw [show a + 1 + i = a + (i + 1) by omega]

theorem bsum_prow (s L : ℕ) : bsum s L 0 (prow L) = bcount s L := by
  rw [prow_eq, bsum_spec]
  unfold bcount
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Nat.zero_add]

/-- Guards for the Pascal machinery (cross-checked in Python). -/
example : prow 5 = [1, 5, 10, 10, 5, 1] := by decide
example : bsum 3 9 0 (prow 9) = 382 := by decide
example : bsum 3 4 0 (prow 4) = 15 := by decide

theorem run_spec (s : ℕ) : ∀ f L A,
    (run s f L (prow L) A : ℝ)
      = 2 ^ f * (A : ℝ) + 2 ^ (L + f) * ∑ i ∈ Finset.range f, (bcount s (L + i) : ℝ) / 2 ^ (L + i) := by
  intro f
  induction f with
  | zero => intro L A; simp [run]
  | succ f ih =>
    intro L A
    have e : run s (f + 1) L (prow L) A
        = run s f (L + 1) (prow (L + 1)) (2 * A + 2 * bsum s L 0 (prow L)) := rfl
    rw [e, ih, bsum_prow, Finset.sum_range_succ']
    have hidx : ∀ i, L + 1 + i = L + (i + 1) := fun i => by omega
    simp only [hidx, Nat.add_zero]
    push_cast
    have h2 : (2 : ℝ) ^ (L + (f + 1)) = 2 ^ L * 2 ^ (f + 1) := pow_add _ _ _
    have h3 : (2 : ℝ) ^ L ≠ 0 := by positivity
    rw [h2]
    have h4 : (2 : ℝ) ^ L * 2 ^ (f + 1) * ((bcount s L : ℝ) / 2 ^ L) = 2 ^ (f + 1) * bcount s L := by
      field_simp
    generalize (∑ x ∈ Finset.range f, (bcount s (L + (x + 1)) : ℝ) / 2 ^ (L + (x + 1))) = Sg
    rw [mul_add (2 ^ L * 2 ^ (f + 1) : ℝ), h4, pow_succ]
    ring

/-- **Exact bad mass, computed.** Distinct bad integers in `[2^M, 2^(M+f))` have reciprocal
sum `≤ run s f M (prow M) 0 / 2^(M+f)`, where the numerator is a kernel-evaluable natural
number. -/
theorem exact_mass_run (s M f : ℕ) (S : Finset ℕ)
    (hS : ∀ n ∈ S, 2 ^ M ≤ n ∧ n < 2 ^ (M + f) ∧ ¬ Good s n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ (run s f M (prow M) 0 : ℝ) / 2 ^ (M + f) := by
  refine (exact_mass s M f S hS).trans (le_of_eq ?_)
  rw [run_spec]
  have h3 : (2 : ℝ) ^ (M + f) ≠ 0 := by positivity
  push_cast
  field_simp
  ring

end Const
end CollatzFMF
