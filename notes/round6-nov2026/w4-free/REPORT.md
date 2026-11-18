<!-- Saved by the coordinator from the w4-free agent's final message (the agent's own write was refused). -->
# FULL REPORT — w4-free, round 6 (2026-11-18)

Nothing here proves Collatz, H1 or Lemma E. No `exploreXX.py` script was run, and `plan.md` / `proof.md` were not touched (track rule: write only in this directory).

Notation: T(n) = n/2 (n even), (3n+1)/2 (n odd); λ = log₂3; L(x) = ⌊log₂x⌋ ("level"); **F(x) = T^L(x)(x)**; a(x) = number of odd terms among x, Tx, …, T^(L−1)x. A "distinct stretch" is a run of consecutive, pairwise distinct terms of a T-trajectory.

## (a) Summary

1. Two small unconditional results are proved; three approaches end in precisely stated obstructions; none gives a route to the conjecture.
2. Theorem B: perturbed-rotation / uniform Benford law for every n (bases 2 and 3), with explicit discrepancy.
3. Theorem B is a size statement and holds on every control map.
4. F-map lemmas F1–F5: exact structure of the Terras-horizon return map; F has only the fixed point 1.
5. Generation counts for L ≤ 33: independence holds for 5 generations; deeper deviations are explained by coalescence.
6. Seed (ii) reduces to G2 (Erdős regime); a deterministic streak bound is the Lagarias–Weiss conjecture.
7. Seed (iii): the real series carries size only; Ridout sits on its boundary.
8. Seeds (i) and (iv) are discarded with reasons.
9. 16 ideas brainstormed, 3 executed.
10. The candidate lead "Lemma C" was tested and killed.

## (b) Statements and proofs

### B. Perturbed rotation and a Benford law along every trajectory

Let o₀, …, o_(N−1) be the odd terms of a distinct stretch, tᵢ = {log₂ oᵢ}, ηᵢ = Σ_(j<i) log₂(1 + 1/(3o_j)).

**B1 (PROVED, exact).** tᵢ = {t₀ + iλ + ηᵢ}. For all terms: {log₃ x_k} = {log₃ x₀ − k·log₃2 + η′_k}, η′_k = Σ_(j<k, x_j odd) log₃(1 + 1/(3x_j)).

Proof. o_(i+1) = (3oᵢ+1)/2^d with d ≥ 1 an integer, so log₂ o_(i+1) = log₂ oᵢ + λ + log₂(1 + 1/(3oᵢ)) − d. In base 3, log₃ T(x) = log₃ x − log₃2 + [x odd]·(1 + log₃(1 + 1/(3x))). ∎

**B2 (PROVED).** η is nondecreasing and 0 ≤ ηᵢ ≤ V, where V can be any of:
- V_el(N) = (1 + ½ln(2N−1))/(3 ln 2). Elementary: the o_j are distinct odd positive integers, so Σ1/o_j ≤ 1 + ½ln(2N−1).
- log₂7.62 < 2.931 (Theorem 70, refereed constant), or 54/ln 2 < 78 (kernel-checked constant).
- The actual value. It was observed to be 0.15–0.32 on every tested trajectory reaching 1.

**Lemma R (PROVED).** If p/q is a convergent of λ, then for every α and every arc J of ℝ/ℤ, |#{0 ≤ j < q : {α+jλ} ∈ J} − q|J|| ≤ 2.

Proof. θ = λ − p/q has |θ| < 1/q². The points α + jp/q are q equally spaced points, and an arc of length ℓ holds between ⌊qℓ⌋ and ⌈qℓ⌉ of them. The true points are these shifted by jθ, all in one direction, each by less than 1/q. Say θ > 0. A true point in [u, w) comes from an equally spaced point in (u − 1/q, w), so the count is ≤ qℓ + 2. An equally spaced point in [u, w − 1/q) gives a true point in [u, w), so the count is ≥ qℓ − 2. ∎

