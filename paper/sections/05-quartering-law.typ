#import "../lib/theorem.typ": *

= The Quartering Law

The fractional-moment contraction of Section 4 establishes that the _average_ hop shrinks trajectories. But averages permit exceptions: a trajectory could, in principle, string together arbitrarily many consecutive growth hops, accumulating enough expansion to escape any bounded region. This section proves a density theorem for the dominant strict growth mechanism, with a precise continuation factor of $1\/4$.

== Growth chains

I begin by isolating the dominant growth mechanism.

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

#theorem(name: "The Quartering Law")[
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

#lemma(name: "Binary Return-Block Gate")[
  In the binary-depth normal form, fix $r >= 0$. The return block
  $ 0 arrow.r 1^r arrow.r 0 $
  is admissible for exactly one residue class of the starting depth-$0$ parameter $n$ modulo $2^(4r+3)$.
]
#proof[
  Each binary transition has the form
  $ n_(i+1) = (a n_i + c) / 2^e $
  with $a$ odd and with $e=3$ for transitions ending at depth $0$, and $e=4$ for transitions ending at depth $1$. If a suffix of the block imposes
  $ n_(i+1) equiv R mod 2^q, $
  then the preimage condition is
  $ a n_i + c equiv 2^e R mod 2^(q+e). $
  Since $a$ is odd, it is invertible modulo $2^(q+e)$, so this is exactly one residue class modulo $2^(q+e)$.

  Pulling back from the final unrestricted depth-$0$ state through the whole block therefore gives one residue class. The total denominator exponent is $3$ for the block $0 arrow.r 0$, and for $r >= 1$ it is $4 + 4(r-1) + 3 = 4r + 3$. Thus in all cases the gate is a single residue class modulo $2^(4r+3)$.
]

#lemma(name: "Binary Return-Block Closed Gate")[
  The unique gate for the binary return block $0 arrow.r 1^r arrow.r 0$ is equivalently
  $ 33 n + 32 equiv epsilon_r 16^r mod 2^(4r+3), $
  where $epsilon_r = 7$ if $r$ is even and $epsilon_r = 5$ if $r$ is odd.
]
#proof[
  For $r=0$, the block is the single transition $0 arrow.r 0$, whose gate is
  $n equiv 7 mod 8$. Since $33 equiv 1 mod 8$ and $32 equiv 0 mod 8$, this is exactly the displayed congruence with $epsilon_0=7$.

  Now let $r >= 1$. Direct composition of the return block gives
  $ n' = (P_r n + D_r) / Q_r, $
  with $P_r = 9 dot 27^r$, $Q_r = 2^(4r+3)$, and
  $ 11 D_r = 2592 dot 27^(r-1) - 85 dot 16^r
            = 96 dot 27^r - 85 dot 16^r. $
  The gate is the condition $P_r n + D_r equiv 0 mod Q_r$. Multiplying by $11$ and rearranging gives
  $ 99 dot 27^r n + 96 dot 27^r equiv 85 dot 16^r mod Q_r, $
  or
  $ 3 dot 27^r (33n+32) equiv 85 dot 16^r mod Q_r. $
  The factor $3 dot 27^r$ is odd, hence invertible modulo $Q_r$. Because the right side is already divisible by $16^r$, only the inverse modulo $8$ matters after division. Modulo $8$ we have
  $85 equiv 5$ and $3 dot 27^r equiv 3^(r+1)$, so
  $ 85 (3 dot 27^r)^(-1) equiv
    cases(7 & "if" r "is even", 5 & "if" r "is odd") mod 8. $
  Therefore
  $33n+32 equiv epsilon_r 16^r mod 2^(4r+3)$,
  as claimed.
]

#proposition(name: "Binary Return-Block Coding")[
  For the binary-depth case, every return block $0 arrow.r 1^r arrow.r 0$ has the form
  $ n_(j+1) = (P_r n_j + D_r) / Q_r, $
  where
  $ P_r = 9 dot 27^r, quad Q_r = 2^(4r+3), $
  and
  $ D_0 = 1, quad D_r = (2592 dot 27^(r-1) - 85 dot 16^r) / 11 quad (r >= 1). $
  Therefore every infinite binary-depth continuation with infinitely many depth-$0$ states is encoded by an infinite $2$-adic return-block code. Such a continuation exists in positive integers only if that return-block code is a nonnegative ordinary integer.
]
#proof[
  The coefficient $P_r$ is the product of the odd coefficients in the block. For $r=0$ this is $9$, and for $r >= 1$ it is $9 dot 27^r$. The denominator exponent is the one computed in the return-block gate lemma, so $Q_r=2^(4r+3)$. The additive term $D_r$ is positive because the one-step block has additive term $1$, and every block with $r >= 1$ ends with the transition $1 arrow.r 0$, which contributes the positive constant $7$ before the final division.

  For the displayed formula for $D_r$, compose the block directly. For $r >= 1$, the first step gives $n_1=9n\/16$, the middle $r-1$ steps iterate
  $ g(n)=(27n+6)\/16, $
  and the final step is $(27n+7)\/8$. Since
  $ g^k(n) = (27\/16)^k n + (6\/11)((27\/16)^k - 1), $
  substituting $k=r-1$ and multiplying by $Q_r=2^(4r+3)$ gives
  $ D_r = (2592 dot 27^(r-1) - 85 dot 16^r) / 11. $

  For a finite sequence of return blocks $r_0, dots, r_(N-1)$, composing the affine maps gives
  $ Q_N n_N = P_N n_0 + D_N, $
  with $Q_N = product_j Q_(r_j)$ and $P_N$ odd. Thus an integer realization must satisfy one congruence class
  $ n_0 equiv -D_N P_N^(-1) mod Q_N. $
  These classes are nested as $N$ increases, so an infinite return-block sequence selects a unique element of $ZZ_2$. If a positive integer binary-depth continuation exists, its initial depth-$0$ parameter satisfies every prefix congruence and hence equals this $2$-adic code. Conversely, an ordinary nonnegative code satisfying all prefixes gives the corresponding integer return-block orbit.
]

#proposition(name: "Binary Return Critical Series")[
  Fix an infinite binary return-length word $(r_0,r_1,dots)$. For each return block, write
  $ alpha_j = P_(r_j) \/ Q_(r_j), quad beta_j = D_(r_j) \/ Q_(r_j). $
  Define the rational partial sums
  $ M_N = - sum_(i=0)^(N-1) beta_i / (alpha_0 alpha_1 dots alpha_i). $
  These sums converge in $RR$ to a value $M_R$ satisfying
  $ -1 <= M_R < 0. $
  The same rational sequence converges in $QQ_2$ to the $2$-adic return code selected by the infinite return word. More precisely, if
  $ Q_N n_N = P_N n_0 + D_N $
  is the integer affine composition of the first $N$ return blocks, and $R_N$ is the least prefix residue modulo $Q_N$, then
  $ M_N = -D_N / P_N, quad R_N equiv M_N mod Q_N. $
]
#proof[
  The block map has real affine form
  $ n_(j+1)=alpha_j n_j + beta_j $
  with $alpha_j>1$ and $beta_j>0$. Solving backward from $n_N=0$ gives
  $ n_0 = - sum_(i=0)^(N-1) beta_i/(alpha_0 alpha_1 dots alpha_i), $
  and the integer composition gives the same value $-D_N\/P_N$.

  The real series converges absolutely: since $D_r < P_r$ and every $alpha_j >= 9\/8$, the absolute value of the $i$-th summand is at most $(8\/9)^i$.

  It remains to locate these real critical values. For every return length $r$,
  $ 0 < D_r <= P_r - Q_r. $
  For $r=0$ this is equality: $D_0=1=P_0-Q_0$. For $r>=1$, using the formula for $D_r$ gives
  $ 11(P_r-Q_r-D_r)
     = 3 dot (27^r - 16^r) > 0. $
  Therefore the inverse branch
  $ x arrow.r (Q_r x - D_r)/P_r $
  maps the interval $[-1,0]$ into itself. Starting from $0$ and applying the inverse branches backward proves $-1 <= M_N < 0$ for every $N$, and hence $-1 <= M_R < 0$.

  Since all $P_r$ are odd, the $i$-th summand can be written as
  $ D_(r_i) Q_(r_0) dots Q_(r_(i-1)) / (P_(r_0) dots P_(r_i)). $
  Its $2$-adic valuation is therefore at least
  $ v_2(Q_(r_0) dots Q_(r_(i-1))), $
  which tends to infinity. Thus the rational series is Cauchy in $QQ_2$.

  Finally, the prefix congruence is
  $ P_N n_0 + D_N equiv 0 mod Q_N. $
  Since $P_N$ is odd, $P_N$ is invertible modulo $Q_N$, and
  $ R_N equiv -D_N P_N^(-1) equiv -D_N\/P_N = M_N mod Q_N. $
  Hence the $QQ_2$ limit of the $M_N$ is exactly the inverse-limit return code.
]

#remark[
  The all-zero return word has real and $2$-adic critical value $-1$. More generally, every eventually periodic return word has a rational critical value in $[-1,0)$, so it cannot be a nonnegative integer. The unresolved binary-depth case is again the nonperiodic possibility: a rational series with negative real limit whose $2$-adic limit is a positive ordinary integer.
]

#proposition(name: "Binary Return Ordinary-Landing Divisibility Criterion")[
  Fix an infinite return-length word $(r_0,r_1,dots)$ and a positive integer $M$. Let
  $ Q_N n_N = P_N n_0 + D_N $
  be the integer affine composition of the first $N$ return blocks, and put $S_N=r_0+dots+r_(N-1)$, so $Q_N=2^(3N+4S_N)$.
  Then $M$ is the positive ordinary return code for this word if and only if
  $ v_2(P_N M + D_N) >= 3N + 4S_N $
  for every $N >= 1$. In that case
  $ n_N = (P_N M + D_N) / Q_N $
  is the corresponding positive return orbit.
]
#proof[
  If $M$ is the ordinary return code, then each composed prefix map is integral at $M$, so $Q_N$ divides $P_N M+D_N$. Since $Q_N=2^(3N+4S_N)$, this is exactly the displayed valuation inequality.

  Conversely, suppose the divisibility holds for every $N$. Define
  $ n_N=(P_N M+D_N)\/Q_N. $
  These are positive integers because $M>0$, $P_N>0$, and $D_N>0$. For one more return block write $p_N=P_(r_N)$, $q_N=Q_(r_N)$, and $d_N=D_(r_N)$. The affine composition recurrences give
  $ P_(N+1)=p_N P_N, quad Q_(N+1)=q_N Q_N, quad D_(N+1)=p_N D_N+d_N Q_N. $
  Therefore
  $ P_(N+1) M+D_(N+1)
     = Q_N(p_N n_N+d_N). $
  The assumed divisibility by $Q_(N+1)=q_N Q_N$ implies
  $ q_N | p_N n_N+d_N, $
  so
  $ n_(N+1)=(p_N n_N+d_N)\/q_N $
  is exactly the next return-block step. Thus $M$ realizes every prefix and is the ordinary return code.
]

#proposition(name: "Binary Return Ordinary Itinerary Uniqueness")[
  For a fixed nonnegative depth-$0$ parameter $n_0$, there is at most one infinite binary return-length word for which $n_0$ is the ordinary return code.
]
#proof[
  The binary return partial map reads the next return length from the factorization
  $33n+32=16^r w.$
  If a return block exists, then $r=v_2(33n+32)\/4$ is uniquely determined, and the next return parameter is uniquely
  $ T(n)=(3 dot 27^r w-85)\/88. $
  Thus the first return length and the next state are forced by $n_0$. Iterating gives at most one infinite return-length word.
]

#proposition(name: "Binary Return Forced-Orbit Prefix Equivalence")[
  Fix a nonnegative depth-$0$ parameter $M$. The binary return partial map is defined for the first $L$ forced return blocks, with forced word $(r_0,dots,r_(L-1))$, if and only if $M$ satisfies every prefix congruence
  $ M equiv R_N mod Q_N quad (1 <= N <= L), $
  where $R_N$ is the least residue of the length-$N$ prefix $(r_0,dots,r_(N-1))$. In particular, once $Q_N > M$, this congruence is equivalent to $R_N=M$.
]
#proof[
  If the forced partial-map orbit exists for $L$ return blocks, then composing those blocks gives
  $ Q_N n_N = P_N M + D_N $
  for every $1 <= N <= L$. Hence
  $ P_N M + D_N equiv 0 mod Q_N, $
  which is exactly the prefix congruence $M equiv R_N mod Q_N$ because $P_N$ is odd and invertible modulo $Q_N$.

  Conversely, if all these prefix congruences hold, then the ordinary-landing divisibility criterion applied to the finite prefix constructs the corresponding positive integer states $n_1,dots,n_L$ and shows that each forced return block is defined. The return word is unique by the ordinary itinerary uniqueness proposition.

  Finally, if $Q_N>M$ and $M equiv R_N mod Q_N$ with $0 <= R_N < Q_N$, then the congruence holds as ordinary integers exactly when $R_N=M$.
]

#proposition(name: "Binary Return-Code Boundedness Criterion")[
  Fix an infinite return-length word $(r_0, r_1, dots)$, and let $R_N$ be the least nonnegative residue of its length-$N$ return-block prefix code modulo
  $ Q_N = product_(j=0)^(N-1) 2^(4r_j+3). $
  The corresponding binary return code is a nonnegative ordinary integer if and only if the sequence $R_N$ is bounded. Equivalently, this happens if and only if $R_N$ is eventually constant.
]
#proof[
  This is the return-block version of the general integer-code boundedness criterion. If the code equals a nonnegative integer $M$, then $R_N equiv M mod Q_N$ for every $N$. Since $Q_N arrow.r infinity$, once $Q_N > M$ the least nonnegative residue is exactly $R_N=M$.

  Conversely, if $R_N$ is bounded, say $R_N <= C$, then for $M > N$ with $Q_N > C$, the nesting relation $R_M equiv R_N mod Q_N$ forces $R_M=R_N$ as ordinary integers. Thus the residues are eventually constant. The eventual constant satisfies every prefix congruence, so it is exactly the ordinary integer represented by the return code.
]

#remark[
  This criterion gives the exact remaining $T=1$ target: prove that every non-eventually-periodic infinite return-length word has unbounded return-prefix residues. Strict increase of these residues is false for finite prefixes; the necessary statement is eventual unboundedness.
]

#proposition(name: "Binary Return Finite Height Search Criterion")[
  Fix a positive integer bound $B$ and a target return-prefix length $L$. To decide whether there is a length-$L$ return word whose least prefix residue $R_L$ is less than $B$, it is enough to search a finite tree. More precisely, suppose a current prefix has composition
  $ Q_i n_i = P_i n_0 + D_i $
  and least residue $R_i < B$. Any extension that can still end with some $R_L < B$ must have next return length $r_i$ satisfying
  $ 16^(r_i) Q_i < 33(P_i B + D_i) + 32Q_i. $
  Any extension whose new least residue is $>= B$ can be discarded.
]
#proof[
  If a length-$L$ extension has $R_L < B$, then the length-$L$ residue reduces to each shorter prefix residue modulo $Q_i$. Since the shorter representative satisfies $0 <= R_i < Q_i$, this congruence gives $R_L = R_i + m Q_i$ for some $m >= 0$. Hence every shorter prefix residue in the same word satisfies $R_i <= R_L < B$. This justifies discarding every branch once its least residue reaches $B$.

  Now fix a surviving prefix. For an ordinary start $n_0=R_L < B$ realizing the full extension, the state after the current prefix is
  $ n_i = (P_i n_0 + D_i) / Q_i
       < (P_i B + D_i) / Q_i. $
  If the next return length is $r_i$, then the return partial map requires
  $ 33n_i+32 = 16^(r_i)w_i $
  with $w_i$ a positive odd integer. Hence $16^(r_i) <= 33n_i+32$, and therefore
  $ 16^(r_i) Q_i < 33(P_i B + D_i) + 32Q_i. $
  For fixed $P_i,Q_i,D_i,B$, only finitely many nonnegative $r_i$ satisfy this inequality. Iterating gives a finite exhaustive search below height $B$.
]

#remark[
  This is the return-code analogue of the finite-height criterion for the reduced ${0,1}$ gap map. The script `explorations/explore54_return_minima.py` implements it and certifies least return-prefix residues through length $20$ with the extended verification option. It supplies exact finite certificates, but the missing binary theorem still requires a uniform lower bound as $L arrow.r infinity$.
]

#proposition(name: "Binary Return Global-Minimum Divergence Criterion")[
  Let
  $ mu_L = min { R_L(r_0,dots,r_(L-1)) : r_i >= 0 } $
  be the least return-prefix residue among all return words of length $L$. Then the binary return system has no nonnegative ordinary infinite return code if and only if
  $ mu_L arrow.r infinity. $
]
#proof[
  First, $mu_L$ exists. The all-zero return word gives a finite candidate bound $B_L$. By the finite-height search criterion, all length-$L$ words with residue below $B_L$ lie in a finite tree, so the minimum below or equal to this candidate is attained.

  Suppose an infinite return word has ordinary code $M >= 0$. Let $R_L$ be its prefix residues. Since $Q_L arrow.r infinity$, for all sufficiently large $L$ one has $Q_L > M$, and the congruence $R_L equiv M mod Q_L$ forces $R_L=M$. Hence $mu_L <= M$ for all sufficiently large $L$, so $mu_L$ cannot tend to infinity.

  Conversely, suppose $mu_L$ does not tend to infinity. The sequence $mu_L$ is nondecreasing: every length-$(L+1)$ prefix residue reduces to its length-$L$ prefix residue, so it is at least that shorter residue, and hence at least $mu_L$. Thus the $mu_L$ are bounded by some integer $B$.

  Consider the tree of finite return words whose least prefix residue is at most $B$. It has nodes at every depth by the definition of $mu_L$. It is finitely branching by the finite-height search criterion applied with bound $B+1$. Therefore, by the elementary infinite-tree lemma, it contains an infinite path. Along that path the prefix residues are nondecreasing and bounded by $B$, so they are eventually constant. By the return-code boundedness criterion, the path defines a nonnegative ordinary infinite return code.
]

#remark[
  This proposition turns the $T=1$ problem into a clean height theorem: prove a lower bound for the global minimum $mu_L$ that tends to infinity with $L$. The finite certificates in `explorations/explore54_return_minima.py` compute initial values of this exact sequence.
]

#proposition(name: "Bounded Return Alphabet Divergence Criterion")[
  Fix $R >= 0$ and define the restricted return minimum
  $ mu_L^(<=R) = min { R_L(r_0,dots,r_(L-1)) : 0 <= r_i <= R " for all " i }. $
  Then there is no nonnegative ordinary infinite return code whose return lengths all lie in ${0,dots,R}$ if and only if
  $ mu_L^(<=R) arrow.r infinity. $
]
#proof[
  Since the alphabet ${0,dots,R}$ is finite, the minimum exists at every finite level $L$.

  If an infinite return word over this alphabet has ordinary code $M >= 0$, then its length-$L$ prefix residue is congruent to $M$ modulo its prefix modulus $Q_L$. Since $Q_L arrow.r infinity$, the least representative is eventually exactly $M$. Hence $mu_L^(<=R) <= M$ for all sufficiently large $L$, so the restricted minima do not diverge.

  Conversely, suppose $mu_L^(<=R)$ does not diverge. These minima are nondecreasing, because every longer prefix residue reduces to its shorter prefix residue modulo the shorter modulus. Hence they are bounded by some $B$. The tree of finite words over ${0,dots,R}$ with least prefix residue at most $B$ has nodes at every depth and is finitely branching. By the elementary infinite-tree lemma, it contains an infinite path. Along that path the prefix residues are nondecreasing and bounded, hence eventually constant. The return-code boundedness criterion then gives a nonnegative ordinary infinite return code over the same bounded alphabet.
]

#proposition(name: "Binary Return Fixed-Height Duality")[
  For $B >= 0$, define the return survival depth below height $B$ by
  $ H_R(B) = sup { L >= 0 : exists r_0,dots,r_(L-1) >= 0 " with " R_L(r_0,dots,r_(L-1)) <= B }. $
  Then
  $ H_R(B) < L quad <=> quad mu_L > B. $
  Consequently, the binary return system has no nonnegative ordinary infinite return code if and only if $H_R(B)<infinity$ for every fixed $B$.
]
#proof[
  By definition of $mu_L$ as the least length-$L$ return-prefix residue, there exists a length-$L$ return word with residue at most $B$ if and only if $mu_L <= B$. Negating gives the displayed equivalence.

  The condition $H_R(B)<infinity$ for every fixed $B$ is therefore exactly the statement that for every $B$ there is some $L$ with $mu_L>B$, which is equivalent to $mu_L arrow.r infinity$ because $mu_L$ is nondecreasing. The global-minimum divergence criterion then gives the final claim.
]

#remark[
  The script `explorations/explore55_height_survival.py` computes these finite values $H_R(B)$ for sample bounds $B=2^m-1$. This is the fixed-height form of the same missing theorem, not a separate heuristic.
]

#proposition(name: "Binary Return Height Scale Lower Bound")[
  The global return minima and fixed-height survival depths satisfy
  $ mu_L <= 8^L - 1, quad H_R(8^L-1) >= L. $
  Consequently, any universal upper bound of the form
  $ H_R(B) <= c log_2(B+1) + O(1) $
  must have $c >= 1\/3$.
]
#proof[
  The all-zero return word of length $L$ is realized exactly by
  $ n_0 equiv -1 mod 8^L, $
  so its least nonnegative prefix residue is $8^L-1$. Hence the global minimum $mu_L$ is at most $8^L-1$, and the fixed-height survival depth at height $8^L-1$ is at least $L$.

  Substituting $B=8^L-1$ into any bound $H_R(B) <= c log_2(B+1)+O(1)$ gives
  $ L <= 3 c L + O(1), $
  so $c >= 1\/3$.
]

#proposition(name: "Binary Return Counting Criterion")[
  Let $N_R(B,L)$ be the number of length-$L$ return words whose least prefix residue is at most $B$.

  If there are constants $C>0$ and $0<rho<1$ such that
  $ N_R(B,L) <= C(B+1) rho^L $
  for every $B,L$, then
  $ H_R(B) <= ceil(log_(1\/rho)(C(B+1))). $
  In particular, this counting bound would rule out nonnegative ordinary infinite binary return codes.
]
#proof[
  If $L > log_(1\/rho)(C(B+1))$, then $C(B+1)rho^L < 1$. Since $N_R(B,L)$ is a nonnegative integer, this forces $N_R(B,L)=0$. Hence no length-$L$ return prefix has least residue at height at most $B$, proving the stated bound on $H_R(B)$.
]

#remark[
  The exact survival density $(2\/15)^L$ suggests the natural candidate $rho=2\/15$, up to discrepancy terms. Here $N_R$ counts least-residue prefix words, not all starts below $B$; it is the exact finite-height quantity computed by the prefix-residue searches. Proving a uniform counting estimate of this kind would be a direct route to the fixed-height theorem. The present paper does not prove such a discrepancy bound.
]

#proposition(name: "Binary Return Counting Rate Lower Bound")[
  Any prefix-counting bound of the form
  $ N_R(B,L) <= C(B+1) rho^L $
  holding for all $B,L$ with fixed $C>0$ must satisfy
  $ rho >= 1\/8. $
]
#proof[
  For each $L$, the all-zero return word has least prefix residue $8^L-1$. Thus
  $ N_R(8^L-1,L) >= 1. $
  The assumed counting bound gives
  $ 1 <= C 8^L rho^L = C(8rho)^L $
  for every $L$. If $rho<1\/8$, the right side tends to $0$, a contradiction. Hence $rho>=1\/8$.
]

#remark[
  The density value $2\/15$ is only slightly above this obstruction $1\/8$. This explains why a proof via counting must be nearly sharp in the worst finite-height regime.
]

#proposition(name: "Binary Return Start-Count Formula")[
  Let $A_R(B,L)$ be the number of ordinary starts $0 <= n <= B$ whose binary return partial-map orbit is defined for at least $L$ return blocks. For a return word $w=(r_0,dots,r_(L-1))$, let $R_w$ be its least prefix residue and $Q_w=product_i 2^(4r_i+3)$. Then
  $ A_R(B,L) = sum_(w: |w|=L, R_w<=B) (floor((B-R_w)\/Q_w)+1). $
  In particular,
  $ N_R(B,L) <= A_R(B,L) <= N_R(B,L) + (B+1)(2\/15)^L. $
]
#proof[
  The prefix-code proposition gives exactly one residue class $R_w mod Q_w$ for each return word $w$. The starts $0 <= n <= B$ in this class are precisely
  $ R_w, R_w+Q_w, R_w+2Q_w, dots, $
  up to $B$, giving $floor((B-R_w)\/Q_w)+1$ when $R_w<=B$ and none otherwise. Summing over words gives the formula. Distinct words give disjoint sets of starts because the return itinerary is unique.

  The lower bound follows because each nonempty residue class contributes at least one start. For the upper bound, use
  $ floor((B-R_w)\/Q_w)+1 <= 1 + (B+1)/Q_w $
  and sum over the words with $R_w<=B$. Extending the reciprocal-modulus sum to all length-$L$ return words gives
  $ sum_(|w|=L) 1/Q_w
     = (sum_(r>=0) 2^(-(4r+3)))^L
     = (2\/15)^L. $
]

#proposition(name: "Binary Return Start/Prefix Counting Equivalence")[
  Fix $2\/15 <= rho < 1$. A uniform prefix-counting bound
  $ N_R(B,L) <= C(B+1)rho^L $
  implies the ordinary-start bound
  $ A_R(B,L) <= (C+1)(B+1)rho^L. $
  Conversely, an ordinary-start bound
  $ A_R(B,L) <= C(B+1)rho^L $
  implies the same prefix-counting bound for $N_R$.
]
#proof[
  The start-count formula gives
  $ N_R(B,L) <= A_R(B,L) <= N_R(B,L) + (B+1)(2\/15)^L. $
  Since $rho >= 2\/15$, the extra term is at most $(B+1)rho^L$. This proves the first implication. The converse follows immediately from $N_R(B,L) <= A_R(B,L)$.
]

#proposition(name: "Binary Return Critical-Height Reduction")[
  Fix a level $L$, a height cutoff $B_max$, and a rate $rho>0$. Among all integer heights $0 <= B <= B_max$, the maximum of
  $ N_R(B,L) / ((B+1)rho^L) $
  is attained at a height $B$ equal to the least prefix residue of some length-$L$ return word, unless $N_R(B_max,L)=0$.
]
#proof[
  List the distinct realized least prefix residues at level $L$ not exceeding $B_max$ as
  $ h_1 < h_2 < dots < h_m. $
  If there are none, then $N_R(B,L)=0$ throughout the interval. Otherwise, on every interval
  $ h_j <= B < h_(j+1) $
  the numerator $N_R(B,L)$ is constant, while the denominator $B+1$ is strictly increasing. Hence the ratio is largest at the left endpoint $B=h_j$. The same argument applies on $h_m <= B <= B_max$.
]

#proposition(name: "Binary Return Critical-Rank Criterion")[
  For a length-$L$ return word $w$, let
  $ op("rank")_R(w) = N_R(R_w,L), $
  the number of length-$L$ return words whose least prefix residue is at most $R_w$.

  A uniform estimate
  $ N_R(B,L) <= C(B+1)rho^L $
  for all $B,L$ is equivalent to the critical-rank estimate
  $ op("rank")_R(w) <= C(R_w+1)rho^L $
  for every finite return word $w$.
]
#proof[
  The uniform estimate implies the rank estimate by taking $B=R_w$.

  Conversely, fix $B,L$. If $N_R(B,L)=0$, there is nothing to prove. Otherwise choose the largest realized least prefix residue $R_w <= B$ among length-$L$ return words. Then
  $ N_R(B,L)=N_R(R_w,L)=op("rank")_R(w). $
  By the critical-rank estimate,
  $ N_R(B,L) <= C(R_w+1)rho^L <= C(B+1)rho^L. $
]

#remark[
  Thus prefix counts and ordinary start counts differ by at most the expected density term. The finite-height obstruction is captured by $N_R(B,L)$ because every low prefix residue contributes at least one ordinary start.
]

#proposition(name: "Binary Return-Prefix Digit Recurrence")[
  For a finite return prefix, write
  $ Q_N n_N = P_N n_0 + D_N $
  and let $R_N$ be the least prefix residue. Define
  $ U_N = (P_N R_N + D_N) / Q_N. $
  For the next return length $r_N$, put
  $ p_N=P_(r_N), quad q_N=Q_(r_N), quad d_N=D_(r_N). $
  If
  $ R_(N+1) = R_N + e_N Q_N, quad 0 <= e_N < q_N, $
  then
  $ e_N equiv - (p_N U_N + d_N) (p_N P_N)^(-1) mod q_N. $
  In particular, $e_N=0$ if and only if
  $ p_N U_N + d_N equiv 0 mod q_N. $
]
#proof[
  The length-$(N+1)$ prefix class reduces to the length-$N$ prefix class modulo $Q_N$, hence the displayed representation of $R_(N+1)$ holds for a unique $e_N$ in the stated range.

  The extended prefix has
  $ P_(N+1)=p_N P_N, quad Q_(N+1)=q_N Q_N, quad D_(N+1)=p_N D_N + d_N Q_N. $
  Substituting $R_(N+1)=R_N+e_N Q_N$ into the integrality congruence
  $ P_(N+1) R_(N+1) + D_(N+1) equiv 0 mod Q_(N+1) $
  gives
  $ p_N(P_N R_N + D_N) + Q_N(p_N P_N e_N + d_N) equiv 0 mod q_N Q_N. $
  Dividing by $Q_N$ and using the definition of $U_N$ yields
  $ p_N U_N + p_N P_N e_N + d_N equiv 0 mod q_N. $
  Since $p_N P_N$ is odd, it is invertible modulo the power of two $q_N$, giving the digit formula. The zero-digit criterion follows by setting $e_N=0$.
]

#proposition(name: "Binary Return Zero-Increment Tail Equivalence")[
  Fix a finite return prefix and define $U_N$ as above. For any return-length suffix $(r_N,r_(N+1),dots)$, a run of zero prefix increments
  $ e_N=e_(N+1)=dots=e_(N+L-1)=0 $
  is equivalent to the existence of positive integers $U_(N+1),dots,U_(N+L)$ satisfying
  $ Q_(r_j) U_(j+1) = P_(r_j) U_j + D_(r_j)
     quad (N <= j < N+L). $
  Consequently, an eventually constant return-prefix residue tail is equivalent to an infinite positive orbit of the same binary return-block map, starting from the auxiliary state $U_N$.
]
#proof[
  By the digit recurrence, $e_j=0$ is equivalent to
  $ P_(r_j) U_j + D_(r_j) equiv 0 mod Q_(r_j). $
  When this divisibility holds, define
  $ U_(j+1) = (P_(r_j) U_j + D_(r_j)) / Q_(r_j). $
  Repeating this construction gives the displayed recurrence for a zero-increment run, and reversing the calculation shows that any such recurrence forces the corresponding digits to be zero.

  Since $U_N>0$ and each block has positive coefficients and positive additive term, all subsequent $U_j$ in such a run are positive. If zero increments continue forever, the auxiliary state therefore follows an infinite positive orbit of the binary return-block map. Conversely, such an infinite positive auxiliary orbit makes every later prefix digit zero, so the prefix residue remains constant.
]

#remark[
  The digit formulation is not a separate easier proof. It shows that an eventually constant return-code tail is exactly the original positive-integer return obstruction in another coordinate. Thus a proof must rule out infinite positive auxiliary return orbits, not merely show that many finite extensions increase the residue.
]

#proposition(name: "Binary Return Landing Growth Envelope")[
  Suppose an infinite return-length word $(r_0,r_1,dots)$ has positive ordinary return code $n_0=M$. Put
  $ S_N = r_0 + dots + r_(N-1). $
  Then the state $n_N$ after the first $N$ return blocks satisfies
  $ n_N = (P_N\/Q_N)(M - M_N), $
  where $M_N$ is the return critical-series partial sum. In particular,
  $ n_N <= (M+1)(9\/8)^N (27\/16)^(S_N). $
  If the next return length is $r_N$, then
  $ 5 dot 16^(r_N)
     <= 33(M+1)(9\/8)^N(27\/16)^(S_N) + 32. $
]
#proof[
  From the finite return composition,
  $ Q_N n_N = P_N M + D_N. $
  Since $M_N=-D_N\/P_N$, this becomes
  $ n_N = (P_N\/Q_N)(M-M_N). $
  The critical-series proposition gives $-1 <= M_N < 0$, hence $M-M_N <= M+1$. Also
  $ P_N\/Q_N = product_(j=0)^(N-1) (9 dot 27^(r_j)) / 2^(4r_j+3)
    = (9\/8)^N (27\/16)^(S_N). $
  This proves the bound for $n_N$.

  The return-length height bound applied to the next block gives
  $ 5 dot 16^(r_N) <= 33n_N + 32. $
  Substituting the preceding upper bound for $n_N$ gives the displayed envelope.
]

