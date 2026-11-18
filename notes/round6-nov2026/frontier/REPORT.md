<!-- Saved by the coordinator from the frontier agent's final message (the agent's own write was refused). Status: agent-proved, referee pending. -->
# FULL REPORT (intended `frontier/REPORT.md`)

## (a) Summary

1. Coordinates verified exactly (`f1`). With w = 33n+32 the return block r is w = 16^r z → (9·27^r z+1)/8. Equivalently the two-rule map is **b: w → 27w/16 (16 | w)** and **a: w → (9w+1)/8 (w ≡ 7 mod 8)**. x = 108n+103 = (36w−19)/11 has Collatz parity word (1110)^r 110 over the block. H1 says no w ≡ 32 (mod 33) has an infinite itinerary in {a,b}^ω.
2. Theorem A (PROVED): the repo's barrier in single-coordinate form, valid for every positive w and every return alphabet.
3. Theorem B (PROVED, new): two-block exclusion with integer certificate 3^9 < 2^16.
4. Corollaries B1–B3 (PROVED): all binary pure-morphic words under any block coding, binary S-adic hierarchies, standard episturmian words. This settles plan.md's open lead "extend Theorem G beyond uniform morphisms" for two letters.
5. Theorem C (PROVED, new): the same for weakly non-descending Collatz orbits at block density < 0.8412; Corollary C1 for primitive binary morphic parity sequences.
6. Proposition D (PROVED, negative): no modular invariant beyond 11.
7. Obstruction O (VERIFIED to a bound): a 4-letter non-uniform morphic return word on which the whole same-factor method gives only w₀ > 2^62.
8. Litmus passed in the sense of BRIEF rule 2 (section d).
9. Dead ends in section (e).
10. Best lead: Lemma T (section g).

## (b) Statements and proofs

### 0. What the repo already excludes from H1

| class of return word (r_j) | where |
|---|---|
| eventually periodic; all-ones tail (Lemma P) | paper §6 remark; Thm 55 |
| {0,1} words with liminf p(m)/m < 3.1493 (fixed-defect, sparse-label, p(m) ≤ m, balanced/Sturmian) | Thm 47 |
| {0,1} words with liminf p/m < 3.2439; uniform-density floor 7.5691 | Thm 60 |
| the q = 9 boundary word | Thm 46 |
| binary fixed points of q-uniform morphisms, all q; codings of uniform fixed points on ≤ 3 letters | Thm 51 |
| spike words of geometric ratio > log₂3 (hop-word form) | Thm 62 |
| (STATE candidate A, unverified, ineffective: spikes of every ratio > 1) | round 6 |

Not covered before this track: non-uniform morphic words of superlinear complexity; return alphabets other than {0,1} (apart from periodic and spike words); S-adic hierarchies.

### 1. Setup

S is the partial map on positive integers with letter **a** if w ≡ 7 (mod 8), w' = (9w+1)/8, and letter **b** if 16 | w, w' = 27w/16. For v ∈ {a,b}*:
- B(v) = 3|v|_a + 4|v|_b (bits),
- e(v) = 2|v|_a + 3|v|_b,
- G(v) = e(v)·log₂3 − B(v) ≥ 0.

Put T0 := 4/(3log₂3 − 4) = 5.2988. Since 3/log₂(9/8) = 17.65 and 4/log₂(27/16) = T0:

**(1.1)** B(v) ≥ T0·G(v) for every word v.

Return letter r is the block b^r a. Everything below holds for all positive w₀, a strictly larger system than H1's w₀ ≡ 32 (mod 33).

### Theorem A (repetition barrier) — PROVED

Let the itinerary of w₀ ≥ 1 begin with P, let u occur in P at letter positions i < i' with i'+|u| ≤ |P|, and let p = P[0,i'). Then 2^B(u) ≤ w_{i'} − w_i and

2^B(u) < (w₀+1)·2^G(p), equivalently 2^(B(u)+B(p)) < (w₀+1)·3^e(p).

