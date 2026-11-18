<!-- Saved by the coordinator from the w2-beta agent's final message (the agent's own write was refused). -->
# FULL REPORT — w2-beta: from positive density toward every integer (round 6, 2026-11-17)

Notation. T(n) = n/2 (n even), (3n+1)/2 (n odd). Syr is the odd-to-odd Syracuse map. G = {n ≥ 1 : n reaches 1}. P(a) = {n : some T^k(n) = a}. d(A), d_low, d_up are natural, lower and upper density. α = log2 3.

Hypotheses taken from others (Lean-built, not rebuilt; audit credences 0.90 / 0.85):
- **(i)** Mazur–ND: for every f → ∞, almost all n (natural density) have an iterate < f(n). Two quantitative forms are used below.
  - ND Thm 1.2: the number of odd N ≤ x whose orbit never goes ≤ N0 is ≤ C_d (log N0)^(−d) x, for d < 5/143, with C_d existential.
  - ND Thm 3.1: for all real x ≥ x0, with y = x^α' (α' = 1.001), B_y = odd ∩ [y, y^α'], U_y uniform and L_y ∝ 1/N on B_y: P(T_x(U_y) > s(x)) ≤ 184 x^(−1/32000) and ‖law Pass_x(U_y) − law Pass_x(L_y)‖_1 ≤ 384256 (log x)^(−d).
  - I read the Lean statement `eventually_ndA5RealSameBranchRateBounds` (real x, both branches); it matches.
- **(ii)** Mazur: #{n < X : n ∈ G} ≥ cX for X ≥ X0, with c > 0 explicit and astronomically small.
- **(iii)** Not claimed by Mazur (the audit thinks his proof transfers): for every a with 3 ∤ a, d_up(P(a)) > 0.

PROVED means a full proof is given here with no hypothesis. CONDITIONAL means a full proof from the named hypothesis.

## (a) Summary

1. CONDITIONAL on ND Thm 3.1 (new, T2): every eventually Syracuse-invariant set has a natural density. In particular G and every P(a) do; Mazur states existence is not asserted. Density at X equals the logarithmic average over [X^0.999, X] plus O((log X)^(−d)).
2. PROVED (T3): the "combine (i) and (ii)" bootstrap is the identity map, F(c) = c.
3. PROVED (T1): (i) ⇔ δ(C) → 0, where δ(C) = d_up{n : orbit never ≤ C}; and d_low(G) ≥ 1 − δ(2^71). This uses (i) and Barina only, not (ii). With ND Thm 1.2 it is vacuous unless C_d < 0.573.
4. PROVED (T5, "the wall"): (iii) ∧ d(G) = 1 ⇒ Collatz. Under (iii), density one is equivalent to Collatz, so this is FAILURE of the family, stated exactly.
5. PROVED, unconditional, elementary (T6): every interval [x, x + Cx(log x)^(−1/13.3)] contains an element of G. (ii) is not needed and only gives h = Cx. The argument is multiplier-blind (true for 5n+1 too).
6. PROVED (T6c): a gap [x, x+h] in G is equivalent to G missing O(log² x) explicit windows at scale x/h. So h = x^θ needs pointwise membership at scale x^(1−θ).
7. Litmus 3n−1 (to 10^8): basins 0.32697 / 0.32471 / 0.34832, stable, equidistributed mod 27 and mod 8 to 10^−3, max gaps 2368 / 2563 / 1871. Inside 3n+1 itself, backward-closed first-passage classes have densities strictly between 0 and 1.
8. Litmus 5n+1 (to 2·10^7): basin of 1 has fraction 0.0016 and falling; 99.5% escape 2^120. (ii) fails there; T6 holds.
9. What distinguishes 3n+1 from 3n−1: nothing at density level. Every input used by (i), (ii) and T2 is invariant under n ↦ −n. The only sign-asymmetric input in existence is finite verification, which enters only via T1.
10. Nothing here touches H1 or Lemma E.

## (b) Statements and proofs

### T1. What (i) says, and what (i) + verification gives — PROVED

Let B_C = {n : every iterate of n is > C} and δ(C) = d_up(B_C), non-increasing in C.

**T1a.** (i) holds for every f → ∞ iff δ(C) → 0.

Proof.
- (⇐) Given f and ε, pick C with δ(C) < ε. Since f(n) > C for n ≥ n0, {n : no iterate < f(n)} ⊂ B_C ∪ [1, n0].
- (⇒) Suppose δ(C) ≥ ε for all C. Choose X_1 < X_2 < … with X_k ≥ k·X_(k−1) and #(B_k ∩ [1, X_k]) ≥ (ε − 1/k)X_k. Put f(n) = k on (X_(k−1), X_k]. Then #{n ≤ X_k : no iterate < f(n)} ≥ #(B_k ∩ (X_(k−1), X_k]) ≥ (ε − 2/k)X_k, contradicting (i). ∎

**T1b.** If [1, M] ⊂ G then G^c ⊂ B_M, so d_low(G) ≥ 1 − δ(M). With M = 2^71 and ND Thm 1.2 (summing over n = 2^j·odd): d_low(G) ≥ 1 − 2C_d(71 ln 2)^(−d). CONDITIONAL on ND Thm 1.2.

- Evaluation: (71 ln 2)^(−0.034965) = 0.8727, so the bound is non-trivial only if C_d < 0.573.
- The paper's C_d is existential and appears to absorb an asymptotic threshold (its construction is trivial below e^100000) by a factor 2(log N_*)^d ≈ 3. So the bound is vacuous today.
- Litmus: for 3n−1 the same inequality holds with M = 4 and is true (0.327 ≥ 0.327). A sign-symmetric δ bound must satisfy δ(16) ≥ 0.32, since 3n−1 has δ_−(16) = d(basin of 17) ≈ 0.348, but nothing forbids it being small at 2^71. This route is not killed by the litmus; it is killed by constants.

### T2. Existence of natural density — CONDITIONAL on ND Thm 3.1 (new)

**Theorem T2.** Let A be a set of odd positive integers and Q_A ≥ 1 such that for all odd N > Q_A: N ∈ A ⇔ Syr(N) ∈ A. Assume ND Thm 3.1 and the logarithmic no-hit bound P(T_x(L_y) = ∞) ≤ Cx^(−c0) (Tao 2019; Lemma T2.1 is an elementary substitute). Then a(X) := 2·#(A ∩ [1, X])/X converges as X → ∞. Consequently every T-invariant set, G, and every P(a) (take Q_A = a) has a natural density.

Proof.
1. Fix x ≥ max(x0, Q_A), y = x^α', X = y^α', r = 1/α'. For N ∈ B_y with T_x(N) < ∞, all iterates before the passage are > x ≥ Q_A, so N ∈ A ⇔ Pass_x(N) ∈ A.
2. With ν_U, ν_L the totalised passage laws: |P(U_y ∈ A) − ν_U(A)| ≤ P(T_x(U_y) = ∞), |P(L_y ∈ A) − ν_L(A)| ≤ P(T_x(L_y) = ∞), and |ν_U(A) − ν_L(A)| ≤ ‖ν_U − ν_L‖_1. Hence |P(U_y ∈ A) − P(L_y ∈ A)| ≤ C1(log x)^(−d).
3. P(U_y ∈ A) = a(X) + O(X^(r−1)).
4. By partial summation, with b(v) = a(e^v) and U = log X: P(L_y ∈ A) = (1/((1−r)U)) ∫_(rU)^U b(v) dv + O(1/U). (Denominator Σ_(B_y) 1/N = (1−r)U/2 + O(1); numerator = O(1) + ½∫_y^X a(t) dt/t.)
5. Substituting v = e^σ, S = log U, c(S) = b(e^S), λ = ln α':
   c(S) = ∫_0^λ c(S−τ) k(τ) dτ + e(S), where k(τ) = e^(−τ)/(1−r) on [0, λ] is a probability density and |e(S)| ≤ C2·e^(−dS).
6. This is a renewal equation Z = z + Z*F on [0, ∞), with Z(t) = c(S0+t), F = k dτ, and z(t) = e(S0+t) + 1_(t<λ) ∫_(τ>t) c(S0+t−τ) k(τ) dτ. Here z is bounded, integrable and tends to 0. F has a bounded compactly supported density, so its renewal density u(t) → 1/μ, and Z = z + z*u → (1/μ)∫z by dominated convergence.
7. So c(S), hence a(X), converges. For T-invariant A ⊂ ℕ, A = ⊔_j 2^j(A ∩ odd), so d(A) = Σ_j 2^(−j−1)·lim a = lim a. ∎

**Lemma T2.1 (substitute for the L-no-hit bound; sketch only).** P(T_x(L_y) = ∞) ≤ ν_L({1}) ≤ ν_U({1}) + ‖ν_U − ν_L‖_1, and ν_U({1}) ≤ P(T_x(U_y) > s(x)) + P_U(some Syracuse valuation among the first s(x) is ≥ ½ log2 x). A prefix (a_1..a_(i−1)) of sum A' together with a_i ≥ L fixes N in one class mod 2^(A'+L). The count in an interval of H integers is therefore ≤ s(x)(H·2^(−L) + 2^K'), plus the N with A_(s(x)) > K', which is ≤ H·e^(−c·s(x)) + 2^K' by the exact geometric law of valuation prefixes and Chernoff (K' = 0.9 log2 x, H ≈ x^1.002). Total ≤ Cx^(−c). This is not written line by line; T2 does not need it if Tao's bound is cited.

