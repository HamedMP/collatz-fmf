import CollatzFMF.KLSound

/-!
# Theorem H (harmonic sums along distinct stretches of a `T`-trajectory)

Source: `notes/round6-nov2026/w2-delta/REPORT.md` section (b), Lemmas 1–3 and Theorem H;
referee notes `notes/round6-nov2026/referee-delta/REPORT.md`.

* `oddCount L x` : number of odd terms among `x, T x, …, T^[L-1] x`.
* `lemma1` : `2^L * T^[L] x = 3^a * x + r` with `r * 2^a + 2^L * 2^a ≤ 3^a * 2^L`.
* `lemma2` : descent `2^s * T^[L] x ≤ x` for good parity data.
* `lemma3` : the ancestor sum bound `Σ_{k ∈ A_t} 1/x_k ≤ 2/(2^s x_t)`.
* `theoremH` : `Σ_{k<K} 1/x_k ≤ (β+1)/(1 - 2/2^s)` under the bad-mass hypothesis `hβ`.

Everything in this file is complete (no `sorry`, no extra axioms).
-/

namespace CollatzFMF
namespace Harmonic

open KL (T)

/-! ## Misformalization guards for `T` -/

example : T 0 = 0 := by decide
example : T 1 = 2 := by decide
example : T 2 = 1 := by decide
example : T 7 = 11 := by decide
example : T 27 = 41 := by decide
example : T^[5] 27 = 71 := by decide
example : T^[4] 16 = 1 := by decide

theorem two_mul_T_even {x : ℕ} (h : x % 2 = 0) : 2 * T x = x := by
  unfold T; split <;> omega

theorem two_mul_T_odd {x : ℕ} (h : x % 2 = 1) : 2 * T x = 3 * x + 1 := by
  unfold T; split <;> omega

/-- Number of odd terms among `x, T x, …, T^[L-1] x`. -/
def oddCount : ℕ → ℕ → ℕ
  | 0, _ => 0
  | L + 1, x => x % 2 + oddCount L (T x)

