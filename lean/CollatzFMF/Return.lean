import CollatzFMF.FMF

/-!
# Lemma P, the binary return partial map, H1 and Lemma E

Goals 2 (Lemma P), 3 (return-block coding identity) and 4 (statements of H1 and Lemma E).
Sources: `proof.md` Theorem 55; `paper/sections/06-binary-return-codes.typ`
(Binary Return Partial Map, Return Reparameterization); `12-july2026-addendum.typ`.
Everything in this file is complete (no `sorry`, no extra axioms).  `H1` and `LemmaE` are
*definitions of open statements*; nothing here asserts them.
-/

namespace CollatzFMF

/-! ### Lemma P -/

/-- The identity behind Lemma P: `16 m' = 27 m + 1  ⟹  16 (11 m' + 1) = 27 (11 m + 1)`. -/
theorem lemmaP_identity {m m' : ℕ} (h : 16 * m' = 27 * m + 1) :
    16 * (11 * m' + 1) = 27 * (11 * m + 1) := by omega

/-- `16^k · a = 27^k · b  ⟹  16^k ∣ b`. -/
theorem pow16_dvd_of {k a b : ℕ} (h : 16 ^ k * a = 27 ^ k * b) : 16 ^ k ∣ b :=
  (Nat.Coprime.pow k k (by norm_num : Nat.Coprime 16 27)).dvd_of_dvd_mul_left ⟨a, h.symm⟩

/-- No positive integer is divisible by every power of 16. -/
theorem not_all_pow16_dvd {b : ℕ} (hb : 0 < b) (h : ∀ k, 16 ^ k ∣ b) : False := by
  have h1 := Nat.le_of_dvd hb (h b)
  have h2 : b < 16 ^ b := Nat.lt_pow_self (by norm_num)
  omega

/-- Quantitative Lemma P: `k` consecutive steps of `m' = (27m+1)/16` force
`16^k ∣ 11 m_0 + 1`, i.e. `v_2(11 m_0 + 1) ≥ 4k`. -/
theorem lemmaP_valuation (m : ℕ → ℕ) (k : ℕ)
    (h : ∀ i < k, 16 * m (i + 1) = 27 * m i + 1) : 16 ^ k ∣ 11 * m 0 + 1 := by
  have key : ∀ j ≤ k, 16 ^ j * (11 * m j + 1) = 27 ^ j * (11 * m 0 + 1) := by
    intro j
    induction j with
    | zero => intro _; simp
    | succ j ih =>
      intro hj
      have h1 := lemmaP_identity (h j (by omega))
      have h2 := ih (by omega)
      calc 16 ^ (j + 1) * (11 * m (j + 1) + 1)
          = 16 ^ j * (16 * (11 * m (j + 1) + 1)) := by ring
        _ = 27 * (16 ^ j * (11 * m j + 1)) := by rw [h1]; ring
        _ = 27 ^ (j + 1) * (11 * m 0 + 1) := by rw [h2]; ring
  exact pow16_dvd_of (key k le_rfl)

/-- **Lemma P** (proof.md Thm 55): the map `m' = (27m+1)/16` has no infinite orbit in the
natural numbers (in particular no infinite positive-integer orbit). -/
theorem lemmaP : ¬ ∃ m : ℕ → ℕ, ∀ k, 16 * m (k + 1) = 27 * m k + 1 := by
  rintro ⟨m, hm⟩
  exact not_all_pow16_dvd (b := 11 * m 0 + 1) (by omega)
    (fun k => lemmaP_valuation m k (fun i _ => hm i))

/-- Lemma P over the integers as well (the 2-adic fixed point `-1/11` is not an integer). -/
theorem lemmaP_int : ¬ ∃ m : ℕ → ℤ, ∀ k, 16 * m (k + 1) = 27 * m k + 1 := by
  rintro ⟨m, hm⟩
  have key : ∀ j, (16 : ℤ) ^ j * (11 * m j + 1) = 27 ^ j * (11 * m 0 + 1) := by
    intro j
    induction j with
    | zero => simp
    | succ j ih =>
      have h1 : 16 * (11 * m (j + 1) + 1) = 27 * (11 * m j + 1) := by have := hm j; omega
      calc (16 : ℤ) ^ (j + 1) * (11 * m (j + 1) + 1)
          = 16 ^ j * (16 * (11 * m (j + 1) + 1)) := by ring
        _ = 27 * (16 ^ j * (11 * m j + 1)) := by rw [h1]; ring
        _ = 27 ^ (j + 1) * (11 * m 0 + 1) := by rw [ih]; ring
  have hne : (11 * m 0 + 1).natAbs ≠ 0 := by omega
  refine not_all_pow16_dvd (Nat.pos_of_ne_zero hne) (fun k => ?_)
  have h := congrArg Int.natAbs (key k)
  simp only [Int.natAbs_mul, Int.natAbs_pow] at h
  exact pow16_dvd_of (a := (11 * m k + 1).natAbs) (by simpa using h)

-- one admissible step: m = 13 ↦ 22  (27·13+1 = 352 = 16·22), and 16·(11·22+1) = 27·(11·13+1)
example : 16 * 22 = 27 * 13 + 1 ∧ 16 * (11 * 22 + 1) = 27 * (11 * 13 + 1) := by norm_num

/-! ### The binary return partial map `T` -/

/-- `ε_r = 7` for even `r`, `5` for odd `r`. -/
def epsR (r : ℕ) : ℕ := if r % 2 = 0 then 7 else 5

/-- Gate of the return block `0 → 1^r → 0` at the depth-0 parameter `n`:
`33 n + 32 = 16^r w` with `w ≡ ε_r (mod 8)` (so `w` is odd). -/
def ReturnGate (n r w : ℕ) : Prop := 33 * n + 32 = 16 ^ r * w ∧ w % 8 = epsR r

/-- `ReturnStep n n'` : the binary return partial map is defined at `n` and `T(n) = n'`,
i.e. `n' = (3·27^r·w − 85)/88` for the gate data `(r, w)` of `n`. -/
def ReturnStep (n n' : ℕ) : Prop := ∃ r w, ReturnGate n r w ∧ 88 * n' + 85 = 3 * 27 ^ r * w

/-- **H1**: the binary return partial map has no infinite orbit (in `ℕ`; `0` is not in the
domain of `T`, see `not_returnStep_zero`, so this is the same as "no positive-integer orbit"). -/
def H1 : Prop := ¬ ∃ n : ℕ → ℕ, ∀ j, ReturnStep (n j) (n (j + 1))

theorem pow27_mod8 (r : ℕ) : 27 ^ r % 8 = if r % 2 = 0 then 1 else 3 := by
  induction r with
  | zero => rfl
  | succ r ih =>
    rw [pow_succ, Nat.mul_mod, ih]
    split_ifs <;> omega

theorem pow27_mod11 (r : ℕ) : 27 ^ r % 11 = 16 ^ r % 11 := by
  rw [Nat.pow_mod, Nat.pow_mod 16]

/-- **Return-block identity (goal 3).**  If `T(n) = n'` through a block of length `r`, then
`88·16^r·n' + 85·16^r = 3·27^r·(33n+32)`. -/
theorem return_identity {n n' r w : ℕ} (hg : ReturnGate n r w)
    (h : 88 * n' + 85 = 3 * 27 ^ r * w) :
    88 * 16 ^ r * n' + 85 * 16 ^ r = 3 * 27 ^ r * (33 * n + 32) := by
  rw [hg.1]
  calc 88 * 16 ^ r * n' + 85 * 16 ^ r = 16 ^ r * (88 * n' + 85) := by ring
    _ = 3 * 27 ^ r * (16 ^ r * w) := by rw [h]; ring

/-- Equivalent `y`-normal form: with `y = 33n+32`, `8·16^r·y' = 9·27^r·y + 16^r`. -/
theorem return_identity_y {n n' r w : ℕ} (hg : ReturnGate n r w)
    (h : 88 * n' + 85 = 3 * 27 ^ r * w) :
    8 * 16 ^ r * (33 * n' + 32) = 9 * 27 ^ r * (33 * n + 32) + 16 ^ r := by
  have := return_identity hg h
  nlinarith [this]

/-- Converse: the identity alone (in natural numbers) already forces the gate.  So
`ReturnStep n n' ↔ ∃ r, 16^r (88 n' + 85) = 3·27^r (33 n + 32)`. -/
theorem returnStep_of_identity {n n' r : ℕ}
    (h : 16 ^ r * (88 * n' + 85) = 3 * 27 ^ r * (33 * n + 32)) : ReturnStep n n' := by
  have hd : 16 ^ r ∣ 33 * n + 32 := by
    have hc : Nat.Coprime (16 ^ r) (3 * 27 ^ r) := by
      apply Nat.Coprime.mul_right
      · exact Nat.Coprime.pow_left r (by norm_num)
      · exact Nat.Coprime.pow r r (by norm_num)
    exact hc.dvd_of_dvd_mul_left ⟨_, h.symm⟩
  obtain ⟨w, hw⟩ := hd
  have h2 : 88 * n' + 85 = 3 * 27 ^ r * w := by
    have : 16 ^ r * (88 * n' + 85) = 16 ^ r * (3 * 27 ^ r * w) := by rw [h, hw]; ring
    exact Nat.eq_of_mul_eq_mul_left (by positivity) this
  refine ⟨r, w, ⟨hw, ?_⟩, h2⟩
  have h8 : (3 * 27 ^ r * w) % 8 = 5 := by rw [← h2]; omega
  rw [Nat.mul_mod, Nat.mul_mod 3, pow27_mod8] at h8
  have hlt : w % 8 < 8 := Nat.mod_lt _ (by norm_num)
  unfold epsR
  generalize w % 8 = u at *
  split_ifs at h8 ⊢ <;> interval_cases u <;> omega

theorem returnStep_iff (n n' : ℕ) :
    ReturnStep n n' ↔ ∃ r, 16 ^ r * (88 * n' + 85) = 3 * 27 ^ r * (33 * n + 32) := by
  constructor
  · rintro ⟨r, w, hg, h⟩
    exact ⟨r, by have := return_identity hg h; nlinarith [this]⟩
  · rintro ⟨r, h⟩
    exact returnStep_of_identity h

theorem epsR_odd (r : ℕ) : epsR r % 2 = 1 := by unfold epsR; split_ifs <;> rfl

/-- The gate data `(r, w)` of `n` are unique. -/
theorem returnGate_unique {n r w r' w' : ℕ} (h : ReturnGate n r w) (h' : ReturnGate n r' w') :
    r = r' ∧ w = w' := by
  have hw : w % 2 = 1 := by have := epsR_odd r; have := h.2; omega
  have hw' : w' % 2 = 1 := by have := epsR_odd r'; have := h'.2; omega
  have e : 2 ^ (4 * r) * w = 2 ^ (4 * r') * w' := by
    rw [pow_mul, pow_mul]; norm_num; rw [← h.1, ← h'.1]
  have hr : 4 * r = 4 * r' := two_pow_mul_odd_unique hw hw' e
  have hr' : r = r' := by omega
  subst hr'
  refine ⟨rfl, ?_⟩
  have := h.1.symm.trans h'.1
  exact Nat.eq_of_mul_eq_mul_left (by positivity) this

/-- `T` is a partial *map*: the value is unique. -/
theorem returnStep_unique {n a b : ℕ} (ha : ReturnStep n a) (hb : ReturnStep n b) : a = b := by
  obtain ⟨r, w, hg, h⟩ := ha
  obtain ⟨r', w', hg', h'⟩ := hb
  obtain ⟨rfl, rfl⟩ := returnGate_unique hg hg'
  omega

/-- The formula `T(n) = (3·27^r·w − 85)/88` is always an exact division on the gate
(paper: Binary Return Reparameterization). -/
theorem returnGate_exact {n r w : ℕ} (hg : ReturnGate n r w) :
    ∃ n', 88 * n' + 85 = 3 * 27 ^ r * w := by
  obtain ⟨h1, h2⟩ := hg
  -- mod 8
  have m8 : (3 * 27 ^ r * w) % 8 = 5 := by
    rw [Nat.mul_mod, Nat.mul_mod 3, pow27_mod8, h2]
    unfold epsR
    split_ifs <;> rfl
  -- mod 11
  have m11 : (3 * 27 ^ r * w) % 11 = 8 := by
    have e : (16 ^ r * w) % 11 = 10 := by rw [← h1]; omega
    rw [Nat.mul_mod, ← pow27_mod11] at e
    rw [mul_assoc, Nat.mul_mod, Nat.mul_mod (27 ^ r), e]
  -- size
  have hsz : 85 ≤ 3 * 27 ^ r * w := by
    rcases Nat.eq_zero_or_pos r with rfl | hr
    · have : w = 33 * n + 32 := by simpa using h1.symm
      simp only [pow_zero, mul_one]; omega
    · have hw : 5 ≤ w := by
        unfold epsR at h2; split_ifs at h2 <;> omega
      have h27 : 27 ≤ 27 ^ r := Nat.le_self_pow (by omega) 27
      nlinarith
  exact ⟨(3 * 27 ^ r * w - 85) / 88, by omega⟩

/-- `0` is outside the domain of `T` (`33·0+32 = 2^5`). -/
theorem not_returnStep_zero (n' : ℕ) : ¬ ReturnStep 0 n' := by
  rintro ⟨r, w, ⟨h1, h2⟩, -⟩
  have hw : w % 2 = 1 := by have := epsR_odd r; omega
  have e : 2 ^ 5 * 1 = 2 ^ (4 * r) * w := by
    rw [pow_mul]; norm_num; simpa using h1
  have := two_pow_mul_odd_unique (by norm_num) hw e
  omega

/-- `H1` restated for positive integers only — literally "no infinite positive-integer orbit". -/
theorem H1_iff_pos :
    H1 ↔ ¬ ∃ n : ℕ → ℕ, (∀ j, 0 < n j) ∧ ∀ j, ReturnStep (n j) (n (j + 1)) := by
  unfold H1
  constructor
  · rintro h ⟨n, -, hn⟩; exact h ⟨n, hn⟩
  · rintro h ⟨n, hn⟩
    refine h ⟨n, fun j => ?_, hn⟩
    rcases Nat.eq_zero_or_pos (n j) with h0 | h0
    · have := hn j; rw [h0] at this; exact absurd this (not_returnStep_zero _)
    · exact h0

/-! Misformalization tests for `T` (cross-checked with `check_defs.py`):
`T(7) = 8` (r = 0, w = 263), `T(15) = 17` (r = 0, w = 527), `T(48) = 92` (r = 1, w = 101);
`T` undefined at `0`, `1`, `16`. -/

example : ReturnStep 7 8 := ⟨0, 263, ⟨by norm_num, by decide⟩, by norm_num⟩
example : ReturnStep 15 17 := ⟨0, 527, ⟨by norm_num, by decide⟩, by norm_num⟩
example : ReturnStep 48 92 := ⟨1, 101, ⟨by norm_num, by decide⟩, by norm_num⟩
example : 88 * 16 ^ 1 * 92 + 85 * 16 ^ 1 = 3 * 27 ^ 1 * (33 * 48 + 32) := by norm_num
example : ¬ ReturnStep 7 9 := fun h => by
  have := returnStep_unique h
    (⟨0, 263, ⟨by norm_num, by decide⟩, by norm_num⟩ : ReturnStep 7 8)
  omega
example : ∀ n', ¬ ReturnStep 0 n' := not_returnStep_zero
/-- `T` is undefined at `1`: `33·1+32 = 65` is odd and `65 % 8 = 1 ≠ 7`. -/
example : ∀ n', ¬ ReturnStep 1 n' := by
  rintro n' ⟨r, w, ⟨h1, h2⟩, -⟩
  have hw : w % 2 = 1 := by have := epsR_odd r; omega
  have e : 2 ^ 0 * 65 = 2 ^ (4 * r) * w := by
    rw [pow_mul]; norm_num; simpa using h1
  have hr : 0 = 4 * r := two_pow_mul_odd_unique (by norm_num) hw e
  have hr0 : r = 0 := by omega
  subst hr0
  have : w = 65 := by simpa using h1.symm
  subst this
  revert h2; decide

/-! ### Lemma E -/

/-- Weak non-descent of the FMF orbit: `x_k ≥ x_0` for all `k`. -/
def NonDescending (x0 : ℕ) : Prop := ∀ k, x0 ≤ hop^[k] x0

/-- The orbit is eventually a depth-{0,1} growth-B chain: letters outside `G01` occur only
finitely often. -/
def EventuallyG01 (x0 : ℕ) : Prop := ∃ N, ∀ k, N ≤ k → InG01 (letter (hop^[k] x0))

/-- **Lemma E** (open statement): every weakly non-descending FMF orbit of an odd `x_0 > 1` is
eventually a depth-{0,1} growth-B chain. -/
def LemmaE : Prop :=
  ∀ x0 : ℕ, x0 % 2 = 1 → 1 < x0 → NonDescending x0 → EventuallyG01 x0

theorem hop_one : hop 1 = 1 ∧ letter 1 = (1, 2) := by
  have := hop_letter_eval (x := 1) (s := 1) (m := 1) (v := 2) (q := 1)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  exact ⟨this.2.1, this.2.2⟩

theorem hop_iter_one (k : ℕ) : hop^[k] 1 = 1 := by
  induction k with
  | zero => rfl
  | succ k ih => rw [Function.iterate_succ_apply', ih]; exact hop_one.1

/-- **Sanity theorem: why `x_0 = 1` must be excluded.**  The orbit of `1` is the fixed point
`1 → 1` with constant letter `(1,2) ∉ G01`: it is non-descending and never enters `G01`. -/
theorem lemmaE_fails_at_one : NonDescending 1 ∧ ¬ EventuallyG01 1 := by
  refine ⟨fun k => by rw [hop_iter_one], ?_⟩
  rintro ⟨N, hN⟩
  have := hN N le_rfl
  rw [hop_iter_one, hop_one.2] at this
  rcases this with h | h <;> exact absurd h (by decide)

/-- Hence Lemma E *without* the hypothesis `x_0 > 1` is false. -/
theorem lemmaE_without_gt_one_false :
    ¬ (∀ x0 : ℕ, x0 % 2 = 1 → NonDescending x0 → EventuallyG01 x0) :=
  fun h => lemmaE_fails_at_one.2 (h 1 (by norm_num) lemmaE_fails_at_one.1)

end CollatzFMF