Remarks.
- The same proof gives d(A) = logarithmic density of A. I expect |a(X) − d(A)| ≪ (log X)^(−d) (CANDIDATE: needs the exponential rate in the renewal theorem, not written).
- 3 enters only through ND Thm 3.1 (orbits descend). The result is sign-blind: for 3n−1 it says each basin has a natural density, consistent with the numerics. For 5n+1 the hypothesis fails. Nothing false is produced.
- Referee residue: I rely on the statement of Thm 3.1, not its proof. It is used for every real x ≥ x0 on the branch y = x^α', which is what the Lean statement says. T2.1 is a sketch.

### T3. The bootstrap is the identity — PROVED (given T2)

For n > C let Pass_C(n) be the first iterate ≤ C; it lies in (C/2, C] because the last step is a halving. Let π_C(m) = d{n : Pass_C(n) = m}, which exists by T2. For every invariant A with density d(A):

d(A) = Σ_(m ∈ A ∩ (C/2, C]) π_C(m) + d(A ∩ B_C), so |d(A) − π_C(A)| ≤ δ(C) → 0, while #(A ∩ (C/2, C])/(C/2) → d(A) trivially.

So the first-passage measure and the uniform measure give every invariant set the same limiting mass. The "missing independence between first-passage location and the convergent set" holds automatically and its content is c = c. A map F(c) > c would need π_C to favour G over G^c, meaning a positive correlation between the size of the backward tree of m and the forward fate of m.

