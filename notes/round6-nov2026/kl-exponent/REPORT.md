<!-- Saved by the coordinator from the kl-exponent agent's final message (the agent's own write was refused). -->
# kl-exponent track — REPORT (round 6, November 2026)

Not a record attempt. Others claim k = 22, exponent 0.9251 (`dpalmqvist/kollatz`, unrefereed).

## (a) Summary

1. **Theorem T is PROVED** (full proof in b1). A hostile re-derivation found no gap. Brute force found no violation in 1.3·10^9 tree nodes with x up to 10^8.
2. **Novelty.** It is not KL's argument with a constant tracked. KL 2003 (§3–5) and Mazur's 0.90 paper (§4) work with envelopes φ_k^m(y) = inf_a π*_a(2^y a) and must eliminate "advanced" terms; Mazur writes "A direct induction is impossible until this advanced argument has been expanded" and adds a second 3^17-byte "adaptive potential" certificate. Theorem T inducts on |S_a(x)| for individual (a, x) and needs neither. msharpe248's Lean source was not read, and the argument is elementary, so prior occurrence elsewhere is possible.
3. **KL Table 2 reproduced, k = 2..11**, each with an exact feasibility certificate and an exact infeasibility certificate 4·10^-8 apart in γ.
4. **Pushed to k = 19** with exact certificates: γ = 0.9094275 feasible, 0.9094475 infeasible. Every value agrees with `lit/kollatz/RESULTS.md`.
5. **Lemma G lead: negative.** Proposition N (PROVED) kills features independent of the next 3-adic digit. Rank-1 compression shows zero gain numerically.
6. **Litmus.** 5n+1 transfers verbatim with exponents far below 1. For 3n−1 the LP is identical but the soundness proof does not transfer.
7. The method bounds the predecessor count of each target. It never says all orbits reach one target, so cycles of the litmus maps cannot contradict it.

## (b) Statements

**Notation.** T(n) = n/2 (n even), (3n+1)/2 (n odd), on positive integers. For a ≥ 1 and real x:

    S_a(x) = { n ≤ x : T^j(n) = a for some j ≥ 0, and T^i(n) ≤ x for 0 ≤ i ≤ j },   π*_a(x) = |S_a(x)|.

This is KL 2003's π*_a(x) (§2), and it is the definition used in every computation here. "a on a cycle" means T^j(a) = a for some j ≥ 1. [3^k] is the set of residues m mod 3^k with m ≡ 2 (mod 3). For c: [3^k] → (0, ∞), c̄(r) = min_{t=0,1,2} c(r + t·3^(k−1)).

KL's lift constraints (L4), eqs. (2.12)–(2.13), print 3^k where 3^(k−1) is meant (their (2.14) has it right). Only the 3^(k−1) reading reproduces their Table 2, as kollatz also records.

Rows of L_k^NT(λ), with λ = 2^γ:

    (L1) m ≡ 2 (9):  c(m) ≤ 4^−γ c(4m) + (3/4)^γ c̄((4m−2)/3)
    (L2) m ≡ 5 (9):  c(m) ≤ 4^−γ c(4m)
    (L3) m ≡ 8 (9):  c(m) ≤ 4^−γ c(4m) + (3/2)^γ c̄((2m−1)/3)

### b1. Theorem T — PROVED

**Theorem T.** Let k ≥ 2, γ > 0, c: [3^k] → (0, ∞) satisfy (L1)–(L3), and M = max c. Then for every integer a ≡ 2 (mod 3) not on a cycle and every real x ≥ a,

    π*_a(x) ≥ c(a mod 3^k) · (x/a)^γ / (4^γ M).

**Proof.** Call (a, x) admissible if a ≡ 2 (mod 3), a is not on a cycle, and x ≥ a. S_a(x) is finite and contains a. Use strong induction on |S_a(x)| over all admissible pairs simultaneously.

