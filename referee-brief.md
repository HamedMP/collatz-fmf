# Referee Brief

This note is a review handoff for the FMF Collatz manuscript. It states what an
external reader should check, what is being claimed, and what is explicitly not
being claimed.

## Requested Review Scope

Please review the manuscript as a density-and-reduction paper, not as a proof of
the Collatz conjecture.

The most useful independent checks are:

1. Verify the FMF hop algebra in Sections 2 and 5.
2. Verify the natural-density normalizations in Sections 3--5.
3. Verify that the binary return and reduced `{0,1}` gap reductions in Sections
   6--8 are exact equivalences, not heuristic models.
4. Check that every use of computation is finite verification or diagnostic
   support, never a substitute for a universal theorem.
5. Check that Section 9 accurately states the remaining pointwise gap.

## Defensible Claims

The manuscript may claim:

- Exact First-Multiple-of-Four odd-to-odd hop formulas.
- A natural-density state distribution theorem from 2-adic unit structure.
- A fractional-moment contraction statement in the natural-density model.
- The Quartering Law for strict growth-B continuations.
- Existence of arbitrarily long finite growth-B shadows.
- Exact binary-depth return and reduced `{0,1}` gap partial-map reductions.
- Terminal-window, weighted-window, shell, and cutoff estimates for the first
  bounded-depth obstructions.
- Exclusion of periodic, finite-defect, low-complexity, balanced/Sturmian, and
  several small automatic/uniform-morphic obstruction templates.

## Claim Matrix

| Claim | Where to audit | What to check | Limitation to keep explicit |
| --- | --- | --- | --- |
| Exact FMF odd-to-odd hop formulas | Sections 2 and 5 | The Type A/Type B split, hop length, and output formulas cover every odd input and agree with the standard Collatz map. | Algebraic exactness does not by itself imply descent. |
| Natural-density state laws | Sections 3--4 | The sample space is odd starts in residue boxes, and the 2-adic inverse counts produce the stated distribution and fractional moment. | These are density-model statements, not independence along a fixed orbit. |
| Quartering Law | Section 5 | Conditional on already being in a growth-B hop, each further strict growth-B continuation imposes exactly one quarter of the remaining odd starts. | Density decay does not rule out an exceptional integer trajectory. |
| Finite growth-shadow construction | Section 5 | The all-zero branch gives arbitrarily long finite strict growth-B shadows. | This blocks finite forbidden-pattern proofs; it is not evidence for divergence. |
| Binary return reduction | Section 6 | The return-code congruences, partial map, critical-series landing criterion, and terminal-window identities are equivalent formulations. | The reduction leaves the unweighted rank/landing theorem open. |
| Reduced `{0,1}` gap reduction | Section 7 | The complete-gap survival density is `112^-L` and the gap partial map preserves ordinary-integer landing in both directions. | Gap merging and terminal multiplicity are not yet uniformly controlled. |
| Endpoint dichotomies | Section 8 | Any remaining bounded-depth obstruction is forced into the stated higher-complexity landing or reset-spike alternatives. | These dichotomies cover the first bounded-depth obstruction classes, not arbitrary mixed FMF epochs. |
| Template exclusions | Sections 6--8 | Periodic, finite-defect, low-complexity, balanced/Sturmian, and listed uniform-morphic branches are excluded by stated recurrence or compactness arguments. | The exclusions are class theorems, not a theorem for all aperiodic finite-alphabet words. |

## Claims To Reject

The manuscript should not be accepted as claiming:

- A proof of the Collatz conjecture.
- Pointwise descent for every odd integer.
- Independence along an individual deterministic trajectory.
- Empty exceptional sets from density-zero estimates.
- Universal theorems from finite verifier output.
- A theorem stronger than Tao's almost-all result without qualification.

## Main Gap To Check

The remaining proof target is the unweighted terminal-window/rank theorem. A
Collatz proof through the current framework would need, at minimum, uniform
bounds of the form

```text
W_R(B,L) <= C(B+1)(2/15)^L
W_G(B,L) <= C B 112^(-L)
```

or a different pointwise theorem strong enough to rule out infinite positive
binary return and reduced-gap partial-map orbits. The current paper proves
weighted, shell, cutoff, periodic, low-complexity, and template exclusions, but
not this unweighted theorem.

## Files To Read First

- `site/paper/collatz-fmf.pdf`: rendered manuscript.
- `publication-readiness.md`: claim-boundary and submission audit.
- `proof-obligations.md`: completion checklist and missing theorem inventory.
- `submission-checklist.md`: source package, command, and claim-boundary gates.
- `diagnostics.md`: what the verifier scripts do and do not establish.
- `review.md`: critical review of the proof framing.

## Verification Commands

The quick smoke snapshot is:

```bash
bash scripts/verify_snapshot.sh quick
```

The full recorded snapshot is:

```bash
bash scripts/verify_snapshot.sh full
```

The full snapshot was last run successfully on May 14, 2026. Passing these
commands supports the algebra, reductions, finite certificates, paper build,
and diagnostic frontier stated in the repository notes. It does not prove the
missing pointwise Collatz theorem.

## Review Questions

- Are the FMF formulas and type splits correct for every odd input?
- Are the density calculations normalized over the intended sample spaces?
- Do the binary return and reduced-gap maps preserve ordinary-integer
  equivalence in both directions?
- Do the terminal-window identities exactly match the least prefix residues?
- Are the weighted and shell estimates stated with their correct limitations?
- Does any theorem accidentally infer pointwise behavior from density or Haar
  measure?
- Is the remaining rank/landing theorem stated sharply enough to guide future
  work?
