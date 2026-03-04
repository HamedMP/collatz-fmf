#import "lib/style.typ": paper-style, title-page
#import "lib/theorem.typ": *

#show: paper-style

#title-page(
  title: "Elementary Exponential Density Bounds for Collatz Growth Chains",
  subtitle: "via First-Multiple-of-Four Decomposition",
  authors: ("Hamed Mohammadpour",),
  date: "March 2026",
  abstract: [
    I introduce the _First-Multiple-of-Four_ (FMF) decomposition of Collatz dynamics, which partitions each trajectory into hops between odd numbers via the first value divisible by 4. This yields exact algebraic formulas for hop length and output value (Theorem A), a proof that hop output distributions are state-independent via 2-adic inverse structure (Theorem B), and a spectral contraction $rho = 0.8638 < 1$ derived from exact formulas rather than sampling (Theorem C). The main result is the _Quartering Law_ (Theorem D): the probability that a growth chain continues for $k$ steps decays as $(1\/4)^k$, giving natural-density bounds strictly stronger than Tao's logarithmic-density result, with exponential rather than sub-polynomial decay, via entirely elementary mod-8 arithmetic. I provide an honest assessment of what this does and does not prove: the "almost all $arrow.r$ all" gap remains open and constitutes a frontier problem in $p$-adic dynamics.
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
