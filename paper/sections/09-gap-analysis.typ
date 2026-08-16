#import "../lib/theorem.typ": *

= What This Does and Does Not Prove

This section provides a direct accounting of the results in this paper: what has been established rigorously, what remains open, and why the remaining gap is genuinely hard. The Collatz conjecture has attracted a large body of work that overstates its conclusions; the purpose here is to avoid that failure mode.

== What is proved

The following results are established by exact algebraic arguments, not heuristic or statistical reasoning.

+ *Exact FMF formulas (Theorem A).* For every odd $x$, the number of Collatz steps to the first multiple of four, and the value of that multiple, are given by closed-form expressions depending on $x mod 4$ and $v_2(k+1)$ where $x = 4k+3$. The FMF value for Type B inputs with $k+1 = 2^t m$ ($m$ odd) is $2(3^(t+2) m - 1)$. These are algebraic identities, not statistical observations.

+ *State distribution (Theorem B).* In natural density over the free parameter in each input state, the distribution of the FMF hop output --- its mod-4 class, its $t$-parameter, and its $v_2$ parameter --- is identical regardless of the input state. This follows from the structure of 2-adic inverses: since $3^(t+2)$ is a unit in $ZZ_2$, multiplication by $3^(t+2)$ permutes residue classes. This is _not_ a heuristic independence assumption about a single trajectory; it is a residue-counting theorem.

+ *Fractional-moment contraction (Theorem C).* The FMF hop ratio satisfies the exact asymptotic natural-density formula $EE[R^0.53] approx 0.8638 < 1$. The critical exponent is exactly $alpha^* = 1$: the moment series at $alpha = 1$ evaluates to the rational identity $M(1) = 1\/4 + 3\/16 + 9\/16 = 1$, the FMF form of the classical fact that the Syracuse first-moment heuristic is exactly critical. This is a rigorous average contraction statement for the FMF density model, not a pointwise contraction theorem.

+ *The Quartering Law (Theorem D).* Growth-B chains have continuation density factor exactly $1\/4$ per step. Among odd starts, the density of strict growth-B chains of length at least $k$ is $4^(-k)$; conditioned on Type B starts it is $2\/4^k$. The proof uses only mod-8 arithmetic and the unit structure of $3^(t+2)$ in $ZZ_2$.

+ *Binary-depth and reduced-gap obstruction reductions.* Sections 6--8 turn the first bounded-depth pointwise obstructions into explicit positive-integer partial-map problems. The binary return map has exact survival density $(2\/15)^L$, start-count and prefix-count formulas, terminal-window identities, weighted terminal-window bounds, and a sharpened endpoint theorem splitting any remaining obstruction into a bounded higher-complexity finite-alphabet word or an unbounded $3$-adic reset-spike. The reduced ${0,1}$ gap map has the parallel density $112^(-L)$, terminal-window identities, and the same bounded/unbounded dichotomy with reset target $-1\/128$ in $QQ_3$.

+ *External cycle bounds.* Simons and de Weger @simons2005 give strong lower bounds for nontrivial Collatz cycles using transcendental number theory and computation. These results support, but are logically separate from, the FMF density analysis.

== What is not proved

This paper does not prove the Collatz conjecture. Specifically:

- *Not every trajectory is shown to converge.* The density bounds show that the set of odd integers with strict growth-B chains of length $>= k$ has natural density $4^(-k)$, which tends to zero. But natural density zero does not mean the set is empty. In fact, the explicit all-zero branch gives infinitely many starts
  $ x_L = 4(8^L - 1) - 1 $
  whose trajectories begin with at least $L$ consecutive growth-B hops. Thus any universal logarithmic upper bound for growth-B chain length must have constant at least $1\/3$ in base-$2$ logarithms (equivalently $2\/3$ in base-$4$ logarithms). The exceptional finite-shadow set is provably _infinite_ in this weak sense; what we show is that it is negligibly thin in natural density at each fixed length.

