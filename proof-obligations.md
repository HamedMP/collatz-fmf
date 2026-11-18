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
| Make the paper publication-ready | `paper/main.typ`, `site/paper/collatz-fmf.pdf`, `README.md`, `publication-readiness.md`, `submission-checklist.md`, `referee-brief.md`, and `diagnostics.md` | Partially covered: the package is presentable as a density-and-reduction preprint, but not as a Collatz proof; external referee review is still needed before broad circulation |
| Produce an important mathematical contribution | Paper Sections 2--8; Sections 6--8 endpoint reductions; verifier snapshot | Covered as a candidate contribution: exact FMF coordinates, sharp density laws, terminal-window reductions, and obstruction-class exclusions |
| Make it potentially fit a major prize | This file, `publication-readiness.md`, and the missing-obligations table below | Not covered: a prize-level Collatz result would require closing pointwise descent or an equivalent universal theorem |
| Solve Collatz completely if possible | No artifact proves pointwise descent for every odd `x > 1` | Missing |
| Criticize the proof | `review.md`; this file's missing-obligations table | Covered: identifies the pointwise/rank gap and rejects density-only completion |
| Improve the proof | Sections 5--8 lemmas; `lemma-roadmap.md` entries 11e.*; verifier scripts | Partially covered: many obstruction classes are now excluded or reduced |
| Come up with all needed lemmas | `lemma-roadmap.md` plus Sections 5--8 propositions | Incomplete: the terminal-window/rank and higher-complexity landing lemmas are still missing |
| Prove Collatz through FMF | No artifact proves pointwise descent for every odd `x > 1` | Missing |
| Verify algebra and reductions | Packaged verifier scripts from `explorations/explore52_*` through `explorations/explore81_*`, plus their helper modules; Typst compile | Supporting evidence only, not a replacement for the missing universal theorem |
| Decide what to do next | Practical Next Target below | Covered: the two lemmas of the refereed two-lemma reduction (H1 via position-aware arithmetic counting, Lemma E via the valuation-coincidence route) are the next targets |

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
| Arbitrarily long finite growth shadows | `paper/sections/05-quartering-law.typ`, `paper/sections/09-gap-analysis.typ` | Proved; prevents finite maximum-chain arguments |
| Binary return-code reduction | `paper/sections/06-binary-return-codes.typ`, `lemma-roadmap.md` | Proved reduction |
| Reduced `{0,1}` gap-code reduction | `paper/sections/07-reduced-gap-codes.typ`, `lemma-roadmap.md` | Proved reduction |
| Periodic branch exclusion | `explorations/explore68_periodic_branches.py`, Sections 6--8 | Proved for the formal branch families |
| Terminal-window formulation | `explorations/explore62_terminal_windows.py`, Sections 6--7 | Proved |
| Terminal depth bounds | `explorations/explore64_terminal_ranks.py`, Sections 6--7 | Proved; fixed terminal states have only logarithmically bounded depth |
| Finite rank-bound frontier | `explorations/explore81_rank_bound_frontier.py` | Diagnostic through `B=2^60-1`, with an optional `2^64-1` spot check: current finite constants peak at about `4.456` for return and `9.631` for gap; not a uniform theorem |
| Terminal rank, weighted, shell, and low-expansion window bounds | `explorations/explore64_terminal_ranks.py`, `explorations/explore69_window_shells.py`, Sections 6--7 | Proved, but weighted/shell/cutoff only; high-expansion low-window words remain open |
| Backward branch and moment contraction | `explorations/explore60_backward_branches.py`, Sections 6--7 | Proved for the reduced systems |
| Reset-spike and finite reset-neighborhood transparency | `explorations/explore52_binary_partial_map.py`, Sections 6--8 | Proved |
| Fixed-count positive-label and finite-defect periodic-shadow strata | Sections 6--8, `lemma-roadmap.md` | Proved divergent for both return and reduced-gap least residues |
| Fixed low-factor-complexity binary strata | Sections 6--8, `lemma-roadmap.md` | Proved divergent for both return and reduced-gap least residues via Morse-Hedlund plus prefix compactness |
| Balanced/Sturmian-like binary frontier | Section 6, `lemma-roadmap.md` | Proved excluded: rational slopes are periodic, while irrational lower mechanical/Sturmian landings would require delayed prefix recurrences contradicted by the standard Sturmian recurrence function |
| Automatic and small uniform morphic binary templates | Section 6, `lemma-roadmap.md`, `explorations/explore77_uniform_morphism_recurrence.py`, `explorations/explore78_uniform_morphism_symbolic_witness.py` | Thue-Morse, period-doubling, and binary 2-, 3-, 4-, 5-, and 6-uniform fixed-point templates are excluded; larger uniform morphisms remain diagnostic |
| Prefix-language compactness principle | Sections 6--8, `lemma-roadmap.md` | Proved as reusable reduction from bounded restricted minima to an ordinary infinite code |
| Honest non-proof framing | `README.md`, `review.md`, `paper/sections/09-gap-analysis.typ` | Present |
| Universal uniform-morphic exclusion ("Theorem G", including q=9) | `proof.md` Section 23, Theorems 46 and 51 | Proved, refereed x2: every binary fixed point of every `q`-uniform morphism, all `q >= 2` with no aperiodicity or primitivity hypothesis, admits no positive ordinary reduced-gap or return code; subsumes the separate q=2..6 classifications and closes the q=9 boundary word |
| Complexity thresholds for `{0,1}` landings | `proof.md` Section 23, Theorems 47 and 60 | Proved, refereed x2 (Theorem 47): return landings need `liminf p(m)/m >= T_R` in `(3.1493, 3.1494)`, gap landings `>= T_G` in `(6.2390, 6.2391)`; the sharpened pointwise density-coupled versions `T_R' = 3.2439007` and `T_G' = 6.3942268` with uniform-density floor `7.5691`, genuinely 3-dependent (`T_R'(a) = 3/(5 log2(a) - 7)` vacuous exactly at `a >= 4`), are proved with machine-verified certificates (Theorem 60) but not separately refereed |
| AP Survivor unconditional rank-type bounds | `proof.md` Section 23, Theorem 48 | Proved, refereed: `W_R(B,L) <= C((B+1)2^(-2.1L) + 2^(0.9L))` and `W_G(B,L) <= C(B 2^(-5.46L) + 2^(1.54L))` uniformly; exponent floors `alpha_R = 0.287761`, `alpha_G = 0.212323`; the additive `2^(0.9L)` term means these do not yet satisfy `g(L) -> 0` |
| Exact criticality of the rank bases | `proof.md` Section 23, Theorem 57 | Proved, refereed x2: the base `2/15` (return) is exactly critical via `16 H(1/16) = 49 + 15 log2(2/15)`, and `1/112` (gap) via `8 H(1/8) = 52 - 7 log2(112)`; for every `rho < 2/15` the bound `C(B+1)rho^L` is false; the AP-Survivor exponent `alpha_R` is optimal even for position-aware counting |
| Saturation and class-counting no-gos | `proof.md` Section 23, Theorems 48 and 57 | Proved: translate-invariant counting schemes can never reach `C(B+1)theta^L`, and every interval+AP class-counting certificate is `>= 1` for all `(B,L)`, so no class-counting scheme can prove `H_R(B) < infinity` for any `B` |
| 5n+1 multiplier-blindness of the rank apparatus | `proof.md` Section 23, Theorem 49 | Proved, refereed: the whole return/gap counting apparatus (moduli `Q_r = 2^(4r+3)`, constants `2/15`, `1/112`, quartering `1/4`, terminal windows, periodic exclusions) transfers verbatim to 5n+1, which has the genuine cycle `F_5(13) = 13` outside every excluded class; rank bounds alone can never imply convergence |
| Two-lemma reduction (Theorem R) with Lemma P | `proof.md` Section 23, Theorem 55 | Proved conditional structure, refereed x2: H1 (no infinite positive binary return orbit) plus Lemma E (every non-descending FMF orbit is eventually a depth-`{0,1}` growth-B chain) imply pointwise FMF descent and Collatz; unconditional Lemma P: no infinite positive orbit of `m' = (27m+1)/16` via `16(11m'+1) = 27(11m+1)` |
| Mirror Equivalence and two-prime vacuity | `proof.md` Section 23, Theorem 61 | Proved: the 2-adic and 3-adic prefix data are the same information under an explicit affine bijection; 3-adic consistency below the envelope of `M` is verbatim the rank condition, so no two-prime pincer can prune the word tree; H1 has an equivalent mirror form in the Erdos--Lagarias / Furstenberg x2x3 class |
| Cocycle, reset law, and spike-ledger | `proof.md` Section 23, Theorem 62 | Proved, refereed x2: cocycle `B_uw = 3^(S_w) B_u + 2^(H_u) B_w`, master identity `v_2(D_p x_0 - B_p) = H_p + v_2(x_0 - x_k)`, reset law `nu' = min(nu, omega) - H_m`; unconditional spike-ledger theorem excludes all hop words whose depth spikes outrun the drift budget at geometric ratio `> log2(3)` |
| Certified pointwise descent record | `proof.md` Section 23, Theorem 54 | Proved, refereed x2: `sigma(x) = kappa(x)` for every odd `x > 1` with coefficient stopping time `kappa(x) <= 301,993` Terras steps (492,529 single steps); exact ledger `Theta(301,993) = 10,824,133,905`, zero-exception scan of `1.35e9` candidates |
| Cycle bound in FMF coordinates | `proof.md` Section 23, Theorem 53 | Proved, refereed x2: the Simons--de Weger m-cycle count equals the FMF hop count, so every nontrivial Collatz cycle makes at least 92 FMF hops at the current `2^71` floor |

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

