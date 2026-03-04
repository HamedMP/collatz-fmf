#import "../lib/theorem.typ": *

= Introduction

The Collatz conjecture, arguably the simplest unsolved problem in mathematics, concerns the iteration of the map
$ C(n) = cases(n\/2 & "if" n "is even", 3n+1 & "if" n "is odd".) $
The conjecture asserts that for every positive integer $n$, repeated application of $C$ eventually reaches $1$. Despite its elementary statement, the problem has resisted all attempts at proof for nearly a century. Computational verification has confirmed convergence for all $n < 2^(71)$ @barina2025, and no nontrivial cycle exists with period less than $2.17 times 10^(11)$ @simons2005. The extensive survey of Lagarias @lagarias2021 catalogs the many approaches attempted and the obstacles each faces.

#v(0.5em)

The difficulty lies in the interplay between multiplication (the $3n+1$ branch) and division (the $n\/2$ branch). Most analyses study individual Collatz steps, leading to stochastic models that treat the sequence of even/odd decisions as effectively random. Tao @tao2022 made this heuristic rigorous, proving that almost all orbits (in logarithmic density) attain almost bounded values --- a landmark result, but one that falls short of the full conjecture by a wide margin.

#v(0.5em)

*The FMF decomposition.* This paper takes a different approach. Rather than analyzing individual Collatz steps, we group them into _hops_. Each hop takes an odd number $x$ and runs the Collatz iteration until the first value divisible by $4$ is reached --- the _First Multiple of Four_ (FMF). Dividing out the full power of $2$ yields the next odd number. On average, one FMF hop compresses roughly six Collatz steps into a single algebraic operation, and the hop map admits exact closed-form formulas.

#v(0.5em)

*Results.* We prove four main theorems and derive a density bound from their combination:

- *Theorem A* (FMF Step Formula): Every odd number is either Type A ($x equiv 1 mod 4$) or Type B ($x equiv 3 mod 4$). For each type, the number of Collatz steps to the FMF and the FMF value itself are given by explicit algebraic formulas depending only on $x mod 4$ and the $2$-adic valuation of a simple expression in $x$.

- *Theorem B* (State Independence): The output state distribution of the FMF hop --- meaning the mod-$4$ class and $2$-adic parameters of the next odd number --- is _independent_ of the input state. This is not a heuristic assumption but a theorem following from the structure of $2$-adic inverses.

- *Theorem C* (Spectral Contraction): The FMF transition operator on weighted state space has spectral radius $rho = 0.8638 < 1$, computed from exact formulas. The rank-$1$ property (a consequence of Theorem B) reduces the spectral radius to a single expected value $EE[R^alpha]$ at optimal exponent $alpha = 0.53$.

- *Theorem D* (Quartering Law): The probability that a growth chain --- a consecutive run of non-shrinking hops --- continues for $k$ steps decays as $(1\/4)^k$. This yields natural-density bounds strictly stronger than Tao's logarithmic-density result @tao2022, with exponential rather than sub-polynomial decay, via entirely elementary mod-$8$ arithmetic.

#v(0.5em)

*What this paper does not prove.* We do not prove the Collatz conjecture. The gap between "almost all trajectories converge" and "all trajectories converge" remains open and is, in my view, a frontier problem in $p$-adic dynamics. I state this limitation upfront and devote Section 6 to an honest analysis of this gap, including why the contraction results --- despite being strictly stronger than prior work --- do not close it.

#v(0.5em)

*Outline.* Section 2 develops the FMF hop formulas and proves Theorem A. Section 3 establishes state independence (Theorem B) via $2$-adic analysis. Section 4 derives the spectral contraction (Theorem C) and explains why $3n+1$ is distinguished among $a n + 1$ maps. Section 5 proves the Quartering Law (Theorem D) and derives the density bounds. Section 6 analyzes the "almost all $arrow.r$ all" gap. Section 7 establishes growth bounds on exceptional trajectories. Section 8 discusses future directions and connections to $p$-adic dynamics.