Proof.
- (i) For a, the map w mod 2^(m+3) ↔ w' mod 2^m is a bijection on the gate class. For b, the same holds with 2^(m+4). By induction the integers whose formal itinerary starts with u form one class mod 2^B(u), so w_i ≡ w_{i'}.
- (ii) w' > w for w ≥ 1 under both letters, so w_{i'} − w_i ≥ 2^B(u).
- (iii) w'+1 = (9/8)(w+1) under a and w'+1 ≤ (27/16)(w+1) under b, so w_{i'}+1 ≤ (w₀+1)·2^G(p). ∎

This is the repo's "factor-recurrence height barrier" (Thm 46); the additions are the single-coordinate form and that no bound on return letters is needed. In Bugeaud–Kim repetition-function language: the shortest prefix containing two occurrences of a factor of bit length β has bit length > 6.2988β − T0·log₂(w₀+1).

**Corollary A1 (PROVED).** The {a,b}-factor complexity of an itinerary of w₀ satisfies p(n) > (3n − log₂(w₀+1))/(3log₂3 − 4), so liminf p(n)/n ≥ 3.9741 for every return alphabet. (Pigeonhole on positions 0..p(n).)

### Lemma L (weighted two-block lemma) — PROVED

Let y ∈ {c,d}^ω start with c, with weights l_c, l_d > 0 and l additive. Then there are positions i < i' and a factor u occurring at both with l(y[0,i')) ≤ 3·l(u) and l(u) ≥ l_c.

Proof. If y starts with cc, take u = c at 0,1. Otherwise y = c d^k …; if k = ∞ take u = d^n at 1,2 with n large. Otherwise y = c d^k c^j …; put ρ = l_d/l_c.
- kρ ≤ 2: u = c at 0 and k+1; ratio 1+kρ ≤ 3.
- kρ > 2, k ≥ 2: u = d^(k−1) at 1 and 2; ratio (1+1/ρ)/(k−1) < (1+k/2)/(k−1) ≤ 2; l(u) = (k−1)ρ·l_c > (2(k−1)/k)·l_c ≥ l_c.
- k = 1, ρ > 2, and (j ≥ 2 with ρ ≤ 3j−5, or j = ∞): u = c^(j−1) at 2 and 3; ratio (2+ρ)/(j−1) ≤ 3.
- k = 1, ρ > 2, otherwise (j finite, next letter d): u = d at 1 and j+2; ratio 1+(1+j)/ρ ≤ 3 because ρ ≥ (1+j)/2 (j = 1,2: ρ > 2; j ≥ 3: ρ > 3j−5 ≥ (1+j)/2); l(u) = l_d > 2l_c. ∎

Remark (proved by the same case split with thresholds √3): the constant 3 can be replaced by 1+√3 = 2.732 with l(u) ≥ (√3/2)·l_c. The exact rational grid maximum of the four-candidate minimum is 2.725.

### Theorem B (two-block exclusion) — PROVED

Let X, Y ∈ {a,b}^+ be arbitrary and suppose the itinerary of the positive integer w₀ lies in {X,Y}^ω with first block X. Then

w₀+1 > 2^(κ·B(X)), κ = 1 − 3/T0 = (16 − 9log₂3)/4 = 0.43383,

i.e. (w₀+1)⁴·3^(9B(X)) > 2^(16B(X)).

Finite form: the conclusion already holds when the itinerary begins with the block word cc or c d^k c^j d.

Proof. Apply Lemma L with l = B∘σ. Theorem A and (1.1) give 2^B(u) < (w₀+1)·2^G(p) ≤ (w₀+1)·2^(B(p)/T0) ≤ (w₀+1)·2^(3B(u)/T0), and B(u) ≥ B(X). ∎

**Corollary B1 (binary pure morphic).** Let φ be a non-erasing morphism on {c,d} with |φ^t(c)| → ∞, y = φ(y) starting with c, and σ any map {c,d} → {a,b}^+. Then σ(y) is not the itinerary of a positive integer (take X_t = σφ^t(c), Y_t = σφ^t(d)). No uniformity, primitivity or aperiodicity is assumed. σ = (a, ba) is the {0,1} return alphabet; σ = (b^r a, b^s a) is any pair of return letters.