After the July 19--21, 2026 refereed rounds (`proof.md` Section 23, Theorems 45--62), the strongest reduction is the two-lemma reduction of Theorem 55: H1 + Lemma E imply pointwise FMF descent and hence Collatz. The remaining gap is exactly these two lemmas.

- **H1** (no infinite positive orbit of the binary return partial map `T`, equivalently `mu_L -> infinity`): any proof is now known to require a position-aware, NON-class-counting arithmetic argument. The base `2/15` is exactly critical (Theorem 57), translate-invariant counting schemes provably saturate (Theorem 48), and every interval+AP class-counting certificate is `>= 1` for all `(B,L)`, so no class-counting scheme can prove `H_R(B) < infinity` for any `B`. The per-`B` decay target is equivalent to `mu_L -> infinity` itself: sufficient downstream but not one bit easier. In mirror form (Theorem 61), H1 is a small-least-residue statement modulo powers of 3 with 2-power denominators, in the Erdos--Lagarias / Furstenberg x2x3 rigidity class.
- **Lemma E** (every non-descending FMF orbit is eventually a depth-`{0,1}` growth-B chain): now known to require arithmetic, not statistics — exact witnesses achieve non-G01 letter density 1 among non-descending prefixes, so no purely frequency-based quantitative form of E exists (Theorem 59). Its residual core is infinitely many exact valuation coincidences: 2-adic near-approaches to eventually-periodic rational seeds, tied to the Lagarias periodicity conjecture (Theorem 62). The unbounded-alphabet branch is partially closed by the unconditional spike-ledger theorem (depth spikes outrunning the drift budget at geometric ratio `> log2(3)` are excluded).

