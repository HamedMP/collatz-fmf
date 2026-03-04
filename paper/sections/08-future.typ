#import "../lib/theorem.typ": *

= Future Directions

The FMF framework opens several lines of investigation, both theoretical and computational.

*Effective equidistribution.* The Quartering Law relies on the equidistribution of $m mod 8$ after each growth-B step, which holds in $ZZ_2$ by the expanding map property. Making this effective --- bounding how quickly $3^n mod 2^K$ equidistributes as a function of $K$ and $n$ --- would strengthen the density bounds and potentially close the gap for integers below a computable threshold. The natural tools are exponential sum estimates for multiplicative characters modulo $2^K$, where the relevant sums have the form $sum_(m "odd") e^(2 pi i dot 3^(t+2) m \/ 2^K)$. Standard bounds on such sums give equidistribution for $K = O(n)$, but the growth-B dynamics require $K$ growing with the number of iterations, not just with $t$.

*Invariant sets in $ZZ_2$.* As formulated in Section 6, the remaining gap reduces to whether the growth-B map has any infinite orbit in $ZZ$. This is a question about invariant subsets of expanding maps on $ZZ_2$. The analogous question for the map $m arrow.r.bar 2m mod p$ on $ZZ\/p ZZ$ is trivial (no nontrivial invariant subsets), but the growth-B map involves variable expansion factors and a nonlinear odd-part extraction. Progress may come from the theory of $p$-adic dynamical systems, particularly results on wandering domains and non-existence of invariant measures for expanding maps.

*Computational extensions.* The Quartering Law has been verified for growth chains up to 60-bit starting values. Pushing this verification to 80 or 100 bits, particularly for structured families like $2^n - 1$ and numbers with extremal $t$-parameters, would provide additional confidence and might reveal unexpected phenomena at larger scales. The epoch bound $op("epoch")(x) <= 2.83 log_2(x)$ is another candidate for extended verification.

*Connection to Syracuse random variables.* Tao's proof @tao2022 constructs Syracuse random variables that model the Collatz dynamics in a measure-theoretic framework. The FMF decomposition provides a natural discretization of these variables: each FMF hop corresponds to a block of Syracuse steps with algebraically determined length. Translating between the two frameworks could allow the Quartering Law's exponential bounds to be combined with Tao's logarithmic-density machinery.

*Code availability.* The computational explorations underlying this paper (44 systematic investigations, labeled `explore01.py` through `explore44.py`) are available at the project repository. Each exploration is self-contained, with verification counts and failure rates reported inline.

== Acknowledgments

All computational explorations were conducted using Claude Code (Anthropic, Claude Opus 4.6) on a MacBook Pro M4 Pro. The 44 systematic explorations --- each designed to test a specific hypothesis, verify it computationally, attempt a proof, and honestly record failures --- were essential to identifying which results could be made rigorous and which could not.