- *Growth phases are not proved to terminate for every starting point.* The growth chain bound is verified empirically (zero violations across $1.5 times 10^6$ growth chains, up to 60-bit starting values) but not proved. A single counterexample --- an odd integer whose growth chain never terminates --- would disprove the Collatz conjecture.

- *The fractional-moment contraction is an average statement.* The bound $EE[R^0.53] < 1$ means that hops contract in natural-density average. But the worst-case single-hop ratio grows without bound: for $x = 2^n - 1$ with large $n$, the hop ratio grows exponentially in $n$ before later recovery. No finite number of hops $k$ is currently known to achieve a uniform pointwise contraction $max_x L(F^k (x))\/L(x) < 1$.

== Comparison with Tao's result

Tao @tao2022 proves that almost all Collatz orbits attain almost bounded values, in the sense of logarithmic density. The present results and Tao's address different aspects of the same problem, and the comparison is instructive.

*Density notion.* Tao works with logarithmic density (weighting integers by $1\/n$), while the Quartering Law is stated in natural density over residue classes. Natural density is the stronger notion when the same event is being measured. Here, however, the events are different: Tao's result is about the _values attained_ by orbits, while the present result is about the _structure of growth-B phases_. These are complementary statements, not a direct dominance claim.

*Decay rate.* Tao's theorem controls a much more global orbit-minimum event. The Quartering Law gives exponential decay for the narrower growth-B-chain event: the fraction among odd starts with growth-B length $>= k$ is $4^(-k)$. This is a sharp elementary bound for that mechanism, but it does not imply Tao's theorem and Tao's theorem does not imply it.

*Methods.* Tao's proof uses entropy methods in 3-adic analysis, Syracuse random variables, and concentration inequalities. The core FMF density proof uses elementary mod-8 arithmetic and the unit structure of 2-adic integers; later obstruction-class exclusions use additional combinatorial and symbolic-dynamical input.

*The related wall.* Despite these differences, both approaches encounter a density-to-pointwise barrier: neither argument, as stated, crosses from density control to all integer trajectories. In Tao's framework, the obstacle is that logarithmic-density exceptional sets can be nonempty. In the FMF framework, the obstacle is that residue-density and Haar-measure arguments do not exclude exceptional integer orbits. The two formulations of the gap are closely related.

== The $5n+1$ litmus test

A useful test for any framework claiming insight into the Collatz conjecture is whether it can distinguish $3n+1$ (conjectured to converge) from $5n+1$ (not globally convergent; for example, $13$ lies in a nontrivial cycle under the usual $5n+1$ dynamics).

The FMF framework passes this test at the average-drift level but not at the pointwise-convergence level. Specifically:

- *State independence holds for $5n+1$.* The FMF hop output distribution for $5n+1$ is state-independent, for the same algebraic reason: $5^(t+2)$ is a 2-adic unit.
- *The $v_2$ geometric distribution holds for $5n+1$.* The distribution $P(v_2 = j) = 1\/2^j$ is a property of 2-adic units, not of the specific multiplier.
- *The same residue-counting tools largely persist for $5n+1$.* Many valuation and output-distribution calculations depend only on the multiplier being a 2-adic unit.

The discriminant is the _contraction channel_. For the map $a n + 1$, Type A hops (inputs $equiv 1 mod 4$) have ratio $a\/4$ before the $v_2$ correction. The integer $3$ is the only odd value where $a\/4 < 1$. This means:

- For $3n+1$: Type A hops _always_ shrink (ratio $3\/4$ before further division). Since Type A hops occur with probability $1\/2$, half of all hops provide guaranteed contraction.
- For $5n+1$: Type A hops have ratio $5\/4 > 1$. No hop type provides guaranteed contraction. The expected drift is positive, correctly predicting divergence.

The FMF framework thus identifies a concrete structural reason why the $3n+1$ drift is negative while the $5n+1$ drift is positive. But this identification is at the level of density averages, not at the level of individual trajectories. The gap between the two remains.

== Why the gap is hard

