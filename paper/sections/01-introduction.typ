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

*Results.* We prove four structural theorems, derive a density bound from their combination, and then sharpen the remaining pointwise obstruction into explicit $2$-adic coding problems:

- *Theorem A* (FMF Step Formula): Every odd number is either Type A ($x equiv 1 mod 4$) or Type B ($x equiv 3 mod 4$). For each type, the number of Collatz steps to the FMF and the FMF value itself are given by explicit algebraic formulas depending only on $x mod 4$ and the $2$-adic valuation of a simple expression in $x$.

- *Theorem B* (State Distribution): The output state distribution of the FMF hop --- meaning the mod-$4$ class and $2$-adic parameters of the next odd number --- is independent of the input state in natural density. This is not a heuristic assumption about one trajectory, but a counting theorem following from the structure of $2$-adic inverses.

- *Theorem C* (Fractional-Moment Contraction): The FMF hop ratio $R = F(x)\/x$ satisfies the exact asymptotic natural-density estimate $EE[R^alpha] < 1$ for $alpha = 0.53$, with $EE[R^0.53] approx 0.8638$. This proves average contraction in a fractional moment; it is not a pointwise Lyapunov function.

- *Theorem D* (Quartering Law): Among starts already in a growth-B hop, each additional growth-B continuation has density factor $1\/4$. Consequently, the density among odd starts of a strict growth-B chain of length at least $k$ is $4^(-k)$. This gives elementary exponential natural-density bounds for one precisely defined growth mechanism.

- *Pointwise obstruction reductions:* The first bounded-depth cases are reduced to explicit partial maps and terminal-window counting problems. In the binary-depth return system, surviving return words have exact density $(2\/15)^L$ and ordinary obstructions are equivalent to positive integer orbits of a return-code partial map. In the reduced ${0,1}$ gap system, the analogous complete-gap survival density is $112^(-L)$. The paper excludes periodic, finite-defect, low-complexity, balanced/Sturmian, and several automatic-template obstruction classes, and identifies the remaining missing theorem as a uniform unweighted terminal-window count.

#v(0.5em)

*What this paper does not prove.* We do not prove the Collatz conjecture. The gap between density statements and universal pointwise convergence remains open and is, in my view, a frontier problem in $p$-adic dynamics. The reductions above make that gap more precise, but they do not eliminate it. I state this limitation upfront and devote Section 9 to an honest analysis of this gap, including why the contraction, growth-chain, and terminal-window results do not close it.

#v(0.5em)

*Outline.* Section 2 develops the FMF hop formulas and proves Theorem A. Section 3 establishes the state-distribution theorem (Theorem B) via $2$-adic analysis. Section 4 derives fractional-moment contraction (Theorem C) and explains why $3n+1$ is distinguished among $a n + 1$ maps. Section 5 proves the Quartering Law (Theorem D) and the basic growth-B density bounds. Section 6 develops the binary return-code reduction and its terminal-window estimates. Section 7 treats the reduced ${0,1}$ gap-code reduction. Section 8 records the endpoint dichotomies and growth-B coding endpoint. Section 9 analyzes the "almost all $arrow.r$ all" gap. Section 10 records supporting growth bounds on exceptional trajectories. Section 11 discusses future directions and connections to $p$-adic dynamics.
