#import "../lib/theorem.typ": *

= Future Directions

The FMF framework opens several lines of investigation, both theoretical and computational.

*Effective equidistribution.* The Quartering Law relies on the equidistribution of $m mod 8$ after each growth-B step, which holds in $ZZ_2$ by the expanding map property. Making this effective --- bounding how quickly $3^n mod 2^K$ equidistributes as a function of $K$ and $n$ --- would strengthen the density bounds and potentially close the gap for integers below a computable threshold. The natural tools are exponential sum estimates for multiplicative characters modulo $2^K$, where the relevant sums have the form $sum_(m "odd") e^(2 pi i dot 3^(t+2) m \/ 2^K)$. Standard bounds on such sums give equidistribution for $K = O(n)$, but the growth-B dynamics require $K$ growing with the number of iterations, not just with $t$.

*Invariant sets in $ZZ_2$.* As formulated in Section 9, the remaining gap reduces to whether the growth-B map has any infinite orbit in $ZZ$. This is a question about invariant subsets of expanding maps on $ZZ_2$. The analogous question for the map $m arrow.r.bar 2m mod p$ on $ZZ\/p ZZ$ is trivial (no nontrivial invariant subsets), but the growth-B map involves variable expansion factors and a nonlinear odd-part extraction. Progress may come from the theory of $p$-adic dynamical systems, particularly results on wandering domains and non-existence of invariant measures for expanding maps.

*Critical-series landing.* The binary return and ${0,1}$ gap reductions both produce rational critical series with a real limit outside the positive integers and a $2$-adic limit equal to the obstruction code. Sections 6--8 now exclude periodic, fixed sparse-label, fixed low-complexity, balanced/Sturmian, Thue--Morse, period-doubling, binary $2$-, $3$-, $4$-, $5$-, and $6$-uniform morphic fixed-point, and finite-defect periodic-shadow templates. The immediate technical target is therefore sharper: prove that no higher-complexity nonperiodic critical series in these families can land on a positive ordinary integer in $QQ_2$. This is stronger and more precise than a density statement: it is a pointwise Diophantine condition on a single $2$-adic limit selected by an infinite word. The prefix-recurrence height barrier and density-recurrence exclusion criteria give one current route into this problem.

*Uniform terminal-window counting.* Sections 6--7 reformulate the same obstruction as a stopping-time problem. For return words, $R_w <= B$ is equivalent to $U_w\/E_w < B+1$; for reduced ${0,1}$ gap words, $S_w <= B$ is equivalent to $u_w\/E_w < B$. A proof of bounds
$ W_R(B,L) <= C(B+1)(2\/15)^L, quad W_G(B,L) <= C B 112^(-L) $
for these normalized terminal-window counts would settle the corresponding fixed-height return and gap obstructions. The existing backward-contraction, cubic-mass, and expansion-pressure lemmas suggest a potential high-moment route. On the return side, terminal injectivity also gives a weighted window bound
$ sum_(|w|=L, R_w <= B) E_w^(-theta) <= (B+1)^theta zeta(theta) $
for every $theta>1$, plus the cutoff count $N_R(B,L;X) <= ceil(X(B+1))-1$. On the reduced gap side, backward contraction gives a weighted window bound
$ sum_(|w|=L, S_w <= B) E_w^(-theta) <= B^theta (43\/81)^L zeta(theta-1) $
for $theta>2$, and an ordinary low-expansion count with a quadratic terminal cutoff and an explicit merge-multiplicity factor. The same weighted estimates control any fixed dyadic expansion shell, but the cost grows exponentially with the shell index, and fixed shells only occur at bounded prefix depth. The frontier diagnostics show that this is still insufficient; the missing ingredient is a genuine terminal-height separation or stopping-time estimate that controls the high-expansion low-window words across shells.

*Computational extensions.* The Quartering Law has been verified for growth chains up to 60-bit starting values. Pushing this verification to 80 or 100 bits, particularly for structured families like $2^n - 1$ and numbers with extremal $t$-parameters, would provide additional confidence and might reveal unexpected phenomena at larger scales. The epoch bound $op("epoch")(x) <= 2.83 log_2(x)$ is another candidate for extended verification.

*Connection to Syracuse random variables.* Tao's proof @tao2022 constructs Syracuse random variables that model the Collatz dynamics in a measure-theoretic framework. The FMF decomposition provides a natural discretization of these variables: each FMF hop corresponds to a block of Syracuse steps with algebraically determined length. Translating between the two frameworks could clarify whether the Quartering Law's growth-chain bounds can be combined with Tao's logarithmic-density machinery.

*Code availability.* The computational explorations underlying this paper are available at the project repository. The core verification scripts are self-contained, with verification counts and failure rates reported inline.

== Acknowledgments

The systematic explorations --- each designed to test a specific hypothesis, verify it computationally, attempt a proof, and honestly record failures --- were essential to identifying which results could be made rigorous and which could not.