#remark[
  Thus any positive return-code landing has a quantitative shape: the next return length is controlled by the accumulated previous return lengths and by the fixed landing integer $M$. A return word with spikes violating this envelope cannot be a positive-integer obstruction.
]

#proposition(name: "Binary Return Spike Exclusion")[
  Let $(r_0,r_1,dots)$ be an infinite return-length word and put $S_N=r_0+dots+r_(N-1)$. If
  $ sup_N 16^(r_N) / ((9\/8)^N(27\/16)^(S_N)) = infinity, $
  then this word has no positive ordinary return code.
]
#proof[
  If the word had positive ordinary return code $M$, the landing growth envelope would give
  $ 5 dot 16^(r_N)
     <= 33(M+1)(9\/8)^N(27\/16)^(S_N) + 32. $
  Since $(9\/8)^N(27\/16)^(S_N) >= 1$, division gives
  $ 16^(r_N) / ((9\/8)^N(27\/16)^(S_N))
     <= (33(M+1)+32)/5 $
  for every $N$, contradicting the assumed unboundedness.
]

#proposition(name: "Binary Return Reparameterization")[
  Suppose a binary-depth continuation is at a depth-$0$ state with parameter $n_j$, and suppose the next return block is $0 arrow.r 1^(r_j) arrow.r 0$. Let $epsilon_j = 7$ if $r_j$ is even and $epsilon_j = 5$ if $r_j$ is odd. Then there is a positive odd integer $w_j equiv epsilon_j mod 8$ such that
  $ 33 n_j + 32 = 16^(r_j) w_j. $
  It also satisfies
  $ 16^(r_j) w_j equiv 32 mod 33, $
  so for each fixed $r_j$ the variable $w_j$ lies in one residue class modulo $264$.
  The next depth-$0$ return value is
  $ n_(j+1) = (3 dot 27^(r_j) w_j - 85) / 88. $
  If the following return block has length $r_(j+1)$ and corresponding value $w_(j+1)$, then
  $ 9 dot 27^(r_j) w_j + 1 = 2^(4r_(j+1)+3) w_(j+1). $
]
#proof[
  The closed gate lemma gives
  $33n_j+32 equiv epsilon_j 16^(r_j) mod 2^(4r_j+3)$.
  Hence
  $33n_j+32 = 16^(r_j)(epsilon_j + 8u_j)$
  for some integer $u_j$. Put $w_j=epsilon_j+8u_j$. Since $n_j >= 0$ and $r_j >= 0$, this $w_j$ is positive and odd, and $w_j equiv epsilon_j mod 8$.
  The same defining equation gives
  $16^(r_j)w_j = 33n_j+32 equiv 32 mod 33$.
  Since $8$ and $33$ are coprime, the two congruences determine one residue class modulo $264$.

  Substituting $n_j=(16^(r_j)w_j-32)\/33$ into the return-block map gives
  $ n_(j+1)
    = (9 dot 27^(r_j)n_j + D_(r_j)) / 2^(4r_j+3)
    = (3 dot 27^(r_j)w_j - 85) / 88, $
  using the displayed formula for $D_r$ from the return-block coding proposition. Finally,
  $ 33n_(j+1)+32
    = (9 dot 27^(r_j)w_j + 1) / 8. $
  Applying the definition of $w_(j+1)$ to the next return block gives the final recurrence.
]

#proposition(name: "Binary Return Partial Map")[
  A finite binary return block starting at a depth-$0$ parameter $n$ exists exactly when
  $ 33n+32 = 16^r w $
  for some $r >= 0$ and odd $w$ satisfying $w equiv 7 mod 8$ if $r$ is even and $w equiv 5 mod 8$ if $r$ is odd. In that case the block is $0 arrow.r 1^r arrow.r 0$, and the next depth-$0$ return parameter is
  $ T(n) = (3 dot 27^r w - 85) / 88. $
  Therefore any positive-integer binary-depth obstruction with infinitely many depth-$0$ states is exactly an infinite positive orbit of this partial map.
]
#proof[
  The closed gate lemma says that a block $0 arrow.r 1^r arrow.r 0$ is admissible exactly when
  $33n+32 equiv epsilon_r 16^r mod 2^(4r+3)$,
  where $epsilon_r$ is $7$ or $5$ according to the parity of $r$. This congruence is equivalent to
  $33n+32 = 16^r(epsilon_r + 8u)$
  for some integer $u$, i.e. to the displayed factorization with $w=epsilon_r+8u$. Conversely, such a factorization gives precisely the closed gate congruence for that return block. The formula for $T(n)$ is the return reparameterization formula. Finally, a binary-depth obstruction with infinitely many depth-$0$ states decomposes uniquely into consecutive return blocks, so it is an infinite orbit of $T$; and any infinite orbit of $T$ reconstructs those return blocks.
]

#proposition(name: "Binary Return Backward Branch Formula")[
  Fix a terminal depth-$0$ return state $n'$ and a return length $r >= 0$. Let
  $ P_r = 9 dot 27^r, quad Q_r = 2^(4r+3), $
  and let $D_r$ be the additive term of the length-$r$ return block. A state $n$ maps to $n'$ through a return block of length $r$ if and only if
  $ n = (Q_r n' - D_r) / P_r $
  is a nonnegative integer. In particular, for fixed $n'$ and $r$ there is at most one backward preimage.
]
#proof[
  The return-block coding proposition gives the forward affine relation
  $ Q_r n' = P_r n + D_r. $
  Solving for $n$ gives the displayed formula, so any forward preimage must have this value.

  Conversely, if the displayed value is a nonnegative integer, then
  $ P_r n + D_r = Q_r n'. $
  Hence $P_r n+D_r$ is divisible by $Q_r$, which is exactly the return-block gate congruence for length $r$. Applying the return block therefore gives terminal state $n'$.
]

#proposition(name: "Binary Return Backward 3-adic Gate")[
  For fixed terminal state $n'$ and return length $r$, the backward branch formula is integral if and only if
  $ 88 n' + 85 = 3^(3r+1) u $
  for an integer $u equiv 2 mod 3$. Consequently, a terminal state has at most one backward return preimage, across all return lengths.
]
#proof[
  The formula
  $ n = (Q_r n' - D_r) / P_r $
  is integral if and only if $Q_r n' equiv D_r mod P_r$, where $P_r=9 dot 27^r=3^(3r+2)$ and $Q_r=8 dot 16^r$. Using
  $ D_r = (96 dot 27^r - 85 dot 16^r) / 11 $
  and multiplying by $11$ gives the equivalent congruence
  $ 16^r(88n' + 85) equiv 96 dot 27^r mod 3^(3r+2). $
  Dividing by $3^(3r+1)$, this holds exactly when
  $88n'+85=3^(3r+1)u$ with
  $16^r u equiv 32 mod 3$.
  Since $16 equiv 1 mod 3$ and $32 equiv 2 mod 3$, this is $u equiv 2 mod 3$.

  If two different return lengths $r<s$ both gave integral backward branches, then $v_3(88n'+85)$ would be both $3r+1$ and $3s+1$, impossible. Thus there is at most one backward return preimage.
]

#proposition(name: "Binary Return Prefix Terminal Injectivity")[
  At a fixed length $L$, two realized binary return prefixes that land at the same terminal depth-$0$ state have the same return word and the same initial residue. Thus the binary return prefix map has no finite forward merging.
]
#proof[
  Suppose two length-$L$ realized return prefixes land at the same terminal state. By the backward $3$-adic gate proposition, this terminal state has at most one immediate predecessor across all return lengths. Therefore the last return length and the preceding state are the same for both prefixes. Repeating the argument backward through the remaining $L-1$ levels shows that every return length agrees and that the initial state is the same. Hence the return words and initial residues agree.
]

#proposition(name: "Binary Return Backward Length Bound")[
  If a terminal state $n'$ has a backward preimage through a return block of length $r$, then
  $ (27\/16)^r <= (88n' + 85) / 96. $
  Hence the possible backward return lengths into a fixed terminal state are logarithmically bounded in $n'$.
]
#proof[
  By the backward branch formula, a nonnegative preimage requires
  $ Q_r n' - D_r >= 0, $
  or $n' >= D_r\/Q_r$. The return-block additive term satisfies
  $ D_r = (96 dot 27^r - 85 dot 16^r) / 11, $
  and $Q_r=8 dot 16^r$. Therefore
  $ D_r\/Q_r = (96(27\/16)^r - 85) / 88. $
  Rearranging $n' >= D_r\/Q_r$ gives the displayed bound.
]

#proposition(name: "Binary Return Backward Contraction")[
  If $n$ maps to $n'$ through a return block of length $r$, then
  $ n < (8\/9)(16\/27)^r n'. $
  In particular, every valid positive backward return branch strictly decreases height.
]
#proof[
  The backward branch formula gives
  $ n = (Q_r n' - D_r) / P_r, $
  with $P_r=9 dot 27^r$ and $Q_r=8 dot 16^r$. Since $D_r>0$,
  $ n < (Q_r\/P_r)n'
      = (8\/9)(16\/27)^r n'. $
  The factor on the right is at most $8\/9$, so every positive backward branch strictly decreases height.
]

#proposition(name: "Binary Return Backward Path Contraction")[
  If a depth-$L$ backward return path has return word $(r_0,dots,r_(L-1))$ and total return length
  $ S_L = r_0 + dots + r_(L-1), $
  then its initial state $n_0$ and terminal state $n_L$ satisfy
  $ n_0 < (8\/9)^L (16\/27)^(S_L) n_L. $
]
#proof[
  Apply the backward contraction proposition to each branch and multiply the resulting inequalities.
]

#proposition(name: "Binary Return Terminal Escape")[
  If a positive state $n_0$ survives $L$ return blocks with return word $(r_0,dots,r_(L-1))$, total return length $S_L$, and terminal state $n_L$, then
  $ n_L > (9\/8)^L (27\/16)^(S_L) n_0. $
]
#proof[
  This is the backward path contraction inequality rearranged.
]

#proposition(name: "Binary Return Terminal Window")[
  For a finite return word $w$ of length $L$, let
  $ E_w = P_w\/Q_w = (9\/8)^L (27\/16)^(S_w), $
  let $M_w=-D_w\/P_w$ be its critical-series partial sum, let $R_w$ be its least prefix residue, and let
  $ U_w = (P_w R_w + D_w)\/Q_w $
  be the terminal state reached from $R_w$. Then
  $ U_w = E_w (R_w - M_w), quad R_w <= U_w\/E_w < R_w + 1. $
  In particular,
  $ R_w = floor(U_w\/E_w). $
  Consequently,
  $ R_w <= B quad ==> quad U_w < E_w(B+1). $
]
#proof[
  The finite return composition gives
  $ Q_w U_w = P_w R_w + D_w. $
  Since $M_w=-D_w\/P_w$, this is
  $ U_w = (P_w\/Q_w)(R_w-M_w)=E_w(R_w-M_w). $
  The return critical-series proposition gives $-1 <= M_w < 0$, hence
  $ R_w <= R_w-M_w < R_w+1. $
  Since $R_w$ is an integer, this also gives $R_w=floor(U_w\/E_w)$.
  The terminal-window implication follows immediately.
]

#proposition(name: "Binary Return Terminal Depth Bound")[
  If a nonempty return word $w$ has length $L$ and terminal state $U_w$, then
  $ U_w >= E_w >= (9\/8)^L. $
  Consequently,
  $ L <= log_(9\/8)(U_w). $
]
#proof[
  The least return-prefix residue $R_w$ is positive for every nonempty return word. If $R_w=0$, then the ordinary state $0$ would realize the first return block of $w$, but the return partial map is not defined at $0$ since $33 dot 0 + 32 = 32$ has $2$-adic valuation $5$, not a multiple of $4$.

  The terminal-window proposition gives $U_w/E_w >= R_w >= 1$, hence $U_w >= E_w$. Since each return block has expansion at least $9\/8$, $E_w >= (9\/8)^L$. Taking logarithms gives the depth bound.
]

#proposition(name: "Binary Return Terminal-Window Counting Equivalence")[
  With the notation of the previous proposition,
  $ R_w <= B $
  if and only if
  $ U_w / E_w < B+1. $
  Consequently, $N_R(B,L)$ is exactly the number of length-$L$ return words satisfying $U_w/E_w < B+1$.
]
#proof[
  If $R_w <= B$, the terminal-window proposition gives $U_w/E_w < R_w+1 <= B+1$. Conversely, if $U_w/E_w < B+1$, then the same proposition gives $R_w <= U_w/E_w < B+1$. Since $R_w$ and $B$ are integers, this implies $R_w <= B$.
]

#proposition(name: "Binary Return Expansion Pressure")[
  For every $theta > 0$ and every length $L$,
  $ sum_(w: |w|=L) E_w^(-theta)
     = (((8\/9)^theta) / (1 - (16\/27)^theta))^L, $
  where $E_w=(9\/8)^L(27\/16)^(sum_j r_j)$ is the return expansion factor of $w=(r_0,dots,r_(L-1))$.

  This pressure decays exponentially in $L$ exactly when
  $ (8\/9)^theta + (16\/27)^theta < 1. $
  The threshold root is $theta_R approx 2.56743$; in particular, cubic pressure decays.
]
#proof[
  A one-block return label $r$ has expansion
  $ E_r = (9\/8)(27\/16)^r. $
  Hence
  $ sum_(r=0)^infinity E_r^(-theta)
    = (8\/9)^theta sum_(r=0)^infinity (16\/27)^(theta r)
    = ((8\/9)^theta) / (1 - (16\/27)^theta). $
  Since the expansion factor of a word is the product of its one-block expansion factors, the length-$L$ sum factorizes as the $L$-th power of the one-step sum.

  The base is less than $1$ exactly when
  $ (8\/9)^theta < 1 - (16\/27)^theta, $
  which is the displayed condition. For $theta=3$,
  $ (8\/9)^3 + (16\/27)^3 = 17920\/19683 < 1. $
]

#proposition(name: "Binary Return Normalized Stopping-Time Criterion")[
  Let $W_R(B,L)$ be the number of length-$L$ return words whose normalized terminal state satisfies
  $ U_w/E_w < B+1. $
  If there are constants $C>0$ and $0<rho<1$ such that
  $ W_R(B,L) <= C(B+1)rho^L $
  for every $B,L$, then
  $ H_R(B) <= ceil(log_(1\/rho)(C(B+1))). $
  In particular, this normalized terminal-window estimate would rule out nonnegative ordinary infinite binary return codes.
]
#proof[
  By the terminal-window counting equivalence, $W_R(B,L)=N_R(B,L)$. The claim is exactly the binary return counting criterion.
]

#proposition(name: "Binary Return Terminal-Rank Criterion")[
  For a length-$L$ return word $w$, let $op("trank")_R(w)$ be the number of length-$L$ return words $v$ satisfying
  $ floor(U_v\/E_v) <= floor(U_w\/E_w). $
  A uniform estimate
  $ W_R(B,L) <= C(B+1)rho^L $
  for all $B,L$ is equivalent to the terminal-rank estimate
  $ op("trank")_R(w) <= C(floor(U_w\/E_w)+1)rho^L $
  for every finite return word $w$.
]
#proof[
  The return terminal-window proposition gives $floor(U_w\/E_w)=R_w$ for every word $w$, and the terminal-window counting equivalence gives $W_R(B,L)=N_R(B,L)$. Thus $op("trank")_R(w)=N_R(R_w,L)$, which is the critical rank of $w$. The claim is exactly the binary return critical-rank criterion written in terminal coordinates.
]

#proposition(name: "Binary Return Weighted Terminal-Window Bound")[
  For every $theta > 1$, every $B >= 0$, and every $L >= 1$,
  $ sum_(w: |w|=L, R_w <= B) E_w^(-theta)
     <= (B+1)^theta zeta(theta), $
  where $zeta(theta)=sum_(u=1)^infinity u^(-theta)$.
]
#proof[
  If $R_w <= B$, the terminal-window proposition gives
  $ U_w < E_w(B+1). $
  Rearranging gives
  $ E_w^(-theta) <= (B+1)^theta U_w^(-theta). $
  By binary return prefix terminal injectivity, the terminal states $U_w$ are distinct positive integers among length-$L$ return words. Therefore
  $ sum_(w: |w|=L, R_w <= B) U_w^(-theta)
     <= sum_(u=1)^infinity u^(-theta)
     = zeta(theta), $
  and the displayed inequality follows.
]
#remark[
  This is a weighted terminal-window estimate, not the desired rank estimate. It controls inverse expansion mass inside the low window, but many very large-expansion words can have tiny weights. The missing counting theorem must upgrade this kind of weighted control into a bound for the number of low-window words.
]

#proposition(name: "Binary Return Low-Expansion Window Count")[
  Let $N_R(B,L;X)$ count length-$L$ return words satisfying $R_w <= B$ and $E_w <= X$. For every expansion cutoff $X >= 1$, every $B >= 0$, and every $L >= 1$,
  $ N_R(B,L;X) <= ceil(X(B+1)) - 1. $
]
#proof[
  If $R_w <= B$ and $E_w <= X$, the terminal-window proposition gives
  $ U_w < E_w(B+1) <= X(B+1). $
  By binary return prefix terminal injectivity, distinct length-$L$ return words have distinct positive terminal states $U_w$. The number of positive integers strictly below $X(B+1)$ is $ceil(X(B+1))-1$, giving the bound.
]
#remark[
  The low-expansion part of the return low window is therefore linearly bounded in the expansion cutoff. The remaining source of difficulty is the high-expansion part of the same low normalized window.
]

#proposition(name: "Binary Return Weighted Expansion-Shell Count")[
  Let $W_R(B,L;s)$ count length-$L$ return words satisfying $R_w <= B$ and
  $ 2^s <= E_w < 2^(s+1). $
  For every $theta > 1$,
  $ W_R(B,L;s) <= 2^(theta(s+1)) (B+1)^theta zeta(theta). $
]
#proof[
  On the shell $E_w < 2^(s+1)$, each word satisfies
  $ E_w^(-theta) > 2^(-theta(s+1)). $
  Therefore
  $ W_R(B,L;s) dot 2^(-theta(s+1))
     <= sum_(w: |w|=L, R_w <= B) E_w^(-theta). $
  Apply the weighted terminal-window bound and multiply by $2^(theta(s+1))$.
]
#remark[
  This turns weighted control into an ordinary count on each fixed expansion shell. The bound deteriorates as the shell index grows, which is exactly why a proof still needs arithmetic separation for high-expansion low-window words.
]

#proposition(name: "Binary Return Expansion-Shell Depth Bound")[
  If a length-$L$ return word satisfies
  $ 2^s <= E_w < 2^(s+1), $
  then
  $ L < log_(9\/8)(2^(s+1)). $
]
#proof[
  Every return block has expansion at least $9\/8$, so $E_w >= (9\/8)^L$. Combining this with $E_w < 2^(s+1)$ gives
  $ (9\/8)^L < 2^(s+1), $
  and taking logarithms gives the displayed bound.
]
#remark[
  Thus fixed return expansion shells only affect bounded prefix depths. Any infinite-depth obstruction must eventually move to arbitrarily high expansion shells.
]

#proposition(name: "Binary Return Terminal Start-Count Formula")[
  Let $A_R(B,L)$ be the number of ordinary starts $0 <= n <= B$ whose binary return partial-map orbit is defined for at least $L$ return blocks. Then
  $ A_R(B,L)
     = sum_(w: |w|=L, floor(U_w\/E_w)<=B)
        (floor((B - floor(U_w\/E_w))\/Q_w)+1). $
]
#proof[
  The return terminal-window proposition gives $floor(U_w\/E_w)=R_w$. Substituting this identity into the binary return start-count formula gives the displayed formula.
]

#proposition(name: "Binary Return Terminal Boundedness Criterion")[
  Fix an infinite return-length word, and let $w_N$ be its length-$N$ prefix. Let $E_N$ and $U_N$ be the expansion factor and terminal state associated to $w_N$ and its least prefix residue. Then the selected $2$-adic return code is a nonnegative ordinary integer if and only if
  $ floor(U_N\/E_N) $
  is bounded as $N arrow.r infinity$. Equivalently, this happens if and only if the sequence $floor(U_N\/E_N)$ is eventually constant.
]
#proof[
  The return terminal-window proposition gives
  $ floor(U_N\/E_N)=R_N, $
  where $R_N$ is the least return-prefix residue. The claim is therefore exactly the binary return-code boundedness criterion.
]

#proposition(name: "Binary Return Terminal Monotonicity")[
  Fix an infinite return-length word, and let $w_N$ be its length-$N$ prefix. Put
  $ T_N = floor(U_N\/E_N), $
  where $E_N$ and $U_N$ are the expansion factor and terminal state associated to $w_N$ and its least prefix residue. If the next return block has modulus $q_N=2^(4r_N+3)$ and the prefix modulus before it is $Q_N$, then
  $ T_(N+1) = T_N + e_N Q_N $
  for some integer $e_N$ with $0 <= e_N < q_N$. In particular, $T_N$ is nondecreasing, and it is eventually constant if and only if $e_N=0$ for all sufficiently large $N$.
]
#proof[
  By the return terminal-window proposition, $T_N=R_N$, the least prefix residue. The return-prefix digit recurrence writes
  $ R_(N+1)=R_N+e_N Q_N, quad 0 <= e_N < q_N. $
  Substituting $T_N=R_N$ gives the displayed formula. Since $Q_N>0$, the sequence is nondecreasing. A nondecreasing integer sequence is eventually constant exactly when all sufficiently late increments vanish, which here is exactly $e_N=0$ eventually.
]

#proposition(name: "Binary Return Terminal Zero-Step Criterion")[
  Fix a finite return prefix with auxiliary terminal state $U_N$. For a proposed next return length $r$, write its one-block data as $p=P_r$, $q=Q_r$, and $d=D_r$. The next rounded terminal increment is zero if and only if
  $ p U_N + d equiv 0 mod q. $
  In that case
  $ U_(N+1) = (p U_N+d)\/q, $
  so the auxiliary terminal state itself takes the same return-block step of length $r$. Consequently, at most one next return length can give a zero terminal increment.
]
#proof[
  The first equivalence is exactly the zero-digit criterion in the return-prefix digit recurrence, written with $U_N$ as the auxiliary state. When the congruence holds, the displayed formula is the return-block map with input $U_N$ and return length $r$. The uniqueness of a zero-increment next length follows from ordinary return itinerary uniqueness for the fixed auxiliary state $U_N$.
]

#proposition(name: "Binary Return Terminal Zero-Increment Congruence")[
  Fix a finite return prefix with auxiliary terminal state $U_N$. For a finite return-length suffix $v=(r_N,dots,r_(N+L-1))$, let $R_v$ and $Q_v$ be the least prefix residue and modulus of the suffix as a standalone return word. Then the rounded return terminal coordinate has zero increments through the whole suffix $v$ if and only if
  $ U_N equiv R_v mod Q_v. $
]
#proof[
  By the terminal zero-step criterion, zero increments through the suffix are equivalent to saying that the auxiliary state $U_N$ realizes the ordinary return itinerary $v$ for $L$ blocks. The binary return forced-orbit prefix equivalence says this happens if and only if $U_N$ satisfies the suffix prefix congruence $U_N equiv R_v mod Q_v$.
]

#proposition(name: "Binary Return Terminal Self-Shadowing Criterion")[
  Fix a finite return prefix with auxiliary terminal state $U_N$ and an infinite return-length suffix $v=(r_N,r_(N+1),dots)$. For $L>=1$, let $R_(v,L)$ and $Q_(v,L)$ be the least prefix residue and modulus of the first $L$ blocks of $v$, considered as a standalone return word. Then the rounded return terminal coordinate has zero increments along the whole suffix $v$ if and only if
  $ U_N equiv R_(v,L) mod Q_(v,L) quad "for every " L>=1. $
  Equivalently, $U_N$ is the positive ordinary return code selected by the suffix $v$.
]
#proof[
  By the terminal zero-increment congruence proposition, zero increments through the first $L$ blocks of $v$ are equivalent to the congruence
  $ U_N equiv R_(v,L) mod Q_(v,L). $
  Requiring zero increments along the whole suffix is therefore equivalent to requiring these congruences for every $L$.

  The binary return forced-orbit prefix equivalence says exactly that a fixed positive state realizes the first $L$ forced return blocks of $v$ if and only if it satisfies all prefix congruences through length $L$. Hence satisfying the displayed congruences for every $L$ is equivalent to $U_N$ being the positive ordinary return code for the suffix.
]

#proposition(name: "Binary Return Shift-Code Recurrence")[
  Suppose an infinite return-length word $v=(r_0,r_1,dots)$ has positive ordinary return code $X_0$. Let $X_j$ be the state after the first $j$ return blocks. Then for every $j>=0$, $X_j$ is the positive ordinary return code of the shifted suffix $(r_j,r_(j+1),dots)$, and
  $ Q_(r_j) X_(j+1) = P_(r_j) X_j + D_(r_j). $
  In particular, for every $L>=1$,
  $ X_L > (9\/8)^L (27\/16)^(r_0+dots+r_(L-1)) X_0. $
]
#proof[
  Since $X_0$ realizes the full return word, the states $X_j$ are positive integers and satisfy the displayed one-block recurrence. Starting from $X_j$, the remaining orbit follows exactly the shifted suffix $(r_j,r_(j+1),dots)$. By ordinary itinerary uniqueness, $X_j$ is the positive ordinary return code selected by that shifted suffix.

  The final inequality is the binary return terminal escape proposition applied to the positive orbit segment $X_0,dots,X_L$.
]

#proposition(name: "Binary Return Terminal Zero-Increment Cylinder Density")[
  Fix a finite return-length suffix $v=(r_0,dots,r_(L-1))$ with modulus
  $ Q_v = product_(i=0)^(L-1) 2^(4r_i+3). $
  Among nonnegative auxiliary states $U$, the set for which the rounded return terminal coordinate has zero increments through $v$ is one residue class modulo $Q_v$, and therefore has natural density $1\/Q_v$.

  Consequently, for a fixed infinite return-length suffix, the set of $2$-adic auxiliary states that shadow the whole suffix is a single $2$-adic point and has Haar measure zero.
]
#proof[
  The terminal zero-increment congruence proposition identifies the finite zero-increment set with
  $ U equiv R_v mod Q_v, $
  one residue class modulo $Q_v$. Its natural density among nonnegative integers is therefore $1\/Q_v$.

  For an infinite suffix, these congruence classes are nested and the moduli $Q_(v,L)$ tend to infinity. Their intersection in $ZZ_2$ is a single inverse-limit point, namely the $2$-adic return code of the suffix. A singleton in $ZZ_2$ has Haar measure zero.
]

#proposition(name: "Binary Return Terminal Zero-Increment Survival Density")[
  Among nonnegative auxiliary states $U$, the natural density of states admitting at least $L$ consecutive rounded return terminal zero-increments is
  $ (2\/15)^L. $
]
#proof[
  For a fixed length-$L$ return suffix $v=(r_0,dots,r_(L-1))$, the terminal zero-increment cylinder-density proposition gives density
  $ 1\/Q_v = product_(i=0)^(L-1) 2^(-(4r_i+3)). $
  Distinct suffix words give disjoint sets of auxiliary states, because the ordinary return itinerary from a fixed auxiliary state is unique. Therefore the total density is
  $ (sum_(r>=0) 2^(-(4r+3)))^L = (2\/15)^L. $
]

#proposition(name: "Bounded Binary Return Terminal Zero-Increment Survival Density")[
  Among nonnegative auxiliary states $U$, the natural density of states whose next $L$ rounded return terminal increments are zero and whose corresponding return lengths all satisfy $0 <= r <= R$ is
  $ ((2\/15)(1 - 16^(-(R+1))))^L. $
]
#proof[
  Repeat the proof of the terminal zero-increment survival density, but sum only over suffix words with $0 <= r_i <= R$. The one-step density sum is
  $ sum_(r=0)^R 2^(-(4r+3))
    = (2\/15)(1 - 16^(-(R+1))). $
  Since distinct finite suffix words are disjoint itinerary cylinders, the $L$-step density is the $L$-th power of this restricted one-step sum.
]

#proposition(name: "Finite Binary Return Terminal Zero-Increment Words Are Locally Realizable")[
  For every finite sequence of return lengths $(r_0,dots,r_(L-1))$, there are infinitely many positive auxiliary states $U_0$ for which the rounded return terminal coordinate has zero increments through exactly this finite sequence.
]
#proof[
  By finite binary return-word realizability, there are infinitely many positive states $U_0$ whose ordinary binary return itinerary begins with the prescribed word. Along such an ordinary orbit, the terminal zero-step criterion gives zero rounded-terminal increment at each of the prescribed return lengths. Thus every finite return-length word is locally realizable as a zero-increment terminal word.
]

#proposition(name: "Binary Return Terminal Zero-Increment Equivalence")[
  Fix a finite return prefix and put $T_N=floor(U_N\/E_N)$. For any return-length suffix, an eventually constant tail of the rounded terminal coordinates
  $ T_N,T_(N+1),T_(N+2),dots $
  is equivalent to an infinite positive orbit of the binary return-block map starting from the auxiliary state $U_N$.
]
#proof[
  By the terminal monotonicity proposition, the rounded terminal coordinate is eventually constant exactly when the corresponding return-prefix increments are eventually zero. The return zero-increment tail equivalence says precisely that such a zero-increment tail is equivalent to an infinite positive orbit of the same binary return-block map starting from $U_N$.
]

#proposition(name: "Binary Return Terminal Zero-Increment Tail Uniqueness")[
  Fix a finite return prefix and its auxiliary terminal state $U_N$. There is at most one infinite return-length suffix for which all later rounded terminal increments are zero.
]
#proof[
  By the terminal zero-increment equivalence, such a suffix is exactly an infinite positive orbit of the binary return-block map starting from $U_N$. The binary return ordinary itinerary uniqueness proposition says that a fixed positive state has at most one infinite return-length itinerary. Hence there is at most one zero-increment suffix.
]

#proposition(name: "Binary Return Terminal Zero-Increment Escape")[
  Fix a finite return prefix and suppose the next $L$ return-prefix increments are zero. If the zero-increment suffix has return lengths $(r_N,dots,r_(N+L-1))$ and total
  $ S = r_N + dots + r_(N+L-1), $
  then the auxiliary terminal states satisfy
  $ U_(N+L) > (9\/8)^L (27\/16)^S U_N. $
]
#proof[
  By the terminal zero-increment equivalence, the auxiliary states $U_N,U_(N+1),dots,U_(N+L)$ form an actual positive orbit of the return partial map along the suffix word. Applying the binary return terminal escape proposition to this finite orbit gives the displayed inequality.
]

#proposition(name: "No Eventually Periodic Binary Return Terminal Tail")[
  No eventually periodic return-length suffix can make the rounded return terminal coordinate eventually constant.
]
#proof[
  If such a suffix made the rounded terminal coordinate eventually constant, the terminal zero-increment equivalence would produce an infinite positive orbit of the binary return-block map whose return itinerary is eventually periodic. This contradicts the no eventually periodic binary return itinerary proposition.
]

#proposition(name: "Binary Return Backward Cubic-Mass Contraction")[
  For every terminal return state $n'$,
  $ sum_(n: T(n)=n') n^3 <= (8\/9)^3 (n')^3 < (n')^3. $
]
#proof[
  By the backward $3$-adic gate, there is at most one backward preimage. If no preimage exists, the sum is zero. If $n$ is the preimage, the backward contraction proposition with $r >= 0$ gives
  $ n < (8\/9)n'. $
  Cubing gives the displayed bound.
]

