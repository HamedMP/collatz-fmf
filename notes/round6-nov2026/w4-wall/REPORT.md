<!-- Saved by the coordinator from the w4-wall agent's final message (the agent's own write was refused). -->
# FULL REPORT — w4-wall: the common wall (digits of 2^(−l) mod 3^ν with l ≍ ν)

Date: 2026-11-18. Labels: PROVED (full proof below), VERIFIED (finite, by the named script), CANDIDATE, REFUTED. Nothing here was refereed by anyone but me.

Notation as in `w3-fp0/REPORT.md`: E_k = E mod 2^k, N_k = #E_k, T_k(ξ) = Σ_{c∈E_k} e(ξc/2^k), s = 0.28776, N_j·2^(−sj) ∈ [1, 1.64].

## (a) Summary

1. Verdict: no published technique reaches j ≍ J. Short sums of g^i mod p^k are controlled for R ≥ exp(c·k^(2/3+ε)) (Korobov; Kerr–Mérai–Shparlinski 2020, saving exponent 10^(−11)·ρ²) and for R ≥ 2^(k/2) by completion. (SGP) needs R ≈ √k. Digit-counting results all stop at the Baker rate log n/log log n.
2. Even perfect square-root cancellation in every short linear sum Σ e(a·3^i/2^j) would not give (SGP). The transfer to Σ|T_k(ξ3^i)| goes through pairs (c,c′) and is capped at K^(−1/8) (Remark 3).
3. New theorem (PROVED, modest): pair counting plus the completed bound for incomplete sums of 3^i mod 2^j improves s/4 = 0.0719 to s/(2+4s) = 0.0913 (Theorems A′, B′) and 0.0512 to 0.0650 (Corollary C′).
4. Korobov–Vinogradov sums do not help further: they would beat completion only with a saving constant ≥ 0.29, where the published constant is 10^(−11).
5. Correction to w3-fp0 (e): (SGP) for R = 2^(k^(1−c)) gives m ≤ (½·log₂Q)^(1/(1−c)), not m ≤ Q^(c′). The saving exp(−(log X)^(c′)) needs R = k^C.
6. (SGP) is not refuted, but "δ₀ ≈ ½" is refuted for adversarial frequencies: ξ = ±3^n·u/t (t ∈ {1, 11}), n ≈ k/log₂3, gives δ₀ = 0.066 at k = 3200, predicted limit 0.0555. A beam search over all odd ξ (k ≤ 96) finds nothing worse.
7. These frequencies never occur in the reduction: Proposition D only needs ξ = h·3^(−P) with |h| ≤ 2^(2m) and P ≥ k (restated as (SGP*) in section e). There δ₀ = 0.50 numerically up to k = 3200.
8. Discrepancy of {ξ3^i mod 2^k}, k ≤ 4000: indistinguishable from random points for every R from √k to k² when the start is generic; for ξ = 1 it is trivial until R ≫ k.
9. Litmus: every statement holds verbatim for −E (3n−1) and for the 5n+1 set (⟨5⟩ also has order 2^(j−2)). Nothing here bears on H1.
10. Best lead: (SGP*) for R = k^C, or failing that the range 1 < ρ < 2 by 2-adic van der Corput (section e).

## (b) Statements

### Lemma 5 (incomplete sums of 3^i mod 2^j) — PROVED; VERIFIED j ≤ 16 (`n3_lemmas.py`)

For j ≥ 4, odd a and every finite interval I ⊂ Z: |Σ_{i∈I} e(a·3^i/2^j)| ≤ j·2^((j+1)/2).

Proof. Put τ = 2^(j−2), the period of 3^i mod 2^j.
- Complete sums vanish: {3^i mod 2^j} = {x ≡ 1, 3 mod 8}, and Σ_{y mod 2^(j−3)} e(ay/2^(j−3)) = 0 for j ≥ 4.
- Twisted complete sums S(a,b) = Σ_{i mod τ} e(a3^i/2^j + bi/τ) satisfy |S(a,b)|² = Σ_{d mod τ} e(bd/τ)·Σ_i e(a(3^d−1)3^i/2^j). If v₂(3^d−1) ≤ j−4 the inner sum is a multiple of a complete sum to a modulus 2^(j′), j′ ≥ 4, hence 0. Since v₂(3^d−1) = 1 (d odd) or v₂(d)+2 (d even), at most 8 residues d survive. So |S(a,b)| ≤ 2^((j+1)/2).
- For an interval I′ of length < τ: Σ_{I′} = τ^(−1)·Σ_b c_b·S(a,b) with |c_0| < τ and |c_b| ≤ τ/(2|b|) for 0 < |b| ≤ τ/2. So |Σ_{I′}| ≤ 2^((j+1)/2)·(2 + ln(τ/2)) ≤ j·2^((j+1)/2). Full periods contribute 0. ∎

