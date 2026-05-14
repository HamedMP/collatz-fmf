#import "../lib/theorem.typ": *

= The Quartering Law

The fractional-moment contraction of Section 4 establishes that the _average_ hop shrinks trajectories. But averages permit exceptions: a trajectory could, in principle, string together arbitrarily many consecutive growth hops, accumulating enough expansion to escape any bounded region. This section proves a density theorem for the dominant strict growth mechanism, with a precise continuation factor of $1\/4$.

== Growth chains

The argument begins by isolating the dominant growth mechanism.

#definition(name: "Growth-B Chain")[
  A _growth-B chain_ of length $k$ starting at odd $x_0$ is a maximal sequence $x_0, x_1, dots, x_k$ of consecutive FMF hops where each hop $x_i arrow.r x_(i+1)$ satisfies:
  + $x_i$ is Type B (i.e., $x_i equiv 3 mod 4$), and
  + $v_2(op("FMF")(x_i)) = 2$ (the minimal valuation for a Type B hop).

  We call such a hop a _growth-B hop_. It is the dominant strict growth mode in the computations: among all Type B hops that increase the trajectory value, $87.9%$ have $v_2 = 2$.
]

The condition $v_2(op("FMF")) = 2$ means the FMF value is divisible by $4$ but not $8$. Writing $x_i = 4k + 3$ with $k + 1 = 2^t m$ ($m$ odd), the FMF is $2(3^(t+2) m - 1)$. For $v_2(op("FMF")) = 2$ we need $3^(t+2) m - 1 equiv 2 mod 4$, i.e., $3^(t+2) m equiv 3 mod 4$.

#lemma(name: "Growth-B Hops Strictly Grow")[
  Every growth-B hop satisfies
  $ F(x) / x > 9\/8. $
]
#proof[
  For a growth-B hop, write $x = 2^(t+2)m - 1$ with $t >= 0$ and $m$ odd. Since $v_2(op("FMF")) = 2$,
  $ F(x) = (3^(t+2)m - 1) / 2. $
  It is enough to show $8F(x) > 9x$, i.e.
  $ 4(3^(t+2)m - 1) > 9(2^(t+2)m - 1). $
  For $t = 0$, this becomes $36m - 4 > 36m - 9$. For $t >= 1$, the coefficient inequality $4 dot 3^(t+2) > 9 dot 2^(t+2)$ is already strict, and the constant term also favors the left side by $5$. Hence $F(x)\/x > 9\/8$ in all cases.
]

== Supporting lemmas

#lemma(name: "Growth-to-Type-A Split")[
  For a Type B hop with $v_2(op("FMF")) = 2$, the output odd number is Type A on exactly half of the eligible residue classes modulo $8$ and Type B on the other half.
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

  In each case, exactly one of two eligible residue classes gives Type A and one gives Type B. Therefore the natural density over eligible growth-B inputs satisfies $P(op("Type A") | op("growth-B")) = 1\/2$.
]

#lemma(name: "Geometric Distribution of Valuations")[
  For odd $m$ drawn uniformly from any sufficiently large range, $P(v_2(3^(t+2) m - 1) = j) = 1\/2^j$ for $j >= 1$.
]
#proof[
  Since $3^(t+2)$ is odd, it is a unit in $ZZ\/2^K ZZ$ for every $K$. Multiplication by a unit permutes residue classes. Thus as $m$ ranges over odd residues modulo $2^K$, the product $3^(t+2) m$ ranges over all odd residues modulo $2^K$. Subtracting $1$ maps odd residues to even residues uniformly, so $v_2(3^(t+2) m - 1)$ has the distribution of $v_2$ applied to a uniform even number: $P(v_2 = j) = 1\/2^j$ for $j >= 1$.
]

#lemma(name: "Type B Independence from Valuation")[
  Let $3^(t+2) m - 1 = 2^w q$ with $q$ odd. In natural density over odd $m$, $P(q equiv 3 mod 4 | w) = 1\/2$ for every value of $w >= 1$.
]
#proof[
  Fix $w$ and work modulo $2^(w+2)$. The condition $v_2(3^(t+2)m - 1) = w$ fixes $m$ modulo $2^w$ but leaves exactly two lifts modulo $2^(w+2)$ that preserve the valuation. Since multiplication by $3^(t+2)$ is a unit, these two lifts give the two possible odd residues $q equiv 1, 3 mod 4$ once each.
]

