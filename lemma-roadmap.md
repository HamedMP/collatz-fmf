# FMF Lemma Roadmap Toward Collatz

This file records the strongest current lemma chain. It separates proved results from the pointwise bridge that is still missing.

## Success Criterion

To prove Collatz through FMF, it is enough to prove:

> For every odd `x > 1`, some finite FMF iterate satisfies `F^n(x) < x`.

Once every odd number descends below itself, infinite descent rules out divergence and nontrivial cycles, so every orbit eventually reaches `1`.

## Proved Lemmas

### Lemma 1: FMF Formula

For every odd `x`, write:

- Type A: `x = 4k + 1`
- Type B: `x = 4k + 3`, with `k + 1 = 2^t m`, `m` odd, `t >= 0`; the case `t = 0` is the old B1 case and `t >= 1` is the old B2 case

Then:

- Type A: `FMF(x) = 4(3k + 1)`
- Type B: `FMF(x) = 2(3^(t+2)m - 1)`
- The FMF hop is `F(x) = FMF(x) / 2^v2(FMF(x))`

Status: proved algebraically in `paper/sections/02-fmf-formulas.typ`.

### Lemma 2: Type A Pointwise Contraction

If `x = 4k + 1 > 1`, then:

`F(x) = (3k + 1) / 2^v2(3k + 1) < x`.

Status: proved. This is the strongest pointwise contraction channel in the framework.

### Lemma 3: Type B Valuation Formula

For Type B with `x = 2^(t+2)m - 1`:

`v2(FMF(x)) = 1 + v2(m - 3^(-(t+2)))`

in the 2-adic integers.

Status: proved.

### Lemma 4: State Distribution In Natural Density

Inside any fixed FMF input state, the output state distribution is:

- `P(Type A) = 1/2`
- `P(Type B with depth j) = 1/2^(j+2)`

Status: proved as a natural-density statement, not as independence along one trajectory.

### Lemma 5: Fractional-Moment Contraction

For the FMF hop ratio `R = F(x)/x`, natural-density averaging gives:

`E[R^0.53] ~= 0.8638 < 1`.

Status: proved as an asymptotic density model. It is not a pointwise Lyapunov theorem.

### Lemma 6: Growth-B Branch Equation

A strict growth-B hop is a Type B hop with `v2(FMF(x)) = 2`. With `x = 2^(t+2)m - 1`, this means:

`3^(t+2)m ≡ 3 (mod 4)`.

If the output is again Type B, then:

`3^(t+2)m ≡ 7 (mod 8)`

and the next parameters satisfy:

`m_next = odd_part((3^(t+2)m + 1) / 8)`.

Equivalently, for `t_next = v2((3^(t+2)m + 1) / 8)`:

`2^(t_next + 3)m_next - 3^(t+2)m = 1`.

Status: proved by algebra from the FMF formula.

### Lemma 7: Quartering Law

Conditional on a current growth-B hop, the density factor for one additional growth-B continuation is `1/4`.

Consequently, among all odd starting values, the natural density of strict growth-B chains of length at least `k` is `4^-k`.

Status: proved as a density theorem. It does not rule out exceptional individual integer orbits.

### Lemma 7b: Growth-B Hops Strictly Grow

Every growth-B hop satisfies:

`F(x) / x > 9/8`.

Proof sketch:

For `x = 2^(t+2)m - 1` and `v2(FMF) = 2`,

`F(x) = (3^(t+2)m - 1) / 2`.

Then `F(x)/x > 9/8` is equivalent to:

`4(3^(t+2)m - 1) > 9(2^(t+2)m - 1)`.

For `t = 0`, this is `36m - 4 > 36m - 9`; for `t >= 1`, the leading coefficient is already strictly larger.

Status: proved. An infinite growth-B chain would therefore be a genuinely divergent increasing odd subsequence.

### Lemma 8: Periodic Growth-B Patterns Are Impossible For Positive Integers

Suppose a growth-B continuation has an eventually periodic depth pattern `t_i`.

For one continuation step:

`2^(t_{i+1} + 3)m_{i+1} - 3^(t_i + 2)m_i = 1`.

For a period of length `p`, composing the affine recurrences gives:

`B m_{n+p} = A m_n + C`

where:

- `A = 3^(sum(t_i + 2))`
- `B = 2^(sum(t_{i+1} + 3))`
- `C > 0`

Over one full period, `sum(t_{i+1}) = sum(t_i)`, so:

`B / A = (8/9)^p (2/3)^(sum t_i) < 1`.

If the depth pattern repeats forever, the corresponding 2-adic tail must be the fixed point:

`m = C / (B - A)`.

Since `B - A < 0` and `C > 0`, this fixed point is negative as a rational number. Therefore it cannot be a positive integer.

Status: proved for eventually periodic depth patterns. This rules out one large class of possible infinite growth-B obstructions, but not arbitrary nonperiodic depth patterns.

### Lemma 9: Every Finite Growth-B Depth Word Is Realizable

For every finite sequence of nonnegative integers:

`(t_0, ..., t_{L-1})`

there are infinitely many positive odd `m_0` such that the growth-B chain starting from:

`x_0 = 2^(t_0 + 2)m_0 - 1`

has depth word exactly `(t_0, ..., t_{L-1})` for its first `L` growth-B hops.

Proof idea:

1. Choose the final parameter `m_{L-1}`.
2. The final growth-B condition imposes one residue class modulo `4`.
3. Each backward equation

   `m_i = (2^(t_{i+1}+3)m_{i+1} - 1) / 3^(t_i+2)`

   imposes one residue class on `m_{i+1}` modulo `3^(t_i+2)`.
4. These odd moduli are coprime to `4`, so CRT gives infinitely many positive choices of `m_{L-1}`.
5. Choosing a sufficiently large representative makes all backward-defined `m_i` positive odd integers.

Status: proved. This is a negative result for proof strategy: no finite forbidden-pattern argument can prove growth-B termination.

### Lemma 10: Exact Zero-Depth Branch

For a start with depth `t_0 = 0`, the first `L` growth-B hops all have depth `0` iff:

`m_0 ≡ -1 (mod 8^L)`.

Proof sketch:

On the zero-depth branch,

`m_{i+1} = (9m_i + 1) / 8`,

so while the branch remains at depth `0`,

`m_i + 1 = (9/8)^i (m_0 + 1)`.

The `i`-th state has depth `0` and is growth-B exactly when `m_i ≡ -1 (mod 8)`, i.e. `8 | m_i + 1`. This is equivalent to:

`8^(i+1) | 9^i(m_0 + 1)`,

and since `9` is odd, to:

`8^(i+1) | m_0 + 1`.

Requiring this for every `0 <= i < L` gives `8^L | m_0 + 1`.

Status: proved.

Consequence: the infinite all-zero depth branch has unique 2-adic code `m_0 = -1`, so no positive integer realizes it forever. This is the exact `T=0` base case for the bounded-depth obstruction program.

### Lemma 10b: Arbitrarily Long Finite Growth-B Chains

For every `L >= 1`, there is a positive odd start whose FMF trajectory begins with at least `L` consecutive growth-B hops.

Explicit construction:

- choose `m_0 = 8^L - 1`
- choose `x_0 = 4m_0 - 1`

Then for `0 <= i < L`:

`m_i = 9^i 8^(L-i) - 1`

and `t_i = 0`, so each of the first `L` hops is growth-B. The next quotient after the `L`-th hop is `9^L - 1`, whose valuation need not be zero; that is irrelevant to the length-`L` lower bound.

Status: proved. This rules out any proof strategy based on a uniform finite maximum growth-chain length.

The same family gives a lower bound on any possible logarithmic theorem. Since `m_0 = 8^L - 1`, any universal bound

`growth_B_chain_length <= c log2(m0) + O(1)`

must have `c >= 1/3`. The empirical candidate `0.55 log2(m0) + 3` is therefore within a small constant factor of the explicit obstruction.

### Lemma 11: Growth-B Congruence Normal Form

In any growth-B continuation branch:

`2^(t_{i+1}+3)m_{i+1} - 3^(t_i+2)m_i = 1`,

the next odd parameter satisfies:

`m_{i+1} ≡ (-1)^(t_{i+1}+3) (mod 3)`.

Therefore, after discarding at most the initial state of an infinite continuation branch, every continuing state satisfies:

- if `t_i` is even, then `m_i ≡ 23 (mod 24)`
- if `t_i` is odd, then `m_i ≡ 13 (mod 24)`

Status: proved.

This is a useful normal form for future attacks: an infinite obstruction eventually lives in one of two residue classes modulo `24`, determined only by depth parity.

### Lemma 11b: Binary-Depth Affine Normal Form

Suppose a growth-B continuation branch has depths restricted to `{0, 1}`. After discarding at most the initial state, write:

- if `t_i = 0`, then `m_i = 24n_i + 23`
- if `t_i = 1`, then `m_i = 24n_i + 13`

Then each continuing transition is one of four affine maps:

- `0 -> 0`: `n_{i+1} = (9n_i + 1) / 8`, requiring `n_i ≡ 7 (mod 8)`
- `0 -> 1`: `n_{i+1} = 9n_i / 16`, requiring `n_i ≡ 0 (mod 16)`
- `1 -> 0`: `n_{i+1} = (27n_i + 7) / 8`, requiring `n_i ≡ 3 (mod 8)`
- `1 -> 1`: `n_{i+1} = (27n_i + 6) / 16`, requiring `n_i ≡ 14 (mod 16)`

Status: proved by substitution into the continuation equation.

This is the exact normal form for the `T = 1` bounded-depth obstruction. It does not yet prove termination, but it reduces the binary-depth case to four explicit affine maps with congruence gates.

### Lemma 11c: Binary Zero-Return Expansion

In the binary-depth normal form, suppose a branch starts at depth `0` with parameter `n` and next returns to depth `0`.

- For the one-step block `0 -> 0`, `n' = (9n + 1) / 8`, so `n' - n = (n + 1) / 8 > 0`.
- For a block `0 -> 1^r -> 0` with `r >= 1`, the affine multiplier is:

`(9/16)(27/16)^(r-1)(27/8) = (243/128)(27/16)^(r-1) > 1`,

and the composed additive constant is positive.

Therefore every admissible return from depth `0` to depth `0` strictly increases the normalized parameter `n`.

Status: proved.

Consequence: a binary-depth infinite obstruction cannot be a bounded recurrence. If it has infinitely many depth-`0` states, those states form a strictly increasing sequence. If it has only finitely many depth-`0` states, the depth word is eventually all `1`s and is already excluded by Lemma 8.

### Lemma 11d: Binary Return-Block Gate

In the binary-depth normal form, fix `r >= 0`. The return block:

`0 -> 1^r -> 0`

is admissible for exactly one residue class of the starting depth-`0` parameter `n` modulo:

`2^(4r+3)`.

Reason: each transition has the form:

`n_next = (a n + c) / 2^e`

with `a` odd. Pulling back a suffix condition `n_next ≡ R (mod 2^q)` gives:

`a n + c ≡ 2^e R (mod 2^(q+e))`,

which has exactly one solution modulo `2^(q+e)`.

Status: proved.

First return-block gates from `explore50_binary_depth_affine.py`:

- `r = 0`: `n ≡ 7 (mod 2^3)`
- `r = 1`: `n ≡ 48 (mod 2^7)`
- `r = 2`: `n ≡ 736 (mod 2^11)`
- `r = 3`: `n ≡ 21472 (mod 2^15)`

### Lemma 11d.1: Binary Return-Block Closed Gate

The unique gate for the binary return block `0 -> 1^r -> 0` is equivalently:

`33n + 32 ≡ epsilon_r 16^r (mod 2^(4r+3))`,

where:

- `epsilon_r = 7` if `r` is even
- `epsilon_r = 5` if `r` is odd

Status: proved.

This replaces the opaque inverse formula `n ≡ -D_r P_r^(-1) (mod Q_r)` with a fixed linear expression. It is the cleanest present target for attacking the binary-depth obstruction.

### Lemma 11e: Binary Return-Block Coding

For the binary-depth case, every return block `0 -> 1^r -> 0` has the form:

`n_{j+1} = (P_r n_j + D_r) / Q_r`,

where:

- `P_r = 9 * 27^r`
- `Q_r = 2^(4r+3)`
- `D_0 = 1`
- `D_r = (2592 * 27^(r-1) - 85 * 16^r) / 11` for `r >= 1`

Therefore every infinite binary-depth continuation with infinitely many depth-`0` states is encoded by an infinite 2-adic return-block code. Such a continuation exists in positive integers only if that return-block code is a nonnegative ordinary integer.

Status: proved.

This is a compressed version of the main integer-code problem for `T = 1`: instead of coding every depth bit, it codes the lengths of the runs of `1`s between successive `0`s.

### Lemma 11e.0a: Binary Return Critical Series

Fix an infinite binary return-length word `(r_0, r_1, ...)`. For each return block, write:

`alpha_j = P_(r_j) / Q_(r_j)`, `beta_j = D_(r_j) / Q_(r_j)`.

Define:

`M_N = - sum_{i=0}^{N-1} beta_i / (alpha_0 alpha_1 ... alpha_i)`.

Then `M_N` converges in `R` to a value `M_R` satisfying:

`-1 <= M_R < 0`.

The same rational sequence converges in `Q_2` to the 2-adic return code selected by the infinite return word. For the finite composition:

`Q_N n_N = P_N n_0 + D_N`,

one has:

`M_N = -D_N / P_N`,

and the least return-prefix residue satisfies:

`R_N ≡ M_N (mod Q_N)`.

Status: proved.

Interpretation: the binary return obstruction has the same adelic shape as the reduced `{0,1}` gap obstruction. Eventually periodic return words have rational critical values in `[-1,0)`, so they cannot be nonnegative integers. The remaining hard case is a nonperiodic return word whose 2-adic critical limit is a positive ordinary integer.

### Lemma 11e.0b: Binary Return Ordinary-Landing Divisibility Criterion

Fix an infinite return-length word `(r_0, r_1, ...)` and a positive integer `M`. Let:

`Q_N n_N = P_N n_0 + D_N`

be the affine composition of the first `N` return blocks, and put:

`S_N = r_0 + ... + r_{N-1}`.

Then `M` is the positive ordinary return code for this word if and only if:

`v_2(P_N M + D_N) >= 3N + 4S_N`

for every `N >= 1`. In that case:

`n_N = (P_N M + D_N) / Q_N`

is the corresponding positive return orbit.

Status: proved.

Interpretation: the return-code landing problem is exactly a problem of forcing arbitrarily high powers of `2` to divide the integer sequence `P_N M + D_N`.

### Lemma 11e.1: Binary Return-Code Boundedness Criterion

Fix an infinite return-length word `(r_0, r_1, ...)`, and let `R_N` be the least nonnegative residue of its length-`N` return-block prefix code modulo:

`Q_N = prod_{j=0}^{N-1} 2^(4r_j+3)`.

The corresponding binary return code is a nonnegative ordinary integer if and only if `R_N` is bounded. Equivalently, this happens if and only if `R_N` is eventually constant.

Status: proved.

Interpretation: this is the exact remaining `T = 1` target. Prove that every non-eventually-periodic infinite return-length word has unbounded return-prefix residues.

### Lemma 11e.1u: Binary Return Ordinary Itinerary Uniqueness

For a fixed nonnegative depth-`0` parameter `n_0`, there is at most one infinite binary return-length word for which `n_0` is the ordinary return code.

Status: proved.

Reason: the partial map reads the next return length from `33n+32=16^r w`, so `r=v_2(33n+32)/4` and the next state are unique whenever a return exists.

Interpretation: for a fixed ordinary integer, the candidate obstruction word is forced. The remaining problem is proving that this forced partial-map orbit eventually fails.

### Lemma 11e.1w: Binary Return Finite Height Search Criterion

Fix a positive integer bound `B` and return-prefix length `L`. To decide whether there is a length-`L` return word with least prefix residue `R_L < B`, it is enough to search a finite tree:

- keep only prefixes whose current least residue is `< B`
- for a current prefix composition `Q_i n_i = P_i n_0 + D_i`, only test next return lengths `r_i` satisfying `16^r_i Q_i < 33(P_i B + D_i) + 32Q_i`

Status: proved.

Reason: prefix residues are nondecreasing, so a final residue `< B` forces every shorter prefix residue `< B`. Also, any ordinary start `n_0 < B` gives intermediate state `n_i < (P_i B + D_i)/Q_i`; if the next return length is `r_i`, then `16^r_i <= 33n_i + 32`.

Interpretation: this gives exact finite certificates for least return-prefix residues at each fixed length. It is not the infinite return-code theorem; it is a rigorous finite-height search tool.

### Lemma 11e.1x: Binary Return Global-Minimum Divergence Criterion

Let `mu_L` be the least return-prefix residue among all return words of length `L`.

Then the binary return system has no nonnegative ordinary infinite return code if and only if:

`mu_L -> infinity`.

Status: proved.

Reason:

- If an ordinary code `M` exists, its prefix residues eventually equal `M`, so `mu_L <= M` for all large `L`.
- If `mu_L` is bounded, the finite-height search criterion gives a finitely branching tree of bounded-residue prefixes with nodes at every depth. The infinite-tree lemma gives an infinite bounded-residue path, and the boundedness criterion turns that path into an ordinary return code.

Interpretation: the full `T = 1` binary return obstruction is equivalent to proving a global minimum-residue height theorem.

### Lemma 11e.1x1: Bounded Return Alphabet Divergence Criterion

Fix `R >= 0`, and let `mu_L^(<=R)` be the least return-prefix residue among all return words of length `L` whose letters lie in `{0, ..., R}`.

Then there is no nonnegative ordinary infinite return code over this bounded alphabet if and only if:

`mu_L^(<=R) -> infinity`.

Status: proved.

Reason:

- If an ordinary code `M` exists over the alphabet, its prefix residues eventually equal `M`, so `mu_L^(<=R) <= M` for all large `L`.
- If `mu_L^(<=R)` is bounded, the bounded alphabet gives a finitely branching tree of bounded-residue prefixes with nodes at every depth. The infinite-tree lemma gives an infinite bounded-residue path, and the return boundedness criterion turns that path into an ordinary code.

Interpretation: the bounded-return-length half of the obstruction is itself an exact minimum-residue divergence theorem for each finite alphabet.

### Lemma 11e.1x2: Binary Return Fixed Positive-Label Divergence

Fix `J >= 0`, and let `mu_(L,J)^+` be the least return-prefix residue among length-`L` return words with at most `J` positive return lengths.

Then:

`mu_(L,J)^+ -> infinity`.

Status: proved.

Reason: if these minima were bounded, the finite-height search criterion would give an infinite bounded-residue path whose prefixes all have at most `J` positive labels. The infinite path then has only finitely many positive labels, so its return itinerary is eventually all zero and hence eventually periodic. The return boundedness criterion would turn the bounded residues into an ordinary infinite return code, contradicting the exclusion of eventually periodic return itineraries.

Interpretation: in the `{0,1}` return alphabet, every fixed-one-count stratum is already settled. A remaining bounded-residue obstruction must contain infinitely many `1` labels.

### Lemma 11e.1x2a: Binary Return Prefix-Language Compactness Principle

Let `C` be any prefix-closed collection of finite return words. Let `mu_C(L)` be the least return-prefix residue among words in `C` of length `L`, when such words exist.

If `mu_C(L)` does not tend to infinity along the lengths where it is defined, then there is an infinite return-length word whose every prefix lies in `C` and whose return code is a nonnegative ordinary integer.

Status: proved.

Reason: bounded minima give a finitely branching bounded-residue prefix tree by the finite-height search criterion. An infinite path through that tree has bounded, nondecreasing prefix residues, so the return boundedness criterion turns it into an ordinary code.

Interpretation: this is the reusable compactness engine behind the finite-alphabet, fixed-positive-label, and finite-defect periodic-shadow divergence lemmas.

### Lemma 11e.1x3: Binary Return Finite-Defect Periodic Shadow Divergence

Fix an eventually periodic infinite return-length word `z` and `J >= 0`. Let `mu_(L,J)(z)` be the least return-prefix residue among length-`L` return words that differ from the length-`L` prefix of `z` in at most `J` positions.

Then:

`mu_(L,J)(z) -> infinity`.

Status: proved.

Reason: if these minima were bounded, finite-height compactness would give an infinite bounded-residue path with at most `J` total deviations from `z`. Since `z` is eventually periodic, that path is eventually periodic. The return boundedness criterion would turn it into an ordinary infinite return code, contradicting the exclusion of eventually periodic return itineraries.

Interpretation: a return obstruction cannot stay at bounded edit distance from any eventually periodic template. It must have unbounded defect from every periodic shadow.

### Lemma 11e.1x4: Binary Return Low-Complexity Divergence

Fix `m >= 1`. For a finite binary return word `w`, let `p_w(m)` count its distinct length-`m` factors. Let `mu_(L,m)^low` be the least return-prefix residue among length-`L` binary return words with `p_w(m) <= m`.

Then:

`mu_(L,m)^low -> infinity`.

Status: proved.

Reason: the class of finite binary words with `p_w(m) <= m` is prefix-closed. Any infinite path through this class has at most `m` distinct length-`m` factors, so Morse-Hedlund makes it eventually periodic. The return prefix-language compactness principle then turns bounded low-complexity minima into an eventually periodic ordinary return code, contradicting the periodic-itinerary exclusion.

Interpretation: a remaining binary return obstruction must be Sturmian-or-higher at every fixed scale: for each `m`, its long low-residue prefixes must have at least `m+1` distinct length-`m` factors.

### Lemma 11e.1x4a: Balanced Aperiodic Positive-Density Lemma

If an infinite balanced binary word is not eventually periodic, then both symbols occur with bounded gaps. Consequently, every long factor contains linearly many `0`s, linearly many `1`s, and linearly many symbol changes.

Status: proved.

Reason: choose two consecutive `1`s and let the factor spanning them have length `m_1`. That factor has two `1`s, so balance forbids any length-`m_1` factor with zero `1`s. Thus every length-`m_1` block contains a `1`. The same argument with consecutive `0`s gives bounded gaps between `0`s.

Interpretation: the balanced/Sturmian-like obstruction is not density-zero sparse and cannot be a bounded-block-change tail. Sparse balanced finite minimizers are finite shadows; an infinite non-eventually-periodic balanced code would have positive lower density of both symbols and both transitions.

### Lemma 11e.1x4b: Balanced Slope Lemma

Every infinite balanced binary word has a slope `alpha in [0,1]`: every length-`n` factor has `alpha n + O(1)` ones. More precisely, the discrepancy is at most `2`. If the word is not eventually periodic, then `0 < alpha < 1`.

Status: proved.

Reason: if `A(n)` counts ones in the length-`n` prefix, balance gives the almost-additivity estimate `|A(n+m)-A(n)-A(m)| <= 1`. This forces `A(n)/n` to converge. Balance then transfers the prefix estimate to every factor. The positive-density lemma excludes slopes `0` and `1` for non-eventually-periodic words.

Interpretation: the balanced frontier is a bounded-discrepancy positive-density slope problem.

### Lemma 11e.1x4c: Balanced Aperiodic Irrational-Slope Lemma

If an infinite balanced binary word is not eventually periodic, then its slope is irrational.

Status: proved by importing the standard balanced-word classification.

Reason: classical balanced-word theory classifies balanced infinite binary words as Sturmian or skew. The non-ultimately-periodic case is aperiodic Sturmian, and Sturmian words have irrational slope; rational-slope balanced binary words are ultimately periodic.

Interpretation: the rational-slope balanced branch is already covered by the periodic-itinerary exclusions. Any balanced ordinary return or reduced-gap obstruction must have irrational slope in `(0,1)`.

### Lemma 11e.1x4d: Balanced Sturmian Complexity Lemma

If an infinite balanced binary word is not eventually periodic, then its factor complexity is exactly minimal:

`p_x(m)=m+1`

for every `m >= 1`.

Status: proved by importing the standard Sturmian classification.

Reason: a non-eventually-periodic balanced binary word is an aperiodic Sturmian word. Sturmian words are precisely the aperiodic binary words of minimal complexity.

Interpretation: the balanced frontier is the exact Sturmian/minimal-complexity frontier. General bounded binary obstructions must be Sturmian-or-higher; balanced obstructions themselves are exactly Sturmian.

### Lemma 11e.1x4e: Balanced Mechanical Normal Form

Every non-eventually-periodic balanced infinite binary word can be written as a lower or upper mechanical word:

`x_i = floor((i+1) alpha + rho) - floor(i alpha + rho)`

or