Measured: max_I |S_I| ≈ 0.65·2^(j/2), and max_b |S(a,b)| = 2^(j/2) exactly for j ≥ 6, so the lemma is sharp up to the factor j.

### Lemma 6 (fibres of E_k) — PROVED; VERIFIED exactly for n ≤ k ≤ 40

Every residue class mod 2^n contains at most 2·N_(k−n) elements of E_k (0 ≤ n ≤ k). Hence #{(c,c′) ∈ E_k² : c ≡ c′ mod 2^n} ≤ 2·N_(k−n)·N_k.

Proof. E_j = f_a(E_(j−3)) ⊔ f_b(E_(j−4)) for j ≥ 4, the two parts are separated mod 8, and f_a (resp. f_b) is a bijection from residues mod 2^(n−3) (resp. 2^(n−4)) onto residues ≡ 7 mod 8 (resp. ≡ 0 mod 16) mod 2^n. So for n ≥ 4 the maximal fibre φ(k,n) ≤ max(φ(k−3,n−3), φ(k−4,n−4)). Iterate down to n′ ≤ 3 with k′−n′ = k−n: φ ≤ N_(k′) ≤ N_(k−n+3) ≤ 2·N_(k−n), because N_(j+3) = N_j + N_(j−1) ≤ 2N_j. ∎

### Proposition F (second moment along a unimodal progression) — PROVED; VERIFIED in 252 cases

Let κ ≥ 4, h a nonzero integer with e = v₂(h), λ₀ odd, and M ≥ 0 a finitely supported unimodal sequence with sum W and maximum M*. Then

Σ_i M(i)·|T_κ(hλ₀3^i)|² ≤ 2N_κ·[ W·N_(min(e+3,κ)) + M*·Σ_{j=4}^{κ−e} N_(j+e)·j·2^((j+1)/2) ] ≤ N_κ²·[ 6·2^(se−sκ)·W + 11.1·κ·2^((κ−e)/2)·M* ].

Proof. Expand |T_κ|² = Σ_{c,c′} e(hλ₀(c−c′)3^i/2^κ). For a pair put j = κ − v₂(h(c−c′)) (j ≤ 0 if the phase is trivial).
- j ≤ 3: bound the i-sum by W. These pairs have c ≡ c′ mod 2^(κ−3−e); Lemma 6 gives at most 2N_κ·N_(e+3) of them.
- 4 ≤ j ≤ κ−e: the i-sum is Σ_i M(i)e(a′3^i/2^j) with a′ odd. By the layer-cake formula M(i) = ∫_0^(M*) 1[M(i) > t]dt and unimodality, each level set is an interval, so the sum is ≤ M*·j·2^((j+1)/2) by Lemma 5. These pairs have v₂(c−c′) = κ−j−e; Lemma 6 gives at most 2N_κ·N_(j+e).
- Closed form: N_j ≤ 1.64·2^(sj), N_κ ≥ 2^(sκ), Σ_{j≤J} 2^((s+½)j) ≤ 2.377·2^((s+½)J). ∎

### Theorem A′ — PROVED

For K > k ≥ 7 with K−k ≥ 84 and every integer h ≠ 0 (e = v₂(h)):

|T_K(h)|/N_K ≤ √( 6·2^(se)·2^(−s(k−3)) + 72·k·2^((k−e)/2)/√(K−k−4) ).

With k = ⌊log₂(K/log₂²K)/(1+2s)⌋: |T_K(h)| ≤ C·2^(se/2)·(log K)^(s/(1+2s))·K^(−s/(2+4s))·N_K, where s/(2+4s) = 0.0913 (w3-fp0 Theorem A: s/4 = 0.0719).

