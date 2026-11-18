<!-- Saved by the coordinator from the w3-fp0 agent's final message (the agent's own write was refused). -->
# FULL REPORT — w3-fp0

Conventions. a(w) = (9w+1)/8 on w ≡ 7 (8); b(w) = 27w/16 on 16 | w. Inverse branches f_a(z) = (8z−1)/9, f_b(z) = 16z/27. A word v has P_v = 2A+3B, Q_v = 3A+4B. E_k := E mod 2^k, N_k := #E_k (N_k = N_{k−3}+N_{k−4} for k ≥ 4; N_0..N_3 = 1,2,2,2). s = 0.2877607871, x = 2^(−s), x³+x⁴ = 1.

Definitions.
- N(Q,m) := #{0 ≤ w < 2^Q : w mod 2^(Q+m) ∈ E_{Q+m}}, the number of elements of E_{Q+m} whose top m binary digits vanish.
- With life(w) = bits consumed by completed steps: #{life ≥ Q+m} ≤ N(Q,m) ≤ #{life ≥ Q+m−3}.
- T_k(ξ) := Σ_{c∈E_k} e(ξc/2^k).

## (a) Summary

1. Theorem B (PROVED): the top m bits of E_{Q+m} equidistribute, with relative error C·log Q·Q^(−s/4), for m ≤ ½log₂Q − 8.
2. Corollary C (PROVED): N(Q,Q) ≤ C(log Q)^(1−s)·Q^(−s(1−s)/4)·2^(sQ), with s(1−s)/4 = 0.0512.
3. Theorem A (PROVED): polynomial-in-K Fourier decay at every fixed integer frequency. Ledger family 19 is blocked only for power decay.
4. Mechanism: the top bits of c ∈ E_K are an affine image λz+τ of a short tail block z ∈ E_k, with λ = 3^(−P_v). P_v spreads over about √K consecutive integers, so λ covers the whole group ⟨3⟩ mod 2^k when 2^k ≪ √K. Parseval on that group gives square-root cancellation on average, whatever τ is.
5. FP-0 is reduced to (SGP): the same average over only about √k consecutive powers of 3.
6. Exact counts to Q = 112: heuristic decay, then saturation at 1; N(Q,Q) is 1 or 2 on the whole reachable range.
7. T_K(h) is computable in O(K²) operations (Proposition E). Up to K = 3200, |T_K(h)|/N_K is at or below N_K^(−1/2).
8. Evaluated exactly rather than through closed-form constants, the proved chain already gives N(Q,1) ≤ 0.94·N_Q at Q = 10⁴ and N(Q,4) ≤ 0.41·N_Q at Q = 10⁸.
9. The litmus maps satisfy the same theorems; there is no emptiness and no conflict with Theorems 48/57.
10. Nothing here is progress on H1. `proof.md` and `plan.md` were not edited.

## (b) Statements

### Lemma 1 (tail-block decomposition) — PROVED

Let K > k ≥ 7 and n = K−k. Let 𝒱 be the words v = v′ℓ with Q_{v′} < n ≤ Q_v, and κ_v := K − Q_v ∈ {k−3,…,k}. Then

E_K = ⊔_{v∈𝒱} { r_v + 2^(Q_v)·((λ_v z + τ_v) mod 2^(κ_v)) : z ∈ E_{κ_v} }, with λ_v = 3^(−P_v) mod 2^(κ_v) and 0 ≤ r_v < 2^(Q_v).

Hence, for m ≤ k−3:
- N(K−m, m) = Σ_v #{z ∈ E_{κ_v} : (λ_v z+τ_v) mod 2^(κ_v) < 2^(κ_v−m)};
- T_K(h) = Σ_v e(h·f_v(0)/2^K)·T_{κ_v}(hλ_v).