**Corollary B2 (hierarchies).** If x ∈ {X_t,Y_t}^ω with first block X_t for infinitely many t and B(X_t) → ∞, then x is not the itinerary of a positive integer. This includes binary S-adic words and characteristic Sturmian words in any coding.

**Corollary B3 (standard episturmian / Arnoux–Rauzy, any alphabet, any block coding σ).** By Justin's formula the palindromic prefixes satisfy u_{n+1} = t·u_n with t a prefix of u_n whenever the new directive letter has occurred before. So u_n recurs at |t| with B(σt) ≤ B(σu_n), and Theorem A gives w₀+1 > 2^((1−1/T0)·B(σu_n)) for infinitely many n. The formula was machine-checked on 3,324 instances.

**Example beyond every earlier repo exclusion.** Take φ: c → cddc, d → dd, σ = (a, ba). Maximal d-runs have lengths 2^(s+1), flanked by φ^s(c) of length (s+1)·2^s with runs ≤ 2^s. Factors of length m whose unique longest full run is d^(2^(s+1)) at offset o are distinct for distinct (s,o). This gives p(m) ≥ (m/2)(log₂log₂m − 3), so p(m)/m → ∞ (sketch; Pansiot's classification gives Θ(m log log m)). The word is therefore not automatic and violates no complexity threshold, yet B1 excludes it.

Caveat: for this individual word the old prefix-recurrence criterion would also work if applied by hand. What is new is the uniform class statement and the weight-independent lemma.

### Theorem C (non-descending Collatz orbits) — PROVED

T(x) = x/2 for x even, (3x+1)/2 for x odd; π is the parity sequence of x₀; k_n is the number of odd steps among the first n.

**Lemma G.** If x_j ≥ x₀ for all j ≤ n, then x_n ≤ x₀·(3^k_n/2^n)·(1+1/(3x₀))^k_n.

Proof. Write x_n = (3^k_n/2^n)(x₀+E_n) with E_n = Σ_{i<k_n} 2^(j_i)/3^(i+1), where j_i is the time of the (i+1)-th odd step. Non-descent at j_i gives 2^(j_i)/3^i ≤ (x₀+E^(i))/x₀, so x₀+E^(i+1) ≤ (x₀+E^(i))(1+1/(3x₀)). ∎ (158,565 exact instances.)

**Theorem C.** Let x₀ ≥ 2 with x_j ≥ x₀ for all j, and π ∈ {X,Y}^ω with X, Y ∈ {0,1}^+, first block X, #1(X) ≤ θ'|X|, #1(Y) ≤ θ'|Y|, and g := θ'log₂3 − 1 ∈ [0, 1/3). Then either the orbit is eventually periodic, or

|X|·(1 − 3g − 3θ'·log₂(1+1/(3x₀))) < log₂x₀.

Hence a weakly non-descending, not eventually periodic orbit cannot have a parity sequence that is two-block decomposable at unbounded scales with densities ≤ θ' < (4/3)/log₂3 = 0.84124. With the 1+√3 form of Lemma L the threshold is 0.86187.

Proof. Lemma L with weights |X|, |Y| gives block-aligned occurrences of u at bit positions i < i' ≤ 3|u| with |u| ≥ |X|. Equal parity factors force x_i ≡ x_{i'} (mod 2^|u|) (Terras). If x_i = x_{i'} the orbit is periodic. Otherwise 2^|u| < max(x_i, x_{i'}). Block-aligned prefixes have 3^k/2^m ≤ 2^(g·i') and k ≤ θ'i', so Lemma G gives |u| < log₂x₀ + (g + θ'·log₂(1+1/(3x₀)))·3|u|. ∎