The gap between "almost all orbits converge" and "all orbits converge" is not a bookkeeping limitation of this paper. It is the central obstruction for the present density-and-reduction approach.

*Tao's barrier.* Tao has observed that any proof of the Collatz conjecture must either exploit existing results in transcendence theory or diophantine approximation, or contribute genuinely new methods to one of these areas. The FMF framework's 2-adic analysis, while providing structural insight, does not engage with transcendence theory. It establishes equidistribution of $3^n mod 2^K$ for fixed $K$ and growing $n$, but this is a standard fact about multiplicative groups modulo prime powers. The hard part --- controlling what happens for $K$ growing with $n$ --- requires quantitative equidistribution estimates that are not available from mod-$8$ arguments alone.

*Baker's theorem.* One might hope that Baker's theorem on linear forms in logarithms could close the gap, since it provides lower bounds on $|a log 2 - b log 3|$. For a growth chain of length $k$, the accumulated growth is approximately $3^(k(t+2))\/2^(2k)$, and the question is whether this can remain close to $1$ (preventing descent). Baker's theorem gives $|a log 2 - b log 3| > C \/ b^mu$ for effective constants $C, mu$. However, for the actual growth chains arising in FMF dynamics, the linear forms $a log 2 - b log 3$ are vastly larger than Baker's lower bound. Baker's theorem bounds the wrong thing: it controls archimedean proximity (how close $2^a$ is to $3^b$ in $RR$), while the FMF dynamics are governed by 2-adic proximity (how close $3^n$ is to $1$ in $ZZ_2$). These are complementary, not interchangeable, conditions.

*A precise remaining question.* One sharp obstruction exposed by the FMF framework is the possibility of integer orbits that remain inside the growth-B domain for unexpectedly long times:

#conjecture(name: "Growth-B Domain Emptiness")[
  The growth-B map $m arrow.r.bar op("odd_part")((3^(t+2) m + 1)\/8)$, restricted to the growth-B domain of $ZZ_2$ (those $m$ with $3^(t+2) m equiv 7 mod 8$ and output again in the growth-B domain), has no infinite orbit in $ZZ$.
]

Equivalently: does there exist an odd positive integer $m_0$ such that the growth-B iteration, started at $m_0$, never exits the growth-B domain? Such an orbit would be a serious obstruction to FMF descent. Proving nonexistence, or proving a quantitative bound on how long integer orbits can remain in this domain, would materially strengthen the approach. By itself, mere termination of growth-B chains is not yet a complete proof of Collatz; one also needs pointwise recovery after mixed growth and shrinkage phases.

The 2-adic coding lemmas in Sections 6--8 suggest a useful intermediate target. Fix $T >= 0$ and restrict the depth word to the finite alphabet ${0, dots, T}$. If one could prove that the least nonnegative prefix residues $r_n$ tend to infinity uniformly over all such bounded-depth words, then no positive-integer infinite growth-B obstruction could have bounded depth. Any remaining obstruction would have to use depths $t_i$ that are unbounded. Computations in `explore48_bounded_depth_beam.py` support this bounded-depth subproblem for small $T$, but the search is beam-pruned and is not a proof.

A tempting finite-state version of this idea does not suffice. Projecting the continuation map to states $(t, m mod 2^K)$ leaves persistent cycles even when $T=0$: the cycle at $m equiv -1 mod 2^K$ is just the finite shadow of the 2-adic code $-1$, not a positive integer obstruction. Thus the bounded-depth problem cannot be solved by residue-graph acyclicity alone. One must distinguish positive ordinary integers from nonpositive or nonintegral 2-adic limit points.

The first nontrivial bounded-depth case, $T=1$, can be compressed further. Section 6 shows that binary-depth paths reduce to four affine maps on a normalized parameter $n$, and that every return block $0 arrow.r 1^r arrow.r 0$ imposes exactly one residue class modulo $2^(4r+3)$. Thus the $T=1$ obstruction is itself an exact $2$-adic coding problem, now indexed by the run lengths $r_0, r_1, dots$ of ones between zero-depth returns. Proving that no non-eventually-periodic return-block code is a positive ordinary integer would settle the binary-depth case.