`x_i = ceil((i+1) alpha + rho) - ceil(i alpha + rho)`,

where `alpha in (0,1)` is irrational and the intercept is normalized to `rho in [0,1)`.

Status: proved by importing the standard mechanical-word characterization of Sturmian words.

Reason: the previous lemmas identify the balanced aperiodic branch as an irrational-slope Sturmian word. Standard Sturmian theory represents such words by irrational rotations with an intercept. Integer shifts of the intercept do not change the digit sequence, so `rho` may be taken modulo `1`.

Interpretation: this reduced the balanced landing problem to a two-parameter irrational-rotation problem with `alpha in (0,1) \\ QQ` and `rho in [0,1)`. The later fast prefix-recurrence lemmas close this branch.

### Lemma 11e.1x4f: Mechanical Convention Reduction

For fixed irrational `alpha in (0,1)` and normalized intercept `rho in [0,1)`, the lower and upper mechanical words differ in at most two adjacent positions.

Consequently, to exclude positive ordinary return or reduced-gap landings for all mechanical words, it is enough to exclude lower mechanical words for all irrational `alpha` and normalized `rho`.

Status: proved.

Reason: write `t_i=i alpha+rho`. The upper-minus-lower digit difference is nonzero only when either `t_i` or `t_(i+1)` is an integer. Irrationality of `alpha` allows at most one such index. If an upper word has an ordinary landing, discard a finite prefix beyond the possible discrepancy and use the return/gap shift-code recurrence; the remaining suffix is a lower mechanical word with intercept `rho+J alpha` normalized modulo `1`.

Interpretation: this reduced the mechanical landing problem to the lower convention. The upper convention contributes only finite-prefix effects, and the later Sturmian recurrence argument closes the balanced branch.

### Lemma 11e.1x4g: Mechanical Uniform Recurrence Lemma

Every non-eventually-periodic balanced infinite binary word is uniformly recurrent: each finite factor occurs with bounded gaps.

Status: proved by importing the standard Sturmian uniform-recurrence theorem.

Reason: the balanced mechanical normal form identifies the word as an aperiodic Sturmian word. Standard Sturmian theory gives uniform recurrence; in the mechanical model this is the bounded-return property of intervals under an irrational circle rotation.

Interpretation: a balanced ordinary landing would be a self-shadowing positive orbit whose finite prefix patterns recur infinitely often with bounded gaps.

### Lemma 11e.1x4h1: Lower Mechanical Prefix-Cylinder Lemma

For a lower mechanical word

`x_i = floor((i+1) alpha + rho) - floor(i alpha + rho)`,

and a finite prefix `w` of length `m`, the set `C_w` of intercepts `eta in [0,1)` that realize the same prefix `w` is a positive-measure finite union of half-open intervals. The prefix `w` recurs at position `j` exactly when

`rho + j alpha mod 1 in C_w`.

Consequently the recurrence positions have natural density `|C_w| > 0` and bounded gaps.

Status: proved.

Reason: lower mechanical digits are generated by the two half-open rotation intervals `[0,1-alpha)` and `[1-alpha,1)`. The length-`m` cylinder is the intersection of finitely many shifted half-open intervals, with boundary among `{0,-alpha,...,-m alpha} mod 1`. Since `alpha` is irrational, the boundary is finite and distinct; the lower convention gives a positive one-sided interval even when the starting intercept lies on a boundary. Equidistribution of irrational rotations gives the visit density, and minimality gives bounded return gaps to the nonempty interval.

Interpretation: after reducing to the lower convention, prefix recurrence can be tracked by explicit irrational-rotation cylinders rather than by abstract uniform recurrence alone.

### Lemma 11e.1x4h: Balanced Landing Recurrent Prefix Congruences

If a non-eventually-periodic balanced return word has positive ordinary return code and initial length-`m` prefix residue/modulus `(R_m,Q_m)`, then there are infinitely many later states `X_j`, with bounded gaps between such `j`, satisfying

`X_j == R_m (mod Q_m)`.

Likewise, if a non-eventually-periodic balanced zero-gap word has positive ordinary gap code and initial prefix residue/modulus `(S_m,H_m)`, then infinitely many later states `Y_j`, with bounded gaps, satisfy

`Y_j == S_m (mod H_m)`.

Status: proved as a conditional structure theorem.

Reason: uniform recurrence makes the initial length-`m` block recur with bounded gaps. The return and gap shift-code recurrences identify each shifted state as the ordinary code of its shifted suffix. The forced-prefix equivalence then imposes the same prefix congruence on each such later state.

Interpretation: a balanced landing would be an expanding positive orbit that repeatedly re-enters every initial prefix congruence class.

### Lemma 11e.1x4h2: Lower Mechanical Landing Prefix-Cylinder Congruences

If a lower mechanical balanced return landing existed, then for every fixed prefix length `m`, with lower prefix cylinder `C_m` and prefix residue/modulus `(R_m,Q_m)`, the set

`J_m = {j >= 0 : rho + j alpha mod 1 in C_m}`

has natural density `|C_m| > 0`, has bounded gaps, and every later state indexed by `J_m` satisfies

`X_j == R_m (mod Q_m)`.

The reduced-gap analogue holds with states `Y_j` and residue/modulus `(S_m,H_m)`.

Status: proved as a lower-convention strengthening of the recurrent-prefix congruence theorem.

Reason: the prefix-cylinder lemma identifies the recurrence positions with a positive-density rotation hitting set. At each such position, the shift-code recurrence makes the later state the ordinary code of the shifted suffix, and forced-prefix equivalence imposes the same prefix congruence.

Interpretation: in the remaining balanced branch, every fixed high-power-of-two prefix congruence is hit on a positive-density set of irrational-rotation times while the same ordinary states follow the slope-controlled exponential height law.

### Lemma 11e.1x4i: Mechanical Prefix-Sum Modulus Formula

For a lower mechanical word,

`x_i = floor((i+1) alpha + rho) - floor(i alpha + rho)`,

the prefix sum is exactly

`X_N = floor(N alpha + rho) - floor(rho)`.

For an upper mechanical word, the same identity holds with `ceil` in place of `floor`.

Consequently, a mechanical balanced return word has prefix modulus

`Q_N = 2^(3N+4X_N)`,

and a mechanical balanced reduced-gap word has prefix modulus

`H_N = 2^(7N+3X_N)`.

Status: proved.

Reason: the prefix sum telescopes, and the return/gap moduli multiply over the binary labels.

Interpretation: the mechanical landing problem has exact floor/ceiling exponent sequences, not only asymptotic slope exponents; this is one input to the later recurrence contradiction.

### Lemma 11e.1x4j: Mechanical Landing Divisibility Normal Form

Let `x_i` be a lower or upper mechanical binary word, and let `X_N=x_0+...+x_(N-1)`.

For the return system:

`P_N = 9^N 27^(X_N)`, `Q_N = 2^(3N+4X_N)`,

and the additive term is determined by

`D_0^*=0`,

`D_(N+1)^* = 9 * 27^(x_N) D_N^* + d_(x_N) Q_N`,

where `d_0=1` and `d_1=112`. A positive integer `M` is the return landing for the mechanical word iff

`v_2(9^N 27^(X_N) M + D_N^*) >= 3N+4X_N`

for every `N`.

For the reduced-gap system:

`A_N = 3^(5N+2X_N)`, `H_N = 2^(7N+3X_N)`,

and

`C_0^*=0`,

`C_(N+1)^* = 3^(5+2x_N) C_N^* + 8^(x_N) H_N`.

A positive integer `A` is the reduced-gap landing for the mechanical word iff

`v_2(3^(5N+2X_N) A - C_N^*) >= 7N+3X_N`

for every `N`.

Status: proved.

Reason: multiply the binary one-block coefficients and moduli, use the mechanical prefix-sum formula for `X_N`, and apply the ordinary-landing divisibility criteria.

Interpretation: the balanced landing problem is an explicit pair of high-2-adic-valuation problems along irrational floor/ceiling words.

### Lemma 11e.1x4k: Balanced Periodic-Shadow Linear Separation

If `x` is a non-eventually-periodic balanced infinite binary word and `z` is any eventually periodic infinite binary word, then the Hamming distance between their length-`L` prefixes is at least `c L + O(1)` for some `c > 0`.

Status: proved.

Reason: `x` has irrational slope `alpha`, while `z` has rational eventual symbol frequency `beta`. The prefix one counts differ by `|alpha-beta|L+O(1)`, and Hamming distance is at least the absolute difference of one counts.

Interpretation: a balanced obstruction is linearly far from every fixed periodic shadow. Periodic rational approximants may shadow finite windows, but no fixed periodic template captures the infinite balanced obstruction with sublinear edit defect.

### Lemma 11e.1x4l: Balanced Ordinary Landing Growth Rate

If a non-eventually-periodic balanced binary return word has ordinary return code `M` and slope `alpha`, then `alpha` is irrational and the realized return states satisfy

`log n_N / N -> log(9/8) + alpha log(27/16)`.

The return prefix modulus also satisfies `log_2 Q_N = (3+4 alpha)N + O(1)`.

If a non-eventually-periodic balanced binary zero-gap word has positive ordinary gap code `A` and slope `alpha`, then `alpha` is irrational and the realized gap states satisfy

`log a_N / N -> log(243/128) + alpha log(9/8)`,

with `log_2 H_N = (7+3 alpha)N + O(1)`.

Status: proved as a conditional structure theorem.

Reason: balanced slope gives `S_N=alpha N+O(1)` or `K_N=alpha N+O(1)`. The return and gap critical-series identities write the realized state as the expansion factor times a bounded positive landing factor. Taking logarithms gives the rates.

Interpretation: the remaining balanced obstruction, if it exists, is an irrational-slope ordinary integer orbit with a fixed exponential height law. The missing theorem is the 2-adic landing exclusion, not an average-growth estimate.

### Lemma 11e.1x4m: Balanced Landing Prefix-Return-Time Lower Bound

If a lower mechanical balanced return landing of irrational slope `alpha` existed, and `tau_m` denotes the least positive recurrence time of its initial length-`m` prefix, then

`liminf tau_m/m >= (3+4 alpha)/(log_2(9/8)+alpha log_2(27/16))`.

If a lower mechanical balanced reduced-gap landing existed, and `sigma_m` denotes the least positive recurrence time of its initial length-`m` prefix, then

`liminf sigma_m/m >= (7+3 alpha)/(log_2(243/128)+alpha log_2(9/8))`.

Status: proved as a conditional quantitative obstruction.

Reason: when the initial prefix recurs at time `tau_m`, the later state is congruent to the initial ordinary code modulo the length-`m` prefix modulus. If the recurrence time were below the displayed threshold infinitely often, the exponential height law would give a later state smaller than the prefix modulus, while the modulus is also eventually larger than the initial code. The congruence would then force the later state to equal the initial state, contradicting positive exponential growth.

Interpretation: the balanced landing problem can now be attacked through recurrence speed. A lower mechanical landing would force every sufficiently long initial prefix to have first recurrence time at least a large slope-dependent multiple of its length. Any theorem giving infinitely many prefix recurrences below this threshold would rule out the balanced landing branch.

### Lemma 11e.1x4n: Fast Prefix-Recurrence Exclusion Criterion

For a lower mechanical word of irrational slope `alpha`, if its first prefix-recurrence function `tau_m` satisfies

`liminf tau_m/m < (3+4 alpha)/(log_2(9/8)+alpha log_2(27/16))`,

then it has no positive ordinary return code.

For the reduced-gap side, if the first prefix-recurrence function `sigma_m` satisfies

`liminf sigma_m/m < (7+3 alpha)/(log_2(243/128)+alpha log_2(9/8))`,

then it has no positive ordinary reduced-gap code.

Status: proved as the contrapositive of Lemma 11e.1x4m.

Reason: Lemma 11e.1x4m shows that any lower mechanical landing forces the opposite lower bound on first prefix-recurrence times. Violating that bound along infinitely many prefix lengths therefore excludes the landing.

Interpretation: this is the clean plug-in criterion that finishes the balanced branch once paired with the Sturmian fast prefix-recurrence lemma.

### Lemma 11e.1x4o: Sturmian Fast Prefix-Recurrence Lemma

For every non-eventually-periodic balanced binary word, if `tau_m` is the least positive recurrence time of the initial length-`m` prefix, then

`liminf tau_m/m <= 2`.

Status: proved by importing the standard Sturmian recurrence-function formula.

Reason: a non-eventually-periodic balanced word is Sturmian. If `R_x(m)` is the recurrence function of a Sturmian word and `q_n` are the continued-fraction denominators of the slope, the standard Morse-Hedlund formula gives `R_x(q_n-1)=(q_n-1)-1+q_n+q_(n-1)`. The length-`R_x(q_n-1)` factor beginning at position `1` contains the initial length-`q_n-1` prefix, so that prefix recurs at some positive shift at most `q_n+q_(n-1)`. Since `q_(n-1)<q_n`, this gives `liminf tau_m/m <= 2`.

Interpretation: this supplies the recurrence input for the balanced branch. The prefix recurrence quotient falls below every balanced obstruction threshold, infinitely often.

### Lemma 11e.1x4p: Balanced Ordinary Landing Exclusion

No non-eventually-periodic balanced infinite binary word has a nonnegative ordinary return code or a positive ordinary reduced-gap code.

Status: proved.

Reason: return code `0` is impossible already at a one-block prefix: the binary return residues are `7 mod 8` for digit `0` and `48 mod 128` for digit `1`. Any nonnegative return landing would therefore be positive. After the mechanical convention reduction, the remaining lower mechanical branch has `liminf tau_m/m <= 2` by the Sturmian fast prefix-recurrence lemma. Both obstruction thresholds in the fast prefix-recurrence exclusion criterion are greater than `2` for every `alpha in (0,1)`, so neither a positive return landing nor a positive reduced-gap landing can exist.

Interpretation: Resolved Lemma F is closed for the balanced/Sturmian frontier. The first nonconstant binary obstruction must now be higher-complexity than balanced Sturmian words.

### Lemma 11e.1x4q: Binary Landing Prefix-Recurrence Height Barrier

For any aperiodic infinite binary return word with positive ordinary return code, if `S_N` is the prefix one-count and `tau_m` is a positive recurrence time of the initial length-`m` prefix with `tau_m -> infinity`, then

`3m+4S_m <= tau_m log_2(9/8)+S_(tau_m) log_2(27/16)+O(1)`.

For any aperiodic infinite binary reduced-gap word with positive ordinary gap code, if `K_N` is the prefix one-count and `sigma_m` is a positive recurrence time of the initial length-`m` prefix with `sigma_m -> infinity`, then

`7m+3K_m <= sigma_m log_2(243/128)+K_(sigma_m) log_2(9/8)+O(1)`.

Status: proved as a general recurrence-height barrier.

Reason: when the initial prefix recurs, the shifted ordinary state is congruent to the original landing code modulo the original prefix modulus. Once the prefix modulus exceeds the original code, the shifted state must be at least the modulus, otherwise the congruence would force the shifted state to equal the original code. The critical-series height formula then converts this into the displayed inequality.

Interpretation: after the balanced/Sturmian branch is excluded, any higher-complexity binary landing must have prefix recurrences whose time and early symbol counts are large enough to clear the prefix modulus. This is the next obstruction shape to attack.

### Lemma 11e.1x4r: Binary Density-Recurrence Exclusion Criterion

For an aperiodic infinite binary return word, suppose there are prefix recurrence times `tau_m -> infinity` along infinitely many prefix lengths such that

`limsup tau_m/m <= T`,

`liminf S_m/m >= a`,

and

`limsup S_(tau_m)/tau_m <= b`.

If

`3+4a > T (log_2(9/8)+b log_2(27/16))`,

then the word has no positive ordinary return code.

For the reduced-gap system, under the analogous assumptions on `sigma_m`, `K_m`, and `K_(sigma_m)`, the exclusion condition is

`7+3a > T (log_2(243/128)+b log_2(9/8))`.

Status: proved as a corollary of the binary landing prefix-recurrence height barrier.

Reason: divide the height-barrier inequality by `m` along the recurring prefix lengths. The left side is bounded below by the prefix-density term, and the right side is bounded above by the recurrence-time ratio and the early one-density before the recurrence time. A strict reverse inequality rules out the landing.

Interpretation: this is the current plug-in criterion for higher-complexity binary classes. To exclude a symbolic class, it is enough to prove sufficiently fast prefix recurrences and enough density separation between the original prefix and the early recurrent state.

### Lemma 11e.1x4s: Density-Free Fast Prefix-Recurrence Exclusion

For an aperiodic infinite binary return word, if the initial prefixes recur along infinitely many lengths with recurrence times satisfying

`limsup tau_m/m < 3/log_2(243/128)`,

then the word has no positive ordinary return code.

For an aperiodic infinite binary reduced-gap word, the density-free cutoff is

`limsup sigma_m/m < 7/(log_2(243/128)+log_2(9/8))`.

Status: proved.

Reason: specialize the binary density-recurrence exclusion criterion with the crude universal bounds `a=0` and `b=1`. The return cutoff is approximately `3.244`; the reduced-gap cutoff is approximately `6.394`.

Interpretation: any remaining binary landing must have no infinitely recurring prefix subsequence faster than these absolute ratios, unless sharper density information is used. This gives a density-free recurrence obstruction for higher-complexity classes.

### Lemma 11e.1x4t: Automatic Template Exclusion Examples

The Thue-Morse word and the period-doubling word have no positive ordinary return code and no positive ordinary reduced-gap code.

Status: proved.

Reason: Thue-Morse prefixes of length `2^h` recur at shift `3*2^(h-1)`, so the recurrence ratio is `3/2`. Period-doubling prefixes of length `2^h` recur at shift `2^(h+1)`, so the recurrence ratio is `2`. Both ratios are below the density-free return cutoff `3/log_2(243/128) ~= 3.244` and below the reduced-gap cutoff `7/(log_2(243/128)+log_2(9/8)) ~= 6.394`.

Interpretation: the recurrence criteria now exclude concrete higher-complexity automatic/morphic aperiodic templates, not just balanced Sturmian words.

### Lemma 11e.1x4u: Binary Two-Uniform Morphic Template Exclusion

Every fixed point beginning in `0` of a binary `2`-uniform morphism whose image of `0` begins in `0` has no positive ordinary return code and no positive ordinary reduced-gap code.

Status: proved by finite classification.

Reason: if `phi(0)=00`, the fixed point is all-zero. If `phi(0)=01`, then `phi(1)` is one of `00`, `01`, `10`, or `11`: these give period-doubling, periodic `(01)^infinity`, Thue-Morse, or eventually periodic `0 1^infinity`, respectively. The two aperiodic cases are excluded by Lemma 11e.1x4t, and the periodic/eventually periodic cases are already excluded.

Interpretation: binary `2`-automatic fixed-point templates are harmless. Any automatic obstruction must come from larger uniform morphisms or from codings that avoid fast recurring prefixes.

### Lemma 11e.1x4v: Binary Three-Uniform Morphic Template Exclusion

Every fixed point beginning in `0` of a binary `3`-uniform morphism whose image of `0` begins in `0` has no positive ordinary return code and no positive ordinary reduced-gap code.

Status: proved by finite classification plus the density-free and density-recurrence exclusion criteria.

Reason: `phi(0)` is one of `000`, `001`, `010`, `011`. The all-zero case is periodic. In the `001` and `010` cases, and in the `011` cases where `phi(1)` begins with `0`, the word `phi^2(0)` contains a repeated `0` within positions `1`, `2`, or `3`; hence the prefixes of length `3^h` recur with ratio at most `3`, below both density-free cutoffs. The case `phi(0)=011, phi(1)=111` is eventually periodic. The remaining cases are `phi(1)=100`, `101`, and `110`; these have recurrence ratio at most `4`, `4`, and `5`, respectively, and are excluded by the density-recurrence criterion using one-density limits `1/2` or `2/3`.

For the borderline `phi(1)=100` case, the needed strict inequalities are

`5 > 4(log_2(9/8)+(1/2)log_2(27/16))`

and

`17/2 > 4(log_2(243/128)+(1/2)log_2(9/8))`.

For the `phi(1)=101` and `phi(1)=110` cases, the worst ratio is handled by

`17/3 > 5(log_2(9/8)+(2/3)log_2(27/16))`

and

`9 > 5(log_2(243/128)+(2/3)log_2(9/8))`.

Interpretation: binary `3`-automatic fixed-point templates are also harmless. This is still far from a theorem for all uniform morphisms or all automatic sequences.

### Lemma 11e.1x4w: Binary Four-Uniform Morphic Template Exclusion

Every fixed point beginning in `0` of a binary `4`-uniform morphism whose image of `0` begins in `0` has no positive ordinary return code and no positive ordinary reduced-gap code.

Status: proved by finite classification plus a two-state density recursion.

Reason: if `phi(0)` has a second zero in positions `1`, `2`, or `3`, then prefixes of length `4^h` recur with ratio at most `3`, below both density-free cutoffs. The only nonperiodic late-zero case has `phi(0)=0111` and `phi(1) != 1111`. If `k` is the number of ones in `phi(1)`, then the one-densities of `phi^h(0)` and `phi^h(1)` satisfy a two-state linear recursion and both converge to `p=3/(7-k)`, with `3/7 <= p <= 3/4`. The first repeated zero in `phi^2(0)` occurs by position `7`, so the density-recurrence criterion applies with `T=7` and `a=b=p`.

The required inequalities hold throughout that interval:

`3+4p > 7(log_2(9/8)+p log_2(27/16))`

and

`7+3p > 7(log_2(243/128)+p log_2(9/8))`.

Interpretation: binary `4`-automatic fixed-point templates are also harmless. The proof uses a reusable pattern: early repeated zero gives density-free recurrence; late repeated zero reduces to an explicit density recursion.

### Lemma 11e.1x4x: Binary Five-Uniform Morphic Template Exclusion

Every fixed point beginning in `0` of a binary `5`-uniform morphism whose image of `0` begins in `0` has no positive ordinary return code and no positive ordinary reduced-gap code.

Status: proved by finite classification plus two-state density recursions and one overlap recurrence.

Reason: if `phi(0)` has a second zero in positions `1`, `2`, or `3`, prefixes of length `5^h` recur with ratio at most `3`, below both density-free cutoffs. Thus only `phi(0)=01110` and `phi(0)=01111` remain.

For `phi(0)=01110`, prefixes recur with ratio `4`. If `k` is the number of ones in `phi(1)`, then the one-densities of `phi^h(0)` and `phi^h(1)` converge to

`p = 3/(8-k)`, with `3/8 <= p <= 1`.

The density-recurrence criterion applies with `T=4` and `a=b=p`; the endpoint inequalities are

`9/2 > 4(log_2(9/8)+(3/8)log_2(27/16))`

and

`65/8 > 4(log_2(243/128)+(3/8)log_2(9/8))`.

For `phi(0)=01111`, the all-one image `phi(1)=11111` is eventually periodic. Otherwise the density limit is

`p = 4/(9-k)`, with `4/9 <= p <= 4/5`.

If the first zero of `phi(1)` occurs before the last position, the repeated prefix ratio is at most `8`, and the density-recurrence criterion applies with endpoint inequalities

`31/5 > 8(log_2(9/8)+(4/5)log_2(27/16))`

and

`25/3 > 8(log_2(243/128)+(4/9)log_2(9/8))`.

The final late-zero case `phi(1)=11110` is handled by an overlap: `phi^2(0)` contains `phi(0)=01111` again at position `9`, so prefixes of length `5^h` recur with ratio `9/5`, below both density-free cutoffs.

Interpretation: binary `5`-uniform fixed-point templates are now theorem-level excluded. The q=5 diagnostic remains useful as a finite check, but the paper no longer relies on it as only sampled evidence.

### Lemma 11e.1x4y: Binary Six-Uniform Morphic Template Exclusion

Every fixed point beginning in `0` of a binary `6`-uniform morphism whose image of `0` begins in `0` has no positive ordinary return code and no positive ordinary reduced-gap code.

Status: proved by finite classification plus symbolic-prefix recurrence witnesses.

Reason: early repeated zero positions `1`, `2`, and `3` are density-free. If `phi(0)` has a zero in position `4` or `5`, prefixes recur with ratio at most `5`, and the density limit `p` lies in `[1/3,1]`; the endpoint inequalities

`13/3 > 5(log_2(9/8)+(1/3)log_2(27/16))`

and

`8 > 5(log_2(243/128)+(1/3)log_2(9/8))`

exclude the case.