**No such F exists by any argument using only backward closure, (i), (ii) and positive density.** Witnesses:
- Inside 3n+1 (VERIFIED to 10^8): the classes F_m = {n > 32 : Pass_32(n) = m} are closed under n → 2n and n → (2n−1)/3 within (32, ∞) and pairwise disjoint. Their fractions:

| m | 23 | 28 | 19 | 31 | 32 | 29 | 25 | 20 | 17 | 22 | 26 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| fraction | 0.340 | 0.191 | 0.145 | 0.093 | 0.062 | 0.059 | 0.034 | 0.029 | 0.0157 | 0.0156 | 0.0150 |

  Multiples of 3 get 0. P(5) has fraction 0.93787 and the route through 32 has 0.06213.
- 3n−1 (VERIFIED to 10^8): three fully invariant basins, 0.32697 / 0.32471 / 0.34832.

G differs from the F_m only by also being forward-closed, and from a 3n−1 basin only by sign.

π_C is far from uniform: max_m π_C(m)·C/2 = 5.45, 10.7, 12.9 at C = 32, 1024, 16384. Mass by m mod 9 at C = 16384 is (0, .250, .201, 0, .103, .237, 0, .135, .074). A comparison "π_C ≤ H·uniform" loses a factor H > 1 and never improves c.

### T4. Residue structure of invariant sets — PROVED relations, CANDIDATE equidistribution

Let A be T-invariant with density d.

PROVED: d(A ∩ 2ℕ) = d/2; d(A ∩ {0 mod 4}) = d(A ∩ {2 mod 4}) = d/4; d(A ∩ {2 mod 3}) = d/3. (A ∩ 2ℕ = 2A, and n ↦ (3n+1)/2 is a bijection from odd n ≤ X onto {m ≡ 2 mod 3, m ≤ (3X+1)/2}.)

