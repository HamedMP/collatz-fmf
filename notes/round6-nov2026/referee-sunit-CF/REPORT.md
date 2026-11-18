# Hostile referee — sunit Corollary B, Theorem D, Corollary C, Theorems E, F (saved by the coordinator from the referee's final message; its own write was refused)

**Verdict: nothing broke.** All statements survive, conditional on Theorem A (taken as given here; refereed separately in `../referee-sunit-A/`) and Evertse 1984 Corollary 1.

| Statement | Verdict | Credence (given A) |
|---|---|---|
| Corollary B | SURVIVES | 0.97 |
| Theorem D | SURVIVES | 0.96 |
| Corollary C | SURVIVES | 0.95 |
| Theorem E | SURVIVES | 0.94 |
| Theorem F | SURVIVES | 0.93 |
| F's corollary | SURVIVES (proof missing in the report; referee only sketched it) | 0.88 |

## Checked
- Quantifiers: k (or s) and δ are fixed before the base point slides; in C, k depends on ρ only. No hidden k → ∞.
- Corollary C: arithmetic redone; the B6 threshold r^(k+1) > θ is exact.
- Lemma 3: proved by hand and checked exactly on 1,019,950 hops.
- Theorem E: stated rate and e^{o(j)} follow; the θ^j comparison is honest.
- Theorem F: Evertse quote exact; identity, valuations, subsums, gcd, inequality chain re-derived and brute-forced on 20,458 tuples (0 ≤ n ≤ 10^6, s ≤ 3).
- Sanity: x = 1 not excluded; no tension with 2^n − 1, the 5n+1 cycle at 13, or 3n−1 cycles.

## Defects (all minor)
1. B6 cites Theorem 60 for hop words, but it is stated for return/gap codings; the hop-word full shift needs its one-line argument.
2. F's "equivalently R_W ≥ c·Q_W^(1−ε)" holds only after re-parametrising ε.
3. Corollary C undersells D, which also excludes spikes interleaved with small depths.
4. B7 for d ≠ 1: Lemma 3 may pick up an additive constant, changing D's limsup constant; verified only for d = 1.
5. "PROVED" should read "modulo Theorem A and Evertse"; everything is ineffective.

## Not checked
Theorem A, Lemma 4, Evertse's proof, the return map's link to Collatz dynamics, "sharp" in Theorem 62, prior art, the sunit data scans.

Files: `check_cf.py`, `check_cf.out` in this directory.
