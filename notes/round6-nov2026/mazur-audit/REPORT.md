# mazur-audit — audit of L. Mazur's ProofAtlas Collatz claims (round 6, 2026-11-17)

Evidence grades used below: **REBUILT** (I compiled it), **READ-STATEMENT** (I read the Lean statement and
every definition under it), **READ-PROOF** (I read that proof step in paper and/or Lean), **PAGE-ASSERTS**
(only the publisher says so), **NUMERIC** (my own computation, bound stated).

## (a) Summary

1. Claim (1) positive lower density, 10.46 ln n clock: **STATEMENT-MATCHES (not rebuilt)**. Credence prose theorem true: **0.85**.
2. Claim (2) predecessor exponent 0.90: **STATEMENT-MATCHES (not rebuilt)**, depends on `native_decide` (disclosed). Credence: **0.93**.
3. Claim (3) natural-density log-time descent: **STATEMENT-MATCHES (not rebuilt)**. Credence: **0.90**.
4. Nothing was rebuilt: all three artifacts pin Lean `v4.30.0-rc2` (Mathlib `5450b53e…` / `v4.30.0-rc2`); the local cache is Mathlib v4.36.0. Per brief I did not fetch a second Mathlib. An opportunistic direct-`lean` compile of claim (1) against v4.36.0 broke on Mathlib drift (4 of the first 47 modules; 43 compiled). So "build passed, axioms = propext/Classical.choice/Quot.sound" remains PAGE-ASSERTS.
5. Claim (1) Lean statement is exactly the prose statement: ordinary map (odd step 3n+1, no halving), `0 < n`, `∃ k, k ≤ (523/50)·ln n ∧ step^[k] n = 1`, `Nat.count` over `n < X`, constant a rational with a separate theorem `0 < densityConstant`, cutoff a natural number. No vacuity, no hidden hypothesis, no weaker counting predicate.
6. Text scan of claim (1) source (386 files, 67,232 lines): zero hits for sorry/axiom/native_decide/unsafe/implemented_by/opaque/extern/admit, no macro/elab/notation/run_cmd/#eval, no shadowing of Mathlib names.
7. The "sublinear to linear" conversion is not a bootstrap from x^gamma. It is a first-moment (harmonic-mass) count on the inverse Syracuse tree of one seed M with S(M)=1: weighted mass >= eta at every scale X, each distinct source x carries weight <= M/x, so #sources in [X,32X) >= eta·X/M (paper Lemma 6.1). Mass is kept alive by Tao's fine-scale mixing (his Prop. 1.14) against a trivial residue-multiplicity bound.
8. Litmus: for 5n+1 the argument dies at the block growth step (needs E[a]·ln2 > ln q: 2 ln2 − ln3 = +0.288, 2 ln2 − ln5 = −0.223). For 3n−1 it goes through for each cycle separately and would give positive lower density for each basin, which matches numerics (0.327 / 0.324 / 0.349 below 2·10^6) and contradicts nothing. It does not give density one.
9. I read the paper's argument end to end and found no gap in the outline; I did NOT check the 61k-line Lean proof body nor the formalised proof of Tao's mixing with explicit constants.
10. Consequence for the repo if true: exponent 1 in the Krasikov–Lagarias counting problem; the whole x^gamma line (kl-exponent track) is superseded for target 1. H1 / Lemma E are untouched.

## (b) Artifacts obtained (all HTTP 200, client `collatz-fmf-research-audit/1.0`; robots.txt = `Allow: /`)

Base `https://www.proofatlas.ai`. Files in `dl/` (git-ignored).

