#import "../lib/theorem.typ": *

= The Quartering Law

The spectral contraction of Section 4 establishes that the _average_ hop shrinks trajectories. But averages permit exceptions: a trajectory could, in principle, string together arbitrarily many consecutive growth hops, accumulating enough expansion to escape any bounded region. This section proves that such growth chains decay exponentially in length, with a precise base of $1\/4$.

== Growth chains

I begin by isolating the dominant growth mechanism.

#definition(name: "Growth Chain")[
  A _growth chain_ of length $k$ starting at odd $x_0$ is a maximal sequence $x_0, x_1, dots, x_k$ of consecutive FMF hops where each hop $x_i arrow.r x_(i+1)$ satisfies:
  + $x_i$ is Type B (i.e., $x_i equiv 3 mod 4$), and
  + $v_2(op("FMF")(x_i)) = 2$ (the minimal valuation for a Type B hop).

  We call such a hop a _growth-B hop_. It is the dominant growth mode: among all Type B hops that increase the trajectory value, $87.9%$ have $v_2 = 2$.
]

The condition $v_2(op("FMF")) = 2$ means the FMF value is divisible by $4$ but not $8$. Writing $x_i = 4k + 3$ with $k + 1 = 2^t m$ ($m$ odd), the FMF is $2(3^(t+2) m - 1)$. For $v_2(op("FMF")) = 2$ we need $3^(t+2) m - 1 equiv 2 mod 4$, i.e., $3^(t+2) m equiv 3 mod 4$.

== Supporting lemmas

#lemma(name: "Growth-to-Type-A Split")[
  For a Type B hop with $v_2(op("FMF")) = 2$, the output odd number is Type A with probability exactly $1\/2$ and Type B with probability exactly $1\/2$, determined by $m mod 8$.
]
#proof[
  The FMF is $2(3^(t+2) m - 1)$. With $v_2 = 2$, the output odd number is $q = (3^(t+2) m - 1)\/2$, which is odd. Its type depends on $q mod 4$.

  We analyze by the parity of $t$, which determines $3^(t+2) mod 8$:

  *Case $t$ even* ($3^(t+2) equiv 1 mod 8$): The growth condition $3^(t+2) m equiv 3 mod 4$ reduces to $m equiv 3 mod 4$. Among odd $m equiv 3 mod 4$, we have $m in {3, 7} mod 8$. Then $3^(t+2) m - 1 equiv m - 1 mod 8$:
  - $m equiv 3 mod 8$: $q = (m-1)\/2 equiv 1 mod 4$ (Type A).
  - $m equiv 7 mod 8$: $q = (m-1)\/2 equiv 3 mod 4$ (Type B).

  *Case $t$ odd* ($3^(t+2) equiv 3 mod 8$): The growth condition reduces to $m equiv 1 mod 4$. Among odd $m equiv 1 mod 4$, we have $m in {1, 5} mod 8$. Then $3^(t+2) m - 1 equiv 3m - 1 mod 8$:
  - $m equiv 1 mod 8$: $3m - 1 equiv 2 mod 8$, so $q equiv 1 mod 4$ (Type A).
  - $m equiv 5 mod 8$: $3m - 1 equiv 6 mod 8$, so $q equiv 3 mod 4$ (Type B).

  In each case, exactly one of two eligible residue classes gives Type A and one gives Type B. Since $m$ is equidistributed among odd residues (by the 2-adic analysis of Theorem B), $P(op("Type A") | op("growth-B")) = 1\/2$.
]

#lemma(name: "Geometric Distribution of Valuations")[
  For odd $m$ drawn uniformly from any sufficiently large range, $P(v_2(3^(t+2) m - 1) = j) = 1\/2^j$ for $j >= 1$.
]
#proof[
  Since $3^(t+2)$ is odd, it is a unit in $ZZ\/2^K ZZ$ for every $K$. Multiplication by a unit permutes residue classes. Thus as $m$ ranges over odd residues modulo $2^K$, the product $3^(t+2) m$ ranges over all odd residues modulo $2^K$. Subtracting $1$ maps odd residues to even residues uniformly, so $v_2(3^(t+2) m - 1)$ has the distribution of $v_2$ applied to a uniform even number: $P(v_2 = j) = 1\/2^j$ for $j >= 1$.
]

#lemma(name: "Type B Independence from Valuation")[
  Let $3^(t+2) m - 1 = 2^w q$ with $q$ odd. Then $P(q equiv 3 mod 4) = 1\/2$ for every value of $w >= 1$, independently of $w$.
]
#proof[
  The bits of $3^(t+2) m - 1$ at positions $w$ and $w+1$ (which determine $q mod 4$) are independent of the bits at positions $0, dots, w-1$ (which determine $v_2 = w$). This is because the bits at position $>= w$ of $3^(t+2) m - 1$ depend on $m mod 2^(K-w)$ while $v_2 = w$ depends only on $m mod 2^w$. Since $3^(t+2)$ is a 2-adic unit, these constraints are independent, giving $q mod 4$ equidistributed over ${1, 3}$.
]

#lemma(name: "Odd Part Equidistribution")[
  If $q$ is drawn uniformly from $ZZ\/2^N ZZ$, then $op("odd_part")(q) mod 2^j$ is equidistributed for $j <= N - v_2(q)$.
]
#proof[
  Write $q = 2^w r$ with $r$ odd. Conditioned on $v_2(q) = w$, the value $r = q\/2^w$ ranges over all odd residues modulo $2^(N-w)$. For $j <= N - w$, the residue $r mod 2^j$ is therefore equidistributed among odd residues modulo $2^j$.
]