The only remaining image is `phi(0)=011111`. If `phi(1)=111111`, the fixed point is eventually periodic. Otherwise, let `j` be the first zero position in `phi(1)` and let `k` be the number of ones, giving density limit `p=5/(11-k)`.

- `j<=1`: the prefix block recurs with ratio at most `7`, and `5/11 <= p <= 5/6`.
- `j=2,k<=4`: the prefix block recurs with ratio `8`, and `5/9 <= p <= 5/7`.
- `j=2,k=5`: the symbolic prefix `01` recurs at position `8`, so prefixes of length `2*6^h` recur with ratio `4`.
- `j>=3`: the symbolic prefix `01` recurs by position `11`, so prefixes of length `2*6^h` recur with ratio at most `11/2`.

The endpoint inequalities in Sections 6--8 verify the density-recurrence criterion in each case.

Verifier: `explorations/explore78_uniform_morphism_symbolic_witness.py` enumerates all `2048` binary `6`-uniform morphisms prolongable on `0`; all are covered by periodicity, density-free symbolic recurrence, or asymptotic density recurrence. The weakest margins are still positive: return `0.184`, gap `0.513`.

Interpretation: the old q=6 power-length diagnostic was a false boundary. Some cases fail at pure lengths `6^h`, but longer symbolic prefixes such as `2*6^h` recur fast enough to exclude them.

Diagnostic extension beyond the proved range:

- `python3 explorations/explore78_uniform_morphism_symbolic_witness.py --q 7 --search-length 8192` covers all `8192` binary `7`-uniform morphisms; weakest return margin `0.111`, weakest gap margin `0.422`.
- `python3 explorations/explore78_uniform_morphism_symbolic_witness.py --q 8 --search-length 8192` covers all `32768` binary `8`-uniform morphisms; weakest return margin `0.055`, weakest gap margin `0.367`.
- `python3 explorations/explore78_uniform_morphism_symbolic_witness.py --q 9 --max-prefix-symbols 18 --search-length 40000` covers all return cases and all but one gap case. The remaining gap-side diagnostic case is `0->011111111, 1->100000000`, whose best symbolic witness up to length `18` is `c=2`, `tau=17`, `T=17/2`, density limit `p=1/2`, and gap margin about `-0.083`.
- `python3 explorations/explore79_q9_boundary.py` targets that residual case with a Z-array recurrence scan through symbolic prefix length `50,000`; all first recurrences are found in the default search window, no gap-success witness appears, and the best gap margin remains the `c=2`, `tau=17` witness.
- `python3 explorations/explore80_q9_boundary_residues.py` follows the same fixed point, equivalently the parity of the number of nonzero base-9 digits, and checks growth of the actual reduced-gap prefix residues through fixed milestones. This supports the no-landing expectation for this template, but it is still finite diagnostic evidence.

Interpretation: the symbolic-prefix method plausibly extends beyond the theorem-level hand classifications, but q=9 exposes a real next boundary for the reduced-gap criterion. Closing that specific morphism would need either a sharper recurrence subsequence, an improved density estimate, or a different landing argument.

### Lemma 11e.1x5: Binary Return Balanced-Frontier Criterion

Let `mu_L^bal` be the least return-prefix residue among balanced binary return words of length `L`.

Then `mu_L^bal -> infinity` if and only if there is no non-eventually-periodic balanced infinite binary return word whose return code is a nonnegative ordinary integer.

Status: proved as an exact criterion.

Reason: balanced finite words form a prefix-closed class. If the balanced minima are bounded, prefix-language compactness gives an infinite ordinary return code whose every finite prefix is balanced, hence whose infinite word is balanced. The periodic exclusion removes the eventually periodic case, leaving exactly a non-eventually-periodic balanced ordinary code. The converse is immediate from eventual equality of prefix residues to any represented ordinary integer.

Interpretation: this isolated the minimal-complexity binary frontier. The later Sturmian fast prefix-recurrence argument removes the irrational-slope balanced return obstruction class.

### Lemma 11e.1x6: Binary Return Balanced Sublinear-Symbol Divergence

Fix a symbol `a in {0,1}` and a function `f(n)=o(n)`. Among balanced binary return words whose every length-`n` factor contains at most `f(n)` occurrences of `a`, the least return-prefix residues tend to infinity along the lengths where this class is nonempty.

Status: proved.

Reason: the class is prefix-closed. Bounded restricted minima would give an infinite balanced ordinary return code by prefix-language compactness. The sublinear factor count contradicts the balanced aperiodic positive-density lemma unless the word is eventually periodic, and periodic return itineraries are already excluded.

Interpretation: balanced return obstructions cannot have density-zero windows in either symbol, even when the sparse symbol count tends to infinity.

### Lemma 11e.1y: Binary Return Fixed-Height Duality

For `B >= 0`, let `H_R(B)` be the largest return-prefix length that can be realized with least residue at most `B`.

Then:

`H_R(B) < L` iff `mu_L > B`.

Consequently, the binary return system has no nonnegative ordinary infinite return code if and only if `H_R(B)` is finite for every fixed `B`.

Status: proved.

Interpretation: the return obstruction can be attacked either by proving `mu_L -> infinity` or by proving every fixed height bound has finite survival depth.

### Lemma 11e.1z: Binary Return Height Scale Lower Bound

The global return minima and fixed-height survival depths satisfy:

`mu_L <= 8^L - 1`, and `H_R(8^L - 1) >= L`.

Consequently, any upper bound `H_R(B) <= c log2(B+1) + O(1)` must have `c >= 1/3`.

Status: proved.

Interpretation: the desired fixed-height theorem, if true, can be logarithmic at best. The all-zero return branch gives the sharp base obstruction.

### Lemma 11e.1za: Binary Return Counting Criterion

Let `N_R(B,L)` count length-`L` return words whose least prefix residue is at most `B`.

If there are constants `C > 0` and `0 < rho < 1` such that:

`N_R(B,L) <= C(B+1) rho^L`

for every `B,L`, then:

`H_R(B) <= ceil(log_{1/rho}(C(B+1)))`.

Status: proved as a conditional criterion.

Interpretation: a uniform prefix-counting discrepancy theorem would prove the fixed-height theorem. The natural density heuristic suggests `rho = 2/15`, but the needed uniform finite-height discrepancy bound is not yet proved.

### Lemma 11e.1zb: Binary Return Counting Rate Lower Bound

Any prefix-counting bound:

`N_R(B,L) <= C(B+1) rho^L`

holding for all `B,L` with fixed `C > 0` must have:

`rho >= 1/8`.

Status: proved.

Reason: the all-zero return word gives `N_R(8^L - 1, L) >= 1`, so `1 <= C(8rho)^L` for every `L`.

Interpretation: the natural density value `rho = 2/15` is only slightly above the worst finite-height obstruction `1/8`; a counting proof must be close to sharp.

### Lemma 11e.1zc: Binary Return Start-Count Formula

Let `A_R(B,L)` count ordinary starts `0 <= n <= B` whose binary return partial-map orbit is defined for at least `L` return blocks. For a return word `w`, let `R_w` be its least prefix residue and let `Q_w` be its prefix modulus.

Then:

`A_R(B,L) = sum_{|w|=L, R_w <= B} (floor((B - R_w)/Q_w) + 1)`.

In particular:

`N_R(B,L) <= A_R(B,L) <= N_R(B,L) + (B+1)(2/15)^L`.

Status: proved.

Interpretation: `N_R` counts nonempty prefix residue classes, while `A_R` counts all ordinary starts in those classes. The difference is controlled by the exact reciprocal-modulus density sum, so a prefix-counting bound is essentially the same obstruction as an ordinary-start counting bound.

### Lemma 11e.1zd: Binary Return Start/Prefix Counting Equivalence

For every `rho` with `2/15 <= rho < 1`, a uniform bound

`N_R(B,L) <= C(B+1)rho^L`

implies

`A_R(B,L) <= (C+1)(B+1)rho^L`.

Conversely, the same bound for `A_R` immediately implies the same bound for `N_R`.

Status: proved.

Interpretation: at the natural density rate, it is enough to prove either the prefix-residue counting theorem or the ordinary-start survival theorem. They differ only by a constant in the bound.

### Lemma 11e.1ze: Binary Return Critical-Height Reduction

For fixed level `L`, cutoff `B_max`, and rate `rho > 0`, the maximum of

`N_R(B,L) / ((B+1)rho^L)`

over `0 <= B <= B_max` occurs at a critical height `B = R_w`, the least prefix residue of some length-`L` return word, unless no such residue is below `B_max`.

Status: proved.

Reason: between consecutive realized least prefix residues, `N_R(B,L)` is constant while `B+1` increases.

Interpretation: the uniform discrepancy theorem can be checked, or attacked, on realized residue heights rather than all integer heights.

### Lemma 11e.1zf: Binary Return Critical-Rank Criterion

For a length-`L` return word `w`, define its critical rank by:

`rank_R(w) = N_R(R_w,L)`.

Then a uniform estimate

`N_R(B,L) <= C(B+1)rho^L`

for all `B,L` is equivalent to:

`rank_R(w) <= C(R_w+1)rho^L`

for every finite return word `w`.

Status: proved.

Interpretation: the return discrepancy theorem is exactly a rank-versus-height theorem for sorted least prefix residues.

### Lemma 11e.1v: Binary Return Forced-Orbit Prefix Equivalence

Fix a nonnegative depth-`0` parameter `M`. The binary return partial map is defined for the first `L` forced return blocks, with forced word `(r_0, ..., r_{L-1})`, if and only if `M` satisfies every prefix congruence:

`M ≡ R_N (mod Q_N)` for `1 <= N <= L`.

Once `Q_N > M`, this is equivalent to `R_N = M`.

Status: proved.

Interpretation: direct forced-orbit scans and return-prefix residue stabilization are the same finite test, written in different coordinates.

### Lemma 11e.1a: Binary Return-Prefix Digit Recurrence

For a finite return prefix, write:

`Q_N n_N = P_N n_0 + D_N`,

and let `R_N` be the least prefix residue. Define:

`U_N = (P_N R_N + D_N) / Q_N`.

For the next return length `r_N`, put:

`p_N = P_(r_N)`, `q_N = Q_(r_N)`, `d_N = D_(r_N)`.

If:

`R_(N+1) = R_N + e_N Q_N`, with `0 <= e_N < q_N`,

then:

`e_N ≡ - (p_N U_N + d_N) * (p_N P_N)^(-1) (mod q_N)`.

In particular, `e_N = 0` iff:

`p_N U_N + d_N ≡ 0 (mod q_N)`.

Status: proved.

Interpretation: return-prefix residues are nondecreasing, and the next base-`q_N` digit is controlled by the auxiliary return state `U_N`.

### Lemma 11e.1b: Binary Return Zero-Increment Tail Equivalence

Fix a finite return prefix and define `U_N` as above. For any return-length suffix `(r_N, r_{N+1}, ...)`, a run of zero prefix increments:

`e_N = e_{N+1} = ... = e_{N+L-1} = 0`

is equivalent to the existence of positive integers `U_{N+1}, ..., U_{N+L}` satisfying:

`Q_(r_j) U_{j+1} = P_(r_j) U_j + D_(r_j)`.

Consequently, an eventually constant return-prefix residue tail is equivalent to an infinite positive orbit of the same binary return-block map, starting from the auxiliary state `U_N`.

Status: proved.

Interpretation: the digit recurrence is not an easier independent problem. It restates the same positive-integer return obstruction in an auxiliary coordinate.

### Lemma 11e.1c: Binary Return Landing Growth Envelope

Suppose an infinite return-length word `(r_0, r_1, ...)` has positive ordinary return code `n_0 = M`. Put:

`S_N = r_0 + ... + r_{N-1}`.

Then:

`n_N = (P_N / Q_N) * (M - M_N)`,

where `M_N` is the return critical-series partial sum. In particular:

`n_N <= (M + 1) * (9/8)^N * (27/16)^(S_N)`.

If the next return length is `r_N`, then:

`5 * 16^(r_N) <= 33(M + 1)(9/8)^N(27/16)^(S_N) + 32`.

Status: proved.

Interpretation: positive return-code landings force a growth envelope. Return words with spikes larger than this envelope cannot be positive-integer obstructions.

### Lemma 11e.1d: Binary Return Spike Exclusion

Let `(r_0, r_1, ...)` be an infinite return-length word and put:

`S_N = r_0 + ... + r_{N-1}`.

If:

`sup_N 16^(r_N) / ((9/8)^N (27/16)^(S_N)) = infinity`,

then this word has no positive ordinary return code.

Status: proved.

Interpretation: an unbounded return-length obstruction, if it exists, cannot be made of isolated spikes that outgrow the accumulated real expansion. It must be balanced against the previous return-length sum.

### Lemma 11e.2: Binary Return Reparameterization

For a binary-depth continuation at a depth-`0` state `n_j`, let the next return block be:

`0 -> 1^(r_j) -> 0`.

Define:

- `epsilon_j = 7` if `r_j` is even
- `epsilon_j = 5` if `r_j` is odd
- `w_j` by `33n_j + 32 = 16^(r_j) w_j`

Then `w_j` is a positive odd integer with `w_j ≡ epsilon_j (mod 8)`, and:

`16^(r_j) w_j ≡ 32 (mod 33)`.

Thus for each fixed `r_j`, the reparameterized variable `w_j` lies in one residue class modulo `264`.

`n_{j+1} = (3 * 27^(r_j) * w_j - 85) / 88`.

If the following return block has length `r_{j+1}`, then:

`9 * 27^(r_j) * w_j + 1 = 2^(4r_{j+1}+3) w_{j+1}`.

Status: proved.

Interpretation: the binary-depth obstruction can be rewritten as an infinite positive-integer recurrence in the return variables `(r_j, w_j)`. This is not a proof of termination, but it removes the affine denominator from one layer of the problem and exposes the exact valuation condition that selects the next return length.

### Lemma 11e.3: Binary Return Partial Map

A finite binary return block starting at a depth-`0` parameter `n` exists exactly when:

`33n + 32 = 16^r w`

for some `r >= 0` and odd `w` satisfying:

- `w ≡ 7 (mod 8)` if `r` is even
- `w ≡ 5 (mod 8)` if `r` is odd

In that case the block is `0 -> 1^r -> 0`, and the next depth-`0` return parameter is:

`T(n) = (3 * 27^r * w - 85) / 88`.

Status: proved.

Consequently, any positive-integer binary-depth obstruction with infinitely many depth-`0` states is exactly an infinite positive orbit of this partial map.

### Lemma 11e.3a: Binary Return Backward Branch Formula

Fix a terminal depth-`0` return state `n'` and a return length `r >= 0`. With:

`P_r = 9 * 27^r`, `Q_r = 2^(4r+3)`,

and additive term `D_r`, a state `n` maps to `n'` through a return block of length `r` if and only if:

`n = (Q_r n' - D_r) / P_r`

is a nonnegative integer.

Status: proved.

Interpretation: each fixed return length contributes at most one backward preimage of a terminal state. The return rank problem can therefore be viewed as a backward preimage-tree counting problem over possible return lengths.

### Lemma 11e.3b: Binary Return Backward Length Bound

If a terminal depth-`0` return state `n'` has a backward preimage through a return block of length `r`, then:

`(27/16)^r <= (88n' + 85) / 96`.

Status: proved.

Interpretation: only logarithmically many return lengths can occur as backward branches into a fixed terminal state.

### Lemma 11e.3b1: Binary Return Backward 3-adic Gate

For fixed terminal state `n'` and return length `r`, the backward branch formula is integral if and only if:

`88n' + 85 = 3^(3r+1) u`, with `u ≡ 2 (mod 3)`.

Consequently, a terminal state has at most one backward return preimage across all return lengths.

Status: proved.

Interpretation: the return partial map is injective on its domain. The return rank problem is therefore not caused by forward merging.

### Lemma 11e.3b2: Binary Return Prefix Terminal Injectivity

At a fixed length `L`, two realized binary return prefixes that land at the same terminal depth-`0` state have the same return word and the same initial residue.

Status: proved.

Interpretation: finite return-prefix clustering is not caused by forward merging. It is a sorted-residue/rank phenomenon among distinct terminal states.

### Lemma 11e.3c: Binary Return Backward Contraction

If `n` maps to `n'` through a return block of length `r`, then:

`n < (8/9)(16/27)^r n'`.

Status: proved.

Interpretation: every valid positive backward return branch strictly decreases height, and longer return labels decrease it faster.

### Lemma 11e.3d: Binary Return Backward Path Contraction

If a depth-`L` backward return path has return word `(r_0, ..., r_{L-1})` and total return length `S_L`, then:

`n_0 < (8/9)^L (16/27)^S_L n_L`.

Status: proved.

Interpretation: backward return trees contract exponentially in both block count and total return length.

### Lemma 11e.3d1: Binary Return Terminal Escape

If a positive state `n_0` survives `L` return blocks with total return length `S_L` and terminal state `n_L`, then:

`n_L > (9/8)^L (27/16)^S_L n_0`.

Status: proved.

Interpretation: the forward return process forces exponential terminal-height escape along every surviving path.

### Lemma 11e.3d2: Binary Return Terminal Window

For a finite return word `w`, let:

`E_w = P_w/Q_w = (9/8)^L(27/16)^S_w`,

let `M_w = -D_w/P_w` be its critical-series partial sum, let `R_w` be its least prefix residue, and let `U_w` be the terminal state reached from `R_w`. Then:

`U_w = E_w(R_w - M_w)`, with `R_w <= U_w/E_w < R_w + 1`.

In particular, `R_w = floor(U_w/E_w)`.

Consequently, `R_w <= B` implies `U_w < E_w(B+1)`.

Status: proved.

Interpretation: low return-prefix residues correspond to normalized terminal states in a fixed-width window. The remaining stopping-time problem is to count such terminal windows uniformly.

### Lemma 11e.3d2a: Binary Return Terminal Depth Bound

If a nonempty return word `w` has length `L`, expansion factor `E_w`, and terminal state `U_w`, then:

`U_w >= E_w >= (9/8)^L`.

Consequently:

`L <= log_{9/8}(U_w)`.

Status: proved.

Reason: the least return-prefix residue of a nonempty word is positive. The terminal-window identity gives `U_w/E_w >= R_w >= 1`, and every return block expands by at least `9/8`.

Interpretation: a fixed return terminal state can only appear at logarithmically bounded prefix depth. This rules out infinite depth at one terminal value; the unresolved rank problem is breadth across many terminals and expansion scales.

### Lemma 11e.3d3: Binary Return Terminal-Window Counting Equivalence

With the notation of Lemma 11e.3d2:

`R_w <= B` if and only if `U_w/E_w < B+1`.

Consequently:

`N_R(B,L) = #{w: |w|=L, U_w/E_w < B+1}`.

Status: proved.

Interpretation: the return critical-rank problem is exactly a window-counting problem for normalized terminal heights.

### Lemma 11e.3d3a: Binary Return Expansion Pressure

For every `theta > 0` and every return-prefix length `L`,

`sum_(|w|=L) E_w^(-theta) = (((8/9)^theta) / (1 - (16/27)^theta))^L`,

where `E_w = (9/8)^L (27/16)^(sum_j r_j)` is the return expansion factor.

This pressure decays exponentially in `L` exactly when:

`(8/9)^theta + (16/27)^theta < 1`.

The threshold root is approximately `2.56743`; in particular, cubic pressure decays.

Status: proved.

Interpretation: high-moment expansion-weighted word mass is subcritical. This is useful analytic structure for a stopping-time proof, but it is not by itself a rank bound because it does not separate terminal states in the low normalized window.

### Lemma 11e.3d4: Binary Return Normalized Stopping-Time Criterion

Let `W_R(B,L)` count length-`L` return words whose normalized terminal state satisfies:

`U_w/E_w < B+1`.

If there are constants `C > 0` and `0 < rho < 1` such that:

`W_R(B,L) <= C(B+1)rho^L`

for every `B,L`, then:

`H_R(B) <= ceil(log_{1/rho}(C(B+1)))`.

Status: proved as a conditional criterion.

Interpretation: the missing return estimate can be stated entirely as a normalized terminal-window stopping-time bound. By Lemma 11e.3d3 this is equivalent to the prefix-counting criterion.

### Lemma 11e.3d5: Binary Return Terminal-Rank Criterion

For a length-`L` return word `w`, let `trank_R(w)` be the number of length-`L` return words `v` satisfying:

`floor(U_v/E_v) <= floor(U_w/E_w)`.

A uniform estimate:

`W_R(B,L) <= C(B+1)rho^L`

for all `B,L` is equivalent to:

`trank_R(w) <= C(floor(U_w/E_w)+1)rho^L`

for every finite return word `w`.

Status: proved.

Interpretation: the return rank obstruction can be stated entirely in normalized terminal coordinates.

### Lemma 11e.3d5a: Binary Return Weighted Terminal-Window Bound

For every `theta > 1`, every `B >= 0`, and every `L >= 1`,

`sum_(|w|=L, R_w <= B) E_w^(-theta) <= (B+1)^theta zeta(theta)`.

Status: proved.

Reason: low return windows satisfy `U_w < E_w(B+1)`, hence `E_w^(-theta) <= (B+1)^theta U_w^(-theta)`. Return prefix terminal injectivity makes the terminal states `U_w` distinct positive integers, so the sum of `U_w^(-theta)` is at most `zeta(theta)`.

Interpretation: this gives a rigorous weighted version of the terminal-window estimate. It still does not prove the rank bound, because very large expansion factors can make many words carry tiny inverse-expansion weights.

### Lemma 11e.3d5b: Binary Return Low-Expansion Window Count

For every expansion cutoff `X >= 1`, `B >= 0`, and `L >= 1`,

`#{w: |w|=L, R_w <= B, E_w <= X} <= ceil(X(B+1)) - 1`.

Status: proved.

Reason: the terminal window gives `U_w < E_w(B+1) <= X(B+1)`, and return terminal states are distinct at fixed prefix length.

Interpretation: the low-expansion part of the return low window is linearly bounded in the cutoff. The hard remainder consists of low-window words with large expansion factors.

### Lemma 11e.3d5c: Binary Return Weighted Expansion-Shell Count

Let `W_R(B,L;s)` count length-`L` return words satisfying `R_w <= B` and `2^s <= E_w < 2^(s+1)`. For every `theta > 1`,

`W_R(B,L;s) <= 2^(theta(s+1)) (B+1)^theta zeta(theta)`.

Status: proved.

Reason: each word in shell `s` contributes more than `2^(-theta(s+1))` to the inverse-expansion mass, and the return weighted terminal-window bound controls that mass.

Interpretation: weighted control gives an ordinary count on each fixed expansion shell. The price grows with the shell index, so high shells still require new arithmetic separation.

### Lemma 11e.3d5d: Binary Return Expansion-Shell Depth Bound

If a length-`L` return word satisfies `2^s <= E_w < 2^(s+1)`, then:

`L < log_{9/8}(2^(s+1))`.

Status: proved.

Reason: every return block has expansion at least `9/8`, so `(9/8)^L <= E_w < 2^(s+1)`.

Interpretation: every fixed return expansion shell only contributes to bounded prefix depths. Infinite-depth obstructions must move through arbitrarily high shells.

### Lemma 11e.3d6: Binary Return Terminal Start-Count Formula

Let `A_R(B,L)` count ordinary starts `0 <= n <= B` whose binary return partial-map orbit is defined for at least `L` return blocks. Then:

`A_R(B,L) = sum_{|w|=L, floor(U_w/E_w) <= B} (floor((B - floor(U_w/E_w))/Q_w) + 1)`.

Status: proved.

Interpretation: ordinary-start survival can also be counted directly from normalized terminal coordinates. The terminal formulation is therefore not just a rank restatement; it controls the ordinary survivor count as well.

### Lemma 11e.3d7: Binary Return Terminal Boundedness Criterion

Fix an infinite return-length word and let `w_N` be its length-`N` prefix. Let `E_N` and `U_N` be the expansion factor and terminal state associated to `w_N` and its least prefix residue. Then the selected `2`-adic return code is a nonnegative ordinary integer if and only if:

`floor(U_N/E_N)`

is bounded as `N -> infinity`.

Equivalently, this happens if and only if `floor(U_N/E_N)` is eventually constant.

Status: proved.

Interpretation: the return-code landing problem can be stated entirely as divergence of rounded normalized terminal coordinates.

### Lemma 11e.3d8: Binary Return Terminal Monotonicity

For an infinite return-length word, let `T_N = floor(U_N/E_N)` be the rounded normalized terminal coordinate of the length-`N` prefix. If the next return block has modulus `q_N = 2^(4r_N+3)` and the current prefix modulus is `Q_N`, then:

`T_{N+1} = T_N + e_N Q_N`, with `0 <= e_N < q_N`.

Consequently `T_N` is nondecreasing, and it is eventually constant if and only if `e_N = 0` for all sufficiently large `N`.

Status: proved.

Interpretation: the return obstruction is now a zero-increment tail problem for a nondecreasing sequence of rounded normalized terminal coordinates.

### Lemma 11e.3d8a: Binary Return Terminal Zero-Step Criterion

Fix a finite return prefix with auxiliary terminal state `U_N`. For a proposed next return length `r`, with one-block data `p=P_r`, `q=Q_r`, and `d=D_r`, the next rounded terminal increment is zero if and only if:

`p U_N + d == 0 (mod q)`.

In that case:

`U_{N+1} = (p U_N + d)/q`,

so the auxiliary terminal state itself takes the same return-block step of length `r`. Consequently, at most one next return length can give a zero terminal increment.

Status: proved.

Interpretation: zero terminal increments are locally forced by the auxiliary terminal state.

### Lemma 11e.3d8b: Binary Return Terminal Zero-Increment Congruence

Fix a finite return prefix with auxiliary terminal state `U_N`. For a finite return-length suffix `v`, let `R_v` and `Q_v` be the least prefix residue and modulus of `v` as a standalone return word. Then the rounded return terminal coordinate has zero increments through the whole suffix `v` if and only if:

`U_N == R_v (mod Q_v)`.

Status: proved.

Interpretation: finite zero-increment return tails are exactly ordinary return prefix congruences imposed on the auxiliary terminal state.

### Lemma 11e.3d8c: Binary Return Terminal Self-Shadowing Criterion

Fix a finite return prefix with auxiliary terminal state `U_N` and an infinite return-length suffix `v`. For `L >= 1`, let `R_{v,L}` and `Q_{v,L}` be the least prefix residue and modulus of the first `L` blocks of `v`, considered as a standalone return word. Then the rounded return terminal coordinate has zero increments along the whole suffix `v` if and only if:

`U_N == R_{v,L} (mod Q_{v,L})` for every `L >= 1`.

Equivalently, `U_N` is the positive ordinary return code selected by the suffix `v`.

Status: proved.

Interpretation: an infinite return terminal obstruction is a self-shadowing condition: the auxiliary terminal state must lie in every nested prefix class of the future suffix.

### Lemma 11e.3d8d: Binary Return Shift-Code Recurrence

Suppose an infinite return-length word `v=(r_0,r_1,...)` has positive ordinary return code `X_0`. Let `X_j` be the state after the first `j` return blocks. Then `X_j` is the positive ordinary return code of the shifted suffix `(r_j,r_{j+1},...)`, and:

`Q_{r_j} X_{j+1} = P_{r_j} X_j + D_{r_j}`.

In particular:

`X_L > (9/8)^L (27/16)^(r_0+...+r_{L-1}) X_0`.

Status: proved.

Interpretation: a self-shadowing return obstruction carries positive ordinary codes for every shifted suffix, forming the same expanding return orbit.

### Lemma 11e.3d8e: Binary Return Terminal Zero-Increment Cylinder Density

For a finite return-length suffix `v=(r_0, ..., r_{L-1})` with modulus:

`Q_v = product_i 2^(4r_i+3)`,

the set of nonnegative auxiliary states whose rounded return terminal coordinate has zero increments through `v` is one residue class modulo `Q_v`, and therefore has natural density `1/Q_v`.

For a fixed infinite return-length suffix, the set of `2`-adic auxiliary states that shadow the whole suffix is a single `2`-adic point and has Haar measure zero.

Status: proved.

Interpretation: every fixed infinite terminal-zero suffix is measure-zero in the auxiliary state, but measure zero still does not rule out one positive ordinary integer.

### Lemma 11e.3d8f: Binary Return Terminal Zero-Increment Survival Density

Among nonnegative auxiliary states `U`, the natural density of states admitting at least `L` consecutive rounded return terminal zero-increments is:

`(2/15)^L`.

Status: proved.

Interpretation: the terminal zero-increment obstruction has the same exact exponential density decay as ordinary binary return survival. This remains density information, not a pointwise exclusion.

### Lemma 11e.3d8f1: Bounded Binary Return Terminal Zero-Increment Survival Density

Among nonnegative auxiliary states `U`, the natural density of states whose next `L` rounded return terminal increments are zero and whose corresponding return lengths all satisfy `0 <= r <= R` is:

`((2/15)(1 - 16^(-(R+1))))^L`.

Status: proved.

Interpretation: bounded-alphabet terminal zero-increment tails have the same exact restricted density as bounded ordinary return survival.

### Lemma 11e.3d8g: Finite Binary Return Terminal Zero-Increment Words Are Locally Realizable

For every finite sequence of return lengths `(r_0, ..., r_{L-1})`, there are infinitely many positive auxiliary states `U_0` for which the rounded return terminal coordinate has zero increments through exactly this finite sequence.

Status: proved.

Interpretation: no proof can rule out return terminal obstructions by forbidding a finite zero-increment suffix pattern. The obstruction is genuinely infinite.

### Lemma 11e.3d9: Binary Return Terminal Zero-Increment Equivalence

Fix a finite return prefix and put `T_N = floor(U_N/E_N)`. For any return-length suffix, an eventually constant tail:

`T_N, T_{N+1}, T_{N+2}, ...`

is equivalent to an infinite positive orbit of the binary return-block map starting from the auxiliary state `U_N`.

Status: proved.

Interpretation: the terminal-coordinate obstruction is exactly the original infinite positive return-orbit obstruction, restarted from the auxiliary terminal state.

### Lemma 11e.3d10a: Binary Return Terminal Zero-Increment Tail Uniqueness

Fix a finite return prefix and its auxiliary terminal state `U_N`. There is at most one infinite return-length suffix for which all later rounded terminal increments are zero.

Status: proved.

Interpretation: after any finite prefix, the zero-increment terminal tail, if it exists, is forced by the auxiliary terminal state.

### Lemma 11e.3d10: Binary Return Terminal Zero-Increment Escape

Fix a finite return prefix and suppose the next `L` return-prefix increments are zero. If the zero-increment suffix has return lengths `(r_N, ..., r_{N+L-1})` and total `S`, then:

`U_{N+L} > (9/8)^L (27/16)^S U_N`.

Status: proved.

Interpretation: a constant rounded terminal coordinate does not mean the auxiliary terminal state is stationary. Any zero-increment tail is an expanding positive orbit in the auxiliary coordinate.

### Lemma 11e.3d11: No Eventually Periodic Binary Return Terminal Tail

No eventually periodic return-length suffix can make the rounded return terminal coordinate eventually constant.

Status: proved.

Interpretation: any return terminal obstruction must have a genuinely nonperiodic zero-increment suffix.

### Lemma 11e.3e: Binary Return Backward Cubic-Mass Contraction

For every terminal return state `n'`:

`sum_{n: T(n)=n'} n^3 <= (8/9)^3 (n')^3 < (n')^3`.

Status: proved.

Interpretation: the full immediate backward return map is a strict contraction for cubic mass.

### Lemma 11e.3f: Binary Return Backward Moment Contraction

For every real `theta > 0` and every terminal return state `n'`:

`sum_{n: T(n)=n'} n^theta <= (8/9)^theta (n')^theta`.

Status: proved.

Interpretation: return backward fibers contract every positive power moment.

### Lemma 11e.4: Binary Return `y`-Normal Form

Put:

`y_j = 33n_j + 32`.

If the `j`-th binary return block has length `r_j`, then:

`y_j = 16^(r_j) w_j`,

with `w_j` odd, and:

`8 y_{j+1} = 9 * 27^(r_j) w_j + 1`.

Equivalently:

`8 * 16^(r_j) y_{j+1} = 9 * 27^(r_j) y_j + 16^(r_j)`.

Consequently:

`y_{j+1} > y_j`,

and for any `N` consecutive return blocks:

`y_N >= (9/8)^N * (27/16)^(r_0 + ... + r_{N-1}) * y_0`.

Status: proved.

Interpretation: this is the cleanest real-growth normal form for the binary return dynamics. It gives a height function that strictly increases on every return, but it still does not prove termination because an exceptional orbit could grow forever while satisfying the dyadic gates.

### Lemma 11e.5: All-Zero Binary Return Branch

A depth-`0` parameter `n_0` has first `L` binary return blocks all of length `0` if and only if:

`n_0 ≡ -1 (mod 8^L)`.

The least nonnegative such start is:

`n_0 = 8^L - 1`,

and along this branch:

`n_i = 9^i * 8^(L-i) - 1`.

The infinite all-zero binary return code is `n_0 = -1`, not a nonnegative integer.

Status: proved.

Interpretation: this explains the long all-zero shadows found by the binary partial-map scan. They converge 2-adically to the negative code `-1`, not to a positive obstruction.

### Lemma 11e.5a: Constant Binary Return Branch

Fix a return length `r >= 0`, and let `P_r, Q_r, D_r` be the one-block return data. A depth-`0` parameter `n_0` has first `L` return blocks all equal to `r` if and only if:

`n_0 ≡ -D_r / (P_r - Q_r) (mod Q_r^L)`,

equivalently:

`(P_r - Q_r)n_0 ≡ -D_r (mod Q_r^L)`.

The infinite constant-`r` return code is:

`n_* = -D_r / (P_r - Q_r)`,

which lies in `[-1, 0)` and hence is not a nonnegative integer.

Status: proved.

Interpretation: every one-letter return alphabet has arbitrarily long finite shadows, but its infinite 2-adic code is a negative rational. The remaining bounded-alphabet case must use at least two symbols and be nonperiodic.

### Lemma 11e.6: Binary Return-Length Height Bound

If a depth-`0` parameter `n` begins a finite binary return block:

`0 -> 1^r -> 0`,

then:

`n >= (5 * 16^r - 32) / 33`.

Equivalently:

`r <= (log2(33n + 32) - log2(5)) / 4`.

Status: proved.

Interpretation: long binary return blocks require exponentially large current return states. This does not rule out an infinite obstruction, because return states strictly increase, but it cleanly separates bounded-return-length obstructions from rapidly growing unbounded-return-length obstructions.

### Lemma 11e.7: Finite Binary Return Words Are Realizable

For every finite sequence of return lengths:

`(r_0, ..., r_{L-1})`,

there are infinitely many nonnegative depth-`0` parameters `n_0` whose binary return itinerary begins with exactly this sequence.

Status: proved.

Reason: the return-block coding proposition gives one congruence class modulo `prod_j 2^(4r_j+3)`. Every nonnegative member of that arithmetic progression realizes the finite word, and the progression is infinite.

Interpretation: no proof of the `T = 1` case can rely on forbidding a finite return pattern. The obstruction is genuinely infinite.

### Lemma 11e.7a: Periodic Binary Return Branch

Let `w=(r_0, ..., r_{p-1})` be a nonempty finite return word, and write its one-period affine data as:

`Q_w n_p = P_w n_0 + D_w`.

For `L >= 1`, let `w^L` denote `L` repetitions of `w`. A depth-`0` parameter `n_0` realizes the return word `w^L` if and only if:

`n_0 ≡ n_w^* (mod Q_w^L)`,

where:

`n_w^* = -D_w / (P_w - Q_w)`.

Equivalently:

`(P_w - Q_w)n_0 ≡ -D_w (mod Q_w^L)`.

The infinite periodic return code selected by `www...` is `n_w^*`, and `n_w^* in [-1,0)`.

Status: proved.

Interpretation: every periodic return word has arbitrarily long finite shadows, but the infinite periodic code is an explicit negative rational. The remaining bounded-alphabet return obstruction is therefore genuinely nonperiodic.

### Lemma 11e.8: No Eventually Periodic Binary Return Itinerary

No infinite positive-integer binary-depth obstruction can have an eventually periodic sequence of return lengths:

`(r_0, r_1, ...)`.

Status: proved.

Reason: after discarding a finite preperiod, a periodic return tail would have to start from the rational periodic code `n_w^* in [-1,0)` given by Lemma 11e.7a, contradicting positivity.

Interpretation: after the finite-word result, this isolates the binary-depth obstruction to non-eventually-periodic infinite return words whose prefix residues stay bounded.

### Lemma 11e.8a: Morse-Hedlund Complexity Criterion

Let `x` be an infinite word over a finite alphabet, and let `p_x(m)` be the number of distinct length-`m` factors appearing in `x`. If `p_x(m) <= m` for some `m >= 1`, then `x` is eventually periodic.

More generally, if `x` is not eventually periodic and uses `q=p_x(1)` distinct symbols, then:

`p_x(m) >= m+q-1`

for every `m >= 1`.

Status: proved.

Reason: if factor complexity stops increasing at some length, every factor at that length has a unique right extension. The resulting finite deterministic window process is eventually periodic. Taking the contrapositive, non-eventual-periodicity forces strict growth `p_x(j+1)>p_x(j)` at every length, hence `p_x(m) >= p_x(1)+m-1`.

Interpretation: after periodic obstructions are excluded, every bounded-alphabet obstruction must have genuinely aperiodic combinatorial complexity.

### Lemma 11e.8b: Bounded Return Obstruction Complexity

Suppose an infinite positive-integer binary return obstruction has bounded return lengths. Let `q` be the number of distinct return lengths appearing in its return-length word, and let `p(m)` be its factor complexity. Then:

`p(m) >= m+q-1`

for every `m >= 1`.

Status: proved.

Reason: the itinerary is a non-eventually-periodic word over a finite alphabet, so the strengthened Morse-Hedlund lower bound applies.

Interpretation: a bounded-return obstruction must have at least the minimal aperiodic complexity allowed by its tail alphabet. Low-complexity nonperiodic candidates are excluded.

### Lemma 11e.9: Binary Return 3-adic Reset

If a binary return block has length `r` and output depth-`0` parameter `n'`, then:

`n' ≡ (2 * 3^(3r+1) - 85) * 88^(-1) (mod 3^(3r+2))`.

In particular, `n' ≡ 2 (mod 3)` for every return block.

Status: proved.

Reason: from the return reparameterization,

`n' = (3^(3r+1) w - 85) / 88`,

and `16^r w ≡ 32 (mod 33)` implies `w ≡ 2 (mod 3)`.

Interpretation: a long binary return block almost resets the next return state to the fixed `3`-adic value `-85/88`. This is exact arithmetic structure, but still not a pointwise contradiction because the next return gate is dyadic.

### Lemma 11e.9a: Binary Return Reset-Spike Constraint

In any infinite positive binary return orbit with states `n_j` and return lengths `r_j`, each block satisfies:

`n_j >= (5 * 16^(r_j) - 32) / 33`,

and:

`n_{j+1} ≡ -85/88 (mod 3^(3r_j+1))`.

Consequently, if the return lengths are unbounded, then along every subsequence with `r_j -> infinity` the incoming states `n_j` tend to infinity in `R`, while the following states `n_{j+1}` converge to `-85/88` in `Q_3`.

Status: proved.

Interpretation: the unbounded-return obstruction is a simultaneous real-height spike and `3`-adic reset phenomenon.

### Lemma 11e.10: Binary `{0,1}` Gap 3-adic Clock

In the binary return subcase where all return lengths are `0` or `1`, suppose a length-`1` return is followed by `k >= 0` length-`0` returns before the next length-`1` return. Let `n` be the depth-`0` return parameter immediately after the first length-`1` block, and let `n_i` be the parameter after the following `i` zero-return blocks. Then:

`v_3(n_i + 1) = 2i + 1`.

In particular, immediately before the next length-`1` block:

`v_3(n_k + 1) = 2k + 1`.

Status: proved.

Reason: a length-`1` block resets the output to `n ≡ 92 (mod 243)`, so `v_3(n+1)=1`. A zero-return block satisfies `n' + 1 = 9(n+1)/8`, increasing the `3`-adic valuation by exactly `2`.

Interpretation: in the smallest open bounded alphabet `{0,1}`, long zero gaps force the pre-`1` state close to `-1` in `Q_3`, while each `1` resets the following state to valuation `1`. This still does not rule out a nonperiodic infinite gap sequence.

### Lemma 11e.11: Binary `{0,1}` Gap Map

In the binary `{0,1}` return subcase with infinitely many length-`1` returns, let:

`a_j = (n_j + 1) / 3`,

where `n_j` is the depth-`0` parameter immediately after the `j`-th length-`1` return. If the next length-`1` return is preceded by exactly `k_j >= 0` zero-return blocks, then:

`a_{j+1} = (3^(2k_j+5) a_j - 8^(k_j)) / 2^(3k_j+7)`.

Equivalently:

`a_{j+1} = (243/128) * (9/8)^k_j * a_j - 1/128`.

In particular, `a_{j+1} > a_j` for every positive integer state.

Status: proved.

Interpretation: the `{0,1}` subcase is an expanding positive-integer gap map indexed by zero-gap lengths. Periodic gap sequences are impossible, but arbitrary nonperiodic gap sequences remain unresolved.

### Lemma 11e.11a: Binary `{0,1}` Gap Critical Series

Fix an infinite zero-gap word `(k_0, k_1, ...)`, and put:

`alpha_j = (243/128) * (9/8)^(k_j)`.

Define:

`L_N = (1/128) * sum_{i=0}^{N-1} 1 / (alpha_0 alpha_1 ... alpha_i)`.

Then `L_N` converges in `R` to a value `L_R` with:

`0 < L_R <= 1/115 < 1`.

The same rational sequence converges in `Q_2` to the 2-adic gap code selected by the infinite word. For the finite composition:

`H_N a_N = A_N a_0 - C_N`,

one has:

`L_N = C_N / A_N`,

and the least prefix residue satisfies:

`S_N ≡ L_N (mod H_N)`.

Status: proved.

Interpretation: the `{0,1}` obstruction has an adelic form. The real critical value is always below `1`, but the same rational partial sums may converge 2-adically. Eventually periodic words give rational limits below `1`; the remaining hard case is proving that no nonperiodic word has a 2-adic limit that is a positive ordinary integer.

### Lemma 11e.11b: Binary `{0,1}` Gap Ordinary-Landing Divisibility Criterion

Fix an infinite zero-gap word `(k_0, k_1, ...)` and a positive integer `A`. Let:

`H_N a_N = A_N a_0 - C_N`

be the affine composition of the first `N` gap maps, and put:

`K_N = k_0 + ... + k_{N-1}`.

Then `A` is the positive ordinary gap code for this word if and only if:

`v_2(A_N A - C_N) >= 7N + 3K_N`

for every `N >= 1`. In that case:

`a_N = (A_N A - C_N) / H_N`

is the corresponding positive gap orbit.

Status: proved.

Interpretation: the reduced gap landing problem is exactly a problem of forcing arbitrarily high powers of `2` to divide the integer sequence `A_N A - C_N`.

### Lemma 11e.11c: Binary `{0,1}` Gap Landing Growth Envelope

Suppose an infinite zero-gap word `(k_0, k_1, ...)` has positive ordinary gap code `a_0 = A`. Put:

`K_N = k_0 + ... + k_{N-1}`.

Then:

`a_N = (A_N / H_N) * (A - L_N)`,

where `L_N` is the gap critical-series partial sum. In particular:

`a_N <= A * (243/128)^N * (9/8)^(K_N)`.

If the next zero-gap length is `k_N`, then:

`8^(k_N) <= A * (243/128)^N * (9/8)^(K_N)`.

Status: proved.

Interpretation: positive gap-code landings force a growth envelope. Gap words with spikes larger than this envelope cannot be positive-integer obstructions; the hard case is balanced nonperiodic growth.

### Lemma 11e.11u: Binary `{0,1}` Gap Ordinary Itinerary Uniqueness

For a fixed positive normalized state `a_0`, there is at most one infinite `{0,1}` zero-gap word for which `a_0` is the ordinary gap code.

Status: proved.

Reason: the partial map reads the next gap from `a_0=8^k b`, so `k=v_2(a_0)/3` and the next state are unique whenever a complete gap transition exists.

Interpretation: for a fixed ordinary integer, the candidate gap word is forced. The remaining problem is proving that this forced partial-map orbit eventually fails.

### Lemma 11e.11v: Binary `{0,1}` Gap Forced-Orbit Prefix Equivalence

Fix a positive normalized state `A`. The `{0,1}` gap partial map is defined for the first `L` forced complete gap transitions, with forced word `(k_0, ..., k_{L-1})`, if and only if `A` satisfies every prefix congruence:

`A ≡ S_N (mod H_N)` for `1 <= N <= L`.

Once `H_N > A`, this is equivalent to `S_N = A`.

Status: proved.

Interpretation: direct forced gap-orbit scans and gap-prefix residue stabilization are the same finite test, written in different coordinates.

### Lemma 11e.11d: Binary `{0,1}` Gap Spike Exclusion

Let `(k_0, k_1, ...)` be an infinite zero-gap word and put:

`K_N = k_0 + ... + k_{N-1}`.

If:

`sup_N 8^(k_N) / ((243/128)^N (9/8)^(K_N)) = infinity`,

then this word has no positive ordinary gap code.

Status: proved.

Interpretation: an unbounded gap obstruction, if it exists, cannot have isolated gaps that outgrow the accumulated real expansion. It must remain quantitatively balanced.

### Lemma 11e.11e: Periodic `{0,1}` Gap Branch

Let `w=(k_0, ..., k_{p-1})` be a nonempty finite zero-gap word, and write its one-period affine data as:

`H_w a_p = A_w a_0 - C_w`.

For `L >= 1`, let `w^L` denote `L` repetitions of `w`. A positive normalized state `a_0` realizes the gap word `w^L` if and only if:

`a_0 ≡ a_w^* (mod H_w^L)`,

where:

`a_w^* = C_w / (A_w - H_w)`.

Equivalently:

`(A_w - H_w)a_0 ≡ C_w (mod H_w^L)`.

The infinite periodic gap code selected by `www...` is `a_w^*`, and `0 < a_w^* < 1`.

Status: proved.

Interpretation: every periodic gap word has arbitrarily long finite shadows, but the infinite periodic code is an explicit rational strictly between `0` and `1`. The remaining reduced-gap obstruction is genuinely nonperiodic.

### Lemma 11e.12: No Eventually Periodic `{0,1}` Gap Itinerary

No positive-integer orbit of the `{0,1}` gap map can have an eventually periodic zero-gap sequence.

Status: proved.

Reason: after discarding a finite preperiod, a periodic gap tail would have to start from the rational periodic code `a_w^* in (0,1)` given by Lemma 11e.11e, contradicting positivity as an integer.

Interpretation: the local `{0,1}` gap system has the same shape as the broader binary problem: finite patterns occur, eventually periodic patterns are impossible, and the only remaining obstruction is nonperiodic bounded-residue coding.

### Lemma 11e.12a: Bounded `{0,1}` Gap Obstruction Complexity

Suppose an infinite positive-integer reduced `{0,1}` gap obstruction has bounded zero-gap lengths. Let `q` be the number of distinct zero-gap lengths appearing in its gap word, and let `p(m)` be its factor complexity. Then:

`p(m) >= m+q-1`

for every `m >= 1`.

Status: proved.

Reason: the gap itinerary is a non-eventually-periodic word over a finite alphabet, so the strengthened Morse-Hedlund lower bound applies.

Interpretation: a bounded zero-gap obstruction must also have at least the minimal aperiodic complexity allowed by its tail alphabet.

### Lemma 11e.13: All-Zero `{0,1}` Gap Branch

A normalized state `a_0` has first `L` zero-gap lengths all equal to `0` if and only if:

`a_0 ≡ 1/115 (mod 128^L)`,

equivalently:

`115 a_0 ≡ 1 (mod 128^L)`.

The infinite all-zero gap code is the 2-adic rational:

`a_0 = 1/115`,

which is not a positive integer.

Status: proved.

Interpretation: long all-zero gap shadows converge 2-adically to a nonintegral rational code, not to a positive integer obstruction.

### Lemma 11e.14: Constant `{0,1}` Gap Branch

Fix `k >= 0` and put:

`A_k = 3^(2k+5)`, `Q_k = 2^(3k+7)`, `B_k = 8^k`.

A normalized state `a_0` has first `L` zero-gap lengths all equal to `k` if and only if:

`a_0 ≡ B_k / (A_k - Q_k) (mod Q_k^L)`,

equivalently:

`(A_k - Q_k) a_0 ≡ B_k (mod Q_k^L)`.

The infinite constant-`k` gap code is:

`a_* = B_k / (A_k - Q_k)`,

which lies strictly between `0` and `1`, so it is not a positive integer.