#lemma(name: "Odd Part Equidistribution")[
  If $q$ is drawn uniformly from $ZZ\/2^N ZZ$, then $op("odd_part")(q) mod 2^j$ is equidistributed for $j <= N - v_2(q)$.
]
#proof[
  Write $q = 2^w r$ with $r$ odd. Conditioned on $v_2(q) = w$, the value $r = q\/2^w$ ranges over all odd residues modulo $2^(N-w)$. For $j <= N - w$, the residue $r mod 2^j$ is therefore equidistributed among odd residues modulo $2^j$.
]

== The main result

#theorem(name: "Theorem D: The Quartering Law")[
  In natural density, conditional on being in a growth-B hop, the density factor for one additional growth-B continuation is exactly $1\/4$. Consequently, among odd starting integers, the density of starts whose strict growth-B chain has length at least $k$ is
  $ delta_k = 4^(-k) quad (k gt.eq 1). $
  Equivalently, among Type B starts $x equiv 3 mod 4$, the conditional density is $2 \/ 4^k$.
]
#proof[
  We combine the preceding lemmas as a residue-counting argument. Given a current growth-B hop, continuation requires two conditions on the output:

  + *The output is Type B.* By the Growth-to-Type-A Split Lemma, exactly half of the eligible residue classes give Type B output.

  + *The Type B output enters another growth-B hop.* The next hop is growth-B if and only if $v_2(op("FMF")) = 2$ for the output, which imposes one additional half-density residue condition on the new odd parameter $m'$. By the Odd Part Equidistribution Lemma combined with the unit multiplication structure of $3^(t'+2)$ in $ZZ_2$, the relevant odd residues of $m'$ are equidistributed modulo $8$ in natural density. Thus exactly half of the Type B outputs continue as growth-B.

  Therefore the density factor for continuation is $1\/2 dot 1\/2 = 1\/4$.

  For the density among all odd starts: the fraction of odd integers that are Type B is $1\/2$, and within Type B the fraction with $v_2(op("FMF")) = 2$ is $1\/2$. Thus $delta_1 = 1\/4$. Each further continuation multiplies density by $1\/4$, so
  $ delta_k = 1\/4 dot (1\/4)^(k-1) = 4^(-k). $
  If one conditions from the start on $x equiv 3 mod 4$, the initial Type B factor $1\/2$ is removed and the conditional density becomes $2\/4^k$.
]

#remark[
  The normalization is easy to misstate. The formula $2\/4^k$ is correct only after conditioning on the input already being Type B. Among all odd inputs, the density is $4^(-k)$.
]

== 2-adic structure

The Quartering Law is not a coincidence of residue counting but reflects a deep structural property of the growth-B map in $ZZ_2$.

#proposition(name: "2-adic Expansion")[
  On the branch where a growth-B hop outputs another Type B value, the induced parameter map
  $ m arrow.r.bar m' = op("odd_part")((3^(t+2) m + 1)\/8) $
  is 2-adically _expanding_ with factor $2^(3+t') >= 8$ on pieces with fixed output valuation $t' = v_2((3^(t+2) m + 1)\/8)$. This expansion explains why low residue classes are rapidly redistributed in the density calculation behind the Quartering Law.
]
#proof[
  The growth-B map computes $q = (3^(t+2) m + 1)\/8$, then extracts $m' = op("odd_part")(q)$. For two inputs $m_1, m_2$ in the growth-B domain with the same output valuation $t'$: the difference $q_1 - q_2 = 3^(t+2)(m_1 - m_2)\/8$. Since $3^(t+2)$ is a 2-adic unit ($|3^(t+2)|_2 = 1$), we have $|q_1 - q_2|_2 = |m_1 - m_2|_2 \/ |8|_2 = 8|m_1 - m_2|_2$. Taking the odd part divides by $2^(t')$, giving total expansion $|m'_1 - m'_2|_2 = 2^(3+t') |m_1 - m_2|_2$, with minimum factor $8$ when $t' = 0$.

  This piecewise expansion is the mechanism behind the residue-counting result above: preimages of a fixed low-order residue class split into uniformly many residue classes at higher precision. It should not be interpreted as a pointwise equidistribution theorem for every integer orbit.
]

#remark[
  *Limitation.* The integers $ZZ$ have Haar measure zero in $ZZ_2$. Haar-measure and natural-density statements over residue classes therefore do not formally imply that every individual integer trajectory equidistributes. This is the precise location of the "almost all $arrow.r$ all" gap for the Quartering Law.
]

== Acyclicity

