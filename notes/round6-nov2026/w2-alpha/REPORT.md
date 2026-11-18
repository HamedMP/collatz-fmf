<!-- Saved by the coordinator from the w2-alpha agent's final message (the agent's own write was refused). -->
# FULL REPORT — w2-alpha: the ×2 ×3 rigidity / ternary-digit side of H1

## (a) Summary

1. H1 (all-w form) is exactly `E ∩ Z_{>0} = ∅`, where `E ⊂ Z_2` is the self-similar Cantor set of the 2-adic IFS `{z → (8z−1)/9, z → 16z/27}`. `dim_H E = s = 0.287761` (x³+x⁴=1, s = −log₂x). Its 3-adic mirror F has dimension `t = 0.25596` (y²+y³=1, t = −log₃y). PROVED (standard).
2. θ-form (PROVED, classical in substance): every orbit is `w_N = θ·3^{P_N}/2^{Q_N} − τ_N` with `τ_N ∈ [0,1]`, `θ = w + γ_R(U)`. The integer points with θ = 0 are exactly 0 and −1. Positivity enters H1 only as "θ ≥ 1 versus θ = 0".
3. Hull vacuity (PROVED): the smallest closed ×2-invariant subset of R/Z containing the binary-digit images of E is the whole circle; same for F and ×3. Shmerkin–Wu applied to any closed invariant hull gives the bound 1, i.e. nothing.
4. Reflection/dilation no-go (PROVED): `E_{3n−1} = −E`, `E_{3n+d} = d·E`. Every quantity the ×2×3 literature uses is identical for E, −E and 115·E, while `−E ∋ 1` and `−115·E ∋ 27, 16`.
5. Conditional (implication PROVED): an L^∞ "Frostman" bound for the digit-reversal projection of E implies `#{w ≤ X with infinite itinerary} ≤ C_ε X^ε`. That is dimension zero, never finiteness. No published theorem covers the projection statement.
6. Numerics (VERIFIED to Q' = 64): the projection behaves like a random set; survivors of depth Q extend by m more bits with frequency close to `2^{−(1−s)m}`.
7. Fourier route (identities PROVED, obstruction stated): low-frequency decay of μ_E needs the top ternary digits of `2^{−j} mod 3^J` with j ≍ J, the Erdős regime.
8. Lagarias' theorems on the Erdős problem are the exact analogue of the repo's Theorems 48/57 (cylinder counting). His Conjecture A (exceptional set of dimension 0) is still open, and he notes even it would not decide λ = 1.
9. Litmus: every statement here holds verbatim for 5n+1 and 3n−1. None distinguishes the systems, which is the content of items 3–4.
10. Best lead: Lemma FP-0 in section (e).

## (b) Statements

Notation. `a(w) = (9w+1)/8` on `w ≡ 7 (8)`; `b(w) = 27w/16` on `16 | w`. Inverse branches `f_a(z) = (8z−1)/9`, `f_b(z) = 16z/27`. For a word with A letters a and B letters b: `P = 2A+3B`, `Q = 3A+4B`; `P_j, Q_j` are the partial values after j letters. Controls: 5n+1 (`(25w+1)/8`, `125w/16`) and 3n−1 (`(9w−1)/8` on `w ≡ 1 (8)`, `27w/16`).

### Theorem 1 (formulation, exact dimensions) — PROVED

`f_a(Z_2) = 7+8Z_2` and `f_b(Z_2) = 16Z_2` are disjoint balls, and `f_a, f_b` are exact 2-adic similarities of ratios 1/8 and 1/16 (9 and 27 are units). Let E be the attractor, i.e. the set of 2-adic integers with an infinite a/b itinerary. Then:

- `dim_H E = dim_B E = s` with `2^{−3s}+2^{−4s} = 1`, `s = 0.287761…`.
- `N_k := #(E mod 2^k)` satisfies `N_k = N_{k−3}+N_{k−4}` for k ≥ 5, and `N_k ≤ 1.64·2^{sk}` (checked for k ≤ 60).
- Symmetrically a, b are 3-adic similarities of ratios 1/9, 1/27 with disjoint images `8+9Z_3`, `27Z_3`. Their attractor `F ⊂ Z_3` has dimension t with `3^{−2t}+3^{−3t} = 1`, `t = 0.25596…`.
- H1 (all positive w) ⇔ `E ∩ Z_{>0} = ∅`. H1 proper ⇔ `E ∩ Z_{>0} ∩ (10 mod 11) = ∅`.

Proof: Moran's theorem for a strictly separated ultrametric IFS; the recursion is the partition of level-k cylinders by first letter. ∎

### Theorem 2 (θ-form; where +1 and positivity enter) — PROVED

For an infinite word U put `γ_N = Σ_{j ≤ N, letter j = a} 2^{Q_{j−1}}/3^{P_j}`. The series converges in R to `γ_R(U) ∈ [0,1]` and in Z_2 to `γ_2(U)`.

- (i) If z ∈ E has itinerary U then `z = −γ_2(U)` and, exactly, `z_N·2^{Q_N} = 3^{P_N}(z+γ_N)`. Hence `z_N = θ·3^{P_N}/2^{Q_N} − τ_N`, with `θ := z+γ_R(U)` and `τ_N = γ_R(σ^N U) ∈ [0,1]`.
- (ii) For rational z ∈ E: either θ = 0, and then z ∈ [−1,0] and U is eventually periodic; or θ ≠ 0 and |z_N| → ∞.
- (iii) `E ∩ Z ∩ {θ = 0} = {0, −1}` (words b^ω, a^ω). So H1 for both signs reads "γ_2(U) ∈ Z ⇒ γ_2(U) = γ_R(U)".
- (iv) `E_{3n−1} = −E`, and for odd d, `E_{3n+d} = d·E` (system `(9w+d)/8`, `27w/16`). Example: `−27/115 ∈ E` with itinerary (ab)^ω, i.e. the system 3n−115 has the cycle 27 → 16 → 27.

Proof.
- (i) One a-step adds `2^{Q_{j−1}}/3^{P_j}` to the normalised value `z_j 2^{Q_j}/3^{P_j}`; a b-step leaves it unchanged; sum. `2^{Q_j}/3^{P_j} ≤ (8/9)^j` gives real convergence and `γ_R ≤ (1/9)Σ(8/9)^j = 1`. 2-adically the terms tend to 0, and `3^{P_N}(z+γ_N) ≡ 0 mod 2^{Q_N}` gives `z = −γ_2`. The tail is the same series for the shifted word.
- (ii) If θ ≠ 0 then `|z_N| ≥ |θ|(9/8)^N − 1`. If θ = 0 then `z_N = −τ_N ∈ [−1,0]` with bounded denominator, a finite set on which the map is deterministic.
- (iii) An integer in [−1,0].
- (iv) `−a(−w) = (9w−1)/8`; `a_d(dz) = d·a(z)`, and the congruence conditions on dz and z coincide for odd d. ∎

Where the constants enter:
- **+1** only through the fixed point of a being the integer −1 (for 5n+1 it is −1/17; for 3n+d it is −d).
- **Positivity** only through θ ≥ 1 versus θ = 0.
- **3** only through the numerical values of s and t.

Nothing else in this report uses them.

### Theorem 3 (hull vacuity) — PROVED

Let `A := closure{(z mod 2^k)/2^k : z ∈ E, k ≥ 1} ⊂ [0,1]`, the smallest closed T_2-invariant set containing all top-down binary readings of E-cylinders. Let `B := closure{(v mod 3^k)/3^k : v ∈ F, k ≥ 1}` (T_3-invariant). Then `A = B = [0,1]`. The same holds for 5n+1 and 3n−1.

Proof.
- `−1 ∈ E`, so `e_k := (16/27)^k·(−1) ∈ E` (b^k maps it to −1).
- For any m, `e_k mod 2^{4k+m} = 16^k·(−27^{−k} mod 2^m)`, so `(e_k mod 2^{4k+m})/2^{4k+m} = (−27^{−k} mod 2^m)/2^m`.
- The group generated by 27 = 3³ in `(Z/2^m)^×` equals that of 3, namely `{1,3 mod 8}`. So these numbers run over all `v/2^m` with `v ≡ 5,7 (mod 8)`, which is dense as m → ∞.
- For B use `(27/16)^k(−1) ∈ F`: `⟨16⟩ = {1 mod 3}` in `(Z/3^m)^×` since 2 is a primitive root, giving all `v/3^m` with `v ≡ 2 (mod 3)`.
- For 5n+1 use the fixed point −1/17 and `⟨125⟩ = {1 mod 4}`; for 3n−1 use +1. ∎

Consequence. Shmerkin's and Wu's theorem (arXiv 1609.07802 and 1609.08053, abstracts re-read) needs closed A, B ⊂ [0,1] invariant under ×p, ×q with `log p/log q ∉ Q`, and then gives `dim((uA+v) ∩ B) ≤ max(0, dim A + dim B − 1)`. The only closed invariant sets attached to E and F by reading digits are full, so the bound is ≤ 1.

This is the same defect Lagarias records for the Erdős problem (math/0512006 §1.2): the exceptional set "is not known to be a closed set, so that results on Hausdorff dimension on closed sets invariant under commuting semigroup actions cannot be directly applied". The dense points used in the proof are the non-integer rationals `−(16/27)^k`: the hull is filled by the binary digits of `3^{−3k}`.

### Theorem 4 (reflection / dilation no-go) — PROVED

Let Φ be any assignment of data to compact subsets (or measures) of Z_2 that is invariant under `z → −z` and `z → dz` (d odd). Then Φ(E) cannot imply `E ∩ Z_{>0} = ∅`.

Invariant data include:
- Hausdorff, box and L^q dimensions, and the multiset of cylinder counts;
- the hull of Theorem 3;
- `|μ̂|` up to the frequency permutations `ξ → −ξ`, `ξ → dξ`;
- under reflection, the whole family of bucket counts of Theorem 6 (bucket σ of −E is bucket −σ−1 of E).

Proof. `Φ(E) = Φ(−E) = Φ(−115·E)`, but `1 ∈ −E` and `16, 27 ∈ −115·E` (Theorem 2(iv); checked exactly in `a4_rational.py`). ∎

This is the precise form of the "dimension 0 versus empty" gap. The positive integers are a countable dense subset of Z_2, invisible to dimension; and −E and −115E, which do contain positive integers, are isometric copies of E.

### Proposition 5 (mirror count) — identity PROVED, numerics VERIFIED

For a word u let `r_u ∈ [0,2^{Q_u})` be the least residue of its 2-adic cylinder and `w'_u = u(r_u)`. Then `0 ≤ w'_u < 3^{P_u}`, `w'_u` is the least residue of the 3-adic F-cylinder of the reversed word, and `r_u = ⌊2^{Q_u} w'_u/3^{P_u}⌋`. There were 0 failures over all 206,897 words at level 60 (5n+1 was checked at level 48, also 0 failures). Consequently

`N(Q,m) := #{0 ≤ w < 2^Q : itinerary ≥ Q+m bits} = #{u at level Q, r_u < 2^Q : w'_u ∈ E mod 2^m}`.

Heuristic (independence of the 3-adic address and the residue mod 2^m): `N(Q,m) ≈ N(Q,0)·2^{−(1−s)m}`. Measured at Q = 60 on 95,265 seeds:

| m | measured fraction | heuristic |
|---|---|---|
| 4 | 0.1379 | 0.1388 |
| 8 | 0.0186 | 0.0193 |
| 12 | 0.00231 | 0.00267 |
| 16 | 0.00026 | 0.00037 |

The controls 5n+1 and 3n−1 give the same picture at Q = 48.

Remark on the repo's Theorem 57(T1): its lower bound `B^{α−o(1)}` is attained at word lengths ≤ log₂B, where every cylinder has a representative. It does not rule out a power saving for `N(Q, εQ)`; that saving is Lemma FP-0.

### Theorem 6 (what a Shmerkin-type theorem would give) — CONDITIONAL, implication PROVED

**Hypothesis FP (Frostman bound for the digit-reversal projection).** For every ε > 0 there is C_ε such that for all `1 ≤ m ≤ Q'` and all σ,

`#{c ∈ E mod 2^{Q'} : ⌊c/2^{Q'−m}⌋ = σ} ≤ C_ε·2^{εQ'}·max(1, 2^{sQ'−m})`.

This is the analogue of the L^∞ end of Shmerkin's L^q theorem. The measure is μ_E pushed to R/Z by `z → {z/2^{Q'}}`; the intersecting set is the interval of integers below `2^{Q'−m}`; and `max(1, 2^{sQ'−m})` is `max(0, dim A + dim B − 1)` expressed in counts.

**Implication.** FP ⇒ `#{0 < w ≤ X : w ∈ E} ≤ C'_ε X^ε` for every ε. Proof: X = 2^Q; take `Q' = ⌈Q/(1−s)⌉`, `m = Q'−Q ≥ sQ'`, σ = 0. ∎

