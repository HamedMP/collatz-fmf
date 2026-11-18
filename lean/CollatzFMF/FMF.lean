import CollatzFMF.Basic

/-!
# Theorem A (FMF step/value formulas), the FMF hop map and hop letters

Goal 2 (first half) of the round-6 Lean track.  Source: `proof.md` Theorems 1–2 and
`paper/sections/02-fmf-formulas.typ` (Theorem A, Unified Type B Formula).
Everything in this file is complete (no `sorry`, no extra axioms).
-/

namespace CollatzFMF

/-- `k` is the index of the *First Multiple of Four* in the Collatz orbit of `x`:
`C^k(x)` is divisible by 4 and no earlier iterate (including `x` itself) is. -/
def IsFMFIndex (x k : ℕ) : Prop :=
  4 ∣ collatzStep^[k] x ∧ ∀ j < k, ¬ 4 ∣ collatzStep^[j] x

theorem isFMFIndex_unique {x k k' : ℕ} (h : IsFMFIndex x k) (h' : IsFMFIndex x k') : k = k' := by
  rcases Nat.lt_trichotomy k k' with hlt | heq | hgt
  · exact absurd h.1 (h'.2 k hlt)
  · exact heq
  · exact absurd h'.1 (h.2 k' hgt)

/-- Closed form of the FMF value: with `s = v_2(x+1)` and `x + 1 = 2^s m`,
`FMF(x) = 2 (3^s m - 1)`.  (`s = 1` is Case A, `s = 2` Case B1, `s = t+2 ≥ 3` Case B2.) -/
def fmf (x : ℕ) : ℕ := 2 * (3 ^ v2 (x + 1) * ((x + 1) / 2 ^ v2 (x + 1)) - 1)

/-- Closed form of the FMF step count: `2 v_2(x+1) - 1`  (1, 3, 3+2t). -/
def fmfSteps (x : ℕ) : ℕ := 2 * v2 (x + 1) - 1

/-- The FMF hop `F(x) = FMF(x) / 2^{v_2(FMF(x))}`. -/
def hop (x : ℕ) : ℕ := fmf x / 2 ^ v2 (fmf x)

/-- The hop letter `(s, v) = (v_2(x+1), v_2(FMF(x)))`. -/
def letter (x : ℕ) : ℕ × ℕ := (v2 (x + 1), v2 (fmf x))

/-- `G01 = {(2,2), (3,2)}`: the depth-{0,1} growth-B letters. -/
def InG01 (l : ℕ × ℕ) : Prop := l = (2, 2) ∨ l = (3, 2)

theorem iter_add_two (j x : ℕ) :
    collatzStep^[j + 2] x = collatzStep^[j] (collatzStep (collatzStep x)) := by
  rw [Function.iterate_add_apply]; rfl

theorem isFMFIndex_shift {x k : ℕ} (h0 : ¬ 4 ∣ x) (h1 : ¬ 4 ∣ collatzStep x)
    (h : IsFMFIndex (collatzStep (collatzStep x)) k) : IsFMFIndex x (k + 2) := by
  refine ⟨by rw [iter_add_two]; exact h.1, ?_⟩
  intro j hj
  match j, hj with
  | 0, _ => exact h0
  | 1, _ => exact h1
  | j + 2, hj =>
    rw [iter_add_two]
    exact h.2 j (by omega)

/-- **Core of Theorem A.** If `x + 1 = 2^(s+1) a` with `a` odd, then the first multiple of four
in the Collatz orbit of `x` occurs at step `2s+1` and equals `2·3^(s+1)·a - 2`. -/
theorem fmf_core : ∀ (s a x : ℕ), a % 2 = 1 → x + 1 = 2 ^ (s + 1) * a →
    IsFMFIndex x (2 * s + 1) ∧ collatzStep^[2 * s + 1] x + 2 = 2 * 3 ^ (s + 1) * a := by
  intro s
  induction s with
  | zero =>
    intro a x ha hx
    have hx' : x + 1 = 2 * a := by simpa using hx
    have h1 : collatzStep x = 3 * x + 1 := collatzStep_odd (by omega)
    refine ⟨⟨?_, ?_⟩, ?_⟩
    · show 4 ∣ collatzStep x
      rw [h1]; omega
    · intro j hj
      have : j = 0 := by omega
      subst this
      show ¬ 4 ∣ x
      omega
    · show collatzStep x + 2 = 2 * 3 ^ (0 + 1) * a
      rw [h1]; omega
  | succ s ih =>
    intro a x ha hx
    have hp : 0 < 2 ^ s * a := Nat.mul_pos (Nat.two_pow_pos s) (by omega)
    have hx' : x + 1 = 4 * (2 ^ s * a) := by rw [hx]; ring
    generalize 2 ^ s * a = p at hp hx'
    have h1 : collatzStep x = 3 * x + 1 := collatzStep_odd (by omega)
    have h2 : collatzStep (3 * x + 1) = 6 * p - 1 := by
      have : 3 * x + 1 = 2 * (6 * p - 1) := by omega
      rw [this, collatzStep_even]
    have hnext : (6 * p - 1) + 1 = 2 ^ (s + 1) * (3 * a) := by
      have : 2 ^ (s + 1) * (3 * a) = 6 * (2 ^ s * a) := by ring
      have hxa : x + 1 = 4 * (2 ^ s * a) := by rw [hx]; ring
      omega
    obtain ⟨hF, hV⟩ := ih (3 * a) (6 * p - 1) (by omega) hnext
    rw [← h2, ← h1] at hF hV
    refine ⟨?_, ?_⟩
    · have := isFMFIndex_shift (x := x) (by omega) (by rw [h1]; omega) hF
      rwa [show 2 * (s + 1) + 1 = 2 * s + 1 + 2 by ring]
    · rw [show 2 * (s + 1) + 1 = 2 * s + 1 + 2 by ring, iter_add_two, hV]; ring

/-- Interface lemma: the closed form `fmf` on `x + 1 = 2^s m`, `m` odd. -/
theorem fmf_eq {x s m : ℕ} (hm : m % 2 = 1) (h : x + 1 = 2 ^ s * m) :
    v2 (x + 1) = s ∧ fmf x + 2 = 2 * 3 ^ s * m := by
  have hv := v2_eq_of h hm
  refine ⟨hv, ?_⟩
  unfold fmf
  rw [hv, Nat.div_eq_of_eq_mul_right (Nat.two_pow_pos s) h]
  have : 0 < 3 ^ s * m := Nat.mul_pos (by positivity) (by omega)
  rw [mul_assoc 2 (3 ^ s) m]
  omega

/-- Interface lemma: the hop on `fmf x = 2^v q`, `q` odd. -/
theorem hop_eq {x v q : ℕ} (hq : q % 2 = 1) (h : fmf x = 2 ^ v * q) :
    v2 (fmf x) = v ∧ hop x = q := by
  have hv := v2_eq_of h hq
  refine ⟨hv, ?_⟩
  unfold hop
  rw [hv]
  exact Nat.div_eq_of_eq_mul_right (Nat.two_pow_pos v) h

/-- Packaged form of Theorem A used downstream. -/
theorem fmf_spec (x : ℕ) (hx : x % 2 = 1) :
    ∃ s m, m % 2 = 1 ∧ x + 1 = 2 ^ (s + 1) * m ∧ v2 (x + 1) = s + 1 ∧
      fmf x + 2 = 2 * 3 ^ (s + 1) * m ∧ IsFMFIndex x (2 * s + 1) ∧
      collatzStep^[2 * s + 1] x = fmf x := by
  obtain ⟨m, hm, h⟩ := exists_odd_mul (x + 1) (by omega)
  obtain ⟨s, hs⟩ : ∃ s, v2 (x + 1) = s + 1 := by
    rcases Nat.eq_zero_or_pos (v2 (x + 1)) with h0 | h0
    · rw [h0] at h; omega
    · exact ⟨v2 (x + 1) - 1, by omega⟩
  rw [hs] at h
  obtain ⟨-, hf⟩ := fmf_eq hm h
  obtain ⟨hF, hV⟩ := fmf_core s m x hm h
  exact ⟨s, m, hm, h, hs, hf, hF, by omega⟩

/-- **Theorem A (unified form).** For odd `x`, the first multiple of four in the Collatz orbit
of `x` is reached after exactly `fmfSteps x = 2 v_2(x+1) - 1` steps and equals
`fmf x = 2 (3^s m - 1)`, where `x + 1 = 2^s m`, `m` odd. -/
theorem theoremA (x : ℕ) (hx : x % 2 = 1) :
    IsFMFIndex x (fmfSteps x) ∧ collatzStep^[fmfSteps x] x = fmf x := by
  obtain ⟨s, m, -, -, hs, -, hF, hV⟩ := fmf_spec x hx
  have : fmfSteps x = 2 * s + 1 := by unfold fmfSteps; omega
  rw [this]
  exact ⟨hF, hV⟩

/-- **Theorem A, Case A**: `x = 4k+1` — exactly 1 step, `FMF = 4(3k+1)`. -/
theorem theoremA_caseA (k x : ℕ) (hx : x = 4 * k + 1) :
    IsFMFIndex x 1 ∧ collatzStep^[1] x = 4 * (3 * k + 1) := by
  obtain ⟨hF, hV⟩ := fmf_core 0 (2 * k + 1) x (by omega) (by omega)
  refine ⟨hF, ?_⟩
  have h2 : collatzStep^[1] x + 2 = 2 * 3 ^ (0 + 1) * (2 * k + 1) := hV
  omega

/-- **Theorem A, Case B1**: `x = 4k+3`, `k = 2j` — exactly 3 steps, `FMF = 4(9j+4)`. -/
theorem theoremA_caseB1 (j x : ℕ) (hx : x = 4 * (2 * j) + 3) :
    IsFMFIndex x 3 ∧ collatzStep^[3] x = 4 * (9 * j + 4) := by
  obtain ⟨hF, hV⟩ := fmf_core 1 (2 * j + 1) x (by omega) (by omega)
  refine ⟨hF, ?_⟩
  have h2 : collatzStep^[3] x + 2 = 2 * 3 ^ (1 + 1) * (2 * j + 1) := hV
  omega

/-- **Unified Type B formula** (paper Prop.): `x = 4k+3`, `k+1 = 2^t m`, `m` odd, `t ≥ 0` —
exactly `3 + 2t` steps, `FMF = 2(3^(t+2) m - 1)`. -/
theorem theoremA_typeB (k t m x : ℕ) (hx : x = 4 * k + 3) (hk : k + 1 = 2 ^ t * m)
    (hm : m % 2 = 1) :
    IsFMFIndex x (3 + 2 * t) ∧ collatzStep^[3 + 2 * t] x = 2 * (3 ^ (t + 2) * m - 1) := by
  have hx1 : x + 1 = 2 ^ (t + 1 + 1) * m := by
    calc x + 1 = 4 * (k + 1) := by omega
      _ = 2 ^ (t + 1 + 1) * m := by rw [hk]; ring
  obtain ⟨hF, hV⟩ := fmf_core (t + 1) m x hm hx1
  rw [show 2 * (t + 1) + 1 = 3 + 2 * t by ring] at hF hV
  refine ⟨hF, ?_⟩
  have : 0 < 3 ^ (t + 2) * m := Nat.mul_pos (by positivity) (by omega)
  have hV' : collatzStep^[3 + 2 * t] x + 2 = 2 * (3 ^ (t + 2) * m) := by rw [hV]; ring
  omega

/-- **Theorem A, Case B2** exactly as stated: `x = 4k+3`, `k` odd, `k+1 = 2^t m`, `m` odd,
`t ≥ 1` — exactly `3 + 2t` steps, `FMF = 2(3^(t+2) m - 1)`.
(The hypotheses `k` odd and `t ≥ 1` are not needed; see `theoremA_typeB`.) -/
theorem theoremA_caseB2 (k t m x : ℕ) (hx : x = 4 * k + 3) (_hkodd : k % 2 = 1)
    (hk : k + 1 = 2 ^ t * m) (hm : m % 2 = 1) (_ht : 1 ≤ t) :
    IsFMFIndex x (3 + 2 * t) ∧ collatzStep^[3 + 2 * t] x = 2 * (3 ^ (t + 2) * m - 1) :=
  theoremA_typeB k t m x hx hk hm

/-! ### Hop map: basic properties -/

/-- For odd `x`: `hop x` is odd and is a positive Collatz iterate of `x`. -/
theorem hop_spec (x : ℕ) (hx : x % 2 = 1) :
    hop x % 2 = 1 ∧ ∃ n, 1 ≤ n ∧ hop x = collatzStep^[n] x := by
  obtain ⟨s, m, hm, -, -, hf, -, hV⟩ := fmf_spec x hx
  have hpos : 0 < 3 ^ (s + 1) * m := Nat.mul_pos (by positivity) (by omega)
  have hf0 : fmf x ≠ 0 := by
    have h3 : 3 ^ (s + 1) = 3 * 3 ^ s := by ring
    have : 0 < 3 ^ s * m := Nat.mul_pos (by positivity) (by omega)
    rw [h3, mul_assoc 2, mul_assoc 3] at hf
    omega
  obtain ⟨q, hq, hfq⟩ := exists_odd_mul (fmf x) hf0
  obtain ⟨-, hh⟩ := hop_eq hq hfq
  refine ⟨by rw [hh]; exact hq, v2 (fmf x) + (2 * s + 1), by omega, ?_⟩
  rw [Function.iterate_add_apply, hV, hh]
  have := collatzStep_iter_two_pow (v2 (fmf x)) q
  rw [← hfq] at this
  exact this.symm

theorem hop_iter_odd (x : ℕ) (hx : x % 2 = 1) (k : ℕ) : hop^[k] x % 2 = 1 :=
  (accel_iter_is_collatz_iter hop hop_spec k x hx).1

/-- **FMF form of the conjecture**: Collatz ⟺ every odd `x` reaches `1` under FMF hops
(proof.md §3, Property 3). -/
theorem collatzConjecture_iff_hop :
    CollatzConjecture ↔ ∀ x, x % 2 = 1 → ∃ k, hop^[k] x = 1 :=
  collatz_iff_accel hop hop_spec

/-! ### Letters `(2,2)` and `(3,2)` as residue classes, with the affine hop formulas -/

theorem hop_of_mod16 {x : ℕ} (h : x % 16 = 11) : letter x = (2, 2) ∧ 8 * hop x = 9 * x + 5 := by
  obtain ⟨c, rfl⟩ : ∃ c, x = 16 * c + 11 := ⟨x / 16, by omega⟩
  obtain ⟨hs, hf⟩ := fmf_eq (x := 16 * c + 11) (s := 2) (m := 4 * c + 3) (by omega) (by omega)
  have hf' : fmf (16 * c + 11) = 2 ^ 2 * (18 * c + 13) := by omega
  obtain ⟨hv, hh⟩ := hop_eq (by omega) hf'
  refine ⟨?_, by rw [hh]; omega⟩
  unfold letter; rw [hs, hv]

theorem hop_of_mod32 {x : ℕ} (h : x % 32 = 7) : letter x = (3, 2) ∧ 16 * hop x = 27 * x + 19 := by
  obtain ⟨c, rfl⟩ : ∃ c, x = 32 * c + 7 := ⟨x / 32, by omega⟩
  obtain ⟨hs, hf⟩ := fmf_eq (x := 32 * c + 7) (s := 3) (m := 4 * c + 1) (by omega) (by omega)
  have hf' : fmf (32 * c + 7) = 2 ^ 2 * (54 * c + 13) := by omega
  obtain ⟨hv, hh⟩ := hop_eq (by omega) hf'
  refine ⟨?_, by rw [hh]; omega⟩
  unfold letter; rw [hs, hv]

theorem mod16_of_letter {x : ℕ} (h : letter x = (2, 2)) : x % 16 = 11 := by
  unfold letter at h
  have hs : v2 (x + 1) = 2 := congrArg Prod.fst h
  have hv : v2 (fmf x) = 2 := congrArg Prod.snd h
  obtain ⟨m, hm, hxm⟩ := exists_odd_mul (x + 1) (by omega)
  rw [hs] at hxm
  obtain ⟨-, hf⟩ := fmf_eq hm hxm
  obtain ⟨q, hq, hfq⟩ := exists_odd_mul (fmf x) (by omega)
  rw [hv] at hfq
  omega

theorem mod32_of_letter {x : ℕ} (h : letter x = (3, 2)) : x % 32 = 7 := by
  unfold letter at h
  have hs : v2 (x + 1) = 3 := congrArg Prod.fst h
  have hv : v2 (fmf x) = 2 := congrArg Prod.snd h
  obtain ⟨m, hm, hxm⟩ := exists_odd_mul (x + 1) (by omega)
  rw [hs] at hxm
  obtain ⟨-, hf⟩ := fmf_eq hm hxm
  obtain ⟨q, hq, hfq⟩ := exists_odd_mul (fmf x) (by omega)
  rw [hv] at hfq
  omega

theorem letter_22_iff (x : ℕ) : letter x = (2, 2) ↔ x % 16 = 11 :=
  ⟨mod16_of_letter, fun h => (hop_of_mod16 h).1⟩

theorem letter_32_iff (x : ℕ) : letter x = (3, 2) ↔ x % 32 = 7 :=
  ⟨mod32_of_letter, fun h => (hop_of_mod32 h).1⟩

/-- A `G01` letter means one of two residue classes with an explicit affine hop. -/
theorem inG01_cases {x : ℕ} (h : InG01 (letter x)) :
    (x % 16 = 11 ∧ 8 * hop x = 9 * x + 5) ∨ (x % 32 = 7 ∧ 16 * hop x = 27 * x + 19) := by
  rcases h with h | h
  · exact Or.inl ⟨mod16_of_letter h, (hop_of_mod16 (mod16_of_letter h)).2⟩
  · exact Or.inr ⟨mod32_of_letter h, (hop_of_mod32 (mod32_of_letter h)).2⟩

/-! ### Misformalization tests (values cross-checked against `check_defs.py`, which computes
FMF semantically by iterating Collatz until the first multiple of 4) -/

