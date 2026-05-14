#import "../lib/theorem.typ": *

= State Distributions

The central structural result of the FMF framework is that, when inputs are counted by natural density inside a fixed FMF input state, the output state law is the same for every input state. This is a density theorem, not a statement that a single deterministic trajectory has independent successive states.

#theorem(name: "Theorem B: State Distribution")[
  Let $F(x)$ denote the FMF hop output. Fix any FMF input state: Type A, Type B with $t = 0$, or Type B with fixed $t gt.eq 1$. As the free parameter in that state ranges over residue classes modulo $2^K$ (over odd residues for the B2 parameter $m$) and $K arrow.r infinity$, the output state distribution is independent of the chosen input state. Specifically,

  $ PP(F(x) "is Type A") &= 1 / 2, \
    PP(F(x) "is Type B with depth" t' = j) &= 1 / 2^(j+2) quad "for" j gt.eq 0. $
]

#proof[
  It suffices to treat the general Type B2 case; the Type A and Type B0 cases are the same argument with different odd affine forms.

  Let $x = 4k + 3$ with $k$ odd and $k + 1 = 2^t m$ ($m$ odd, $t gt.eq 1$). By Theorem A, $op("FMF")(x) = 2(3^(t+2) m - 1)$ and
  $ F(x) = (3^(t+2) m - 1) / 2^(v_2(3^(t+2) m - 1)). $

  *Step 1: valuation distribution.* Since $3^(t+2)$ is a $2$-adic unit, we have
  $ v_2(3^(t+2) m - 1) = v_2(m - (3^(t+2))^(-1)) $
  where $(3^(t+2))^(-1) in ZZ_2$ is the $2$-adic inverse. This inverse is odd. As $m$ ranges uniformly over odd residues modulo $2^K$, the difference $m - (3^(t+2))^(-1)$ ranges uniformly over even residues modulo $2^K$. Therefore, in the limit $K arrow.r infinity$,
  $ PP(v_2(m - (3^(t+2))^(-1)) = j) = 1 / 2^j quad "for" j gt.eq 1. $

  *Step 2: odd part uniformity.* Conditional on $v_2(m - (3^(t+2))^(-1)) = j$, write $m - (3^(t+2))^(-1) = 2^j u$ in $ZZ_2$, with $u$ odd. The odd part $u$ is uniformly distributed among odd residues modulo every fixed $2^L$ once $K$ is large enough. In $ZZ_2$,
  $ 3^(t+2) m - 1 = 2^j dot 3^(t+2) u, $
  hence $F(x) equiv 3^(t+2) u mod 2^L$ for every fixed $L$. Multiplication by the odd unit $3^(t+2)$ permutes odd residues, so $F(x)$ is uniformly distributed among odd residues modulo $2^L$.

  *Step 3: output type distribution.* Taking $L = 2$ gives
  $ PP(F(x) equiv 1 mod 4) = PP(F(x) equiv 3 mod 4) = 1 / 2. $
  For Type B outputs with $F(x) = 4k' + 3$, writing $k' + 1 = 2^(t') m'$ with $m'$ odd, the usual valuation count gives
  $ PP(t' = j | F(x) "is Type B") = 1 / 2^(j+1) quad "for" j gt.eq 0. $
  Combined with $PP("Type B") = 1\/2$, this gives $PP("Type B with depth" t' = j) = 1\/2^(j+2)$.

  *Step 4: input-state independence.* None of the counts above depends on the value of $t$ except through multiplication by a fixed odd unit and subtraction of a fixed odd $2$-adic inverse. Both operations preserve the relevant residue counts. The Type A and Type B0 cases produce analogous odd affine forms, so the same distribution follows.
]

#v(0.5em)

#remark[
  This theorem should not be read as stochastic independence along a fixed Collatz orbit. It is a natural-density statement over all inputs in a fixed state. Successive states on one deterministic trajectory can be correlated, and those correlations are exactly where the pointwise Collatz difficulty remains.
]

== Consequences of the State Distribution

The state distribution has immediate average consequences for the hop dynamics.

#observation(name: "Negative Expected Drift")[
  The expected logarithmic growth per FMF hop is
  $ EE[log_2(F(x) \/ x)] = -0.830 "bits per hop." $
  Decomposing by type: Type A contributes $-1.415$ bits (always shrinks), while Type B with depth $t$ contributes $0.585(t + 2) - 3$ bits. The overall probability of shrinkage is $PP(F(x) < x) = 71.4%$.
]

#v(0.3em)

The negative drift means that a "typical" hop reduces $x$ by a factor of roughly $2^(0.83)$. However, drift alone does not prove convergence --- rare large-$t$ hops can produce exponential growth, and it is the _tail behavior_ of these growth events that determines whether all trajectories converge.

In density, severe growth events are followed by Type A outputs half the time, and Type A hops always shrink. This is a useful average self-correction mechanism. It does not, by itself, rule out exceptional deterministic orbits that repeatedly land in the growth-favoring residue classes.
