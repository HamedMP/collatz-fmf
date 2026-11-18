import CollatzFMF.ConstCount

/-!
# Theorem H with exact binomial bad mass below a cut and a Chernoff tail above it

Source: `notes/round6-nov2026/w2-delta/REPORT.md` section (b), Theorem H, Theorem R (the
level-restricted repetition of the proof of Theorem H) and Corollary D.

* `bad_mass_tail_odd` : bad integers `≥ 2^L1` (for `s = 2v+1`): mass `≤ 30·2^(v+1)·(29/30)^L1`.
* `bad_mass_split` : bad integers `≥ 2^M`: mass `≤ (exact levels M … M+f-1) + (tail from M+f)`.
* `theoremH_split` : Theorem H restricted to the terms `≥ 2^M` of a distinct stretch
  (abstract `β`; overhang `(M+1)/2^M`; each term `< 2^M` of the stretch costs `2/2^M`).
* `theoremH_ge` : the special case where all terms are `≥ 2^M`.
* `run0`, `run32`, `run71` : the three kernel evaluations (`decide +kernel`, no `native_decide`).
* `theoremH_3134` : every distinct stretch has harmonic sum `≤ 31.34` (was `162`).
* `harmonic_ge_71` : if all terms are `≥ 2^71`, the harmonic sum is `≤ 1.38`.
* `harmonic_ge_32` : if all terms are `≥ 2^32`, the harmonic sum is `≤ 6.71`.

Everything in this file is complete (no `sorry`, no extra axioms, no `native_decide`).
-/

namespace CollatzFMF
namespace Const

open KL (T)
open Harmonic

/-! ## Chernoff tail from an arbitrary level (odd `s`) -/

theorem sum_weight_from (v L1 : ℕ) : ∀ j : ℕ,
    ∑ n ∈ Finset.Ico (2 ^ L1) (2 ^ (L1 + j)), HarmonicSharp.weight v n
      = 2 ^ (v + 1) * 30 * ((29 / 30 : ℝ) ^ L1 - (29 / 30) ^ (L1 + j)) := by
  intro j
  induction j with
  | zero => simp
  | succ j ih =>
    rw [show L1 + (j + 1) = L1 + j + 1 by omega, ← Finset.sum_Ico_consecutive _
      (Nat.pow_le_pow_right (by norm_num : 0 < 2) (Nat.le_add_right L1 j))
      (Nat.pow_le_pow_right (by norm_num : 0 < 2) (Nat.le_succ (L1 + j))), ih,
      HarmonicSharp.sum_weight_block]
    ring

