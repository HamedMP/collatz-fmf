# Collatz FMF Proof Obligations

This audit records what would be required for the FMF program to become a proof of Collatz, what is already established in the repository, and what remains missing.

## Completion Verdict

Objective: prove Collatz through the FMF framework by producing all required lemmas and closing the pointwise descent gap.

Status: **not complete**.

| Required deliverable | Evidence currently in repo | Verdict |
| --- | --- | --- |
| Exact FMF algebra | Paper Sections 2--5 and verifier scripts | Complete |
| Density and average-contraction theorems | Paper Sections 3--5 | Complete as density/average statements |
| Pointwise descent for every odd `x > 1` | No theorem currently proves this | Missing |
| No infinite positive binary return orbit | Reduced to terminal-window/rank and 2-adic landing problems | Missing |
| No infinite positive reduced `{0,1}` gap orbit | Reduced to terminal-window/rank and 2-adic landing problems | Missing |
| Uniform unweighted terminal-window counting | Weighted, shell, and cutoff estimates proved | Missing at natural-rate unweighted strength |
| Verification support | Core verifier snapshot below | Supporting evidence only |

The repository now contains a rigorous reduction and a strong package of density, terminal-window, weighted, shell, and obstruction lemmas. It does not contain a proof of Collatz because the pointwise unweighted rank/landing theorem is still absent.

## Prompt-to-Artifact Checklist

| User-requested deliverable | Concrete artifact/evidence | Coverage |
| --- | --- | --- |
| Criticize the proof | `review.md`; this file's missing-obligations table | Covered: identifies the pointwise/rank gap and rejects density-only completion |
| Improve the proof | Section 5 lemmas; `lemma-roadmap.md` entries 11e.*; verifier scripts | Partially covered: many obstruction classes are now excluded or reduced |
| Come up with all needed lemmas | `lemma-roadmap.md` plus Section 5 propositions | Incomplete: the terminal-window/rank and higher-complexity landing lemmas are still missing |
| Prove Collatz through FMF | No artifact proves pointwise descent for every odd `x > 1` | Missing |
| Verify algebra and reductions | `explorations/explore52_*` through `explorations/explore76_*`; Typst compile | Supporting evidence only, not a replacement for the missing universal theorem |
| Decide what to do next | Practical Next Target below | Covered: higher-complexity finite-alphabet exclusion and unweighted terminal-window counting are the next targets |

## Success Criteria

A completed proof must establish all of the following.

1. For every odd `x > 1`, some finite FMF iterate is smaller than `x`.
2. The descent statement must be pointwise over ordinary positive integers, not merely a natural-density or Haar-measure statement.
3. The proof must rule out sustained growth-B obstructions, including bounded nonperiodic 2-adic codes and unbounded reset-spike orbits.
4. The proof must handle recovery after mixed growth and shrinkage phases, not only termination of the strict growth-B submechanism.
5. All computational scripts must be supporting verification only; no finite search may be treated as proof of a universal statement.

## Established Artifacts