In general the normalised class densities satisfy ν(s mod 3^b) = ½ν(s/2 mod 3^b) + (3/2)ν((3s+1)/2 mod 3^(b+1)). Haar measure on ℤ_3 is a solution (PROVED by substitution). Equidistribution mod 2^k is equivalent to equidistribution mod 3^a along r mod 2^k ↔ r' mod 3^a, the same mirror as ledger family 4.

CANDIDATE (not proved): Haar is the only solution, so every invariant set with a density is equidistributed in every class mod 2^a·3^b.
- VERIFIED to 10^8 for the three 3n−1 basins: all classes mod 27 within [0.9989, 1.0011] of uniform, mod 8 within [0.9984, 1.0014].
- VERIFIED to 10^8 for the non-trivial basins of 3n+5, 3n+11 and 3n+13 (mod 9 and mod 8).

If true, no congruence information distinguishes G from a hypothetical positive-density alien component.

### T5. From density one to all — PROVED implication; the wall

**T5a.** If (iii) holds and d_up(G^c) = 0, every positive integer reaches 1.

Proof. Let n0 ∉ G. Its orbit has infinitely many odd terms; take one, n', and put a = (3n'+1)/2. Then 3 ∤ a and a ∉ G, so P(a) ∩ G = ∅ and d_up(G^c) ≥ d_up(P(a)) > 0. ∎

**T5b.** Under (iii): d(G) = 1 ⇔ Collatz. Without (iii): d(G) = 1 ⇔ every non-convergent a has d(P(a)) = 0.

**T5c (with T2).** Each component K of the Collatz graph is invariant, so it has a density d_K, and Σ_K d_K ≤ 1 with d_G ≥ c. Under (iii) every d_K > 0, so at most 1/ε components have d_K ≥ ε. This gives no finiteness of cycles, because d(P(a)) is not ≍ 1/a: a·d(a) ranges from 0.39 to 1337 for a ≤ 4096, 3 ∤ a, X = 2·10^7 (VERIFIED).

Meaning. The only implication "density one ⇒ all" is T5a, and it needs (iii), which is the drift-dependent statement (4 > 3).
- 5n+1: (iii) fails. Basin fractions are 0.0016, 0.0025, 0.0006 at 2·10^7, falling like x^(−0.34). "Almost all escape" coexists with three cycles.
- 3n−1: (iii) holds numerically, cycles exist, and no basin has density one. Consistent.

Verdict: under (iii), density one is as strong as Collatz. Any bootstrap c → 1 is a Collatz proof in disguise and must contain a sign-asymmetric input. FAILURE of the family.

### T6. Short intervals — PROVED (unconditional), plus the exact obstruction

**Lemma G (covering).** Let 3 ∤ m, d ≥ 0, k ≥ 4d. There is n with T^k(n) = m, exactly d odd steps, and 2^k·m/3^d − 2^(k−d) < n ≤ 2^k·m/3^d.

Proof. For 3 ∤ n_(i−1), the numbers 2^c·n_(i−1) with c of the admissible parity run through {1, 4, 7} mod 9 as c steps by 2. So among the two smallest admissible c (both ≤ 4), at least one gives n_i = (2^c·n_(i−1) − 1)/3 with 3 ∤ n_i. This yields n_d with k0 = Σc_i ≤ 4d; put n = 2^(k−k0)·n_d. Then n_d = 2^k0·m/3^d − Σ_(i=1)^d 2^(c_(i+1)+…+c_d)/3^(d−i+1), and the sum is < (2^k0/3^(d+1))·Σ_i(3/2)^i < 2^(k0−d). ∎ (Exact test: `verify_gap.py`, 2821 random cases.)

**Theorem G.** If m ∈ G, 3 ∤ m, k ≥ 4d, then G meets (2^k·m/3^d − 2^(k−d), 2^k·m/3^d].

**Corollary G1 (verification).** If [1, M] ⊂ G then every [x, x + 2x/M] with x ≥ M meets G (d = 0). With M = 2^71 this is h = 2^(−70)·x for all x. Trees do not improve this beyond constants, since the lattice n = (2^k·m − S)/3^d, m ≤ M, has relative spacing 3^d/M.

**Corollary G2 (asymptotic).** Let g_D be the largest gap of {−dα mod 1 : 0 ≤ d ≤ D}. For D ≥ 1, 0 < ε < 1 and real x ≥ 2^(5D + log2(1/ε) + 2), the interval [x, x·2^(g_D)/(1−ε)] contains an element of G.

