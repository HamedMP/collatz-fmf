<!-- Saved by the coordinator from the w4-E agent's final message (the agent's own write was refused). -->
# FULL REPORT (intended `w4-E/REPORT.md`)

Date: 2026-11-18.

Labels: PROVED (full proof here), VERIFIED (to the stated bound), CANDIDATE, REFUTED.
- "Given 2^71" means the statement uses the published verification that every n < 2^71 reaches 1.
- "Given NFB" means it uses Nikzad–Frinkle–Bagherzadeh, Hexagon 2611.00033, Cor. 3.20 (unrefereed, AI-assisted, not re-derived here): for a non-terminating orbit Σ_odd 1/x ≤ 9/50 and Π(1+1/(3x_i)) ≤ e^(3/50) = 1.0618.

Notation:
- T(x) = x/2 or (3x+1)/2; x_k = T^k(n); a_k = number of odd terms among x_0..x_{k−1}.
- W_k = a_k·log₂3 − k; ξ_k = x_k·2^k/(3^(a_k)·n) = Π_{i<k, x_i odd}(1+1/(3x_i)).
- θ₀ = log 2/log 3; η = H₂(θ₀) = 0.94995553.
- Hop letter of an odd x: (s, v) with s = v₂(x+1), parity block 1^s 0^(v−1). G01 = {(2,2),(3,2)}, i.e. blocks 110 and 1110.

## (a) Summary

1. Nothing here proves Collatz, H1, Lemma E, or any slice of Lemma E. The tools say only that an orbit cannot linger, and every scenario Lemma E must exclude grows fast (Obstruction O, b6).
2. Prior art: (H), (R), (S), (C) are not new and NFB has sharper constants. Everything below is a corollary. NFB's text contains no cycle-length, divergence, Baker or fractional-part consequence (grep).
3. Correction to the brief: "(S) gives x_k ≥ c·k^1.05 on a divergent orbit" does not follow. (S) is a counting statement; the proved forms are in Theorem G. A pointwise bound is equivalent to a glide-length bound (G5).
4. Correction to the brief, item 2: (H), (R), (S) are unproved for 5n+1, but their conclusions hold on every 5n+1 stretch tested. No consequence of the conclusions alone can exclude the observed 5n+1 behaviour.
5. Theorem Sh (PROVED, elementary): exact real shadow x_k = ν·3^(a_k)/2^k − δ_k. Divergence ⇔ the real series converges, and then its value is ≤ 0.386·n (≤ 0.0618·n given NFB).
6. Theorem G (PROVED from S and R): correct growth statements, including the parity-only sojourn law #{k : W_k ≤ t} ≤ 11.3·(1.386·n·2^t)^η.
7. Theorem C (PROVED given 2^71; sharper given NFB): for every nontrivial cycle 0 < p·ln2 − a·ln3 ≤ min(a/(3m), W_odd(m)/3). Hence {a·log₂3} ≥ 0.5291, or ≥ 0.9134 given NFB, with no assumption relating a to the minimum m. It adds to the classical bound only for a > 3.04·m (0.22·m given NFB).
8. Litmus: identities checked exactly on 3n+1, 3n−1, 5n+1, 3n+5, 3n+7, 3n+11, S_0, S_3, S_6 (169,560 instances). The failure points of "p = ⌈a·log₂3⌉" are located in b8.
9. Nine dead ends with reasons (d).
10. Best lead: Lemma LE (last-exit bound), section (e). Credence it is provable with present tools: 3%.

## (b) Statements and proofs

### b1. Theorem Sh (real shadow) — PROVED given 2^71; elementary; probably folklore

w2-delta dead end 5 has the H1 special case. Let n have a divergent trajectory with parity word w.

(i) ν := lim x_k·2^k/3^(a_k) exists and n < ν ≤ 1.386·n (≤ 1.0618·n given NFB).

(ii) Put y_k = ν·3^(a_k)/2^k and δ_k = y_k − x_k. Then y_{k+1} = y_k/2 or 3y_k/2 by the parity of x_k, and:
- δ_k = 2δ_{k+1} when x_k is even; δ_k = (2δ_{k+1}+1)/3 when x_k is odd.
- δ_k = Σ_{i≥k, x_i odd} (1/3)·2^(i−k)/3^(a_i−a_k), a convergent positive series depending only on σ^k w.
- δ_k = x_k·(Π_{i≥k, x_i odd}(1+1/(3x_i)) − 1). So δ_k ≥ 1/3 at odd terms, and δ_k/x_k ≤ exp(τ_k/3) − 1 → 0 with τ_k = Σ_{i≥k, odd} 1/x_i.

