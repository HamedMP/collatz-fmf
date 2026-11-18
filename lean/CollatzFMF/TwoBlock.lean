import CollatzFMF.Barrier

/-!
# Lemma L (weighted two-block lemma) and Theorem B (two-block exclusion)

Source: `notes/round6-nov2026/frontier/REPORT.md`, section (b).
Infinite words over the two block letters `c`, `d` are functions `y : ℕ → Bool`
(`true = c`, `false = d`).  Weights are natural numbers (in Theorem B they are `B X`, `B Y`).

Everything in this file is complete (no `sorry`, no extra axioms).
-/

namespace CollatzFMF
namespace Barrier

open Letter

/-- The factor `y[i, i+n)` of the infinite word `y`. -/
def seg (y : ℕ → Bool) (i n : ℕ) : List Bool := (List.range n).map fun t => y (i + t)

/-- Additive weight of a finite block word: `c ↦ lc`, `d ↦ ld`. -/
def wt (lc ld : ℕ) (v : List Bool) : ℕ := (v.map fun b => if b then lc else ld).sum

@[simp] theorem seg_zero (y : ℕ → Bool) (i : ℕ) : seg y i 0 = [] := rfl

theorem seg_succ (y : ℕ → Bool) (i n : ℕ) : seg y i (n + 1) = seg y i n ++ [y (i + n)] := by
  simp [seg, List.range_succ]

@[simp] theorem seg_length (y : ℕ → Bool) (i n : ℕ) : (seg y i n).length = n := by
  simp [seg]

theorem seg_add (y : ℕ → Bool) (i m n : ℕ) :
    seg y i (m + n) = seg y i m ++ seg y (i + m) n := by
  induction n with
  | zero => simp
  | succ n ih => rw [← Nat.add_assoc, seg_succ, ih, seg_succ, List.append_assoc, Nat.add_assoc]

