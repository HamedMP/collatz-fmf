# Round 6 — Lean track REPORT

## (a) Summary

1. **FULL**: `CollatzConjecture ↔ H1 ∧ LemmaE` is kernel-checked (Lean 4.36.0 + Mathlib), with no
   `sorry`, `axiom`, `native_decide`, `unsafe` or `implemented_by` anywhere in the project.
2. All 69 theorems were audited with `#print axioms`; every one uses a subset of
   `[propext, Classical.choice, Quot.sound]` (file `lean/CollatzFMF/Axioms.lean`, output in
   `final-build.log`).
3. Collatz itself is NOT proved: `H1` and `LemmaE` are definitions of open statements.
4. Theorem A is proved against a *semantic* definition of FMF (`IsFMFIndex`: first Collatz iterate
   divisible by 4), not merely as algebra on the closed formula.
5. Lemma P is proved (over ℕ and over ℤ), with the quantitative form `16^k ∣ 11 m_0 + 1`.
6. The return identity `88·16^r·n' + 85·16^r = 3·27^r·(33n+32)` in STATE.md is CORRECT as stated
   (confirmed numerically from the real FMF dynamics on 3·10^6 values of n, then proved).
7. No statement of proof.md was found false. Three redundancies/sharpenings were found (section d).
8. The direction Collatz ⇒ H1 ∧ E is trivial in content (both are non-existence statements about
   orbits that Collatz forbids); the equivalence is a faithfulness check, not new mathematics.
9. Build: 52 s wall on 2 cores for the whole project (Mathlib cache intact, nothing rebuilt).
10. Toolchain note: this Mathlib has renamed the `padicValNat` API to `multiplicity` (deprecations
    dated 2026-10-28); the project avoids it apart from `Nat.padicValNat_def`.

## (b) Files

| File | Content |
|---|---|
| `lean/CollatzFMF/Smoke.lean` | pre-existing smoke test (goal 0: builds, 41 s wall first time, 26 s for the file) |
| `lean/CollatzFMF/Basic.lean` | `collatzStep`, `CollatzConjecture`, `v2`, Syracuse form and equivalence |
| `lean/CollatzFMF/FMF.lean` | `IsFMFIndex`, `fmf`, `fmfSteps`, `hop`, `letter`, `InG01`, Theorem A, letter/residue lemmas |
| `lean/CollatzFMF/Return.lean` | Lemma P, `ReturnGate`, `ReturnStep` (= T), return identity, `H1`, `LemmaE`, x_0 = 1 sanity |
| `lean/CollatzFMF/TheoremR.lean` | Theorem R, converse, `collatzConjecture_iff_H1_and_LemmaE` |
| `lean/CollatzFMF/Axioms.lean` | `#print axioms` for all 69 theorems |
| `notes/round6-nov2026/lean/check_defs.py` | independent Python check of every formalized identity and of the examples |
| `notes/round6-nov2026/lean/final-build.log` | full build output including the axiom audit |

There is no UNFINISHED file: nothing was left with `sorry`.

### How the paper's objects are encoded

* FMF: `IsFMFIndex x k := 4 ∣ C^[k] x ∧ ∀ j < k, ¬ 4 ∣ C^[j] x`. The closed forms are
  `fmf x = 2(3^s m − 1)`, `fmfSteps x = 2s − 1` with `s = v2 (x+1)`, `x + 1 = 2^s m`
  (s = 1 Case A, s = 2 Case B1, s = t+2 Case B2). `theoremA` ties the closed form to the semantics.
* Hop `F(x) = fmf x / 2^(v2 (fmf x))`, letter `(v2 (x+1), v2 (fmf x))`, `G01 = {(2,2),(3,2)}`.
* `ReturnStep n n'` is the paper's partial map: `33n+32 = 16^r w`, `w ≡ ε_r (mod 8)`,
  `88 n' + 85 = 3·27^r·w`. Proved: unique `(r,w)`, unique `n'`, exact division, undefined at 0.
