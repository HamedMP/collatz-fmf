import CollatzFMF.ConstCycle

/-!
# Odd-only refinement of the conditional residue split (`W_odd` of Theorem R)

Source: `notes/round6-nov2026/w2-delta/REPORT.md` section (b), Theorem R
(`W_odd ≤ β_odd(32) + ε + 2^(1-s) U`).

* `bcountOdd s L` : `Σ_a [BadA s (L+1) (a+1)] C(L,a)`, the number `bo_{L+1}` of bad vectors of
  length `L+1` whose first bit is `1`.
* `card_bad_odd_block_le` : `#{n ∈ [2^(L+1), 2^(L+2)) : n odd, ¬ Good s n} ≤ bcountOdd s L`.
* `exact_mass_odd_run` : bad odd integers in `[2^(M+1), 2^(M+1+f))` have reciprocal sum
  `≤ runOdd s f M (prow M) 0 / 2^(M+f)` (kernel-evaluable numerator).
* `bad_mass_odd_32` : bad odd integers `≥ 2^32` (`s = 3`): reciprocal sum `≤ 3.1486`.
* `residue_split_odd`, `residue_split_32_odd` : the conditional residue split with the
  odd-only sum: `SmallHyp 32 E 497` ⇒ ratio `≤ E · exp(16087/10000)`.

Everything in this file is complete (no `sorry`, no extra axioms, no `native_decide`).
-/

namespace CollatzFMF
namespace Const

open KL (T)
open Harmonic Sharp

/-! ## Counting bad odd integers of a level -/

