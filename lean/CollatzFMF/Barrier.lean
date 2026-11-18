import CollatzFMF.Return

/-!
# The repetition barrier (Theorem A of `notes/round6-nov2026/frontier/REPORT.md`, section (b))

Setting: the partial map on natural numbers with two letters
* `a : w ↦ (9w+1)/8` when `w % 8 = 7`,
* `b : w ↦ 27w/16`  when `16 ∣ w`.

For a word `v` over `{a,b}`: `B v = 3·#a + 4·#b`, `e v = 2·#a + 3·#b`.
Everything is stated in integer form (no real logarithms):
`2^(B u) < (w₀+1)·2^(G p)` with `G = e·log₂3 − B` is `2^(B u + B p) < (w₀+1)·3^(e p)`.

Everything in this file is complete (no `sorry`, no extra axioms).
-/

namespace CollatzFMF
namespace Barrier

/-- The two letters. -/
inductive Letter
  | a
  | b
  deriving DecidableEq, Repr

open Letter

/-- One step of the partial map: `Step l w w'` iff letter `l` is admissible at `w` and maps
`w` to `w'`. -/
def Step : Letter → ℕ → ℕ → Prop
  | a, w, w' => w % 8 = 7 ∧ 8 * w' = 9 * w + 1
  | b, w, w' => w % 16 = 0 ∧ 16 * w' = 27 * w

/-- `Run v w w'`: reading the word `v` from `w` is admissible letter by letter and ends at `w'`
("the itinerary of `w` starts with `v`", with end state `w'`). -/
def Run : List Letter → ℕ → ℕ → Prop
  | [], w, w' => w = w'
  | l :: v, w, w'' => ∃ w', Step l w w' ∧ Run v w' w''

/-- Bits consumed by a letter. -/
def bits : Letter → ℕ
  | a => 3
  | b => 4

/-- Powers of three produced by a letter. -/
def expo : Letter → ℕ
  | a => 2
  | b => 3

instance (l : Letter) (w w' : ℕ) : Decidable (Step l w w') := by
  cases l <;> unfold Step <;> infer_instance

/-- Linear congruences with a unit coefficient are solvable. -/
theorem exists_mul_modEq {k n : ℕ} (hc : Nat.Coprime k n) (c : ℕ) : ∃ t, k * t ≡ c [MOD n] := by
  rcases Nat.lt_trichotomy n 1 with h | h | h
  · have hn : n = 0 := by omega
    subst hn
    have hk : k = 1 := by simpa using hc
    exact ⟨c, by subst hk; simp [Nat.ModEq]⟩
  · subst h; exact ⟨0, Nat.modEq_one⟩
  · obtain ⟨m, -, hm⟩ := Nat.exists_mul_mod_eq_one_of_coprime hc h
    refine ⟨m * c, ?_⟩
    have h1 : k * m ≡ 1 [MOD n] := by
      unfold Nat.ModEq; rw [hm, Nat.mod_eq_of_lt h]
    have h2 := h1.mul_right c
    rw [one_mul] at h2
    rw [← mul_assoc]; exact h2

/-- `B v = 3·#a + 4·#b`. -/
def B (v : List Letter) : ℕ := (v.map bits).sum

/-- `e v = 2·#a + 3·#b`. -/
def e (v : List Letter) : ℕ := (v.map expo).sum

@[simp] theorem B_nil : B [] = 0 := rfl
@[simp] theorem e_nil : e [] = 0 := rfl
@[simp] theorem B_cons (l : Letter) (v : List Letter) : B (l :: v) = bits l + B v := by
  simp [B]
@[simp] theorem e_cons (l : Letter) (v : List Letter) : e (l :: v) = expo l + e v := by
  simp [e]
@[simp] theorem B_append (u v : List Letter) : B (u ++ v) = B u + B v := by
  simp [B]
@[simp] theorem e_append (u v : List Letter) : e (u ++ v) = e u + e v := by
  simp [e]

/-- `B` and `e` are the functions of the source report. -/
theorem B_eq_count (v : List Letter) : B v = 3 * v.count a + 4 * v.count b := by
  induction v with
  | nil => rfl
  | cons l v ih => cases l <;> simp [bits, ih] <;> omega