Status: proved.

Interpretation: every constant gap itinerary has arbitrarily long finite shadows, but its infinite 2-adic code is a nonintegral rational below `1`.

### Lemma 11e.15: Binary `{0,1}` Gap Partial Map

In the `{0,1}` gap-map notation, a gap of exactly `k >= 0` zeros occurs after a length-`1` return if and only if:

`a = 8^k b`,

where `b` is odd and:

`3 * 9^k * b ≡ 49 (mod 128)`.

In that case the next post-length-`1` normalized state is:

`a' = (3^(2k+5) b - 1) / 128`.

Status: proved.

Interpretation: the next zero-gap length is read directly from the exact `2`-adic valuation of `a=(n+1)/3`, and the residue of the remaining odd part decides whether the next nonzero return is length `1`. This is the current cleanest formulation of the `{0,1}` subproblem.

### Lemma 11e.15a: Binary `{0,1}` Gap Partial-Map Equivalence

A positive-integer obstruction in the `{0,1}` gap system is exactly an infinite positive orbit of the partial map:

`a = 8^k b`, `3 * 9^k * b ≡ 49 (mod 128)` maps to `(3^(2k+5)b - 1) / 128`.

Status: proved.

Interpretation: proving that this partial map has no infinite positive orbit settles the `{0,1}` return-length subcase.

### Lemma 11e.15b: Binary `{0,1}` Gap Backward Branch Formula

Fix a terminal normalized state `a'` and a gap length `k >= 0`. A positive state `a` maps to `a'` through a complete `{0,1}` gap transition of length `k` if and only if:

`a = (2^(3k+7) a' + 8^k) / 3^(2k+5)`

is a positive integer.

Status: proved.

Interpretation: each fixed gap length contributes at most one backward preimage of a terminal state. Thus finite gap-prefix clustering is controlled by arithmetic divisibility along a backward preimage tree.

### Lemma 11e.15c: Binary `{0,1}` Gap Backward Length Bound

If a terminal normalized state `a'` has a backward preimage through a gap of length `k`, then:

`(9/8)^k <= (128a' + 1) / 243`.

Status: proved.

Interpretation: only logarithmically many gap lengths can occur as backward branches into a fixed terminal state.

### Lemma 11e.15c1: Binary `{0,1}` Gap Backward 3-adic Gate

For fixed terminal normalized state `a'`, a backward gap branch of length `k` exists if and only if:

`3^(2k+5) | 128a' + 1`.

Hence the number of backward gap branches into `a'` is:

`max(0, floor((v3(128a'+1)-5)/2) + 1)`.

Status: proved.

Interpretation: unlike the return map, the gap map has nested backward branches. Forward merging is exactly controlled by proximity of the terminal state to `-1/128` in `Q_3`.

### Lemma 11e.15c2: Binary `{0,1}` Gap Backward Merge Chain

Fix a terminal normalized state `a'` with at least one backward gap branch and put:

`K = floor((v3(128a'+1)-5)/2)`.

Then its complete set of backward preimages is:

`a_k = 8^k(128a'+1)/3^(2k+5)` for `0 <= k <= K`.

Consecutive preimages satisfy:

`a_{k+1} = (8/9)a_k`.

Status: proved.

Interpretation: immediate forward merges in the reduced gap map are finite geometric chains, not arbitrary clusters.

### Lemma 11e.15c3: Binary `{0,1}` Gap Backward Merge Bounds

Let `M(a')` be the number of immediate backward gap preimages of a terminal normalized state `a'`. Then:

`M(a') <= max(0, (log_3(128a'+1)-3)/2)`.

Moreover:

`sum_{a: T_G(a)=a'} a <= (128a'+1)/27 <= (43/9)a'`.

Status: proved.

Interpretation: the gap map can merge branches, but immediate merge multiplicity is only logarithmic in the terminal height, and the whole immediate preimage chain has bounded total real mass.

### Lemma 11e.15d: Binary `{0,1}` Gap Backward Contraction

If `a` maps to `a'` through a complete `{0,1}` gap transition of length `k`, then:

`a <= (43/81)(8/9)^k a'`.

Status: proved.

Interpretation: every valid positive backward gap branch strictly decreases height, and longer gap labels decrease it faster.

### Lemma 11e.15e: Binary `{0,1}` Gap Backward Path Contraction

If a depth-`L` backward gap path has gap word `(k_0, ..., k_{L-1})` and total gap length `K_L`, then:

`a_0 <= (43/81)^L (8/9)^K_L a_L`.

Status: proved.

Interpretation: backward gap trees contract exponentially in both transition count and total zero-gap length, even though immediate merge chains can have more than one preimage.

### Lemma 11e.15e1: Binary `{0,1}` Gap Terminal Escape

If a positive state `a_0` survives `L` complete gap transitions with total zero-gap length `K_L` and terminal state `a_L`, then:

`a_L >= (81/43)^L (9/8)^K_L a_0`.

Status: proved.

Interpretation: the forward gap process forces exponential terminal-height escape along every surviving path.

### Lemma 11e.15e2: Binary `{0,1}` Gap Terminal Window

For a finite gap word `w`, let:

`E_w = A_w/H_w = (243/128)^L(9/8)^K_w`,

let `L_w = C_w/A_w` be its gap critical-series partial sum, let `S_w` be its least prefix residue, and let `u_w` be the terminal state reached from `S_w`. Then:

`u_w = E_w(S_w - L_w)`, with `S_w - 1/115 < u_w/E_w < S_w`.

In particular, `S_w = ceil(u_w/E_w)`.

Consequently, `S_w <= B` implies `u_w < E_w B`.

Status: proved.

Interpretation: low gap-prefix residues correspond to normalized terminal states in a fixed-width window. This is the exact window that a stopping-time proof must control.

### Lemma 11e.15e2a: Binary `{0,1}` Gap Terminal Depth Bound

If a gap word `w` has length `L`, expansion factor `E_w`, and terminal state `u_w`, then:

`u_w > (114/115)E_w >= (114/115)(243/128)^L`.

Consequently:

`L < log_{243/128}((115/114)u_w)`.

Status: proved.

Reason: the least gap-prefix residue satisfies `S_w >= 1`. The gap terminal-window identity gives `u_w/E_w > S_w - 1/115 >= 114/115`, and every reduced gap block expands by at least `243/128`.

Interpretation: a fixed reduced-gap terminal state can only appear at logarithmically bounded prefix depth. The remaining gap problem is not infinite depth at one terminal value, but uniform counting across terminals together with merge multiplicity.

### Lemma 11e.15e3: Binary `{0,1}` Gap Terminal-Window Counting Equivalence

With the notation of Lemma 11e.15e2:

`S_w <= B` if and only if `u_w/E_w < B`.

Consequently:

`N_G(B,L) = #{w: |w|=L, u_w/E_w < B}`.

Status: proved.

Interpretation: the gap critical-rank problem is exactly a window-counting problem for normalized terminal heights.

### Lemma 11e.15e3a: Binary `{0,1}` Gap Expansion Pressure

For every `theta > 0` and every gap-prefix length `L`,

`sum_(|w|=L) E_w^(-theta) = (((128/243)^theta) / (1 - (8/9)^theta))^L`,

where `E_w = (243/128)^L (9/8)^(sum_j k_j)` is the gap expansion factor.

This pressure decays exponentially in `L` exactly when:

`(128/243)^theta + (8/9)^theta < 1`.

The threshold root is approximately `2.26483`; in particular, cubic pressure decays.

Status: proved.

Interpretation: the reduced gap label pressure is also subcritical at high moments. It is slightly sharper than the coarse backward gap moment bound, but still needs a terminal-window separation or stopping-time estimate to become a counting proof.

### Lemma 11e.15e3b: Binary `{0,1}` Gap Weighted Terminal-Window Bound

For every `theta > 2`, every `B >= 1`, and every `L >= 1`,

`sum_(|w|=L, S_w <= B) E_w^(-theta) <= B^theta (43/81)^L zeta(theta - 1)`.

Status: proved.

Reason: for a fixed terminal state `u`, backward gap contraction bounds the number of length-`L` words landing at `u` by `floor((43/81)^L u)`. The terminal window gives `E_w^(-theta) < B^theta u_w^(-theta)`, and summing over terminals leaves `zeta(theta-1)`.

Interpretation: this is the gap analogue of the return weighted terminal-window estimate, but it also absorbs merge multiplicity. It remains weighted control, not the unweighted rank theorem.

### Lemma 11e.15e3c: Binary `{0,1}` Gap Weighted Expansion-Shell Count

Let `W_G(B,L;s)` count length-`L` gap words satisfying `S_w <= B` and `2^s <= E_w < 2^(s+1)`. For every `theta > 2`,

`W_G(B,L;s) <= 2^(theta(s+1)) B^theta (43/81)^L zeta(theta-1)`.

Status: proved.

Reason: each word in shell `s` contributes more than `2^(-theta(s+1))` to the inverse-expansion mass, and the gap weighted terminal-window bound controls that mass including merge multiplicity.

Interpretation: the reduced gap shell count has an extra depth-decay factor from backward contraction, but it still worsens with the shell index. The missing rank theorem must control high shells more sharply.

### Lemma 11e.15e3d: Binary `{0,1}` Gap Expansion-Shell Depth Bound

If a length-`L` gap word satisfies `2^s <= E_w < 2^(s+1)`, then:

`L < log_{243/128}(2^(s+1))`.

Status: proved.

Reason: every reduced gap block has expansion at least `243/128`, so `(243/128)^L <= E_w < 2^(s+1)`.

Interpretation: every fixed reduced-gap expansion shell only contributes to bounded prefix depths. Infinite-depth obstructions must move through arbitrarily high shells.

### Lemma 11e.15e3e: Binary `{0,1}` Gap Low-Expansion Distinct-Terminal Count

Let `D_G(B,L;X)` be the number of distinct terminal states `u_w` arising from length-`L` gap words with `S_w <= B` and `E_w <= X`. Then:

`D_G(B,L;X) <= floor(X B)`.

Status: proved.

Reason: the gap terminal window gives `u_w < E_w B`; if `E_w <= X`, then `u_w < X B`, leaving at most `floor(XB)` positive integer terminal states.

Interpretation: this is only a distinct-terminal bound. Unlike the return system, the reduced gap system has forward merging, so the remaining low-expansion counting problem also needs multiplicity control over words landing at the same terminal state.

### Lemma 11e.15e3f: Binary `{0,1}` Gap Low-Expansion Window Count with Multiplicity

Let `N_G(B,L;X)` count length-`L` gap words satisfying `S_w <= B` and `E_w <= X`, where `B >= 1`, `L >= 1`, and `X >= 1`. Put:

`M = ceil(XB) - 1`.

Then:

`N_G(B,L;X) <= sum_{u=1}^M floor((43/81)^L u) <= (43/81)^L M(M+1)/2`.

Status: proved.

Reason: low expansion gives `u_w < XB`. For a fixed terminal state `u`, every length-`L` word landing at `u` has a distinct positive start, and backward gap contraction gives that start at most `(43/81)^L u`.

Interpretation: this is an ordinary count for the low-expansion part of the gap low window, including merge multiplicity. It is still too weak for the desired rank theorem because it is quadratic in the terminal cutoff rather than linear in `B` at the natural survival rate.

### Lemma 11e.15f: Binary `{0,1}` Gap Backward Cubic-Mass Contraction

For every terminal gap state `a'`:

`sum_{a: T_G(a)=a'} a^3 <= (43^3/(729*217)) (a')^3 < (a')^3`.

Status: proved.

Interpretation: despite finite forward merging, the full immediate backward gap map is a strict contraction for cubic mass.

### Lemma 11e.15g: Binary `{0,1}` Gap Backward Moment Contraction

For every real `theta > 0` and every terminal gap state `a'`:

`sum_{a: T_G(a)=a'} a^theta <= ((43/81)^theta/(1-(8/9)^theta)) (a')^theta`.

This is a strict moment contraction whenever:

`(43/81)^theta + (8/9)^theta < 1`.

Status: proved.

Interpretation: the gap map has a tunable potential family. Cubic mass is a simple strict case, but any sufficiently high power works.

Numerically, the threshold equation `(43/81)^theta + (8/9)^theta = 1` has root approximately `2.28216`.

### Lemma 11e.16: Finite `{0,1}` Gap Words Are Realizable

For every finite sequence of zero-gap lengths:

`(k_0, ..., k_{L-1})`,

there are infinitely many positive normalized states `a_0` whose `{0,1}` gap itinerary begins with exactly this sequence.

Status: proved.

Reason: each fixed gap length `k` imposes one residue class on `a` modulo `2^(3k+7)`, and pulling back finite suffix conditions preserves a single residue class with multiplied modulus.

Interpretation: the `{0,1}` gap system cannot be solved by forbidding a finite gap pattern. Any obstruction is necessarily an infinite nonperiodic coding phenomenon.

### Lemma 11e.17: Binary `{0,1}` Gap-Code Boundedness Criterion

Fix an infinite zero-gap word `(k_0, k_1, ...)`, and let `S_N` be the least nonnegative residue of its length-`N` gap-prefix code modulo:

`H_N = prod_{j=0}^{N-1} 2^(3k_j+7)`.

The corresponding `{0,1}` gap code is a nonnegative ordinary integer if and only if `S_N` is bounded. Equivalently, this happens if and only if `S_N` is eventually constant.

Status: proved.

Interpretation: this is the exact remaining `{0,1}` target. Prove that every non-eventually-periodic infinite gap word has unbounded gap-prefix residues.

### Lemma 11e.18: Binary `{0,1}` Gap-Prefix Monotonicity

For a fixed infinite gap word, the least nonnegative prefix residues `S_N` satisfy:

`S_{N+1} = S_N + d_N H_N`,

where:

`0 <= d_N < 2^(3k_N+7)`.

Therefore `S_N` is nondecreasing. It is bounded if and only if `d_N = 0` for all sufficiently large `N`.

Status: proved.

Important caveat: strict increase is false for finite prefixes. The gap prefix:

`(0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0)`

has the same least residue at lengths `15` and `16`.

Interpretation: the missing `{0,1}` theorem must prove that nonzero increments occur infinitely often for every non-eventually-periodic infinite gap word.

### Lemma 11e.18a: Binary `{0,1}` Gap Finite Height Search Criterion

Fix a positive integer bound `B` and prefix length `L`. To decide whether there is a length-`L` gap word with least prefix residue `S_L < B`, it is enough to search a finite tree:

- keep only prefixes whose current least residue is `< B`
- for a current prefix composition `H_i a_i = A_i a_0 - C_i`, only test next gaps `k_i` satisfying `8^k_i H_i < A_i B`

Status: proved.

Reason: prefix residues are nondecreasing, so a final residue `< B` forces every shorter prefix residue `< B`. Also, any ordinary start `a_0 < B` gives intermediate state `a_i < A_i B / H_i`; if the next gap is `k_i`, then `8^k_i <= a_i`.

Interpretation: this gives a certifiable finite search for least prefix residues at each fixed length. It is not the missing infinite theorem, but it turns finite minimum-residue claims into exact certificates rather than raw scans.

### Lemma 11e.18b: Binary `{0,1}` Gap Global-Minimum Divergence Criterion

Let `nu_L` be the least gap-prefix residue among all zero-gap words of length `L`.

Then the reduced `{0,1}` gap system has no positive ordinary infinite gap code if and only if:

`nu_L -> infinity`.

Status: proved.

Reason:

- If a positive ordinary gap code `A` exists, its prefix residues eventually equal `A`, so `nu_L <= A` for all large `L`.
- If `nu_L` is bounded, the finite-height search criterion gives a finitely branching tree of bounded-residue gap prefixes with nodes at every depth. The infinite-tree lemma gives an infinite bounded-residue path, and the boundedness criterion turns that path into a positive ordinary gap code.

Interpretation: the reduced `{0,1}` obstruction is exactly a global height-growth theorem for the minima `nu_L`.

### Lemma 11e.18b1: Bounded `{0,1}` Gap Alphabet Divergence Criterion

Fix `K >= 0`, and let `nu_L^(<=K)` be the least gap-prefix residue among all zero-gap words of length `L` whose letters lie in `{0, ..., K}`.

Then there is no positive ordinary infinite gap code over this bounded alphabet if and only if:

`nu_L^(<=K) -> infinity`.

Status: proved.

Reason:

- If a positive ordinary gap code `A` exists over the alphabet, its prefix residues eventually equal `A`, so `nu_L^(<=K) <= A` for all large `L`.
- If `nu_L^(<=K)` is bounded, the bounded alphabet gives a finitely branching tree of bounded-residue prefixes with nodes at every depth. The infinite-tree lemma gives an infinite bounded-residue path, and the gap boundedness criterion turns that path into a positive ordinary code.

Interpretation: the bounded-gap-length half of the reduced obstruction is also an exact finite-alphabet minimum-residue divergence theorem.

### Lemma 11e.18b2: Binary `{0,1}` Gap Fixed Positive-Label Divergence

Fix `J >= 0`, and let `nu_(L,J)^+` be the least gap-prefix residue among length-`L` zero-gap words with at most `J` positive zero-gap lengths.

Then:

`nu_(L,J)^+ -> infinity`.

Status: proved.

Reason: if these minima were bounded, the finite-height search criterion would give an infinite bounded-residue path whose prefixes all have at most `J` positive labels. The infinite path has only finitely many positive labels, hence is eventually all zero. The gap boundedness criterion would turn the bounded residues into a positive ordinary infinite gap code with an eventually periodic gap itinerary, contradicting the periodic gap exclusion.

Interpretation: in the `{0,1}` gap alphabet, every fixed-one-count stratum is already settled. Any remaining bounded-residue obstruction needs infinitely many `1` labels.

### Lemma 11e.18b2a: Binary `{0,1}` Gap Prefix-Language Compactness Principle

Let `C` be any prefix-closed collection of finite zero-gap words. Let `nu_C(L)` be the least gap-prefix residue among words in `C` of length `L`, when such words exist.

If `nu_C(L)` does not tend to infinity along the lengths where it is defined, then there is an infinite zero-gap word whose every prefix lies in `C` and whose gap code is a positive ordinary integer.

Status: proved.

Reason: bounded minima give a finitely branching bounded-residue prefix tree by the gap finite-height search criterion. An infinite path through that tree has bounded, nondecreasing prefix residues, so the gap boundedness criterion turns it into a positive ordinary code.

Interpretation: this is the reusable compactness engine behind the bounded-gap-alphabet, fixed-positive-label, and finite-defect periodic-shadow divergence lemmas.

### Lemma 11e.18b3: Binary `{0,1}` Gap Finite-Defect Periodic Shadow Divergence

Fix an eventually periodic infinite zero-gap word `z` and `J >= 0`. Let `nu_(L,J)(z)` be the least gap-prefix residue among length-`L` zero-gap words that differ from the length-`L` prefix of `z` in at most `J` positions.

Then:

`nu_(L,J)(z) -> infinity`.

Status: proved.

Reason: if these minima were bounded, finite-height compactness would give an infinite bounded-residue path with at most `J` total deviations from `z`. Since `z` is eventually periodic, that path is eventually periodic. The gap boundedness criterion would turn it into a positive ordinary infinite gap code, contradicting the exclusion of eventually periodic gap itineraries.

Interpretation: a reduced-gap obstruction cannot stay at bounded edit distance from any eventually periodic zero-gap template. It must drift away from every periodic shadow in unboundedly many positions.

### Lemma 11e.18b4: Binary `{0,1}` Gap Low-Complexity Divergence

Fix `m >= 1`. For a finite binary zero-gap word `w`, let `p_w(m)` count its distinct length-`m` factors. Let `nu_(L,m)^low` be the least gap-prefix residue among length-`L` binary zero-gap words with `p_w(m) <= m`.

Then:

`nu_(L,m)^low -> infinity`.

Status: proved.

Reason: the class of finite binary words with `p_w(m) <= m` is prefix-closed. Any infinite path through this class has at most `m` distinct length-`m` factors, so Morse-Hedlund makes it eventually periodic. The gap prefix-language compactness principle then turns bounded low-complexity minima into an eventually periodic positive gap code, contradicting the periodic-itinerary exclusion.

Interpretation: a remaining binary reduced-gap obstruction must be Sturmian-or-higher at every fixed scale: for each `m`, its long low-residue prefixes must have at least `m+1` distinct length-`m` factors.

### Lemma 11e.18b5: Binary `{0,1}` Gap Balanced-Frontier Criterion

Let `nu_L^bal` be the least gap-prefix residue among balanced binary zero-gap words of length `L`.

Then `nu_L^bal -> infinity` if and only if there is no non-eventually-periodic balanced infinite binary zero-gap word whose gap code is a positive ordinary integer.

Status: proved as an exact criterion.

Reason: balanced finite words form a prefix-closed class. If the balanced minima are bounded, prefix-language compactness gives an infinite positive gap code whose every finite prefix is balanced, hence whose infinite word is balanced. The periodic exclusion removes the eventually periodic case, leaving exactly a non-eventually-periodic balanced positive ordinary gap code. The converse is immediate from eventual equality of prefix residues to any represented ordinary integer.

Interpretation: this is the exact reduced-gap version of the minimal-complexity frontier. The later Sturmian fast prefix-recurrence argument removes the irrational-slope balanced reduced-gap obstruction class.

### Lemma 11e.18b6: Binary `{0,1}` Gap Balanced Sublinear-Symbol Divergence

Fix a symbol `a in {0,1}` and a function `f(n)=o(n)`. Among balanced binary zero-gap words whose every length-`n` factor contains at most `f(n)` occurrences of `a`, the least gap-prefix residues tend to infinity along the lengths where this class is nonempty.

Status: proved.

Reason: the class is prefix-closed. Bounded restricted minima would give an infinite balanced positive gap code by prefix-language compactness. The sublinear factor count contradicts the balanced aperiodic positive-density lemma unless the word is eventually periodic, and periodic gap itineraries are already excluded.

Interpretation: balanced reduced-gap obstructions cannot have density-zero windows in either symbol, even when the sparse symbol count tends to infinity.

### Lemma 11e.18c: Binary `{0,1}` Gap Fixed-Height Duality

For `B >= 0`, let `H_G(B)` be the largest reduced gap-prefix length that can be realized with least residue at most `B`.

Then:

`H_G(B) < L` iff `nu_L > B`.

Consequently, the reduced `{0,1}` gap system has no positive ordinary infinite gap code if and only if `H_G(B)` is finite for every fixed `B`.

Status: proved.

Interpretation: the reduced gap obstruction can be attacked either by proving `nu_L -> infinity` or by proving every fixed height bound has finite survival depth.

### Lemma 11e.18d: Binary `{0,1}` Gap Height Scale Lower Bound

The global reduced-gap minima and fixed-height survival depths satisfy:

`nu_L < 128^L`, and `H_G(128^L - 1) >= L`.

Consequently, any upper bound `H_G(B) <= c log2(B+1) + O(1)` must have `c >= 1/7`.

Status: proved.

Interpretation: the desired reduced-gap fixed-height theorem, if true, can be logarithmic at best. The all-zero gap branch gives the scale obstruction.

### Lemma 11e.18e: Binary `{0,1}` Gap Counting Criterion

Let `N_G(B,L)` count length-`L` gap words whose least prefix residue is at most `B`.

If there are constants `C > 0` and `0 < rho < 1` such that:

`N_G(B,L) <= C B rho^L`

for every `B,L`, then:

`H_G(B) <= ceil(log_{1/rho}(C B))`.

Status: proved as a conditional criterion.

Interpretation: a uniform prefix-counting discrepancy theorem would prove the reduced gap fixed-height theorem. The natural density heuristic suggests `rho = 1/112`, but the needed uniform finite-height discrepancy bound is not yet proved.

### Lemma 11e.18e1: Binary `{0,1}` Gap Normalized Stopping-Time Criterion

Let `W_G(B,L)` count length-`L` gap words whose normalized terminal state satisfies:

`u_w/E_w < B`.

If there are constants `C > 0` and `0 < rho < 1` such that:

`W_G(B,L) <= C B rho^L`

for every `B,L`, then:

`H_G(B) <= ceil(log_{1/rho}(C B))`.

Status: proved as a conditional criterion.

Interpretation: the missing reduced-gap estimate can be stated entirely as a normalized terminal-window stopping-time bound. By Lemma 11e.15e3 this is equivalent to the gap prefix-counting criterion.

### Lemma 11e.18e2: Binary `{0,1}` Gap Terminal-Rank Criterion

For a length-`L` gap word `w`, let `trank_G(w)` be the number of length-`L` gap words `v` satisfying:

`ceil(u_v/E_v) <= ceil(u_w/E_w)`.

A uniform estimate:

`W_G(B,L) <= C B rho^L`

for all `B,L` is equivalent to:

`trank_G(w) <= C ceil(u_w/E_w) rho^L`

for every finite gap word `w`.

Status: proved.

Interpretation: the reduced-gap rank obstruction can be stated entirely in normalized terminal coordinates.

### Lemma 11e.18e3: Binary `{0,1}` Gap Terminal Start-Count Formula

Let `A_G(B,L)` count ordinary starts `1 <= a <= B` whose reduced `{0,1}` gap partial-map orbit is defined for at least `L` complete gap transitions. Then:

`A_G(B,L) = sum_{|w|=L, 1 <= ceil(u_w/E_w) <= B} (floor((B - ceil(u_w/E_w))/H_w) + 1)`.

Status: proved.

Interpretation: ordinary reduced-gap survivor counts can be computed directly from rounded normalized terminal coordinates.

### Lemma 11e.18e4: Binary `{0,1}` Gap Terminal Boundedness Criterion

Fix an infinite gap word and let `w_N` be its length-`N` prefix. Let `E_N` and `u_N` be the expansion factor and terminal state associated to `w_N` and its least gap-prefix residue. Then the selected `2`-adic gap code is a positive ordinary integer if and only if:

`ceil(u_N/E_N)`

is bounded as `N -> infinity`.

Equivalently, this happens if and only if `ceil(u_N/E_N)` is eventually constant.

Status: proved.

Interpretation: the reduced-gap landing problem can be stated entirely as divergence of rounded normalized terminal coordinates.

### Lemma 11e.18e5: Binary `{0,1}` Gap Terminal Monotonicity

For an infinite gap word, let `T_N = ceil(u_N/E_N)` be the rounded normalized terminal coordinate of the length-`N` prefix. If the next gap block has modulus `q_N = 2^(3k_N+7)` and the current prefix modulus is `H_N`, then:

`T_{N+1} = T_N + d_N H_N`, with `0 <= d_N < q_N`.

Consequently `T_N` is nondecreasing, and it is eventually constant if and only if `d_N = 0` for all sufficiently large `N`.

Status: proved.

Interpretation: the reduced-gap obstruction is likewise a zero-increment tail problem for a nondecreasing sequence of rounded normalized terminal coordinates.

### Lemma 11e.18e5a: Binary `{0,1}` Gap Terminal Zero-Step Criterion

Fix a finite gap prefix with auxiliary terminal state `u_N`. For a proposed next gap length `k`, put:

`p = 3^(2k+5)`, `q = 2^(3k+7)`, and `c = 8^k`.

The next rounded terminal increment is zero if and only if:

`p u_N == c (mod q)`.

In that case:

`u_{N+1} = (p u_N - c)/q`,

so the auxiliary terminal state itself takes the same reduced gap-map step of length `k`. Consequently, at most one next gap length can give a zero terminal increment.

Status: proved.

Interpretation: zero gap-terminal increments are locally forced by the auxiliary terminal state.

### Lemma 11e.18e5b: Binary `{0,1}` Gap Terminal Zero-Increment Congruence

Fix a finite gap prefix with auxiliary terminal state `u_N`. For a finite zero-gap suffix `v`, let `S_v` and `H_v` be the least prefix residue and modulus of `v` as a standalone gap word. Then the rounded gap terminal coordinate has zero increments through the whole suffix `v` if and only if:

`u_N == S_v (mod H_v)`.

Status: proved.

Interpretation: finite zero-increment gap tails are exactly ordinary gap prefix congruences imposed on the auxiliary terminal state.

### Lemma 11e.18e5c: Binary `{0,1}` Gap Terminal Self-Shadowing Criterion

Fix a finite gap prefix with auxiliary terminal state `u_N` and an infinite zero-gap suffix `v`. For `L >= 1`, let `S_{v,L}` and `H_{v,L}` be the least prefix residue and modulus of the first `L` gaps of `v`, considered as a standalone gap word. Then the rounded gap terminal coordinate has zero increments along the whole suffix `v` if and only if:

`u_N == S_{v,L} (mod H_{v,L})` for every `L >= 1`.

Equivalently, `u_N` is the positive ordinary gap code selected by the suffix `v`.

Status: proved.

Interpretation: an infinite reduced-gap terminal obstruction is a self-shadowing condition: the auxiliary terminal state must lie in every nested prefix class of the future suffix.

### Lemma 11e.18e5d: Binary `{0,1}` Gap Shift-Code Recurrence

Suppose an infinite zero-gap word `v=(k_0,k_1,...)` has positive ordinary gap code `Y_0`. Let `Y_j` be the state after the first `j` complete gap transitions. Then `Y_j` is the positive ordinary gap code of the shifted suffix `(k_j,k_{j+1},...)`, and:

`2^(3k_j+7) Y_{j+1} = 3^(2k_j+5) Y_j - 8^k_j`.

In particular:

`Y_L >= (81/43)^L (9/8)^(k_0+...+k_{L-1}) Y_0`.

Status: proved.

Interpretation: a self-shadowing reduced-gap obstruction carries positive ordinary codes for every shifted suffix, forming the same expanding gap orbit.

### Lemma 11e.18e5e: Binary `{0,1}` Gap Terminal Zero-Increment Cylinder Density

For a finite zero-gap suffix `v=(k_0, ..., k_{L-1})` with modulus:

`H_v = product_i 2^(3k_i+7)`,

the set of positive auxiliary states whose rounded gap terminal coordinate has zero increments through `v` is one residue class modulo `H_v`, and therefore has natural density `1/H_v`.

For a fixed infinite zero-gap suffix, the set of `2`-adic auxiliary states that shadow the whole suffix is a single `2`-adic point and has Haar measure zero.

Status: proved.

Interpretation: every fixed infinite reduced-gap terminal-zero suffix is measure-zero in the auxiliary state, but this remains a density statement and not a pointwise exclusion.

### Lemma 11e.18e5f: Binary `{0,1}` Gap Terminal Zero-Increment Survival Density

Among positive auxiliary states `u`, the natural density of states admitting at least `L` consecutive rounded gap terminal zero-increments is:

`112^(-L)`.

Status: proved.

Interpretation: the terminal zero-increment obstruction has the same exact exponential density decay as ordinary reduced-gap survival. This remains density information, not a pointwise exclusion.

### Lemma 11e.18e5f1: Bounded Binary `{0,1}` Gap Terminal Zero-Increment Survival Density

Among positive auxiliary states `u`, the natural density of states whose next `L` rounded gap terminal increments are zero and whose corresponding zero-gap lengths all satisfy `0 <= k <= K` is:

`((1/112)(1 - 8^(-(K+1))))^L`.

Status: proved.

Interpretation: bounded-alphabet terminal zero-increment tails have the same exact restricted density as bounded ordinary reduced-gap survival.

### Lemma 11e.18e5g: Finite Binary `{0,1}` Gap Terminal Zero-Increment Words Are Locally Realizable

For every finite sequence of zero-gap lengths `(k_0, ..., k_{L-1})`, there are infinitely many positive auxiliary states `u_0` for which the rounded gap terminal coordinate has zero increments through exactly this finite sequence.

Status: proved.

Interpretation: no proof can rule out reduced-gap terminal obstructions by forbidding a finite zero-increment suffix pattern. The obstruction is genuinely infinite.

### Lemma 11e.18e6: Binary `{0,1}` Gap Terminal Zero-Increment Equivalence

Fix a finite gap prefix and put `T_N = ceil(u_N/E_N)`. For any gap suffix, an eventually constant tail:

`T_N, T_{N+1}, T_{N+2}, ...`

is equivalent to an infinite integer orbit of the reduced `{0,1}` gap map starting from the auxiliary state `u_N`.

Status: proved.

Interpretation: the terminal-coordinate reduced-gap obstruction is exactly the original infinite gap-orbit obstruction, restarted from the auxiliary terminal state.

### Lemma 11e.18e6a: Binary `{0,1}` Gap Terminal Zero-Increment Tail Uniqueness

Fix a finite gap prefix and its auxiliary terminal state `u_N`. There is at most one infinite gap suffix for which all later rounded terminal increments are zero.

Status: proved.

Interpretation: after any finite gap prefix, the zero-increment terminal tail, if it exists, is forced by the auxiliary terminal state.

### Lemma 11e.18e7: Binary `{0,1}` Gap Terminal Zero-Increment Escape

Fix a finite gap prefix and suppose the next `L` gap-prefix increments are zero. If the zero-increment suffix has gap lengths `(k_N, ..., k_{N+L-1})` and total `K`, then:

`u_{N+L} >= (81/43)^L (9/8)^K u_N`.

Status: proved.

Interpretation: a constant rounded gap terminal coordinate still forces real growth of the auxiliary terminal state.

### Lemma 11e.18e8: No Eventually Periodic Binary `{0,1}` Gap Terminal Tail

No eventually periodic zero-gap suffix can make the rounded gap terminal coordinate eventually constant.

Status: proved.

Interpretation: any reduced-gap terminal obstruction must have a genuinely nonperiodic zero-increment suffix.

### Lemma 11e.18f: Binary `{0,1}` Gap Counting Rate Lower Bound

Any prefix-counting bound:

`N_G(B,L) <= C B rho^L`

holding for all `B,L` with fixed `C > 0` must have:

`rho >= 1/128`.

Status: proved.

Reason: the all-zero gap word has a positive least residue below `128^L`, so `N_G(128^L - 1, L) >= 1`.

Interpretation: the natural density value `rho = 1/112` is only slightly above the worst finite-height obstruction `1/128`; a counting proof must control finite-height clustering tightly.

### Lemma 11e.18g: Binary `{0,1}` Gap Start-Count Formula

Let `A_G(B,L)` count ordinary starts `1 <= a <= B` whose reduced `{0,1}` gap partial-map orbit is defined for at least `L` complete gap transitions. For a gap word `w`, let `S_w` be its least prefix residue and let `H_w` be its prefix modulus.

Then:

`A_G(B,L) = sum_{|w|=L, 1 <= S_w <= B} (floor((B - S_w)/H_w) + 1)`.

In particular:

`N_G(B,L) <= A_G(B,L) <= N_G(B,L) + B 112^{-L}`.

Status: proved.

Interpretation: `N_G` counts nonempty gap prefix residue classes, while `A_G` counts all ordinary starts in those classes. The error is governed by the exact reciprocal-modulus density sum `112^{-L}`.

### Lemma 11e.18h: Binary `{0,1}` Gap Start/Prefix Counting Equivalence

For every `rho` with `1/112 <= rho < 1`, a uniform bound

`N_G(B,L) <= C B rho^L`

implies

`A_G(B,L) <= (C+1) B rho^L`.

Conversely, the same bound for `A_G` immediately implies the same bound for `N_G`.

Status: proved.

Interpretation: the reduced gap problem can be attacked through prefix residues or through ordinary-start survival counts; at the natural rate they are equivalent up to constants.

### Lemma 11e.18i: Binary `{0,1}` Gap Critical-Height Reduction

For fixed level `L`, cutoff `B_max`, and rate `rho > 0`, the maximum of

`N_G(B,L) / (B rho^L)`

over `1 <= B <= B_max` occurs at a critical height `B = S_w`, the least prefix residue of some length-`L` gap word, unless no such residue is below `B_max`.

Status: proved.

Reason: between consecutive realized least prefix residues, `N_G(B,L)` is constant while `B` increases.

Interpretation: all-height gap discrepancy reduces to the discrete set of realized least gap residues.

### Lemma 11e.18j: Binary `{0,1}` Gap Critical-Rank Criterion

For a length-`L` gap word `w`, define its critical rank by:

`rank_G(w) = N_G(S_w,L)`.

Then a uniform estimate

`N_G(B,L) <= C B rho^L`

for all `B,L` is equivalent to:

`rank_G(w) <= C S_w rho^L`

for every finite gap word `w`.

Status: proved.

Interpretation: the gap discrepancy theorem is exactly a rank-versus-height theorem for sorted least gap-prefix residues.

### Lemma 11e.19: Binary `{0,1}` Gap-Prefix Digit Recurrence

For a finite gap prefix, write:

`H_N a_N = A_N a_0 - C_N`,

let `S_N` be the least prefix residue, and define:

`u_N = (A_N S_N - C_N) / H_N`.

For the next gap `k_N`, put:

`p_N = 3^(2k_N+5)`, `q_N = 2^(3k_N+7)`, `c_N = 8^(k_N)`.

If:

`S_{N+1} = S_N + d_N H_N`,

then:

`d_N ≡ (c_N - p_N u_N) * (p_N A_N)^(-1) (mod q_N)`.

In particular, `d_N = 0` iff:

`p_N u_N ≡ c_N (mod q_N)`.

Status: proved.

### Lemma 11e.20: Binary `{0,1}` Zero-Increment Tail Equivalence

A run of zero gap-prefix increments:

`d_N = d_{N+1} = ... = d_{N+L-1} = 0`

is equivalent to a finite orbit of the same `{0,1}` gap map starting from the auxiliary integer `u_N` and following the gap word:

`k_N, ..., k_{N+L-1}`.

Consequently, an eventually constant gap-prefix residue tail is equivalent to an infinite integer orbit of the `{0,1}` gap map starting from some auxiliary state.

Status: proved.

Interpretation: this confirms that the digit target is not a different problem. It is the same infinite gap-orbit obstruction expressed in prefix-residue coordinates.

### Lemma 11e.21: Binary `{0,1}` Gap-Core Recurrence

In the `{0,1}` gap-map notation, write:

`a_j = 8^(k_j) b_j`,

where `b_j` is odd and `k_j` is the number of zero-return blocks before the next length-`1` return. Then:

`3 * 9^(k_j) * b_j ≡ 49 (mod 128)`,

and, whenever the next gap `k_{j+1}` is also defined, consecutive odd cores satisfy:

`2^(3k_{j+1}+7) b_{j+1} = 3^(2k_j+5) b_j - 1`.

In particular:

`b_{j+1} ≡ (-1)^(k_{j+1}) (mod 3)`.

Status: proved.

Interpretation: the `{0,1}` subcase can be written entirely as a recurrence on zero-gap lengths and odd cores. This is a sharper arithmetic target than the `a`-map alone.

### Lemma 11e.22: Binary `{0,1}` Post-One 3-adic Reset

In the `{0,1}` gap-map notation, after a zero gap of length `k` followed by a length-`1` return, the next normalized state `a'` satisfies:

`a' ≡ -128^(-1) (mod 3^(2k+5))`.

In particular, every post-length-`1` normalized state satisfies:

`a' ≡ 31 (mod 81)`.

Status: proved.

Interpretation: long zero gaps in the `{0,1}` case reset the next post-`1` state toward a fixed `3`-adic value in the reduced coordinate, mirroring the broader binary `3`-adic reset.

### Lemma 11e.22a: Binary `{0,1}` Gap Reset-Spike Constraint

In any infinite positive `{0,1}` gap orbit with states `a_j` and zero-gap lengths `k_j`, each complete gap transition satisfies:

`a_j >= 8^(k_j)`,

and:

`a_{j+1} ≡ -128^(-1) (mod 3^(2k_j+5))`.

Consequently, if the zero-gap lengths are unbounded, then along every subsequence with `k_j -> infinity` the incoming states `a_j` tend to infinity in `R`, while the following states `a_{j+1}` converge to `-1/128` in `Q_3`.

Status: proved.

Interpretation: the unbounded reduced-gap obstruction also combines real-height spikes before long gaps with a fixed `3`-adic reset after those gaps.

### Lemma 11e.23: Binary `{0,1}` Gap Obstruction Dichotomy

If an infinite positive-integer orbit of the `{0,1}` gap map exists, then exactly one of the following holds:

- its zero-gap lengths are bounded, so its gap itinerary is an infinite non-eventually-periodic word over a finite alphabet
- its zero-gap lengths are unbounded, and the corresponding post-length-`1` normalized states have a subsequence converging to `-1/128` in `Q_3`

Status: proved.

Reason: bounded gaps give a finite alphabet and eventual periodicity is already ruled out. Unbounded gaps combine with the post-one `3`-adic reset:

`a' ≡ -128^(-1) (mod 3^(2k+5))`.

Interpretation: this is the local `{0,1}` version of the broader binary obstruction dichotomy.

### Lemma 11e.23a: Binary `{0,1}` Gap Terminal Tail Dichotomy

Fix a finite gap prefix. If the rounded gap terminal coordinate is eventually constant along an infinite suffix, then, after discarding a finite initial part of the suffix, exactly one of the following holds:

- the zero-gap lengths in the zero-increment tail are bounded, so the tail is an infinite non-eventually-periodic word over a finite alphabet
- the zero-gap lengths in the zero-increment tail are unbounded, and the corresponding later auxiliary gap states have a subsequence converging to `-1/128` in `Q_3`

Status: proved.

Reason: once the rounded terminal coordinate is constant, the gap terminal zero-increment equivalence turns the tail into an infinite positive orbit of the reduced `{0,1}` gap map. The gap obstruction dichotomy applies to that auxiliary orbit.

Interpretation: the terminal formulation introduces no third kind of obstruction. A constant rounded gap terminal coordinate is either a bounded-alphabet nonperiodic self-shadowing tail, or it repeatedly approaches the same `3`-adic reset point.

### Lemma 11e.23b: Sharpened Binary `{0,1}` Gap Endpoint

If an infinite positive-integer orbit of the reduced `{0,1}` gap map exists, then exactly one of the following holds:

- the zero-gap lengths are bounded. If `K` is their maximum and `q` is the number of distinct zero-gap lengths that occur, then the restricted minima `nu_L^(<=K)` do not tend to infinity, and the zero-gap word has factor complexity at least `m+q-1` at every length `m`
- the zero-gap lengths are unbounded. Along every subsequence with `k_j -> infinity`, the incoming states satisfy `a_j >= 8^(k_j)` and tend to infinity in `R`, while the following states satisfy `a_{j+1} ≡ -128^(-1) (mod 3^(2k_j+5))` and converge to `-1/128` in `Q_3`

Status: proved.

Reason: combine the gap obstruction dichotomy, bounded gap alphabet divergence criterion, bounded gap obstruction complexity, and gap reset-spike constraint.

Interpretation: this is the sharpest current endpoint for the reduced gap problem.

### Lemma 11e.24: Binary `{0,1}` Gap Survival Density

In the `{0,1}` gap-map coordinate `a=(n+1)/3`, the natural density of `a` admitting at least one complete next gap-to-length-`1` transition is:

`1/112`.

The density of `a` admitting at least `L` consecutive such gap transitions is:

`112^(-L)`.

Conditioned on one transition existing, the zero-gap length has law:

`P(k) = 7 / 8^(k+1)`,

with mean:

`1/7`.

If zero-gap lengths are restricted to `0 <= k <= K`, then the density of starts admitting at least `L` such bounded gap transitions is:

`((1/112)(1 - 8^(-(K+1))))^L`.

Status: proved.

Interpretation: even inside the `{0,1}` reduced problem, infinite survival is density zero. The pointwise issue remains exactly the same: density zero does not exclude a single bounded-residue 2-adic code that is a positive integer.

### Lemma 11e.24a: Binary `{0,1}` Odd-Modulus Independence

Fix an odd modulus `M` and a residue class `a ≡ s (mod M)`. Within this class, the relative natural density of `a` admitting one complete `{0,1}` gap-to-length-`1` transition is still:

`1/112`.

More generally, the relative density of `a` admitting at least `L` consecutive complete gap transitions is still:

`112^(-L)`.

Conditioned on one transition existing, the zero-gap length still has law:

`P(k) = 7 / 8^(k+1)`.

Status: proved.

Reason: for a fixed finite gap word, the gap-prefix condition selects one residue class modulo a power of `2`. Since `M` is odd, the Chinese remainder theorem combines it with any fixed odd residue class into one residue class modulo the product modulus.

Interpretation: the `3`-adic reset is useful structure but cannot by itself prove the `{0,1}` case. Any fixed odd-modulus or fixed finite `3`-adic restriction still contains the same dyadic density of finite next-gap prefixes, so the missing step must be pointwise: a height, coding, or infinite-orbit obstruction.

### Lemma 11e.24b: Binary `{0,1}` Finite Reset-Neighborhood Transparency

Fix `s >= 1` and let `c_s ≡ -128^(-1) (mod 3^s)`. Inside the finite `3`-adic reset neighborhood:

`a ≡ c_s (mod 3^s)`,

a fixed gap word `(k_0, ..., k_{L-1})` has relative natural density:

`prod_j 2^(-(3k_j+7))`.

Consequently, within this reset neighborhood, the relative density of starts admitting at least `L` complete gap transitions is `112^(-L)`, and the bounded-label density with all `0 <= k_j <= K` is:

`((1/112)(1 - 8^(-(K+1))))^L`.

Status: proved.

Interpretation: no finite `3`-adic approximation to the reset point can exclude finite gap prefixes. The unbounded reset-spike obstruction needs an infinite or height-sensitive argument, not a finite congruence trap.

### Lemma 11e.25: Binary Obstruction Dichotomy

If an infinite positive-integer binary-depth obstruction exists, then exactly one of the following holds:

- its return lengths are bounded, so its return itinerary is an infinite non-eventually-periodic word over a finite alphabet
- its return lengths are unbounded, and the post-return depth-`0` parameters have a subsequence converging to `-85/88` in `Q_3`

Status: proved.

Reason: bounded return lengths give a finite alphabet, and eventual periodicity is already ruled out. Unbounded return lengths combine with the `3`-adic reset congruence:

`n' ≡ -85/88 (mod 3^(3r+1))`.

Interpretation: this is the sharpest current split of the remaining binary case. A proof can now attack either bounded finite-alphabet nonperiodic return words, or unbounded return words whose post-return states approach a fixed `3`-adic rational.

### Lemma 11e.25a: Binary Return Terminal Tail Dichotomy

Fix a finite return prefix. If the rounded return terminal coordinate is eventually constant along an infinite suffix, then, after discarding a finite initial part of the suffix, exactly one of the following holds:

- the return lengths in the zero-increment tail are bounded, so the tail is an infinite non-eventually-periodic word over a finite alphabet
- the return lengths in the zero-increment tail are unbounded, and the corresponding later auxiliary return states have a subsequence converging to `-85/88` in `Q_3`

Status: proved.

Reason: once the rounded terminal coordinate is constant, the return terminal zero-increment equivalence turns the tail into an infinite positive orbit of the binary return-block map. The binary obstruction dichotomy applies to that auxiliary orbit.

Interpretation: the terminal self-shadowing obstruction has the same final split as the ordinary return obstruction; it is now expressed directly in the auxiliary terminal states.

### Lemma 11e.25b: Sharpened Binary Return Endpoint

If an infinite positive-integer binary-depth return obstruction exists, then exactly one of the following holds:

- the return lengths are bounded. If `R` is their maximum and `q` is the number of distinct return lengths that occur, then the restricted minima `mu_L^(<=R)` do not tend to infinity, and the return word has factor complexity at least `m+q-1` at every length `m`
- the return lengths are unbounded. Along every subsequence with `r_j -> infinity`, the incoming states satisfy `n_j >= (5*16^(r_j)-32)/33` and tend to infinity in `R`, while the following states satisfy `n_{j+1} ≡ -85/88 (mod 3^(3r_j+1))` and converge to `-85/88` in `Q_3`

Status: proved.

Reason: combine the binary obstruction dichotomy, bounded return alphabet divergence criterion, bounded return obstruction complexity, and return reset-spike constraint.

Interpretation: this is the sharpest current endpoint for the binary return problem.

### Lemma 11e.26: Binary Return Survival Density

Among depth-`0` parameters `n >= 0`, the natural density of parameters admitting at least one finite binary return block is:

`2/15`.

More generally, the natural density of parameters admitting at least `L` consecutive binary return blocks is:

`(2/15)^L`.

Status: proved.

Reason: for a fixed return length `r`, the gate is one residue class modulo `2^(4r+3)`, hence has density `2^(-(4r+3))`; summing over `r >= 0` gives `2/15`. For a fixed return word, the return-block coding proposition gives one residue class modulo the product of the block moduli, and summing over all length-`L` return words gives `(2/15)^L`.

Interpretation: infinite binary-depth return obstructions have density zero. This is still not a pointwise proof; it leaves open the possibility of a single exceptional positive integer.

### Lemma 11e.26a: Binary Return Odd-Modulus Independence

Fix an odd modulus `M` and a residue class `n ≡ s (mod M)`. Within this class, the relative natural density of depth-`0` parameters admitting one finite binary return block is still:

`2/15`.

More generally, the relative density of parameters admitting at least `L` consecutive finite binary return blocks is still:

`(2/15)^L`.

Conditioned on one return existing, the return length still has law:

`P(r) = 15 / 16^(r+1)`.

Status: proved.

Reason: for a fixed finite return word, the return-prefix condition selects one residue class modulo a power of `2`. Since `M` is odd, CRT combines this gate with any fixed class modulo `M` into one class modulo the product modulus.

Interpretation: the binary return mod-`3` trap is real structure, but it cannot by itself prove the `T = 1` case. Any fixed finite odd congruence class, including `n ≡ 2 (mod 3)`, still has the same relative dyadic density of finite next-return prefixes.

### Lemma 11e.26b: Binary Return Finite Reset-Neighborhood Transparency

Fix `s >= 1` and let `c_s ≡ -85/88 (mod 3^s)`. Inside the finite `3`-adic reset neighborhood:

`n ≡ c_s (mod 3^s)`,

a fixed return word `(r_0, ..., r_{L-1})` has relative natural density:

`prod_j 2^(-(4r_j+3))`.

Consequently, within this reset neighborhood, the relative density of starts admitting at least `L` return blocks is `(2/15)^L`, and the bounded-label density with all `0 <= r_j <= R` is:

`((2/15)(1 - 16^(-(R+1))))^L`.

Status: proved.

Interpretation: no finite `3`-adic approximation to the return reset point can rule out finite return prefixes. The reset-spike obstruction must be attacked through the infinite pointwise orbit or through a height/counting theorem.

### Lemma 11e.27: Binary Return-Length Law

Conditioned on the existence of one finite binary return block, the return length `r` has distribution:

`P(r) = 15 / 16^(r+1)`.

The conditional mean return length is:

`E(r) = 1/15`.

If return lengths are restricted to `0 <= r <= R`, then the density of starts admitting at least `L` such bounded return blocks is:

`((2/15) * (1 - 16^(-(R+1))))^L`.

Status: proved.

Interpretation: the binary return process is overwhelmingly concentrated on zero-return blocks. This explains why long finite shadows in computation tend to be all-zero prefixes, while still leaving the pointwise exceptional-code problem open.

### Lemma 11f: Binary Return Mod-3 Trap

For every binary return block `0 -> 1^r -> 0`, the output depth-`0` parameter satisfies:

`n_{j+1} ≡ 2 (mod 3)`.

Reason:

`Q_r n_{j+1} = P_r n_j + D_r`,

with `P_r = 9 * 27^r ≡ 0 (mod 3)`, `Q_r = 2^(4r+3) ≡ -1 (mod 3)`, and `D_r ≡ 1 (mod 3)`. Therefore `-n_{j+1} ≡ 1 (mod 3)`.

Status: proved.

This does not close the binary-depth case, but it further constrains every return after the first: all later depth-`0` parameters lie in `2 mod 3`.

### Lemma 11g: Bounded-Depth Real Expansion

For a growth-B continuation prefix of length `N` with depths `0 <= t_i <= T`, the affine multiplier from `m_0` to `m_N` is:

`A_N / B_N = (9/8)^N (3/2)^(sum_{i=0}^{N-1} t_i) 2^(t_0 - t_N)`.

Therefore:

`A_N / B_N >= 2^(-T) (9/8)^N`.

Status: proved.

This proves uniform real expansion on every bounded-depth branch. It does not prove bounded-depth termination, because a positive integer orbit could grow in the expanding direction. The missing part is arithmetic: the congruence gates must be shown impossible to satisfy forever by a fixed positive integer start.

### Lemma 12: Exact 2-adic Coding of Infinite Growth-B Chains

For every infinite sequence of nonnegative integers:

`(t_0, t_1, t_2, ...)`

there is a unique 2-adic integer:

`m(t_0, t_1, ...) in Z_2`

such that any infinite growth-B chain with this depth sequence must start with:

`m_0 = m(t_0, t_1, ...)`.

Construction:

Let:

- `a_i = 3^(t_i + 2)`
- `b_i = 2^(t_{i+1} + 3)`

The continuation equations are:

`b_i m_{i+1} = a_i m_i + 1`.

Composing the first `n` equations gives:

`B_n m_n = A_n m_0 + C_n`

with:

- `A_{n+1} = a_n A_n`
- `B_{n+1} = b_n B_n`
- `C_{n+1} = a_n C_n + B_n`

Thus any integer solution must satisfy:

`m_0 ≡ -C_n A_n^(-1) (mod B_n)`.

The moduli `B_n` are increasing powers of `2`, and the congruence classes are nested. Their inverse limit is the unique 2-adic code.

Status: proved. An infinite positive integer growth-B chain exists if and only if the corresponding 2-adic code is a positive odd integer.

### Lemma 13: Integer-Code Boundedness Criterion

Let `r_n` be the least nonnegative residue of the length-`n` prefix code modulo `B_n`.

Then the infinite 2-adic code is a nonnegative ordinary integer iff `r_n` is bounded as an integer. Equivalently, this happens iff `r_n` is eventually constant.

Proof:

- If the code is an ordinary integer `M`, then once `B_n > M`, `M mod B_n = M`, so `r_n = M`.
- If `r_n` is bounded by `R`, then once `B_n > R`, nesting forces all later residues equal to `r_n`.
- If `r_n` is eventually constant at `M`, then `M` satisfies every prefix congruence, so the inverse-limit code is exactly `M`.

Status: proved.

### Lemma 14: Prefix Digit Recurrence

Let `r_n` be the prefix residue modulo `B_n`. Write:

`r_{n+1} = r_n + d_n B_n`

where `0 <= d_n < b_n = 2^(t_{n+1}+3)`. If:

`s_n = (A_n r_n + C_n) / B_n`

then:

`d_n ≡ -(3^(t_n+2)s_n + 1) A_{n+1}^(-1) (mod b_n)`.

Therefore the residue stabilizes at step `n` iff:

`3^(t_n+2)s_n + 1 ≡ 0 (mod 2^(t_{n+1}+3))`.

Status: proved.

This turns the remaining integer-code problem into a digit problem. A positive integer obstruction requires `d_n = 0` for every sufficiently large `n`.

### Lemma 15: Zero-Digit Tail Equivalence

For a finite depth prefix, define the auxiliary co-state:

`s_n = (A_n r_n + C_n) / B_n`.

Then a zero extension digit `d_n = 0` is equivalent to the divisibility:

`2^(t_{n+1}+3) | 3^(t_n+2)s_n + 1`.

When this holds, define:

`s_{n+1} = (3^(t_n+2)s_n + 1) / 2^(t_{n+1}+3)`.

A run of zero digits:

`d_n = d_{n+1} = ... = d_{n+L-1} = 0`

is equivalent to the finite recurrence:

`2^(t_{j+1}+3)s_{j+1} = 3^(t_j+2)s_j + 1`

for `n <= j < n+L`.

Therefore an eventually constant prefix-residue tail is equivalent to an infinite positive integer orbit in the growth-B continuation domain, starting from the auxiliary state `s_n`.

Status: proved.

Consequence: the digit target and Missing Lemma C are not two different problems. The digit target is Missing Lemma C written in prefix-code coordinates.

## Missing Pointwise Lemmas

### Missing Lemma A: Growth-B Termination Bound

Candidate statement:

`growth_B_chain_length(x) <= C log2(m0) + C0`

for every strict growth-B chain starting with parameter `m0`.

Empirical candidate:

`growth_B_chain_length(x) <= 0.55 log2(m0) + 3`.

Why it matters: this would turn the Quartering Law from an average statement into a pointwise growth-control theorem.

Current status: heavily tested, not proved.

### Missing Lemma B: Epoch Recovery Bound

Candidate statement:

For every odd `x > 1`, after the initial growth phase and recovery phase:

`F^n(x) < x`

for some `n <= C log2(x)`.

Why it matters: this directly proves descent below the starting value.

Current status: empirically strong, but proving it is essentially the Collatz difficulty in FMF form.

### Missing Lemma C: No Infinite Integer Orbit In Growth-B Domain

Candidate statement:

The map

`m -> odd_part((3^(t+2)m + 1) / 8)`

restricted to the growth-B continuation domain has no infinite orbit in positive integers.

Why it matters: it would exclude the most dangerous sustained-growth mechanism.

Current status: true in all tested finite searches; not proved. Haar-measure arguments in `Z_2` do not settle integer orbits because `Z` has Haar measure zero inside `Z_2`.

By Lemma 9, every finite prefix of an infinite obstruction is compatible with infinitely many positive starts. By Lemma 8, an actual infinite obstruction cannot have an eventually periodic depth sequence. By Lemma 11, after one step it must also live in the corresponding modulo-24 class determined by depth parity. Therefore the remaining bad case is sharply isolated:

> a positive integer whose growth-B depth sequence is infinite and non-eventually-periodic.

By Lemma 12, this is equivalent to:

> a non-eventually-periodic infinite depth word whose exact 2-adic code is a positive odd integer.

By Lemma 13, this sharpens to:

> For every non-eventually-periodic infinite depth word, prove the prefix residues `r_n` are unbounded.

By Lemma 14, an equivalent digit version is:

> For every non-eventually-periodic infinite depth word, prove the prefix digits `d_n` are nonzero infinitely often.

By Lemma 15, this digit version is exactly the no-infinite-positive-integer-growth-B-continuation problem in the auxiliary co-state. It is a useful coordinate change, but it does not remove the core difficulty.

### Missing Lemma D: Binary Return Partial-Map Termination

Candidate statement:

The partial map on depth-`0` return parameters,

`33n + 32 = 16^r w`, with `w` odd and `w ≡ 7 (mod 8)` for even `r`, `w ≡ 5 (mod 8)` for odd `r`,

`T(n) = (3 * 27^r * w - 85) / 88`,

has no infinite positive orbit.

Equivalent formulations:

- every non-eventually-periodic return-length word has unbounded return-prefix residues
- no positive integer `M` satisfies `v_2(P_N M + D_N) >= 3N + 4(r_0 + ... + r_{N-1})` for every prefix of its forced return itinerary
- no balanced nonperiodic return critical series lands 2-adically on a positive ordinary integer

Why it matters: this would settle the full bounded-depth `T = 1` binary case.

Current status: reduced to a deterministic partial-map problem; finite scans find only short forced orbits, but every finite return word is still realizable by infinitely many starts, so finite scans are evidence only.

### Missing Lemma E: Binary `{0,1}` Gap Partial-Map Termination

Candidate statement:

The reduced gap partial map,

`a = 8^k b`, `3 * 9^k * b ≡ 49 (mod 128)`,

`G(a) = (3^(2k+5)b - 1) / 128`,

has no infinite positive orbit.

Equivalent formulations:

- every non-eventually-periodic zero-gap word has unbounded gap-prefix residues
- no positive integer `A` satisfies `v_2(A_N A - C_N) >= 7N + 3(k_0 + ... + k_{N-1})` for every prefix of its forced gap itinerary
- no balanced nonperiodic gap critical series lands 2-adically on a positive ordinary integer

Why it matters: this is the smallest currently isolated nontrivial finite-alphabet subcase of Missing Lemma D.

Current status: reduced to a deterministic partial-map problem. The latest forced-orbit scan up to `a <= 5,000,000` finds maximum length `3`, at start `a = 800,827` with gap word `(0, 2, 1)`. This is supporting evidence only.

### Resolved Lemma F: Balanced Ordinary Landing Exclusion

Candidate statement:

No non-eventually-periodic balanced infinite binary word has a nonnegative ordinary return code or a positive ordinary reduced-gap code.

Equivalent formulations:

- the balanced return minima `mu_L^bal` tend to infinity
- the balanced reduced-gap minima `nu_L^bal` tend to infinity
- no mechanical/Sturmian binary critical series with irrational slope `alpha in (0,1)` and intercept `rho in [0,1)` lands 2-adically on an ordinary positive integer

Why it mattered: this was the minimal-complexity finite-alphabet frontier. Lemmas 11e.1x4a through 11e.1x4p, 11e.1x5, 11e.1x6, 11e.18b5, and 11e.18b6 reduce any balanced counterexample to a lower mechanical Sturmian word, then contradict the delayed prefix-recurrence behavior forced by an ordinary landing. The balanced/Sturmian obstruction class is now removed; the remaining finite-alphabet obstruction must have higher factor complexity than balanced words.

Current status: proved for the balanced/Sturmian frontier. The direct balanced verifier `explorations/explore73_balanced_frontier.py` remains supporting finite evidence through length `64`, not part of the proof.

Natural subtargets:

1. Proved/imported: rational-slope balanced infinite binary words are ultimately periodic, hence already excluded by the periodic-branch lemmas.
2. Proved: no lower irrational mechanical word with normalized intercept `rho in [0,1)` can make the return or reduced-gap critical series land on an ordinary positive integer.
3. Upgrade from balanced/minimal-complexity words to higher-complexity uniformly positive-density aperiodic words.

## Conditional Proof Skeleton

If Missing Lemma B is proved, then Collatz follows:

1. Start from any odd `x > 1`.
2. Lemma B gives an FMF iterate `y = F^n(x)` with `y < x`.
3. Repeat from `y`.
4. The odd positive integers are well-ordered, so repeated strict descent must terminate.
5. The only terminal odd value under the accelerated Collatz map is `1`.

If only Missing Lemma A is proved, more work remains:

1. Lemma A bounds sustained strict growth.
2. Lemma 2 gives deterministic Type A contraction.
3. Lemma 5 gives average recovery pressure.
4. A separate pointwise recovery lemma is still needed to turn bounded growth into descent below the starting value.

## Main Research Target

The cleanest next theorem to attack is Missing Lemma B. It is stronger than the growth-B termination lemma and exactly matches what the Collatz proof needs:

> Every FMF epoch descends below its starting value in `O(log x)` hops.

This should be treated as the central conjecture of the FMF framework until proved or falsified.

## Current Bridge Tests

`explorations/explore45_bridge_lemmas.py` tests the pointwise bridge candidates.

Latest run:

- Odd `x` in `[3, 200000]`
- Growth-B bound `length <= 0.55 log2(m0) + 3`: `0` violations
- Worst growth-B ratio: `x = 4591`, length `7`, `m0 = 287`, ratio `0.934`
- Epoch bound `duration <= 3.2 log2(x)`: `0` violations
- Worst epoch ratio: `x = 27`, duration `15`, peak `911`, ratio `3.155`
- Mersenne scan through `2^50 - 1`: all descended in the tested epoch bound regime
- Periodic depth patterns with period `<= 5` and `t <= 7`: `0` positive odd integer fixed points
- Finite depth words with length `<= 4` and `t <= 3`: all `340` words realized by some positive odd `m`; maximum found `m = 478065`
- Explicit zero-depth family `m_i = 9^i 8^(L-i) - 1`: verified for `L <= 20`
- Exact zero-depth classification `m0 ≡ -1 (mod 8^L)`: verified for `L <= 8`, `m0 <= 200000`

`explorations/explore46_infinite_code.py` computes the prefix residues:

`m_0 ≡ -C_n A_n^(-1) (mod B_n)`

for sample infinite depth words. It confirms the exact code behavior:

- constant zero depths converge to the 2-adic code `-1`
- periodic words show repeating low-bit patterns, matching Lemma 8
- nonperiodic sample words produce well-defined 2-adic codes with no visible finite-integer stabilization
- smallest-residue search over words of length `<= 8` and `t <= 3` found no stabilizing code; the smallest residues still jump upward, with best length-8 residue `40885`
- zero extension-digit search over words of length `9` and `t <= 3` found longest unchanged-residue run `4`

Negative guidance:

- finite runs with `d_n = 0` do occur, including runs of length `4` in small bounded alphabets
- therefore the proof cannot show "zero digits never occur"
- the required theorem is strictly tail-based: `d_n = 0` cannot hold eventually unless the depth word is eventually periodic or otherwise non-integer-coded

`explorations/explore47_integer_code_search.py` searches the exact positive-integer continuation obstruction. It scans ordinary integer pairs `(m0, t0)` under the deterministic recurrence:

`q_i = (3^(t_i+2)m_i + 1) / 8`

`t_{i+1} = v2(q_i)`

`m_{i+1} = odd_part(q_i)`

continuing only when `3^(t_i+2)m_i ≡ 7 (mod 8)`, i.e. when the current hop is growth-B and the output remains Type B.

Latest bounded run:

- Command: `python3 explorations/explore47_integer_code_search.py --max-m0 1000000 --max-t0 24`
- Scanned odd `m0 <= 1000000` and `0 <= t0 <= 24`
- Longest continuation survivor: `m0 = 999053`, `t0 = 9`, length `11`
- Final state after those continuations: `m = 9320788991825`, `t = 0`
- Best length ratio: `length / log2(m0) = 0.552`
- Tail counts: length `9`: `26`, length `10`: `11`, length `11`: `1`

Interpretation:

- This is direct evidence for Missing Lemma C in the searched region.
- It also shows why the empirical coefficient near `0.55 log2(m0)` is not arbitrary: the best bounded continuation ratio lands essentially on that scale.
- It is not proof. Finite searches cannot exclude a larger positive integer code or an unbounded-depth construction.

`explorations/explore48_bounded_depth_beam.py` searches bounded-depth alphabets for small prefix residues and long zero-extension runs.

Latest bounded-depth beam runs:

- `t <= 1`, length `50`, beam `2000`: best residue has `136` bits; longest observed zero-run among beam survivors `5`
- `t <= 2`, length `45`, beam `5000`: best residue has `118` bits; longest observed zero-run among beam survivors `8`
- `t <= 3`, length `40`, beam `8000`: best residue has `101` bits; longest observed zero-run among beam survivors `8`

Interpretation:

- These searches support a possible bounded-depth version of Missing Lemma C: for fixed `T`, prefix residues over depth alphabet `{0, ..., T}` may tend to infinity.
- The data is not proof because the search is beam-pruned after the exact small lengths.
- If this bounded-depth theorem were proved, any infinite positive-integer growth-B obstruction would have to use unbounded depths.

`explorations/explore49_bounded_depth_graph.py` tests a finite-state over-approximation for bounded-depth growth-B paths using states `(t, m mod 2^K)`.

Latest finite-quotient runs:

- `T = 0`, `K <= 14`: cyclic nodes persist; the cyclic residue is `(0, 2^K - 1)`, the finite shadow of the negative 2-adic code `-1`
- `T = 1`, `K <= 14`: cyclic nodes persist and slowly grow in count
- `T = 2`, `K <= 12`: cyclic nodes persist
- `T = 3`, `K <= 11`: cyclic nodes persist

Interpretation:

- Acyclicity of finite residue quotients is not the right bounded-depth proof strategy.
- Persistent finite cycles can be shadows of negative 2-adic periodic codes, which are already ruled out as positive integers by Lemma 8.
- A valid proof must use an ordinary-integer height/bounded-residue argument, not just finite-state graph acyclicity.

`explorations/explore50_binary_depth_affine.py` checks the exact affine normal form for depth alphabet `{0, 1}`.

Latest run:

- Affine maps verified for `n <= 100000`
- Transition gates:
  - `0 -> 0`: `n ≡ 7 (mod 8)`
  - `0 -> 1`: `n ≡ 0 (mod 16)`
  - `1 -> 0`: `n ≡ 3 (mod 8)`
  - `1 -> 1`: `n ≡ 14 (mod 16)`
- Longest binary-depth tail found for `n <= 500000`: length `7`, at `(t0, n0) = (0, 170047)`
- Binary zero-return expansion verified on `66666` admissible returns in the same range
- Return-block gates `0 -> 1^r -> 0` computed for `0 <= r <= 12`; each is one residue class modulo `2^(4r+3)`

`explorations/explore51_binary_return_code.py` computes the compressed return-block 2-adic code for binary-depth paths.

Latest run:

- Return blocks, the closed gate formula, the return reparameterization, and the mod-3 trap verified for `r <= 20`
- Binary return critical series verified for length `<= 5` and return lengths `r <= 5` (`9,330` words)
- Binary return ordinary-landing divisibility verified for length `<= 5` and return lengths `r <= 4` (`3,905` words)
- Binary return-prefix digit recurrence verified on `3,905` finite extensions with return lengths `r <= 4`, including `102` zero digits
- Binary return landing growth envelope verified for finite return words with return lengths `r <= 4`
- Binary return odd-modulus independence verified for odd moduli `(3, 5, 7, 9, 11, 13, 25, 81)`, one-step return lengths `r <= 12`, and `780` finite return words
- Smallest return-code prefixes for block lengths `r <= 4`:
  - length `1`: residue `7`, word `(0,)`
  - length `2`: residue `63`, word `(0, 0)`
  - length `3`: residue `511`, word `(0, 0, 0)`
  - length `6`: residue `170047`, word `(0, 0, 1, 0, 0, 0)`

Interpretation:

- The all-zero return-block word is the already-proved `-1` 2-adic code.
- Nonconstant finite return-block patterns are computable by the same nested-congruence mechanism.
- No positive integer infinite binary-depth code has been found.

`explorations/explore54_return_minima.py` certifies least prefix residues in the binary return-block system using Lemma 11e.1w.

Latest run:

- Exact least return-prefix residues certified for lengths `1` through `20`
- The length-`20` minimum is `1,152,921,504,606,846,975`, with the all-zero word
- The length-`15` certificate shows a finite plateau: the minimum remains `4,398,046,511,103`, now realized by `(0,0,0,0,0,0,0,0,0,0,0,0,0,0,1)`
- The certificate uses the inequality `16^r Q_i < 33(P_i B + D_i) + 32Q_i` to make the search exhaustive below height `B`

Interpretation:

- Return-prefix residues appear to grow, but not strictly at every length.
- By Lemma 11e.1x, proving these global minima tend to infinity is equivalent to ruling out nonnegative ordinary binary return codes.

`explorations/explore52_binary_partial_map.py` verifies the single partial-map formulation of the binary-depth return dynamics.

Latest run:

- Partial map verified against direct step-by-step simulation for `0 <= n <= 2,000,000`
- Exact one-return survival density verified as `2/15`, with length-`L` survival density `(2/15)^L`
- Conditional return-length law verified: `P(r) = 15 / 16^(r+1)` for checked return lengths
- Binary return odd-modulus independence verified for odd moduli `(3, 5, 7, 9, 11, 13, 25, 81)`, one-step return lengths `r <= 12`, and `780` finite return words
- Binary return reset-neighborhood transparency verified for `3^s`, `s <= 4`, length `<= 4`, and return lengths `r <= 4`
- Binary `y`-normal form verified on `133,333` returns for `n <= 1,000,000`
- All-zero binary return branch verified for `L <= 20`
- Periodic binary return obstruction verified for periods `<= 5` and return lengths `r <= 5` (`9,330` words)
- Periodic `{0,1}` gap obstruction verified for periods `<= 5` and zero gaps `<= 5` (`9,330` words)
- All-zero `{0,1}` gap branch verified for `L <= 12`
- Constant `{0,1}` gap branches verified for gaps `<= 8` and `L <= 6`
- Finite binary return words verified for length `<= 5` and return lengths `r <= 5` (`9,330` words)
- Binary `3`-adic reset verified for return lengths `r <= 12`
- Binary `{0,1}` gap `3`-adic clock verified for zero gaps `<= 12`
- Binary `{0,1}` gap map verified for zero gaps `<= 12`
- Binary `{0,1}` gap critical series verified for length `<= 5` and gaps `<= 4` (`3,905` words)
- Binary `{0,1}` gap ordinary-landing divisibility verified for length `<= 5` and gaps `<= 4` (`3,905` words)
- Binary `{0,1}` gap landing growth envelope verified for length `<= 5` and gaps `<= 4` (`3,905` words)
- Binary `{0,1}` gap partial map verified for zero gaps `<= 12`
- Direct binary `{0,1}` gap partial-map scan found longest forced gap orbit for `a <= 5,000,000`: start `a = 800,827`, gap word `(0, 2, 1)`
- Finite `{0,1}` gap words verified for length `<= 4` and gaps `<= 5` (`1,554` words)
- Gap-prefix codes verified for length `<= 4` and gaps `<= 5` (`1,554` words)
- Gap-prefix monotonicity and a finite plateau example verified
- Gap-prefix digit recurrence verified on `3,905` finite extensions, including `4` zero digits
- Binary `{0,1}` gap survival density verified as `1/112`, with conditional law `P(k)=7/8^(k+1)` for checked gaps
- Binary `{0,1}` odd-modulus independence verified for odd moduli `(3, 5, 7, 9, 11, 13, 25, 81)`, one-step gaps `<= 12`, and `780` finite gap words
- Binary `{0,1}` gap reset-neighborhood transparency verified for `3^s`, `s <= 4`, length `<= 4`, and gaps `<= 4`
- Binary `{0,1}` gap-core recurrence verified for consecutive gaps `<= 8`
- Binary `{0,1}` post-one `3`-adic reset verified for zero gaps `<= 12`
- Longest binary return orbit found for `n <= 20,000,000`: start `n = 16,777,215`, return word `(0, 0, 0, 0, 0, 0, 0, 0)`

