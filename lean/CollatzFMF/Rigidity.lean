import CollatzFMF.KLSound

/-!
# Rigidity of the `3x+1` map `T` (w2-gamma Lemma 1 and Theorem R)

Source: `notes/round6-nov2026/w2-gamma/REPORT.md` section (b), and
`notes/round6-nov2026/referee-gamma/REPORT.md`.

* `PrefixProp S` : valuation form of the parity-prefix property (I), stated with `padicValInt`.
* `DvdProp S`    : the same property stated with divisibility (no junk value `v2(0) = 0`).
* `LitProp S`    : the literal property (I): `n ≡ n' mod 2^k` iff the first `k` parities of the
  `S`-orbits of `n` and `n'` agree.
* `prefixProp_iff_dvdProp`, `litProp_iff_dvdProp`, `lemma1` : all three are equivalent
  (the last two for `S` mapping positives to positives) -- source Lemma 1.
* `prefixProp_T`, `litProp_T`, `pos_T`, `condII_T`, `condIII_T` : `T` has all the properties.
* `theoremR`, `theoremR_lit` : rigidity.

Everything in this file is complete (no `sorry`, no extra axioms).
-/

namespace CollatzFMF
namespace Rigidity

open KL (T)

/-! ## Definitions -/

/-- `S` maps positive integers to positive integers. -/
def Pos (S : ℕ → ℕ) : Prop := ∀ n, 0 < n → 0 < S n

/-- Parity-prefix property (I), valuation form (source Lemma 1):
`v2(S n − S n') + 1 = v2(n − n')` for distinct positive `n, n'` of equal parity. -/
def PrefixProp (S : ℕ → ℕ) : Prop :=
  ∀ n n', 0 < n → 0 < n' → n ≠ n' → n % 2 = n' % 2 →
    padicValInt 2 ((S n : ℤ) - (S n' : ℤ)) + 1 = padicValInt 2 ((n : ℤ) - (n' : ℤ))

/-- Parity-prefix property (I), divisibility form:
`2^k ∣ S n − S n'  ↔  2^(k+1) ∣ n − n'` for distinct positive `n, n'` of equal parity. -/
def DvdProp (S : ℕ → ℕ) : Prop :=
  ∀ n n', 0 < n → 0 < n' → n ≠ n' → n % 2 = n' % 2 →
    ∀ k : ℕ, (2 : ℤ) ^ k ∣ ((S n : ℤ) - (S n' : ℤ)) ↔ (2 : ℤ) ^ (k + 1) ∣ ((n : ℤ) - (n' : ℤ))

/-- Parity-prefix property (I), literal form: for positive `n, n'` and every `k`,
`n ≡ n' (mod 2^k)` iff the first `k` parities of the `S`-orbits agree. -/
def LitProp (S : ℕ → ℕ) : Prop :=
  ∀ n n', 0 < n → 0 < n' → ∀ k : ℕ,
    n % 2 ^ k = n' % 2 ^ k ↔ ∀ i, i < k → S^[i] n % 2 = S^[i] n' % 2

/-- (II): `S n < n` for even positive `n`. -/
def CondII (S : ℕ → ℕ) : Prop := ∀ n, 0 < n → n % 2 = 0 → S n < n

/-- (III): `n < S n ≤ 2n` for odd `n`. -/
def CondIII (S : ℕ → ℕ) : Prop := ∀ n, n % 2 = 1 → n < S n ∧ S n ≤ 2 * n

/-! ## 2-adic helpers -/

theorem two_pow_dvd_iff_le {z : ℤ} (hz : z ≠ 0) (k : ℕ) :
    (2 : ℤ) ^ k ∣ z ↔ k ≤ padicValInt 2 z := by
  have h := padicValInt_dvd_iff (p := 2) k z
  simpa [hz] using h

theorem val_succ_eq_iff {w u : ℤ} (hw : w ≠ 0) (hu : u ≠ 0) :
    padicValInt 2 w + 1 = padicValInt 2 u ↔
      ∀ k : ℕ, (2 : ℤ) ^ k ∣ w ↔ (2 : ℤ) ^ (k + 1) ∣ u := by
  constructor
  · intro h k
    rw [two_pow_dvd_iff_le hw, two_pow_dvd_iff_le hu]
    omega
  · intro h
    have h1 := h (padicValInt 2 w)
    rw [two_pow_dvd_iff_le hw, two_pow_dvd_iff_le hu] at h1
    have h2 := h (padicValInt 2 u - 1)
    rw [two_pow_dvd_iff_le hw, two_pow_dvd_iff_le hu] at h2
    omega