/-- Bad integers above `2^L1` (for `s = 2v+1`): reciprocal sum `≤ 30·2^(v+1)·(29/30)^L1`. -/
theorem bad_mass_tail_odd (v L1 : ℕ) (S : Finset ℕ)
    (hS : ∀ n ∈ S, 2 ^ L1 ≤ n ∧ ¬ Good (2 * v + 1) n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ 2 ^ (v + 1) * 30 * (29 / 30 : ℝ) ^ L1 := by
  have hpos : ∀ n ∈ S, 0 < n := fun n hn =>
    lt_of_lt_of_le (Nat.pow_pos (by norm_num)) (hS n hn).1
  have hsub : S ⊆ Finset.Ico (2 ^ L1) (2 ^ (L1 + S.sup id)) := by
    intro n hn
    have h1 : n ≤ S.sup id := Finset.le_sup (f := id) hn
    have h2 : n < 2 ^ n := Nat.lt_two_pow_self
    have h3 : 2 ^ n ≤ 2 ^ (L1 + S.sup id) := Nat.pow_le_pow_right (by norm_num) (by omega)
    exact Finset.mem_Ico.mpr ⟨(hS n hn).1, lt_of_lt_of_le h2 h3⟩
  calc ∑ n ∈ S, (1 / (n : ℝ)) ≤ ∑ n ∈ S, HarmonicSharp.weight v n :=
        Finset.sum_le_sum fun n hn => HarmonicSharp.inv_le_weight (hpos n hn) (hS n hn).2
    _ ≤ ∑ n ∈ Finset.Ico (2 ^ L1) (2 ^ (L1 + S.sup id)), HarmonicSharp.weight v n :=
        Finset.sum_le_sum_of_subset_of_nonneg hsub
          fun n _ _ => HarmonicSharp.weight_nonneg v n
    _ = 2 ^ (v + 1) * 30 * ((29 / 30 : ℝ) ^ L1 - (29 / 30) ^ (L1 + S.sup id)) :=
        sum_weight_from v L1 _
    _ ≤ 2 ^ (v + 1) * 30 * (29 / 30 : ℝ) ^ L1 := by
        have h1 : (0 : ℝ) ≤ (29 / 30) ^ (L1 + S.sup id) := by positivity
        have h2 : (0 : ℝ) ≤ 2 ^ (v + 1) * 30 := by positivity
        nlinarith [mul_nonneg h2 h1]

/-- **Bad mass above `2^M`, split form** (`s = 2v+1`): exact binomial counts on the levels
`M, …, M+f-1` (as the kernel-evaluable number `run s f M (prow M) 0`), Chernoff tail from
level `M+f`. -/
theorem bad_mass_split (s v : ℕ) (hsv : s = 2 * v + 1) (M f : ℕ) (S : Finset ℕ)
    (hS : ∀ n ∈ S, 2 ^ M ≤ n ∧ ¬ Good s n) :
    ∑ n ∈ S, (1 / (n : ℝ))
      ≤ (run s f M (prow M) 0 : ℝ) / 2 ^ (M + f) + 2 ^ (v + 1) * 30 * (29 / 30 : ℝ) ^ (M + f) := by
  subst hsv
  rw [← Finset.sum_filter_add_sum_filter_not S (fun n => n < 2 ^ (M + f))]
  apply add_le_add
  · apply exact_mass_run
    intro n hn
    obtain ⟨h1, h2⟩ := Finset.mem_filter.mp hn
    exact ⟨(hS n h1).1, h2, (hS n h1).2⟩
  · apply bad_mass_tail_odd
    intro n hn
    obtain ⟨h1, h2⟩ := Finset.mem_filter.mp hn
    exact ⟨not_lt.mp h2, (hS n h1).2⟩

/-! ## Theorem H restricted to the terms `≥ 2^M` -/

theorem geom_tail (t M : ℕ) :
    ∑ k ∈ (Finset.range (t + 1)).filter (fun k => k + M ≤ t), ((1 : ℝ) / 2) ^ (t - k)
      ≤ 2 * (1 / 2) ^ M := by
  by_cases h : M ≤ t
  · have hf : (Finset.range (t + 1)).filter (fun k => k + M ≤ t) = Finset.range (t - M + 1) := by
      ext k; simp only [Finset.mem_filter, Finset.mem_range]; omega
    rw [hf]
    have hterm : ∀ k ∈ Finset.range (t - M + 1),
        ((1 : ℝ) / 2) ^ (t - k) = 2 * (1 / 2) ^ M * (1 / 2) ^ (t - M + 1 - k) := by
      intro k hk
      have hk' := Finset.mem_range.mp hk
      have e : t - M + 1 - k = (t - k - M) + 1 := by omega
      have e2 : t - k = M + (t - k - M) := by omega
      rw [e, pow_succ]
      conv_lhs => rw [e2, pow_add]
      ring
    rw [Finset.sum_congr rfl hterm, ← Finset.mul_sum, Harmonic.sum_half_pow]
    have a1 : (0 : ℝ) ≤ (1 / 2) ^ (t - M + 1) := by positivity
    have a2 : (0 : ℝ) ≤ (1 / 2 : ℝ) ^ M := by positivity
    nlinarith [mul_nonneg a2 a1]
  · have hf : (Finset.range (t + 1)).filter (fun k => k + M ≤ t) = ∅ := by
      apply Finset.filter_eq_empty_iff.mpr
      intro k _; omega
    rw [hf, Finset.sum_empty]; positivity

/-- **One step of the proof of Theorem H, split at level `M`, for a class `Q` of integers.**
Let `x` be a `T`-sequence whose first `K` terms are pairwise distinct and let `β` bound the
reciprocal sum of every finite set of bad integers `≥ 2^M` in the class `Q`. Then
`Σ_{x_k ≥ 2^M, Q(x_k)} 1/x_k ≤ β + (M+1)/2^M + P·2/2^M + 2^(1-s) · Σ_{x_k ≥ 2^M} 1/x_k`,
`P` = number of terms `< 2^M`. (`Q = True`: Theorem H; `Q = odd`: the source's `W_odd`.) -/
theorem split_step (s M : ℕ) (Q : ℕ → Prop) [DecidablePred Q] (β : ℝ)
    (hβ : ∀ S : Finset ℕ, (∀ n ∈ S, 2 ^ M ≤ n ∧ Q n ∧ ¬ Good s n) →
      ∑ n ∈ S, (1 / (n : ℝ)) ≤ β)
    (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) :
    ∑ k ∈ (Finset.range K).filter (fun k => 2 ^ M ≤ x k ∧ Q (x k)), (1 / (x k : ℝ))
      ≤ β + (M + 1) / 2 ^ M
          + (((Finset.range K).filter (fun k => x k < 2 ^ M)).card : ℝ) * (2 / 2 ^ M)
          + 2 / 2 ^ s * ∑ k ∈ (Finset.range K).filter (fun k => 2 ^ M ≤ x k), (1 / (x k : ℝ)) := by
  set Big := (Finset.range K).filter (fun k => 2 ^ M ≤ x k ∧ Q (x k)) with hBig
  set W := ∑ k ∈ Big, (1 / (x k : ℝ)) with hW
  set W0 := ∑ k ∈ (Finset.range K).filter (fun k => 2 ^ M ≤ x k), (1 / (x k : ℝ)) with hW0
  have hbigQ : ∀ k ∈ Big, Q (x k) := fun k hk => (Finset.mem_filter.mp hk).2.2
  have hbigmem : ∀ k ∈ Big, k < K ∧ 2 ^ M ≤ x k := fun k hk => by
    obtain ⟨h1, h2, -⟩ := Finset.mem_filter.mp hk
    exact ⟨Finset.mem_range.mp h1, h2⟩
  have hlev : ∀ k, 2 ^ M ≤ x k → M ≤ Nat.log 2 (x k) := fun k h =>
    Nat.le_log_of_pow_le (by norm_num) h
  have hpowle : ∀ k, 2 ^ M ≤ x k → (2 : ℝ) ^ Nat.log 2 (x k) ≤ (x k : ℝ) := fun k h => by
    have h0 : 0 < x k := lt_of_lt_of_le (Nat.pow_pos (by norm_num)) h
    exact_mod_cast Nat.pow_log_le_self 2 h0.ne'
  -- bad part
  have hbad : ∑ k ∈ Big.filter (fun k => ¬ Good s (x k)), (1 / (x k : ℝ)) ≤ β := by
    set B := Big.filter (fun k => ¬ Good s (x k)) with hB
    have hinjB : Set.InjOn x (B : Set ℕ) := by
      intro i hi j hj hij
      have hi' := (hbigmem i (Finset.mem_filter.mp hi).1).1
      have hj' := (hbigmem j (Finset.mem_filter.mp hj).1).1
      exact hinj i hi' j hj' hij
    have h1 : ∑ n ∈ B.image x, (1 / (n : ℝ)) = ∑ k ∈ B, (1 / (x k : ℝ)) :=
      Finset.sum_image hinjB
    rw [← h1]
    apply hβ
    intro n hn
    obtain ⟨k, hk, rfl⟩ := Finset.mem_image.mp hn
    obtain ⟨hk1, hk2⟩ := Finset.mem_filter.mp hk
    exact ⟨(hbigmem k hk1).2, hbigQ k hk1, hk2⟩
  -- overhang part
  have hover : ∑ k ∈ (Big.filter (fun k => Good s (x k))).filter
      (fun k => ¬ k + Nat.log 2 (x k) < K), (1 / (x k : ℝ)) ≤ (M + 1) / 2 ^ M := by
    set O := (Big.filter (fun k => Good s (x k))).filter
      (fun k => ¬ k + Nat.log 2 (x k) < K) with hO
    have hOmem : ∀ k ∈ O, k < K ∧ 2 ^ M ≤ x k ∧ K ≤ k + Nat.log 2 (x k) := fun k hk => by
      obtain ⟨h1, h2⟩ := Finset.mem_filter.mp hk
      obtain ⟨h3, -⟩ := Finset.mem_filter.mp h1
      exact ⟨(hbigmem k h3).1, (hbigmem k h3).2, not_lt.mp h2⟩
    rw [← Finset.sum_filter_add_sum_filter_not O (fun k => K ≤ k + M)]
    have h1 : ∑ k ∈ O.filter (fun k => K ≤ k + M), (1 / (x k : ℝ)) ≤ M * (1 / 2) ^ M := by
      calc _ ≤ ∑ _k ∈ O.filter (fun k => K ≤ k + M), ((1 : ℝ) / 2) ^ M := by
            apply Finset.sum_le_sum
            intro k hk
            obtain ⟨hk1, -⟩ := Finset.mem_filter.mp hk
            obtain ⟨-, hb, -⟩ := hOmem k hk1
            have h2 : (2 : ℝ) ^ M ≤ (x k : ℝ) := by exact_mod_cast hb
            rw [div_pow, one_pow]
            exact one_div_le_one_div_of_le (by positivity) h2
        _ = ((O.filter (fun k => K ≤ k + M)).card : ℝ) * (1 / 2) ^ M := by
            rw [Finset.sum_const, nsmul_eq_mul]
        _ ≤ M * (1 / 2) ^ M := by
            apply mul_le_mul_of_nonneg_right _ (by positivity)
            have hsub : O.filter (fun k => K ≤ k + M) ⊆ Finset.Ico (K - M) K := by
              intro k hk
              obtain ⟨hk1, hk2⟩ := Finset.mem_filter.mp hk
              exact Finset.mem_Ico.mpr ⟨by omega, (hOmem k hk1).1⟩
            have hc := Finset.card_le_card hsub
            rw [Nat.card_Ico] at hc
            have h' : (O.filter (fun k => K ≤ k + M)).card ≤ M := by omega
            exact_mod_cast h'
    have h2 : ∑ k ∈ O.filter (fun k => ¬ K ≤ k + M), (1 / (x k : ℝ)) ≤ (1 / 2) ^ M := by
      calc _ ≤ ∑ k ∈ O.filter (fun k => ¬ K ≤ k + M), ((1 : ℝ) / 2) ^ (K - k) := by
            apply Finset.sum_le_sum
            intro k hk
            obtain ⟨hk1, -⟩ := Finset.mem_filter.mp hk
            obtain ⟨-, hb, hc⟩ := hOmem k hk1
            have h3 : (2 : ℝ) ^ (K - k) ≤ 2 ^ Nat.log 2 (x k) :=
              pow_le_pow_right₀ (by norm_num) (by omega)
            have h4 := hpowle k hb
            rw [div_pow, one_pow]
            exact one_div_le_one_div_of_le (by positivity) (h3.trans h4)
        _ ≤ ∑ k ∈ Finset.range (K - M), ((1 : ℝ) / 2) ^ (K - k) := by
            apply Finset.sum_le_sum_of_subset_of_nonneg
            · intro k hk
              obtain ⟨hk1, hk2⟩ := Finset.mem_filter.mp hk
              exact Finset.mem_range.mpr (by omega)
            · intro k _ _; positivity
        _ = (1 / 2) ^ M * ∑ k ∈ Finset.range (K - M), ((1 : ℝ) / 2) ^ (K - M - k) := by
            rw [Finset.mul_sum]
            refine Finset.sum_congr rfl fun k hk => ?_
            have hk' := Finset.mem_range.mp hk
            rw [← pow_add]
            congr 1
            omega
        _ ≤ (1 / 2) ^ M := by
            rw [Harmonic.sum_half_pow]
            have a1 : (0 : ℝ) ≤ (1 / 2) ^ (K - M) := by positivity
            have a2 : (0 : ℝ) ≤ (1 / 2 : ℝ) ^ M := by positivity
            nlinarith [mul_nonneg a2 a1]
    have e : ((M : ℝ) + 1) / 2 ^ M = M * (1 / 2) ^ M + (1 / 2) ^ M := by
      rw [div_pow, one_pow]; ring
    rw [e]
    exact add_le_add h1 h2
  -- main part
  have hmain : ∑ k ∈ (Big.filter (fun k => Good s (x k))).filter
      (fun k => k + Nat.log 2 (x k) < K), (1 / (x k : ℝ))
      ≤ 2 / 2 ^ s * W0
        + (((Finset.range K).filter (fun k => x k < 2 ^ M)).card : ℝ) * (2 / 2 ^ M) := by
    set Mn := (Big.filter (fun k => Good s (x k))).filter
      (fun k => k + Nat.log 2 (x k) < K) with hMn
    have hMnmem : ∀ k ∈ Mn, k < K ∧ 2 ^ M ≤ x k ∧ Good s (x k) := fun k hk => by
      obtain ⟨h1, -⟩ := Finset.mem_filter.mp hk
      obtain ⟨h3, h4⟩ := Finset.mem_filter.mp h1
      exact ⟨(hbigmem k h3).1, (hbigmem k h3).2, h4⟩
    have hfib := Finset.sum_fiberwise_of_maps_to (s := Mn) (t := Finset.range K)
      (g := fun k => k + Nat.log 2 (x k)) (f := fun k => 1 / (x k : ℝ))
      (fun k hk => Finset.mem_range.mpr (Finset.mem_filter.mp hk).2)
    have hfe : (Finset.range K).filter (fun k => ¬ 2 ^ M ≤ x k)
        = (Finset.range K).filter (fun k => x k < 2 ^ M) :=
      Finset.filter_congr fun k _ => not_le
    have hF : ∑ t ∈ Finset.range K,
          (if 2 ^ M ≤ x t then 2 / 2 ^ s * (1 / (x t : ℝ)) else 2 / 2 ^ M)
        = 2 / 2 ^ s * W0
          + (((Finset.range K).filter (fun k => x k < 2 ^ M)).card : ℝ) * (2 / 2 ^ M) := by
      rw [Finset.sum_ite, hfe, Finset.sum_const, nsmul_eq_mul, hW0, Finset.mul_sum]
    rw [← hfib, ← hF]
    apply Finset.sum_le_sum
    intro t _
    by_cases hbt : 2 ^ M ≤ x t
    · rw [if_pos hbt]
      calc _ ≤ ∑ k ∈ (Finset.range K).filter
            (fun k => k + Nat.log 2 (x k) = t ∧ Good s (x k)), (1 / (x k : ℝ)) := by
            apply Finset.sum_le_sum_of_subset_of_nonneg
            · intro k hk
              obtain ⟨hk1, hk2⟩ := Finset.mem_filter.mp hk
              obtain ⟨a1, -, a3⟩ := hMnmem k hk1
              exact Finset.mem_filter.mpr ⟨Finset.mem_range.mpr a1, hk2, a3⟩
            · intro k _ _; positivity
        _ ≤ 2 / (2 ^ s * (x t : ℝ)) := lemma3 s x hx K t
        _ = 2 / 2 ^ s * (1 / (x t : ℝ)) := by ring
    · rw [if_neg hbt]
      calc _ ≤ ∑ k ∈ Mn.filter (fun k => k + Nat.log 2 (x k) = t), ((1 : ℝ) / 2) ^ (t - k) := by
            apply Finset.sum_le_sum
            intro k hk
            obtain ⟨hk1, hk2⟩ := Finset.mem_filter.mp hk
            have hk2' : k + Nat.log 2 (x k) = t := hk2
            obtain ⟨-, a2, -⟩ := hMnmem k hk1
            have h4 := hpowle k a2
            have e : t - k = Nat.log 2 (x k) := by omega
            rw [e, div_pow, one_pow]
            exact one_div_le_one_div_of_le (by positivity) h4
        _ ≤ ∑ k ∈ (Finset.range (t + 1)).filter (fun k => k + M ≤ t),
              ((1 : ℝ) / 2) ^ (t - k) := by
            apply Finset.sum_le_sum_of_subset_of_nonneg
            · intro k hk
              obtain ⟨hk1, hk2⟩ := Finset.mem_filter.mp hk
              have hk2' : k + Nat.log 2 (x k) = t := hk2
              obtain ⟨-, a2, -⟩ := hMnmem k hk1
              have hl := hlev k a2
              exact Finset.mem_filter.mpr ⟨Finset.mem_range.mpr (by omega), by omega⟩
            · intro k _ _; positivity
        _ ≤ 2 * (1 / 2) ^ M := geom_tail t M
        _ = 2 / 2 ^ M := by rw [div_pow, one_pow]; ring
  -- assemble
  have hsplit : W = ∑ k ∈ (Big.filter (fun k => Good s (x k))).filter
        (fun k => k + Nat.log 2 (x k) < K), (1 / (x k : ℝ))
      + ∑ k ∈ (Big.filter (fun k => Good s (x k))).filter
        (fun k => ¬ k + Nat.log 2 (x k) < K), (1 / (x k : ℝ))
      + ∑ k ∈ Big.filter (fun k => ¬ Good s (x k)), (1 / (x k : ℝ)) := by
    rw [Finset.sum_filter_add_sum_filter_not, Finset.sum_filter_add_sum_filter_not]
  linarith [hbad, hover, hmain, hsplit]

/-- **Theorem H, split at level `M` (abstract `β`).** Let `x` be a `T`-sequence whose first
`K` terms are pairwise distinct, `s ≥ 2`, and let `β` bound the reciprocal sum of every finite
set of bad integers `≥ 2^M`. Then the terms `≥ 2^M` among the first `K` satisfy
`Σ 1/x_k ≤ (β + (M+1)/2^M + P·2/2^M) / (1 - 2^(1-s))`, `P` = number of terms `< 2^M`. -/
theorem theoremH_split (s : ℕ) (hs : 2 ≤ s) (M : ℕ) (β : ℝ)
    (hβ : ∀ S : Finset ℕ, (∀ n ∈ S, 2 ^ M ≤ n ∧ ¬ Good s n) → ∑ n ∈ S, (1 / (n : ℝ)) ≤ β)
    (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) :
    ∑ k ∈ (Finset.range K).filter (fun k => 2 ^ M ≤ x k), (1 / (x k : ℝ))
      ≤ (β + (M + 1) / 2 ^ M
          + (((Finset.range K).filter (fun k => x k < 2 ^ M)).card : ℝ) * (2 / 2 ^ M))
        / (1 - 2 / 2 ^ s) := by
  have h := split_step s M (fun _ => True) β
    (fun S hS => hβ S fun n hn => ⟨(hS n hn).1, (hS n hn).2.2⟩) x hx K hinj
  have hfe : (Finset.range K).filter (fun k => 2 ^ M ≤ x k ∧ True)
      = (Finset.range K).filter (fun k => 2 ^ M ≤ x k) :=
    Finset.filter_congr fun k _ => by simp
  rw [hfe] at h
  have hq : (2 : ℝ) / 2 ^ s ≤ 1 / 2 := by
    have h4 : (2 : ℝ) ^ 2 ≤ 2 ^ s := pow_le_pow_right₀ (by norm_num) hs
    rw [div_le_div_iff₀ (by positivity) (by norm_num)]
    linarith
  have hden : (0 : ℝ) < 1 - 2 / 2 ^ s := by linarith
  rw [le_div_iff₀ hden]
  nlinarith [h]

/-- **Theorem H above `2^M` (abstract `β`).** If all of the first `K` (pairwise distinct)
terms are `≥ 2^M`, then `Σ_{k<K} 1/x_k ≤ (β + (M+1)/2^M) / (1 - 2^(1-s))`. -/
theorem theoremH_ge (s : ℕ) (hs : 2 ≤ s) (M : ℕ) (β : ℝ)
    (hβ : ∀ S : Finset ℕ, (∀ n ∈ S, 2 ^ M ≤ n ∧ ¬ Good s n) → ∑ n ∈ S, (1 / (n : ℝ)) ≤ β)
    (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (hbig : ∀ k < K, 2 ^ M ≤ x k) :
    ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) ≤ (β + (M + 1) / 2 ^ M) / (1 - 2 / 2 ^ s) := by
  have h := theoremH_split s hs M β hβ x hx K hinj
  have h1 : (Finset.range K).filter (fun k => 2 ^ M ≤ x k) = Finset.range K :=
    Finset.filter_true_of_mem fun k hk => hbig k (Finset.mem_range.mp hk)
  have h2 : (Finset.range K).filter (fun k => x k < 2 ^ M) = ∅ := by
    apply Finset.filter_eq_empty_iff.mpr
    intro k hk
    exact not_lt.mpr (hbig k (Finset.mem_range.mp hk))
  rw [h1, h2] at h
  simpa using h

/-! ## The kernel evaluations

`run 3 f M (prow M) 0 = 2^(M+f) · Σ_{L=M}^{M+f-1} b_L / 2^L` for `s = 3`. Values cross-checked
with exact rationals in `notes/round6-nov2026/lean-constants/crosscheck.py`:
`Σ_{L<300} b_L/2^L = 22.499461…`, `Σ_{32≤L<300} = 5.026878…`, `Σ_{71≤L<300} = 1.029811…`. -/

theorem run0 : run 3 300 0 (prow 0) 0 * 1000 ≤ 22500 * 2 ^ (0 + 300) := by decide +kernel

theorem run32 : run 3 268 32 (prow 32) 0 * 1000 ≤ 5027 * 2 ^ (32 + 268) := by decide +kernel

theorem run71 : run 3 229 71 (prow 71) 0 * 1000 ≤ 1030 * 2 ^ (71 + 229) := by decide +kernel

/-- Guards: the bounds are tight to the stated digit (so `run` is not vacuously small). -/
theorem run0_lower : 22499 * 2 ^ (0 + 300) ≤ run 3 300 0 (prow 0) 0 * 1000 := by decide +kernel

theorem run71_lower : 1029 * 2 ^ (71 + 229) ≤ run 3 229 71 (prow 71) 0 * 1000 := by
  decide +kernel

theorem tail300_nat : 120 * 29 ^ 300 * 5000 ≤ 23 * 30 ^ 300 := by decide +kernel

theorem tail300 : (2 : ℝ) ^ (1 + 1) * 30 * (29 / 30) ^ 300 ≤ 46 / 10000 := by
  have hR : (120 : ℝ) * 29 ^ 300 * 5000 ≤ 23 * 30 ^ 300 := by exact_mod_cast tail300_nat
  rw [show (2 : ℝ) ^ (1 + 1) * 30 = 120 by norm_num, show (46 : ℝ) / 10000 = 23 / 5000 by norm_num,
    div_pow, mul_div_assoc', div_le_div_iff₀ (by positivity) (by norm_num)]
  exact hR

/-- Bad mass (`s = 3`) of all positive integers: `≤ 22.5046` (source: `β_all(0) ≈ 19.37`
with the logarithmic refinement, `22.4997` without). -/
theorem bad_mass_0 (S : Finset ℕ) (hS : ∀ n ∈ S, 2 ^ 0 ≤ n ∧ ¬ Good 3 n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ 225046 / 10000 := by
  have h := bad_mass_split 3 1 rfl 0 300 S hS
  have hr : (run 3 300 0 (prow 0) 0 : ℝ) / 2 ^ (0 + 300) ≤ 22500 / 1000 := by
    rw [div_le_div_iff₀ (by positivity) (by norm_num)]
    exact_mod_cast run0
  have ht := tail300
  exact h.trans ((add_le_add hr ht).trans (by norm_num))

/-- Bad mass (`s = 3`) of the integers `≥ 2^32`: `≤ 5.0316`. -/
theorem bad_mass_32 (S : Finset ℕ) (hS : ∀ n ∈ S, 2 ^ 32 ≤ n ∧ ¬ Good 3 n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ 50316 / 10000 := by
  have h := bad_mass_split 3 1 rfl 32 268 S hS
  have hr : (run 3 268 32 (prow 32) 0 : ℝ) / 2 ^ (32 + 268) ≤ 5027 / 1000 := by
    rw [div_le_div_iff₀ (by positivity) (by norm_num)]
    exact_mod_cast run32
  have ht := tail300
  exact h.trans ((add_le_add hr ht).trans (by norm_num))

/-- Bad mass (`s = 3`) of the integers `≥ 2^71`: `≤ 1.0346`. -/
theorem bad_mass_71 (S : Finset ℕ) (hS : ∀ n ∈ S, 2 ^ 71 ≤ n ∧ ¬ Good 3 n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ 10346 / 10000 := by
  have h := bad_mass_split 3 1 rfl 71 229 S hS
  have hr : (run 3 229 71 (prow 71) 0 : ℝ) / 2 ^ (71 + 229) ≤ 1030 / 1000 := by
    rw [div_le_div_iff₀ (by positivity) (by norm_num)]
    exact_mod_cast run71
  have ht := tail300
  exact h.trans ((add_le_add hr ht).trans (by norm_num))

/-! ## Explicit constants -/

/-- **Theorem H with constant 31.34** (was `162`; refereed value `27.163`). Every pairwise
distinct stretch of a `T`-trajectory has harmonic sum `≤ 1567/50`. -/
theorem theoremH_3134 (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k))
    (K : ℕ) (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) :
    ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) ≤ 1567 / 50 := by
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
    refine (theoremH_ge 3 (by norm_num) 0 _ bad_mass_0 x hx K hinj hbig).trans ?_
    norm_num

/-- **Harmonic sum above `2^71`: `≤ 1.38`** (refereed value `1.3594`). If the first `K` terms
of a `T`-sequence are pairwise distinct and all `≥ 2^71`, then `Σ_{k<K} 1/x_k ≤ 69/50`. -/
theorem harmonic_ge_71 (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k))
    (K : ℕ) (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (hbig : ∀ k < K, 2 ^ 71 ≤ x k) :
    ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) ≤ 69 / 50 := by
  refine (theoremH_ge 3 (by norm_num) 71 _ bad_mass_71 x hx K hinj hbig).trans ?_
  norm_num

/-- **Harmonic sum above `2^32`: `≤ 6.71`** (refereed value `6.3754`, which also absorbs the
`ε` of the terms below `2^32`). -/
theorem harmonic_ge_32 (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k))
    (K : ℕ) (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (hbig : ∀ k < K, 2 ^ 32 ≤ x k) :
    ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) ≤ 671 / 100 := by
  refine (theoremH_ge 3 (by norm_num) 32 _ bad_mass_32 x hx K hinj hbig).trans ?_
  norm_num

end Const
end CollatzFMF
