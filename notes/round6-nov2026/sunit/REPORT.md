<!-- Saved by the coordinator from the sunit agent's final message (the agent's own write was refused). Status: agent-proved, referee pending. -->
# FULL REPORT — Track `sunit` (round 6, 2026-11-17)

## (a) Summary

1. Evertse 1984, Corollary 1, read from the source (p. 227; copy at `sunit/lit/page04.png`): the form quoted from memory in STATE.md §A is exactly what the paper proves. It is ineffective.
2. The hop identity and the return-block identity were re-derived and machine-checked in exact integers on about 1.45·10^5 orbits (2^n−1, prescribed spike and growth words, negative integers, 5n+1, 3n+d, an+d).
3. PROVED (Theorem A): for fixed k ≥ 1 and δ > 0, only finitely many odd x_0 have H_k + s_k > (1+δ)·log2(x_0+1). Equivalently H_k + s_k ≤ (1+δ)L_0 + C(k,δ) with C ineffective.
4. PROVED: C(k,δ) ≥ 2k − δ (witness x_0 = 1; also x_0 = 3). No uniform-in-k version exists.
5. PROVED (Theorem D, Corollary C): the k-window depth ledger; no hop word with liminf s_{j+1}/s_j > 1 is realised by a positive integer. The spike corollary of §A is valid.
6. PROVED (Theorem E): S_j, H_j, log x_j are e^{o(j)} in the hop count j.
7. PROVED (Theorem F): the return-map version.
8. Litmus: everything transfers verbatim to an+d. It is a size constraint; 3 enters only as the number log2(3/2).
9. Data to 10^10 is consistent with limsup = 1. The excess T_k − L_0 grows roughly like (k+1)·log2 L_0.
10. Prior art: the identity is known (Chang 2026, who reports Subspace as blocked). Theorem A was not found anywhere; it is a routine application.

## (b) Statements

**Notation** (repo definitions; θ = log2 3). For odd x ≥ 1 write y = x+1 = 2^s·m with m odd, s ≥ 1. The hop is x' = (3^s m − 1)/2^(v−1), where v−1 = v_2(3^s m − 1) ≥ 1 and v = v_2(FMF) ≥ 2. The letter is (s,v), and h = s+v−1 ≥ s+1. Along an orbit: y_i = 2^(s_i) m_i, S_j = Σ_{i<j} s_i, H_j = Σ_{i<j} h_i, σ_i = S_k − S_{i+1}, L_i = log2 y_i, T_k = H_k + s_k. The hop formula was checked against the literal "first orbit value divisible by 4" on 13,199 inputs.

### B0. Evertse's theorem, quoted from p. 227

> COROLLARY 1. Let c, d be constants with c > 0, 0 ≤ d < 1, let S_0 be a finite set of prime numbers and let n be a positive integer. Then there are only finitely many tuples x = (x_0, …, x_n) of rational integers such that x_0 + … + x_n = 0 (9); x_{i_0} + … + x_{i_s} ≠ 0 (10) for each proper, non-empty subset {i_0,…,i_s} of {0,…,n}; gcd(x_0,…,x_n) = 1 (11); ∏_{k=0}^{n} (|x_k| ∏_{p∈S_0} |x_k|_p) ≤ c·‖x‖^d (12).

Here ‖x‖ = max|x_k|, and the left side of (12) is the product of the S_0-free parts.

Theorem 1 is the number-field version. It asserts finitely many (c,d,S)-admissible projective points X ∈ P^n(K) with coordinate sum 0 and no vanishing proper subsum. Admissible means the coordinates can be chosen as S-integers with ∏_{v∈S}∏_k ‖x_k‖_v ≤ c·H(X)^d. The corollary follows from ‖x‖ = H(X) iff gcd = 1.

- **Hypotheses:** n fixed; all proper non-empty subsums non-zero; primitive; d < 1 strictly. "Finitely many" ranges over integer tuples for fixed (c, d, S_0, n).
- **Effectivity:** the proof rests on Schlickewei's p-adic Subspace theorem (the paper's Theorem 4), which gives no size bound. The paper states no effective bound and does not itself use the word "ineffective"; that is my reading.
- **Against STATE.md:** the remembered form is correct. Nothing changes.

