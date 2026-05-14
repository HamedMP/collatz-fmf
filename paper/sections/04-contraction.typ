#import "../lib/theorem.typ": *

= Fractional-Moment Contraction and the $3\/4$ Discriminant

The FMF decomposition cleanly isolates the elementary contraction channel in the $3n+1$ problem. For the generalized map $C_a(n) = a n + 1$, the first value divisible by $4$ has asymptotic ratio $a\/4$ on the immediate-FMF residue class. The multiplier $a = 3$ is the largest odd value for which this channel contracts. I then use the state-distribution theorem to compute an exact asymptotic fractional moment for the FMF hop ratio.

== The $a\/4$ Discriminant

#lemma(name: "The $a\/4$ Discriminant")[
  Consider the generalized odd branch $C_a(n) = a n + 1$ for odd $a gt.eq 3$. There is a unique odd residue class modulo $4$ on which $a x + 1$ is divisible by $4$, namely $x equiv -a^(-1) mod 4$. On that immediate-FMF channel the odd hop has asymptotic ratio $a\/4$ before any extra powers of $2$ are stripped.

  For $a = 3$, the immediate channel is $x equiv 1 mod 4$, and every nontrivial such hop shrinks. For every odd $a gt.eq 5$, the immediate channel has asymptotic ratio $a\/4 > 1$, so this deterministic contraction channel disappears.
]

#proof[
  Since $a$ is odd, it is invertible modulo $4$. Thus $a x + 1 equiv 0 mod 4$ exactly when $x equiv -a^(-1) mod 4$. On this residue class, write $x = 4k + r$ with fixed odd $r$. Then $a x + 1 = 4(a k + c)$ for an integer constant $c$ depending only on $a$ and $r$. After dividing by at least this factor $4$, the odd output is at most $a k + c$, while the input is $4k + r$, so the asymptotic ratio is $a\/4$.

  For $a = 3$, the immediate residue is $r = 1$, and $3(4k+1)+1 = 4(3k+1)$. The hop output is $(3k+1)\/2^(v_2(3k+1)) lt 4k+1$ for every $k gt.eq 1$. For odd $a gt.eq 5$, the same immediate channel has limiting ratio $a\/4 > 1$, so it cannot supply a uniform pointwise contraction analogous to the $3n+1$ Type A hop.
]

#v(0.3em)

The discriminant reveals that $3$ occupies a unique position: it is the largest odd integer below $4$. This is the elementary reason that the $3n+1$ FMF dynamics have a deterministic contraction channel of density $1\/2$.

#remark[
  For $a = 1$ (the map $n + 1$), the dynamics are trivially bounded. For $a = 3$, the competition between Type A shrinkage and Type B growth is delicate. For $a gt.eq 5$, the immediate-FMF channel no longer contracts, and the analogous random-walk drift becomes positive in the standard $5n+1$ model.
]

== Fractional-Moment Contraction

#theorem(name: "Fractional-Moment Contraction")[
  Let $R(x) = F(x)\/x$ be the FMF hop ratio. In natural density over odd inputs, the asymptotic fractional moment of $R$ is

  $ M(alpha) &= 1\/2 dot (3\/4)^alpha / (2 - 2^(-alpha)) \
    &quad + 1\/4 dot (9\/4)^alpha / (2^(1+alpha) - 1) \
    &quad + sum_(t=1)^(infinity) 1\/2^(t+2) dot ((3\/2)^(t+2))^alpha / (2^(1+alpha) - 1). $

  The series converges for $alpha < log 2 \/ log(3\/2)$. At $alpha = 0.53$,
  $ M(0.53) approx 0.8638 < 1. $
  The critical exponent satisfying $M(alpha^*) = 1$ is approximately $alpha^* = 1.0002$.
]