| file | bytes | sha256 |
|---|---|---|
| `/papers/positive-density-log-time-collatz/Mazur_Explicit_Positive_Density_Collatz_Convergence_in_Logarithmic_Time_v2.pdf` (v2.1, 2026-09-06, 13 pp) | 186,494 | a7e8a0ad049bc1de16d67be5cb5c3b5890f85ee231bb079f4289c657753fb64a |
| `/papers/positive-density-log-time-collatz/positive-density-log-time-collatz-v2.1-source.zip` (has lakefile, toolchain, Verification/, evidence/) | 914,975 | 23f5cac4d66e696401144658752cf180a13ce70373a122f00693e1e1fe969c1f |
| `/sources/positive-density-log-time-collatz/commits/830b9d3f…/positive-density-log-time-collatz-checked-source-830b9d3f38f2.zip` | 807,472 | 5fb4af83a4ee002fcd692ce12e3e2766e56f9899a930440db22e74a00855f022 |
| `…/artifact.collatz.positive_density_log_time.lean-package.v003.evidence.json` | 107,270 | c486380ca735ad4b906c8ca3ee993ff84156b43d1b3cc51358b1fdf145406a07 |
| `/papers/collatz-predecessor-090/Mazur_Certified_x090_Lower_Bounds_for_Collatz_Predecessor_Sets_v2.pdf` | 170,031 | cbae5d71ead733b380c3325503e46a7094fb4641244853a37dc220207d133a61 |
| `/sources/collatz-predecessor-090/commits/5f76a170…/collatz_predecessor_090-1.0.0.tar.gz` (1.29 GB unpacked; `artifacts/` hex certificates NOT extracted) | 570,509,134 | bc59cf3067a9377dbc0d4fc32d2eb4f228051f65cf2f41087a0066ef7ddedc9b |
| `/papers/natural-density-log-time-collatz/Mazur_Natural_Density_Collatz_Orbits_in_Logarithmic_Time_v2.pdf` | 253,981 | 08a46dd1cdd9183beb2e09af517361f24d3b7945a6ee00db563a944a4a2373cf |
| `/sources/natural-density-log-time-collatz/commits/ca3dd0d6…/natural-density-log-time-collatz-checked-source-ca3dd0d63920.zip` | 1,984,188 | 5761e6bdad1284275f3a19aa51d8278a68b19cb569c516c20df956e6fac91864 |

Extracted to `src/posdens-paper`, `src/posdens-checked`, `src/natdens-checked`, `src/pred090` (no path traversal, no symlinks).
The 386 `.lean` files of the two claim-(1) archives are byte-identical (`diff -rq`: only metadata differs).

## (c) Claim (1): statement audit — READ-STATEMENT, status of "Lean statement = prose statement": VERIFIED by reading

Top file `CollatzPositiveDensity.lean` (34 lines), unfolded to Mathlib:

- `step n = if Even n then n/2 else 3*n+1` — the ordinary Collatz map on ℕ. No acceleration.
- `fastConvergent C n := 0 < n ∧ ∃ k:ℕ, (k:ℝ) ≤ C * Real.log (n:ℝ) ∧ step^[k] n = 1`.
- `countBelow C X := Nat.count (fastConvergent C) X` with the classical decidability instance, i.e. `#{n ∈ {0,…,X−1} : fastConvergent C n}` (strictly below X; 0 excluded by `0 < n`; n = 1 counted with k = 0).
- `densityConstant : ℚ := explicitPositiveDensityUnitSeedConstant = 3 / (256 · M̄ · 2^m)` with `M̄ = explicitOnePeriodSeedRootBound b N : ℕ` (proved `> 0`), `m = Nat.nthRoot 6 (88·M̄·C) + 1`, `b = 2^80`, `C` = explicit mixing coefficient. `theorem densityConstant_pos : 0 < densityConstant` (proof: `positivity` after unfolding). Cast ℚ→ℝ in the statement is the standard one.
- `cutoff : ℕ := 32 * (2^(E(J) + ⌊2β(J)/3⌋) · M̄ + 1)`; `theorem cutoff_pos`. A natural number, so `cutoff ≤ X` is satisfiable.
- `theorem positive_density (X:ℕ) (hX : cutoff ≤ X) : (densityConstant:ℝ) * X ≤ (countBelow (523/50) X : ℝ)`.

Ordinary mathematics: there are a rational c > 0 and a natural X0 such that for all naturals X ≥ X0,
`#{1 ≤ n < X : T^k(n) = 1 for some k ≤ 10.46·ln n} ≥ c·X`. This is Theorem 1.1 of the paper, and the constants match
paper eq. (8.6) `c = 3/(256 M̄ 2^m)`, `X0 = 32(2^B M̄ + 1)`.