`explorations/explore53_gap_minima.py` certifies least prefix residues in the reduced `{0,1}` gap system using Lemma 11e.18a.

Latest run:

- Exact least gap-prefix residues certified for lengths `1` through `14`
- The length-`14` minimum is `40172331663434910254977164475`, with word `(0,0,0,0,0,0,0,0,0,0,0,0,1,0)`
- The certificate is not a raw bounded-gap scan: for each height bound `B`, it uses the inequality `8^k H_i < A_i B` to make the search tree finite and exhaustive below `B`

Interpretation:

- These data support the height-growth conjecture for reduced `{0,1}` gap codes.
- By Lemma 11e.18b, proving these global minima tend to infinity is equivalent to ruling out positive ordinary reduced gap codes.

`explorations/explore55_height_survival.py` computes the dual fixed-height survival depths.

Latest default run:

- Return-prefix residues below `2^52` survive for at most `18` return blocks
- Gap-prefix residues below `2^64` survive for at most `9` complete gap transitions
- The computation is exact for the displayed bounds, using the same finite-height pruning inequalities as `explore53` and `explore54`

Interpretation:

- This is the finite-height form of the global-minimum target: for every fixed height bound `B`, prove a finite maximum survival depth.
- Equivalently, prove that the maximum survival depth tends to infinity only when `B` tends to infinity.

`explorations/explore56_counting_discrepancy.py` measures exact finite-height prefix counts against the natural density rates.

Latest default run:

- Return samples up to `B = 2^52 - 1`: worst normalized count against `(B+1)(2/15)^L` is about `2.14`
- Gap samples up to `B = 2^64 - 1`: worst normalized count against `B(1/112)^L` is about `1.80`
- These are exact finite-height counts for the displayed bounds, not Monte Carlo estimates

Interpretation:

- The data supports the prefix-counting route: a uniform discrepancy constant may be plausible.
- This remains evidence only; the missing theorem is a proof that the normalized counts stay bounded uniformly in both `B` and `L`.

`explorations/explore57_start_counts.py` verifies the start-count bridge from prefix residue classes to ordinary starts.

Latest default run:

- Return start counts agree with direct iteration for selected cases up to `B = 2^20 - 1`
- Gap start counts agree with direct iteration for selected cases up to `B = 2^24 - 1`
- In each tested case, the exact inequalities from Lemma 11e.1zc and Lemma 11e.18g hold:
  `N_R <= A_R <= N_R + (B+1)(2/15)^L` and `N_G <= A_G <= N_G + B 112^{-L}`

Interpretation:

- Prefix-class counts and ordinary-start counts are not identical, especially at shallow levels.
- The exact reciprocal-modulus correction shows that proving the prefix-counting discrepancy theorem would also control ordinary-start counts.

`explorations/explore58_critical_discrepancy.py` scans the all-height normalized discrepancy at critical prefix residues.

Latest default run:

- Return samples through `B = 2^56 - 1`: worst critical ratio is about `4.46`, at level `16`, height `67477744910335`, count `3`
- Gap samples through `B = 2^72 - 1`: worst critical ratio is about `9.63`, at level `4`, height `32679099`, count `2`
- These values are higher than the dyadic-endpoint ratios from `explore56`, showing that the worst finite-height discrepancy can occur inside a dyadic interval

Interpretation:

- The critical-height reduction makes the uniform discrepancy target more concrete: control clustering of realized least residues near small critical heights.
- The current evidence still supports bounded discrepancy, but with constants larger than the dyadic-endpoint scan suggested.

`explorations/explore59_critical_clusters.py` records the finite words responsible for the largest critical ratios found by `explore58`.

Latest default run:

- Return critical cluster at level `16`, height `67477744910335`, count `3`, with words
  `(0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0)`,
  `(0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0)`, and
  `(0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0)`
- Gap critical cluster at level `4`, height `32679099`, count `2`, with words `(1,0,0,0)` and `(0,0,0,0)`
- The return witnesses land at three distinct terminal states, consistent with return prefix terminal injectivity
- The two gap witnesses merge after one transition at state `62039227`, then share the tail to terminal state `424478101`

Interpretation:

- A proof of the rank bound must control not just the minimum residue, but small clusters of nearby low residues.
- Forward merging is absent in the return prefix map but present in the reduced gap map, where it is controlled by the backward `3`-adic gate.

`explorations/explore60_backward_branches.py` verifies the backward branch formulas for the return and gap partial maps.

Latest default run:

- Return backward branches, return backward-length bound, return backward contraction, return backward path contraction, return cubic-mass contraction, the 3-adic branch gate, and backward uniqueness verified against direct partial-map iteration for `n_next <= 200000`, return lengths `r <= 12`, starts `<= 50000`, and path depth `<= 8`
- Gap backward branches, gap backward-length bound, gap backward contraction, gap backward path contraction, gap cubic-mass contraction, exact 3-adic branch count, merge-chain ratio, merge-multiplicity bound, and merge-mass bound verified against direct partial-map iteration for `a_next <= 200000`, gap lengths `k <= 12`, starts `<= 50000`, and path depth `<= 8`
- Return and gap expansion-pressure bases verified as `> 1` at `theta=2` and `< 1` at `theta=3`, with roots approximately `2.567424` and `2.264831` and exact tail checks through labels `<= 8`

Interpretation:

- For the return map, a fixed terminal state has at most one backward preimage across all return lengths.
- For the gap map, backward branch count is exactly controlled by `v3(128a'+1)`.
- Gap backward preimages of a fixed terminal state form a finite geometric chain with ratio `8/9`.
- Immediate gap merge multiplicity is logarithmic in terminal height, and the total immediate preimage mass is at most `(43/9)` times terminal height.
- Valid backward paths strictly decrease height exponentially in both path length and total branch-label sum.
- Both immediate backward maps are strict contractions for cubic mass.
- Expansion-weighted word mass is also subcritical at cubic order.
- This reframes the critical-rank theorem as a problem of bounding arithmetic branching in contracting backward preimage trees.

`explorations/explore61_frontier_moments.py` tests whether cubic-mass contraction directly controls low finite-height frontiers.

Latest default run:

- Return normalized frontier cubic mass grows from about `4.06` at `B=2^24-1` to about `501.37` at `B=2^48-1`
- Gap normalized frontier cubic mass grows from about `1.00` at `B=2^24-1` to about `94.18` at `B=2^56-1`
- These are exact finite-height frontier computations for the displayed bounds

Interpretation:

- Immediate backward moment contraction is real, but it does not by itself prove the critical-rank bound.
- A successful proof needs an additional terminal-height, escape, or stopping-time estimate connecting the contracting backward fibers to the low-residue frontier.

`explorations/explore62_terminal_windows.py` verifies the terminal-window identities for low finite-height prefix residues.

Latest default run:

- Return terminal windows verified for all low prefixes through `B=2^32-1`, covering `658` windows across `10` levels
- Gap terminal windows verified for all low prefixes through `B=2^32-1`, covering `70` windows across `4` levels

Interpretation:

- Low return residues satisfy `R <= U/E < R+1`, so `R<=B` forces `U<E(B+1)`.
- Low gap residues satisfy `S-1/115 < u/E < S`, so `S<=B` forces `u<EB`.
- This is the exact terminal-height window a stopping-time proof must count.

`explorations/explore63_terminal_profiles.py` profiles expansion factors and terminal states for exact low finite-height frontiers.

Latest default run:

- Return profile for `B=2^32-1`: low frontiers survive through level `10`; expansion factors range from at least `1.125` at level `1` to at least `3.247` at level `10`, while terminal states reach `154,993,677,308` on the displayed frontier
- Gap profile for `B=2^32-1`: low frontiers survive through level `4`; expansion factors range from at least `1.898` at level `1` to at least `12.989` at level `4`, while terminal states reach `39,290,960,254`

`explorations/explore69_window_shells.py` refines this by grouping the same low normalized terminal-window frontiers into dyadic expansion shells.

Latest default run:

- Return frontiers are now checked for `B=2^32-1`, `2^36-1`, and `2^40-1`. At `B=2^40-1` they survive through level `13`; the shell range reaches `[0,7]` in the middle levels and narrows to `[2,2]` at the final checked level.
- Gap frontiers are now checked for `B=2^32-1`, `2^36-1`, and `2^40-1`. At `B=2^40-1` they survive through level `6`; the shell range moves from `[0,2]` at level `1` to `[5,5]` at the final checked level.

Interpretation:

- The low-window obstruction is not explained by a single expansion scale.
- The next theorem must separate normalized terminal heights arithmetically inside and across expansion shells.

`explorations/explore70_bounded_alphabet_minima.py` exhaustively checks the first nonconstant bounded alphabets: return lengths `{0,1}` and reduced zero-gap lengths `{0,1}`.

Latest default run:

- Return `{0,1}` minima verified through length `20`; the fixed-one-count profile is now checked through length `21`.
- Gap `{0,1}` minima verified through length `20`; the fixed-one-count profile is now checked through length `21`. At length `3` the bounded-alphabet minimum is the all-zero word with residue `1,221,819`, while the unrestricted global gap minimum uses the word `(0,2,1)`.
- Length `20` bounded minima: return minimum `1,152,921,504,606,846,975`; gap minimum `5,327,483,134,500,439,866,600,283,610,852,124,435,643`.
- The verifier reports the number of `1` labels in each minimizing word; the checked minimizers are sparse in `1`s.
- Optional runs such as `--profile-ones 18`, `--profile-ones 19`, `--profile-ones 20`, and `--profile-ones 21` report the least residue in every fixed-one-count stratum.
- The fixed-one-count strata are now settled theoretically by Lemmas 11e.1x2 and 11e.18b2.
- Lemmas 11e.1x3 and 11e.18b3 rule out bounded-defect perturbations of any eventually periodic template. The remaining `{0,1}` sparse problem must have the number of `1` labels tending to infinity and unbounded edit distance from every periodic shadow.

Interpretation:

- These are finite checks for the first genuinely nonconstant bounded-alphabet targets `mu_L^(<=1) -> infinity` and `nu_L^(<=1) -> infinity`.
- The data support divergence but do not prove the infinite bounded-alphabet theorem; finite enumeration cannot replace a proof for words with infinitely many `1` labels.

`explorations/explore71_aperiodic_templates.py` probes canonical aperiodic `{0,1}` templates after the periodic-shadow lemmas:

- Fibonacci, Thue-Morse, period-doubling, and the irrational mechanical word of slope `sqrt(2)-1` were checked through length `1024`.
- In all four probes, return and reduced-gap prefix-residue bit lengths grow roughly linearly with prefix length.

Interpretation:

- These probes support the view that low-complexity aperiodic templates still diverge.
- They are not a proof; the remaining theorem must cover all genuinely aperiodic bounded-alphabet words, not just named examples.

`explorations/explore73_balanced_frontier.py` enumerates balanced binary words directly, targeting the balanced/Sturmian-like frontier isolated by Lemmas 11e.1x5 and 11e.18b5.

Latest default run:

- Balanced binary words checked through length `64`; the level-`64` balanced frontier contains `27,834` words.
- At length `64`, the least balanced return-prefix residue has bit length `186` and uses `2` one-labels.
- At length `64`, the least balanced reduced-gap prefix residue has bit length `444` and uses `2` one-labels.
- The default run asserts this final summary: `(64, 27834, 186, 2, 444, 2)`.

Interpretation:

- Balanced prefixes remain consistent with divergence at the minimal-complexity frontier.
- The minimizing balanced words are still sparse finite shadows, so this does not replace the proof obligation to exclude non-eventually-periodic balanced ordinary codes.

`explorations/explore74_mechanical_landing.py` verifies the mechanical landing normal form on exact quadratic-irrational mechanical words.

Latest default run:

- Checks lower and upper mechanical words for slopes `sqrt(2)-1`, `sqrt(3)-1`, and `sqrt(5)-2` with exact rational intercepts through length `128`.
- For each prefix it verifies the telescoping prefix-sum formula, the return coefficient/modulus/additive recurrence, and the reduced-gap coefficient/modulus/additive recurrence against the existing prefix engines.
- The default run asserts the final summaries:
  `("sqrt2-minus-1-lower-rho0", 128, 53, 595, 1050)`,
  `("sqrt2-minus-1-upper-rho1_3", 128, 53, 596, 1055)`,
  `("sqrt3-minus-1-lower-rho1_2", 128, 94, 759, 1178)`,
  `("sqrt3-minus-1-upper-rho2_3", 128, 94, 759, 1178)`,
  `("sqrt5-minus-2-lower-rho1_5", 128, 30, 497, 986)`, and
  `("sqrt5-minus-2-upper-rho3_5", 128, 30, 504, 985)`.

Extended diagnostic run:

- `python3 explorations/explore74_mechanical_landing.py --length 512`
- At length `512`, the lower-convention samples have:
  `sqrt2-minus-1` with `212` ones, return bit length `2384`, gap bit length `4217`;
  `sqrt3-minus-1` with `375` ones, return bit length `3032`, gap bit length `4708`;
  `sqrt5-minus-2` with `121` ones, return bit length `2019`, gap bit length `3947`.

Interpretation:

- This is regression coverage for the mechanical prefix and divisibility normal forms, Lemmas 11e.1x4i and 11e.1x4j, with samples from both conventions.
- It does not prove the irrational mechanical landing exclusion; it verifies that the new normal form matches the established prefix-residue algebra on representative exact irrational samples.

`explorations/explore75_mechanical_recurrence.py` checks the new prefix-recurrence obstruction on exact lower mechanical samples.

Latest default run:

- `python3 explorations/explore75_mechanical_recurrence.py`
- For `sqrt(2)-1`, the thresholds are approximately return `9.649` and gap `8.282`; the observed milestone recurrence ratios through length `128` are `0.625`, `1.812`, `0.906`, `0.453`, and `1.320`.
- For `sqrt(3)-1`, the thresholds are approximately return `8.205` and gap `8.765`; the observed ratios are `0.500`, `1.625`, `1.750`, `0.875`, and `0.438`.
- For `sqrt(5)-2`, the thresholds are approximately return `11.330` and gap `7.988`; the observed ratios are `0.500`, `1.062`, `0.531`, `1.125`, and `1.258`.
- All default milestone ratios are below both the return and reduced-gap obstruction thresholds.
- The default run asserts the first recurrence snapshots:
  `("sqrt2-minus-1-lower-rho0", ((8,5), (16,29), (32,29), (64,29), (128,169)))`,
  `("sqrt3-minus-1-lower-rho1_2", ((8,4), (16,26), (32,56), (64,56), (128,56)))`, and
  `("sqrt5-minus-2-lower-rho1_5", ((8,4), (16,17), (32,17), (64,72), (128,161)))`.

Interpretation:

- This supports the recurrence-speed attack suggested by Lemma 11e.1x4m: ordinary landings would require anomalously delayed first prefix recurrences, while the tested mechanical samples have fast prefix recurrences.
- It does not prove that every lower irrational mechanical word has infinitely many below-threshold prefix recurrences.

Extended diagnostic run:

- `python3 explorations/explore75_mechanical_recurrence.py --length 512 --search-factor 128`
- All milestone recurrence ratios through length `512` remain below both obstruction thresholds.
- At `L=512`, the observed ratios are:
  `sqrt2-minus-1`: `985/512 ~= 1.924`;
  `sqrt3-minus-1`: `780/512 ~= 1.523`;
  `sqrt5-minus-2`: `305/512 ~= 0.596`.

`explorations/explore76_template_recurrence.py` checks the density-free recurrence cutoffs on canonical aperiodic templates.

Latest default run:

- `python3 explorations/explore76_template_recurrence.py`
- Cutoffs: return approximately `3.244`, reduced gap approximately `6.394`.
- Fibonacci prefix recurrence ratios through length `1024`: `0.812`, `0.656`, `0.859`, `0.695`, `0.910`, `0.736`, `0.964`.
- Thue-Morse ratios through length `1024`: all `1.500`.
- Period-doubling ratios through length `1024`: all `2.000`.
- Mechanical `sqrt(2)-1` ratios through length `1024`: `1.812`, `0.906`, `0.453`, `1.320`, `0.660`, `1.924`, `0.962`.
- Every checked milestone in every template is below both density-free cutoffs.

Interpretation:

- These templates are not plausible ordinary landing obstructions under the new recurrence criteria.
- This remains finite diagnostic evidence; a proof for each template family would require an infinite recurrence-ratio theorem.

`explorations/explore77_uniform_morphism_recurrence.py` enumerates binary `q`-uniform morphisms prolongable on `0` and checks prefix recurrence ratios.

Latest default run:

- `python3 explorations/explore77_uniform_morphism_recurrence.py`
- Parameters: `q=3`, `max_power=5`, `search_factor=16`.
- Total morphisms checked: `32`.
- All checked prefix recurrences below return cutoff: `30`.
- All checked prefix recurrences below reduced-gap cutoff: `31`.
- Missing recurrence in the finite search window: `1`.
- Worst ratio: `4.000` for `0->011`, `1->100`, at `L=3`, `tau=12`.

Interpretation:

- Unlike the binary `2`-uniform case, the density-free cutoff does not automatically remove every `3`-uniform morphism in finite diagnostics.
- The automatic-sequence route needs either sharper density information, longer structural recurrence arguments, or a case split for the exceptional morphisms.

`explorations/explore72_bounded_alphabet_beam.py` performs a heuristic long-prefix search for small `{0,1}` residues beyond the exhaustive frontier.

Latest run:

- `--max-length 120 --beam-width 2000 --report-every 20`
- The beam's best return and gap candidates remain sparse at the reported long lengths; for example, at length `120`, the best return candidate has residue bit length `356` with one `1`, and the best gap candidate has residue bit length `833` with one `1`.

Interpretation:

- This is not a proof, and beam pruning can miss dangerous branches.
- The fact that the beam keeps rediscovering fixed-count sparse candidates is consistent with the fixed-positive-label theorem: these are finite shadows, not possible infinite obstructions.

`explorations/explore64_terminal_ranks.py` verifies the terminal-rank formulation by sorting finite words using only the rounded normalized terminal coordinates `floor(U/E)` and `ceil(u/E)`.

Latest default run:

- Terminal depth bounds checked on the same low frontiers through `B=2^40-1`: `5,587` return states and `491` gap states
- Return terminal-rank worst cases: `B=2^24-1` has worst level `6`, terminal coordinate `262,143`, rank `2`; `B=2^32-1` has worst level `10`, terminal coordinate `391,188,479`, rank `1`; `B=2^36-1` and `B=2^40-1` have worst level `11`, terminal coordinate `8,589,934,591`, rank `3`
- Return weighted terminal-window and linear low-expansion cutoff bounds checked at `theta=3`: `128`, `658`, `1,479`, and `3,322` low states for `B=2^24-1`, `2^32-1`, `2^36-1`, and `2^40-1`
- Gap terminal-rank worst cases: `B=2^24-1` has worst level `3`, terminal coordinate `1,565,883`, rank `4`; `B=2^32-1`, `2^36-1`, and `2^40-1` have worst level `4`, terminal coordinate `32,679,099`, rank `2`
- Gap weighted terminal-window bounds checked at `theta=3`: `24`, `70`, `142`, and `255` low states for `B=2^24-1`, `2^32-1`, `2^36-1`, and `2^40-1`
- Gap distinct-terminal and multiplicity-adjusted low-expansion cutoff bounds checked on the same low frontiers
- Gap terminal multiplicity appears on the low frontiers: maximum checked multiplicity is `2`; at `B=2^36-1` and `B=2^40-1` the first maximum occurs at level `1`, terminal state `72,813,864,874`

Interpretation:

- The critical-rank obstruction is unchanged when expressed entirely in normalized terminal coordinates.
- Fixed terminal states have only logarithmically bounded prefix depth; the obstruction is breadth across terminal windows, not infinite depth at one terminal value.
- The return-side weighted zeta bound holds on the same low frontiers, but it is weaker than a rank count.
- This supports the stopping-time formulation: the missing estimate is a terminal-window rank bound, not a separate prefix-residue artifact.

`explorations/explore65_terminal_boundedness.py` verifies finite shadows of the terminal boundedness criteria on forced ordinary starts.

Latest default run:

- Return starts `n <= 50,000`, depth `<= 7`: `7,687` surviving prefixes checked; all rounded terminal coordinates were monotone with valid modulus-sized increments; `20` prefixes had modulus larger than the start and therefore stabilized to the original start
- Gap starts `a <= 500,000`, depth `<= 4`: `4,503` surviving prefixes checked; all rounded terminal coordinates were monotone with valid modulus-sized increments; `8` prefixes stabilized to the original start

Interpretation:

- For actual ordinary starts, the rounded terminal coordinate equals the least prefix residue at every checked prefix.
- Once the modulus exceeds the start, the rounded terminal coordinate is forced to equal the start, matching the terminal boundedness criterion.
- No zero increments occurred in the default finite forced-start scan before stabilization; the missing theorem is to rule out infinite zero-increment tails in all cases, not just in this bounded sample.

`explorations/explore66_terminal_zero_digits.py` verifies the terminal zero-increment uniqueness mechanism on low finite-height frontiers.

Latest default run:

- Return frontiers below `2^24-1`: `128` extensions across `8` levels checked; `10` zero terminal increments; every zero increment matched the unique forced auxiliary return step
- Gap frontiers below `2^24-1`: `24` extensions across `3` levels checked; `1` zero terminal increment; it matched the unique forced auxiliary gap step
- Finite local zero-increment realizability checked for all return and gap words of length `<= 4` with labels `<= 3`: `340` words in each system
- Bounded terminal zero-density sums checked for return and gap labels `<= 3`, length `<= 4`, matching the restricted rates

Interpretation:

- A zero terminal increment is not a freely chosen branch. It occurs exactly when the auxiliary terminal state itself takes the same next partial-map step.
- This computationally mirrors the terminal zero-increment tail uniqueness lemmas.
- Every checked finite terminal zero-increment word is locally realizable from the least prefix residue of that word, reinforcing that the obstruction cannot be killed by finite forbidden-pattern arguments.

`explorations/explore67_constant_branches.py` verifies the one-letter return and gap branch formulas.

Latest default run:

- Constant return branches verified for `r <= 8`, prefix length `<= 6`, with `162` sampled starts
- Constant gap branches verified for `k <= 8`, prefix length `<= 6`, with `162` sampled starts

Interpretation:

- Every one-letter finite alphabet has arbitrarily long finite shadows.
- The corresponding infinite code is explicit: negative rational for return, rational strictly between `0` and `1` for gap.
- The bounded-alphabet obstruction therefore starts at genuinely nonperiodic alphabets with at least two symbols.

`explorations/explore68_periodic_branches.py` verifies the exact periodic-shadow formulas for return and gap period words.

Latest default run:

- Periodic return branches verified for period `<= 4`, return lengths `r <= 4`, repeats `<= 4`, with `6,240` sampled starts
- Periodic gap branches verified for period `<= 4`, zero gaps `k <= 4`, repeats `<= 4`, with `6,240` sampled starts

Interpretation:

- For any checked period word `w`, the residue of `w^L` is exactly the rational fixed code modulo the period modulus to the `L`-th power.
- This computationally mirrors the periodic branch lemmas: periodic finite shadows exist at all depths, but their infinite 2-adic limits are rational non-obstructions.

Interpretation:

- Terminal escape is visible in the data, but the terminal state can be far above the original height bound while its normalized coordinate remains in the low window.
- The missing stopping-time theorem must control those normalized terminal windows, not merely prove that terminal states grow.

Overall binary-depth interpretation:

- This is the sharpest current reduction of the `T = 1` bounded-depth case.
- It is still not proof, because finite starts can realize arbitrarily long finite depth words by Lemma 9.
- The most concrete next theorem is a global return-code height bound: prove `mu_N -> infinity`.
- By the global-minimum criterion, that height bound is exactly equivalent to ruling out positive ordinary binary-depth return codes.

Important negative result: the stronger epoch bound `duration <= 3.0 log2(x)` is false already at `x = 27`.