#proof[
  I compute the three FMF input cases separately, ignoring only the lower-order additive constants in the ratio; these vanish in natural density as the free parameter tends to infinity.

  *Type A.* For $x = 4k + 1$, $F(x) = (3k+1) \/ 2^J$ with $J = v_2(3k+1)$. As $k$ ranges by natural density, $PP(J = j) = 2^(-(j+1))$ for $j gt.eq 0$. The asymptotic ratio is $(3\/4) 2^(-J)$, so
  $ EE[R^alpha | A] = (3\/4)^alpha sum_(j=0)^(infinity) 2^(-(j+1)) 2^(-alpha j) = (3\/4)^alpha / (2 - 2^(-alpha)). $

  *Type B0.* For $x = 8j + 3$, $F(x) = (9j+4) \/ 2^J$ with $J = v_2(9j+4)$ and the same distribution $PP(J = j) = 2^(-(j+1))$. The asymptotic ratio is $(9\/8) 2^(-J)$, equivalently $(9\/4) 2^(-W)$ with $W gt.eq 1$ geometric, hence
  $ EE[R^alpha | "B0"] = (9\/4)^alpha / (2^(1+alpha) - 1). $

  *Type B with $t gt.eq 1$.* For $x = 2^(t+2)m - 1$, $F(x) = (3^(t+2)m - 1) \/ 2^J$ with $J = v_2(3^(t+2)m - 1)$. Since $3^(t+2)m - 1$ is always even, $PP(J = j) = 2^(-j)$ for $j gt.eq 1$. The asymptotic ratio is $(3\/2)^(t+2) 2^(-J)$, so
  $ EE[R^alpha | B(t)] = ((3\/2)^(t+2))^alpha / (2^(1+alpha) - 1). $

  Finally, the input-state densities are $PP(A) = 1\/2$, $PP("B0") = 1\/4$, and $PP(B(t)) = 2^(-(t+2))$ for $t gt.eq 1$. Summing the three contributions gives $M(alpha)$. Numerical evaluation gives $M(0.53) approx 0.8638$ and $M(alpha^*) = 1$ at $alpha^* approx 1.0002$.
]

== Inverse Movement Rate

The following lemma quantifies how quickly the $2$-adic inverses shift as the depth parameter changes, providing structural insight into the transition between consecutive hops.

#lemma(name: "Inverse Movement Rate")[
  For any odd integer $a gt.eq 3$ and any $t gt.eq 0$,
  $ v_2(a^(-(t+3)) - a^(-(t+2))) = v_2(1 - a) $
  where the inverses are $2$-adic. For $a = 3$: shift $= 1$ bit (minimum possible). For $a = 5$: shift $= 2$ bits.
]

#proof[
  The difference factors as
  $ a^(-(t+3)) - a^(-(t+2)) = a^(-(t+2))(a^(-1) - 1). $
  Since $a$ is a $2$-adic unit, so is $a^(-(t+2))$, and $v_2(a^(-(t+2))) = 0$. Therefore
  $ v_2(a^(-(t+3)) - a^(-(t+2))) = v_2(a^(-1) - 1) = v_2((1 - a) / a) = v_2(1 - a) $
  using $v_2(a) = 0$.

  For $a = 3$: $v_2(1 - 3) = v_2(-2) = 1$. For $a = 5$: $v_2(1 - 5) = v_2(-4) = 2$.
]

#v(0.3em)

The $1$-bit minimum shift for $a = 3$ means that consecutive $2$-adic inverses are maximally "close" in the $2$-adic metric, producing the slowest possible decorrelation between consecutive hops. This is another facet of why $3n + 1$ sits at the boundary: the dynamics are contractive, but only barely, with the tightest possible coupling between successive states.

#remark[
  The fractional-moment contraction $M(0.53) approx 0.8638 < 1$ is closely related to the average-contraction results of Carletti and Fanelli @carletti2017, who estimate Collatz Lyapunov exponents by different methods. The FMF derivation makes the contribution of the Type A contraction channel and the Type B valuation tail explicit.
]