The closed gate and return reparameterization in Section 6 sharpen this into a quantitative target. For a return block of length $r_j$, the reparameterized variable $w_j$ satisfies
$ 33n_j+32 = 16^(r_j)w_j $
and one fixed residue class modulo $264$ determined by $r_j$. The next return is governed by
$ 9 dot 27^(r_j)w_j + 1 = 2^(4r_(j+1)+3)w_(j+1). $
Equivalently, the depth-$0$ return states are governed by one explicit partial map $T(n)$ read from the factorization of $33n+32$. Thus a proof that this partial map has no infinite positive orbit, or equivalently that the least return-code prefix residues grow without bound as the number of return blocks tends to infinity, would settle the full $T=1$ case. Section 6 sharpens this equivalence: if the global minimum $mu_L$ of all length-$L$ return-prefix residues fails to diverge, finite-height compactness produces an infinite bounded-residue return word and hence an ordinary return code. The dual fixed-height statement is equivalent: every fixed height bound $B$ must admit only finitely many return blocks. The all-zero return branch shows the best possible bound is logarithmic in $B$, with constant at least $1\/3$ in base-$2$ logarithms. Computations suggest $mu_L arrow.r infinity$, but no proof is known; this is the most concrete current subproblem.

The return-code critical-series formulation shows the same obstruction from another angle. Every infinite return-length word defines rational partial sums with real limit in $[-1,0)$ and $2$-adic limit equal to the return code. Periodic return words are excluded because their critical limits are rational and negative. The unresolved possibility is a nonperiodic return word whose $2$-adic critical limit is nevertheless a positive ordinary integer.

Equivalently, for some fixed positive integer $M$, the divisibilities $v_2(P_N M + D_N) >= 3N + 4(r_0+dots+r_(N-1))$ would have to hold for every prefix. This is the current Diophantine form of the return-code obstruction.

The landing-envelope lemmas rule out one broad family of such words: return lengths cannot contain spikes that outgrow the accumulated expansion factor $(9\/8)^N(27\/16)^(r_0+dots+r_(N-1))$. Thus any remaining unbounded return-length obstruction must be quantitatively balanced, not merely nonperiodic.

The binary return survival density is exact: the set of depth-$0$ parameters admitting $L$ consecutive binary return blocks has density $(2\/15)^L$. Thus the $T=1$ obstruction is already a density-zero phenomenon. The gap is again pointwise: density zero does not exclude a single positive integer whose return-code residues remain bounded forever.

One precise way to close this pointwise gap would be a uniform prefix-counting estimate. Let $N_R(B,L)$ count length-$L$ return words whose least prefix residue is at most $B$. If
$ N_R(B,L) <= C(B+1)rho^L $
for some $rho<1$ and all $B,L$, then the fixed-height survival depth would be $O(log B)$. The density theorem suggests $rho=2\/15$ as the natural value, but the missing ingredient is a discrepancy bound strong enough to hold uniformly in the finite-height regime.

This is not merely an artifact of counting prefix words instead of starts. Section 6 gives an exact start-count formula: the number $A_R(B,L)$ of ordinary starts $0 <= n <= B$ surviving $L$ return blocks differs from $N_R(B,L)$ by at most $(B+1)(2\/15)^L$. Thus, at the natural rate, prefix-counting and ordinary-start survival bounds are equivalent up to constants.

Section 6 also reduces the all-height estimate to a critical-rank estimate. Sort length-$L$ return words by their least prefix residues. The desired counting theorem is equivalent to bounding the rank of each word by a constant multiple of $(R_w+1)(2\/15)^L$. This is the most compact current form of the return-code obstruction.