| Requirement | Current evidence | Status |
| --- | --- | --- |
| Exact FMF hop formulas | `paper/sections/02-fmf-formulas.typ` | Proved |
| Natural-density state distribution | `paper/sections/03-state-independence.typ` | Proved as density, not trajectory independence |
| Fractional-moment contraction | `paper/sections/04-contraction.typ` | Proved as average contraction |
| Quartering Law | `paper/sections/05-quartering-law.typ` | Proved as natural-density decay |
| Arbitrarily long finite growth shadows | `paper/sections/05-quartering-law.typ`, `paper/sections/06-gap-analysis.typ` | Proved; prevents finite maximum-chain arguments |
| Binary return-code reduction | `paper/sections/05-quartering-law.typ`, `lemma-roadmap.md` | Proved reduction |
| Reduced `{0,1}` gap-code reduction | `paper/sections/05-quartering-law.typ`, `lemma-roadmap.md` | Proved reduction |
| Periodic branch exclusion | `explorations/explore68_periodic_branches.py`, Section 5 | Proved for the formal branch families |
| Terminal-window formulation | `explorations/explore62_terminal_windows.py`, Section 5 | Proved |
| Terminal depth bounds | `explorations/explore64_terminal_ranks.py`, Section 5 | Proved; fixed terminal states have only logarithmically bounded depth |
| Terminal rank, weighted, shell, and low-expansion window bounds | `explorations/explore64_terminal_ranks.py`, `explorations/explore69_window_shells.py`, Section 5 | Proved, but weighted/shell/cutoff only; high-expansion low-window words remain open |
| Backward branch and moment contraction | `explorations/explore60_backward_branches.py`, Section 5 | Proved for the reduced systems |
| Reset-spike and finite reset-neighborhood transparency | `explorations/explore52_binary_partial_map.py`, Section 5 | Proved |
| Fixed-count positive-label and finite-defect periodic-shadow strata | Section 5, `lemma-roadmap.md` | Proved divergent for both return and reduced-gap least residues |
| Fixed low-factor-complexity binary strata | Section 5, `lemma-roadmap.md` | Proved divergent for both return and reduced-gap least residues via Morse-Hedlund plus prefix compactness |
| Balanced/Sturmian-like binary frontier | Section 5, `lemma-roadmap.md` | Proved excluded: rational slopes are periodic, while irrational lower mechanical/Sturmian landings would require delayed prefix recurrences contradicted by the standard Sturmian recurrence function |
| Automatic and small uniform morphic binary templates | Section 5, `lemma-roadmap.md`, `explorations/explore77_uniform_morphism_recurrence.py`, `explorations/explore78_uniform_morphism_symbolic_witness.py` | Thue-Morse, period-doubling, and binary 2-, 3-, 4-, 5-, and 6-uniform fixed-point templates are excluded; larger uniform morphisms remain diagnostic |
| Prefix-language compactness principle | Section 5, `lemma-roadmap.md` | Proved as reusable reduction from bounded restricted minima to an ordinary infinite code |
| Honest non-proof framing | `README.md`, `review.md`, `paper/sections/06-gap-analysis.typ` | Present |

## Missing Obligations

| Missing item | Needed statement | Why current artifacts do not cover it |
| --- | --- | --- |
| Pointwise FMF descent | Every odd `x > 1` has an FMF iterate below `x` | Density and average contraction do not exclude exceptional integer orbits |
| Growth-B termination or stronger epoch recovery | A pointwise `O(log x)` bound for growth/recovery epochs | Finite tests and density decay do not imply universal termination |
| Binary return partial-map termination | No infinite positive orbit of the return map `T(n)` | Periodic, sparse, low-complexity, and balanced branches are excluded; higher-complexity nonperiodic binary orbits remain open |
| Reduced `{0,1}` gap partial-map termination | No infinite positive orbit of the gap map `G(a)` | Same unresolved higher-complexity nonperiodic 2-adic landing obstruction |
| Higher-complexity ordinary landing exclusion | No higher-complexity nonperiodic finite-alphabet word has an ordinary return or reduced-gap code | The balanced/Sturmian frontier, Thue-Morse/period-doubling templates, and binary 2-, 3-, 4-, 5-, and 6-uniform morphic fixed points are now excluded, but general higher-complexity aperiodic words remain open |
| Uniform return counting | `N_R(B,L) <= C(B+1)(2/15)^L` for all `B,L` | Current pressure and zeta bounds are weighted, not rank bounds |
| Uniform gap counting | `N_G(B,L) <= C B 112^(-L)` for all `B,L` | Gap merging is structured but still not uniformly counted |
| Terminal-window separation | A mechanism turning terminal escape into unweighted low-window counts | Backward moment contraction alone is empirically insufficient |
| High-expansion low-window control | A bound for low-window words with large `E_w` | Current return and gap bounds become unweighted only after imposing an expansion cutoff |
| Gap multiplicity control | A sharp bound for the number of gap words landing at each low terminal state | Current weighted and cutoff bounds control merging, but not strongly enough to imply the linear natural-rate rank theorem |
| Unbounded reset-spike exclusion | A contradiction for balanced real-height spikes with repeated `3`-adic resets | Finite reset neighborhoods preserve the dyadic prefix densities |

## Current Sharp Endpoint

The strongest current reduction is:

