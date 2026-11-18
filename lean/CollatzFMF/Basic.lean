import Mathlib

/-!
# Basic definitions: Collatz step, the conjecture, 2-adic valuation, Syracuse form

Goal 1 of the round-6 Lean track.  Everything in this file is complete
(no `sorry`, no extra axioms).
-/

namespace CollatzFMF

/-- The Collatz function `C(n) = n/2` (n even), `3n+1` (n odd)  (proof.md §1). -/
def collatzStep (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else 3 * n + 1

/-- The Collatz conjecture in its standard form: every `n ≥ 1` reaches `1`. -/
def CollatzConjecture : Prop :=
  ∀ n : ℕ, 1 ≤ n → ∃ k : ℕ, collatzStep^[k] n = 1

/-- 2-adic valuation `v_2(n)` (with the Mathlib convention `v2 0 = 0`). -/
def v2 (n : ℕ) : ℕ := padicValNat 2 n

/-! ### Misformalization tests for `collatzStep` -/

example : collatzStep 1 = 4 := by decide
example : collatzStep 4 = 2 := by decide
example : collatzStep 27 = 82 := by decide
example : collatzStep 82 = 41 := by decide
example : collatzStep^[3] 1 = 1 := by decide
example : collatzStep^[16] 7 = 1 := by decide
set_option maxRecDepth 100000 in
example : collatzStep^[111] 27 = 1 := by decide
set_option maxRecDepth 100000 in
example : ∀ k < 16, collatzStep^[k] 7 ≠ 1 := by decide

/-! ### Elementary lemmas -/

theorem collatzStep_even (n : ℕ) : collatzStep (2 * n) = n := by
  simp [collatzStep]

theorem collatzStep_odd {n : ℕ} (h : n % 2 = 1) : collatzStep n = 3 * n + 1 := by
  simp [collatzStep, h]

theorem collatzStep_iter_two_pow (a q : ℕ) : collatzStep^[a] (2 ^ a * q) = q := by
  induction a with
  | zero => simp
  | succ a ih =>
    rw [Function.iterate_succ_apply, pow_succ, mul_assoc, mul_comm 2 q, ← mul_assoc,
      mul_comm (2 ^ a * q) 2, collatzStep_even, ih]

theorem collatzStep_iter_one (i : ℕ) :
    collatzStep^[i] 1 = 1 ∨ collatzStep^[i] 1 = 2 ∨ collatzStep^[i] 1 = 4 := by
  induction i with
  | zero => simp
  | succ i ih =>
    rw [Function.iterate_succ_apply']
    rcases ih with h | h | h <;> rw [h] <;> decide

/-- Every nonzero `n` is `2 ^ v2 n * m` with `m` odd. -/
theorem exists_odd_mul (n : ℕ) (hn : n ≠ 0) : ∃ m, m % 2 = 1 ∧ n = 2 ^ v2 n * m := by
  obtain ⟨m, hm⟩ : 2 ^ v2 n ∣ n := by
    unfold v2; rw [Nat.padicValNat_def]; exact pow_multiplicity_dvd 2 n
  refine ⟨m, ?_, hm⟩
  by_contra hodd
  obtain ⟨c, rfl⟩ : 2 ∣ m := Nat.dvd_of_mod_eq_zero (by omega)
  have h : ¬ 2 ^ (v2 n + 1) ∣ n := by
    unfold v2; rw [Nat.padicValNat_def]; exact pow_succ_multiplicity_not_dvd (p := 2) hn
  apply h
  exact ⟨c, by rw [pow_succ, mul_assoc]; exact hm⟩

/-- Uniqueness of the decomposition `2^a * (odd)`. -/
theorem two_pow_mul_odd_unique {a b m m' : ℕ} (hm : m % 2 = 1) (hm' : m' % 2 = 1)
    (h : 2 ^ a * m = 2 ^ b * m') : a = b := by
  have key : ∀ a b m m' : ℕ, m % 2 = 1 → 2 ^ a * m = 2 ^ b * m' → ¬ a < b := by
    intro a b m m' hm h hab
    obtain ⟨d, rfl⟩ : ∃ d, b = a + (d + 1) := ⟨b - a - 1, by omega⟩
    rw [pow_add, mul_assoc] at h
    have h2 := Nat.eq_of_mul_eq_mul_left (Nat.two_pow_pos a) h
    rw [pow_succ] at h2
    have : m = 2 * (2 ^ d * m') := by rw [h2]; ring
    omega
  have h1 := key a b m m' hm h
  have h2 := key b a m' m hm' h.symm
  omega

/-- `v2 (2^k * m) = k` for odd `m`. -/
theorem v2_eq_of {n k m : ℕ} (h : n = 2 ^ k * m) (hm : m % 2 = 1) : v2 n = k := by
  have hn : n ≠ 0 := by
    rw [h]; exact Nat.mul_ne_zero (Nat.two_pow_pos k).ne' (by omega)
  obtain ⟨m', hm', h'⟩ := exists_odd_mul n hn
  exact two_pow_mul_odd_unique hm' hm (h'.symm.trans h)

example : v2 12 = 2 := v2_eq_of (m := 3) (by norm_num) (by norm_num)
example : v2 1 = 0 := v2_eq_of (m := 1) (by norm_num) (by norm_num)
example : v2 32 = 5 := v2_eq_of (m := 1) (by norm_num) (by norm_num)

/-! ### Accelerated maps: a general equivalence -/

/-- If `G` maps odd numbers to odd numbers and `G x` is a positive Collatz iterate of `x`,
then reaching `1` under Collatz implies reaching `1` under `G`. -/
theorem accel_reaches_one (G : ℕ → ℕ)
    (hG : ∀ x, x % 2 = 1 → G x % 2 = 1 ∧ ∃ n, 1 ≤ n ∧ G x = collatzStep^[n] x) :
    ∀ k x, x % 2 = 1 → collatzStep^[k] x = 1 → ∃ j, G^[j] x = 1 := by
  intro k
  induction k using Nat.strong_induction_on with
  | _ k ih =>
    intro x hx hk
    obtain ⟨hodd, n, hn1, hn⟩ := hG x hx
    by_cases hnk : n ≤ k
    · have h1 : collatzStep^[k - n] (G x) = 1 := by
        rw [hn, ← Function.iterate_add_apply, Nat.sub_add_cancel hnk]; exact hk
      obtain ⟨j, hj⟩ := ih (k - n) (by omega) (G x) hodd h1
      exact ⟨j + 1, by rw [Function.iterate_succ_apply]; exact hj⟩
    · have h1 : collatzStep^[n] x = collatzStep^[n - k] (collatzStep^[k] x) := by
        rw [← Function.iterate_add_apply, Nat.sub_add_cancel (by omega)]
      rw [hk] at h1
      refine ⟨1, ?_⟩
      rw [Function.iterate_one]
      rcases collatzStep_iter_one (n - k) with h | h | h <;> omega

theorem accel_iter_is_collatz_iter (G : ℕ → ℕ)
    (hG : ∀ x, x % 2 = 1 → G x % 2 = 1 ∧ ∃ n, 1 ≤ n ∧ G x = collatzStep^[n] x) :
    ∀ j x, x % 2 = 1 → G^[j] x % 2 = 1 ∧ ∃ i, G^[j] x = collatzStep^[i] x := by
  intro j
  induction j with
  | zero => intro x hx; exact ⟨hx, 0, rfl⟩
  | succ j ih =>
    intro x hx
    obtain ⟨hodd, i, hi⟩ := ih x hx
    obtain ⟨hodd', n, -, hn⟩ := hG _ hodd
    rw [Function.iterate_succ_apply']
    exact ⟨hodd', n + i, by rw [hn, hi, Function.iterate_add_apply]⟩

/-- General principle: the Collatz conjecture is equivalent to its accelerated form for any
map `G` on odd numbers such that `G x` is odd and a positive Collatz iterate of `x`. -/
theorem collatz_iff_accel (G : ℕ → ℕ)
    (hG : ∀ x, x % 2 = 1 → G x % 2 = 1 ∧ ∃ n, 1 ≤ n ∧ G x = collatzStep^[n] x) :
    CollatzConjecture ↔ ∀ x, x % 2 = 1 → ∃ j, G^[j] x = 1 := by
  constructor
  · intro h x hx
    obtain ⟨k, hk⟩ := h x (by omega)
    exact accel_reaches_one G hG k x hx hk
  · intro h n hn
    obtain ⟨m, hm, hnm⟩ := exists_odd_mul n (by omega)
    obtain ⟨j, hj⟩ := h m hm
    obtain ⟨-, i, hi⟩ := accel_iter_is_collatz_iter G hG j m hm
    have hc : collatzStep^[v2 n] n = m := by
      have := collatzStep_iter_two_pow (v2 n) m
      rwa [← hnm] at this
    refine ⟨i + v2 n, ?_⟩
    rw [Function.iterate_add_apply, hc, ← hi, hj]

/-! ### The Syracuse (odd-to-odd) form — misformalization guard for `CollatzConjecture` -/

/-- Syracuse map `U(x) = (3x+1) / 2^{v_2(3x+1)}`. -/
def syracuse (x : ℕ) : ℕ := (3 * x + 1) / 2 ^ v2 (3 * x + 1)

/-- Syracuse form of the conjecture: every odd `x` reaches `1` under `U`. -/
def SyracuseConjecture : Prop := ∀ x : ℕ, x % 2 = 1 → ∃ k : ℕ, syracuse^[k] x = 1

theorem syracuse_spec (x : ℕ) (hx : x % 2 = 1) :
    syracuse x % 2 = 1 ∧ ∃ n, 1 ≤ n ∧ syracuse x = collatzStep^[n] x := by
  obtain ⟨m, hm, h⟩ := exists_odd_mul (3 * x + 1) (by omega)
  have hs : syracuse x = m := by
    unfold syracuse
    exact Nat.div_eq_of_eq_mul_right (Nat.two_pow_pos _) h
  have hc : collatzStep^[v2 (3 * x + 1)] (3 * x + 1) = m := by
    have := collatzStep_iter_two_pow (v2 (3 * x + 1)) m
    rwa [← h] at this
  refine ⟨by rw [hs]; exact hm, v2 (3 * x + 1) + 1, by omega, ?_⟩
  rw [Function.iterate_succ_apply, collatzStep_odd hx, hs, hc]

/-- **Test lemma (goal 1).** `CollatzConjecture` is equivalent to the Syracuse form. -/
theorem collatzConjecture_iff_syracuse : CollatzConjecture ↔ SyracuseConjecture :=
  collatz_iff_accel syracuse syracuse_spec

end CollatzFMF
