import CollatzFMF.ConstH

/-!
# Cycle length above `2^71`, sharper residue bounds, and the conditional residue split

Source: `notes/round6-nov2026/w2-delta/REPORT.md` section (b), Theorem R and Corollary D (D3).

* `cycle_length_above_71` : a `T`-cycle of minimal period `p` all of whose elements are
  `≥ 2^71`, with `a` odd elements, has `3^a < 2^p < 2·3^a`, i.e. `p = clog₂(3^a + 1)`.
  NO further hypothesis (no numerical input, no verification input).
* `residue_bound_1045`, `cycle_pow_bounds_1045` : the unconditional residue bound with
  `exp(1567/150)` (about `3.4e4`) in place of `exp(54)`.
* `residue_above_71` : on a distinct stretch with all terms `≥ 2^71` the ratio is `≤ exp(23/50)`.
* `SmallHyp M E P` : the single computational hypothesis of Theorem R (a `Prop`, NOT asserted).
* `residue_split` : `SmallHyp M E P` ⇒ ratio `≤ E · exp(U/3)` for every distinct stretch.
* `residue_split_32` : the instance `M = 32`, `P = 497`: ratio `≤ E · exp(5591/2500)`.

Everything in this file is complete (no `sorry`, no extra axioms, no `native_decide`).
-/

namespace CollatzFMF
namespace Const

open KL (T)
open Harmonic Sharp

/-! ## Cycles above `2^71` -/