(iii) Let e_0 < e_1 < … be the positions of ones of u = σ^k w. The single series Z(u) = Σ_i 2^(e_i)/3^(i+1) has 2-adic sum −x_k (classical) and real sum δ_k. So Y(u) := Z_∞(u) − Z_2(u) = y_k obeys Y(σu) = Y(u)/2 or 3Y(u)/2; the shift is conjugated to pure multiplication.

(iv) Dichotomy: for a positive integer n the real series Z_∞(w(n)) converges ⇔ the trajectory of n is divergent. When it converges its sum is ≤ 0.386·n (≤ 0.0618·n given NFB).

Proof.
- x_k·2^k = 3^(a_k)·n·ξ_k is exact; ξ_k increases and is bounded by 1.386 because all terms are ≥ 2^71 (Theorem 70). This gives (i).
- Subtracting T from the y-recursion gives the δ-recursion. Iterating from k to K gives the exact finite identity
  x_k = M(k,K)·x_K − Σ_{k≤i<K, x_i odd} (1/3)·M(k,i), with M(k,i) = 2^(i−k)/3^(a_i−a_k).
- M(k,K)·x_K = x_k·ξ_K/ξ_k → x_k·ξ/ξ_k = y_k. So the series converges to δ_k = x_k(ξ/ξ_k − 1), which is the product form. τ_k → 0 because Σ1/x converges.
- (iii) is (ii) plus Bernstein's 2-adic formula.
- (iv): a non-divergent orbit is eventually periodic, and the i-th term equals n·ξ_{d_i}/(3x_{d_i}) ≥ n/(3·max x), which does not tend to 0. ∎

Checks:
- The finite identity, in the general form x_k = M·x_K − Σ(c_i/q)·M(k,i) for x → (qx+c(x))/2, holds on 169,560 exact instances over nine maps (`e1_shadow.py`).
- On 5n+1, n = 7, the infinite form agrees to 15 digits: ν/7 = 1.07369292…, δ_0 = 0.515850…, δ_40 = 2.069196… (`e2_5n1.py`).

Rate (`e3_cycles.py`): for a stretch with all terms ≥ 2^L0, 71 ≤ L0 ≤ 2400, W_odd(L0) ≤ 11.50·2^(−0.05004·L0). So at a future-minimum record x_k = m in that range, δ_k ≤ 4.7·m^0.94996. For all L0 the same holds with some constant by the Chernoff step of Theorem S.

Worth: a reformulation, not a reduction in difficulty. In this language Lemma E_div says the word is eventually in {110,1110}^ω, where δ at block starts lies in [19/11, 5] (fixed points of the two block maps: x+5 → (9/8)(x+5) and x+19/11 → (27/16)(x+19/11)).

### b2. Does the pair (real sum small, 2-adic sum = −n) force anything about the tail? — NO beyond Theorem H

- The real constraint is exactly Σ_odd 1/x_i < ∞ rewritten (term_i = n·ξ_{d_i}/(3x_{d_i})).
- The 2-adic constraint is Bernstein's bijection, valid for every 2-adic integer.
- The 2-adic reading fixes n mod 2^k from the first k letters. The real reading fixes the fractional part of ν·3^(a_k)/2^k from the future letters.
- They do not interact unless one controls fractional parts of ν·3^a/2^k, which is Mahler territory (D3).

### b3. Theorem G (growth of a divergent orbit, correct forms) — PROVED from Theorems S and R, given 2^71

Let n be divergent, C = 11.3, c₁ = 1.386 (1.0618 given NFB).

- **G1 (parity-only sojourn law).** For every real t: #{k : W_k ≤ t} ≤ C·(c₁·n·2^t)^η.
- **G2.** max_{j<K} x_j ≥ (K/C)^(1/η), with 1/η = 1.0527.
- **G3 (density one).** For every g(k) → ∞ the set {k : x_k ≤ (k/(C·g(k)))^(1/η)} has density zero.
- **G4.** For those k: a_k − θ₀k ≥ (θ₀/η)·log₂k − O_n(1) − θ₀·log₂g(k), with θ₀/η = 0.6642. For all k: W_k ≥ log₂(x_k/n) − log₂c₁ ≥ 71 − log₂(c₁n).
- **G5 (not implied).** No bound x_k ≥ c·k^β for all large k follows.