The backward formulation adds an important asymmetry. The binary return partial map is backward-injective: a terminal return state has at most one predecessor across all return lengths. Along a backward return path, height contracts by $(8\/9)^L(16\/27)^S$, where $L$ is the number of return blocks and $S$ is their total return length; equivalently, forward surviving paths force terminal-height escape by the reciprocal factor. Thus return-prefix clustering is not caused by forward merging; it is a rank-versus-height problem among distinct terminal states.

The terminal-window identity makes the stopping-time target exact. If $E_w=(9\/8)^L(27\/16)^S$ is the expansion factor for a return word and $U_w$ is the terminal state reached from the least prefix residue $R_w$, then $R_w <= U_w\/E_w < R_w+1$, so $R_w=floor(U_w\/E_w)$. Thus $R_w <= B$ is equivalent to $U_w\/E_w < B+1$. A low return prefix is exactly a path whose normalized terminal height remains in this low unit-width window; a stopping-time proof would have to count these windows uniformly in $B$ and $L$.

Equivalently, the critical-rank criterion can be written without mentioning prefix residues: order length-$L$ words by $floor(U_w\/E_w)$ and prove that the rank of each word is $O((floor(U_w\/E_w)+1)(2\/15)^L)$.

The ordinary-start formula also has this terminal form: replace $R_w$ by $floor(U_w\/E_w)$ in the start-count sum. Thus the terminal-window formulation controls both prefix ranks and actual ordinary survivors.

The high-moment estimates in Sections 6--7 give partial control of this terminal-window problem. The return and reduced-gap expansion-pressure sums are subcritical at cubic order, so expansion-weighted word mass decays exponentially. On the return side, terminal injectivity also gives the weighted bound
$ sum_(|w|=L, R_w <= B) E_w^(-theta) <= (B+1)^theta zeta(theta) $
for every $theta>1$, and the stronger cutoff count
$ N_R(B,L;X) <= ceil(X(B+1))-1. $
For the reduced gap system, backward contraction gives the weighted bound
$ sum_(|w|=L, S_w <= B) E_w^(-theta) <= B^theta (43\/81)^L zeta(theta-1) $
for $theta>2$, including merge multiplicity; the analogous low-expansion count has an extra multiplicity factor controlled by the same contraction. The weighted estimates also give ordinary counts on each fixed dyadic expansion shell, at the cost of a factor exponential in the shell index. Fixed shells themselves only occur at bounded prefix depth, so an infinite obstruction must pass through arbitrarily high shells. These are genuine constraints on low normalized windows, but they still do not bound the full unweighted rank.

For an infinite return word, the pointwise obstruction is exactly boundedness of these rounded terminal coordinates. The selected return code is a nonnegative ordinary integer if and only if $floor(U_N\/E_N)$ is bounded, equivalently eventually constant, along the prefixes.

Moreover these rounded terminal coordinates are nondecreasing. If $Q_N$ is the current prefix modulus, then
$ floor(U_(N+1)\/E_(N+1)) = floor(U_N\/E_N) + e_N Q_N $
with $e_N >= 0$. Thus the pointwise obstruction is precisely an infinite zero-increment tail in these terminal coordinates.
The local zero-step criterion says that $e_N=0$ exactly when the auxiliary terminal state $U_N$ itself admits the same next return-block step.
More generally, a finite suffix has zero terminal increments exactly when $U_N$ lies in the ordinary return prefix-residue class of that suffix.
For an infinite suffix, this becomes a nested congruence condition: $U_N$ must lie in every prefix class selected by the future return word, equivalently it must be the positive ordinary return code of that suffix.
Every shifted suffix must then also have a positive ordinary code: the shifted codes are exactly the later auxiliary states, and they obey the same expanding return recurrence.
For any fixed finite suffix, the zero-increment condition is one residue class whose density is the reciprocal of the suffix modulus. For any fixed infinite suffix, the shadowing set is a single $2$-adic point of Haar measure zero.
After summing over all length-$L$ suffixes, the density of auxiliary states with $L$ consecutive return zero-increments is exactly $(2\/15)^L$.
Every finite return-length word is locally realizable as such a zero-increment terminal word from some auxiliary state, so finite forbidden-pattern arguments still cannot settle the obstruction.