Proof. Let t0 = log2(x/(1−ε)). Pick d ≤ D and an integer K with K − dα ∈ [t0, t0 + g_D]. Put j = ⌈d·log2(3/2) + log2(1/ε)⌉, k = K − j ≥ 4d, m = 2^j. Theorem G gives n ∈ G with 2^K·3^(−d)(1−ε) < n ≤ 2^K·3^(−d). ∎

By the three-gap theorem, g_D < 2/q for the largest convergent denominator q ≤ D of α. Rhin's ‖qα‖ ≥ c·q^(−13.3) (as quoted in the ND paper) gives q > (cD)^(1/13.3). Hence:

**Every interval [x, x + Cx(log x)^(−1/13.3)] contains an integer that reaches 1**, with h = O(x/log x) along the scales where D is a convergent denominator.

- Examples from `verify_gap.py`: relative length 0.061 for x ≥ 2^194, and 0.0076 for x ≥ 2^1412. Below about exp(2^900), Corollary G1 is far stronger.
- Litmus: the proof never uses 3 or +1 (for 5n+1: c ≤ 8, α = log2 5), and it is true there. The basin of 1 of 5n+1 has relative max gap 0.10, 0.024, 0.016, 0.0056, 0.0027, 0.0018 at 10^3 … 2·10^7 while its density → 0. G2 carries no Collatz content.
- It may be folklore; I did not find it stated.
- It answers the question put to Tao on 23 Aug 2026 (his reply, saved in `nd-referee/sources/taoblog/post.html`: the natural-density results should give some h = o(x), "possibly even a logarithmic saving") without using (i) or (ii).

**T6c (obstruction; PROVED equivalence up to edge terms).**
- Forward: if n ∈ G ∩ [x, x+h] then for every k, T^k(n) = (3^d·n + S)/2^k ∈ G with 0 ≤ S/2^k < (3/2)^d. So G meets W(k,d) = [3^d·x/2^k, 3^d(x+h)/2^k + (3/2)^d].
- Converse (Theorem G): an m ∈ G with 3 ∤ m, k ≥ 4d and x + 2^(k−d) ≤ 2^k·m/3^d ≤ x + h puts an element of G in [x, x+h].

So "G ∩ [x, x+h] = ∅" says G misses O(log² x) windows of relative length h/x at every lower scale ≥ (3/2)^d·x/h; at scale x/h these are windows of O(1) integers. Compositions do not enlarge the family, since the ratios 3^d/2^k commute. Consequences:
- h = x^θ is equivalent to pointwise membership in G of at least one of polylog(x) prescribed integers of size x^(1−θ). A set of density c can miss polylog prescribed integers, so (ii) + backward closure cannot give any θ < 1.
- (ii) alone gives h = (1/c − 1 + o(1))x; G2 beats it unconditionally.
- An ℓ1 "short-interval transport" is false: the passage law of a short interval sits on a few windows of relative width H/X (REFUTED as a route).

Numerics on what backward-closed positive-density sets actually do (VERIFIED to 10^8; not a proof of a rate):

| X | 10^3 | 10^4 | 10^5 | 10^6 | 10^7 | 10^8 |
|---|---|---|---|---|---|---|
| 3n−1 basin of 1, max gap up to X | 26 | 76 | 112 | 340 | 859 | 2368 |

This is about x^0.42; a random set of density 1/3 would give about 45. In 3n+1, class F_23 (density 0.34) has max gap 1845 and F_17 (density 0.0157) has 470831. The gap-length histogram decays faster than a power, so I do not claim polynomial growth.

## (c) Scripts (in `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/w2-beta/`, core 1)