Proof.
- x_k = n·ξ_k·2^(W_k) with 1 ≤ ξ_k ≤ c₁, so W_k ≤ t implies x_k ≤ c₁n·2^t, and (S) counts such k. This is G1.
- G2 is (S) at X = max.
- G3: on the dyadic block [K/2^(j+1), K/2^j) the threshold is ≤ (K/(2^j·C·g_j))^(1/η), with g_j the minimum of g on the block. By (S) the block contributes ≤ K/(2^j·g_j). Summing over j ≤ J and adding K/2^J for the rest gives o(K).
- G4 is G3 and (R) in logarithms. ∎

Reason for G5:
- Let L(X) be the last time with x_k ≤ X. A pointwise bound is L(X) ≤ (X/c)^(1/β).
- (S) bounds how many times are spent below X, not when the last one occurs.
- Between consecutive future-minimum records r_i < r_{i+1} the orbit makes an excursion whose terms all exceed r_{i+1}. (S) allows it to be arbitrarily long if it is high (at most C·Y^η of its terms are ≤ Y).
- Bounding its length by a function of r_i is a glide-length bound; none is known unconditionally for any class of integers.
- The brief's "x_k ≥ c·k^1.05" and "3^(a_k)/2^k ≥ c·k^1.05/n" should be read as G1–G3.

Prior art: G1–G4 are immediate from García–Tal 1999 eq. (6) or Lagarias 1985 Thm F plus the residue bound; MO 513539 has W_k → ∞. Not new.

### b4. Bounded depths and "eventually G01"

- Not decided by the tools.
- Depths obey only the trivial bounds 2^s ≤ x+1 and 2^(v−1) ≤ (3/2)^s·(x+1).
- The harmonic sum does not weight depth: within one hop from x = 2^s·m − 1 the T-terms contribute Σ1/x ≤ 3/x + 1/F(x), with no 1/m term.
- Theorem 59 (linear complexity for bounded alphabets) is not improved.

### b5. Theorem C (cycles) — PROVED given 2^71; sharper given NFB

Let a nontrivial cycle have p terms, a odd terms, minimum m ∈ [2^L0, 2^(L0+1)) (so L0 ≥ 71), and Λ := p·ln2 − a·ln3.

- **C1 (exact).** Λ = Σ_{x odd in cycle} ln(1+1/(3x)).
- **C2.** 0 < Λ ≤ min( a/(3m), 1/(3m) + (1/6)·ln(1+2a/m), W_odd(L0)/3 ). Given NFB the third entry may be replaced by min(W_odd(L0)/3, 0.06).
- **C3 (fractional-part window).** {a·log₂3} ≥ 1 − W_odd(L0)/(3·ln2), with no hypothesis relating a and m.
- **C4 (with Rhin, quoted second-hand).** 3·p^(−13.3) ≤ Σ_odd 1/x ≤ W_odd(L0). This yields m ≤ C·p^266, weaker than the classical m ≤ a^14.3.

Values of W_odd and the resulting window (`e3_cycles.py`):

| floor on m | W_odd | {a·log₂3} ≥ |
|---|---|---|
| 2^71 | 0.97906 | 0.5291 |
| 2^100 | 0.3165 | 0.8478 |
| 2^200 | 0.00753 | 0.9964 |
| any non-terminating orbit, given NFB | 0.18 | 0.9134 |

For 71 ≤ L0 ≤ 2400, W_odd(L0) ≤ 11.50·2^(−0.05004·L0).

Proof.
- C1 is 2^p = 3^a·Π(1+1/(3x_i)) in logarithms.
- C2: the first entry uses 1/x ≤ 1/m; the second uses distinct odd integers ≥ m; the third is w2-delta Corollary D restricted to levels ≥ L0. The constants were recomputed with exact binomials and reproduce 1.35939 / 0.97906 at L0 = 71.
- C3: 0 < p − a·log₂3 = Λ/ln2 < 1, so p = ⌈a·log₂3⌉ and 1 − {a·log₂3} = Λ/ln2. ∎

