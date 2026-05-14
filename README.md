# First-Multiple-of-Four Coordinates for Collatz Growth Chains

Density bounds and pointwise obstruction reductions via First-Multiple-of-Four (FMF) decomposition.

## Key Results

- **Theorem A (FMF Step Formula):** Exact algebraic formulas for hop length and output value
- **Theorem B (State Distribution):** Hop output distributions are input-state independent in natural density via 2-adic inverse structure
- **Theorem C (Fractional-Moment Contraction):** E[R^0.53] ~= 0.8638 < 1 from exact asymptotic 2-adic formulas
- **Theorem D (Quartering Law):** Growth chain continuation has density factor 1/4, giving 4^-k decay among odd starts
- **Pointwise obstruction reductions:** The binary-depth return obstruction is reduced to an explicit return-code partial map with survival density (2/15)^L; the reduced {0,1} gap obstruction has survival density 112^-L.
- **Main contribution:** Elementary natural-density bounds and exact reductions for isolated FMF growth mechanisms. This is not a proof of Collatz.

## Honest Assessment

The "almost all to all" gap remains open. There are infinitely many finite growth-shadow starts, but no nonconvergent exception is known. This is a frontier problem in p-adic dynamics.

See `proof-obligations.md` for the completion verdict, verified artifacts, and the exact missing pointwise theorem.

## Structure

```
paper/          Typst source for the paper
site/           GitHub Pages website
explorations/   Python exploration and verifier scripts
lemma-roadmap.md proof-status roadmap and missing pointwise bridge lemmas
review.md       critical review and repaired theorem framing
proof-obligations.md checklist of what remains for a complete proof
publication-readiness.md submission audit and claim-boundary checklist
```

## Building

```bash
typst compile paper/main.typ site/paper/collatz-fmf.pdf
```

## Verification

The current verifier snapshot is listed in `proof-obligations.md`.

## License

CC BY 4.0