#lemma(name: "No Growth-B Cycles")[
  No cycle in positive integers can be composed entirely of growth-B hops.
]
#proof[
  By the Growth-B Hops Strictly Grow Lemma, every growth-B hop satisfies $F(x) > x$. Along a nonempty chain of such hops the odd value therefore increases strictly at every step, so it cannot return to an earlier positive integer.
]

#proposition(name: "No Eventually Periodic Growth-B Depth Pattern")[
  No infinite growth-B chain in positive integers can have an eventually periodic depth sequence $t_i$.
]
#proof[
  Along a growth-B continuation branch, the parameters satisfy
  $ 2^(t_(i+1)+3) m_(i+1) - 3^(t_i+2) m_i = 1. $
  Suppose that from some index onward the depths repeat with period $p$. Composing one period gives an affine relation
  $ B m_(n+p) = A m_n + C, $
  where
  $ A = product_(i=0)^(p-1) 3^(t_i+2), quad
     B = product_(i=0)^(p-1) 2^(t_(i+1)+3), quad
     C > 0. $
  Since the depth sequence is periodic, $sum_i t_(i+1) = sum_i t_i$, and therefore
  $ B / A = (8\/9)^p (2\/3)^(sum_i t_i) < 1. $
  Hence $B - A < 0$.

  Repeating the same period indefinitely forces $m_n$ into a nested sequence of congruence classes modulo $B^q$ for every $q$. These congruences converge in $ZZ_2$ to the unique fixed point of the period map,
  $ m_* = C / (B - A). $
  But $C > 0$ and $B - A < 0$, so $m_*$ is a negative rational number. A positive integer cannot equal this rational in $QQ_2$ unless it is equal to it in $QQ$, which is impossible. Therefore no positive integer growth-B chain can have an eventually periodic depth sequence.
]

#remark[
  This proposition rules out a concrete class of possible pointwise obstructions, but it does not exclude arbitrary nonperiodic depth sequences. The remaining hard case is an infinite growth-B chain whose depths do not eventually repeat.
]

#proposition(name: "Finite Growth-B Depth Words Are Realizable")[
  For every finite sequence of nonnegative integers $(t_0, dots, t_(L-1))$, there are infinitely many positive odd $m_0$ such that the growth-B chain starting from $x_0 = 2^(t_0+2)m_0 - 1$ has depth word exactly $(t_0, dots, t_(L-1))$ for its first $L$ growth-B hops.
]
#proof[
  It is enough to construct positive odd parameters $m_0, dots, m_(L-1)$ satisfying the continuation equations
  $ 2^(t_(i+1)+3)m_(i+1) - 3^(t_i+2)m_i = 1
     quad (0 <= i < L-1), $
  and the final growth-B condition
  $ 3^(t_(L-1)+2)m_(L-1) equiv 3 mod 4. $

  Choose $m_(L-1)$ first. The final condition imposes one residue class modulo $4$. Working backward, the equation at index $i$ determines
  $ m_i = (2^(t_(i+1)+3)m_(i+1) - 1) / 3^(t_i+2). $
  For $m_i$ to be an integer, $m_(i+1)$ must lie in one residue class modulo $3^(t_i+2)$, because $2^(t_(i+1)+3)$ is invertible modulo this odd modulus. Iterating backward gives finitely many congruence conditions on $m_(L-1)$ modulo powers of $3$, together with the modulo-$4$ final condition. These moduli are coprime to $4$, so the Chinese Remainder Theorem gives a single residue class modulo a finite modulus.

  Taking $m_(L-1)$ sufficiently large in that residue class makes every backward-defined $m_i$ positive. Each $m_i$ is odd because it is an odd integer divided by an odd power of $3$. The continuation equations then imply
  $ 3^(t_i+2)m_i - 1 = 2(2^(t_(i+1)+2)m_(i+1)-1), $
  whose parenthesized factor is odd; hence the $i$-th hop is growth-B and has next depth $t_(i+1)$. This realizes the prescribed word. Since the residue class contains infinitely many positive values of $m_(L-1)$, it yields infinitely many positive starts.
]

#remark[
  This proposition is a useful warning: no finite forbidden-pattern argument can prove growth-B termination. Every finite depth pattern occurs. A proof must exploit a genuinely infinite obstruction, such as showing that the unique $2$-adic code for an infinite nonperiodic depth sequence cannot be a positive integer.
]

