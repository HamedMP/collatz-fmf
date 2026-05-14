#import "lib/style.typ": paper-style, title-page
#import "lib/theorem.typ": *

#show: paper-style

#title-page(
  title: "First-Multiple-of-Four Coordinates for Collatz Growth Chains",
  subtitle: "Density Bounds and Pointwise Obstruction Reductions",
  authors: ("Hamed Mohammadpour",),
  date: "March 2026",
  abstract: [
    I introduce the _First-Multiple-of-Four_ (FMF) decomposition of Collatz dynamics, which partitions each trajectory into hops between odd numbers via the first value divisible by 4. This yields exact algebraic formulas for hop length and output value (Theorem A), natural-density output laws from 2-adic inverse structure (Theorem B), and an exact asymptotic fractional-moment contraction $EE[R^0.53] approx 0.8638 < 1$ for the FMF hop ratio (Theorem C). The main density result is the _Quartering Law_ (Theorem D): among starts already in a growth-B hop, each additional growth-B continuation has density factor $1\/4$, so the density among odd starts of a strict growth-B chain of length at least $k$ is $4^(-k)$. The paper also gives exact pointwise obstruction reductions for the first bounded-depth cases: binary-depth return obstructions are reduced to an explicit 2-adic return-code partial map with survival density $(2\/15)^L$, while the reduced ${0,1}$ gap obstruction has survival density $112^(-L)$. Periodic, finite-defect, low-complexity, balanced/Sturmian, and several automatic-template obstruction classes are excluded, leaving a precise unweighted terminal-window counting problem. These results are elementary density and reduction theorems for isolated Collatz growth mechanisms; they are not a proof of the Collatz conjecture and not a replacement for Tao's orbit-minimum theorem. I state the remaining "almost all $arrow.r$ all" gap explicitly as a frontier problem in $p$-adic dynamics.
  ],
)

#include "sections/01-introduction.typ"
#include "sections/02-fmf-formulas.typ"
#include "sections/03-state-independence.typ"
#include "sections/04-contraction.typ"
#include "sections/05-quartering-law.typ"
#include "sections/06-gap-analysis.typ"
#include "sections/07-growth-bounds.typ"
#include "sections/08-future.typ"

#bibliography("refs.bib")
