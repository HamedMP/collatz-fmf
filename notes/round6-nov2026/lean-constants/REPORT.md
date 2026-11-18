<!-- Saved by the coordinator from the lean-constants agent's final message (the agent's own write was refused). -->
# lean-constants — REPORT (full text; file write was refused)

## Modules to import

```
import CollatzFMF.ConstCount    -- count identity, b_L, Pascal-row evaluator
import CollatzFMF.ConstH        -- split Theorem H, constants 31.34 / 6.71 / 1.38
import CollatzFMF.ConstCycle    -- cycle length above 2^71, residue bounds, SmallHyp, split
import CollatzFMF.ConstOdd      -- odd-only refinement of the split
import CollatzFMF.ConstRefine   -- eight-step block bound, constant 27.93
import CollatzFMF.ConstAxioms   -- audit (imports ConstOdd and ConstRefine)
```

Import chain: `ResidueProduct → ConstCount → ConstH → {ConstCycle → ConstOdd, ConstRefine}`. `ConstAxioms` alone pulls in everything.

## Method

1. **Count identity** (`card_oddCount_block`): the number of n in [2^L, 2^(L+1)) with `oddCount L n = a` is C(L,a). It comes from the existing `sum_pow_oddCount_block` by comparing polynomial coefficients.
2. **Exact bad counts**: `BadA s L a := ¬ (3^a (2^a+1) 2^s ≤ 2^(L+a))` and `bcount s L = Σ_a [BadA s L a]·C(L,a)`. `card_bad_block` proves this is exactly the number of bad integers of level L. No monotonicity in a is needed.
3. **Kernel evaluation**: `run s f M (prow M) 0` computes 2^(M+f)·Σ_{L=M}^{M+f−1} b_L/2^L from Pascal rows held as lists. `run_spec` proves it correct against `bcount`. The kernel then decides inequalities between 300-bit naturals.
4. **Tail**: levels ≥ 300 reuse the Chernoff weight of `HarmonicSharp` (ratio 29/30) started at level 300, giving mass ≤ 120·(29/30)^300 ≤ 0.0046.
5. **Level-restricted Theorem H** (`split_step`, `theoremH_split`, `theoremH_ge`): the proof of Theorem H for the terms ≥ 2^M of a distinct stretch. Overhang is ≤ (M+1)/2^M and each term below 2^M costs 2/2^M as a target. `split_step` takes a class `Q` of integers, so `Q = odd` gives the source's W_odd.
6. **Eight-step block bound** (`chunk_block`): b distinct integers of [8c, 16c) have reciprocal sum ≤ `chunkNum c b / (360360 c)`. This stands in for the source's `2^(−L) + ln(1 + b_L/2^L)`.

## Lean statements (verbatim)

### ConstCount

```lean
theorem card_oddCount_block (L a : ℕ) :
    ((Finset.Ico (2 ^ L) (2 ^ (L + 1))).filter (fun n => oddCount L n = a)).card
      = L.choose a

def BadA (s L a : ℕ) : Prop := ¬ (3 ^ a * (2 ^ a + 1) * 2 ^ s ≤ 2 ^ (L + a))
def bcount (s L : ℕ) : ℕ := ∑ a ∈ Finset.range (L + 1), if BadA s L a then L.choose a else 0

theorem card_bad_block (s L : ℕ) :
    ((Finset.Ico (2 ^ L) (2 ^ (L + 1))).filter (fun n => ¬ Good s n)).card = bcount s L

theorem exact_mass_run (s M f : ℕ) (S : Finset ℕ)
    (hS : ∀ n ∈ S, 2 ^ M ≤ n ∧ n < 2 ^ (M + f) ∧ ¬ Good s n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ (run s f M (prow M) 0 : ℝ) / 2 ^ (M + f)
```

### ConstH

