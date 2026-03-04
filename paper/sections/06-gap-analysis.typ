#import "../lib/theorem.typ": *

= What This Does and Does Not Prove

This section provides an honest accounting of the results in this paper: what has been established rigorously, what remains open, and why the remaining gap is genuinely hard. I consider this assessment essential. The Collatz conjecture has attracted a large body of work that overstates its conclusions; I aim to avoid that failure mode.

== What is proved

The following results are established by exact algebraic arguments, not heuristic or statistical reasoning.

+ *Exact FMF formulas (Theorem A).* For every odd $x$, the number of Collatz steps to the first multiple of four, and the value of that multiple, are given by closed-form expressions depending on $x mod 4$ and $v_2(k+1)$ where $x = 4k+3$. The FMF value for Type B inputs with $k+1 = 2^t m$ ($m$ odd) is $2(3^(t+2) m - 1)$. These are algebraic identities, not statistical observations.

+ *State independence (Theorem B).* The distribution of the FMF hop output --- its mod-4 class, its $t$-parameter, and its $v_2$ parameter --- is identical regardless of the input state. This follows from the structure of 2-adic inverses: since $3^(t+2)$ is a unit in $ZZ_2$, multiplication by $3^(t+2)$ permutes residue classes, making the output distribution a fixed function of the 2-adic structure alone. This is _not_ a heuristic independence assumption; it is a theorem about the algebraic structure of the map.

+ *Spectral contraction (Theorem C).* The FMF transition operator on weighted state space has spectral radius $rho = 0.8638 < 1$, with the rank-1 property (a consequence of state independence) reducing the spectral analysis to a single expected value $EE[R^alpha]$ at optimal exponent $alpha = 0.53$. The exact value $alpha^* = 1.0002$ satisfies $EE[R^(alpha^*)] = 1$, establishing that the transition operator is a strict contraction for all $alpha < alpha^*$.

+ *The Quartering Law (Theorem D).* Growth chains --- consecutive runs of growth-B hops --- have continuation probability exactly $1\/4$ per step, giving natural-density bounds $delta_k = 2\/4^k$. The proof uses only mod-8 arithmetic and the unit structure of $3^(t+2)$ in $ZZ_2$.

+ *No small cycles.* By the results of Simons and de Weger @simons2005, any nontrivial cycle in the Collatz map requires more than $2.17 times 10^(11)$ odd steps. In FMF terms, this corresponds to more than $3.6 times 10^(10)$ hops.

== What is not proved

I do not prove the Collatz conjecture. Specifically:

- *Not every trajectory is shown to converge.* The density bounds show that the set of integers with growth chains of length $>= k$ has natural density at most $2\/4^k$, which tends to zero. But natural density zero does not mean the set is empty. In fact, by a straightforward pigeonhole argument, for any constant $C < 1$, infinitely many odd integers $n$ have growth chains of length at least $C dot log_4(n)$. The exceptional set is provably _infinite_ in this weak sense; what we show is that it is negligibly thin.

- *Growth phases are not proved to terminate for every starting point.* The growth chain bound is verified empirically (zero violations across $1.5 times 10^6$ growth chains, up to 60-bit starting values) but not proved. A single counterexample --- an odd integer whose growth chain never terminates --- would disprove the Collatz conjecture.

- *The spectral contraction is an average statement.* The spectral radius $rho < 1$ means that _on average_ (weighted by the Lyapunov function $L(x) = x^alpha dot w(x mod 8)$), hops are contracting. But the worst-case single-hop ratio grows without bound: for $x = 2^n - 1$ with large $n$, the hop ratio can exceed $n$ itself. No finite number of hops $k$ achieves a uniform pointwise contraction $max_x L(F^k (x))\/L(x) < 1$.

== Comparison with Tao's result

Tao @tao2022 proves that almost all Collatz orbits attain almost bounded values, in the sense of logarithmic density. The present results and Tao's address different aspects of the same problem, and the comparison is instructive.

*Density notion.* Tao works with logarithmic density (weighting integers by $1\/n$), which is weaker than natural density (uniform weighting). The Quartering Law gives bounds in natural density, which is the strictly stronger measure. However, Tao's result is about the _values attained_ by orbits (they become small), while the present result is about the _structure of growth phases_ (they are short). These are complementary statements.

*Decay rate.* Tao's bounds on the exceptional set are sub-polynomial: the fraction of integers up to $N$ whose orbits fail to reach below $f(N)$ decays slower than any power of $N$. The Quartering Law gives exponential decay: the fraction with growth chains of length $>= k$ is $2\/4^k$. This is an exponentially stronger quantitative bound, but on a different (more restricted) quantity.

*Methods.* Tao's proof uses entropy methods in 3-adic analysis, Syracuse random variables, and concentration inequalities. The FMF proof uses elementary mod-8 arithmetic and the unit structure of 2-adic integers. The FMF approach is entirely self-contained and requires no machinery beyond undergraduate algebra.

*The shared wall.* Despite these differences, both approaches encounter the same fundamental barrier: neither can cross from "almost all" to "all." In Tao's framework, the obstacle is that logarithmic density cannot distinguish a set of density zero from the empty set. In the FMF framework, the obstacle is that 2-adic Haar measure assigns measure zero to $ZZ subset ZZ_2$, so ergodic equidistribution in $ZZ_2$ does not formally imply that every integer trajectory equidistributes. The two formulations of the gap are, at a deep level, the same problem.

