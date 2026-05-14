# Publication Readiness Audit

Current date: May 14, 2026.

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
- A precise remaining proof target: an unweighted terminal-window/rank theorem.

## Claims To Avoid

The manuscript should not claim:

- A proof of the Collatz conjecture.
- Pointwise descent for every odd integer.
- Trajectory independence from state-distribution laws.
- That density-zero exceptional sets are empty.
- That finite verifier runs prove a universal theorem.
- That the FMF results are strictly stronger than Tao's theorem without
  qualifying that the events being measured are different.

## Prize-Level Completion Gate

To become a Collatz proof, the paper must add a theorem implying:

> For every odd `x > 1`, some finite FMF iterate is smaller than `x`.

Within the current framework, the most concrete sufficient route is:

1. Prove the return terminal-window count
   `W_R(B,L) <= C(B+1)(2/15)^L` uniformly in `B,L`.
2. Prove the reduced gap terminal-window count
   `W_G(B,L) <= C B 112^(-L)` uniformly in `B,L`.
3. Use those fixed-height bounds to rule out infinite positive binary return
   and reduced `{0,1}` gap orbits.
4. Generalize from the first bounded-depth obstructions to all growth-B and
   mixed recovery epochs.
5. Deduce pointwise FMF descent for every odd `x > 1`, then conclude Collatz by
   infinite descent.

The current paper reaches step 0: it defines the objects, proves exact
equivalences, proves density and weighted bounds, and identifies the missing
unweighted rank theorem. It does not prove that theorem.

## Submission Work Remaining

Before external submission:

- Split the very long Section 5 into shorter sections: growth-B density,
  binary return codes, reduced gap codes, terminal-window estimates, and
  obstruction-class exclusions.
- Keep the main-results endpoint map synchronized with the strongest Section 5
  endpoint theorems and criteria as the manuscript is reorganized.
- Keep finite diagnostic output and long exploratory classifications in the
  companion repository note, `diagnostics.md`, rather than in the main paper.
- Run the full verifier snapshot in `proof-obligations.md` after the split.
- Add a compact "not a proof of Collatz" paragraph to the abstract and
  introduction, which the current manuscript now has.
- Ask an external number theorist to review only the exact algebra, density
  normalizations, and obstruction reductions before broad circulation.

## Latest Local Sanity Checks

The packaged full verifier was run on May 14, 2026:

- `bash scripts/verify_snapshot.sh full`

This includes the Typst compile, PDF text smoke check, core algebra and
reduction scripts, bounded-alphabet profiles, uniform-morphism diagnostics
through the recorded frontier, the q=9 boundary scan, the bounded-alphabet beam
search, and `git diff --check`.

These checks support the current density/reduction manuscript. They do not
verify the missing pointwise Collatz theorem.
