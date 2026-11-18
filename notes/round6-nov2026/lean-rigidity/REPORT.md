<!-- Saved by the coordinator from the lean-rigidity agent's final message (the agent's own write was refused). -->
## Modules for the coordinator to import

```
import CollatzFMF.Rigidity
import CollatzFMF.RigiditySharp
import CollatzFMF.RigidityAxioms
```

All three files are new; no existing file was edited.

- `/home/matrix/home/projects/collatz/repo/lean/CollatzFMF/Rigidity.lean` — definitions, Lemma 1, `T` has the properties, Theorem R.
- `/home/matrix/home/projects/collatz/repo/lean/CollatzFMF/RigiditySharp.lean` — `Sa`, `Ua`, Theorem S, other-side sharpness, `decide` guards.
- `/home/matrix/home/projects/collatz/repo/lean/CollatzFMF/RigidityAxioms.lean` — `#print axioms` for all 64 theorems of the two files.
- `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/lean-rigidity/build.log` — full output of the audit build.

The namespace is `CollatzFMF.Rigidity`, so `theoremR` does not clash with the existing module `CollatzFMF.TheoremR`. `T` is `CollatzFMF.KL.T` from `KLSound.lean`, reused unchanged.

## Lean statements (verbatim)

### Definitions

```lean
def Pos (S : ℕ → ℕ) : Prop := ∀ n, 0 < n → 0 < S n

def PrefixProp (S : ℕ → ℕ) : Prop :=
  ∀ n n', 0 < n → 0 < n' → n ≠ n' → n % 2 = n' % 2 →
    padicValInt 2 ((S n : ℤ) - (S n' : ℤ)) + 1 = padicValInt 2 ((n : ℤ) - (n' : ℤ))

def DvdProp (S : ℕ → ℕ) : Prop :=
  ∀ n n', 0 < n → 0 < n' → n ≠ n' → n % 2 = n' % 2 →
    ∀ k : ℕ, (2 : ℤ) ^ k ∣ ((S n : ℤ) - (S n' : ℤ)) ↔ (2 : ℤ) ^ (k + 1) ∣ ((n : ℤ) - (n' : ℤ))

def LitProp (S : ℕ → ℕ) : Prop :=
  ∀ n n', 0 < n → 0 < n' → ∀ k : ℕ,
    n % 2 ^ k = n' % 2 ^ k ↔ ∀ i, i < k → S^[i] n % 2 = S^[i] n' % 2

def CondII (S : ℕ → ℕ) : Prop := ∀ n, 0 < n → n % 2 = 0 → S n < n
def CondIII (S : ℕ → ℕ) : Prop := ∀ n, n % 2 = 1 → n < S n ∧ S n ≤ 2 * n

def Sa (a n : ℕ) : ℕ :=
  if n % 2 = 0 then n / 2
  else if n % 2 ^ (a + 1) = 2 ^ (a + 1) - 1 then (3 * n + 1) / 2 - 2 ^ a
  else (3 * n + 1) / 2

def Ua (a n : ℕ) : ℕ :=
  if n % 2 = 0 then n / 2
  else if n % 2 ^ (a + 1) = 2 ^ (a + 1) - 1 then (3 * n + 1) / 2 + 2 ^ a
  else (3 * n + 1) / 2
```

`padicValInt 2 z` is `padicValNat 2 z.natAbs` by definition, so `PrefixProp` is the requested form.

### Equivalences and Lemma 1 — KERNEL-CHECKED

```lean
theorem prefixProp_ne {S : ℕ → ℕ} (h : PrefixProp S) {n n' : ℕ} (hn : 0 < n) (hn' : 0 < n')
    (hne : n ≠ n') (hpar : n % 2 = n' % 2) : S n ≠ S n'
theorem prefixProp_iff_dvdProp (S : ℕ → ℕ) : PrefixProp S ↔ DvdProp S
theorem litProp_iff_dvdProp {S : ℕ → ℕ} (hpos : Pos S) : LitProp S ↔ DvdProp S
theorem lemma1 {S : ℕ → ℕ} (hpos : Pos S) : LitProp S ↔ PrefixProp S
```

### `T` has the properties — KERNEL-CHECKED

```lean
theorem prefixProp_T : PrefixProp T
theorem litProp_T : LitProp T
theorem pos_T : Pos T
theorem condII_T : CondII T
theorem condIII_T : CondIII T
```

### Theorem R — KERNEL-CHECKED

