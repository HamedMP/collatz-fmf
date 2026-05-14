#import "../lib/theorem.typ": *

= Reduced ${0,1}$ Gap Codes

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

== Reduced gap terminal windows

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

== Reduced gap prefix minima

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
