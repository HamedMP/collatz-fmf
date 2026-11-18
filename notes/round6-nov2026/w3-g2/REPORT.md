<!-- Saved by the coordinator from the w3-g2 agent's final message (the agent's own write was refused). -->
# FULL REPORT (intended `w3-g2/REPORT.md`)

Date: 2026-11-18. Labels: PROVED (full proof below; external inputs named), VERIFIED (finite, by the stated script), CANDIDATE, REFUTED. Nothing here was refereed by anyone but me. Constants c, C are absolute and not explicit.

Notation. T(x) = x/2 or (3x+1)/2. θ0 = log 2/log 3 = 0.63093, λ = θ0/(1−θ0) = 1.70951, η = H2(θ0) = 0.9499555, 1−η = 0.0500445. V(L,a) = vectors v ∈ {0,1}^L with a ones; y_v = the integer of [2^L, 2^(L+1)) with parity vector v; z_v = T^L(y_v) = 3^a + τ_v (Proposition I of w2-delta). a_j(y) = number of odd terms among y, …, T^(j−1)y.

## (a) Summary

1. G2 is not proved. One weaker saving is proved, one elementary sharpening of Theorem S is proved, and the power-saving statement is reduced to one named estimate (E_exp) with numerical support.
2. Data (VERIFIED to X = 2^38): the generation counts E_λ(2^L) agree with the "independent generations" random-walk model to within 0.02 % for λ ≤ 3 at L = 30–38. The model gives exponent 1 − λ(1−η) times (log X)^(−3/2); for λ = 2 that is 0.8999 < η.
3. Theorem W (PROVED given two published inputs): equidistribution of the low m binary digits of z_v at the critical pinning, error C·exp(−c·log a/log log a).
4. Corollary N (PROVED from W): the (L+m)-step non-descent count is ≤ C·λ^(sθ0)·m·2^(−(1−η)m)·2^(ηL)/√L for s+2 ≤ m ≤ c·log L/log log L. The model value is ≍ 2^(−(1−η)m)·2^(ηL)/√L, so this is sharp up to the factor m. It is not a power saving.
5. Theorem S+ (PROVED given a ballot inequality): sojourn count ≤ C·X^η·(log X)^(−0.986)·log log X.
6. Corollary N does not improve the sojourn bound beyond S+. Theorem H's constants are unchanged.
7. The power saving is out of reach because the required tilt is the critical one: the renewal walk of Tao's Section 7 runs parallel to the hypotenuse of his black triangles. That is the boundary q* excluded in `proof.md` Theorem 56. Only a 2-adic Baker bound limits triangle size, and it loses log² n per scale.
8. Reduction (PROVED implication): E_exp ⇒ G2 with λ = 1+κ.
9. Litmus: W, N, S+ hold for 3n−1; they say nothing about cycles; for 5n+1 every saving disappears.
10. Credences in (h); best lead in (f).

## (b) Statements and proofs

### B0. Three exact identities — PROVED, VERIFIED on 32,751 vectors (`g4_identities.py`)

Let v ∈ V(L,a), a ≥ 1, with ones at d_0 < … < d_(a−1). Put α_1 = L − d_(a−1), α_j = d_(a−j+1) − d_(a−j) for 2 ≤ j ≤ a, and α_(a+1) = d_0 + 1. All α_j ≥ 1 and they sum to L+1.

- **(I1)** v ↦ (α_1, …, α_(a+1)) is a bijection from V(L,a) onto compositions of L+1 into a+1 positive parts.
- **(I2)** τ_v ≡ Σ_{j=1..a} 3^(j−1)·2^(−α_[1,j]) (mod 3^a), with α_[1,j] = α_1+…+α_j. This is Lemma 1 of w2-delta re-indexed, i.e. Tao's F_a in the ordering of his Section 7.
- **(I3)** For m ≥ 0 let σ ∈ [0,3^a) be the residue of τ_v·2^(−m) mod 3^a and c = ⌊2^m·σ/3^a⌋. Then 2^m·σ = τ_v + c·3^a, 0 ≤ c < 2^m, and z_v ≡ (1−c)·3^a (mod 2^m).
  Proof: 2^m·σ ≡ τ_v mod 3^a and 0 ≤ τ_v < 3^a give the first claim; then z_v = 3^a + τ_v = (1−c)·3^a + 2^m·σ. ∎

So the low m binary digits of z_v are the top m binary digits of σ/3^a, where σ is the Syracuse residue with its first valuation lengthened by m. G2 concerns the archimedean position of a 3-adically defined point.

### B1. External inputs