theorem exists_exact_pow {c : ℤ} (hc : c ≠ 0) :
    ∃ a : ℕ, (2 : ℤ) ^ a ∣ c ∧ ¬ (2 : ℤ) ^ (a + 1) ∣ c := by
  refine ⟨padicValInt 2 c, ?_, ?_⟩
  · rw [two_pow_dvd_iff_le hc]
  · rw [two_pow_dvd_iff_le hc]
    omega

theorem two_pow_le_abs {a : ℕ} {c : ℤ} (hc : c ≠ 0) (h : (2 : ℤ) ^ a ∣ c) :
    (2 : ℤ) ^ a ≤ |c| :=
  Int.le_of_dvd (abs_pos.mpr hc) ((dvd_abs _ _).mpr h)

theorem two_pow_dvd_three_mul (k : ℕ) (u : ℤ) : (2 : ℤ) ^ k ∣ 3 * u ↔ (2 : ℤ) ^ k ∣ u := by
  have hc : IsCoprime ((2 : ℤ) ^ k) 3 :=
    IsCoprime.pow_left ⟨-1, 1, by norm_num⟩
  exact ⟨fun h => hc.dvd_of_dvd_mul_left h, fun h => Dvd.dvd.mul_left h 3⟩

theorem dvd_even_case (x x' : ℤ) (k : ℕ) :
    (2 : ℤ) ^ (k + 1) ∣ 2 * x - 2 * x' ↔ (2 : ℤ) ^ k ∣ x - x' := by
  rw [pow_succ, ← mul_sub, mul_comm ((2 : ℤ) ^ k) 2]
  exact mul_dvd_mul_iff_left (by norm_num : (2 : ℤ) ≠ 0)

/-- If `w` and `u` have the same 2-adic valuation and `2^a ∣ u`, then `w ≡ u mod 2^(a+1)`. -/
theorem lip_of_dvd_iff {w u : ℤ} (h : ∀ k : ℕ, (2 : ℤ) ^ k ∣ w ↔ (2 : ℤ) ^ k ∣ u) {a : ℕ}
    (ha : (2 : ℤ) ^ a ∣ u) : (2 : ℤ) ^ (a + 1) ∣ w - u := by
  by_cases hu : (2 : ℤ) ^ (a + 1) ∣ u
  · exact dvd_sub ((h _).mpr hu) hu
  · have hw : ¬ (2 : ℤ) ^ (a + 1) ∣ w := fun hw => hu ((h _).mp hw)
    obtain ⟨w', rfl⟩ := (h a).mpr ha
    obtain ⟨u', rfl⟩ := ha
    have hp : (2 : ℤ) ^ a ≠ 0 := by positivity
    have hu' : ¬ (2 : ℤ) ∣ u' := fun hd => hu (by
      rw [pow_succ]; exact mul_dvd_mul_left _ hd)
    have hw' : ¬ (2 : ℤ) ∣ w' := fun hd => hw (by
      rw [pow_succ]; exact mul_dvd_mul_left _ hd)
    obtain ⟨c, hc⟩ : (2 : ℤ) ∣ w' - u' := by omega
    exact ⟨c, by rw [pow_succ]; linear_combination (2 : ℤ) ^ a * hc⟩

/-! ## Equivalence of the valuation form and the divisibility form -/

theorem dvdProp_ne {S : ℕ → ℕ} (h : DvdProp S) {n n' : ℕ} (hn : 0 < n) (hn' : 0 < n')
    (hne : n ≠ n') (hpar : n % 2 = n' % 2) : S n ≠ S n' := by
  intro heq
  have hu : (n : ℤ) - (n' : ℤ) ≠ 0 := sub_ne_zero.mpr (by exact_mod_cast hne)
  have h1 := (h n n' hn hn' hne hpar (padicValInt 2 ((n : ℤ) - n'))).mp (by simp [heq])
  rw [two_pow_dvd_iff_le hu] at h1
  omega

/-- The valuation form as specified (with Lean's junk value `padicValInt 2 0 = 0`) already
forces `S n ≠ S n'`, so it is faithful to the source's `v2` with `v2(0) = ∞`. -/
theorem prefixProp_ne {S : ℕ → ℕ} (h : PrefixProp S) {n n' : ℕ} (hn : 0 < n) (hn' : 0 < n')
    (hne : n ≠ n') (hpar : n % 2 = n' % 2) : S n ≠ S n' := by
  intro heq
  have hu : (n : ℤ) - (n' : ℤ) ≠ 0 := sub_ne_zero.mpr (by exact_mod_cast hne)
  -- `v2(n - n') = 1`
  have h0 := h n n' hn hn' hne hpar
  rw [heq, sub_self, padicValInt.zero] at h0
  have hnot4 : ¬ (2 : ℤ) ^ 2 ∣ (n : ℤ) - n' := by
    rw [two_pow_dvd_iff_le hu]; omega
  -- third point `m = n + 4`
  have e4 : (((n + 4 : ℕ) : ℤ)) - (n : ℤ) = 4 := by push_cast; ring
  have h4 : (4 : ℤ) ≠ 0 := by norm_num
  have hv4 : padicValInt 2 (4 : ℤ) = 2 := by
    have a1 := (two_pow_dvd_iff_le h4 2).mp (by norm_num)
    have a2 := (two_pow_dvd_iff_le h4 3).not.mp (by norm_num)
    omega
  have hm := h (n + 4) n (by omega) hn (by omega) (by omega)
  rw [e4, hv4] at hm
  by_cases hmn : n + 4 = n'
  · apply hnot4
    refine ⟨-1, ?_⟩
    rw [← hmn]; push_cast; ring
  · have hm' := h (n + 4) n' (by omega) hn' hmn (by omega)
    rw [← heq] at hm'
    have hu' : (((n + 4 : ℕ) : ℤ)) - (n' : ℤ) ≠ 0 := sub_ne_zero.mpr (by exact_mod_cast hmn)
    have hd : (2 : ℤ) ^ 2 ∣ (((n + 4 : ℕ) : ℤ)) - (n' : ℤ) := by
      rw [two_pow_dvd_iff_le hu']; omega
    apply hnot4
    have : (n : ℤ) - n' = ((((n + 4 : ℕ) : ℤ)) - (n' : ℤ)) - 2 ^ 2 := by push_cast; ring
    rw [this]
    exact dvd_sub hd dvd_rfl

theorem prefixProp_iff_dvdProp (S : ℕ → ℕ) : PrefixProp S ↔ DvdProp S := by
  constructor
  · intro h n n' hn hn' hne hpar
    have hu : (n : ℤ) - (n' : ℤ) ≠ 0 := sub_ne_zero.mpr (by exact_mod_cast hne)
    have hw : (S n : ℤ) - (S n' : ℤ) ≠ 0 :=
      sub_ne_zero.mpr (by exact_mod_cast prefixProp_ne h hn hn' hne hpar)
    exact (val_succ_eq_iff hw hu).mp (h n n' hn hn' hne hpar)
  · intro h n n' hn hn' hne hpar
    have hu : (n : ℤ) - (n' : ℤ) ≠ 0 := sub_ne_zero.mpr (by exact_mod_cast hne)
    have hw : (S n : ℤ) - (S n' : ℤ) ≠ 0 :=
      sub_ne_zero.mpr (by exact_mod_cast dvdProp_ne h hn hn' hne hpar)
    exact (val_succ_eq_iff hw hu).mpr (h n n' hn hn' hne hpar)

/-! ## Lemma 1: the literal form is equivalent to the valuation form -/

theorem mod_two_pow_eq_iff (n n' k : ℕ) :
    n % 2 ^ k = n' % 2 ^ k ↔ (2 : ℤ) ^ k ∣ (n : ℤ) - (n' : ℤ) := by
  have h : n' ≡ n [MOD 2 ^ k] ↔ ((2 ^ k : ℕ) : ℤ) ∣ (n : ℤ) - (n' : ℤ) := Nat.modEq_iff_dvd
  push_cast at h
  rw [← h]
  exact ⟨fun e => e.symm, fun e => e.symm⟩

theorem parity_iff (n n' : ℕ) : n % 2 = n' % 2 ↔ (2 : ℤ) ^ 1 ∣ (n : ℤ) - (n' : ℤ) := by
  rw [← mod_two_pow_eq_iff]; simp

theorem prefix_succ (S : ℕ → ℕ) (n n' k : ℕ) :
    (∀ i, i < k + 1 → S^[i] n % 2 = S^[i] n' % 2) ↔
      n % 2 = n' % 2 ∧ ∀ i, i < k → S^[i] (S n) % 2 = S^[i] (S n') % 2 := by
  constructor
  · intro h
    refine ⟨h 0 (by omega), fun i hi => ?_⟩
    have := h (i + 1) (by omega)
    simpa [Function.iterate_succ_apply] using this
  · rintro ⟨h0, h⟩ i hi
    cases i with
    | zero => simpa using h0
    | succ j =>
      have := h j (by omega)
      simpa [Function.iterate_succ_apply] using this

theorem dvdProp_of_litProp {S : ℕ → ℕ} (hpos : Pos S) (h : LitProp S) : DvdProp S := by
  intro n n' hn hn' _ hpar k
  rw [← mod_two_pow_eq_iff, ← mod_two_pow_eq_iff,
    h (S n) (S n') (hpos n hn) (hpos n' hn') k, h n n' hn hn' (k + 1), prefix_succ]
  exact ⟨fun hk => ⟨hpar, hk⟩, fun hk => hk.2⟩

theorem litProp_of_dvdProp {S : ℕ → ℕ} (hpos : Pos S) (h : DvdProp S) : LitProp S := by
  intro n n' hn hn' k
  induction k generalizing n n' with
  | zero => simp [Nat.mod_one]
  | succ k ih =>
    rw [prefix_succ, ← ih (S n) (S n') (hpos n hn) (hpos n' hn')]
    by_cases hne : n = n'
    · subst hne; simp
    · rw [mod_two_pow_eq_iff, mod_two_pow_eq_iff]
      constructor
      · intro hd
        have hpar : n % 2 = n' % 2 := by
          rw [parity_iff]
          exact (pow_dvd_pow 2 (by omega)).trans hd
        exact ⟨hpar, (h n n' hn hn' hne hpar k).mpr hd⟩
      · rintro ⟨hpar, hd⟩
        exact (h n n' hn hn' hne hpar k).mp hd

theorem litProp_iff_dvdProp {S : ℕ → ℕ} (hpos : Pos S) : LitProp S ↔ DvdProp S :=
  ⟨dvdProp_of_litProp hpos, litProp_of_dvdProp hpos⟩

/-- **Lemma 1** (w2-gamma): for `S : N → N`, the literal parity-prefix property (I) is
equivalent to the valuation identity `v2(S n − S n') = v2(n − n') − 1` on distinct
positive `n, n'` of equal parity. -/
theorem lemma1 {S : ℕ → ℕ} (hpos : Pos S) : LitProp S ↔ PrefixProp S := by
  rw [litProp_iff_dvdProp hpos, prefixProp_iff_dvdProp]

/-! ## `T` has all the properties -/

theorem T_even (x : ℕ) : T (2 * x) = x := by
  unfold T; split <;> omega

theorem T_odd (x : ℕ) : T (2 * x + 1) = 3 * x + 2 := by
  unfold T; split <;> omega

theorem dvdProp_T : DvdProp T := by
  intro n n' _ _ _ hpar k
  obtain ⟨x, rfl | rfl⟩ := Nat.even_or_odd' n <;>
    obtain ⟨x', rfl | rfl⟩ := Nat.even_or_odd' n'
  · rw [T_even, T_even]; push_cast
    exact (dvd_even_case _ _ _).symm
  · omega
  · omega
  · rw [T_odd, T_odd]; push_cast
    have e1 : (3 * (x : ℤ) + 2) - (3 * (x' : ℤ) + 2) = 3 * ((x : ℤ) - x') := by ring
    have e2 : (2 * (x : ℤ) + 1) - (2 * (x' : ℤ) + 1) = 2 * (x : ℤ) - 2 * x' := by ring
    rw [e1, e2, two_pow_dvd_three_mul, dvd_even_case]

theorem prefixProp_T : PrefixProp T := (prefixProp_iff_dvdProp T).mpr dvdProp_T

theorem pos_T : Pos T := by
  intro n hn; unfold T; split <;> omega

theorem condII_T : CondII T := by
  intro n hn he; unfold T; split <;> omega

theorem condIII_T : CondIII T := by
  intro n ho; unfold T; split <;> omega

theorem litProp_T : LitProp T := litProp_of_dvdProp pos_T dvdProp_T

/-! ## Theorem R -/

/-- The minimal-representative argument: a function `g : ℕ → ℤ` with `|g x| ≤ x` that is
2-adically "1-Lipschitz with a gain" (`x ≡ x' mod 2^a ⇒ g x ≡ g x' mod 2^(a+1)`) vanishes. -/
theorem descent (g : ℕ → ℤ) (hb : ∀ x, |g x| ≤ x)
    (hl : ∀ (x x' a : ℕ), x ≠ x' → (2 : ℤ) ^ a ∣ (x : ℤ) - (x' : ℤ) →
      (2 : ℤ) ^ (a + 1) ∣ g x - g x') : ∀ z, g z = 0 := by
  intro z
  by_contra hz
  obtain ⟨a, ha, hna⟩ := exists_exact_pow hz
  have h1 : (2 : ℤ) ^ a ≤ z := (two_pow_le_abs hz ha).trans (hb z)
  have hP : 0 < 2 ^ a := Nat.pos_of_ne_zero (by positivity)
  have hxlt : z % 2 ^ a < 2 ^ a := Nat.mod_lt _ hP
  have h1' : 2 ^ a ≤ z := by exact_mod_cast h1
  have hne : z ≠ z % 2 ^ a := by omega
  have hdvd : (2 : ℤ) ^ a ∣ (z : ℤ) - ((z % 2 ^ a : ℕ) : ℤ) := by
    rw [← mod_two_pow_eq_iff]; simp
  have h2 := hl z (z % 2 ^ a) a hne hdvd
  have hx0 : g (z % 2 ^ a) ≠ 0 := by
    intro h0; rw [h0, sub_zero] at h2; exact hna h2
  have hxa : (2 : ℤ) ^ a ∣ g (z % 2 ^ a) := by
    have := dvd_sub ha ((pow_dvd_pow 2 (Nat.le_succ a)).trans h2)
    simpa using this
  have h3 : (2 : ℤ) ^ a ≤ ((z % 2 ^ a : ℕ) : ℤ) := (two_pow_le_abs hx0 hxa).trans (hb _)
  have h3' : 2 ^ a ≤ z % 2 ^ a := by exact_mod_cast h3
  omega

/-- Even part of Theorem R: (I), (II) and positivity force `S (2x) = x`. -/
theorem even_part {S : ℕ → ℕ} (hpos : Pos S) (hD : DvdProp S) (hII : CondII S) :
    ∀ x, 0 < x → S (2 * x) = x := by
  have key := descent (fun y => (S (2 * (y + 1)) : ℤ) - ((y + 1 : ℕ) : ℤ)) (by
      intro y
      have h1 := hpos (2 * (y + 1)) (by omega)
      have h2 := hII (2 * (y + 1)) (by omega) (by omega)
      rw [abs_le]; push_cast; constructor <;> omega) (by
      intro y y' a hne hd
      have h := hD (2 * (y + 1)) (2 * (y' + 1)) (by omega) (by omega) (by omega) (by omega)
      have h' : ∀ k : ℕ, (2 : ℤ) ^ k ∣ (S (2 * (y + 1)) : ℤ) - (S (2 * (y' + 1)) : ℤ) ↔
          (2 : ℤ) ^ k ∣ (y : ℤ) - (y' : ℤ) := by
        intro k
        have : ((2 * (y + 1) : ℕ) : ℤ) - ((2 * (y' + 1) : ℕ) : ℤ) = 2 * (y : ℤ) - 2 * y' := by
          push_cast; ring
        rw [h k, this, dvd_even_case]
      have := lip_of_dvd_iff h' hd
      have e : (S (2 * (y + 1)) : ℤ) - ((y + 1 : ℕ) : ℤ) -
          ((S (2 * (y' + 1)) : ℤ) - ((y' + 1 : ℕ) : ℤ)) =
          (S (2 * (y + 1)) : ℤ) - (S (2 * (y' + 1)) : ℤ) - ((y : ℤ) - (y' : ℤ)) := by
        push_cast; ring
      show (2 : ℤ) ^ (a + 1) ∣ (S (2 * (y + 1)) : ℤ) - ((y + 1 : ℕ) : ℤ) -
          ((S (2 * (y' + 1)) : ℤ) - ((y' + 1 : ℕ) : ℤ))
      rw [e]; exact this)
  intro x hx
  obtain ⟨y, rfl⟩ : ∃ y, x = y + 1 := ⟨x - 1, by omega⟩
  have this : (S (2 * (y + 1)) : ℤ) - ((y + 1 : ℕ) : ℤ) = 0 := key y
  exact_mod_cast sub_eq_zero.mp this

/-- Odd part of Theorem R: (I) and (III) force `S (2x+1) = 3x+2 = T (2x+1)`. -/
theorem odd_part {S : ℕ → ℕ} (hD : DvdProp S) (hIII : CondIII S) :
    ∀ x, S (2 * x + 1) = 3 * x + 2 := by
  have key := descent (fun x => (S (2 * x + 1) : ℤ) - ((3 * x + 2 : ℕ) : ℤ)) (by
      intro x
      have h1 := hIII (2 * x + 1) (by omega)
      rw [abs_le]; push_cast; constructor <;> omega) (by
      intro x x' a hne hd
      have h := hD (2 * x + 1) (2 * x' + 1) (by omega) (by omega) (by omega) (by omega)
      have h' : ∀ k : ℕ, (2 : ℤ) ^ k ∣ (S (2 * x + 1) : ℤ) - (S (2 * x' + 1) : ℤ) ↔
          (2 : ℤ) ^ k ∣ 3 * ((x : ℤ) - (x' : ℤ)) := by
        intro k
        have : ((2 * x + 1 : ℕ) : ℤ) - ((2 * x' + 1 : ℕ) : ℤ) = 2 * (x : ℤ) - 2 * x' := by
          push_cast; ring
        rw [h k, this, dvd_even_case, two_pow_dvd_three_mul]
      have := lip_of_dvd_iff h' ((two_pow_dvd_three_mul a _).mpr hd)
      have e : (S (2 * x + 1) : ℤ) - ((3 * x + 2 : ℕ) : ℤ) -
          ((S (2 * x' + 1) : ℤ) - ((3 * x' + 2 : ℕ) : ℤ)) =
          (S (2 * x + 1) : ℤ) - (S (2 * x' + 1) : ℤ) - 3 * ((x : ℤ) - (x' : ℤ)) := by
        push_cast; ring
      show (2 : ℤ) ^ (a + 1) ∣ (S (2 * x + 1) : ℤ) - ((3 * x + 2 : ℕ) : ℤ) -
          ((S (2 * x' + 1) : ℤ) - ((3 * x' + 2 : ℕ) : ℤ))
      rw [e]; exact this)
  intro x
  have this : (S (2 * x + 1) : ℤ) - ((3 * x + 2 : ℕ) : ℤ) = 0 := key x
  exact_mod_cast sub_eq_zero.mp this

/-- Theorem R for the divisibility form. -/
theorem theoremR_dvd {S : ℕ → ℕ} (hpos : Pos S) (hI : DvdProp S) (hII : CondII S)
    (hIII : CondIII S) : ∀ n, 0 < n → S n = T n := by
  intro n hn
  obtain ⟨x, rfl | rfl⟩ := Nat.even_or_odd' n
  · rw [T_even]; exact even_part hpos hI hII x (by omega)
  · rw [T_odd]; exact odd_part hI hIII x

/-- **Theorem R (rigidity)**, valuation form of (I): if `S` maps positives to positives, has
the parity-prefix property, `S n < n` for even `n > 0`, and `n < S n ≤ 2n` for odd `n`,
then `S = T` on the positive integers. -/
theorem theoremR {S : ℕ → ℕ} (hpos : Pos S) (hI : PrefixProp S) (hII : CondII S)
    (hIII : CondIII S) : ∀ n, 0 < n → S n = T n :=
  theoremR_dvd hpos ((prefixProp_iff_dvdProp S).mp hI) hII hIII

/-- **Theorem R (rigidity)**, literal form of (I), exactly as in the source statement. -/
theorem theoremR_lit {S : ℕ → ℕ} (hpos : Pos S) (hI : LitProp S) (hII : CondII S)
    (hIII : CondIII S) : ∀ n, 0 < n → S n = T n :=
  theoremR_dvd hpos (dvdProp_of_litProp hpos hI) hII hIII

end Rigidity
end CollatzFMF