Proof.
- E = f_a(E) ⊔ f_b(E). f_a(z) mod 2^j depends exactly on z mod 2^(j−3), f_b(z) mod 2^j on z mod 2^(j−4), and the images differ mod 8. So E_j = f_a(E_{j−3}) ⊔ f_b(E_{j−4}) for j ≥ 4.
- Iterate along the prefixes of v. f_v(z) = (2^(Q_v) z − D_v)/3^(P_v) ≡ f_v(0) + 2^(Q_v)·3^(−P_v)·z (mod 2^K). Write f_v(0) mod 2^K = r_v + 2^(Q_v)τ_v.
- Since K−m ≥ Q_v, c = r_v + 2^(Q_v)·y < 2^(K−m) iff y < 2^(κ_v−m). ∎

### Lemma 2 (P spreads) — PROVED

For q ≥ 80 let M(q,i) be the number of words with Q = q and P = P_0(q) − i, and W_q = Σ_i M(q,i). For every D ≥ 1 and every residue ϖ:

Σ_{i≡ϖ (D)} M(q,i) ≤ W_q/D + 3·max_i M(q,i) ≤ W_q·(1/D + 3c₁/√q), with c₁ = 6.5.

Proof.
- Solutions of 3A+4B = q are (A_0+4i, B_0−3i), with P = P_0 − i and M = C(A+B, A).
- φ(t) = lnΓ(A_0+B_0+t+1) − lnΓ(A_0+4t+1) − lnΓ(B_0−3t+1) has φ″ = ψ′(A+B+1) − 16ψ′(A+1) − 9ψ′(B+1) < 0, since ψ′ is positive and decreasing. So i ↦ M(q,i) is log-concave, hence unimodal.
- For a unimodal sequence, each progression term at distance ≥ D from the peak is at most the mean of a block of D consecutive terms towards the peak. These blocks are disjoint except possibly at the peak, and at most 2 terms are uncovered.
- M(q,i)·x^q = C(A+B,A)(x³)^A(x⁴)^B is a binomial probability with N = A+B ≥ q/4 ≥ 20 trials and p = x³ = 0.5497. By Robbins' Stirling bounds the modal probability is ≤ e^(1/12N)·√(N/(2πj(N−j))) ≤ 0.9/√N, because the mode has j ≥ 0.4997N and N−j ≥ 0.4003N. So M·x^q ≤ 1.8/√q.
- U_q = W_q·x^q satisfies U_q = x³U_{q−3} + x⁴U_{q−4}, a convex combination. So inf_{q≥60} U_q = min(U_60..U_63) = 0.2897, and c₁ = 1.8/0.2897 < 6.5. ∎

Measured: max M√q/W_q = 5.14 over 80 ≤ q < 3000.

### Lemma 3 (Parseval on ⟨3⟩) — PROVED

Let κ ≥ 3, G = ⟨3⟩ ⊂ (Z/2^κ)^× (order 2^(κ−2)), h ≠ 0, e = v₂(h). Then (1/|G|)·Σ_{λ∈G} |T_κ(hλ)| ≤ 2^(1+e/2)·√N_κ.

Proof. λ ↦ hλ mod 2^κ has fibres of size ≤ 2^e on G, so Σ_G |T_κ(hλ)|² ≤ 2^e·Σ_{ξ mod 2^κ}|T_κ(ξ)|² = 2^e·2^κ·N_κ. Divide by 2^(κ−2) and apply Cauchy–Schwarz. ∎

Measured: the left side is about 0.35 of the right side for κ = 12, 16, 20 and h ≤ 64, so the lemma is sharp up to a factor 3.

### Lemma 4 (windows) — PROVED

Let a_h be the Fourier coefficients on Z/2^κ of the indicator of [0, 2^(κ−m)), and F_κ(λ) := Σ_{h≢0} |a_h|·|T_κ(hλ)|. Then for all τ:
- |#{z∈E_κ : (λz+τ) mod 2^κ < 2^(κ−m)} − 2^(−m)N_κ| ≤ F_κ(λ);
- avg_{λ∈G} F_κ(λ) ≤ (4.47+2.37κ)·√N_κ.