- **(T) Tao, arXiv:1909.03562, Lemma 7.4 (structure of the black set).** Read in full in `nd-referee/tao-src/collatz.tex`, lines 1196–1363. Fix n, an integer ξ not divisible by 3, and a small absolute ε > 0. Let θ(j,l) be the signed fractional part of ξ·9^(j−1)·(2^(−l+1) mod 3^n)/3^n; (j,l) ∈ [n/2]×Z is black if |θ| ≤ ε. The black set is a disjoint union of triangles Δ = {j ≥ j_Δ, l ≤ l_Δ, (j−j_Δ)·log 9 + (l_Δ−l)·log 2 ≤ s_Δ} with |θ(j_Δ,l_Δ)| = ε·e^(−s_Δ). Every point of [n/2]×Z outside Δ at distance ≤ D := (1/10)·log(1/ε) from Δ is white. The lemma is deterministic and independent of the law of the valuations.
- **(P) Linear forms in two 2-adic logarithms.** For nonzero integers ρ, t and ν ≥ 1 with ρ + t·3^ν ≠ 0: v_2(ρ + t·3^ν) ≤ C0·log(2 + max(|ρ|,|t|))·log²(ν+2). Source: Bugeaud–Laurent, J. Number Theory 61 (1996), Théorème 3, or Yu's theorems. I quote this from memory and could not retrieve the text this session. Reduction to their hypotheses: remove the common power of 2 from ρ, t (if the valuations differ the claim is trivial); then v_2 = v_2(3^ν − β) with β = −ρ/t a 2-adic unit of height log max(|ρ|,|t|); pass to squares so that β², 9 ≡ 1 mod 8; if β and 3 are multiplicatively dependent then β = ±3^k and v_2(3^e ∓ 1) ≤ 2 + log2 e directly. This is the one dependency a referee must check against the printed statement.
- **(ET) Erdős–Turán.** For a finite multiset in R/Z with Fourier coefficients μ^(h): sup over intervals |μ(I) − |I|| ≤ C/H + C·Σ_{h=1..H} |μ^(h)|/h.
- **(LLT)** For S_M a sum of M i.i.d. Geom(q) variables (P(α=k) = q(1−q)^(k−1)), q in a compact subset of (0,1): max_x P(S_M = x) ≤ C/√M, and P(S_M = x) ≥ c/√M for |x − M/q| ≤ 1.
- **(Bern)** Bernstein's maximal inequality for i.i.d. sums with exponential tails.

### B2. Theorem W (equidistribution at the critical pinning) — PROVED given (T), (P); not refereed

**Statement.** There are absolute c, C > 0 such that for all a ≥ 3, all L with |L − a·log2 3| ≤ √a, all 0 ≤ m ≤ √a and all residues r mod 2^m:

| #{v ∈ V(L,a) : z_v ≡ r mod 2^m} / C(L,a) − 2^(−m) | ≤ C·exp(−c·log a/log log a) =: C·Ψ(a).

**Proof.** Assume a ≥ a0; smaller a go into C. Let v be uniform on V(L,a).

*Step 1 (to an interval discrepancy).* By (I3) the law of z_v mod 2^m is the image, under a bijection of Z/2^m, of the law of c, and P(c = c0) = μ([c0/2^m, (c0+1)/2^m)) where μ is the law of σ/3^a on R/Z. By (ET) it suffices to show |μ^(h)| ≤ C·Ψ0(a) for 1 ≤ h ≤ H, where Ψ0(a) = exp(−c3·log a/log log a) and H = ⌈1/Ψ0⌉ (so log H ≤ √a). Then the discrepancy is ≤ C·Ψ0·log(1/Ψ0) ≤ C·Ψ.

