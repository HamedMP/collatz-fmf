# lean-gate — REPORT (round 6, November 2026)

## Verdict

| item | verdict |
|---|---|
| Theorem A (repetition barrier), incl. (A-i), (A-ii), (A-iii) | **KERNEL-CHECKED** |
| Lemma L (weighted two-block lemma) | **KERNEL-CHECKED** (natural-number weights) |
| Theorem B (two-block exclusion), full infinite form + finite `XX` form + B2-type corollary | **KERNEL-CHECKED** |
| H1 link (`ReturnStep` = block `b^r a` at `w = 33n+32`) and Theorem-B corollary for H1 orbits | **KERNEL-CHECKED** |
| Theorem T-core (disjoint subsets, `π*_a ≥ 1 + π*_{4a} + π*_{r₂}`) | **KERNEL-CHECKED** |
| Theorem T-full (Lemma G and Theorem T with real `γ`, `Real.rpow`, real `x`) | **KERNEL-CHECKED** |

No error was found in either source proof. No `sorry`, `axiom`, `native_decide`, `unsafe`,
`implemented_by` in any new file (grep-checked). Every theorem below reports only
`propext`, `Classical.choice`, `Quot.sound` (or a subset) under `#print axioms`.
Nothing is UNFINISHED; no unfinished-file was needed.

Files (all new; existing files untouched except four `import` lines appended to
`lean/CollatzFMF.lean`):

- `lean/CollatzFMF/Barrier.lean` — setup, (A-i)–(A-iii), Theorem A
- `lean/CollatzFMF/TwoBlock.lean` — Lemma L, Theorem B
- `lean/CollatzFMF/BarrierH1.lean` — link to `ReturnStep` / H1
- `lean/CollatzFMF/KLSound.lean` — Theorem T core, Lemma G, Theorem T
- `lean/CollatzFMF/GateAxioms.lean` — `#print axioms` audit
- `notes/round6-nov2026/lean-gate/crosscheck.py` — Python cross-check of the Lean examples and
  of the formal statements (6635 Theorem-A instances, 180 KL-core instances, exact integers)
- `notes/round6-nov2026/lean-gate/build.log` — full final build log

## Discrepancies with the source reports (none is an error)

1. **Lemma L weights.** The source lets `l_c, l_d > 0` be (implicitly real) weights; the Lean
   statement has natural-number weights, which is what Theorem B uses (`l = B∘σ`). In the two
   infinite-run cases the source says "n large"; Lean uses the explicit `n = l_c`
   (`y = c d^ω`) and `n = l_d + 1` (`y = c d c^ω`). A real-weight version would need the
   Archimedean property in exactly those two cases; it was not formalized.
2. **Theorem B "finite form".** The source says the conclusion already holds when the itinerary
   begins with `cc` or `c d^k c^j d`. That list omits the two infinite-run cases (`c d^ω`,
   `c d c^ω`), where a longer finite prefix (`c d^(l_c+1)`, resp. `c d c^(l_d+2)`) is what is
   used. Cosmetic. Lean proves the full infinite-word theorem and, separately, the `XX` finite
   form; the other finite forms are not stated separately.
3. **Integer form of (1.1).** `B(v) ≥ T0·G(v)` is exactly `4·e(v) ≤ 3·B(v)`
   (`four_e_le_three_B`); the certificate used in Theorem B is `16 ≤ 27` and `3^9 ≤ 2^16`.
4. **Theorem T hypotheses.** `c > 0` and `M = max c` are not needed: Lean assumes only
   `c m ≤ M` for `m < 3^k` and `M > 0`. Real `x` is handled as `S a ⌊x⌋₊`.
5. **Lemma G.** Formalized with the referee's repair (case `W(r) ≤ 0` handled by `π* ≥ 0`) and
   with explicit quantifiers (`a ≡ 2 (3)`, not on a cycle, real `x ≥ a`). `W ≤ M` is assumed
   on all naturals.
