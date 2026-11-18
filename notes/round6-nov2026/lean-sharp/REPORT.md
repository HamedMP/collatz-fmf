<!-- Saved by the coordinator from the lean-sharp agent's final message (the agent's own write was refused). -->
# lean-sharp report

All audited theorems depend only on `propext, Classical.choice, Quot.sound`. There is no `sorry`, `axiom`, `native_decide`, `unsafe` or `implemented_by`, and no WIP file. No existing file was edited, Mathlib was not rebuilt, and nothing was committed.

## Modules to import

Add to `lean/CollatzFMF.lean`:

```
import CollatzFMF.HarmonicSharp
import CollatzFMF.ResidueProduct
import CollatzFMF.SojournCount
import CollatzFMF.SharpAxioms
```

`SharpAxioms` imports the other three, so that line alone is enough.

## Statements (verbatim)

### `HarmonicSharp.lean` (namespace `CollatzFMF.HarmonicSharp`) — COMPLETE

```lean
theorem bad_mass_odd (v : ℕ) (S : Finset ℕ) (hS : ∀ n ∈ S, 0 < n ∧ ¬ Good (2 * v + 1) n) :
    ∑ n ∈ S, (1 / (n : ℝ)) ≤ 30 * 2 ^ (v + 1)

theorem theoremH_162 (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k))
    (K : ℕ) (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) :
    ∑ k ∈ Finset.range K, (1 / (x k : ℝ)) ≤ 162
```

The proof is the same as `bad_mass`, with two cheap changes:
- Base points `26/15 ≥ √3` and `41/29 ≤ √2` give a block ratio of exactly 29/30 (55/56 before).
- For odd `s` the bad condition is used through its square root, giving `2^((s+1)/2)` in place of `2^(s+1)`.

At `s = 3` this gives β = 120 and a bound of 121/(3/4) = 161.33. The source's 27.2 was not attempted.

### `ResidueProduct.lean` (namespace `CollatzFMF.Sharp`) — COMPLETE

```lean
noncomputable def oddFactor (m : ℕ) : ℝ := if m % 2 = 1 then 1 + 1 / (3 * (m : ℝ)) else 1

theorem product_identity_iterate (n k : ℕ) :
    (T^[k] n : ℝ) * 2 ^ k
      = (n : ℝ) * 3 ^ oddCount k n * ∏ i ∈ Finset.range k, oddFactor (T^[i] n)

theorem product_identity (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (k : ℕ) :
    (x k : ℝ) * 2 ^ k
      = (x 0 : ℝ) * 3 ^ oddCount k (x 0)
        * ∏ i ∈ (Finset.range k).filter (fun i => x i % 2 = 1), (1 + 1 / (3 * (x i : ℝ)))

theorem residue_bound_of_sum (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (k : ℕ) (σ : ℝ)
    (hσ : ∑ i ∈ Finset.range k, (1 / (x i : ℝ)) ≤ σ) :
    (x 0 : ℝ) * 3 ^ oddCount k (x 0) ≤ (x k : ℝ) * 2 ^ k ∧
      (x k : ℝ) * 2 ^ k ≤ Real.exp (σ / 3) * ((x 0 : ℝ) * 3 ^ oddCount k (x 0))

theorem residue_bound (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (k : ℕ) (hk : k ≤ K) :
    (x 0 : ℝ) * 3 ^ oddCount k (x 0) ≤ (x k : ℝ) * 2 ^ k ∧
      (x k : ℝ) * 2 ^ k ≤ Real.exp 54 * ((x 0 : ℝ) * 3 ^ oddCount k (x 0))

theorem cycle_injective (n p : ℕ) (hp : T^[p] n = n)
    (hmin : ∀ q, 0 < q → q < p → T^[q] n ≠ n) :
    ∀ i < p, ∀ j < p, T^[i] n = T^[j] n → i = j

theorem cycle_bounds_of_sum (n p : ℕ) (hn : 1 ≤ n) (hp1 : 1 ≤ p) (hp : T^[p] n = n) (σ : ℝ)
    (hσ : ∑ i ∈ Finset.range p, (1 / (T^[i] n : ℝ)) ≤ σ) :
    3 ^ oddCount p n < 2 ^ p ∧ (2 : ℝ) ^ p ≤ Real.exp (σ / 3) * 3 ^ oddCount p n

theorem cycle_pow_bounds (n p : ℕ) (hn : 1 ≤ n) (hp1 : 1 ≤ p) (hp : T^[p] n = n)
    (hmin : ∀ q, 0 < q → q < p → T^[q] n ≠ n) :
    3 ^ oddCount p n < 2 ^ p ∧ (2 : ℝ) ^ p ≤ Real.exp 54 * 3 ^ oddCount p n

theorem cycle_sharp (n p : ℕ) (hn : 1 ≤ n) (hp1 : 1 ≤ p) (hp : T^[p] n = n) (σ : ℝ)
    (hσ : ∑ i ∈ Finset.range p, (1 / (T^[i] n : ℝ)) ≤ σ) (hσ2 : Real.exp (σ / 3) < 2) :
    3 ^ oddCount p n < 2 ^ p ∧ 2 ^ p < 2 * 3 ^ oddCount p n ∧
      2 ^ (p - 1) < 3 ^ oddCount p n ∧
      (∀ q, 3 ^ oddCount p n < 2 ^ q → p ≤ q) ∧
      p = Nat.clog 2 (3 ^ oddCount p n + 1)

theorem cycle_sharp_of_sum_le_two (n p : ℕ) (hn : 1 ≤ n) (hp1 : 1 ≤ p) (hp : T^[p] n = n)
    (hσ : ∑ i ∈ Finset.range p, (1 / (T^[i] n : ℝ)) ≤ 2) :
    3 ^ oddCount p n < 2 ^ p ∧ 2 ^ p < 2 * 3 ^ oddCount p n ∧
      2 ^ (p - 1) < 3 ^ oddCount p n ∧
      (∀ q, 3 ^ oddCount p n < 2 ^ q → p ≤ q) ∧
      p = Nat.clog 2 (3 ^ oddCount p n + 1)
```