**Lemma O (PROVED).** Let λ = [1; 1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, 55, …] with convergent denominators qᵢ = 1, 1, 2, 5, 12, 41, 53, 306, 665, 15601, 31867, 79335, 111202, 190537, 10590737, …. For q_m ≤ M < q_(m+1) put S(M) = a₁ + … + a_(m+1). Then for every α and arc J, |#{j < M : {α+jλ} ∈ J} − M|J|| ≤ 2S(M).

Proof. Greedy division M = b_m q_m + r, r = b_(m−1) q_(m−1) + …, gives digits bᵢ ≤ a_(i+1), and it terminates because q₀ = 1. Cut the index range into Σbᵢ blocks of consecutive indices of lengths qᵢ. Each block is a rotation orbit with a shifted α; apply Lemma R to each. ∎

Certified values (400-digit arithmetic, |λ − pᵢ/qᵢ| < 1/(qᵢq_(i+1)) checked for i < 100):

| N | 10³ | 10⁴ | 10⁵ | 10⁶ | 10⁹ | 10¹² | 10²⁰ | 10³⁰ |
|---|---|---|---|---|---|---|---|---|
| S(N) | 40 | 40 | 45 | 101 | 126 | 150 | 219 | 392 |

**Theorem B (PROVED).** Let D_N = sup over arcs J of |#{i < N : tᵢ ∈ J}/N − |J||. For every δ ∈ (0, 1]:

  N·D_N ≤ Nδ + (⌊V/δ⌋ + 1)·2S(N), hence D_N ≤ √(8·S(N)·V/N) + 2S(N)/N.

The same holds for {log₃ x_k} over all K terms, with the S-function of log₃2 and V ≤ log₃7.62 < 1.85.

Proof. η is monotone with values in [0, V], so the sets I_j = {i : ηᵢ ∈ [jδ, (j+1)δ)}, 0 ≤ j ≤ ⌊V/δ⌋, are index intervals. On one of size M write ηᵢ = h + εᵢ with 0 ≤ εᵢ < δ. For J = [u, w) of length ℓ:
- tᵢ ∈ J forces {t₀+iλ} into the arc (u−h−δ, w−h) of length ℓ + δ;
- {t₀+iλ} ∈ [u−h, w−h−δ) forces tᵢ ∈ J.

By Lemma O (trivially if ℓ + δ ≥ 1 or ℓ ≤ δ) the count on I_j is within Mδ + 2S(N) of Mℓ. Sum over j and take δ = √(2S(N)V/N). ∎

**Corollary B3 (PROVED): uniform Benford law.** For every ε > 0 there is N₀(ε) such that for every positive integer n and every distinct stretch with N ≥ N₀ odd terms, the proportion of odd terms with mantissa o/2^L(o) in [u, w) ⊂ [1, 2) differs from log₂(w/u) by at most ε. The same holds for leading ternary digits over all terms.

Proof. Take V = 2.931. Rotation orbits have discrepancy tending to 0 uniformly in the starting point (Weyl), so the block argument gives D_N ≤ δ + (V/δ + 1)·o(1). ∎

Explicit values with V = 2.931: D_N ≤ 0.049 at N = 10⁶, 0.0018 at 10⁹, 6·10⁻⁵ at 10¹².

Sketch, not written in full: with a finite irrationality exponent μ of log₂3 (Baker/Rhin, second-hand), D_N ≤ C_ε·N^(−1/μ+ε).

**Corollary B4 (PROVED).** For a stretch with K steps, N of them odd: L(x_K) − L(x₀) = N − K + ⌊t + N(λ−1) + η⌋ with t = {log₂x₀} and 0 ≤ η ≤ V. So the number of level-raising odd steps is a Beatty function of N up to an additive error ≤ 3.

**Remark B5 (conditional on the published 2^71 verification and cycle length ≥ 114,208,327,604).** On a nontrivial cycle V ≤ a/(3·2^71·ln 2) ≈ 1.5·10⁻¹¹, so the odd elements have binary mantissa discrepancy < 10⁻⁸. The trivial cycle {1, 2} is the opposite extreme.

