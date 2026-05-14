#import "../lib/theorem.typ": *

#v(0.8em)
#text(size: 1.45em, weight: "bold")[Main Results and Logical Dependencies]

This overview records the logical shape of the paper before the technical proofs begin. The main contribution is not a proof of Collatz, but an exact coordinate system and a set of reductions that make one pointwise obstruction explicit.

#v(0.6em)
#text(size: 1.18em, weight: "bold")[Established theorem package]

#theorem(name: "FMF Density and Obstruction Package")[
  The First-Multiple-of-Four coordinate system establishes the following results.

  + Every odd input has an exact FMF hop formula, split into Type A and Type B cases.
  + FMF output states have an input-state-independent natural-density distribution.
  + The FMF hop ratio has a strict fractional-moment contraction in the natural-density model: $EE[R^0.53] approx 0.8638 < 1$.
  + Strict growth-B continuations have density factor exactly $1\/4$ at each step.
  + Arbitrarily long finite growth-B shadows exist, so no finite forbidden-pattern argument can settle the pointwise problem.
  + The first binary-depth return obstruction and the reduced ${0,1}$ gap obstruction reduce to explicit positive-integer partial maps, critical-series landing criteria, and terminal-window counting problems.
]

#proof[
  The first item is Theorem A in Section 2. The second and third items are Theorems B and C in Sections 3 and 4. The fourth and fifth items are proved in Section 5 by the Quartering Law and the explicit all-zero branch. The final item is the sequence of binary return and reduced-gap reductions in Section 5, including the partial-map, boundedness, terminal-window, start-count, rank, and endpoint-dichotomy statements.
]

The theorem package has three roles. First, it isolates deterministic contraction through the Type A channel. Second, it proves sharp density decay for the dominant strict growth mechanism. Third, it turns the first nontrivial pointwise obstructions into explicit arithmetic problems rather than heuristic exceptional sets.

#v(0.6em)
#text(size: 1.18em, weight: "bold")[Dependency map]

#table(
  columns: (1.4fr, 1.4fr, 2.2fr),
  inset: 5pt,
  [*Component*], [*Established where*], [*Role in the argument*],
  [FMF formulas], [Section 2], [Define the accelerated odd-to-odd dynamics exactly.],
  [State distribution], [Section 3], [Gives natural-density output laws; does not imply trajectory independence.],
  [Fractional moment], [Section 4], [Proves average contraction in the density model.],
  [Quartering Law], [Section 5], [Gives exact $4^(-k)$ density for strict growth-B chains.],
  [Finite-shadow construction], [Section 5], [Shows that finite forbidden-pattern proofs cannot work.],
  [Binary return map], [Section 5], [Reduces bounded-depth return obstructions to explicit 2-adic landing.],
  [Reduced gap map], [Section 5], [Reduces the first nonconstant binary alphabet to a second explicit partial map.],
  [Terminal windows], [Section 5], [Reformulates low prefix residues as low normalized terminal heights.],
  [Weighted and shell bounds], [Section 5], [Control inverse-expansion mass and fixed shells, but not full unweighted rank.],
  [Gap analysis], [Section 6], [States what remains open and why density does not imply universal convergence.],
)

#v(0.6em)
#text(size: 1.18em, weight: "bold")[Endpoint reduction map]

The longest part of Section 5 is organized around two endpoint theorems and the counting criteria that would close them.

#table(
  columns: (1.25fr, 1.8fr, 2.15fr),
  inset: 5pt,
  [*Endpoint object*], [*Named statements*], [*What they prove or isolate*],
  [Binary return map],
  [Binary Return Partial Map; Binary Return Counting, Critical-Rank, and Terminal-Rank Criteria],
  [Reduces the bounded binary-depth obstruction to an explicit positive-integer partial map and to equivalent finite-height counting and rank problems.],
  [Binary return endpoint],
  [Binary Obstruction Dichotomy; Binary Return Terminal Tail Dichotomy; Sharpened Binary Return Endpoint],
  [Shows that any remaining binary return obstruction must be either a higher-complexity bounded-alphabet ordinary landing or an unbounded reset-spike approaching $-85\/88$ in $QQ_3$.],
  [Reduced ${0,1}$ gap map],
  [Binary ${0,1}$ Gap Partial Map; Gap Counting, Critical-Rank, and Terminal-Rank Criteria],
  [Reduces the first nonconstant return-alphabet case to a second explicit partial map with survival density $112^(-L)$ and parallel terminal-window formulations.],
  [Reduced ${0,1}$ gap endpoint],
  [Binary ${0,1}$ Gap Obstruction Dichotomy; Gap Terminal Tail Dichotomy; Sharpened Binary ${0,1}$ Gap Endpoint],
  [Shows that any remaining reduced-gap obstruction must be either a higher-complexity bounded-alphabet ordinary landing or an unbounded reset-spike approaching $-1\/128$ in $QQ_3$.],
  [Excluded template classes],
  [Low-Complexity Divergence; Balanced Ordinary Landing Exclusion; Binary Two- through Six-Uniform Morphic Template Exclusion],
  [Removes periodic, finite-defect, sparse-label, low-complexity, balanced/Sturmian, and several automatic-template branches from the endpoint obstruction list.],
)

#v(0.6em)
#text(size: 1.18em, weight: "bold")[Missing pointwise bridge]

#conjecture(name: "Uniform Terminal-Window Rank Bound")[
  There are constants $C_R,C_G>0$ such that for every height bound $B$ and prefix length $L$,
  $ W_R(B,L) <= C_R(B+1)(2\/15)^L $
  for the binary return terminal-window count, and
  $ W_G(B,L) <= C_G B 112^(-L) $
  for the reduced ${0,1}$ gap terminal-window count.
]

This conjecture is the current sharp finite-height target. The paper proves weighted, shell, and low-expansion estimates toward it, but not the full unweighted bounds.

#proposition(name: "Pointwise Descent Criterion")[
  If the FMF framework is supplemented by a theorem proving that every odd $x>1$ has a finite FMF iterate below $x$, then the Collatz conjecture follows.
]

#proof[
  Suppose every odd $x>1$ eventually reaches a smaller odd value under the FMF map. Starting from any positive integer, divide by powers of two until an odd value is reached. If that odd value is $1$, the orbit has reached the standard cycle. Otherwise the assumed descent gives a smaller positive odd value. Repeating produces a strictly decreasing sequence of positive odd integers until $1$ is reached. This is impossible to continue indefinitely, so every orbit reaches $1$.
]

The terminal-window rank conjecture is not claimed to be equivalent to full Collatz. It is a concrete sufficient subtarget for the first bounded-depth obstruction classes. A complete proof through FMF would still have to extend from these partial maps to arbitrary growth-B and mixed recovery epochs.