FP cannot give finiteness. Bucket σ = 0 always contains the point 0, bucket `2^m−1` contains −1, and for −E (3n−1) bucket 0 contains 0 and 1. FP holds or fails simultaneously for E and −E.

Why no published theorem gives FP. Shmerkin needs measures of the form `*_n S_{λ^n}Δ(T^n x)` over a uniquely ergodic base. Here `{z/2^{Q'}} = −Σ_{a-steps j} y(Q'−Q_{j−1}, P_j) mod 1`, where `y(k,P) := (3^{−P} mod 2^k)/2^k = (−2^{−k} mod 3^P)/3^P + 1/(2^k 3^P)`. Every term is full-size and carries all the digits of `2^{−k} mod 3^P`, so there is no geometric scale separation and no convolution structure. The identity for y is one line (`a = 3^{−P} mod 2^k ⇒ a·3^P = 1 + c·2^k`, `c ≡ −2^{−k} mod 3^P`); the rest of this paragraph is derived by hand and not machine-checked.

Numerical status of FP — VERIFIED to Q' = 64 only (459,459 points):

| m | mean bucket | max bucket |
|---|---|---|
| 14 | 28.0 | 52 |
| 18 | 1.75 | 10 |
| 22 | 0.11 | 4 |
| ≥ 38 | — | 1 |

