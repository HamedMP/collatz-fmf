# Round 6 — approach-family registry and do-not-repeat ledger

Written by the coordinator, 2026-11-17, after the first wave. For second-wave
agents: these routes are BLOCKED. Do not re-run one unless you bring a
materially new mechanism, and say what it is. Sources: `plan.md` lines 301–709
(July rounds), `STATE.md` "Dead ends", and the first-wave track reports
(`<track>/REPORT.md` in this directory).

Standing facts
- Collatz ⇔ H1 ∧ Lemma E (kernel-checked in `lean/CollatzFMF/TheoremR.lean`).
  A reduction of Collatz to H1, to Lemma E, or to anything equivalent to either
  counts as FAILURE, not progress.
- H1, single-coordinate form: no positive integer w has an infinite itinerary
  under a: w → (9w+1)/8 (w ≡ 7 mod 8), b: w → 27w/16 (16 | w). (H1 proper only
  needs w ≡ 32 mod 33.) Equivalently no positive integer has Collatz parity
  sequence in {110, 1110}^ω.
- Verified computationally by others: all n < 2^71 reach 1 (Barina).
- Claimed by others, Lean-built, not independently rebuilt: positive lower
  natural density of n reaching 1 (Mazur, Sept 2026); natural-density Tao
  (Allikvere, Mazur, July 2026); predecessor exponent 0.90–0.925.

| # | Family | Status | Why blocked / what it gives |
|---|---|---|---|
| 1 | Finite-modulus certificates, any horizon | BLOCKED (proved) | Uncertified frontier grows ~1.93^n; uncertified tree is a Cantor set |
| 2 | 2-adic transfer operator / spectral | BLOCKED (proved) | Operator data is multiplier-blind; a.e. is optimal on Z_2 |
| 3 | Class counting, translate-invariant rank counting | BLOCKED (proved) | Saturates; seed count exponent 0.2878 is optimal (Thms 48/57) |
| 4 | Two-prime (2-adic + 3-adic) pincer | BLOCKED (proved vacuous) | Mirror Equivalence: both sides carry the same information |
| 5 | Statistical forms of Lemma E; complexity pincers; re-chunking FM2^k | BLOCKED | See plan.md |
| 6 | Baker / archimedean bounds on cycles-like coincidences | BLOCKED | Wrong metric; equally valid for 5n+1 which has cycles |
| 7 | Same-factor repetition barrier (factor recurrence ⇒ size bound) | EXHAUSTED | Frontier Thms A/B: excludes all two-block words and binary morphic words; fails on an explicit 4-letter morphic word (Obstruction O: yields only w₀ > 2^62). Open only: 3-letter case ("Lemma T") |
| 8 | S-unit / Subspace theorem on fixed-length windows | EXHAUSTED | Sunit Thms A–F: finiteness for fixed window length, ineffective, not uniform in length (false uniformly), vacuous for bounded alphabets, transfers to 5n+1 and 3n−1 |
| 9 | Subspace theorem on periodic approximants | BLOCKED | Reproduces the same-factor bound |
| 10 | Modular invariants of the return map | BLOCKED (proved) | Only invariant is w ≡ −1 mod 11 (Frontier Prop. D) |
| 11 | Seed gap principle | BLOCKED | Equals the optimal seed count |
| 12 | Krasikov–Lagarias LP at larger k; non-periodic weights | BLOCKED | Others at k = 22; 2-adic/size features give no gain (Prop. N); possibly superseded by positive density |
| 13 | Stopping-time lower bounds (Applegate–Lagarias trees, sliding-window game) | BLOCKED | Amano has 1/2; game stalls at 0.46; tree statement only, sign-blind |
| 14 | SAT/matrix-interpretation termination of rewriting systems | BLOCKED at feasible sizes (`srs-termination/REPORT.md`) | Dimension ≤ 3 interpretations see only the 2-adic valuation of the represented number; cannot even find Lemma P outside an adapted coordinate; open systems and non-terminating controls have the same UNSAT frontier. Open: one-rule relative termination in system W |
| 15 | Carry-free neighbours (F_2[x]) | NEIGHBOUR ONLY | Truncation monotonicity fails on integers (σ(27)=70, σ(59)=22) |
| 16 | 3-smooth representation counting | BLOCKED | Identical for 5n+1 at the surjectivity level; counting form is family 12 |
| 17 | Tao-style statistical mixing → natural density | DONE BY OTHERS | Gives density statements, never "every n" |

Mandatory controls for any new argument: 5n+1 (cycle 13→33→83, believed
divergent orbits), 3n−1 (cycles through 1, 5, 17), 3n+d (many cycles). State
where 3, +1 and positivity enter. An argument that never uses them is wrong.

