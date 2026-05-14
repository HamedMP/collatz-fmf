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

## Diagnostic Groups

| Group | Scripts | Evidence provided |
| --- | --- | --- |
| Binary return and reduced-gap algebra | `explore52_binary_partial_map.py`, `explore60_backward_branches.py` | Checks the partial maps, survival densities, backward branches, reset neighborhoods, and moment-contraction formulas used in Sections 6--8. |
| Terminal-window and rank formulations | `explore62_terminal_windows.py`, `explore64_terminal_ranks.py`, `explore66_terminal_zero_digits.py`, `explore69_window_shells.py` | Checks that low prefix residues match normalized terminal windows, verifies finite terminal-depth/rank profiles, and records weighted/shell evidence. |
| Periodic and bounded-alphabet branches | `explore68_periodic_branches.py`, `explore70_bounded_alphabet_minima.py`, `explore72_bounded_alphabet_beam.py` | Checks periodic exclusions and finite `{0,1}` minima/profiles; the beam search is heuristic evidence, not a proof. |
| Aperiodic and balanced templates | `explore71_aperiodic_templates.py`, `explore73_balanced_frontier.py`, `explore74_mechanical_landing.py`, `explore75_mechanical_recurrence.py`, `explore76_template_recurrence.py` | Checks finite evidence and recurrence witnesses for balanced, mechanical, and named automatic-style templates. |
| Uniform morphism frontier | `explore77_uniform_morphism_recurrence.py`, `explore78_uniform_morphism_symbolic_witness.py`, `explore79_q9_boundary.py`, `explore80_q9_boundary_residues.py` | Supports the small-uniform-morphism exclusions, records the residual q=9 reduced-gap recurrence boundary, and checks prefix-residue growth along that specific morphic word. |
| Paper build and hygiene | `typst compile`, `pdftotext`, `git diff --check` | Confirms the manuscript builds, key rendered text, expected section numbers, Theorem A--D labels, and endpoint labels are present, and edited files have no whitespace errors. |

## What The Scripts Do Not Establish

- They do not prove pointwise FMF descent for every odd `x > 1`.
- They do not prove the uniform return count
  `W_R(B,L) <= C(B+1)(2/15)^L`.
- They do not prove the uniform reduced-gap count
  `W_G(B,L) <= C B 112^(-L)`.
- They do not turn density-zero exceptional sets into empty exceptional sets.
- They do not replace a proof of the higher-complexity nonperiodic landing
  exclusion.

The current mathematical endpoint remains the same as in
`proof-obligations.md`: prove an unweighted pointwise counting,
height-separation, or 2-adic landing theorem strong enough to rule out infinite
positive return and reduced-gap partial-map orbits.
