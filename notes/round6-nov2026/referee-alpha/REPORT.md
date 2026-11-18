# Hostile referee — w2-alpha Theorems 1–4, 6, Propositions 5, 8 (saved by the coordinator from the referee's final message; its own write was refused)

**Verdict: nothing broken. All seven statements survive, four with wording repairs; none is progress on H1 (the w2-alpha report says so itself).**

| Statement | Verdict | Credence |
|---|---|---|
| Thm 1 | SURVIVES | 99% |
| Thm 2 | FIXABLE: (iv) must state the gate `w ≡ −d (mod 8)` | 98% |
| Thm 3 | SURVIVES | 98% |
| Thm 4 | FIXABLE: restate the quantifier | 97% |
| Prop 5 | FIXABLE: count identity needs a convention | 96% |
| Thm 6 (implication) | SURVIVES | 98% |
| Prop 8 | SURVIVES ("Hence" skips a convergent-sum step) | 95% |

## Checked independently
- Counts: N_k by brute force to k = 22 and by set recursion to k = 64; recursion holds from k = 4; s = 0.2877608; max N_k/2^{sk} = 1.638.
- θ-identity: exact on 1.28M periodic steps and 3000 random integer-start words; γ_R ≤ 1; every rational of height ≤ 400 with life ≥ 400 bits lies in [−1,0]; integers only 0, −1.
- Dilation: E_d = d·E mod 2^16 for seven d; both −115 cycles verified exactly.
- Hull: ⟨27⟩ gives exactly {5,7 mod 8} for m ≤ 12; all 10-bit windows occur.
- Mirror identity: 0 failures on all 1040 words with Q ≤ 33.
- Thm 6 parameters: valid for Q ≤ 399.

## Defects
1. Medium, Thm 2(iv): E_d = d·E is false with the literal gate `w ≡ 7 (mod 8)`; the gate must be `w ≡ −d (mod 8)`.
2. Medium, the −115 example: 27 → 16 → 27 is a cycle of the w-system only. Assuming w = 33n+32d, 27 is not of that form, so no integer 3n−115 orbit is shown. It does lie in the class w ≡ −d (mod 11).
3. Low, Thm 4: "Φ(E) cannot imply" should read "no theorem valid for all compact X with Φ(X) = Φ(E)". Only reflection carries it. Bucket reflection is off by one at boundaries.
4. Low, Prop 5: N(Q,m) holds only with completed-step lives (≤ 3-bit slack). "Verbatim for 3n−1/5n+1" is overstated.
5. Low, Thm 3: covers digit-reading hulls only (both reading directions); not all possible uses of Shmerkin–Wu.

## Novelty
Thm 1–2 are standard (Lagarias, Bernstein–Lagarias). Thm 4 is trivial but worth one ledger line. Thm 3 is elementary and worth recording.

## Not checked
Shmerkin/Wu hypotheses against the papers, FP beyond Q' = 56, Prop 7, the 5n+1 and 3-adic hulls beyond small cases.

Scripts: `step1.py`, `check2.py`, `check3.py` in this directory.