Scope:
- The third entry of C2 beats the first two only when a > 3.04·m (given 2^71, so a > 7.2·10^21) or a > 0.2167·m (given NFB). For a < m, C3 is weaker than the classical p/a < log₂(3+1/m).
- Eliahou's p ≥ 114,208,327,604 is unchanged. There a ≈ 7·10^10 ≪ m, and all odd terms may lie in [m, 2m) as far as (S) knows (about 2^67.5 bad vectors at level 71).
- Hercher / Simons–de Weger is untouched.
- What it adds: a constraint on length that is uniform in a. Novelty is low; it is one line from NFB Cor. 3.20 or Theorem 70.
- "Exclusion of lengths not near a convergent denominator" is not obtained. A window of width 0.087 excludes 91% of all a but does not force a near a convergent; that needs width ≪ 1/a, which is the classical regime a ≪ m.

### b6. Obstruction O (why no slice of Lemma E_div comes out) — an argument, not a theorem about T

Lemma E_div must exclude divergent orbits in which, say, (4,2) (block 11110, factor 81/32) or (1,2) recurs with positive frequency while W_k keeps positive drift.

(H), (R), (S) are downward-closed in speed. If x_k ≥ A·λ^k with λ > 1 then, whatever the letters:
- Σ1/x ≤ 1/(A(1−1/λ));
- #{k : x_k ≤ X} ≤ log_λ(X/A) + 1;
- ξ converges.

So the conclusions carry no information about which letters occur.

Witness (VERIFIED to K = 20000 steps; `e2_5n1.py`, `e4_letters.py`), the 5n+1 orbit of 7:
- x_K ≈ 2^3107, a_K/K = 0.4975 (critical value 0.4307).
- Σ1/x_k = 0.4345, Π(1+1/(5x_i)) = 1.0737, minimum over k ≥ 10000 is 2^1554.
- Its 4971 hop letters are generic: 17.5% in G01 (random model 18.75%), the last letter examined is non-G01, and the most frequent letter is (1,2).

It satisfies the conclusions with a wide margin and is nothing like "eventually G01". So no E_div slice can be derived from the conclusions of (H), (R), (S) plus multiplier-blind hop algebra. A proof would have to use the multiplier 3 a second time, on the letters.

The three targets of mission item 3:
- "Upper density zero of depth ≥ 2 hops": not obtainable (above).
- "Non-G01 hops have summable reciprocal sizes with an explicit bound": true and trivial, because all hops do (Σ_odd 1/x ≤ 0.979, or 9/50 given NFB). It does not distinguish G01.
- "Each non-G01 hop costs a definite amount": false in size terms; the letter (4,2) gains more than any G01 letter.

### b7. Item 2: 5n+1 — VERIFIED to the stated bounds

| map | odd n < 30001, cap 2^300 | sup Σ1/x_k | sup log Π | sup #{x_k < 2^L}/2^(ηL) |
|---|---|---|---|---|
| 5n+1 | 14502 escapes | 2.6664 (n = 15) | 0.2706 | 0.8039 |
| 3n+1 | 0 | 2.9362 (n = 12555) | 0.5133 (n = 993) | 0.8039 |
| 3n−1 | 0 | 2.2666 | −0.0657 | 0.8039 |

The sojourn supremum is identical in all three rows and is attained at n = 1 or 3; I did not check further why it coincides.

- The conclusions hold on all tested 5n+1 stretches; only the proof fails for 5n+1. Whether the statements are true for 5n+1 is open (a random-walk heuristic says yes).
- The tools are litmus-immune for a weak reason: they assert non-lingering, and divergent-looking 5n+1 orbits do not linger.
- No clean "3x+1 divergent orbits grow at most / at least …" statement derivable from the tools is false for 5n+1. The lower bounds G1–G3 hold there with room to spare, and the tools give no upper bound on growth.
- The analogue of (C) holds on the known 5n+1 cycles: p = ⌈a·log₂5⌉ for the cycles through 1, 13, 17.

### b8. Mandatory controls (exact, `e1_shadow.py`)