6. **(F4) disjointness.** Lean does not use "first visit times"; any visit times `j₁, j₂` work,
   with the same case split. The side facts needed are exactly `r₂ ≠ 4a`, `r₂ ≠ 2a`, and (for
   `a ≡ 2 mod 9`) `T(r₂) ≠ 4a`.
7. **(A-i)** is proved in full: forward (`run_modEq`), converse (`run_of_modEq`), the iff
   (`cylinder_eq_residue_class`) and non-emptiness with a positive representative
   (`cylinder_nonempty`).

## Definitions (verbatim)

```lean
-- Barrier.lean, namespace CollatzFMF.Barrier
inductive Letter | a | b
def Step : Letter → ℕ → ℕ → Prop
  | a, w, w' => w % 8 = 7 ∧ 8 * w' = 9 * w + 1
  | b, w, w' => w % 16 = 0 ∧ 16 * w' = 27 * w
def Run : List Letter → ℕ → ℕ → Prop
  | [], w, w' => w = w'
  | l :: v, w, w'' => ∃ w', Step l w w' ∧ Run v w' w''
def bits : Letter → ℕ | a => 3 | b => 4
def expo : Letter → ℕ | a => 2 | b => 3
def B (v : List Letter) : ℕ := (v.map bits).sum
def e (v : List Letter) : ℕ := (v.map expo).sum

-- TwoBlock.lean
def seg (y : ℕ → Bool) (i n : ℕ) : List Bool := (List.range n).map fun t => y (i + t)
def wt (lc ld : ℕ) (v : List Bool) : ℕ := (v.map fun b => if b then lc else ld).sum
def blk (X Y : List Letter) : List Bool → List Letter
  | [] => []
  | x :: v => (if x then X else Y) ++ blk X Y v

-- BarrierH1.lean
def retBlock (r : ℕ) : List Letter := List.replicate r b ++ [a]

-- KLSound.lean, namespace CollatzFMF.KL
def T (n : ℕ) : ℕ := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2
def Reach (x n a : ℕ) : Prop := ∃ j, T^[j] n = a ∧ ∀ i, i ≤ j → T^[i] n ≤ x
noncomputable def S (a x : ℕ) : Finset ℕ := (Finset.Icc 1 x).filter fun n => Reach x n a
def OnCycle (a : ℕ) : Prop := ∃ j, 1 ≤ j ∧ T^[j] a = a
def r2 (a : ℕ) : ℕ := if a % 9 = 8 then (2 * a - 1) / 3 else (4 * a - 2) / 3
noncomputable def cbar (k : ℕ) (c : ℕ → ℝ) (r : ℕ) : ℝ :=
  min (c (r % 3 ^ k)) (min (c ((r + 3 ^ (k - 1)) % 3 ^ k)) (c ((r + 2 * 3 ^ (k - 1)) % 3 ^ k)))
```

## Statements (verbatim), all COMPLETE

### Target 1 — Theorem A