```lean
theorem split_step (s M : ℕ) (Q : ℕ → Prop) [DecidablePred Q] (β : ℝ)
    (hβ : ∀ S : Finset ℕ, (∀ n ∈ S, 2 ^ M ≤ n ∧ Q n ∧ ¬ Good s n) →
      ∑ n ∈ S, (1 / (n : ℝ)) ≤ β)
    (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) :
    ∑ k ∈ (Finset.range K).filter (fun k => 2 ^ M ≤ x k ∧ Q (x k)), (1 / (x k : ℝ))
      ≤ β + (M + 1) / 2 ^ M
          + (((Finset.range K).filter (fun k => x k < 2 ^ M)).card : ℝ) * (2 / 2 ^ M)
          + 2 / 2 ^ s * ∑ k ∈ (Finset.range K).filter (fun k => 2 ^ M ≤ x k), (1 / (x k : ℝ))

theorem theoremH_ge (s : ℕ) (hs : 2 ≤ s) (M : ℕ) (β : ℝ)
    (hβ : ∀ S : Finset ℕ, (∀ n ∈ S, 2 ^ M ≤ n ∧ ¬ Good s n) → ∑ n ∈ S, (1 / (n : ℝ)) ≤ β)
    (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (hbig : ∀ k < K, 2 ^ M ≤ x k) :
    ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) ≤ (β + (M + 1) / 2 ^ M) / (1 - 2 / 2 ^ s)

theorem run0 : run 3 300 0 (prow 0) 0 * 1000 ≤ 22500 * 2 ^ (0 + 300) := by decide +kernel
theorem run32 : run 3 268 32 (prow 32) 0 * 1000 ≤ 5027 * 2 ^ (32 + 268) := by decide +kernel
theorem run71 : run 3 229 71 (prow 71) 0 * 1000 ≤ 1030 * 2 ^ (71 + 229) := by decide +kernel

theorem bad_mass_71 (S : Finset ℕ) (hS : ∀ n ∈ S, 2 ^ 71 ≤ n ∧ ¬ Good 3 n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ 10346 / 10000

theorem theoremH_3134 (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k))
    (K : ℕ) (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) :
    ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) ≤ 1567 / 50

theorem harmonic_ge_71 (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k))
    (K : ℕ) (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (hbig : ∀ k < K, 2 ^ 71 ≤ x k) :
    ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) ≤ 69 / 50
```

`harmonic_ge_32` is the same with `2 ^ 32` and bound `671 / 100`. `theoremH_split` is the abstract-β form with the count of terms below 2^M.

### ConstCycle

```lean
theorem cycle_length_above_71 (n p : ℕ) (hp1 : 1 ≤ p) (hp : T^[p] n = n)
    (hmin : ∀ q, 0 < q → q < p → T^[q] n ≠ n) (hbig : ∀ i < p, 2 ^ 71 ≤ T^[i] n) :
    3 ^ oddCount p n < 2 ^ p ∧ 2 ^ p < 2 * 3 ^ oddCount p n ∧
      2 ^ (p - 1) < 3 ^ oddCount p n ∧
      (∀ q, 3 ^ oddCount p n < 2 ^ q → p ≤ q) ∧
      p = Nat.clog 2 (3 ^ oddCount p n + 1)

theorem cycle_ratio_above_71 (n p : ℕ) (hp1 : 1 ≤ p) (hp : T^[p] n = n)
    (hmin : ∀ q, 0 < q → q < p → T^[q] n ≠ n) (hbig : ∀ i < p, 2 ^ 71 ≤ T^[i] n) :
    (2 : ℝ) ^ p ≤ Real.exp (23 / 50) * 3 ^ oddCount p n

theorem residue_bound_1045 (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (k : ℕ) (hk : k ≤ K) :
    (x 0 : ℝ) * 3 ^ oddCount k (x 0) ≤ (x k : ℝ) * 2 ^ k ∧
      (x k : ℝ) * 2 ^ k ≤ Real.exp (1567 / 150) * ((x 0 : ℝ) * 3 ^ oddCount k (x 0))

def SmallHyp (M : ℕ) (E : ℝ) (P : ℕ) : Prop :=
  ∀ n K : ℕ, n < 2 ^ M → (∀ i < K, ∀ j < K, T^[i] n = T^[j] n → i = j) →
    (∏ i ∈ (Finset.range K).filter (fun i => T^[i] n < 2 ^ M), oddFactor (T^[i] n)) ≤ E ∧
    ((Finset.range K).filter (fun i => T^[i] n < 2 ^ M)).card ≤ P

theorem residue_split (M : ℕ) (E : ℝ) (P : ℕ) (h : SmallHyp M E P)
    (s : ℕ) (hs : 2 ≤ s) (β : ℝ)
    (hβ : ∀ S : Finset ℕ, (∀ n ∈ S, 2 ^ M ≤ n ∧ ¬ Good s n) → ∑ n ∈ S, (1 / (n : ℝ)) ≤ β)
    (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (k : ℕ) (hk : k ≤ K) :
    (x 0 : ℝ) * 3 ^ oddCount k (x 0) ≤ (x k : ℝ) * 2 ^ k ∧
      (x k : ℝ) * 2 ^ k
        ≤ E * Real.exp ((β + (M + 1) / 2 ^ M + (P : ℝ) * (2 / 2 ^ M)) / (1 - 2 / 2 ^ s) / 3)
          * ((x 0 : ℝ) * 3 ^ oddCount k (x 0))
```

`oddFactor m` is `1 + 1/(3m)` for odd m and 1 otherwise (`ResidueProduct.lean`). Also in this file: `residue_split_32` (non-odd instance, constant `E * Real.exp (5591 / 2500)`, about E·9.36), `cycle_pow_bounds_1045`, and `residue_above_71` (ratio ≤ exp(23/50) when all terms ≥ 2^71).