Proof. By w3-fp0 Lemma 1, |T_K(h)| ≤ Σ_v |T_(κ_v)(hλ_v)|. Group v by (q′, ℓ): 7 groups, κ constant on each, q′ ≥ K−k−4. In a group λ_v = λ₀3^i with multiplicity M(q′,i), which is unimodal with M* ≤ c₁W/√q′, c₁ = 6.5 (w3-fp0 Lemma 2). Cauchy–Schwarz and Proposition F give Σ_i M|T_κ| ≤ W·N_κ·√(6·2^(se−sκ) + 72κ2^((κ−e)/2)/√q′). Sum over groups with Σ W·N_κ = N_K. If e ≥ κ the right side exceeds 1. ∎

### Theorem B′ — PROVED

For m ≥ 1, k ≥ max(7, m+3), K = Q+m, K−k ≥ 84:

|N(Q,m)/N_K − 2^(−m)| ≤ 2.45·(1.5+0.78k)·2^(−s(k−3)/2) + 8.5·(1+0.7k)·√k·2^(k/4)·(K−k−4)^(−1/4).

Proof. As in w3-fp0 Theorem B up to |N(Q,m) − 2^(−m)N_K| ≤ Σ_v Σ_{h≢0} |a_h|·|T_(κ_v)(hλ_v)|, with |a_h| ≤ 1/(2|h|). Apply the group bound above for each h, split the square root, and use Σ_{h≤2^(κ−1)} 2^(s·v₂(h)/2)/h ≤ 1.46+0.78κ and Σ_{h≤2^(κ−1)} 1/h ≤ 1+0.7κ. ∎