*Case x < 4a.* The right side is (c(a)/M)·((x/a)/4)^γ < 1 ≤ π*_a(x).

*Case x ≥ 4a.* Let r be an integer with T^e(r) = a for some e ≥ 1 and r, T(r), …, a all ≤ x. Then:

- (F1) S_r(x) ⊆ S_a(x), by appending the segment r → … → a.
- (F2) a ∉ S_r(x); otherwise a reaches r and r reaches a in e ≥ 1 steps, putting a on a cycle. So |S_r(x)| < |S_a(x)|.
- (F3) r is not on a cycle, since a cycle through r contains a.

Apply these to r₁ = 4a (e = 2; 4a, 2a, a ≤ x) and to r₂ chosen by residue:

- a ≡ 8 (mod 9): r₂ = b := (2a−1)/3. It is an odd integer with T(b) = a, b ≡ 2 (mod 3) (since 2a−1 ≡ 6 mod 9), and 1 ≤ b < a ≤ x.
- a ≡ 2 (mod 9): r₂ = 2b = (4a−2)/3, where b ≡ 1 (mod 3) is odd, T(2b) = b, T(b) = a, 2b ≡ 2 (mod 3), and b < 2b < 4a/3 < x. (2b = a forces a = 2, which is on the cycle 1 → 2 → 1 and is excluded.)
- a ≡ 5 (mod 9): no r₂.

Since 4a ≡ a ≡ 2 (mod 3), both (r₁, x) and (r₂, x) are admissible with strictly smaller sets.

(F4) S_{r₁}(x) ∩ S_{r₂}(x) = ∅. Suppose n lies in both, with first visit times j₁ and j₂; r₁ ≠ r₂ because r₂ < 4a/3.
- If j₁ < j₂: after r₁ the orbit runs 4a, 2a, a, and r₂ ∉ {2a, a}. So the orbit visits a and later r₂, which maps back to a. Then a is on a cycle.
- If j₂ < j₁: the orbit visits r₂, then a within two steps, then r₁ = 4a, which maps back to a. Again a is on a cycle.

By (F1), (F2), (F4):   π*_a(x) ≥ 1 + π*_{4a}(x) + π*_{r₂}(x).   (*)

Apply the induction hypothesis with D := 1/(4^γ M) and m = a mod 3^k:

- π*_{4a}(x) ≥ D c(4a)(x/4a)^γ = D·4^−γ c(4m)·(x/a)^γ.
- a ≡ 8 (9): x/b = 3x/(2a−1) > (3/2)(x/a). Also b ≡ (2m−1)/3 (mod 3^(k−1)), because b − (2m−1)/3 = 2(a−m)/3. So c(b) ≥ c̄((2m−1)/3) and π*_b(x) ≥ D(3/2)^γ c̄((2m−1)/3)(x/a)^γ.
- a ≡ 2 (9): x/2b = 3x/(4a−2) > (3/4)(x/a) and 2b ≡ (4m−2)/3 (mod 3^(k−1)). So π*_{2b}(x) ≥ D(3/4)^γ c̄((4m−2)/3)(x/a)^γ.

Summing in (*) and using row (L3), (L1) or (L2) of m gives π*_a(x) ≥ D c(m)(x/a)^γ. ∎

**Corollaries.**
- (i) KL Theorem 2.2 holds with Δ₁ = 1/(4^γ M) ≥ 1/(4M).
- (ii) The bound is threshold-free: π_a(x) ≥ c(a)(x/a)^γ/(4^γ M) for all x ≥ a. For a ≡ 1 (3) use π*_a(x) ≥ π*_{2a}(x). For a = 2, the only known periodic a ≡ 2 (3), use π*_2(x) ≥ π*_8(x) ≥ c(8)(x/8)^γ/(4^γ M).
- (iii) The proof does not need λ ≤ 2. Since π* ≤ x, the theorem itself shows L_k^NT(2^γ) is infeasible for γ > 1.
- (iv) With the k = 19 certificate (M = 2782.25): π_a(x) ≥ (x/a)^0.90942/9816 for all x ≥ a and a ≡ 2 (3) not on a cycle. With k = 18 (M = 1834.56): (x/a)^0.90327/6418. No x₀ and no second certificate. Nobody else has checked this proof.

