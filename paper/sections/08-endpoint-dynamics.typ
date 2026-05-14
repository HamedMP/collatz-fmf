#import "../lib/theorem.typ": *

= Endpoint Dynamics and Growth-B Coding

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

== Growth-B coding endpoint

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
  This corollary rules out any proof strategy based on a uniform finite maximum for growth chains. The best plausible pointwise bounds must grow with the size of the starting value, such as the empirical $O(log x)$ epoch bounds in Section 10.
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