/-- generic evaluator used by the examples below -/
theorem hop_letter_eval {x s m v q : ℕ} (hm : m % 2 = 1) (h : x + 1 = 2 ^ s * m)
    (hq : q % 2 = 1) (hf : 2 * 3 ^ s * m = 2 ^ v * q + 2) :
    fmf x = 2 ^ v * q ∧ hop x = q ∧ letter x = (s, v) := by
  obtain ⟨hs, hf'⟩ := fmf_eq hm h
  have hfx : fmf x = 2 ^ v * q := by omega
  obtain ⟨hv, hh⟩ := hop_eq hq hfx
  exact ⟨hfx, hh, by unfold letter; rw [hs, hv]⟩

-- x = 1: FMF = 4 (1 step), hop = 1, letter (1,2)
example : fmf 1 = 4 ∧ hop 1 = 1 ∧ letter 1 = (1, 2) := by
  have := hop_letter_eval (x := 1) (s := 1) (m := 1) (v := 2) (q := 1)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  simpa using this
-- x = 3: FMF = 16 (3 steps), hop = 1, letter (2,4)
example : fmf 3 = 16 ∧ hop 3 = 1 ∧ letter 3 = (2, 4) := by
  have := hop_letter_eval (x := 3) (s := 2) (m := 1) (v := 4) (q := 1)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  simpa using this