Notes on the exact forms:
- **No positivity needed:** the product identity and residue bound hold without `x 0 ≥ 1`.
- **Strictness:** `3^a < 2^p` is strict for every cycle, including 1→2→1, by parity.
- **Conditional form:** `cycle_sharp` takes `hσ` and `hσ2` as hypotheses. The 2^71 verification and the 1.386 evaluation are not formalized.
- **No `M` hypothesis:** with σ given directly, a lower bound on cycle elements is unused, as is minimality of `p`.
- **Ceiling:** `p = ⌈a·log₂ 3⌉` is rendered as `p = Nat.clog 2 (3^a + 1)`, alongside an explicit minimality clause.

### `SojournCount.lean` (namespace `CollatzFMF.Sojourn`) — COMPLETE

```lean
def count (x : ℕ → ℕ) (K Y : ℕ) : ℕ := ((Finset.range K).filter fun k => x k < Y).card

theorem landing (j x : ℕ) (hx : x < 2 ^ (j + 1)) : T^[j] x < 3 ^ (oddCount j x + 1)

def idx (P Q a : ℕ) : ℕ := (P * (a + 1) + Q - 1) / Q

theorem class_card_le (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (K j a i : ℕ)
    (hi : 3 ^ (a + 1) ≤ 2 ^ i) :
    ((Finset.range K).filter
        fun k => Nat.log 2 (x k) = j ∧ oddCount j (x k) = a ∧ k + j < K).card
      ≤ count x K (2 ^ i)

noncomputable def G (P Q d : ℕ) (κ : ℝ) : ℝ :=
  κ ^ (P + Q - 1) * κ ^ P / ((κ ^ P - 1) * κ ^ (d + 1))

theorem sojourn_abstract (P Q d : ℕ) (ν κ A : ℝ) (hQ : 1 ≤ Q) (hPQ : 3 ^ Q ≤ 2 ^ P)
    (hd : P ≤ d + 1) (hν : 1 ≤ ν) (hκ : 1 < κ) (hA0 : 0 ≤ A)
    (hch : 1 + ν ^ P ≤ κ ^ Q * ν ^ Q)
    (hA : 1 + ν ^ d + A * G P Q d κ ≤ A * (κ ^ Q - 1))
    (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (hx0 : 1 ≤ x 0) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (L : ℕ) :
    (count x K (2 ^ L) : ℝ) ≤ A * (κ ^ Q) ^ L

theorem sojourn_39_20 (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (hx0 : 1 ≤ x 0) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (L : ℕ) :
    (count x K (2 ^ L) : ℝ) ≤ 9 * (39 / 20 : ℝ) ^ L

theorem sojourn_sharp (x : ℕ → ℕ) (hx : ∀ k, x (k + 1) = T (x k)) (hx0 : 1 ≤ x 0) (K : ℕ)
    (hinj : ∀ i < K, ∀ j < K, x i = x j → i = j) (L : ℕ) :
    (count x K (2 ^ L) : ℝ) ≤ 10 * (9661 / 5000 : ℝ) ^ L
```

The irrational exponent is avoided by replacing every real power in blind-H's Theorem A with integer powers of two rationals:
- **Setup:** naturals `P, Q` with `3^Q ≤ 2^P`, Chernoff parameter `λ = ν^P`, base `q = κ^Q`.
- **High classes** (`Q·j ≤ P·a + d`): the weight `ν^(Pa+d)/ν^(Qj)` is at least 1, and `sum_pow_oddCount_block` sums it to at most `ν^d·q^j`.
- **Low classes with `k + j < K`:** `k ↦ k + j` injects into indices with term `< 3^(a+1) ≤ 2^idx(a)`, where `idx(a) = ⌈P(a+1)/Q⌉ ≤ j`. The induction hypothesis then sums geometrically to `A·G·q^j`.
- **End terms:** at most `L`.