Bucket 0 is {0} from m = 22 on. The correlation exponent D₂ is 0.996 at m = 14. The controls at Q' = 56 behave identically; 3n−1 has bucket 0 = {0, 1} for all large m, as it must.

### Proposition 7 (Fourier side) — identities PROVED, conclusion is an OBSTRUCTION

Let μ be the natural measure on E (weights x³, x⁴). For ξ ∈ Q_2/Z_2:

- `μ̂(ξ) = x³χ(−ξ/9)μ̂(8ξ/9) + x⁴μ̂(16ξ/27)`.
- Grouping ab with ba, the coefficient of `μ̂((8/9)(16/27)ξ)` is `x⁷[χ(−ξ/9) + χ(−16ξ/243)]`, of modulus `2x⁷|cos(π{11ξ/243})|`. The 11 is the repo's invariant w ≡ −1 mod 11 (b is the identity mod 11).
- For ξ = h/2^n, after a prefix u the running frequency is exactly `ξ_u = k_u/3^{P_u} + h/(2^{n−Q_u}3^{P_u})`, with `k_u ≡ −h·2^{−(n−Q_u)} mod 3^{P_u}`.

So cancellation at step u is lost exactly when the leading ternary digits of `h·2^{−j} mod 3^J` (j = n−Q_u, J = P_u+5) agree with those of some p/11. That is a period-5 digit window along a staircase with j ≍ J.