theorem e_eq_count (v : List Letter) : e v = 2 * v.count a + 3 * v.count b := by
  induction v with
  | nil => rfl
  | cons l v ih => cases l <;> simp [expo, ih] <;> omega

/-- Integer form of (1.1) `B ≥ T0·G`, `T0 = 4/(3 log₂3 − 4)`: it is exactly `4 e ≤ 3 B`. -/
theorem four_e_le_three_B (v : List Letter) : 4 * e v ≤ 3 * B v := by
  rw [B_eq_count, e_eq_count]; omega

theorem three_len_le_B (v : List Letter) : 3 * v.length ≤ B v := by
  induction v with
  | nil => simp
  | cons l v ih => cases l <;> simp [bits] <;> omega

theorem B_pos {v : List Letter} (h : v ≠ []) : 0 < B v := by
  have := three_len_le_B v
  have : 0 < v.length := List.length_pos_iff.mpr h
  omega

/-! ### Basic facts about `Step` and `Run` -/

theorem step_unique {l : Letter} {w x x' : ℕ} (h : Step l w x) (h' : Step l w x') : x = x' := by
  cases l <;> simp only [Step] at h h' <;> omega

theorem run_unique {v : List Letter} {w x x' : ℕ} (h : Run v w x) (h' : Run v w x') :
    x = x' := by
  induction v generalizing w with
  | nil => simp only [Run] at h h'; omega
  | cons l v ih =>
    obtain ⟨y, hs, hr⟩ := h
    obtain ⟨y', hs', hr'⟩ := h'
    obtain rfl := step_unique hs hs'
    exact ih hr hr'

theorem run_append {u v : List Letter} {w x : ℕ} :
    Run (u ++ v) w x ↔ ∃ y, Run u w y ∧ Run v y x := by
  induction u generalizing w with
  | nil => simp [Run]
  | cons l u ih =>
    simp only [List.cons_append, Run, ih]
    constructor
    · rintro ⟨w', hs, y, hu, hv⟩; exact ⟨y, ⟨w', hs, hu⟩, hv⟩
    · rintro ⟨y, ⟨w', hs, hu⟩, hv⟩; exact ⟨w', hs, y, hu, hv⟩

/-- (A-ii) strict growth: `w < step w` for `w ≥ 1`. -/
theorem step_lt {l : Letter} {w w' : ℕ} (h : Step l w w') (hw : 1 ≤ w) : w < w' := by
  cases l <;> simp only [Step] at h <;> omega

theorem run_le {v : List Letter} {w w' : ℕ} (h : Run v w w') (hw : 1 ≤ w) : w ≤ w' := by
  induction v generalizing w with
  | nil => simp only [Run] at h; omega
  | cons l v ih =>
    obtain ⟨y, hs, hr⟩ := h
    have := step_lt hs hw
    have := ih hr (by omega)
    omega

theorem run_lt {v : List Letter} {w w' : ℕ} (h : Run v w w') (hw : 1 ≤ w) (hv : v ≠ []) :
    w < w' := by
  cases v with
  | nil => exact absurd rfl hv
  | cons l v =>
    obtain ⟨y, hs, hr⟩ := h
    have := step_lt hs hw
    have := run_le hr (by omega)
    omega

/-- (A-iii), one letter: `(w'+1)·8 = 9(w+1)` for `a`. -/
theorem step_a_growth {w w' : ℕ} (h : Step a w w') : (w' + 1) * 8 = 9 * (w + 1) := by
  simp only [Step] at h; omega

/-- (A-iii), one letter: `(w'+1)·16 ≤ 27(w+1)` for `b`. -/
theorem step_b_growth {w w' : ℕ} (h : Step b w w') : (w' + 1) * 16 ≤ 27 * (w + 1) := by
  simp only [Step] at h; omega

theorem step_growth {l : Letter} {w w' : ℕ} (h : Step l w w') :
    (w' + 1) * 2 ^ bits l ≤ 3 ^ expo l * (w + 1) := by
  cases l
  · have := step_a_growth h; simp only [bits, expo]; omega
  · have := step_b_growth h; simp only [bits, expo]; omega

/-- (A-iii): after reading the prefix `p` from `w₀`, `(w_i + 1)·2^(B p) ≤ 3^(e p)·(w₀+1)`. -/
theorem run_growth {p : List Letter} {w w' : ℕ} (h : Run p w w') :
    (w' + 1) * 2 ^ B p ≤ 3 ^ e p * (w + 1) := by
  induction p generalizing w with
  | nil => simp only [Run] at h; subst h; simp
  | cons l p ih =>
    obtain ⟨y, hs, hr⟩ := h
    have h1 := ih hr
    have h2 := step_growth hs
    calc (w' + 1) * 2 ^ B (l :: p) = (w' + 1) * 2 ^ B p * 2 ^ bits l := by
          rw [B_cons, pow_add]; ring
      _ ≤ 3 ^ e p * (y + 1) * 2 ^ bits l := Nat.mul_le_mul_right _ h1
      _ = 3 ^ e p * ((y + 1) * 2 ^ bits l) := by ring
      _ ≤ 3 ^ e p * (3 ^ expo l * (w + 1)) := Nat.mul_le_mul_left _ h2
      _ = 3 ^ e (l :: p) * (w + 1) := by rw [e_cons, pow_add]; ring

/-! ### (A-i): the cylinder of a word is one residue class mod `2^(B u)` -/

theorem step_modEq {l : Letter} {w w' y y' m : ℕ} (h : Step l w y) (h' : Step l w' y')
    (hy : y ≡ y' [MOD 2 ^ m]) : w ≡ w' [MOD 2 ^ (bits l + m)] := by
  cases l
  · simp only [Step] at h h'
    simp only [bits]
    have h1 : 8 * y ≡ 8 * y' [MOD 8 * 2 ^ m] := Nat.ModEq.mul_left' 8 hy
    rw [h.2, h'.2] at h1
    have h2 : 9 * w ≡ 9 * w' [MOD 8 * 2 ^ m] := Nat.ModEq.add_right_cancel' 1 h1
    have h3 : (8 : ℕ) * 2 ^ m = 2 ^ (3 + m) := by rw [pow_add]; norm_num
    rw [h3] at h2
    exact Nat.ModEq.cancel_left_of_coprime
      (Nat.Coprime.pow_left _ (by norm_num : Nat.Coprime 2 9)) h2
  · simp only [Step] at h h'
    simp only [bits]
    have h1 : 16 * y ≡ 16 * y' [MOD 16 * 2 ^ m] := Nat.ModEq.mul_left' 16 hy
    rw [h.2, h'.2] at h1
    have h3 : (16 : ℕ) * 2 ^ m = 2 ^ (4 + m) := by rw [pow_add]; norm_num
    rw [h3] at h1
    exact Nat.ModEq.cancel_left_of_coprime
      (Nat.Coprime.pow_left _ (by norm_num : Nat.Coprime 2 27)) h1

/-- **(A-i), forward direction** (the consequence used in Theorem A): two integers whose
itineraries both start with `u` are congruent mod `2^(B u)`. -/
theorem run_modEq {u : List Letter} {w w' x x' : ℕ} (h : Run u w x) (h' : Run u w' x') :
    w ≡ w' [MOD 2 ^ B u] := by
  induction u generalizing w w' with
  | nil => simp [Nat.modEq_one]
  | cons l u ih =>
    obtain ⟨y, hs, hr⟩ := h
    obtain ⟨y', hs', hr'⟩ := h'
    rw [B_cons]
    exact step_modEq hs hs' (ih hr hr')

/-- **(A-i), converse direction**: the set of integers whose itinerary starts with `u` is closed
under congruence mod `2^(B u)`. -/
theorem run_of_modEq {u : List Letter} {w w' x : ℕ} (h : Run u w x)
    (hw : w' ≡ w [MOD 2 ^ B u]) : ∃ x', Run u w' x' := by
  induction u generalizing w w' with
  | nil => exact ⟨w', rfl⟩
  | cons l u ih =>
    obtain ⟨y, hs, hr⟩ := h
    rw [B_cons, pow_add] at hw
    cases l
    · simp only [Step] at hs
      simp only [bits] at hw
      have h8 : w' ≡ w [MOD 8] := by
        have : (8 : ℕ) = 2 ^ 3 := by norm_num
        rw [this]; exact Nat.ModEq.of_mul_right _ hw
      have h8' : w' % 8 = 7 := by have := h8; unfold Nat.ModEq at this; omega
      obtain ⟨y', hy'⟩ : ∃ y', 8 * y' = 9 * w' + 1 := ⟨(9 * w' + 1) / 8, by omega⟩
      have h1 : 9 * w' + 1 ≡ 9 * w + 1 [MOD 2 ^ 3 * 2 ^ B u] :=
        Nat.ModEq.add_right 1 (Nat.ModEq.mul_left 9 hw)
      rw [← hy', ← hs.2] at h1
      have h2 : y' ≡ y [MOD 2 ^ B u] := Nat.ModEq.mul_left_cancel' (by norm_num) h1
      obtain ⟨x', hx'⟩ := ih hr h2
      exact ⟨x', y', ⟨h8', hy'⟩, hx'⟩
    · simp only [Step] at hs
      simp only [bits] at hw
      have h16 : w' ≡ w [MOD 16] := by
        have : (16 : ℕ) = 2 ^ 4 := by norm_num
        rw [this]; exact Nat.ModEq.of_mul_right _ hw
      have h16' : w' % 16 = 0 := by have := h16; unfold Nat.ModEq at this; omega
      obtain ⟨y', hy'⟩ : ∃ y', 16 * y' = 27 * w' := ⟨27 * w' / 16, by omega⟩
      have h1 : 27 * w' ≡ 27 * w [MOD 2 ^ 4 * 2 ^ B u] := Nat.ModEq.mul_left 27 hw
      rw [← hy', ← hs.2] at h1
      have h2 : y' ≡ y [MOD 2 ^ B u] := Nat.ModEq.mul_left_cancel' (by norm_num) h1
      obtain ⟨x', hx'⟩ := ih hr h2
      exact ⟨x', y', ⟨h16', hy'⟩, hx'⟩

/-- **(A-i), full form**: given one integer `w` whose itinerary starts with `u`, the integers
whose itinerary starts with `u` are exactly the residue class of `w` mod `2^(B u)`. -/
theorem cylinder_eq_residue_class {u : List Letter} {w x : ℕ} (h : Run u w x) (w' : ℕ) :
    (∃ x', Run u w' x') ↔ w' ≡ w [MOD 2 ^ B u] :=
  ⟨fun ⟨_, h'⟩ => run_modEq h' h, fun hw => run_of_modEq h hw⟩

/-- Every word has a nonempty cylinder (so the cylinder is exactly one residue class). -/
theorem cylinder_nonempty (u : List Letter) : ∃ w x, 1 ≤ w ∧ Run u w x := by
  induction u with
  | nil => exact ⟨1, 1, le_rfl, rfl⟩
  | cons l u ih =>
    obtain ⟨y, x, -, hr⟩ := ih
    cases l
    · -- need w ≡ 7 (mod 8) with (9w+1)/8 ≡ y (mod 2^(B u)); take w = 7 + 8 t, image 8 + 9 t.
      obtain ⟨t, ht⟩ : ∃ t, 9 * t ≡ y + (2 ^ B u - 1) * 8 [MOD 2 ^ B u] :=
        exists_mul_modEq (Nat.Coprime.pow_right _ (by norm_num : Nat.Coprime 9 2)) _
      have hpos : 1 ≤ 2 ^ B u := Nat.one_le_two_pow
      have h2 : 8 + 9 * t ≡ y [MOD 2 ^ B u] := by
        have h3 : 8 + 9 * t ≡ 8 + (y + (2 ^ B u - 1) * 8) [MOD 2 ^ B u] :=
          Nat.ModEq.add_left 8 ht
        have h4 : 8 + (y + (2 ^ B u - 1) * 8) = y + 2 ^ B u * 8 := by
          have : (2 ^ B u - 1) * 8 + 8 = 2 ^ B u * 8 := by
            have := Nat.sub_add_cancel hpos
            nlinarith
          omega
        rw [h4] at h3
        refine h3.trans ?_
        have : y + 2 ^ B u * 8 ≡ y + 0 [MOD 2 ^ B u] :=
          Nat.ModEq.add_left y ((Nat.modEq_zero_iff_dvd).mpr ⟨8, rfl⟩)
        simp
      obtain ⟨x', hx'⟩ := run_of_modEq hr h2
      exact ⟨7 + 8 * t, x', by omega, 8 + 9 * t, ⟨by omega, by ring⟩, hx'⟩
    · -- take w = 16 t, image 27 t.
      obtain ⟨t, ht⟩ : ∃ t, 27 * t ≡ y [MOD 2 ^ B u] :=
        exists_mul_modEq (Nat.Coprime.pow_right _ (by norm_num : Nat.Coprime 27 2)) _
      have hpos : 1 ≤ 2 ^ B u := Nat.one_le_two_pow
      -- shift t by 2^B u to make w positive
      have ht' : 27 * (t + 2 ^ B u) ≡ y [MOD 2 ^ B u] := by
        have : 27 * (t + 2 ^ B u) = 27 * t + 2 ^ B u * 27 := by ring
        rw [this]
        have h5 : 27 * t + 2 ^ B u * 27 ≡ y + 0 [MOD 2 ^ B u] :=
          Nat.ModEq.add ht ((Nat.modEq_zero_iff_dvd).mpr ⟨27, rfl⟩)
        simpa using h5
      obtain ⟨x', hx'⟩ := run_of_modEq hr ht'
      exact ⟨16 * (t + 2 ^ B u), x', by omega, 27 * (t + 2 ^ B u), ⟨by omega, by ring⟩, hx'⟩

/-! ### Theorem A -/

/-- **Theorem A, state form.**  `w₀ ≥ 1`; reading `q` from `w₀` gives `w_i`, reading a further
nonempty `t` gives `w_{i'}`, and the word `u` is admissible at both `w_i` and `w_{i'}` (the
factor `u` occurs at positions `i = |q| < i' = |q ++ t|`).  Then
`2^(B u) ≤ w_{i'} − w_i` and `2^(B u + B p) < (w₀+1)·3^(e p)` for the prefix `p = q ++ t`. -/
theorem barrier_core {q t u : List Letter} {w0 wi wi' x x' : ℕ} (h0 : 1 ≤ w0)
    (hq : Run q w0 wi) (ht : Run t wi wi') (htne : t ≠ [])
    (hu : Run u wi x) (hu' : Run u wi' x') :
    wi < wi' ∧ 2 ^ B u ≤ wi' - wi ∧
      2 ^ (B u + B (q ++ t)) < (w0 + 1) * 3 ^ e (q ++ t) := by
  have hwi : 1 ≤ wi := le_trans h0 (run_le hq h0)
  have hlt : wi < wi' := run_lt ht hwi htne
  have hmod : wi ≡ wi' [MOD 2 ^ B u] := run_modEq hu hu'
  have hdvd : 2 ^ B u ∣ wi' - wi := (Nat.modEq_iff_dvd' hlt.le).mp hmod
  have hle : 2 ^ B u ≤ wi' - wi := Nat.le_of_dvd (by omega) hdvd
  refine ⟨hlt, hle, ?_⟩
  have hp : Run (q ++ t) w0 wi' := run_append.mpr ⟨wi, hq, ht⟩
  have hg := run_growth hp
  have h1 : 2 ^ B u < wi' + 1 := by omega
  calc 2 ^ (B u + B (q ++ t)) = 2 ^ B u * 2 ^ B (q ++ t) := pow_add _ _ _
    _ < (wi' + 1) * 2 ^ B (q ++ t) := Nat.mul_lt_mul_of_pos_right h1 (by positivity)
    _ ≤ 3 ^ e (q ++ t) * (w0 + 1) := hg
    _ = (w0 + 1) * 3 ^ e (q ++ t) := Nat.mul_comm _ _

/-- **Theorem A (repetition barrier), integer form.**  Let the itinerary of `w₀ ≥ 1` begin with
`P`, and let the factor `u` occur in `P` at letter positions `i = |q| < i' = |p|`
(`P = q ++ u ++ s = p ++ u ++ s'`).  Then `2^(B u + B p) < (w₀+1)·3^(e p)`. -/
theorem theoremA {P q p u s s' : List Letter} {w0 wend : ℕ} (h0 : 1 ≤ w0)
    (hP : Run P w0 wend) (h1 : P = q ++ u ++ s) (h2 : P = p ++ u ++ s')
    (hlen : q.length < p.length) :
    2 ^ (B u + B p) < (w0 + 1) * 3 ^ e p := by
  have heq : q ++ (u ++ s) = p ++ (u ++ s') := by
    rw [← List.append_assoc, ← List.append_assoc, ← h1, ← h2]
  rcases List.append_eq_append_iff.mp heq with ⟨t, hpt, -⟩ | ⟨c, hqc, -⟩
  · subst hpt
    have htne : t ≠ [] := by
      rintro rfl; simp at hlen
    -- states
    have hP1 := hP
    rw [h1, List.append_assoc] at hP1
    obtain ⟨wi, hq, hus⟩ := run_append.mp hP1
    obtain ⟨x, hu, -⟩ := run_append.mp hus
    have hP2 := hP
    rw [h2, List.append_assoc] at hP2
    obtain ⟨wi', hp, hus'⟩ := run_append.mp hP2
    obtain ⟨x', hu', -⟩ := run_append.mp hus'
    obtain ⟨wi2, hq2, ht⟩ := run_append.mp hp
    obtain rfl := run_unique hq hq2
    exact (barrier_core h0 hq ht htne hu hu').2.2
  · subst hqc
    simp at hlen

/-- Theorem A with the difference bound exposed: `2^(B u) ≤ w_{i'} − w_i`. -/
theorem theoremA_diff {q t u : List Letter} {w0 wi wi' x x' : ℕ} (h0 : 1 ≤ w0)
    (hq : Run q w0 wi) (ht : Run t wi wi') (htne : t ≠ [])
    (hu : Run u wi x) (hu' : Run u wi' x') : 2 ^ B u ≤ wi' - wi :=
  (barrier_core h0 hq ht htne hu hu').2.1

/-! ### Sanity examples (cross-checked with Python, see the lean-gate report) -/

-- a at 7: (9·7+1)/8 = 8
example : Step a 7 8 := by decide
-- b at 16: 27
example : Step b 16 27 := by decide
-- the word `a a b` is admissible at 55:  55 → 62?  no: 55 % 8 = 7, (9·55+1)/8 = 62, 62 % 8 = 6.
example : ¬ ∃ x, Run [a, a] 55 x := by
  rintro ⟨x, y, ⟨-, h⟩, z, ⟨h2, -⟩, -⟩
  omega
-- 7 --a--> 8, and 8 is in neither gate
example : Run [a] 7 8 := ⟨8, by decide, rfl⟩
-- 16 --b--> 27, 27 is in neither gate (27 % 8 = 3)
example : Run [b] 16 27 := ⟨27, by decide, rfl⟩
-- 4096 --b--> 6912 --b--> 11664 --b--> 19683   (b b b; 4096 = 16^3)
example : Run [b, b, b] 4096 19683 :=
  ⟨6912, by decide, 11664, by decide, 19683, by decide, rfl⟩
-- 368 --b--> 621?  621 % 8 = 5: no.  1136 = 16·71 --b--> 1917, 1917 % 8 = 5: no.
-- 112 = 16·7 --b--> 189, 189 % 8 = 5.  2032 = 16·127 --b--> 3429, 3429 % 8 = 5.
-- 16·(8k+5): 80 --b--> 135 (135 % 8 = 7) --a--> 152
example : Run [b, a] 80 152 := ⟨135, by decide, 152, by decide, rfl⟩
-- 71 --a--> 80 --b--> 135 --a--> 152: the factor `a` occurs at positions 0 and 2
example : Run [a, b, a] 71 152 := ⟨80, by decide, 135, by decide, 152, by decide, rfl⟩
-- Theorem A on it: u = [a], p = [a, b]: 2^(3 + 7) = 1024 < 72 · 3^5 = 17496,
-- and 2^3 ≤ 135 − 71 = 64  (indeed 71 ≡ 135 mod 8).
example : 2 ^ (B [a] + B [a, b]) < (71 + 1) * 3 ^ e [a, b] :=
  theoremA (P := [a, b, a]) (q := []) (p := [a, b]) (u := [a]) (s := [b, a]) (s' := [])
    (w0 := 71) (wend := 152) (by norm_num)
    ⟨80, by decide, 135, by decide, 152, by decide, rfl⟩ rfl rfl (by simp)
example : 2 ^ (B [a] + B [a, b]) = 1024 ∧ (71 + 1) * 3 ^ e [a, b] = 17496 := by decide
example : B [b, b, a] = 11 ∧ e [b, b, a] = 8 := by decide

end Barrier
end CollatzFMF