* `H1 := ¬ ∃ n : ℕ → ℕ, ∀ j, ReturnStep (n j) (n (j+1))` (and `H1_iff_pos`: same as positive orbits).
* `LemmaE := ∀ x0, x0 odd → 1 < x0 → (∀ k, x0 ≤ F^[k] x0) → ∃ N, ∀ k ≥ N, letter (F^[k] x0) ∈ G01`.

### Proof architecture of Theorem R (all kernel-checked)

Letter (2,2) ⟺ x ≡ 11 (mod 16), hop `8x' = 9x+5`; letter (3,2) ⟺ x ≡ 7 (mod 32), hop
`16x' = 27x+19`. With `V(x) = 11x+19`, `W(x) = V(x)+4`: `16 V(x') = 27 V(x)` on (3,2) (this IS
Lemma P, `m = (x+1)/8`), `8 V(x') = 9 W(x)` on (2,2). A block (2,2)(3,2)^r therefore gives
`8·16^r·V(x_(r+1)) = 9·27^r·W(x_0)` (`block_identity`), which at depth-0 normal-form states
`x = 96n+91` is exactly the return identity. `no_G01_tail`: an infinite G01 chain has either
finitely many depth-0 states (contradiction by `lemmaP`) or infinitely many (an infinite
`ReturnStep` orbit built by dependent choice, contradicting `H1`). `fmf_descent` then gives
pointwise descent, and strong induction gives `theoremR`. Converse: `hop_of_returnStep` realises
every return step by real FMF hops, so an infinite T-orbit is an FMF orbit that never reaches 1.

## (c) Statements (verbatim) and status

### `lean/CollatzFMF/Basic.lean`

```lean
def collatzStep (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else 3 * n + 1
```
Status: DEFINITION

```lean
def CollatzConjecture : Prop :=
  ∀ n : ℕ, 1 ≤ n → ∃ k : ℕ, collatzStep^[k] n = 1
```
Status: DEFINITION

```lean
def v2 (n : ℕ) : ℕ := padicValNat 2 n
```
Status: DEFINITION

```lean
theorem collatzStep_even (n : ℕ) : collatzStep (2 * n) = n
```
Status: COMPLETE — axioms: [propext]

```lean
theorem collatzStep_odd {n : ℕ} (h : n % 2 = 1) : collatzStep n = 3 * n + 1
```
Status: COMPLETE — axioms: [propext]

```lean
theorem collatzStep_iter_two_pow (a q : ℕ) : collatzStep^[a] (2 ^ a * q) = q
```
Status: COMPLETE — axioms: [propext]

```lean
theorem collatzStep_iter_one (i : ℕ) :
    collatzStep^[i] 1 = 1 ∨ collatzStep^[i] 1 = 2 ∨ collatzStep^[i] 1 = 4
```
Status: COMPLETE — axioms: [propext, Quot.sound]

```lean
theorem exists_odd_mul (n : ℕ) (hn : n ≠ 0) : ∃ m, m % 2 = 1 ∧ n = 2 ^ v2 n * m
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem two_pow_mul_odd_unique {a b m m' : ℕ} (hm : m % 2 = 1) (hm' : m' % 2 = 1)
    (h : 2 ^ a * m = 2 ^ b * m') : a = b
```
Status: COMPLETE — axioms: [propext, Quot.sound]

```lean
theorem v2_eq_of {n k m : ℕ} (h : n = 2 ^ k * m) (hm : m % 2 = 1) : v2 n = k
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem accel_reaches_one (G : ℕ → ℕ)
    (hG : ∀ x, x % 2 = 1 → G x % 2 = 1 ∧ ∃ n, 1 ≤ n ∧ G x = collatzStep^[n] x) :
    ∀ k x, x % 2 = 1 → collatzStep^[k] x = 1 → ∃ j, G^[j] x = 1
```
Status: COMPLETE — axioms: [propext, Quot.sound]

