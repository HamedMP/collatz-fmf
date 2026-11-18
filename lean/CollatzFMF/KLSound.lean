import CollatzFMF.Basic

/-!
# Theorem T (Krasikov–Lagarias soundness by induction on the predecessor set)

Source: `notes/round6-nov2026/kl-exponent/REPORT.md` section b1 (Theorem T), b2 (Lemma G) and
`notes/round6-nov2026/referee-kl-T/REPORT.md`.

* `T n = n/2` (n even), `(3n+1)/2` (n odd).
* `S a x = { 1 ≤ n ≤ x : T^j n = a for some j ≥ 0 with T^i n ≤ x for all 0 ≤ i ≤ j }`.
* Combinatorial core (`core_card`): for `a ≡ 2 (mod 3)` not on a cycle and `4a ≤ x`,
  `S (4a) x` and `S (r₂ a) x` are disjoint subsets of `S a x \ {a}`.
* `lemmaG`, `theoremT`: the full inequalities with real `γ` via `Real.rpow`.

Everything in this file is complete (no `sorry`, no extra axioms).
-/

set_option linter.deprecated false

namespace CollatzFMF
namespace KL

/-- The `3x+1` function `T`. -/
def T (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

/-- `n` reaches `a` with all values `T^i n`, `0 ≤ i ≤ j`, at most `x`. -/
def Reach (x n a : ℕ) : Prop := ∃ j, T^[j] n = a ∧ ∀ i, i ≤ j → T^[i] n ≤ x

open Classical in
/-- `S_a(x)` of Krasikov–Lagarias (`π*_a(x)` is its cardinality). -/
noncomputable def S (a x : ℕ) : Finset ℕ := (Finset.Icc 1 x).filter fun n => Reach x n a

/-- `a` lies on a cycle of `T`. -/
def OnCycle (a : ℕ) : Prop := ∃ j, 1 ≤ j ∧ T^[j] a = a

/-- The second predecessor: `(2a−1)/3` if `a ≡ 8 (mod 9)`, `(4a−2)/3` otherwise
(used for `a ≡ 2 (mod 9)`). -/
def r2 (a : ℕ) : ℕ := if a % 9 = 8 then (2 * a - 1) / 3 else (4 * a - 2) / 3

theorem mem_S {a x n : ℕ} : n ∈ S a x ↔ 1 ≤ n ∧ n ≤ x ∧ Reach x n a := by
  simp [S, and_assoc]

theorem reach_refl {x a : ℕ} (h : a ≤ x) : Reach x a a :=
  ⟨0, rfl, fun i hi => by
    have : i = 0 := by omega
    subst this; exact h⟩

theorem self_mem_S {a x : ℕ} (h1 : 1 ≤ a) (h : a ≤ x) : a ∈ S a x :=
  mem_S.mpr ⟨h1, h, reach_refl h⟩

theorem reach_trans {x n r a : ℕ} (h1 : Reach x n r) (h2 : Reach x r a) : Reach x n a := by
  obtain ⟨j1, e1, b1⟩ := h1
  obtain ⟨j2, e2, b2⟩ := h2
  refine ⟨j2 + j1, by rw [Function.iterate_add_apply, e1, e2], fun i hi => ?_⟩
  rcases Nat.le_total i j1 with h | h
  · exact b1 i h
  · have : i = (i - j1) + j1 := by omega
    rw [this, Function.iterate_add_apply, e1]
    exact b2 _ (by omega)

/-- (F1) `S_r(x) ⊆ S_a(x)` when `r` reaches `a` below `x`. -/
theorem S_subset {x r a : ℕ} (h : Reach x r a) : S r x ⊆ S a x := by
  intro n hn
  obtain ⟨h1, h2, h3⟩ := mem_S.mp hn
  exact mem_S.mpr ⟨h1, h2, reach_trans h3 h⟩

/-- (F2) `a ∉ S_r(x)` when `r` reaches `a` in `e ≥ 1` steps and `a` is not on a cycle. -/
theorem not_mem_S_of_reach {x r a e : ℕ} (hc : ¬ OnCycle a) (he : 1 ≤ e) (hr : T^[e] r = a) :
    a ∉ S r x := by
  intro h
  obtain ⟨-, -, j, hj, -⟩ := mem_S.mp h
  exact hc ⟨e + j, by omega, by rw [Function.iterate_add_apply, hj, hr]⟩

/-- (F3) if `r` reaches `a` and `r` is on a cycle then `a` is on a cycle. -/
theorem onCycle_of_reach {r a e : ℕ} (hr : T^[e] r = a) (h : OnCycle r) : OnCycle a := by
  obtain ⟨j, hj1, hj⟩ := h
  refine ⟨j, hj1, ?_⟩
  rw [← hr, ← Function.iterate_add_apply, Nat.add_comm, Function.iterate_add_apply, hj]

theorem T_two_mul (a : ℕ) : T (2 * a) = a := by
  unfold T; split_ifs <;> omega

theorem T_iter2_four_mul (a : ℕ) : T^[2] (4 * a) = a := by
  have : 4 * a = 2 * (2 * a) := by ring
  simp only [Function.iterate_succ, Function.iterate_zero, Function.comp, id]
  rw [this, T_two_mul, T_two_mul]

theorem reach_four_mul {a x : ℕ} (hx : 4 * a ≤ x) : Reach x (4 * a) a := by
  refine ⟨2, T_iter2_four_mul a, fun i hi => ?_⟩
  have h1 : T (4 * a) = 2 * a := by
    have : 4 * a = 2 * (2 * a) := by ring
    rw [this, T_two_mul]
  interval_cases i
  · exact hx
  · simp only [Function.iterate_succ, Function.iterate_zero, Function.comp, id]
    rw [h1]; omega
  · rw [T_iter2_four_mul]; omega

/-- The number of steps from `r2 a` to `a`: 1 if `a ≡ 8 (mod 9)`, 2 if `a ≡ 2 (mod 9)`. -/
def e2 (a : ℕ) : ℕ := if a % 9 = 8 then 1 else 2

theorem T_r2_of_8 {a : ℕ} (h : a % 9 = 8) : T ((2 * a - 1) / 3) = a := by
  unfold T; split_ifs <;> omega

theorem T_r2_of_2 {a : ℕ} (h : a % 9 = 2) : T ((4 * a - 2) / 3) = (2 * a - 1) / 3 := by
  unfold T; split_ifs <;> omega

theorem T_T_r2_of_2 {a : ℕ} (h : a % 9 = 2) : T (T ((4 * a - 2) / 3)) = a := by
  rw [T_r2_of_2 h]; unfold T; split_ifs <;> omega

theorem iter_e2_r2 {a : ℕ} (h : a % 9 = 8 ∨ a % 9 = 2) : T^[e2 a] (r2 a) = a := by
  rcases h with h | h
  · simp [e2, r2, h, T_r2_of_8 h]
  · have h' : ¬ a % 9 = 8 := by omega
    simp [e2, r2, h', T_T_r2_of_2 h]

theorem reach_r2 {a x : ℕ} (h : a % 9 = 8 ∨ a % 9 = 2) (hx : 4 * a ≤ x) : Reach x (r2 a) a := by
  rcases h with h | h
  · refine ⟨1, by simp [r2, h, T_r2_of_8 h], fun i hi => ?_⟩
    interval_cases i
    · simp only [Function.iterate_zero, id, r2, h, ite_true]; omega
    · simp only [Function.iterate_succ, Function.iterate_zero, Function.comp, id, r2, h, ite_true]
      rw [T_r2_of_8 h]; omega
  · have h' : ¬ a % 9 = 8 := by omega
    refine ⟨2, by simp [r2, h', T_T_r2_of_2 h], fun i hi => ?_⟩
    interval_cases i
    · simp only [Function.iterate_zero, id, r2, h', ite_false]; omega
    · simp only [Function.iterate_succ, Function.iterate_zero, Function.comp, id, r2, h',
        ite_false]
      rw [T_r2_of_2 h]; omega
    · simp only [Function.iterate_succ, Function.iterate_zero, Function.comp, id, r2, h',
        ite_false]
      rw [T_T_r2_of_2 h]; omega

theorem iter_sub {n j1 j2 : ℕ} (h : j1 ≤ j2) : T^[j2] n = T^[j2 - j1] (T^[j1] n) := by
  rw [← Function.iterate_add_apply, Nat.sub_add_cancel h]

/-- (F4) disjointness, abstract form. -/
theorem disjoint_aux {a r e x : ℕ} (hc : ¬ OnCycle a) (he : 1 ≤ e) (hr : T^[e] r = a)
    (h1 : r ≠ 4 * a) (h2 : r ≠ 2 * a) (h3 : ∀ d, 1 ≤ d → d < e → T^[d] r ≠ 4 * a) :
    Disjoint (S (4 * a) x) (S r x) := by
  rw [Finset.disjoint_left]
  intro n hn1 hn2
  obtain ⟨-, -, j1, hj1, -⟩ := mem_S.mp hn1
  obtain ⟨-, -, j2, hj2, -⟩ := mem_S.mp hn2
  rcases Nat.lt_trichotomy j1 j2 with h | h | h
  · -- 4a is visited first
    have hd : T^[j2 - j1] (4 * a) = r := by rw [← hj1, ← iter_sub h.le, hj2]
    rcases Nat.lt_or_ge (j2 - j1) 2 with hlt | hge
    · have h1' : j2 - j1 = 1 := by omega
      rw [h1'] at hd
      have : T (4 * a) = 2 * a := by
        have : 4 * a = 2 * (2 * a) := by ring
        rw [this, T_two_mul]
      simp only [Function.iterate_succ, Function.iterate_zero, Function.comp, id] at hd
      exact h2 (by rw [← hd, this])
    · obtain ⟨d', hd'⟩ : ∃ d', j2 - j1 = d' + 2 := ⟨j2 - j1 - 2, by omega⟩
      rw [hd', Function.iterate_add_apply, T_iter2_four_mul] at hd
      exact hc ⟨e + d', by omega, by rw [Function.iterate_add_apply, hd, hr]⟩
  · subst h
    exact h1 (by rw [← hj2, hj1])
  · -- r is visited first
    have hd : T^[j1 - j2] r = 4 * a := by rw [← hj2, ← iter_sub h.le, hj1]
    rcases Nat.lt_or_ge (j1 - j2) e with hlt | hge
    · exact h3 _ (by omega) hlt hd
    · have hd2 : T^[j1 - j2 - e] a = 4 * a := by
        have := iter_sub (n := r) hge
        rw [hr, hd] at this; exact this.symm
      exact hc ⟨2 + (j1 - j2 - e), by omega, by
        rw [Function.iterate_add_apply, hd2, T_iter2_four_mul]⟩

theorem not_onCycle_two_of {a : ℕ} (hc : ¬ OnCycle a) : a ≠ 2 := by
  rintro rfl
  exact hc ⟨2, by norm_num, by decide⟩

/-- (F4) `S_{4a}(x) ∩ S_{r₂}(x) = ∅`. -/
theorem disjoint_S {a x : ℕ} (ha : a % 3 = 2) (hc : ¬ OnCycle a)
    (h : a % 9 = 8 ∨ a % 9 = 2) : Disjoint (S (4 * a) x) (S (r2 a) x) := by
  refine disjoint_aux (e := e2 a) hc (by unfold e2; split_ifs <;> omega) (iter_e2_r2 h) ?_ ?_ ?_
  · unfold r2; split_ifs <;> omega
  · unfold r2; split_ifs <;> omega
  · intro d hd1 hd2
    rcases h with h | h
    · simp only [e2, h, ite_true] at hd2; omega
    · have h' : ¬ a % 9 = 8 := by omega
      simp only [e2, h', ite_false] at hd2
      have : d = 1 := by omega
      subst this
      simp only [Function.iterate_succ, Function.iterate_zero, Function.comp, id, r2, h',
        ite_false]
      rw [T_r2_of_2 h]; omega

/-- (F1)+(F2) for `r₁ = 4a`. -/
theorem S_four_mul_subset {a x : ℕ} (hc : ¬ OnCycle a) (hx : 4 * a ≤ x) :
    S (4 * a) x ⊆ S a x \ {a} := by
  intro n hn
  rw [Finset.mem_sdiff, Finset.mem_singleton]
  refine ⟨S_subset (reach_four_mul hx) hn, ?_⟩
  rintro rfl
  exact not_mem_S_of_reach hc (by norm_num : 1 ≤ 2) (T_iter2_four_mul n) hn

/-- (F1)+(F2) for `r₂`. -/
theorem S_r2_subset {a x : ℕ} (hc : ¬ OnCycle a) (h : a % 9 = 8 ∨ a % 9 = 2)
    (hx : 4 * a ≤ x) : S (r2 a) x ⊆ S a x \ {a} := by
  intro n hn
  rw [Finset.mem_sdiff, Finset.mem_singleton]
  refine ⟨S_subset (reach_r2 h hx) hn, ?_⟩
  rintro rfl
  exact not_mem_S_of_reach hc (by unfold e2; split_ifs <;> omega : 1 ≤ e2 n) (iter_e2_r2 h) hn

/-- **Theorem T, combinatorial core** (the inequality `(*)` of the source proof).
For `a ≡ 2 (mod 3)` not on a cycle, `a ≡ 8` or `2 (mod 9)`, and `4a ≤ x`: the sets
`S_{4a}(x)` and `S_{r₂}(x)` are disjoint subsets of `S_a(x) \ {a}`, hence
`π*_a(x) ≥ 1 + π*_{4a}(x) + π*_{r₂}(x)`. -/
theorem core (a x : ℕ) (ha : a % 3 = 2) (hc : ¬ OnCycle a) (h : a % 9 = 8 ∨ a % 9 = 2)
    (hx : 4 * a ≤ x) :
    S (4 * a) x ⊆ S a x \ {a} ∧ S (r2 a) x ⊆ S a x \ {a} ∧
      Disjoint (S (4 * a) x) (S (r2 a) x) ∧
      1 + (S (4 * a) x).card + (S (r2 a) x).card ≤ (S a x).card := by
  have s1 := S_four_mul_subset hc hx
  have s2 := S_r2_subset hc h hx
  have dj := disjoint_S (x := x) ha hc h
  refine ⟨s1, s2, dj, ?_⟩
  have hmem : a ∈ S a x := self_mem_S (by omega) (by omega)
  have hsub : S (4 * a) x ∪ S (r2 a) x ⊆ S a x \ {a} := Finset.union_subset s1 s2
  have hcard := Finset.card_le_card hsub
  rw [Finset.card_union_of_disjoint dj, Finset.card_sdiff_of_subset
    (Finset.singleton_subset_iff.mpr hmem), Finset.card_singleton] at hcard
  have hpos : 0 < (S a x).card := Finset.card_pos.mpr ⟨a, hmem⟩
  omega

/-- The core for every residue (`a ≡ 5 (mod 9)` has no second predecessor):
`π*_a(x) ≥ 1 + π*_{4a}(x)`. -/
theorem core_four (a x : ℕ) (ha : 1 ≤ a) (hc : ¬ OnCycle a) (hx : 4 * a ≤ x) :
    1 + (S (4 * a) x).card ≤ (S a x).card := by
  have s1 := S_four_mul_subset hc hx
  have hmem : a ∈ S a x := self_mem_S ha (by omega)
  have hcard := Finset.card_le_card s1
  rw [Finset.card_sdiff_of_subset (Finset.singleton_subset_iff.mpr hmem),
    Finset.card_singleton] at hcard
  have hpos : 0 < (S a x).card := Finset.card_pos.mpr ⟨a, hmem⟩
  omega

/-- Admissibility is inherited: `4a` and `r₂ a` are `≡ 2 (mod 3)` and not on a cycle. -/
theorem admissible_four_mul {a : ℕ} (ha : a % 3 = 2) (hc : ¬ OnCycle a) :
    (4 * a) % 3 = 2 ∧ ¬ OnCycle (4 * a) :=
  ⟨by omega, fun h => hc (onCycle_of_reach (T_iter2_four_mul a) h)⟩

theorem admissible_r2 {a : ℕ} (hc : ¬ OnCycle a) (h : a % 9 = 8 ∨ a % 9 = 2) :
    (r2 a) % 3 = 2 ∧ ¬ OnCycle (r2 a) :=
  ⟨by unfold r2; split_ifs <;> omega, fun h' => hc (onCycle_of_reach (iter_e2_r2 h) h')⟩

/-! ### Lemma G and Theorem T with a real exponent -/

theorem ratio_le {x a r p q : ℝ} (ha : 0 < a) (hr : 0 < r) (hx : 0 ≤ x) (hq : 0 < q)
    (h : p * r ≤ q * a) : p / q * (x / a) ≤ x / r := by
  rw [le_div_iff₀ hr]
  have e : p / q * (x / a) * r = x / (q * a) * (p * r) := by field_simp
  rw [e]
  calc x / (q * a) * (p * r) ≤ x / (q * a) * (q * a) :=
        mul_le_mul_of_nonneg_left h (by positivity)
    _ = x := by field_simp

theorem term_bound {γ x a r κ Wr D : ℝ} {c : ℕ} (hγ : 0 < γ) (hκ : 0 ≤ κ) (hxa : 0 ≤ x / a)
    (hratio : κ * (x / a) ≤ x / r) (hD : 0 ≤ D) (hih : Wr * (x / r) ^ γ * D ≤ c) :
    κ ^ γ * Wr * (x / a) ^ γ * D ≤ c := by
  have h1 : 0 ≤ κ ^ γ := Real.rpow_nonneg hκ γ
  have h2 : 0 ≤ (x / a) ^ γ := Real.rpow_nonneg hxa γ
  rcases le_or_gt Wr 0 with hW | hW
  · have : κ ^ γ * Wr * (x / a) ^ γ * D ≤ 0 := by
      have e : κ ^ γ * Wr * (x / a) ^ γ * D = Wr * (κ ^ γ * (x / a) ^ γ * D) := by ring
      rw [e]; exact mul_nonpos_of_nonpos_of_nonneg hW (by positivity)
    exact le_trans this (Nat.cast_nonneg c)
  · have h3 : κ ^ γ * (x / a) ^ γ ≤ (x / r) ^ γ := by
      rw [← Real.mul_rpow hκ hxa]
      exact Real.rpow_le_rpow (mul_nonneg hκ hxa) hratio hγ.le
    calc κ ^ γ * Wr * (x / a) ^ γ * D = Wr * (κ ^ γ * (x / a) ^ γ) * D := by ring
      _ ≤ Wr * (x / r) ^ γ * D :=
          mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_left h3 hW.le) hD
      _ ≤ c := hih

/-- **Lemma G** (source b2, with the referee's repair for `W(r) ≤ 0` and explicit quantifiers).
Let `γ > 0`, `M > 0`, `W ≤ M` on the naturals, and for every `a ≡ 2 (mod 3)` not on a cycle
`W(a) ≤ 4^(−γ) W(4a) + [a ≡ 8 (9)] (3/2)^γ W((2a−1)/3) + [a ≡ 2 (9)] (3/4)^γ W((4a−2)/3)`.
Then for every such `a` and every real `x ≥ a`:
`π*_a(x) ≥ W(a) (x/a)^γ / (4^γ M)`, where `π*_a(x) = |S_a(⌊x⌋)|`. -/
theorem lemmaG (γ M : ℝ) (hγ : 0 < γ) (hM : 0 < M) (W : ℕ → ℝ) (hW : ∀ a, W a ≤ M)
    (hrow : ∀ a, a % 3 = 2 → ¬ OnCycle a →
      W a ≤ (4 : ℝ) ^ (-γ) * W (4 * a)
        + (if a % 9 = 8 then (3 / 2 : ℝ) ^ γ * W ((2 * a - 1) / 3) else 0)
        + (if a % 9 = 2 then (3 / 4 : ℝ) ^ γ * W ((4 * a - 2) / 3) else 0))
    (a : ℕ) (ha : a % 3 = 2) (hc : ¬ OnCycle a) (x : ℝ) (hx : (a : ℝ) ≤ x) :
    W a * (x / a) ^ γ / (4 ^ γ * M) ≤ ((S a ⌊x⌋₊).card : ℝ) := by
  have hx0 : 0 ≤ x := le_trans (Nat.cast_nonneg a) hx
  have h4pos : (0 : ℝ) < 4 ^ γ := Real.rpow_pos_of_pos (by norm_num) γ
  obtain ⟨D, hDdef⟩ : ∃ D : ℝ, D = (4 ^ γ * M)⁻¹ := ⟨_, rfl⟩
  have hD : 0 ≤ D := by rw [hDdef]; positivity
  suffices H : ∀ N a, (S a ⌊x⌋₊).card = N → a % 3 = 2 → ¬ OnCycle a → (a : ℝ) ≤ x →
      W a * (x / a) ^ γ * D ≤ ((S a ⌊x⌋₊).card : ℝ) by
    rw [div_eq_mul_inv, ← hDdef]; exact H _ a rfl ha hc hx
  intro N
  induction N using Nat.strong_induction_on with
  | _ N ih =>
  intro a hN ha hc hx
  subst hN
  have ha1 : 1 ≤ a := by omega
  have hapos : (0 : ℝ) < a := by exact_mod_cast ha1
  have hxa : 0 ≤ x / a := by positivity
  have haX : a ≤ ⌊x⌋₊ := Nat.le_floor hx
  have hmem : a ∈ S a ⌊x⌋₊ := self_mem_S ha1 haX
  have hcard1 : (1 : ℝ) ≤ ((S a ⌊x⌋₊).card : ℝ) := by
    exact_mod_cast Finset.card_pos.mpr ⟨a, hmem⟩
  have hpow : 0 ≤ (x / a) ^ γ := Real.rpow_nonneg hxa γ
  rcases lt_or_ge x (4 * a) with hlt | hge
  · -- base case `x < 4a`
    rcases le_or_gt (W a) 0 with hW0 | hW0
    · have : W a * (x / a) ^ γ * D ≤ 0 := by
        rw [mul_assoc]
        exact mul_nonpos_of_nonpos_of_nonneg hW0 (mul_nonneg hpow hD)
      linarith
    · have h1 : (x / a) ^ γ ≤ 4 ^ γ :=
        Real.rpow_le_rpow hxa (by rw [div_le_iff₀ hapos]; linarith) hγ.le
      have h2 : W a * (x / a) ^ γ ≤ M * 4 ^ γ :=
        mul_le_mul (hW a) h1 hpow hM.le
      have h3 : W a * (x / a) ^ γ * D ≤ M * 4 ^ γ * D := mul_le_mul_of_nonneg_right h2 hD
      have e : M * 4 ^ γ * D = 1 := by rw [hDdef]; field_simp
      linarith
  · -- induction step `x ≥ 4a`
    have h4X : 4 * a ≤ ⌊x⌋₊ := Nat.le_floor (by push_cast; exact hge)
    obtain ⟨ha4, hc4⟩ := admissible_four_mul ha hc
    have hcf := core_four a ⌊x⌋₊ ha1 hc h4X
    have ih4 := ih _ (by omega) (4 * a) rfl ha4 hc4 (by push_cast; exact hge)
    have t4 : (4 : ℝ) ^ (-γ) * W (4 * a) * (x / a) ^ γ * D ≤ ((S (4 * a) ⌊x⌋₊).card : ℝ) := by
      have e : (4 : ℝ) ^ (-γ) = (4⁻¹ : ℝ) ^ γ := by
        rw [Real.rpow_neg (by norm_num), Real.inv_rpow (by norm_num)]
      rw [e]
      refine term_bound hγ (by norm_num) hxa ?_ hD ih4
      have := ratio_le (x := x) (a := a) (r := ((4 * a : ℕ) : ℝ)) (p := 1) (q := 4) hapos
        (by push_cast; positivity) hx0 (by norm_num) (by push_cast; linarith)
      simpa [one_div] using this
    have hrowa := hrow a ha hc
    have hP : 0 ≤ (x / a) ^ γ * D := mul_nonneg hpow hD
    have h9 : a % 9 = 8 ∨ a % 9 = 2 ∨ a % 9 = 5 := by omega
    rcases h9 with h8 | h2 | h5
    · have hcore := (core a ⌊x⌋₊ ha hc (Or.inl h8) h4X).2.2.2
      obtain ⟨har, hcr⟩ := admissible_r2 hc (Or.inl h8)
      have hr2 : r2 a = (2 * a - 1) / 3 := by simp [r2, h8]
      rw [hr2] at hcore har hcr
      generalize hb : (2 * a - 1) / 3 = b at *
      have hb1 : 1 ≤ b := by omega
      have hbpos : (0 : ℝ) < b := by exact_mod_cast hb1
      have h3b : 3 * b ≤ 2 * a := by omega
      have hbx : (b : ℝ) ≤ x := by
        have : (b : ℝ) ≤ a := by exact_mod_cast (by omega : b ≤ a)
        linarith
      have ihb := ih _ (by omega) b rfl har hcr hbx
      have tb : (3 / 2 : ℝ) ^ γ * W b * (x / a) ^ γ * D ≤ ((S b ⌊x⌋₊).card : ℝ) :=
        term_bound hγ (by norm_num) hxa
          (ratio_le hapos hbpos hx0 (by norm_num) (by exact_mod_cast h3b)) hD ihb
      have hnot : ¬ a % 9 = 2 := by omega
      rw [if_pos h8, if_neg hnot, add_zero] at hrowa
      have hmain := mul_le_mul_of_nonneg_right hrowa hP
      have hcoreR : (1 : ℝ) + ((S (4 * a) ⌊x⌋₊).card : ℝ) + ((S b ⌊x⌋₊).card : ℝ)
          ≤ ((S a ⌊x⌋₊).card : ℝ) := by exact_mod_cast hcore
      nlinarith [hmain, t4, tb, hcoreR]
    · have hcore := (core a ⌊x⌋₊ ha hc (Or.inr h2) h4X).2.2.2
      obtain ⟨har, hcr⟩ := admissible_r2 hc (Or.inr h2)
      have hnot : ¬ a % 9 = 8 := by omega
      have hr2 : r2 a = (4 * a - 2) / 3 := by simp [r2, hnot]
      rw [hr2] at hcore har hcr
      have hane : a ≠ 2 := not_onCycle_two_of hc
      generalize hb : (4 * a - 2) / 3 = b at *
      have hb1 : 1 ≤ b := by omega
      have hbpos : (0 : ℝ) < b := by exact_mod_cast hb1
      have h3b : 3 * b ≤ 4 * a := by omega
      have hbx : (b : ℝ) ≤ x := by
        have : (b : ℝ) ≤ 4 * a := by exact_mod_cast (by omega : b ≤ 4 * a)
        linarith
      have ihb := ih _ (by omega) b rfl har hcr hbx
      have tb : (3 / 4 : ℝ) ^ γ * W b * (x / a) ^ γ * D ≤ ((S b ⌊x⌋₊).card : ℝ) :=
        term_bound hγ (by norm_num) hxa
          (ratio_le hapos hbpos hx0 (by norm_num) (by exact_mod_cast h3b)) hD ihb
      rw [if_neg hnot, if_pos h2, add_zero] at hrowa
      have hmain := mul_le_mul_of_nonneg_right hrowa hP
      have hcoreR : (1 : ℝ) + ((S (4 * a) ⌊x⌋₊).card : ℝ) + ((S b ⌊x⌋₊).card : ℝ)
          ≤ ((S a ⌊x⌋₊).card : ℝ) := by exact_mod_cast hcore
      nlinarith [hmain, t4, tb, hcoreR]
    · have hnot8 : ¬ a % 9 = 8 := by omega
      have hnot2 : ¬ a % 9 = 2 := by omega
      rw [if_neg hnot8, if_neg hnot2, add_zero, add_zero] at hrowa
      have hmain := mul_le_mul_of_nonneg_right hrowa hP
      have hcoreR : (1 : ℝ) + ((S (4 * a) ⌊x⌋₊).card : ℝ) ≤ ((S a ⌊x⌋₊).card : ℝ) := by
        exact_mod_cast hcf
      nlinarith [hmain, t4, hcoreR]

/-- `c̄(r) = min_{t = 0,1,2} c(r + t·3^(k−1))`, residues taken mod `3^k`. -/
noncomputable def cbar (k : ℕ) (c : ℕ → ℝ) (r : ℕ) : ℝ :=
  min (c (r % 3 ^ k)) (min (c ((r + 3 ^ (k - 1)) % 3 ^ k)) (c ((r + 2 * 3 ^ (k - 1)) % 3 ^ k)))

theorem cbar_le_lift (k : ℕ) (hk : 1 ≤ k) (c : ℕ → ℝ) (r z : ℕ) :
    cbar k c r ≤ c ((r + 3 ^ (k - 1) * z) % 3 ^ k) := by
  obtain ⟨k', rfl⟩ : ∃ k', k = k' + 1 := ⟨k - 1, by omega⟩
  simp only [Nat.add_sub_cancel]
  have e3 : 3 ^ (k' + 1) = 3 ^ k' * 3 := pow_succ 3 k'
  have hz : r + 3 ^ k' * z = r + 3 ^ k' * (z % 3) + 3 ^ (k' + 1) * (z / 3) := by
    have := Nat.mod_add_div z 3
    calc r + 3 ^ k' * z = r + 3 ^ k' * (z % 3 + 3 * (z / 3)) := by rw [this]
      _ = r + 3 ^ k' * (z % 3) + 3 ^ (k' + 1) * (z / 3) := by rw [e3]; ring
  rw [hz, Nat.add_mul_mod_self_left]
  have h3 : z % 3 = 0 ∨ z % 3 = 1 ∨ z % 3 = 2 := by omega
  unfold cbar
  simp only [Nat.add_sub_cancel]
  rcases h3 with h | h | h <;> rw [h]
  · simp
  · rw [mul_one]; exact le_trans (min_le_right _ _) (min_le_left _ _)
  · rw [Nat.mul_comm]; exact le_trans (min_le_right _ _) (min_le_right _ _)

/-- **Theorem T.**  Let `k ≥ 2`, `γ > 0`, `c` a weight on residues mod `3^k` bounded by `M > 0`
and satisfying the rows (L1)–(L3) of the Krasikov–Lagarias system (with the `3^(k−1)` lift
reading).  Then for every `a ≡ 2 (mod 3)` not on a cycle and every real `x ≥ a`,
`π*_a(x) ≥ c(a mod 3^k)·(x/a)^γ / (4^γ M)`.
(The source assumes `c > 0` and `M = max c`; neither is needed.) -/
theorem theoremT (k : ℕ) (hk : 2 ≤ k) (γ M : ℝ) (hγ : 0 < γ) (hM : 0 < M) (c : ℕ → ℝ)
    (hcM : ∀ m, m < 3 ^ k → c m ≤ M)
    (L1 : ∀ m, m < 3 ^ k → m % 9 = 2 →
      c m ≤ (4 : ℝ) ^ (-γ) * c (4 * m % 3 ^ k)
        + (3 / 4 : ℝ) ^ γ * cbar k c ((4 * m - 2) / 3))
    (L2 : ∀ m, m < 3 ^ k → m % 9 = 5 → c m ≤ (4 : ℝ) ^ (-γ) * c (4 * m % 3 ^ k))
    (L3 : ∀ m, m < 3 ^ k → m % 9 = 8 →
      c m ≤ (4 : ℝ) ^ (-γ) * c (4 * m % 3 ^ k)
        + (3 / 2 : ℝ) ^ γ * cbar k c ((2 * m - 1) / 3))
    (a : ℕ) (ha : a % 3 = 2) (hc : ¬ OnCycle a) (x : ℝ) (hx : (a : ℝ) ≤ x) :
    c (a % 3 ^ k) * (x / a) ^ γ / (4 ^ γ * M) ≤ ((S a ⌊x⌋₊).card : ℝ) := by
  have hn : 0 < 3 ^ k := by positivity
  refine lemmaG γ M hγ hM (fun a => c (a % 3 ^ k)) (fun a => hcM _ (Nat.mod_lt _ hn)) ?_
    a ha hc x hx
  intro a ha _
  obtain ⟨k', rfl⟩ : ∃ k', k = k' + 2 := ⟨k - 2, by omega⟩
  have e9 : 3 ^ (k' + 2) = 9 * 3 ^ k' := by rw [pow_add]; ring
  have eP : 3 ^ (k' + 2) = 3 * 3 ^ (k' + 2 - 1) := by
    simp only [show k' + 2 - 1 = k' + 1 from rfl]; rw [pow_succ]; ring
  have hm9 : a % 3 ^ (k' + 2) % 9 = a % 9 := Nat.mod_mod_of_dvd a ⟨3 ^ k', e9⟩
  have hmlt : a % 3 ^ (k' + 2) < 3 ^ (k' + 2) := Nat.mod_lt _ hn
  have h4 : 4 * (a % 3 ^ (k' + 2)) % 3 ^ (k' + 2) = 4 * a % 3 ^ (k' + 2) :=
    (Nat.mod_modEq a _).mul_left 4
  have hdiv := Nat.mod_add_div a (3 ^ (k' + 2))
  generalize hm : a % 3 ^ (k' + 2) = m at *
  generalize hq : a / 3 ^ (k' + 2) = q at *
  have h32 : (0 : ℝ) ≤ (3 / 2 : ℝ) ^ γ := Real.rpow_nonneg (by norm_num) γ
  have h34 : (0 : ℝ) ≤ (3 / 4 : ℝ) ^ γ := Real.rpow_nonneg (by norm_num) γ
  have ha' : a = m + 3 * (3 ^ (k' + 2 - 1) * q) := by rw [← hdiv, eP]; ring
  generalize hz : 3 ^ (k' + 2 - 1) * q = z at ha'
  have h9 : a % 9 = 8 ∨ a % 9 = 2 ∨ a % 9 = 5 := by omega
  rcases h9 with h8 | h2 | h5
  · have hnot : ¬ a % 9 = 2 := by omega
    rw [if_pos h8, if_neg hnot, add_zero]
    have hb : (2 * a - 1) / 3 = (2 * m - 1) / 3 + 3 ^ (k' + 2 - 1) * (2 * q) := by
      have : 3 ^ (k' + 2 - 1) * (2 * q) = 2 * z := by rw [← hz]; ring
      rw [this]; omega
    have hlift := cbar_le_lift (k' + 2) (by omega) c ((2 * m - 1) / 3) (2 * q)
    rw [← hb] at hlift
    have := L3 m hmlt (by omega)
    rw [h4] at this
    nlinarith [mul_le_mul_of_nonneg_left hlift h32]
  · have hnot : ¬ a % 9 = 8 := by omega
    rw [if_neg hnot, if_pos h2, add_zero]
    have hb : (4 * a - 2) / 3 = (4 * m - 2) / 3 + 3 ^ (k' + 2 - 1) * (4 * q) := by
      have : 3 ^ (k' + 2 - 1) * (4 * q) = 4 * z := by rw [← hz]; ring
      rw [this]; omega
    have hlift := cbar_le_lift (k' + 2) (by omega) c ((4 * m - 2) / 3) (4 * q)
    rw [← hb] at hlift
    have := L1 m hmlt (by omega)
    rw [h4] at this
    nlinarith [mul_le_mul_of_nonneg_left hlift h34]
  · have hnot8 : ¬ a % 9 = 8 := by omega
    have hnot2 : ¬ a % 9 = 2 := by omega
    rw [if_neg hnot8, if_neg hnot2, add_zero, add_zero]
    have := L2 m hmlt (by omega)
    rw [h4] at this
    exact this

/-! ### Sanity examples (cross-checked with Python) -/

example : T 5 = 8 ∧ T 8 = 4 ∧ T 11 = 17 ∧ T 7 = 11 := by decide
example : r2 8 = 5 ∧ r2 11 = 14 ∧ r2 17 = 11 ∧ r2 20 = 26 := by decide
example : OnCycle 2 := ⟨2, by norm_num, by decide⟩
example : OnCycle 1 := ⟨2, by norm_num, by decide⟩

end KL
end CollatzFMF
