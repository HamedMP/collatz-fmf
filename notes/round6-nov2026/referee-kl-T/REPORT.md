# Hostile referee — kl-exponent Theorem T, Lemma G, Proposition N (saved by the coordinator from the referee's final message; its own write was refused)

**Verdict.** T: SURVIVES (98%). G: FIXABLE, trivial (96%). N: FIXABLE, trivial (93%). **T's statement is not new; only the proof and the constant 4^γ are.**

## Numerics (referee's own code)
Own LP reproduces KL Table 2 for k = 2, 3, 4 (γ = 0.436588, 0.611262, 0.689109). All a ≡ 2 (3), a ≤ 5000, x ≤ 4·10^6, at and just before every jump, 8·10^7 tree nodes, 31 weight vectors: no violation.
- Minimum ratio: 2.31 (k=2, γ=0.131, a=4997, x→6662⁻). Near-optimal γ: 3.23. For x ≥ 4a: 6.00.
- a = 2 (cycle): still holds, minimum 2.19.
- γ > 1: rows infeasible at γ ∈ {1, …, 10}, k = 2..5.
- 5n+1: proof transfers (checked by hand); γ_k = 0.257795, 0.297549, 0.333237; minimum 6.58.
- 3n−1: same γ_k; ratio step fails since b = (2a+1)/3 > 2a/3, as reported. Numerically holds: 2.65 non-cycle, 1.43 at a = 1.

## Proof of T
Every step checked (base case, F1–F4, admissibility, residue claims, ratios, summation, well-foundedness); no gap found.

## Defects
- G (minor): the ratio step needs W(r) ≥ 0. Repair: if W(r) ≤ 0, use π*_r ≥ 0. Quantifiers (a non-periodic, x ≥ a) are missing.
- N (minor): "W > 0 somewhere" must be at a non-periodic a. The (IND) examples assume every class mod 2^j·3^(k+1) contains a non-periodic integer; asserted, not proved.
- Citation (cosmetic): in the KL TeX the misprint is at (2.13)–(2.14); (2.15) is correct. The printed (L4) is equivalent, not a different LP.
- Novelty overclaim (moderate): KL Theorem 2.2 already gives φ_k^m(y) ≥ c·λ^y/(4·max c) for all y ≥ 0, explicit and threshold-free. T improves 4 to 4^γ and drops λ ≤ 2. The proof is genuinely different: KL use back-substitution trees, LP transfer and induction in y; T inducts directly on |S_a(x)|.

## Not checked
Mazur's paper, the kollatz Lean source, certificates for k ≥ 5, sections b4 and b6, literature beyond KL 2003.

Scripts and outputs are in this directory.