Proof. τ only contributes phases. |a_h| ≤ 1/(2|h|) for 0 < |h| ≤ 2^(κ−1). By Lemma 3 the average is at most √N_κ·2·Σ_{h≤2^(κ−1)} 2^(v₂(h)/2)/h ≤ √N_κ·2·Σ_e 2^(−e/2)·(1 + ½ln2·(κ−1)). ∎

### Theorem B — PROVED

For m ≥ 1, k ≥ max(7, m+3), and Q+m−k ≥ 84:

|N(Q,m) − 2^(−m)·N_{Q+m}| ≤ (1 + 3c₁·2^(k−2)/√(Q+m−k−4))·(4.47+2.37k)·N_{Q+m}/√N_{k−3}.

Proof.
- Put K = Q+m. By Lemmas 1 and 4, |N(Q,m) − 2^(−m)N_K| ≤ Σ_v F_{κ_v}(λ_v), because Σ_v N_{κ_v} = N_K exactly.
- Group 𝒱 by (q′ = Q_{v′}, ℓ). There are 7 groups; κ is constant on each, and q′ ≥ n−4 ≥ 80.
- Within a group λ_v = λ_0·3^i with multiplicity M(q′,i), and λ_0 ∈ G. F_κ(λ_0·3^i) depends only on i mod D with D = 2^(κ−2) = |G|, and i mod D runs once over G.
- By Lemma 2, Σ_i M(q′,i)·F_κ(λ_0 3^i) ≤ W_{q′}·(1 + 3c₁D/√q′)·avg_G F_κ.
- Apply Lemma 4 and sum over groups with Σ_groups W_{q′}·N_κ = N_K and N_κ ≥ N_{k−3}. ∎

**Corollary B1 — PROVED.** Take k = ⌊½log₂Q⌋ − 4. For Q ≥ 2^22 and 1 ≤ m ≤ ½log₂Q − 8:

|N(Q,m)/N_{Q+m} − 2^(−m)| ≤ 3.7·log₂Q·Q^(−s/4).

Since N_j·2^(−sj) → const (roots of z⁴ = z+1 have moduli 1.2207 = 2^s, 1.063, 1.063, 0.724), N(Q,m)/N(Q,0) → 2^(−(1−s)m) for every fixed m, and uniformly while 2^m = o(Q^(s/4)/log Q).

This answers seed (b): there is no finite matrix, but the per-bit decay rate is exactly the heuristic one for each fixed m.

**Corollary C (weak FP-0) — PROVED.** With m* = ⌊(s/4)log₂Q − log₂log₂Q⌋:
- N(Q,m) ≤ 8·2^(sQ)·2^(−(1−s)m) for 1 ≤ m ≤ m*;
- N(Q,Q) ≤ N(Q,m*) ≤ 13·(log₂Q)^(1−s)·Q^(−s(1−s)/4)·2^(sQ).

This uses 1.2·2^(sj) ≤ N_j ≤ 1.64·2^(sj), by the convex-combination recursion for N_j·2^(−sj). With these closed-form constants m* ≥ 1 only for Q ≥ 2^110; the numerical constants are hand arithmetic (CANDIDATE).

**Seeds.** #{w ≤ X : w ∈ E} ≤ C·X^s·(log log X)^0.72·(log X)^(−0.0512). The same bound holds for H1 seeds, which form a subset. The exponent 0.2878 is unchanged. Theorem 57(T1) is a lower bound at lives ≤ log₂B; the new saving is at lives ≥ log₂B + m and is only a power of log B.

**Concrete evaluation — VERIFIED (floating-point evaluation of the proved inequality N(Q,m) ≤ Σ_v sup_τ window count; `f6_concrete.py`).**

| Q | m | k | bound on N(Q,m)/N_Q | heuristic |
|---|---|---|---|---|
| 10⁴ | 1 | 8 | 0.936 | 0.610 |
| 10⁵ | 1 | 10 | 0.881 | 0.610 |
| 10⁶ | 2 | 12 | 0.695 | 0.373 |
| 10⁸ | 3 | 16 | 0.486 | 0.227 |
| 10⁸ | 4 | 16 | 0.413 | 0.139 |

### Theorem A — PROVED

