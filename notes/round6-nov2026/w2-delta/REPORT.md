<!-- Saved by the coordinator from the w2-delta agent's final message (the agent's own write was refused). -->
# FULL REPORT (intended `w2-delta/REPORT.md`)

Date: 2026-11-17. Labels: PROVED (full proof below), VERIFIED (to the stated bound, by the stated script), CANDIDATE, REFUTED.

Notation: T(x) = x/2 (x even), (3x+1)/2 (x odd); x_k = T^k(n); a_k = number of odd terms among x_0..x_{k−1}; the level of x is L(x) = ⌊log2 x⌋; θ0 = log 2/log 3 = 0.63093; η = H2(θ0) = 0.94995553 (binary entropy).

## (a) Summary

1. **Theorem H (PROVED, every n).** Along any stretch of a trajectory with pairwise distinct terms, Σ 1/x_k ≤ 27.2, independent of n and of the length.
2. **Theorem R (PROVED; constant uses my exhaustive computation below 2^32).** For every n and every k up to the first repetition, 1 ≤ T^k(n)·2^k/(3^{a_k}·n) ≤ 7.62. For every n reaching 1, Res(n) = 2^E/(3^O·n) ≤ 5.72.
3. This proves boundedness of the residue. Roosendaal's site treats it as conjectural (his Conjecture 2b, Res ≤ Res(993) = 1.2531, stays open). Luo (arXiv:2506.23070) assumes Res < 2 as a "Weak Residue Conjecture"; Res < 2 for all n is not proved here.
4. **Corollary D (PROVED given the published 2^71 verification).** For a divergent trajectory or nontrivial cycle the constant is 1.386. Consequences: 3^{a_k}/2^k → ∞ on any divergent trajectory, and a nontrivial cycle with a odd terms has exactly ⌈a·log2 3⌉ terms.
5. **Theorem S (PROVED).** Any such stretch has at most 11.3·X^η terms ≤ X, so k distinct terms force a term ≥ (k/11.3)^{1.0527}.
6. Mechanism: Terras' bijection between [2^L, 2^{L+1}) and parity vectors of length L, plus an injective charge of each good term to the term L steps later. It is not in the repo (grep) or the ledger; two web searches found no prior proof.
7. Litmus: the statements are also true for 3n−1 (and numerically consistent for 3n+d), so they cannot separate +1 from −1. The proof needs 3 < 4 and gives nothing for 5n+1.
8. η is the "1.93^n frontier" constant of ledger family 1, used here as a tool rather than a certificate.
9. Second and third executed items: the generation counts E_λ (VERIFIED to 2^30) and the exact identity of Proposition I, which turns the λ = 2 count into a statement about binary digits of Syracuse residues.
10. Sixteen ideas are logged in (f); seven dead ends have exact reasons in (d). Best lead: Lemma G2 in (e).

## (b) Statements and proofs

### Lemma 1 (Terras) — PROVED (standard)

For L ≥ 0 the first L parities of x, Tx, … depend only on x mod 2^L, and x mod 2^L ↦ parity vector is a bijection onto {0,1}^L. If the vector v has ones at positions d_0 < … < d_{a−1}, then T^L(x) = (3^a·x + r_v)/2^L with r_v = Σ_i 3^{a−1−i}·2^{d_i}, and r_v/2^L ≤ (3/2)^a − 1.

Proof of the last bound: d_i ≤ L − (a − i), so r_v/2^L ≤ Σ_{j=1}^{a} 3^{j−1}/2^j = (3/2)^a − 1. ∎ (131,070 exact instances, `s1`.)

Consequence: the 2^L integers of [2^L, 2^{L+1}) carry each vector of length L exactly once.

### Lemma 2 (descent) — PROVED

Let x ∈ [2^L, 2^{L+1}), let a be the number of odd terms among x, …, T^{L−1}x, and let s ≥ 0. If 3^a(1 + 2^{−a}) ≤ 2^{L−s}, then T^L(x) ≤ x/2^s.

Proof. T^L(x) ≤ 3^a·x/2^L + (3/2)^a − 1 < (3^a/2^L)·x + (3^a/2^a)·(x/2^L) = (3^a/2^L)(1 + 2^{−a})·x ≤ x/2^s, using x ≥ 2^L. ∎ (688,133 exact instances, `s7` R1.)

