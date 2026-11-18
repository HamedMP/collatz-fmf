import CollatzFMF.Return

/-!
# Theorem R (proof.md Theorem 55) and the faithfulness check `Collatz ↔ H1 ∧ LemmaE`

Goal 5 of the round-6 Lean track.  Everything in this file is complete
(no `sorry`, no extra axioms).

Normal forms used (paper §5, Binary-Depth Affine Normal Form):
* depth-0 state with parameter `n`:  `x = 4(24n+23) − 1 = 96n + 91`;
* letter `(2,2)` ⟺ `x ≡ 11 (mod 16)`, hop `8x' = 9x + 5`;
* letter `(3,2)` ⟺ `x ≡ 7 (mod 32)`, hop `16x' = 27x + 19`.
Linear invariants: `V(x) = 11x + 19` (Lemma P: `16 V(x') = 27 V(x)` on `(3,2)`),
`W(x) = 11x + 23 = V(x) + 4`, with `8 V(x') = 9 W(x)` on `(2,2)` and
`W(96n+91) = 32(33n+32)`, `V(96n'+91) = 12(88n'+85)`.
-/

namespace CollatzFMF

/-- Dependent-choice helper. -/
theorem exists_seq {α : Type} (P : α → Prop) (R : α → α → Prop)
    (h0 : ∃ a, P a) (hstep : ∀ a, P a → ∃ b, P b ∧ R a b) :
    ∃ f : ℕ → α, ∀ j, P (f j) ∧ R (f j) (f (j + 1)) := by
  obtain ⟨a0, ha0⟩ := h0
  have : Nonempty α := ⟨a0⟩
  choose! nx hnx using hstep
  have hP : ∀ j, P (nx^[j] a0) := by
    intro j
    induction j with
    | zero => exact ha0
    | succ j ih => rw [Function.iterate_succ_apply']; exact (hnx _ ih).1
  refine ⟨fun j => nx^[j] a0, fun j => ⟨hP j, ?_⟩⟩
  show R (nx^[j] a0) (nx^[j + 1] a0)
  rw [Function.iterate_succ_apply']
  exact (hnx _ (hP j)).2

/-! ### From a return step to real FMF hops (used for `Collatz → H1`) -/

theorem hop_depth0 (n : ℕ) : hop (96 * n + 91) = 108 * n + 103 := by
  have := (hop_of_mod16 (x := 96 * n + 91) (by omega)).2
  omega

/-- A run of `j` letters `(3,2)`: if `11x + 19 = 32·16^j·c` then
`11·F^j(x) + 19 = 32·27^j·c`. -/
theorem depth1_run : ∀ (j x c : ℕ), 11 * x + 19 = 32 * 16 ^ j * c →
    11 * hop^[j] x + 19 = 32 * 27 ^ j * c := by
  intro j
  induction j with
  | zero => intro x c h; simpa using h
  | succ j ih =>
    intro x c h
    have h' : 11 * x + 19 = 512 * (16 ^ j * c) := by rw [h]; ring
    have hx : x % 32 = 7 := by omega
    have hh := (hop_of_mod32 hx).2
    have h2 : 11 * hop x + 19 = 32 * 16 ^ j * (27 * c) := by
      have : 32 * 16 ^ j * (27 * c) = 864 * (16 ^ j * c) := by ring
      omega
    have := ih (hop x) (27 * c) h2
    rw [Function.iterate_succ_apply, this]; ring

/-- **Return steps are realised by FMF hops**: if `T(n) = n'` then some positive number of
FMF hops takes `96n + 91` to `96n' + 91`. -/
theorem hop_of_returnStep {n n' : ℕ} (h : ReturnStep n n') :
    ∃ k, 1 ≤ k ∧ hop^[k] (96 * n + 91) = 96 * n' + 91 := by
  obtain ⟨r, w, ⟨h1, -⟩, h2⟩ := h
  cases r with
  | zero =>
    refine ⟨1, le_rfl, ?_⟩
    rw [Function.iterate_one, hop_depth0]
    simp only [pow_zero, one_mul, mul_one] at h1 h2
    omega
  | succ r =>
    refine ⟨r + 2, by omega, ?_⟩
    rw [Function.iterate_succ_apply', Function.iterate_succ_apply, hop_depth0]
    have hrun := depth1_run r (108 * n + 103) (18 * w) (by
      have : 32 * 16 ^ r * (18 * w) = 36 * (16 ^ (r + 1) * w) := by ring
      omega)
    generalize hop^[r] (108 * n + 103) = z at hrun
    have hz : 11 * z + 19 = 576 * (27 ^ r * w) := by rw [hrun]; ring
    have h2' : 88 * n' + 85 = 81 * (27 ^ r * w) := by rw [h2]; ring
    have hz32 : z % 32 = 7 := by omega
    have hh := (hop_of_mod32 hz32).2
    omega

/-! ### From FMF hops to return steps (used for `H1 ∧ E → Collatz`) -/

/-- Block identity: one `(2,2)` hop followed by `r` hops of type `(3,2)`. -/
theorem block_identity (g : ℕ → ℕ) (a : ℕ) (h0 : 8 * g (a + 1) = 9 * g a + 5) :
    ∀ r, (∀ i < r, 16 * g (a + 1 + i + 1) = 27 * g (a + 1 + i) + 19) →
      8 * 16 ^ r * (11 * g (a + 1 + r) + 19) = 9 * 27 ^ r * (11 * g a + 23) := by
  intro r
  induction r with
  | zero => intro _; simp only [pow_zero, mul_one, add_zero]; omega
  | succ r ih =>
    intro h
    have h1 := ih (fun i hi => h i (by omega))
    have h2 := h r (by omega)
    have h3 : 16 * (11 * g (a + 1 + r + 1) + 19) = 27 * (11 * g (a + 1 + r) + 19) := by omega
    calc 8 * 16 ^ (r + 1) * (11 * g (a + 1 + (r + 1)) + 19)
        = 8 * 16 ^ r * (16 * (11 * g (a + 1 + r + 1) + 19)) := by ring_nf
      _ = 27 * (8 * 16 ^ r * (11 * g (a + 1 + r) + 19)) := by rw [h3]; ring
      _ = 9 * 27 ^ (r + 1) * (11 * g a + 23) := by rw [h1]; ring

/-- **Core of Theorem R.**  Given H1, there is no sequence all of whose transitions are
`G01` hops (in affine form) and whose entries are `≡ 1 (mod 3)`.
Case 1 (finitely many depth-0 states) is Lemma P; Case 2 (infinitely many) is H1. -/
theorem no_G01_tail (h1 : H1) (g : ℕ → ℕ)
    (hg : ∀ k, (g k % 16 = 11 ∧ 8 * g (k + 1) = 9 * g k + 5) ∨
               (g k % 32 = 7 ∧ 16 * g (k + 1) = 27 * g k + 19))
    (h3 : ∀ k, g k % 3 = 1) : False := by
  by_cases hB : ∀ K, ∃ k, K ≤ k ∧ g k % 16 = 11
  · -- infinitely many depth-0 states: build an infinite orbit of the return map
    have form : ∀ k, g k % 16 = 11 → g k = 96 * (g k / 96) + 91 := by
      intro k hk
      have a1 := hg k
      have a2 := hg (k + 1)
      have a3 := h3 k
      omega
    apply h1
    obtain ⟨f, hf⟩ := exists_seq (fun n : ℕ => ∃ a, g a = 96 * n + 91) ReturnStep
      (by
        obtain ⟨k, -, hk⟩ := hB 0
        exact ⟨g k / 96, k, form k hk⟩)
      (by
        rintro n ⟨a, ha⟩
        have hex := hB (a + 1)
        have hspec := Nat.find_spec hex
        have hmin := fun i => Nat.find_min (m := i) hex
        generalize Nat.find hex = b at hspec hmin
        obtain ⟨hab, hb⟩ := hspec
        obtain ⟨r, rfl⟩ : ∃ r, b = a + 1 + r := ⟨b - (a + 1), by omega⟩
        have h0 : 8 * g (a + 1) = 9 * g a + 5 := by
          have := hg a; omega
        have hrun : ∀ i < r, 16 * g (a + 1 + i + 1) = 27 * g (a + 1 + i) + 19 := by
          intro i hi
          have hne : ¬ (a + 1 ≤ a + 1 + i ∧ g (a + 1 + i) % 16 = 11) := hmin (a + 1 + i) (by omega)
          have := hg (a + 1 + i)
          have hne' : g (a + 1 + i) % 16 ≠ 11 := fun h => hne ⟨by omega, h⟩
          omega
        have hblock := block_identity g a h0 r hrun
        have hb' := form _ hb
        refine ⟨g (a + 1 + r) / 96, ⟨a + 1 + r, hb'⟩, ?_⟩
        generalize g (a + 1 + r) / 96 = n' at hb' ⊢
        rw [hb', ha] at hblock
        apply returnStep_of_identity (r := r)
        have e : 96 * (16 ^ r * (88 * n' + 85)) = 96 * (3 * 27 ^ r * (33 * n + 32)) := by
          linarith
        exact Nat.eq_of_mul_eq_mul_left (by norm_num) e)
    exact ⟨f, fun j => (hf j).2⟩
  · -- eventually only depth-1 states: Lemma P
    push Not at hB
    obtain ⟨K, hK⟩ := hB
    apply lemmaP
    refine ⟨fun k => (g (K + k) + 1) / 8, fun k => ?_⟩
    show 16 * ((g (K + (k + 1)) + 1) / 8) = 27 * ((g (K + k) + 1) / 8) + 1
    have a1 := hg (K + k)
    have a2 := hg (K + (k + 1))
    have b1 := hK (K + k) (by omega)
    have b2 := hK (K + (k + 1)) (by omega)
    have e : K + k + 1 = K + (k + 1) := rfl
    rw [e] at a1
    omega

/-- **Pointwise FMF descent from H1 and Lemma E** (the middle step of Theorem R). -/
theorem fmf_descent (h1 : H1) (hE : LemmaE) (x : ℕ) (hx : x % 2 = 1) (hx1 : 1 < x) :
    ∃ k, hop^[k] x < x := by
  by_contra hno
  push Not at hno
  obtain ⟨N, hN⟩ := hE x hx hx1 hno
  have hstep : ∀ k, hop^[k + 1] x = hop (hop^[k] x) :=
    fun k => Function.iterate_succ_apply' hop k x
  refine no_G01_tail h1 (fun k => hop^[N + 1 + k] x) (fun k => ?_) (fun k => ?_)
  · show (hop^[N + 1 + k] x % 16 = 11 ∧ 8 * hop^[N + 1 + k + 1] x = 9 * hop^[N + 1 + k] x + 5) ∨
        (hop^[N + 1 + k] x % 32 = 7 ∧ 16 * hop^[N + 1 + k + 1] x = 27 * hop^[N + 1 + k] x + 19)
    rw [hstep]
    exact inG01_cases (hN (N + 1 + k) (by omega))
  · show hop^[N + 1 + k] x % 3 = 1
    have e : N + 1 + k = N + k + 1 := by omega
    rw [e, hstep]
    have := inG01_cases (hN (N + k) (by omega))
    omega

/-- **Theorem R** (proof.md Theorem 55): `H1 ∧ Lemma E ⟹ Collatz`. -/
theorem theoremR (h1 : H1) (hE : LemmaE) : CollatzConjecture := by
  rw [collatzConjecture_iff_hop]
  intro x
  induction x using Nat.strong_induction_on with
  | _ x ih =>
    intro hx
    by_cases hx1 : x = 1
    · exact ⟨0, hx1⟩
    · obtain ⟨k, hk⟩ := fmf_descent h1 hE x hx (by omega)
      obtain ⟨j, hj⟩ := ih _ hk (hop_iter_odd x hx k)
      exact ⟨j + k, by rw [Function.iterate_add_apply]; exact hj⟩

/-! ### The converse: Collatz implies H1 and Lemma E -/

theorem lemmaE_of_collatz (hC : CollatzConjecture) : LemmaE := by
  intro x0 hodd hgt hnd
  obtain ⟨k, hk⟩ := (collatzConjecture_iff_hop.mp hC) x0 hodd
  have := hnd k
  omega

theorem H1_of_collatz (hC : CollatzConjecture) : H1 := by
  rintro ⟨n, hn⟩
  have reach : ∀ j, ∃ K, j ≤ K ∧ hop^[K] (96 * n 0 + 91) = 96 * n j + 91 := by
    intro j
    induction j with
    | zero => exact ⟨0, le_rfl, rfl⟩
    | succ j ih =>
      obtain ⟨K, hK, hKe⟩ := ih
      obtain ⟨k, hk, hke⟩ := hop_of_returnStep (hn j)
      exact ⟨k + K, by omega, by rw [Function.iterate_add_apply, hKe, hke]⟩
  obtain ⟨k0, hk0⟩ := (collatzConjecture_iff_hop.mp hC) (96 * n 0 + 91) (by omega)
  obtain ⟨K, hK, hKe⟩ := reach k0
  have : hop^[K] (96 * n 0 + 91) = 1 := by
    have e : K = (K - k0) + k0 := by omega
    rw [e, Function.iterate_add_apply, hk0, hop_iter_one]
  omega

/-- **Faithfulness check**: the Collatz conjecture is equivalent to `H1 ∧ Lemma E`. -/
theorem collatzConjecture_iff_H1_and_LemmaE : CollatzConjecture ↔ H1 ∧ LemmaE :=
  ⟨fun hC => ⟨H1_of_collatz hC, lemmaE_of_collatz hC⟩, fun h => theoremR h.1 h.2⟩

/-- Given Lemma P, H1 implies: no `x` has all its hop letters in `G01`
("no positive integer has a hop word in `G01^ω`", STATE.md §B).  Only this direction is
formalized; the converse is not needed for Theorem R. -/
theorem no_G01_word_of_H1 (h1 : H1) : ¬ ∃ x : ℕ, ∀ k, InG01 (letter (hop^[k] x)) := by
  rintro ⟨x, hx⟩
  have hstep : ∀ k, hop^[k + 1] x = hop (hop^[k] x) :=
    fun k => Function.iterate_succ_apply' hop k x
  refine no_G01_tail h1 (fun k => hop^[1 + k] x) (fun k => ?_) (fun k => ?_)
  · show (hop^[1 + k] x % 16 = 11 ∧ 8 * hop^[1 + k + 1] x = 9 * hop^[1 + k] x + 5) ∨
        (hop^[1 + k] x % 32 = 7 ∧ 16 * hop^[1 + k + 1] x = 27 * hop^[1 + k] x + 19)
    rw [hstep]
    exact inG01_cases (hx (1 + k))
  · show hop^[1 + k] x % 3 = 1
    have e : 1 + k = k + 1 := by omega
    rw [e, hstep]
    have := inG01_cases (hx k)
    omega

end CollatzFMF