Checks against the specific failure modes in the brief:
- Vacuity: none. Hypothesis is `cutoff ≤ X` with cutoff ∈ ℕ; constant is proved positive by a public theorem; no ℕ-subtraction or floor appears in the statement itself.
- Weaker counting predicate: no. The predicate contains `step^[k] n = 1` literally; internal set `rawCollatzLogTimeOneSet` (Erdos1135/ND/PositiveDensity/Statement.lean:25) has the same body with `collatzStep` = `CollatzConjecture.collatzStep` = same `if Even n …`.
- Not-Collatz step: no.
- Trivial witnesses: `Nat.count … X ≤ X` and the bound is `c·X`, so it is a genuine linear bound; powers of two give only log2 X. (Own Lean file `scripts/StatementSanity.lean`, compiled on local Lean 4.36/Mathlib: REBUILT for the vocabulary only.)
- Hidden hypotheses: the theorem has none besides `hX`; no `variable` lines in the top file; the internal chain discharges `Tao.syracFineScaleMixingAt 6 C` by `explicitSyracuseMixing_six` (a theorem, not an assumption).
- `Classical.choice`-defined constants: the constants are closed arithmetic recipes (`Nat.nthRoot`, `Nat.clog`, recursions), not `Classical.choose`. (Not that it would matter for truth: positivity is proved.)
- The vendored `FormalConjectures/Wikipedia/CollatzConjecture.lean` in claim (1) contains only `def collatzStep`; the sorry-stated conjecture has been removed there (it is present in claim (3)'s tree, see (f)).

Caveats stated by the authors and confirmed: c and X0 are astronomically small/large (M̄ ~ 4^(2b+1+3^q) with b = 2^80); no density-one claim; the paper is unrefereed, AI-generated (OpenAI Codex), "publication review pending".

## (d) Grep for unsound constructs (word-boundary regex `sorry|axiom|native_decide|unsafe|implemented_by|opaque|extern|admit|sorryAx|ofReduceBool|trustCompiler|partial|debug.skipKernelTC`)

Claim (1), both archives, all 386 (+3 Verification) files: **0 hits**. Also 0 hits for `macro|elab|syntax|notation|run_cmd|#eval|initialize|csimp|_root_` in the proof library (`run_cmd` occurs only in the three `Verification/*.lean` audit files, which I did not run). 3 `local instance … Decidable … := Classical.propDecidable` (harmless).

Claim (3) `src/natdens-checked` (599 files, 195,215 lines):
- `FormalConjectures/Wikipedia/CollatzConjecture.lean:55: sorry` — the proof of `theorem collatz_conjecture (n) (hn : n > 0) : ∃ m, collatzStep^[m] n = 1`. **A sorry-"proved" full Collatz conjecture is in the import closure.** `grep -rw collatz_conjecture` finds no other mention in the tree, so it is textually unused; only a real `#print axioms` (not rerun) can exclude use via automation.
- remaining hits are prose in comments ("opaque", "partial", "not an axiom"): PhaseGap.lean:39, Band/A5TerminalAtomReconstruction.lean:398, Tao/Section3/AmbientPartialTrace.lean:252,269, Tao/Section3/TimeBoundedAmbientTrace.lean:85,102, Tao/Section6/Prop117ToProp114.lean:21, Tao/Renewal/Lemma77FirstPassageEndpoint.lean:50, Tao/Renewal/SourceRegeneration.lean:237, Tao/Renewal/Lemma77KernelTail.lean:134, Tao/Fourier/DecayStatement.lean:87, Tao/Renewal/Prop78Case3Stopping.lean:6034, Tao/Renewal/Prop78Case3EventualScale.lean:57.

Claim (2) `src/pred090/collatz_predecessor_090-1.0.0` (64 files, 12,036 lines):
- `sorry`: Challenge.lean:44,50,57 and ComparatorChallenge.lean:28,34,41 (statement-only comparator files, by design; not imported by the proof).
- `native_decide` (17): Erdos1135/KrasikovLagarias/ChunkedEncoding.lean:61,65,69,73; EncodedCertificate.lean:54,58; Generated/K18AdaptiveForcedPotential.lean:23,27; AdaptiveForcedPotentialCertificate.lean:227; ForcedPotentialCertificate.lean:232,238,247,256; Generated/K18Gamma901.lean:41,45. ASSUMPTIONS.md says exactly two are in the public cone (`k18Gamma901EncodedCertificate_check`, `k18AdaptiveForcedPotentialCertificate_check`): PAGE-ASSERTS.

## (e) Rebuild — NOT DONE (blocked by version pin)

- Pin: `lean-toolchain = leanprover/lean4:v4.30.0-rc2`, Mathlib rev `5450b53e5ddc75d46418fabb605edbf36bd0beb6` (claims 1, 3), `v4.30.0-rc2` (claim 2). Local: Lean 4.36.0 / Mathlib v4.36.0. Different rev, so no fetch.
- Opportunistic attempt (no network, cache read-only): `scripts/mkbuild.py` + `scripts/run_build.sh` compile the 386 modules by direct `lean -o` against the local v4.36.0 oleans. Result: 47 attempted, 43 OK, 4 FAIL, the rest blocked downstream. Failures are library drift, not proof holes: `Tao/Probability/CountableMarkov.lean:106` unknown `mul_le_mul_left'`; `Tao/Probability/Geom.lean:11` unknown `ProbabilityTheory.geometricPMF`; `Tao/Fourier/Section7Geometry.lean:1352` and `Tao/Renewal/SeparatedWindowFlattening.lean:52` simp-normal-form mismatches. Porting 61k lines across six Mathlib releases was out of scope.
- The shipped `evidence/axioms.log` lists `[propext, Classical.choice, Quot.sound]` for all four roots: PAGE-ASSERTS. The README itself says the recorded build was "serial direct Lean compilation … did not … run an independent leanchecker, or claim a Lake-orchestrated build".

## (f) Mathematical audit of claim (1) — READ-PROOF (paper, all 13 pages; Lean only at the endpoint)

Notation: S Syracuse map; an inverse history from an odd R with valuation word w=(a_1..a_d) has source x with
Φ_w(x) = R and weight ω(w) = 3^d·2^(−A(w)); ρ_q = (2/3)·3^q·μ_q with μ_q Tao's Syracuse law on Z/3^q.

**The conversion step (paper Lemma 6.1 + Prop. 6.3; Lean `explicit_count_ten46_from_supplied_margin_and_reference_height`, ExplicitSeedToCount.lean).**
> Lemma (source charge). Let M > 1 be odd with S(M) = 1, and let 𝒮 be a set of distinct odd integers in [X, 32X) each carrying one history to M. Then Σ_{x∈𝒮} ω(x) ≤ (M/X)·#𝒮. Hence if the total selected weight U_{n,X} ≥ η for every large X, then #{x < 32X reaching 1} ≥ ηX/M.

Proof is two lines: M = ω·x + β with β > 0 gives ω < M/x ≤ M/X; uniqueness of the history because the orbit of x meets the non-periodic M once and every block cut is a first-crossing time. STATUS: PROVED (elementary; I re-derived it). So the linear bound is not extracted from x^γ information; the whole content is the *lower bound η > 0 on harmonic mass, uniformly in X*.

**Where η > 0 comes from (the real crux), in order:**
1. (Prop. 4.2 / §8.3) On Z/3^q the N-generation pulled-back mass, as a function of the endpoint residue, has mean exactly (2/3)·Π p_j ≥ (2/3)(255/256) (Lemma 2.1, exact; NUMERIC-EXACT check of Lemma 2.1 on 200 random words). So some unit class has mass ≥ 255/256.
2. (Lemma 4.1) M_v = (4^v − 1)/3 has S(M_v)=1 and runs through all classes mod 3^q with period 3^q (v_3(4^a−1) = 1+v_3(a)). NUMERIC-EXACT for q ≤ 7. Pick the seed in the good class. **This is where "+1" and "target 1" enter.**
3. (Prop. 3.1, uniform variation) |Z_{n+1}(M) − Z_n(M)| ≤ E_n, summable, independent of M: an L^∞×L^1 pairing of
   (i) the endpoint residue histogram, bounded by a *trivial* count — endpoints with fixed (depth, valuation sum) lie in an interval of length 2^(b0+1)/W, so a class mod 3^q holds ≤ that/3^q + 1 of them (eq. 3.9); loss factor poly(n)·(2013/2000)^n·16^b0;
   (ii) Tao's fine-scale mixing ⟨|ρ_q − ρ_m∘π|⟩ ≤ C_A m^(−A) with A = 6 at m ≈ b_n/4, b_n ≥ b0(201/200)^n.
   Summability is q1 = (2013/2000)(200/201)^6 ≈ 0.977 < 1 and q2 = (2013/2000)·2^(−1/100) ≈ 0.9996 < 1. I re-derived (3.9) and both ratios; they are correct. **The only deep input is Tao's Prop. 1.14**, which the Lean development claims to prove with explicit constants (not checked by me).
4. (Prop. 5.3) removal of the ρ-weight at a fixed modulus 3^m, m^6 ≥ 88·M̄·C, again L^∞×L^1 using the source-charge bound for the histogram.
5. (§7) clock: κ = 3.4881 Syracuse steps per ln x, then κ(L+h)+1 ≤ (523/50)L. NUMERIC (50 digits): margins +1.99e-4 for (7.9) and +2.9e-5 for (7.8); the constant is 10.4597 against the typical clock 3/ln(4/3) = 10.4282, so 10.46 is "just above typical", as it must be.

**Where 3 enters.** Blocks are first crossings of A ≈ 2d (the *mean* of the geometric valuation law), and the inverse block multiplies the endpoint by ≈ 4^b/3^b (eq. 3.5). Growth needs 2·ln2 > ln3. For qn+1 with q ≥ 5 the mean drift is 2ln2 − ln q < 0: a growing inverse history needs A/d > log2 q, an exponentially rare event under 2^(−A), so p_j → 0 exponentially, Π p_j = 0 and step 1 gives mass 0. The seed lemma (step 2) *does* transfer to 5n+1 ((16^j−1)/5 covers all classes mod 5^q, NUMERIC-EXACT q ≤ 5), so step 2 is not the 3-specific step; the drift is.

**Litmus results.**
- 5n+1: argument fails at (3.5)/(3.6) as above. NUMERIC: #{n<X reaching 1} = 81, 256, 982, 4324 at X = 10^3..10^6 (escape cap 2^61), local exponents 0.50, 0.58, 0.64: sublinear, consistent.
- 3n−1: drift is the same +0.288, mixing transfers by y ↦ −y, seeds (2·4^j+1)/3 cover all classes mod 3^q (NUMERIC-EXACT q ≤ 7), and the same works with seeds chosen among predecessors of 5 or of 17. So the argument gives positive lower density for each of the three basins and never density one for any. NUMERIC below 2·10^6: basins 0.3273 / 0.3240 / 0.3487. No contradiction; the argument is correctly "cycle-agnostic".
- Positivity: histories are positive integers by construction ((2^a R − 1)/3 > 0); a negative target such as −1, −5, −17 is unreachable from positive sources, so nothing false is produced.
- 3n+1 itself, NUMERIC: fraction of n < X with τ(n) ≤ 10.46 ln n is 0.5630, 0.5535, 0.5422, 0.5411, 0.5411 at X = 10^4, 10^5, 10^6, 10^7, 3·10^7 (linear, as claimed; says nothing about X ≥ X0).

**Hostile-referee residue (what could still be wrong).** (i) I did not verify that the Lean proof body compiles; (ii) the explicit-constant version of Tao's Prop. 1.14 (C built from A*=6409, E*=2170 …) is asserted in §8.1 with the proof only in Lean; the qualitative theorem needs only some finite C_6, which is Tao's published result; (iii) the paper's §3 first-crossing/overshoot bookkeeping (3.6), Prop. 5.2 and Lemma 6.2 were read but not independently re-derived line by line; (iv) PDF text extraction dropped superscripts/overlines, so a few formulas were read through the Lean definitions instead.

## (g) Claims (2) and (3) — short verdicts

**(2) Predecessor exponent 0.90.** READ-STATEMENT. `CollatzPredecessor090.predecessor_count_lower_bound_090 {target} (0 < target) (target % 3 ≠ 0) : ∀ᶠ x in atTop, x^(9/10) ≤ predecessorCountReal target x`, with `accelerated n = if Even n then n/2 else (3n+1)/2`, `Reaches s t := ∃ k, accelerated^[k] s = t`, count over `Finset.Icc 1 ⌊x⌋₊`. Also `_0901`: ∃ c > 0, eventually c·x^0.901 ≤ count. Matches the prose. Not kernel-clean: two `native_decide` checks over 129,140,163 LP rows and 215,233,605 potential inequalities (disclosed; classification `NATIVE_ASSISTED`). Not rebuilt (pin v4.30.0-rc2; 1.29 GB of hex certificates not even extracted). The page's "improves the earlier 0.88" vs "2003 benchmark 0.84" inconsistency noted in ai-math-methods.md was not resolved. If claim (1) holds, (2) is superseded for target 1 but not for general targets.

**(3) Natural-density log-time descent.** READ-STATEMENT. `ndRhinLogTimePaperPackage` (Erdos1135/ND/LogTime/Paper.lean) has no hypotheses and includes `ND13LogTimeStatement ndCollatzLogTimeConstant`: for every f : ℕ→ℝ with f → ∞, the set {N > 0 : ∃ m, m ≤ C·ln N ∧ Col^m(N) < f(N)} has natural density 1 (`Tendsto (count(n<N)/N) → 1`), C = 1509503/(5000 ln 2) < 436; the odd/Syracuse form has clock 501501/(5000 ln 2) < 145 and relative density one among odds (density 1/2 of {odd ∧ good}). Rate exponent 6993/200000 < 5/143. Matches the prose. One `sorry` in the tree (the unused Collatz conjecture statement, see (d)). Not rebuilt.

## (h) Scripts (all own code, in `scripts/`)

- `taskset -c 0-1 /home/matrix/home/projects/collatz/venv/bin/python scripts/numeric_checks.py` — expected output saved in `scripts/numeric_checks.out` (≈2 min). Sections 2–4 exact, 1/5/6 floating/exploratory.
- `python -I scripts/pdf2txt.py dl/<paper>.pdf txt/<name>.txt` — text extraction (pypdf).
- `python -I scripts/mkbuild.py <src> <out> CollatzPositiveDensity > build/posdens/Makefile; scripts/run_build.sh $PWD/build/posdens` — the failed v4.36.0 compile attempt; expected: `FAIL` on the four modules named in (e).
- `scripts/StatementSanity.lean` — compiles clean on local Lean 4.36.0/Mathlib (no output, exit 0).

## (i) Dead ends

- Building claim (1) against Mathlib v4.36.0: fails on renamed/removed lemmas (`mul_le_mul_left'`, `ProbabilityTheory.geometricPMF`) and simp-normal-form changes within the first 47 modules. Do not retry without the pinned toolchain.
- Looking for a "sublinear ⇒ linear" bootstrap to attack: there is none; the proof never uses the x^0.90 result (the paper says so and the import graph of the endpoint confirms it does not import `KrasikovLagarias`).
- Trying to break the argument with 5n+1 via the seed lemma: the seed lemma is true for 5n+1 too; the failure is the drift sign, not the seeds.

## (j) Best lead for a follow-up agent

Decisive and cheap: **rebuild claim (1) on the pinned toolchain** (needs owner approval to fetch Lean v4.30.0-rc2 + the Mathlib `5450b53e` olean cache, ≈6–7 GB), run `#print axioms CollatzPositiveDensity.positive_density` and `lean4checker`, and compile an independently written statement against it. That turns 0.85 into ≈0.99 or into a refutation.

Mathematical lead, stated as a lemma to prove or kill by hand (it is the only non-elementary step, and is independent of Lean):
> **Lemma (uniform variation, Mazur Prop. 3.1).** Let b_0 ≥ 325, b_{j+1} = b_j + ⌊b_j/100⌋, k_n = ⌊b_n/4⌋, and for odd M ≥ 16^{b_0} let Z_n(M) = Σ_h ω(h)·ρ_{k_n}(R_h mod 3^{k_n}) over generation-n central first-crossing histories h from M with endpoint R_h. Then |Z_{n+1}(M) − Z_n(M)| ≤ C_{b_0}(n+1)^3 (q_1^n + q_2^n) with q_1, q_2 < 1 and C_{b_0} independent of M, given only Tao's bound Osc_{m,q}(μ_q) ≤ C_6 m^{−6}.

If this lemma is right (I believe so, having re-derived the multiplicity bound (3.9) and the ratios), positive lower density of {n : n → 1} follows by the elementary steps 1, 2, 4 and the source-charge lemma, and the same proof gives positive lower density of the predecessor set of every target a with 3 ∤ a. For this repo the corollary is that a density-one statement for "reaches 1" is now the wall, and FMF-side effort on x^γ exponents has no remaining value for target 1.

## Rebuild (2026-11-18)

Verdict: **REBUILT — axioms: [propext, Classical.choice, Quot.sound]** for claim (1). Supersedes item 4 of (a) and section (e) for claim (1): "build passes, standard axioms only" is now REBUILT here, no longer PAGE-ASSERTS. Claims (2), (3) remain not rebuilt.

**Setup.** Build copy `build/posdens-rebuild/` = `CollatzPositiveDensity.lean`, `Erdos1135/`, `FormalConjectures/`, `lakefile.toml`, `lake-manifest.json`, `lean-toolchain` copied from `src/posdens-paper/positive-density-log-time-collatz/` (v2.1 paper archive; the commit archive `posdens-checked` ships no lakefile). Not copied and not run: `Verification/` (its `run_cmd` blocks write files via `IO.FS.writeFile`; it is a non-default lake target) and `scripts/`. Pre-build scan of lakefile + 386 built `.lean` files for `IO.Process|run_cmd|extern|moreLinkArgs|initialize|#eval|IO.FS|script|unsafe|implemented_by|macro|elab|syntax|plugin|dynlib`: 0 hits; lakefile is plain TOML (one `require`, four `lean_lib`, no scripts/targets/link args).
- Pin: Lean `leanprover/lean4:v4.30.0-rc2` (`lean --version`: commit `3dc1a088b6d2…`); Mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` (`git rev-parse HEAD` in `.lake/packages/mathlib` confirms; manifest unchanged by the build).
- `lake exe cache get`: 8297/8297 files downloaded and decompressed, no errors. Mathlib was not compiled from source (0 `Built Mathlib…` lines).
- `taskset -c 0-1 lake build` (`LEAN_NUM_THREADS=2`): `Build completed successfully (3949 jobs).` All 386 project modules (67,232 lines) built; 0 errors, 0 `sorry` warnings; 35 files with linter/deprecation warnings only (unused simp args, `<;>` style, deprecated `mul_le_mul_left'`). Wall time 28 min 40 s (20:15:15Z to 20:43:55Z). Disk: 8.2 GB build dir (7.1 GB Mathlib packages+cache) + 2.6 GB toolchain in `~/.elan`; 32 GB free afterwards. Logs: `build/posdens-rebuild/build.log` (sha256 `b84d57f7…`), `cache.log`.

**Axioms, printed here** (`lake env lean RebuildAxioms.lean`, source in `scripts/RebuildAxioms.lean`, output `build/posdens-rebuild/axioms.out`), verbatim:
```
positive_density : ∀ (X : ℕ), cutoff ≤ X → ↑densityConstant * ↑X ≤ ↑(countBelow (523 / 50) X)
theorem CollatzPositiveDensity.positive_density : ∀ (X : ℕ),
  cutoff ≤ X → ↑densityConstant * ↑X ≤ ↑(countBelow (523 / 50) X) :=
fun X hX => Erdos1135.ND.PositiveDensity.explicitPositiveDensityUnitSeedCount_ten46 X hX
def CollatzPositiveDensity.step : ℕ → ℕ :=
fun n => if Even n then n / 2 else 3 * n + 1
def CollatzPositiveDensity.fastConvergent : ℝ → ℕ → Prop :=
fun C n => 0 < n ∧ ∃ k, ↑k ≤ C * Real.log ↑n ∧ step^[k] n = 1
def CollatzPositiveDensity.countBelow : ℝ → ℕ → ℕ :=
fun C X => Nat.count (fastConvergent C) X
def CollatzPositiveDensity.densityConstant : ℚ :=
Erdos1135.ND.PositiveDensity.explicitPositiveDensityUnitSeedConstant
def CollatzPositiveDensity.cutoff : ℕ :=
Erdos1135.ND.PositiveDensity.explicitPositiveDensityUnitSeedCutoff
densityConstant_pos : 0 < densityConstant
cutoff_pos : 0 < cutoff
'CollatzPositiveDensity.positive_density' depends on axioms: [propext, Classical.choice, Quot.sound]
'CollatzPositiveDensity.densityConstant_pos' depends on axioms: [propext, Classical.choice, Quot.sound]
'CollatzPositiveDensity.cutoff_pos' depends on axioms: [propext, Classical.choice, Quot.sound]
'CollatzPositiveDensity.positive_density_ten48' depends on axioms: [propext, Classical.choice, Quot.sound]
'rebuild_restatement' depends on axioms: [propext, Classical.choice, Quot.sound]
```
No `sorryAx`, no `Lean.ofReduceBool`, no custom axioms.

**Independent restatement (own code, compiled against the built library).** `rebuild_restatement` in `scripts/RebuildAxioms.lean` states, in Mathlib vocabulary only (step written as `if m % 2 = 0 then m / 2 else 3 * m + 1`, no project definitions in the statement): `∃ c : ℝ, 0 < c ∧ ∃ X₀ : ℕ, ∀ X ≥ X₀, c * X ≤ Nat.count (fun n => 0 < n ∧ ∃ k : ℕ, (k:ℝ) ≤ (523/50) * Real.log n ∧ step^[k] n = 1) X`. It is derived from `positive_density` + `densityConstant_pos` and type-checks with the same three axioms.

**Source identity.** `CollatzPositiveDensity.lean` sha256 `0670b896862f7b8a289c1e41e073ad250fd1898b5b27f6f98232e1ecb29a042a` in the build copy, in `src/posdens-paper` and in `src/posdens-checked` (`cmp` identical); `diff -rq` of `Erdos1135/` and `FormalConjectures/` between build copy and `src/posdens-checked`: no differences. The earlier audit did not record a per-file hash; identity is to the same extracted trees it read (archive hashes in (b)).

**What it asserts.** There are an explicit rational c > 0 and natural X0 such that for every natural X ≥ X0, at least c·X of the integers 1 ≤ n < X reach 1 under the ordinary Collatz map (n/2 for even n, 3n+1 for odd n, no acceleration) within k ≤ 10.46·ln n steps. That is positive lower density of fast-converging starting values; it is not density one and not the Collatz conjecture, and c, X0 are astronomically small/large.

**Step 6 (predecessor exponent 0.90): SKIPPED, not rebuilt.** Same pins (Lean v4.30.0-rc2, manifest Mathlib `5450b53e…`), but the archive's own `REPRODUCIBILITY.md` gives peak RSS about 10.6 GiB and 9.3 GiB for the two `native_decide` certificate modules (19.5 + 14.6 min on their machine), above this run's 5 GB RAM budget; it also needs the 1.29 GB `artifacts/` hex chunks extracted (`include_str`). Its axiom list (expected to include `Lean.ofReduceBool`) stays PAGE-ASSERTS.

**Still unchecked.** (i) No `lean4checker`/external kernel replay of the produced oleans; the result rests on the Lean 4.30.0-rc2 kernel as run by `lake build`, on a release-candidate toolchain, and on the downloaded Mathlib olean cache being honest for that revision (Mathlib itself not recompiled). (ii) The 67k-line proof body was machine-checked, not read. (iii) Claims (2), (3) not rebuilt. (iv) `Verification/*.lean` from the archive not run (own axiom file used instead).
