<!-- Saved by the coordinator from the blind-H agent's final message (the agent's own write was refused). -->
## Full proof

**Notation.** θ = log2/log3, so 3^θ = 2. λ = θ/(1−θ) = 1.7095. η = H_2(θ) = 0.949956. B_j = [2^j, 2^(j+1)). a_j(x) is the number of odd terms among x, Tx, …, T^(j−1)x. Fix a distinct stretch x_0..x_{K−1} with K ≤ ∞. N(Y) = #{k<K : x_k < Y} and n_j = #{k<K : x_k ∈ B_j}, so N(2^L) = Σ_{j<L} n_j.

**L1 (Terras).** The map x mod 2^j → (first j parities) is a bijection onto {0,1}^j. Hence any 2^j consecutive integers contain exactly binom(j,a) with a_j = a.

*Proof.* Induction on j. If x ≡ y mod 2^j, the first j parities agree and T^j(x) − T^j(y) = 3^a(x−y)/2^j, because the same affine branches are taken. Conversely, if the length-(j+1) vectors agree, then x ≡ y mod 2^j by induction, and equal parity of T^j forces 3^a(x−y)/2^j to be even. So x ≡ y mod 2^(j+1). Injectivity between sets of equal size gives the bijection. ∎

**L2 (affine bound).** T^j(x) = 3^a·x/2^j + r with 0 ≤ r ≤ (3/2)^a − 1. Hence x < 2^(j+1) implies T^j(x) < 2·3^a + (3/2)^a ≤ 3^(a+1).

*Proof.* r_0 = 0. An even step sends r → r/2, an odd step sends r → (3r+1)/2, and (3((3/2)^a − 1) + 1)/2 = (3/2)^(a+1) − 1. ∎

**L3 (Chernoff).** For real t: Σ_{a≥t} binom(j,a) ≤ λ^(−t)(1+λ)^j = 2^(ηj)·λ^(θj−t).

*Proof.* Since λ ≥ 1, 1_{a≥t} ≤ λ^(a−t); apply the binomial theorem. For the identity, 1+λ = 1/(1−θ), so (1+λ)·λ^(−θ) = θ^(−θ)(1−θ)^(−(1−θ)) = 2^η. ∎

**L4 (class injection).** Let I(j,a) = {k<K : x_k ∈ B_j, a_j(x_k) = a, k+j < K}. Then #I(j,a) ≤ min(binom(j,a), N(3^(a+1))).

*Proof.* The x_k are distinct elements of B_j in class a, so there are at most binom(j,a) by L1. For k ∈ I(j,a), x_{k+j} is a term of the same stretch and is < 3^(a+1) by L2. The map k → k+j is injective, so the count is at most the number of indices with term < 3^(a+1). ∎

**L5 (end terms).** Let e_j = #{k<K : x_k ∈ B_j, k+j ≥ K}. Then Σ_{j<L} e_j ≤ L−1, since all such k are ≥ K−(L−1) and each index lies in one block. If K = ∞, every e_j = 0.

**Theorem A.** N(2^L) ≤ A·2^(ηL) for all L ≥ 0, with A = 9.3.

*Proof.* Strong induction on L within the fixed stretch. Base: N(1) = 0. Let L ≥ 1, fix j < L, u = 3.2, t = θj − u.
- Terms of B_j with a_j ≥ t number at most 2^(ηj)·λ^u, by L1 and L3.
- Non-end terms with a_j = a < t number at most N(3^(a+1)), by L4. Since u ≥ 1, a+1 < θj, so 3^(a+1) < 2^j and i := ⌈(a+1)·log_2 3⌉ ≤ j < L. The hypothesis gives N(3^(a+1)) ≤ N(2^i) ≤ A·6^η·3^(ηa).
- Summing over integers 0 ≤ a < t: Σ 3^(ηa) < 3^(ηt)·3^η/(3^η−1), and 3^(ηt) = 2^(ηj)·3^(−ηu).
- End terms with a < t number at most e_j.

So n_j ≤ e_j + S·2^(ηj), where S = λ^u + A·6^η·(3^η/(3^η−1))·3^(−ηu). By L5,

N(2^L) ≤ (L−1) + S·(2^(ηL)−1)/(2^η−1) ≤ 2^(ηL)·[S/(2^η−1) + (L−1)·2^(−ηL)].

Now sup_{L≥1} (L−1)·2^(−ηL) = 2/2^(3η) = 0.2774, attained at L = 3. With 2^η = 1.93181, 3^η = 2.83951, 6^η = 5.4854, λ^3.2 = 5.5615 and 3^(−3.2η) = 0.03546:

S = 5.5615 + 9.3·5.4854·1.5437·0.03546 = 8.354, and the bracket is 8.354/0.93181 + 0.2774 = 9.242 ≤ 9.3. ∎

**Claim 2.** For X ≥ 1 take L = ⌊log_2 X⌋ + 1, so X < 2^L ≤ 2X. Then #{x_k ≤ X} ≤ N(2^L) ≤ 9.3·2^η·X^η < 18.0·X^η.

**Claim 1.** Σ 1/x_k ≤ Σ_j n_j·2^(−j). By Abel summation, Σ_{j≤J} n_j·2^(−j) = Σ_{i=1}^{J} N(2^i)·2^(−i) + 2·N(2^(J+1))·2^(−(J+1)), and the last term tends to 0 by Theorem A. Using N(2^i) ≤ min(2^i − 1, 9.3·2^(ηi)):

Σ 1/x_k ≤ Σ_{i≥1} min(1, 9.3·2^(−(1−η)i)) ≤ 64 + 9.3·2^(−0.05004·65)/(1 − 2^(−0.05004)) ≈ 92.6 < 94.

**Claim 3.** For odd x_i, x_{i+1} = (3x_i/2)(1 + 1/(3x_i)); for even x_i, x_{i+1} = x_i/2. So the ratio equals Π_{odd}(1 + 1/(3x_i)) ≤ exp(Σ 1/(3x_i)) ≤ exp(C/3).

**3x−1 map.** L1 is unchanged. L2 becomes T^j(x) = 3^a·x/2^j − r ≤ 3^a·x/2^j < 3^(a+1). L3–L5 and Theorem A carry over with the same constants.

**Computer-assisted sharpening (not needed for the proof).** `checks.py` runs the same recursion in exact integers, using the sharper landing bound x_{k+j} < 2·3^a + ⌈(3/2)^a⌉:

F_0 = 0, F_L = min(2^L − 1, (L−1) + Σ_{j<L} min(2^j, Σ_a min(binom(j,a), F_{i(a)}))).

- sup_{L≤1500} F_L/2^(ηL) = 1.406, at L = 12; the ratio is 0.191 at L = 1500 and decaying.
- Σ_{i≤1500} F_i/2^i = 31.8067, and the tail beyond 1500 is < 10^(−20) by Theorem A, so C ≤ 31.81.
- The 1.406 is not a uniform constant: beyond L = 1500 only A = 9.3 is proved.

**Hostile-referee pass**
1. Circularity: L4 is invoked only when 3^(a+1) < 2^j, i.e. at strictly lower scales; the other classes use only the binomial count. The induction is strong, with base N(1) = 0.
2. Injection: for fixed j, k → k+j is injective on indices, and the target is counted by index, so coincident values cannot arise.
3. End effects: only terms with k+j ≥ K escape L4, and L5 bounds them by L−1 in total. Stretches truncated at K/2 and K−3 were tested.
4. Small x: no relative drop is needed. L2 uses only x < 2^(j+1) and yields the absolute bound 3^(a+1), which absorbs the additive term.
5. Geometric sum: the factor is q/(q−1), not 1/(q−1). I made this error in a first draft and corrected it; it moves A from about 5.2 to 9.3.
6. L3 is trivially true for t ≤ 0 or t > j.
7. Dyadic rounding costs only constant factors (2^η in C', 6^η in the step).

No gap found.

**Tests (all pass, exact integer/Fraction arithmetic)**
- L1: exhaustive for j ≤ 14, four block positions, both maps.
- L2: 40000 random (x, j) with x up to 2^140 and j ≤ 120, plus exhaustive on blocks j ≤ 12.
- L3: all j ≤ 700 and all integer t.
- L4 and N(2^L) ≤ F_L: all n ≤ 20000, 3000 random n < 2^60, n = 2^200 − 1, and 3x−1 for n ≤ 5000 plus 500 random, each also truncated.

**Disproof attempt.** A violation of Claim 2 needs one distinct path visiting far more than X^η of the integers below X. L4 forbids this structurally. Real trajectories are nowhere near it: the longest stretch for n ≤ 2·10^7 has 442 terms, so the ratio is below 0.001 for X > 2^20.

Sources:
- [Iteration Steps of 3x+1 Problem (arXiv:2506.23070)](https://arxiv.org/pdf/2506.23070)
- [There are no Collatz m-Cycles with m ≤ 91 (arXiv:2201.00406)](https://arxiv.org/pdf/2201.00406)
- [Almost all orbits of the Collatz map attain almost bounded values (arXiv:1909.03562)](https://arxiv.org/pdf/1909.03562)