| map / cycle | p | a | 2^p/q^a | p = ⌈a·log₂q⌉? | where the argument changes |
|---|---|---|---|---|---|
| 3n−1, {1} | 1 | 1 | 2/3 | no (floor) | c = −1: Π(1−1/(3x)) < 1, so Λ < 0 |
| 3n−1 through 5 | 3 | 2 | 8/9 | no (floor) | same |
| 3n−1 through 17 | 11 | 7 | 0.93644 | no (floor) | same |
| S_a fixed point 2^(a+1)−1 (a = 0, 3, 6) | 1 | 1 | 2/3 | no | c(x) = 1−2^(a+1) at that point; C1 needs c = +1 at every odd term, i.e. n < T(n) at n = 2^(a+1)−1 |
| 3n+5 through 1 | 3 | 1 | 8/3 | no | elements below d: Σ d/(3x) is not small; no analogue of the 2^71 floor |
| 3n+11 through 1 | 6 | 2 | 7.111 | no | same |
| 3n+11 through 13 | 14 | 8 | 2.497 | no | same |
| 3n+5 through 19, 23 | 5 | 3 | 1.185 | yes | |
| 3n+5 through 187, 347 | 27 | 17 | 1.039 | yes | |
| 3n+7 through 5 | 4 | 2 | 1.778 | yes | |
| 5n+1 through 1 | 5 | 2 | 1.28 | yes | identity is multiplier-blind; only the Σ1/x bound is unproved |
| 5n+1 through 13, 17 | 7 | 3 | 1.024 | yes | same |

- Nothing here claims "no cycles", so nothing must fail on 3n−1.
- Theorem C holds for 3n−1 with floor in place of ceiling. Its cycles give Λ' = a·ln3 − p·ln2 = 0.405, 0.118, 0.0657.
- 3 enters as 3 < 4 (Theorem 70, bad vectors rare). +1 gives the sign of Λ (ceiling versus floor) and is used at every odd term. Positivity gives x ≥ 2^L.

## (c) Scripts

Directory: `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/w4-E/`. Run each as `taskset -c 4 /home/matrix/home/projects/collatz/venv/bin/python <script>`; logs sit alongside.

| script | expected output |
|---|---|
| `e1_shadow.py` | nine lines "shadow identity: 18840 exact instances OK"; TOTAL 169560; the cycle table of b8 (exact rationals) |
| `e2_5n1.py` (about 1 min) | the three lines of b7; orbit of 7: bits 3107, Σ1/x = 0.43447…, ξ = 1.07369…; shadow check at k = 0..40 agreeing to 15 digits. Floats and 60-digit mpmath are exploration only |
| `e3_cycles.py` (2 s) | U_all and W_odd for L0 = 32..2000 (L0 = 71: 1.35939, 0.97906; frac_min 0.529169); max of W_odd·2^(0.05004·L0) over 71..2400 = 11.4926 at L0 = 71 |
| `e4_letters.py` | hops 4971; G01 fraction 0.1754; most common letter (1,2) |

## (d) Dead ends, with reasons

- **D1. Pointwise growth from (S).** Not implied; equivalent to a last-exit / glide bound (G5).
- **D2. Rigidity from the real and 2-adic sums of the (D) series.** The real sum is Theorem H restated, the 2-adic sum is Bernstein's bijection, and they do not interact (b2).
- **D3. Mahler / Flatto–Lagarias–Pollington on ν·3^(a_k)/2^k.** FLP needs a single ratio; here the exponent pair follows the word, and for G01 words the two block maps on δ overlap. Rationality of ν = P/Q gives no contradiction: N_k = P·3^(a_k) − Q·2^k·x_k is a positive integer with constant 2-adic valuation and nothing bounds it.
- **D4. Lemma E_div slices from size tools.** Obstruction O.
- **D5. A 5n+1-refuted growth statement.** None exists among consequences of the tools (b7).
- **D6. Improving Eliahou with (S).** Needs a ≥ m^0.95; the classical regime has a ≪ m.
- **D7. Cycle lengths near convergent denominators.** The window width is about m^(−0.05), far wider than 1/a unless a < m^0.05, which Baker already forbids (a ≥ m^0.07).
- **D8. Baker on near-returns of a divergent orbit.** |ln(x_l/x_k)| ≥ Δk^(−13.3) − τ_k/3 is non-trivial only for Δk < x_k^0.07. It is multiplier-blind and of cycle-bound type (ledger family 6).
- **D9. Control maps satisfying Theorem H's hypotheses with a divergent orbit.** By rigidity (Theorem 68), a perturbation c(x) keeping the exact Terras property must be of S_a / 3n+d type with shift ≥ modulus; divergent orbits there are as unknown as for T. So no rigorous no-go by control map exists at the level of hypotheses. Obstruction O works on conclusions only.