```lean
theorem descent (g : ℕ → ℤ) (hb : ∀ x, |g x| ≤ x)
    (hl : ∀ (x x' a : ℕ), x ≠ x' → (2 : ℤ) ^ a ∣ (x : ℤ) - (x' : ℤ) →
      (2 : ℤ) ^ (a + 1) ∣ g x - g x') : ∀ z, g z = 0
theorem even_part {S : ℕ → ℕ} (hpos : Pos S) (hD : DvdProp S) (hII : CondII S) :
    ∀ x, 0 < x → S (2 * x) = x
theorem odd_part {S : ℕ → ℕ} (hD : DvdProp S) (hIII : CondIII S) :
    ∀ x, S (2 * x + 1) = 3 * x + 2
theorem theoremR {S : ℕ → ℕ} (hpos : Pos S) (hI : PrefixProp S) (hII : CondII S)
    (hIII : CondIII S) : ∀ n, 0 < n → S n = T n
theorem theoremR_lit {S : ℕ → ℕ} (hpos : Pos S) (hI : LitProp S) (hII : CondII S)
    (hIII : CondIII S) : ∀ n, 0 < n → S n = T n
```

### Theorem S — KERNEL-CHECKED (every clause)

```lean
theorem pos_Sa (a : ℕ) : Pos (Sa a)                                   -- (i)
theorem prefixProp_Sa (a : ℕ) : PrefixProp (Sa a)                     -- (i)
theorem litProp_Sa (a : ℕ) : LitProp (Sa a)                           -- (i), literal form
theorem condII_Sa (a : ℕ) : CondII (Sa a)                             -- (iii)
theorem condIII_Sa (a n : ℕ) (ho : n % 2 = 1) (hne : n ≠ 2 ^ (a + 1) - 1) :
    n < Sa a n ∧ Sa a n ≤ 2 * n                                       -- (iii)
theorem Sa_fixed (a : ℕ) : Sa a (2 ^ (a + 1) - 1) = 2 ^ (a + 1) - 1   -- (iii)
theorem Sa_eq_T_off_class (a n : ℕ) (h : n % 2 ^ (a + 1) ≠ 2 ^ (a + 1) - 1) : Sa a n = T n  -- (ii)
theorem Sa_eq_T_of_lt (a n : ℕ) (h : n < 2 ^ (a + 1) - 1) : Sa a n = T n                    -- (ii)
theorem Sa_mod (a n : ℕ) : Sa a n % 2 ^ a = T n % 2 ^ a               -- (ii)
theorem Sa_zero (n : ℕ) (ho : n % 2 = 1) : Sa 0 n = (3 * n - 1) / 2   -- (iv)
theorem Sa_ne_T (a : ℕ) : Sa a (2 ^ (a + 1) - 1) ≠ T (2 ^ (a + 1) - 1)
theorem theoremS (a : ℕ) :
    Pos (Sa a) ∧ PrefixProp (Sa a) ∧ LitProp (Sa a) ∧ CondII (Sa a) ∧
    (∀ n, n % 2 = 1 → n ≠ 2 ^ (a + 1) - 1 → n < Sa a n ∧ Sa a n ≤ 2 * n) ∧
    Sa a (2 ^ (a + 1) - 1) = 2 ^ (a + 1) - 1 ∧
    (∀ n, n < 2 ^ (a + 1) - 1 → Sa a n = T n) ∧
    (∀ n, n % 2 ^ (a + 1) ≠ 2 ^ (a + 1) - 1 → Sa a n = T n) ∧
    (∀ n, Sa a n % 2 ^ a = T n % 2 ^ a) ∧
    Sa a (2 ^ (a + 1) - 1) ≠ T (2 ^ (a + 1) - 1)
```

Supporting general lemma (any perturbation supported on the class with `2^a ∣ e` keeps (I)):

```lean
theorem dvdProp_of_pert (S : ℕ → ℕ) (a : ℕ) (e : ℤ) (he : (2 : ℤ) ^ a ∣ e)
    (hev : ∀ x, S (2 * x) = x)
    (hodd : ∀ x, (S (2 * x + 1) : ℤ) =
      3 * (x : ℤ) + 2 + if x % 2 ^ a = 2 ^ a - 1 then e else 0) : DvdProp S
```

### Other-side sharpness — KERNEL-CHECKED

```lean
theorem sharp_upper (a : ℕ) :
    Pos (Ua a) ∧ PrefixProp (Ua a) ∧ LitProp (Ua a) ∧ CondII (Ua a) ∧
    (∀ n, n % 2 = 1 → n < Ua a n ∧ Ua a n ≤ 2 * n + 1) ∧
    (∀ n, n % 2 = 1 → n ≠ 2 ^ (a + 1) - 1 → n < Ua a n ∧ Ua a n ≤ 2 * n) ∧
    Ua a (2 ^ (a + 1) - 1) = 2 * (2 ^ (a + 1) - 1) + 1 ∧
    (∀ n, n % 2 ^ (a + 1) ≠ 2 ^ (a + 1) - 1 → Ua a n = T n) ∧
    Ua a (2 ^ (a + 1) - 1) ≠ T (2 ^ (a + 1) - 1)
```