== The $5n+1$ litmus test

A useful test for any framework claiming insight into the Collatz conjecture is whether it can distinguish $3n+1$ (conjectured to converge) from $5n+1$ (known to have divergent trajectories, starting from $n = 13$).

The FMF framework passes this test at the structural level but not at the pointwise level. Specifically:

- *State independence holds for $5n+1$.* The FMF hop output distribution for $5n+1$ is state-independent, for the same algebraic reason: $5^(t+2)$ is a 2-adic unit.
- *The $v_2$ geometric distribution holds for $5n+1$.* The distribution $P(v_2 = j) = 1\/2^j$ is a property of 2-adic units, not of the specific multiplier.
- *The Quartering Law structure holds for $5n+1$.* Growth chains in the $5n+1$ system also have geometric length distributions.

The discriminant is the _contraction channel_. For the map $a n + 1$, Type A hops (inputs $equiv 1 mod 4$) have ratio $a\/4$ before the $v_2$ correction. The integer $3$ is the only odd value where $a\/4 < 1$. This means:

- For $3n+1$: Type A hops _always_ shrink (ratio $3\/4$ before further division). Since Type A hops occur with probability $1\/2$, half of all hops provide guaranteed contraction.
- For $5n+1$: Type A hops have ratio $5\/4 > 1$. No hop type provides guaranteed contraction. The expected drift is positive, correctly predicting divergence.

The FMF framework thus correctly identifies _why_ $3n+1$ should converge and $5n+1$ should diverge. But the identification is at the level of expected values and spectral radii, not at the level of individual trajectories. The gap between the two remains.

== Why the gap is hard

The gap between "almost all orbits converge" and "all orbits converge" is not a technical limitation of this paper. It is a reflection of a deep mathematical obstruction that affects all known approaches.

*Tao's barrier.* Tao has observed that any proof of the Collatz conjecture must either exploit existing results in transcendence theory or diophantine approximation, or contribute genuinely new methods to one of these areas. The FMF framework's 2-adic analysis, while providing structural insight, does not engage with transcendence theory. It establishes equidistribution of $3^n mod 2^K$ for fixed $K$ and growing $n$, but this is a standard fact about multiplicative groups modulo prime powers. The hard part --- controlling what happens for $K$ growing with $n$ --- requires quantitative equidistribution estimates that are not available from mod-$8$ arguments alone.

*Baker's theorem.* One might hope that Baker's theorem on linear forms in logarithms could close the gap, since it provides lower bounds on $|a log 2 - b log 3|$. For a growth chain of length $k$, the accumulated growth is approximately $3^(k(t+2))\/2^(2k)$, and the question is whether this can remain close to $1$ (preventing descent). Baker's theorem gives $|a log 2 - b log 3| > C \/ b^mu$ for effective constants $C, mu$. However, for the actual growth chains arising in FMF dynamics, the linear forms $a log 2 - b log 3$ are vastly larger than Baker's lower bound. Baker's theorem bounds the wrong thing: it controls archimedean proximity (how close $2^a$ is to $3^b$ in $RR$), while the FMF dynamics are governed by 2-adic proximity (how close $3^n$ is to $1$ in $ZZ_2$). These are complementary, not interchangeable, conditions.

*The precise remaining question.* The gap reduces to a single question in $p$-adic dynamics:

#conjecture(name: "Growth-B Domain Emptiness")[
  The growth-B map $m arrow.r.bar op("odd_part")((3^(t+2) m + 1)\/8)$, restricted to the growth-B domain of $ZZ_2$ (those $m$ with $3^(t+2) m equiv 7 mod 8$ and output again in the growth-B domain), has no infinite orbit in $ZZ$.
]

Equivalently: does there exist an odd positive integer $m_0$ such that the growth-B iteration, started at $m_0$, never exits the growth-B domain? If no such $m_0$ exists, the Collatz conjecture follows (combined with the spectral contraction and cycle exclusion results). If such an $m_0$ exists, it would provide a counterexample to the conjecture.

The 2-adic expansion property (Proposition 5.2) shows that the growth-B map is expanding on $ZZ_2$ with factor $>= 8$, which implies no positive-measure invariant set exists in the growth-B domain of $ZZ_2$. But $ZZ$ has Haar measure zero in $ZZ_2$. Closing this gap would require new mathematics: either effective equidistribution results for expanding maps on $ZZ_2$ that apply to integer orbits, or $p$-adic Littlewood-type results that constrain how long an integer orbit can remain in a prescribed region of $ZZ_2$.

== Summary

The FMF framework establishes:
- That the Collatz map, when viewed through the FMF decomposition, has a clean algebraic structure with exact formulas (Theorem A), universal output distributions (Theorem B), strict average contraction (Theorem C), and exponentially decaying growth chains (Theorem D).
- That these properties correctly distinguish $3n+1$ from $5n+1$ at the structural level.
- That the remaining gap is a precise, well-defined question in $p$-adic dynamics, not a vague "we need better bounds."

What it does not establish is the conjecture itself. The honest conclusion is that the FMF framework provides the strongest known elementary density bounds for Collatz growth chains, but the passage from density bounds to universal convergence remains a frontier problem.
