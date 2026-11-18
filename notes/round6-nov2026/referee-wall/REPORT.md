<!-- Saved by the coordinator from the referee-wall agent's final message (the agent's own write was refused). -->
**Verdict: the theorems and both main exponents (0.0913, 0.0650) survive. Remark 5 is broken, and Remark 2 has wrong thresholds.** The write of `referee-wall/REPORT.md` was refused, so this message is the report.

| Statement | Verdict | Credence |
|---|---|---|
| Lemma 5 | SURVIVES (worst ratio to bound 0.08, j ≤ 14) | 99% |
| Lemma 6 | SURVIVES (exact, n ≤ k ≤ 40) | 99% |
| Prop. F | SURVIVES (8,288 instances, κ ≤ 26) | 98% |
| Thm A′ | SURVIVES | 95% |
| Thm B′, Cor. B1′ | SURVIVES | 94% |
| Cor. C′, seeds | SURVIVES | 93% |
| Remark 3 | SURVIVES as a heuristic ceiling | 85% |
| Remark 2 | FIXABLE | 90% |
| Remark 5 | BROKEN | 95% |
| Prop. G numerics | SURVIVES | 97% |

**Defects**
1. **Remark 5 (major for the roadmap, harmless to the theorems).** It assumes windows need R ≤ √K. But (SGP) at window R gives the pointwise bound |T_k(ξ)| ≤ C·R·2^(v₂(ξ)/2)·N_k^(1−δ₀), since all terms are non-negative. With R = 2^(k^(1−c)) the loss is subexponential, so Lemma 4 at k = K gives m ≍ Q. w3-fp0's "m ≤ Q^(c′)" was true and understated; w4's correction is wrong. Summary items 1 and 5, the gap table and lead (e) inherit this.
2. **Remark 2 (minor).** Thresholds should be c > 1.46 (ρ ≥ 2) and c > 0.59 (down to ρ = 1.27), not 2.3 and 0.29. The conclusion stands.
3. **Cosmetic.** 11.1 × 6.5 = 72.15 > 72, though the sharper 11.03 gives 71.7. Exact log exponents are 0.183, 1.183, 0.842.
4. Theorem A′'s explicit bound exceeds 1 below K ≈ 3·10⁹, so only its proof chain was testable.

**Prop. G.** My recursion matches direct sums for k ≤ 26. The dip is confirmed, though at k = 200 it bottoms at n/k = 0.62.

| k | 0.1 | 0.5 | 0.63 | 0.7 | min δ | window δ₀ |
|---|---|---|---|---|---|---|
| 200 | 0.449 | 0.210 | 0.155 | 0.533 | 0.097 | 0.126 |
| 400 | 0.463 | 0.174 | 0.085 | 0.467 | 0.085 | 0.099 |

**Litmus.** E′_k = −E_k for k ≤ 30; nothing asserts emptiness.

**Not checked.** The 0.0555 limit, k ≥ 1600 rows, denominator-11 and beam-search claims, Remark 1's literature, the 5n+1 control, `n7_compare.py`.

Scripts and outputs are in `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/referee-wall/` (`w1_lemma5.py` through `w4_litmus.py`, `w1_out.txt` to `w3_out.txt`).