Obstruction. This is the Erdős–Lagarias regime: digits of 2^j at height comparable to j. To my knowledge the available equidistribution results for `2^j mod 3^J` (Korobov-type short sums) need j super-polynomial in J. So Kaufman / Erdős–Kahane decay for μ_E at integer-scale frequencies is out of reach of current tools. Numerically the decay is square-root: `|μ̂(h/2^n)| ≈ 2^{−sn/2}` for h = 1, 3, 5, 11 and n ≤ 60.

### Proposition 8 (rational points, average over d) — PROVED, trivial strength

`#{r ∈ E ∩ Q : height ≤ H} ≪ H^{2s} = H^{0.5756}`, because distinct rationals of height ≤ H are distinct mod 2^k once 2^k > 2H². Hence

`#{(w,d) : 1 ≤ w,d ≤ X, d odd, w has an infinite itinerary in 3n+d} ≤ C·X`.

On average over d ≤ X there are O(1) seeds below X, against X^{0.2878} for an individual d. A scan found no positive rational of height ≤ 600 in E (max life 21 bits), which improves the constant by the factor `600^{−0.4244}`. This is cylinder counting (LEDGER family 3) applied to rationals; it says nothing about d = 1.

### Answers to the brief's questions

- **What does Shmerkin–Wu give?** Nothing unconditional (Theorem 3). The conditional analogue FP would give seeds = `X^{o(1)}`, a dimension-zero statement, not finiteness.
- **Can an intersection theorem beat 0.2878?** Only through FP or FP-0; neither follows from a published theorem.
  - Lagarias' proved results (`N_λ(X) ≤ 25X^{0.9725}`; `Ñ_λ(X) ≤ 2X^{log₃2}`; `dim E(Z_3) ≤ 1/2`) are cylinder-counting bounds of the same kind as the repo's Theorem 48.
  - Abram–Lagarias path sets need digit-automatic sets. The follower sets of E are the affine copies `3^{−P_u}(E − w'_u)`, an unbounded family; I did not prove these pairwise distinct.