**Hostile referee notes.**
- *"Not on a cycle".* It is the right hypothesis for the proof: it is used in (F2) twice, in (F4), and to exclude 2b = a. Without it (*) is false as a set statement (for a = 2, r₂ = a). The inequality itself still holds numerically at a = 2 (min ratio 2.71) and at all cycle elements of 5n+1 and 3n−1 tested, but that is VERIFIED to bound, not proved.
- *Disjointness.* Correct; it needs r₂ ∉ {2a, a}, which holds.
- *Ratios.* (3/2)(x/a) and (3/4)(x/a) are strict lower bounds because 2a−1 < 2a and 4a−2 < 4a. This is the only place the sign of "+1" enters.
- *Well-foundedness.* KL's advanced argument y + α − 1 is harmless here, because S_b(x) ⊊ S_a(x) even though b < a.
- *Lifts.* The induction gives c at b's true residue, which is ≥ the min over lifts. The direction is correct.
- *Does it prove too much?* No. γ > 1 is impossible by (iii), consistent with the summed inequality 3(λ−1) ≤ λ^α, which fails for λ > 2.

**Brute force (VERIFIED to bound).** `src/pistar.c` enumerates the full predecessor tree with path maxima and checks every real x in [a, XMAX]. Weights are feasible in double precision at γ_k − 10^−6 for k = 2..6 (growth factor ≥ 1 + 5·10^−7).

| run (3n+1) | targets | tree nodes | min π*/bound, k = 2..6 (non-cycle) |
|---|---|---|---|
| all a ≤ 120, x ≤ 10^8 | 40 | 6.28·10^8 | 3.237, 5.046, 5.432, 6.327, 9.039 |
| all a ≤ 3000, x ≤ 10^7 | 1000 | 1.82·10^8 | 3.231, 5.033, 5.407, 6.211, 6.221 |
| all a ≤ 2·10^5, x ≤ 16a (covers x just above a and x < 4a) | 66667 | 8.4·10^6 | 3.231, 5.032, 5.407, 6.211, 6.220 |
| 334 a in [3000, 10^6], x ≤ min(65536a, 10^8) | 334 | 1.5·10^6 | 3.231, 5.032, 5.407, 6.211, 6.220 |
| 31 a in [10^6, 10^7], x ≤ 4096a | 31 | 1.0·10^6 | 3.231, 5.032, 5.407, 6.211, 6.774 |

- At a = 2 (on the cycle) the ratios are 2.707, 3.856, 4.982, 6.713, 8.066.
- All classes 2, 5, 8 mod 9 are covered.
- The minimum always sits at the first jump of π*, so the constant has a factor ≥ 3 to spare.
- Negative control: with γ = 1.5 the tester reports ratio 0.077.

### b2. Lemma G — PROVED (same proof)

Let γ > 0, M > 0, and W: {a ≡ 2 (3)} → (−∞, M] satisfy, for every a not on a cycle,

    W(a) ≤ 4^−γ W(4a) + [a ≡ 8 (9)](3/2)^γ W((2a−1)/3) + [a ≡ 2 (9)](3/4)^γ W((4a−2)/3).

Then π*_a(x) ≥ W(a)(x/a)^γ/(4^γ M). The base case uses W ≤ M. Where W(r) ≤ 0 the hypothesis is trivially true, so W need not be positive or periodic.

### b3. Proposition N — PROVED

**Proposition N.** Let W(a) = w(a mod 3^k, f(a)) with w bounded above, satisfying:

(IND) for every non-periodic a ≡ 2 (3) and every t ∈ {0,1,2} there is a non-periodic a' ≡ a (mod 3^k) with f(a') = f(a) and a' ≡ a + t·3^k (mod 3^(k+1)).