```lean
theorem B_eq_count (v : List Letter) : B v = 3 * v.count a + 4 * v.count b
theorem e_eq_count (v : List Letter) : e v = 2 * v.count a + 3 * v.count b
theorem four_e_le_three_B (v : List Letter) : 4 * e v ≤ 3 * B v

-- (A-i)
theorem run_modEq {u : List Letter} {w w' x x' : ℕ} (h : Run u w x) (h' : Run u w' x') :
    w ≡ w' [MOD 2 ^ B u]
theorem run_of_modEq {u : List Letter} {w w' x : ℕ} (h : Run u w x)
    (hw : w' ≡ w [MOD 2 ^ B u]) : ∃ x', Run u w' x'
theorem cylinder_eq_residue_class {u : List Letter} {w x : ℕ} (h : Run u w x) (w' : ℕ) :
    (∃ x', Run u w' x') ↔ w' ≡ w [MOD 2 ^ B u]
theorem cylinder_nonempty (u : List Letter) : ∃ w x, 1 ≤ w ∧ Run u w x

-- (A-ii)
theorem step_lt {l : Letter} {w w' : ℕ} (h : Step l w w') (hw : 1 ≤ w) : w < w'

-- (A-iii)
theorem step_a_growth {w w' : ℕ} (h : Step a w w') : (w' + 1) * 8 = 9 * (w + 1)
theorem step_b_growth {w w' : ℕ} (h : Step b w w') : (w' + 1) * 16 ≤ 27 * (w + 1)
theorem run_growth {p : List Letter} {w w' : ℕ} (h : Run p w w') :
    (w' + 1) * 2 ^ B p ≤ 3 ^ e p * (w + 1)

-- Theorem A, state form (gives also 2^B(u) ≤ w_{i'} − w_i)
theorem barrier_core {q t u : List Letter} {w0 wi wi' x x' : ℕ} (h0 : 1 ≤ w0)
    (hq : Run q w0 wi) (ht : Run t wi wi') (htne : t ≠ [])
    (hu : Run u wi x) (hu' : Run u wi' x') :
    wi < wi' ∧ 2 ^ B u ≤ wi' - wi ∧
      2 ^ (B u + B (q ++ t)) < (w0 + 1) * 3 ^ e (q ++ t)

-- Theorem A, integer form: u occurs in P at positions |q| < |p|
theorem theoremA {P q p u s s' : List Letter} {w0 wend : ℕ} (h0 : 1 ≤ w0)
    (hP : Run P w0 wend) (h1 : P = q ++ u ++ s) (h2 : P = p ++ u ++ s')
    (hlen : q.length < p.length) :
    2 ^ (B u + B p) < (w0 + 1) * 3 ^ e p
```
Axioms: `run_of_modEq`, `step_lt`, `step_*_growth`, `run_growth`, `four_e_le_three_B`:
`[propext, Quot.sound]`; all others `[propext, Classical.choice, Quot.sound]`.

### Target 1 — Lemma L and Theorem B

```lean
theorem lemmaL (y : ℕ → Bool) (lc ld : ℕ) (hc : 0 < lc) (hd : 0 < ld) (h0 : y 0 = true) :
    ∃ i i' n, i < i' ∧ seg y i n = seg y i' n ∧
      wt lc ld (seg y 0 i') ≤ 3 * wt lc ld (seg y i' n) ∧ lc ≤ wt lc ld (seg y i' n)

theorem twoBlock_arith {w Bu Bp ep BX : ℕ} (h : 2 ^ (Bu + Bp) < (w + 1) * 3 ^ ep)
    (h1 : 4 * ep ≤ 3 * Bp) (h2 : Bp ≤ 3 * Bu) (h3 : BX ≤ Bu) :
    2 ^ (16 * BX) < (w + 1) ^ 4 * 3 ^ (9 * BX)

theorem theoremB (X Y : List Letter) (hX : X ≠ []) (hY : Y ≠ []) (y : ℕ → Bool)
    (h0 : y 0 = true) (w0 : ℕ) (hw : 1 ≤ w0)
    (hrun : ∀ n, ∃ w', Run (blk X Y (seg y 0 n)) w0 w') :
    2 ^ (16 * B X) < (w0 + 1) ^ 4 * 3 ^ (9 * B X)

theorem theoremB_XX (X : List Letter) (hX : X ≠ []) (w0 w' : ℕ) (hw : 1 ≤ w0)
    (hrun : Run (X ++ X) w0 w') : 2 ^ (16 * B X) < (w0 + 1) ^ 4 * 3 ^ (9 * B X)

theorem theoremB_bound (X Y : List Letter) (hX : X ≠ []) (hY : Y ≠ []) (y : ℕ → Bool)
    (h0 : y 0 = true) (w0 : ℕ) (hw : 1 ≤ w0)
    (hrun : ∀ n, ∃ w', Run (blk X Y (seg y 0 n)) w0 w') :
    B X < (w0 + 1) ^ 4

theorem no_twoBlock_hierarchy (w0 : ℕ) (hw : 1 ≤ w0) :
    ¬ ∀ N : ℕ, ∃ (X Y : List Letter) (y : ℕ → Bool), X ≠ [] ∧ Y ≠ [] ∧ y 0 = true ∧ N ≤ B X ∧
      ∀ n, ∃ w', Run (blk X Y (seg y 0 n)) w0 w'
```
"Itinerary of `w₀` lies in `{X,Y}^ω` with first block `X`" is rendered as: a block word
`y : ℕ → Bool` (`true = X`) with `y 0 = true`, every finite block prefix of which is admissible
at `w₀`. `no_twoBlock_hierarchy` is the integer form of Corollary B2 (and hence the engine of
B1); B1/B3 themselves (morphisms, episturmian words) are NOT formalized.
Axioms: all `[propext, Classical.choice, Quot.sound]`.