#proposition(name: "Binary Return Backward Moment Contraction")[
  For every real $theta > 0$ and every terminal return state $n'$,
  $ sum_(n: T(n)=n') n^theta <= (8\/9)^theta (n')^theta. $
]
#proof[
  As in the cubic case, there is at most one backward preimage. If it exists, the backward contraction proposition gives $n < (8\/9)n'$. Raising to the positive power $theta$ gives the claim.
]

#proposition(name: "Binary Return $y$-Normal Form")[
  Put $y_j = 33n_j + 32$. If the $j$-th binary return block has length $r_j$, then
  $ y_j = 16^(r_j) w_j $
  with $w_j$ odd, and
  $ 8 y_(j+1) = 9 dot 27^(r_j) w_j + 1. $
  Equivalently,
  $ 8 dot 16^(r_j) y_(j+1)
     = 9 dot 27^(r_j) y_j + 16^(r_j). $
  Consequently,
  $ y_(j+1) > y_j $
  and for any $N$ consecutive return blocks,
  $ y_N >= (9\/8)^N (27\/16)^(r_0 + dots + r_(N-1)) y_0. $
]
#proof[
  The identity $y_j=16^(r_j)w_j$ is just the return reparameterization. The same proposition gives
  $33n_(j+1)+32 = (9 dot 27^(r_j) w_j + 1)/8,$
  which is the first displayed equation. Substituting $w_j=y_j\/16^(r_j)$ and clearing denominators gives the equivalent equation.

  Since $r_j >= 0$, the coefficient
  $ (9\/8)(27\/16)^(r_j) $
  is greater than $1$, and the affine form
  $ y_(j+1) = (9\/8)(27\/16)^(r_j)y_j + 1\/8 $
  gives $y_(j+1) > y_j$. Iterating and dropping the positive additive terms gives the displayed lower bound.
]

#proposition(name: "All-Zero Binary Return Branch")[
  A depth-$0$ parameter $n_0$ has first $L$ binary return blocks all of length $0$ if and only if
  $ n_0 equiv -1 mod 8^L. $
  The least nonnegative such start is $n_0 = 8^L - 1$, and along this branch
  $ n_i = 9^i 8^(L-i) - 1 quad (0 <= i <= L). $
  The corresponding infinite all-zero binary return code is $n_0=-1$, not a nonnegative integer.
]
#proof[
  On a zero return block the map is
  $ n_(i+1) = (9n_i+1)\/8. $
  Thus
  $ n_i + 1 = (9\/8)^i (n_0+1). $
  The $i$-th return block has length $0$ exactly when $n_i equiv 7 mod 8$, equivalently $8 | n_i+1$. Since $9$ is odd, requiring this for $0 <= i < L$ is equivalent to $8^L | n_0+1$. The least nonnegative representative and the displayed formula follow immediately. Taking $L arrow.r infinity$ gives the unique $2$-adic code $n_0=-1$.
]

#proposition(name: "Constant Binary Return Branch")[
  Fix a return length $r >= 0$, and let $P_r,Q_r,D_r$ be the one-block data from the binary return-block coding proposition. A depth-$0$ parameter $n_0$ has first $L$ return blocks all equal to $r$ if and only if
  $ n_0 equiv -D_r / (P_r - Q_r) mod Q_r^L, $
  equivalently
  $ (P_r - Q_r)n_0 equiv -D_r mod Q_r^L. $
  The infinite constant-$r$ return code is the rational
  $ n_* = -D_r / (P_r - Q_r), $
  which lies in $[-1,0)$ and hence is not a nonnegative integer.
]
#proof[
  For fixed $r$, the return map is
  $ f_r(n) = (P_r n + D_r) / Q_r. $
  Since $P_r > Q_r$, its fixed point is
  $ n_* = -D_r / (P_r - Q_r). $
  The return critical-series proposition gives $0 < D_r <= P_r-Q_r$, with equality only for $r=0$, so $n_* in [-1,0)$.

  The denominator $P_r-Q_r$ is odd, so $n_*$ is a valid residue modulo every power of $Q_r$. Also
  $ n_i - n_* = (P_r\/Q_r)^i (n_0-n_*) $
  along a constant-$r$ branch. Since $P_r$ is odd, requiring the length-$r$ return divisibility condition for $0 <= i < L$ is equivalent to
  $ n_0 equiv n_* mod Q_r^L. $
  Multiplying by the odd denominator $P_r-Q_r$ gives the displayed integral congruence.
]

#proposition(name: "Binary Return-Length Height Bound")[
  If a depth-$0$ parameter $n$ begins a finite binary return block $0 arrow.r 1^r arrow.r 0$, then
  $ n >= (5 dot 16^r - 32) / 33. $
  Equivalently,
  $ r <= (log_2(33n+32) - log_2 5) / 4. $
]
#proof[
  By the partial-map proposition, $33n+32 = 16^r w$ with $w$ a positive odd integer. Moreover $w equiv 7 mod 8$ when $r$ is even and $w equiv 5 mod 8$ when $r$ is odd, so in all cases $w >= 5$. Hence $33n+32 >= 5 dot 16^r$, which is the first inequality. Taking base-$2$ logarithms gives the displayed upper bound for $r$.
]

#proposition(name: "Finite Binary Return Words Are Realizable")[
  For every finite sequence of return lengths $(r_0, dots, r_(L-1))$, there are infinitely many nonnegative depth-$0$ parameters $n_0$ whose binary return itinerary begins with exactly this sequence.
]
#proof[
  By the return-block coding proposition, the finite word imposes one congruence class
  $ n_0 equiv R mod Q, $
  where
  $ Q = product_(j=0)^(L-1) 2^(4r_j+3). $
  Every $n_0$ in this class satisfies the integrality gate for the first return block. The resulting return parameter $n_1$ then satisfies the prefix congruence for the remaining suffix word; iterating gives the prescribed return lengths $r_0, dots, r_(L-1)$.

  The arithmetic progression $R + Q k$ contains infinitely many nonnegative integers. For these starts all intermediate return parameters are nonnegative and in fact strictly increasing by the binary zero-return expansion lemma. Hence infinitely many starts realize the finite return word.
]

#remark[
  This is the binary-depth analogue of finite depth-word realizability. It rules out any proof of the $T=1$ case based on forbidding a finite pattern of return lengths. A successful proof must use an infinite height or bounded-residue argument.
]

#proposition(name: "Periodic Binary Return Branch")[
  Let $w=(r_0,dots,r_(p-1))$ be a nonempty finite return word, and write its one-period affine data as
  $ Q_w n_p = P_w n_0 + D_w. $
  For $L>=1$, let $w^L$ denote $L$ repetitions of $w$. A depth-$0$ parameter $n_0$ realizes the return word $w^L$ if and only if
  $ n_0 equiv n_w^* mod Q_w^L, quad
     n_w^* = -D_w / (P_w - Q_w), $
  equivalently
  $ (P_w-Q_w)n_0 equiv -D_w mod Q_w^L. $
  The infinite periodic return code selected by $w w w dots$ is $n_w^*$, and $n_w^* in [-1,0)$.
]
#proof[
  Each return block has multiplier greater than $1$, so $P_w>Q_w$. Since $D_w>0$, the period map
  $ F_w(n)=(P_w n + D_w)\/Q_w $
  has the fixed point
  $ n_w^*=-D_w\/(P_w-Q_w). $
  Applying the binary return critical-series proposition to the infinite periodic word $w w w dots$ shows that this same fixed point is the real critical value of the periodic word, hence lies in $[-1,0)$.

  Iterating the period map $L$ times gives
  $ Q_w^L n_(p L)
      = P_w^L n_0
        + D_w (P_w^L-Q_w^L)/(P_w-Q_w). $
  Since
  $ P_w^L n_w^*
      + D_w (P_w^L-Q_w^L)/(P_w-Q_w)
      = -D_w Q_w^L/(P_w-Q_w), $
  and $P_w-Q_w$ is odd, the divisibility condition modulo $Q_w^L$ is equivalent to
  $ P_w^L (n_0-n_w^*) equiv 0 mod Q_w^L. $
  The coefficient $P_w^L$ is odd, hence invertible modulo $Q_w^L$, so this is equivalent to $n_0 equiv n_w^* mod Q_w^L$. For $L=1$ this is exactly the finite-word residue class of $w$, and the same calculation for $w^L$ gives the stated finite-shadow criterion.
]

#proposition(name: "No Eventually Periodic Binary Return Itinerary")[
  No infinite positive-integer binary-depth obstruction can have an eventually periodic sequence of return lengths $(r_0, r_1, dots)$.
]
#proof[
  If an infinite positive orbit had an eventually periodic return itinerary, discard the finite preperiod and let $w$ be the repeating return word of the remaining positive tail. The periodic branch proposition shows that the starting state of this tail would have to equal the rational periodic code $n_w^* in [-1,0)$, contradicting positivity.
]

#proposition(name: "Binary Return Fixed Positive-Label Divergence")[
  Fix $J >= 0$. Let $mu_(L,J)^+$ be the least return-prefix residue among length-$L$ return words with at most $J$ positive return lengths. Then
  $ mu_(L,J)^+ arrow.r infinity $
  as $L arrow.r infinity$.
]
#proof[
  The minimum exists at every length: the all-zero word gives a finite candidate, and the binary return finite-height search criterion makes the set of words below any fixed candidate finite.

  The sequence $mu_(L,J)^+$ is nondecreasing. Indeed, any length-$(L+1)$ word with at most $J$ positive labels has a length-$L$ prefix with at most $J$ positive labels, and prefix residues are nondecreasing under extension.

  Suppose the sequence did not tend to infinity. Since it is nondecreasing, it is bounded by some integer $B$. Consider the tree of finite return words with at most $J$ positive labels and least prefix residue at most $B$. It has nodes at every depth by the definition of $mu_(L,J)^+$, and it is finitely branching by the finite-height search criterion. Hence the elementary infinite-tree lemma gives an infinite path.

  Every prefix of this path has at most $J$ positive labels, so the infinite path itself has at most $J$ positive labels. Therefore its return-length word is eventually all zero, hence eventually periodic. Along the path the prefix residues are bounded, so the return-code boundedness criterion gives a nonnegative ordinary infinite return code with an eventually periodic return itinerary. This contradicts the no eventually periodic binary return itinerary proposition.
]
#remark[
  In the first nonconstant alphabet ${0,1}$, this proves that every fixed-one-count stratum has diverging least residues. A bounded-residue obstruction over ${0,1}$ would therefore need infinitely many $1$ labels; the remaining sparse case is not "finitely many spikes," but an infinite nonperiodic sparse pattern.
]

#proposition(name: "Binary Return Prefix-Language Compactness Principle")[
  Let $C$ be a prefix-closed collection of finite return words, and let $C_L$ be its words of length $L$. Suppose $C_L$ is nonempty for arbitrarily large $L$. For each such $L$, let
  $ mu_C(L) = min { R_w : w in C_L }. $
  If $mu_C(L)$ does not tend to infinity along the lengths where it is defined, then there is an infinite return-length word whose every finite prefix lies in $C$ and whose return code is a nonnegative ordinary integer.

  Consequently, if every infinite word with all prefixes in $C$ is already excluded as an ordinary return itinerary, then $mu_C(L) arrow.r infinity$.
]
#proof[
  If $mu_C(L)$ does not tend to infinity, then because prefix residues are nondecreasing under extension, the values $mu_C(L)$ are bounded by some integer $B$ along arbitrarily large lengths. Consider the tree of words $w in C$ satisfying $R_w <= B$. This tree has nodes at arbitrarily large depths, and by prefix closure it has nodes at every smaller depth. It is finitely branching below the fixed height bound $B$ by the binary return finite-height search criterion. Hence it has an infinite path.

  Along this path the return-prefix residues are nondecreasing and bounded by $B$, so they are eventually constant. The return-code boundedness criterion turns the path into a nonnegative ordinary infinite return code. The final consequence is the contrapositive.
]

#proposition(name: "Binary Return Finite-Defect Periodic Shadow Divergence")[
  Fix an eventually periodic infinite return-length word $z=(z_0,z_1,dots)$ and an integer $J >= 0$. Let $mu_(L,J)(z)$ be the least return-prefix residue among length-$L$ return words that differ from $(z_0,dots,z_(L-1))$ in at most $J$ positions. Then
  $ mu_(L,J)(z) arrow.r infinity $
  as $L arrow.r infinity$.
]
#proof[
  The prefix $(z_0,dots,z_(L-1))$ itself is an admissible finite candidate. The binary return finite-height search criterion makes the set of words below any fixed candidate finite, so the minimum exists.

  The sequence $mu_(L,J)(z)$ is nondecreasing: any admissible length-$(L+1)$ word has an admissible length-$L$ prefix relative to the prefix of $z$, and return-prefix residues are nondecreasing under extension.

  If $mu_(L,J)(z)$ did not tend to infinity, then it would be bounded by some $B$. Consider the tree of finite return words that differ from the corresponding prefix of $z$ in at most $J$ positions and have least prefix residue at most $B$. It has nodes at every depth and is finitely branching by the finite-height search criterion, so it contains an infinite path.

  The infinite path differs from $z$ in at most $J$ positions total. Since $z$ is eventually periodic, the path is also eventually periodic. Its bounded prefix residues give a nonnegative ordinary infinite return code by the return-code boundedness criterion, contradicting the no eventually periodic binary return itinerary proposition.
]
#remark[
  Thus a bounded-residue return obstruction cannot stay within bounded edit distance of any eventually periodic return-length template. It must have genuinely unbounded defect from every periodic shadow, not just from the all-zero shadow.
]

#proposition(name: "Morse-Hedlund Complexity Criterion")[
  Let $x=x_0 x_1 x_2 dots$ be an infinite word over a finite alphabet, and let $p_x(m)$ be the number of distinct length-$m$ factors appearing in $x$. If $p_x(m) <= m$ for some $m>=1$, then $x$ is eventually periodic.
  More generally, if $x$ is not eventually periodic and uses $q=p_x(1)$ distinct symbols, then
  $ p_x(m) >= m+q-1 $
  for every $m>=1$.
]
#proof[
  If the alphabet actually used by $x$ has one symbol, the word is periodic. Otherwise $p_x(1)>=2$.
  If $m=1$, then $p_x(m)<=m$ forces $p_x(1)<=1$, which is the one-symbol case. Hence assume $m>=2$.

  If $p_x(j+1)>p_x(j)$ for every $1 <= j < m$, then
  $ p_x(m) >= p_x(1)+m-1 >= m+1, $
  contradicting $p_x(m)<=m$. Hence for some $j<m$ one has $p_x(j+1)=p_x(j)$.

  Every length-$j$ factor has at least one right extension in the infinite word. Since the number of length-$(j+1)$ factors equals the number of length-$j$ factors, each length-$j$ factor has exactly one right extension. Now slide a length-$j$ window along $x$. The next window is determined uniquely by the current one. There are only finitely many such windows, so the window sequence is eventually periodic, and therefore the original word is eventually periodic.

  The contrapositive of the equality argument says that a non-eventually-periodic word must satisfy $p_x(j+1)>p_x(j)$ for every $j>=1$. Since $p_x(1)=q$, induction gives $p_x(m)>=m+q-1$.
]

#definition(name: "Balanced Binary Word")[
  A finite or infinite binary word is _balanced_ if any two finite factors $u$ and $v$ of the same length satisfy
  $ |op("ones")(u) - op("ones")(v)| <= 1. $
]

#proposition(name: "Balanced Aperiodic Positive-Density Lemma")[
  Let $x$ be a non-eventually-periodic balanced infinite binary word. Then both symbols occur with bounded gaps. In particular, there are constants $c_0,c_1,c_2>0$ such that every length-$L$ factor of $x$ contains at least $c_1 L + O(1)$ ones, at least $c_0 L + O(1)$ zeros, and at least $c_2 L + O(1)$ symbol changes.
]
#proof[
  Since $x$ is not eventually periodic, neither symbol can occur only finitely many times. Hence there are two consecutive occurrences of $1$ in $x$; let the factor from the first to the second have length $m_1$. This factor contains two ones. By balance, every factor of $x$ of length $m_1$ must contain at least one one, since a length-$m_1$ factor with no ones would differ from it by two ones. Therefore runs of zeros have length less than $m_1$.

  The same argument with two consecutive occurrences of $0$ gives a length $m_0$ such that every factor of length $m_0$ contains at least one zero. Thus runs of ones have length less than $m_0$.

  Partition any length-$L$ factor into consecutive blocks of length $m_1$, discarding only the final incomplete block. Each full block is itself a factor of $x$, hence contains a one, so the number of ones is at least $floor(L\/m_1)$. Similarly, the number of zeros is at least $floor(L\/m_0)$.

  Since every run of zeros has length less than $m_1$ and every run of ones has length less than $m_0$, every constant run has length at most $M=max(m_0,m_1)-1$. A length-$L$ factor therefore contains at least $floor(L\/M)-1$ symbol changes. This gives all displayed uniform linear lower bounds.
]
#remark[
  Therefore the balanced/Sturmian-like obstruction is neither a density-zero sparse problem nor a bounded-block-change problem. Sparse balanced finite minimizers can occur as finite shadows, but an infinite non-eventually-periodic balanced code would have both symbols and both transitions with positive lower density.
]

#proposition(name: "Balanced Slope Lemma")[
  Let $x$ be an infinite balanced binary word. Then there is a real number $alpha in [0,1]$ such that every length-$n$ factor $u$ of $x$ satisfies
  $ |op("ones")(u) - alpha n| <= 2. $
  If $x$ is not eventually periodic, then $0 < alpha < 1$.
]
#proof[
  Let $A(n)$ be the number of ones in the length-$n$ prefix of $x$. If $u$ is any length-$n$ factor, balance gives
  $ |op("ones")(u)-A(n)| <= 1. $

  Apply this to the length-$m$ factor that starts immediately after the first $n$ symbols. Its number of ones is $A(n+m)-A(n)$. Hence
  $ |A(n+m)-A(n)-A(m)| <= 1 $
  for all $m,n>=1$.

  Fix $n$ and write $N=q n+r$ with $0<=r<n$. Iterating the preceding almost-additivity inequality gives
  $ q A(n) + A(r) - q <= A(N) <= q A(n) + A(r) + q. $
  Dividing by $N$ and letting $N arrow.r infinity$ along this fixed $n$ gives
  $ (A(n)-1)\/n <= liminf_(N arrow.r infinity) A(N)\/N
     <= limsup_(N arrow.r infinity) A(N)\/N
     <= (A(n)+1)\/n. $
  Since this holds for every $n$, the limsup and liminf differ by at most $2\/n$ for every $n$, hence they are equal. Call the common limit $alpha$.

  The same displayed inequality, now with the common limit, gives $|A(n)-alpha n|<=1$ for every $n$. Combining this with $|op("ones")(u)-A(n)|<=1$ gives the factor bound.

  If $x$ is not eventually periodic, the balanced aperiodic positive-density lemma gives positive lower density of both symbols in every long prefix. Therefore $alpha$ is neither $0$ nor $1$.
]
#remark[
  The balanced frontier can therefore be parameterized by a slope $alpha in (0,1)$ up to bounded discrepancy. The missing landing theorem is not about arbitrary sparse balanced words; it is about bounded-discrepancy positive-density binary codings.
]

#proposition(name: "Balanced Aperiodic Irrational-Slope Lemma")[
  Let $x$ be a non-eventually-periodic balanced infinite binary word, and let $alpha$ be its slope. Then $alpha$ is irrational.
]
#proof[
  We use the classical classification of balanced infinite binary words: such words are Sturmian or skew, and the non-ultimately-periodic case is the aperiodic Sturmian case @glen2008. Aperiodic Sturmian words have irrational slope; conversely, rational-slope balanced binary words are ultimately periodic. Since $x$ is not eventually periodic, it lies in the aperiodic Sturmian case, so its slope $alpha$ is irrational.
]
#remark[
  The rational-slope balanced branch is therefore already covered by the periodic-itinerary exclusions. Any balanced ordinary return or reduced-gap obstruction must have irrational slope in $(0,1)$.
]

#proposition(name: "Balanced Sturmian Complexity Lemma")[
  Let $x$ be a non-eventually-periodic balanced infinite binary word, and let $p_x(m)$ be its factor complexity. Then
  $ p_x(m)=m+1 $
  for every $m>=1$.
]
#proof[
  By the same balanced-word classification, a non-eventually-periodic balanced binary word is an aperiodic Sturmian word @glen2008. Sturmian words are precisely the aperiodic binary words of minimal complexity, so their factor complexity is $p_x(m)=m+1$ at every length $m$.
]
#remark[
  Thus the balanced frontier is the exact minimal-complexity frontier. General bounded binary obstructions must be Sturmian-or-higher, but balanced obstructions themselves are exactly Sturmian.
]

#proposition(name: "Balanced Mechanical Normal Form")[
  Let $x=(x_i)_(i>=0)$ be a non-eventually-periodic balanced infinite binary word. Then there are an irrational $alpha in (0,1)$, an intercept $rho in [0,1)$, and a choice of lower or upper convention such that either
  $ x_i = floor((i+1) alpha + rho) - floor(i alpha + rho) $
  for every $i>=0$, or
  $ x_i = ceil((i+1) alpha + rho) - ceil(i alpha + rho) $
  for every $i>=0$.
]
#proof[
  By the balanced aperiodic irrational-slope lemma and the Sturmian complexity lemma, $x$ is an aperiodic Sturmian word of irrational slope $alpha$. The standard mechanical-word characterization of Sturmian words gives exactly the displayed lower or upper rotation coding with some intercept $rho$ @lothaire2002. Replacing $rho$ by $rho-m$ for an integer $m$ shifts both floor terms, or both ceiling terms, by the same integer and therefore leaves every digit unchanged. Hence the intercept may be normalized to $[0,1)$.
]
#remark[
  Consequently, the balanced landing problem is a two-parameter irrational-rotation problem: no choice of irrational slope $alpha$ and intercept $rho$ should make the return or reduced-gap critical series land on a positive ordinary integer.
]

#proposition(name: "Mechanical Convention Reduction")[
  Fix irrational $alpha in (0,1)$ and $rho in [0,1)$. The lower and upper mechanical words with slope $alpha$ and intercept $rho$ differ in at most two adjacent positions.

  Consequently, to exclude positive ordinary return or reduced-gap landings for all mechanical words, it is enough to exclude the lower mechanical convention for all irrational $alpha in (0,1)$ and all normalized intercepts $rho in [0,1)$.
]
#proof[
  Put $t_i=i alpha+rho$. Let
  $ ell_i=floor(t_(i+1))-floor(t_i) $
  be the lower digit and
  $ u_i=ceil(t_(i+1))-ceil(t_i) $
  the upper digit. Then
  $ u_i-ell_i = (ceil(t_(i+1))-floor(t_(i+1))) - (ceil(t_i)-floor(t_i)). $
  The parenthesized term is $0$ exactly when its argument is an integer and is $1$ otherwise.

  Since $alpha$ is irrational, there is at most one index $j>=0$ for which $t_j$ is an integer: two such indices would make $(j-k)alpha$ an integer. Hence $u_i-ell_i$ can be nonzero only when $i=j-1$ or $i=j$. The lower and upper words therefore differ in at most two adjacent positions.

  Now suppose an upper mechanical word has a positive ordinary return code. Choose $J$ after the possible exceptional positions. By the binary return shift-code recurrence, the positive state reached after the first $J$ return blocks is the ordinary return code for the shifted suffix. That shifted suffix agrees with the corresponding lower mechanical suffix. But shifting a lower mechanical word by $J$ positions gives another lower mechanical word with the same slope and intercept $rho+J alpha$, normalized modulo $1$. Therefore an upper-convention return landing would imply a lower-convention return landing. The reduced-gap case is identical, using the binary ${0,1}$ gap shift-code recurrence. Thus excluding lower mechanical landings excludes both conventions.
]
#remark[
  The balanced landing problem may therefore be attacked using only lower mechanical words. The upper convention introduces at most a finite prefix effect, and finite prefixes are absorbed by the shift-code recurrences.
]

#proposition(name: "Mechanical Uniform Recurrence Lemma")[
  Let $x$ be a non-eventually-periodic balanced infinite binary word. Then $x$ is uniformly recurrent: every finite factor of $x$ occurs in $x$ with bounded gaps.
]
#proof[
  By the balanced mechanical normal form, $x$ is an aperiodic Sturmian word, up to the lower/upper convention and a normalized intercept. Standard Sturmian theory gives uniform recurrence for aperiodic Sturmian words @lothaire2002. Equivalently, in the mechanical representation, factors correspond to intervals for an irrational circle rotation, and irrational rotations return to each such interval with bounded gaps.
]
#remark[
  Therefore a balanced ordinary landing, if it exists, is not a one-time exotic coding. Every finite prefix pattern of its mechanical word reappears infinitely often with bounded gaps, and the shift-code recurrences then attach positive ordinary codes to all of those shifted suffixes.
]

#proposition(name: "Lower Mechanical Prefix-Cylinder Lemma")[
  Fix irrational $alpha in (0,1)$ and a lower mechanical word
  $ x_i=floor((i+1)alpha+rho)-floor(i alpha+rho) $
  with $rho in [0,1)$. For a finite binary word
  $w=(w_0,dots,w_(m-1))$, let $cal(C)_w$ be the set of intercepts $eta in [0,1)$ for which
  $ floor((i+1)alpha+eta)-floor(i alpha+eta)=w_i $
  for every $0<=i<m$.

  If $w$ is the initial length-$m$ prefix of $x$, then $cal(C)_w$ has positive Lebesgue measure, contains $rho$ in the lower half-open convention, and
  $ (x_j,dots,x_(j+m-1))=w $
  if and only if
  $ rho+j alpha mod 1 in cal(C)_w. $
  Consequently the set of such indices $j$ has natural density $|cal(C)_w|>0$ and has bounded gaps.
]
#proof[
  Put $theta_i=eta+i alpha mod 1$, represented in $[0,1)$. The lower digit at position $i$ equals $1$ exactly when $theta_i in [1-alpha,1)$, and equals $0$ exactly when $theta_i in [0,1-alpha)$. Hence $cal(C)_w$ is the finite intersection, over $0<=i<m$, of shifted half-open intervals on the circle. Its boundary is contained in the finite set
  $ {0,-alpha,-2alpha,dots,-m alpha} mod 1. $
  Since $alpha$ is irrational, these boundary points are distinct.

  The initial word $w$ is realized at the intercept $rho$. If $rho$ is not one of the displayed boundary points, local constancy of the digit map gives a neighborhood of $rho$ contained in $cal(C)_w$. If $rho$ is a boundary point, the lower convention selects one of the two adjacent half-open continuity intervals; that adjacent interval is still contained in $cal(C)_w$ near $rho$. Thus $cal(C)_w$ has positive measure.

  The suffix beginning at position $j$ is obtained from the same lower mechanical coding with intercept $rho+j alpha mod 1$, so the length-$m$ prefix of that suffix is $w$ exactly when $rho+j alpha mod 1 in cal(C)_w$. Irrational rotations are equidistributed @kuipers1974, hence visits to the finite-union set $cal(C)_w$, whose boundary has measure zero, have natural density $|cal(C)_w|$. Since irrational rotations are minimal on the circle and $cal(C)_w$ contains a nonempty interval, the gaps between visits are bounded.
]
#remark[
  After the mechanical convention reduction, the balanced landing problem can be phrased through these lower prefix cylinders. A hypothetical balanced landing would force fixed high-power-of-two prefix congruences on positive-density rotation hitting sets, not merely along a sparse recurrence subsequence.
]

#proposition(name: "Balanced Landing Recurrent Prefix Congruences")[
  Suppose a non-eventually-periodic balanced return word $r=(r_0,r_1,dots)$ has positive ordinary return code $X_0$, and let $X_j$ be the positive state after the first $j$ return blocks. Fix $m>=1$, and let $R_m,Q_m$ be the least prefix residue and modulus of the initial return prefix $(r_0,dots,r_(m-1))$. Then there are infinitely many indices $j$, with bounded gaps depending on $m$, such that
  $ X_j equiv R_m mod Q_m. $

  Similarly, suppose a non-eventually-periodic balanced zero-gap word $k=(k_0,k_1,dots)$ has positive ordinary gap code $Y_0$, and let $Y_j$ be the positive state after the first $j$ gap transitions. If $S_m,H_m$ are the least prefix residue and modulus of the initial gap prefix $(k_0,dots,k_(m-1))$, then there are infinitely many indices $j$, with bounded gaps depending on $m$, such that
  $ Y_j equiv S_m mod H_m. $
]
#proof[
  The initial length-$m$ block is a finite factor of the balanced word. By the mechanical uniform recurrence lemma, it occurs with bounded gaps. Thus there are infinitely many indices $j$ such that
  $ (r_j,dots,r_(j+m-1))=(r_0,dots,r_(m-1)) $
  in the return case, with gaps between successive such $j$ bounded in terms of $m$.

  By the binary return shift-code recurrence, $X_j$ is the positive ordinary return code of the shifted suffix $(r_j,r_(j+1),dots)$. Since that shifted suffix begins with the same length-$m$ prefix as the original word, the binary return forced-orbit prefix equivalence gives
  $ X_j equiv R_m mod Q_m. $

  The reduced-gap proof is identical: uniform recurrence gives bounded-gap occurrences of the initial length-$m$ gap block, the binary ${0,1}$ gap shift-code recurrence makes $Y_j$ the ordinary code of the shifted suffix, and the binary ${0,1}$ gap forced-orbit prefix equivalence gives
  $ Y_j equiv S_m mod H_m. $
]
#remark[
  A balanced landing would therefore generate an expanding positive orbit that repeatedly returns to every initial prefix congruence class. The missing contradiction can be sought as an incompatibility between this recurrent congruence self-shadowing and the real exponential height law.
]

#proposition(name: "Lower Mechanical Landing Prefix-Cylinder Congruences")[
  Suppose a lower mechanical balanced return word of irrational slope $alpha$ and intercept $rho$ has positive ordinary return code. Fix $m>=1$, let $w$ be its initial length-$m$ prefix, let $cal(C)_w$ be the lower prefix cylinder from the preceding lemma, and let $R_m,Q_m$ be the least prefix residue and modulus of $w$. If $X_j$ is the positive return state after $j$ return blocks, then the set
  $ J_m={j>=0: rho+j alpha mod 1 in cal(C)_w} $
  has natural density $|cal(C)_w|>0$, has bounded gaps, and satisfies
  $ X_j equiv R_m mod Q_m $
  for every $j in J_m$.

  The same statement holds for a lower mechanical balanced reduced-gap landing, with the gap states $Y_j$ and the least prefix residue/modulus $S_m,H_m$.
]
#proof[
  By the lower mechanical prefix-cylinder lemma, $J_m$ is exactly the set of positions where the initial length-$m$ prefix reappears, and this set has positive natural density and bounded gaps. For each $j in J_m$, the shifted suffix begins with the same length-$m$ prefix $w$. The return shift-code recurrence makes $X_j$ the ordinary return code of that shifted suffix, and the return forced-orbit prefix equivalence gives $X_j equiv R_m mod Q_m$. The reduced-gap proof is identical, using the binary ${0,1}$ gap shift-code recurrence and the gap forced-orbit prefix equivalence.
]
#remark[
  This is the strongest current form of the balanced self-shadowing obstruction. For every fixed prefix modulus, a positive-density set of later ordinary states lies in the same residue class modulo that modulus, while the same states follow the irrational-slope exponential growth law.
]

#proposition(name: "Mechanical Prefix-Sum Modulus Formula")[
  Let $x=(x_i)_(i>=0)$ be a mechanical binary word of irrational slope $alpha in (0,1)$ and intercept $rho in [0,1)$. Put
  $ X_N = x_0 + dots + x_(N-1). $
  In the lower convention
  $ x_i = floor((i+1) alpha + rho) - floor(i alpha + rho) $
  one has
  $ X_N = floor(N alpha + rho) - floor(rho). $
  In the upper convention
  $ x_i = ceil((i+1) alpha + rho) - ceil(i alpha + rho) $
  one has
  $ X_N = ceil(N alpha + rho) - ceil(rho). $

  Consequently, for a mechanical balanced return word the prefix modulus is exactly
  $ Q_N = 2^(3N+4X_N), $
  and for a mechanical balanced reduced-gap word the prefix modulus is exactly
  $ H_N = 2^(7N+3X_N). $
]
#proof[
  Both prefix-sum identities telescope immediately:
  $ sum_(i=0)^(N-1) (floor((i+1) alpha + rho) - floor(i alpha + rho))
     = floor(N alpha + rho) - floor(rho), $
  and the same calculation with ceilings gives the upper convention.

  In the binary return system, the one-block modulus for a digit $x_i in {0,1}$ is $2^(4x_i+3)$, so the length-$N$ prefix modulus is
  $ product_(i=0)^(N-1) 2^(4x_i+3) = 2^(3N+4X_N). $
  In the reduced-gap system, the one-block modulus is $2^(3x_i+7)$, giving
  $ product_(i=0)^(N-1) 2^(3x_i+7) = 2^(7N+3X_N). $
]
#remark[
  At this stage of the reduction, the mechanical landing problem can be written with exact floor or ceiling exponents, not just slope-asymptotic exponents. The obstruction is a divisibility problem along the sequence $floor(N alpha + rho)$ or $ceil(N alpha + rho)$; the later Sturmian recurrence argument closes this balanced branch.
]

