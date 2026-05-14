# First-Multiple-of-Four Coordinates for Collatz Growth Chains

Density bounds and pointwise obstruction reductions via First-Multiple-of-Four (FMF) decomposition.

## Key Results

- **Theorem A (FMF Step Formula):** Exact algebraic formulas for hop length and output value
- **Theorem B (State Distribution):** Hop output distributions are input-state independent in natural density via 2-adic inverse structure
- **Theorem C (Fractional-Moment Contraction):** E[R^0.53] ~= 0.8638 < 1 from exact asymptotic 2-adic formulas
- **Theorem D (Quartering Law):** Growth chain continuation has density factor 1/4, giving 4^-k decay among odd starts
- **Pointwise obstruction reductions:** The binary-depth return obstruction is reduced to an explicit return-code partial map with survival density (2/15)^L; the reduced {0,1} gap obstruction has survival density 112^-L.
- **Main contribution:** Elementary natural-density bounds and exact reductions for isolated FMF growth mechanisms. This is not a proof of Collatz.

## Claim Boundary

The "almost all to all" gap remains open. There are infinitely many finite growth-shadow starts, but no nonconvergent exception is known. In the current formulation, the sharp endpoint is a 2-adic terminal-window/rank problem.

See `proof-obligations.md` for the completion verdict, verified artifacts, and the exact missing pointwise theorem.

## Structure

```
paper/          Typst source for the paper
site/           GitHub Pages website
explorations/   Python exploration and verifier scripts
diagnostics.md  companion note explaining verifier scope and limitations
lemma-roadmap.md proof-status roadmap and missing pointwise bridge lemmas
review.md       critical review and repaired theorem framing
proof-obligations.md checklist of what remains for a complete proof
publication-readiness.md submission audit and claim-boundary checklist
referee-brief.md external-review handoff for algebra and reduction checks
proof.md       historical research log; not the current manuscript
plan.md        historical exploration log; early claims are superseded
critic.md      historical literature/context review of the research log
```

## Building

```bash
typst compile paper/main.typ site/paper/collatz-fmf.pdf
```

## Verification

The current verifier snapshot is listed in `proof-obligations.md`. See
`diagnostics.md` for a reader-facing guide to what each script group verifies
and what remains outside computational coverage.

```bash
bash scripts/verify_snapshot.sh quick
```

Use `bash scripts/verify_snapshot.sh full` for the longer frontier checks.

## License

CC BY 4.0

## Citation

Citation metadata is provided in `CITATION.cff`. Please cite the project as a
density-and-reduction manuscript, not as a proof of the Collatz conjecture.
