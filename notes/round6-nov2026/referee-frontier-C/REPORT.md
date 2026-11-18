# Hostile referee — frontier Lemma G, Theorem C, Corollaries C0, C1 (saved by the coordinator from the referee's final message; its own write was refused)

**Verdict: none of the four statements could be broken.** Lemma L was taken as given (refereed separately in `../referee-frontier-AB/`).

| Statement | Verdict | Credence |
|---|---|---|
| Lemma G | SURVIVES | 99% |
| Theorem C | SURVIVES (given Lemma L) | 97% |
| Corollary C0 | FIXABLE | 95% after repair |
| Corollary C1 | SURVIVES (proof is a sketch; gaps fill) | 93% |

## Defects
1. C0 (minor): under-specified. Repair: require S^m(π) ∈ {X,Y}^ω starting with X, then apply Theorem C to x_m.
2. C1 (minor): needs, and has: fixed point starts with c; both level-t block densities tend to θ; for θ < log₃2, uniform frequencies plus x_{m+N} ≤ 2^(−δN)·x_m + C_N; uniform recurrence for "π periodic". Gelfond–Schneider is cited correctly; E_∞ < ∞ and "no non-descent" check out.
3. Theorem C (cosmetic): the case of a non-positive coefficient is omitted (trivial since x₀ ≥ 2). The 0.86187 threshold rests on Lemma L's √3 remark.
4. Evidence (moderate): tests on 2-adically lifted seeds have no power, because x₀ ≈ 2^N makes the inequality trivial. It held on 5.3M pairs even without non-descent. The frontier report's 14,788 / 28,652 cases look like this kind.
5. Scope: the hypotheses are conjecturally unsatisfiable; the bound has content only for x₀ < 2^(|X|(1−3g)).

## Checks run (exact integers)
- Lemma G: x₀ < 10^5, n ≤ 400: 347,842 instances, 0 violations; indices and direction right.
- Theorem C chain: Terras modulus exactly 2^|u| (0 failures both directions); Lemma G applied at both i and i'.
- Strongest finite form (any repeated factor): 0 violations for 3x+1 (x₀ ≤ 2·10^5), 5x+1, 7x+1 and negative x₀. Only 204 of 2.27M pairs for 3x+1 have 2^L > x₀; tightest slack 0.006 bits.
- Litmus: the 5n+1 cycle through 13 and x₀ = −5, −17 all land in the periodic branch.

## Novelty
Elementary (Terras, growth bound, repetition) and shallow, but not vacuous as a conditional. One search found no prior statement; arXiv 2101.12747 lists the rational-parity-vector analogue as open.

## Not checked
Lemma L's proof, `frontier/f5_general_collatz.py`, literature beyond one search.

Scripts: `r1_lemmaG.py`, `r2_finite.py`, `r3_small.py` in this directory.