- **What separates dimension 0 from empty?** Theorem 4, plus the rank-one obstruction: H1 uses a single path `3^{P_N}/2^{Q_N}` inside the rank-2 ×2×3 action, which is a Mahler Z-number-type problem. Furstenberg, Rudolph–Johnson and Bourgain–Lindenstrauss–Michel–Venkatesh rigidity needs both directions free; a single hyperbolic direction has invariant Cantor sets of every dimension (E × F is one). The Mahler and BLMV statements are from memory, not re-read.

## (c) Scripts

All exact integer arithmetic except the float sums in a3. Run from `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/w2-alpha/` with `taskset -c 0 /home/matrix/home/projects/collatz/venv/bin/python <script> <args>`.

- `a1_core.py <3n+1|5n+1|3n-1> 60` — enumerates E mod 2^Q, checks the mirror identity, prints the extension table and the infinite-life integers. Expected: "failures: 0"; `[0]` (or `[0, 1]` for 3n−1). The mirror check is skipped for 3n−1, where the map is the reflected one.
- `a2_projection.py <system> 64` — bucket table of Theorem 6.
- `a3_fourier.py 3n+1` — Fourier table and the two group-orbit facts used in Theorem 3. Expected: six lines "True".
- `a4_rational.py 600` — θ-identity on 46,035 orbit steps; the 3n−115 cycle; the rational scan; the cylinder recursion. Expected: no positive infinite-life rational; 6 negative ones with q < 130, none outside [−1,0]; max `N_k/2^{sk}` = 1.638.
- `lit/` — arXiv metadata and the two Lagarias PDFs, with pages 1–4 as text.

