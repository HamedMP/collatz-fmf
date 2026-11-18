<!-- Saved by the coordinator from the referee-delta agent's final message (the agent's own write was refused). -->
# referee-delta: hostile review of `w2-delta/REPORT.md` section (b)

**Verdict: I could not break any statement.** One quoted constant in Theorem S is wrong but harmless. The `REPORT.md` write was refused, so this message is the report.

| statement | verdict | credence |
|---|---|---|
| Lemma 1 | SURVIVES | 99% |
| Lemma 2 | SURVIVES | 99% |
| Lemma 3 | SURVIVES | 98% |
| Theorem H (27.2) | SURVIVES | 96% |
| Theorem R (7.62 / 5.72) | SURVIVES | 94% |
| Corollary D (1.386), given 2^71 | SURVIVES | 93% |
| Theorem S (11.3·X^0.94996) | SURVIVES | 95% |
| Proposition I | SURVIVES | 99% |

**Recomputed constants (independent code, exact binomials)**
- **Theorem H:** β_all(0) = 19.37215 at s = 3, giving 27.16286.
- **Theorem R:** U = 6.37535, W_odd = 4.55068, Res ≤ 5.71188, segment ratio ≤ 7.61585.
- **M_B:** my own exhaustive run below 2^32 gives 0.225654112732 at n = 993 and P_B = 495; every n reaches 1.
- **Corollary D (levels ≥ 71):** 1.35939, 0.97906, product 1.38591.
- **Theorem S:** small-L sup is 1.60776 at L = 2; K0 must be ≥ 11.262, so 11.3 holds.
- **5n+1:** bad fractions 0.923, 0.976, 0.9998, so the proof fails there as stated.

**Numerics**
- **3n+1, n ≤ 10^7:** max harmonic sum 2.936738 (993·2^13).
- **3n−1:** max 2.4167; cycle sums 1.0, 0.4429, 0.2595.
- **3n+5:** max 2.1597 across six cycles.
- **Sojourn ratios:** at most 0.37, 0.25 and 0.27 respectively.
- **Exact checks:** Lemmas 1–2 and Proposition I on all 65,535 integers of levels 0–15; Lemma 3 and the H bookkeeping on about 108,000 (stretch, s) pairs for 3n±1, with zero violations.

**Defects (all low severity)**
1. Theorem S quotes the Chernoff constant as 3.868; it is 3.86993.
2. `s2_constants.log` holds constants from a superseded contraction factor; only its Theorem S line is used.
3. "Same constants for 3n−1" is justified for H and S, but not written out for R.

**Novelty**
- Not found in print; I put 60% on it being new, with real folklore risk since it is a short step from Terras and Lagarias.
- Lagarias 1985 bounds only the infinite-stopping-time terms of a divergent trajectory by x^0.95 (from memory; the page's formulas did not load).
- Roosendaal and Luo (arXiv:2506.23070) treat residue boundedness as conjecture.
- A recent preprint calls p = ⌈a·log2 3⌉ a conjecture and proves it only when a < 304·min, so D3 looks new.

**Not checked**
- The 2^71 verification itself.
- D4, the generation counts, and sections (d)–(f).
- A line-by-line proof for 3n−1 or 3n+d.
- Literature beyond three searches.

Everything is in `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/referee-delta/`: `r1_numerics.c`, `r2_constants.py`, `r3_exact.py`, `r5_MB.c` and their logs.