This is slightly stronger than the referee's remark: `S n ≤ 2n` cannot be relaxed to `2n + 1` even at the single point `2^(a+1) − 1`.

## Discrepancies with the source

1. **Junk value of `v2(0)`.** Lean has `padicValInt 2 0 = 0`, while the source has `v2(0) = ∞`. Read literally, `PrefixProp` would allow `S n = S n'` when `v2(n − n') = 1`. This is harmless: `prefixProp_ne` proves `PrefixProp` already forces `S n ≠ S n'` (compare with the third point `n + 4`). `prefixProp_iff_dvdProp` then shows it is equivalent to the junk-free divisibility form `DvdProp`, so `PrefixProp` was not strengthened.
2. **Lemma 1 needs `S: N → N`.** `lemma1` carries the hypothesis `Pos S`, which is the source's standing assumption.
3. **Domain.** `S : ℕ → ℕ`, with every hypothesis and conclusion restricted to `n > 0`; `S 0` is unconstrained.
4. **Proof of Theorem R.** Same argument as the source, with the even and odd parts sharing one lemma `descent`. It is applied to `g(y) = S(2(y+1)) − (y+1)` and to `g(x) = S(2x+1) − (3x+2)`, and the minimal representative is `z mod 2^a`. No gap found.
5. **Where hypotheses are used.** `odd_part` uses neither positivity nor (II); `even_part` does not use (III).
6. **Truncated subtraction.** `(3n+1)/2 − 2^a` in `Sa` is natural-number subtraction, but it never truncates on the class. `Sa_zero` uses `3 * n - 1`, exact for `n ≥ 1`.

## Misformalization guards

`RigiditySharp.lean` contains 19 `decide` examples:

- `Sa 0 1 = 1`, `Sa 0 5 = 7`, `Sa 0 7 = 10`
- `Sa 1 3 = 3`, `Sa 1 5 = 8`, `Sa 1 7 = 9`
- `Sa 2 7 = 7`, `Sa 2 23 = 31`, `Sa 2 9 = 14`
- `Sa 3 12 = 6`, `Sa 3 15 = 15`, `Sa 3 31 = 39`
- `Ua 0 1 = 3`, `Ua 1 3 = 7`, `Ua 2 7 = 15`, `Ua 2 23 = 39`, `Ua 2 9 = 14`
- `T 7 = 11`, `T 23 = 35`

All 19 agree with an independent Python implementation run with the project venv. The same script confirmed the valuation identity (with `S n ≠ S n'`) for `T`, `S_0..S_5` and `U_0..U_5` on all same-parity pairs below 600. The script was run inline and not saved.

## Build

All three modules build on cores 2-3 with no Mathlib file recompiled, and with 0 warnings and 0 errors from these modules. The audit covers 64 theorems: 45 depend on `[propext, Classical.choice, Quot.sound]`, 13 on `[propext, Quot.sound]`, 6 on `[propext]`, and nothing else. The source files contain no `sorry`, `axiom`, `native_decide`, `unsafe` or `implemented_by`.

Selected lines from `build.log`:

```
'CollatzFMF.Rigidity.lemma1' depends on axioms: [propext, Classical.choice, Quot.sound]
'CollatzFMF.Rigidity.prefixProp_T' depends on axioms: [propext, Classical.choice, Quot.sound]
'CollatzFMF.Rigidity.theoremR' depends on axioms: [propext, Classical.choice, Quot.sound]
'CollatzFMF.Rigidity.theoremR_lit' depends on axioms: [propext, Classical.choice, Quot.sound]
'CollatzFMF.Rigidity.theoremS' depends on axioms: [propext, Classical.choice, Quot.sound]
'CollatzFMF.Rigidity.sharp_upper' depends on axioms: [propext, Classical.choice, Quot.sound]
Build completed successfully (18259 jobs).
```

## Not formalized

- The source's "Consequence" paragraph as a standalone iff ((I) ⇔ the two congruences on `γ` and `g`). Only the direction needed for Theorem R is proved, plus the converse for class-supported perturbations (`dvdProp_of_pert`).
- The Corollary ("what a proof must use"), the infimum-`1/2` claim, and the H1 remark.