/-- **Cycle length above `2^71` (Corollary D3, kernel-checked, hypothesis-free).** If `n` lies
on a `T`-cycle of minimal period `p ≥ 1` and every element of the cycle is `≥ 2^71`, then with
`a = oddCount p n` (the number of odd elements): `3^a < 2^p < 2·3^a`, `p` is the least `q`
with `3^a < 2^q`, and `p = Nat.clog 2 (3^a + 1)` (i.e. `p = ⌈a log₂ 3⌉`). -/
theorem cycle_length_above_71 (n p : ℕ) (hp1 : 1 ≤ p) (hp : T^[p] n = n)
    (hmin : ∀ q, 0 < q → q < p → T^[q] n ≠ n) (hbig : ∀ i < p, 2 ^ 71 ≤ T^[i] n) :
    3 ^ oddCount p n < 2 ^ p ∧ 2 ^ p < 2 * 3 ^ oddCount p n ∧
      2 ^ (p - 1) < 3 ^ oddCount p n ∧
      (∀ q, 3 ^ oddCount p n < 2 ^ q → p ≤ q) ∧
      p = Nat.clog 2 (3 ^ oddCount p n + 1) := by
  have hn : 1 ≤ n := by
    have h0 : 2 ^ 71 ≤ n := hbig 0 (by omega)
    exact le_trans (Nat.one_le_two_pow) h0
  have hσ := harmonic_ge_71 (fun k => T^[k] n) (fun k => Function.iterate_succ_apply' T k n) p
    (cycle_injective n p hp hmin) hbig
  exact cycle_sharp_of_sum_le_two n p hn hp1 hp (hσ.trans (by norm_num))

/-- Quantitative form: on such a cycle `2^p ≤ exp(23/50) · 3^a` (`exp(0.46) ≈ 1.584`;
refereed value `1.386`). -/
theorem cycle_ratio_above_71 (n p : ℕ) (hp1 : 1 ≤ p) (hp : T^[p] n = n)
    (hmin : ∀ q, 0 < q → q < p → T^[q] n ≠ n) (hbig : ∀ i < p, 2 ^ 71 ≤ T^[i] n) :
    (2 : ℝ) ^ p ≤ Real.exp (23 / 50) * 3 ^ oddCount p n := by
  have hn : 1 ≤ n := by
    have h0 : 2 ^ 71 ≤ n := hbig 0 (by omega)
    exact le_trans (Nat.one_le_two_pow) h0
  have hσ := harmonic_ge_71 (fun k => T^[k] n) (fun k => Function.iterate_succ_apply' T k n) p
    (cycle_injective n p hp hmin) hbig
  have h := (cycle_bounds_of_sum n p hn hp1 hp (69 / 50) hσ).2
  rwa [show (69 : ℝ) / 50 / 3 = 23 / 50 by norm_num] at h

/-- Guard: the hypotheses of `cycle_length_above_71` minus the size condition are satisfied
by the trivial cycle `1 → 2 → 1`, for which the conclusion holds too (`3 < 4 < 6`). The size
condition is what the published verification below `2^71` supplies for nontrivial cycles. -/
example : T^[2] 1 = 1 ∧ (∀ q, 0 < q → q < 2 → T^[q] 1 ≠ 1) ∧ oddCount 2 1 = 1 ∧
    3 ^ 1 < 2 ^ 2 ∧ 2 ^ 2 < 2 * 3 ^ 1 ∧ 2 = Nat.clog 2 (3 ^ 1 + 1) := by
  refine ⟨by decide, ?_, by decide, by decide, by decide, by decide⟩
  intro q h1 h2
  have : q = 1 := by omega
  subst this
  decide

/-! ## Unconditional residue bounds with the sharper constant -/

/-- **Residue bound, `exp(1567/150)`** (`≈ 3.4e4`; was `exp(54) ≈ 2.8e23`; refereed `7.62`). -/
theorem residue_bound_1045 (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (k : ℕ) (hk : k ≤ K) :
    (x 0 : ℝ) * 3 ^ oddCount k (x 0) ≤ (x k : ℝ) * 2 ^ k ∧
      (x k : ℝ) * 2 ^ k ≤ Real.exp (1567 / 150) * ((x 0 : ℝ) * 3 ^ oddCount k (x 0)) := by
  have h := residue_bound_of_sum x hx k (1567 / 50)
    (theoremH_3134 x hx k fun i hi j hj h => hinj i (by omega) j (by omega) h)
  rwa [show (1567 : ℝ) / 50 / 3 = 1567 / 150 by norm_num] at h

/-- Cycle exponent bounds, unconditional, with `exp(1567/150)`. -/
theorem cycle_pow_bounds_1045 (n p : ℕ) (hn : 1 ≤ n) (hp1 : 1 ≤ p) (hp : T^[p] n = n)
    (hmin : ∀ q, 0 < q → q < p → T^[q] n ≠ n) :
    3 ^ oddCount p n < 2 ^ p ∧ (2 : ℝ) ^ p ≤ Real.exp (1567 / 150) * 3 ^ oddCount p n := by
  have h := cycle_bounds_of_sum n p hn hp1 hp (1567 / 50)
    (theoremH_3134 (fun k => T^[k] n) (fun k => Function.iterate_succ_apply' T k n) p
      (cycle_injective n p hp hmin))
  rwa [show (1567 : ℝ) / 50 / 3 = 1567 / 150 by norm_num] at h

/-- Residue bound on a distinct stretch all of whose terms are `≥ 2^71`: ratio in
`[1, exp(23/50)]` (refereed: `1.386`). -/
theorem residue_above_71 (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (hbig : ∀ i < K, 2 ^ 71 ≤ x i)
    (k : ℕ) (hk : k ≤ K) :
    (x 0 : ℝ) * 3 ^ oddCount k (x 0) ≤ (x k : ℝ) * 2 ^ k ∧
      (x k : ℝ) * 2 ^ k ≤ Real.exp (23 / 50) * ((x 0 : ℝ) * 3 ^ oddCount k (x 0)) := by
  have h := residue_bound_of_sum x hx k (69 / 50)
    (harmonic_ge_71 x hx k (fun i hi j hj h => hinj i (by omega) j (by omega) h)
      (fun i hi => hbig i (by omega)))
  rwa [show (69 : ℝ) / 50 / 3 = 23 / 50 by norm_num] at h

/-! ## The conditional split (Theorem R with one computational hypothesis) -/

/-- **The computational hypothesis of Theorem R at `B = 2^M`** (a `Prop`; it is NOT asserted
anywhere in this development). For every start `n < 2^M` and every pairwise distinct initial
stretch of its trajectory: the product of the odd factors `1 + 1/(3x)` over the terms
`x < 2^M` of the stretch is `≤ E`, and the stretch has at most `P` terms `< 2^M`.

Source values at `M = 32` (run `s5`, not formalized): every `n < 2^32` reaches `1`, the odd
log-sum excluding the term `1` is `≤ M_B = 0.2256541127`, and a trajectory has at most
`P_B = 495` terms below `2^32`; hence `E = (4/3)·exp(0.2256541127)` and `P = 497`. -/
def SmallHyp (M : ℕ) (E : ℝ) (P : ℕ) : Prop :=
  ∀ n K : ℕ, n < 2 ^ M → (∀ i < K, ∀ j < K, T^[i] n = T^[j] n → i = j) →
    (∏ i ∈ (Finset.range K).filter (fun i => T^[i] n < 2 ^ M), oddFactor (T^[i] n)) ≤ E ∧
    ((Finset.range K).filter (fun i => T^[i] n < 2 ^ M)).card ≤ P

/-- Guard: the hypothesis is satisfiable in a small case and has the intended content:
`SmallHyp 1 (4/3) 1` (the only starts are `0` and `1`; `T 1 = 2 ≥ 2^1`, `T 2 = 1` repeats). -/
example : SmallHyp 1 (4 / 3) 1 := by
  intro n K hn hinj
  have hK : K ≤ 2 := by
    by_contra hK
    have hn' : n = 0 ∨ n = 1 := by omega
    rcases hn' with rfl | rfl
    · have := hinj 0 (by omega) 1 (by omega) (by decide); omega
    · have := hinj 0 (by omega) 2 (by omega) (by decide); omega
  have hn' : n = 0 ∨ n = 1 := by omega
  have hK' : K = 0 ∨ K = 1 ∨ K = 2 := by omega
  rcases hn' with rfl | rfl <;> rcases hK' with rfl | rfl | rfl
  · constructor <;> norm_num
  · constructor
    · rw [show (Finset.range 1).filter (fun i => T^[i] 0 < 2 ^ 1) = {0} by decide]
      norm_num [oddFactor]
    · decide
  · exact absurd (hinj 0 (by omega) 1 (by omega) (by decide)) (by omega)
  · constructor <;> norm_num
  · constructor
    · rw [show (Finset.range 1).filter (fun i => T^[i] 1 < 2 ^ 1) = {0} by decide]
      norm_num [oddFactor]
    · decide
  · constructor
    · rw [show (Finset.range 2).filter (fun i => T^[i] 1 < 2 ^ 1) = {0} by decide]
      norm_num [oddFactor]
    · decide

theorem prod_oddFactor_filter_le (x : ℕ → ℕ) (F : Finset ℕ) :
    ∏ i ∈ F, oddFactor (x i) ≤ Real.exp ((∑ i ∈ F, (1 / (x i : ℝ))) / 3) := by
  rw [Finset.sum_div, Real.exp_sum]
  exact Finset.prod_le_prod₀ (fun i _ => le_trans zero_le_one (one_le_oddFactor _))
    (fun i _ => oddFactor_le_exp _)

/-- The small terms of a distinct stretch lie on the trajectory of the first small term. -/
theorem small_part (M : ℕ) (E : ℝ) (P : ℕ) (h : SmallHyp M E P)
    (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) :
    (∏ i ∈ (Finset.range K).filter (fun i => x i < 2 ^ M), oddFactor (x i)) ≤ E ∧
    ((Finset.range K).filter (fun i => x i < 2 ^ M)).card ≤ P := by
  by_cases hex : ∃ i, i < K ∧ x i < 2 ^ M
  · classical
    set i0 := Nat.find hex with hi0
    obtain ⟨hi0K, hi0s⟩ := Nat.find_spec hex
    have hmin : ∀ i, i < i0 → ¬ x i < 2 ^ M := fun i hi hs =>
      Nat.find_min hex hi ⟨by omega, hs⟩
    have hit : ∀ j, T^[j] (x i0) = x (i0 + j) := fun j => (seq_iterate hx i0 j).symm
    obtain ⟨h1, h2⟩ := h (x i0) (K - i0) hi0s (by
      intro i hi j hj hij
      rw [hit, hit] at hij
      have := hinj (i0 + i) (by omega) (i0 + j) (by omega) hij
      omega)
    have hK : K = i0 + (K - i0) := by omega
    constructor
    · rw [Finset.prod_filter] at h1 ⊢
      rw [hK, Finset.prod_range_add]
      have hfirst : ∏ i ∈ Finset.range i0, (if x i < 2 ^ M then oddFactor (x i) else 1) = 1 :=
        Finset.prod_eq_one fun i hi => if_neg (hmin i (Finset.mem_range.mp hi))
      rw [hfirst, one_mul]
      simpa only [hit] using h1
    · rw [Finset.card_filter] at h2 ⊢
      rw [hK, Finset.sum_range_add]
      have hfirst : ∑ i ∈ Finset.range i0, (if x i < 2 ^ M then 1 else 0) = 0 :=
        Finset.sum_eq_zero fun i hi => if_neg (hmin i (Finset.mem_range.mp hi))
      rw [hfirst, Nat.zero_add]
      simpa only [hit] using h2
  · have hempty : (Finset.range K).filter (fun i => x i < 2 ^ M) = ∅ := by
      apply Finset.filter_eq_empty_iff.mpr
      intro i hi hs
      exact hex ⟨i, Finset.mem_range.mp hi, hs⟩
    obtain ⟨h1, -⟩ := h 0 0 (Nat.pow_pos (by norm_num)) (by intro i hi; omega)
    rw [hempty]
    constructor
    · simpa using h1
    · simp

/-- **Theorem R, conditional split form.** Assume the computational hypothesis
`SmallHyp M E P` and a bad-mass bound `β` for integers `≥ 2^M` (the latter is PROVED for
`M = 32`: `bad_mass_32`). Then on every pairwise distinct stretch, for all `k ≤ K`:
`x_0 3^(a_k) ≤ x_k 2^k ≤ E · exp(U/3) · x_0 3^(a_k)` with
`U = (β + (M+1)/2^M + 2P/2^M) / (1 - 2^(1-s))`. -/
theorem residue_split (M : ℕ) (E : ℝ) (P : ℕ) (h : SmallHyp M E P)
    (s : ℕ) (hs : 2 ≤ s) (β : ℝ)
    (hβ : ∀ S : Finset ℕ, (∀ n ∈ S, 2 ^ M ≤ n ∧ ¬ Good s n) → ∑ n ∈ S, (1 / (n : ℝ)) ≤ β)
    (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (k : ℕ) (hk : k ≤ K) :
    (x 0 : ℝ) * 3 ^ oddCount k (x 0) ≤ (x k : ℝ) * 2 ^ k ∧
      (x k : ℝ) * 2 ^ k
        ≤ E * Real.exp ((β + (M + 1) / 2 ^ M + (P : ℝ) * (2 / 2 ^ M)) / (1 - 2 / 2 ^ s) / 3)
          * ((x 0 : ℝ) * 3 ^ oddCount k (x 0)) := by
  have hinjk : ∀ i < k, ∀ j < k, x i = x j → i = j := fun i hi j hj e =>
    hinj i (by omega) j (by omega) e
  have hid : (x k : ℝ) * 2 ^ k
      = (x 0 : ℝ) * 3 ^ oddCount k (x 0) * ∏ i ∈ Finset.range k, oddFactor (x i) := by
    rw [seq_eq_iterate hx k, product_identity_iterate]
    congr 1
    refine Finset.prod_congr rfl fun i _ => ?_
    rw [← seq_eq_iterate hx i]
  have h0 : (0 : ℝ) ≤ (x 0 : ℝ) * 3 ^ oddCount k (x 0) := by positivity
  have h1 := one_le_prod_oddFactor x k
  obtain ⟨hsmall, hcard⟩ := small_part M E P h x hx k hinjk
  have hq : (2 : ℝ) / 2 ^ s ≤ 1 / 2 := by
    have h4 : (2 : ℝ) ^ 2 ≤ 2 ^ s := pow_le_pow_right₀ (by norm_num) hs
    rw [div_le_div_iff₀ (by positivity) (by norm_num)]
    linarith
  have hden : (0 : ℝ) < 1 - 2 / 2 ^ s := by linarith
  have hU : ∑ i ∈ (Finset.range k).filter (fun i => 2 ^ M ≤ x i), (1 / (x i : ℝ))
      ≤ (β + (M + 1) / 2 ^ M + (P : ℝ) * (2 / 2 ^ M)) / (1 - 2 / 2 ^ s) := by
    refine (theoremH_split s hs M β hβ x hx k hinjk).trans ?_
    apply div_le_div_of_nonneg_right _ hden.le
    have hc : (((Finset.range k).filter (fun i => x i < 2 ^ M)).card : ℝ) ≤ (P : ℝ) := by
      exact_mod_cast hcard
    have hpos : (0 : ℝ) ≤ 2 / 2 ^ M := by positivity
    nlinarith [mul_le_mul_of_nonneg_right hc hpos]
  have hfe : (Finset.range k).filter (fun i => ¬ x i < 2 ^ M)
      = (Finset.range k).filter (fun i => 2 ^ M ≤ x i) :=
    Finset.filter_congr fun i _ => not_lt
  have hbigprod : ∏ i ∈ (Finset.range k).filter (fun i => 2 ^ M ≤ x i), oddFactor (x i)
      ≤ Real.exp ((β + (M + 1) / 2 ^ M + (P : ℝ) * (2 / 2 ^ M)) / (1 - 2 / 2 ^ s) / 3) :=
    (prod_oddFactor_filter_le x _).trans (Real.exp_le_exp.mpr (by linarith))
  have hE : (0 : ℝ) ≤ E := le_trans
    (Finset.prod_nonneg fun i _ => le_trans zero_le_one (one_le_oddFactor _)) hsmall
  have hprod : ∏ i ∈ Finset.range k, oddFactor (x i)
      ≤ E * Real.exp ((β + (M + 1) / 2 ^ M + (P : ℝ) * (2 / 2 ^ M)) / (1 - 2 / 2 ^ s) / 3) := by
    rw [← Finset.prod_filter_mul_prod_filter_not (Finset.range k) (fun i => x i < 2 ^ M), hfe]
    exact mul_le_mul hsmall hbigprod
      (Finset.prod_nonneg fun i _ => le_trans zero_le_one (one_le_oddFactor _)) hE
  rw [hid]
  constructor
  · nlinarith
  · calc (x 0 : ℝ) * 3 ^ oddCount k (x 0) * ∏ i ∈ Finset.range k, oddFactor (x i)
        ≤ (x 0 : ℝ) * 3 ^ oddCount k (x 0)
          * (E * Real.exp ((β + (M + 1) / 2 ^ M + (P : ℝ) * (2 / 2 ^ M))
              / (1 - 2 / 2 ^ s) / 3)) := mul_le_mul_of_nonneg_left hprod h0
      _ = _ := by ring

/-- **Theorem R at `B = 2^32`, conditional on exactly one computational fact.**
`SmallHyp 32 E 497` ⇒ on every distinct stretch `x_k 2^k ≤ E · exp(5591/2500) · x_0 3^(a_k)`.
With the source's `E = (4/3)·exp(0.2256541127)` this is `≤ 15.65` (refereed: `7.62`; the
gap is the odd-only refinement `W_odd` and the logarithmic block refinement, neither
formalized). -/
theorem residue_split_32 (E : ℝ) (h : SmallHyp 32 E 497)
    (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (k : ℕ) (hk : k ≤ K) :
    (x 0 : ℝ) * 3 ^ oddCount k (x 0) ≤ (x k : ℝ) * 2 ^ k ∧
      (x k : ℝ) * 2 ^ k ≤ E * Real.exp (5591 / 2500) * ((x 0 : ℝ) * 3 ^ oddCount k (x 0)) := by
  obtain ⟨h1, h2⟩ := residue_split 32 E 497 h 3 (by norm_num) _ bad_mass_32 x hx K hinj k hk
  refine ⟨h1, h2.trans ?_⟩
  have hE : (0 : ℝ) ≤ E := by
    obtain ⟨hh, -⟩ := h 0 0 (by norm_num) (by intro i hi; omega)
    have : (1 : ℝ) ≤ E := by simpa using hh
    linarith
  have h0 : (0 : ℝ) ≤ (x 0 : ℝ) * 3 ^ oddCount k (x 0) := by positivity
  apply mul_le_mul_of_nonneg_right _ h0
  apply mul_le_mul_of_nonneg_left _ hE
  apply Real.exp_le_exp.mpr
  norm_num

end Const
end CollatzFMF
