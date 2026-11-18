<!-- Saved by the coordinator from the lean-gate-H agent's final message (the agent's own write was refused). -->
# lean-gate-H — REPORT (intended `notes/round6-nov2026/lean-gate-H/REPORT.md`)

## Files

All Lean files are new; no existing statement was edited. Paths are under `/home/matrix/home/projects/collatz/repo/`.

- `lean/CollatzFMF/Harmonic.lean` — Lemmas 1–3, Theorem H (abstract β), guards.
- `lean/CollatzFMF/HarmonicBeta.lean` — Terras periodicity, the Terras bijection in generating-function form, explicit bad mass, hypothesis-free Theorem H.
- `lean/CollatzFMF/HarmonicAxioms.lean` — the `#print axioms` audit.
- `lean/CollatzFMF.lean` — one added line: `import CollatzFMF.HarmonicAxioms`.
- `notes/round6-nov2026/lean-gate-H/crosscheck.py` and `build.log`.

The new files contain no `sorry`, `axiom`, `native_decide`, `unsafe` or `implemented_by` (grep). There is no unfinished file.

## Statements (verbatim)

Namespace `CollatzFMF.Harmonic`; `T` is `CollatzFMF.KL.T` from `KLSound.lean`. Every theorem below is COMPLETE with axioms `[propext, Classical.choice, Quot.sound]`, except `oddCount_add`, which uses only `[propext, Quot.sound]`.

```lean
def oddCount : ℕ → ℕ → ℕ
  | 0, _ => 0
  | L + 1, x => x % 2 + oddCount L (T x)

def Good (s x : ℕ) : Prop :=
  3 ^ oddCount (Nat.log 2 x) x * (2 ^ oddCount (Nat.log 2 x) x + 1) * 2 ^ s
    ≤ 2 ^ (Nat.log 2 x + oddCount (Nat.log 2 x) x)

-- guard: oddCount is the number of odd terms among the first L iterates
theorem oddCount_eq_card (L x : ℕ) :
    oddCount L x = ((Finset.range L).filter fun i => T^[i] x % 2 = 1).card

-- Lemma 1
theorem lemma1 (L x : ℕ) :
    ∃ r : ℕ, 2 ^ L * T^[L] x = 3 ^ oddCount L x * x + r ∧
      r * 2 ^ oddCount L x + 2 ^ L * 2 ^ oddCount L x ≤ 3 ^ oddCount L x * 2 ^ L

-- Lemma 2
theorem lemma2 (L s x : ℕ) (hx : 2 ^ L ≤ x)
    (hg : 3 ^ oddCount L x * (2 ^ oddCount L x + 1) * 2 ^ s ≤ 2 ^ (L + oddCount L x)) :
    2 ^ s * T^[L] x ≤ x

-- satisfiability guards
theorem good_16 : Good 3 16
theorem bad_27 : ¬ Good 3 27

-- Lemma 3
theorem ancestors_double {x : ℕ → ℕ} (hx : ∀ k, x (k + 1) = T (x k)) {k' k t : ℕ}
    (hk' : k' + Nat.log 2 (x k') = t) (hk : k + Nat.log 2 (x k) = t)
    (hpos' : 0 < x k') (hlt : k' < k) : 2 * x k ≤ x k'

theorem lemma3 (s : ℕ) (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K t : ℕ) :
    ∑ k ∈ (Finset.range K).filter (fun k => k + Nat.log 2 (x k) = t ∧ Good s (x k)),
        (1 / (x k : ℝ))
      ≤ 2 / (2 ^ s * (x t : ℝ))

-- Theorem H, abstract β
theorem theoremH (s : ℕ) (hs : 2 ≤ s) (β : ℝ)
    (hβ : ∀ S : Finset ℕ, (∀ n ∈ S, 0 < n ∧ ¬ Good s n) → ∑ n ∈ S, (1 / (n : ℝ)) ≤ β)
    (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) :
    ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) ≤ (β + 1) / (1 - 2 / 2 ^ s)

-- β discharged (HarmonicBeta.lean)
theorem oddCount_add (L x j : ℕ) : oddCount L (x + 2 ^ L * j) = oddCount L x

theorem sum_pow_oddCount_block (y : ℝ) (L : ℕ) :
    ∑ n ∈ Finset.Ico (2 ^ L) (2 ^ (L + 1)), y ^ oddCount L n = (1 + y) ^ L

theorem bad_mass (s : ℕ) (S : Finset ℕ) (hS : ∀ n ∈ S, 0 < n ∧ ¬ Good s n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ 56 * 2 ^ (s + 1)

theorem theoremH_explicit (s : ℕ) (hs : 2 ≤ s) (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k))
    (K : ℕ) (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) :
    ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) ≤ (56 * 2 ^ (s + 1) + 1) / (1 - 2 / 2 ^ s)

theorem theoremH_three (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k))
    (K : ℕ) (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) :
    ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) ≤ 1196
```