```lean
theorem accel_iter_is_collatz_iter (G : ℕ → ℕ)
    (hG : ∀ x, x % 2 = 1 → G x % 2 = 1 ∧ ∃ n, 1 ≤ n ∧ G x = collatzStep^[n] x) :
    ∀ j x, x % 2 = 1 → G^[j] x % 2 = 1 ∧ ∃ i, G^[j] x = collatzStep^[i] x
```
Status: COMPLETE — axioms: [propext, Quot.sound]

```lean
theorem collatz_iff_accel (G : ℕ → ℕ)
    (hG : ∀ x, x % 2 = 1 → G x % 2 = 1 ∧ ∃ n, 1 ≤ n ∧ G x = collatzStep^[n] x) :
    CollatzConjecture ↔ ∀ x, x % 2 = 1 → ∃ j, G^[j] x = 1
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
def syracuse (x : ℕ) : ℕ := (3 * x + 1) / 2 ^ v2 (3 * x + 1)
```
Status: DEFINITION

```lean
def SyracuseConjecture : Prop := ∀ x : ℕ, x % 2 = 1 → ∃ k : ℕ, syracuse^[k] x = 1
```
Status: DEFINITION

```lean
theorem syracuse_spec (x : ℕ) (hx : x % 2 = 1) :
    syracuse x % 2 = 1 ∧ ∃ n, 1 ≤ n ∧ syracuse x = collatzStep^[n] x
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem collatzConjecture_iff_syracuse : CollatzConjecture ↔ SyracuseConjecture
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]


### `lean/CollatzFMF/FMF.lean`

```lean
def IsFMFIndex (x k : ℕ) : Prop :=
  4 ∣ collatzStep^[k] x ∧ ∀ j < k, ¬ 4 ∣ collatzStep^[j] x