### ConstOdd

```lean
def bcountOdd (s L : ℕ) : ℕ :=
  ∑ a ∈ Finset.range (L + 1), if BadA s (L + 1) (a + 1) then L.choose a else 0

theorem card_bad_odd_block_le (s L : ℕ) :
    ((Finset.Ico (2 ^ (L + 1)) (2 ^ (L + 1 + 1))).filter
        (fun n => n % 2 = 1 ∧ ¬ Good s n)).card ≤ bcountOdd s L

theorem runOdd32 : runOdd 3 268 31 (prow 31) 0 * 1000 ≤ 3144 * 2 ^ (31 + 268) := by
  decide +kernel

theorem bad_mass_odd_32 (S : Finset ℕ)
    (hS : ∀ n ∈ S, 2 ^ 32 ≤ n ∧ n % 2 = 1 ∧ ¬ Good 3 n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ 31486 / 10000

theorem residue_split_32_odd (E : ℝ) (h : SmallHyp 32 E 497)
    (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (k : ℕ) (hk : k ≤ K) :
    (x 0 : ℝ) * 3 ^ oddCount k (x 0) ≤ (x k : ℝ) * 2 ^ k ∧
      (x k : ℝ) * 2 ^ k
        ≤ E * Real.exp (16087 / 10000) * ((x 0 : ℝ) * 3 ^ oddCount k (x 0))
```

`residue_split_odd` is the general form (parameters M, E, P, s, β, βo).

### ConstRefine

```lean
def chunkNum (c b : ℕ) : ℕ :=
  24024 * b + 5005 * min b c + 4004 * min b (2 * c) + 3276 * min b (3 * c)
    + 2730 * min b (4 * c) + 2310 * min b (5 * c) + 1980 * min b (6 * c) + 1716 * min b (7 * c)

theorem chunk_block (c b : ℕ) (hc : 0 < c) (S : Finset ℕ) (hS : ∀ n ∈ S, 8 * c ≤ n ∧ n < 16 * c)
    (hb : S.card ≤ b) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ (chunkNum c b : ℝ) / (360360 * c)

theorem runC0 :
    runC 3 297 0 (prow 3) 0 * 2 * 10000 ≤ 169426 * (360360 * 2 ^ (0 + 297)) := by
  decide +kernel

theorem bad_mass_0_refined (S : Finset ℕ) (hS : ∀ n ∈ S, 2 ^ 0 ≤ n ∧ ¬ Good 3 n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ 199472 / 10000

theorem theoremH_2793 (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k))
    (K : ℕ) (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) :
    ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) ≤ 2793 / 100

theorem residue_bound_931 (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (k : ℕ) (hk : k ≤ K) :
    (x 0 : ℝ) * 3 ^ oddCount k (x 0) ≤ (x k : ℝ) * 2 ^ k ∧
      (x k : ℝ) * 2 ^ k ≤ Real.exp (931 / 100) * ((x 0 : ℝ) * 3 ^ oddCount k (x 0))
```

## Constants: certified vs refereed

All with s = 3. "Exact" is the Python value in exact rationals. Refereed entries marked "inferred" are my back-calculation from the source's published numbers, not figures the source states.

| quantity | exact value | certified bound | refereed |
|---|---|---|---|
| bad mass, levels 0–299, plain | 22.499461 | 22.500 | — |
| bad mass, all levels, plain | — | 22.5046 | — |
| bad mass, all levels, eight-step | 19.942600 + tail | 19.9472 | 19.3719 |
| Theorem H constant | — | **27.93** (plain 31.34) | 27.163 |
| bad mass ≥ 2^32 | 5.026878 | 5.0316 | about 4.78 (inferred) |
| harmonic sum, all terms ≥ 2^32 | — | 6.71 | 6.3754 |
| odd bad mass ≥ 2^32 | 3.143590 | 3.1486 | about 2.96 (inferred) |
| W_odd at 2^32 | — | 4.8261 | 4.5507 |
| bad mass ≥ 2^71 | 1.029811 | 1.0346 | about 1.02 (inferred) |
| harmonic sum, all terms ≥ 2^71 | — | **1.38** | 1.3594 |
| cycle ratio 2^p/3^a above 2^71 | — | exp(0.46) = 1.5841 | 1.3860 |
| unconditional residue ratio | — | exp(9.31) ≈ 11048 | none without computation |
| Res given `SmallHyp 32 E 497` | — | E·4.9964 | E·4.558 |

## What remains

