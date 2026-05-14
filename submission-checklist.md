# Submission Checklist

This checklist is for preparing the FMF manuscript as a density-and-reduction
preprint. It is not a checklist for claiming a proof of the Collatz conjecture.

## Submission Positioning

- Title: `First-Multiple-of-Four Coordinates for Collatz Growth Chains:
  Density Bounds and Pointwise Obstruction Reductions`.
- Scope: elementary FMF coordinates, natural-density growth-chain bounds, and
  exact reductions of the first bounded-depth pointwise obstructions.
- Non-claim: no proof of pointwise Collatz convergence is included.
- Main mathematical gap to state in every submission channel: the unweighted
  terminal-window/rank theorem is open.

## Files To Include

| Artifact | Path | Submission role | Gate |
| --- | --- | --- | --- |
| Rendered manuscript | `site/paper/collatz-fmf.pdf` | Primary PDF | Must be rebuilt from `paper/main.typ` immediately before submission |
| Typst source | `paper/main.typ`, `paper/sections/*.typ`, `paper/lib/*.typ` | Reproducible source package | Must compile with the same command listed below |
| Bibliography | `paper/refs.bib` | External references | Check that every cited claim has a corresponding entry |
| Citation metadata | `CITATION.cff` | Repository citation | Must describe the project as a density-and-reduction manuscript |
| Proof obligations | `proof-obligations.md` | Completion verdict and missing theorem inventory | Must still say `Status: **not complete**` unless pointwise descent is proved |
| Publication audit | `publication-readiness.md` | Submission risk ledger | Must distinguish preprint readiness from Collatz-proof readiness |
| Referee brief | `referee-brief.md` | External review handoff | Must list exact checks and limitations |
| Diagnostics guide | `diagnostics.md` | Verifier scope | Must state that scripts do not prove Collatz |

## Pre-Submission Commands

Run the quick verifier before any draft circulation:

```bash
bash scripts/verify_snapshot.sh quick
```

Run the full verifier before archival submission or after structural manuscript
changes:

```bash
bash scripts/verify_snapshot.sh full
```

Both commands support the algebra, reductions, finite certificates, paper build,
and diagnostic frontier. Neither command verifies the missing pointwise theorem.

## Claim-Boundary Checks

Before submission, search the public-facing files for overclaiming:

```bash
rg -n "proof of the Collatz|solves Collatz|solution to Collatz|stronger than Tao|replacement for Tao" \
  README.md publication-readiness.md submission-checklist.md referee-brief.md proof-obligations.md paper site
```

Acceptable matches should either reject those claims or describe them as missing
requirements. Any positive claim of a Collatz proof must be removed unless a new
pointwise descent theorem has been added and independently checked.

## Referee Request

Ask the first external reviewer to check the manuscript in this order:

1. FMF hop formulas and Type A/Type B coverage.
2. Natural-density normalizations and sample spaces.
3. Binary return and reduced `{0,1}` gap partial-map equivalences.
4. Terminal-window identities and weighted/shell estimates.
5. Section 9 gap statement: density zero must not be used as pointwise
   exclusion.

Do not ask for a review of a claimed Collatz proof unless
`proof-obligations.md` has been updated with a proved pointwise descent theorem.

## Remaining Major-Prize Gate

A major-prize-level Collatz result through the current framework would require
a theorem implying:

> For every odd `x > 1`, some finite FMF iterate is smaller than `x`.

The most concrete current route is still to prove uniform unweighted bounds

```text
W_R(B,L) <= C_R(B+1)(2/15)^L
W_G(B,L) <= C_G B 112^(-L)
```

and then propagate the resulting fixed-height obstruction exclusions through
arbitrary growth-B and mixed recovery epochs.