### Target 1 — link to `ReturnStep` / `H1`

```lean
theorem returnStep_run {n n' : ℕ} (h : ReturnStep n n') :
    ∃ r w, ReturnGate n r w ∧ Run (retBlock r) (33 * n + 32) (33 * n' + 32)
theorem returnStep_of_run {n n' r : ℕ} (h : Run (retBlock r) (33 * n + 32) (33 * n' + 32)) :
    ReturnStep n n'
theorem H1_orbit_run_twoBlock (n : ℕ → ℕ) (hn : ∀ j, ReturnStep (n j) (n (j + 1))) (r0 s : ℕ)
    (y : ℕ → Bool)
    (hy : ∀ j, ∃ w, ReturnGate (n j) (if y j then r0 else s) w) (N : ℕ) :
    Run (blk (retBlock r0) (retBlock s) (seg y 0 N)) (33 * n 0 + 32) (33 * n N + 32)
theorem H1_orbit_twoBlock_bound (n : ℕ → ℕ) (hn : ∀ j, ReturnStep (n j) (n (j + 1)))
    (r0 s : ℕ) (y : ℕ → Bool) (h0 : y 0 = true)
    (hy : ∀ j, ∃ w, ReturnGate (n j) (if y j then r0 else s) w) :
    2 ^ (16 * (4 * r0 + 3)) < (33 * n 0 + 33) ^ 4 * 3 ^ (9 * (4 * r0 + 3))
```
The last one: an orbit of the binary return map whose return word takes only two values
`r0 = r_0` and `s` has `(33 n_0 + 33)^4 · 3^(9(4r0+3)) > 2^(16(4r0+3))`. This is a size bound
for one two-letter return alphabet, not an exclusion; it does not prove any case of H1.
Axioms: `returnStep_run` `[propext, Quot.sound]`; others
`[propext, Classical.choice, Quot.sound]`.

### Target 2 — Theorem T

