import CollatzFMF.Rigidity

/-!
# Sharpness of Theorem R: the control families `S_a` and `U_a` (w2-gamma Theorem S)

* `Sa a n` : `T n`, except `T n − 2^a` on odd `n ≡ −1 mod 2^(a+1)`.  It has positivity, (I), (II),
  and (III) at every odd `n ≠ 2^(a+1) − 1`, which is a fixed point.  `Sa 0` is the `3n−1` map.
  So the lower bound `n < S n` of (III) cannot be dropped even at a single point.
* `Ua a n` : `T n`, except `T n + 2^a` on the same class (referee-gamma remark).  It has
  positivity, (I), (II), `n < U n ≤ 2n + 1` for all odd `n`, and (III) at every odd
  `n ≠ 2^(a+1) − 1`, where `U n = 2n + 1`.  So the upper bound `S n ≤ 2n` cannot be relaxed
  to `2n + 1` even at a single point.

Everything in this file is complete (no `sorry`, no extra axioms).
-/

set_option linter.deprecated false

namespace CollatzFMF
namespace Rigidity

open KL (T)

/-- The litmus family `S_a`. -/
def Sa (a n : ℕ) : ℕ :=
  if n % 2 = 0 then n / 2
  else if n % 2 ^ (a + 1) = 2 ^ (a + 1) - 1 then (3 * n + 1) / 2 - 2 ^ a
  else (3 * n + 1) / 2

/-- The other-side family `U_a`. -/
def Ua (a n : ℕ) : ℕ :=
  if n % 2 = 0 then n / 2
  else if n % 2 ^ (a + 1) = 2 ^ (a + 1) - 1 then (3 * n + 1) / 2 + 2 ^ a
  else (3 * n + 1) / 2

/-! ## Misformalization guards (cross-checked with Python, see the notes directory) -/

example : Sa 0 1 = 1 := by decide
example : Sa 0 5 = 7 := by decide
example : Sa 0 7 = 10 := by decide
example : Sa 1 3 = 3 := by decide
example : Sa 1 5 = 8 := by decide
example : Sa 1 7 = 9 := by decide
example : Sa 2 7 = 7 := by decide
example : Sa 2 23 = 31 := by decide
example : Sa 2 9 = 14 := by decide
example : Sa 3 12 = 6 := by decide
example : Sa 3 15 = 15 := by decide
example : Sa 3 31 = 39 := by decide
example : Ua 0 1 = 3 := by decide
example : Ua 1 3 = 7 := by decide
example : Ua 2 7 = 15 := by decide
example : Ua 2 23 = 39 := by decide
example : Ua 2 9 = 14 := by decide
example : T 7 = 11 := by decide
example : T 23 = 35 := by decide

/-! ## Arithmetic of the class `−1 mod 2^(a+1)` -/

theorem class_iff (a x : ℕ) :
    (2 * x + 1) % 2 ^ (a + 1) = 2 ^ (a + 1) - 1 ↔ x % 2 ^ a = 2 ^ a - 1 := by
  have hP : 0 < 2 ^ a := Nat.pos_of_ne_zero (by positivity)
  have hr := Nat.mod_lt x hP
  have hd := Nat.div_add_mod x (2 ^ a)
  have e : 2 * x + 1 = (2 * (x % 2 ^ a) + 1) + 2 ^ (a + 1) * (x / 2 ^ a) := by
    rw [pow_succ]; linarith
  have hlt : 2 * (x % 2 ^ a) + 1 < 2 ^ (a + 1) := by rw [pow_succ]; omega
  rw [e, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hlt, pow_succ]
  omega

/-- In the class, `x ≥ 2^a − 1`. -/
theorem class_ge {a x : ℕ} (h : x % 2 ^ a = 2 ^ a - 1) : 2 ^ a - 1 ≤ x :=
  h ▸ Nat.mod_le x (2 ^ a)

/-- In the class, `x = 2^a − 1` or `x ≥ 2^(a+1) − 1`. -/
theorem class_ge' {a x : ℕ} (h : x % 2 ^ a = 2 ^ a - 1) (hx : x ≠ 2 ^ a - 1) :
    2 * 2 ^ a - 1 ≤ x := by
  have hP : 0 < 2 ^ a := Nat.pos_of_ne_zero (by positivity)
  have hd := Nat.div_add_mod x (2 ^ a)
  rw [h] at hd
  have hq : x / 2 ^ a ≠ 0 := by
    intro h0; rw [h0] at hd; omega
  have := Nat.le_mul_of_pos_right (2 ^ a) (Nat.pos_of_ne_zero hq)
  omega