#proposition(name: "Mechanical Landing Divisibility Normal Form")[
  Let $x=(x_i)_(i>=0)$ be a lower or upper mechanical binary word of irrational slope $alpha$ and intercept $rho in [0,1)$, and let $X_N=x_0+dots+x_(N-1)$ be given by the mechanical prefix-sum formula.

  For the binary return system, define $D_0^*=0$ and
  $ D_(N+1)^* = 9 dot 27^(x_N) D_N^* + d_(x_N) Q_N, $
  where $d_0=1$, $d_1=112$, and $Q_N=2^(3N+4X_N)$. Then the length-$N$ return prefix has
  $ P_N = 9^N dot 27^(X_N), quad Q_N=2^(3N+4X_N), quad D_N=D_N^*. $
  Hence a positive integer $M$ is the ordinary return landing for the mechanical word if and only if, for every $N>=1$,
  $ v_2(9^N dot 27^(X_N) M + D_N^*) >= 3N+4X_N. $

  For the reduced-gap system, define $C_0^*=0$ and
  $ C_(N+1)^* = 3^(5+2x_N) C_N^* + 8^(x_N) H_N, $
  where $H_N=2^(7N+3X_N)$. Then the length-$N$ gap prefix has
  $ A_N = 3^(5N+2X_N), quad H_N=2^(7N+3X_N), quad C_N=C_N^*. $
  Hence a positive integer $A$ is the ordinary reduced-gap landing for the mechanical word if and only if, for every $N>=1$,
  $ v_2(3^(5N+2X_N) A - C_N^*) >= 7N+3X_N. $
]
#proof[
  In the return system, the binary one-block data are
  $ p_x=9 dot 27^x, quad q_x=2^(4x+3), quad d_0=1, quad d_1=112. $
  The affine-composition recurrence is
  $ P_(N+1)=p_(x_N)P_N, quad Q_(N+1)=q_(x_N)Q_N, quad
     D_(N+1)=p_(x_N)D_N+d_(x_N)Q_N, $
  starting from $P_0=Q_0=1$ and $D_0=0$. Multiplying the coefficients over the first $N$ digits gives
  $ P_N=product_(i=0)^(N-1) 9 dot 27^(x_i)=9^N dot 27^(X_N), $
  while the mechanical prefix-sum modulus formula gives $Q_N=2^(3N+4X_N)$. The displayed recursion is exactly the same additive recurrence. The return ordinary-landing divisibility criterion then gives the valuation condition.

  In the reduced-gap system, the binary one-block data are
  $ a_x=3^(5+2x), quad h_x=2^(7+3x), quad c_x=8^x, $
  with composition recurrence
  $ A_(N+1)=a_(x_N)A_N, quad H_(N+1)=h_(x_N)H_N, quad
     C_(N+1)=a_(x_N)C_N+c_(x_N)H_N. $
  Thus $A_N=3^(5N+2X_N)$, $H_N=2^(7N+3X_N)$, and the displayed recursion gives $C_N^*$. The reduced-gap ordinary-landing divisibility criterion gives the final valuation condition.
]
#remark[
  The balanced landing problem is now an explicit pair of valuation problems for irrational floor or ceiling words. The return obstruction would require the signs $+D_N^*$ to create arbitrarily high powers of $2$ along $9^N dot 27^(X_N)M+D_N^*$; the reduced-gap obstruction would require the signs $-C_N^*$ to do the same along $3^(5N+2X_N)A-C_N^*$.
]

#proposition(name: "Balanced Periodic-Shadow Linear Separation")[
  Let $x$ be a non-eventually-periodic balanced infinite binary word, and let $z$ be any eventually periodic infinite binary word. Then there is a constant $c>0$ such that the Hamming distance between their length-$L$ prefixes is at least
  $ c L + O(1). $
]
#proof[
  Let $alpha$ be the slope of $x$. By the balanced aperiodic irrational-slope lemma, $alpha$ is irrational. The balanced slope lemma gives
  $ op("ones")(x_0 dots x_(L-1)) = alpha L + O(1). $

  Since $z$ is eventually periodic, its prefix-one count has a rational frequency $beta$:
  $ op("ones")(z_0 dots z_(L-1)) = beta L + O(1), $
  where $beta$ is the number of ones in one eventual period divided by the period length. Thus $beta in QQ$. Since $alpha$ is irrational, $c=|alpha-beta|>0$.

  The Hamming distance between two binary words is at least the absolute difference of their one counts. Therefore
  $ d_H(x_0 dots x_(L-1), z_0 dots z_(L-1))
     >= |alpha-beta| L + O(1), $
  as claimed.
]
#remark[
  Thus a balanced obstruction is not merely at unbounded edit distance from every periodic shadow; it is linearly far from each fixed eventually periodic shadow. Rational periodic approximants may still shadow finite windows, but no fixed periodic template can track an infinite balanced obstruction with sublinear defect.
]

#proposition(name: "Balanced Ordinary Landing Growth Rate")[
  Suppose a non-eventually-periodic balanced binary return word has ordinary return code $M$ and slope $alpha$. Let $n_N$ be the positive return state after its first $N$ return blocks. Then $alpha$ is irrational and
  $ log n_N / N arrow.r log(9\/8) + alpha log(27\/16). $
  Moreover its prefix modulus satisfies
  $ log_2 Q_N = (3+4 alpha)N + O(1). $

  Similarly, suppose a non-eventually-periodic balanced binary zero-gap word has positive ordinary gap code $A$ and slope $alpha$, and let $a_N$ be the state after its first $N$ gap blocks. Then $alpha$ is irrational and
  $ log a_N / N arrow.r log(243\/128) + alpha log(9\/8), $
  while
  $ log_2 H_N = (7+3 alpha)N + O(1). $
]
#proof[
  The irrationality of $alpha$ follows from the balanced aperiodic irrational-slope lemma.

  For the return statement, let $S_N=r_0+dots+r_(N-1)$. The balanced slope lemma gives $S_N=alpha N+O(1)$. The return block multipliers satisfy
  $ P_N\/Q_N = product_(j=0)^(N-1) (9 dot 27^(r_j)) / 2^(4r_j+3)
    = (9\/8)^N (27\/16)^(S_N), $
  and
  $ Q_N = 2^(3N+4S_N). $
  If $M_N=-D_N\/P_N$ is the return critical-series partial sum, the affine composition gives
  $ n_N=(P_N\/Q_N)(M-M_N). $
  The return critical-series proposition gives $-1 <= M_N < 0$, so the factor $M-M_N$ is bounded above and below by positive constants independent of $N$. Taking logarithms and dividing by $N$ gives the claimed return growth rate, and the modulus estimate follows from $S_N=alpha N+O(1)$.

  For the reduced gap statement, let $K_N=k_0+dots+k_(N-1)$. Again $K_N=alpha N+O(1)$. The gap expansion factor is
  $ A_N\/H_N = (243\/128)^N (9\/8)^(K_N), $
  and $H_N=2^(7N+3K_N)$. If $L_N=C_N\/A_N$ is the gap critical-series partial sum, then
  $ a_N=(A_N\/H_N)(A-L_N). $
  Since $0<L_N<1\/115$ and $A>=1$, the factor $A-L_N$ is bounded above and below by positive constants independent of $N$. Taking logarithms gives the gap growth rate and the modulus estimate.
]
#remark[
  Thus the remaining balanced obstruction, if it exists, is not only positive-density and irrational-slope; it is an ordinary integer orbit with an irrational-slope exponential height law. The missing theorem must show that this 2-adic landing cannot happen, not merely that the orbit has the wrong average expansion.
]

#proposition(name: "Balanced Landing Prefix-Return-Time Lower Bound")[
  Suppose a lower mechanical balanced return word of irrational slope $alpha$ has positive ordinary return code, and let $tau_m$ be the least positive index at which its initial length-$m$ prefix recurs. Then
  $ liminf_(m arrow.r infinity) tau_m / m
     >= (3+4 alpha) / (log_2(9\/8)+alpha log_2(27\/16)). $

  Similarly, if a lower mechanical balanced reduced-gap word of slope $alpha$ has a positive ordinary gap code, and $sigma_m$ is the least positive recurrence time of its initial length-$m$ prefix, then
  $ liminf_(m arrow.r infinity) sigma_m / m
     >= (7+3 alpha) / (log_2(243\/128)+alpha log_2(9\/8)). $
]
#proof[
  We prove the return statement. Let $M$ be the ordinary return code, $Q_m$ the length-$m$ prefix modulus, and $X_j$ the positive state after $j$ return blocks. Since $M$ realizes the infinite code, the forced-prefix congruence gives
  $ M equiv R_m mod Q_m $
  for the length-$m$ prefix residue $R_m$. If $tau_m$ is a recurrence time for the initial prefix, the lower mechanical landing prefix-cylinder congruence gives
  $ X_(tau_m) equiv R_m mod Q_m, $
  hence
  $ X_(tau_m) equiv M mod Q_m. $

  The word is not eventually periodic, so $tau_m arrow.r infinity$: otherwise some fixed positive shift would agree with arbitrarily long initial prefixes. The balanced ordinary landing growth-rate lemma gives
  $ log_2 X_(tau_m) = (log_2(9\/8)+alpha log_2(27\/16)) tau_m + o(tau_m), $
  while the mechanical prefix-sum modulus formula gives
  $ log_2 Q_m = (3+4 alpha)m+O(1). $

  If the displayed lower bound failed, then for some $epsilon>0$ and infinitely many $m$ one would have
  $ tau_m <= ((3+4 alpha) / (log_2(9\/8)+alpha log_2(27\/16)) - epsilon)m. $
  Along this subsequence, the two logarithmic estimates imply $X_(tau_m)<Q_m$ for all large $m$. Also $Q_m>M$ for all large $m$, and $X_(tau_m)>M$ for all large $m$ because $tau_m arrow.r infinity$ and the growth rate is positive. But $X_(tau_m) equiv M mod Q_m$ with both numbers strictly between $0$ and $Q_m$ forces $X_(tau_m)=M$, a contradiction.

  The reduced-gap statement is identical. Replace $M,X_j,Q_m$ by the ordinary gap code $A$, gap states $Y_j$, and prefix modulus $H_m$. Use
  $ log_2 Y_(sigma_m) = (log_2(243\/128)+alpha log_2(9\/8)) sigma_m+o(sigma_m) $
  and
  $ log_2 H_m=(7+3 alpha)m+O(1). $
]
#remark[
  This converts the balanced landing problem into a recurrence-speed obstruction. Any lower mechanical landing would require every sufficiently long initial prefix to have first recurrence time at least a large slope-dependent multiple of its length. A proof that lower mechanical prefixes recur below this threshold infinitely often would eliminate the balanced landing branch.
]

#proposition(name: "Fast Prefix-Recurrence Exclusion Criterion")[
  Let $x$ be a lower mechanical binary word of irrational slope $alpha$, and let $tau_m$ be the least positive recurrence time of its initial length-$m$ prefix. If
  $ liminf_(m arrow.r infinity) tau_m / m
     < (3+4 alpha) / (log_2(9\/8)+alpha log_2(27\/16)), $
  then $x$ has no positive ordinary return code.

  Likewise, let $y$ be a lower mechanical binary word of irrational slope $alpha$, and let $sigma_m$ be the least positive recurrence time of the initial length-$m$ prefix of $y$. If
  $ liminf_(m arrow.r infinity) sigma_m / m
     < (7+3 alpha) / (log_2(243\/128)+alpha log_2(9\/8)), $
  then $y$ has no positive ordinary reduced-gap code.
]
#proof[
  This is exactly the contrapositive of the balanced landing prefix-return-time lower bound, after applying the mechanical convention reduction to restrict the balanced branch to lower mechanical words.
]
#remark[
  This gives a clean plug-in target for Sturmian recurrence theory. To finish the balanced branch it is enough to prove, for every lower irrational mechanical word, that its initial prefixes recur infinitely often below the relevant threshold. The exact thresholds are all large: the return threshold ranges from about $7.57$ to $17.66$ as $alpha$ varies in $(0,1)$, while the reduced-gap threshold ranges from about $7.56$ to $9.12$.
]

#proposition(name: "Sturmian Fast Prefix-Recurrence Lemma")[
  Let $x$ be a non-eventually-periodic balanced binary word, and let $tau_m$ be the least positive recurrence time of its initial length-$m$ prefix. Then
  $ liminf_(m arrow.r infinity) tau_m / m <= 2. $
]
#proof[
  By the balanced mechanical normal form, $x$ is an aperiodic Sturmian word. Let $R_x(m)$ be its recurrence function: the least integer $N$ such that every length-$N$ factor of $x$ contains every length-$m$ factor of $x$.

  The standard Morse--Hedlund recurrence-function formula for Sturmian words gives, for the continued-fraction denominators $q_n$ of the slope,
  $ R_x(q_n-1) = (q_n-1)-1+q_n+q_(n-1) $
  @morse1940 @lothaire2002. This is the only part of the formula needed here.

  Put $m_n=q_n-1$. Apply the definition of $R_x(m_n)$ to the length-$R_x(m_n)$ factor beginning at position $1$. It contains every length-$m_n$ factor, including the initial prefix $x_0 dots x_(m_n-1)$. Hence that prefix occurs again at some position
  $ 1 <= j <= R_x(m_n)-m_n+1 = q_n+q_(n-1). $
  Therefore
  $ tau_(m_n) / m_n <= (q_n+q_(n-1))/(q_n-1). $
  Since $q_(n-1)<q_n$ and $q_n arrow.r infinity$, the liminf of $tau_m\/m$ is at most $2$.
]
#remark[
  This supplies the recurrence input for the balanced branch. It uses only the classical Sturmian recurrence function, not any Collatz-specific arithmetic.
]

#proposition(name: "Balanced Ordinary Landing Exclusion")[
  No non-eventually-periodic balanced infinite binary word has a nonnegative ordinary return code or a positive ordinary reduced-gap code.
]
#proof[
  First, a return code $M=0$ cannot satisfy even a one-block binary return prefix. For first digit $0$ the prefix residue is $7 mod 8$, and for first digit $1$ it is $48 mod 128$. Thus any nonnegative ordinary return code would in fact be positive.

  By the balanced mechanical normal form and the mechanical convention reduction, it is enough to consider lower mechanical words of irrational slope $alpha in (0,1)$. The Sturmian fast prefix-recurrence lemma gives
  $ liminf tau_m/m <= 2 $
  for the initial-prefix recurrence function.

  The return threshold in the fast prefix-recurrence exclusion criterion is
  $ gamma_R(alpha)=(3+4alpha)/(log_2(9\/8)+alpha log_2(27\/16)). $
  For $0<alpha<1$, this threshold is larger than $2$ because
  $ 3+4alpha > 2(log_2(9\/8)+alpha log_2(27\/16)). $
  Hence $liminf tau_m/m <= 2 < gamma_R(alpha)$, so no positive ordinary return code exists.

  The reduced-gap threshold is
  $ gamma_G(alpha)=(7+3alpha)/(log_2(243\/128)+alpha log_2(9\/8)). $
  Again $gamma_G(alpha)>2$ for $0<alpha<1$, since
  $ 7+3alpha > 2(log_2(243\/128)+alpha log_2(9\/8)). $
  The same fast prefix-recurrence criterion excludes positive ordinary reduced-gap codes.
]
#remark[
  Thus the balanced ordinary landing exclusion is closed: the exact Sturmian recurrence function contradicts the delayed-prefix-recurrence behavior forced by any balanced lower mechanical landing.
]

#proposition(name: "Binary Landing Prefix-Recurrence Height Barrier")[
  Let $r=(r_0,r_1,dots)$ be an aperiodic infinite binary return word with positive ordinary return code $M$. Put
  $ S_N=r_0+dots+r_(N-1). $
  Assume $tau_m arrow.r infinity$ and that the initial length-$m$ prefix recurs at $tau_m$, i.e.
  $ (r_(tau_m),dots,r_(tau_m+m-1))=(r_0,dots,r_(m-1)). $
  Then
  $ 3m+4S_m
     <= tau_m log_2(9\/8)+S_(tau_m) log_2(27\/16)+O(1). $

  Likewise, let $k=(k_0,k_1,dots)$ be an aperiodic infinite binary reduced-gap word with positive ordinary gap code $A$, and put
  $ K_N=k_0+dots+k_(N-1). $
  If $sigma_m$ is a positive recurrence time of the initial length-$m$ prefix and $sigma_m arrow.r infinity$, then
  $ 7m+3K_m
     <= sigma_m log_2(243\/128)+K_(sigma_m) log_2(9\/8)+O(1). $
]
#proof[
  We prove the return statement. Let $Q_m=2^(3m+4S_m)$ be the length-$m$ return prefix modulus and $R_m$ its least residue. Since $M$ realizes the infinite return code,
  $ M equiv R_m mod Q_m. $
  At a prefix recurrence time $tau_m$, the shifted suffix begins with the same length-$m$ prefix. The binary return shift-code recurrence and forced-prefix equivalence give
  $ X_(tau_m) equiv R_m mod Q_m, $
  where $X_j$ is the positive return state after $j$ return blocks. Hence
  $ X_(tau_m) equiv M mod Q_m. $

  Since $Q_m arrow.r infinity$, eventually $Q_m>M$. Since every binary return block has real expansion at least $9\/8>1$ and $tau_m arrow.r infinity$, one also has $X_(tau_m)>M$ for all large $m$. Therefore $X_(tau_m)<Q_m$ would force $X_(tau_m)=M$, impossible for all large $m$. Thus $X_(tau_m)>=Q_m$ eventually.

  The return critical-series identity gives
  $ X_j=(P_j\/Q_j)(M-M_j), $
  where $-1<=M_j<0$. Thus $M-M_j$ is bounded above and below by positive constants, and
  $ log_2 X_j
    = j log_2(9\/8)+S_j log_2(27\/16)+O(1). $
  Applying this at $j=tau_m$ and using $X_(tau_m)>=Q_m$ gives the displayed return inequality.

  The reduced-gap proof is identical. The prefix modulus is $H_m=2^(7m+3K_m)$, a prefix recurrence gives $Y_(sigma_m) equiv A mod H_m$, and the gap critical-series identity gives
  $ log_2 Y_j
    = j log_2(243\/128)+K_j log_2(9\/8)+O(1). $
  Hence $Y_(sigma_m)>=H_m$ eventually, giving the displayed gap inequality.
]
#remark[
  This is the higher-complexity replacement for the balanced recurrence contradiction. Any remaining binary ordinary landing must have prefix recurrences that are not merely delayed in time; their early symbol counts must also make the later real height large enough to clear the much larger prefix modulus.
]

#proposition(name: "Binary Density-Recurrence Exclusion Criterion")[
  Let $r$ be an aperiodic infinite binary return word, let $S_N=r_0+dots+r_(N-1)$, and suppose there are prefix recurrence times $tau_m arrow.r infinity$ along an infinite set of prefix lengths such that
  $ limsup tau_m/m <= T, quad
     liminf S_m/m >= a, quad
     limsup S_(tau_m)/tau_m <= b. $
  Under the additional strict inequality
  $ 3+4a > T (log_2(9\/8)+b log_2(27\/16)), $
  the word $r$ has no positive ordinary return code.

  Likewise, let $k$ be an aperiodic infinite binary reduced-gap word, let $K_N=k_0+dots+k_(N-1)$, and suppose there are prefix recurrence times $sigma_m arrow.r infinity$ with
  $ limsup sigma_m/m <= T, quad
     liminf K_m/m >= a, quad
     limsup K_(sigma_m)/sigma_m <= b. $
  Under the additional strict inequality
  $ 7+3a > T (log_2(243\/128)+b log_2(9\/8)), $
  the word $k$ has no positive ordinary reduced-gap code.
]
#proof[
  If a positive ordinary return code existed, the binary landing prefix-recurrence height barrier would give
  $ 3m+4S_m
     <= tau_m log_2(9\/8)+S_(tau_m) log_2(27\/16)+O(1) $
  along the chosen recurrence times. Divide by $m$ and take a subsequential limsup/liminf along the same infinite set. The hypotheses imply
  $ 3+4a <= T (log_2(9\/8)+b log_2(27\/16)), $
  contradicting the displayed strict inequality.

  The reduced-gap statement is the same argument applied to
  $ 7m+3K_m
     <= sigma_m log_2(243\/128)+K_(sigma_m) log_2(9\/8)+O(1). $
]
#remark[
  This criterion is deliberately stated in a form that can absorb higher-complexity symbolic dynamics. A future proof may attack the remaining binary obstruction by showing that every candidate class has sufficiently frequent prefix recurrences with controlled early one-density.
]

#proposition(name: "Density-Free Fast Prefix-Recurrence Exclusion")[
  Let $r$ be an aperiodic infinite binary return word. If its initial prefixes recur along an infinite sequence of lengths with recurrence times $tau_m$ satisfying
  $ limsup tau_m/m < 3 / log_2(243\/128), $
  then $r$ has no positive ordinary return code.

  Let $k$ be an aperiodic infinite binary reduced-gap word. If its initial prefixes recur along an infinite sequence of lengths with recurrence times $sigma_m$ satisfying
  $ limsup sigma_m/m < 7 / (log_2(243\/128)+log_2(9\/8)), $
  then $k$ has no positive ordinary reduced-gap code.
]
#proof[
  In the binary density-recurrence exclusion criterion, take the density-free bounds $a=0$ and $b=1$. On the return side the strict inequality becomes
  $ 3 > T(log_2(9\/8)+log_2(27\/16)) = T log_2(243\/128), $
  which is exactly $T < 3\/log_2(243\/128)$. The reduced-gap statement is identical, using the worst-case bound $b=1$ in
  $ 7 > T(log_2(243\/128)+log_2(9\/8)). $
]
#remark[
  Numerically, the return cutoff is about $3.244$ and the reduced-gap cutoff is about $6.394$. Thus any remaining binary landing must have all infinitely recurring prefix subsequences slower than these absolute ratios, unless its symbol densities make the sharper density-recurrence criterion fail.
]

#proposition(name: "Automatic Template Exclusion Examples")[
  Let $t=(t_n)_(n>=0)$ be the Thue--Morse word $t_n=s_2(n) mod 2$, where $s_2(n)$ is the binary digit sum. Let $p$ be the period-doubling word, the fixed point beginning in $0$ of the morphism $0 mapsto 01$, $1 mapsto 00$. Neither $t$ nor $p$ has a positive ordinary return code or a positive ordinary reduced-gap code.
]
#proof[
  For Thue--Morse, fix $h>=1$ and put $m=2^h$. The length-$m$ prefix recurs at shift $3 dot 2^(h-1)$. Indeed, if $0<=n<2^(h-1)$, then
  $ s_2(3 dot 2^(h-1)+n)=s_2(n)+2, $
  so the parity is unchanged. If $n=2^(h-1)+u$ with $0<=u<2^(h-1)$, then
  $ 3 dot 2^(h-1)+n=2^(h+1)+u, $
  and both binary digit sums have parity $1+s_2(u) mod 2$. Hence the prefix of length $2^h$ recurs at shift $3 dot 2^(h-1)$, with recurrence ratio $3\/2$.

  For the period-doubling word, let $phi(0)=01$ and $phi(1)=00$. The length-$2^h$ prefix is $phi^h(0)$. Since
  $ phi^(h+1)(1)=phi^h(0) phi^h(0), $
  the block $phi^h(0)$ occurs again beginning at shift $2^(h+1)$ in the fixed point. Thus the recurrence ratio is $2$ along the lengths $2^h$.

  Both ratios are below the density-free return cutoff $3\/log_2(243\/128)$ and below the density-free reduced-gap cutoff $7\/(log_2(243\/128)+log_2(9\/8))$. The density-free fast prefix-recurrence exclusion therefore rules out positive ordinary return and reduced-gap codes for both templates.
]
#remark[
  These examples show how the recurrence criteria eliminate concrete higher-complexity aperiodic templates. The remaining obstruction, if any, must avoid this kind of automatic or morphic fast prefix recurrence.
]

#proposition(name: "Binary Two-Uniform Morphic Template Exclusion")[
  Let $x$ be the fixed point beginning in $0$ of a binary $2$-uniform morphism $phi$ with $phi(0)$ beginning in $0$. Then $x$ has no positive ordinary return code and no positive ordinary reduced-gap code.
]
#proof[
  Since $phi$ is binary and $2$-uniform with $phi(0)$ beginning in $0$, either $phi(0)=00$ or $phi(0)=01$.

  If $phi(0)=00$, the fixed point beginning in $0$ is the all-zero word, hence is periodic and is excluded by the no eventually periodic binary return itinerary and reduced-gap itinerary propositions.

  Now suppose $phi(0)=01$. There are four choices for $phi(1)$. If $phi(1)=00$, the fixed point is the period-doubling word, excluded by the automatic template exclusion examples. If $phi(1)=10$, the fixed point is the Thue--Morse word, also excluded there. If $phi(1)=01$, the fixed point is $(01)^(infinity)$, periodic. If $phi(1)=11$, the iterates are $0$ followed by longer and longer blocks of $1$s after the first symbol, so the fixed point is $0 1^(infinity)$, eventually periodic. The periodic and eventually periodic cases are excluded by the periodic-itinerary propositions.
]
#remark[
  Thus the first automatic family beyond Sturmian words is also harmless. Any automatic obstruction would have to come from larger uniform morphisms or from codings that avoid fast recurring prefixes.
]

#proposition(name: "Binary Three-Uniform Morphic Template Exclusion")[
  Let $x$ be the fixed point beginning in $0$ of a binary $3$-uniform morphism $phi$ with $phi(0)$ beginning in $0$. Then $x$ has no positive ordinary return code and no positive ordinary reduced-gap code.
]
#proof[
  If $x$ is eventually periodic, the periodic-itinerary propositions already exclude it. Thus assume $x$ is aperiodic.

  Put $A_h=phi^h(0)$ and $m_h=3^h$. Since $phi(0)$ begins in $0$, there are four cases:
  $ phi(0) in {000,001,010,011}. $

  If $phi(0)=000$, then the fixed point beginning in $0$ is the all-zero word, hence periodic.

  Next suppose that a zero occurs at position $c>=1$ in the length-$9$ word $phi^2(0)$, where positions are counted from $0$. Since
  $ phi^(h+2)(0)=phi^h(phi^2(0)), $
  the prefix $A_h$ occurs again beginning at shift $c m_h$. Hence the prefix recurrence ratio is at most $c$ along all lengths $m_h$.

  If $phi(0)=001$, then one may take $c=1$. If $phi(0)=010$, take $c=2$. If $phi(0)=011$ and $phi(1)$ begins in $0$, take $c=3$. In all of these cases the density-free fast prefix-recurrence exclusion applies because
  $ c <= 3 < 3\/log_2(243\/128) < 7\/(log_2(243\/128)+log_2(9\/8)). $

  It remains to consider $phi(0)=011$ and $phi(1)$ beginning in $1$. If $phi(1)=111$, then the iterates are $0$ followed by longer and longer blocks of $1$s after the first symbol, so the fixed point is $0 1^(infinity)$, eventually periodic.

  For $phi(1)=100$, put $B_h=phi^h(1)$. Since $phi(1)$ is the symbolwise complement of $phi(0)$, the word $B_h$ is the symbolwise complement of $A_h$ for every $h$. The identity $phi^2(0)=011100100$ gives
  $ phi^(h+2)(0)=A_h B_h B_h B_h A_h A_h B_h A_h A_h, $
  so $A_h$ recurs at shift $4m_h$. If $s_h$ is the number of $1$s in $A_h$ and $d_h=s_h/m_h$, then
  $ s_(h+1)=2m_h-s_h, quad d_(h+1)=(2-d_h)\/3, $
  so $d_h arrow.r 1\/2$. The first $4m_h$ symbols are $A_h B_h B_h B_h$, hence
  $ S_(4m_h)\/(4m_h)=(s_h+3(m_h-s_h))\/(4m_h) arrow.r 1\/2. $
  The density-recurrence criterion applies with $T=4$ and $a=b=1\/2$, using the strict inequalities
  $ 5 > 4(log_2(9\/8)+(1\/2) log_2(27\/16)),
     quad 17\/2 > 4(log_2(243\/128)+(1\/2) log_2(9\/8)). $

  Finally suppose $phi(1) in {101,110}$. Both images contain exactly two $1$s, so every $h$-level superblock $phi^h(0)$ and $phi^h(1)$ has one-density $2\/3$. Also $phi^2(0)$ contains a zero after the initial position at some $c<=5$, so $A_h$ recurs at shift at most $5m_h$. The density-recurrence criterion applies with $T=5$ and $a=b=2\/3$, using the strict inequalities
  $ 17\/3 > 5(log_2(9\/8)+(2\/3) log_2(27\/16)),
     quad 9 > 5(log_2(243\/128)+(2\/3) log_2(9\/8)). $

  These cases exhaust all binary $3$-uniform morphisms prolongable on $0$, so the claimed exclusions follow.
]
#remark[
  Thus all binary $3$-uniform fixed-point templates prolongable on $0$ are harmless. The proof also shows why the density-free cutoff alone is not the final word for uniform-morphic templates: the case $phi(0)=011, phi(1)=100$ has prefix recurrence ratio $4$, above the return cutoff, but the sharper density-recurrence criterion still rules it out.
]

#proposition(name: "Binary Four-Uniform Morphic Template Exclusion")[
  Let $x$ be the fixed point beginning in $0$ of a binary $4$-uniform morphism $phi$ with $phi(0)$ beginning in $0$. Then $x$ has no positive ordinary return code and no positive ordinary reduced-gap code.
]
#proof[
  As before, the eventually periodic case is already excluded. Assume $x$ is aperiodic. Put $A_h=phi^h(0)$ and $m_h=4^h$.

  If $phi(0)$ has a zero in one of positions $1,2,3$, then $phi^2(0)$ contains a zero at that same position. Therefore $A_h$ recurs in $phi^(h+2)(0)$ at shift at most $3m_h$, and the density-free fast prefix-recurrence exclusion applies.

  It remains to consider $phi(0)=0111$. If $phi(1)=1111$, then the fixed point is $0 1^(infinity)$, which is eventually periodic. Otherwise let $j$ be the first zero-position in $phi(1)$, counted from $0$. Then $0<=j<=3$, and $phi^2(0)=phi(0) phi(1) phi(1) phi(1)$ contains the next zero at position $c=4+j<=7$. Hence $A_h$ recurs at shift $c m_h<=7m_h$.

  Let $k$ be the number of $1$s in $phi(1)$, so $0<=k<=3$. Let $a_h$ and $b_h$ be the one-densities of $phi^h(0)$ and $phi^h(1)$. Since $phi(0)=0111$ and $phi(1)$ has $k$ ones,
  $ a_(h+1)=(a_h+3b_h)\/4, quad
     b_(h+1)=((4-k)a_h+k b_h)\/4. $
  The second eigenvalue of this density recursion is $(k-3)\/4$, whose absolute value is less than $1$ for $0<=k<=3$. Thus both densities converge to
  $ p=3\/(7-k), quad 3\/7 <= p <= 3\/4. $

  The first $c m_h$ symbols before the recurring copy consist of one $A_h$ block followed by $c-1$ blocks of type $B_h=phi^h(1)$, so their one-density also tends to $p$. The density-recurrence criterion therefore applies with $T=7$ and $a=b=p$. For every $p in [3\/7,3\/4]$,
  $ 3+4p > 7(log_2(9\/8)+p log_2(27\/16)),
     quad 7+3p > 7(log_2(243\/128)+p log_2(9\/8)). $
  The two differences are linear in $p$, and direct endpoint checks at $p=3\/7$ and $p=3\/4$ are positive. Thus both ordinary landing codes are excluded.
]
#remark[
  The $4$-uniform classification shows the same mechanism persisting one level farther: fast recurrence handles the early-zero cases, while the late-zero cases are controlled by explicit symbol-density limits.
]