The zero-increment formulation is not a new independent problem: by the auxiliary-state equivalence, such a terminal tail is exactly an infinite positive orbit of the same return partial map, now started from the terminal auxiliary state $U_N$.
For any fixed finite prefix, this tail is unique if it exists, because the return partial map has a unique ordinary itinerary from a fixed auxiliary state.

Along any finite zero-increment return tail, the auxiliary terminal state still escapes:
$ U_(N+L) > (9\/8)^L(27\/16)^S U_N. $
Thus a hypothetical obstruction has a distinctive shape: the rounded terminal coordinate is eventually constant while the auxiliary terminal state grows exponentially along the same suffix.

The suffix cannot be eventually periodic. If it were, the terminal zero-increment equivalence would give an eventually periodic positive return orbit, already excluded in Section 6. The terminal-tail dichotomy sharpens this: after the terminal coordinate becomes constant, either the return lengths are bounded and form a non-eventually-periodic word over a finite alphabet, or they are unbounded and the later auxiliary return states have a subsequence converging to $-85\/88$ in $QQ_3$.

The remaining binary case now splits into two explicit subcases. If return lengths are bounded, then an obstruction is a bounded-alphabet non-eventually-periodic return word whose prefix residues nevertheless stay bounded; equivalently, for some fixed alphabet ${0,dots,R}$ the restricted return minima $mu_L^(<=R)$ fail to diverge. The Morse-Hedlund criterion sharpens "non-eventually-periodic": if the tail uses $q$ distinct return lengths, its factor complexity must be at least $m+q-1$ at every block length $m$. Section 6 also rules out every fixed-count positive-label stratum and, more generally, every bounded-defect perturbation of an eventually periodic return template. Thus a bounded-alphabet obstruction must use infinitely many positive labels and must drift unboundedly far from every periodic shadow, not merely introduce finitely many delayed spikes. If return lengths are unbounded, every long return block is a reset-spike: its incoming state is at least $(5 dot 16^r-32)\/33$ while its output is congruent to $-85\/88$ modulo $3^(3r+1)$. The bounded case with unbounded defect from periodic shadows and the unbounded reset-spike case remain the present endpoint of the exact binary-depth reduction.

The smallest bounded-alphabet subcase, return lengths in ${0,1}$, can be reduced one level further. Between length-$1$ returns, let $k_j$ be the number of intervening zero returns and put $a_j=(n_j+1)\/3$ immediately after the $j$-th length-$1$ return. Section 7 gives the gap map
$ a_(j+1) = (243\/128)(9\/8)^(k_j) a_j - 1\/128, $
with an exact gate read from $a_j=8^(k_j)b_j$ and
$3 dot 9^(k_j)b_j equiv 49 mod 128$. Every finite gap word occurs, every eventually periodic gap itinerary has a rational fixed point between $0$ and $1$, and the survival density for $L$ complete gap transitions is $112^(-L)$. Thus even this first nontrivial finite alphabet has the same endpoint: only non-eventually-periodic infinite gap words with bounded prefix residues remain open.

The critical-series formulation makes this endpoint sharper. For any infinite gap word, the same rational partial sums converge in $RR$ to a value at most $1\/115$, while converging in $QQ_2$ to the selected $2$-adic gap code. Eventually periodic words give rational limits below $1$ and are excluded. The remaining question is whether a genuinely nonperiodic critical series can converge $2$-adically to a positive ordinary integer despite having real critical value below $1$.

Equivalently, for some fixed positive integer $A$, the divisibilities $v_2(A_N A - C_N) >= 7N + 3(k_0+dots+k_(N-1))$ would have to hold for every prefix.

The corresponding gap envelope rules out zero-gap spikes that outgrow $(243\/128)^N(9\/8)^(k_0+dots+k_(N-1))$. Therefore the remaining ${0,1}$ case is not arbitrary nonperiodicity; it is balanced nonperiodic critical-series landing.