*Step 2 (Tao's pairing under the pinned measure).* Write h = 3^i·h′ with 3 ∤ h′; then i ≤ log3 H and n := a − i ≥ a/2. By (I2), e(h·σ/3^a) = e(h′·X/3^n) with X ≡ Σ_{j=1..n} 3^(j−1)·2^(−α_[1,j]−m) mod 3^n. Put b_j = α_(2j−1) + α_(2j) for j ≤ ⌊n/2⌋ and let G be generated by all b_j and all α_i with i > 2⌊n/2⌋. By (I1) the law of (α_i) is uniform on compositions, so given G the pairs are independent and α_(2j) is uniform on {1,…,b_j −1}. The two terms of pair j are 3^(2j−2)·2^(−b_[1,j]−m)·(2^(α_2j) + 3); all other terms are G-measurable. Hence |E[e(h′X/3^n) | G]| = Π_j |f_j| with |f_j| ≤ 1 and, when b_j = 3, |f_j| = |cos(π·θ(j, m + b_[1,j]))| with θ as in (T) for ξ = h′. (Checked numerically in `g4_identities.py`, second part.) With cos(πx) ≤ exp(−x²):

|μ^(h)| ≤ E exp(−ε²·W), W = #{j ≤ ⌊n/2⌋ : b_j = 3 and (j, m + b_[1,j]) white}.

The pinning Σα = L+1 costs nothing here because it is G-measurable.

*Step 3 (to i.i.d. variables).* Define q by 1/q = (L+1)/(a+1); then |1/q − log2 3| ≤ 2/√a and q ∈ [0.55, 0.72]. The uniform composition law is i.i.d. Geom(q) conditioned on S_(a+1) = L+1. Let N = 2⌊a/4⌋. For any g ≥ 0 depending only on α_1..α_N, E_unif g ≤ E_iid g · max_x P(S_(a+1−N) = x)/P(S_(a+1) = L+1) ≤ C·E_iid g by (LLT). Apply this to g = exp(−ε²·W_N), where W_N ≤ W is the count over j ≤ N/2. From here the α_i are i.i.d. Geom(q). The b_j are i.i.d. with P(b > r) = (1−q)^(r−1)(1−q+rq), and p3 := P(b = 3) = 2q²(1−q) ≥ 0.27.

*Step 4 (band).* Let P_j = (j, m + b_[1,j]) and d(j,l) = l·log 2 − j·log 9. The increments of d(P_j) have mean 2·log 2·(1/q − log2 3), of size ≤ 3/√a. With Y = √a·log a and Y1 = Y + m·log 2, (Bern) gives P(G^c) ≤ exp(−c·log² a), where G = {|d(P_j)| ≤ Y1 for all j ≤ N/2}.

*Step 5 (Lemma X: near the diagonal, triangles are short).* Let Δ be a triangle of (T) for (n, h′) with l_Δ ≥ 2 + log2 H that contains a point with d ≤ Y1. Then every point (j,l) of Δ with d ≥ −Y1 has j ≤ C1·(j_Δ + Y1 + log H + 1)·log²(n+2).

Proof. θ(j_Δ,l_Δ) = M/3^n with M ≡ h′·9^(j_Δ−1)·2^(−λ′) mod 3^n, λ′ := l_Δ − 1 ≥ 1, |M| = ε·e^(−s_Δ)·3^n. M ≠ 0 because 2j_Δ − 2 < n and 3 ∤ h′. So M·2^λ′ = h′·9^(j_Δ−1) + t·3^n for an integer t. If t = 0 then 2^λ′ | h′, so l_Δ ≤ 1 + log2 H, which is excluded. Otherwise |t| ≤ ε·e^(−s_Δ)·2^λ′ + H, and dividing by 9^(j_Δ−1): 2^λ′ divides h′ + t·3^ν with ν = n − 2j_Δ + 2 ≥ 2 and h′ + t·3^ν ≠ 0. By (P), λ′ ≤ C0·log(2 + H + ε·e^(−s_Δ)·2^λ′)·log²(n+2). Now e^(−s_Δ)·2^λ′ = ½·exp(h_Δ + j_Δ·log 9), where h_Δ := d(j_Δ,l_Δ) − s_Δ. The defining inequality of Δ says exactly d ≥ h_Δ on Δ, so h_Δ ≤ Y1. Hence λ′ ≤ C0·(Y1 + j_Δ·log 9 + log(2+H) + 1)·log²(n+2). Finally a point of Δ with d ≥ −Y1 has j·log 9 ≤ l·log 2 + Y1 ≤ (λ′+1)·log 2 + Y1. ∎

*Step 6 (one white renewal point per epoch, with probability ≥ p\*).* Fix x0 with ψ(x0) := (1−q)^x0·(1 + x0·q/(1−q)) ≤ 1/2 for all q ∈ [0.55,0.72]. Then fix ε so small that D ≥ x0 + 5 and (T) applies. Let J_0 = ⌈Y1 + log2 H⌉ + 10 and J_(k+1) = ⌈4·C1·log²(n+2)⌉·J_k for k < K := max{k : J_k ≤ N/2}; then K ≥ c·log a/log log a. Let X_k = 1 if some j ∈ (J_k, J_(k+1)) has b_j = 3 and P_j white. Let R_k = 1 if the exit described below has not happened by time J_(k+1) − 2.

Claim: P(X_k = 1 or R_k = 1 | α_1..α_(2J_k)) ≥ p\* := p3²/2.

Given the past, Q := P_(J_k) is fixed. If Q is white, let Q′ = Q + (1,3); with probability p3, b_(J_k+1) = 3 and the walk is at Q′. If Q′ is white, X_k = 1. Otherwise (Q black, or Q′ black after that step) the walk sits in a triangle Δ with j_Δ ≤ J_k + 1 and l_Δ ≥ 2J_k ≥ 2 + log2 H. Let e be the first later time with P_e ∉ Δ.

- *Exit before J_(k+1) − 2 unless R_k = 1.* On G the walk stays in the band, Δ contains a band point, and by Lemma X the band points of Δ have j ≤ C1·(J_k + 2 + Y1 + log H)·log²(n+2) < J_(k+1) − 2.
- *The exit point is close to Δ.* The walk moves right, so P_e ∉ Δ means l_e > l_Δ ("top") or d(P_e) < h_Δ ("floor").
  - Floor: one step changes d by b·log 2 − log 9 ≥ −0.811. Then (j_e, l_e + 2) ∈ Δ if l_e + 2 ≤ l_Δ; otherwise (j_(e−1), l_Δ) ∈ Δ is within distance 2.
  - Top with overshoot l_e − l_Δ ≤ x0: (j_(e−1), l_Δ) ∈ Δ, because columns of Δ are intervals ending at l_Δ; distance ≤ x0 + 1.
  - Top with overshoot > x0 has probability ≤ ψ(x0) ≤ 1/2. Summing over the step i at which it happens: P(b > r + x0) ≤ ψ(x0)·P(b > r) with r = l_Δ − l_(i−1) ≥ 0, and {b_i > r} forces exit at step i, so the sum is ≤ ψ(x0)·P(exit).
- *One more step.* Given a close exit at e, b_(e+1) = 3 has probability p3 independently of the past. Then P_(e+1) = P_e + (1,3) is not in Δ (l increased; d decreased by log 9 − 3·log 2 > 0), is within x0 + 5 ≤ D of Δ, and lies in [n/2]×Z. So it is white by (T), and b = 3 there, so X_k = 1.

Altogether P(X_k ∨ R_k) ≥ p3·(p3·(1 − ψ(x0))) ≥ p3²/2; the case "Q black" has the better bound p3/2. ∎

X_k ∨ R_k is determined by the steps before J_(k+1), so by successive conditioning E exp(−ε²·Σ_k (X_k ∨ R_k)) ≤ (1 − p\*·(1−e^(−ε²)))^K. On G all R_k = 0 and W_N ≥ Σ X_k. Therefore

E_iid exp(−ε²·W_N) ≤ (1 − p\*(1−e^(−ε²)))^K + P(G^c) ≤ exp(−c3·log a/log log a) = Ψ0(a).

Steps 2–6 give |μ^(h)| ≤ C·Ψ0(a) for all 1 ≤ h ≤ H, and Step 1 finishes. ∎

Remarks.
- The rate comes from Lemma X: a triangle starting at j_Δ may run to j_Δ·log² n, so there are only log n/log log n scales and that many guaranteed exits. Tao gets n^(−A) because his walk has slope 4 > log2 9 and leaves every triangle through the top after at most 79 % of the remaining strip.
- Replacing (P) by an abc-strength bound gives "any constant number of exits", still no power of n.
- Numerically the truth is far better: on pinned paths about 90 % of renewal points are white at ε = 0.05 (`g5_white.py`, a up to 2000), i.e. W grows linearly in a.

### B3. Corollary N (count beyond the Terras horizon) — PROVED from Theorem W

**Statement.** There are c′, C such that for L ≥ 3, s ≥ 0 and s+2 ≤ m ≤ c′·log L/log log L,

N(L,m,s) := #{y ∈ [2^L, 2^(L+1)) : T^(L+m)(y) > y/2^s} ≤ C·λ^(sθ0)·m·2^(−(1−η)m)·2^(ηL)/√L.

**Proof.** Let A = a_(L+m)(y) = a + w, where a = a(v) and w is the number of odd terms among the first m iterates of z_v (a function of z_v mod 2^m by Terras). By Lemma 1 of w2-delta, T^(L+m)(y) < (3^A·y/2^(L+m))·(1 + 2^(m−A)). If A < m the right side is ≤ 2·(3/2)^m·y/2^L ≤ y/2^s for L ≥ s+1+m. So a bad y has 2·3^A > 2^(L+m−s), i.e. w > θ0·m − κ − (s+1)·θ0 where a = θ0·L + κ.

- κ > m: at most Σ_{a > θ0L+m} C(L,a) ≤ C·2^(ηL)·L^(−1/2)·λ^(−m), using C(L,a) ≤ C·L^(−1/2)·2^(L·H2(a/L)) and concavity, L·H2(a/L) ≤ ηL − κ·log2 λ.
- κ < −m: needs w > m once m ≥ s+2. Empty.
- |κ| ≤ m: here |L − a·log2 3| ≤ 1.6m ≤ √a, so Theorem W applies to every class: P_a(w > t) ≤ 2^(−m)·#{u ∈ {0,1}^m : |u| > t} + 2^m·C·Ψ(a). By the Chernoff bound (blind-H L3) and (1+λ)·λ^(−θ0) = 2^η, 2^(−m)·#{|u| ≥ t} ≤ λ^(−t)·((1+λ)/2)^m = λ^(κ+(s+1)θ0)·2^(−(1−η)m) at t = θ0·m − κ − (s+1)θ0. Multiplying by C(L,a) ≤ C·2^(ηL)·L^(−1/2)·λ^(−κ) and summing over the ≤ 2m+1 values of a gives ≤ C·2^(ηL)·L^(−1/2)·(2m+1)·[λ^((s+1)θ0)·2^(−(1−η)m) + (2λ)^m·Ψ(L/2)].

Choose c′ so that (2λ)^m·Ψ(L/2) ≤ 2^(−m) in the stated range. ∎

Reading: among the ≍ 2^(ηL)/√L integers of a dyadic block that have not descended after L steps, the proportion still not descended (in the end-point sense) after L+m steps is ≤ C·m·2^(−0.05m), for m up to c·log L/log log L. With m maximal the saving is exp(−c·log log X/log log log X).

Exact check (`g9_corN.py`): N(L,m,s) against the independence prediction at L = 20, 24, s ∈ {0,3}, m ≤ 16: ratios 0.986–1.001.

### B4. Theorem S+ (sojourn bound with a log power) — PROVED given the ballot inequality (BAL)

**(BAL)** Let S_j = a_j·log2 3 − j for a vector with i.i.d. Bernoulli(θ0) bits (mean-zero walk, steps +0.585 and −1). Then P(min_{j≤L} S_j > −u and S_L + u ∈ [h, h+1)) ≤ C·(u+1)·(h+1)/L^(3/2) for all u, h ≥ 0. This is the standard ballot theorem for centred finite-variance walks (Addario-Berry–Reed 2008; the (u+1)(h+1) form is e.g. Aïdékon–Shi 2014, Lemma 2.4). Quoted from memory, not re-proved. VERIFIED consequence in exact integers for L ≤ 2400, s ≤ 20: B_L(s)·L^(3/2)/((s+2)·λ^(θ0(s+1))·2^(ηL)) ≤ 15.5 (`g6_ballot.py`).

**Statement.** With ω = 3/2 − θ0·log2 λ/η = 0.98621: every pairwise distinct stretch of a T-trajectory satisfies #{k : x_k ≤ X} ≤ C·X^η·(log X)^(−ω)·log log X for X ≥ 16.

**Proof.** Call x ∈ [2^L, 2^(L+1)) *s-good* if 2·3^(a_j) ≤ 2^(j−s) for some j ≤ L. Then T^j(x) ≤ x/2^s, because T^j(x) < 3^(a_j)·x/2^j + (3/2)^(a_j) ≤ 2·3^(a_j)·x/2^j for j ≤ L. The s-bad vectors are those with S_j > −(s+1) for all j ≤ L. Each v has 2^(−ηL)·λ^(θ0·S_L) times its Bernoulli(θ0) mass, so by (BAL)

B_L(s) = 2^(ηL)·E[λ^(−θ0·S_L); min S_j > −(s+1)] ≤ C·(s+2)·λ^(θ0(s+1))·2^(ηL)·L^(−3/2).

Let N_L be the number of indices with x_k < 2^(L+1). An s-good index k of level L, with first good time j and k+j < K, is charged to t = k+j. Then x_t ≤ 2^(L+1−s), and at most L indices of level L are charged to one t (k ∈ [t−L, t)). Indices with k+j ≥ K number at most L. So

N_L ≤ N_(L−1) + L·N_(L−s) + B_L(s) + L.

Take s = s(L) = ⌈log2(10L)/η⌉, so L·2^(−ηs) ≤ 1/10 and λ^(θ0·s) ≤ λ^θ0·(10L)^(0.51379). With g(L) = L^(−ω)·log(L+2), induct on N_L ≤ A·2^(ηL)·g(L): the first two terms are ≤ A·2^(ηL)·g(L)·(2^(−η)·g(L−1)/g(L) + 0.1·g(L−s)/g(L)) ≤ 0.77·A·2^(ηL)·g(L) for L ≥ L0, and B_L + L ≤ C·2^(ηL)·g(L). Take A ≥ C/0.23 and large enough for L < L0. ∎

Caveat (VERIFIED, `g6_ballot.py`): B_L(s(L))/(2^(ηL)·L^(−1/2)) is 19, 31, 40, 42, 38, 33 at L = 50, 100, 200, 400, 800, 1600. The gain over Theorem S is asymptotic; it starts near L ≈ 400, far above any computed range, and C is not explicit.

### B5. Proposition Rd (reduction of the power saving) — PROVED implication; E_exp itself is CANDIDATE

**E_exp(κ).** There are C and c1 > κ·log2 λ = 0.7736κ such that for all L, with m = ⌊κL⌋ and every a with |a − θ0·L| ≤ κL: Σ_{r mod 2^m} | P_{V(L,a)}(z_v ≡ r) − 2^(−m) | ≤ C·2^(−c1·L).

**Claim.** E_exp(κ) ⇒ G2 with λ_G2 = 1+κ, any γ with 1−γ < min(κ/(2λ), 0.1κ), and δ = min(κ·log2 λ, (1−η)κ − 0.4881·(1−γ), c1 − κ·log2 λ) > 0.

Proof. A survivor has T^(L+m)(y) > 2^(γL), so 3^(a+w) > 2^(γL+m−2). For a ≥ θ0L + κL use the binomial tail (saving λ^(−κL)). For a < θ0L − κL one needs w > m, impossible because (1−γ) < κ/(2λ). In between, as in B3, the count is ≤ C·2^(ηL)·[λ^(θ0(1−γ)L)·2^(−(1−η)κL) + λ^(κL)·2^(−c1·L)]·(2κL+1). ∎

Equivalent Fourier form, via (I3): exponential decay of E_{V(L,a)} e(ρ·σ_v/3^a) for 1 ≤ |ρ| ≤ 2^(κL), the low-frequency characters of the pinned Syracuse residue. Through the pairing majorant this would follow from: on pinned paths a positive proportion of renewal points is white, off an exponentially small event. That needs "ρ·2^(−l) mod 3^ν is small for few (l, ν) near the line l = (n−ν)·log2 3", a statement about ternary digits of 2^(−l) in the Erdős regime (ledger family 19).

Numerical support (VERIFIED, `g3_equi.c`, exhaustive over V(L,a)): TV/√(2^m/(2π·C(L,a))) for a = round(θ0·L)−1, 0, +1:

| L | m = 4 | m = 8 | m = 12 | m = 16 |
|---|---|---|---|---|
| 20 | 0.82, 0.75, 0.55 | 0.98, 1.09, 1.13 | 1.44, 1.45, 1.34 | 1.64, 1.43, 1.30 |
| 24 | 0.58, 0.83, 1.05 | 1.24, 1.32, 1.36 | 1.71, 1.52, 1.33 | 2.06, 1.68, 1.48 |
| 28 | 1.16, 0.80, 0.86 | 1.53, 1.11, 1.05 | 1.63, 1.33, 1.27 | 1.78, 1.57, 1.37 |
| 32 | 0.51, 0.39, 0.52 | 0.83, 0.79, 0.72 | 1.40, 1.25, 1.12 | 1.70, 1.57, 1.40 |
| 34 | 0.44, 0.22, 0.41 | 0.78, 0.77, 0.78 | 1.28, 1.17, 1.17 | 1.76, 1.56, 1.51 |

The ratio stays O(1) while TV itself falls from 0.47 to 0.005 at m = 16 (square-root cancellation). χ²/dof rises to 2–4.4 at m = 12–16 and is below 1 at m = 4: the multiset {z_v} is over-dispersed at fine scales and more regular than random at coarse scales. Exact coincidences z_v = z_v′ exist, e.g. T^4(y) = T^4(y−1) for y ≡ 3 mod 16.

## (c) Data, scripts, commands

Directory: `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/w3-g2/`. `PY=/home/matrix/home/projects/collatz/venv/bin/python`. All runs under `taskset -c 4-5`.

**Generation counts.** E_λ(X) = #{y ∈ [X,2X) : T^j(y) ≥ X/2 for all j ≤ λ·log2 X}, X = 2^L (the source's definition). `g1_gen.c` walks the Terras tree of residues y mod 2^j with state (T^j(y mod 2^j), 3^(a_j)), prunes a class when even its largest member is below X/2, and iterates only surviving leaves in 128-bit arithmetic. It reproduces the source's `s4_generations.log` exactly at L = 12, 20, 26, 30. Cost is about 2.5 nodes per leaf; L = 38 visited 2.6·10^10 nodes.

Model: y uniform in [X,2X), all parities i.i.d. fair, T^j(y) = y·3^(a_j)/2^j (`g2_model.py`). Exact for j ≤ L up to the +1 terms; for j > L it is the tilted-independence heuristic.

| L | λ=1 | λ=1.25 | λ=1.5 | λ=2 | λ=3 | λ=4 | λ=8 |
|---|---|---|---|---|---|---|---|
| 26 | 4,777,034 | 3,142,246 | 2,084,696 | 971,357 | 242,165 | 71,801 | 906 |
| 30 | 58,606,996 | 36,608,601 | 22,739,189 | 9,986,189 | 2,200,818 | 547,497 | 3,317 |
| 32 | 201,121,995 | 120,782,736 | 75,421,587 | 31,835,943 | 6,610,168 | 1,527,156 | 6,893 |
| 34 | 717,551,677 | 439,286,714 | 256,527,644 | 104,520,620 | 19,570,389 | 4,261,734 | 15,524 |
| 36 | 2,575,623,006 | 1,454,991,238 | 877,673,903 | 338,358,889 | 59,341,359 | 12,001,795 | 32,866 |
| 38 | 8,956,301,461 | 5,315,462,767 | 2,993,927,059 | 1,112,857,964 | 182,050,549 | 33,805,091 | 70,758 |
| E/model, L=30 | 1.0001 | 1.0001 | 1.0002 | 1.0002 | 0.9991 | 1.0004 | 0.979 |
| E/model, L=34 | 1.0000 | 1.0000 | 1.0000 | 1.0001 | 1.0006 | 0.9979 | 1.015 |
| E/model, L=36 | 1.0000 | 1.0000 | 1.0000 | 0.9999 | 1.0000 | 1.0005 | 1.012 |
| E/model, L=38 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9999 | 1.0002 | 1.025 |
| local exponent 36→38 | 0.899 | 0.935 | 0.885 | 0.859 | 0.809 | 0.747 | 0.553 |
| same + 1.5·log2(L2/L1)/(L2−L1) | 0.958 | 0.993 | 0.944 | 0.917 | 0.867 | 0.806 | 0.612 |
| predicted 1 − λ(1−η) | 0.9500 | 0.9374 | 0.9249 | 0.8999 | 0.8499 | 0.7998 | 0.5996 |
| model, corrected, L 240→256 | 0.951 | 0.940 | 0.925 | 0.900 | 0.852 | 0.799 | 0.600 |

The local exponents oscillate by ±0.03 with L (lattice effects of ⌊λL⌋ and of the thresholds); the model reproduces the same oscillation, which is why E/model is the right test. Poisson z-scores reach 3–7 at λ = 8 and at λ = 1 for L = 38 (relative deviation 4·10^(−5), the model's grid error); survivors at large λ come in coalescing families, so Poisson errors understate the variance there.

**Predicted exponent.** In the model E_λ(2^L) = 2^L·P(walk with steps log2 3 − 1 and −1 stays ≥ −1−u for λL steps). Cramér plus ballot give E_λ ≍ C_λ·2^((1−λ(1−η))L)·L^(−3/2). For two generations there is no further optimisation: the optimal profile is flat, both generations at the critical tilt θ0, so η_2 = 1 − 2(1−η) = 0.89991. With threshold X^γ and horizon λ·log2 X the model exponent is 1 − λ·I(−(1−γ)/λ), where I(u) = 1 − H2((1+u)·θ0) is the rate for mean log2-drift u per step (I(0) = 1−η, I(−0.2075) = 0). This is < η iff λ·I(−(1−γ)/λ) > 1−η; for λ = 2 that needs roughly γ > 0.88.

| command | expected output |
|---|---|
| `gcc -O2 -o g1_gen g1_gen.c; ./g1_gen 30 > g1_L30.log; $PY g1_sum.py 30 g1_L30.log` (10 s) | `30 71541218 71541218 58606996 36608601 22739189 9986189 2200818 547497 3317` |
| `./g1_gen 38 0 2 > g1_L38_p0.log; ./g1_gen 38 1 2 > g1_L38_p1.log` (9 and 25 min) | `nodes 5766718149 leaves 2395754075` and `nodes 20700139297 leaves 8668660692` |
| `$PY g2_model.py 30` | `30 5.8604e+07 3.66039e+07 2.27339e+07 9.98465e+06 2.2027e+06 547295 3389.02` |
| `$PY g7_fit.py 26 30 32 34 36 38` | the table above |
| `gcc -O2 -o g3_equi g3_equi.c -lm; ./g3_equi 30 17 21 14` | per (a, m): N, χ², dof, z, TV, noise; `g3_table.log` holds L = 16–34 |
| `$PY g4_identities.py` | `identities OK on 32751 vectors`; five lines `|char|=… majorant=…` |
| `$PY g5_white.py` | white fraction 0.88–0.93 on pinned paths, a = 60…2000 |
| `$PY g6_ballot.py` | `omega=…0.98621`; `sup ratio 15.46`; the six lines quoted in B4 |
| `$PY g8_critical.py` | for ξ = 2^(l0), K = −2: white fraction 0.080 (n=200), 0.037 (n=800) pinned; 0.24, 0.22 for i.i.d. Geom(1/2) |
| `$PY g9_corN.py` | exact N(L,m,s)/prediction between 0.986 and 1.001 |

## (d) Litmus

- **3n−1.** T^L(y) = (3^a·y − r_v)/2^L and z_v = 3^a − τ′_v with the same Syracuse sum. Characters are conjugated; Steps 1–6 are unchanged. B_L and the charging of S+ use only T^j(x) ≤ 3^a·x/2^j, which is exact there. So W, N, S+ hold for 3n−1 with the same constants. They are true for a map with cycles, as they must be.
- **Cycles.** Nothing here mentions cycles. For the cycles of 3n−1 (1, 5, 17) and of 3n+d the statements bound counts in dyadic blocks and sojourn counts; they are true and empty for the known cycles.
- **3n+d, gcd(d,6) = 1.** r_v is multiplied by d, so frequency h becomes h·d; W should hold with d-dependent constants. Sketch only: CANDIDATE.
- **5n+1.** (T) is specific to 9 and 2 but should adapt to 25 and 2 (not checked). Even granting equidistribution, Corollary N has no content: non-descent needs a ≥ 0.431·L, which is typical, so the first-generation count is ≈ 2^L and no factor 2^(−(1−η)m) appears. S+ fails at its first line. The mixing statement is multiplier-blind and every saving comes from 3 < 4, which is the correct failure mode.
- **S_a control maps (ledger 22).** Not relevant: no statement here concerns a single orbit's fate.
- Where the constants enter: 3 through 3 < 4 and through (P); +1 through r_v ≥ 0 and Proposition I; positivity through y ≥ 2^L.

## (e) Dead ends (exact reasons)

1. **Absorbing the tilt into Tao's Proposition 1.17 (brief's idea (a)).** The tilted geometric law is geometric, and pinning the sum is free in the pairing step. But the required tilt is the critical one: mean valuation log2 3, so the renewal walk has slope log2 9, the slope of the hypotenuse of Tao's triangles. His Case 3 needs the walk to leave a triangle after ≤ 0.79m of the remaining m steps; at the critical slope it can stay to the end. For ξ ≡ 2^(l0) with l0 ≈ n·log2 3 − K√n one triangle covers the diagonal. VERIFIED (`g8_critical.py`): at K = −2 the white fraction on pinned paths is 0.080 (n = 200) and 0.037 (n = 800), against 0.90 for generic ξ and 0.22–0.24 for Tao's slope. So the uniform-in-ξ decay of the majorant fails at q*, and "S4-T" (`proof.md` Theorem 56, stated for compacts of (q*, 1)) cannot be extended to q*, which is exactly our case. That the true character sum (not just the majorant) fails to decay there is not shown.
2. **Excluding giant triangles by Baker.** (P) bounds v_2(ρ + t·3^ν) by C·log|t|·log² ν, while a triangle at horizontal position j0 needs it to exceed log2|t| ≈ j0·log2 9 by a positive proportion. Only triangles longer than j0·log² n are excluded: log n/log log n scales, no power of n. An abc-strength bound would exclude length > ε·n and still give only O(1/ε) exits. A power saving needs statistics of small values of ρ·2^(−l) mod 3^ν, not a pointwise Diophantine bound.
3. **Dispersion / second moment on collisions (idea (b)).** v ↦ z_v is not injective and the collision structure is arithmetic; χ²/dof reaches 4.4 at m = 16. A second moment controls the variance of class counts, not their mean over the bad set; the mean is the Fourier question again.
4. **Forced second-generation descent on a positive-density class (idea (c)).** REFUTED by data at the level of classes (L, a) and m ≤ 16: the conditional law of z_v mod 2^m is uniform to within sampling noise, and E_λ/model = 1.000. There is no deterministic gain beyond independence to iterate.
5. **Sparse landing scales [3^a, 2·3^a) (idea (d)).** The landing set has 2^(ηL) points in an interval of length 2^L; intersecting it with the 2^(ηL) bad residues needs z_v to full precision, m = L. That is the plateau two-prime count (w2-delta dead end 2, ledger family 4).
6. **Large sieve for bad residues in a short interval.** It needs the Fourier transform of 1_B at frequencies k/2^(L+m), |k| ≤ 2^m, i.e. the high binary digits of the inverse Terras map. By (I3) this is the same object as E_exp.
7. **Corollary N for the sojourn bound.** Its saving is smaller than the (log X)^(−0.486) that S+ takes from the barrier, and the two do not multiply without Lemma W-bar below.
8. **First-descent charging with O(1) multiplicity.** Sources of one target lie in one dyadic window but can be numerous; the trivial bound L costs the exponent 3/2 → 0.986. The distinct-levels trick (Lemma 3 of w2-delta) is lost once the charging time is not a function of the level.

## (f) Best lead

**Barrier-compatible pairing — PROVED (small).** The barrier event {S_j > −u for all j ≤ L} is {α_[1,j] > L − (a−j)·log2 3 − u for all j}. For even j this is G-measurable; for odd j = 2k−1 it reads α_2k < c_k with c_k G-measurable. So given G and the barrier the α_2k are still independent and uniform on an interval, and |E[χ | G, barrier]| = Π|cos πθ| over pairs with b_k = 3 and c_k > 2.

**Lemma W-bar (CANDIDATE).** Theorem W holds with V(L,a) replaced by the barrier-surviving vectors, uniformly in u ≤ log L. It needs Step 6 under the h-transformed walk, i.e. two-sided ballot estimates to bound one-step Radon–Nikodym factors away from the barrier. It would give #{y ∈ [X,2X) : T^j(y) > X/2^s for all j ≤ L+m} ≤ C_s·X^η·(log X)^(−3/2)·m·2^(−0.05m), the survival form of G2 with a sub-power saving, and would multiply the two savings in the sojourn bound.

**For the power saving: E_exp (B5).** Sharpest sub-question, purely about powers of 2 and 3: for fixed ρ ≠ 0 and δ > 0, the number of (j, l) with j ≤ n/2, |l − j·log2 9| ≤ √n·log n and ‖ρ·9^j·2^(−l)/3^n‖ ≤ ε·e^(−S) is ≤ C·n^(3/2)·e^(−cS) for S ≤ δn. With it, Step 6 gives W ≥ c·n off an exponentially small event, hence E_exp for small κ, hence G2. I see no present tool for it; it is of the type of Erdős' ternary-digit problem.

## (g) Brainstorm record (kill test first)

| # | idea | kill test | outcome |
|---|---|---|---|
| 1 | exact model for E_λ against exhaustive counts | ratio ≠ 1 beyond noise | not killed: ratio 1.000 |
| 2 | Tao 1.17 at a tilted geometric parameter | is the needed tilt inside (q*,1)? | killed: it is q* itself (dead end 1) |
| 3 | pin the sum instead of tilting | is the pinning G-measurable? | yes; Step 2 of Theorem W |
| 4 | low bits of z = top bits of σ/3^a | exact identity fails | (I3) holds; Step 1 |
| 5 | 2-adic Baker to bound triangles near the diagonal | does it exclude length ≥ j0·polylog? | yes, nothing better; Theorem W |
| 6 | abc-conditional version | does it give a power? | no (dead end 2) |
| 7 | dispersion on collisions | are collisions random? | no, arithmetic (dead end 3) |
| 8 | forced descent classes | TV of class laws above noise? | no (dead end 4) |
| 9 | sparse scales [3^a, 2·3^a) | needs m < L? | needs m = L (dead end 5) |
| 10 | large sieve in Z/2^(L+m) | independent of E_exp? | no (dead end 6) |
| 11 | ballot refinement of Theorem S | multiplicity against barrier gain | Theorem S+ (0.986) |
| 12 | barrier-conditioned pairing | product structure survives? | yes; Lemma W-bar left open |

## (h) Hostile self-review and credences

- *Step 3 transfer.* Only functionals of the first half of the letters are transferred; the density ratio is bounded by (LLT) because q is matched to the pinned mean. Epochs stop at N/2 ≤ a/4.
- *Step 6 stopping-time bias.* A first draft used "the exit step is O(1) with probability ≫ 1", which is not justified for a stopped walk. Replaced: the floor overshoot is deterministically ≤ 0.811 (one b-step, not one holding time), and the top overshoot is controlled by the tail ratio ψ summed against P(exit).
- *White at the exit is not enough*: counted points need b_j = 3. Hence the extra step (1,3) and the check that it cannot re-enter Δ (uses log 9 > 3·log 2).
- *h divisible by 3* is handled by lowering n; n ≥ a/2.
- *The trivial triangle* (t = 0, l ≤ 1 + log2 H) is real (it shows in `g5_white.py` as depth 60–650 at small l) and is avoided by starting epochs at J_0 > log2 H.
- *Sign error caught*: I first wrote the covering triangle of dead end 1 at l0 = n·log2 3 + K√n; the computation shows it is at −K√n.
- *Not checked against print*: the exact hypotheses of (P) and the exact form of (BAL). If (P) held only with log³ ν the theorem would keep its form.
- *Corollary N main term*: the factor m is a loss of the proof (union over a), not of the truth.
- Exact arithmetic: all identity checks and counts are integer; floats appear only in the model, in χ²/TV and in `g5`, `g8`.

| item | label | credence |
|---|---|---|
| Identities (I1)–(I3), pairing identity under pinning | PROVED, VERIFIED | 99 % |
| Generation counts to 2^38 as finite data | VERIFIED | 97 % |
| Exponent of E_λ is 1 − λ(1−η) asymptotically (λ = 2: 0.8999 < η) | CANDIDATE (data) | 93 % |
| Theorem W as stated | PROVED given (T), (P); unrefereed | 78 % |
| Corollary N given W | PROVED | 93 % |
| Theorem S+ | PROVED given (BAL); unrefereed | 85 % |
| Proposition Rd (E_exp ⇒ G2) | PROVED implication | 90 % |
| E_exp true | CANDIDATE | 88 % |
| E_exp provable with present tools | — | 5 % |
| G2 true | CANDIDATE | 92 % |
| Dead end 1 (majorant fails at the critical tilt) | VERIFIED numerically, argument sketched | 88 % |
| Any of this bears on Collatz, H1 or Lemma E | — | 0 % |

Sources: [Tao, arXiv:1909.03562](https://arxiv.org/abs/1909.03562) (TeX source read locally); Bugeaud–Laurent, J. Number Theory 61 (1996) 311–342 (quoted from memory); [Yamada, arXiv:math/0607072](https://arxiv.org/abs/math/0607072) (consulted for the shape of the Bugeaud–Laurent theorem; it does not restate the corollary used); Addario-Berry–Reed, "Ballot theorems, old and new" (2008), and Aïdékon–Shi (2014) (quoted from memory).