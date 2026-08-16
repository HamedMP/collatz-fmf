# Computational Diagnostics Companion

This note explains the repository's verification scripts for readers checking
the FMF manuscript. The scripts are supporting diagnostics. They verify algebra,
finite certificates, and exploratory frontiers used by the paper; they do not
prove the Collatz conjecture or the missing unweighted terminal-window theorem.

## Recommended Commands

Run the current smoke snapshot with:

```bash
bash scripts/verify_snapshot.sh quick
```

Run the full recorded snapshot with:

```bash
bash scripts/verify_snapshot.sh full
```

The full snapshot was last run successfully on May 14, 2026. Its exact command
list is recorded in `proof-obligations.md`.

The submission packaging script also extracts the finished archive and runs a
small representative diagnostic smoke test from that archived copy. This checks
that the bundle closes over the helper modules needed by the packaged scripts.

## Diagnostic Groups

| Group | Scripts | Evidence provided |
| --- | --- | --- |
| Binary return and reduced-gap algebra | `explore52_binary_partial_map.py`, `explore60_backward_branches.py` | Checks the partial maps, survival densities, backward branches, reset neighborhoods, and moment-contraction formulas used in Sections 6--8. |
| Terminal-window and rank formulations | `explore62_terminal_windows.py`, `explore64_terminal_ranks.py`, `explore66_terminal_zero_digits.py`, `explore69_window_shells.py` | Checks that low prefix residues match normalized terminal windows, verifies finite terminal-depth/rank profiles, and records weighted/shell evidence. |
| Rank-bound frontier | `explore81_rank_bound_frontier.py` | Reports the finite constants required by the conjectured unweighted return and gap terminal-window bounds through the recorded bit cutoffs. The default scan covers `B=2^60-1`; `--extended` also checks the slower `2^64-1` cutoff. |
| Periodic and bounded-alphabet branches | `explore68_periodic_branches.py`, `explore70_bounded_alphabet_minima.py`, `explore72_bounded_alphabet_beam.py` | Checks periodic exclusions and finite `{0,1}` minima/profiles; the beam search is heuristic evidence, not a proof. |
| Aperiodic and balanced templates | `explore71_aperiodic_templates.py`, `explore73_balanced_frontier.py`, `explore74_mechanical_landing.py`, `explore75_mechanical_recurrence.py`, `explore76_template_recurrence.py` | Checks finite evidence and recurrence witnesses for balanced, mechanical, and named automatic-style templates. |
| Uniform morphism frontier | `explore77_uniform_morphism_recurrence.py`, `explore78_uniform_morphism_symbolic_witness.py`, `explore79_q9_boundary.py`, `explore80_q9_boundary_residues.py` | Supports the small-uniform-morphism exclusions, records the residual q=9 reduced-gap recurrence boundary, and checks prefix-residue growth along that specific morphic word. |
| Paper build and hygiene | `typst compile`, `scripts/check_site_links.py`, `pdftotext`, `git diff --check` | Confirms the manuscript builds, local site links resolve, key rendered text, front-matter labels, expected section numbers, Theorem A--D labels, and endpoint labels are present, and edited files have no whitespace errors. The Git hygiene check runs only inside a Git worktree, so unpacked submission archives skip it. |

## July 2026 Attack-Round Artifacts (notes/)

The July 19--21, 2026 multi-agent rounds preserved their verification scripts
under `notes/round4-july2026/` and `notes/round5-july2026/`. These are NOT part
of `scripts/verify_snapshot.sh`; they are finite machine checks supporting the
Section 23 theorems of `proof.md` (or, in one case, a candidate manuscript).

- `notes/round4-july2026/s5-completion/` (`sA`--`sE`): checks for the
  **candidate** Theorem ND manuscript `PROOFS.md` (joint mixing identity,
  phased Section-7 majorant, Lemma R renewal-equidistribution, end-to-end
  assembly, max-mass lemma). These support an AI-proved, AI-refereed draft
  awaiting human review; they establish no repository claim.
- `notes/round4-july2026/lemma-e-attack/` (`lea01`--`lea04`): finite checks
  for the hop-word factor barrier and depth-`{0,1,2}` threshold
  `3/log2(41/16) = 2.20986`, the `(s,v)` block-map invariant table, the LP
  no-go for statistical forms of Lemma E, and the depth hierarchy.
- `notes/round4-july2026/complexity-pincer/` (`s1`--`s3`): checks the
  full-shift ambient-language mechanism, beam-minimizer complexities, and the
  sharpened thresholds `T_R' = 3.2439007`, `T_G' = 6.3942268`.
- `notes/round5-july2026/h1-two-prime/` (`s1`--`s4`): machine verification of
  the Mirror Equivalence Lemma (2184 words, both `a = 3` and `a = 5`), the
  survival/kill census over `10^6` seeds, and Theorem V vacuity
  (398,480 checks, 0 violations).
- `notes/round5-july2026/lemma-e-arithmetic/` (`lar01`--`lar04`): checks the
  cocycle and master identity, the reset/Wronskian law, the transported
  hierarchy thresholds, and the spike-ledger boundary.

What these artifacts do and do not establish: the round-4/5 scripts are finite
evidence accompanying the results recorded in `proof.md` Section 23 (Theorems
58--62 and related: Theorems 59 and 62 refereed x2, Theorems 60 and 61 proved
negative results with machine-verified certificates but not separately
refereed, Theorem 58 candidate-only) and the referee records in each round
directory; none of them proves H1, Lemma E, or pointwise descent, and the
`s5-completion` scripts in particular support only a candidate result that is
not a repository claim until human review.

## What The Scripts Do Not Establish

- They do not prove pointwise FMF descent for every odd `x > 1`.
- They do not prove the uniform return count
  `W_R(B,L) <= C(B+1)(2/15)^L`.
- They do not prove the uniform reduced-gap count
  `W_G(B,L) <= C B 112^(-L)`.
- The finite rank-frontier scan records worst cases through selected height
  cutoffs only; it does not bound all `B,L`.
- They do not turn density-zero exceptional sets into empty exceptional sets.
- They do not replace a proof of the higher-complexity nonperiodic landing
  exclusion.

The current mathematical endpoint is recorded in `proof-obligations.md`: prove
the two lemmas of the refereed two-lemma reduction — H1 (no infinite positive
return orbit, requiring a position-aware, non-class-counting arithmetic
argument) and Lemma E (eventual depth-`{0,1}` structure of non-descending
orbits, requiring arithmetic rather than letter statistics).