If W satisfies Lemma G's inequality at γ and W > 0 somewhere, then L_k^NT(2^γ) has a positive feasible point. So such W certify nothing beyond γ_k.

(IND) holds for f = a mod 2^j (by CRT) and for size buckets such as ⌊log₂ a⌋ mod J.

*Proof.* Put c(m) = sup{W(a) : a ≡ m (mod 3^k), a non-periodic}.
- Fix m ≡ 8 (9), ε > 0, and a with W(a) ≥ c(m) − ε. The a'_t from (IND) have W(a'_t) = W(a), and (2a'_t − 1)/3 runs through the three lifts of (2m−1)/3.
- So c(m) − ε ≤ 4^−γ c(4m) + (3/2)^γ c(lift_t) for every t. Take the min over t and let ε → 0. The case m ≡ 2 (9) is the same.
- c⁺ = max(c, 0) still satisfies the rows, because the right side is monotone and ≥ 0. It is ≥ 0 and ≠ 0.
- Let F be the right-hand-side map. From c⁺ ≤ F(c⁺), monotonicity gives c⁺ ≤ F^n(c⁺) ≤ F^(n+1)(c⁺).
- F(v)(m) ≥ 4^−γ v(4m), and m ↦ 4m is a single cycle on [3^k] (4 has order 3^(k−1)). So F^(3^(k−1))(c⁺) is strictly positive and feasible. ∎

### b4. Solver and certificates — VERIFIED (exact integer checks)

- **Lower certificate:** an integer vector w with w ≤ F_γ(w), coefficients rounded down.
- **Upper certificate:** w with F_γ(w) < w, coefficients rounded up. Then no positive feasible d exists at that γ: with s = max d/w attained at m*, d(m*) ≤ F(d)(m*) ≤ sF(w)(m*) < s·w(m*) = d(m*).
- **Arithmetic:** γ = num/2^40 exactly. 4^−γ, (3/4)^γ, (3/2)^γ are bounded by 160-bit directed-rounding integer square-root chains, cross-checked against mpmath to 1 unit in 2^64.
- **Row checks:** for k ≤ 16, all rows in Python integers from residue definitions with u64 weights. For k ≥ 17, numpy uint64 with overflow excluded a priori, u32 weights, plus a 20006-row Python-integer sample.
- **Independence:** the checker (`check_cert.py`) shares no code with the solver (`klrho.c`, `run_k.py`).
- **Negative controls:** 8 mutated certificates are all rejected.

| k | γ_lo certified feasible | γ_hi certified infeasible | λ_lo | λ_hi | KL 2003 γ_k / λ_k | kollatz λ_k float [cert feasible, infeasible] |
|---|---|---|---|---|---|---|
| 2 | 0.436588373 | 0.436588413 | 1.35340007 | 1.35340011 | 0.4365880 / 1.3534010 | – [1.3534, 1.35342] |
| 3 | 0.611262180 | 0.611262220 | 1.52759508 | 1.52759512 | 0.6112620 / 1.5275960 | – [1.5275, 1.5278] |
| 4 | 0.689108910 | 0.689108950 | 1.61228737 | 1.61228742 | 0.6891080 / 1.6122870 | – [1.6122, 1.61230] |
| 5 | 0.733579839 | 0.733579879 | 1.66275988 | 1.66275992 | 0.7335790 / 1.6627590 | – [1.6627, 1.66277] |
| 6 | 0.760818791 | 0.760818831 | 1.69445203 | 1.69445207 | 0.7608180 / 1.6944520 | – [1.6944, 1.69447] |
| 7 | 0.782568694 | 0.782568734 | 1.72019092 | 1.72019097 | 0.7825670 / 1.7201900 | – [1.7201, 1.72020] |
| 8 | 0.803196833 | 0.803196873 | 1.74496347 | 1.74496352 | 0.8031960 / 1.7449630 | – [1.7449, 1.74498] |
| 9 | 0.816831047 | 0.816831087 | 1.76153244 | 1.76153249 | 0.8168300 / 1.7615320 | – [1.7615, 1.76155] |
| 10 | 0.829546231 | 0.829546271 | 1.77712632 | 1.77712637 | 0.8295450 / 1.7771270 | – [1.7771, 1.77714] |
| 11 | 0.841756588 | 0.841756628 | 1.79223099 | 1.79223104 | 0.8417560 / 1.7922310 | – [1.7922, 1.79225] |
| 12 | 0.853136242 | 0.853136282 | 1.80642360 | 1.80642365 | – | 1.8064236 [1.8064, 1.80644] |
| 13 | 0.863005764 | 0.863005804 | 1.81882377 | 1.81882382 | – | 1.8188237 [1.8188, 1.81884] |
| 14 | 0.872452394 | 0.872452434 | 1.83077233 | 1.83077238 | – | 1.8307723 [1.8307, 1.83079] |
| 15 | 0.881248330 | 0.881248370 | 1.84196842 | 1.84196847 | – | 1.8419687 [1.8419, 1.84198] |
| 16 | 0.889266976 | 0.889267016 | 1.85223478 | 1.85223483 | – | 1.8522346 [1.8522, 1.85225] |
| 17 | 0.896601898 | 0.896621898 | 1.86167585 | 1.86170166 | – | 1.8616888 [1.8616, 1.86170] |
| 18 | 0.903278960 | 0.903298960 | 1.87031200 | 1.87033793 | – | 1.8703250 [1.8703, 1.87034] |
| 19 | 0.909427513 | 0.909447513 | 1.87830001 | 1.87832605 | – | 1.8783132 [1.8783, 1.87833] |

Float optima (secant search, not proofs): λ_17 ≈ 1.86168876, λ_18 ≈ 1.87032497, λ_19 ≈ 1.87831303.

**Reading the table.**
- *Against KL.* Their γ_k lies below my γ_lo by 1.8·10^−7 to 1.7·10^−6 at every k, consistent with a truncated lower bound. Their λ_k is inside or below my bracket except at k = 2, 3, 10, where it exceeds my certified-infeasible λ by 8.9·10^−7, 8.8·10^−7 and 6.3·10^−7. That is last-digit rounding and is immaterial to their theorem, which uses k = 11.
- *Against kollatz.* Every recorded feasible λ is below my λ_hi and every recorded infeasible λ is above my λ_lo. Their float optima agree with my search optima to ≤ 3·10^−7. Agreement at every k = 2..19.
- *Caveat.* An upper certificate proves infeasibility at that single γ. Concluding "γ_k < γ_hi" also needs feasibility to be monotone in γ. Numerically the growth factor is strictly decreasing on γ ∈ [0.05, 1.5] for k = 4, 8, 12. kollatz's `notes/strict_monotonicity.md` claims a Lean-checked proof, which I did not verify.

### b5. Litmus — maps (pn+d)/2

The generic system is in `src/gen_lp.py`. The principal class is p | 2m − d, E = ord_p(2), b = (2m−d)/p, and j is minimal with 2^j b principal:

    c(m) ≤ 2^(−Eγ) c(2^E m) + (p/2^(j+1))^γ c̄(2^j b).

For p = 3, d = 1 this second implementation reproduces γ_2..γ_6 to 9 digits.

**5n+1 — transfers verbatim (PROVED, same proof).** Here b = (2a−1)/5 < 2a/5, the constant is 1/(16^γ M), and the base case is x < 16a.
- γ_k(5) for k = 2..7 (float): 0.257795, 0.297549, 0.333237, 0.380909, 0.410576, 0.432795. These are identical to kollatz `kl5.json`.
- Brute force: 600 targets a ≤ 3000 with x ≤ 10^9, and 20000 targets a ≤ 10^5 with x ≤ 256a. Min ratio is 6.99 to 20.0 for non-cycle a and ≥ 7.3 at the nine cycle elements ≡ 3 (mod 5).
- No contradiction: the exponents are far below 1. kollatz records the LP ceiling for p = 5 as 0.650919; I did not re-derive it.
- Each cycle's predecessor set gets its own ≥ x^γ members. Nothing is said about divergence.

**3n−1 — same LP, but the proof does not transfer (REFUTED as a verbatim transfer).**
- Under m ↦ −m the rows coincide with L_k^NT; γ_k is identical to 9 digits for k = 2..6.
- But b = (2a+1)/3 > 2a/3, so x/b < (3/2)(x/a). Each odd branch loses a factor (1 + 1/(2a))^−γ.
- No affine shift a ↦ a + θ repairs both branches: the odd branch needs θ ≤ −1 and the even branch θ ≥ 0. For 3n+1 the range 0 ≤ θ ≤ 1 works.
- The fixed points of the inverse branches are 0 and +1 for 3n−1, against 0 and −1 for 3n+1. Positive integers sit on the wrong side, where the cycles 1, {5,7,10}, {17,…} live.
- Numerically the verbatim inequality still holds: min ratio 3.19 to 6.22 for non-cycle a (a ≤ 3000 with x ≤ 10^7; a ≤ 120 with x ≤ 10^8; a ≤ 2·10^5 with x ≤ 16a), and 1.43 to 2.30 at cycle elements, with the minimum at the fixed point a = 1. This is VERIFIED to bound only.
- CANDIDATE repair (not proved): Lemma G with the non-periodic W(a) = c(a)(1 − κ·u(a mod 3^k)·a^−s) for small s > 0, where u is a strict super-solution at γ + s.

### b6. Task 5 — structured non-periodic W

| construction | description size | result |
|---|---|---|
| (A) w(a mod 3^k, a mod 2^j), k = 2..5, j = 1..3 | 3^(k−1)·2^j | LP optimum equals γ_k within the 2·10^−7 bisection tolerance in all 12 cases. PROVED no gain (Prop. N). |
| (B) w(a mod 3^k, ⌊log₂a⌋ mod J), k = 2..4, J = 2, 3, 5 | 3^(k−1)·J | LP optimum equals γ_k in all 9 cases. PROVED no gain (Prop. N). |
| (C) rank-1: c_(k+j) = u(a mod 3^k)·v(next j base-3 digits), 14 pairs with k ≤ 7 | 3^(k−1) + 3^j | Best γ found equals γ_k in all 14: gain 0.000 of the available γ_(k+j) − γ_k. For j = 1, k = 2, 3, an exhaustive 4800-point log-grid over v ∈ [1,50]³ with an LP in u finds no v feasible at γ_k + 10^−4. CANDIDATE theorem "zero gain", no proof. |
| (D) variable-depth 3-adic tree | – | Not run by me. kollatz `adaptive_k12.json` records a loss at equal variable count: 50 % of the variables capture 29 % of the gain. |

**Why.** The loss in L_k^NT is the min over three lifts in the odd branch.
- A feature that does not predict the next base-3 digit cannot reduce that min (Prop. N).
- A product ansatz pays min v / max v in every odd-branch row.
- The true level-8/9 vectors are not near rank 1: log-domain singular values fall only to about 0.10, 0.09, 0.045 of the first.

## (c) Scripts

All paths are under `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/kl-exponent/`; run from there. PY = `/home/matrix/home/projects/collatz/venv/bin/python`.

- **Build.** `gcc -O3 -march=native src/klrho.c -lm -o src/klrho_d` (add `-DUSE_FLOAT` for `src/klrho_f`). `gcc -O3 -march=native src/pistar.c -lm -o src/pistar` (add `-DH32` for `src/pistar32`).
- **Search and check.** `src/run_all.sh 2 16 0.43` writes `logs/run_k2_16.log` with 30 `VERIFIED` lines in about 4 minutes. `src/run_all.sh 17 19 0.8973` writes `logs/run_k17_19.log` in about 30 minutes; k = 19 is float32 at 3.1 GB.
- **Single certificate.** `$PY src/check_cert.py cert/k19_lower` prints `VERIFIED k=19 N=387420489 mode=lower gamma=999926124816/2^40=0.9094275127 lambda=1.87830001 feasible: all rows hold`.
- **Table.** `$PY src/make_table.py` rebuilds the b4 table from the logs.
- **Checker controls.** `src/negative_controls.sh <scratch dir>` prints eight `rejected as expected` lines (`logs/negative_controls.log`).
- **Brute force.** `$PY src/gen_lp.py 3 1 $k --wfile data/w/p3d1_k$k.txt` for k = 2..6 (likewise `3 -1` and `5 1`), then `src/run_pistar.sh` and `src/run_pistar_1e8.sh`, writing `logs/pistar.log` and `logs/pistar_1e8.log`. Every min ratio must exceed 1; the smallest are 3.187 (non-cycle) and 1.425 (3n−1 fixed point).
- **Task 5.** `$PY src/nonperiodic.py` writes `logs/nonperiodic.log`. `cd src && $PY nonperiodic_c_check.py` prints "0 of 4800 grid points v feasible".
- **Old drafts.** `src/kl_solver.c` and `src/test_induction_bound.py` are superseded and were never run. `check_cert.py` was rewritten.
- **Literature fetched** (plain client name): `lit/mazur/mazur090_v2.pdf` and `.txt`.
- **Disk.** `cert/` is 4.5 GB, of which k = 17..19 weights are 4.3 GB. It is untracked and regenerable; do not commit.

## (d) Dead ends

1. **2-adic or size features in W.** Proposition N: the sup over the feature is a level-k feasible point.
2. **Rank-1 compression.** Zero gain. Alternating optimisation from random starts gets stuck at growth factors 0.76 to 0.999, worse than v ≡ 1, so do not trust local search here. The grid + LP check is the reliable one.
3. **Theorem T for 3n−1 by the same induction.** The ratio step has the wrong sign and no affine shift fixes it.
4. **Tight brackets with u32 weights at k ≥ 17.** Quantisation forces a margin of 10^−5 in γ. Tighter needs u64 weights and Python-integer rows at about 3 µs per row.
5. **Same-constant theorem for a on a cycle.** The decomposition (*) is false there; only corollary (ii) is proved.
6. **k ≥ 20.** The float32 working pair is 9.3 GB at k = 20, above the 4 GB cap.

## (e) Best lead

**Formalise Theorem T in Lean and drop the second certificate.** Target:

    ∀ k ≥ 2, γ > 0, c > 0 on [3^k] satisfying (L1)–(L3):
    ∀ a x, a % 3 = 2 → ¬periodic a → a ≤ x → c(a)·(x/a)^γ ≤ 4^γ·(max c)·π*_a(x),

by strong induction on `(S a x).card`.

- A level-k theorem then needs only the weights check, not Mazur's adaptive-potential check. kollatz records that check at 5825 s and 27.8 GB for k = 20.
- It also gives an explicit constant for all x ≥ a.

Secondary leads: prove or refute "rank-1 top-digit compression has zero gain"; prove the 3n−1 repair in b5.

## Credences

- Theorem T and Lemma G correct: 97 %.
- Absent from KL 2003 and Mazur 0.90 v2: 95 %. New to the literature at large: 50 %.
- Certificates k ≤ 19 exact as described: 99 %. Each bracket contains γ_k (needs monotonicity): 95 %.
- Proposition N: 93 %. Rank-1 zero gain is a theorem: 60 %.
- 3n−1 proof-transfer failure: 99 %. The inequality is nevertheless true for 3n−1: 85 %.