```lean
-- core
theorem disjoint_S {a x : ℕ} (ha : a % 3 = 2) (hc : ¬ OnCycle a)
    (h : a % 9 = 8 ∨ a % 9 = 2) : Disjoint (S (4 * a) x) (S (r2 a) x)
theorem core (a x : ℕ) (ha : a % 3 = 2) (hc : ¬ OnCycle a) (h : a % 9 = 8 ∨ a % 9 = 2)
    (hx : 4 * a ≤ x) :
    S (4 * a) x ⊆ S a x \ {a} ∧ S (r2 a) x ⊆ S a x \ {a} ∧
      Disjoint (S (4 * a) x) (S (r2 a) x) ∧
      1 + (S (4 * a) x).card + (S (r2 a) x).card ≤ (S a x).card
theorem core_four (a x : ℕ) (ha : 1 ≤ a) (hc : ¬ OnCycle a) (hx : 4 * a ≤ x) :
    1 + (S (4 * a) x).card ≤ (S a x).card
theorem admissible_four_mul {a : ℕ} (ha : a % 3 = 2) (hc : ¬ OnCycle a) :
    (4 * a) % 3 = 2 ∧ ¬ OnCycle (4 * a)
theorem admissible_r2 {a : ℕ} (hc : ¬ OnCycle a) (h : a % 9 = 8 ∨ a % 9 = 2) :
    (r2 a) % 3 = 2 ∧ ¬ OnCycle (r2 a)

-- full
theorem lemmaG (γ M : ℝ) (hγ : 0 < γ) (hM : 0 < M) (W : ℕ → ℝ) (hW : ∀ a, W a ≤ M)
    (hrow : ∀ a, a % 3 = 2 → ¬ OnCycle a →
      W a ≤ (4 : ℝ) ^ (-γ) * W (4 * a)
        + (if a % 9 = 8 then (3 / 2 : ℝ) ^ γ * W ((2 * a - 1) / 3) else 0)
        + (if a % 9 = 2 then (3 / 4 : ℝ) ^ γ * W ((4 * a - 2) / 3) else 0))
    (a : ℕ) (ha : a % 3 = 2) (hc : ¬ OnCycle a) (x : ℝ) (hx : (a : ℝ) ≤ x) :
    W a * (x / a) ^ γ / (4 ^ γ * M) ≤ ((S a ⌊x⌋₊).card : ℝ)

theorem theoremT (k : ℕ) (hk : 2 ≤ k) (γ M : ℝ) (hγ : 0 < γ) (hM : 0 < M) (c : ℕ → ℝ)
    (hcM : ∀ m, m < 3 ^ k → c m ≤ M)
    (L1 : ∀ m, m < 3 ^ k → m % 9 = 2 →
      c m ≤ (4 : ℝ) ^ (-γ) * c (4 * m % 3 ^ k)
        + (3 / 4 : ℝ) ^ γ * cbar k c ((4 * m - 2) / 3))
    (L2 : ∀ m, m < 3 ^ k → m % 9 = 5 → c m ≤ (4 : ℝ) ^ (-γ) * c (4 * m % 3 ^ k))
    (L3 : ∀ m, m < 3 ^ k → m % 9 = 8 →
      c m ≤ (4 : ℝ) ^ (-γ) * c (4 * m % 3 ^ k)
        + (3 / 2 : ℝ) ^ γ * cbar k c ((2 * m - 1) / 3))
    (a : ℕ) (ha : a % 3 = 2) (hc : ¬ OnCycle a) (x : ℝ) (hx : (a : ℝ) ≤ x) :
    c (a % 3 ^ k) * (x / a) ^ γ / (4 ^ γ * M) ≤ ((S a ⌊x⌋₊).card : ℝ)
```
Axioms: `admissible_*` `[propext, Quot.sound]`; others
`[propext, Classical.choice, Quot.sound]`.

What Theorem T in Lean does NOT cover: the existence of feasible weights `c` for any `k`, `γ`
(the LP certificates of section b4 are not in Lean), so no numerical exponent is
kernel-checked; Proposition N; the corollaries (ii)–(iv). The `cbar` lift uses the `3^(k−1)`
reading, as in the source.

## Sanity examples (Lean `example`s by `decide`/`norm_num`, mirrored in `crosscheck.py`)

- `Step a 7 8`, `Step b 16 27`, `Run [b,b,b] 4096 19683`, `Run [b,a] 80 152`,
  `Run [a,b,a] 71 152`; Theorem A on the last: `2^(3+7) = 1024 < 72·3^5 = 17496`.
- `Run ([b]++[b]) 256 729`; Theorem B: `2^64 < 257^4·3^36 = 654783403832048509485517521`.
- `3^9 < 2^16`, and `¬ 5^9 < 2^16` (the 5n+1 litmus).
- `Run (retBlock 0) (33·7+32) (33·8+32)`, `Run (retBlock 1) (33·48+32) (33·92+32)`
  (matches `T(7)=8`, `T(48)=92` in `Return.lean`).