## (e) Best lead

**Lemma LE (last exit) — CANDIDATE.** There are β > 0 and C such that for every divergent n and every X ≥ n, the last time L(X) with x_k ≤ X satisfies L(X) ≤ C·X^(1/β).

- Equivalent form: for future-minimum records r_i at times t_i, Σ_{r_i ≤ X}(t_{i+1} − t_i) ≤ C·X^(1/β).
- It would turn G1–G3 into pointwise growth x_k ≥ c·k^β and a pointwise ones-density law.
- It is a glide-length bound for non-returning excursions. Lemma G2 (blocked in w3-g2) would give only the counting form again.
- It would still not touch Lemma E_div (Obstruction O). For Lemma E itself this toolset contributes nothing, and I have no lemma weaker than E_div that is reachable from it.

Secondary, cheap: make W_odd(L0) ≤ C·2^(−0.05004·L0) explicit for all L0, merge with NFB's 9/50, and state C3 as {a·log₂3} ≥ 1 − min(0.0866, 5.53·2^(−0.05004·L0)).

## (f) Brainstorm record

| # | idea | kill test | outcome |
|---|---|---|---|
| 1 | real vs 2-adic value of the (D) series forces tail structure | is the real constraint more than Σ1/x < ∞? | no; D2. Salvage: Theorem Sh |
| 2 | pointwise x_k ≥ c·k^1.05 from (S) | can a late term be small without violating (S)? | yes; D1, Theorem G |
| 3 | parity-only form of (S) via (R) | — | G1 proved |
| 4 | 3-specific statement false for 5n+1 orbit of 7 | compute the conclusions on 5n+1 | they hold; D5 |
| 5 | density zero of depth ≥ 2 hops | does a fast generic-letter orbit satisfy the tools? | yes; Obstruction O |
| 6 | weighted harmonic sum over non-G01 hops | is there a depth weight inside a hop? | no; b4 |
| 7 | cycle harmonic sum pinned by Λ, distribution via (S) | compare with a/(3m) | Theorem C; gain only for a > 0.22·m |
| 8 | exclude lengths away from convergents | window width versus 1/a | D7 |
| 9 | Baker on near-returns | multiplier-blind? | yes; D8 |
| 10 | Mahler/FLP on ν; irrationality of ν | single-ratio requirement | D3 |
| 11 | control map with H's hypotheses and a divergent orbit | rigidity | impossible; D9 |
| 12 | improve Eliahou with (S) | a versus m^0.95 | D6 |

## (g) Hostile self-review

- **Theorem Sh.** The limit uses only monotone bounded ξ, and the series has positive terms. The finite identity is exact on nine maps, including x-dependent c(x). The infinite form cannot be tested on 3x+1; it was tested on 5n+1, n = 7, which is only conjecturally divergent.
- **Theorem G.** G1 uses ξ_k ≥ 1, valid for 3n+1 only (for 3n−1 the constant moves to the other side). G3's dyadic sum was re-derived twice.
- **Theorem C.** The third entry of C2 rests on floating-point sums of exact binomial masses (same scheme and values as w2-delta s6). The "11.50·2^(−0.05004·L0)" claim covers 71 ≤ L0 ≤ 2400 only. C4 uses Rhin's exponent as quoted second-hand.
- **NFB constants** were not re-derived.
- **5n+1 table.** n < 30001 and cap 2^300 only; "escape" means exceeding the cap, not divergence.
- Nothing assumes the conclusion; nothing claims "no cycles" or "no divergent orbits".

## (h) Credences

| item | credence |
|---|---|
| Theorem Sh (i)–(iv), given Theorem 70 and 2^71 | 97% |
| Theorem G (G1–G4) | 96% |
| G5: pointwise growth is not a consequence of (S), (R), (H) | 90% |
| Theorem C (C1–C3), given 2^71 | 95% |
| NFB-dependent constants (0.9134, 1.0618) | 75% |
| Obstruction O fairly describes the tools' limits | 85% |
| Anything here is new in print | 20% |
| Any of this advances Lemma E | 2% |
| Lemma LE provable with present tools | 3% |