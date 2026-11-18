# w6-runs — brief for the attempt that did NOT run (2026-11-18)

Status: launched on 18 Nov 2026 and terminated by a usage limit before it
produced anything (no files, no results). Relaunch this as a fresh agent, or
do it by hand. Everything below is the coordinator's plan; the "sketch" parts
are UNVERIFIED and were written quickly — expect sign, direction and constant
errors. Verifying or refuting the geometry by exact computation is step one.

## Read first
`BRIEF-COMMON.md`, `LEDGER.md` (family 28), then `w5-fourier/REPORT.md`
(Proposition 1, Theorem 5, Lemma R, Corollary 6) with
`referee-fourier/REPORT.md`, `w4-wall/REPORT.md` (Proposition G), and
`w3-g2/REPORT.md` Step 5 "Lemma X" and dead end 1 (where a path PARALLEL to
the triangle hypotenuse killed the argument in the sister problem G2).

## Target
Hypothesis (D): there are η, ε, c > 0 such that for all large K and all
integers 1 ≤ |h| ≤ 2^(ηK), every block path from (P,k) = (0,K) with steps
(ΔP, Δk) ∈ {(4,−6), (5,−7), (6,−8)}, continued while k ≥ 8, meets at least
cK nodes that are ε-good, where (P,k) is ε-good iff
‖11h·3^(−(P+5))/2^k‖ ≥ ε (inverse of 3 taken mod 2^k).

Proved and refereed: (D) ⇒ pointwise power Fourier decay of the H1 Cantor set
at integer frequencies ⇒ lemma FP-0 (power saving on the count of potential
H1 seeds). FP-0 is strictly weaker than H1 and holds equally for the 3n−1
system; it is NOT a route to Collatz by itself.

## Facts to use (proved, refereed)
- Lemma R: for ε ≤ 10^(−3), if a node and its child are both bad then the
  symmetric residues satisfy m(P,k) = 3^(ΔP)·m(child) exactly. A run of J+1
  consecutive bad nodes from (P₀,k₀) forces
  ‖11h·3^(−(P_J+5))/2^(k₀)‖ ≤ ε·3^(−4J).
- Node (P,k) looks at the bits just below position k of the single big
  integer x_p = 11h·3^(−p) mod 2^K, p = P+5: bad ⇔ a run of ≥ log₂(1/2ε)
  equal bits ending at position k−1.
- Numerics (w5): fraction of bad nodes ≈ 2ε; longest bad run for h = 1,
  K = 1600 is 2; minimum number of good nodes over paths g_K/K ≈ 0.046–0.050
  at ε = 0.1 for K ≤ 3200; adversarial h = 3^n have one big bad region at
  the root of size ≈ n.

## Sketch to verify or refute (coordinator's, unverified)
1. Column relation: at fixed k, moving p → p+1 divides the residue by 3 when
   3 | m (stays bad) and otherwise produces a residue ≥ 2^k(1−ε)/3 (good).
   Row relation: at fixed p, moving k → k−1 keeps the same integer m, bad
   while |m| < ε·2^k.
2. So the bad set should be a union of right triangles with apex at a
   "super-bad" node (p*,k*) of tiny residue m₁:
   {(p,k) : p ≤ p*, k ≤ k*, |m₁|·3^(p*−p) < ε·2^k}; hypotenuse slope
   dk/dp = log₂3 = 1.585. This is the 2-adic guise of Tao's black triangles
   (arXiv:1909.03562, Lemma 7.4; local TeX may be at
   `nd-referee/tao-src/collatz.tex`, lines ~1100–1400).
3. Path slopes are |Δk|/ΔP ∈ [8/6, 6/4] = [1.33, 1.5] < 1.585. Per step the
   quantity (p*−p)·log₂3 + (k*−k) changes by −0.34, −0.92 or −1.51, so a path
   inside a triangle moves away from the hypotenuse and exits through the
   vertical side p = p*, after at most (p-extent)/4 steps. If right, paths
   are NOT parallel to the hypotenuse here (unlike G2).
4. Then (D) can fail only through chains of very large triangles (size
   comparable to the remaining path length) with O(1) good stretches between
   them. Each apex is an exact relation 11h = m·3^p + t·2^k with m, t small:
   t = 0 forces 3^p | 11h (the adversarial family, harmless for
   |h| ≤ 2^(ηK) with η small). For t ≠ 0, 2-adic/3-adic Baker only excludes
   triangles of size within a polylog factor of the maximum.
5. Possible routes to finish: exact arithmetic relating consecutive
   triangles of a chain; a counting argument over h using that a long bad run
   costs about 6.34 bits of constraint per node; a sharper Theorem 5 that
   needs good nodes only on all but an exponentially small part of the path
   MASS (then a large-deviation bound for the natural path measure suffices);
   a 2-dimensional density statement for bad nodes in boxes of the (p,k)
   grid, where the field y(p,k) = (c·2^(−k) mod 3^p)/3^p has genuine ×2 and
   ÷3 structure (Furstenberg / Bourgain–Lindenstrauss–Michel–Venkatesh type
   rigidity, as opposed to the rank-one paths that blocked earlier attempts).

## Computation to run
For h ∈ {1, 5, 7, 13, 2^20+7, a few random 40-bit} and K up to 10^4–10^5:
one sequence x_p = 11h·3^(−p) mod 2^K for p ≤ 0.75K; longest equal-bit runs
in the cone; exact minimum number of good nodes over block paths by dynamic
programming for ε ∈ {10^(−3), 0.02, 0.1}; sizes of the largest triangles met
by paths against the 3^(−ℓ) heuristic (≈ 2·log₃K); adversarial search over
h ≤ 2^(ηK).

## Outcomes that count
(D) proved (give η, ε, c and the resulting FP-0 exponent); (D) refuted
(exhibit h, K, path — then the majorant route is dead); or a precise residual
statement about triangle chains with numerical evidence. Litmus: everything
is symmetric under E ↦ −E and must never imply E ∩ ℤ_{>0} = ∅; check the
5n+1 analogue geometry (hypotenuse slope log₂5 = 2.32). Run a prior-art
search BEFORE refereeing or formalizing anything. Final message verdict-first.