```
Status: DEFINITION

```lean
theorem isFMFIndex_unique {x k k' : ℕ} (h : IsFMFIndex x k) (h' : IsFMFIndex x k') : k = k'
```
Status: COMPLETE — axioms: no axioms

```lean
def fmf (x : ℕ) : ℕ := 2 * (3 ^ v2 (x + 1) * ((x + 1) / 2 ^ v2 (x + 1)) - 1)
```
Status: DEFINITION

```lean
def fmfSteps (x : ℕ) : ℕ := 2 * v2 (x + 1) - 1
```
Status: DEFINITION

```lean
def hop (x : ℕ) : ℕ := fmf x / 2 ^ v2 (fmf x)
```
Status: DEFINITION

```lean
def letter (x : ℕ) : ℕ × ℕ := (v2 (x + 1), v2 (fmf x))
```
Status: DEFINITION

```lean
def InG01 (l : ℕ × ℕ) : Prop := l = (2, 2) ∨ l = (3, 2)
```
Status: DEFINITION

```lean
theorem iter_add_two (j x : ℕ) :
    collatzStep^[j + 2] x = collatzStep^[j] (collatzStep (collatzStep x))
```
Status: COMPLETE — axioms: no axioms

```lean
theorem isFMFIndex_shift {x k : ℕ} (h0 : ¬ 4 ∣ x) (h1 : ¬ 4 ∣ collatzStep x)
    (h : IsFMFIndex (collatzStep (collatzStep x)) k) : IsFMFIndex x (k + 2)
```
Status: COMPLETE — axioms: [propext, Quot.sound]

```lean
theorem fmf_core : ∀ (s a x : ℕ), a % 2 = 1 → x + 1 = 2 ^ (s + 1) * a →
    IsFMFIndex x (2 * s + 1) ∧ collatzStep^[2 * s + 1] x + 2 = 2 * 3 ^ (s + 1) * a
```
Status: COMPLETE — axioms: [propext, Quot.sound]

```lean
theorem fmf_eq {x s m : ℕ} (hm : m % 2 = 1) (h : x + 1 = 2 ^ s * m) :
    v2 (x + 1) = s ∧ fmf x + 2 = 2 * 3 ^ s * m
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem hop_eq {x v q : ℕ} (hq : q % 2 = 1) (h : fmf x = 2 ^ v * q) :
    v2 (fmf x) = v ∧ hop x = q
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem fmf_spec (x : ℕ) (hx : x % 2 = 1) :
    ∃ s m, m % 2 = 1 ∧ x + 1 = 2 ^ (s + 1) * m ∧ v2 (x + 1) = s + 1 ∧
      fmf x + 2 = 2 * 3 ^ (s + 1) * m ∧ IsFMFIndex x (2 * s + 1) ∧
      collatzStep^[2 * s + 1] x = fmf x
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem theoremA (x : ℕ) (hx : x % 2 = 1) :
    IsFMFIndex x (fmfSteps x) ∧ collatzStep^[fmfSteps x] x = fmf x
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem theoremA_caseA (k x : ℕ) (hx : x = 4 * k + 1) :
    IsFMFIndex x 1 ∧ collatzStep^[1] x = 4 * (3 * k + 1)
```
Status: COMPLETE — axioms: [propext, Quot.sound]

```lean
theorem theoremA_caseB1 (j x : ℕ) (hx : x = 4 * (2 * j) + 3) :
    IsFMFIndex x 3 ∧ collatzStep^[3] x = 4 * (9 * j + 4)
```
Status: COMPLETE — axioms: [propext, Quot.sound]

```lean
theorem theoremA_typeB (k t m x : ℕ) (hx : x = 4 * k + 3) (hk : k + 1 = 2 ^ t * m)
    (hm : m % 2 = 1) :
    IsFMFIndex x (3 + 2 * t) ∧ collatzStep^[3 + 2 * t] x = 2 * (3 ^ (t + 2) * m - 1)
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem theoremA_caseB2 (k t m x : ℕ) (hx : x = 4 * k + 3) (_hkodd : k % 2 = 1)
    (hk : k + 1 = 2 ^ t * m) (hm : m % 2 = 1) (_ht : 1 ≤ t) :
    IsFMFIndex x (3 + 2 * t) ∧ collatzStep^[3 + 2 * t] x = 2 * (3 ^ (t + 2) * m - 1)
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem hop_spec (x : ℕ) (hx : x % 2 = 1) :
    hop x % 2 = 1 ∧ ∃ n, 1 ≤ n ∧ hop x = collatzStep^[n] x
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem hop_iter_odd (x : ℕ) (hx : x % 2 = 1) (k : ℕ) : hop^[k] x % 2 = 1
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem collatzConjecture_iff_hop :
    CollatzConjecture ↔ ∀ x, x % 2 = 1 → ∃ k, hop^[k] x = 1
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem hop_of_mod16 {x : ℕ} (h : x % 16 = 11) : letter x = (2, 2) ∧ 8 * hop x = 9 * x + 5
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem hop_of_mod32 {x : ℕ} (h : x % 32 = 7) : letter x = (3, 2) ∧ 16 * hop x = 27 * x + 19
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem mod16_of_letter {x : ℕ} (h : letter x = (2, 2)) : x % 16 = 11
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem mod32_of_letter {x : ℕ} (h : letter x = (3, 2)) : x % 32 = 7
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem letter_22_iff (x : ℕ) : letter x = (2, 2) ↔ x % 16 = 11
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem letter_32_iff (x : ℕ) : letter x = (3, 2) ↔ x % 32 = 7
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem inG01_cases {x : ℕ} (h : InG01 (letter x)) :
    (x % 16 = 11 ∧ 8 * hop x = 9 * x + 5) ∨ (x % 32 = 7 ∧ 16 * hop x = 27 * x + 19)
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem hop_letter_eval {x s m v q : ℕ} (hm : m % 2 = 1) (h : x + 1 = 2 ^ s * m)
    (hq : q % 2 = 1) (hf : 2 * 3 ^ s * m = 2 ^ v * q + 2) :
    fmf x = 2 ^ v * q ∧ hop x = q ∧ letter x = (s, v)
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]