### B1. Identities (PROVED, machine-checked)

**Lemma 1.** 2^h y' = 3^s y + 2^h − 2^s.
Proof: 2^(v−1) y' = 3^s m − 1 + 2^(v−1); multiply by 2^s. ∎

**Lemma 2.** 2^(H_k) y_k = 3^(S_k) y_0 + Σ_{i<k} 3^(σ_i)(2^(H_{i+1}) − 2^(H_i+s_i)). Dividing by 2^(s_0):

2^(T_k−s_0) m_k = 3^(S_k) m_0 + Σ_{i<k} 3^(σ_i)(2^(H_{i+1}−s_0) − 2^(H_i+s_i−s_0)).

This is the §A hop-word identity. Proof: induction with Lemma 1. ∎

**Lemma 3 (size).** Z_k := 2^(H_k) y_k ≤ 2^k 3^(S_k) y_0, and L_{j+1} ≤ L_j + (θ−1)s_j.
Proof: Z_{j+1} = 3^(s_j) Z_j + 2^(H_{j+1}) − 2^(H_j+s_j) < 3^(s_j) Z_j + Z_{j+1}/2 because y_{j+1} ≥ 2. For the second, y' ≤ (3^s m − 1)/2 + 1 ≤ 3^s m = (3/2)^s y. ∎

**Lemma 4 (tuple).** Let x ∈ Z^(2k+2) have entries 2^(T_k−s_0) m_k, −3^(S_k) m_0, and for i = 0..k−1 the pair −3^(σ_i) 2^(H_{i+1}−s_0), +3^(σ_i) 2^(H_i+s_i−s_0). Then:
- (i) Σx = 0 and all entries are non-zero.
- (ii) Before dividing by 2^(s_0), the 2-adic valuations are s_0, s_0, H_1, H_1+s_1, H_2, …, H_k, H_k+s_k. There is one tie at the bottom and the rest are strictly increasing, since s_i ≥ 1 and h_i ≥ s_i+1.
- (iii) No proper non-empty subsum vanishes. If Σ_I = 0 then Σ_{I^c} = 0 too. Whichever of I, I^c does not contain both tied entries has a unique entry of minimal valuation, so its sum is non-zero. This uses no signs.
- (iv) gcd = 1: the tuple contains 3^(σ_0) (i = 0, exponent 0) and 2^(H_k−s_0) (i = k−1, σ = 0).
- (v) With S_0 = {2,3}, the left side of (12) is ≤ m_0 m_k, and ‖x‖ ≥ 2^(T_k−s_0) m_k.

### B2. Theorem A (PROVED)

**Theorem A.** For every k ≥ 1 and δ > 0, the set Exc(k,δ) = {odd x_0 ≥ 1 : H_k + s_k > (1+δ) log2(x_0+1)} is finite. Equivalently, there is C(k,δ) with H_k + s_k ≤ (1+δ)L_0 + C(k,δ) for all odd x_0 ≥ 1. More precisely, for 0 < η < 1/θ, all x_0 outside a finite set E(k,η) satisfy (1−ηθ)(H_k+s_k) < (1+η)L_0 − η(θ−1)k.

Proof. Apply Corollary 1 with n = 2k+1, S_0 = {2,3}, c = 1, d = 1−η to the tuples of Lemma 4. For all but finitely many tuples, (12) fails:

m_0 m_k > (2^(T−s_0) m_k)^(1−η), i.e. (1−η)(T−s_0) < log2 m_0 + η·log2 m_k.

Lemma 3 gives log2 m_k ≤ k + θS_k + L_0 − T. With log2 m_0 = L_0 − s_0 this yields T < (1+η)L_0 − ηs_0 + ηk + ηθS_k. Since S_k ≤ T − k − 1, we get (1−ηθ)T < (1+η)L_0 + ηk − ηθ(k+1).