1. **27.93 vs 27.163.** The gap is the step function against the logarithm at low levels. Sixteen steps give about 27.83 (Python estimate). Reaching 27.2 needs a formal `Σ_{i<b} 1/(N+i) ≤ 1/N + ln(1 + b/N)` plus rational enclosures of about 300 logarithms. Not attempted.
2. **Cycle ratio 1.584 vs 1.386.** `cycle_ratio_above_71` divides the sum over all terms by 3; the source uses odd terms only. The odd refinement exists for M = 32 but was not instantiated at 71, because the cycle-length theorem only needs `< 2`. Doing so should give roughly 1.39–1.40 (estimate, not computed).
3. **Split constant 4.9964 vs 4.558.** Same logarithmic refinement, for both the full and the odd bad mass above 2^32. The eight-step bound would lower U from 6.71 to 6.63 (Python only); an odd `chunk_block` was not written.
4. **`SmallHyp 32 E 497` is unproved.** It should follow from run `s5` with E = (4/3)·exp(0.2256541127) and P = P_B + 2. I did not check that reading, in particular whether P_B = 495 counts the terms 1 and 2. The hypothesis asks for a product bound, while the source records a floating-point log-sum with a 10^−9 margin.
5. **Only s = 3.** The tail reuses `HarmonicSharp.weight`, which exists for odd s only. For this method s = 3 gave the best constants among s = 2..6 at M = 0, 32 and 71 (Python).
6. **Odd counts start at level 1.** `bcountOdd` does not cover level 0; `bad_mass_odd_32` does not need it.

## Guards

- `card_oddCount_block`: `example` on level 2 (odd counts 0, 1, 1, 2).
- Evaluator: `prow 5 = [1,5,10,10,5,1]`, `bsum 3 9 0 (prow 9) = 382`, `bsum 3 4 0 (prow 4) = 15`, `bcountOdd 3 2 = 4`, all matching brute force in Python.
- `run0_lower`, `run71_lower`, `runOdd32_lower`, `runC0_lower`: each kernel evaluation is tight to its last digit.
- `chunkNum 1 8 / 360360 = 1/8 + … + 1/15` and `chunkNum 1 1 / 360360 = 1/8`.
- `SmallHyp 1 (4/3) 1` is proved as an `example`, so the hypothesis is satisfiable in the smallest case.
- `theoremH_2793` and `residue_bound_931` are instantiated at n = 27; `harmonic_ge_71` on the stretch 2^72, 2^71.
- `cycle_length_above_71` cannot be instantiated (no such cycle is known). An `example` checks its conclusion and non-size hypotheses on 1 → 2 → 1.
- `crosscheck.py` recomputes every certified number in exact rationals and brute-forces both count identities for levels ≤ 13; it ends `ALL CHECKS PASSED`.

## Build

```
export PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=2
cd /home/matrix/home/projects/collatz/repo/lean && taskset -c 2-3 lake build CollatzFMF.ConstAxioms
```

ConstCount took about 3 min and ConstH about 2.5 min, mostly loading Mathlib; ConstCycle, ConstOdd and ConstRefine each took under a minute. No `maxRecDepth` or `maxHeartbeats` was raised, and Mathlib was never rebuilt.

Excerpt of the final build (all 45 audit lines: 9 kernel evaluations show `[propext]`, the other 36 `[propext, Classical.choice, Quot.sound]`):

```
info: CollatzFMF/ConstAxioms.lean:18:0: 'CollatzFMF.Const.run0' depends on axioms: [propext]
info: CollatzFMF/ConstAxioms.lean:20:0: 'CollatzFMF.Const.run71' depends on axioms: [propext]
info: CollatzFMF/ConstAxioms.lean:28:0: 'CollatzFMF.Const.harmonic_ge_71' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/ConstAxioms.lean:30:0: 'CollatzFMF.Const.cycle_length_above_71' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/ConstAxioms.lean:44:0: 'CollatzFMF.Const.residue_split_32_odd' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/ConstAxioms.lean:51:0: 'CollatzFMF.Const.theoremH_2793' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/ConstAxioms.lean:52:0: 'CollatzFMF.Const.residue_bound_931' depends on axioms: [propext, Classical.choice, Quot.sound]
Build completed successfully (18273 jobs).
```

Warnings only: two "exponent 300 exceeds the threshold 256" notices (the power is left unevaluated on purpose) and deprecation notices for `if_pos` / `if_neg`.

## Files

All new:
- `/home/matrix/home/projects/collatz/repo/lean/CollatzFMF/ConstCount.lean`
- `/home/matrix/home/projects/collatz/repo/lean/CollatzFMF/ConstH.lean`
- `/home/matrix/home/projects/collatz/repo/lean/CollatzFMF/ConstCycle.lean`
- `/home/matrix/home/projects/collatz/repo/lean/CollatzFMF/ConstOdd.lean`
- `/home/matrix/home/projects/collatz/repo/lean/CollatzFMF/ConstRefine.lean`
- `/home/matrix/home/projects/collatz/repo/lean/CollatzFMF/ConstAxioms.lean`
- `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/lean-constants/crosscheck.py`