## Added after the second wave (2026-11-17, late)

| # | Family | Status | Why blocked / what it gives |
|---|---|---|---|
| 18 | ×2×3 rigidity / Furstenberg intersections applied to H1 | BLOCKED (w2-alpha, refereed) | Digit-reading hulls of the H1 Cantor set E are all of [0,1]; every reflection-invariant datum is shared with −E (the 3n−1 system), which contains 1. Open lemma FP-0 only |
| 19 | Fourier decay of the natural measure on E | BLOCKED | Needs ternary digits of 2^(−j) mod 3^J with j ≍ J (Erdős regime) |
| 20 | Density bootstrap (almost-all-small + positive proportion ⇒ more) | BLOCKED (w2-beta, refereed) | The bootstrap map is the identity; under positive-density predecessor sets, density one ⇔ Collatz |
| 21 | Structured 2-adic seeds for divergence / long glides | REFUTED (w2-gamma) | 1–4 steps per bit against 14–18 for records |
| 22 | Arguments using only parity-prefix property + T below a bound + T mod 2^a | BLOCKED (w2-gamma Thms S, B, A, refereed) | Control maps S_a, cycle implants and isometric conjugates satisfy all of these and have cycles / divergent orbits |
| 23 | Injective charging along one trajectory (Terras bijection, 3 < 4) | DONE (w2-delta Thm H; Lean with constant 1196) | Gives uniform Σ 1/x_k bound, sojourn exponent 0.94996, bounded residue. True for 3n−1 too: cannot give descent. Lowering 0.94996 needs lemma G2 |

Mandatory controls, extended: 5n+1, 3n−1, 3n+d, **and S_a for every a ≥ 0**
(S_a = T except T − 2^a on n ≡ −1 mod 2^(a+1); fixed point 2^(a+1) − 1;
S_0 is 3n−1). A correct proof of "no nontrivial cycle" must use
n < T(n) at n = 2^(a+1) − 1 for every a.

## Added after the third wave (2026-11-18)

| # | Family | Status | Why blocked / what it gives |
|---|---|---|---|
| 19′ | Fourier decay of the H1 Cantor set (update of 19) | PARTLY DONE (w3-fp0, refereed) | Polynomial-in-K decay at fixed frequency and a (log X)^(−0.0512) saving on the seed count are proved; POWER decay / FP-0 needs square-root cancellation over ~√k consecutive powers of 3 (Erdős regime) |
| 24 | Second-generation large deviations (lemma G2) via Tao's Section 7 at a tilted parameter | BLOCKED (w3-g2, refereed) | The required tilt is the critical boundary q* excluded by Theorem 56; black triangles can cover the diagonal; 2-adic Baker gives only log n/log log n scales. Log-power sojourn saving proved by a ballot argument instead |
| 25 | Machine-checked controls | DONE (Lean) | Rigidity of T and the S_a family are kernel-checked; use them to test any "no cycles" argument |

Common wall of families 18, 19, 24: digits of 2^(−j) mod 3^J with j ≍ J.

## Added after the fourth and fifth waves (2026-11-18)

| # | Family | Status | Why blocked / what it gives |
|---|---|---|---|
| 26 | All-trajectory size tools (harmonic bound, residue, sojourn) applied to Lemma E | BLOCKED (w4-E) | They only forbid lingering; the 5n+1 orbit of 7 satisfies their conclusions with generic hop letters. Statements are prior art (Nikzad–Frinkle–Bagherzadeh 2026; García–Tal 1999) |
| 27 | Short exponential sums of 3^i mod 2^k (Korobov–Vinogradov) for the digit wall | BLOCKED (w4-wall, refereed) | Published range R ≥ exp(c k^(2/3)) with saving exponent 10^(−11); pair method capped at K^(−1/8). Gave only 0.0719 → 0.0913 |
| 28 | Pointwise power Fourier decay of the H1 Cantor set (PFD) | OPEN, the precise wall (w5-fourier) | PFD for integers |h| ≤ N^δ ⇒ FP-0 (proved). PFD ⇐ no long equal-bit runs in 3^(−p) at heights ≥ 4p/3 (Lemma R). Explicit affine self-similar measures: only (poly)log decay is known in the literature |
| 29 | Time-L return map F(x) = T^⌊log₂x⌋(x); mantissa rotation; real-vs-2-adic series; rigidity-based potentials; nonstandard models | BLOCKED (w4-free) | Two bad F-steps = lemma G2; mantissa law is control-blind; series encodes size only; S_a differs from T at one far-out point |

Process rule added: run a prior-art search (preprint servers and forums
directly: Hexagon, Zenodo, rStation, StackExchange API, GitHub; not just web
search) BEFORE refereeing or formalizing a result.