For K ≥ 2^22 and every integer h ≠ 0: |T_K(h)| ≤ 6.2·2^(v₂(h)/2)·K^(−s/4)·N_K.

Proof. Lemma 1, the triangle inequality, Lemma 2 and Lemma 3, with k = ⌊½log₂K⌋ − 4. ∎

Some dependence on v₂(h) is necessary: T_K(2^(K−j)·h′) depends only on E_j.

### Proposition D (reduction) — implication PROVED, hypothesis OPEN

**(SGP).** There are δ₀ > 0, β ∈ (0,1) and C such that for all k, all R ≥ √(k/β), and all ξ ≢ 0 mod 2^k:

(1/R)·Σ_{i<R} |T_k(ξ·3^i)| ≤ C·2^(v₂(ξ)/2)·N_k^(1−δ₀).

Then FP-0 holds with δ ≥ (1−s)·s·δ₀·β/2.

Proof (same chain as Theorem B).
- Take k = ⌊βK⌋ and cut each group's i-range into windows of length R ≍ √K.
- Σ_windows max M ≤ W/R + 2·max M ≤ C′·W/R by Lemma 2.
- So Σ_v |T_κ(hλ_v)| ≤ C″·2^(v₂(h)/2)·N_K·N_κ^(−δ₀), and N(Q,m) ≤ N_K·(2^(−m) + C‴·K·N_k^(−δ₀)).
- Take m = ⌊sδ₀βK/2⌋. ∎

Status of (SGP): proved for R ≥ 2^(k−2) with δ₀ = ½ (Lemma 3); needed for R ≈ √k. This is the exact form of the Erdős-regime obstruction: the orbit 3^i mod 2^k over only √k steps.

VERIFIED numerically (`f5_sgp.py`, log₂ of the average and maximum of |T_k|/N_k over the progression):

| k | h | R | log₂ avg | log₂ max | √ benchmark |
|---|---|---|---|---|---|
| 100 | 1 | 10 | −16.6 | −15.5 | −14.6 |
| 200 | 1 | 15 | −30.9 | −28.5 | −29.0 |
| 400 | 1 | 20 | −59.9 | −58.4 | −57.8 |
| 400 | 6 | 20 | −59.7 | −58.3 | −57.8 |
| 800 | 1 | 29 | −116.3 | −113.5 | −115.3 |
| 800 (5n+1) | 1 | 29 | −118.5 | −116.2 | −115.3 |
| 1600 | 1 | 40 | −235.6 | −231.9 | −230.4 |

### Proposition E (O(K²) Fourier sums) — identity PROVED; checked against direct sums at K = 30, 37

G(P,k) := T_k(h·3^(−P) mod 2^k) satisfies G(P,k) = e(−h·3^(−(P+2))/2^k)·G(P+2,k−3) + G(P+3,k−4) for k ≥ 4, and T_K(h) = G(0,K).

log₂(|T_K(h)|/N_K) from `f3_dp.py`:

| K | h=1 | h=3 | h=5 | h=2 | h=11 | h=1001 | √ benchmark |
|---|---|---|---|---|---|---|---|
| 100 | −16.4 | −18.9 | −15.6 | −16.3 | −14.3 | −14.8 | −14.6 |
| 200 | −31.6 | −30.8 | −35.0 | −30.5 | −31.1 | −32.7 | −29.0 |
| 800 | −122.9 | −118.3 | −116.6 | −119.8 | −122.1 | −120.3 | −115.3 |
| 1600 | −238.0 | −239.2 | −239.7 | −239.9 | −242.2 | −239.8 | −230.4 |
| 3200 | −471.3 | −470.4 | −471.0 | −470.6 | −469.3 | −483.0 | −460.6 |

Controls at K = 800: 5n+1 gives −116.2, −121.7, −115.5, −115.0, −116.1, −123.5; 3n−1 gives the same moduli as 3n+1 (complex conjugates).

### Data: N(Q,m) — VERIFIED (exact, `f1_count.c`)

Q = 104, N_Q = 1,340,341,377:

| m | N(Q,m) | N(Q,m)/N(Q,0) | 2^(−(1−s)m) | quotient |
|---|---|---|---|---|
| 1 | 818,123,612 | 0.6104 | 0.6104 | 1.000 |
| 4 | 186,045,849 | 0.1388 | 0.1388 | 1.000 |
| 8 | 25,818,422 | 1.926e−2 | 1.926e−2 | 1.000 |
| 16 | 498,136 | 3.716e−4 | 3.711e−4 | 1.001 |
| 24 | 9,392 | 7.007e−6 | 7.149e−6 | 0.980 |
| 32 | 172 | 1.283e−7 | 1.377e−7 | 0.932 |
| 40 | 3 | 2.24e−9 | 2.65e−9 | 0.84 |
| 41–45 | 2 | | | |
| ≥ 46 | 1 (w = 0) | | | |

Q = 112, N_Q = 6,610,168,495: N(Q,m) = 4,034,658,915; 917,476,591; 127,331,043; 2,452,858; 47,043; 969; 19 at m = 1, 4, 8, 16, 24, 32, 40. It is 2 for m = 48..51 and 1 from m = 52.

- First m with N(Q,m) = 1: 28, 38, 46, 52 for Q = 64, 96, 104, 112, against the prediction sQ/(1−s) = 0.404·Q.
- Longest finite life of a positive w < 2^Q: 35, 42, 54, 69, 75, 91, 106, 112, 129, 133, 149, 163 bits for Q = 24, 32, …, 112 (life/Q between 1.31 and 1.46; heuristic 1.404).
- For every Q from 9 to 66 the longest finite life is below 2Q, so N(Q,Q) = 1. For Q = 6, 7, 8 it is 16 (w = 63 → 71 → 80 → 135 → 152), so N(Q,Q) = 2.
- Controls at Q = 96: 5n+1 matches the 3n+1 table within noise (saturates at 1 from m = 38). 3n−1 has two infinite points (0 and 1) and saturates at 2.
- The Q = 120 run was stopped unfinished to stay in budget.

## (c) Scripts

All in `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/w3-fp0/`, with PY = `/home/matrix/home/projects/collatz/venv/bin/python`.

- `f1_count.c`: build with `gcc -O2 -fopenmp -o f1_count f1_count.c`; run `OMP_NUM_THREADS=2 taskset -c 6-7 ./f1_count Q [3|5] [1|-1]`. Prints `Q m N(Q,m)`. Exact (128-bit enumeration, 256-bit orbit). Agrees with brute-force Python at Q = 8, 12, 20 for all three systems. Outputs are `out_3p1_Q*.txt`, `out_5p1_Q96.txt`, `out_3m1_Q96.txt`.
- `$PY f2_check.py [3|5] [1|-1] [kmax]`: checks the E_k recursion against the definition (k ≤ 16), the constants of Lemma 2, and Lemma 3; prints the exact table of avg_λ sup_τ window counts.
- `$PY f3_dp.py K h1,h2,… [mult d]`: Proposition E. Output in `out_dp.txt`.
- `$PY f4_chain.py K m k [mult d]`: checks every inequality of Theorem B's proof on exact data; last line should be `chain OK`. Passed for (44,3,12), (50,4,14), (47,2,9), (52,5,16) and the controls (44,3,12,5,1), (44,3,12,3,−1).
- `$PY f5_sgp.py k h R [mult d]`: the (SGP) table. Output in `out_sgp.txt`.
- `$PY f6_concrete.py log10Q m k`: the concrete bounds. Do not use Q ≥ 10^10; memory grows like Q/4 array entries.

## (d) Brainstorm, kill tests, dead ends