The same prefix-counting route applies here. If $N_G(B,L)$ counts length-$L$ gap words whose least prefix residue is at most $B$, a bound
$ N_G(B,L) <= C B rho^L $
with $rho<1$ would imply finite fixed-height survival for every $B$. The exact gap survival density suggests $rho=1\/112$, but again the open problem is turning density into a uniform finite-height discrepancy theorem.

Again, this can be stated in ordinary-start language without changing the substance. The exact gap start-count formula gives $N_G(B,L) <= A_G(B,L) <= N_G(B,L)+B 112^(-L)$, so a uniform prefix-counting bound at any rate $rho >= 1\/112$ is equivalent, up to constants, to the corresponding ordinary-start survival bound.

Equivalently, after sorting length-$L$ gap words by least prefix residue, one must prove a rank bound of order $S_w 112^(-L)$ for every finite gap word. The finite computations suggest that the worst clusters occur at specific critical residues, not necessarily at the global minimum residue.

Here forward merging is real but structured. Section 7 shows that all immediate backward preimages of a fixed gap terminal state form a finite geometric chain with ratio $8\/9$, and the number of such preimages is exactly controlled by $v_3(128a'+1)$. Along a backward gap path, height contracts by $(43\/81)^L(8\/9)^K$, where $K$ is the total zero-gap length; equivalently, forward surviving paths force terminal-height escape by $(81\/43)^L(9\/8)^K$. The immediate merge multiplicity is only logarithmic in terminal height, and the total immediate preimage mass is at most $(43\/9)$ times the terminal height. Thus any gap-rank proof must control repeated visits near the $3$-adic point $-1\/128$ while respecting the real backward contraction.

The gap terminal-window identity is analogous but slightly sharper: if $E_w=(243\/128)^L(9\/8)^K$ and $u_w$ is the terminal state reached from the least gap-prefix residue $S_w$, then $S_w-1\/115 < u_w\/E_w < S_w$, so $S_w=ceil(u_w\/E_w)$. Thus $S_w <= B$ is equivalent to $u_w\/E_w < B$. Low gap prefixes are exactly paths whose normalized terminal height remains in this low interval of width less than $1\/115$.

Equivalently, order length-$L$ gap words by $ceil(u_w\/E_w)$ and prove that the rank of each word is $O(ceil(u_w\/E_w)112^(-L))$.

As in the return case, the ordinary-start formula is obtained by replacing $S_w$ with $ceil(u_w\/E_w)$ in the exact start-count sum.

For an infinite gap word, the selected gap code is a positive ordinary integer if and only if $ceil(u_N\/E_N)$ is bounded, equivalently eventually constant, along the prefixes.

Again the rounded terminal coordinates are nondecreasing:
$ ceil(u_(N+1)\/E_(N+1)) = ceil(u_N\/E_N) + d_N H_N $
with $d_N >= 0$. The reduced-gap obstruction is therefore an eventual zero-increment tail in the terminal coordinate.
Here $d_N=0$ exactly when the auxiliary terminal state $u_N$ itself admits the same next reduced gap-map step.
More generally, a finite suffix has zero terminal increments exactly when $u_N$ lies in the ordinary gap prefix-residue class of that suffix.
For an infinite suffix, $u_N$ must lie in every nested gap prefix class selected by the future word, equivalently it must be the positive ordinary gap code of that suffix.
Every shifted suffix must also have a positive ordinary code, given by the later auxiliary gap states, and these shifted codes obey the same expanding gap recurrence.
For any fixed finite suffix this is one residue class of density equal to the reciprocal suffix modulus; for a fixed infinite suffix the shadowing set is a single $2$-adic point.
After summing over all length-$L$ suffixes, the density of auxiliary states with $L$ consecutive gap zero-increments is exactly $112^(-L)$.
Every finite zero-gap word is locally realizable as a zero-increment terminal word from some auxiliary state.

Again this is the same obstruction in terminal coordinates: an eventual zero-increment terminal tail is equivalent to an infinite orbit of the reduced gap map starting from the auxiliary terminal state $u_N$.
For any fixed finite gap prefix, such a tail is unique if it exists.

Along any finite zero-increment gap tail, the auxiliary terminal state satisfies
$ u_(N+L) >= (81\/43)^L(9\/8)^K u_N. $
So the reduced-gap obstruction also has constant rounded coordinate but growing auxiliary terminal height.

Here too the suffix cannot be eventually periodic, by the corresponding periodic gap-itinerary exclusion. The gap terminal-tail dichotomy gives the same bounded/unbounded split: bounded zero-gap lengths leave only a finite-alphabet non-eventually-periodic terminal tail, equivalently failure of divergence for some restricted gap minimum $nu_L^(<=K)$; if such a tail uses $q$ distinct gap lengths, its factor complexity is at least $m+q-1$ at every length. Sections 7--8 rule out every fixed-count positive-label stratum and every bounded-defect perturbation of an eventually periodic zero-gap template here as well. Thus a remaining bounded gap obstruction must contain infinitely many positive zero-gap lengths and must drift unboundedly far from every periodic shadow. Unbounded zero-gap lengths are again reset-spikes: the incoming gap state is at least $8^k$ while the following state is congruent to $-128^(-1)$ modulo $3^(2k+5)$.

The same backward analysis gives a weighted contraction not visible from raw branch counts: return backward fibers contract every positive power moment, while gap backward fibers contract every $theta$-moment satisfying $(43\/81)^theta+(8\/9)^theta<1$ (threshold approximately $2.28216$). In particular, the gap backward map contracts cubic mass, with the full immediate backward fiber having cubic mass at most $(43^3)/(729 dot 217)$ times the terminal cubic mass. This suggests a possible potential-theoretic route to the rank bound, but it is not yet a proof of the needed uniform finite-height discrepancy theorem. Direct finite-height diagnostics show that normalized cubic mass of low prefix frontiers can still grow, so an additional terminal-height or stopping-time estimate is needed.

The partial-map equivalence makes the deterministic form even simpler: for a fixed positive normalized state $a$, the next gap length and the next state are unique whenever a transition exists. Thus the ${0,1}$ endpoint is precisely the assertion that this explicit partial map has no infinite positive orbit. Equivalently, the global minimum $nu_L$ of all length-$L$ gap-prefix residues must tend to infinity. If $nu_L$ stayed bounded, the finite-height criterion would give an infinite bounded-residue gap word and therefore a positive ordinary gap code; equivalently, every fixed height bound must have finite gap survival depth. The all-zero gap branch again fixes the scale: any logarithmic survival-depth bound must have constant at least $1\/7$. In the latest direct scan, no start $a <= 5,000,000$ survives more than three complete gap transitions; this is evidence only, not a proof.

The 2-adic expansion property (Proposition 5.2) shows that the growth-B map expands residue precision on each fixed branch, explaining the density decay. But $ZZ$ has Haar measure zero in $ZZ_2$. Closing the pointwise gap would require new mathematics: either effective equidistribution results for expanding maps on $ZZ_2$ that apply to integer orbits, or $p$-adic Diophantine estimates that constrain how long an integer orbit can remain in a prescribed region of $ZZ_2$.

== Summary

The FMF framework establishes:
- That the Collatz map, when viewed through the FMF decomposition, has a clean algebraic structure with exact formulas (Theorem A), universal output distributions (Theorem B), strict average contraction (Theorem C), and exponentially decaying growth chains (Theorem D).
- That these properties correctly distinguish $3n+1$ from $5n+1$ at the structural level.
- That the remaining gap is a precise, well-defined question in $p$-adic dynamics, not a vague "we need better bounds."

What it does not establish is the conjecture itself. The conclusion is that the FMF framework provides elementary density bounds for a clearly isolated Collatz growth mechanism, but the passage from density bounds to universal convergence remains open.