### `lean/CollatzFMF/Return.lean`

```lean
theorem lemmaP_identity {m m' : ℕ} (h : 16 * m' = 27 * m + 1) :
    16 * (11 * m' + 1) = 27 * (11 * m + 1)
```
Status: COMPLETE — axioms: [propext, Quot.sound]

```lean
theorem pow16_dvd_of {k a b : ℕ} (h : 16 ^ k * a = 27 ^ k * b) : 16 ^ k ∣ b
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem not_all_pow16_dvd {b : ℕ} (hb : 0 < b) (h : ∀ k, 16 ^ k ∣ b) : False
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem lemmaP_valuation (m : ℕ → ℕ) (k : ℕ)
    (h : ∀ i < k, 16 * m (i + 1) = 27 * m i + 1) : 16 ^ k ∣ 11 * m 0 + 1
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem lemmaP : ¬ ∃ m : ℕ → ℕ, ∀ k, 16 * m (k + 1) = 27 * m k + 1
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem lemmaP_int : ¬ ∃ m : ℕ → ℤ, ∀ k, 16 * m (k + 1) = 27 * m k + 1
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
def epsR (r : ℕ) : ℕ := if r % 2 = 0 then 7 else 5
```
Status: DEFINITION

```lean
def ReturnGate (n r w : ℕ) : Prop := 33 * n + 32 = 16 ^ r * w ∧ w % 8 = epsR r
```
Status: DEFINITION

```lean
def ReturnStep (n n' : ℕ) : Prop := ∃ r w, ReturnGate n r w ∧ 88 * n' + 85 = 3 * 27 ^ r * w
```
Status: DEFINITION

```lean
def H1 : Prop := ¬ ∃ n : ℕ → ℕ, ∀ j, ReturnStep (n j) (n (j + 1))
```
Status: DEFINITION

```lean
theorem pow27_mod8 (r : ℕ) : 27 ^ r % 8 = if r % 2 = 0 then 1 else 3
```
Status: COMPLETE — axioms: [propext, Quot.sound]

```lean
theorem pow27_mod11 (r : ℕ) : 27 ^ r % 11 = 16 ^ r % 11
```
Status: COMPLETE — axioms: [propext]

```lean
theorem return_identity {n n' r w : ℕ} (hg : ReturnGate n r w)
    (h : 88 * n' + 85 = 3 * 27 ^ r * w) :
    88 * 16 ^ r * n' + 85 * 16 ^ r = 3 * 27 ^ r * (33 * n + 32)
```
Status: COMPLETE — axioms: [propext]

```lean
theorem return_identity_y {n n' r w : ℕ} (hg : ReturnGate n r w)
    (h : 88 * n' + 85 = 3 * 27 ^ r * w) :
    8 * 16 ^ r * (33 * n' + 32) = 9 * 27 ^ r * (33 * n + 32) + 16 ^ r
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem returnStep_of_identity {n n' r : ℕ}
    (h : 16 ^ r * (88 * n' + 85) = 3 * 27 ^ r * (33 * n + 32)) : ReturnStep n n'
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem returnStep_iff (n n' : ℕ) :
    ReturnStep n n' ↔ ∃ r, 16 ^ r * (88 * n' + 85) = 3 * 27 ^ r * (33 * n + 32)
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem epsR_odd (r : ℕ) : epsR r % 2 = 1
```
Status: COMPLETE — axioms: no axioms

```lean
theorem returnGate_unique {n r w r' w' : ℕ} (h : ReturnGate n r w) (h' : ReturnGate n r' w') :
    r = r' ∧ w = w'
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem returnStep_unique {n a b : ℕ} (ha : ReturnStep n a) (hb : ReturnStep n b) : a = b
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem returnGate_exact {n r w : ℕ} (hg : ReturnGate n r w) :
    ∃ n', 88 * n' + 85 = 3 * 27 ^ r * w
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem not_returnStep_zero (n' : ℕ) : ¬ ReturnStep 0 n'
```
Status: COMPLETE — axioms: [propext, Quot.sound]

