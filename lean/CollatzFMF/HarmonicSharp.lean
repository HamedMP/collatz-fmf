import CollatzFMF.HarmonicBeta

/-!
# A sharper explicit constant in Theorem H: `Σ 1/x_k ≤ 162` (was `1196`)

Same proof as `HarmonicBeta.bad_mass`, with two cheap improvements:
* rational base points `26/15 ≥ √3`, `41/29 ≤ √2`, for which the block ratio is exactly
  `(1 + 26/15) / (2 * 41/29) = 29/30` (the irrational optimum is `(1+√3)/(2√2) ≈ 0.9659`);
* for odd `s = 2v+1` the bad condition `2^L < 3^a 2^(s+1)` is used through its square root,
  giving the factor `2^(v+1)` instead of `2^(s+1)`.

Result: bad mass `≤ 30 * 2^(v+1)`; for `s = 3`: `β = 120`, `Σ 1/x_k ≤ 121 / (3/4) < 162`.
(The source's exact-binomial value is `27.2`; that is NOT attempted here.)

Everything in this file is complete (no `sorry`, no extra axioms).
-/

namespace CollatzFMF
namespace HarmonicSharp

open KL (T)
open Harmonic

/-- Chernoff weight dominating the reciprocal of an integer that is bad for `s = 2v+1`. -/
noncomputable def weight (v n : ℕ) : ℝ :=
  2 ^ (v + 1) * (26 / 15 : ℝ) ^ oddCount (Nat.log 2 n) n / (82 / 29 : ℝ) ^ Nat.log 2 n

theorem weight_nonneg (v n : ℕ) : 0 ≤ weight v n := by unfold weight; positivity

theorem inv_le_weight {v n : ℕ} (hn : 0 < n) (hb : ¬ Good (2 * v + 1) n) :
    1 / (n : ℝ) ≤ weight v n := by
  unfold Good at hb
  unfold weight
  have hlog : 2 ^ Nat.log 2 n ≤ n := Nat.pow_log_le_self 2 hn.ne'
  generalize Nat.log 2 n = L at *
  generalize oddCount L n = a at *
  -- integer consequence of badness: 2^L < 3^a * 2^(s+1), with s + 1 = 2 (v+1)
  have hnat : 2 ^ L < 3 ^ a * 2 ^ (2 * v + 1 + 1) := by
    have h1 : 2 ^ (L + a) < 3 ^ a * (2 ^ a + 1) * 2 ^ (2 * v + 1) := Nat.lt_of_not_le hb
    have h2 : (2:ℕ) ^ a + 1 ≤ 2 * 2 ^ a := by
      have : 0 < 2 ^ a := by positivity
      omega
    have h3 : 3 ^ a * (2 ^ a + 1) * 2 ^ (2 * v + 1) ≤ 3 ^ a * (2 * 2 ^ a) * 2 ^ (2 * v + 1) :=
      Nat.mul_le_mul_right _ (Nat.mul_le_mul_left _ h2)
    have h4 : 2 ^ L * 2 ^ a < 3 ^ a * 2 ^ (2 * v + 1 + 1) * 2 ^ a := by
      calc 2 ^ L * 2 ^ a = 2 ^ (L + a) := (pow_add 2 L a).symm
        _ < 3 ^ a * (2 ^ a + 1) * 2 ^ (2 * v + 1) := h1
        _ ≤ 3 ^ a * (2 * 2 ^ a) * 2 ^ (2 * v + 1) := h3
        _ = 3 ^ a * 2 ^ (2 * v + 1 + 1) * 2 ^ a := by rw [pow_succ _ (2 * v + 1)]; ring
    exact Nat.lt_of_mul_lt_mul_right h4
  have hreal : (2:ℝ) ^ L < 3 ^ a * (2 ^ (v + 1) * 2 ^ (v + 1)) := by
    have : (2:ℝ) ^ L < 3 ^ a * 2 ^ (2 * v + 1 + 1) := by exact_mod_cast hnat
    rwa [show 2 * v + 1 + 1 = (v + 1) + (v + 1) by ring, pow_add] at this
  have hv : (0:ℝ) < (41 / 29) ^ L := by positivity
  have hu : (0:ℝ) ≤ 2 ^ (v + 1) * (26 / 15) ^ a := by positivity
  have hvu : ((41:ℝ) / 29) ^ L ≤ 2 ^ (v + 1) * (26 / 15) ^ a := by
    by_contra hcon
    have hlt := mul_self_lt_mul_self hu (lt_of_not_ge hcon)
    have hvv : ((41:ℝ) / 29) ^ L * (41 / 29) ^ L ≤ 2 ^ L := by
      rw [← mul_pow]; exact pow_le_pow_left₀ (by norm_num) (by norm_num) L
    have h3 : (3:ℝ) ^ a ≤ (26 / 15) ^ a * (26 / 15) ^ a := by
      rw [← mul_pow]; exact pow_le_pow_left₀ (by norm_num) (by norm_num) a
    have h6 : (3:ℝ) ^ a * (2 ^ (v + 1) * 2 ^ (v + 1))
        ≤ 2 ^ (v + 1) * (26 / 15) ^ a * (2 ^ (v + 1) * (26 / 15) ^ a) := by
      have e1 : (3:ℝ) ^ a * (2 ^ (v + 1) * 2 ^ (v + 1))
          ≤ (26 / 15) ^ a * (26 / 15) ^ a * (2 ^ (v + 1) * 2 ^ (v + 1)) :=
        mul_le_mul_of_nonneg_right h3 (by positivity)
      linarith
    linarith
  have hlogR : (2:ℝ) ^ L ≤ (n : ℝ) := by exact_mod_cast hlog
  have hsplit : (82 / 29 : ℝ) ^ L = 2 ^ L * (41 / 29) ^ L := by rw [← mul_pow]; norm_num
  have hnR : (0:ℝ) < n := by exact_mod_cast hn
  rw [hsplit, div_le_div_iff₀ hnR (by positivity), one_mul]
  calc (2:ℝ) ^ L * (41 / 29) ^ L ≤ (n : ℝ) * (2 ^ (v + 1) * (26 / 15) ^ a) :=
        mul_le_mul hlogR hvu hv.le hnR.le
    _ = 2 ^ (v + 1) * (26 / 15) ^ a * (n : ℝ) := by ring

theorem sum_weight_block (v L : ℕ) :
    ∑ n ∈ Finset.Ico (2 ^ L) (2 ^ (L + 1)), weight v n = 2 ^ (v + 1) * (29 / 30 : ℝ) ^ L := by
  have hcongr : ∀ n ∈ Finset.Ico (2 ^ L) (2 ^ (L + 1)),
      weight v n = 2 ^ (v + 1) / (82 / 29 : ℝ) ^ L * (26 / 15 : ℝ) ^ oddCount L n := by
    intro n hn
    obtain ⟨h1, h2⟩ := Finset.mem_Ico.mp hn
    have hlog : Nat.log 2 n = L := Nat.log_eq_of_pow_le_of_lt_pow h1 h2
    unfold weight; rw [hlog]; ring
  rw [Finset.sum_congr rfl hcongr, ← Finset.mul_sum, sum_pow_oddCount_block]
  have : (29 / 30 : ℝ) ^ L = (1 + 26 / 15) ^ L / (82 / 29) ^ L := by rw [← div_pow]; norm_num
  rw [this]; ring

theorem sum_weight_total (v M : ℕ) :
    ∑ n ∈ Finset.Ico 1 (2 ^ M), weight v n = 2 ^ (v + 1) * 30 * (1 - (29 / 30 : ℝ) ^ M) := by
  induction M with
  | zero => simp
  | succ M ih =>
    rw [← Finset.sum_Ico_consecutive _ (Nat.one_le_two_pow (n := M))
      (Nat.pow_le_pow_right (by norm_num) (Nat.le_succ M)), ih, sum_weight_block, pow_succ]
    ring

/-- **Bad mass, sharper.** For `s = 2v+1`, any finite set of positive bad integers has
reciprocal sum at most `30 * 2^(v+1)`. -/
theorem bad_mass_odd (v : ℕ) (S : Finset ℕ) (hS : ∀ n ∈ S, 0 < n ∧ ¬ Good (2 * v + 1) n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ 30 * 2 ^ (v + 1) := by
  have hsub : S ⊆ Finset.Ico 1 (2 ^ S.sup id) := by
    intro n hn
    have h1 : n ≤ S.sup id := Finset.le_sup (f := id) hn
    have h2 : n < 2 ^ n := Nat.lt_two_pow_self
    have h3 : 2 ^ n ≤ 2 ^ S.sup id := Nat.pow_le_pow_right (by norm_num) h1
    exact Finset.mem_Ico.mpr ⟨(hS n hn).1, lt_of_lt_of_le h2 h3⟩
  calc ∑ n ∈ S, (1 / (n : ℝ)) ≤ ∑ n ∈ S, weight v n :=
        Finset.sum_le_sum fun n hn => inv_le_weight (hS n hn).1 (hS n hn).2
    _ ≤ ∑ n ∈ Finset.Ico 1 (2 ^ S.sup id), weight v n :=
        Finset.sum_le_sum_of_subset_of_nonneg hsub fun n _ _ => weight_nonneg v n
    _ = 2 ^ (v + 1) * 30 * (1 - (29 / 30 : ℝ) ^ S.sup id) := sum_weight_total v _
    _ ≤ 30 * 2 ^ (v + 1) := by
        have h1 : (0:ℝ) ≤ (29 / 30) ^ S.sup id := by positivity
        have h2 : (0:ℝ) ≤ 2 ^ (v + 1) := by positivity
        nlinarith

/-- **Theorem H with constant 162.** Every distinct stretch of a `T`-trajectory has harmonic
sum `≤ 484/3 < 162` (take `s = 3`, `β = 120`). -/
theorem theoremH_162 (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k))
    (K : ℕ) (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) :
    ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) ≤ 162 := by
  have h := theoremH 3 (by norm_num) (30 * 2 ^ (1 + 1)) (bad_mass_odd 1) x hx K hinj
  refine h.trans ?_
  norm_num

end HarmonicSharp
end CollatzFMF