Definitions:
- A vector of length L is **bad** (for s) if 3^a(1 + 2^{−a}) > 2^{L−s}; an integer is bad if its level-L vector is bad.
- b_L = number of bad vectors; bo_L = number of bad vectors with first bit 1.
- Every bad vector has a > (L−s−1)·θ0, so b_L/2^L ≤ P(Bin(L,½) > (L−s−1)·θ0), which decays like 2^{−(1−η)L} because θ0 > 1/2. **This is the only place the multiplier 3 is used: 3 < 4.**
- Bad mass: β_all(L0) = Σ_{L≥L0} min(b_L/2^L, 2^{−L} + ln(1 + b_L/2^L)). It bounds Σ 1/x over distinct bad integers of level ≥ L0.
- β_odd(L0) is the same with bo_L and min(bo_L/2^L, 2^{−L} + ½·ln(1 + 2bo_L/2^L)).

### Lemma 3 (ancestors) — PROVED

Let x_0, …, x_{K−1} (K ≤ ∞) be pairwise distinct with x_{k+1} = T(x_k). For a good index k put t(k) = k + L(x_k). For fixed t let A_t = {good k : t(k) = t < K}. Then Σ_{k∈A_t} 1/x_k ≤ 2^{1−s}/x_t.

Proof. Each k ∈ A_t has x_t = T^L(x_k) ≤ x_k/2^s by Lemma 2. Distinct k ∈ A_t have distinct levels, since L = t − k. Take k' < k in A_t with levels L' > L.
- If L' ≥ L+2, then x_{k'} ≥ 2^{L+2} > 2x_k.
- If L' = L+1, then k' = k−1 and x_k = T(x_{k'}) has smaller level, which is impossible for an odd step, so x_{k'} = 2x_k.

Ordered by level the terms at least double, so the sum is ≤ 2/min ≤ 2/(2^s·x_t). ∎ (Largest observed ratio 1.9354 of the allowed 2, `s7` R2.)

### Theorem H (harmonic sums) — PROVED

For every pairwise distinct stretch x_0, …, x_{K−1} of a T-trajectory (K ≤ ∞) and every s ≥ 2:

Σ_{k<K} 1/x_k ≤ (β_all(0) + 1)/(1 − 2^{1−s}).

With s = 3 the right side is 27.163 (exact binomial sums to L = 1400, rigorous Chernoff tail < 10^{−19}; `s6`).

Proof. Fix Y and let W(Y) = Σ_{k<K, x_k≤Y} 1/x_k, a finite sum. Split the indices:
- Bad k: distinct bad integers, total ≤ β_all(0).
- Good k with k + L(x_k) ≥ K (overhang, only if K < ∞): 1/x_k ≤ 2^{−L} ≤ 2^{−(K−k)}, total ≤ 1.
- The other good k: t(k) < K and x_{t(k)} ≤ x_k/2^s ≤ Y, so by Lemma 3 their total is ≤ 2^{1−s}·W(Y).

Hence W(Y) ≤ β_all(0) + 1 + 2^{1−s}·W(Y). Let Y → ∞. ∎

Empirical supremum over all n < 2^32: 2.9367 including the term 1 (n = 993·2^j).

### Theorem R (residue bound) — PROVED; constant depends on `s5` (exhaustive; floating-point sums with a 10^{−9} margin)

Identity: T^k(n) = n·(3^{a_k}/2^k)·Π_{i<k, x_i odd}(1 + 1/(3x_i)).

Let B = 2^32. The run `s5` shows:
- every 2 ≤ n < B reaches 1;
- M_B = 0.2256541127 (attained at n = 993), where M_B is the maximum over n < B of Σ log(1 + 1/(3x)) over odd terms x < B of the trajectory of n, with 1 excluded;
- a trajectory has at most P_B = 495 terms below B.

For a distinct stretch, the terms below B lie on the trajectory of the first such term, so their odd log-sum is ≤ M_B (plus ln(4/3) if the stretch contains 1). For terms of level ≥ 32, repeat the proof of Theorem H restricted to those levels:
- overhang ≤ 33·2^{−32};
- a target t below B receives at most Σ_{L≥32} 2^{−L} = 2^{−31}, and there are at most P_B + 2 such targets;
- so ε = 33·2^{−32} + 497·2^{−31} = 2.4·10^{−7}.

This gives:
- U := Σ_{x_k≥B} 1/x_k ≤ min_s (β_all(32) + ε)/(1 − 2^{1−s}) = 6.3754;
- W_odd := Σ_{x_k≥B, odd} 1/x_k ≤ min_s (β_odd(32) + ε + 2^{1−s}·U) = 4.5507.

Therefore, for every n and every k ≤ K (K = number of distinct initial terms):

**1 ≤ T^k(n)·2^k/(3^{a_k}·n) ≤ (4/3)·exp(M_B + W_odd/3) = 7.62, and Res(n) ≤ exp(M_B + W_odd/3) = 5.72 for every n reaching 1.** ∎

Also Σ 1/x_k ≤ 9.32 for any distinct stretch. With the table only to 2^26 the same proof gives 8.54. The truth is probably 1.2531 (Roosendaal); the gap comes from the slowly decaying bad mass, roughly 29·P(bad at level L0).

### Corollary D (divergent trajectories, cycles) — PROVED given that all n < 2^71 reach 1 (Barina; verified by others)

If no term of the stretch is below 2^71 (true for every divergent trajectory and every nontrivial cycle), then Σ 1/x_k ≤ 1.3594, Σ_odd 1/x_k ≤ 0.9791 and Π(1 + 1/(3x_i)) ≤ 1.3860. With only my own 2^32 verification the constants are 6.375, 4.551 and 4.558.

- **(D1)** Divergent trajectory: ξ_k := x_k·2^k/(3^{a_k}·n) increases to ξ ∈ (1, 1.386]. Equivalently the real series Σ_i 2^{d_i}/3^{i+1} (d_i = time of the (i+1)-th odd step) converges to (ξ−1)·n ≤ 0.386n, while 2-adically the same series equals −n (Bernstein).
- **(D2)** Since x_k → ∞ on a non-periodic trajectory, 3^{a_k}/2^k ≥ x_k/(1.386n) → ∞. No divergent trajectory has 3^{a_k} ≤ 2^k for infinitely many k. The trivial bound Π ≤ C·k^{1/6} does not give this, because a late term can be small.
- **(D3)** Nontrivial cycle with p terms, a of them odd: 1 < 2^p/3^a < 1.386 < 2, so p = ⌈a·log2 3⌉, with no assumption relating a to the minimum.
- **(D4)** Unconditional form of the frontier track's Lemma G: x_k ≤ 7.62·n·3^{a_k}/2^k on every distinct stretch, without "non-descending". Its Theorem C should then hold for all non-periodic orbits with x_0 replaced by 7.62·x_0; I did not re-derive that line by line, so this is CANDIDATE.

### Theorem S (sojourn count) — PROVED

For a distinct stretch and every X ≥ 1: #{k < K : x_k ≤ X} ≤ 11.3·X^η.

Proof. Use the cruder criterion "bad iff 16·3^a > 2^L" (3^a·2^{s+1} ≤ 2^L ⇒ T^L(x) ≤ x/2^s with s = 3; 1,253,851 exact instances). Let n_L be the number of terms of level L and N_L = Σ_{l≤L} n_l.
- Bad terms at level L: ≤ b_L. Overhang: ≤ L.
- The remaining good terms map injectively (k ↦ k+L) to terms of level ≤ L−3.
- So N_L ≤ N_{L−1} + N_{L−3} + b_L + L.
- For L < 1200, (b_L + L)/2^{ηL} ≤ 1.608 (`s2`). For L ≥ 1200, Chernoff and the mean value theorem give b_L ≤ 2^{L·H2((L−4)θ0/L)} ≤ 2^{ηL}·2^{4θ0·log2(θ0/(1−θ0))} = 3.868·2^{ηL}.
- Induction with K0·(1 − 2^{−η} − 2^{−3η}) ≥ 3.87, i.e. K0 = 11.3, gives N_L ≤ 11.3·2^{ηL}. ∎

Corollaries: a cycle with ℓ terms has maximum ≥ (ℓ/11.3)^{1.0527}; an n needing σ steps to reach 1 has height ≥ (σ/11.3)^{1.0527}; in a divergent trajectory the j-th smallest term is ≥ (j/11.3)^{1.0527}. Observed supremum of #/X^η: 1.09.

### Proposition I (second-generation identity) — PROVED

Let v ∈ {0,1}^L have a ones and let y_v be the integer of [2^L, 2^{L+1}) with vector v. Then T^L(y_v) = 3^a + τ_v, where τ_v is the least non-negative residue of r_v·2^{−L} modulo 3^a.

Proof. T^L(y_v) = T^L(y_v − 2^L) + 3^a. Put τ_v := T^L(y_v − 2^L) ≥ 0; then 2^L·τ_v ≡ r_v (mod 3^a). Finally τ_v − 3^a = T^L(y_v − 2^{L+1}) < 0, because T maps negative integers to negative integers. ∎ (131,070 exact instances, `s8`.)

### Generation counts — VERIFIED to X = 2^30 (`s4`)

E_λ(X) = #{y ∈ [X,2X) : T^j(y) ≥ X/2 for all j ≤ λ·log2 X}.

| L = log2 X | λ=1 | λ=1.5 | λ=2 | λ=3 | λ=4 | λ=8 |
|---|---|---|---|---|---|---|
| 26 | 4,777,034 | 2,084,696 | 971,357 | 242,165 | 71,801 | 906 |
| 30 | 58,606,996 | 22,739,189 | 9,986,189 | 2,200,818 | 547,497 | 3,317 |
| local exponent (26→30) | 0.904 | 0.862 | 0.840 | 0.796 | 0.733 | 0.468 |

The heuristic exponent is 1 − 0.05λ. Lemma 1 proves E_1(X) ≤ C·X^η and nothing better for λ > 1.

## (c) Scripts

Directory: `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/w2-delta/`. Python is `/home/matrix/home/projects/collatz/venv/bin/python`; all runs under `taskset -c 5`.

| command | expected output |
|---|---|
| `python s1_exact_checks.py` | L1 bijection OK; L2 1,253,851 instances, 0 violations; L3 131,070 OK; L4 3,375 trajectories OK, max harmonic sum 2.936235 at n = 1986 |
| `python s2_constants.py` (older criterion; used for Theorem S) | eta = 0.94995553; `sup (b_L+L)/2^(eta L) = 1.6078 at L=2`; q = 5 bad fraction 0.9405, 0.9859, 0.99998 at L = 50, 200, 800 |
| `gcc -O2 -o s3_small s3_small.c -lm; ./s3_small 26` | all n < 2^26 reach 1; M_B = 0.225654112732 at n = 993 (Res 1.253142144); P_B = 339 |
| `gcc -O2 -o s4_generations s4_generations.c -lm; ./s4_generations 12 30` | the table above (`s4_generations.log`) |
| `gcc -O2 -o s5_small_stream s5_small_stream.c -lm; ./s5_small_stream 26 32` (about 20 min, 1.2 GB) | every n < 2^32 reaches 1; M_B = 0.225654112732 (n = 993); H_B = 1.936738538 (n = 993·2^22); P_B = 495 |
| `python s6_final_constants.py 32 0.225654112732 495 1.936738538` | tier-1 27.1629 (s = 3); `FINAL L0=32 … Res(n) <= 5.7119`; segment product 7.6158; levels ≥ 71: 1.35939, 0.97906, 1.38591 |
| `python s7_review_litmus.py` | R1 688,133 instances, 0 violations; R2 2,866 trajectories OK, max ancestor ratio 1.9354; R3 1.0938; litmus lines for 3n−1, 3n+d, 5n+1 |
| `python s8_syracuse_identity.py` | 131,070 exact instances OK, no "+3^a" case |

Every lemma test uses exact integers or rationals. Floats appear only in the constants: binomial masses are exact rationals converted with a 10^{−12} relative margin, and M_B is a double-precision sum of at most a few hundred terms (10^{−9} margin added).

## (d) Litmus and dead ends

**Litmus for Theorems H, R, S.**
- **5n+1.** Lemma 2 becomes 5^a(1 + 2^{−a}) ≤ 2^{L−s}. The threshold 1/log2 5 = 0.431 is below 1/2, so the bad fraction tends to 1 (0.923, 0.976, 0.9999 at L = 40, 160, 640) and β diverges. The argument proves nothing for any multiplier ≥ 4. Whether the statement itself holds for 5n+1 is unknown.
- **3n−1 (negative integers).** The remainder is ≤ 0, Lemma 2 holds verbatim, and the theorems are true with the same constants. Checked on 3,100 stretches; cycle sums are 1.0, 0.443, 0.259 for the cycles through 1, 5, 17. The theorems therefore cannot distinguish +1 from −1, and should not.
- **3n+d.** I expect it to hold with a d-dependent constant (terms below about 2^{s+1}·d² declared bad); this is a sketch only. Numerically the harmonic sums stay below 3.4 for d ∈ {5, 7, 11, 13, 17, 23, 499}, with up to 21 cycles met.
- So 3 enters as 3 < 4, +1 only through the bounded remainder, and positivity through x ≥ 2^L. This is a statement true for the cycle-bearing relatives, not a route to Collatz.

**Dead ends.**
1. **Lowering η by charging backwards (3-adic past).** A term reached from above has a generic past; only pasts coming from below can be charged, and those are already paid for.
2. **Two-prime counting of plateau points** (bad future mod 2^m, plateau past mod 3^a). With 2^m·3^a ≤ X the CRT count is X·2^{−0.05(m + a·log2 3)} ≥ X^η again; with larger moduli there is no independence in an interval of length X. Same information on both sides (ledger family 4).
3. **Res < 2 for all n (Luo's form).** Needs odd bad mass < 1.40 above the exhaustively computed range. The mass above 2^{L0} is about 29·P(bad at L0), which is below 1.40 only for L0 ≈ 63. Not reachable by this method.
4. **Short gaps in the set of integers reaching 1.** If an interval of length 2^{h_0} is refined through stages with h_{i+1} = a_i·log2 3 free bits, the total descent telescopes to ≤ h_0, so the method never beats gap ≤ N/2^71. A power saving needs entropy ≥ mean for the gap distribution, which holds with equality only at Geom(½). It is also multiplier-blind, so discarded.
5. **Mahler / Flatto–Lagarias–Pollington shadow of H1.** In w-coordinates w_k = ξ·G_k − ρ_k with ρ_k ∈ [0,1] and ρ = (8ρ'+1)/9 or 16ρ'/27. The two maps overlap (8/9 + 16/27 > 1) and cover [0,1], so the fractional parts are unconstrained.
6. **Unavoidable residue classes.** A single class mod 2^k is certifiably unavoidable only if the subshift avoiding its k-bit word has zero entropy (k ≤ 2: "every positive orbit meets 1 mod 4", trivial). "Every positive orbit meets 1 mod 8" means avoiding the factor 101, and {110,1110}^ω avoids 101, so it implies H1.
7. **Coefficient-stopping-time conjecture via Theorem R.** Gives Π − 1 ≤ C·n^{−0.05} uniformly in the stopping time, but with Rhin's bound only τ ≥ n^{0.0037}; the classical route gives n^{0.07} (ledger family 6).

## (e) Best lead

**Lemma G2 (second-generation large deviations) — CANDIDATE.** There are λ > 1, γ < 1, δ > 0 with

#{y ∈ [X,2X) : T^j(y) > X^γ for all j ≤ λ·log2 X} ≤ C·X^{η−δ}.

By Proposition I, for λ = 2 this says: among the roughly 2^{ηL} vectors v with a(v) ≥ θ0·L, the integers 3^{a(v)} + (r_v·2^{−L} mod 3^{a(v)}) have a bad level vector for at most a 2^{−δL} fraction of v. That is equidistribution of the low binary digits of Syracuse residues under the exponentially tilted measure, with exponential error. Tao's Fourier decay is polynomial and for the untilted measure, so this is open; but it is a density statement, far weaker than Collatz.

If true, Theorem S holds with η − δ (charge each good term to its first term below X^γ; the multiplicity ≤ λ·log2 X is absorbed because γ < 1), and the constants in Theorem R and Corollary D drop sharply. Data: local exponent 0.84 at λ = 2 against 0.90 at λ = 1.

Credence that G2 is true: 90%. Credence that it can be proved with present tools: 15%.

## (f) Brainstorm record

The barrier column says which litmus maps the idea must separate and where 3, +1 and positivity enter.

| # | idea | imported technique | kill test | barrier / outcome |
|---|---|---|---|---|
| 1 | harmonic sum along a trajectory by injective charging | Terras 1976; Lagarias 1985 x^{0.95} count | β diverges or contraction ≥ 1 | 3 < 4; true for 3n−1 as well. **Theorems H, R, S** |
| 2 | second-generation count E_λ | Tao's Syracuse variables | E_2 ≈ E_1 numerically | not killed (0.84 vs 0.90); **lead G2** |
| 3 | Syracuse-residue form of generation 2 | Terras remainder | exact identity fails | **Proposition I** |
| 4 | unavoidable residue sets | Monks 2006, Monks et al. 2013, SFT entropy | avoiding subshift has positive entropy | sign enters through −1, −5, −17; dead end 6 |
| 5 | short gaps among predecessors of 1 | branch counting, Krasikov–Lagarias | telescoping of free bits | multiplier-blind; dead end 4 |
| 6 | Mahler/FLP real shadow of H1 | Flatto–Lagarias–Pollington 1995 | IFS overlap | positivity only; dead end 5 |
| 7 | 2-adic future × 3-adic past transversality | Shmerkin, Wu 2019 | is the count an archimedean statement? | no, it equals E_2; dead end 2 |
| 8 | nonstandard counter-model | compactness, Presburger | does iteration become internal? | ω−1 never descends in Presburger+T; 3 and +1 never enter; discarded |
| 9 | base-6 automatic structure (x/2 = 3x/6) | Cobham, regular model checking | forward-invariant regular sets | mod 3^k invariants are valuation classes only (2 is a primitive root); reasoning only |
| 10 | automaton group of ×3, +1 on Z_2 | Bartholdi–Šunić, BS(1,3) | any orbit-level statement? | amenable, says nothing on N; discarded |
| 11 | primitive cycles of 3x+d for every d | Lagarias 1990 | trapping interval for coprime orbits | gcd(x,d) invariant but no trapping region; not executed |
| 12 | orbit of 2^k − 1 as a 2-adic family in k | continuity of 3^k in k | information left after log2 k steps | exhausted; equivalent to generic n |
| 13 | low-complexity parity sequences | Morse–Hedlund | prefix squares | p(m) ≥ 1.7095·(m − log2 n) for divergent orbits is immediate; otherwise ledger family 7 |
| 14 | weak 3x+1 semigroup with word-length bounds | Applegate–Lagarias 2006 | 5x+1 analogue | 5 lies in the 5x+1 semigroup (hand check); multiplier-blind; discarded |
| 15 | density of forward-invariant sets on which T is injective | Dirichlet series | better than 5X/9? | superseded by idea 1 |
| 16 | coefficient stopping time via idea 1 | Rhin | compare with n^{0.07} | dead end 7 |

## (g) Hostile self-review

- The integral comparison for Σ 1/(M+i) was the wrong way round in a first draft (ln(1 + b/M) is a lower bound). Fixed by adding 2^{−L} per level; the effect is < 10^{−7} at L0 ≥ 26 and +1.5 on the tier-1 constant.
- The contraction constant was first proved as 3·2^{−s}; Lemma 3 gives 2·2^{−s}, and the exact checks assert the stronger form.
- Nothing assumes Collatz. Theorem H uses no computation; Theorem R uses my exhaustive run below 2^32; Corollary D uses the published 2^71 bound and is labelled so (its 2^32 fallback is 4.56).
- Adversarial inputs: 2^k − 1 (k < 90), 2^k + 1, (4^k − 1)/3, delay record holders up to 75,128,138,247, and random 100-bit integers. All bookkeeping inequalities hold in exact rationals.
- Novelty risk: the result is a short step from Terras and Lagarias and may be folklore. I found Roosendaal's page (conjectural) and Luo 2025 (assumes it), and no proof.

## (h) Confidence

| item | credence |
|---|---|
| Lemmas 1–3 | 99% |
| Theorem H (27.2) | 97% |
| Theorem R (5.72 / 7.62), including the floating-point evaluation | 93% |
| Corollary D (1.386), given 2^71 | 93% |
| Theorem S | 95% |
| Proposition I | 99% |
| Generation counts as finite data | 97% |
| Lemma G2 true | 90% |
| Boundedness of the residue is new in print | 65% |
| Any of this proves Collatz, H1 or Lemma E | 0% |

Sources: [Roosendaal, More on 3x+1 Residues](http://www.ericr.nl/wondrous/residues.html); [Luo, Iteration Steps of 3x+1 Problem, arXiv:2506.23070](https://arxiv.org/abs/2506.23070).