#proposition(name: "Binary Five-Uniform Morphic Template Exclusion")[
  Let $x$ be the fixed point beginning in $0$ of a binary $5$-uniform morphism $phi$ with $phi(0)$ beginning in $0$. Then $x$ has no positive ordinary return code and no positive ordinary reduced-gap code.
]
#proof[
  As before, the eventually periodic case is already excluded. Assume $x$ is aperiodic. Put $A_h=phi^h(0)$, $B_h=phi^h(1)$, and $m_h=5^h$.

  If $phi(0)$ has a zero in one of positions $1$, $2$, or $3$, then $A_h$ recurs in $phi^(h+1)(0)$ at shift at most $3m_h$, and the density-free fast prefix-recurrence exclusion applies.

  Thus only $phi(0)=01110$ and $phi(0)=01111$ remain. First suppose $phi(0)=01110$. Then $A_h$ recurs in
  $ phi^(h+1)(0)=A_h B_h B_h B_h A_h $
  at shift $4m_h$. Let $k$ be the number of $1$s in $phi(1)$. If $a_h$ and $b_h$ are the one-densities of $A_h$ and $B_h$, then
  $ a_(h+1)=(2a_h+3b_h)\/5, quad
     b_(h+1)=((5-k)a_h+k b_h)\/5. $
  The second eigenvalue is $(k-3)\/5$, so the densities converge to
  $ p=3\/(8-k), quad 3\/8 <= p <= 1. $
  The first $4m_h$ symbols before the recurring copy have density tending to $p$. The density-recurrence criterion applies with $T=4$ and $a=b=p$. The two displayed differences are linear in $p$, and their endpoint minima are positive:
  $ 9\/2 > 4(log_2(9\/8)+(3\/8) log_2(27\/16)),
     quad 65\/8 > 4(log_2(243\/128)+(3\/8) log_2(9\/8)). $

  Now suppose $phi(0)=01111$. If $phi(1)=11111$, then the fixed point is $0 1^(infinity)$, hence eventually periodic. Otherwise let $k<=4$ be the number of $1$s in $phi(1)$. The density recursion is
  $ a_(h+1)=(a_h+4b_h)\/5, quad
     b_(h+1)=((5-k)a_h+k b_h)\/5, $
  whose second eigenvalue is $(k-4)\/5$. Hence both densities converge to
  $ p=4\/(9-k), quad 4\/9 <= p <= 4\/5. $

  If the first zero in $phi(1)$ occurs in position $j<=3$, then $phi^2(0)$ contains the next zero at position $c=5+j<=8$. Therefore $A_h$ recurs in $phi^(h+2)(0)$ at shift $c m_h<=8m_h$, and the preceding $c m_h$ symbols have one-density tending to $p$. The density-recurrence criterion applies with $T=8$ and $a=b=p$. Again the differences are linear, with positive endpoint minima:
  $ 31\/5 > 8(log_2(9\/8)+(4\/5) log_2(27\/16)),
     quad 25\/3 > 8(log_2(243\/128)+(4\/9) log_2(9\/8)). $

  The final case is $phi(1)=11110$. Here
  $ phi^2(0)=01111 11110 11110 11110 11110 $
  contains $phi(0)=01111$ again beginning at position $9$. Applying $phi^(h-1)$ shows that, for $h>=1$, the prefix $A_h$ recurs at shift $9 dot 5^(h-1)$, with recurrence ratio $9\/5$. Since
  $ 9\/5 < 3\/log_2(243\/128)
     < 7\/(log_2(243\/128)+log_2(9\/8)), $
  the density-free fast prefix-recurrence exclusion applies.

  These cases exhaust all binary $5$-uniform morphisms prolongable on $0$.
]
#remark[
  The $5$-uniform case is the last level reached here by a short finite classification. The exceptional overlap $0 mapsto 01111$, $1 mapsto 11110$ shows why a naive "first repeated zero" bound would be too weak; the recurring prefix appears inside the next superblock and drops the ratio from $9$ to $9\/5$.
]

#proposition(name: "Binary Six-Uniform Morphic Template Exclusion")[
  Let $x$ be the fixed point beginning in $0$ of a binary $6$-uniform morphism $phi$ with $phi(0)$ beginning in $0$. Then $x$ has no positive ordinary return code and no positive ordinary reduced-gap code.
]
#proof[
  As before, assume $x$ is aperiodic and put $A_h=phi^h(0)$, $B_h=phi^h(1)$, and $m_h=6^h$. If $phi(0)$ has a zero in one of positions $1$, $2$, or $3$, then $A_h$ recurs at shift at most $3m_h$, and the density-free fast prefix-recurrence exclusion applies.

  If $phi(0)$ has a zero in position $4$ or $5$, then $A_h$ recurs at shift at most $5m_h$. Let $r$ be the number of $1$s in $phi(0)$ and $k$ the number of $1$s in $phi(1)$. Here $3<=r<=4$. The one-density recursion has common limit
  $ p = r\/(6-k+r), quad 1\/3 <= p <= 1. $
  The density-recurrence criterion applies with $T=5$ and $a=b=p$, since the linear endpoint checks
  $ 13\/3 > 5(log_2(9\/8)+(1\/3) log_2(27\/16)),
     quad 8 > 5(log_2(243\/128)+(1\/3) log_2(9\/8)) $
  are positive.

  It remains to handle $phi(0)=011111$. If $phi(1)=111111$, then the fixed point is $0 1^(infinity)$, hence eventually periodic. Otherwise let $j$ be the first zero-position in $phi(1)$ and let $k$ be the number of $1$s in $phi(1)$. The density limit is
  $ p=5\/(11-k). $

  If $j<=1$, then the prefix block $A_h$ recurs at shift at most $7m_h$. In this case $5\/11 <= p <= 5\/6$, and the density-recurrence criterion applies with $T=7$, using
  $ 19\/3 > 7(log_2(9\/8)+(5\/6) log_2(27\/16)),
     quad 92\/11 > 7(log_2(243\/128)+(5\/11) log_2(9\/8)). $

  If $j=2$ and $k<=4$, then $A_h$ recurs at shift $8m_h$, while $5\/9 <= p <= 5\/7$. The criterion applies with $T=8$, using
  $ 41\/7 > 8(log_2(9\/8)+(5\/7) log_2(27\/16)),
     quad 26\/3 > 8(log_2(243\/128)+(5\/9) log_2(9\/8)). $

  If $j=2$ and $k=5$, then $phi(1)=110111$. The symbolic prefix $01$ recurs in $phi^2(0)$ beginning at position $8$. Applying $phi^h$, the length-$2m_h$ prefix $A_h B_h$ recurs at shift $8m_h$, with ratio $4$. Since $p=5\/6$, the density-recurrence criterion applies with
  $ 19\/3 > 4(log_2(9\/8)+(5\/6) log_2(27\/16)),
     quad 19\/2 > 4(log_2(243\/128)+(5\/6) log_2(9\/8)). $

  Finally suppose $j>=3$. The symbolic prefix $01$ appears again in the repeated word $phi(1) phi(1)$ no later than the boundary between two copies of $phi(1)$, hence it occurs in $phi^2(0)$ at some position at most $11$. Thus $A_h B_h$ recurs at shift at most $11m_h$, with ratio at most $11\/2$. Here $5\/8 <= p <= 5\/6$, and the density-recurrence criterion applies because
  $ 19\/3 > (11\/2)(log_2(9\/8)+(5\/6) log_2(27\/16)),
     quad 71\/8 > (11\/2)(log_2(243\/128)+(5\/8) log_2(9\/8)). $

  These cases exhaust all binary $6$-uniform morphisms prolongable on $0$.
]
#remark[
  The $6$-uniform proof explains the earlier false boundary in the pure power-length diagnostic. Some morphisms fail the density test at lengths $6^h$, but their longer symbolic prefixes, such as $2 dot 6^h$, recur much faster and are still excluded by the same prefix-recurrence height barrier.
]

#proposition(name: "Binary Return Low-Complexity Divergence")[
  Fix $m>=1$. For a finite binary return word $w in {0,1}^L$, let $p_w(m)$ be the number of distinct length-$m$ factors appearing in $w$, with $p_w(m)=0$ when $L<m$. Let $mu_(L,m)^("low")$ be the least return-prefix residue among length-$L$ binary return words satisfying $p_w(m) <= m$. Then
  $ mu_(L,m)^("low") arrow.r infinity $
  as $L arrow.r infinity$.
]
#proof[
  Let $C_m$ be the collection of finite binary return words $w$ with $p_w(m) <= m$. This collection is prefix-closed, and it has words of every length because the all-zero word belongs to it.

  Any infinite word whose every finite prefix lies in $C_m$ has at most $m$ distinct length-$m$ factors: the finite factor sets are nested and each has size at most $m$. By the Morse-Hedlund complexity criterion, such an infinite word is eventually periodic.

  The no eventually periodic binary return itinerary proposition excludes every eventually periodic ordinary return itinerary. Applying the binary return prefix-language compactness principle to $C_m$ gives the claimed divergence.
]
#remark[
  Thus a bounded-residue obstruction in the binary return alphabet must be Sturmian-or-higher at every fixed scale: for each $m$, sufficiently long low-residue prefixes must contain at least $m+1$ distinct length-$m$ factors.
]

#proposition(name: "Binary Return Balanced-Frontier Criterion")[
  Let $mu_L^("bal")$ be the least return-prefix residue among balanced binary return words of length $L$. Then
  $ mu_L^("bal") arrow.r infinity $
  if and only if there is no non-eventually-periodic balanced infinite binary return word whose return code is a nonnegative ordinary integer.
]
#proof[
  If such an ordinary balanced code exists, its prefix residues are eventually equal to the represented integer, so $mu_L^("bal")$ cannot tend to infinity.

  Conversely, suppose $mu_L^("bal")$ does not tend to infinity. Let $C_("bal")$ be the collection of finite balanced binary return words. This class is prefix-closed and has words of every length. By the binary return prefix-language compactness principle, bounded balanced minima give an infinite binary return word whose every finite prefix is balanced and whose return code is a nonnegative ordinary integer.

  The resulting infinite word is balanced: any two of its finite factors occur together in some long enough finite prefix, and that prefix is balanced. If the infinite word were eventually periodic, it would contradict the no eventually periodic binary return itinerary proposition. Hence it is a non-eventually-periodic balanced ordinary code.
]
#remark[
  This isolates the minimal-complexity binary frontier. The later Sturmian fast prefix-recurrence argument removes this balanced aperiodic return obstruction class.
]

#proposition(name: "Binary Return Balanced Sublinear-Symbol Divergence")[
  Fix a symbol $a in {0,1}$ and a function $f: NN arrow.r NN$ with $f(n)\/n arrow.r 0$. Let $C_f^a$ be the class of balanced finite binary return words $w$ such that every length-$n$ factor of $w$ contains at most $f(n)$ occurrences of $a$. Let $mu_(f,a)(L)$ be the least return-prefix residue among words in $C_f^a$ of length $L$, when such words exist. Then
  $ mu_(f,a)(L) arrow.r infinity $
  along the lengths where it is defined.
]
#proof[
  The class $C_f^a$ is prefix-closed. If its restricted minima did not tend to infinity, the binary return prefix-language compactness principle would give an infinite binary return word $x$ whose every prefix lies in $C_f^a$ and whose return code is a nonnegative ordinary integer.

  The word $x$ is balanced, because any two finite factors occur together in a sufficiently long balanced prefix. Also, every length-$n$ factor of $x$ occurs in a sufficiently long prefix lying in $C_f^a$, so it contains at most $f(n)=o(n)$ occurrences of $a$.

  If $x$ were not eventually periodic, the balanced aperiodic positive-density lemma would force every long factor to contain linearly many occurrences of both symbols, including $a$, a contradiction. Hence $x$ is eventually periodic, contradicting the no eventually periodic binary return itinerary proposition.
]
#remark[
  Thus any hypothetical balanced return obstruction could not have density-zero windows in either symbol, even with the sparse count tending to infinity. The later Sturmian recurrence argument removes this balanced frontier entirely.
]

#proposition(name: "Bounded Return Obstruction Complexity")[
  Suppose an infinite positive-integer binary return obstruction has bounded return lengths. Let $q$ be the number of distinct return lengths appearing in its return-length word, and let $p(m)$ be its factor complexity. Then
  $ p(m) >= m+q-1 $
  for every $m>=1$.
]
#proof[
  The bounded return lengths form a finite alphabet, and the no eventually periodic binary return itinerary proposition shows that the word is not eventually periodic. The strengthened part of the Morse-Hedlund complexity criterion gives the claim.
]

#proposition(name: "Binary Return 3-adic Reset")[
  If a binary return block has length $r$ and output depth-$0$ parameter $n'$, then
  $ n' equiv (2 dot 3^(3r+1) - 85) dot 88^(-1) mod 3^(3r+2). $
  In particular, $n' equiv 2 mod 3$ for every return block.
]
#proof[
  By the return reparameterization,
  $ n' = (3 dot 27^r w - 85) / 88
       = (3^(3r+1) w - 85) / 88. $
  The same proposition gives $16^r w equiv 32 mod 33$. Reducing modulo $3$ gives $w equiv 2 mod 3$, since $16^r equiv 1 mod 3$ and $32 equiv 2 mod 3$. Therefore
  $ 3^(3r+1) w equiv 2 dot 3^(3r+1) mod 3^(3r+2). $
  Because $88$ is invertible modulo powers of $3$, division by $88$ gives the displayed congruence. Reducing it modulo $3$ gives $n' equiv -85 dot 88^(-1) equiv 2 mod 3$.
]

#remark[
  Thus a long binary return block almost resets the next return state to the fixed $3$-adic value $-85\/88$: if $r$ is large, then $n' equiv -85\/88 mod 3^(3r+1)$. This is another exact constraint, but it is still not a pointwise contradiction because the next return gate is dyadic.
]

#proposition(name: "Binary Return Reset-Spike Constraint")[
  In any infinite positive binary return orbit with states $n_j$ and return lengths $r_j$, each block satisfies
  $ n_j >= (5 dot 16^(r_j) - 32) / 33, quad
     n_(j+1) equiv -85\/88 mod 3^(3r_j+1). $
  Consequently, if the return lengths are unbounded, then along every subsequence with $r_j arrow.r infinity$ the incoming states $n_j$ tend to infinity in $RR$, while the following states $n_(j+1)$ converge to $-85\/88$ in $QQ_3$.
]
#proof[
  The real lower bound is the binary return-length height bound applied to the $j$-th block. The $3$-adic congruence follows from the binary return reset proposition after reducing its displayed congruence modulo $3^(3r_j+1)$.
]

#proposition(name: "Binary ${0,1}$ Gap 3-adic Clock")[
  In the binary return subcase where all return lengths are $0$ or $1$, suppose a return block of length $1$ is followed by $k >= 0$ return blocks of length $0$ before the next length-$1$ return. Let $n$ be the depth-$0$ return parameter immediately after the first length-$1$ block, and let $n_i$ be the parameter after the following $i$ zero-return blocks. Then
  $ v_3(n_i + 1) = 2i + 1 quad (0 <= i <= k). $
  In particular, immediately before the next length-$1$ block one has
  $ v_3(n_k + 1) = 2k + 1. $
]
#proof[
  The binary return $3$-adic reset with $r=1$ gives the output of a length-$1$ return block as
  $ n equiv (2 dot 3^4 - 85) dot 88^(-1) mod 3^5. $
  Equivalently, $n equiv 92 mod 243$, so $n+1 equiv 93 mod 243$ and therefore $v_3(n+1)=1$.

  A zero-return block has map $n'=(9n+1)\/8$, hence
  $ n' + 1 = 9(n+1)\/8. $
  Since $8$ is a $3$-adic unit, each zero-return block increases $v_3(n+1)$ by exactly $2$. Iterating gives $v_3(n_i+1)=2i+1$.
]

#remark[
  This gives a sharp clock for the first nontrivial bounded alphabet. Long gaps between length-$1$ returns force the pre-return state close to $-1$ in $QQ_3$, while each length-$1$ return resets the following state to valuation $1$. This structure still does not rule out a nonperiodic infinite gap sequence.
]

#proposition(name: "Binary ${0,1}$ Gap Map")[
  In the binary ${0,1}$ return subcase with infinitely many length-$1$ returns, let $a_j=(n_j+1)\/3$, where $n_j$ is the depth-$0$ parameter immediately after the $j$-th length-$1$ return. If the next length-$1$ return is preceded by exactly $k_j >= 0$ zero-return blocks, then
  $ a_(j+1) = (3^(2k_j+5) a_j - 8^(k_j)) / 2^(3k_j+7). $
  Equivalently,
  $ a_(j+1) = (243\/128)(9\/8)^(k_j) a_j - 1\/128. $
  In particular, $a_(j+1) > a_j$ for every positive integer state.
]
#proof[
  By the gap clock, $n_j+1=3a_j$ with $a_j$ an integer not divisible by $3$. After $k_j$ zero-return blocks,
  $ n_* + 1 = (9\/8)^(k_j)(n_j+1)
             = 3^(2k_j+1)a_j / 8^(k_j). $
  The next length-$1$ return uses $n_(j+1) = (243n_*+112)\/128$, so
  $ n_(j+1)+1
    = (243(n_*+1)-3)\/128
    = 3(3^(2k_j+5)a_j - 8^(k_j)) / 2^(3k_j+7). $
  Dividing by $3$ gives the first displayed gap map. Since $8^(k_j)=2^(3k_j)$, this is equivalently
  $ a_(j+1) = (243\/128)(9\/8)^(k_j) a_j - 1\/128. $

  For $k_j=0$,
  $ a_(j+1)-a_j = (115a_j - 1)\/128 > 0. $
  For $k_j >= 1$, the coefficient difference
  $3^(2k_j+5) - 2^(3k_j+7)$ is positive, and for $a_j >= 1$ it is larger than $8^(k_j)$. Thus $a_(j+1)>a_j$ in all cases.
]

#remark[
  The ${0,1}$ subcase has now been reduced to an expanding positive-integer gap map indexed by the zero-gap lengths $k_j$. Periodic gap sequences are impossible by the same multiplier argument as before, but arbitrary nonperiodic gap sequences remain the unresolved bounded-alphabet obstruction.
]

#proposition(name: "Binary ${0,1}$ Gap Critical Series")[
  Fix an infinite zero-gap word $(k_0,k_1,dots)$, and put
  $ alpha_j = (243\/128)(9\/8)^(k_j). $
  Define the rational partial sums
  $ L_N = 1\/128 sum_(i=0)^(N-1) 1 / (alpha_0 alpha_1 dots alpha_i). $
  These sums converge in $RR$ to a value $L_R$ satisfying
  $ 0 < L_R <= 1\/115 < 1. $
  The same rational sequence converges in $QQ_2$ to the $2$-adic gap code selected by the infinite word. More precisely, if
  $ H_N a_N = A_N a_0 - C_N $
  is the integer affine composition of the first $N$ gap maps, and $S_N$ is the least prefix residue modulo $H_N$, then
  $ L_N = C_N / A_N, quad S_N equiv L_N mod H_N. $
]
#proof[
  Write each gap step as
  $ q_j a_(j+1) = p_j a_j - c_j, $
  where
  $ p_j=3^(2k_j+5), quad q_j=2^(3k_j+7), quad c_j=8^(k_j), $
  so $alpha_j=p_j\/q_j$ and $q_j=128 c_j$. Composing the first $N$ steps gives
  $ H_N a_N = A_N a_0 - C_N $
  with $A_N=product_(j=0)^(N-1) p_j$ and $H_N=product_(j=0)^(N-1) q_j$.

  Solving the real affine recurrence
  $ a_(j+1)=alpha_j a_j - 1\/128 $
  backward from $a_N=0$ gives exactly
  $ a_0 = 1\/128 sum_(i=0)^(N-1) 1/(alpha_0 alpha_1 dots alpha_i). $
  This same value is $C_N\/A_N$ from the integer composition, so $L_N=C_N\/A_N$.

  Since every $alpha_j >= 243\/128$,
  $ 0 < L_N <= 1\/128 sum_(i=0)^(N-1) (128\/243)^(i+1) < 1\/115. $
  Hence the real limit exists and satisfies $0<L_R<=1\/115$.

  The $i$-th summand has $2$-adic valuation
  $ v_2(q_0 q_1 dots q_i) - 7, $
  because all $p_j$ are odd. These valuations tend to infinity, so the same rational series is Cauchy in $QQ_2$.

  Finally, the prefix integrality condition is
  $ A_N a_0 equiv C_N mod H_N. $
  Since $A_N$ is odd, it is invertible modulo $H_N$, and therefore
  $ S_N equiv C_N A_N^(-1) equiv C_N\/A_N = L_N mod H_N. $
  Thus the $2$-adic limit of the $L_N$ is exactly the inverse-limit gap code.
]

#remark[
  This is the adelic form of the remaining ${0,1}$ obstruction. The real critical series always lies below $1$, while the same rational partial sums may have a $2$-adic limit. For eventually periodic words that limit is a rational number below $1$, so it is immediately excluded as a positive integer. The hard case is proving that a nonperiodic word cannot make the $2$-adic limit land on a positive ordinary integer.
]

#proposition(name: "Binary ${0,1}$ Gap Ordinary-Landing Divisibility Criterion")[
  Fix an infinite zero-gap word $(k_0,k_1,dots)$ and a positive integer $A$. Let
  $ H_N a_N = A_N a_0 - C_N $
  be the integer affine composition of the first $N$ gap maps, and put $K_N=k_0+dots+k_(N-1)$, so $H_N=2^(7N+3K_N)$.
  Then $A$ is the positive ordinary gap code for this word if and only if
  $ v_2(A_N A - C_N) >= 7N + 3K_N $
  for every $N >= 1$. In that case
  $ a_N = (A_N A - C_N) / H_N $
  is the corresponding positive gap orbit.
]
#proof[
  If $A$ is the ordinary gap code, each composed gap-prefix map is integral at $A$, so $H_N$ divides $A_N A-C_N$. Since $H_N=2^(7N+3K_N)$, this is the displayed valuation inequality.

  Conversely, suppose the divisibility holds for every $N$. Define
  $ a_N=(A_N A-C_N)\/H_N. $
  The critical-series proposition gives $C_N\/A_N<1$, while $A>=1$, so $A_N A-C_N>0$. Thus every $a_N$ is a positive integer.

  For one more gap, write $p_N=3^(2k_N+5)$, $q_N=2^(3k_N+7)$, and $c_N=8^(k_N)$. The affine composition recurrences are
  $ A_(N+1)=p_N A_N, quad H_(N+1)=q_N H_N, quad C_(N+1)=p_N C_N+c_N H_N. $
  Hence
  $ A_(N+1) A-C_(N+1)
     = H_N(p_N a_N-c_N). $
  Divisibility by $H_(N+1)=q_N H_N$ gives
  $ q_N | p_N a_N-c_N, $
  and therefore
  $ a_(N+1)=(p_N a_N-c_N)\/q_N $
  is exactly the next gap-map step. Thus $A$ realizes every prefix and is the ordinary gap code.
]

#proposition(name: "Binary ${0,1}$ Gap Ordinary Itinerary Uniqueness")[
  For a fixed positive normalized state $a_0$, there is at most one infinite ${0,1}$ zero-gap word for which $a_0$ is the ordinary gap code.
]
#proof[
  The gap partial map reads the next zero-gap length from $a_0=8^k b$: if a complete gap transition exists, then $k=v_2(a_0)\/3$ is uniquely determined, and the next normalized state is uniquely
  $ a_1=(3^(2k+5)b-1)\/128. $
  Thus the first gap length and next state are forced by $a_0$. Iterating gives at most one infinite zero-gap word.
]

#proposition(name: "Binary ${0,1}$ Gap Forced-Orbit Prefix Equivalence")[
  Fix a positive normalized state $A$. The ${0,1}$ gap partial map is defined for the first $L$ forced complete gap transitions, with forced word $(k_0,dots,k_(L-1))$, if and only if $A$ satisfies every prefix congruence
  $ A equiv S_N mod H_N quad (1 <= N <= L), $
  where $S_N$ is the least residue of the length-$N$ gap prefix $(k_0,dots,k_(N-1))$. In particular, once $H_N>A$, this congruence is equivalent to $S_N=A$.
]
#proof[
  If the forced gap orbit exists for $L$ complete gap transitions, then composing those gap maps gives
  $ H_N a_N = A_N A - C_N $
  for every $1 <= N <= L$. Thus
  $ A_N A - C_N equiv 0 mod H_N, $
  which is exactly the prefix congruence $A equiv S_N mod H_N$ because $A_N$ is odd and invertible modulo $H_N$.

  Conversely, if these prefix congruences hold, then the ordinary-landing divisibility criterion applied to each finite prefix constructs positive integer states $a_1,dots,a_L$ and shows that each forced gap transition is defined. The gap word is unique by the ordinary itinerary uniqueness proposition.

  Finally, if $H_N>A$ and $A equiv S_N mod H_N$ with $0 <= S_N < H_N$, then the congruence is equivalent to $S_N=A$ as ordinary integers.
]

#proposition(name: "Binary ${0,1}$ Gap Landing Growth Envelope")[
  Suppose an infinite zero-gap word $(k_0,k_1,dots)$ has positive ordinary gap code $a_0=A$. Put
  $ K_N = k_0 + dots + k_(N-1). $
  Then the state $a_N$ after the first $N$ complete gap transitions satisfies
  $ a_N = (A_N\/H_N)(A - L_N), $
  where $L_N$ is the gap critical-series partial sum. In particular,
  $ a_N <= A(243\/128)^N(9\/8)^(K_N). $
  If the next zero-gap length is $k_N$, then
  $ 8^(k_N) <= A(243\/128)^N(9\/8)^(K_N). $
]
#proof[
  From the finite gap composition,
  $ H_N a_N = A_N A - C_N. $
  Since $L_N=C_N\/A_N$, this gives
  $ a_N=(A_N\/H_N)(A-L_N). $
  The critical-series proposition gives $L_N>=0$, so $A-L_N<=A$. Also
  $ A_N\/H_N = product_(j=0)^(N-1) 3^(2k_j+5) / 2^(3k_j+7)
    = (243\/128)^N (9\/8)^(K_N). $
  This proves the bound for $a_N$.

  If the next gap is $k_N$, the gap partial map requires $a_N=8^(k_N)b$ with $b$ a positive odd integer. Hence $8^(k_N) <= a_N$. Combining this with the upper bound above gives the envelope.
]

#remark[
  As with the return-code envelope, this rules out gap words with gaps too large relative to their previous cumulative gap total and the fixed landing integer. It still leaves the difficult balanced nonperiodic case.
]

#proposition(name: "Binary ${0,1}$ Gap Spike Exclusion")[
  Let $(k_0,k_1,dots)$ be an infinite zero-gap word and put $K_N=k_0+dots+k_(N-1)$. If
  $ sup_N 8^(k_N) / ((243\/128)^N(9\/8)^(K_N)) = infinity, $
  then this word has no positive ordinary gap code.
]
#proof[
  If the word had positive ordinary gap code $A$, the gap landing growth envelope would give
  $ 8^(k_N) <= A(243\/128)^N(9\/8)^(K_N) $
  for every $N$. Dividing by the denominator gives a uniform upper bound $A$, contradicting the assumed unboundedness.
]

#proposition(name: "Periodic ${0,1}$ Gap Branch")[
  Let $w=(k_0,dots,k_(p-1))$ be a nonempty finite zero-gap word, and write its one-period affine data as
  $ H_w a_p = A_w a_0 - C_w. $
  For $L>=1$, let $w^L$ denote $L$ repetitions of $w$. A positive normalized state $a_0$ realizes the gap word $w^L$ if and only if
  $ a_0 equiv a_w^* mod H_w^L, quad
     a_w^* = C_w / (A_w - H_w), $
  equivalently
  $ (A_w-H_w)a_0 equiv C_w mod H_w^L. $
  The infinite periodic gap code selected by $w w w dots$ is $a_w^*$, and $0<a_w^*<1$.
]
#proof[
  Each gap map has real multiplier greater than $1$, so $A_w>H_w$. Also $C_w>0$, and the period map
  $ G_w(a)=(A_w a-C_w)\/H_w $
  has the fixed point
  $ a_w^*=C_w\/(A_w-H_w). $
  Since every single gap map sends $1$ to a value greater than $1$ and is increasing, the period map satisfies $G_w(1)>1$. Thus
  $ (A_w-C_w)\/H_w > 1, $
  so $C_w < A_w-H_w$ and therefore $0<a_w^*<1$.

  Iterating the period map $L$ times gives
  $ H_w^L a_(p L)
      = A_w^L a_0
        - C_w (A_w^L-H_w^L)/(A_w-H_w). $
  Since
  $ A_w^L a_w^*
      - C_w (A_w^L-H_w^L)/(A_w-H_w)
      = C_w H_w^L/(A_w-H_w), $
  and $A_w-H_w$ is odd, the divisibility condition modulo $H_w^L$ is equivalent to
  $ A_w^L (a_0-a_w^*) equiv 0 mod H_w^L. $
  The coefficient $A_w^L$ is odd, hence invertible modulo $H_w^L$, so this is equivalent to $a_0 equiv a_w^* mod H_w^L$. For $L=1$ this is exactly the finite-word residue class of $w$, and the same calculation for $w^L$ gives the stated finite-shadow criterion.
]

#proposition(name: "No Eventually Periodic ${0,1}$ Gap Itinerary")[
  No positive-integer orbit of the ${0,1}$ gap map can have an eventually periodic zero-gap sequence.
]
#proof[
  If a positive orbit had an eventually periodic gap itinerary, discard the finite preperiod and let $w$ be the repeating zero-gap word of the remaining positive tail. The periodic gap branch proposition shows that the starting state of this tail would have to equal the rational periodic code $a_w^*$, which lies strictly between $0$ and $1$. This is impossible for a positive integer.
]

#proposition(name: "Bounded ${0,1}$ Gap Obstruction Complexity")[
  Suppose an infinite positive-integer reduced ${0,1}$ gap obstruction has bounded zero-gap lengths. Let $q$ be the number of distinct zero-gap lengths appearing in its gap word, and let $p(m)$ be its factor complexity. Then
  $ p(m) >= m+q-1 $
  for every $m>=1$.
]
#proof[
  The bounded zero-gap lengths form a finite alphabet, and the no eventually periodic ${0,1}$ gap itinerary proposition shows that the word is not eventually periodic. The strengthened part of the Morse-Hedlund complexity criterion gives the claim.
]

#proposition(name: "All-Zero ${0,1}$ Gap Branch")[
  A normalized state $a_0$ has first $L$ zero-gap lengths all equal to $0$ if and only if
  $ a_0 equiv 1\/115 mod 128^L, $
  equivalently
  $ 115 a_0 equiv 1 mod 128^L. $
  The infinite all-zero gap code is the $2$-adic rational $a_0=1\/115$, not a positive integer.
]
#proof[
  On a zero-gap step,
  $ a_(i+1) = (243a_i - 1)\/128. $
  The fixed point is $a_* = 1\/115$. A zero-gap step is admissible exactly when $243a_i-1$ is divisible by $128$, i.e.
  $ a_i equiv 243^(-1) equiv 1\/115 mod 128. $
  Also
  $ a_i - a_* = (243\/128)^i (a_0-a_*). $
  Thus the condition $a_i equiv a_* mod 128$ for every $0 <= i < L$ is equivalent to
  $ a_0 equiv a_* mod 128^L. $
  Taking $L arrow.r infinity$ gives the unique $2$-adic code $a_0=1\/115$, which is rational but not an integer.
]