-- x = 7: FMF = 52 (5 steps), hop = 13, letter (3,2)
example : fmf 7 = 52 ∧ hop 7 = 13 ∧ letter 7 = (3, 2) := by
  have := hop_letter_eval (x := 7) (s := 3) (m := 1) (v := 2) (q := 13)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  simpa using this
-- x = 27: FMF = 124 (3 steps), hop = 31, letter (2,2)
example : fmf 27 = 124 ∧ hop 27 = 31 ∧ letter 27 = (2, 2) := by
  have := hop_letter_eval (x := 27) (s := 2) (m := 7) (v := 2) (q := 31)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  simpa using this
-- semantic cross-checks: the first multiple of 4 in the orbit, by brute force
example : IsFMFIndex 1 1 ∧ collatzStep^[1] 1 = 4 := by
  refine ⟨⟨by decide, by decide⟩, by decide⟩
example : IsFMFIndex 3 3 ∧ collatzStep^[3] 3 = 16 := by
  refine ⟨⟨by decide, by decide⟩, by decide⟩
example : IsFMFIndex 7 5 ∧ collatzStep^[5] 7 = 52 := by
  refine ⟨⟨by decide, by decide⟩, by decide⟩
example : IsFMFIndex 27 3 ∧ collatzStep^[3] 27 = 124 := by
  refine ⟨⟨by decide, by decide⟩, by decide⟩
example : InG01 (2, 2) ∧ InG01 (3, 2) ∧ ¬ InG01 (1, 2) ∧ ¬ InG01 (2, 4) := by
  unfold InG01; decide

end CollatzFMF