```lean
theorem H1_iff_pos :
    H1 ↔ ¬ ∃ n : ℕ → ℕ, (∀ j, 0 < n j) ∧ ∀ j, ReturnStep (n j) (n (j + 1))
```
Status: COMPLETE — axioms: [propext, Quot.sound]

```lean
def NonDescending (x0 : ℕ) : Prop := ∀ k, x0 ≤ hop^[k] x0
```
Status: DEFINITION

```lean
def EventuallyG01 (x0 : ℕ) : Prop := ∃ N, ∀ k, N ≤ k → InG01 (letter (hop^[k] x0))
```
Status: DEFINITION

```lean
def LemmaE : Prop :=
  ∀ x0 : ℕ, x0 % 2 = 1 → 1 < x0 → NonDescending x0 → EventuallyG01 x0
```
Status: DEFINITION

```lean
theorem hop_one : hop 1 = 1 ∧ letter 1 = (1, 2)
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem hop_iter_one (k : ℕ) : hop^[k] 1 = 1
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem lemmaE_fails_at_one : NonDescending 1 ∧ ¬ EventuallyG01 1
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem lemmaE_without_gt_one_false :
    ¬ (∀ x0 : ℕ, x0 % 2 = 1 → NonDescending x0 → EventuallyG01 x0)
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]


### `lean/CollatzFMF/TheoremR.lean`

```lean
theorem exists_seq {α : Type} (P : α → Prop) (R : α → α → Prop)
    (h0 : ∃ a, P a) (hstep : ∀ a, P a → ∃ b, P b ∧ R a b) :
    ∃ f : ℕ → α, ∀ j, P (f j) ∧ R (f j) (f (j + 1))
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem hop_depth0 (n : ℕ) : hop (96 * n + 91) = 108 * n + 103
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem depth1_run : ∀ (j x c : ℕ), 11 * x + 19 = 32 * 16 ^ j * c →
    11 * hop^[j] x + 19 = 32 * 27 ^ j * c
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem hop_of_returnStep {n n' : ℕ} (h : ReturnStep n n') :
    ∃ k, 1 ≤ k ∧ hop^[k] (96 * n + 91) = 96 * n' + 91
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem block_identity (g : ℕ → ℕ) (a : ℕ) (h0 : 8 * g (a + 1) = 9 * g a + 5) :
    ∀ r, (∀ i < r, 16 * g (a + 1 + i + 1) = 27 * g (a + 1 + i) + 19) →
      8 * 16 ^ r * (11 * g (a + 1 + r) + 19) = 9 * 27 ^ r * (11 * g a + 23)
```
Status: COMPLETE — axioms: [propext, Quot.sound]

```lean
theorem no_G01_tail (h1 : H1) (g : ℕ → ℕ)
    (hg : ∀ k, (g k % 16 = 11 ∧ 8 * g (k + 1) = 9 * g k + 5) ∨
               (g k % 32 = 7 ∧ 16 * g (k + 1) = 27 * g k + 19))
    (h3 : ∀ k, g k % 3 = 1) : False
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem fmf_descent (h1 : H1) (hE : LemmaE) (x : ℕ) (hx : x % 2 = 1) (hx1 : 1 < x) :
    ∃ k, hop^[k] x < x
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem theoremR (h1 : H1) (hE : LemmaE) : CollatzConjecture
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem lemmaE_of_collatz (hC : CollatzConjecture) : LemmaE
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem H1_of_collatz (hC : CollatzConjecture) : H1
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem collatzConjecture_iff_H1_and_LemmaE : CollatzConjecture ↔ H1 ∧ LemmaE
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]