- A bounded obstruction must be a genuinely non-eventually-periodic finite-alphabet word whose restricted least-prefix minima fail to diverge, whose factor complexity is strictly above the balanced Sturmian frontier, whose nonzero labels occur infinitely often in the `{0,1}` cases, whose binary low-complexity strata with `p_w(m) <= m` already diverge, whose balanced sublinear-density factor-window strata already diverge, whose balanced rational-slope branch is excluded, and whose itinerary has unbounded edit distance from every eventually periodic template. The balanced/Sturmian subcase is now excluded by the fast prefix-recurrence argument, the Thue-Morse and period-doubling templates are excluded by explicit automatic prefix recurrences, and all binary 2-, 3-, 4-, 5-, and 6-uniform morphic fixed-point templates are excluded by finite classification plus recurrence criteria. This remains far short of a general automatic-sequence theorem. Symbolic-prefix diagnostics cover q=7 and q=8, but q=9 leaves a concrete reduced-gap boundary case, `0->011111111, 1->100000000`, with best checked symbolic recurrence ratio `17/2` and negative gap margin through a targeted recurrence scan to prefix length `50,000`. Any remaining binary landing must satisfy the prefix-recurrence height barrier tying recurrence times and early symbol counts to the prefix modulus; in particular, no infinitely recurring prefix subsequence may have ratio below the density-free cutoffs, and any class satisfying the sharper density-recurrence exclusion inequality is ruled out.
- An unbounded obstruction must be a reset-spike orbit: incoming real height tends to infinity along long labels, while the following state converges to `-85/88` in the return system or `-1/128` in the reduced gap system.
- Fixed terminal states cannot support arbitrarily deep prefixes; terminal depth is logarithmic in terminal height. The unresolved issue is uniform breadth/rank across terminals, and merge multiplicity in the reduced gap system.
- Weighted terminal-window estimates are now available on both sides, fixed expansion shells have ordinary weighted-to-count bounds, and low-expansion windows have ordinary cutoff counts. These do not yet control the high-expansion low-window words needed for the unweighted rank theorem.

Thus the next proof obligation is not another density calculation. It is an unweighted pointwise counting, height-separation, or 2-adic landing theorem.

The existing cutoff estimates do not have the right asymptotic shape by themselves: the smallest possible expansion still grows exponentially in `L`, while the desired survivor rates decay exponentially. A proof must therefore exploit arithmetic separation of normalized terminal heights, not only terminal escape or expansion size.
The shell estimates make the same point in another coordinate: converting inverse-expansion mass into ordinary counts costs a factor exponential in the shell index.
Fixed expansion shells occur only at bounded prefix depth, so an infinite obstruction must pass through arbitrarily high shells.

## Practical Next Target

The most concrete target remains the terminal-window counting theorem:

`W_R(B,L) <= C(B+1)(2/15)^L`

and

`W_G(B,L) <= C B 112^(-L)`.

Proving these would settle the fixed-height return and reduced-gap obstructions. Failure to prove them should be treated as the main unresolved mathematical gap, not as a documentation or verification issue.

Smaller bounded-alphabet subtargets:

- Return: prove `mu_L^(<=1) -> infinity`, where `mu_L^(<=1)` is the least return-prefix residue among length-`L` words over return lengths `{0,1}`.
- Reduced gap: prove `nu_L^(<=1) -> infinity`, where `nu_L^(<=1)` is the least gap-prefix residue among length-`L` words over zero-gap lengths `{0,1}`.

These subtargets would not prove the full theorem, but they are the first genuinely nonconstant finite-alphabet cases after constant and eventually periodic branches have been excluded.

The current finite `{0,1}` minimizers are sparse in `1` labels. The fixed-count sparse strata are now proved harmless: for each fixed `J`, the least residues among words with at most `J` positive labels diverge in both the return and reduced-gap systems. More generally, bounded-defect perturbations of any eventually periodic template are proved harmless, and fixed low-factor-complexity strata `p_w(m) <= m` diverge by compactness plus Morse-Hedlund. The balanced-prefix minima are now removed from the obstruction list: any balanced counterexample reduces to a lower mechanical Sturmian word, but the Sturmian recurrence function gives fast prefix recurrences that contradict the delayed recurrence forced by an ordinary landing. The remaining `{0,1}` problem is therefore sharper: rule out higher-complexity aperiodic binary codings with uniformly positive-density labels, no fixed periodic shadow, and prefix recurrences that evade the density-recurrence exclusion inequality.