#proposition(name: "Constant ${0,1}$ Gap Branch")[
  Fix $k >= 0$ and put
  $ A_k = 3^(2k+5), quad Q_k = 2^(3k+7), quad B_k = 8^k. $
  A normalized state $a_0$ has first $L$ zero-gap lengths all equal to $k$ if and only if
  $ a_0 equiv B_k / (A_k - Q_k) mod Q_k^L, $
  equivalently
  $ (A_k - Q_k)a_0 equiv B_k mod Q_k^L. $
  The infinite constant-$k$ gap code is the rational
  $ a_* = B_k / (A_k - Q_k), $
  which satisfies $0 < a_* < 1$ and hence is not a positive integer.
]
#proof[
  For fixed $k$, the gap map is
  $ f_k(a) = (A_k a - B_k) / Q_k. $
  Its fixed point is
  $ a_* = B_k / (A_k - Q_k). $
  Since
  $ A_k - Q_k = 8^k (243(9\/8)^k - 128) > 8^k = B_k, $
  the fixed point lies strictly between $0$ and $1$.

  The denominator $A_k-Q_k$ is odd, so $a_*$ is a valid $2$-adic residue. Also
  $ a_i - a_* = (A_k\/Q_k)^i (a_0-a_*) $
  along a constant-$k$ branch. Since $A_k$ is odd, requiring the $k$-gap divisibility condition for $0 <= i < L$ is equivalent to
  $ a_0 equiv a_* mod Q_k^L. $
  Written without rational residues, this is
  $ (A_k-Q_k)a_0 equiv B_k mod Q_k^L. $
]

#proposition(name: "Binary ${0,1}$ Gap Partial Map")[
  In the notation of the preceding proposition, a gap of exactly $k >= 0$ zeros occurs after a length-$1$ return if and only if
  $ a = 8^k b $
  where $b$ is odd and
  $ 3 dot 9^k b equiv 49 mod 128. $
  In that case the next post-length-$1$ normalized state is
  $ a' = (3^(2k+5)b - 1) / 128. $
]

#proof[
  After $i$ zero-return blocks,
  $ n_i + 1 = 3 dot 9^i a / 8^i. $
  Thus the first $k$ blocks are zeros precisely when $8^k | a$. Write $a=8^k b$. The state before the next length-$1$ return is
  $ n_k = 3 dot 9^k b - 1. $
  A length-$1$ return has gate $n_k equiv 48 mod 128$, so
  $ 3 dot 9^k b equiv 49 mod 128. $
  This congruence forces $b$ to be odd, so the gap length is exactly $k$. Substituting $a=8^k b$ into the gap map gives
  $ a' = (3^(2k+5)b - 1) / 128. $
]

#proposition(name: "Binary ${0,1}$ Gap Partial-Map Equivalence")[
  A positive-integer obstruction in the ${0,1}$ gap system is exactly an infinite positive orbit of the partial map
  $ a = 8^k b, quad 3 dot 9^k b equiv 49 mod 128
     arrow.r (3^(2k+5)b - 1)\/128. $
  Consequently, proving that this partial map has no infinite positive orbit settles the ${0,1}$ return-length subcase.
]
#proof[
  The preceding partial-map proposition shows that every complete gap-to-length-$1$ transition is exactly one application of this map, with the gap length $k$ uniquely recovered as $v_2(a)\/3$. Therefore an infinite positive ${0,1}$ gap obstruction gives an infinite positive orbit of the partial map.

  Conversely, each infinite positive orbit of the partial map reconstructs consecutive zero gaps followed by length-$1$ returns in the binary return system. Thus the two formulations are equivalent.
]

#proposition(name: "Binary ${0,1}$ Gap Backward Branch Formula")[
  Fix a terminal normalized state $a'$ and a gap length $k >= 0$. A positive state $a$ maps to $a'$ through a complete ${0,1}$ gap transition of length $k$ if and only if
  $ a = (2^(3k+7) a' + 8^k) / 3^(2k+5) $
  is a positive integer. In particular, for fixed $a'$ and $k$ there is at most one backward preimage.
]
#proof[
  The forward gap map has the affine form
  $ a' = (3^(2k+5)a - 8^k) / 2^(3k+7). $
  Solving for $a$ gives the displayed formula, so any forward preimage must have this value.

  Conversely, suppose the displayed value is a positive integer. Then
  $ 3^(2k+5)a - 8^k = 2^(3k+7)a'. $
  Since $8^k$ divides the right side and the subtracted term, $a=8^k b$ for an integer $b$. Dividing by $8^k$ gives
  $ 3^(2k+5)b - 1 = 128 a'. $
  Reducing modulo $128$ and using $3^(2k+5)=81 dot 3 dot 9^k$ with $81^(-1) equiv 49 mod 128$ gives
  $ 3 dot 9^k b equiv 49 mod 128. $
  Thus the gap partial-map gate holds, and applying it gives terminal state $a'$.
]

#proposition(name: "Binary ${0,1}$ Gap Backward 3-adic Gate")[
  For fixed terminal normalized state $a'$, a backward gap branch of length $k$ exists if and only if
  $ 3^(2k+5) divides 128a' + 1. $
  Hence the number of backward gap branches into $a'$ is
  $ max(0, floor((v_3(128a'+1)-5)\/2) + 1). $
]
#proof[
  The backward branch formula can be rewritten as
  $ a = 8^k (128a' + 1) / 3^(2k+5). $
  Therefore $a$ is an integer if and only if $3^(2k+5)$ divides $128a'+1$. When this divisibility holds, $a$ is positive. Writing $a=8^k b$, the identity becomes
  $3^(2k+5)b=128a'+1$, which is the gate congruence used in the previous proof.

  Thus the admissible gap lengths are exactly the integers $k >= 0$ such that $2k+5 <= v_3(128a'+1)$. Counting them gives the displayed formula, with zero branches when $v_3(128a'+1)<5$.
]

#proposition(name: "Binary ${0,1}$ Gap Backward Merge Chain")[
  Fix a terminal normalized state $a'$ and suppose it has backward gap branches. Put
  $K = floor((v_3(128a'+1)-5)\/2).$
  Then its complete set of backward preimages is
  $ a_k = 8^k (128a'+1) / 3^(2k+5) quad (0 <= k <= K). $
  Consecutive preimages satisfy
  $ a_(k+1) = (8\/9) a_k. $
  Hence all immediate forward merges in the reduced gap map are finite geometric chains with ratio $8\/9$.
]
#proof[
  The backward $3$-adic gate gives exactly the admissible gap lengths $0 <= k <= K$, and the backward branch formula gives the displayed $a_k$. For consecutive values,
  $ a_(k+1) / a_k
    = (8^(k+1) / 3^(2k+7)) (3^(2k+5) / 8^k)
    = 8\/9. $
]

#proposition(name: "Binary ${0,1}$ Gap Backward Merge Bounds")[
  For a terminal normalized state $a'$, let $M(a')$ be the number of immediate backward gap preimages. Then
  $ M(a') <= max(0, (log_3(128a'+1)-3)\/2). $
  Moreover, the sum of all immediate backward preimages satisfies
  $ sum_(a: T_G(a)=a') a <= (128a'+1)\/27 <= (43\/9)a'. $
]
#proof[
  The exact branch-count formula gives
  $ M(a') = max(0, floor((v_3(128a'+1)-5)\/2)+1). $
  Since $v_3(128a'+1) <= log_3(128a'+1)$, the stated logarithmic bound follows when $M(a')>0$; when $M(a')=0$ it is trivial.

  If there are preimages, the merge-chain formula gives
  $ a_k = ((128a'+1)\/243)(8\/9)^k. $
  Summing over the finite chain and extending to the infinite geometric series gives
  $ sum_(a: T_G(a)=a') a
     <= ((128a'+1)\/243) sum_(k=0)^infinity (8\/9)^k
     = (128a'+1)\/27. $
  Since $a' >= 1$, $128a'+1 <= 129a'$, giving the final bound.
]

#proposition(name: "Binary ${0,1}$ Gap Backward Length Bound")[
  If a terminal normalized state $a'$ has a backward preimage through a gap of length $k$, then
  $ (9\/8)^k <= (128a' + 1) / 243. $
  Hence the possible backward gap lengths into a fixed terminal state are logarithmically bounded in $a'$.
]
#proof[
  By the backward branch formula, a positive preimage requires
  $ 2^(3k+7)a' + 8^k >= 3^(2k+5). $
  Dividing by $8^k$ gives
  $ 128a' + 1 >= 243(9\/8)^k, $
  which is the displayed inequality.
]

#proposition(name: "Binary ${0,1}$ Gap Backward Contraction")[
  If $a$ maps to $a'$ through a complete ${0,1}$ gap transition of length $k$, then
  $ a <= (43\/81)(8\/9)^k a'. $
  In particular, every valid positive backward gap branch strictly decreases height.
]
#proof[
  The backward branch formula gives
  $ a = ((128a' + 1) / 243) (8\/9)^k. $
  Since $a' >= 1$, we have $128a'+1 <= 129a'$, hence
  $ a <= (129\/243)(8\/9)^k a'
      = (43\/81)(8\/9)^k a'. $
  The factor on the right is at most $43\/81<1$, so every positive backward gap branch strictly decreases height.
]

#proposition(name: "Binary ${0,1}$ Gap Backward Path Contraction")[
  If a depth-$L$ backward gap path has gap word $(k_0,dots,k_(L-1))$ and total gap length
  $ K_L = k_0 + dots + k_(L-1), $
  then its initial state $a_0$ and terminal state $a_L$ satisfy
  $ a_0 <= (43\/81)^L (8\/9)^(K_L) a_L. $
]
#proof[
  Apply the backward gap contraction proposition to each branch and multiply the resulting inequalities.
]

#proposition(name: "Binary ${0,1}$ Gap Terminal Escape")[
  If a positive state $a_0$ survives $L$ complete gap transitions with gap word $(k_0,dots,k_(L-1))$, total zero-gap length $K_L$, and terminal state $a_L$, then
  $ a_L >= (81\/43)^L (9\/8)^(K_L) a_0. $
]
#proof[
  This is the backward gap path contraction inequality rearranged.
]

#proposition(name: "Binary ${0,1}$ Gap Terminal Window")[
  For a finite gap word $w$ of length $L$, let
  $ E_w = A_w\/H_w = (243\/128)^L (9\/8)^(K_w), $
  let $L_w=C_w\/A_w$ be its gap critical-series partial sum, let $S_w$ be its least prefix residue, and let
  $ u_w = (A_w S_w - C_w)\/H_w $
  be the terminal state reached from $S_w$. Then
  $ u_w = E_w(S_w-L_w), quad S_w - 1\/115 < u_w\/E_w < S_w. $
  In particular,
  $ S_w = ceil(u_w\/E_w). $
  Consequently,
  $ S_w <= B quad ==> quad u_w < E_w B. $
]
#proof[
  The finite gap composition gives
  $ H_w u_w = A_w S_w - C_w. $
  Since $L_w=C_w\/A_w$, this is
  $ u_w = (A_w\/H_w)(S_w-L_w)=E_w(S_w-L_w). $
  The gap critical-series proposition gives $0<L_w<1\/115$, hence
  $ S_w-1\/115 < S_w-L_w < S_w. $
  Since $S_w$ is an integer, this gives $S_w=ceil(u_w\/E_w)$.
  The terminal-window implication follows immediately.
]

#proposition(name: "Binary ${0,1}$ Gap Terminal Depth Bound")[
  If a gap word $w$ has length $L$ and terminal state $u_w$, then
  $ u_w > (114\/115) E_w >= (114\/115)(243\/128)^L. $
  Consequently,
  $ L < log_(243\/128)((115\/114)u_w). $
]
#proof[
  The least gap-prefix residue satisfies $S_w >= 1$. The gap terminal-window proposition gives
  $ u_w/E_w > S_w - 1\/115 >= 114\/115. $
  Also every gap block has expansion at least $243\/128$, so $E_w >= (243\/128)^L$. The displayed depth bound follows by rearranging and taking logarithms.
]

#proposition(name: "Binary ${0,1}$ Gap Terminal-Window Counting Equivalence")[
  With the notation of the previous proposition,
  $ S_w <= B $
  if and only if
  $ u_w / E_w < B. $
  Consequently, $N_G(B,L)$ is exactly the number of length-$L$ gap words satisfying $u_w/E_w < B$.
]
#proof[
  If $S_w <= B$, the terminal-window proposition gives $u_w/E_w < S_w <= B$. Conversely, if $u_w/E_w < B$, then the same proposition gives
  $ S_w < u_w/E_w + 1\/115 < B + 1. $
  Since $S_w$ and $B$ are integers, this implies $S_w <= B$.
]

#proposition(name: "Binary ${0,1}$ Gap Expansion Pressure")[
  For every $theta > 0$ and every length $L$,
  $ sum_(w: |w|=L) E_w^(-theta)
     = (((128\/243)^theta) / (1 - (8\/9)^theta))^L, $
  where $E_w=(243\/128)^L(9\/8)^(sum_j k_j)$ is the gap expansion factor of $w=(k_0,dots,k_(L-1))$.

  This pressure decays exponentially in $L$ exactly when
  $ (128\/243)^theta + (8\/9)^theta < 1. $
  The threshold root is $theta_G approx 2.26483$; in particular, cubic pressure decays.
]
#proof[
  A one-block gap label $k$ has expansion
  $ E_k = (243\/128)(9\/8)^k. $
  Hence
  $ sum_(k=0)^infinity E_k^(-theta)
    = (128\/243)^theta sum_(k=0)^infinity (8\/9)^(theta k)
    = ((128\/243)^theta) / (1 - (8\/9)^theta). $
  Since the expansion factor of a word is the product of its one-block expansion factors, the length-$L$ sum factorizes as the $L$-th power of the one-step sum.

  The base is less than $1$ exactly when
  $ (128\/243)^theta < 1 - (8\/9)^theta, $
  which is the displayed condition. For $theta=3$,
  $ (128\/243)^3 + (8\/9)^3 < (43\/81)^3 + (8\/9)^3 < 1 $
  by the cubic gap moment contraction estimate.
]

#proposition(name: "Binary ${0,1}$ Gap Weighted Terminal-Window Bound")[
  For every $theta > 2$, every $B >= 1$, and every $L >= 1$,
  $ sum_(w: |w|=L, S_w <= B) E_w^(-theta)
     <= B^theta (43\/81)^L zeta(theta - 1). $
]
#proof[
  Fix a terminal state $u$ and let $m_L(u)$ be the number of length-$L$ gap words landing at $u$ from their least prefix residues. Distinct such words have distinct positive initial states, since the reduced gap partial map is deterministic forward. By the backward gap path contraction proposition, each such initial state $S_w$ satisfies
  $ S_w <= (43\/81)^L (8\/9)^(K_w) u <= (43\/81)^L u. $
  Hence $m_L(u) <= floor((43\/81)^L u) <= (43\/81)^L u$.

  If $S_w <= B$, the gap terminal-window proposition gives $u_w < E_w B$, so
  $ E_w^(-theta) < B^theta u_w^(-theta). $
  Grouping words by terminal state,
  $ sum_(w: |w|=L, S_w <= B) E_w^(-theta)
    <= B^theta sum_(u=1)^infinity m_L(u) u^(-theta)
    <= B^theta (43\/81)^L sum_(u=1)^infinity u^(1-theta). $
  Since $theta>2$, the final sum is $zeta(theta-1)$.
]
#remark[
  This weighted bound includes the reduced gap map's forward merging. It is still not an unweighted rank estimate: converting it into a count would require controlling the high-expansion words whose inverse-expansion weights are tiny.
]

#proposition(name: "Binary ${0,1}$ Gap Weighted Expansion-Shell Count")[
  Let $W_G(B,L;s)$ count length-$L$ gap words satisfying $S_w <= B$ and
  $ 2^s <= E_w < 2^(s+1). $
  For every $theta > 2$,
  $ W_G(B,L;s) <= 2^(theta(s+1)) B^theta (43\/81)^L zeta(theta-1). $
]
#proof[
  On the shell $E_w < 2^(s+1)$, each word satisfies
  $ E_w^(-theta) > 2^(-theta(s+1)). $
  Therefore
  $ W_G(B,L;s) dot 2^(-theta(s+1))
     <= sum_(w: |w|=L, S_w <= B) E_w^(-theta). $
  Apply the gap weighted terminal-window bound and multiply by $2^(theta(s+1))$.
]
#remark[
  This shell estimate includes gap merge multiplicity through the weighted terminal-window bound. Like the return analogue, it is useful only when the shell index is controlled; it does not by itself give the natural-rate rank theorem.
]

#proposition(name: "Binary ${0,1}$ Gap Expansion-Shell Depth Bound")[
  If a length-$L$ gap word satisfies
  $ 2^s <= E_w < 2^(s+1), $
  then
  $ L < log_(243\/128)(2^(s+1)). $
]
#proof[
  Every reduced gap block has expansion at least $243\/128$, so $E_w >= (243\/128)^L$. Combining this with $E_w < 2^(s+1)$ gives
  $ (243\/128)^L < 2^(s+1), $
  and taking logarithms gives the displayed bound.
]
#remark[
  Fixed reduced-gap expansion shells only occur at bounded prefix depths. Hence the infinite reduced-gap obstruction, if it exists, must eventually live in arbitrarily high expansion shells.
]

#proposition(name: "Binary ${0,1}$ Gap Low-Expansion Distinct-Terminal Count")[
  Let $D_G(B,L;X)$ be the number of distinct terminal states $u_w$ arising from length-$L$ gap words with $S_w <= B$ and $E_w <= X$. Then
  $ D_G(B,L;X) <= floor(X B). $
]
#proof[
  If $S_w <= B$, the gap terminal-window proposition gives $u_w < E_w B$. If also $E_w <= X$, then $u_w < X B$. Since $u_w$ is a positive integer, there are at most $floor(X B)$ possible distinct terminal states.
]
#remark[
  This is a distinct-terminal bound, not a word-count bound. The reduced gap map has forward merging, so several gap words can share the same terminal state. Thus the remaining gap counting problem includes a genuine multiplicity component absent from the return system.
]

#proposition(name: "Binary ${0,1}$ Gap Low-Expansion Window Count with Multiplicity")[
  Let $N_G(B,L;X)$ count length-$L$ gap words satisfying $S_w <= B$ and $E_w <= X$, where $B >= 1$, $L >= 1$, and $X >= 1$. Put
  $ M = ceil(X B) - 1. $
  Then
  $ N_G(B,L;X) <= sum_(u=1)^M floor((43\/81)^L u)
     <= (43\/81)^L M(M+1) / 2. $
]
#proof[
  The gap terminal-window proposition gives $u_w < E_w B <= X B$. Hence every terminal state counted by $N_G(B,L;X)$ lies among the integers $1 <= u <= M$.

  Fix such a terminal value $u$. Every length-$L$ word landing at $u$ has a distinct positive initial state $S_w$, because the reduced gap partial map is deterministic forward. The backward path contraction proposition gives
  $ S_w <= (43\/81)^L (8\/9)^(K_w) u <= (43\/81)^L u. $
  Therefore at most $floor((43\/81)^L u)$ length-$L$ words can land at this terminal value. Summing over all possible $u <= M$ gives the first bound, and bounding the floors by their arguments gives the second.
]
#remark[
  This is an ordinary word-count bound for the low-expansion part of the reduced gap low window, but it is quadratic in the terminal cutoff. The desired gap rank theorem needs a linear-in-$B$ estimate at the natural rate, so the high-expansion and multiplicity problems remain open.
]

#proposition(name: "Binary ${0,1}$ Gap Backward Cubic-Mass Contraction")[
  For every terminal gap state $a'$,
  $ sum_(a: T_G(a)=a') a^3
     <= ((43\/81)^3)/(1-(8\/9)^3) (a')^3
     = (43^3)/(729 dot 217) (a')^3
     < (a')^3. $
]
#proof[
  If there are no backward preimages, the sum is zero. Otherwise the backward merge-chain proposition writes them as
  $ a_k = a_0 (8\/9)^k, quad 0 <= k <= K. $
  By the backward contraction proposition, $a_0 <= (43\/81)a'$. Therefore
  $ sum_(a: T_G(a)=a') a^3
     <= ((43\/81)^3)(a')^3 sum_(k=0)^K (8\/9)^(3k). $
  Extending to the infinite geometric series gives
  $ sum_(k=0)^infinity (8\/9)^(3k)
     = 1/(1-(8\/9)^3). $
  The exact constant simplifies to $43^3/(729 dot 217)$, which is less than $1$.
]

#proposition(name: "Binary ${0,1}$ Gap Backward Moment Contraction")[
  For every real $theta > 0$ and every terminal gap state $a'$,
  $ sum_(a: T_G(a)=a') a^theta
     <= ((43\/81)^theta)/(1-(8\/9)^theta) (a')^theta. $
  In particular, this is a strict moment contraction whenever
  $ (43\/81)^theta + (8\/9)^theta < 1. $
]
#proof[
  If there are no preimages, the sum is zero. Otherwise the merge-chain proposition gives
  $ a_k = a_0 (8\/9)^k, quad 0 <= k <= K, $
  and the backward contraction proposition gives $a_0 <= (43\/81)a'$. Therefore
  $ sum_(a: T_G(a)=a') a^theta
     <= ((43\/81)^theta)(a')^theta sum_(k=0)^K (8\/9)^(theta k). $
  Extending to the infinite geometric series gives the displayed bound. The multiplicative constant is less than $1$ exactly when
  $ (43\/81)^theta < 1 - (8\/9)^theta, $
  which is the stated condition.
]

#proposition(name: "Finite ${0,1}$ Gap Words Are Realizable")[
  For every finite sequence of zero-gap lengths $(k_0, dots, k_(L-1))$, there are infinitely many positive normalized states $a_0$ whose ${0,1}$ gap itinerary begins with exactly this sequence.
]
#proof[
  For a fixed gap length $k$, the gap partial map imposes one congruence class on $a$ modulo $2^(3k+7)$, because the coefficient $3^(2k+5)$ in
  $ a' = (3^(2k+5)a - 8^k) / 2^(3k+7) $
  is odd. Pulling back a suffix congruence through one more gap map again gives one congruence class, with the modulus multiplied by $2^(3k+7)$.

  Iterating over the finite word gives one residue class modulo
  $ product_(j=0)^(L-1) 2^(3k_j+7). $
  Every positive integer in this residue class realizes the prescribed finite gap sequence, and the arithmetic progression contains infinitely many positive values.
]

#remark[
  Thus the ${0,1}$ gap system also cannot be settled by finding a forbidden finite gap pattern. Its obstruction, if any, is necessarily an infinite nonperiodic coding phenomenon.
]

#proposition(name: "Binary ${0,1}$ Gap-Code Boundedness Criterion")[
  Fix an infinite zero-gap word $(k_0, k_1, dots)$, and let $S_N$ be the least nonnegative residue of its length-$N$ gap-prefix code modulo
  $ H_N = product_(j=0)^(N-1) 2^(3k_j+7). $
  The corresponding ${0,1}$ gap code is a nonnegative ordinary integer if and only if the sequence $S_N$ is bounded. Equivalently, this happens if and only if $S_N$ is eventually constant.
]
#proof[
  For a finite gap prefix, composing
  $ 2^(3k_j+7) a_(j+1) = 3^(2k_j+5)a_j - 8^(k_j) $
  gives
  $ H_N a_N = A_N a_0 - C_N, $
  where $A_N$ is odd. Therefore $a_0$ must lie in one residue class
  $ S_N equiv C_N A_N^(-1) mod H_N. $
  These residue classes are nested as $N$ increases.

  If the inverse-limit code is a nonnegative ordinary integer $M$, then $S_N equiv M mod H_N$ for all $N$. Since $H_N arrow.r infinity$, for all sufficiently large $N$ one has $S_N=M$. Thus $S_N$ is eventually constant.

  Conversely, if $S_N$ is bounded, say $S_N <= C$ for every $N$, then for $M>N$ with $H_N>C$, the nesting relation $S_M equiv S_N mod H_N$ forces $S_M=S_N$ as ordinary integers. Hence the sequence is eventually constant. The eventual constant satisfies every finite prefix congruence and is therefore exactly the ordinary integer represented by the gap code.
]

#remark[
  This is the exact remaining ${0,1}$ target: prove that every non-eventually-periodic infinite gap word has unbounded gap-prefix residues.
]

#proposition(name: "Binary ${0,1}$ Gap-Prefix Monotonicity")[
  For a fixed infinite gap word, the least nonnegative prefix residues $S_N$ satisfy
  $ S_(N+1) = S_N + d_N H_N $
  for some integer
  $ 0 <= d_N < 2^(3k_N+7). $
  Hence $S_N$ is nondecreasing. It is bounded if and only if $d_N=0$ for all sufficiently large $N$.
]
#proof[
  The length-$(N+1)$ prefix class reduces to the length-$N$ prefix class modulo $H_N$. Since
  $H_(N+1)=H_N 2^(3k_N+7)$,
  the least nonnegative representative has the form
  $S_(N+1)=S_N+d_N H_N$
  with $0 <= d_N < 2^(3k_N+7)$. This proves monotonicity. The sequence is bounded exactly when these nonnegative increments vanish from some point onward.
]

#remark[
  Strict increase is false for finite prefixes. For example, the gap prefix
  $(0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0)$
  has the same least residue at lengths $15$ and $16$. Thus the missing theorem cannot be a naive strict-monotonicity statement; it must prove that nonzero increments occur infinitely often for every non-eventually-periodic infinite gap word.
]

#proposition(name: "Binary ${0,1}$ Gap Finite Height Search Criterion")[
  Fix a positive integer bound $B$ and a target prefix length $L$. To decide whether there is a length-$L$ gap word whose least prefix residue $S_L$ is less than $B$, it is enough to search a finite tree. More precisely, suppose a current prefix has composition
  $ H_i a_i = A_i a_0 - C_i $
  and least residue $S_i < B$. Any extension that can still end with some $S_L < B$ must have next gap $k_i$ satisfying
  $ 8^(k_i) H_i < A_i B. $
  Any extension whose new least residue is $>= B$ can be discarded.
]
#proof[
  If a length-$L$ extension has $S_L < B$, then by gap-prefix monotonicity every shorter prefix residue in the same word also satisfies $S_i <= S_L < B$. This justifies discarding every branch once its least residue reaches $B$.

  Now fix a surviving prefix. For any ordinary start $a_0 < B$ realizing an extension of this prefix, the state after the prefix is
  $ a_i = (A_i a_0 - C_i) / H_i. $
  Since $C_i >= 0$ and $a_0 < B$, this gives
  $ a_i < A_i B / H_i. $
  If the next gap is $k_i$, then the gap partial map requires $a_i=8^(k_i)b_i$ with $b_i >= 1$. Hence $8^(k_i) <= a_i$, and therefore
  $ 8^(k_i) H_i < A_i B. $
  For fixed $A_i,H_i,B$, only finitely many nonnegative $k_i$ satisfy this inequality. Iterating the argument gives a finite search tree.
]

#remark[
  This is a certification tool, not a proof of the infinite gap theorem. The script `explorations/explore53_gap_minima.py` implements this finite-height criterion and certifies the least gap-prefix residues through length $12$. The certified minima already grow quickly, but an infinite proof would need a uniform lower-bound theorem as $L arrow.r infinity$.
]

#proposition(name: "Binary ${0,1}$ Gap Global-Minimum Divergence Criterion")[
  Let
  $ nu_L = min { S_L(k_0,dots,k_(L-1)) : k_i >= 0 } $
  be the least gap-prefix residue among all zero-gap words of length $L$. Then the reduced ${0,1}$ gap system has no positive ordinary infinite gap code if and only if
  $ nu_L arrow.r infinity. $
]
#proof[
  The minimum $nu_L$ exists by the same finite-height argument as in the return case: the all-zero gap word gives a finite candidate bound, and the finite-height search criterion reduces all words below that bound to a finite tree.

  If an infinite gap word has positive ordinary code $A$, then its prefix residues satisfy $S_L equiv A mod H_L$ for every $L$. Since $H_L arrow.r infinity$, once $H_L>A$ the least nonnegative representative is exactly $S_L=A$. Therefore $nu_L <= A$ for all sufficiently large $L$, so $nu_L$ cannot diverge.

  Conversely, suppose $nu_L$ does not tend to infinity. The sequence $nu_L$ is nondecreasing because every longer prefix residue reduces to its shorter prefix residue modulo the shorter modulus. Hence the $nu_L$ are bounded by some integer $B$. The tree of finite gap words with least prefix residue at most $B$ has nodes at every depth and is finitely branching by the finite-height search criterion with bound $B+1$. It therefore has an infinite path. Along this path the prefix residues are nondecreasing and bounded, hence eventually constant. The gap-code boundedness criterion then gives a nonnegative ordinary gap code. Since every gap prefix residue is positive, this ordinary code is positive.
]

#remark[
  Thus the smallest reduced obstruction is exactly the global height-growth problem $nu_L arrow.r infinity$. The computations in `explorations/explore53_gap_minima.py` certify initial values of $nu_L$; a proof must replace those certificates with a uniform lower bound.
]

#proposition(name: "Bounded ${0,1}$ Gap Alphabet Divergence Criterion")[
  Fix $K >= 0$ and define the restricted gap minimum
  $ nu_L^(<=K) = min { S_L(k_0,dots,k_(L-1)) : 0 <= k_i <= K " for all " i }. $
  Then there is no positive ordinary infinite gap code whose zero-gap lengths all lie in ${0,dots,K}$ if and only if
  $ nu_L^(<=K) arrow.r infinity. $
]
#proof[
  Since the alphabet ${0,dots,K}$ is finite, the minimum exists at every finite level $L$.

  If an infinite gap word over this alphabet has positive ordinary code $A$, then its length-$L$ prefix residue is congruent to $A$ modulo its prefix modulus $H_L$. Since $H_L arrow.r infinity$, the least representative is eventually exactly $A$. Hence $nu_L^(<=K) <= A$ for all sufficiently large $L$, so the restricted minima do not diverge.

  Conversely, suppose $nu_L^(<=K)$ does not diverge. The restricted minima are nondecreasing, because every longer prefix residue reduces to its shorter prefix residue modulo the shorter modulus. Hence they are bounded by some $B$. The tree of finite words over ${0,dots,K}$ with least prefix residue at most $B$ has nodes at every depth and is finitely branching. By the elementary infinite-tree lemma, it contains an infinite path. Along that path the prefix residues are nondecreasing and bounded, hence eventually constant. The gap-code boundedness criterion then gives a nonnegative ordinary gap code. Since every gap prefix residue is positive, this code is positive.
]

#proposition(name: "Binary ${0,1}$ Gap Fixed Positive-Label Divergence")[
  Fix $J >= 0$. Let $nu_(L,J)^+$ be the least gap-prefix residue among length-$L$ zero-gap words with at most $J$ positive zero-gap lengths. Then
  $ nu_(L,J)^+ arrow.r infinity $
  as $L arrow.r infinity$.
]
#proof[
  The all-zero gap word is an admissible finite candidate. The finite-height search criterion makes the set of words below any fixed candidate finite, so the minimum exists.

  The sequence $nu_(L,J)^+$ is nondecreasing: any length-$(L+1)$ word with at most $J$ positive labels has a length-$L$ prefix with at most $J$ positive labels, and gap-prefix residues are nondecreasing under extension.

  Suppose $nu_(L,J)^+$ did not tend to infinity. Then it is bounded by some integer $B$. The tree of finite gap words with at most $J$ positive labels and least prefix residue at most $B$ has nodes at every depth and is finitely branching by the finite-height search criterion. Hence it has an infinite path.

  Since every prefix on this path has at most $J$ positive labels, the infinite gap word has at most $J$ positive labels and is eventually all zero. The bounded prefix residues give a positive ordinary infinite gap code by the gap-code boundedness criterion. This positive orbit has an eventually periodic gap itinerary, contradicting the no eventually periodic ${0,1}$ gap itinerary proposition.
]
#remark[
  For the two-symbol zero-gap alphabet ${0,1}$, this proves divergence in every fixed-one-count stratum. A remaining bounded-residue gap obstruction must contain infinitely many positive zero-gap labels.
]

#proposition(name: "Binary ${0,1}$ Gap Prefix-Language Compactness Principle")[
  Let $C$ be a prefix-closed collection of finite zero-gap words, and let $C_L$ be its words of length $L$. Suppose $C_L$ is nonempty for arbitrarily large $L$. For each such $L$, let
  $ nu_C(L) = min { S_w : w in C_L }. $
  If $nu_C(L)$ does not tend to infinity along the lengths where it is defined, then there is an infinite zero-gap word whose every finite prefix lies in $C$ and whose gap code is a positive ordinary integer.

  Consequently, if every infinite word with all prefixes in $C$ is already excluded as an ordinary gap itinerary, then $nu_C(L) arrow.r infinity$.
]
#proof[
  If $nu_C(L)$ does not tend to infinity, then the monotonicity of gap-prefix residues implies that the values $nu_C(L)$ are bounded by some integer $B$ along arbitrarily large lengths. Consider the tree of words $w in C$ satisfying $S_w <= B$. This tree has nodes at arbitrarily large depths, hence at every smaller depth by prefix closure. It is finitely branching below the fixed height bound $B$ by the gap finite-height search criterion. Therefore it has an infinite path.

  Along this path the gap-prefix residues are nondecreasing and bounded, hence eventually constant. The gap-code boundedness criterion turns the path into a nonnegative ordinary gap code; because every nonempty gap prefix residue is positive, this code is positive. The final consequence is the contrapositive.
]

