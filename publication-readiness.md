# Publication Readiness Audit

Current date: May 14, 2026. Claim-boundary sections last updated July 31, 2026
to incorporate the July 19--21, 2026 refereed rounds (`proof.md` Section 23).

## Verdict

The project is not publication-ready as a proof of the Collatz conjecture.

It is close to being presentable as a research preprint on an elementary
First-Multiple-of-Four (FMF) coordinate system, natural-density bounds for
growth chains, and exact 2-adic obstruction reductions. The defensible
contribution is structural: the paper isolates a growth mechanism, proves sharp
density laws for it, and reduces the first bounded-depth pointwise obstructions
to explicit partial maps and terminal-window counting problems.

The manuscript should not be marketed as a solution to Collatz, a prize-level
proof, or a replacement for Tao's almost-all theorem. A major-prize-level result
would require closing the pointwise descent gap listed in
`proof-obligations.md`.

## Current Literature Baseline

The introduction's main external baseline is still appropriate:

- Tao's accepted 2022 paper proves that almost all Collatz orbits attain almost
  bounded values in logarithmic density. The FMF paper should describe this as a
  landmark almost-all theorem, not as something directly dominated by the FMF
  density bounds.
- Barina's 2025 verification reports convergence for all starting values below
  `2^71`. This is the current computational-verification baseline used by the
  manuscript.
- Simons and de Weger's cycle-length lower bounds remain useful background, but
  they are logically separate from the FMF arguments.
- Recent 2025--2026 Collatz preprints exist, including topological/ergodic and
  flow formulations. None should be treated as an accepted proof or as a theorem
  that closes the FMF pointwise gap unless independently verified and accepted.

Sources checked:

- Tao, "Almost all orbits of the Collatz map attain almost bounded values":
  https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/almost-all-orbits-of-the-collatz-map-attain-almost-bounded-values/1008CC2DF91AF87F66D190C5E01C907F
- Tao arXiv version: https://arxiv.org/abs/1909.03562
- Barina verification project page: https://pcbarina.fit.vutbr.cz/
- Barina 2025 DOI page: https://doi.org/10.1007/s11227-025-07337-0
- Recent topological/ergodic arXiv preprint noted for awareness:
  https://arxiv.org/abs/2601.03297

## Claims That Are Defensible

The manuscript can defensibly claim:

- Exact FMF hop formulas for odd-to-odd Collatz dynamics.
- Natural-density state-distribution laws from 2-adic unit structure.
- Fractional-moment average contraction for the FMF density model.
- The Quartering Law: strict growth-B continuation density factor `1/4`.
- Existence of arbitrarily long finite growth-B shadows, preventing finite
  forbidden-pattern proof strategies.
- Exact binary-depth return and reduced `{0,1}` gap partial-map reductions.
- Terminal-window identities, weighted terminal-window estimates, shell
  estimates, and low-expansion cutoff counts.
- Exclusion of several obstruction classes: periodic, finite-defect periodic
  shadows, fixed sparse-label strata, low-complexity strata, balanced/Sturmian
  branches, and several small automatic/uniform-morphic templates.
- From the July 19--21, 2026 refereed rounds (`proof.md` Section 23,
  Theorems 45--62):
  - Universal uniform-morphic exclusion ("Theorem G"): every binary
    `q`-uniform-morphic fixed point excluded for every `q >= 2`, including the
    q=9 boundary word.
  - Complexity thresholds for `{0,1}` landings: `liminf p(m)/m >= T_R` in
    `(3.1493, 3.1494)` (return) / `T_G` in `(6.2390, 6.2391)` (gap), with
    sharpened 3-dependent versions `T_R' = 3.2439007`, `T_G' = 6.3942268`.
  - Unconditional AP Survivor rank-type bounds with exponent floors
    `alpha_R = 0.287761`, `alpha_G = 0.212323`, plus exact criticality of the
    bases `2/15` and `1/112` and the saturation/class-counting no-gos.
  - The two-lemma reduction (Theorem 55): H1 + Lemma E imply Collatz, with the
    unconditional Lemma P.
  - The 5n+1 litmus: the rank apparatus is multiplier-blind, so rank bounds
    alone cannot imply convergence.
  - Mirror Equivalence / two-prime vacuity, and the cocycle / reset-law /
    spike-ledger structure of Lemma E.
  - Certified descent record `sigma = kappa` to `301,993` Terras steps; every
    nontrivial cycle makes at least 92 FMF hops.
