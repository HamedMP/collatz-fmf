# Hostile referee — w2-gamma Lemma 1, Theorems R, S, B, A, Prop. B2, Lemma C2 (saved by the coordinator from the referee's final message; its own write was refused)

**Verdict: nothing broken. Two statements need small repairs (Theorem A Corollary 2 and Lemma C2).**

| Statement | Verdict | Credence |
|---|---|---|
| Lemma 1 | SURVIVES | 99% |
| Theorem R | SURVIVES | 99% |
| Theorem S + Corollary | SURVIVES | 99% |
| Remark for this repo | H1 part SURVIVES; Lemma E sentence unproved | 97% / 50% |
| Theorem B | SURVIVES | 99% |
| Proposition B2 | SURVIVES (trivial) | 99% |
| Lemma 2, Theorem A, Corollary 1 | SURVIVES | 97% |
| Theorem A Corollary 2 | FIXABLE | 95% after repair |
| Lemma C2 | FIXABLE | 90% after repair |

## Defects
1. Lemma C2 (moderate). Koksma is applied to {ℓ_0+iθ}, but the points are {ℓ_0+iθ+δ_i}; points within δ of 1 wrap and raise 2^(−t) from 1/2 to 1. Repair: add an error term (δ + 2D_K)/2. Since δ ≤ K·log2(1+1/(3X0)), the "10^-6 for all K ≥ 10^9" claim fails once K exceeds about 10^-6·X0. It holds for the table's candidates. "Optimal for size-only arguments" is asserted, not proved.
2. Theorem A Corollary 2 (minor). With A = Z_2 ∩ Q, T(−1/3) = 0, so S_A sends a positive integer to 0; it is a map on N_0, not N → N.
3. Remark (minor). The H1 claim holds in both directions for a ≥ 3. "Everything sits in Lemma E" assumes the repo's Theorem 55 reduction transfers to S_a, which is not shown.

## Checks run
- Theorem R, finite form: on {1..N} the solution is unique and equals T for every tested N from 4 to 64.
- (III) is sharp on both sides: S ≤ 2n+1 admits T + 2^a on the class −1 mod 2^(a+1); n ≤ S admits S_a.
- Theorem S: confirmed on all pairs below 2^14 for a ≤ 10.
- Theorem B: seven instances recomputed exactly.
- Theorem A: independent test with A = Z passes.
- Eliahou: K = 72,057,431,991, L = 114,208,327,604 reproduced.

## Novelty
Two searches found no such statement; Theorem R is likely new but elementary.

## Not checked
Hercher comparisons, observed S_a cycle lists, the 3n+d scan, disproof-search numbers, `barrier_check.py`, `cper_scan.py`.

Scripts: `bf_R.py`, `check_SB.py`, `check_AC.py`, `check_A.py` in this directory.
Sources consulted: Bernstein–Lagarias (The 3x+1 conjugacy map); Lagarias bibliography II (arXiv math/0608208); arXiv 1206.0553; arXiv 1102.5547.