theorem Sa_even (a x : ℕ) : Sa a (2 * x) = x := by
  unfold Sa; rw [if_pos (by omega)]; omega

theorem Sa_odd (a x : ℕ) :
    Sa a (2 * x + 1) = if x % 2 ^ a = 2 ^ a - 1 then 3 * x + 2 - 2 ^ a else 3 * x + 2 := by
  unfold Sa
  rw [if_neg (by omega)]
  simp only [class_iff]
  have : (3 * (2 * x + 1) + 1) / 2 = 3 * x + 2 := by omega
  rw [this]

theorem Ua_even (a x : ℕ) : Ua a (2 * x) = x := by
  unfold Ua; rw [if_pos (by omega)]; omega

theorem Ua_odd (a x : ℕ) :
    Ua a (2 * x + 1) = if x % 2 ^ a = 2 ^ a - 1 then 3 * x + 2 + 2 ^ a else 3 * x + 2 := by
  unfold Ua
  rw [if_neg (by omega)]
  simp only [class_iff]
  have : (3 * (2 * x + 1) + 1) / 2 = 3 * x + 2 := by omega
  rw [this]

/-! ## The prefix property for perturbations of `T` supported on the class -/

theorem pert_dvd_iff {a k : ℕ} {u e : ℤ} (he : (2 : ℤ) ^ a ∣ e) (hu : ¬ (2 : ℤ) ^ a ∣ u) :
    (2 : ℤ) ^ k ∣ 3 * u + e ↔ (2 : ℤ) ^ k ∣ u := by
  by_cases hk : k ≤ a
  · have hke : (2 : ℤ) ^ k ∣ e := (pow_dvd_pow 2 hk).trans he
    rw [dvd_add_left hke, two_pow_dvd_three_mul]
  · have hak : (2 : ℤ) ^ a ∣ (2 : ℤ) ^ k := pow_dvd_pow 2 (by omega)
    constructor
    · intro h
      exfalso; apply hu
      have h1 : (2 : ℤ) ^ a ∣ 3 * u + e := hak.trans h
      rw [dvd_add_left he, two_pow_dvd_three_mul] at h1
      exact h1
    · intro h
      exact absurd (hak.trans h) hu