theorem card_oc_affine_le (L a : ℕ) :
    ((Finset.Ico (2 ^ L) (2 ^ (L + 1))).filter (fun m => oddCount L (3 * m + 2) = a)).card
      ≤ L.choose a := by
  rw [← card_oddCount_block L a]
  have hN : 0 < 2 ^ L := by positivity
  apply Finset.card_le_card_of_injOn (fun m => 2 ^ L + (3 * m + 2) % 2 ^ L)
  · intro m hm
    rw [Finset.mem_coe] at hm ⊢
    obtain ⟨hm1, hm2⟩ := Finset.mem_filter.mp hm
    obtain ⟨h1, h2⟩ := Finset.mem_Ico.mp hm1
    have hlt := Nat.mod_lt (3 * m + 2) hN
    have hoc : oddCount L (2 ^ L + (3 * m + 2) % 2 ^ L) = a := by
      have h := oddCount_add L ((3 * m + 2) % 2 ^ L) 1
      rw [Nat.mul_one] at h
      rw [Nat.add_comm, h, oddCount_mod, hm2]
    refine Finset.mem_filter.mpr ⟨Finset.mem_Ico.mpr ⟨Nat.le_add_right _ _, ?_⟩, hoc⟩
    show 2 ^ L + (3 * m + 2) % 2 ^ L < 2 ^ (L + 1)
    rw [pow_succ]; omega
  · intro m hm m' hm' e
    rw [Finset.mem_coe] at hm hm'
    obtain ⟨h1, h2⟩ := Finset.mem_Ico.mp (Finset.mem_filter.mp hm).1
    obtain ⟨h1', h2'⟩ := Finset.mem_Ico.mp (Finset.mem_filter.mp hm').1
    have hmod : 3 * m + 2 ≡ 3 * m' + 2 [MOD 2 ^ L] := Nat.add_left_cancel e
    have h2m : 3 * m ≡ 3 * m' [MOD 2 ^ L] := Nat.ModEq.add_right_cancel' 2 hmod
    have hc : Nat.gcd (2 ^ L) 3 = 1 := Nat.Coprime.pow_left L (by norm_num)
    have h3 : m ≡ m' [MOD 2 ^ L] := Nat.ModEq.cancel_left_of_coprime hc h2m
    have h4 : m % 2 ^ L = m' % 2 ^ L := h3
    rw [pow_succ] at h2 h2'
    have d1 : m / 2 ^ L = 1 := Nat.div_eq_of_lt_le (by omega) (by omega)
    have d2 : m' / 2 ^ L = 1 := Nat.div_eq_of_lt_le (by omega) (by omega)
    have q1 := Nat.div_add_mod m (2 ^ L)
    have q2 := Nat.div_add_mod m' (2 ^ L)
    rw [d1] at q1
    rw [d2] at q2
    omega

/-- `bo_{L+1}`: the number of bad vectors of length `L+1` with first bit `1`. -/
def bcountOdd (s L : ℕ) : ℕ :=
  ∑ a ∈ Finset.range (L + 1), if BadA s (L + 1) (a + 1) then L.choose a else 0

/-- The bad odd integers of level `L+1` number at most `bo_{L+1}`. -/
theorem card_bad_odd_block_le (s L : ℕ) :
    ((Finset.Ico (2 ^ (L + 1)) (2 ^ (L + 1 + 1))).filter
        (fun n => n % 2 = 1 ∧ ¬ Good s n)).card ≤ bcountOdd s L := by
  have step1 : ((Finset.Ico (2 ^ (L + 1)) (2 ^ (L + 1 + 1))).filter
        (fun n => n % 2 = 1 ∧ ¬ Good s n)).card
      ≤ ((Finset.Ico (2 ^ L) (2 ^ (L + 1))).filter
        (fun m => BadA s (L + 1) (oddCount L (3 * m + 2) + 1))).card := by
    apply Finset.card_le_card_of_injOn (fun n => n / 2)
    · intro n hn
      rw [Finset.mem_coe] at hn ⊢
      obtain ⟨hn1, hodd, hbad⟩ := Finset.mem_filter.mp hn
      obtain ⟨h1, h2⟩ := Finset.mem_Ico.mp hn1
      have hb := (not_good_iff h1 h2).mp hbad
      have hT : T n = 3 * (n / 2) + 2 := by unfold T; split <;> omega
      have hoc : oddCount (L + 1) n = oddCount L (3 * (n / 2) + 2) + 1 := by
        rw [oddCount, hodd, hT, Nat.add_comm]
      rw [hoc] at hb
      rw [pow_succ] at h1
      rw [pow_succ 2 (L + 1)] at h2
      have g1 : 2 ^ L ≤ n / 2 := by omega
      have g2 : n / 2 < 2 ^ (L + 1) := by omega
      exact Finset.mem_filter.mpr ⟨Finset.mem_Ico.mpr ⟨g1, g2⟩, hb⟩
    · intro n hn n' hn' e
      rw [Finset.mem_coe] at hn hn'
      have o1 := (Finset.mem_filter.mp hn).2.1
      have o2 := (Finset.mem_filter.mp hn').2.1
      have e' : n / 2 = n' / 2 := e
      omega
  have step2 : ((Finset.Ico (2 ^ L) (2 ^ (L + 1))).filter
        (fun m => BadA s (L + 1) (oddCount L (3 * m + 2) + 1))).card ≤ bcountOdd s L := by
    rw [Finset.card_eq_sum_card_fiberwise (f := fun m => oddCount L (3 * m + 2))
      (t := Finset.range (L + 1))
      (fun m _ => Finset.mem_range.mpr (Nat.lt_succ_of_le (oddCount_le L _)))]
    unfold bcountOdd
    apply Finset.sum_le_sum
    intro a _
    by_cases hb : BadA s (L + 1) (a + 1)
    · rw [if_pos hb]
      refine le_trans (Finset.card_le_card ?_) (card_oc_affine_le L a)
      intro m hm
      obtain ⟨hm1, hm2⟩ := Finset.mem_filter.mp hm
      exact Finset.mem_filter.mpr ⟨(Finset.mem_filter.mp hm1).1, hm2⟩
    · rw [if_neg hb]
      apply le_of_eq
      rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
      intro m hm e
      have e' : oddCount L (3 * m + 2) = a := e
      have hh := (Finset.mem_filter.mp hm).2
      rw [e'] at hh
      exact hb hh
  exact step1.trans step2

/-- Guard (cross-checked by brute force in Python): level 3 is `8..15`; its odd integers
`9, 11, 13, 15` are all bad for `s = 3`, and `bo_3 = 4`. -/
example : bcountOdd 3 2 = 4 := by decide

/-- Bad odd integers of a single level `L+1`: reciprocal sum `≤ bo_{L+1} / 2^(L+1)`. -/
theorem block_mass_odd (s L : ℕ) (S : Finset ℕ)
    (hS : ∀ n ∈ S, 2 ^ (L + 1) ≤ n ∧ n < 2 ^ (L + 1 + 1) ∧ n % 2 = 1 ∧ ¬ Good s n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ (bcountOdd s L : ℝ) / 2 ^ (L + 1) := by
  have hsub : S ⊆ (Finset.Ico (2 ^ (L + 1)) (2 ^ (L + 1 + 1))).filter
      (fun n => n % 2 = 1 ∧ ¬ Good s n) := by
    intro n hn
    obtain ⟨a1, a2, a3, a4⟩ := hS n hn
    exact Finset.mem_filter.mpr ⟨Finset.mem_Ico.mpr ⟨a1, a2⟩, a3, a4⟩
  have hcard : S.card ≤ bcountOdd s L :=
    (Finset.card_le_card hsub).trans (card_bad_odd_block_le s L)
  calc ∑ n ∈ S, (1 / (n : ℝ)) ≤ ∑ _n ∈ S, (1 / (2 : ℝ) ^ (L + 1)) := by
        apply Finset.sum_le_sum
        intro n hn
        have h1 : ((2 : ℝ)) ^ (L + 1) ≤ (n : ℝ) := by exact_mod_cast (hS n hn).1
        exact one_div_le_one_div_of_le (by positivity) h1
    _ = (S.card : ℝ) * (1 / (2 : ℝ) ^ (L + 1)) := by rw [Finset.sum_const, nsmul_eq_mul]
    _ ≤ (bcountOdd s L : ℝ) * (1 / (2 : ℝ) ^ (L + 1)) := by
        apply mul_le_mul_of_nonneg_right _ (by positivity)
        exact_mod_cast hcard
    _ = (bcountOdd s L : ℝ) / 2 ^ (L + 1) := by ring

/-- Exact odd bad mass on the levels `M+1, …, M+f`. -/
theorem exact_mass_odd (s M : ℕ) : ∀ (f : ℕ) (S : Finset ℕ),
    (∀ n ∈ S, 2 ^ (M + 1) ≤ n ∧ n < 2 ^ (M + f + 1) ∧ n % 2 = 1 ∧ ¬ Good s n) →
    ∑ n ∈ S, (1 / (n : ℝ))
      ≤ ∑ i ∈ Finset.range f, (bcountOdd s (M + i) : ℝ) / 2 ^ (M + i + 1) := by
  intro f
  induction f with
  | zero =>
    intro S hS
    have : S = ∅ := by
      apply Finset.eq_empty_of_forall_notMem
      intro n hn
      obtain ⟨a1, a2, -⟩ := hS n hn
      rw [Nat.add_zero] at a2
      omega
    rw [this]; simp
  | succ f ih =>
    intro S hS
    rw [Finset.sum_range_succ,
      ← Finset.sum_filter_add_sum_filter_not S (fun n => n < 2 ^ (M + f + 1))]
    apply add_le_add
    · apply ih
      intro n hn
      obtain ⟨h1, h2⟩ := Finset.mem_filter.mp hn
      exact ⟨(hS n h1).1, h2, (hS n h1).2.2⟩
    · apply block_mass_odd
      intro n hn
      obtain ⟨h1, h2⟩ := Finset.mem_filter.mp hn
      exact ⟨not_lt.mp h2, (hS n h1).2.1, (hS n h1).2.2⟩

/-! ## Kernel-evaluable computation of the odd mass -/

theorem bsum_spec' (s L' : ℕ) (c : ℕ → ℕ) : ∀ k a b,
    bsum s L' a ((List.range' b k).map c)
      = ∑ i ∈ Finset.range k, if BadA s L' (a + i) then c (b + i) else 0 := by
  intro k
  induction k with
  | zero => intro a b; simp [bsum]
  | succ k ih =>
    intro a b
    rw [List.range'_succ, List.map_cons, bsum, ih (a + 1) (b + 1), Finset.sum_range_succ',
      Nat.add_zero, Nat.add_zero, Nat.add_comm]
    congr 1
    refine Finset.sum_congr rfl fun i _ => ?_
    rw [show a + 1 + i = a + (i + 1) by omega, show b + 1 + i = b + (i + 1) by omega]

theorem bsum_prow_odd (s L : ℕ) : bsum s (L + 1) 1 (prow L) = bcountOdd s L := by
  rw [prow_eq, bsum_spec']
  unfold bcountOdd
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Nat.zero_add, Nat.add_comm 1 i]

/-- `runOdd s f L (prow L) A = 2^f A + 2^(L+f) Σ_{i<f} bo_{L+i+1} / 2^(L+i+1)`. -/
def runOdd (s : ℕ) : ℕ → ℕ → List ℕ → ℕ → ℕ
  | 0, _, _, A => A
  | f + 1, L, r, A => runOdd s f (L + 1) (pnext 0 r) (2 * A + bsum s (L + 1) 1 r)

theorem runOdd_spec (s : ℕ) : ∀ f L A,
    (runOdd s f L (prow L) A : ℝ)
      = 2 ^ f * (A : ℝ)
        + 2 ^ (L + f) * ∑ i ∈ Finset.range f, (bcountOdd s (L + i) : ℝ) / 2 ^ (L + i + 1) := by
  intro f
  induction f with
  | zero => intro L A; simp [runOdd]
  | succ f ih =>
    intro L A
    have e : runOdd s (f + 1) L (prow L) A
        = runOdd s f (L + 1) (prow (L + 1)) (2 * A + bsum s (L + 1) 1 (prow L)) := rfl
    rw [e, ih, bsum_prow_odd, Finset.sum_range_succ']
    have hidx : ∀ i, L + 1 + i = L + (i + 1) := fun i => by omega
    simp only [hidx, Nat.add_zero]
    push_cast
    have h2 : (2 : ℝ) ^ (L + (f + 1)) = 2 ^ (L + 1) * 2 ^ f := by
      rw [← pow_add]; congr 1; omega
    have h3 : (2 : ℝ) ^ (L + 1) ≠ 0 := by positivity
    rw [h2]
    have h4 : (2 : ℝ) ^ (L + 1) * 2 ^ f * ((bcountOdd s L : ℝ) / 2 ^ (L + 1))
        = 2 ^ f * bcountOdd s L := by
      field_simp
    generalize (∑ x ∈ Finset.range f, (bcountOdd s (L + (x + 1)) : ℝ) / 2 ^ (L + (x + 1) + 1))
      = Sg
    rw [mul_add (2 ^ (L + 1) * 2 ^ f : ℝ), h4]
    ring

/-- Bad odd integers in `[2^(M+1), 2^(M+f+1))` have reciprocal sum
`≤ runOdd s f M (prow M) 0 / 2^(M+f)`. -/
theorem exact_mass_odd_run (s M f : ℕ) (S : Finset ℕ)
    (hS : ∀ n ∈ S, 2 ^ (M + 1) ≤ n ∧ n < 2 ^ (M + f + 1) ∧ n % 2 = 1 ∧ ¬ Good s n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ (runOdd s f M (prow M) 0 : ℝ) / 2 ^ (M + f) := by
  refine (exact_mass_odd s M f S hS).trans (le_of_eq ?_)
  rw [runOdd_spec]
  have h3 : (2 : ℝ) ^ (M + f) ≠ 0 := by positivity
  push_cast
  field_simp
  ring

/-- Kernel evaluation: `Σ_{32 ≤ L < 300} bo_L / 2^L = 3.14359… ≤ 3.144` (`s = 3`). -/
theorem runOdd32 : runOdd 3 268 31 (prow 31) 0 * 1000 ≤ 3144 * 2 ^ (31 + 268) := by
  decide +kernel

/-- Guard: the bound is tight to the stated digit. -/
theorem runOdd32_lower : 3143 * 2 ^ (31 + 268) ≤ runOdd 3 268 31 (prow 31) 0 * 1000 := by
  decide +kernel

/-- Bad odd integers `≥ 2^32` (`s = 3`): reciprocal sum `≤ 3.1486`. -/
theorem bad_mass_odd_32 (S : Finset ℕ)
    (hS : ∀ n ∈ S, 2 ^ 32 ≤ n ∧ n % 2 = 1 ∧ ¬ Good 3 n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ 31486 / 10000 := by
  rw [← Finset.sum_filter_add_sum_filter_not S (fun n => n < 2 ^ 300)]
  have h1 : ∑ n ∈ S.filter (fun n => n < 2 ^ 300), (1 / (n : ℝ))
      ≤ (runOdd 3 268 31 (prow 31) 0 : ℝ) / 2 ^ (31 + 268) := by
    apply exact_mass_odd_run
    intro n hn
    obtain ⟨a1, a2⟩ := Finset.mem_filter.mp hn
    exact ⟨(hS n a1).1, a2, (hS n a1).2⟩
  have h2 : ∑ n ∈ S.filter (fun n => ¬ n < 2 ^ 300), (1 / (n : ℝ))
      ≤ 2 ^ (1 + 1) * 30 * (29 / 30 : ℝ) ^ 300 := by
    apply bad_mass_tail_odd 1 300
    intro n hn
    obtain ⟨a1, a2⟩ := Finset.mem_filter.mp hn
    exact ⟨not_lt.mp a2, (hS n a1).2.2⟩
  have hr : (runOdd 3 268 31 (prow 31) 0 : ℝ) / 2 ^ (31 + 268) ≤ 3144 / 1000 := by
    rw [div_le_div_iff₀ (by positivity) (by norm_num)]
    exact_mod_cast runOdd32
  exact (add_le_add (h1.trans hr) (h2.trans tail300)).trans (by norm_num)

/-! ## The conditional split with the odd-only sum -/

/-- **Theorem R, conditional split form with the odd-only refinement.** Assume `SmallHyp M E P`,
a bad-mass bound `β` for integers `≥ 2^M` and a bad-mass bound `βo` for ODD integers `≥ 2^M`.
Then on every pairwise distinct stretch, for all `k ≤ K`:
`x_0 3^(a_k) ≤ x_k 2^k ≤ E · exp(W_odd/3) · x_0 3^(a_k)` with
`W_odd = βo + ε + 2^(1-s) U`, `U = (β + ε)/(1 - 2^(1-s))`, `ε = (M+1)/2^M + 2P/2^M`. -/
theorem residue_split_odd (M : ℕ) (E : ℝ) (P : ℕ) (h : SmallHyp M E P)
    (s : ℕ) (hs : 2 ≤ s) (β βo : ℝ)
    (hβ : ∀ S : Finset ℕ, (∀ n ∈ S, 2 ^ M ≤ n ∧ ¬ Good s n) → ∑ n ∈ S, (1 / (n : ℝ)) ≤ β)
    (hβo : ∀ S : Finset ℕ, (∀ n ∈ S, 2 ^ M ≤ n ∧ n % 2 = 1 ∧ ¬ Good s n) →
      ∑ n ∈ S, (1 / (n : ℝ)) ≤ βo)
    (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (k : ℕ) (hk : k ≤ K) :
    (x 0 : ℝ) * 3 ^ oddCount k (x 0) ≤ (x k : ℝ) * 2 ^ k ∧
      (x k : ℝ) * 2 ^ k
        ≤ E * Real.exp ((βo + (M + 1) / 2 ^ M + (P : ℝ) * (2 / 2 ^ M)
              + 2 / 2 ^ s * ((β + (M + 1) / 2 ^ M + (P : ℝ) * (2 / 2 ^ M)) / (1 - 2 / 2 ^ s))) / 3)
          * ((x 0 : ℝ) * 3 ^ oddCount k (x 0)) := by
  set Wo : ℝ := βo + (M + 1) / 2 ^ M + (P : ℝ) * (2 / 2 ^ M)
    + 2 / 2 ^ s * ((β + (M + 1) / 2 ^ M + (P : ℝ) * (2 / 2 ^ M)) / (1 - 2 / 2 ^ s)) with hWo
  have hinjk : ∀ i < k, ∀ j < k, x i = x j → i = j := fun i hi j hj e =>
    hinj i (by omega) j (by omega) e
  have hid : (x k : ℝ) * 2 ^ k
      = (x 0 : ℝ) * 3 ^ oddCount k (x 0) * ∏ i ∈ Finset.range k, oddFactor (x i) := by
    rw [seq_eq_iterate hx k, product_identity_iterate]
    congr 1
    refine Finset.prod_congr rfl fun i _ => ?_
    rw [← seq_eq_iterate hx i]
  have h0 : (0 : ℝ) ≤ (x 0 : ℝ) * 3 ^ oddCount k (x 0) := by positivity
  have h1 := one_le_prod_oddFactor x k
  obtain ⟨hsmall, hcard⟩ := small_part M E P h x hx k hinjk
  have hq : (2 : ℝ) / 2 ^ s ≤ 1 / 2 := by
    have h4 : (2 : ℝ) ^ 2 ≤ 2 ^ s := pow_le_pow_right₀ (by norm_num) hs
    rw [div_le_div_iff₀ (by positivity) (by norm_num)]
    linarith
  have hq0 : (0 : ℝ) ≤ 2 / 2 ^ s := by positivity
  have hden : (0 : ℝ) < 1 - 2 / 2 ^ s := by linarith
  have hc : (((Finset.range k).filter (fun i => x i < 2 ^ M)).card : ℝ) * (2 / 2 ^ M)
      ≤ (P : ℝ) * (2 / 2 ^ M) := by
    apply mul_le_mul_of_nonneg_right _ (by positivity)
    exact_mod_cast hcard
  have hU : ∑ i ∈ (Finset.range k).filter (fun i => 2 ^ M ≤ x i), (1 / (x i : ℝ))
      ≤ (β + (M + 1) / 2 ^ M + (P : ℝ) * (2 / 2 ^ M)) / (1 - 2 / 2 ^ s) := by
    refine (theoremH_split s hs M β hβ x hx k hinjk).trans ?_
    apply div_le_div_of_nonneg_right _ hden.le
    linarith
  have hWodd : ∑ i ∈ (Finset.range k).filter (fun i => 2 ^ M ≤ x i ∧ x i % 2 = 1),
      (1 / (x i : ℝ)) ≤ Wo := by
    have hstep := split_step s M (fun n => n % 2 = 1) βo hβo x hx k hinjk
    have hmul := mul_le_mul_of_nonneg_left hU hq0
    rw [hWo]
    linarith
  have hfe : (Finset.range k).filter (fun i => ¬ x i < 2 ^ M)
      = (Finset.range k).filter (fun i => 2 ^ M ≤ x i) :=
    Finset.filter_congr fun i _ => not_lt
  have hff : ((Finset.range k).filter (fun i => 2 ^ M ≤ x i)).filter (fun i => x i % 2 = 1)
      = (Finset.range k).filter (fun i => 2 ^ M ≤ x i ∧ x i % 2 = 1) := Finset.filter_filter _ _ _
  have hbigprod : ∏ i ∈ (Finset.range k).filter (fun i => 2 ^ M ≤ x i), oddFactor (x i)
      ≤ Real.exp (Wo / 3) := by
    rw [← Finset.prod_filter_mul_prod_filter_not _ (fun i => x i % 2 = 1), hff]
    have heven : ∏ i ∈ ((Finset.range k).filter (fun i => 2 ^ M ≤ x i)).filter
        (fun i => ¬ x i % 2 = 1), oddFactor (x i) = 1 :=
      Finset.prod_eq_one fun i hi => by
        unfold oddFactor
        rw [if_neg (Finset.mem_filter.mp hi).2]
    rw [heven, mul_one]
    exact (prod_oddFactor_filter_le x _).trans (Real.exp_le_exp.mpr (by linarith))
  have hE : (0 : ℝ) ≤ E := le_trans
    (Finset.prod_nonneg fun i _ => le_trans zero_le_one (one_le_oddFactor _)) hsmall
  have hprod : ∏ i ∈ Finset.range k, oddFactor (x i) ≤ E * Real.exp (Wo / 3) := by
    rw [← Finset.prod_filter_mul_prod_filter_not (Finset.range k) (fun i => x i < 2 ^ M), hfe]
    exact mul_le_mul hsmall hbigprod
      (Finset.prod_nonneg fun i _ => le_trans zero_le_one (one_le_oddFactor _)) hE
  rw [hid]
  constructor
  · nlinarith
  · calc (x 0 : ℝ) * 3 ^ oddCount k (x 0) * ∏ i ∈ Finset.range k, oddFactor (x i)
        ≤ (x 0 : ℝ) * 3 ^ oddCount k (x 0) * (E * Real.exp (Wo / 3)) :=
          mul_le_mul_of_nonneg_left hprod h0
      _ = _ := by ring

/-- **Theorem R at `B = 2^32`, conditional on exactly one computational fact, odd-refined.**
`SmallHyp 32 E 497` ⇒ on every distinct stretch `x_k 2^k ≤ E · exp(16087/10000) · x_0 3^(a_k)`.
`exp(1.6087) ≈ 4.9963`. With the source's `E = exp(0.2256541127)` (stretch not containing `1`)
this is `≤ 6.27` (refereed `Res ≤ 5.72`); with `E = (4/3)·exp(0.2256541127)` it is `≤ 8.35`
(refereed `7.62`). The remaining gap is the logarithmic block refinement only. -/
theorem residue_split_32_odd (E : ℝ) (h : SmallHyp 32 E 497)
    (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (k : ℕ) (hk : k ≤ K) :
    (x 0 : ℝ) * 3 ^ oddCount k (x 0) ≤ (x k : ℝ) * 2 ^ k ∧
      (x k : ℝ) * 2 ^ k
        ≤ E * Real.exp (16087 / 10000) * ((x 0 : ℝ) * 3 ^ oddCount k (x 0)) := by
  obtain ⟨h1, h2⟩ := residue_split_odd 32 E 497 h 3 (by norm_num) _ _ bad_mass_32
    bad_mass_odd_32 x hx K hinj k hk
  refine ⟨h1, h2.trans ?_⟩
  have hE : (0 : ℝ) ≤ E := by
    obtain ⟨hh, -⟩ := h 0 0 (by norm_num) (by intro i hi; omega)
    have : (1 : ℝ) ≤ E := by simpa using hh
    linarith
  have h0 : (0 : ℝ) ≤ (x 0 : ℝ) * 3 ^ oddCount k (x 0) := by positivity
  apply mul_le_mul_of_nonneg_right _ h0
  apply mul_le_mul_of_nonneg_left _ hE
  apply Real.exp_le_exp.mpr
  norm_num

end Const
end CollatzFMF