**Corollary C0.** For a divergent orbit, the bound holds at every floor time m (x_n ≥ x_m for all n ≥ m), with x₀ := x_m.

**Corollary C1** (uses two standard facts: uniform letter frequencies of primitive substitutions, and transcendence of log₃2). Let y be a fixed point of a primitive morphism on {c,d}, σ: {c,d} → {0,1}^+, π = σ(y) with ones-frequency θ < 0.84124. If π is the parity sequence of a positive integer, the orbit is eventually periodic, hence π is periodic.

Proof. θ is algebraic, so θ ≠ log₃2.
- If θ < log₃2, then 3^k/2^n decays geometrically on every factor, x_n is bounded and the orbit is eventually periodic.
- If θ > log₃2, then E_∞ < ∞ and x_n ≤ (x₀+E_∞)·3^k_n/2^n. The proof of Theorem C runs at levels σφ^t(c), σφ^t(d) with g = θlog₂3 − 1 + o(1) and no non-descent hypothesis. ∎

Theorem B is the sharp-constant, hypothesis-free special case: the H1 sublanguage has blocks 110 and 1110 (densities 2/3, 3/4) and is letterwise expanding.

### Proposition D (modular invariants) — PROVED

Let gcd(m,6) = 1, α(w) = (9w+1)/8, β(w) = 27w/16 on Z/m. Both are bijections, and the 2-adic gates are independent of w mod m by CRT. Then αβ(w) − βα(w) = 1/8 − 27/128 = −11/128, so ⟨α,β⟩ contains translation by 11·unit.
- If 11 ∤ m the group is transitive.
- If 11 | m the orbits are exactly {w ≡ −1 mod 11} and its complement (β ≡ id mod 11; α has the fixed point −1 and a 10-cycle).

Checked for all m < 2000: 61 moduli have two orbits, all multiples of 11, of sizes m/11 and 10m/11. So no modular invariant beyond w ≡ −1 (mod 11), which every H1 state already satisfies.

### Obstruction O — VERIFIED to a bound, not proved

For an itinerary x let V(N) = max over repetitions (u at i < i' < N) of B(u) − G(x[0,i')). Theorem A says log₂(w₀+1) > V(N) and nothing more. Complexity thresholds, uniform-morphic exclusions, prefix recurrence and Theorem B are all consequences of V(N) → ∞. V was computed by suffix array and longest-previous-factor (`f6`, checked against brute force).