**Corollary B1′ — PROVED.** With k = ⌊log₂(K/log₂²K)/(1+2s)⌋ (so k ≈ 0.635·log₂Q, against w3-fp0's 0.5·log₂Q): |N(Q,m)/N_(Q+m) − 2^(−m)| ≤ C·(log Q)^(1.19)·Q^(−0.0913) for 1 ≤ m ≤ k−3.

**Corollary C′ — PROVED (constants not explicit).** With m* = ⌊0.0913·log₂Q − 1.19·log₂log₂Q − C⌋: N(Q,Q) ≤ N(Q,m*) ≤ C·(log Q)^(0.85)·Q^(−0.0650)·2^(sQ), where 0.0650 = (1−s)·s/(2+4s).

Seeds: #{w ≤ X : w ∈ E} ≤ C·X^s·(log log X)^(0.85)·(log X)^(−0.0650) (w3-fp0: −0.0512). The exponent s is unchanged.

Evaluated with exact N_j (`n7_compare.py`; "Theorem A" is my rendering of w3-fp0's proof, h odd):

| log₂K | Theorem A: log₂ bound | Theorem A′: log₂ bound |
|---|---|---|
| 40 | −0.75 | −0.91 |
| 80 | −3.60 | −4.28 |
| 160 | −9.35 | −11.39 |
| 320 | −20.86 | −25.81 |
| 640 | −43.88 | −54.83 |

The gain is asymptotic: both bounds exceed 1 at K = 2^20.

### Remarks (what the wall is and is not)

**Remark 1 (Korobov range, exact).** Kerr–Mérai–Shparlinski, "On digits of Mersenne numbers" (arXiv:2001.03380), Corollary 2.12 as read on ar5iv: for a fixed prime q ≥ 3, q ∤ g, and M ≤ q^(Aγ),

Σ_{K<m≤K+M} e(z·g^m/q^γ) ≪ M^(1−cρ²)·log M + M^(1−c)·q^(8G), ρ = log M/log q^γ.

- Lemma 2.11 has the explicit exponent 10^(−11)·ρ² for M ≤ q^(2γ/65).
- They state the bound is nontrivial for q^(γ^(2/3+ε)) ≤ X. So the range is R ≥ exp(c·k^(2/3+ε)), with saving exp(−c(log R)³/k²), which is subexponential in k.
- The statement is for odd q. It covers (TRI) (g = 2, q = 3) directly. For modulus 2^k I did not find a printed statement (CANDIDATE that it extends).
- Vandehey (arXiv:1606.07911) treats general moduli, with a threshold near exp(log m/log log m) as rendered in the abstract; that is weaker than Korobov for prime powers.

**Remark 2 (Korobov cannot enlarge Theorem B′) — PROVED as arithmetic.** In Proposition F, a bound "saving R^(−σ(ρ)) for sums of length R = √K to modulus 2^j = R^ρ" gives a total saving R^(−min(sρ, σ(ρ))) in the second moment. Completion has σ = 1 − ρ/2, with optimum ρ = 1/(s+½) = 1.27: this is Theorem A′. A Korobov saving c/ρ² wins only if c/ρ² ≥ sρ for some ρ ≥ 2, i.e. c ≥ 8s = 2.3 (c ≥ 0.29 if it were valid down to ρ = 1). Published: 10^(−11).

**Remark 3 (ceiling of linear sums).** The sum over odd a of |Σ_i M(i)e(a3^i/2^j)|² is about 2^(j−1)·ΣM², so some linear sum is ≥ W·K^(−1/4) whenever M has width √K. The pair method therefore never gives more than K^(−1/4) in the second moment, K^(−1/8) for |T_K(h)|, and (log X)^(−(1−s)/8) = (log X)^(−0.089) for seeds. Short sums really are square-root small for 1.1 ≤ ρ ≤ 4 (VERIFIED j ≤ 24, `n4_short.py`: max window sum ≤ 3.9·√R). The missing range 1.27 < ρ ≤ 1.74 would be worth 0.0913 → 0.125.

**Remark 4 (why equidistribution of the orbit does not transfer).** T_k(ξ) depends on all bits of ξ: the top t bits of ξ pair with c mod 2^t, the low bits with the top bits of c. There is no regularity in the low bits. Discrepancy of {ξ3^i/2^k} at scale 2^(−t) therefore controls Σ|T_k(ξ3^i)|² only through the Wiener norm of |T_k|², which is N_k² against a mean of N_k. That is exactly Proposition F.

**Remark 5 (correction to w3-fp0 section e) — PROVED as arithmetic.** In Proposition D the window length is R ≍ √K. (SGP) for R = 2^(k^(1−c)) allows k = (½log₂K)^(1/(1−c)), hence m ≍ (log Q)^(1/(1−c)) and a seed saving exp(−c′(log log X)^(1/(1−c))). That beats any power of log X but is far from exp(−(log X)^(c′)). Reaching m ≤ Q^(1/(2C)) needs (SGP) for R = k^C.

### Proposition G (adversarial frequencies) — VERIFIED numerically; mechanism derived by hand

By w3-fp0 Proposition E, T_k(ξ) = e(−ξ·9^(−1)/2^k)·T_(k−3)(ξ/9) + T_(k−4)(ξ/27). For ξ = 3^n with 3^n < 2^k the running frequency 3^(n−P) stays a small integer and every phase is ≈ 1 until P ≥ n, which for typical words happens at Q ≈ 1.408n. Only the tail of length k − 1.408n cancels. Prediction (tails of square-root size): δ(n/k) = ½(1 − 1.408·n/k) up to large-deviation corrections, minimum 0.0555 at n/k = 1/log₂3.

Single-frequency δ = −log(|T_k|/N_k)/log N_k for ξ = 3^n (`n2_table.py`; prediction from `n5_predict.py`):

| n/k | 0.1 | 0.3 | 0.5 | 0.6 | 0.63 | 0.66 | 0.7 |
|---|---|---|---|---|---|---|---|
| k = 800 | 0.450 | 0.328 | 0.163 | 0.098 | 0.074 | 0.236 | 0.451 |
| k = 3200 | 0.448 | 0.302 | 0.155 | 0.082 | 0.064 | 0.219 | 0.427 |
| predicted | 0.430 | 0.289 | 0.148 | 0.077 | 0.056 | — | — |

Worst (SGP) window average, R = ⌈√k⌉, over the whole two-sided orbit of h = 1:

| k | 200 | 400 | 800 | 1600 | 3200 |
|---|---|---|---|---|---|
| adversarial zone (ξ = 3^n), δ₀ | 0.126 | 0.099 | 0.077 | 0.070 | 0.066 |
| generic zone (ξ = 3^(−P), P ≥ 0), δ₀ | 0.519 | 0.506 | 0.496 | 0.502 | 0.507 |

- 5n+1 control at k = 800: adversarial δ₀ = 0.218 at n/k = 0.43 (prediction 0.197). 3n−1 is identical to 3n+1.
- Denominator 11 resonates: b is the identity mod 11 and a permutes the other residues in one 10-cycle, so the twist depends only on the number of a's mod 10. ξ = 3^n/11 gives δ = 0.066 at k = 800, the same family.
- Other denominators at k = 400 (`n6_rational.py`): 5, 7, 13, 19, 23, 25, 121 give δ ≥ 0.46; 17 gives 0.31. At k = 800, 17 and 43 give 0.31–0.33.
- Beam search over all odd ξ, k ≤ 96 (`n9_beam.py`): at the larger sizes (k = 48 to 96) the maximiser is in the family ±3^n·u/t or within 0.002 of it; at k = 24 and 36 it is not, with gaps 0.033 and 0.006.
- Exhaustive k = 24 (`n8_brute.py`): max |T| = N^0.83, too small to separate from the random-set level N^0.78.

Consequence. (SGP) as stated (all ξ) can hold only with δ₀ ≤ 0.066 (CANDIDATE limit 0.0555). No counterexample family (δ₀ → 0) was found.

### Discrepancy of the short orbit — VERIFIED (floats, `n1_disc.py`)

D*_R·√R for {ξ3^i mod 2^k / 2^k : i < R}; random points give 0.4–1.2.

| k | R | ξ = 1 | ξ = 3^(5k) | ξ random | random points |
|---|---|---|---|---|---|
| 1000 | 32 (√k) | 5.66 | 1.26 | 0.57 | 0.60 |
| 1000 | 1000 | 19.8 | 0.72 | 0.59 | 1.00 |
| 4000 | 31810 | 14.2 | 0.79 | 0.75 | 1.06 |
| 4000 | 1.6·10⁷ (k²) | 0.87 | 0.60 | 0.58 | 0.73 |

For ξ = 1 and R < 0.63k all points lie in [0, 3^R/2^k), so D* ≈ 1 (5.66 = √32). Full output is in `out_disc.txt`.

### State of the art (task 1)

[R] = abstract or statement fetched this session. [M] = from memory, not re-read.

- **Erdős's conjecture:** 2^n has a digit 2 in base 3 for n > 8 (1, 4, 256 are the only exceptions). Open.
- **Lagarias, arXiv:math/0512006 [R, abstract level]:** the truncated real exceptional set has Hausdorff dimension log₃2 = 0.6309; the 3-adic exceptional set E(Z₃) is conjectured to have dimension 0; the level-2 set has dimension in [0.315, 0.5].
- **Abram–Lagarias arXiv:1308.3133; Abram–Bolshakov–Lagarias arXiv:1508.05967 [R]:** dim E(Z₃) ≤ log₃φ = 0.438. All of these are cylinder-counting statements; none concerns a single orbit.
- **Narkiewicz 1980 [M]:** #{n ≤ N : 2^n omits the digit 2} ≤ 1.62·N^(log₃2).
- **Dimitrov–Howe, arXiv:2105.06440 [R]:** the powers of 3 with at most 22 one-bits are 3^x, x < 25; the only powers of 2 that are sums of at most 25 distinct powers of 3 are 1, 4, 256. Elementary and finite.
- **Senge–Straus 1973; Stewart, J. reine angew. Math. 319 (1980) 63–72 [R via citations]:** the number of nonzero digits of n in two multiplicatively independent bases exceeds log log n/(2·log log log n) for large n. For 3^m in base 2 this is ≍ log m/log log m, the Baker rate, the same as w3-g2's Lemma X. The brief's form "log log n/(log log log n + C) − 1" could not be confirmed.
- **Bugeaud, arXiv:2608.23017 (Aug 2026) [R, abstract]:** only finitely many powers of 3 have a "simple" binary representation.
- **Stephan, arXiv:2607.14774 (2026) [R, abstract]:** p-periodicity of the binary expansion of 3^m breaks at ≍ log m/log log m positions. Baker rate again.
- **Dupuy–Weirich, J. Number Theory 158 (2016) 268–280 [R, slides only]:** the low m bits of 3^n are periodic in n with period ord(3 mod 2^m). This is the complete-period regime R = 2^(k−2) of w3-fp0 Lemma 3.
- **Holdum–Klausen–Rasmussen, arXiv:2601.09510 [R, abstract]:** density-zero results for digit patterns of α^k in base p as k varies, again over long ranges of k.
- **Burrell–Yu, arXiv:1905.00832 [R]:** integers with only digits 0, 1 in bases 3, 4, 5 number ≤ C_ε·n^ε. A dimension-zero statement for sets, of Shmerkin–Wu type, not for a single orbit.
- **Mauduit–Rivat, Drmota–Mauduit–Rivat, Spiegelhofer [M]:** digit sums along primes, squares, cubes. These sequences grow polynomially; nothing covers exponentially growing sequences.
- **Bourgain 2005 [M]:** Σ_{x∈H} e(ax/q) ≤ |H|·q^(−ε) for subgroups |H| ≥ q^δ, and sums of g^n over n ≤ N with N ≥ q^ε. Still exponentially long in k.

### Verdict (task 4): the gap

| Statement | Known | Needed |
|---|---|---|
| Linear sums Σ_{i<R} e(a3^i/2^k), power saving in R | R ≥ 2^(k/2)·k (Lemma 5) | — |
| Same, some saving | R ≥ exp(c·k^(2/3+ε)) (Korobov, KMS) | would not suffice (Remark 3) |
| (SGP): Σ_{i<R} \|T_k(ξ3^i)\| ≤ R·N_k^(1−δ₀) | R ≥ 2^(k−2), δ₀ = ½ (w3-fp0 Lemma 3) | R ≈ √k for a power saving; R = k^C for exp(−(log X)^c) |
| Average of \|T_k\| over √K points, saving only | N_k·K^(−0.0913+o(1)) with k = 0.635·log₂K (Theorem A′) | N_k^(1−δ₀) with k = βK |
| (TRI): deep black points near the diagonal | triangles of size ≤ j_Δ·log²n by 2-adic Baker, so log n/log log n scales (w3-g2) | ≤ C·n^(3/2)·e^(−cS) for S ≤ δn |

Weakest sufficient statements: for FP-0, (SGP*) below with R ≈ √k; for G2, w3-g2's E_exp. Both are exponential equidistribution of digits of 2^(−l) mod 3^ν with l/ν bounded above and below. Nothing published is within an exponential of that range.

## (c) Scripts

All in `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/w4-wall/`, with PY = `/home/matrix/home/projects/collatz/venv/bin/python`.

- `$PY n3_lemmas.py` (about 80 s): Lemmas 5, 6, Proposition F, chain of Theorem A′. Last line `ALL CHECKS OK`.
- `$PY n2_table.py K h [mult d] [levels]`: table of T_k(h·3^(−P)) for all P ∈ [−0.75K, 0.35K], gmpy2 precision 0.2K+96 bits. `run_table.sh` writes `out_table.txt`; the K = 3200 run takes tens of minutes.
- `$PY n5_predict.py [mult]`: first-passage prediction; last line `n/k=0.6309 predicted delta=0.0555`.
- `$PY n6_rational.py 400`: frequencies 3^n·u/t.
- `$PY n9_beam.py 96 24`: beam search, output in `out_beam.txt`.
- `$PY n8_brute.py 24`: exhaustive maximum.
- `$PY n1_disc.py k`: discrepancy, output in `out_disc.txt`.
- `$PY n4_short.py`: short window sums.
- `$PY n7_compare.py`: the comparison table, output in `out_compare.txt`.

## (d) Brainstorm and dead ends

| # | Idea | Kill test | Outcome |
|---|---|---|---|
| 1 | Korobov/Vinogradov short sums in place of Parseval | is the saving ≥ 2^(−m)? | DEAD: saving exp(−c(log R)³/k²) with c = 10^(−11); needs c ≥ 0.29 (Remark 2) |
| 2 | Completion (Pólya–Vinogradov) plus pair counting | closed form | DONE: Theorems A′, B′ |
| 3 | Transfer "orbit equidistributed at scale 2^(−t)" to Σ\|T_k\| | regularity of T_k in the low bits of ξ | DEAD: none; Wiener norm N_k² (Remark 4) |
| 4 | Square-root cancellation hypothesis for all linear short sums | L² lower bound | CEILING K^(−1/8) (Remark 3); cannot give (SGP) |
| 5 | Counterexample to (SGP): ξ = 3^n | DP table | δ₀ drops to 0.066, not to 0. (SGP) survives; "δ₀ ≈ ½" does not |
| 6 | Counterexample via rational frequencies u/t | scan t | only t = 11 resonates, same exponent as t = 1 |
| 7 | Frequencies 3^n with n > k/log₂3 | profile at n/k = 0.64–0.7 | DEAD: the incoherent head grows 9× faster than the tail shrinks; δ rises to 0.43 |
| 8 | Rigorous lower bound for \|T_k(3^n)\| | needs a lower bound for tails T_k′(1), T_k′(3) | NOT DONE: no handle on cancellation between O(k) tail terms |
| 9 | 2-adic van der Corput for 1 < ρ < 2 | — | NOT PURSUED: worth at most 0.0913 → 0.125 |
| 10 | Stewart/Baker for digit windows | rate | DEAD: log n/log log n, as in w3-g2 Lemma X |

Hostile self-review.
- Theorems A′ and B′ use w3-fp0's Lemmas 1, 2 and 4 (first bullet) unchanged. If those fail, these fail.
- The closed-form constants (6, 72, 2.45, 8.5) are hand arithmetic: CANDIDATE. The inequality with exact N_j was checked on 252 (group, h) cases with K ≤ 240, where it is far from sharp (the bound exceeds 1).
- Proposition G is numerical. `n1`, `n4`, `n8`, `n9` use floats.
- Literature: only abstracts and one ar5iv rendering were read. Korobov's 1972 paper itself was not.
- I found no prior statement of Theorems A′/B′ but did not search for one specifically.

## (e) Best lead

**(SGP*) — the hypothesis Proposition D actually needs.** There are δ₀ > 0 and C such that for all k, all integers 1 ≤ |h| ≤ 2^k with v₂(h) = e, all P₀ ≥ k and R = ⌈√k⌉:

Σ_{i<R} |T_k(h·3^(−P₀−i) mod 2^k)| ≤ C·R·2^(e/2)·N_k^(1−δ₀).

- With Erdős–Turán truncation at H = 2^(2m), only |h| ≤ 2^(2m) is used. The adversarial frequencies of Proposition G (ξ = +3^n) would need |h| ≥ 3^(P₀) and never occur. Numerically δ₀ = 0.50 here up to k = 3200.
- Intermediate targets, in order:
  1. Linear sums of length R = 2^(j/ρ) for 1.27 < ρ < 1.74 with saving R^(−sρ), by a 2-adic van der Corput or stationary-phase iteration. Gives K^(−1/8) at best.
  2. (SGP*) for R = k^C. Gives exp(−(log X)^(1/(2C))).
  3. (SGP*) for R = √k. Gives FP-0.
- Targets 2 and 3 need cancellation between pairs (c,c′), i.e. structure of E, not of the orbit of 3.

**Credences**

| Claim | Credence |
|---|---|
| Lemmas 5, 6, Proposition F | 95% |
| Theorems A′, B′, Corollary C′ (exponents 0.0913, 0.0650; constants unspecified) | 88% (inherits w3-fp0 Lemmas 1, 2, 4) |
| Explicit constants as printed | 70% |
| Korobov range and Remark 2 | 90% |
| Remark 5 (correction of the R = 2^(k^(1−c)) claim) | 92% |
| Adversarial δ₀ ≤ 0.07 for all-ξ (SGP) | 90% |
| Limit 0.0555 | 65% |
| (SGP*) true with δ₀ near ½ | 80% |
| Any published technique reaches R = k^C | < 3% |
| Theorems A′/B′ new to the literature | 55% |
| This family yields H1 | < 1% |

Sources:
- [arXiv:2001.03380](https://arxiv.org/abs/2001.03380) (Kerr–Mérai–Shparlinski)
- [arXiv:1606.07911](https://arxiv.org/abs/1606.07911) (Vandehey)
- [arXiv:math/0512006](https://arxiv.org/abs/math/0512006) (Lagarias)
- [arXiv:1308.3133](https://arxiv.org/abs/1308.3133) (Abram–Lagarias)
- [arXiv:1508.05967](https://arxiv.org/abs/1508.05967) (Abram–Bolshakov–Lagarias)
- [arXiv:2105.06440](https://arxiv.org/abs/2105.06440) (Dimitrov–Howe)
- [arXiv:2608.23017](https://arxiv.org/abs/2608.23017) (Bugeaud)
- [arXiv:2607.14774](https://arxiv.org/abs/2607.14774) (Stephan)
- [arXiv:2601.09510](https://arxiv.org/abs/2601.09510) (Holdum–Klausen–Rasmussen)
- [arXiv:1905.00832](https://arxiv.org/abs/1905.00832) (Burrell–Yu)
- [arXiv:1704.00432](https://arxiv.org/abs/1704.00432) (source for the Stewart bound as cited)
- Stewart, J. reine angew. Math. 319 (1980) 63–72
- Dupuy–Weirich, J. Number Theory 158 (2016) 268–280