Two framing facts constrain the route:

- The uniform gap-rank conjecture `W_G` is logically redundant given `W_R`: the `{0,1}` gap system is a sub-case of the return system.
- Rank bounds alone cannot imply convergence (5n+1 litmus, Theorem 49): the entire rank apparatus is multiplier-blind, and `F_5(13) = 13` sits outside every excluded class. Lemma E carries all the 3-dependence of any completion through this framework (its 5n+1 analogue is false, witness hop letter `(3,5)`); the coefficient `2 - log2(a)` in the ballot inequality flips sign exactly at `a = 4`.

## Practical Next Target

The concrete targets are now the two lemmas of the refereed reduction (Theorem 55).

For H1, the original terminal-window statement

`W_R(B,L) <= C(B+1)(2/15)^L`

remains a sufficient fixed-height form (the gap analogue `W_G(B,L) <= C B 112^(-L)` is redundant given `W_R`), but two refereed simplifications and two refereed constraints apply:

- Any uniform `f(B) g(L)` bound with `g(L) -> 0` suffices downstream; the sharp base `2/15` is not needed (Theorem 48). The per-`B` decay target is equivalent to `mu_L -> infinity` (Theorem 57).
- The AP Survivor bound already gives the exponential main term unconditionally; what is missing is removing the additive `2^(0.9L)` defect, which is the thick-class count and is positionally irremovable by counting alone.
- The proof must be position-aware (translate-invariant schemes saturate) and must not be a class-counting certificate (every interval+AP certificate is `>= 1` for all `(B,L)`).
- Uniform-morphic, low-complexity, balanced/Sturmian, and now ALL `q`-uniform-morphic fixed-point landings are excluded (Theorem G); the surviving `{0,1}` regime is aperiodic words with `liminf p(m)/m` above the sharpened thresholds `T_R' = 3.2439007` (return) / `T_G' = 6.3942268` (gap).