- A precise remaining proof target: the two lemmas H1 and Lemma E of the
  refereed two-lemma reduction.

## Claims To Avoid

The manuscript should not claim:

- A proof of the Collatz conjecture.
- Pointwise descent for every odd integer.
- Trajectory independence from state-distribution laws.
- That density-zero exceptional sets are empty.
- That finite verifier runs prove a universal theorem.
- That the FMF results are strictly stronger than Tao's theorem without
  qualifying that the events being measured are different.
- That the candidate natural-density upgrade of Tao's theorem ("Theorem ND",
  `notes/round4-july2026/s5-completion/PROOFS.md`) is established mathematics:
  it is AI-proved and AI-refereed only and awaits human expert review.
- That rank/terminal-window bounds alone would prove convergence: the 5n+1
  litmus (Theorem 49) shows the rank apparatus is multiplier-blind.

## Prize-Level Completion Gate

To become a Collatz proof, the paper must add a theorem implying:

> For every odd `x > 1`, some finite FMF iterate is smaller than `x`.

Within the current framework, the most concrete sufficient route is the
refereed two-lemma reduction (`proof.md` Section 23, Theorem 55):

1. Prove H1: no infinite positive orbit of the binary return partial map,
   equivalently `mu_L -> infinity`. The original fixed-height form
   `W_R(B,L) <= C(B+1)(2/15)^L` suffices (the gap count `W_G` is logically
   redundant given `W_R`, and any uniform `f(B)g(L)` with `g(L) -> 0` also
   suffices), but the proof must be position-aware and non-class-counting: the
   base `2/15` is exactly critical, translate-invariant schemes provably
   saturate, and interval+AP class-counting certificates are provably useless.
2. Prove Lemma E: every non-descending FMF orbit is eventually a depth-`{0,1}`
   growth-B chain. This is the 3-specific missing piece (its 5n+1 analogue is
   false), and it must be proved by arithmetic — its core is exact valuation
   coincidences tied to rational seeds — not by letter statistics.
3. Conclude by Theorem 55: H1 + Lemma E imply pointwise FMF descent for every
   odd `x > 1`, hence Collatz by infinite descent.

Two updates to the old five-step gate:

- The former step 4 (bounded-depth to all mixed recovery epochs) now HAS a
  writeup: the mixed-epoch bridge and the two-lemma reduction formalize it
  exactly, with Lemma E as the isolated missing piece.
- The rank-only route (the old steps 1--3 by themselves) is proved
  insufficient by the 5n+1 litmus (Theorem 49): the entire rank apparatus
  transfers verbatim to 5n+1, which has the nontrivial cycle 13.

The current paper reaches step 0 of this route: it defines the objects, proves
exact equivalences, and proves density and weighted bounds. The claim inventory
has since grown by the addendum section (`proof.md` Section 23, Theorems
45--62, from the July 19--21, 2026 adversarial rounds; the load-bearing
positive claims adversarially refereed, Theorem 58 candidate-only), which adds
the reduction itself, the
unconditional AP Survivor bounds, and the negative delimiters — but neither H1
nor Lemma E is proved.

## Submission Work Remaining

Before external submission:

- Keep the main-results endpoint map synchronized with the strongest Sections
  5--8 endpoint theorems and criteria as the manuscript is reorganized.
- Keep finite diagnostic output and long exploratory classifications in the
  companion repository note, `diagnostics.md`, rather than in the main paper.
- Use `submission-checklist.md` as the concrete file inventory and command gate
  before circulating or archiving a draft.
- After any future structural change, rerun the full verifier snapshot recorded
  in `proof-obligations.md`.
- Use `referee-brief.md` when asking an external number theorist to review only
  the exact algebra, density normalizations, and obstruction reductions before
  broad circulation.

## Latest Local Sanity Checks

The packaged full verifier was run on May 14, 2026:

- `bash scripts/verify_snapshot.sh full`

This includes the Typst compile, PDF text smoke checks for the main-results and
notation front matter, expected section numbers, Theorem A--D labels, and key endpoint labels, core algebra and reduction scripts,
bounded-alphabet profiles, uniform-morphism diagnostics through the recorded
frontier, the q=9 recurrence and residue boundary scans, the bounded-alphabet beam search, and
`git diff --check` when run inside the Git checkout.

These checks support the current density/reduction manuscript. They do not
verify the missing pointwise Collatz theorem.