Literature caveat: the arXiv API abstract of 1308.3133 says the exceptional set "has been shown" to have dimension 0, but the PDF (v1) says "conjectured" and states the proved bound ≤ 1/2. I rely on the PDF. Dimitrov–Howe was checked from its abstract only. Not checked: Saye's computational bound, the Abram–Bolshakov–Lagarias refinements, Hochman–Shmerkin, exact BLMV statements.

## (d) Sub-ideas, kill tests, outcomes

| # | Idea | Kill test | Outcome |
|---|---|---|---|
| 1 | Shmerkin–Wu on the ×2/×3 hulls of E, F | compute the hulls | DEAD: hulls are [0,1] (Thm 3) |
| 2 | Lagarias exceptional-set dimension | is the exceptional set smaller than E? | DEAD: it is E; reproduces 0.2878 (LEDGER 3) |
| 3 | Abram–Lagarias path-set automata | is E digit-automatic? | DEAD (not proved): follower sets `3^{−P}(E−w')` are unbounded |
| 4 | Kaufman / Erdős–Kahane Fourier decay | derive the frequency recursion | OBSTRUCTION: needs digits of `2^{−j} mod 3^J`, j ≍ J |
| 5 | Shmerkin L^q for the digit-reversal projection | is it dynamically driven self-similar? | NOT APPLICABLE; conditional Thm 6; numerics support FP |
| 6 | Furstenberg / BLMV rigidity on the array `2^{−j} mod 3^J` | does the orbit use both directions? | DEAD: rank-one path (Mahler regime) |
| 7 | Rational points of E, averaging over 3n+d | count rationals by height | PROVED but trivial (Prop 8) |
| 8 | Flatto–Lagarias–Pollington range of fractional parts | compute them | DEAD: they are `τ_N = γ_R(σ^N U)`, arbitrary in [0,1] |
| 9 | Dimitrov–Howe congruence sieving | is there a modulus with an invariant? | DEAD by LEDGER 1 and 10 (only mod 11) |
| 10 | Real attractor [−1,0] and positivity | classify θ | gives Thm 2(ii)–(iii) only (periodic itineraries, already known) |

Hostile self-review.
- Theorem 3 uses only −1 ∈ E and the group generated by 27 mod 2^m; machine-checked for m ≤ 14, and by hand in general.
- Theorem 2 was checked with exact fractions on every orbit step of every level-40 cylinder representative.
- The weakest point is Theorem 6's claim that no published theorem implies FP. That is my reading of Shmerkin's hypotheses, not a proof that no reformulation exists.
- Nothing here is equivalent to H1, and nothing here is progress on H1 itself.

## (e) Best lead

**Lemma FP-0 (open).** There are δ > 0 and C such that for all Q,

`#{0 ≤ w < 2^Q : w has an a/b itinerary of at least 2Q bits} ≤ C·2^{(s−δ)Q}`.

Equivalently (Prop. 5): among level-Q words u with `r_u < 2^Q`, at most `C·2^{(s−δ)Q}` have mirror residue `w'_u ∈ E mod 2^Q`.

- It implies `#{w ≤ X : w ∈ E} ≤ C·X^{s−δ}`, beating 0.2878.
- It is strictly weaker than H1, and true or false simultaneously for 3n+1 and 3n−1 (and presumably 5n+1).
- Numerically it holds with a saving close to (1−s) = 0.712 per extra bit.

The natural attack is equidistribution of the least residues of F-cylinders modulo 2^m with m ≍ Q; Prop. 7 identifies the arithmetic input this needs. A realistic first target is m = c·√Q, a saving of `exp(−c√log X)`. A Riesz-product argument would suffice there if the ternary digit blocks of `w'_u` could be decoupled; I could not decouple them.

**Credences**

| Claim | Credence |
|---|---|
| Theorems 1–4 correct | 97% |
| Prop. 5 and 7 identities correct | 95% |
| Theorem 6 implication correct | 97% |
| FP true | 80% |
| FP-0 true | 90% |
| FP-0 provable with present techniques | 5% |
| This family yields H1 | < 1% |