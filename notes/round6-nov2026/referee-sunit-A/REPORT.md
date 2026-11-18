# Hostile referee — sunit Theorem A (saved by the coordinator from the referee's final message; its own write was refused)

**Verdict: SURVIVES.** Credence that Theorem A is correctly proved, taking Evertse 1984 Cor. 1 as published: 0.97.

## Checked
1. Identity derived before reading the proof; matches Lemma 2. The hop is the s-fold Syracuse map; verified numerically.
2. Evertse hypotheses, read from `sunit/lit/page04.png` and `page03.png` (‖x‖ = max|x_k|): quotation is accurate.
   - Integrality: H_{i+1} − s_0 ≥ 1; H_i + s_i − s_0 is 0 at i = 0 (entry 3^(σ_0)) and ≥ 1 otherwise.
   - gcd: 3^(σ_0) and 2^(H_k−s_0) are real entries; for k = 1 they are 1 and −2^(h_0−s_0).
   - Subsums: valuation list right, single tie at the bottom; argument holds whether or not the tie pair is split; uses no signs.
   - (12): free parts multiply to at most m_0·m_k; the ‖x‖ inequality is used in the right direction.
3. Deduction re-derived line by line (Lemma 3, S_k ≤ T−k−1, choice of η). Finite-to-one holds: m_0 divides N = 3^(S_k)·m_0 and s_0 ≤ log_3 N.
4. Brute force: all 500,000 odd x_0 < 10^6, k = 1, 2, 3 — sum, gcd, all 2^(2k+2) subsums, (12), Lemma 3 — zero failures. 425 adversarial inputs at k ≤ 5 also pass.
5. Counter-families: none found (deep s < 1500 with m < 400: max T−L_0 = 20/26/32 for k = 1/2/3; 2-adic lattice solve: best T/L_0 = 1.155 at L_0 > 80).
6. Not trivial, not vacuous; a routine S-unit application.

## Defects
- Cosmetic: the finite-to-one sentence should say "m_0 | N" ((S_k, m_0) is not unique when 3 | m_0).

## Not checked
Evertse's own proof and Schlickewei's theorem; B3 onward; x_0 > 10^6 exhaustively; prior art; no formalisation.

Scripts: `brute.py`, `attack.py`, `out_a.txt`, `out_b.txt` in this directory.