| # | Idea | Kill test | Outcome |
|---|---|---|---|
| 1 | Tail block, average over the multiplier 3^(−P) | is P equidistributed mod 2^k? | PROVED for 2^k ≪ √Q (Theorems A, B). Stops there: P spreads over only √Q values |
| 2 | Head block, 3-adic side: phases θ(p,k) = (2^(−k) mod 3^p)/3^p | take K ≡ 0 mod 2·3^(L−1) | DEAD uniformly in K: then θ = 2^q/3^p is a real number tending to 0 and the head phases are e(hγ(v)), a constant-factor saving only. The head is rigid because the level is fixed 2-adically. Derived by hand, not machine-checked |
| 3 | Finite-state transducer for w′ mod 2^m (seed b) | does one step close up mod 2^m? | DEAD: forward needs 3 more bits, backward needs all higher trits. Superseded by Corollary B1 |
| 4 | Large sieve / second moment over all ξ mod 2^m (seed a as posed) | what is Σ_ξ |S(ξ)|²? | CIRCULAR: equals 2^m × the collision count of w′_u mod 2^m, which is the unknown; L² → L^∞ also halves the exponent |
| 5 | ab/ba Riesz pairing in mid-word | where is |1+e(11hX)| small? | OBSTRUCTION: X is a ternary window of 2^(−k) mod 3^p with k ≍ p (ledger 19). Only a fixed (1−c) at the first pair is provable, useless after summing over h |
| 6 | Multi-block induction | P-spread seen from a block at distance t from the end | DEAD: needs spread ≥ 2^t, available √K. This is (SGP) |
| 7 | Iterate a constant-factor saving along the extra bits | are survivors a product set (head × tail)? | DEAD: once m > s·q at most one head survives per tail |
| 8 | Size / degrees of freedom of the mirror endpoint (seed d) | does orbit size constrain anything? | DEAD: a and b both increase w; pair counting is the heuristic, not a proof |
| 9 | Theorem 57 complement (seed c) | regimes | CONSISTENT, as stated under Corollary C |
| 10 | Averaging over Q via idea 2 | — | NOT PURSUED: log-power savings for generic Q only |
| 11 | Congruence invariants of endpoints | ledger 10 | DEAD: only mod 11 |

Hostile self-review.
- All inequalities of Theorem B's proof were evaluated on exact data for three systems (`f4_chain.py`); all hold.
- The true discrepancy |N(Q,m) − 2^(−m)N_K| was 3–12 at N(Q,m) ≈ 10³, far below the proved bound.
- The argument takes a supremum over translations τ, so it is of the translate-invariant type that Theorem 48 shows cannot give emptiness. There is no conflict: the bound is never below 2^(−m)N_{Q+m}.
- Litmus. For −E, T is conjugated and nothing else changes; N ≥ 2 always. For 5n+1, ⟨5⟩ also has order 2^(κ−2). For a multiplier whose group has order 2^(κ−c) the constant grows by 2^(c/2). The constant 3 enters only through that order.
- A bug was caught during review: `f6_concrete.py` first used a wrong 10th digit of s, giving bounds below the truth at Q = 10⁸. It was fixed with a 17-digit s and a normalisation assert. `f2_check.py` still uses s = 0.28776081, which is harmless at k ≤ 64.
- No literature search was done; Theorems A/B may be known in a Lagarias-type setting.

## (e) Best lead

**Lemma SGP (open).** There is δ₀ > 0 such that for all large k, all odd ξ and R = ⌈√k⌉: Σ_{i<R} |T_k(ξ·3^i)| ≤ R·N_k^(1−δ₀).

- It implies FP-0 (Proposition D) and is true or false simultaneously for E, −E and the 5n+1 set.
- It is proved for R = 2^(k−2). A proof for R = 2^(k^(1−c)) would already extend Theorem B to m ≤ Q^(c′), a saving of exp(−(log X)^(c′)).
- T_k is computable in O(k²) (Proposition E), so any refinement can be tested cheaply. Numerically δ₀ ≈ ½ up to k = 1600.

**Credences**

| Claim | Credence |
|---|---|
| Theorem B and Lemmas 1–4 (unspecified constants) | 93% |
| Theorem A | 93% |
| Explicit constants as stated | 75% |
| Proposition D implication | 85% |
| (SGP) true | 85% |
| FP-0 true | 92% |
| FP-0 provable with present tools | 5% |
| Theorems A/B new to the literature | 50% |
| This family yields H1 | < 1% |