import CollatzFMF.HarmonicSharp

/-!
# Product identity, residue bound (qualitative Theorem R) and cycle-length corollary (D3)

Source: `notes/round6-nov2026/w2-delta/REPORT.md` section (b), Theorem R and Corollary D;
`notes/round6-nov2026/blind-H/REPORT.md` Claim 3.

* `product_identity` : `x_k * 2^k = x_0 * 3^(a_k) * ∏_{i<k, x_i odd} (1 + 1/(3 x_i))`.
* `residue_bound` : `x_0 * 3^(a_k) ≤ x_k * 2^k ≤ exp(54) * x_0 * 3^(a_k)` on a distinct stretch.
* `cycle_pow_bounds` : a cycle with `p` distinct terms, `a` odd: `3^a < 2^p ≤ exp(54) * 3^a`.
* `cycle_sharp` : if the harmonic sum over the cycle is `≤ σ` with `exp(σ/3) < 2` (HYPOTHESES;
  in the source they come from the 2^71 verification and the numerical value 1.386, neither of
  which is formalized here), then `3^a < 2^p < 2 * 3^a`, and `p` is the least `q` with
  `3^a < 2^q`, i.e. `p = Nat.clog 2 (3^a + 1)`.

Everything in this file is complete (no `sorry`, no extra axioms).
-/

namespace CollatzFMF
namespace Sharp

open KL (T)
open Harmonic HarmonicSharp

theorem oddCount_succ_last (k n : ℕ) :
    oddCount (k + 1) n = oddCount k n + T^[k] n % 2 := by
  rw [oddCount_eq_sum, oddCount_eq_sum, Finset.sum_range_succ]

/-- The per-step factor: `1 + 1/(3m)` at odd `m`, `1` at even `m`. -/
noncomputable def oddFactor (m : ℕ) : ℝ := if m % 2 = 1 then 1 + 1 / (3 * (m : ℝ)) else 1

theorem step_real (m : ℕ) : (T m : ℝ) * 2 = (m : ℝ) * 3 ^ (m % 2) * oddFactor m := by
  rcases Nat.mod_two_eq_zero_or_one m with h | h
  · have h' : (2 : ℝ) * (T m : ℝ) = m := by exact_mod_cast two_mul_T_even h
    simp only [oddFactor, h]
    norm_num
    linarith
  · have h' : (2 : ℝ) * (T m : ℝ) = 3 * m + 1 := by exact_mod_cast two_mul_T_odd h
    have hm : (m : ℝ) ≠ 0 := by
      have : m ≠ 0 := by omega
      exact_mod_cast this
    simp only [oddFactor, h, ite_true, pow_one]
    field_simp
    linarith

theorem one_le_oddFactor (m : ℕ) : 1 ≤ oddFactor m := by
  unfold oddFactor
  split
  · have : (0 : ℝ) ≤ 1 / (3 * (m : ℝ)) := by positivity
    linarith
  · exact le_refl _

theorem oddFactor_le_exp (m : ℕ) : oddFactor m ≤ Real.exp (1 / (m : ℝ) / 3) := by
  unfold oddFactor
  split
  · have := Real.add_one_le_exp (1 / (m : ℝ) / 3)
    have e : 1 / (3 * (m : ℝ)) = 1 / (m : ℝ) / 3 := by rw [div_div, mul_comm]
    rw [e]; linarith
  · exact Real.one_le_exp (by positivity)

/-- Product identity, iterate form (no hypothesis on `n`). -/
theorem product_identity_iterate (n k : ℕ) :
    (T^[k] n : ℝ) * 2 ^ k
      = (n : ℝ) * 3 ^ oddCount k n * ∏ i ∈ Finset.range k, oddFactor (T^[i] n) := by
  induction k with
  | zero => simp [oddCount]
  | succ k ih =>
    rw [Function.iterate_succ_apply', oddCount_succ_last, Finset.prod_range_succ, pow_add,
      pow_succ]
    linear_combination (2 ^ k) * step_real (T^[k] n)
      + (3 ^ (T^[k] n % 2) * oddFactor (T^[k] n)) * ih