| word | N ({a,b} letters) | V |
|---|---|---|
| Fibonacci, blocks a, ba | 1000 / 4000 / 16000 | 4179 / 17737 / 75167 |
| c→cddc, d→dd, blocks a, ba | 1000 / 4000 / 16000 / 51199 | 1690 / 7361 / 35664 / 77550 |
| Thue–Morse, blocks a, ba | 1000 / 4000 / 16000 | 1070 / 4279 / 17117 |
| **φ4** = (0312113, 201, 000303302, 301110), blocks b^(4+k)a | 1000 … 242,218 | **62.14, constant** (attained at i' = 186) |
| φ4, blocks b^(20+k)a | 1000 … 275,435 | 213.18, constant (i' = 67) |

φ4 is primitive. Its weighted early-repetition constant ι (the infimum of l(p)/l(u) over repetitions, l the left Perron vector) is about 6.39 on a 6000-letter prefix. That is above the ratios B/G of its blocks (5.68–5.96 for b^4a…b^7a).

Statement: the return word r_j = 4+y_j (y = φ4^ω(0)), over the alphabet {4,5,6,7}, is not excluded by any repetition-type argument through 40,000 return letters. The method gives only w₀ > 2^62, weaker than the 2^69 already implied by Barina's 2^71. Whether its 2-adic seed is a positive integer ≡ 32 mod 33 is a concrete H1 instance the repo's methods cannot decide. Boundedness of V for all N is expected but unproved; it needs a desubstitution argument.

## (c) Scripts

All are in `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/frontier/`. Run with `taskset -c 5 /home/matrix/home/projects/collatz/venv/bin/python <script>`.

| command | expected output |
|---|---|
| `f1_verify_formulas.py` | `OK blocks checked: 2800 random gate-consistency checks: 20000, admissible: 2635` |
| `f2_barrier_twoblock.py` (about 1 min) | T-A: 450098 instances, 0 violations. T-B (3,+1): 142228 cases, 0 violations, min log₂(w₀+1)/B(X) = 1.6548. (5,+1): 0 violations on these small cases, min 1.1547. (3,−1): w = 1 fixed point, 1210 violations. (3,+5): 0 |
| `f3_lemma_and_search.py 1 3 6000 6` | lemma grid max 2.72500 at (1, 2, 69/40); random 3-letter top ι = 4.000 |
| `f4_hillclimb.py 4 5 18000 9` | `K=4 best screen 6.4284 refined(N=6000) 6.3906 … phi=['0312113','201','000303302','301110']` |
| `f4_hillclimb.py 3 21 24000 12` | `K=3 best … 4.4850 … phi=['0210011','11012222','220020221210']` |
| `f5_general_collatz.py` | G1: 158565 instances, 0 violations. G2 (3x+1): (14788, 0, None). G2 (5x+1): (28652, 0, None). G3: 3324 instances, 0 violations |
| `f6_obstruction_lpf.py 40000` (about 4 min) | the Obstruction O table; saved in `f6_obstruction.log` |
| `f7_mod_invariants.py` | only multiples of 11 have two orbits (61 moduli < 2000) |

Logs: `f3_K3_len10.log` and `f3_K4_len8.log` (about 30k random morphisms each; max ι 4.05 and 4.42), `f4_hillclimb.log`, `f4_hillclimb_K3.log`, `f6_obstruction.log`. Floats are used only in the ι searches and for log₂3 inside V; every theorem test is exact integer arithmetic.

Two process notes: `f5` was run once on core 4 rather than core 5 (a few seconds), and the K=5 hill-climb was stopped before finishing, so there is no K=5 result.

## (d) Litmus (BRIEF rule 2)

- **5n+1.** Rules b: 125w/16, a: (25w+1)/8. Theorem A holds verbatim with G₅. Theorem B needs T > 3, and T_b(a) = 4/(3log₂a − 4) > 3 iff a < 2^(16/9) = 3.43. For a = 5, T = 1.349, so only repetitions of ratio < 1.349 survive (unboundedly long prefix squares). The argument does not prove the 5n+1 analogue. The constant 3 enters as 3^9 < 2^16 (5^9 > 2^16).
- **3n−1 / negative integers.** a: w → (9w−1)/8 has the positive fixed point w = 1 with itinerary a^ω. The conclusion of B is false there (1210 exact violations). The failing step is strict growth w' > w, which for +1 holds for all w ≥ 1 because the fixed point is −1. That is where +1 and positivity enter.
- **3n+d, d > 0.** B holds with w₀+d. There is no conflict, because every block of the sublanguage expands, so its positive orbits are never cycles.
- **Theorem C.** It holds for (ax+1)/2 with window θ' < (4/3)/log₂a (0.574 for a = 5; 28,652 exact cases) and for negative x₀. It only ever concludes "eventually periodic", so the cycles of 5n+1 (13-cycle, parity word 1110000, the x_i = x_{i'} branch), −5, −17 and 3n+d are consistent with it. It is multiplier-covariant and does not separate 3 from 5 beyond the window width.

## (e) Dead ends