The map from orbits to tuples is finite-to-one: a tuple fixes N = 3^(S_k) m_0, so m_0 ≤ N and s_0 ≤ S_k ≤ log_3 N. Finally choose η with (1+η)/(1−ηθ) ≤ 1+δ. ∎

**Quantifiers.**
- The order is ∀k ∀δ ∃C ∀x_0. C is uniform in x_0 and depends on k and δ.
- C is ineffective. There is no bound on max Exc and no claim about |Exc|.
- **Nothing is uniform in k.** x_0 = 1 has T_k = 2k+1 and L_0 = 1, so C(k,δ) ≥ 2k − δ (PROVED). x_0 = 3 → 1 gives the same for x_0 > 1.

**Content check.** The trivial bound is T_k ≤ L_0 + θS_k + k. Theorem A removes the θS_k term, so it is non-trivial only when some depth s_i (i < k) is comparable to L_0. For bounded depths it adds nothing.

**Sharpness.** x_0 = 2^n − 1 gives T_k ≥ n = L_0, so limsup_{x_0→∞} T_k/L_0 = 1 exactly for each fixed k (PROVED).

**k = 1** reads v_2(3^s m − 1 + 2^(v−1)) ≤ (1+δ)·log2 m + δs + C, which matches §A.

### B3. Window law and spikes (PROVED)

**Corollary B.** For all odd x_0, all j ≥ 0, fixed k and δ: H_{j+k} − H_j + s_{j+k} ≤ (1+δ)L_j + C(k,δ), with the same C. This is Theorem A at base point x_j.

**Theorem D.** Σ_{i=j}^{j+k} s_i + k ≤ (1+δ)(L_0 + (θ−1)S_j) + C(k,δ) for all j. Hence limsup_j (s_j+…+s_{j+k})/(s_0+…+s_{j−1}) ≤ log2(3/2) for every fixed k.
Proof: the left side is ≤ the window, because h_i ≥ s_i+1. Lemma 3 gives L_j ≤ L_0 + (θ−1)S_j. S_j ≥ j → ∞; let δ → 0. ∎

**Corollary C.** No odd x_0 ≥ 1 has a hop word with liminf s_{j+1}/s_j > 1, for any v-letters. In particular pure spike words of every geometric ratio r > 1 are excluded.
Proof: if s_{i+1} ≥ ρs_i eventually, then S_j ≤ s_j/(ρ−1) + O(1) and the window is ≥ ρ^k s_j. The ratio is ≥ ρ^k(ρ−1)(1−o(1)). Pick k with ρ^k(ρ−1) > θ−1. ∎

**The overclaim check.** The fixed-k limitation does not break this. The argument fixes k = k(ρ) once and slides the base point; it never lets k grow. What is not obtained:
- any rate or explicit prefix-length bound (C is ineffective and k(ρ) → ∞ as ρ → 1);
- any exclusion of sub-geometric depth growth such as s_j = j^p.

**Theorem E.** For every odd x_0 ≥ 1: S_j, H_j and log x_j are e^{o(j)}. More precisely H_j ≤ A(k,δ')·(1+L_0)·(θ+δ')^(j/(k+1)).
Proof: H_{j+k+1} − H_j is at most the (k+1)-hop window, which is ≤ (1+δ)L_j + C(k+1,δ), and L_j ≤ L_0 + (θ−1)H_j. Iterate. ∎

The elementary bound is θ^j. In Syracuse-step count the statement is invisible; it concerns how many odd steps j hops can hold.

### B4. Return-map version (PROVED)

With v = 8(33n+32) = 2^(4r+3) w, a block is v → 3^(3r+2) w + 1. This was checked equal to the repo closed form (P_r n + D_r)/Q_r with gates on 140,000 integers.

With a_l = 4r_l+3, b_l = 3r_l+2, A = a_1+…+a_s, B = b_0+…+b_{s−1}:

2^A w_s = 3^B w_0 + Σ_{l=1}^{s} 3^(b_l+…+b_{s−1}) 2^(a_1+…+a_{l−1}).

The valuations are A; 0; 0, a_1, …, A−a_s. There is one tie, so the Lemma 4(iii) argument applies and is sign-free. gcd = 1, and Σ units ≤ 3^B.