| instance | (P, Q, d, ν, κ) | q = κ^Q | A needed | A stated |
|---|---|---|---|---|
| `sojourn_39_20` | (8, 5, 24, 16/15, 8/7) | 1.94966 ≤ 39/20 | 8.38 | 9 |
| `sojourn_sharp` | (65, 41, 211, 126/125, 251/247) | 1.932180 ≤ 9661/5000 | 9.72 | 10 |

The floor for `P/Q = 65/41` is 1.93197, against the true base 1.93181. Reaching 1.932 would need `ν, κ` accurate to about 1e-7 and was not attempted.

## Guards

- **Product identity:** n = 27 and n = 7 at k = 5 as exact rational identities by `norm_num`, with `oddCount` and `T^[5]` values by `decide`. The theorem itself is also instantiated at n = 27.
- **Cycle:** `T^[2] 1 = 1 ∧ oddCount 2 1 = 1 ∧ Nat.clog 2 (3^1+1) = 2` by `decide`.
- **Sojourn:** `count (fun k => T^[k] 27) 71 (2^5) = 10` by `decide`, and `sojourn_sharp` applied to the first 71 terms of the trajectory of 27.
- **Non-vacuity:** `10·1.9322^L < 2^L − 1` holds from L = 67 on and fails at L = 66; both are examples in the file. Below L = 67 the bound is true but weaker than the trivial count.
- **Python cross-check** (exact `Fraction` arithmetic, all pass): product identity for n < 300 plus 200 random 80-bit n; landing bound exhaustively for j ≤ 12; all parameter inequalities; both sojourn bounds for n ≤ 20000 and L < 20 (max ratio 0.83).

The kernel rejected two guard values I had guessed (13 terms, threshold 68); the Python values (10, 67) are the ones in the file.

## Discrepancies with the sources

None is an error; the differences are in strength.
1. **Theorem R:** exp(54) against the source's 7.62.
2. **Corollary D3:** unconditional `3^a < 2^p ≤ exp(54)·3^a`, plus the conditional sharp form. The source's 1.386 depends on the 2^71 verification.
3. **Theorem S:** base 1.9322 with A = 10, against 2^0.94996 ≈ 1.93181 with A = 9.3 (blind-H) or 11.3·X^η (w2-delta). End terms are bounded by L, not L − 1.
4. **Theorem H:** 162 against 27.2.
5. **Scope:** only the 3x+1 map `KL.T` is covered, not 3x−1.

## Build output tail

Command: `taskset -c 0-1 lake build CollatzFMF.SharpAxioms`

```
✔ [18262/18265] Built CollatzFMF.SojournCount (10s)
ℹ [18264/18265] Built CollatzFMF.SharpAxioms (4.8s)
info: ...:13:0: 'CollatzFMF.HarmonicSharp.bad_mass_odd' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:14:0: 'CollatzFMF.HarmonicSharp.theoremH_162' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:15:0: 'CollatzFMF.Sharp.product_identity_iterate' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:16:0: 'CollatzFMF.Sharp.product_identity' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:17:0: 'CollatzFMF.Sharp.residue_bound_of_sum' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:18:0: 'CollatzFMF.Sharp.residue_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:19:0: 'CollatzFMF.Sharp.cycle_injective' depends on axioms: [propext, Quot.sound]
info: ...:20:0: 'CollatzFMF.Sharp.cycle_bounds_of_sum' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:21:0: 'CollatzFMF.Sharp.cycle_pow_bounds' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:22:0: 'CollatzFMF.Sharp.cycle_sharp' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:23:0: 'CollatzFMF.Sharp.cycle_sharp_of_sum_le_two' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:24:0: 'CollatzFMF.Sojourn.landing' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:25:0: 'CollatzFMF.Sojourn.class_card_le' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:26:0: 'CollatzFMF.Sojourn.sojourn_abstract' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:27:0: 'CollatzFMF.Sojourn.sojourn_39_20' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ...:28:0: 'CollatzFMF.Sojourn.sojourn_sharp' depends on axioms: [propext, Classical.choice, Quot.sound]
Build completed successfully (18265 jobs).
```

## Files

New Lean modules, in `/home/matrix/home/projects/collatz/repo/lean/CollatzFMF/`:
- `HarmonicSharp.lean`
- `ResidueProduct.lean`
- `SojournCount.lean`
- `SharpAxioms.lean`

Notes, in `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/lean-sharp/` (`REPORT.md` is absent because the write was refused):
- `build.log`
- `crosscheck.py`
- `crosscheck.log`
- `params_search.py`