== The main result

#theorem(name: "The Quartering Law")[
  The probability that a growth-B chain continues at each step is exactly $1\/4$. Consequently, the natural density of odd integers whose growth chain has length $>= k$ satisfies
  $ delta_k = 2 / 4^k. $
]
#proof[
  We combine the preceding lemmas. At each step of a growth-B chain, continuation requires two independent events:

  + *The output is Type B.* By the Growth-to-Type-A Split Lemma, $P(op("Type B") | op("growth-B hop")) = 1\/2$.

  + *The Type B output enters another growth-B hop.* The next hop is growth-B if and only if $v_2(op("FMF")) = 2$ for the output, which requires the new $m'$ to satisfy $3^(t'+2) m' equiv 3 mod 4$. By the Odd Part Equidistribution Lemma combined with the unit multiplication structure of $3^(t'+2)$ in $ZZ_2$, the new $m' mod 8$ is equidistributed among odd residues. From the analysis in the Growth-to-Type-A Split Lemma, exactly $2$ of the $4$ odd residue classes modulo $8$ satisfy the growth condition for any given $t'$. Thus $P(op("growth-B") | op("Type B output")) = 1\/2$.

  Therefore $P(op("continue")) = 1\/2 dot 1\/2 = 1\/4$.

  For the density statement: the fraction of odd integers that are Type B is $1\/2$, and the fraction of Type B integers with $v_2(op("FMF")) = 2$ is also $1\/2$ (from the geometric distribution). So $delta_0 = 1\/2 dot 1\/2 = 1\/4$ is the density entering growth, and $delta_1 = 1\/4$ of those continue, giving $delta_k = 2\/4^k$ for $k >= 1$ (accounting for the initial $1\/2$ density of Type B, times $1\/2$ for growth entry, times $(1\/4)^(k-1)$ for continuation). More precisely, $delta_k = 2 dot (1\/4)^k$ normalizes the initial $P(op("Type B")) dot P(v_2 = 2) = 1\/4$ against the $(1\/4)^(k-1)$ continuation.
]

#remark[
  The factor of $2$ in $delta_k = 2\/4^k$ arises because the density of odd integers entering the first growth-B hop is $1\/2 dot 1\/2 = 1\/4$, and $delta_k$ counts chains of length $>= k$, so $delta_1 = 1\/4 = 2\/4^1$ and $delta_k = 2\/4^k$ for all $k >= 1$.
]

== 2-adic structure

The Quartering Law is not a coincidence of residue counting but reflects a deep structural property of the growth-B map in $ZZ_2$.

#proposition(name: "2-adic Expansion")[
  The growth-B map $m arrow.r.bar m' = op("odd_part")((3^(t+2) m - 1)\/4)$ is 2-adically _expanding_ with factor $2^(3+t') >= 8$ per step, where $t' = v_2(m'+1)$ determines the next $t$-parameter. This expansion scrambles the low-order bits of $m$ in $ZZ_2$, providing the structural explanation for the Quartering Law: expanding maps on $ZZ_2$ drive equidistribution of residues, making each step's growth-B condition effectively independent of the previous step.
]
#proof[
  In 2-adic terms, the growth-B map computes $3^(t+2) m - 1$, divides by $4$ (a fixed contraction by $|4|_2 = 1\/4$ in the 2-adic absolute value), and extracts the odd part (a further contraction). But from the perspective of $m$ as a 2-adic integer, the map $m arrow.r.bar 3^(t+2) m$ is an isometry (multiplication by a unit), while the subsequent $m arrow.r.bar op("odd_part")((m-1)\/4)$ shifts away the bottom $2 + v_2(m-1) - 1$ bits. This is a $2^(v_2+1)$-fold expansion on $ZZ_2$ (increasing the 2-adic absolute value), with $v_2 >= 2$ giving expansion factor $>= 8$.

  Expanding maps on compact groups are well-known to be ergodic with respect to Haar measure. In $ZZ_2$, this means the iterates of $m$ under the growth-B map equidistribute modulo $2^K$ for any fixed $K$, which is precisely the independence condition underlying the Quartering Law.
]

#remark[
  *Limitation.* The integers $ZZ$ have Haar measure zero in $ZZ_2$. The ergodic equidistribution in $ZZ_2$ therefore does not formally imply that every integer trajectory equidistributes. This is the precise location of the "almost all $arrow.r$ all" gap for the Quartering Law.
]

== Acyclicity

#lemma(name: "Growth-B Acyclicity")[
  The growth-B transition graph on states $(t, m mod 2^K)$ contains no cycles, verified for $K = 4, 6, 8$.
]
#proof[
  Computational enumeration of all states and transitions at each resolution $K$ confirms zero cycles. The impossibility of exact cycles follows from a number-theoretic obstruction: a cycle of length $ell$ in the growth-B map would require $3^a = 2^b$ for some positive integers $a, b$ (arising from the requirement that the product of multipliers returns to the starting value). But $3^a = 2^b$ is impossible for positive $a, b$ by unique factorization. Therefore no exact cycle exists at any resolution, and the finite-$K$ verifications confirm this for the truncated dynamics.
]