**Theorem F.** For every s ≥ 1 and ε > 0 there is C(s,ε) such that every n ≥ 0 with return letters r_0..r_s satisfies Σ_{l=0}^{s}(4r_l+3) ≤ (1+ε)·log2(8(33n+32)) + C(s,ε). Equivalently R_W ≥ c(s,ε)·Q_W^(1−ε) for words of length s+1.
Proof: Evertse gives w_0 w_s > (2^A w_s)^(1−η). With w_s ≤ 2·3^B w_0·2^(−A) and B ≤ (3/4)(a_0+A), we get (A+a_0)(1 − 3ηθ/4) < (1+η)·log2 v_0 + η. ∎

**Corollary.** log n_N and r_0+…+r_{N−1} are e^{o(N)}.

**Limits.** For bounded alphabets Theorem F is vacuous. c(s,ε) → 0 is forced for this method, because the same sign-free proof covers n = −1 (word 0^∞), where it needs 8^s ≤ C·9^(sε). A version uniform in s is not obtained and would be stronger than H1.

### B5. Status table

| Statement | Status |
|---|---|
| Evertse Cor. 1 as quoted in §A | VERIFIED against the source |
| Lemmas 1–4, return identity | PROVED; machine-checked |
| Theorems A, D, E, F; Corollaries B, C | PROVED (modulo Evertse's published corollary) |
| C(k,δ) ≥ 2k−δ; limsup T_k/L_0 = 1 | PROVED |
| Trend toward limsup ≤ 1 in data | VERIFIED to x_0 < 10^10 as a trend only |
| "power runs u^k g u'^k' excluded" (§A) | CANDIDATE; subsum and degeneracy analysis not done |
| "only m = 1 is elementary via LTE" (§A) | NOT VERIFIED, doubtful (s_1 for x_0 = 2^s−1 is a 2-adic closeness condition, not an LTE consequence) |
| Any constant independent of k | REFUTED (x_0 = 1) |
| T_k ≤ L_0 + (k+1+o(1))·log2 L_0 | CONJECTURED (heuristic count n^(k+1)·2^(−E) per band; fits data) |

### B6. New relative to proof.md Theorem 62

Theorem 62's ledger is the k = 0 case, s_j ≤ L_0 + Σ log2 g. It is elementary, exact and effective, with pure-spike boundary log2 3. Its "sharp" refers to the ledger criterion, not to realisability.

New here:
- (k+1)-hop windows, which exclude ratio r > θ^(1/(k+1)) and hence every r > 1, for arbitrary v-letters;
- Theorem E.

The price is ineffective constants, k-dependence and a deep external theorem. Words with 1 < r ≤ θ pass the ledger and are realised by 2-adic seeds (Theorem 60); Corollary C says none of those seeds is a positive integer.

This does not touch Lemma E in the bounded-depth regime and gives no descent.

### B7. Litmus

For x → (ax+d)/2 on odd x: y = (a−2)x + d = 2^s m, y' = (a^s m − d)/2^(v−1) + d, and 2^h y' = a^s y + d(2^h − 2^s). Lemma 2, the valuation pattern, the subsum argument and gcd | d hold verbatim. This was checked exactly for (5,1), (3,±5), (3,7), (3,11), (3,13), (5,3), (7,1), (5,−1), (9,1), and for negative x under (3,1), which is the 3n−1 map.

Evertse applies with S_0 = {2,a} ∪ {p | d}. Lemma 3 holds with 2 replaced by 1+|d|+d². So Theorems A, D, E, F hold for all these maps with θ → log2 a.

- **5n+1:** the fixed point F_5(13) = 13 (letter (3,5), y = 40) has T_k = 7k+3. There is no contradiction because C depends on k.
- **3n−1:** x = −5 has T_k = 3k + const. Same remark.
- **Where 3, +1 and positivity enter:** 3 enters only via θ−1; +1 only via the choice of y; positivity only via y_i ≠ 0. Negative orbits can hit x = −1 (for example −3 → −1; 257 such cases in the test range), where the statement is void.

The law equally holds for maps with cycles and conjecturally divergent orbits. It cannot prove descent, H1 or Lemma E.

### B8. Prior art (four queries; limited)

- **E. Y. Chang, "Exploring Collatz Dynamics with Human-LLM Collaboration", [arXiv:2603.11066](https://arxiv.org/abs/2603.11066)** (v6, 22 Apr 2026; copy in `sunit/lit/chang2026/`).
  - Result 221, "S-unit Reformulation": (m+1)·3^L − T^L(m)·2^(S_L) = 2^L − P_L.
  - Result 235 and the paradigm list on p. 142: the Subspace theorem is "blocked" because P_L has primes outside {2,3}, and coefficients depend on L.
  - Its "episodes" are FMF hops.
  - So the identity is known and the application was reported as impossible. The step here is to expand P_L into two unit terms per hop, which fixes the term count for a fixed hop count.
- **Lagarias' annotated bibliographies** ([math/0309224](https://arxiv.org/pdf/math/0309224), [math/0608208](https://arxiv.org/pdf/math/0608208)): the transcendence-theory entries surfaced there (e.g. Belaga–Mignotte) use Baker / linear forms in logarithms for cycles. Nothing of the present type was found.
- **Not checked:** MathOverflow, Tao's blog.

Decision: the identities are known or folklore. Theorem A is apparently new but low depth (credence about 65% that it is unpublished).

### B9. Brainstorm and outcome

1. Hop-level S-unit equation, fixed k: done (Theorem A).
2. Return-block version: done (Theorem F).
3. Sliding base point for infinite words: done (D, E, C).
4. Power-run compression u^K into two terms: CANDIDATE, see (e).
5. Uniform k via quantitative Subspace: killed by x_0 = 1.
6. Bounding |Exc| via Evertse–Schlickewei–Schmidt counts: not attempted; those counts are for pure unit equations, not free cofactors.
7. Effective k = 1 via p-adic Baker (Yu): only for bounded m; with free m it gives nothing.
8. n-term abc as a conditional uniform version: still k-dependent; dropped.
9. Using A against divergence: fails, because A bounds halvings from above and divergence needs few halvings.

## (c) Scripts (in `sunit/scripts/`)

1. `taskset -c 2 /home/matrix/home/projects/collatz/venv/bin/python verify_identities.py` (about 15 s).
   - Expected last line: `ALL CHECKS PASSED`.
   - Counts: H2/H3/H5/H6 = 145076; H4 (all subsets, ≤ 12 terms) = 141965; R0 = 140000; R2–R4 = 25889; cycle slopes 2 / 7 / 3.
2. `gcc -O2 -o budget_scan budget_scan.c -lm && taskset -c 2 ./budget_scan 100000000` (1.3 s; output in `data/budget_scan_1e8.txt`). With argument `10000000000` it takes 134 s (`data/budget_scan_1e10.txt`). It uses exact 128-bit arithmetic with an overflow abort; floats appear only in the threshold tally.
3. `taskset -c 2 …/python litmus_scan.py > ../data/litmus_scan.txt` (2 s): records for 3n+1, 5n+1, 3n−1, 3n+5 to |x_0| < 10^6. All four maps show the same shape.

**Record holders, odd 3 ≤ x_0 < 10^8** (max T_k @ x_0, with ratio T_k/log2(x_0+1); n is the bit-length of x_0+1):

| k | n=12 | n=16 | n=20 | n=24 | n=26 | n=27 (partial) |
|---|---|---|---|---|---|---|
| 1 | 22 @ 4095 (1.83) | 23 @ 65535 (1.44) | 26 @ 680191 (1.34) | 32 @ 16777215 (1.33) | 35 @ 41313279 (1.38) | 33 @ 92954879 (1.25) |
| 2 | 26 @ 4095 (2.17) | 32 @ 51775 (2.04) | 32 @ 839679 (1.63) | 37 @ 9699327 (1.59) | 41 @ 67108863 (1.58) | 39 @ 83742975 (1.48) |
| 3 | 29 @ 4095 (2.42) | 36 @ 51775 (2.30) | 39 @ 736355 (2.00) | 46 @ 9699327 (1.98) | 48 @ 42865023 (1.89) | 48 @ 81745759 (1.83) |

To 10^10, the n = 33 records are 42 @ 6032939583 (1.29), 48 @ 4757493247 (1.49) and 57 @ 6450184191 (1.75).

**Exceptional sets {3 ≤ x_0 < 10^10 : T_k > c·L_0}** as (count, largest element):

| c | k=1 | k=2 | k=3 |
|---|---|---|---|
| 3 | — | — | (8, 63) |
| 2.5 | — | (5, 23) | (22, 351) |
| 2 | (2, 15) | (22, 51775) | (157, 4849663) |
| 1.75 | (6, 4095) | (74, 2056191) | (657, 369098751) |
| 1.5 | (25, 103935) | (330, 3026288639) | — |
| 1.4 | (39, 1472895) | — | — |
| 1.3 | (74, 798490623) | — | — |

(— = not listed here; the full tally is in the data files.)

Reading: consistent with limsup = 1, with slow convergence. The band excess max(T_k − n) at n = 20–33 is about 5–10, 11–18 and 19–24 for k = 1, 2, 3, roughly (k+1)·log2 n. For c near 1 the sets are still growing at 10^10, so finiteness there is not visible in the data and is not claimed from it.

## (d) Dead ends

- **Uniform-in-k constant:** false (C ≥ 2k − δ). Any use of Theorem A with k growing along the orbit is invalid.
- **Deriving H1 or Lemma E:** A and F are upper bounds on halving in a fixed window. They transfer to 5n+1 and 3n−1 and are vacuous for bounded depths or alphabets.
- **Effectivity:** none from Evertse 1984. Do not quote any numerical C(k,δ).
- **Plain Syracuse-step version** (n+2 terms for n odd steps): trivial, since Σa_i ≤ nθ + log2(x_0+1) directly. The gain exists only because a depth-s hop packs s odd steps into two unit terms.
- **Draft scripts:** the identities in `h1/scripts/s1_identities.py` (I1, I2, I6, I7) were re-implemented and pass. The size bound for general d needs the constant 1+|d|+d², not 2; my first version had this wrong and the check caught it.

## (e) Best lead

**Lemma (power-run compression; CANDIDATE).** Fix primitive hop blocks u, u' and a connector g such that u g u' is not a factor of one periodic word. With 2^(H_u) y' = 3^(S_u) y + B_u and β_u = B_u/(2^(H_u) − 3^(S_u)), the run u^K acts by y' − β_u = (3^(S_u)/2^(H_u))^K (y − β_u). A prefix u^K g u'^(K') therefore gives an S-unit equation over {2,3} ∪ (primes of the fixed denominators) with a fixed number of terms and free exponents K, K'.

Claim to prove: for every δ > 0, K·H_u + K'·H_{u'} ≤ (1+δ)L_0 + C(u,g,u',δ).

Work needed:
- the vanishing-subsum analysis (the valuations of the β-terms are no longer strictly ordered);
- showing the only degenerate solutions are cycles.

If true, it bounds how well an integer orbit can re-approach a second periodic seed after leaving a first one. That is the "coincidence channel" of Theorem 62, in the bounded-alphabet regime where A and F are vacuous.

Cheapest kill: brute-force K, K' ≤ 12 for G01 blocks and look for a vanishing proper subsum, or for seeds with K·H_u + K'·H_{u'} > 1.5·L_0 at large L_0.

---

Files are in `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/sunit/`:
- `scripts/verify_identities.py`
- `scripts/budget_scan.c`
- `scripts/litmus_scan.py`
- `data/budget_scan_1e8.txt`
- `data/budget_scan_1e10.txt`
- `data/litmus_scan.txt`
- `lit/evertse1984.pdf`
- `lit/page03.png`, `lit/page04.png`, `lit/page05.png`
- `lit/chang2026/arxiv-2603.11066v6.pdf`

`REPORT.md` was not written (harness refusal); the report above is the full text.