/-- Any map equal to `n/2` on evens and to `T + e·[n ≡ −1 mod 2^(a+1)]` on odds, with
`2^a ∣ e`, has the parity-prefix property. -/
theorem dvdProp_of_pert (S : ℕ → ℕ) (a : ℕ) (e : ℤ) (he : (2 : ℤ) ^ a ∣ e)
    (hev : ∀ x, S (2 * x) = x)
    (hodd : ∀ x, (S (2 * x + 1) : ℤ) =
      3 * (x : ℤ) + 2 + if x % 2 ^ a = 2 ^ a - 1 then e else 0) : DvdProp S := by
  intro n n' _ _ _ hpar k
  obtain ⟨x, rfl | rfl⟩ := Nat.even_or_odd' n <;>
    obtain ⟨x', rfl | rfl⟩ := Nat.even_or_odd' n'
  · rw [hev, hev]; push_cast
    exact (dvd_even_case _ _ _).symm
  · omega
  · omega
  · rw [hodd, hodd]
    have e2 : (((2 * x + 1 : ℕ) : ℤ)) - ((2 * x' + 1 : ℕ) : ℤ) = 2 * (x : ℤ) - 2 * x' := by
      push_cast; ring
    rw [e2, dvd_even_case]
    have hmod : ∀ {y y' : ℕ}, y % 2 ^ a = 2 ^ a - 1 → ¬ y' % 2 ^ a = 2 ^ a - 1 →
        ¬ (2 : ℤ) ^ a ∣ (y : ℤ) - (y' : ℤ) := by
      intro y y' h1 h2 hd
      rw [← mod_two_pow_eq_iff] at hd
      omega
    by_cases h1 : x % 2 ^ a = 2 ^ a - 1 <;> by_cases h2 : x' % 2 ^ a = 2 ^ a - 1
    · rw [if_pos h1, if_pos h2]
      have : 3 * (x : ℤ) + 2 + e - (3 * (x' : ℤ) + 2 + e) = 3 * ((x : ℤ) - x') := by ring
      rw [this, two_pow_dvd_three_mul]
    · rw [if_pos h1, if_neg h2]
      have : 3 * (x : ℤ) + 2 + e - (3 * (x' : ℤ) + 2 + 0) = 3 * ((x : ℤ) - x') + e := by ring
      rw [this]
      exact pert_dvd_iff he (hmod h1 h2)
    · rw [if_neg h1, if_pos h2]
      have : 3 * (x : ℤ) + 2 + 0 - (3 * (x' : ℤ) + 2 + e) = 3 * ((x : ℤ) - x') + -e := by ring
      rw [this]
      refine pert_dvd_iff ((dvd_neg).mpr he) ?_
      intro hd
      apply hmod h2 h1
      have : (x' : ℤ) - x = -((x : ℤ) - x') := by ring
      rw [this]; exact (dvd_neg).mpr hd
    · rw [if_neg h1, if_neg h2]
      have : 3 * (x : ℤ) + 2 + 0 - (3 * (x' : ℤ) + 2 + 0) = 3 * ((x : ℤ) - x') := by ring
      rw [this, two_pow_dvd_three_mul]

/-! ## Theorem S -/

theorem dvdProp_Sa (a : ℕ) : DvdProp (Sa a) := by
  refine dvdProp_of_pert (Sa a) a (-(2 : ℤ) ^ a) ((dvd_neg).mpr dvd_rfl) (Sa_even a) ?_
  intro x
  rw [Sa_odd]
  have hP : 0 < 2 ^ a := Nat.pos_of_ne_zero (by positivity)
  split_ifs with h
  · have := class_ge h
    rw [Nat.cast_sub (by omega)]; push_cast; ring
  · push_cast; ring

/-- Theorem S (i), first half: `S_a` has the parity-prefix property (valuation form). -/
theorem prefixProp_Sa (a : ℕ) : PrefixProp (Sa a) :=
  (prefixProp_iff_dvdProp _).mpr (dvdProp_Sa a)

/-- Theorem S (i), second half: `S_a` maps positives to positives. -/
theorem pos_Sa (a : ℕ) : Pos (Sa a) := by
  intro n hn
  have hP : 0 < 2 ^ a := Nat.pos_of_ne_zero (by positivity)
  obtain ⟨x, rfl | rfl⟩ := Nat.even_or_odd' n
  · rw [Sa_even]; omega
  · rw [Sa_odd]
    split_ifs with h
    · have := class_ge h; omega
    · omega

/-- `S_a` has the literal parity-prefix property (I). -/
theorem litProp_Sa (a : ℕ) : LitProp (Sa a) := litProp_of_dvdProp (pos_Sa a) (dvdProp_Sa a)

/-- Theorem S (iii): (II) holds for `S_a`. -/
theorem condII_Sa (a : ℕ) : CondII (Sa a) := by
  intro n hn he
  obtain ⟨x, rfl | rfl⟩ := Nat.even_or_odd' n
  · rw [Sa_even]; omega
  · omega

/-- Theorem S (iii): (III) holds for `S_a` at every odd `n ≠ 2^(a+1) − 1`. -/
theorem condIII_Sa (a n : ℕ) (ho : n % 2 = 1) (hne : n ≠ 2 ^ (a + 1) - 1) :
    n < Sa a n ∧ Sa a n ≤ 2 * n := by
  have hP : 0 < 2 ^ a := Nat.pos_of_ne_zero (by positivity)
  obtain ⟨x, rfl | rfl⟩ := Nat.even_or_odd' n
  · omega
  · rw [Sa_odd]
    rw [pow_succ] at hne
    split_ifs with h
    · have := class_ge' h (by omega); omega
    · omega

/-- Theorem S (iii): `n_a = 2^(a+1) − 1` is a fixed point of `S_a`. -/
theorem Sa_fixed (a : ℕ) : Sa a (2 ^ (a + 1) - 1) = 2 ^ (a + 1) - 1 := by
  have hP : 0 < 2 ^ a := Nat.pos_of_ne_zero (by positivity)
  have e : 2 ^ (a + 1) - 1 = 2 * (2 ^ a - 1) + 1 := by rw [pow_succ]; omega
  rw [e, Sa_odd, if_pos (Nat.mod_eq_of_lt (by omega))]
  omega

/-- Theorem S (ii): `S_a = T` off the class `−1 mod 2^(a+1)`. -/
theorem Sa_eq_T_off_class (a n : ℕ) (h : n % 2 ^ (a + 1) ≠ 2 ^ (a + 1) - 1) : Sa a n = T n := by
  unfold Sa T
  rw [if_neg h]

/-- Theorem S (ii): `S_a = T` below `2^(a+1) − 1`. -/
theorem Sa_eq_T_of_lt (a n : ℕ) (h : n < 2 ^ (a + 1) - 1) : Sa a n = T n := by
  apply Sa_eq_T_off_class
  rw [Nat.mod_eq_of_lt (by omega)]
  omega

/-- Theorem S (ii): `S_a ≡ T mod 2^a` everywhere. -/
theorem Sa_mod (a n : ℕ) : Sa a n % 2 ^ a = T n % 2 ^ a := by
  have hP : 0 < 2 ^ a := Nat.pos_of_ne_zero (by positivity)
  obtain ⟨x, rfl | rfl⟩ := Nat.even_or_odd' n
  · rw [Sa_even, T_even]
  · rw [Sa_odd, T_odd]
    split_ifs with h
    · have := class_ge h
      have e : 3 * x + 2 = (3 * x + 2 - 2 ^ a) + 2 ^ a := by omega
      conv_rhs => rw [e, Nat.add_mod_right]
    · rfl

/-- Theorem S (iv): `S_0` is the `3n − 1` map on odd `n`. -/
theorem Sa_zero (n : ℕ) (ho : n % 2 = 1) : Sa 0 n = (3 * n - 1) / 2 := by
  unfold Sa
  rw [if_neg (by omega), if_pos (by simpa using ho)]
  simp
  omega

/-- `S_a ≠ T`: they differ at `n_a = 2^(a+1) − 1`. -/
theorem Sa_ne_T (a : ℕ) : Sa a (2 ^ (a + 1) - 1) ≠ T (2 ^ (a + 1) - 1) := by
  have hP : 0 < 2 ^ a := Nat.pos_of_ne_zero (by positivity)
  rw [Sa_fixed]
  have e : 2 ^ (a + 1) - 1 = 2 * (2 ^ a - 1) + 1 := by rw [pow_succ]; omega
  rw [e, T_odd]
  omega

/-- **Theorem S**, packaged: for every `a`, `S_a` satisfies every hypothesis of Theorem R
except (III) at the single point `n_a = 2^(a+1) − 1`, and `S_a ≠ T`. -/
theorem theoremS (a : ℕ) :
    Pos (Sa a) ∧ PrefixProp (Sa a) ∧ LitProp (Sa a) ∧ CondII (Sa a) ∧
    (∀ n, n % 2 = 1 → n ≠ 2 ^ (a + 1) - 1 → n < Sa a n ∧ Sa a n ≤ 2 * n) ∧
    Sa a (2 ^ (a + 1) - 1) = 2 ^ (a + 1) - 1 ∧
    (∀ n, n < 2 ^ (a + 1) - 1 → Sa a n = T n) ∧
    (∀ n, n % 2 ^ (a + 1) ≠ 2 ^ (a + 1) - 1 → Sa a n = T n) ∧
    (∀ n, Sa a n % 2 ^ a = T n % 2 ^ a) ∧
    Sa a (2 ^ (a + 1) - 1) ≠ T (2 ^ (a + 1) - 1) :=
  ⟨pos_Sa a, prefixProp_Sa a, litProp_Sa a, condII_Sa a, condIII_Sa a, Sa_fixed a,
    Sa_eq_T_of_lt a, Sa_eq_T_off_class a, Sa_mod a, Sa_ne_T a⟩

/-! ## Other-side sharpness: `U_a = T + 2^a·[class]` (referee-gamma remark) -/

theorem dvdProp_Ua (a : ℕ) : DvdProp (Ua a) := by
  refine dvdProp_of_pert (Ua a) a ((2 : ℤ) ^ a) dvd_rfl (Ua_even a) ?_
  intro x
  rw [Ua_odd]
  split_ifs with h <;> push_cast <;> ring

theorem prefixProp_Ua (a : ℕ) : PrefixProp (Ua a) :=
  (prefixProp_iff_dvdProp _).mpr (dvdProp_Ua a)

theorem pos_Ua (a : ℕ) : Pos (Ua a) := by
  intro n hn
  obtain ⟨x, rfl | rfl⟩ := Nat.even_or_odd' n
  · rw [Ua_even]; omega
  · rw [Ua_odd]; split_ifs <;> omega

theorem litProp_Ua (a : ℕ) : LitProp (Ua a) := litProp_of_dvdProp (pos_Ua a) (dvdProp_Ua a)

theorem condII_Ua (a : ℕ) : CondII (Ua a) := by
  intro n hn he
  obtain ⟨x, rfl | rfl⟩ := Nat.even_or_odd' n
  · rw [Ua_even]; omega
  · omega

/-- The relaxed (III): `n < U_a n ≤ 2n + 1` for every odd `n`. -/
theorem condIII_relaxed_Ua (a n : ℕ) (ho : n % 2 = 1) : n < Ua a n ∧ Ua a n ≤ 2 * n + 1 := by
  have hP : 0 < 2 ^ a := Nat.pos_of_ne_zero (by positivity)
  obtain ⟨x, rfl | rfl⟩ := Nat.even_or_odd' n
  · omega
  · rw [Ua_odd]
    split_ifs with h
    · have := class_ge h; omega
    · omega

/-- (III) itself holds for `U_a` at every odd `n ≠ 2^(a+1) − 1`. -/
theorem condIII_Ua (a n : ℕ) (ho : n % 2 = 1) (hne : n ≠ 2 ^ (a + 1) - 1) :
    n < Ua a n ∧ Ua a n ≤ 2 * n := by
  have hP : 0 < 2 ^ a := Nat.pos_of_ne_zero (by positivity)
  obtain ⟨x, rfl | rfl⟩ := Nat.even_or_odd' n
  · omega
  · rw [Ua_odd]
    rw [pow_succ] at hne
    split_ifs with h
    · have := class_ge' h (by omega); omega
    · omega

/-- At `n_a = 2^(a+1) − 1`, `U_a n_a = 2 n_a + 1`. -/
theorem Ua_at (a : ℕ) : Ua a (2 ^ (a + 1) - 1) = 2 * (2 ^ (a + 1) - 1) + 1 := by
  have hP : 0 < 2 ^ a := Nat.pos_of_ne_zero (by positivity)
  have e : 2 ^ (a + 1) - 1 = 2 * (2 ^ a - 1) + 1 := by rw [pow_succ]; omega
  rw [e, Ua_odd, if_pos (Nat.mod_eq_of_lt (by omega))]
  omega

theorem Ua_eq_T_off_class (a n : ℕ) (h : n % 2 ^ (a + 1) ≠ 2 ^ (a + 1) - 1) : Ua a n = T n := by
  unfold Ua T
  rw [if_neg h]

theorem Ua_ne_T (a : ℕ) : Ua a (2 ^ (a + 1) - 1) ≠ T (2 ^ (a + 1) - 1) := by
  have hP : 0 < 2 ^ a := Nat.pos_of_ne_zero (by positivity)
  rw [Ua_at]
  have e : 2 ^ (a + 1) - 1 = 2 * (2 ^ a - 1) + 1 := by rw [pow_succ]; omega
  rw [e, T_odd]
  omega

/-- **Other-side sharpness**, packaged: for every `a`, `U_a` satisfies positivity, (I), (II),
`n < U n ≤ 2n + 1` at all odd `n`, (III) at all odd `n ≠ 2^(a+1) − 1`, and `U_a ≠ T`. -/
theorem sharp_upper (a : ℕ) :
    Pos (Ua a) ∧ PrefixProp (Ua a) ∧ LitProp (Ua a) ∧ CondII (Ua a) ∧
    (∀ n, n % 2 = 1 → n < Ua a n ∧ Ua a n ≤ 2 * n + 1) ∧
    (∀ n, n % 2 = 1 → n ≠ 2 ^ (a + 1) - 1 → n < Ua a n ∧ Ua a n ≤ 2 * n) ∧
    Ua a (2 ^ (a + 1) - 1) = 2 * (2 ^ (a + 1) - 1) + 1 ∧
    (∀ n, n % 2 ^ (a + 1) ≠ 2 ^ (a + 1) - 1 → Ua a n = T n) ∧
    Ua a (2 ^ (a + 1) - 1) ≠ T (2 ^ (a + 1) - 1) :=
  ⟨pos_Ua a, prefixProp_Ua a, litProp_Ua a, condII_Ua a, condIII_relaxed_Ua a, condIII_Ua a,
    Ua_at a, Ua_eq_T_off_class a, Ua_ne_T a⟩

end Rigidity
end CollatzFMF
