#import "../lib/theorem.typ": *

= State Independence

The central structural result of the FMF framework is that the output of a hop "forgets" the input. This is not an empirical observation or a heuristic assumption: it is a theorem following from the arithmetic of $2$-adic inverses.

#theorem(name: "State Independence")[
  Let $x$ be any odd positive integer, and let $F(x)$ denote the FMF hop output. The distribution of the output state --- the mod-$4$ class and depth parameter of $F(x)$ --- is independent of the input state. Specifically, as $x$ ranges uniformly over odd numbers in any residue class:

  $ PP(F(x) "is Type A") &= 1 / 2, \
    PP(F(x) "is Type B with depth" t' = j) &= 1 / 2^(j+2) quad "for" j gt.eq 0. $

  These probabilities hold regardless of whether the input $x$ is Type A, Type B with depth $t = 0$, or Type B with any depth $t gt.eq 1$.
]

#proof[
  We treat the general Type B2 case; the other cases are similar (and simpler).

  Let $x = 4k + 3$ with $k$ odd and $k + 1 = 2^t m$ ($m$ odd, $t gt.eq 1$). By Theorem A, $op("FMF")(x) = 2(3^(t+2) m - 1)$ and
  $ F(x) = (3^(t+2) m - 1) / 2^(v_2(3^(t+2) m - 1)). $

  *Step 1: Valuation distribution.* Since $3^(t+2)$ is a $2$-adic unit, we have
  $ v_2(3^(t+2) m - 1) = v_2(m - (3^(t+2))^(-1)) $
  where $(3^(t+2))^(-1) in ZZ_2$ is the $2$-adic inverse. This inverse is an odd number (since $3^(t+2)$ is odd and the $2$-adic inverse of an odd number is odd). As $m$ ranges over odd positive integers, the difference $m - (3^(t+2))^(-1)$ is even (odd minus odd), and its $2$-adic valuation follows an exact geometric distribution:
  $ PP(v_2(m - (3^(t+2))^(-1)) = j) = 1 / 2^j quad "for" j gt.eq 1. $
  This is a standard property of $2$-adic distances: among all even integers, the fraction with $v_2 = j$ is exactly $1\/2^j$.

  *Step 2: Odd part uniformity.* Writing $m - (3^(t+2))^(-1) = 2^j dot u$ where $u$ is the odd part, $u$ is uniformly distributed among odd integers (conditional on $v_2 = j$). The hop output is
  $ F(x) = (3^(t+2) m - 1) / 2^j = 3^(t+2) dot u + (3^(t+2) dot (3^(t+2))^(-1) - 1) / 2^j. $
  Simplifying: $3^(t+2) m - 1 = 3^(t+2)(2^j u + (3^(t+2))^(-1)) - 1 = 2^j dot 3^(t+2) u + (1 - 1) = 2^j dot 3^(t+2) u$, so $F(x) = 3^(t+2) u$. Since $3^(t+2)$ is an odd constant and $u$ is uniformly distributed among odd integers, $F(x) = 3^(t+2) u$ is also uniformly distributed among odd integers (multiplication by an odd constant is a bijection on odd integers).

  *Step 3: Output type distribution.* Since $F(x)$ is uniform among odd integers:
  $ PP(F(x) equiv 1 mod 4) = PP(F(x) equiv 3 mod 4) = 1 / 2. $
  For Type B outputs with $F(x) = 4k' + 3$ and $k'$ odd, writing $k' + 1 = 2^(t') m'$:
  $ PP(t' = j) = 1 / 2^(j+1) quad "for" j gt.eq 0. $
  Combined with $PP("Type B") = 1\/2$, this gives $PP("Type B with depth" t' = j) = 1\/2^(j+2)$.

  *Step 4: Independence.* Crucially, none of the above depends on the specific value of $t$ in the input. The distribution of $v_2(m - (3^(t+2))^(-1))$ is geometric _for every_ value of the $2$-adic inverse $(3^(t+2))^(-1)$, since the geometric law depends only on $m$ being odd, not on the particular odd number being subtracted. The same argument applies to Type A and Type B1 inputs, which produce analogous $2$-adic expressions with different constants but identical distributional properties.
]

#v(0.5em)

#remark[
  State independence is related to, but distinct from, the "rapid mixing" observations of Kontorovich and Lagarias @kontorovich2009, who studied the distribution of Collatz iterates modulo $2^k$ and found that residue class distributions equilibrate quickly. The FMF result is stronger in a precise sense: it shows that a _single_ hop completely erases the input state, rather than requiring multiple steps for approximate mixing. The mechanism is different as well --- the proof exploits the exact algebraic structure of $2$-adic inverses rather than ergodic properties of the iteration.
]

== Consequences of State Independence

State independence has immediate probabilistic consequences for the hop dynamics.

#observation(name: "Negative Expected Drift")[
  The expected logarithmic growth per FMF hop is
  $ EE[log_2(F(x) \/ x)] = -0.830 "bits per hop." $
  Decomposing by type: Type A contributes $-1.415$ bits (always shrinks), while Type B with depth $t$ contributes $0.585(t + 2) - 3$ bits. The overall probability of shrinkage is $PP(F(x) < x) = 71.4%$.
]

#v(0.3em)

The negative drift means that a "typical" hop reduces $x$ by a factor of roughly $2^(0.83)$. However, drift alone does not prove convergence --- rare large-$t$ hops can produce exponential growth, and it is the _tail behavior_ of these growth events that determines whether all trajectories converge.

State independence is itself a self-correction mechanism: regardless of how severe a growth event is, the very next hop has probability $1\/2$ of being Type A (which always shrinks). The dynamics cannot "lock in" to a growth mode --- every hop resets the odds. Making this quantitative requires the contraction analysis of the next section.