theorem seg_const (y : ℕ → Bool) (i n : ℕ) (b : Bool) (h : ∀ t, t < n → y (i + t) = b) :
    seg y i n = List.replicate n b := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [seg_succ, ih (fun t ht => h t (by omega)), h n (by omega), List.replicate_succ']

@[simp] theorem wt_nil (lc ld : ℕ) : wt lc ld [] = 0 := rfl
@[simp] theorem wt_cons (lc ld : ℕ) (b : Bool) (v : List Bool) :
    wt lc ld (b :: v) = (if b then lc else ld) + wt lc ld v := by simp [wt]
@[simp] theorem wt_append (lc ld : ℕ) (u v : List Bool) :
    wt lc ld (u ++ v) = wt lc ld u + wt lc ld v := by simp [wt]
@[simp] theorem wt_replicate_true (lc ld n : ℕ) : wt lc ld (List.replicate n true) = n * lc := by
  simp [wt]
@[simp] theorem wt_replicate_false (lc ld n : ℕ) :
    wt lc ld (List.replicate n false) = n * ld := by
  simp [wt]

/-- **Lemma L (weighted two-block lemma).**  Every infinite word `y` over `{c,d}` starting with
`c`, with positive additive weights `lc`, `ld`, has a factor `u = y[i,i+n) = y[i',i'+n)`
occurring at positions `i < i'` with `l(y[0,i')) ≤ 3·l(u)` and `l(u) ≥ lc`. -/
theorem lemmaL (y : ℕ → Bool) (lc ld : ℕ) (hc : 0 < lc) (hd : 0 < ld) (h0 : y 0 = true) :
    ∃ i i' n, i < i' ∧ seg y i n = seg y i' n ∧
      wt lc ld (seg y 0 i') ≤ 3 * wt lc ld (seg y i' n) ∧ lc ≤ wt lc ld (seg y i' n) := by
  have hcd : lc ≤ lc * ld := Nat.le_mul_of_pos_right _ hd
  have hdc : ld ≤ lc * ld := Nat.le_mul_of_pos_left _ hc
  by_cases h1 : y 1 = true
  · -- y = c c ...
    refine ⟨0, 1, 1, by omega, ?_, ?_, ?_⟩ <;> simp [seg, h0, h1]
    omega
  have h1 : y 1 = false := by simpa using h1
  have hpre2 : seg y 0 2 = [true, false] := by simp [seg, List.range_succ, h0, h1]
  by_cases hall : ∀ t, 1 ≤ t → y t = false
  · -- y = c d^ω : u = d^lc at 1 and 2
    have e1 : seg y 1 lc = List.replicate lc false := seg_const _ _ _ _ fun t _ => hall _ (by omega)
    have e2 : seg y 2 lc = List.replicate lc false := seg_const _ _ _ _ fun t _ => hall _ (by omega)
    refine ⟨1, 2, lc, by omega, by rw [e1, e2], ?_, ?_⟩
    · rw [hpre2, e2]; simp; nlinarith
    · rw [e2]; simp; nlinarith
  -- first return of c
  have hex : ∃ t, 1 ≤ t ∧ y t = true := by
    by_contra hne
    exact hall fun t ht => by
      by_contra hf
      exact hne ⟨t, ht, by simpa using hf⟩
  classical
  obtain ⟨hm1, hm2⟩ := Nat.find_spec hex
  have hmin : ∀ t, 1 ≤ t → t < Nat.find hex → y t = false := by
    intro t ht1 ht2
    have := Nat.find_min hex ht2
    by_contra hf
    exact this ⟨ht1, by simpa using hf⟩
  generalize Nat.find hex = m at hm1 hm2 hmin
  have hm : 2 ≤ m := by
    rcases Nat.lt_or_ge m 2 with h | h
    · have : m = 1 := by omega
      subst this; rw [h1] at hm2; exact absurd hm2 (by simp)
    · exact h
  obtain ⟨k, rfl⟩ : ∃ k, m = k + 1 := ⟨m - 1, by omega⟩
  have hk1 : 1 ≤ k := by omega
  -- y = c d^k c ...
  have hprek : seg y 0 (k + 1) = [true] ++ List.replicate k false := by
    rw [Nat.add_comm k 1, seg_add]
    congr 1
    · simp [seg, h0]
    · exact seg_const _ _ _ _ fun t ht => hmin _ (by omega) (by omega)
  by_cases hk : k * ld ≤ 2 * lc
  · -- u = c at 0 and k+1
    refine ⟨0, k + 1, 1, by omega, ?_, ?_, ?_⟩
    · simp [seg, h0, hm2]
    · rw [hprek]; simp [seg, hm2]; omega
    · simp [seg, hm2]
  have hk : 2 * lc < k * ld := by omega
  by_cases hk2 : 2 ≤ k
  · -- u = d^(k-1) at 1 and 2
    obtain ⟨k', rfl⟩ : ∃ k', k = k' + 2 := ⟨k - 2, by omega⟩
    have e1 : seg y 1 (k' + 1) = List.replicate (k' + 1) false :=
      seg_const _ _ _ _ fun t ht => hmin _ (by omega) (by omega)
    have e2 : seg y 2 (k' + 1) = List.replicate (k' + 1) false :=
      seg_const _ _ _ _ fun t ht => hmin _ (by omega) (by omega)
    refine ⟨1, 2, k' + 1, by omega, by rw [e1, e2], ?_, ?_⟩
    · rw [hpre2, e2]; simp; nlinarith
    · rw [e2]; simp; nlinarith
  -- k = 1 : y = c d c ..., ld > 2 lc
  have hk' : k = 1 := by omega
  subst hk'
  have h2 : y 2 = true := hm2
  have hρ : 2 * lc < ld := by omega
  have hpre3 : seg y 0 3 = [true, false, true] := by simp [seg, List.range_succ, h0, h1, h2]
  by_cases hall2 : ∀ t, 2 ≤ t → y t = true
  · -- y = c d c^ω : u = c^(ld+1) at 2 and 3
    have e1 : seg y 2 (ld + 1) = List.replicate (ld + 1) true :=
      seg_const _ _ _ _ fun t _ => hall2 _ (by omega)
    have e2 : seg y 3 (ld + 1) = List.replicate (ld + 1) true :=
      seg_const _ _ _ _ fun t _ => hall2 _ (by omega)
    refine ⟨2, 3, ld + 1, by omega, by rw [e1, e2], ?_, ?_⟩
    · rw [hpre3, e2]; simp; nlinarith
    · rw [e2]; simp; nlinarith
  have hex2 : ∃ t, 2 ≤ t ∧ y t = false := by
    by_contra hne
    exact hall2 fun t ht => by
      by_contra hf
      exact hne ⟨t, ht, by simpa using hf⟩
  obtain ⟨hn1, hn2⟩ := Nat.find_spec hex2
  have hmin2 : ∀ t, 2 ≤ t → t < Nat.find hex2 → y t = true := by
    intro t ht1 ht2
    have := Nat.find_min hex2 ht2
    by_contra hf
    exact this ⟨ht1, by simpa using hf⟩
  generalize Nat.find hex2 = m2 at hn1 hn2 hmin2
  have hm3 : 3 ≤ m2 := by
    rcases Nat.lt_or_ge m2 3 with h | h
    · have : m2 = 2 := by omega
      subst this; rw [h2] at hn2; exact absurd hn2 (by simp)
    · exact h
  obtain ⟨j, rfl⟩ : ∃ j, m2 = j + 2 := ⟨m2 - 2, by omega⟩
  have hj1 : 1 ≤ j := by omega
  -- y = c d c^j d ...
  by_cases hj : 2 ≤ j ∧ ld + 5 * lc ≤ 3 * j * lc
  · -- u = c^(j-1) at 2 and 3
    obtain ⟨hj2, hjρ⟩ := hj
    obtain ⟨j', rfl⟩ : ∃ j', j = j' + 2 := ⟨j - 2, by omega⟩
    have e1 : seg y 2 (j' + 1) = List.replicate (j' + 1) true :=
      seg_const _ _ _ _ fun t ht => hmin2 _ (by omega) (by omega)
    have e2 : seg y 3 (j' + 1) = List.replicate (j' + 1) true :=
      seg_const _ _ _ _ fun t ht => hmin2 _ (by omega) (by omega)
    refine ⟨2, 3, j' + 1, by omega, by rw [e1, e2], ?_, ?_⟩
    · rw [hpre3, e2]; simp; nlinarith
    · rw [e2]; simp; nlinarith
  · -- u = d at 1 and j+2
    have hprej : seg y 0 (j + 2) = [true, false] ++ List.replicate j true := by
      rw [Nat.add_comm j 2, seg_add, hpre2]
      congr 1
      exact seg_const _ _ _ _ fun t ht => hmin2 _ (by omega) (by omega)
    refine ⟨1, j + 2, 1, by omega, ?_, ?_, ?_⟩
    · simp [seg, h1, hn2]
    · rw [hprej]; simp [seg, hn2]
      rcases Nat.lt_or_ge j 2 with hjlt | hjge
      · have : j = 1 := by omega
        subst this; omega
      · have hjρ : 3 * j * lc < ld + 5 * lc := by
          by_contra hcon; exact hj ⟨hjge, by omega⟩
        rcases Nat.lt_or_ge j 3 with hj3 | hj3
        · have : j = 2 := by omega
          subst this; omega
        · obtain ⟨j', rfl⟩ : ∃ j', j = j' + 3 := ⟨j - 3, by omega⟩
          nlinarith [Nat.zero_le (j' * lc)]
    · simp [seg, hn2]; omega

/-! ### Theorem B -/

/-- The `{a,b}`-word of a block word: `c ↦ X`, `d ↦ Y`. -/
def blk (X Y : List Letter) : List Bool → List Letter
  | [] => []
  | x :: v => (if x then X else Y) ++ blk X Y v

@[simp] theorem blk_nil (X Y : List Letter) : blk X Y [] = [] := rfl

theorem blk_append (X Y : List Letter) (u v : List Bool) :
    blk X Y (u ++ v) = blk X Y u ++ blk X Y v := by
  induction u with
  | nil => rfl
  | cons b u ih => simp [blk, ih]

theorem B_blk (X Y : List Letter) (v : List Bool) : B (blk X Y v) = wt (B X) (B Y) v := by
  induction v with
  | nil => rfl
  | cons b v ih => cases b <;> simp [blk, ih]

theorem blk_ne_nil {X Y : List Letter} (hX : X ≠ []) (hY : Y ≠ []) {v : List Bool}
    (hv : v ≠ []) : blk X Y v ≠ [] := by
  cases v with
  | nil => exact absurd rfl hv
  | cons b v => cases b <;> simp [blk, hX, hY]

/-- Pure arithmetic behind Theorem B: from the barrier `2^(Bu+Bp) < (w+1)·3^ep`,
`4 ep ≤ 3 Bp`, `Bp ≤ 3 Bu`, `BX ≤ Bu`, get `2^(16 BX) < (w+1)^4 · 3^(9 BX)`
(the integer certificate is `3^9 < 2^16`, together with `16 < 27`). -/
theorem twoBlock_arith {w Bu Bp ep BX : ℕ} (h : 2 ^ (Bu + Bp) < (w + 1) * 3 ^ ep)
    (h1 : 4 * ep ≤ 3 * Bp) (h2 : Bp ≤ 3 * Bu) (h3 : BX ≤ Bu) :
    2 ^ (16 * BX) < (w + 1) ^ 4 * 3 ^ (9 * BX) := by
  obtain ⟨k, hk⟩ : ∃ k, 3 * Bu = Bp + k := ⟨3 * Bu - Bp, by omega⟩
  obtain ⟨d, hd⟩ : ∃ d, Bu = BX + d := ⟨Bu - BX, by omega⟩
  -- fourth power
  have h4 : (2 ^ (Bu + Bp)) ^ 4 < ((w + 1) * 3 ^ ep) ^ 4 :=
    Nat.pow_lt_pow_left h (by norm_num)
  have h5 : ((w + 1) * 3 ^ ep) ^ 4 ≤ (w + 1) ^ 4 * 3 ^ (3 * Bp) := by
    rw [mul_pow, ← pow_mul]
    exact Nat.mul_le_mul_left _ (Nat.pow_le_pow_right (by norm_num) (by omega))
  have h6 : 2 ^ (4 * Bu + 4 * Bp) < (w + 1) ^ 4 * 3 ^ (3 * Bp) := by
    have : (2 ^ (Bu + Bp)) ^ 4 = 2 ^ (4 * Bu + 4 * Bp) := by rw [← pow_mul]; congr 1; ring
    rw [← this]; exact lt_of_lt_of_le h4 h5
  -- multiply by 27^k ≥ 16^k
  have h7 : (2 : ℕ) ^ (4 * k) ≤ 3 ^ (3 * k) := by
    rw [pow_mul, pow_mul]; exact Nat.pow_le_pow_left (by norm_num) k
  have h8 : 2 ^ (16 * Bu) < (w + 1) ^ 4 * 3 ^ (9 * Bu) := by
    have e1 : 16 * Bu = (4 * Bu + 4 * Bp) + 4 * k := by omega
    have e2 : 9 * Bu = 3 * Bp + 3 * k := by omega
    rw [e1, e2, pow_add _ (4 * Bu + 4 * Bp), pow_add _ (3 * Bp), ← mul_assoc]
    calc 2 ^ (4 * Bu + 4 * Bp) * 2 ^ (4 * k) ≤ 2 ^ (4 * Bu + 4 * Bp) * 3 ^ (3 * k) :=
          Nat.mul_le_mul_left _ h7
      _ < (w + 1) ^ 4 * 3 ^ (3 * Bp) * 3 ^ (3 * k) :=
          Nat.mul_lt_mul_of_pos_right h6 (by positivity)
  -- descend from Bu to BX using 3^9 ≤ 2^16
  have h9 : (3 : ℕ) ^ (9 * d) ≤ 2 ^ (16 * d) := by
    rw [pow_mul, pow_mul]; exact Nat.pow_le_pow_left (by norm_num) d
  by_contra hcon
  have hcon : (w + 1) ^ 4 * 3 ^ (9 * BX) ≤ 2 ^ (16 * BX) := by omega
  have : (w + 1) ^ 4 * 3 ^ (9 * Bu) ≤ 2 ^ (16 * Bu) := by
    have e1 : 16 * Bu = 16 * BX + 16 * d := by omega
    have e2 : 9 * Bu = 9 * BX + 9 * d := by omega
    rw [e1, e2, pow_add, pow_add, ← mul_assoc]
    exact Nat.mul_le_mul hcon h9
  omega

/-- **Theorem B (two-block exclusion), integer form.**  Let `X, Y` be nonempty words over
`{a,b}` and suppose the itinerary of `w₀ ≥ 1` lies in `{X,Y}^ω` with first block `X`: there is
an infinite block word `y` with `y 0 = c` such that every finite block prefix of `y`, spelled
out over `{a,b}`, is admissible at `w₀`.  Then `(w₀+1)^4 · 3^(9·B X) > 2^(16·B X)`. -/
theorem theoremB (X Y : List Letter) (hX : X ≠ []) (hY : Y ≠ []) (y : ℕ → Bool)
    (h0 : y 0 = true) (w0 : ℕ) (hw : 1 ≤ w0)
    (hrun : ∀ n, ∃ w', Run (blk X Y (seg y 0 n)) w0 w') :
    2 ^ (16 * B X) < (w0 + 1) ^ 4 * 3 ^ (9 * B X) := by
  obtain ⟨i, i', n, hii, hseg, hL1, hL2⟩ := lemmaL y (B X) (B Y) (B_pos hX) (B_pos hY) h0
  obtain ⟨d, rfl⟩ : ∃ d, i' = i + d := ⟨i' - i, by omega⟩
  have hd : 0 < d := by omega
  -- the two occurrences
  obtain ⟨z, hz⟩ := hrun (i + d + n)
  rw [seg_add, seg_add, Nat.zero_add, blk_append, blk_append, Nat.zero_add] at hz
  obtain ⟨wi', hp, hu'⟩ := run_append.mp hz
  obtain ⟨wi, hq, ht⟩ := run_append.mp hp
  obtain ⟨z2, hz2⟩ := hrun (i + n)
  rw [seg_add, Nat.zero_add, blk_append] at hz2
  obtain ⟨wi2, hq2, hu⟩ := run_append.mp hz2
  obtain rfl := run_unique hq hq2
  rw [hseg] at hu
  have htne : blk X Y (seg y i d) ≠ [] := by
    apply blk_ne_nil hX hY
    intro hnil
    have := congrArg List.length hnil
    simp at this; omega
  have hA := (barrier_core hw hq ht htne hu hu').2.2
  have hpe : seg y 0 (i + d) = seg y 0 i ++ seg y i d := by rw [seg_add, Nat.zero_add]
  rw [← blk_append, ← hpe] at hA
  have hBu : B (blk X Y (seg y (i + d) n)) = wt (B X) (B Y) (seg y (i + d) n) := B_blk _ _ _
  have hBp : B (blk X Y (seg y 0 (i + d))) = wt (B X) (B Y) (seg y 0 (i + d)) := B_blk _ _ _
  exact twoBlock_arith hA (four_e_le_three_B _) (by rw [hBu, hBp]; exact hL1)
    (by rw [hBu]; exact hL2)

/-- **Theorem B, finite form, first case**: the conclusion already holds when the itinerary
begins with the block word `X X`. -/
theorem theoremB_XX (X : List Letter) (hX : X ≠ []) (w0 w' : ℕ) (hw : 1 ≤ w0)
    (hrun : Run (X ++ X) w0 w') : 2 ^ (16 * B X) < (w0 + 1) ^ 4 * 3 ^ (9 * B X) := by
  obtain ⟨wi', ht, hu'⟩ := run_append.mp hrun
  have hA := (barrier_core (q := []) hw rfl ht hX ht hu').2.2
  simp only [List.nil_append] at hA
  exact twoBlock_arith hA (four_e_le_three_B _) (by omega) le_rfl

/-- **Corollary B2 (hierarchies), integer form.**  A positive integer cannot have an itinerary
that is two-block decomposable (first block `X`) with `B X` arbitrarily large:
the bound gives `B X < (w₀+1)^4`. -/
theorem theoremB_bound (X Y : List Letter) (hX : X ≠ []) (hY : Y ≠ []) (y : ℕ → Bool)
    (h0 : y 0 = true) (w0 : ℕ) (hw : 1 ≤ w0)
    (hrun : ∀ n, ∃ w', Run (blk X Y (seg y 0 n)) w0 w') :
    B X < (w0 + 1) ^ 4 := by
  have h := theoremB X Y hX hY y h0 w0 hw hrun
  have h1 : (3 : ℕ) ^ (10 * B X) ≤ 2 ^ (16 * B X) := by
    rw [pow_mul, pow_mul]; exact Nat.pow_le_pow_left (by norm_num) _
  have h2 : (3 : ℕ) ^ (10 * B X) = 3 ^ B X * 3 ^ (9 * B X) := by rw [← pow_add]; congr 1; omega
  have h3 : 3 ^ B X * 3 ^ (9 * B X) < (w0 + 1) ^ 4 * 3 ^ (9 * B X) := by omega
  have h4 : 3 ^ B X < (w0 + 1) ^ 4 := Nat.lt_of_mul_lt_mul_right h3
  exact lt_trans (Nat.lt_pow_self (by norm_num)) h4

theorem no_twoBlock_hierarchy (w0 : ℕ) (hw : 1 ≤ w0) :
    ¬ ∀ N : ℕ, ∃ (X Y : List Letter) (y : ℕ → Bool), X ≠ [] ∧ Y ≠ [] ∧ y 0 = true ∧ N ≤ B X ∧
      ∀ n, ∃ w', Run (blk X Y (seg y 0 n)) w0 w' := by
  intro h
  obtain ⟨X, Y, y, hX, hY, h0, hN, hrun⟩ := h ((w0 + 1) ^ 4)
  have := theoremB_bound X Y hX hY y h0 w0 hw hrun
  omega

/-! ### Sanity examples -/

-- 71 → 80 → 135 → 152 reads `a b a`; with X = [a] this is not of the form X X, but
-- 7 → 8 shows `a a` fails at 7.  A genuine `X X` start: X = [b], w₀ = 256: 256 → 432 → 729.
example : Run ([b] ++ [b]) 256 729 := ⟨432, by decide, 729, by decide, rfl⟩
example : 2 ^ (16 * B [b]) < (256 + 1) ^ 4 * 3 ^ (9 * B [b]) :=
  theoremB_XX [b] (by simp) 256 729 (by norm_num) ⟨432, by decide, 729, by decide, rfl⟩
example : (2 : ℕ) ^ (16 * 4) = 18446744073709551616 ∧
    (256 + 1) ^ 4 * 3 ^ (9 * 4) = 654783403832048509485517521 := by norm_num
-- the integer certificate
example : (3 : ℕ) ^ 9 < 2 ^ 16 := by norm_num
-- the litmus: for multiplier 5 the certificate fails
example : ¬ (5 : ℕ) ^ 9 < 2 ^ 16 := by norm_num

end Barrier
end CollatzFMF
