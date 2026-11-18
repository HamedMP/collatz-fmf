import CollatzFMF.Harmonic

/-!
# Discharging the bad-mass hypothesis of Theorem H with an explicit `β`

* `oddCount_add` : the first `L` parities depend only on `x mod 2^L` (Terras periodicity).
* `sum_pow_oddCount_block` : `Σ_{2^L ≤ n < 2^(L+1)} y^(oddCount L n) = (1+y)^L`
  (generating-function form of the Terras bijection: each parity vector of length `L`
  occurs exactly once in the block).
* `bad_mass` : every finite set of positive bad integers has reciprocal sum `≤ 56 * 2^(s+1)`
  (Chernoff-type bound with rational base points `7/4 ≥ √3`, `7/5 ≤ √2`).
* `theoremH_explicit`, `theoremH_three` : Theorem H with no hypothesis on `β`.

The constant is crude (the source's exact-binomial value is `β_all(0) ≈ 19.37` for `s = 3`);
only finiteness with a rigorous explicit value is claimed here.

Everything in this file is complete (no `sorry`, no extra axioms).
-/

namespace CollatzFMF
namespace Harmonic

open KL (T)

theorem T_add_even {x : ℕ} (h : x % 2 = 0) (c : ℕ) : T (x + 2 * c) = T x + c := by
  simp only [T]; split_ifs <;> omega

theorem T_add_odd {x : ℕ} (h : x % 2 = 1) (c : ℕ) : T (x + 2 * c) = T x + 3 * c := by
  simp only [T]; split_ifs <;> omega

/-- Terras periodicity: the first `L` parities depend only on `x mod 2^L`. -/
theorem oddCount_add (L x j : ℕ) : oddCount L (x + 2 ^ L * j) = oddCount L x := by
  induction L generalizing x j with
  | zero => rfl
  | succ L ih =>
    have e : x + 2 ^ (L + 1) * j = x + 2 * (2 ^ L * j) := by rw [pow_succ]; ring
    rw [e, oddCount, oddCount]
    have hp : (x + 2 * (2 ^ L * j)) % 2 = x % 2 := by omega
    rw [hp]
    rcases Nat.mod_two_eq_zero_or_one x with h | h
    · rw [T_add_even h, ih]
    · rw [T_add_odd h, show 3 * (2 ^ L * j) = 2 ^ L * (3 * j) by ring, ih]

theorem oddCount_mod (L x : ℕ) : oddCount L (x % 2 ^ L) = oddCount L x := by
  conv_rhs => rw [← Nat.mod_add_div x (2 ^ L)]
  rw [oddCount_add]

theorem sum_range_two_mul (g : ℕ → ℝ) (N : ℕ) :
    ∑ n ∈ Finset.range (2 * N), g n = ∑ m ∈ Finset.range N, (g (2 * m) + g (2 * m + 1)) := by
  induction N with
  | zero => simp
  | succ N ih =>
    rw [show 2 * (N + 1) = 2 * N + 1 + 1 by ring, Finset.sum_range_succ, Finset.sum_range_succ,
      ih, Finset.sum_range_succ]
    ring

/-- `m ↦ (3m+2) mod N` permutes `range N` when `N` is a power of two. -/
theorem sum_affine_perm (L : ℕ) (h : ℕ → ℝ) :
    ∑ m ∈ Finset.range (2 ^ L), h ((3 * m + 2) % 2 ^ L) = ∑ m ∈ Finset.range (2 ^ L), h m := by
  have hN : 0 < 2 ^ L := by positivity
  have hinj : Set.InjOn (fun m => (3 * m + 2) % 2 ^ L) (Finset.range (2 ^ L) : Set ℕ) := by
    intro m hm m' hm' hmm
    have hm1 : m < 2 ^ L := Finset.mem_range.mp hm
    have hm2 : m' < 2 ^ L := Finset.mem_range.mp hm'
    have h1 : 3 * m + 2 ≡ 3 * m' + 2 [MOD 2 ^ L] := hmm
    have h2 : 3 * m ≡ 3 * m' [MOD 2 ^ L] := Nat.ModEq.add_right_cancel' 2 h1
    have hc : Nat.gcd (2 ^ L) 3 = 1 := Nat.Coprime.pow_left L (by norm_num)
    have h3 : m ≡ m' [MOD 2 ^ L] := Nat.ModEq.cancel_left_of_coprime hc h2
    have h4 : m % 2 ^ L = m' % 2 ^ L := h3
    rwa [Nat.mod_eq_of_lt hm1, Nat.mod_eq_of_lt hm2] at h4
  have himg : (Finset.range (2 ^ L)).image (fun m => (3 * m + 2) % 2 ^ L)
      = Finset.range (2 ^ L) := by
    apply Finset.eq_of_subset_of_card_le
    · intro n hn
      obtain ⟨m, -, rfl⟩ := Finset.mem_image.mp hn
      exact Finset.mem_range.mpr (Nat.mod_lt _ hN)
    · rw [Finset.card_image_of_injOn hinj]
  conv_rhs => rw [← himg]
  rw [Finset.sum_image hinj]

/-- Generating-function form of the Terras bijection on residues mod `2^L`. -/
theorem sum_pow_oddCount (y : ℝ) (L : ℕ) :
    ∑ m ∈ Finset.range (2 ^ L), y ^ oddCount L m = (1 + y) ^ L := by
  induction L with
  | zero => simp [oddCount]
  | succ L ih =>
    rw [pow_succ 2 L, Nat.mul_comm, sum_range_two_mul, Finset.sum_add_distrib]
    have he : ∀ m, oddCount (L + 1) (2 * m) = oddCount L m := fun m => by
      rw [oddCount, KL.T_two_mul]; omega
    have ho : ∀ m, oddCount (L + 1) (2 * m + 1) = 1 + oddCount L ((3 * m + 2) % 2 ^ L) := by
      intro m
      have hT : T (2 * m + 1) = 3 * m + 2 := by unfold T; split <;> omega
      rw [oddCount, hT, oddCount_mod]; omega
    simp only [he, ho, pow_add, pow_one]
    rw [← Finset.mul_sum, sum_affine_perm L (fun n => y ^ oddCount L n), ih]
    ring

/-- Terras, block form: over the integers of level `L` the parity vectors of length `L`
occur exactly once each, so `Σ y^a = (1+y)^L`. -/
theorem sum_pow_oddCount_block (y : ℝ) (L : ℕ) :
    ∑ n ∈ Finset.Ico (2 ^ L) (2 ^ (L + 1)), y ^ oddCount L n = (1 + y) ^ L := by
  rw [Finset.sum_Ico_eq_sum_range]
  have : 2 ^ (L + 1) - 2 ^ L = 2 ^ L := by rw [pow_succ]; omega
  rw [this, ← sum_pow_oddCount y L]
  refine Finset.sum_congr rfl fun k _ => ?_
  have := oddCount_add L k 1
  rw [Nat.mul_one] at this
  rw [Nat.add_comm, this]

/-- Chernoff weight dominating the reciprocal of a bad integer. -/
noncomputable def weight (s n : ℕ) : ℝ :=
  2 ^ (s + 1) * (7 / 4 : ℝ) ^ oddCount (Nat.log 2 n) n / (14 / 5 : ℝ) ^ Nat.log 2 n

theorem weight_nonneg (s n : ℕ) : 0 ≤ weight s n := by unfold weight; positivity

theorem inv_le_weight {s n : ℕ} (hn : 0 < n) (hb : ¬ Good s n) : 1 / (n : ℝ) ≤ weight s n := by
  unfold Good at hb
  unfold weight
  have hlog : 2 ^ Nat.log 2 n ≤ n := Nat.pow_log_le_self 2 hn.ne'
  generalize Nat.log 2 n = L at *
  generalize oddCount L n = a at *
  -- integer consequence of badness: 2^L < 3^a * 2^(s+1)
  have hnat : 2 ^ L < 3 ^ a * 2 ^ (s + 1) := by
    have h1 : 2 ^ (L + a) < 3 ^ a * (2 ^ a + 1) * 2 ^ s := Nat.lt_of_not_le hb
    have h2 : (2:ℕ) ^ a + 1 ≤ 2 * 2 ^ a := by
      have : 0 < 2 ^ a := by positivity
      omega
    have h3 : 3 ^ a * (2 ^ a + 1) * 2 ^ s ≤ 3 ^ a * (2 * 2 ^ a) * 2 ^ s :=
      Nat.mul_le_mul_right _ (Nat.mul_le_mul_left _ h2)
    have h4 : 2 ^ L * 2 ^ a < 3 ^ a * 2 ^ (s + 1) * 2 ^ a := by
      calc 2 ^ L * 2 ^ a = 2 ^ (L + a) := (pow_add 2 L a).symm
        _ < 3 ^ a * (2 ^ a + 1) * 2 ^ s := h1
        _ ≤ 3 ^ a * (2 * 2 ^ a) * 2 ^ s := h3
        _ = 3 ^ a * 2 ^ (s + 1) * 2 ^ a := by rw [pow_succ]; ring
    exact Nat.lt_of_mul_lt_mul_right h4
  have hreal : (2:ℝ) ^ L < 3 ^ a * 2 ^ (s + 1) := by exact_mod_cast hnat
  have hv : (0:ℝ) < (7 / 5) ^ L := by positivity
  have hu : (0:ℝ) ≤ 2 ^ (s + 1) * (7 / 4) ^ a := by positivity
  have hvu : ((7:ℝ) / 5) ^ L ≤ 2 ^ (s + 1) * (7 / 4) ^ a := by
    by_contra hcon
    have hlt := mul_self_lt_mul_self hu (lt_of_not_ge hcon)
    have hvv : ((7:ℝ) / 5) ^ L * (7 / 5) ^ L ≤ 2 ^ L := by
      rw [← mul_pow]; exact pow_le_pow_left₀ (by norm_num) (by norm_num) L
    have h3 : (3:ℝ) ^ a ≤ (7 / 4) ^ a * (7 / 4) ^ a := by
      rw [← mul_pow]; exact pow_le_pow_left₀ (by norm_num) (by norm_num) a
    have h1 : (1:ℝ) ≤ 2 ^ (s + 1) := one_le_pow₀ (by norm_num)
    have h5 : (0:ℝ) < 3 ^ a := by positivity
    have h6 : (3:ℝ) ^ a * 2 ^ (s + 1) ≤ 2 ^ (s + 1) * (7 / 4) ^ a * (2 ^ (s + 1) * (7 / 4) ^ a) := by
      have e1 : (3:ℝ) ^ a * 2 ^ (s + 1) ≤ (7 / 4) ^ a * (7 / 4) ^ a * 2 ^ (s + 1) :=
        mul_le_mul_of_nonneg_right h3 (by positivity)
      have e2 : ((7:ℝ) / 4) ^ a * (7 / 4) ^ a * 2 ^ (s + 1) * 1
          ≤ (7 / 4) ^ a * (7 / 4) ^ a * 2 ^ (s + 1) * 2 ^ (s + 1) :=
        mul_le_mul_of_nonneg_left h1 (by positivity)
      linarith
    linarith
  have hlogR : (2:ℝ) ^ L ≤ (n : ℝ) := by exact_mod_cast hlog
  have hsplit : (14 / 5 : ℝ) ^ L = 2 ^ L * (7 / 5) ^ L := by rw [← mul_pow]; norm_num
  have hnR : (0:ℝ) < n := by exact_mod_cast hn
  rw [hsplit, div_le_div_iff₀ hnR (by positivity), one_mul]
  have h2pos : (0:ℝ) ≤ 2 ^ L := by positivity
  calc (2:ℝ) ^ L * (7 / 5) ^ L ≤ (n : ℝ) * (2 ^ (s + 1) * (7 / 4) ^ a) :=
        mul_le_mul hlogR hvu hv.le hnR.le
    _ = 2 ^ (s + 1) * (7 / 4) ^ a * (n : ℝ) := by ring

theorem sum_weight_block (s L : ℕ) :
    ∑ n ∈ Finset.Ico (2 ^ L) (2 ^ (L + 1)), weight s n = 2 ^ (s + 1) * (55 / 56 : ℝ) ^ L := by
  have hcongr : ∀ n ∈ Finset.Ico (2 ^ L) (2 ^ (L + 1)),
      weight s n = 2 ^ (s + 1) / (14 / 5 : ℝ) ^ L * (7 / 4 : ℝ) ^ oddCount L n := by
    intro n hn
    obtain ⟨h1, h2⟩ := Finset.mem_Ico.mp hn
    have hlog : Nat.log 2 n = L := Nat.log_eq_of_pow_le_of_lt_pow h1 h2
    unfold weight; rw [hlog]; ring
  rw [Finset.sum_congr rfl hcongr, ← Finset.mul_sum, sum_pow_oddCount_block]
  have : (55 / 56 : ℝ) ^ L = (1 + 7 / 4) ^ L / (14 / 5) ^ L := by rw [← div_pow]; norm_num
  rw [this]; ring

theorem sum_weight_total (s M : ℕ) :
    ∑ n ∈ Finset.Ico 1 (2 ^ M), weight s n = 2 ^ (s + 1) * 56 * (1 - (55 / 56 : ℝ) ^ M) := by
  induction M with
  | zero => simp
  | succ M ih =>
    rw [← Finset.sum_Ico_consecutive _ (Nat.one_le_two_pow (n := M))
      (Nat.pow_le_pow_right (by norm_num) (Nat.le_succ M)), ih, sum_weight_block, pow_succ]
    ring

/-- **Bad mass is finite, explicitly.** Any finite set of positive bad integers has
reciprocal sum at most `56 * 2^(s+1)`. -/
theorem bad_mass (s : ℕ) (S : Finset ℕ) (hS : ∀ n ∈ S, 0 < n ∧ ¬ Good s n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ 56 * 2 ^ (s + 1) := by
  have hsub : S ⊆ Finset.Ico 1 (2 ^ S.sup id) := by
    intro n hn
    have h1 : n ≤ S.sup id := Finset.le_sup (f := id) hn
    have h2 : n < 2 ^ n := Nat.lt_two_pow_self
    have h3 : 2 ^ n ≤ 2 ^ S.sup id := Nat.pow_le_pow_right (by norm_num) h1
    exact Finset.mem_Ico.mpr ⟨(hS n hn).1, lt_of_lt_of_le h2 h3⟩
  calc ∑ n ∈ S, (1 / (n : ℝ)) ≤ ∑ n ∈ S, weight s n :=
        Finset.sum_le_sum fun n hn => inv_le_weight (hS n hn).1 (hS n hn).2
    _ ≤ ∑ n ∈ Finset.Ico 1 (2 ^ S.sup id), weight s n :=
        Finset.sum_le_sum_of_subset_of_nonneg hsub fun n _ _ => weight_nonneg s n
    _ = 2 ^ (s + 1) * 56 * (1 - (55 / 56 : ℝ) ^ S.sup id) := sum_weight_total s _
    _ ≤ 56 * 2 ^ (s + 1) := by
        have h1 : (0:ℝ) ≤ (55 / 56) ^ S.sup id := by positivity
        have h2 : (0:ℝ) ≤ 2 ^ (s + 1) := by positivity
        nlinarith

/-- **Theorem H, hypothesis-free.** For every `T`-sequence whose first `K` terms are pairwise
distinct and every `s ≥ 2`: `Σ_{k<K} 1/x_k ≤ (56·2^(s+1) + 1)/(1 - 2^(1-s))`. -/
theorem theoremH_explicit (s : ℕ) (hs : 2 ≤ s) (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k))
    (K : ℕ) (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) :
    ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) ≤ (56 * 2 ^ (s + 1) + 1) / (1 - 2 / 2 ^ s) :=
  theoremH s hs _ (bad_mass s) x hx K hinj

/-- The case `s = 3`: every distinct stretch of a `T`-trajectory has harmonic sum `≤ 1196`. -/
theorem theoremH_three (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k))
    (K : ℕ) (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) :
    ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) ≤ 1196 := by
  refine (theoremH_explicit 3 (by norm_num) x hx K hinj).trans (le_of_eq ?_)
  norm_num

end Harmonic
end CollatzFMF