#proposition(name: "Binary ${0,1}$ Gap Finite-Defect Periodic Shadow Divergence")[
  Fix an eventually periodic infinite zero-gap word $z=(z_0,z_1,dots)$ and an integer $J >= 0$. Let $nu_(L,J)(z)$ be the least gap-prefix residue among length-$L$ zero-gap words that differ from $(z_0,dots,z_(L-1))$ in at most $J$ positions. Then
  $ nu_(L,J)(z) arrow.r infinity $
  as $L arrow.r infinity$.
]
#proof[
  The minimum exists at every length by using the all-zero gap word as a finite candidate and applying the finite-height search criterion below that candidate.

  The sequence $nu_(L,J)(z)$ is nondecreasing, because any admissible length-$(L+1)$ word has an admissible length-$L$ prefix and gap-prefix residues are nondecreasing under extension.

  If $nu_(L,J)(z)$ did not tend to infinity, then it would be bounded by some $B$. The tree of finite gap words that differ from the corresponding prefix of $z$ in at most $J$ positions and have least prefix residue at most $B$ has nodes at every depth and is finitely branching by the finite-height search criterion. Hence it has an infinite path.

  This infinite path differs from $z$ in at most $J$ positions total, and is therefore eventually periodic. The bounded prefix residues give a positive ordinary infinite gap code by the gap-code boundedness criterion. This contradicts the no eventually periodic ${0,1}$ gap itinerary proposition.
]
#remark[
  A reduced-gap obstruction cannot be a bounded-defect perturbation of any eventually periodic zero-gap template. Any bounded-alphabet obstruction must drift away from every periodic shadow in unboundedly many positions.
]

#proposition(name: "Binary ${0,1}$ Gap Low-Complexity Divergence")[
  Fix $m>=1$. For a finite binary zero-gap word $w in {0,1}^L$, let $p_w(m)$ be the number of distinct length-$m$ factors appearing in $w$, with $p_w(m)=0$ when $L<m$. Let $nu_(L,m)^("low")$ be the least gap-prefix residue among length-$L$ binary zero-gap words satisfying $p_w(m) <= m$. Then
  $ nu_(L,m)^("low") arrow.r infinity $
  as $L arrow.r infinity$.
]
#proof[
  Let $C_m$ be the collection of finite binary zero-gap words $w$ with $p_w(m) <= m$. This collection is prefix-closed, and it has words of every length because the all-zero word belongs to it.

  Any infinite word whose every finite prefix lies in $C_m$ has at most $m$ distinct length-$m$ factors: the finite factor sets are nested and each has size at most $m$. By the Morse-Hedlund complexity criterion, such an infinite word is eventually periodic.

  The no eventually periodic ${0,1}$ gap itinerary proposition excludes every eventually periodic ordinary gap itinerary. Applying the binary ${0,1}$ gap prefix-language compactness principle to $C_m$ gives the claimed divergence.
]
#remark[
  Thus a bounded-residue obstruction in the binary reduced-gap alphabet must be Sturmian-or-higher at every fixed scale: for each $m$, sufficiently long low-residue prefixes must contain at least $m+1$ distinct length-$m$ factors.
]

#proposition(name: "Binary ${0,1}$ Gap Balanced-Frontier Criterion")[
  Let $nu_L^("bal")$ be the least gap-prefix residue among balanced binary zero-gap words of length $L$. Then
  $ nu_L^("bal") arrow.r infinity $
  if and only if there is no non-eventually-periodic balanced infinite binary zero-gap word whose gap code is a positive ordinary integer.
]
#proof[
  If such an ordinary balanced gap code exists, its prefix residues are eventually equal to the represented positive integer, so $nu_L^("bal")$ cannot tend to infinity.

  Conversely, suppose $nu_L^("bal")$ does not tend to infinity. Let $C_("bal")$ be the collection of finite balanced binary zero-gap words. This class is prefix-closed and has words of every length. By the binary ${0,1}$ gap prefix-language compactness principle, bounded balanced minima give an infinite binary zero-gap word whose every finite prefix is balanced and whose gap code is a positive ordinary integer.

  The resulting infinite word is balanced: any two of its finite factors occur together in some long enough finite prefix, and that prefix is balanced. If the infinite word were eventually periodic, it would contradict the no eventually periodic ${0,1}$ gap itinerary proposition. Hence it is a non-eventually-periodic balanced positive ordinary gap code.
]
#remark[
  This is the exact reduced-gap version of the Sturmian-like frontier. The later Sturmian fast prefix-recurrence argument settles this minimal-complexity binary obstruction before the higher-complexity aperiodic cases.
]

#proposition(name: "Binary ${0,1}$ Gap Balanced Sublinear-Symbol Divergence")[
  Fix a symbol $a in {0,1}$ and a function $f: NN arrow.r NN$ with $f(n)\/n arrow.r 0$. Let $C_f^a$ be the class of balanced finite binary zero-gap words $w$ such that every length-$n$ factor of $w$ contains at most $f(n)$ occurrences of $a$. Let $nu_(f,a)(L)$ be the least gap-prefix residue among words in $C_f^a$ of length $L$, when such words exist. Then
  $ nu_(f,a)(L) arrow.r infinity $
  along the lengths where it is defined.
]
#proof[
  The class $C_f^a$ is prefix-closed. If its restricted minima did not tend to infinity, the binary ${0,1}$ gap prefix-language compactness principle would give an infinite binary zero-gap word $x$ whose every prefix lies in $C_f^a$ and whose gap code is a positive ordinary integer.

  The word $x$ is balanced, because any two finite factors occur together in a sufficiently long balanced prefix. Also, every length-$n$ factor of $x$ occurs in a sufficiently long prefix lying in $C_f^a$, so it contains at most $f(n)=o(n)$ occurrences of $a$.

  If $x$ were not eventually periodic, the balanced aperiodic positive-density lemma would force every long factor to contain linearly many occurrences of both symbols, including $a$, a contradiction. Hence $x$ is eventually periodic, contradicting the no eventually periodic ${0,1}$ gap itinerary proposition.
]
#remark[
  Thus any hypothetical balanced reduced-gap obstruction could not have density-zero windows in either symbol, even with the sparse count tending to infinity. The later Sturmian recurrence argument removes this balanced frontier entirely.
]

#proposition(name: "Binary ${0,1}$ Gap Fixed-Height Duality")[
  For $B >= 0$, define the reduced gap survival depth below height $B$ by
  $ H_G(B) = sup { L >= 0 : exists k_0,dots,k_(L-1) >= 0 " with " S_L(k_0,dots,k_(L-1)) <= B }. $
  Then
  $ H_G(B) < L quad <=> quad nu_L > B. $
  Consequently, the reduced ${0,1}$ gap system has no positive ordinary infinite gap code if and only if $H_G(B)<infinity$ for every fixed $B$.
]
#proof[
  By definition of $nu_L$ as the least length-$L$ gap-prefix residue, there exists a length-$L$ gap word with residue at most $B$ if and only if $nu_L <= B$. Negating gives $H_G(B)<L$ if and only if $nu_L>B$.

  Thus $H_G(B)<infinity$ for every fixed $B$ is equivalent to saying that for every $B$ some $nu_L$ exceeds $B$. Since $nu_L$ is nondecreasing, this is equivalent to $nu_L arrow.r infinity$. The gap global-minimum divergence criterion then gives the final claim.
]

#remark[
  The script `explorations/explore55_height_survival.py` computes $H_G(B)$ for sample bounds. Any proof that $H_G(B)$ is finite for every $B$ would settle the reduced ${0,1}$ gap obstruction.
]

#proposition(name: "Binary ${0,1}$ Gap Height Scale Lower Bound")[
  The global reduced-gap minima and fixed-height survival depths satisfy
  $ nu_L < 128^L, quad H_G(128^L-1) >= L. $
  Consequently, any universal upper bound of the form
  $ H_G(B) <= c log_2(B+1) + O(1) $
  must have $c >= 1\/7$.
]
#proof[
  The all-zero gap word of length $L$ has least residue
  $ S_L equiv 1\/115 mod 128^L, quad 0 <= S_L < 128^L. $
  Therefore $nu_L <= S_L < 128^L$, and the height bound $B=128^L-1$ admits a length-$L$ gap prefix. Thus $H_G(128^L-1) >= L$.

  Substituting $B=128^L-1$ into $H_G(B) <= c log_2(B+1)+O(1)$ gives
  $ L <= 7 c L + O(1), $
  hence $c >= 1\/7$.
]

#proposition(name: "Binary ${0,1}$ Gap Counting Criterion")[
  Let $N_G(B,L)$ be the number of length-$L$ gap words whose least prefix residue is at most $B$.

  If there are constants $C>0$ and $0<rho<1$ such that
  $ N_G(B,L) <= C B rho^L $
  for every $B,L$, then
  $ H_G(B) <= ceil(log_(1\/rho)(C B)). $
  In particular, this counting bound would rule out positive ordinary infinite reduced gap codes.
]
#proof[
  If $L > log_(1\/rho)(C B)$, then $C B rho^L < 1$. Since $N_G(B,L)$ is a nonnegative integer, this gives $N_G(B,L)=0$, so no length-$L$ gap prefix has least residue at height at most $B$. This is exactly the stated bound on $H_G(B)$.
]

#proposition(name: "Binary ${0,1}$ Gap Normalized Stopping-Time Criterion")[
  Let $W_G(B,L)$ be the number of length-$L$ gap words whose normalized terminal state satisfies
  $ u_w/E_w < B. $
  If there are constants $C>0$ and $0<rho<1$ such that
  $ W_G(B,L) <= C B rho^L $
  for every $B,L$, then
  $ H_G(B) <= ceil(log_(1\/rho)(C B)). $
  In particular, this normalized terminal-window estimate would rule out positive ordinary infinite reduced gap codes.
]
#proof[
  By the terminal-window counting equivalence, $W_G(B,L)=N_G(B,L)$. The claim is exactly the binary ${0,1}$ gap counting criterion.
]

#proposition(name: "Binary ${0,1}$ Gap Terminal-Rank Criterion")[
  For a length-$L$ gap word $w$, let $op("trank")_G(w)$ be the number of length-$L$ gap words $v$ satisfying
  $ ceil(u_v\/E_v) <= ceil(u_w\/E_w). $
  A uniform estimate
  $ W_G(B,L) <= C B rho^L $
  for all $B,L$ is equivalent to the terminal-rank estimate
  $ op("trank")_G(w) <= C ceil(u_w\/E_w) rho^L $
  for every finite gap word $w$.
]
#proof[
  The gap terminal-window proposition gives $ceil(u_w\/E_w)=S_w$ for every word $w$, and the terminal-window counting equivalence gives $W_G(B,L)=N_G(B,L)$. Thus $op("trank")_G(w)=N_G(S_w,L)$, which is the gap critical rank of $w$. The claim is exactly the binary ${0,1}$ gap critical-rank criterion written in terminal coordinates.
]

#proposition(name: "Binary ${0,1}$ Gap Terminal Start-Count Formula")[
  Let $A_G(B,L)$ be the number of ordinary starts $1 <= a <= B$ whose reduced ${0,1}$ gap partial-map orbit is defined for at least $L$ complete gap transitions. Then
  $ A_G(B,L)
     = sum_(w: |w|=L, 1<=ceil(u_w\/E_w)<=B)
        (floor((B - ceil(u_w\/E_w))\/H_w)+1). $
]
#proof[
  The gap terminal-window proposition gives $ceil(u_w\/E_w)=S_w$. Substituting this identity into the binary ${0,1}$ gap start-count formula gives the displayed formula.
]

#proposition(name: "Binary ${0,1}$ Gap Terminal Boundedness Criterion")[
  Fix an infinite gap word, and let $w_N$ be its length-$N$ prefix. Let $E_N$ and $u_N$ be the expansion factor and terminal state associated to $w_N$ and its least gap-prefix residue. Then the selected $2$-adic gap code is a positive ordinary integer if and only if
  $ ceil(u_N\/E_N) $
  is bounded as $N arrow.r infinity$. Equivalently, this happens if and only if the sequence $ceil(u_N\/E_N)$ is eventually constant.
]
#proof[
  The gap terminal-window proposition gives
  $ ceil(u_N\/E_N)=S_N, $
  where $S_N$ is the least gap-prefix residue. The claim is therefore exactly the binary ${0,1}$ gap-code boundedness criterion.
]

#proposition(name: "Binary ${0,1}$ Gap Terminal Monotonicity")[
  Fix an infinite gap word, and let $w_N$ be its length-$N$ prefix. Put
  $ T_N = ceil(u_N\/E_N), $
  where $E_N$ and $u_N$ are the expansion factor and terminal state associated to $w_N$ and its least gap-prefix residue. If the next gap block has modulus $q_N=2^(3k_N+7)$ and the prefix modulus before it is $H_N$, then
  $ T_(N+1) = T_N + d_N H_N $
  for some integer $d_N$ with $0 <= d_N < q_N$. In particular, $T_N$ is nondecreasing, and it is eventually constant if and only if $d_N=0$ for all sufficiently large $N$.
]
#proof[
  By the gap terminal-window proposition, $T_N=S_N$, the least gap-prefix residue. The gap-prefix digit recurrence writes
  $ S_(N+1)=S_N+d_N H_N, quad 0 <= d_N < q_N. $
  Substituting $T_N=S_N$ gives the displayed formula. Since $H_N>0$, the sequence is nondecreasing, and it is eventually constant exactly when all sufficiently late increments vanish.
]

#proposition(name: "Binary ${0,1}$ Gap Terminal Zero-Step Criterion")[
  Fix a finite gap prefix with auxiliary terminal state $u_N$. For a proposed next gap length $k$, write
  $ p=3^(2k+5), quad q=2^(3k+7), quad c=8^k. $
  The next rounded terminal increment is zero if and only if
  $ p u_N equiv c mod q. $
  In that case
  $ u_(N+1) = (p u_N-c)\/q, $
  so the auxiliary terminal state itself takes the same reduced gap-map step of length $k$. Consequently, at most one next gap length can give a zero terminal increment.
]
#proof[
  The first equivalence is exactly the zero-digit criterion in the gap-prefix digit recurrence, written with $u_N$ as the auxiliary state. When the congruence holds, the displayed formula is the reduced gap-map step with input $u_N$ and gap length $k$. The uniqueness of a zero-increment next length follows from ordinary gap itinerary uniqueness for the fixed auxiliary state $u_N$.
]

#proposition(name: "Binary ${0,1}$ Gap Terminal Zero-Increment Congruence")[
  Fix a finite gap prefix with auxiliary terminal state $u_N$. For a finite zero-gap suffix $v=(k_N,dots,k_(N+L-1))$, let $S_v$ and $H_v$ be the least prefix residue and modulus of the suffix as a standalone gap word. Then the rounded gap terminal coordinate has zero increments through the whole suffix $v$ if and only if
  $ u_N equiv S_v mod H_v. $
]
#proof[
  By the terminal zero-step criterion, zero increments through the suffix are equivalent to saying that the auxiliary state $u_N$ realizes the ordinary gap itinerary $v$ for $L$ complete gap transitions. The binary ${0,1}$ gap forced-orbit prefix equivalence says this happens if and only if $u_N$ satisfies the suffix prefix congruence $u_N equiv S_v mod H_v$.
]

#proposition(name: "Binary ${0,1}$ Gap Terminal Self-Shadowing Criterion")[
  Fix a finite gap prefix with auxiliary terminal state $u_N$ and an infinite zero-gap suffix $v=(k_N,k_(N+1),dots)$. For $L>=1$, let $S_(v,L)$ and $H_(v,L)$ be the least prefix residue and modulus of the first $L$ gaps of $v$, considered as a standalone gap word. Then the rounded gap terminal coordinate has zero increments along the whole suffix $v$ if and only if
  $ u_N equiv S_(v,L) mod H_(v,L) quad "for every " L>=1. $
  Equivalently, $u_N$ is the positive ordinary gap code selected by the suffix $v$.
]
#proof[
  By the terminal zero-increment congruence proposition, zero increments through the first $L$ gaps of $v$ are equivalent to the congruence
  $ u_N equiv S_(v,L) mod H_(v,L). $
  Requiring zero increments along the whole suffix is therefore equivalent to requiring these congruences for every $L$.

  The binary ${0,1}$ gap forced-orbit prefix equivalence says exactly that a fixed positive state realizes the first $L$ forced gap transitions of $v$ if and only if it satisfies all prefix congruences through length $L$. Hence satisfying the displayed congruences for every $L$ is equivalent to $u_N$ being the positive ordinary gap code for the suffix.
]

#proposition(name: "Binary ${0,1}$ Gap Shift-Code Recurrence")[
  Suppose an infinite zero-gap word $v=(k_0,k_1,dots)$ has positive ordinary gap code $Y_0$. Let $Y_j$ be the state after the first $j$ complete gap transitions. Then for every $j>=0$, $Y_j$ is the positive ordinary gap code of the shifted suffix $(k_j,k_(j+1),dots)$, and
  $ 2^(3k_j+7) Y_(j+1) = 3^(2k_j+5) Y_j - 8^(k_j). $
  In particular, for every $L>=1$,
  $ Y_L >= (81\/43)^L (9\/8)^(k_0+dots+k_(L-1)) Y_0. $
]
#proof[
  Since $Y_0$ realizes the full gap word, the states $Y_j$ are positive integers and satisfy the displayed one-gap recurrence. Starting from $Y_j$, the remaining orbit follows exactly the shifted suffix $(k_j,k_(j+1),dots)$. By ordinary gap itinerary uniqueness, $Y_j$ is the positive ordinary gap code selected by that shifted suffix.

  The final inequality is the binary ${0,1}$ gap terminal escape proposition applied to the positive orbit segment $Y_0,dots,Y_L$.
]

#proposition(name: "Binary ${0,1}$ Gap Terminal Zero-Increment Cylinder Density")[
  Fix a finite zero-gap suffix $v=(k_0,dots,k_(L-1))$ with modulus
  $ H_v = product_(i=0)^(L-1) 2^(3k_i+7). $
  Among positive auxiliary states $u$, the set for which the rounded gap terminal coordinate has zero increments through $v$ is one residue class modulo $H_v$, and therefore has natural density $1\/H_v$.

  Consequently, for a fixed infinite zero-gap suffix, the set of $2$-adic auxiliary states that shadow the whole suffix is a single $2$-adic point and has Haar measure zero.
]
#proof[
  The terminal zero-increment congruence proposition identifies the finite zero-increment set with
  $ u equiv S_v mod H_v, $
  one residue class modulo $H_v$. Its natural density among positive integers is therefore $1\/H_v$.

  For an infinite suffix, these congruence classes are nested and the moduli $H_(v,L)$ tend to infinity. Their intersection in $ZZ_2$ is a single inverse-limit point, namely the $2$-adic gap code of the suffix. A singleton in $ZZ_2$ has Haar measure zero.
]

#proposition(name: "Binary ${0,1}$ Gap Terminal Zero-Increment Survival Density")[
  Among positive auxiliary states $u$, the natural density of states admitting at least $L$ consecutive rounded gap terminal zero-increments is
  $ 112^(-L). $
]
#proof[
  For a fixed length-$L$ gap suffix $v=(k_0,dots,k_(L-1))$, the terminal zero-increment cylinder-density proposition gives density
  $ 1\/H_v = product_(i=0)^(L-1) 2^(-(3k_i+7)). $
  Distinct suffix words give disjoint sets of auxiliary states, because the ordinary gap itinerary from a fixed auxiliary state is unique. Therefore the total density is
  $ (sum_(k>=0) 2^(-(3k+7)))^L = 112^(-L). $
]

#proposition(name: "Bounded Binary ${0,1}$ Gap Terminal Zero-Increment Survival Density")[
  Among positive auxiliary states $u$, the natural density of states whose next $L$ rounded gap terminal increments are zero and whose corresponding zero-gap lengths all satisfy $0 <= k <= K$ is
  $ ((1\/112)(1 - 8^(-(K+1))))^L. $
]
#proof[
  Repeat the proof of the terminal zero-increment survival density, but sum only over suffix words with $0 <= k_i <= K$. The one-step density sum is
  $ sum_(k=0)^K 2^(-(3k+7))
    = (1\/112)(1 - 8^(-(K+1))). $
  Since distinct finite suffix words are disjoint itinerary cylinders, the $L$-step density is the $L$-th power of this restricted one-step sum.
]

#proposition(name: "Finite Binary ${0,1}$ Gap Terminal Zero-Increment Words Are Locally Realizable")[
  For every finite sequence of zero-gap lengths $(k_0,dots,k_(L-1))$, there are infinitely many positive auxiliary states $u_0$ for which the rounded gap terminal coordinate has zero increments through exactly this finite sequence.
]
#proof[
  By finite ${0,1}$ gap-word realizability, there are infinitely many positive states $u_0$ whose ordinary reduced gap itinerary begins with the prescribed word. Along such an ordinary orbit, the terminal zero-step criterion gives zero rounded-terminal increment at each prescribed gap length. Thus every finite gap word is locally realizable as a zero-increment terminal word.
]

#remark[
  The exact survival density $112^(-L)$ suggests the natural candidate $rho=1\/112$, again up to finite-height discrepancy terms. Here $N_G$ counts least-residue gap words, not all starts below $B$. Such a counting-discrepancy theorem would settle the reduced ${0,1}$ gap obstruction, but it remains open.
]

#proposition(name: "Binary ${0,1}$ Gap Counting Rate Lower Bound")[
  Any prefix-counting bound of the form
  $ N_G(B,L) <= C B rho^L $
  holding for all $B,L$ with fixed $C>0$ must satisfy
  $ rho >= 1\/128. $
]
#proof[
  For each $L$, the all-zero gap word has a positive least residue $S_L < 128^L$. Thus
  $ N_G(128^L-1,L) >= 1. $
  The assumed counting bound gives
  $ 1 <= C(128^L-1)rho^L < C(128rho)^L $
  for every large $L$. If $rho<1\/128$, the right side tends to $0$, a contradiction. Hence $rho>=1\/128$.
]

#remark[
  The density value $1\/112$ is again close to the worst-case obstruction $1\/128$. A uniform counting proof would therefore need to control finite-height clustering quite tightly.
]

#proposition(name: "Binary ${0,1}$ Gap Start-Count Formula")[
  Let $A_G(B,L)$ be the number of ordinary starts $1 <= a <= B$ whose reduced ${0,1}$ gap partial-map orbit is defined for at least $L$ complete gap transitions. For a gap word $w=(k_0,dots,k_(L-1))$, let $S_w$ be its least prefix residue and $H_w=product_i 2^(3k_i+7)$. Then
  $ A_G(B,L) = sum_(w: |w|=L, 1<=S_w<=B) (floor((B-S_w)\/H_w)+1). $
  In particular,
  $ N_G(B,L) <= A_G(B,L) <= N_G(B,L) + B 112^(-L). $
]
#proof[
  Each finite gap word gives exactly one residue class $S_w mod H_w$, and ordinary itinerary uniqueness makes the classes disjoint as realized starts. The count of representatives between $1$ and $B$ in such a class is $floor((B-S_w)\/H_w)+1$ if $1<=S_w<=B$, and zero otherwise, which gives the formula.

  The lower bound is immediate. For the upper bound, use
  $ floor((B-S_w)\/H_w)+1 <= 1 + B/H_w $
  and sum over words with $S_w<=B$. Extending the reciprocal-modulus sum to all length-$L$ gap words gives
  $ sum_(|w|=L) 1/H_w
     = (sum_(k>=0) 2^(-(3k+7)))^L
     = 112^(-L). $
]

#proposition(name: "Binary ${0,1}$ Gap Start/Prefix Counting Equivalence")[
  Fix $1\/112 <= rho < 1$. A uniform prefix-counting bound
  $ N_G(B,L) <= C B rho^L $
  implies the ordinary-start bound
  $ A_G(B,L) <= (C+1) B rho^L. $
  Conversely, an ordinary-start bound
  $ A_G(B,L) <= C B rho^L $
  implies the same prefix-counting bound for $N_G$.
]
#proof[
  The start-count formula gives
  $ N_G(B,L) <= A_G(B,L) <= N_G(B,L) + B 112^(-L). $
  Since $rho >= 1\/112$, the extra term is at most $B rho^L$. This proves the first implication. The converse follows from $N_G(B,L) <= A_G(B,L)$.
]

#proposition(name: "Binary ${0,1}$ Gap Critical-Height Reduction")[
  Fix a level $L$, a height cutoff $B_max$, and a rate $rho>0$. Among all integer heights $1 <= B <= B_max$, the maximum of
  $ N_G(B,L) / (B rho^L) $
  is attained at a height $B$ equal to the least prefix residue of some length-$L$ gap word, unless $N_G(B_max,L)=0$.
]
#proof[
  List the distinct realized least gap-prefix residues at level $L$ not exceeding $B_max$ as
  $ h_1 < h_2 < dots < h_m. $
  If there are none, then $N_G(B,L)=0$ throughout the interval. Otherwise, on every interval
  $ h_j <= B < h_(j+1) $
  the numerator $N_G(B,L)$ is constant, while the denominator $B$ is strictly increasing. Hence the ratio is largest at the left endpoint $B=h_j$. The same argument applies on $h_m <= B <= B_max$.
]

#proposition(name: "Binary ${0,1}$ Gap Critical-Rank Criterion")[
  For a length-$L$ gap word $w$, let
  $ op("rank")_G(w) = N_G(S_w,L), $
  the number of length-$L$ gap words whose least prefix residue is at most $S_w$.

  A uniform estimate
  $ N_G(B,L) <= C B rho^L $
  for all $B,L$ is equivalent to the critical-rank estimate
  $ op("rank")_G(w) <= C S_w rho^L $
  for every finite gap word $w$.
]
#proof[
  The uniform estimate implies the rank estimate by taking $B=S_w$.

  Conversely, fix $B,L$. If $N_G(B,L)=0$, there is nothing to prove. Otherwise choose the largest realized least gap-prefix residue $S_w <= B$ among length-$L$ gap words. Then
  $ N_G(B,L)=N_G(S_w,L)=op("rank")_G(w). $
  By the critical-rank estimate,
  $ N_G(B,L) <= C S_w rho^L <= C B rho^L. $
]

#remark[
  As in the return case, controlling low least residues controls actual ordinary survivors. The extra density term is already exponentially small in $L$.
]

#proposition(name: "Binary ${0,1}$ Gap-Prefix Digit Recurrence")[
  For a finite gap prefix, write
  $ H_N a_N = A_N a_0 - C_N $
  and let $S_N$ be the least prefix residue. Define
  $ u_N = (A_N S_N - C_N) / H_N. $
  For the next gap $k_N$, put
  $ p_N=3^(2k_N+5), quad q_N=2^(3k_N+7), quad c_N=8^(k_N). $
  If
  $ S_(N+1) = S_N + d_N H_N, quad 0 <= d_N < q_N, $
  then
  $ d_N equiv (c_N - p_N u_N) (p_N A_N)^(-1) mod q_N. $
  In particular, $d_N=0$ if and only if
  $ p_N u_N equiv c_N mod q_N. $
]
#proof[
  The extension has
  $ A_(N+1)=p_N A_N, quad H_(N+1)=H_N q_N, quad C_(N+1)=p_N C_N + c_N H_N. $
  Substitute $S_(N+1)=S_N+d_N H_N$ into
  $ A_(N+1) S_(N+1) - C_(N+1) equiv 0 mod H_(N+1). $
  Using $A_N S_N-C_N=H_N u_N$ and dividing by $H_N$ gives
  $ p_N u_N - c_N + p_N A_N d_N equiv 0 mod q_N. $
  Since $p_N A_N$ is odd, it is invertible modulo $q_N$, yielding the displayed congruence.
]

#proposition(name: "Binary ${0,1}$ Zero-Increment Tail Equivalence")[
  With the notation above, a run of zero gap-prefix increments
  $ d_N=d_(N+1)=dots=d_(N+L-1)=0 $
  is equivalent to a finite orbit of the same ${0,1}$ gap map starting from the auxiliary integer $u_N$ and following the gap word $k_N, dots, k_(N+L-1)$. Consequently, an eventually constant gap-prefix residue tail is equivalent to an infinite integer orbit of the ${0,1}$ gap map starting from some auxiliary state.
]
#proof[
  The previous proposition shows that $d_j=0$ is equivalent to
  $ p_j u_j equiv c_j mod q_j. $
  When this divisibility holds, define
  $ u_(j+1) = (p_j u_j - c_j) / q_j. $
  This is exactly the gap-map recurrence
  $ q_j u_(j+1)=p_j u_j-c_j. $
  Iterating proves the finite-run equivalence.

  If zero increments continue forever, the prefix residue is constant and the auxiliary recurrence gives an infinite integer orbit. Conversely, any such auxiliary orbit makes every later digit zero and hence keeps the prefix residue constant.
]

#proposition(name: "Binary ${0,1}$ Gap Terminal Zero-Increment Equivalence")[
  Fix a finite gap prefix and put $T_N=ceil(u_N\/E_N)$. For any gap suffix, an eventually constant tail of the rounded terminal coordinates
  $ T_N,T_(N+1),T_(N+2),dots $
  is equivalent to an infinite integer orbit of the reduced ${0,1}$ gap map starting from the auxiliary state $u_N$.
]
#proof[
  By the gap terminal monotonicity proposition, the rounded terminal coordinate is eventually constant exactly when the corresponding gap-prefix increments are eventually zero. The ${0,1}$ zero-increment tail equivalence says precisely that such a zero-increment tail is equivalent to an infinite integer orbit of the same gap map starting from $u_N$.
]

#proposition(name: "Binary ${0,1}$ Gap Terminal Zero-Increment Tail Uniqueness")[
  Fix a finite gap prefix and its auxiliary terminal state $u_N$. There is at most one infinite gap suffix for which all later rounded terminal increments are zero.
]
#proof[
  By the gap terminal zero-increment equivalence, such a suffix is exactly an infinite orbit of the reduced ${0,1}$ gap map starting from $u_N$. The binary ${0,1}$ gap ordinary itinerary uniqueness proposition says that a fixed positive normalized state has at most one infinite gap itinerary. Hence there is at most one zero-increment suffix.
]

#proposition(name: "Binary ${0,1}$ Gap Terminal Zero-Increment Escape")[
  Fix a finite gap prefix and suppose the next $L$ gap-prefix increments are zero. If the zero-increment suffix has gap lengths $(k_N,dots,k_(N+L-1))$ and total
  $ K = k_N + dots + k_(N+L-1), $
  then the auxiliary terminal states satisfy
  $ u_(N+L) >= (81\/43)^L (9\/8)^K u_N. $
]
#proof[
  By the terminal zero-increment equivalence, the auxiliary states $u_N,u_(N+1),dots,u_(N+L)$ form an actual positive orbit of the reduced gap partial map along the suffix word. Applying the binary ${0,1}$ gap terminal escape proposition to this finite orbit gives the displayed inequality.
]

#proposition(name: "No Eventually Periodic Binary ${0,1}$ Gap Terminal Tail")[
  No eventually periodic zero-gap suffix can make the rounded gap terminal coordinate eventually constant.
]
#proof[
  If such a suffix made the rounded terminal coordinate eventually constant, the gap terminal zero-increment equivalence would produce an infinite integer orbit of the reduced ${0,1}$ gap map whose gap itinerary is eventually periodic. This contradicts the no eventually periodic ${0,1}$ gap itinerary proposition.
]