- `gcc -O2 -o basins basins.c`; `taskset -c 1 ./basins 3 -1 100000000 0` → `out_3nm1_1e8.txt` (4 s). Expected last checkpoint: `c0: dens=0.326973 maxgap=2368@94684225 | c1: dens=0.324708 maxgap=2563@… | c2: dens=0.348319 maxgap=1871@…`.
- `taskset -c 1 ./basins 3 1 100000000 32 pass32.tsv` → `out_3np1_C32.txt`. The same with 1024 and 16384 → `out_3np1_passC.txt` (`H = 10.725092`, `H = 12.922703`).
- `taskset -c 1 sh run_controls.sh` → `out_3npd.txt` (3n+5, 7, 11, 13 to 10^8) and `out_5np1.txt` (5n+1 to 2·10^7, escape cap 2^120). Expected: `X=20000000 esc=19905800(0.995290) | c0: dens=0.001573 maxgap=34162@19488335`.
- `gcc -O2 -o visits visits.c`; `taskset -c 1 ./visits 20000000 4096` → `out_visits.txt`. Expected: `min a*d(a) = 0.3864 at a=3184 ; max = 1337.0124 at a=3644`.
- `python verify_gap.py` → `q=3: 2821 random (m,d,k) OK; largest single c used = 4 (bound 4)` and `q=5: 3373 … (bound 8)`.

3n+d results at 10^8:
- 3n+5: basins 0.1404 / 0.4979 / 0.2000 / 0.0922 / 0.0326 / 0.0369.
- 3n+7: 6/7 and 1/7.
- 3n+11: 0.1968 / 0.7123 / 0.0909.
- 3n+13: ten basins, largest 0.4775.

No `exploreXX.py` was run, and `plan.md` / `proof.md` were not touched (track rule: write only in the track directory). No git commit.

## (d) Brainstorm (kill test → outcome) and dead ends

1. First-passage bootstrap c → F(c). Kill test: 3n−1 basins. DEAD: it is the identity (T3).
2. (i) + Barina ⇒ explicit density. Kill test: read the constant. DEAD for now: C_d is existential and would need to be < 0.573.
3. Density existence from transport. Kill test: is the error summable in log log X? ALIVE → T2.
4. Uniqueness of the 3-adic profile by Fourier. DEAD END: û(ξ) − ½û(2ξ) = ½Σ_(3η=ξ) e(−η)û(2η) is underdetermined level by level (2·3^(k−1) equations, 2·3^k unknowns). It needs positivity or mixing.
5. Density one ⇒ all via tree density. Kill test: 5n+1. Result T5: true exactly under (iii), and then equivalent to Collatz.
6. Short intervals from (ii). DEAD: only h = Cx.
7. Short intervals from the backward tree. ALIVE → G2; T6c is the ceiling.
8. ℓ1 short-interval transport for h = x^θ. DEAD: the passage law of a short interval is not the common profile.
9. Uniform d(P(a)) ≍ 1/a to count cycles. DEAD: a·d(a) spans 0.39 … 1337.
10. Counter-model ℕ \ (forward closure of an interval). DEAD END: the forward closure of [x, x+h] swallows most of [x/h, h], destroying density at lower scales.

Blocked ledger families were not re-run. T4 touches family 4 only as an observation.

## (e) Best lead

**Lemma (target-uniform positive density, = (iii) with constants).** For every odd a with 3 ∤ a there is a seed M = (2^c·a − 1)/3, with c chosen so that M lies in Mazur's good residue class mod 3^q and M ≥ 16^(b0), such that Mazur's Prop. 3.1, Prop. 5.3 and Lemma 6.1 hold verbatim with "S(M) = 1" replaced by "Syr(M) = a, M non-periodic". This gives #(P(a) ∩ [X, 32X)) ≥ ηX/M for X ≥ X0(M).

Why this one: with T2 and T5 it yields a single clean statement. Every component of the Collatz graph would have a positive natural density, the densities would sum to at most 1, and "d(G) = 1" would literally be Collatz. It is a finite check of an existing proof; target 1 is used only in the seed Lemma 4.1 and in uniqueness of histories. It would not prove Collatz.

Second lead: make C_d in ND Thm 1.2 explicit. d_low(G) ≥ 1 − 2C_d(log M)^(−d) is the only place where verification converts into density, and no litmus blocks it.

## (f) Credences

- T2 derivation correct given its hypotheses: 0.85. Hypotheses true (ND Thm 3.1): the audit's 0.90. T2.1 sketch: 0.8.
- T1, T3, T5: 0.97.
- T6 (Lemma G, G1, G2): 0.95; the exponent 1/13.3 relies on Rhin as quoted in the ND paper.
- T4 equidistribution true: 0.8; provable soon: 0.3.
- (iii) true: 0.9; follows from Mazur's proof as written: 0.6 (not checked).
- This family yields "every integer": < 0.001.