**Novelty.** Kontorovich–Miller (2005) and Lagarias–Soundararajan (2006) treat most starting values and N ≤ c·log x₀ iterates, in any base. Theorem B is for every start and any length, but only base 2 on odd terms and base 3 on all terms. In other bases the phase a_k·log_B3 − k·log_B2 depends on the parity sequence. One web search found no per-trajectory statement; it may be folklore.

**Litmus.** B1 holds for qn+1 with rotation log₂q, and V_el uses only distinctness. So Theorem B holds for 5n+1 and 3n−1 (observed D ≈ 0.0002 on 30000 odd steps for each). For S_a the perturbation at modified points is log₂(1 − (2^(a+1)−1)/(3o)), again summable over distinct visits. It survives on every control map and is useless for descent. There is no 2-adic input at all.

A coupling attempt was vacuous: the rotation predicts the top j bits for W ≤ 2^(L−j) steps, and the bottom j′ bits give the next j′ parities. An overlap needs j + j′ ≥ L, so W ≤ 2^(j′), which the bottom bits already give.

### F. The Terras-horizon map

For x ≥ 2 let v ∈ {0,1}^L be its parity vector, a = |v|, k₀ < … < k_(a−1) the positions of the ones, c_v = Σᵢ 3^(a−1−i)·2^(kᵢ). Then 2^L·F(x) = 3^a·x + c_v. Terras: x ↦ v is a bijection from [2^L, 2^(L+1)) onto {0,1}^L.

**F1 (PROVED).** F(x) = 3^a + T^L(x − 2^L), with T(0) = 0. Proof: x − 2^L has the same parity vector; subtract the two affine formulas. ∎

**F2 (PROVED).** 3^a ≤ F(x) < 2·3^a + (3/2)^a, and L(F(x)) − ⌊aλ⌋ ∈ {0, 1, 2}. Proof: kᵢ ≤ L − a + i gives c_v/2^L ≤ (3/2)^a − 1. ∎

So F parses the parity sequence of x into consecutive blocks, each of length λ times the number of ones in the previous block, up to +2. Collatz ⇔ every such parse reaches block length ≤ 1.

**F3 (PROVED; this is Mirror Equivalence, Theorem 61, at the horizon — not new).** For a ≥ 1 let γ_v = c_v·2^(−L) mod 3^a ∈ [0, 3^a). Then F(x) ∈ {3^a + γ_v, 2·3^a + γ_v}, the second only if γ_v < (3/2)^a.