#lemma(name: "Growth-B Congruence Normal Form")[
  In any growth-B continuation branch
  $ 2^(t_(i+1)+3)m_(i+1) - 3^(t_i+2)m_i = 1, $
  the next odd parameter satisfies
  $ m_(i+1) equiv (-1)^(t_(i+1)+3) mod 3. $
  Consequently, after discarding at most the initial state of an infinite continuation branch, every continuing state satisfies
  $ m_i equiv 23 mod 24 $ if $t_i$ is even, and
  $ m_i equiv 13 mod 24 $ if $t_i$ is odd.
]
#proof[
  Reduce the continuation equation modulo $3$. Since $3^(t_i+2)m_i equiv 0 mod 3$, we get
  $ 2^(t_(i+1)+3)m_(i+1) equiv 1 mod 3. $
  As $2 equiv -1 mod 3$, this gives
  $ m_(i+1) equiv (-1)^(t_(i+1)+3) mod 3. $

  If the state $i$ itself is a growth-B continuation state, then it also satisfies $3^(t_i+2)m_i equiv 7 mod 8$. Since $3^(t_i+2) equiv 1 mod 8$ for even $t_i$ and $3 mod 8$ for odd $t_i$, this gives $m_i equiv 7 mod 8$ for even $t_i$ and $m_i equiv 5 mod 8$ for odd $t_i$. Combining these congruences with the modulo-$3$ condition by the Chinese Remainder Theorem gives $m_i equiv 23 mod 24$ for even $t_i$ and $m_i equiv 13 mod 24$ for odd $t_i$.
]

#proposition(name: "Binary-Depth Affine Normal Form")[
  Suppose a growth-B continuation branch has depths restricted to ${0,1}$. After discarding at most the initial state, write
  $ m_i = cases(24n_i + 23 & "if " t_i = 0, 24n_i + 13 & "if " t_i = 1.) $
  Then each continuing transition is one of the following affine maps:
  $ t_i=0, t_(i+1)=0: quad n_(i+1) = (9n_i+1)\/8, quad n_i equiv 7 mod 8, $
  $ t_i=0, t_(i+1)=1: quad n_(i+1) = 9n_i\/16, quad n_i equiv 0 mod 16, $
  $ t_i=1, t_(i+1)=0: quad n_(i+1) = (27n_i+7)\/8, quad n_i equiv 3 mod 8, $
  $ t_i=1, t_(i+1)=1: quad n_(i+1) = (27n_i+6)\/16, quad n_i equiv 14 mod 16. $
]
#proof[
  Substitute the modulo-$24$ normal form into
  $ 2^(t_(i+1)+3)m_(i+1) = 3^(t_i+2)m_i + 1. $
  For example, when $t_i=t_(i+1)=0$ this gives
  $ 8(24n_(i+1)+23) = 9(24n_i+23)+1, $
  hence $n_(i+1)=(9n_i+1)\/8$, and integrality is equivalent to $n_i equiv 7 mod 8$.

  The other three cases are the same calculation:
  $ 16(24n_(i+1)+13) = 9(24n_i+23)+1, $
  $ 8(24n_(i+1)+23) = 27(24n_i+13)+1, $
  and
  $ 16(24n_(i+1)+13) = 27(24n_i+13)+1. $
  Solving these equations gives the four displayed affine maps and their divisibility conditions.
]

#lemma(name: "Binary Zero-Return Expansion")[
  In the binary-depth normal form, suppose a branch starts at depth $0$ with parameter $n$ and next returns to depth $0$ after a finite block $0,1,1,dots,1,0$ or after the one-step block $0,0$. If the block is admissible, the resulting depth-$0$ parameter $n'$ satisfies $n' > n$.
]
#proof[
  For the one-step block $0,0$, the affine formula gives
  $ n' = (9n+1)\/8, $
  and the gate requires $n equiv 7 mod 8$. Hence $n' - n = (n+1)\/8 > 0$.

  For a block $0,1^r,0$ with $r >= 1$, compose the maps
  $0 arrow.r 1$, then $r-1$ copies of $1 arrow.r 1$, then $1 arrow.r 0$. The resulting affine multiplier is
  $ (9\/16)(27\/16)^(r-1)(27\/8)
     = (243\/128)(27\/16)^(r-1) > 1. $
  All additive constants in the composed map are nonnegative, and the final $1 arrow.r 0$ step contributes the positive constant $7\/8$. Therefore $n' > n$.
]

#remark[
  Thus a binary-depth infinite obstruction cannot be a bounded recurrence in this normal form. If it has infinitely many depth-$0$ states, those states form a strictly increasing sequence of ordinary integers. If it has only finitely many depth-$0$ states, then the depth sequence is eventually all $1$s, which is already excluded by the no-eventually-periodic-depth proposition. This still does not prove the binary-depth case; it converts it into an arithmetic problem about satisfying the gate congruences along an increasing sequence.
]