#proposition(name: "Binary ${0,1}$ Gap-Core Recurrence")[
  In the ${0,1}$ gap-map notation, write
  $ a_j = 8^(k_j) b_j $
  where $b_j$ is odd and $k_j$ is the number of zero-return blocks before the next length-$1$ return. If the next gap $k_(j+1)$ is also defined, then
  $ 3 dot 9^(k_j) b_j equiv 49 mod 128, $
  and consecutive odd cores satisfy
  $ 2^(3k_(j+1)+7) b_(j+1) = 3^(2k_j+5)b_j - 1. $
  In particular,
  $ b_(j+1) equiv (-1)^(k_(j+1)) mod 3. $
]
#proof[
  The first congruence is exactly the gate condition from the gap partial map. Its output is
  $ a_(j+1) = (3^(2k_j+5)b_j - 1) / 128. $
  Since the next gap length is $k_(j+1)$, write $a_(j+1)=8^(k_(j+1))b_(j+1)$ with $b_(j+1)$ odd. Multiplying by $128=2^7$ gives the displayed recurrence.

  Reducing that recurrence modulo $3$ gives
  $ 2^(3k_(j+1)+7)b_(j+1) equiv -1 mod 3. $
  Since $2 equiv -1 mod 3$ and $3k_(j+1)+7$ has parity $k_(j+1)+1$, this is equivalent to
  $ b_(j+1) equiv (-1)^(k_(j+1)) mod 3. $
]

#proposition(name: "Binary ${0,1}$ Post-One 3-adic Reset")[
  In the ${0,1}$ gap-map notation, after a zero gap of length $k$ followed by a length-$1$ return, the next normalized state $a'$ satisfies
  $ a' equiv -128^(-1) mod 3^(2k+5). $
  In particular, every post-length-$1$ normalized state satisfies
  $ a' equiv 31 mod 81. $
]
#proof[
  By the gap partial map,
  $ a' = (3^(2k+5)b - 1) / 128. $
  Reducing modulo $3^(2k+5)$ gives
  $ a' equiv -128^(-1) mod 3^(2k+5). $
  Since $2k+5 >= 5$, this congruence implies its reduction modulo $81$. Computing $-128^(-1) mod 81$ gives $31$.
]

#proposition(name: "Binary ${0,1}$ Gap Reset-Spike Constraint")[
  In any infinite positive ${0,1}$ gap orbit with states $a_j$ and zero-gap lengths $k_j$, each complete gap transition satisfies
  $ a_j >= 8^(k_j), quad
     a_(j+1) equiv -128^(-1) mod 3^(2k_j+5). $
  Consequently, if the zero-gap lengths are unbounded, then along every subsequence with $k_j arrow.r infinity$ the incoming states $a_j$ tend to infinity in $RR$, while the following states $a_(j+1)$ converge to $-1\/128$ in $QQ_3$.
]
#proof[
  The gap partial map writes $a_j=8^(k_j)b_j$ with $b_j$ a positive odd integer, giving $a_j>=8^(k_j)$. The $3$-adic congruence is exactly the post-one $3$-adic reset proposition.
]

#proposition(name: "Binary ${0,1}$ Gap Obstruction Dichotomy")[
  If an infinite positive-integer orbit of the ${0,1}$ gap map exists, then exactly one of the following holds:
  - its zero-gap lengths are bounded, so its gap itinerary is an infinite non-eventually-periodic word over a finite alphabet;
  - its zero-gap lengths are unbounded, and the corresponding post-length-$1$ normalized states have a subsequence converging to $-1\/128$ in $QQ_3$.
]
#proof[
  If the zero-gap lengths are bounded, then they take values in a finite alphabet. The no-eventually-periodic gap itinerary proposition shows that the itinerary cannot eventually repeat, so it is a non-eventually-periodic infinite word over that finite alphabet.

  If the zero-gap lengths are unbounded, choose a subsequence of gaps $k_j arrow.r infinity$. By the post-one $3$-adic reset proposition, the following normalized states $a_(j+1)$ satisfy
  $ a_(j+1) equiv -128^(-1) mod 3^(2k_j+5), $
  and hence converge to $-1\/128$ in $QQ_3$.
]

#proposition(name: "Binary ${0,1}$ Gap Terminal Tail Dichotomy")[
  Fix a finite gap prefix. If the rounded gap terminal coordinate is eventually constant along an infinite suffix, then, after discarding a finite initial part of the suffix, exactly one of the following holds:
  - the zero-gap lengths in the zero-increment tail are bounded, so the tail is an infinite non-eventually-periodic word over a finite alphabet;
  - the zero-gap lengths in the zero-increment tail are unbounded, and the corresponding later auxiliary gap states have a subsequence converging to $-1\/128$ in $QQ_3$.
]
#proof[
  Once the rounded terminal coordinate is constant, all later rounded increments are zero. By the gap terminal zero-increment equivalence, the auxiliary terminal states form an infinite positive-integer orbit of the reduced ${0,1}$ gap map. Applying the binary ${0,1}$ gap obstruction dichotomy to this auxiliary orbit gives exactly the displayed bounded/unbounded split.
]

#theorem(name: "Sharpened Binary ${0,1}$ Gap Endpoint")[
  If an infinite positive-integer orbit of the reduced ${0,1}$ gap map exists, then exactly one of the following holds:
  - the zero-gap lengths are bounded. If $K$ is their maximum and $q$ is the number of distinct zero-gap lengths that occur, then the restricted minima $nu_L^(<=K)$ do not tend to infinity, and the zero-gap word has factor complexity at least $m+q-1$ at every length $m$;
  - the zero-gap lengths are unbounded. Along every subsequence with $k_j arrow.r infinity$, the incoming states satisfy $a_j >= 8^(k_j)$ and tend to infinity in $RR$, while the following states satisfy
    $ a_(j+1) equiv -128^(-1) mod 3^(2k_j+5) $
    and converge to $-1\/128$ in $QQ_3$.
]
#proof[
  The ordinary gap obstruction dichotomy gives the bounded/unbounded split. In the bounded case, the bounded gap alphabet divergence criterion shows that the restricted minima for the used alphabet do not diverge, and the bounded gap obstruction complexity proposition gives the factor-complexity lower bound. In the unbounded case, the gap reset-spike constraint gives the real lower bound and the $3$-adic convergence.
]

#proposition(name: "Binary ${0,1}$ Gap Survival Density")[
  In the ${0,1}$ gap-map coordinate $a=(n+1)\/3$, the natural density of $a$ admitting at least one complete next gap-to-length-$1$ transition is $1\/112$. The density of $a$ admitting at least $L$ consecutive such gap transitions is
  $ 112^(-L). $
  Conditioned on one transition existing, the zero-gap length has law
  $ P(k) = 7 / 8^(k+1) quad (k >= 0), $
  with mean $1\/7$.
  More generally, if zero-gap lengths are restricted to $0 <= k <= K$, then the density of starts admitting at least $L$ such bounded gap transitions is
  $ ((1\/112)(1 - 8^(-(K+1))))^L. $
]
#proof[
  For fixed $k$, the gap partial map requires
  $ a = 8^k b, quad 3 dot 9^k b equiv 49 mod 128. $
  Since $3 dot 9^k$ is odd, the congruence selects exactly one residue class for $b$ modulo $128$. Therefore it selects exactly one residue class for $a$ modulo $2^(3k+7)$, of density $2^(-(3k+7))$.

  Summing over all $k >= 0$ gives
  $ sum_(k=0)^infinity 2^(-(3k+7))
    = 1\/128 dot 1 / (1 - 1\/8)
    = 1\/112. $
  For a fixed finite gap word $(k_0, dots, k_(L-1))$, composing the gap maps gives one residue class modulo the product of the corresponding powers of $2$, since each transition has odd numerator coefficient. Summing over all gap words gives $112^(-L)$.

  Dividing the fixed-$k$ density by $1\/112$ gives
  $ P(k) = 112 / 2^(3k+7) = 7 / 8^(k+1). $
  This is the geometric law $(7\/8)(1\/8)^k$, whose mean is $(1\/8)/(7\/8)=1\/7$.

  Restricting to $0 <= k <= K$ replaces the one-step sum by
  $ sum_(k=0)^K 2^(-(3k+7))
    = (1\/112)(1 - 8^(-(K+1))). $
  The same product-and-sum argument gives the displayed $L$-transition density.
]

#proposition(name: "Binary ${0,1}$ Odd-Modulus Independence")[
  Fix an odd modulus $M$ and a residue class $a equiv s mod M$. Within this class, the relative natural density of $a$ admitting one complete ${0,1}$ gap-to-length-$1$ transition is still $1\/112$. More generally, the relative density of $a$ admitting at least $L$ consecutive complete gap transitions is still $112^(-L)$. Conditioned on one transition existing, the zero-gap length still has law
  $ P(k) = 7 / 8^(k+1). $
]
#proof[
  For a fixed gap length $k$, the gap partial map selects exactly one residue class for $a$ modulo $2^(3k+7)$. Since $M$ is odd, the Chinese remainder theorem combines this dyadic class with $a equiv s mod M$ into exactly one residue class modulo $M 2^(3k+7)$. Therefore the relative density inside the fixed class modulo $M$ is $2^(-(3k+7))$, the same as without the odd-modulus restriction.

  Summing over $k >= 0$ gives $1\/112$, and dividing the fixed-$k$ relative density by this sum gives the same conditional law $P(k)=7\/8^(k+1)$.

  For a fixed finite gap word $(k_0,dots,k_(L-1))$, the finite-word coding proposition gives one residue class modulo $product_j 2^(3k_j+7)$. Applying the same Chinese remainder argument with the fixed odd class gives the same relative density $product_j 2^(-(3k_j+7))$ inside $a equiv s mod M$. Summing over all finite gap words of length $L$ gives $112^(-L)$.
]

#proposition(name: "Binary ${0,1}$ Finite Reset-Neighborhood Transparency")[
  Fix $s >= 1$ and let $c_s$ be the residue class
  $ c_s equiv -128^(-1) mod 3^s. $
  Inside the finite $3$-adic reset neighborhood $a equiv c_s mod 3^s$, a fixed gap word $w=(k_0,dots,k_(L-1))$ has relative natural density
  $ product_(j=0)^(L-1) 2^(-(3k_j+7)). $
  Consequently, within this same reset neighborhood, the relative density of starts admitting at least $L$ complete gap transitions is $112^(-L)$, and the relative density with all $0 <= k_j <= K$ is
  $ ((1\/112)(1 - 8^(-(K+1))))^L. $
]
#proof[
  The fixed reset neighborhood is a single residue class modulo the odd modulus $3^s$. A fixed gap word selects one residue class modulo the dyadic modulus $product_j 2^(3k_j+7)$. These moduli are coprime, so the Chinese remainder theorem gives one combined residue class and hence the displayed relative density.

  Summing the fixed-word density over all gap words of length $L$ gives $112^(-L)$. Restricting the sum to $0 <= k_j <= K$ gives
  $ (sum_(k=0)^K 2^(-(3k+7)))^L
    = ((1\/112)(1 - 8^(-(K+1))))^L. $
]
#remark[
  This explains why the $3$-adic reset statements alone do not settle the ${0,1}$ case. Any fixed finite $3$-adic congruence class still contains the same dyadic density of finite next-gap prefixes. The missing step must use a pointwise height, coding, or infinite-orbit obstruction rather than an odd-modulus exclusion.
]

#proposition(name: "Binary Obstruction Dichotomy")[
  If an infinite positive-integer binary-depth obstruction exists, then exactly one of the following holds:
  - its return lengths are bounded, so its return itinerary is an infinite non-eventually-periodic word over a finite alphabet;
  - its return lengths are unbounded, and the corresponding post-return depth-$0$ parameters have a subsequence converging to $-85\/88$ in $QQ_3$.
]
#proof[
  If the return lengths are bounded, then they take values in a finite alphabet. The no-eventually-periodic binary return itinerary proposition shows that the itinerary cannot eventually repeat, so it is a non-eventually-periodic infinite word over that finite alphabet.

  If the return lengths are unbounded, choose a subsequence of return blocks with lengths $r_j arrow.r infinity$. By the binary return $3$-adic reset proposition, the following return parameters $n_(j+1)$ satisfy
  $ n_(j+1) equiv -85\/88 mod 3^(3r_j+1), $
  and hence converge to $-85\/88$ in $QQ_3$ along that subsequence.
]

#proposition(name: "Binary Return Terminal Tail Dichotomy")[
  Fix a finite return prefix. If the rounded return terminal coordinate is eventually constant along an infinite suffix, then, after discarding a finite initial part of the suffix, exactly one of the following holds:
  - the return lengths in the zero-increment tail are bounded, so the tail is an infinite non-eventually-periodic word over a finite alphabet;
  - the return lengths in the zero-increment tail are unbounded, and the corresponding later auxiliary return states have a subsequence converging to $-85\/88$ in $QQ_3$.
]
#proof[
  Once the rounded terminal coordinate is constant, all later rounded increments are zero. By the return terminal zero-increment equivalence, the auxiliary terminal states form an infinite positive-integer orbit of the binary return-block map. Applying the binary obstruction dichotomy to this auxiliary orbit gives exactly the displayed bounded/unbounded split.
]

#theorem(name: "Sharpened Binary Return Endpoint")[
  If an infinite positive-integer binary-depth return obstruction exists, then exactly one of the following holds:
  - the return lengths are bounded. If $R$ is their maximum and $q$ is the number of distinct return lengths that occur, then the restricted minima $mu_L^(<=R)$ do not tend to infinity, and the return word has factor complexity at least $m+q-1$ at every length $m$;
  - the return lengths are unbounded. Along every subsequence with $r_j arrow.r infinity$, the incoming states satisfy
    $ n_j >= (5 dot 16^(r_j)-32)\/33 $
    and tend to infinity in $RR$, while the following states satisfy
    $ n_(j+1) equiv -85\/88 mod 3^(3r_j+1) $
    and converge to $-85\/88$ in $QQ_3$.
]
#proof[
  The binary obstruction dichotomy gives the bounded/unbounded split. In the bounded case, the bounded return alphabet divergence criterion shows that the restricted minima for the used alphabet do not diverge, and the bounded return obstruction complexity proposition gives the factor-complexity lower bound. In the unbounded case, the return reset-spike constraint gives the real lower bound and the $3$-adic convergence.
]

#proposition(name: "Binary Return Survival Density")[
  Among depth-$0$ parameters $n >= 0$, the natural density of parameters admitting at least one finite binary return block is $2\/15$. More generally, the natural density of parameters admitting at least $L$ consecutive binary return blocks is
  $ (2\/15)^L. $
]
#proof[
  For a fixed return length $r$, the return-block gate is one residue class modulo $2^(4r+3)$. Thus its density among nonnegative integers is $2^(-(4r+3))$. The gates for different $r$ are disjoint, because $r$ is recovered uniquely as $v_2(33n+32)\/4$ in the partial-map formulation. Therefore the one-return density is
  $ sum_(r=0)^infinity 2^(-(4r+3))
    = 1\/8 dot 1 / (1 - 1\/16)
    = 2\/15. $

  For a fixed finite return word $(r_0, dots, r_(L-1))$, the return-block coding proposition gives exactly one residue class modulo
  $ product_(j=0)^(L-1) 2^(4r_j+3), $
  hence density $product_j 2^(-(4r_j+3))$. Distinct return words give disjoint classes, since the return lengths are determined by the successive partial-map factorizations. Summing over all $r_0, dots, r_(L-1) >= 0$ gives
  $ (sum_(r=0)^infinity 2^(-(4r+3)))^L = (2\/15)^L. $
]

#remark[
  This proves that infinite binary-depth return obstructions have density zero. It still does not rule out a single exceptional positive integer; the missing binary-depth theorem is the pointwise strengthening from zero density to emptiness.
]

#proposition(name: "Binary Return Odd-Modulus Independence")[
  Fix an odd modulus $M$ and a residue class $n equiv s mod M$. Within this class, the relative natural density of depth-$0$ parameters admitting one finite binary return block is still $2\/15$. More generally, the relative density of parameters admitting at least $L$ consecutive finite binary return blocks is still $(2\/15)^L$. Conditioned on one return existing, the return length still has law
  $ P(r)=15\/16^(r+1). $
]
#proof[
  For a fixed return length $r$, the return-block gate selects exactly one residue class for $n$ modulo $2^(4r+3)$. Since $M$ is odd, the Chinese remainder theorem combines this dyadic gate with $n equiv s mod M$ into exactly one residue class modulo $M 2^(4r+3)$. Thus the relative density inside the fixed odd-modulus class is $2^(-(4r+3))$, unchanged from the unrestricted calculation.

  Summing over $r >= 0$ gives $2\/15$, and dividing the fixed-$r$ relative density by $2\/15$ gives $P(r)=15\/16^(r+1)$.

  For a fixed finite return word $(r_0,dots,r_(L-1))$, the return-block coding proposition gives one residue class modulo $product_j 2^(4r_j+3)$. The same CRT argument with $n equiv s mod M$ gives the same relative density $product_j 2^(-(4r_j+3))$ inside the fixed odd class. Summing over all return words of length $L$ gives $(2\/15)^L$.
]

#proposition(name: "Binary Return Finite Reset-Neighborhood Transparency")[
  Fix $s >= 1$ and let $c_s$ be the residue class
  $ c_s equiv -85\/88 mod 3^s. $
  Inside the finite $3$-adic reset neighborhood $n equiv c_s mod 3^s$, a fixed return word $w=(r_0,dots,r_(L-1))$ has relative natural density
  $ product_(j=0)^(L-1) 2^(-(4r_j+3)). $
  Consequently, within this same reset neighborhood, the relative density of starts admitting at least $L$ return blocks is $(2\/15)^L$, and the relative density with all $0 <= r_j <= R$ is
  $ ((2\/15)(1 - 16^(-(R+1))))^L. $
]
#proof[
  The fixed reset neighborhood is a single residue class modulo the odd modulus $3^s$. A fixed return word selects one residue class modulo the dyadic modulus $product_j 2^(4r_j+3)$. These moduli are coprime, so CRT gives one combined residue class and hence the displayed relative density inside $n equiv c_s mod 3^s$.

  Summing the fixed-word density over all return words of length $L$ gives $(2\/15)^L$. Restricting the sum to $0 <= r_j <= R$ gives
  $ (sum_(r=0)^R 2^(-(4r+3)))^L
    = ((2\/15)(1 - 16^(-(R+1))))^L. $
]

#remark[
  This shows why the binary return mod-$3$ trap cannot by itself settle the $T=1$ case. Any fixed finite odd-modulus congruence class, including $n equiv 2 mod 3$, still contains the same relative dyadic density of finite next-return prefixes.
]

#proposition(name: "Binary Return-Length Law")[
  Conditioned on the existence of one finite binary return block, the return length $r$ has distribution
  $ P(r) = 15 / 16^(r+1) quad (r >= 0). $
  In particular, the conditional mean return length is
  $ E(r) = 1\/15. $
  More generally, if return lengths are restricted to $0 <= r <= R$, then the density of starts admitting at least $L$ such bounded return blocks is
  $ ((2\/15)(1 - 16^(-(R+1))))^L. $
]
#proof[
  From the survival-density proof, the unconditioned density of a return block with length exactly $r$ is $2^(-(4r+3))$. Dividing by the one-return density $2\/15$ gives
  $ P(r) = 2^(-(4r+3)) / (2\/15)
         = 15 / 2^(4r+4)
         = 15 / 16^(r+1). $
  This is the geometric law $(1-1\/16)(1\/16)^r$, so its mean is
  $ (1\/16)/(1 - 1\/16) = 1\/15. $

  Restricting to $0 <= r <= R$ replaces the one-step sum by
  $ sum_(r=0)^R 2^(-(4r+3))
    = (2\/15)(1 - 16^(-(R+1))). $
  The same product-and-sum argument as in the survival-density proposition gives the displayed $L$-block density.
]

#lemma(name: "Binary Return Mod-3 Trap")[
  For every binary return block $0 arrow.r 1^r arrow.r 0$, the output depth-$0$ parameter satisfies
  $ n_(j+1) equiv 2 mod 3. $
]
#proof[
  In the return-block coding notation,
  $ Q_r n_(j+1) = P_r n_j + D_r. $
  Since $P_r = 9 dot 27^r$, we have $P_r n_j equiv 0 mod 3$. Also $Q_r = 2^(4r+3) equiv -1 mod 3$. It remains to note that $D_r equiv 1 mod 3$ for every $r$.

  This last congruence follows by induction over the transitions inside the block. Each transition has numerator $a n + c$ with $a$ divisible by $3$ and $c equiv 1 mod 3$ for transitions ending at depth $0$ or $c equiv 0 mod 3$ for $0 arrow.r 1$, $c equiv 0 mod 3$ for $1 arrow.r 1$. The only contribution to the block's additive term modulo $3$ that survives the final return to depth $0$ is the final $1 arrow.r 0$ constant $7 equiv 1 mod 3$, or the one-step $0 arrow.r 0$ constant $1$. Thus $D_r equiv 1 mod 3$.

  Reducing $Q_r n_(j+1) = P_r n_j + D_r$ modulo $3$ gives $-n_(j+1) equiv 1 mod 3$, so $n_(j+1) equiv 2 mod 3$.
]

#proposition(name: "Bounded-Depth Real Expansion")[
  For a growth-B continuation prefix of length $N$ with depths $0 <= t_i <= T$, the affine multiplier from $m_0$ to $m_N$ is
  $ A_N / B_N
     = (9\/8)^N (3\/2)^(sum_(i=0)^(N-1) t_i) 2^(t_0-t_N). $
  In particular,
  $ A_N / B_N >= 2^(-T) (9\/8)^N. $
]
#proof[
  From the composed recurrence in the coding proposition below, the coefficient of $m_0$ in $m_N$ is
  $ A_N / B_N =
    product_(i=0)^(N-1) 3^(t_i+2) /
    product_(i=0)^(N-1) 2^(t_(i+1)+3). $
  This equals
  $ 3^(2N + sum_(i=0)^(N-1)t_i) /
    2^(3N + sum_(i=1)^N t_i). $
  Since $sum_(i=1)^N t_i = sum_(i=0)^(N-1)t_i - t_0 + t_N$, the displayed formula follows. If every $t_i <= T$, then $2^(t_0-t_N) >= 2^(-T)$ and $(3\/2)^(sum t_i) >= 1$, giving the lower bound.
]

#remark[
  This is an archimedean expansion statement, not a proof of bounded-depth termination. A positive integer orbit could grow along the expanding direction. The missing bounded-depth theorem is arithmetic: show that the congruence gates defining the branch cannot be satisfied forever by a fixed positive integer start.
]

#proposition(name: "Exact Zero-Depth Branch")[
  For a start with depth $t_0=0$, the first $L$ growth-B hops all have depth $0$ if and only if
  $ m_0 equiv -1 mod 8^L. $
  Thus the infinite all-zero depth branch has the unique $2$-adic code $m_0=-1$, and no positive integer realizes it forever.
]
#proof[
  On the zero-depth branch the continuation recurrence is
  $ m_(i+1) = (9m_i+1)\/8. $
  Hence, as long as the branch remains at depth $0$,
  $ m_i + 1 = (9\/8)^i (m_0+1). $
  The $i$-th state has depth $0$ and is growth-B exactly when $m_i equiv -1 mod 8$, i.e. $8 | m_i+1$. Substituting the displayed formula, this condition is
  $ 8^(i+1) | 9^i(m_0+1). $
  Since $9$ is odd, this is equivalent to $8^(i+1) | m_0+1$. Requiring this for all $0 <= i < L$ is therefore equivalent to $8^L | m_0+1$, which is the stated congruence.

  Taking $L arrow.r infinity$ gives $m_0 equiv -1 mod 8^L$ for every $L$, so the unique $2$-adic code is $m_0=-1$. This is not a positive integer.
]

#proposition(name: "Arbitrarily Long Finite Growth-B Chains")[
  For every $L >= 1$, there exists a positive odd starting value whose FMF trajectory begins with at least $L$ consecutive growth-B hops.
]
#proof[
  Take the least positive representative in the preceding proposition:
  $ m_0 = 8^L - 1, quad x_0 = 4m_0 - 1. $
  Then the first $L$ growth-B hops all have depth $0$. Explicitly,
  $ m_i = 9^i 8^(L-i) - 1 quad (0 <= i < L), $
  so each $m_i$ is positive, odd, and congruent to $-1 mod 8$.
]

#remark[
  This corollary rules out any proof strategy based on a uniform finite maximum for growth chains. The best plausible pointwise bounds must grow with the size of the starting value, such as the empirical $O(log x)$ epoch bounds in Section 7.
]

#proposition(name: "Logarithmic Lower Bound for Growth-B Chain Bounds")[
  Any universal upper bound of the form
  $ op("growth_chain_length") <= c log_2(m_0) + O(1) $
  must have $c >= 1\/3$.
]
#proof[
  The explicit family in the previous proposition has $m_0 = 8^L - 1$ and growth-B chain length at least $L$. Since
  $ log_2(m_0) = log_2(8^L - 1) = 3L + O(1), $
  any bound $L <= c log_2(m_0) + O(1)$ requires $c >= 1\/3$.
]

#proposition(name: "Exact 2-adic Coding of Infinite Growth-B Chains")[
  For every infinite sequence of nonnegative integers $(t_0, t_1, t_2, dots)$ there is a unique $2$-adic integer $m(t_0, t_1, dots) in ZZ_2$ such that any infinite growth-B chain with this depth sequence must start with $m_0 = m(t_0, t_1, dots)$. Moreover, an infinite growth-B chain in positive integers with this depth sequence exists if and only if this $2$-adic code is a positive odd integer.
]
#proof[
  Let
  $ a_i = 3^(t_i+2), quad b_i = 2^(t_(i+1)+3). $
  The continuation equations are
  $ b_i m_(i+1) = a_i m_i + 1. $
  Composing the first $n$ equations gives
  $ B_n m_n = A_n m_0 + C_n, $
  where $A_0 = B_0 = 1$, $C_0 = 0$, and
  $ A_(n+1)=a_n A_n, quad B_(n+1)=b_n B_n, quad C_(n+1)=a_n C_n + B_n. $
  Since every $A_n$ is odd, it is invertible modulo $B_n$, and any integer solution must satisfy
  $ m_0 equiv - C_n A_n^(-1) mod B_n. $
  The moduli $B_n$ are increasing powers of $2$, and these congruence classes are nested because the equations are obtained by extending the same recurrence one more step. Therefore they define a unique element
  $ m(t_0,t_1,dots) in ZZ_2. $

  If a positive integer growth-B chain exists, its starting parameter $m_0$ satisfies every congruence, hence equals this $2$-adic code. Conversely, if the code is a positive odd integer, then it satisfies all congruences. The forward recurrence then defines positive integers $m_i$ for all $i$. Each $m_i$ is odd: if some $m_i$ were even, then $3^(t_i+2)m_i+1$ would be odd and could not be divisible by the even factor $2^(t_(i+1)+3)$ needed for the next equation. Therefore the equations force each hop to be a growth-B continuation with the prescribed next depth. Thus the code is a positive odd integer exactly in the exceptional case.
]

#remark[
  This proposition is the sharpest current reduction of the pointwise gap. The Quartering Law says the set of length-$n$ prefixes has density $4^(-n)$; the coding proposition says an infinite obstruction is a single $2$-adic point selected by an infinite depth word. Collatz via this route requires proving that none of these $2$-adic points is a positive integer.
]

#proposition(name: "Integer-Code Boundedness Criterion")[
  Let $r_n$ be the least nonnegative residue of the length-$n$ prefix code modulo $B_n$. The infinite $2$-adic code $m(t_0,t_1,dots)$ is a nonnegative ordinary integer if and only if the integer sequence $r_n$ is bounded. Equivalently, this happens if and only if $r_n$ is eventually constant. In that case the eventual constant is exactly that ordinary integer.
]
#proof[
  If the code equals a nonnegative integer $M$, then for every $n$ we have $r_n equiv M mod B_n$. Since $B_n arrow.r infinity$, once $B_n > M$ the least nonnegative residue is $r_n = M$. Thus $r_n$ is eventually constant.

  If $r_n$ is bounded, say $r_n <= R$ for all $n$, then for any $m > n$ with $B_n > R$, the nesting relation $r_m equiv r_n mod B_n$ forces $r_m = r_n$ as ordinary integers. Hence the sequence is eventually constant. Conversely, eventual constancy is plainly bounded.

  Finally, if $r_n$ is eventually constant with value $M$, then $M$ satisfies every prefix congruence modulo $B_n$. Hence the inverse-limit code equals the ordinary integer $M$ in $ZZ_2$.
]

#remark[
  This criterion gives a concrete way to attack the remaining obstruction: prove that for every non-eventually-periodic depth word, the prefix residues $r_n$ are unbounded. The constant-zero word illustrates the distinction: its residues are $2^(3n)-1$, converging $2$-adically to $-1$, not to a positive integer.
]

#proposition(name: "Prefix Digit Recurrence")[
  Let $r_n$ be the prefix residue modulo $B_n$, and write
  $ r_(n+1) = r_n + d_n B_n $
  with $0 <= d_n < b_n = 2^(t_(n+1)+3)$. If
  $ s_n = (A_n r_n + C_n) / B_n, $
  then
  $ d_n equiv - (3^(t_n+2) s_n + 1) (A_(n+1))^(-1) mod b_n. $
  In particular, the prefix residue stabilizes at step $n$ precisely when
  $ 3^(t_n+2) s_n + 1 equiv 0 mod 2^(t_(n+1)+3). $
]
#proof[
  The extension from length $n$ to length $n+1$ requires
  $ A_(n+1) r_(n+1) + C_(n+1) equiv 0 mod B_(n+1), $
  where $A_(n+1)=3^(t_n+2) A_n$, $B_(n+1)=B_n b_n$, and $C_(n+1)=3^(t_n+2) C_n + B_n$. Substitute $r_(n+1)=r_n+d_n B_n$ and divide by $B_n$:
  $ 3^(t_n+2) (A_n r_n + C_n) / B_n + 1 + A_(n+1)d_n equiv 0 mod b_n. $
  This is the stated congruence. Since $A_(n+1)$ is odd, it is invertible modulo $b_n$. The residue is unchanged exactly when $d_n=0$, giving the final criterion.
]

#proposition(name: "Zero-Digit Tail Equivalence")[
  Fix a finite depth prefix and write
  $ s_n = (A_n r_n + C_n) / B_n. $
  For any extension depths $t_(n+1), t_(n+2), dots$, a run of zero extension digits
  $ d_n = d_(n+1) = dots = d_(n+L-1) = 0 $
  is equivalent to the existence of integers $s_(n+1), dots, s_(n+L)$ satisfying
  $ 2^(t_(j+1)+3) s_(j+1) = 3^(t_j+2) s_j + 1
     quad (n <= j < n+L). $
  Consequently, an eventually constant prefix-residue tail is equivalent to an infinite positive integer orbit in the growth-B continuation domain, starting from the auxiliary state $s_n$.
]
#proof[
  The preceding proposition shows that $d_j=0$ is equivalent to
  $ 3^(t_j+2) s_j + 1 equiv 0 mod 2^(t_(j+1)+3). $
  When this divisibility holds, define
  $ s_(j+1) = (3^(t_j+2) s_j + 1) / 2^(t_(j+1)+3). $
  Repeating this construction gives exactly the displayed recurrence, and reversing the calculation shows that any such recurrence gives zero extension digits.

  If the zero digits continue forever, then every $s_j$ must be odd: if some $s_j$ were even, then $3^(t_j+2)s_j+1$ would be odd and could not be divisible by $2^(t_(j+1)+3)$. The same observation rules out $s_j=0$, so the tail is a positive odd integer continuation orbit. Conversely, if the auxiliary state admits such an infinite positive odd continuation, setting every later digit to zero keeps $r_j$ constant. The 2-adic code is then the ordinary integer $r_n$.
]

#remark[
  The digit formulation is therefore not an easier separate problem; it is an exact restatement of the positive-integer continuation obstruction in a different coordinate. Finite zero-digit runs do occur, so the target cannot be strengthened to "$d_n$ is always nonzero." The necessary theorem is genuinely tail-based: for every non-eventually-periodic depth word, $d_n$ must be nonzero infinitely often. Computations in `explore46_infinite_code.py` and `explore48_bounded_depth_beam.py` search for long zero-digit runs and small prefix residues in bounded depth alphabets. The direct integer search in `explore47_integer_code_search.py` found no positive-integer continuation code for odd $m_0 <= 10^6$ and $0 <= t_0 <= 24$; the longest continuation tail in that bounded scan had length $11$. This is supporting evidence only, not a substitute for the missing tail theorem.
]
