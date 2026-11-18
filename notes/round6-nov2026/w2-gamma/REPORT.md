<!-- Saved by the coordinator from the w2-gamma agent's final message (the agent's own write was refused). -->
# FULL REPORT (intended REPORT.md) — w2-gamma: disproof search, cycle bounds, barrier theorems

Notation: `T(n) = n/2` (n even), `(3n+1)/2` (n odd). `N = {1,2,…}`, `N_0 = N ∪ {0}`. `v2` is the 2-adic valuation. The parity word is `π_S(n) = (S^i(n) mod 2)_{i≥0}`.

## (a) Summary

1. **Theorem R (rigidity, PROVED).** `T` is the only `S: N → N` with (I) the parity-prefix property (`n ≡ n' mod 2^k` ⇔ first `k` parities agree, for all `k`), (II) `S(n) < n` for even `n`, (III) `n < S(n) ≤ 2n` for odd `n`.
2. **Theorem S (sharpness, PROVED and verified).** For every `a ≥ 0`, the map `S_a` ("`T`, except `T(n) − 2^a` on `n ≡ −1 mod 2^(a+1)`") has (I), (II), and (III) at every odd `n` except `2^(a+1) − 1`, which is a fixed point. `S_0` is the `3n−1` control, so `3n−1` is the first member of an infinite litmus family converging to `T`.
3. **Theorem B (implant, PROVED and verified).** For every modulus `m` and bound `X` there is `S ≥ T`, `S ≡ T mod m`, `S = T` on `[1,X]` and off one class of density `< 1/X`, with (I) and `S(2x) = x`, having a nontrivial cycle above `X`.
4. **Theorem A (isometry class, PROVED with finite demo).** Every countable dense `T`-invariant `A ⊂ Z_2` gives `S_A: N_0 → N_0` with (I) and `(N_0, S_A) ≅ (A, T)`. With `A = N_0 ∪ orbit(z)`, `z` irrational, `S_A` has a divergent orbit, equals `T` on `[0,X]`, and is `≡ T mod 2^k`.
5. **Cycle bound (recomputed exactly).** Plain Eliahou at `X0 = 2^71` gives `K ≥ 72,057,431,991`, `L ≥ 114,208,327,604`, the same as at `2^68`. Lemma C2 (PROVED) improves the size-only constant to `1/(2 ln 2)` but still needs `2^71.413`. The published state of the art is `K ≥ 137,528,045,312` (Hercher Cor. 29 with Barina's `2^71`).
6. **Disproof search (VERIFIED numbers).** Structured seeds lose to random-model records by a factor of 4–5. Nothing anomalous was found.
7. Dead ends are in (d).

## (b) Statements and proofs

### Lemma 1 (structure of the prefix property) — PROVED
`S: N → N` has (I) iff for all `n ≠ n'` of equal parity, `v2(S(n) − S(n')) = v2(n − n') − 1`.

*Proof.* (⇒) Let `v = v2(n−n') ≥ 1`. By (I) with `k = v` and `k = v+1`, the words of `n, n'` agree in exactly the first `v` places. So the words of `S(n), S(n')` agree in exactly the first `v−1` places, and (I) gives `v2(S(n)−S(n')) = v−1`.

(⇐) Induction on `k`; `k = 1` is trivial. If `n ≡ n' mod 2^k`, `n ≠ n'`, `k ≥ 2`, then `v2(Sn − Sn') ≥ k−1`. By the case `k−1`, the words of `Sn, Sn'` agree in `k−1` places, so those of `n, n'` agree in `k`. Conversely, if the words agree in `k` places and `n ≠ n'`, then `Sn ≠ Sn'`, their words agree in `k−1` places, so `v2(n−n') − 1 ≥ k−1`. ∎

Consequence. Write `S(2x) = x + γ(x)` and `S(n) = T(n) + g(n)` for odd `n`. Then (I) is equivalent to `γ(x) ≡ γ(x') mod 2^(v2(x−x')+1)` and `g(n) ≡ g(n') mod 2^(v2(n−n'))`. Call **𝒞** the class with (I) and `γ ≡ 0`: `S(2x) = x`, `S = T + g` on odds, `g` 2-adically 1-Lipschitz. It contains `(an+d)/2` for odd `a, d`; compare Bernstein–Lagarias, Appendix B.

### Theorem R (rigidity) — PROVED
If `S: N → N` satisfies (I), (II) and (III), then `S = T`.

*Proof, even part.* (II) gives `|γ(x)| ≤ x − 1`. Suppose `γ(z) ≠ 0` with `a = v2(γ(z))`. Take `x ∈ {1,…,2^a}` with `x ≡ z mod 2^a`. If `x = z`, then `|γ(z)| ≥ 2^a ≥ z`, a contradiction. Otherwise `γ(x) ≡ γ(z) mod 2^(a+1)`, so `|γ(x)| ≥ 2^a ≥ x`, a contradiction.

*Proof, odd part.* (III) gives `|g(n)| ≤ (n−1)/2`. Suppose `g(z) ≠ 0` with `a = v2(g(z))`. Take the odd `x < 2^(a+1)` with `x ≡ z mod 2^(a+1)`. If `x = z`, then `|g(z)| ≥ 2^a > (z−1)/2`. Otherwise `g(x) ≡ g(z) mod 2^(a+1)`, so `|g(x)| ≥ 2^a > (x−1)/2`. Contradiction either way. ∎

Where 3, +1 and positivity enter: (III) at `n = 1` forces `S(1) = 2`. The control `3n−1` has `S(1) = 1`; `5n+1` has `S(n) > 2n` for `n ≥ 2`; `3n+d` with `d ≥ 3` has `S(1) > 2`. All three have (I) and (II) and fail (III).

Exhaustive check: there is no nonzero 1-Lipschitz `g` with `|g(x)| ≤ (x−1)/2` on odd `x < 128`, while more than 1000 exist with `|g(x)| ≤ (x+1)/2`. A brief literature search did not find the statement; it may be folklore.

### Theorem S (the litmus family `S_a`) — PROVED, verified `a ≤ 12`
Let `S_a(n) = n/2` for even `n`, and `S_a(n) = (3n+1)/2 − 2^a·[n ≡ −1 mod 2^(a+1)]` for odd `n`. Then:

- (i) `S_a ∈ 𝒞` and `S_a: N → N`.
- (ii) `S_a = T` off the class `−1 mod 2^(a+1)`, in particular on `[1, 2^(a+1)−2]`, and `S_a ≡ T mod 2^a` everywhere.
- (iii) (II) holds, and (III) holds at every odd `n` except `n_a = 2^(a+1) − 1`, where `S_a(n_a) = n_a`.
- (iv) `S_0(n) = (3n−1)/2` on odds.

*Proof.* Here `g = −2^a·1[class]`. For odd `n ≠ n'` with `v = v2(n−n')`: if `v ≥ a+1`, both or neither lie in the class; if `v ≤ a`, the difference is `0` or `±2^a ≡ 0 mod 2^v`. So `g` is 1-Lipschitz and Lemma 1 gives (i). In the class, `n ≥ n_a`, so `S_a(n) ≥ 2^(a+1) − 1 ≥ 1`, and `S_a(n) > n ⇔ n > n_a`. Finally `S_a(n_a) = 3·2^a − 1 − 2^a = n_a`. ∎

**Corollary (what a proof must use).** For each `a`, an argument for "no nontrivial cycle" is wrong if it uses only:
- (I) and (II);
- all values of `T` below `2^(a+1) − 1`;
- `T` modulo `2^a`;
- `T` on a set of density `1 − 2^(−a−1)`;
- (III) at all odd `n ≠ 2^(a+1) − 1`.

The infimum over nonzero perturbations in 𝒞 of `sup |S−T|(n)/n` is exactly `1/2`, and it is not attained.

**Remark for this repo.** An H1 orbit (parities in `{110,1110}^ω`) never meets `−1 mod 16`. So H1 is literally the same statement for `T` and for every `S_a` with `a ≥ 3`. Everything that distinguishes `T` from `S_a` therefore sits in Lemma E, whose analogue is false for every `S_a`.

**Observed (VERIFIED).** For starts `n ≤ 2·10^5` (`a ≤ 8`) and `n ≤ 5·10^4` (`a ≤ 12`), every orbit of `S_a` enters a cycle. The cycle minima are `{1, n_a}`, plus `5, 17` (`a=0`), `7` (`a=1`), `347` (`a=2`) and `3071` (`a=6`).

### Theorem B (cycle implant) — PROVED, verified on 5 instances
For all `m, X ≥ 1` there is `S ∈ 𝒞`, `S: N → N`, with:
- `S ≥ T` and `S ≡ T mod m` pointwise, and `S − T ∈ {0, G}`;
- `S = T` on `[1, X]` and outside one residue class mod `2^k'`, where `2^(−k') < 1/X`;
- a cycle of length `a ≥ 3` with all elements `> X`.

*Proof.* Choose `a ≥ 3` divisible by `p−1` for every prime `p ≥ 5` dividing `m`. Then `D = 2^a − 3 ≡ −2 mod p`, so `D` is coprime to `6m`. Write `m = 2^k M`, pick `k' ≥ max(k,2)` with `2^k' > DX`, and set `m' = 2^k' M`, `r = D^(−1) mod 2^k'`. From `Dr = 1 + 2^k' t` with `t ≥ 1`, we get `r > X`.

Pick `c ∈ [1,D]` with `2m'c ≡ −1 mod D`, and set `G = m'c`, `x_0 = (1+2G)/D`, so `x_0 ≡ r mod 2^k'`. Define `S = T + G·1[n ≡ r mod 2^k']` on odds. This is 1-Lipschitz because `2^k' | G`. Then `S(x_0) = (D+3)x_0/2 = 2^(a−1) x_0`, and `a−1` halvings return to `x_0`. All cycle elements are `≥ x_0 ≥ r > X`. ∎

### Proposition B2 (finite sets of primes) — PROVED
For every finite set Σ of primes, `x = 1/(2^L − 3)` with `(p−1) | L` for all `p ∈ Σ`, `p ≥ 5`, and `L ≥ 3`, is a positive non-integer rational on a `T`-cycle. Its parity word is `1 0^(L−1)`, since `T(x) = 2^(L−1) x`. It is integral at 2, 3 and every prime of Σ. So positivity plus integrality at finitely many primes cannot exclude cycles.

VERIFIED: every `d` coprime to 6 with `5 ≤ d < 3000` (999 values) has a primitive positive cycle of `3n+d`.

### Theorem A (the isometry class) — PROVED; finite demo
**Lemma 2.** Let `A = {a_0, a_1, …} ⊂ Z_2` be countable and dense. There is a bijection `h: N_0 → A` with `v2(h(n) − h(n')) = v2(n − n')`. If `a_i = i` for `i ≤ X`, then `h(n) = n` for `n ≤ X`.

*Proof.* For a ball `C`, let `own(C)` be the least-index element of `A ∩ C`. Set `h(0) = a_0`. For `n = n' + 2^j` with `n' < 2^j`, set `h(n) = own(h(n') + 2^j + 2^(j+1) Z_2)`.
- Isometry: induction on `j`, using `h(n) ≡ h(n') mod 2^j` and `h(n) − h(n') ≡ 2^j mod 2^(j+1)`.
- Surjectivity: `{h(n): n < 2^j}` is the set of owners of the level-`j` balls. The owner of a ball owns the child containing it, and `h(n'+2^j)` owns the other child. Each `a_i` owns its level-`j` ball once that ball excludes `a_0..a_(i−1)`.
- Last claim: the least natural number in `n + 2^(j+1) Z_2` is `n`. ∎

**Theorem A.** Let `A` be countable, dense, `T(A) ⊂ A`, with `a_0` even, and let `S_A = h^(−1) T h: N_0 → N_0`. Then:
- (i) `S_A` has (I), because `h` is a parity-preserving isometry and `T` has (I) on `Z_2`.
- (ii) `(N_0, S_A) ≅ (A, T)`.
- (iii) If `a_i = i` for `i ≤ X` and `X ≥ 2^k − 1`, then `S_A ≡ T mod 2^(k−1)` pointwise, and `S_A(n) = T(n)` for `n ≤ (2X−1)/3`.

**Corollaries.**
1. Take `A = N_0 ∪ {T^t z}` with `z ∈ Z_2 \ Q`. The orbit of `z` never repeats, since an eventually periodic parity word forces `z ∈ Q`. So `S_A` has an orbit visiting each natural number at most once, which therefore tends to infinity, while `S_A` on `h^(−1)(N_0)` is a copy of Collatz.
2. Take `A = Z_2 ∩ Q`. Then `S_A` has a cycle for every periodic parity word.

Hence no argument using only (I), any finite set of values of `T`, and `T` modulo a fixed `2^k` proves either half of Collatz. This is one uniform statement of ledger families 1–3. By Theorem R, none of these `S_A` satisfies both (II) and (III).

**Demo (exact).** With `X = 63` and `z` having the binary Champernowne word as parity word:
- `S(n) = T(n)` for `n ≤ 40` (first difference at 69);
- `S ≡ T mod 32` for `n < 1500`;
- prefix bijection mod `2^7` holds;
- the orbit of 91 follows `h^(−1)(z_t)` for 399 steps with 400 distinct values (maximum 524,483).

### Cycle length bound — recomputed exactly
Eliahou: a cycle with `K` odd terms and `L` terms, all `> X0`, has `0 < L − Kθ ≤ K log2(1 + 1/(3X0))`, where `θ = log2 3`. The least admissible denominators were found by Stern–Brocot search with 200-digit arithmetic and an endpoint perturbation test.

| X0 | K ≥ | L ≥ (T-steps) | L+K (unshortened) | excluded iff X0 > | with Lemma C2 |
|---|---|---|---|---|---|
| 2^68 … 2^71 | 72,057,431,991 | 114,208,327,604 | 186,265,759,595 | 2^71.8843 | 2^71.413 |
| 2^72 … 2^75 | 137,528,045,312 | 217,976,794,617 | 355,504,839,929 | 2^75.4333 | 2^74.962 |
| 2^76 … 2^78 | 890,638,885,193 | 1,411,629,234,715 | 2,302,268,119,908 | 2^78.3332 | 2^77.862 |

**Lemma C2 (PROVED; discrepancy constant not optimised).** Let `x_0..x_(K−1)` be the odd terms in order and `ℓ_i = log2(x_i/X0) ≥ 0`. Since `x_(i+1) = (3x_i+1)/2^(e_i)`, we have `ℓ_i ≡ ℓ_0 + iθ + δ_i mod 1` with `0 ≤ δ_i ≤ L − Kθ`. Hence `1/x_i ≤ 2^(−{ℓ_0+iθ+δ_i})/X0`. By equidistribution of `iθ` (Koksma plus the Ostrowski bound, error below `10^(−6)` for `K ≥ 10^9`), `Σ 1/x_i ≤ (K/X0)(1/(2 ln 2) + 10^(−6))`. So Eliahou's inequality holds with `X0` replaced by `2 ln 2 · X0 = 2^0.4712 X0`. This is optimal for size-only arguments: the walk `ℓ → {ℓ+θ}` attains it.

Comparison with Hercher (arXiv 2201.00406, read through an ar5iv summary, not re-derived):
- His Theorem 27 has constant `3/4`, giving threshold `2^71.47`.
- His Corollary 29 (residue tracking by program) needs only `X0 ≥ 3·2^69 = 2^70.585`. With Barina's `2^71` the best published bound is therefore `K ≥ 137,528,045,312`, `L ≥ 217,976,794,617`.

What an improvement would need:
- Verification of all `n` up to about `2^75` (size-only: `2^74.962`), which is 8–16 times Barina's effort.
- For `m`-cycles (`m ≥ 92`), redoing Hercher's Baker-bound and continued-fraction computation with `X0 = 2^71`. I did not attempt this. A 2026 Zenodo preprint claims `m ≤ 95`; unverified.

### Disproof search — VERIFIED numbers
`σ(n)` is the least `k` with `T^k(n) < n`. The model is `#{n < 2^N: σ(n) > k} ≈ 2^(N−k) A_k`, where `A_k` counts parity words with `3^j > 2^i` on every prefix (exact DP; growth 1.9303 for `k ≤ 2600`, limit 1.93185). The predicted record is `k*(N)`, with asymptote 19.99 per bit.

| N | exhaustive max σ, n < 2^N | model k*(N) |
|---|---|---|
| 20 | 183 | 229 |
| 24 | 287 | 297 |
| 26 | 376 | 332 |
| 28 | 395 | 369 |
| 32 | 447 (n = 2,788,008,987) | 442 |

Record holders (values recalled from Roosendaal's table; σ recomputed exactly, record status not rechecked):

| n | size | σ | model |
|---|---|---|---|
| 1008932249296231 | 2^49.8 | 886 | 779 (about a 2.5% tail event under the model) |
| 118303688851791519 | 2^56.7 | 902 | 911 |
| 180352746940718527 | 2^57.3 | 966 | 931 |
| 2602714556700227743 | 2^61.2 | 1005 | 1008 |

Structured seeds, σ per bit at `N = 60, 120, 240, 480`:
- `2^N − 1`: 3.42, 3.86, 3.40, 3.88.
- Seeds near `−5`: 1.1–1.3.
- Seeds near `−17`: 1.0–1.6.
- Seeds near rational cycles `(1110)`, `(11101)`, `(1101)`: 1.5–2.9.
- Hybrid at `N = 60` (36 low ones plus all `2^24` top parts): `σ = 584`. The best of `2^24` random 60-bit numbers gives 302; the true record at this size is about 1000.

**REFUTED:** "structured 2-adic seeds beat random search". A divergent orbit would need ones-density `≥ 1/log2(3 + 1/x_0)` on every prefix from its minimum. Nothing found deviates from the model.

**Proposition G (PROVED, folklore).** `σ(2^N − 1) > N log2 3 − 1`. Conversely, any lower bound on `σ(n)` that uses only `n mod 2^k` (`j` ones in the prefix, then worst-case halving) is at most `j log2 3 ≤ k log2 3`, while `n < 2^k` costs `k` bits. So 1.585 per bit is the limit of that method.

## (c) Scripts (core 4)
All are in `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/w2-gamma/`.

| Command | Expected output | Time |
|---|---|---|
| `python cycle_bound.py` | `j=  68  K=72057431991  L=114208327604`, `j=  72  K=137528045312 …`, `dies when X0 > … = 2^ 71.8843174685`, threshold list | 5 s |
| `python barrier_check.py 3000` | all `True`; violation lists `[2^(a+1)−1]`; `nonzero solutions: 0`; five implants; final list `[]` | 2 min |
| `python theoremA_demo.py` | all checks `True` | 20 s |
| `python cper_scan.py` | `27616` maps; `maps with an orbit exceeding 2^400: 0` | 3 min |
| `gcc -O2 -o glide glide.c; ./glide 1 32` | last line `N=32 max_sigma(n<2^N)=447 at n=2788008987` | 33 s |
| `./glide 2 60 24` and `./glide 3 60 24` | `584` and `302` | — |
| `python glide_model.py` | model table and structured seeds | 1 min |

## (d) Dead ends
1. **Structured seeds for long glides.** They lose by a factor of 4–5. Bits spent on a rising prefix buy about 3.8 steps each (a random fall from height `1.5^N`); bits spent on search buy 14–20.
2. **A provable stopping-time constant above `log2 3` per bit.** Blocked by Proposition G.
3. **A divergent orbit in 𝒞 with small relative perturbation.** Impossible: Theorem R forbids any nonzero `g` with `|g(x)| ≤ (x−1)/2` everywhere. An explicit block design (`2^m − 1 → 2·3^(m−1) − 1 →` perturb `→ 2^e(2^m' − 1)`) also fails. Lemma 1 forces pairwise distinct `e_j` with `v2(m_j − m_j') = min(e_j, e_j') − 2`, which needs search windows of width `2^j` at block `j` while `m_j` grows only like `1.585^j`.
4. **Divergence in 𝒞 with periodic bounded `g`.** A periodic itinerary pins a rational fixed point, so the itinerary must be aperiodic. A scan of all 27,616 admissible `g` mod 16 with `|g| ≤ 8` found that every start `n ≤ 3000` enters a cycle; no orbit exceeds `2^400`.
5. **Eliahou with `2^71`.** No change from `2^68`; even the optimal size-only refinement needs `2^71.413`.
6. **Prime-by-prime barrier** (a cycle in `Z[1/q] \ Z` for every prime `q ≥ 5`). This is Lagarias' open existence conjecture for `d = q^j`; it is only verified for `d < 3000`.
7. **Undecidability inside 𝒞.** Conway and Kurtz–Simon need arbitrary multipliers. In 𝒞 every branch has slope `3/2` or `1/2`, and I found no encoding.

Brainstorm list, with outcome:
- Glide lattice search: killed by the model.
- Seeds near negative cycles: killed.
- Seeds near rational cycles: killed.
- Provable glide constant: Proposition G.
- Eliahou recomputation: done.
- Size-only refinement: Lemma C2, insufficient.
- Isometric conjugates preserving `N`: Theorem A.
- Residue-class perturbations with exact multiplier 3: Theorems S and B.
- Minimal property set singling out `T`: Theorem R.
- Divergence in 𝒞_per: open, scan negative.
- Finite-prime integrality: Proposition B2.

## (e) Best lead
**Lemma L (open).** There is a periodic, 2-adically 1-Lipschitz `g: 2N−1 → Z` such that `T + g` maps `N` to `N` and has a divergent orbit.

If true, "no divergent orbit" cannot be proved by any argument valid on all of 𝒞_per (exact slopes `3/2` and `1/2`, shift conjugacy, bounded additive term), just as Theorem S shows for cycles. If false, its negation is strictly stronger than the divergence half of Collatz. Credence true: 55%; provable with current tools: 10%.

Usable immediately: add `S_a` for all `a ≥ 0` to the mandatory controls, since `3n−1 = S_0`. Any correct proof must use `n < T(n)` at `n = 2^(a+1) − 1` for every `a`.

Sources:
- [Hercher, arXiv 2201.00406](https://arxiv.org/abs/2201.00406v3)
- [Hercher, J. Integer Seq. 26 (2023)](https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.pdf)
- [Hercher, ar5iv rendering](https://ar5iv.labs.arxiv.org/html/2201.00406)
- [Bernstein–Lagarias, The 3x+1 conjugacy map](https://dept.math.lsa.umich.edu/~lagarias/doc/bernstein.pdf)
- [Lagarias, annotated bibliography II](https://arxiv.org/pdf/math/0608208)
- [Zenodo preprint claiming m ≤ 95 (unverified)](https://zenodo.org/records/20755034)