theorem oddCount_eq_sum (L x : ℕ) :
    oddCount L x = ∑ i ∈ Finset.range L, T^[i] x % 2 := by
  induction L generalizing x with
  | zero => simp [oddCount]
  | succ L ih =>
    rw [oddCount, ih (T x), Finset.sum_range_succ']
    simp only [Function.iterate_succ_apply, Function.iterate_zero, id_eq]
    exact Nat.add_comm _ _

/-- Guard: `oddCount` really is the number of odd terms among the first `L` iterates. -/
theorem oddCount_eq_card (L x : ℕ) :
    oddCount L x = ((Finset.range L).filter fun i => T^[i] x % 2 = 1).card := by
  rw [oddCount_eq_sum, Finset.card_filter]
  refine Finset.sum_congr rfl fun i _ => ?_
  split <;> omega

theorem oddCount_le (L x : ℕ) : oddCount L x ≤ L := by
  induction L generalizing x with
  | zero => simp [oddCount]
  | succ L ih =>
    have := ih (T x)
    have : x % 2 < 2 := Nat.mod_lt _ (by norm_num)
    rw [oddCount]; omega

/-! ## Lemma 1 (affine form) -/

/-- **Lemma 1 (affine form, integers).** With `a = oddCount L x`:
`2^L * T^L(x) = 3^a * x + r` with `r * 2^a + 2^L * 2^a ≤ 3^a * 2^L`,
i.e. `r / 2^L ≤ (3/2)^a - 1`. -/
theorem lemma1 (L x : ℕ) :
    ∃ r : ℕ, 2 ^ L * T^[L] x = 3 ^ oddCount L x * x + r ∧
      r * 2 ^ oddCount L x + 2 ^ L * 2 ^ oddCount L x ≤ 3 ^ oddCount L x * 2 ^ L := by
  induction L generalizing x with
  | zero => exact ⟨0, by simp [oddCount], by simp [oddCount]⟩
  | succ L ih =>
    obtain ⟨r', h1, h2⟩ := ih (T x)
    have hle := oddCount_le L (T x)
    rw [Function.iterate_succ_apply]
    rcases Nat.mod_two_eq_zero_or_one x with h | h
    · have hT := two_mul_T_even h
      have ha : oddCount (L + 1) x = oddCount L (T x) := by rw [oddCount, h, Nat.zero_add]
      rw [ha]
      generalize oddCount L (T x) = a at *
      generalize T^[L] (T x) = y at *
      refine ⟨2 * r', ?_, ?_⟩
      · have : 2 * (3 ^ a * T x) = 3 ^ a * x := by
          rw [show 2 * (3 ^ a * T x) = 3 ^ a * (2 * T x) by ring, hT]
        rw [pow_succ]; linarith
      · rw [pow_succ]; linarith
    · have hT := two_mul_T_odd h
      have ha : oddCount (L + 1) x = oddCount L (T x) + 1 := by rw [oddCount, h, Nat.add_comm]
      rw [ha]
      generalize oddCount L (T x) = a at *
      generalize T^[L] (T x) = y at *
      refine ⟨3 ^ a + 2 * r', ?_, ?_⟩
      · have : 2 * (3 ^ a * T x) = 3 ^ a * (3 * x + 1) := by
          rw [show 2 * (3 ^ a * T x) = 3 ^ a * (2 * T x) by ring, hT]
        rw [pow_succ, pow_succ]; linarith
      · have hB : (2:ℕ) ^ a ≤ 2 ^ L := Nat.pow_le_pow_right (by norm_num) hle
        have hAB : 3 ^ a * 2 ^ a ≤ 3 ^ a * 2 ^ L := Nat.mul_le_mul_left _ hB
        rw [pow_succ, pow_succ, pow_succ]; linarith

/-- Guards: the affine identity on concrete numbers (cross-checked in Python). -/
example : oddCount 4 27 = 3 := by decide
example : 2 ^ 4 * T^[4] 27 = 3 ^ 3 * 27 + 23 := by decide
example : 23 * 2 ^ 3 + 2 ^ 4 * 2 ^ 3 ≤ 3 ^ 3 * 2 ^ 4 := by decide
example : oddCount 6 97 = 4 := by decide
example : 2 ^ 6 * T^[6] 97 = 3 ^ 4 * 97 + 143 := by decide

theorem iterate_pos {x : ℕ} (hx : 0 < x) (L : ℕ) : 0 < T^[L] x := by
  obtain ⟨r, h1, -⟩ := lemma1 L x
  by_contra h0
  have h0' : T^[L] x = 0 := by omega
  rw [h0', Nat.mul_zero] at h1
  have : 0 < 3 ^ oddCount L x * x := Nat.mul_pos (by positivity) hx
  omega

/-! ## Lemma 2 (descent) -/

/-- **Lemma 2 (descent).** If `2^L ≤ x` and `3^a (2^a + 1) 2^s ≤ 2^(L+a)`
(integer form of `3^a (1 + 2^(-a)) ≤ 2^(L-s)`), then `2^s * T^L(x) ≤ x`. -/
theorem lemma2 (L s x : ℕ) (hx : 2 ^ L ≤ x)
    (hg : 3 ^ oddCount L x * (2 ^ oddCount L x + 1) * 2 ^ s ≤ 2 ^ (L + oddCount L x)) :
    2 ^ s * T^[L] x ≤ x := by
  obtain ⟨r, h1, h2⟩ := lemma1 L x
  rw [pow_add] at hg
  generalize oddCount L x = a at *
  generalize T^[L] x = y at *
  have hP : 0 < 2 ^ L * 2 ^ a := by positivity
  refine Nat.le_of_mul_le_mul_left ?_ hP
  have e1 : 2 ^ s * (r * 2 ^ a + 2 ^ L * 2 ^ a) ≤ 2 ^ s * (3 ^ a * 2 ^ L) :=
    Nat.mul_le_mul_left _ h2
  have e2 : 2 ^ s * 3 ^ a * 2 ^ L ≤ 2 ^ s * 3 ^ a * x := Nat.mul_le_mul_left _ hx
  have e3 : 3 ^ a * (2 ^ a + 1) * 2 ^ s * x ≤ 2 ^ L * 2 ^ a * x := Nat.mul_le_mul_right _ hg
  have e4 : 2 ^ a * 2 ^ s * (2 ^ L * y) = 2 ^ a * 2 ^ s * (3 ^ a * x + r) := by rw [h1]
  nlinarith [e1, e2, e3, e4]

/-- `x` is **good** for `s`: Lemma 2's hypothesis with `L = ⌊log₂ x⌋`. -/
def Good (s x : ℕ) : Prop :=
  3 ^ oddCount (Nat.log 2 x) x * (2 ^ oddCount (Nat.log 2 x) x + 1) * 2 ^ s
    ≤ 2 ^ (Nat.log 2 x + oddCount (Nat.log 2 x) x)

instance (s x : ℕ) : Decidable (Good s x) := by unfold Good; infer_instance

theorem good_pos {s x : ℕ} (h : Good s x) : 0 < x := by
  by_contra h0
  have hx : x = 0 := by omega
  subst hx
  have : 0 < 2 ^ s := by positivity
  simp [Good, oddCount] at h
  omega

/-- Descent for good integers. -/
theorem good_descent {s x : ℕ} (h : Good s x) : 2 ^ s * T^[Nat.log 2 x] x ≤ x :=
  lemma2 _ s x (Nat.pow_log_le_self 2 (good_pos h).ne') h

/-- Guard: the hypothesis of Lemma 2 is satisfiable (`16` is good for `s = 3`) … -/
theorem good_16 : Good 3 16 := by
  have h : Nat.log 2 16 = 4 := by
    rw [show (16:ℕ) = 2 ^ 4 by norm_num]; exact Nat.log_pow (by norm_num) 4
  unfold Good; rw [h]; decide

/-- … and not always satisfied (`27` is bad for `s = 3`). -/
theorem bad_27 : ¬ Good 3 27 := by
  have h : Nat.log 2 27 = 4 := by
    rw [Nat.log_eq_iff (by norm_num)]; norm_num
  unfold Good; rw [h]; decide

/-! ## Lemma 3 (ancestors) -/

theorem seq_iterate {x : ℕ → ℕ} (hx : ∀ k, x (k + 1) = T (x k)) (k L : ℕ) :
    x (k + L) = T^[L] (x k) := by
  induction L with
  | zero => rfl
  | succ L ih => rw [← Nat.add_assoc, hx, ih, Function.iterate_succ_apply']

/-- Reciprocal sum of positive reals that at least double (ordered by decreasing index). -/
theorem sum_inv_le_of_doubling (f : ℕ → ℝ) (S : Finset ℕ) (hpos : ∀ k ∈ S, 0 < f k)
    (hd : ∀ k' ∈ S, ∀ k ∈ S, k' < k → 2 * f k ≤ f k') :
    ∀ c : ℝ, 0 < c → (∀ k ∈ S, 2 * c ≤ f k) → ∑ k ∈ S, 1 / f k ≤ 1 / c := by
  induction S using Finset.induction_on_max with
  | empty => intro c hc _; simp; positivity
  | insert a S ha ih =>
    intro c hc hlow
    have haS : a ∉ S := fun h => lt_irrefl _ (ha a h)
    rw [Finset.sum_insert haS]
    have hfa := hpos a (Finset.mem_insert_self _ _)
    have h1 := ih (fun k hk => hpos k (Finset.mem_insert_of_mem hk))
      (fun k' hk' k hk => hd k' (Finset.mem_insert_of_mem hk') k (Finset.mem_insert_of_mem hk))
      (f a) hfa
      (fun k hk => hd k (Finset.mem_insert_of_mem hk) a (Finset.mem_insert_self _ _) (ha k hk))
    have h2 : 1 / f a + 1 / f a ≤ 1 / c := by
      rw [← add_div, div_le_div_iff₀ hfa hc]
      have := hlow a (Finset.mem_insert_self _ _)
      linarith
    linarith

/-- Sub-fact of Lemma 3: two good indices `k' < k` with the same target `t = k + level`
have `2 * x k ≤ x k'` (levels are distinct; the level cannot drop across an odd step;
adjacent levels force `x k' = 2 * x k`). -/
theorem ancestors_double {x : ℕ → ℕ} (hx : ∀ k, x (k + 1) = T (x k)) {k' k t : ℕ}
    (hk' : k' + Nat.log 2 (x k') = t) (hk : k + Nat.log 2 (x k) = t)
    (hpos' : 0 < x k') (hlt : k' < k) : 2 * x k ≤ x k' := by
  have hup : x k < 2 ^ (Nat.log 2 (x k) + 1) := Nat.lt_pow_succ_log_self (by norm_num) _
  have hlow : 2 ^ Nat.log 2 (x k') ≤ x k' := Nat.pow_log_le_self 2 hpos'.ne'
  by_cases hadj : k = k' + 1
  · subst hadj
    rcases Nat.mod_two_eq_zero_or_one (x k') with h | h
    · have := two_mul_T_even h
      rw [hx]; omega
    · exfalso
      have h3 := two_mul_T_odd h
      have hmono : x k' ≤ x (k' + 1) := by rw [hx]; omega
      have := Nat.log_mono_right (b := 2) hmono
      omega
  · have hL : Nat.log 2 (x k) + 2 ≤ Nat.log 2 (x k') := by omega
    have h4 : 2 ^ (Nat.log 2 (x k) + 2) ≤ 2 ^ Nat.log 2 (x k') :=
      Nat.pow_le_pow_right (by norm_num) hL
    rw [pow_succ] at hup h4
    rw [pow_succ] at h4
    omega

/-- **Lemma 3 (ancestors).** For a `T`-sequence `x` and a target index `t`, the good indices
`k < K` with `k + ⌊log₂ x_k⌋ = t` satisfy `Σ 1/x_k ≤ 2/(2^s x_t)`.
(Neither `t < K` nor pairwise distinctness is needed.) -/
theorem lemma3 (s : ℕ) (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K t : ℕ) :
    ∑ k ∈ (Finset.range K).filter (fun k => k + Nat.log 2 (x k) = t ∧ Good s (x k)),
        (1 / (x k : ℝ))
      ≤ 2 / (2 ^ s * (x t : ℝ)) := by
  set A := (Finset.range K).filter (fun k => k + Nat.log 2 (x k) = t ∧ Good s (x k)) with hA
  have hmem : ∀ k ∈ A, k + Nat.log 2 (x k) = t ∧ Good s (x k) := fun k hk =>
    (Finset.mem_filter.mp hk).2
  have hdesc : ∀ k ∈ A, 2 ^ s * x t ≤ x k := fun k hk => by
    obtain ⟨h1, h2⟩ := hmem k hk
    have := good_descent h2
    rwa [← seq_iterate hx, h1] at this
  have hxt : ∀ k ∈ A, 0 < x t := fun k hk => by
    obtain ⟨h1, h2⟩ := hmem k hk
    have := iterate_pos (good_pos h2) (Nat.log 2 (x k))
    rwa [← seq_iterate hx, h1] at this
  rcases A.eq_empty_or_nonempty with he | ⟨k0, hk0⟩
  · rw [he, Finset.sum_empty]; positivity
  have hxt0 : (0:ℝ) < x t := by exact_mod_cast hxt k0 hk0
  have hc : (0:ℝ) < 2 ^ s * (x t : ℝ) / 2 := by positivity
  have key := sum_inv_le_of_doubling (fun k => (x k : ℝ)) A
    (fun k hk => by exact_mod_cast good_pos (hmem k hk).2)
    (fun k' hk' k hk hlt => by
      have := ancestors_double hx (hmem k' hk').1 (hmem k hk).1 (good_pos (hmem k' hk').2) hlt
      exact_mod_cast this)
    (2 ^ s * (x t : ℝ) / 2) hc
    (fun k hk => by
      have := hdesc k hk
      have h' : (2:ℝ) ^ s * (x t : ℝ) ≤ (x k : ℝ) := by exact_mod_cast this
      linarith)
  calc ∑ k ∈ A, 1 / (x k : ℝ) ≤ 1 / (2 ^ s * (x t : ℝ) / 2) := key
    _ = 2 / (2 ^ s * (x t : ℝ)) := by rw [one_div_div]

/-! ## Theorem H (abstract-β form) -/

theorem sum_half_pow (K : ℕ) :
    ∑ k ∈ Finset.range K, ((1:ℝ) / 2) ^ (K - k) = 1 - (1 / 2) ^ K := by
  induction K with
  | zero => simp
  | succ K ih =>
    rw [Finset.sum_range_succ']
    simp only [Nat.add_sub_add_right, Nat.sub_zero]
    rw [ih, pow_succ]; ring

/-- **Theorem H (abstract-β form).** Let `x` be a `T`-sequence whose first `K` terms are
pairwise distinct, `s ≥ 2`, and let `β` bound the reciprocal sum of every finite set of
(distinct) positive bad integers. Then `Σ_{k<K} 1/x_k ≤ (β + 1)/(1 - 2^(1-s))`. -/
theorem theoremH (s : ℕ) (hs : 2 ≤ s) (β : ℝ)
    (hβ : ∀ S : Finset ℕ, (∀ n ∈ S, 0 < n ∧ ¬ Good s n) → ∑ n ∈ S, (1 / (n : ℝ)) ≤ β)
    (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) :
    ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) ≤ (β + 1) / (1 - 2 / 2 ^ s) := by
  set W := ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) with hW
  -- bad part
  have hbad : ∑ k ∈ (Finset.range K).filter (fun k => ¬ Good s (x k)), (1 / (x k : ℝ)) ≤ β := by
    set B := (Finset.range K).filter (fun k => ¬ Good s (x k)) with hB
    have hinjB : Set.InjOn x (B : Set ℕ) := by
      intro i hi j hj hij
      have hi' := Finset.mem_range.mp (Finset.mem_filter.mp hi).1
      have hj' := Finset.mem_range.mp (Finset.mem_filter.mp hj).1
      exact hinj i hi' j hj' hij
    have h1 : ∑ n ∈ B.image x, (1 / (n : ℝ)) = ∑ k ∈ B, (1 / (x k : ℝ)) :=
      Finset.sum_image hinjB
    have h2 : ∑ n ∈ (B.image x).erase 0, (1 / (n : ℝ)) = ∑ n ∈ B.image x, (1 / (n : ℝ)) :=
      Finset.sum_erase _ (by simp)
    rw [← h1, ← h2]
    apply hβ
    intro n hn
    obtain ⟨hn0, hn⟩ := Finset.mem_erase.mp hn
    obtain ⟨k, hk, rfl⟩ := Finset.mem_image.mp hn
    exact ⟨Nat.pos_of_ne_zero hn0, (Finset.mem_filter.mp hk).2⟩
  -- overhang part
  have hover : ∑ k ∈ ((Finset.range K).filter (fun k => Good s (x k))).filter
      (fun k => ¬ k + Nat.log 2 (x k) < K), (1 / (x k : ℝ)) ≤ 1 := by
    calc _ ≤ ∑ k ∈ ((Finset.range K).filter (fun k => Good s (x k))).filter
          (fun k => ¬ k + Nat.log 2 (x k) < K), ((1:ℝ) / 2) ^ (K - k) := by
          apply Finset.sum_le_sum
          intro k hk
          obtain ⟨hk1, hk2⟩ := Finset.mem_filter.mp hk
          obtain ⟨hk3, hk4⟩ := Finset.mem_filter.mp hk1
          have hp := good_pos hk4
          have h1 : 2 ^ (K - k) ≤ 2 ^ Nat.log 2 (x k) :=
            Nat.pow_le_pow_right (by norm_num) (by omega)
          have h2 : 2 ^ (K - k) ≤ x k := h1.trans (Nat.pow_log_le_self 2 hp.ne')
          have h3 : ((2:ℝ)) ^ (K - k) ≤ (x k : ℝ) := by exact_mod_cast h2
          rw [div_pow, one_pow]
          exact one_div_le_one_div_of_le (by positivity) h3
      _ ≤ ∑ k ∈ Finset.range K, ((1:ℝ) / 2) ^ (K - k) := by
          apply Finset.sum_le_sum_of_subset_of_nonneg
          · exact (Finset.filter_subset _ _).trans (Finset.filter_subset _ _)
          · intro k _ _; positivity
      _ ≤ 1 := by
          rw [sum_half_pow]
          have : (0:ℝ) ≤ (1 / 2) ^ K := by positivity
          linarith
  -- main part
  have hmain : ∑ k ∈ ((Finset.range K).filter (fun k => Good s (x k))).filter
      (fun k => k + Nat.log 2 (x k) < K), (1 / (x k : ℝ)) ≤ 2 / 2 ^ s * W := by
    set M := ((Finset.range K).filter (fun k => Good s (x k))).filter
      (fun k => k + Nat.log 2 (x k) < K) with hM
    have hfib := Finset.sum_fiberwise_of_maps_to (s := M) (t := Finset.range K)
      (g := fun k => k + Nat.log 2 (x k)) (f := fun k => 1 / (x k : ℝ))
      (fun k hk => Finset.mem_range.mpr (Finset.mem_filter.mp hk).2)
    rw [← hfib, hW, Finset.mul_sum]
    apply Finset.sum_le_sum
    intro t _
    calc _ ≤ ∑ k ∈ (Finset.range K).filter
            (fun k => k + Nat.log 2 (x k) = t ∧ Good s (x k)), (1 / (x k : ℝ)) := by
          apply Finset.sum_le_sum_of_subset_of_nonneg
          · intro k hk
            obtain ⟨hk1, hk2⟩ := Finset.mem_filter.mp hk
            obtain ⟨hk3, -⟩ := Finset.mem_filter.mp hk1
            obtain ⟨hk4, hk5⟩ := Finset.mem_filter.mp hk3
            exact Finset.mem_filter.mpr ⟨hk4, hk2, hk5⟩
          · intro k _ _; positivity
      _ ≤ 2 / (2 ^ s * (x t : ℝ)) := lemma3 s x hx K t
      _ = 2 / 2 ^ s * (1 / (x t : ℝ)) := by ring
  -- assemble
  have hsplit : W = ∑ k ∈ ((Finset.range K).filter (fun k => Good s (x k))).filter
        (fun k => k + Nat.log 2 (x k) < K), (1 / (x k : ℝ))
      + ∑ k ∈ ((Finset.range K).filter (fun k => Good s (x k))).filter
        (fun k => ¬ k + Nat.log 2 (x k) < K), (1 / (x k : ℝ))
      + ∑ k ∈ (Finset.range K).filter (fun k => ¬ Good s (x k)), (1 / (x k : ℝ)) := by
    rw [Finset.sum_filter_add_sum_filter_not, Finset.sum_filter_add_sum_filter_not]
  have hq : (2:ℝ) / 2 ^ s ≤ 1 / 2 := by
    have h4 : (2:ℝ) ^ 2 ≤ 2 ^ s := pow_le_pow_right₀ (by norm_num) hs
    rw [div_le_div_iff₀ (by positivity) (by norm_num)]
    linarith
  have hden : (0:ℝ) < 1 - 2 / 2 ^ s := by linarith
  rw [le_div_iff₀ hden]
  nlinarith [hbad, hover, hmain, hsplit]

end Harmonic
end CollatzFMF
