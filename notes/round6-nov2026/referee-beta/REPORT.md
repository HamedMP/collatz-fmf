# Hostile referee — w2-beta T1, T2, T3, T5, T6 (saved by the coordinator from the referee's final message; its own write was refused)

**Verdict: nothing on the review list is broken.** The short-interval headline holds as stated, but it is elementary, has no Collatz content (it holds verbatim for 5n+1), and its exponent 13.3 is second-hand.

| Statement | Verdict | Credence |
|---|---|---|
| Lemma G | SURVIVES | 0.99 |
| Theorem G, G1 | SURVIVES | 0.99 |
| G2 | SURVIVES | 0.98 |
| Headline | SURVIVES | 0.90 (0.99 with some exponent) |
| T6c | FIXABLE: two true one-way statements, not an equivalence | 0.95 each |
| T2 | SURVIVES as conditional (derivation) | 0.88 |
| T1 | SURVIVES | 0.97 |
| T3 | SURVIVES after defect 3's repair | 0.95 |
| T5a | SURVIVES | 0.98 |

**Headline as proved:** for every real x ≥ 3 some n ∈ (x, x(1 + C(log x)^(−1/13.3))] reaches 1. C is explicit in principle but not computed; it rests on Rhin's (7) via Mazur's quotation, which gives ‖q·log2 3‖ ≥ (2^(−13.3)/ln 2)·q^(−13.3).

## Tests
- Lemma G: exhaustive backward tree, 8442 cases, 0 failures.
- G2 construction: 720 exact cases, x up to 2^2000, all inside the interval and reaching 1.
- Three-gap bound: g_D < 2/q holds for every D tested.

## Defects
1. Minor, T6c: the "equivalence" is trivial at k = 0, and the forward direction lands in windows with d ≈ k/2, outside k ≥ 4d. "Cannot give θ < 1" is heuristic.
2. Minor, T5b second sentence: BROKEN (unproved); it takes a countable union of density-zero sets.
3. Cosmetic, T2/T3: P(a) for even a and the classes F_m are not eventually Syracuse-invariant as stated (21 ∈ P(16), Syr(21) = 1). Adjoining the odd part repairs both.
4. Cosmetic: Lemma T2.1 stays an unproved sketch; Tao's Prop. 1.11 no-hit bound is citable instead.

## Novelty
Folklore-level; one search found no prior statement. Holds verbatim for 5n+1, so no bearing on Collatz. It literally answers the 23 Aug 2026 blog question (h ≪ x/(log x)^C, with C = 1/13.3) without the density theorems.

## Not checked
Rhin in the primary, Mazur's proofs and Lean, the value of C, T4, T5c, basin numerics.

Scripts: `lemmaG_brute.py`, `g2_construct.py` in this directory.
