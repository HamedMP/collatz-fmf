#import "lib/style.typ": paper-style, title-page
#import "lib/theorem.typ": *

#show: paper-style

#title-page(
  title: "First-Multiple-of-Four Coordinates for Collatz Growth Chains",
  subtitle: "Density Bounds and Pointwise Obstruction Reductions",
  authors: ("Hamed Mohammadpour",),
  date: "May 2026",
  abstract: [
    The _First-Multiple-of-Four_ (FMF) decomposition partitions Collatz dynamics into odd-to-odd hops ending at the first value divisible by 4. In these coordinates the hop length and output value have exact algebraic formulas (Theorem A), the output states have natural-density laws obtained from 2-adic inverse structure (Theorem B), and the FMF hop ratio has an exact asymptotic fractional-moment contraction $EE[R^0.53] approx 0.8638 < 1$ in the density model (Theorem C). The main density theorem is the _Quartering Law_ (Theorem D): conditional on a growth-B hop, each additional strict growth-B continuation has density factor $1\/4$, so the density among odd starts of a strict growth-B chain of length at least $k$ is $4^(-k)$.

    The paper also gives pointwise reductions for the first bounded-depth obstruction classes. Binary-depth return obstructions are reduced to an explicit 2-adic return-code partial map with survival density $(2\/15)^L$; the reduced ${0,1}$ gap obstruction is reduced to a parallel partial map with survival density $112^(-L)$. Periodic, finite-defect, low-complexity, balanced/Sturmian, and several automatic-template obstruction classes are excluded, leaving a concrete unweighted terminal-window counting problem. These are elementary density and reduction theorems for isolated Collatz growth mechanisms, not a proof of the Collatz conjecture and not a replacement for Tao's orbit-minimum theorem. The remaining "almost all $arrow.r$ all" gap is stated explicitly as a pointwise problem in 2-adic dynamics.
  ],
)

#include "sections/01-introduction.typ"
#include "sections/01b-main-results.typ"
#include "sections/01c-notation.typ"
#include "sections/02-fmf-formulas.typ"
#include "sections/03-state-independence.typ"
#include "sections/04-contraction.typ"
#include "sections/05-quartering-law.typ"
#include "sections/06-binary-return-codes.typ"
#include "sections/07-reduced-gap-codes.typ"
#include "sections/08-endpoint-dynamics.typ"
#include "sections/09-gap-analysis.typ"
#include "sections/10-growth-bounds.typ"
#include "sections/11-future.typ"

#bibliography("refs.bib")
