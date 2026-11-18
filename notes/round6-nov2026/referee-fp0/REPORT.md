<!-- Saved by the coordinator from the referee-fp0 agent's final message (the agent's own write was refused). -->
**Verdict: nothing broke.** Every statement survives; the defects are cosmetic. The explicit Theorem B inequality is vacuous (RHS > N_K) for all Q below about 10^35, so only its proof chain could be tested. The write of `referee-fp0/REPORT.md` was refused, so this message is the report.

| Statement | Verdict | Credence |
|---|---|---|
| Lemma 1 | SURVIVES (exact, K ≤ 40, all k ≥ 7, all m ≤ k−3, plus the T identity) | 99% |
| Lemma 2 | SURVIVES (q ≤ 3000, 73 values of D) | 98% |
| Lemma 3 | SURVIVES (κ ≤ 14, every h) | 99% |
| Lemma 4 | SURVIVES (κ ≤ 12, every m, λ, τ) | 98% |
| Theorem B | SURVIVES | 96% |
| Cor. B1 | SURVIVES | 94% |
| Cor. C and seeds bound | SURVIVES | 93% |
| Theorem A | SURVIVES | 95% |
| Prop. D implication | SURVIVES (bookkeeping only) | 85% |
| Prop. E | SURVIVES (relative error 3e−15, K ≤ 30) | 99% |

**Constants confirmed**
- c₁: min U_60..63 = 0.28972; measured max M√q/W = 5.14.
- 4.47 + 2.37κ re-derived by hand.
- 1.2 ≤ N_j·2^(−sj) ≤ 1.64 holds for j ≥ 4 (it fails at j = 0 and 3, which are never used).
- 3.7 (B1) and 6.2 (Theorem A) hold on a grid Q = 2^22..2^4000.
- 8 and 13 (Cor. C): 7.71 and 12.63.
- s(1−s)/4 = 0.05124; 1−s = 0.712; m* ≥ 1 from Q = 2^108.
- Concrete table: 0.9359 (Q = 10⁴) and 0.8812 (Q = 10⁵) reproduced in exact integer arithmetic.
- `f1_count`: my own counter matches all 39 values at Q = 96.

**Theorem B chain at admissible parameters** (Q = 96, m = 1..4, k = 7..15): |N − 2^(−m)N_K| ≤ 4808, against Σ_v F ≈ 0.6–0.8·N_K and an RHS of 800–180,000·N_K. All inequalities point the right way. The range m ≤ ½log₂Q − 8 does come from needing 2^k ≪ √Q.

**Defects (all minor)**
1. Theorem B is first non-trivial near Q ≈ 10^37; Cor. C beats the trivial 1.64·2^(sQ) only from roughly Q ≈ 10^45–10^50.
2. Lemma 2: the proof gives 2·max, not 3; observed ≤ 1.
3. Lemma 3 also needs the case h ≡ 0 mod 2^κ for Theorem A; it holds trivially.
4. The necessity remark is imprecise: T_K(2^(K−j)h′) also depends on lift multiplicities. The conclusion is right.
5. The data note omits N(3,3) = 2.

**Litmus.** The 3n−1 system has two infinite points (0 and 1) at Q = 40 and 64. All bounds are upper bounds ≥ 2^(−m)N_K, and none asserts emptiness.

**Novelty.** Two searches found no matching statement. The method (Parseval over a multiplier orbit plus a local limit theorem) is standard, so this is probably new but a modest log-power result.

**Not checked.** Counts at Q = 104 and 112, the 5n+1 system, the SGP and large-K tables, the Q ≥ 10⁶ rows of the concrete table, and Prop. D beyond its parameters.

Scripts and outputs are in `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/referee-fp0/` (`r1_basic.py` through `r6_concrete.py`, `r1_out.txt`, `cnt_3p1_Q96.txt`).