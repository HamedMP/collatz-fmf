# Hostile referee — frontier Theorem A, Cor. A1, Lemma L, Theorem B, Cor. B1–B3, Prop. D (saved by the coordinator from the referee's final message; its own write was refused)

**Verdict: nothing broken.** All eight statements survive; two wording defects.

| item | verdict | credence |
|---|---|---|
| Theorem A | SURVIVES | 99% |
| Cor. A1 | SURVIVES | 98% |
| Lemma L | SURVIVES | 99% |
| Theorem B + finite form | SURVIVES | 98% |
| B1 | SURVIVES | 97% |
| B2 | FIXABLE (wording) | 97% |
| B3 | SURVIVES | 95% |
| Prop. D | SURVIVES | 98% |

## Defects
- B2, minor: "includes binary S-adic words" is false unless B(X_t) → ∞. For c→c, d→dc repeated, the first block stays c. Repair: require first-block length → ∞.
- D, minor: proved only for gcd(m,6) = 1.
- Cosmetic: (1.1) is the integer fact 3B(v) ≥ 4e(v); B3 needs a finite alphabet.
- Significance: B is not vacuous but excludes nothing observed. It bites only when B(X) > 2.305·log₂(w₀+1); for w₀ < 2^64 the whole-prefix B/log₂(w₀+1) peaks at 1.515. Longest itinerary there: 26 letters (w₀ = 13260338733143908048).

## Checks (exact arithmetic, 0 violations throughout)
- Residue class: confirmed for all 510 words of length ≤ 8.
- B finite form: 45,000 cases, also with w₀ ≡ 32 (mod 33); min log₂(w₀+1)/B(X) = 1.6548.
- Lemma L: case split complete, including k = ∞ and j = ∞; positions and inequalities correct. Brute force over 191 shapes × ρ grid plus threshold rationals.
- Theorem A: 418,338 instances, 74,874 overlapping. Overlap is allowed; the itinerary must reach i'+|u|, as stated.
- B chain: integer form re-derived; Lemma L supplies B(u) ≥ B(X).
- B1, B3, A1: B1 has no degenerate gap; Justin shape held in 1,888 instances; 3.9741 correct.
- D: commutator −11/128; m < 500 orbit structure as claimed.
- Litmus: genuine. 5n+1 fails because 5^9 > 2^16 (T = 1.349 < 3). 3n−1 fails only through non-growth at fixed point w = 1, which is the −5 cycle.

## Novelty
A is Theorem 46's barrier (acknowledged). A1 is Theorem 60 renormalised. Lemma L is the one new idea, absent from Theorems 46, 47, 51, 60. The claim is fair but modest.

## Not checked
The 1+√3 remark, the complexity example, Theorem C onward, Obstruction O, the author's scripts, plan.md and earlier rounds, outside literature.

Scripts and logs: `r1_sim.py`, `r2_lemmaL.py`, `r3_rest.py`, `r1.log`–`r3.log` in this directory.