```lean
theorem no_G01_word_of_H1 (h1 : H1) : ¬ ∃ x : ℕ, ∀ k, InG01 (letter (hop^[k] x))
```
Status: COMPLETE — axioms: [propext, Classical.choice, Quot.sound]


## (d) Discrepancies and findings relative to proof.md / STATE.md

No false statement was found. Points a reader should know:

1. **STATE.md identity is correct**: `88·16^r·n' + 85·16^r = 3·27^r·(33n+32)` (`return_identity`).
   Equivalent y-form `8·16^r·y' = 9·27^r·y + 16^r` also proved (`return_identity_y`).
2. **The mod-8 gate condition is redundant** (`returnStep_iff`): for natural numbers,
   `T(n) = n'` ⟺ `∃ r, 16^r(88n'+85) = 3·27^r(33n+32)`. The congruence `w ≡ ε_r (mod 8)` and the
   oddness of `w` follow from integrality of `n'`. Not an error in the paper, a simplification.
3. **Theorem A Case B2**: the hypotheses "k odd" and "t ≥ 1" are not needed (`theoremA_typeB`),
   matching the paper's Unified Type B proposition; one formula `2(3^s m − 1)`, `2s − 1` steps,
   covers Case A as well (s = 1).
4. **Lemma P** holds over all integers, not only positive ones (`lemmaP_int`); positivity plays no
   role, consistent with "H1/P are multiplier- and sign-blind, E carries the 3-dependence".
5. **Lemma E needs both repairs named in STATE.md §B**: `x_0 > 1` (`lemmaE_fails_at_one`: the orbit
   of 1 is constant with letter (1,2)) and weak non-descent. The formal proof of `fmf_descent`
   uses exactly the negation of descent, `∀ k, x_0 ≤ x_k`; a strict version of E would not feed it.
6. **Normal form subtlety**: a depth-0 state is `96n+91` only if (i) the previous hop had even
   `v` (gives x ≡ 1 mod 3) and (ii) the next letter is again in G01 (gives m ≡ 7 mod 8). This is
   the paper's "after discarding at most the initial state"; the Lean proof shifts the tail by one
   hop to obtain (i). `x ≡ 11 (mod 16)` alone is not enough.
7. Not formalized: "equivalently μ_L → ∞" in the statement of H1; the converse of
   `no_G01_word_of_H1`; "finite epoch" (only pointwise descent is stated); the supporting partials
   of Theorem 55 (ballot inequality, shadow theorem, dimension identity).

## (e) Reproduce

```
export PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=2
cd /home/matrix/home/projects/collatz/repo/lean && taskset -c 3-4 lake build
/home/matrix/home/projects/collatz/venv/bin/python notes/round6-nov2026/lean/check_defs.py   # prints ALL OK
```

Build output tail (`final-build.log`; the 69 axiom lines precede it, none outside the allowed set):

```
info: CollatzFMF/Axioms.lean:72:0: 'CollatzFMF.theoremR' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/Axioms.lean:73:0: 'CollatzFMF.lemmaE_of_collatz' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/Axioms.lean:74:0: 'CollatzFMF.H1_of_collatz' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/Axioms.lean:75:0: 'CollatzFMF.collatzConjecture_iff_H1_and_LemmaE' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/Axioms.lean:76:0: 'CollatzFMF.no_G01_word_of_H1' depends on axioms: [propext, Classical.choice, Quot.sound]
✔ [18262/18264] Built CollatzFMF (7.4s)
Build completed successfully (18264 jobs).
exit: 0
```

Forbidden-construct scan: `grep -rnE "sorry|axiom |native_decide|unsafe|implemented_by" lean/CollatzFMF/*.lean`
matches only doc-comment text ("no `sorry`") and the `#print axioms` lines.

## (f) Best lead for a follow-up

The formalization shows the whole reduction lives in two linear forms, `V = 11x+19` and
`W = V+4`. A natural next Lean target is the cocycle/master identity of Theorem 62 (A1, A2) for
arbitrary hop words, of which `block_identity` is the G01 special case.