Suggested attack order:

1. Generalize from balanced/Sturmian `{0,1}` words to higher-complexity uniformly positive-density aperiodic binary words.
2. Generalize from `{0,1}` to each fixed finite alphabet `{0, ..., R}` or `{0, ..., K}`.
3. Upgrade finite-alphabet divergence to the full unweighted terminal-window rank theorem.
4. Use the rank theorem to close the fixed-height return/gap obstructions, then connect that back to pointwise FMF descent.

## Verification Snapshot

Full snapshot last checked on May 14, 2026 with:

- `bash scripts/verify_snapshot.sh full`

The commands below are packaged in `scripts/verify_snapshot.sh`. The default
`quick` mode runs the core algebra/reduction checks and paper compile; `full`
also runs the longer frontier scans listed later in this section.

- `python3 explorations/explore52_binary_partial_map.py`
- `python3 explorations/explore60_backward_branches.py`
- `python3 explorations/explore64_terminal_ranks.py`
- `python3 explorations/explore66_terminal_zero_digits.py`
- `python3 explorations/explore68_periodic_branches.py`
- `python3 explorations/explore69_window_shells.py`
- `python3 explorations/explore70_bounded_alphabet_minima.py`
- `python3 explorations/explore70_bounded_alphabet_minima.py --profile-ones 18`
- `python3 explorations/explore70_bounded_alphabet_minima.py --profile-ones 19`
- `python3 explorations/explore70_bounded_alphabet_minima.py --profile-ones 20`
- `python3 explorations/explore70_bounded_alphabet_minima.py --profile-ones 21`
- `python3 explorations/explore71_aperiodic_templates.py --length 1024`
- `python3 explorations/explore73_balanced_frontier.py`
- `python3 explorations/explore74_mechanical_landing.py`
- `python3 explorations/explore75_mechanical_recurrence.py`
- `python3 explorations/explore76_template_recurrence.py`
- `python3 explorations/explore77_uniform_morphism_recurrence.py`
- `python3 explorations/explore77_uniform_morphism_recurrence.py --q 4 --max-power 4 --search-factor 16`
- `python3 explorations/explore77_uniform_morphism_recurrence.py --q 5 --max-power 4 --search-factor 16`
- `python3 explorations/explore77_uniform_morphism_recurrence.py --q 6 --max-power 3 --search-factor 16`
- `python3 explorations/explore78_uniform_morphism_symbolic_witness.py`
- `python3 explorations/explore78_uniform_morphism_symbolic_witness.py --q 7 --search-length 8192`
- `python3 explorations/explore78_uniform_morphism_symbolic_witness.py --q 8 --search-length 8192`
- `python3 explorations/explore78_uniform_morphism_symbolic_witness.py --q 9 --max-prefix-symbols 18 --search-length 40000`
- `python3 explorations/explore79_q9_boundary.py`
- `python3 explorations/explore72_bounded_alphabet_beam.py --max-length 120 --beam-width 2000 --report-every 20`
- `typst compile paper/main.typ site/paper/collatz-fmf.pdf`
- `pdftotext site/paper/collatz-fmf.pdf /tmp/collatz-fmf.txt`
- `rg -n "Expansion-Shell Count" /tmp/collatz-fmf.txt`
- `git diff --check`

Scope: these commands verify the algebraic reductions, periodic exclusions, reset-neighborhood transparency, terminal-window/rank formulations, weighted and shell estimates, mechanical normal-form recurrences, recurrence-speed diagnostics, template recurrence diagnostics, uniform-morphism recurrence diagnostics, and finite diagnostic frontiers currently used by the paper. The q=5 and q=6 uniform-morphism theorems are now proved in Section 5 by finite classification; `explore78` verifies the q=6 symbolic-prefix witness table that repairs the pure-power diagnostic failure, records clean q=7 and q=8 diagnostics, and isolates the first q=9 reduced-gap boundary case. `explore79` confirms that this residual q=9 case has no successful symbolic-prefix gap witness through length `50,000`. These commands do not verify the missing pointwise Collatz descent theorem or the unweighted terminal-window counting theorem.