**F4 (PROVED for L ≤ 20000 by exact computation; all L given Ellison's |2^x − 3^y| > 2^x·e^(−x/10) for large x, cited from memory, exception list unverified).** For x ≥ 2: F(x) ≥ x ⇔ 3^a > 2^L. Hence #{x ∈ [2^L, 2^(L+1)) : F(x) ≥ x} = Σ_(a > L/λ) C(L, a) exactly, and the only fixed point of F is 1.

Proof.
- (⇐) T^L(x) ≥ 3^a·x/2^L, because every step is at least the linear branch.
- (⇒) If 3^a < 2^L and F(x) ≥ x, then c_v ≥ (2^L − 3^a)·2^L, so 2^L − 3^a ≤ (3/2)^a − 1. `check_gap.py` verifies exactly that this fails for every L ≤ 20000. Beyond that, 2^(0.855L) > 2^(0.369L) ≥ (3/2)^a.
- Fixed point: for x ≥ 2, F(x) = x gives 3^a > 2^L and then F(x) > x, since 3^a·x/2^L > x. ∎

Litmus: (⇐) is exactly n < T(n) on odds. It fails for S_a at 2^(a+1) − 1 (all-ones vector, F(x) = x) and for 3n−1 at 10. Computed F-fixed points below 2^12: {1, 2^(a+1) − 1} for S_a with a = 2..7; {1, 3, 9, 14} for S₁; {1, 10} for S₀ = 3n−1 (the 3n−1 list is the same through 2^16). Checked for n < 2^14, a ≤ 8: S_a violates n < S(n) ≤ 2n at exactly the one point 2^(a+1) − 1.

**F5 (PROVED): coalescence at the horizon.** #T^L([2^L, 2^(L+1))) ≤ Σ_a min(C(L,a), 3^a + (3/2)^a + 1) ≤ C·2^(0.9654L), where the exponent is H(θ*) with H(θ*) = θ*λ, θ* = 0.609. Proof: by F2 the values with a ones lie in an interval of length < 3^a + (3/2)^a. ∎

Data:

| L | 12 | 16 | 20 | 24 |
|---|---|---|---|---|
| #distinct F values / 2^L | 0.375 | 0.294 | 0.236 | 0.192 |

On the bad set F is nearly injective: #distinct/#bad = 0.60–0.72 for 12 ≤ L ≤ 24, with no decay. This is map-blind (the 5n+1 analogue has exponent 0.983).

**Generation counts (VERIFIED, exhaustive over all 2^L starts, 8 ≤ L ≤ 33).** N_k(L) = #{x of level L : F^(j+1)(x) ≥ F^j(x) for all j < k}. The model M_k sums β(L(F^(k−1)x)) over x counted in N_(k−1), with β(l) = 2^(−l)·Σ_(a>l/λ) C(l,a). N₁ = M₁ exactly at every L. The table shows N_k/M_k with N_k in brackets:

| L | N₁ | k=2 | k=3 | k=4 | k=5 | k=6 | k=7 | k=8 |
|---|---|---|---|---|---|---|---|---|
| 28 | 24,821,333 | 0.9987 | 0.9944 | 0.9736 | 0.853 (610) | 0.94 (35) | 0.46 (1) | N=0 |
| 29 | 36,519,556 | 1.0001 | 0.9925 | 0.9791 | 0.949 (844) | 1.56 (76) | 0.42 (2) | N=0 |
| 30 | 107,636,402 | 1.0000 | 0.9963 | 0.9857 | 0.971 (2475) | 1.31 (188) | 0.59 (7) | N=0 |
| 31 | 160,645,504 | 1.0002 | 1.0019 | 0.9810 | 0.988 (1988) | 0.80 (83) | 2.15 (9) | N=0 |
| 32 | 236,618,693 | 1.0001 | 1.0011 | 0.9870 | 1.041 (2840) | 0.92 (134) | 1.64 (11) | N=0 |
| 33 | 699,030,226 | 1.0001 | 1.0001 | 0.9910 | 1.019 (8066) | 0.94 (387) | 1.35 (26) | N=0 |

At L = 33: N₂ = 44,133,902, N₃ = 2,617,662, N₄ = 146,424.

Readings:
1. Consecutive bad F-steps behave as independent events through generation 5 (within 2% for k ≤ 4, 5% for k = 5, L ≥ 30).
2. Deeper generations deviate by up to 13.6× (L = 23, k = 7) and down to 0.15× (L = 26, k = 6). The cause is that N_k counts starting points, and starting points coalesce. The k = 7 entries at L = 20–25 are the family of glide record 1126015, whose F-orbit is 1126015 → 46225835 → 59302772 → 76079101 → 439205822 → 1901656439 → 6175288961 → 45119577824 → 6280768 → …. The recorded maxima are x = 2^j·1126015.
3. log₂N_k/L drops about 0.13 per generation at L ≈ 30, and N₈ = 0 for all L ≤ 33. In the model the largest k with N_k ≥ 1 is about L/(0.05L + ½log₂L + 1), which tends to 1/(1 − H(1/λ)) = 19.98.

**CANDIDATE (heuristic; same content as the Lagarias–Weiss prediction 41.68·ln n; not new):** no positive integer has 20 consecutive non-descending F-steps.

**Obstruction for seed (ii).** N₂(L) ≤ 2^((1−δ₂)L) with δ₂ > 0.05004 is lemma G2 (family 24). In F-coordinates: F(x) = 3^a + γ_v with γ_v known mod 3^a, and generation 2 needs F(x) mod 2^(L′) with L′ ≈ aλ. That is the binary digits of a 3-adically specified number, the Erdős regime. A deterministic streak bound is false for S_a (fixed points); for T it implies no divergence plus a logarithmic stopping-time bound. F1–F5 are all one-generation statements, and no structural reason for a bound was found. F is an adaptive re-chunking (family 5).

### S. The divergence series (seed (iii))

For a parity word v with A_j ones before position j, put R(v) = Σ_(j: v_j=1) 2^j·3^(−A_j−1). The 2-adic sum is minus the 2-adic integer with word v. The real sum converges for dense-ones words.

**S1 (PROVED).** R_∞(σv) = R_∞(v)/2 if v₀ = 0, and (3R_∞(v) − 1)/2 if v₀ = 1. So the real value follows the real branches of 3y−1. On a T-trajectory with convergent product, R_∞(σ^k v) = (ξ_k − 1)·x_k, where ξ_k = Π_(odd x_j, j≥k)(1 + 1/(3x_j)).

**S2 (PROVED).** If the real series converges and v has infinitely many ones, then y_k = R_∞(σ^k v) ≥ 1 for all k.

Proof. y > 0 always, and y ≥ 1/3 at odd positions. If y < 1 at some time, it stays below 1 and each odd step lowers it by at least (1 − y_k)/2, so it eventually drops below 1/3 at an odd step. ∎

This is all the real identity says, and it is trivial: it restates that the i-th later odd term is ≤ (3/2)^i·x_k·(1+o(1)). The real series encodes sizes; the 2-adic series encodes parities.

**S3 (PROVED).** For eventually periodic v with 3^a > 2^p on the period, R_∞(v) and R₂(v) are the same rational. So the integer is −R < 0: these are the negative cycles (v = (110)^∞ gives R = 5). A positive divergent orbit is a word with R₂ = −n < 0 < R_∞, where the two completions disagree. Nothing forces agreement for aperiodic words (the series is lacunary, not a G-function).

**S4 (obstruction).** The partial sums p/q, with q = 3^a and p = 2^K·x_K, approximate ξn with error (2^K/3^a)·y_K = H^(−λ₀)·y_K. Here H = 3^a, x_K ≍ H^(λ₀), and y_K ≥ 1. Ridout excludes error < H^(−λ₀−ε) for algebraic targets, so the Collatz approximations sit exactly on the boundary, and ξn is not known to be algebraic. Same wall as families 8 and 9.

Litmus: S1–S4 are formal identities in v, valid for every parity-prefix map. Dead.

## (c) Scripts

All in `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/w4-free/`; python is the repo venv.

| Command | Expected output |
|---|---|
| `python check_F.py` | `ALL F CHECKS PASSED` (F1–F4 for x < 2^17, 3000 random x up to 400 bits, 2^n ± 1; F-fixed points for T, 3n−1, S₀..S₇) |
| `python check_gap.py 20000` | `gap check ok up to L=20000; …` |
| `gcc -O2 -fopenmp -o fgen fgen.c -lm; OMP_NUM_THREADS=2 taskset -c 6-7 ./fgen 8 22` | generation tables; the L=20 line reads `maxstreak=7 at x=1126015` |
| `./fgen 23 33` | the table above; about 20 minutes on 2 cores |
| `python fimage.py 12 24` | F5 ratios |
| `python lemmaC_test.py 14 24` | distinct-image ratios 0.55–0.68 |
| `python check_benford.py` | `ALL BENFORD CHECKS PASSED` (continued fraction, Lemmas R and O by brute force, Theorem B asserted on 11 trajectories up to 60000 bits including 2^n − 1) |
| `python check_benford2.py` | `ALL WINDOW CHECKS PASSED` (bases 2 and 3; all n < 3000, random windows, tails near 1) |
| `python check_series.py` | `ALL SERIES CHECKS PASSED` (S1–S3 exact on periodic words; S2 on random dense words) |

The existing log is named `fgen_23_34.log` but holds L = 23..33; the run was stopped before L = 34.

## (d) Brainstorm (16 ideas) and dead ends

Each entry gives: imported technique / cheapest kill / where the order inequality enters / fate on S_a.

1. **F = T^L as a dynamical system** (Terras; seed ii). Kill: is generation 2 the G2 lemma? Yes. Order enters in F4 (⇐), which fails on S_a as it should. EXECUTED → obstruction, F1–F5, data.
2. **Mantissa rotation** (Weyl, Ostrowski). Kill: does it hold for 5n+1? Yes. Order enters only as multiplicative size. Survives on S_a. EXECUTED → Theorem B, no leverage.
3. **Mahler Z-number / Flatto–Lagarias–Pollington import.** There the same digit series has real value = fractional part and 2-adic value = integer part, and the real position forces the parity. Kill: is Collatz parity forced by a real quantity? No (S1–S2). EXECUTED.
4. **Ridout / Subspace on partial sums of the divergence series.** Exactly at the boundary (S4). Dead.
5. **Greedy or transfinite potential from the rigidity axioms** (seed i). S_a violates (III) at a single point, so a construction "from the axioms" must react to one changed value arbitrarily far out. No such mechanism was found. DISCARDED.
6. **Contraction in a space of orderings.** Fixed points of contractions are stable under small perturbations, and T ↦ S_a is a single-point change arbitrarily far out. Survives on S_a. DISCARDED.
7. **Nonstandard models / weak arithmetic** (seed iv). In a Z-ring such as ℤ + tℚ[t] the cycle equation (2^p − 3^a)x = c_v is linear, so there are no new cycles. A nonstandard x has, for standard time, the orbit of its 2-adic shadow: T^k(x) = T^k(c) + 3^(a_k)(x−c)/2^k. That is Terras's theorem. Collatz witnesses have length O(log x), so there is no independence handle. DISCARDED.
8. **Base-6 cellular automaton** (Kari). S_a is a rule of the same type with radius a. Survives. DISCARDED.
9. **Minimal-counterexample shadowing**: T^k(n) = T^k(n − 2^k q) + 3^(a_k)·q. The orbits decouple after k steps, and 2^(a+1) − 1 is a minimal counterexample for S_a. DISCARDED.
10. **Merge certificates** (n merges with a smaller m without descending; classes mod 2^k·3^b). For n = 2^k·m − 1 the rising segment has only larger off-path predecessors at the first two backward levels. This is a hand computation, not a proof for all depths. Relative of families 1 and 4. DISCARDED, not fully closed.
11. **Coalescence counting at the horizon.** Proved (F5); map-blind.
12. **Divergence of Σ1/x_k on infinite trajectories** would contradict Theorem 70 and exclude divergent orbits. It is equivalent to no divergence, with no independent mechanism. DISCARDED.
13. **Induction on binary length through F1.** The next step needs the parities of 3^a + y; adding 3^a destroys the 2-adic information. Erdős wall. Dead.
14. **Mantissa–parity overlap at small levels.** Vacuous (end of section B).
15. **Global relation real = 2-adic.** True for eventually periodic words only (S3).
16. **Deterministic bad-streak bound.** This is the Lagarias–Weiss conjecture; data only.

## (e) Best lead

**Lemma C (tested, no gain).** "The set {F²(x) : x of level L, F(x) ≥ x, F²(x) ≥ F(x)} has ≤ C·2^((1−δ)L) elements for some δ > 0.05004." The kill test for 14 ≤ L ≤ 24 gives #distinct F² images / N₂ = 0.55–0.68 with no decay. So counting trajectories instead of starting points saves a constant, and Lemma C is G2 up to that constant (VERIFIED to L = 24 only).

The single missing statement for the F-route therefore remains:

**Lemma G2, F-form (open; blocked, family 24).** There are δ₂ > 0.05004 and C with #{x ∈ [2^L, 2^(L+1)) : F(x) ≥ x and F(F(x)) ≥ F(x)} ≤ C·2^((1−δ₂)L) for all L.

Equivalently: for a ≥ L/λ, the numbers 3^a + γ_v (|v| = a, γ_v as in F3) are equidistributed modulo 2^(L′), L′ ≈ aλ, with a power saving against the set of residues whose L′-bit parity vector has more than L′/λ ones. The data support it with the exact independent-model constant (ratio 1.0001 at L = 33). Being a counting statement, it cannot by itself give descent.