## Discrepancies with the source

1. **Constant.** The source's β_all(0) (exact binomials to L = 1400 plus a Chernoff tail, giving 27.163 at s = 3) is not formalized. `bad_mass` uses a rational Chernoff bound instead:
   - bad implies 2^L < 3^a·2^(s+1), hence 1 ≤ 2^(s+1)·(7/4)^a/(7/5)^L, because (7/4)² ≥ 3 and (7/5)² ≤ 2;
   - the level-L sum of (7/4)^a/(14/5)^L is (55/56)^L, so the total is at most 56·2^(s+1).
   
   Reaching 27.2 would need a kernel-checked evaluation of Σ b_L/2^L with exact binomials plus the tail, and the source's min(…, 2^(−L) + ln(1 + b_L/2^L)) refinement.
2. **Terras bijection.** It is formalized in generating-function form: Σ y^a over a level block equals (1+y)^L for every real y. The literal bijection onto {0,1}^L and the explicit formula for r_v are not formalized. Lemma 1 gives existence of r with the bound, as the task specified.
3. **Lemma 2.** The Lean version is non-strict and does not need x < 2^(L+1), so it is slightly more general.
4. **Lemma 3.** Neither `t < K` nor pairwise distinctness is needed, because distinct levels in A_t follow from L = t − k alone. Both hypotheses are dropped, giving a stronger statement. Distinctness is used only in Theorem H, for the bad part.
5. **Finite K.** The simplification is legitimate. With K finite, W is a finite sum, so W ≤ β + 1 + 2^(1−s)·W holds directly and 1 − 2^(1−s) ≥ 1/2 for s ≥ 2. A prefix of a distinct stretch is distinct, so the bound for all finite K gives the infinite case as a supremum of partial sums. The infinite (`tsum`) wording is not stated in Lean.
6. **Zero.** `x 0 = 0` is allowed. `Good s 0` is false and 1/0 = 0 in ℝ, and `hβ` is only asked about positive bad integers.
7. **Range of s.** Lemmas 1–3 hold for all s; Theorem H needs s ≥ 2. 2^(1−s) is written `2 / 2 ^ s`.

## Guards

- **`decide` examples:**
  - T 0 = 0, T 1 = 2, T 2 = 1, T 7 = 11, T 27 = 41, T^[5] 27 = 71, T^[4] 16 = 1.
  - oddCount 4 27 = 3; 2^4·T^4(27) = 3^3·27 + 23; 23·2^3 + 2^4·2^3 ≤ 3^3·2^4.
  - oddCount 6 97 = 4; 2^6·T^6(97) = 3^4·97 + 143.
  - My first draft of the 97 example had wrong numbers and `decide` rejected it; the values above come from Python.
- **`crosscheck.py`** (exact arithmetic, zero violations):
  - Lemma 1 on 24,573 instances and Lemma 2 on 44,204 instances.
  - Terras counts equal C(L,a) for L < 15.
  - Bad mass below 2^16 is 7.65, 9.03, 10.02 for s = 2, 3, 4, against bounds 448, 896, 1792.
  - Lemma 3 and Theorem H on all stretches from n < 3000; the largest harmonic sum is 2.936235.

## Build

`taskset -c 2-3 lake build` exited 0 with no Mathlib recompilation. Tail of the log:

```
ℹ [18276/18280] Built CollatzFMF.HarmonicAxioms (4.8s)
info: ...:5:0: 'CollatzFMF.Harmonic.oddCount_eq_card' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:6:0: 'CollatzFMF.Harmonic.lemma1' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:7:0: 'CollatzFMF.Harmonic.lemma2' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:8:0: 'CollatzFMF.Harmonic.good_16' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:9:0: 'CollatzFMF.Harmonic.bad_27' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:10:0: 'CollatzFMF.Harmonic.ancestors_double' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:11:0: 'CollatzFMF.Harmonic.lemma3' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:12:0: 'CollatzFMF.Harmonic.theoremH' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:13:0: 'CollatzFMF.Harmonic.oddCount_add' depends on axioms: [propext, Quot.sound]
info: ...:14:0: 'CollatzFMF.Harmonic.sum_pow_oddCount_block' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:15:0: 'CollatzFMF.Harmonic.bad_mass' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:16:0: 'CollatzFMF.Harmonic.theoremH_explicit' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:17:0: 'CollatzFMF.Harmonic.theoremH_three' depends on axioms: [propext, Classical.choice, Quot.sound]
✔ [18278/18280] Built CollatzFMF (5.2s)
Build completed successfully (18280 jobs).
```

## Claim boundary

Kernel-checked: the combinatorial core of Theorem H and an explicit finite bound for every finite distinct stretch. Not kernel-checked: the constant 27.2, the `tsum` wording, Theorems R and S, Corollary D, and Proposition I. None of this bears on the Collatz conjecture itself. Nothing was committed.