- `T 5 = 8`, `T 8 = 4`, `T 11 = 17`, `T 7 = 11`; `r2 8 = 5`, `r2 11 = 14`, `r2 17 = 11`,
  `r2 20 = 26`; `OnCycle 1`, `OnCycle 2`.
- `crosscheck.py` output: `Theorem A instances: 6635`, `KL core instances: 180`, `OK`.
  (One arithmetic slip of mine in a draft `example` — a wrong decimal for `257^4·3^36` — was
  caught by Lean and corrected from Python; it was never in a theorem.)

## Build

Command: `export PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=2; cd lean && taskset -c 6 lake build`
(Mathlib was never rebuilt or re-fetched). Tail of `build.log` (gate lines, then the end):

```
ℹ [18270/18274] Built CollatzFMF.GateAxioms (4.1s)
info: CollatzFMF/GateAxioms.lean:10:0: 'CollatzFMF.Barrier.run_modEq' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:11:0: 'CollatzFMF.Barrier.run_of_modEq' depends on axioms: [propext, Quot.sound]
info: CollatzFMF/GateAxioms.lean:12:0: 'CollatzFMF.Barrier.cylinder_eq_residue_class' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:13:0: 'CollatzFMF.Barrier.cylinder_nonempty' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:14:0: 'CollatzFMF.Barrier.step_lt' depends on axioms: [propext, Quot.sound]
info: CollatzFMF/GateAxioms.lean:15:0: 'CollatzFMF.Barrier.step_a_growth' depends on axioms: [propext, Quot.sound]
info: CollatzFMF/GateAxioms.lean:16:0: 'CollatzFMF.Barrier.step_b_growth' depends on axioms: [propext, Quot.sound]
info: CollatzFMF/GateAxioms.lean:17:0: 'CollatzFMF.Barrier.run_growth' depends on axioms: [propext, Quot.sound]
info: CollatzFMF/GateAxioms.lean:18:0: 'CollatzFMF.Barrier.four_e_le_three_B' depends on axioms: [propext, Quot.sound]
info: CollatzFMF/GateAxioms.lean:19:0: 'CollatzFMF.Barrier.barrier_core' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:20:0: 'CollatzFMF.Barrier.theoremA' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:21:0: 'CollatzFMF.Barrier.theoremA_diff' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:22:0: 'CollatzFMF.Barrier.lemmaL' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:23:0: 'CollatzFMF.Barrier.twoBlock_arith' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:24:0: 'CollatzFMF.Barrier.theoremB' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:25:0: 'CollatzFMF.Barrier.theoremB_XX' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:26:0: 'CollatzFMF.Barrier.theoremB_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:27:0: 'CollatzFMF.Barrier.no_twoBlock_hierarchy' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:28:0: 'CollatzFMF.Barrier.returnStep_run' depends on axioms: [propext, Quot.sound]
info: CollatzFMF/GateAxioms.lean:29:0: 'CollatzFMF.Barrier.returnStep_of_run' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:30:0: 'CollatzFMF.Barrier.H1_orbit_run_twoBlock' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:31:0: 'CollatzFMF.Barrier.H1_orbit_twoBlock_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:32:0: 'CollatzFMF.KL.core' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:33:0: 'CollatzFMF.KL.core_four' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:34:0: 'CollatzFMF.KL.disjoint_S' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:35:0: 'CollatzFMF.KL.admissible_four_mul' depends on axioms: [propext, Quot.sound]
info: CollatzFMF/GateAxioms.lean:36:0: 'CollatzFMF.KL.admissible_r2' depends on axioms: [propext, Quot.sound]
info: CollatzFMF/GateAxioms.lean:37:0: 'CollatzFMF.KL.lemmaG' depends on axioms: [propext, Classical.choice, Quot.sound]
info: CollatzFMF/GateAxioms.lean:38:0: 'CollatzFMF.KL.theoremT' depends on axioms: [propext, Classical.choice, Quot.sound]
✔ [18272/18274] Built CollatzFMF (4.2s)
Build completed successfully (18274 jobs).
exit: 0
```
