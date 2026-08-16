# Round 4 (July 21, 2026) — Preserved Artifacts

Multi-agent session artifacts, preserved from the session scratchpad. Provenance
and claim status:

## s5-completion/ — Theorem ND candidate manuscript

`PROOFS.md` (571 lines): a complete claimed proof of the **natural-density
upgrade of Tao's theorem** (arXiv:1909.03562, Thm 1.3): the set
{N : Col_min(N) > N0} has upper natural density <= C·log^(-1/25) N0; hence
Col_min(N) <= f(N) for almost all N in NATURAL density, for every f -> infinity.
Includes a proof of the object of Tao's Remark 1.16 (fine-scale mixing of the
entire affine map (S_n, X_n)), which Tao described as "plausibly attainable
from the methods in this paper."

**STATUS: candidate theorem — NOT established mathematics.** Produced by an AI
agent and adversarially reviewed by two independent AI referees (both
NOT-REFUTED, minor findings; every Tao citation verified against the local
arXiv v7 text; all 5 verification scripts pass). It has NOT been reviewed by a
human expert. Treat exactly as an unrefereed preprint draft. Do not cite as a
theorem. The natural next step is review by a human analytic number theorist.

Scripts: sA (joint mixing identity), sB (phased Section-7 majorant),
sC (Lemma R renewal-equidistribution), sD (end-to-end assembly, log included),
sE (max-mass lemma).

**Human-referee package:** `s5-completion/REFEREE-PACKAGE.md` — exact
statement + roadmap, Tao dependency table, risk-ranked checklist, script
index, and provenance cover note. Start there.

Note on paths: PROOFS.md and the referee records cite session-scratchpad
artifacts that are NOT preserved in this repo — the local Tao source copy
(`../tao-natural-density/tao_v7.txt`; fetch arXiv:1909.03562v7 instead),
the prior-round `verify_s5.py`/`verify_s4.py`, and the referee stress
scripts. Everything load-bearing that survives is either in this directory
or summarized in proof.md (Theorems 50, 56, 58).

## lemma-e-attack/ — Lemma E partial results

Hop-word factor barrier; depth-{0,1,2} complexity threshold 2.20986;
complete invariant table for (s,v) block maps (depth-2 analogue of Lemma P:
32(49m'+1) = 81(49m+1), invariant 7^2); reduction R_2; LP no-go for any
statistical quantitative form of Lemma E. Refereed x2: load-bearing content
confirmed by both; one side clause (LE1(c)) requires a one-line repair
(trivial-cycle carve-out) — see referee record.

## complexity-pincer/ — negative result + sharpened thresholds

The direct pincer is provably impossible (ambient language of both coding
systems is the full shift; any complexity upper bound would need H1 itself).
Salvage: sharpened effectivized thresholds T_R' = 3.2439007, T_G' = 6.3942268
(pointwise, density-coupled; genuinely 3-dependent — vacuous at a >= 4).

## full-claims-and-referee-records.txt

Complete structured outputs of all three attack agents and all referee
verdicts for this round.

See plan.md (Phase 9, "July 21 round 4") and proof.md (Section 23) for the
session log, and proof-obligations.md for the repository's vetted claim
boundary (which this round does NOT change until human review).