For Lemma E, the mapped route is arithmetic: the cocycle/master-identity/reset-law structure of Theorem 62, whose residual core is infinitely many exact valuation coincidences tied to rational seeds and the Lagarias periodicity conjecture. Proved slices to extend: the depth-`{0,1,2}` complexity bound `3/log2(41/16) = 2.20986` (Theorem 59), the block-power lemma (all periodic tails `u^infinity` with `|u| <= 91`), and the spike-ledger theorem for the unbounded-alphabet branch.

Note that even both rank bounds with sharp constants cannot alone imply convergence (5n+1 litmus): H1 without Lemma E does not close the pointwise gap, and neither lemma is dispensable.

## Candidate Results (Not Repo Claims)

| Candidate | Artifact | Status |
| --- | --- | --- |
| **Theorem ND (CANDIDATE; no priority)**: natural-density form of Tao's theorem — `{N : Col_min(N) > N0}` has upper natural density `<= C log^(-1/25) N0`, C not explicit | `notes/round4-july2026/s5-completion/PROOFS.md` (571-line manuscript; scripts sA--sE alongside); round-6 referee report `notes/round6-nov2026/nd-referee/REPORT.md` | AI-generated, no human review; not a repo claim. First claimed by J. Allikvere (Zenodo, 13 July 2026) by essentially the same method and by L. Mazur (ProofAtlas, 21 July 2026, claimed Lean-checked); the repository claims no priority and no novelty. The November 2026 AI referee found no fatal gap but five defects needing written repairs (including a misquoted Rhin bound). It does not change any obligation above. |

## Verification Snapshot

Full snapshot last checked on May 14, 2026 with:

- `bash scripts/verify_snapshot.sh full`

The commands below are packaged in `scripts/verify_snapshot.sh`. The default
`quick` mode runs the core algebra/reduction checks and paper compile; `full`
also runs the longer frontier scans listed later in this section. The companion
note `diagnostics.md` groups these scripts by mathematical role and records
their limitations.

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
- `python3 explorations/explore80_q9_boundary_residues.py`
- `python3 explorations/explore72_bounded_alphabet_beam.py --max-length 120 --beam-width 2000 --report-every 20`
- `typst compile paper/main.typ site/paper/collatz-fmf.pdf`
- `pdftotext site/paper/collatz-fmf.pdf /tmp/collatz-fmf.txt`
- `rg -n` PDF-text checks for the main-results overview, notation guide,
  expected section numbers, Theorem A--D labels, and Proposition 6.52
- `git diff --check` when the verifier is run inside a Git worktree; unpacked
  submission archives skip this hygiene check.

Scope: these commands verify the algebraic reductions, periodic exclusions, reset-neighborhood transparency, terminal-window/rank formulations, weighted and shell estimates, mechanical normal-form recurrences, recurrence-speed diagnostics, template recurrence diagnostics, uniform-morphism recurrence diagnostics, and finite diagnostic frontiers currently used by the paper. The q=5 and q=6 uniform-morphism theorems are now proved in Section 6 by finite classification; `explore78` verifies the q=6 symbolic-prefix witness table that repairs the pure-power diagnostic failure, records clean q=7 and q=8 diagnostics, and isolates the first q=9 reduced-gap boundary case. `explore79` confirms that this residual q=9 case has no successful symbolic-prefix gap witness through length `50,000`; `explore80` records prefix-residue growth along the same boundary word. When run from an unpacked archive rather than a Git checkout, the verifier skips only the `git diff --check` hygiene step. These commands do not verify the missing pointwise Collatz descent theorem or the unweighted terminal-window counting theorem.