1. **Seed gap principle (target c).** Two seeds sharing β itinerary bits differ by ≥ 2^β. Counting gives ≤ C·X^0.2878 seeds below X, which is Theorem 48, proved exponent-optimal by Theorem 57. Theorem A adds nothing below β = log₂X, so "one seed per [X, X^c]" is unreachable this way.
2. **3-adic side of a repetition.** States after the two occurrences agree mod 3^e(u), but 3^e(u) = 2^(B(u)+G(u)) and the later state is larger by 2^G(u). The inequality is identical (Mirror Equivalence, Thm 61), for any 3-adic/2-adic split of u.
3. **Multiple occurrences.** s occurrences give spread (s−1)·2^B(u): a log₂s gain only.
4. **Modular invariants (target d).** Proposition D.
5. **Explicit 2^71 numbers (target b).** H1 seeds have w₀ > 11·2^71/36. Theorems A–C constrain only factors with B(u) > log₂w₀. The only output is "no two-block structure with B(X) > 2.305·log₂(w₀+1)".
6. **More than two blocks.** Lemma L fails for three weighted letters in general words, and the method fails outright for 4-letter morphic words (Obstruction O). Bounded-skew K-block words stay covered by pigeonhole when K·R < T0 (R = max/min block bit length), which is Theorem 51's mechanism.
7. **Parity density above 0.862.** Lemma L's universal constant is at least 1+1/√2 = 1.7071 (morphism 0→01, 1→100) and at most 1+√3. The barrier ratio at density 1 is 1/(log₂3−1) = 1.7095, so no uniform statement over all densities follows.
8. **Literature.** One web search found no prior statement of Theorem C or C1. Novelty outside the repo is unknown; Bugeaud–Kim's repetition function is the natural home.

## (f) Brainstorm record

| # | idea | kill test | outcome |
|---|---|---|---|
| 1 | weighted two-block lemma | grid search for (k,j,ρ) with all candidates > T0 | survived → Theorem B |
| 2 | repetition-function form, unbounded alphabets | 450k exact barrier instances | Theorem A, Corollary A1 |
| 3 | lift to all non-descending orbits | exact growth-lemma test | Theorem C |
| 4 | K ≥ 3 blocks | search for ι > T0 | K=4 killed (6.39); K=3 open (4.485) |
| 5 | seed gap principle | compare with α_R count | dead |
| 6 | 3-adic post-state congruence | algebra | dead |
| 7 | many occurrences | algebra | dead |
| 8 | mod-p invariants | commutator and orbit computation | Proposition D, dead |
| 9 | Subspace theorem on approximants | STATE.md dead end | not repeated |
| 10 | constraints from 2^71 | arithmetic | corollary only |

## (g) Single best lead

**Lemma T (ternary early repetition) — CANDIDATE.** For every primitive morphism φ on three letters with fixed point y and left Perron vector l, there are a factor u and positions i < i' with l(y[0,i')) < T0·l(u), T0 = 4/(3log₂3 − 4) = 5.2988.

If true, then by Theorem A (exactly as in B1) no positive integer has an itinerary that is a block coding of a ternary pure-morphic word. That would cover every three-letter return alphabet.

Evidence: about 30k random morphisms plus four hill-climbs give sup ι = 4.485 (0→0210011, 1→11012222, 2→220020221210). The value creeps up with image length. The 4-letter analogue is false (6.39).

A proof would start from y = c·s·φ(s)·φ²(s)… and apply Lemma L, with an offset, to the two-letter subsystem on the letters of s.

Credence that Lemma T is true: 40%. The same question with T0 replaced by 1/(θlog₂3 − 1) decides Corollary C1 for three letters.

## (h) Confidence

| item | credence |
|---|---|
| Theorem A | 97% |
| Lemma L | 97% |
| Theorem B | 96% |
| Corollaries B1–B3 | 93% |
| Lemma G | 97% |
| Theorem C | 92% |
| Corollary C1 (asymptotic bookkeeping is terse) | 85% |
| Proposition D | 97% |
| Obstruction O as a finite statement | 95% |
| Obstruction O extended to all N | 75% |

B, C and D are new relative to proof.md §23 and plan.md 301–709 as I read them; earlier round notes were not read exhaustively. None of this bears on H1 for generic high-complexity words.

Sources consulted in the single literature search (no relevant prior result found): [Words and Transcendence](https://arxiv.org/pdf/0908.4034), [The reflection complexity of sequences over finite alphabets](https://arxiv.org/html/2406.09302v4).