theorem seq_eq_iterate {x : ℕ → ℕ} (hx : ∀ k, x (k + 1) = T (x k)) (k : ℕ) :
    x k = T^[k] (x 0) := by
  have := seq_iterate hx 0 k
  rwa [Nat.zero_add] at this

/-- **Product identity.** For a `T`-sequence `x` (any start, including `0`):
`x_k * 2^k = x_0 * 3^(a_k) * ∏_{i<k, x_i odd} (1 + 1/(3 x_i))`, `a_k = oddCount k (x 0)`. -/
theorem product_identity (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (k : ℕ) :
    (x k : ℝ) * 2 ^ k
      = (x 0 : ℝ) * 3 ^ oddCount k (x 0)
        * ∏ i ∈ (Finset.range k).filter (fun i => x i % 2 = 1), (1 + 1 / (3 * (x i : ℝ))) := by
  rw [seq_eq_iterate hx k, product_identity_iterate, Finset.prod_filter]
  congr 1
  refine Finset.prod_congr rfl fun i _ => ?_
  rw [← seq_eq_iterate hx i]; rfl

/-! ### Guards: the identity on `n = 27` and `n = 7`, in cleared-denominator integer form
(cross-checked in Python: `notes/round6-nov2026/lean-sharp/crosscheck.py`).
Odd terms among the first 5 iterates of 27: `27, 41, 31, 47`; of 7: `7, 11, 17, 13`. -/
example : oddCount 5 27 = 4 := by decide
example : T^[5] 27 = 71 := by decide
example : (71 : ℚ) * 2 ^ 5 = 27 * 3 ^ 4
    * ((1 + 1 / (3 * 27)) * (1 + 1 / (3 * 41)) * (1 + 1 / (3 * 31)) * (1 + 1 / (3 * 47))) := by
  norm_num
example : oddCount 5 7 = 4 := by decide
example : T^[5] 7 = 20 := by decide
example : (20 : ℚ) * 2 ^ 5 = 7 * 3 ^ 4
    * ((1 + 1 / (3 * 7)) * (1 + 1 / (3 * 11)) * (1 + 1 / (3 * 17)) * (1 + 1 / (3 * 13))) := by
  norm_num
/-- Guard: the Lean theorem itself, instantiated at `n = 27`, `k = 5`. -/
example : (T^[5] 27 : ℝ) * 2 ^ 5 = (27 : ℝ) * 3 ^ oddCount 5 27
    * ∏ i ∈ (Finset.range 5).filter (fun i => T^[i] 27 % 2 = 1),
        (1 + 1 / (3 * (T^[i] 27 : ℝ))) := by
  have := product_identity (fun k => T^[k] 27)
    (fun k => Function.iterate_succ_apply' T k 27) 5
  simpa using this

theorem one_le_prod_oddFactor (x : ℕ → ℕ) (k : ℕ) :
    1 ≤ ∏ i ∈ Finset.range k, oddFactor (x i) := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [Finset.prod_range_succ]
    have := one_le_oddFactor (x k)
    nlinarith

theorem prod_oddFactor_le_exp_sum (x : ℕ → ℕ) (k : ℕ) :
    ∏ i ∈ Finset.range k, oddFactor (x i)
      ≤ Real.exp ((∑ i ∈ Finset.range k, (1 / (x i : ℝ))) / 3) := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [Finset.prod_range_succ, Finset.sum_range_succ, add_div, Real.exp_add]
    exact mul_le_mul ih (oddFactor_le_exp _) (le_trans zero_le_one (one_le_oddFactor _))
      (Real.exp_pos _).le

theorem prod_oddFactor_le (x : ℕ → ℕ) (k : ℕ) (σ : ℝ)
    (hσ : ∑ i ∈ Finset.range k, (1 / (x i : ℝ)) ≤ σ) :
    ∏ i ∈ Finset.range k, oddFactor (x i) ≤ Real.exp (σ / 3) :=
  (prod_oddFactor_le_exp_sum x k).trans (Real.exp_le_exp.mpr (by linarith))

/-- **Residue bound, abstract form**: any bound `σ` on the harmonic sum of the first `k` terms
gives `x_0 3^a ≤ x_k 2^k ≤ exp(σ/3) x_0 3^a`. -/
theorem residue_bound_of_sum (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (k : ℕ) (σ : ℝ)
    (hσ : ∑ i ∈ Finset.range k, (1 / (x i : ℝ)) ≤ σ) :
    (x 0 : ℝ) * 3 ^ oddCount k (x 0) ≤ (x k : ℝ) * 2 ^ k ∧
      (x k : ℝ) * 2 ^ k ≤ Real.exp (σ / 3) * ((x 0 : ℝ) * 3 ^ oddCount k (x 0)) := by
  have hid : (x k : ℝ) * 2 ^ k
      = (x 0 : ℝ) * 3 ^ oddCount k (x 0) * ∏ i ∈ Finset.range k, oddFactor (x i) := by
    rw [seq_eq_iterate hx k, product_identity_iterate]
    congr 1
    refine Finset.prod_congr rfl fun i _ => ?_
    rw [← seq_eq_iterate hx i]
  have h0 : (0 : ℝ) ≤ (x 0 : ℝ) * 3 ^ oddCount k (x 0) := by positivity
  have h1 := one_le_prod_oddFactor x k
  have h2 := prod_oddFactor_le x k σ hσ
  rw [hid]
  constructor
  · nlinarith
  · rw [mul_comm (Real.exp _)]
    exact mul_le_mul_of_nonneg_left h2 h0

/-- **Residue bound (qualitative Theorem R).** If the first `K` terms of a `T`-sequence are
pairwise distinct then for all `k ≤ K`:
`x_0 * 3^(a_k) ≤ x_k * 2^k ≤ exp(54) * x_0 * 3^(a_k)`.
The constant `exp(54) = exp(162/3)` (about `2.9e23`) is crude; the source's value is `7.62`. -/
theorem residue_bound (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (k : ℕ) (hk : k ≤ K) :
    (x 0 : ℝ) * 3 ^ oddCount k (x 0) ≤ (x k : ℝ) * 2 ^ k ∧
      (x k : ℝ) * 2 ^ k ≤ Real.exp 54 * ((x 0 : ℝ) * 3 ^ oddCount k (x 0)) := by
  have h := residue_bound_of_sum x hx k 162
    (theoremH_162 x hx k fun i hi j hj h => hinj i (by omega) j (by omega) h)
  rwa [show (162 : ℝ) / 3 = 54 by norm_num] at h

/-! ## Cycles -/

/-- The `p` terms of a cycle of minimal period `p` are pairwise distinct. -/
theorem cycle_injective (n p : ℕ) (hp : T^[p] n = n)
    (hmin : ∀ q, 0 < q → q < p → T^[q] n ≠ n) :
    ∀ i < p, ∀ j < p, T^[i] n = T^[j] n → i = j := by
  have key : ∀ i j, i < j → j < p → T^[i] n ≠ T^[j] n := by
    intro i j hij hj h
    apply hmin (j - i) (by omega) (by omega)
    have h1 : T^[p - i] (T^[i] n) = n := by
      rw [← Function.iterate_add_apply, Nat.sub_add_cancel (by omega), hp]
    have h2 : T^[p - i] (T^[j] n) = T^[j - i] n := by
      rw [← Function.iterate_add_apply, show p - i + j = (j - i) + p by omega,
        Function.iterate_add_apply, hp]
    rw [← h2, ← h, h1]
  intro i hi j hj h
  rcases Nat.lt_trichotomy i j with hlt | heq | hgt
  · exact absurd h (key i j hlt hj)
  · exact heq
  · exact absurd h.symm (key j i hgt hi)

theorem three_pow_ne_two_pow (a p : ℕ) (hp : 1 ≤ p) : 3 ^ a ≠ 2 ^ p := by
  intro h
  have h3 : 3 ^ a % 2 = 1 := by simp [Nat.pow_mod]
  have h2 : 2 ^ p % 2 = 0 := by
    obtain ⟨p', rfl⟩ : ∃ p', p = p' + 1 := ⟨p - 1, by omega⟩
    rw [pow_succ]; omega
  omega

/-- Cycle identity: `2^p = 3^a * ∏ (odd factors)` for a `p`-periodic point `n ≥ 1`. -/
theorem cycle_identity (n p : ℕ) (hn : 1 ≤ n) (hp : T^[p] n = n) :
    (2 : ℝ) ^ p = 3 ^ oddCount p n * ∏ i ∈ Finset.range p, oddFactor (T^[i] n) := by
  have h := product_identity_iterate n p
  rw [hp] at h
  have hn' : (n : ℝ) ≠ 0 := by
    have : n ≠ 0 := by omega
    exact_mod_cast this
  apply mul_left_cancel₀ hn'
  rw [h]; ring

/-- Abstract cycle bound: `3^a < 2^p` and `2^p ≤ exp(σ/3) 3^a` for any bound `σ` on the
harmonic sum over one period (no minimality needed here). -/
theorem cycle_bounds_of_sum (n p : ℕ) (hn : 1 ≤ n) (hp1 : 1 ≤ p) (hp : T^[p] n = n) (σ : ℝ)
    (hσ : ∑ i ∈ Finset.range p, (1 / (T^[i] n : ℝ)) ≤ σ) :
    3 ^ oddCount p n < 2 ^ p ∧ (2 : ℝ) ^ p ≤ Real.exp (σ / 3) * 3 ^ oddCount p n := by
  have hid := cycle_identity n p hn hp
  have h1 := one_le_prod_oddFactor (fun i => T^[i] n) p
  have h2 := prod_oddFactor_le (fun i => T^[i] n) p σ hσ
  have h3 : (0 : ℝ) < 3 ^ oddCount p n := by positivity
  constructor
  · have hle : (3 : ℝ) ^ oddCount p n ≤ 2 ^ p := by rw [hid]; nlinarith
    have hle' : 3 ^ oddCount p n ≤ 2 ^ p := by exact_mod_cast hle
    exact lt_of_le_of_ne hle' (three_pow_ne_two_pow _ _ hp1)
  · rw [hid, mul_comm (Real.exp _)]
    exact mul_le_mul_of_nonneg_left h2 h3.le

/-- **Cycle-length corollary (qualitative D3), unconditional.** If `n ≥ 1` lies on a `T`-cycle
of minimal period `p ≥ 1` and `a = oddCount p n` is the number of odd terms of the cycle, then
`3^a < 2^p` (always strict) and `2^p ≤ exp(54) * 3^a`. -/
theorem cycle_pow_bounds (n p : ℕ) (hn : 1 ≤ n) (hp1 : 1 ≤ p) (hp : T^[p] n = n)
    (hmin : ∀ q, 0 < q → q < p → T^[q] n ≠ n) :
    3 ^ oddCount p n < 2 ^ p ∧ (2 : ℝ) ^ p ≤ Real.exp 54 * 3 ^ oddCount p n := by
  have h := cycle_bounds_of_sum n p hn hp1 hp 162
    (theoremH_162 (fun k => T^[k] n) (fun k => Function.iterate_succ_apply' T k n) p
      (cycle_injective n p hp hmin))
  rwa [show (162 : ℝ) / 3 = 54 by norm_num] at h

/-- **Cycle-length corollary, conditional sharp form (D3).** HYPOTHESES `hσ`, `hσ2`: the
harmonic sum over one period is `≤ σ` and `exp(σ/3) < 2`. (In the source these follow from
"all cycle elements are `≥ 2^71`" plus the numerical evaluation `exp(σ/3) ≤ 1.386`; neither
is formalized.) CONCLUSION: `3^a < 2^p < 2 * 3^a`; `p` is the least `q` with `3^a < 2^q`;
`p = Nat.clog 2 (3^a + 1)`, i.e. `p = ⌈a log₂ 3⌉` (as `3^a` is not a power of two). -/
theorem cycle_sharp (n p : ℕ) (hn : 1 ≤ n) (hp1 : 1 ≤ p) (hp : T^[p] n = n) (σ : ℝ)
    (hσ : ∑ i ∈ Finset.range p, (1 / (T^[i] n : ℝ)) ≤ σ) (hσ2 : Real.exp (σ / 3) < 2) :
    3 ^ oddCount p n < 2 ^ p ∧ 2 ^ p < 2 * 3 ^ oddCount p n ∧
      2 ^ (p - 1) < 3 ^ oddCount p n ∧
      (∀ q, 3 ^ oddCount p n < 2 ^ q → p ≤ q) ∧
      p = Nat.clog 2 (3 ^ oddCount p n + 1) := by
  obtain ⟨h1, h2⟩ := cycle_bounds_of_sum n p hn hp1 hp σ hσ
  have h3 : (0 : ℝ) < 3 ^ oddCount p n := by positivity
  have h4 : (2 : ℝ) ^ p < 2 * 3 ^ oddCount p n := by nlinarith
  have h5 : 2 ^ p < 2 * 3 ^ oddCount p n := by exact_mod_cast h4
  have h6 : 2 ^ (p - 1) < 3 ^ oddCount p n := by
    obtain ⟨p', rfl⟩ : ∃ p', p = p' + 1 := ⟨p - 1, by omega⟩
    rw [pow_succ] at h5
    simp only [Nat.add_sub_cancel]
    omega
  have h7 : ∀ q, 3 ^ oddCount p n < 2 ^ q → p ≤ q := by
    intro q hq
    by_contra hlt
    have : 2 ^ q ≤ 2 ^ (p - 1) := Nat.pow_le_pow_right (by norm_num) (by omega)
    omega
  refine ⟨h1, h5, h6, h7, ?_⟩
  apply le_antisymm
  · apply h7
    have := Nat.le_pow_clog (b := 2) (by norm_num) (3 ^ oddCount p n + 1)
    omega
  · exact Nat.clog_le_of_le_pow (by omega)

theorem exp_two_thirds_lt_two : Real.exp (2 / 3) < 2 := by
  have he : Real.exp 1 < 2.7182818286 := Real.exp_one_lt_d9
  have h3 : Real.exp (2 / 3) ^ 3 = Real.exp 1 ^ 2 := by
    rw [← Real.exp_nat_mul, ← Real.exp_nat_mul]; norm_num
  have hpos := Real.exp_pos (2 / 3 : ℝ)
  by_contra hcon
  have hge : (2 : ℝ) ≤ Real.exp (2 / 3) := not_lt.mp hcon
  have h8 : (2 : ℝ) ^ 3 ≤ Real.exp (2 / 3) ^ 3 := pow_le_pow_left₀ (by norm_num) hge 3
  have h9 : Real.exp 1 ^ 2 < 2.7182818286 ^ 2 :=
    pow_lt_pow_left₀ he (Real.exp_pos 1).le (by norm_num)
  rw [h3] at h8
  norm_num at h8 h9
  linarith

/-- Concrete instance of the conditional form: harmonic sum over the cycle `≤ 2` suffices. -/
theorem cycle_sharp_of_sum_le_two (n p : ℕ) (hn : 1 ≤ n) (hp1 : 1 ≤ p) (hp : T^[p] n = n)
    (hσ : ∑ i ∈ Finset.range p, (1 / (T^[i] n : ℝ)) ≤ 2) :
    3 ^ oddCount p n < 2 ^ p ∧ 2 ^ p < 2 * 3 ^ oddCount p n ∧
      2 ^ (p - 1) < 3 ^ oddCount p n ∧
      (∀ q, 3 ^ oddCount p n < 2 ^ q → p ≤ q) ∧
      p = Nat.clog 2 (3 ^ oddCount p n + 1) :=
  cycle_sharp n p hn hp1 hp 2 hσ exp_two_thirds_lt_two

/-- Guard: the trivial cycle `1 → 2 → 1` (`p = 2`, `a = 1`): `3 < 4 < 6`, and the harmonic
sum `1 + 1/2 ≤ 2`, so the hypotheses of the conditional form are satisfiable. -/
example : T^[2] 1 = 1 ∧ oddCount 2 1 = 1 ∧ Nat.clog 2 (3 ^ 1 + 1) = 2 := by decide

end Sharp
end CollatzFMF
