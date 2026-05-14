# Review of the FMF Collatz Work

## Executive assessment

The strongest part of the work is the First-Multiple-of-Four decomposition. The FMF step and value formulas are genuine algebraic structure, not numerology. They give a clean accelerated odd-to-odd map and isolate the Type A channel where every nontrivial hop shrinks.

The main weakness was proof classification. Several statements that were written as trajectory-level theorems are only natural-density or 2-adic Haar-measure statements. That distinction is decisive: density-one behavior does not exclude exceptional integer orbits, and Collatz is exactly about excluding all exceptions.

Current strength: the work is a strong elementary framework for studying Collatz growth phases, but it is not a proof of Collatz. Its publishable core is the exact FMF algebra, the state-distribution theorem in natural density, the fractional-moment contraction calculation, and the Quartering Law for growth-B chains. Its main research value is that it reduces one dangerous obstruction to a precise 2-adic integer-code problem, further compresses the first binary-depth cases into explicit critical-series landing problems, and identifies a uniform finite-height counting theorem as the sharp next bridge.

## Main criticisms

1. The rank-1/spectral argument was overstated. Output residue distributions can be state-independent in density, but the deterministic hop ratio still depends on the input. This gives average contraction, not pointwise contraction.

2. The Quartering Law had a normalization error. Among all odd starts, the density of strict growth-B chains of length at least `k` is `4^-k`. The formula `2/4^k` is correct only after conditioning on the start already being Type B.

3. The old proof treated exact 2-adic distribution as if it implied independence along each orbit. It does not. It proves residue-density laws over many starts.

4. The old finite-truncation acyclicity argument was aimed at the wrong target. Exact growth-B cycles are impossible simply because every growth-B hop strictly increases the odd value. The hard case is not a cycle; it is an infinite nonperiodic path.

5. The comparison with Tao was too strong. The FMF result uses natural density, but it controls a narrower event: growth-chain length. Tao controls orbit minima. These are complementary, not directly ordered.

## Improved theorem package

The defensible proof should be framed as:

**Theorem A: FMF formulas.** For every odd input, the FMF step count and FMF value are given by the three explicit cases in `paper/sections/02-fmf-formulas.typ`.

**Theorem B: State distribution in density.** Within each fixed FMF input state, the output state distribution is independent of the input state in natural density. This follows from multiplication by 2-adic units and odd-part equidistribution.

**Theorem C: Fractional-moment contraction.** For the FMF hop ratio `R = F(x)/x`, the asymptotic natural-density moment satisfies `E[R^0.53] ~= 0.8638 < 1`. This is a rigorous average-contraction statement, not a Lyapunov proof.

**Theorem D: Quartering Law.** Conditional on a current growth-B hop, the density factor for one further growth-B continuation is exactly `1/4`. Thus strict growth-B chains have density `4^-k` among odd starts.

## Remaining proof target

A complete Collatz proof still needs a pointwise bridge:

> Prove an effective bound showing that every integer trajectory exits growth-favoring 2-adic domains quickly enough, and that the subsequent recovery beats accumulated growth.

The FMF framework narrows the obstruction to a concrete 2-adic dynamics problem, but it does not currently solve that problem.

The sharpest current endpoint is adelic. In the binary return problem, every infinite return word defines rational partial sums with real limit in `[-1,0)` and 2-adic limit equal to the selected return code. In the reduced `{0,1}` gap problem, every infinite gap word defines rational partial sums with real limit at most `1/115` and 2-adic limit equal to the selected gap code. Periodic words are excluded because these limits are rational and nonpositive or below `1`; the open case is a genuinely nonperiodic word whose 2-adic limit is nevertheless a positive ordinary integer.

The cleanest quantitative route is now a uniform finite-height discrepancy theorem. For return codes, prove `N_R(B,L) <= C(B+1)(2/15)^L`; for reduced gap codes, prove `N_G(B,L) <= C B (1/112)^L`. The start-count formulas show that these prefix-residue bounds are equivalent up to constants to ordinary-start survival bounds. The critical-rank criterion sharpens this further: it is enough, and necessary, to bound the rank of each finite word when words are sorted by least prefix residue. This makes the missing statement precise, but it is still not proved.

The backward-branch lemmas sharpen the obstruction again. The binary return partial map is backward-injective: a terminal return state has at most one predecessor across all return lengths, and backward paths contract by `(8/9)^L(16/27)^S`. The reduced gap map is different: its backward branch count is exactly controlled by `v3(128a'+1)`, all immediate preimages form a finite geometric chain with ratio `8/9`, and backward paths contract by `(43/81)^L(8/9)^K`. Immediate merge multiplicity is only logarithmic in terminal height, and the immediate preimage mass is bounded by `(43/9)a'`. Thus finite-prefix merging is a highly structured `3`-adic proximity phenomenon near `-1/128`, not arbitrary clustering.

Equivalently, surviving forward paths have terminal-height escape: return paths grow by at least `(9/8)^L(27/16)^S`, and gap paths grow by at least `(81/43)^L(9/8)^K`. The remaining rank problem is to turn that escape into a uniform count of low initial residues.

The terminal-window identities make that last sentence exact: after dividing terminal height by the path expansion factor, return prefixes land in `[R, R+1)`, while gap prefixes land in `(S-1/115, S)`. Equivalently, `R_w = floor(U_w/E_w)` and `S_w = ceil(u_w/E_w)`. Thus `R_w <= B` is equivalent to `U_w/E_w < B+1`, and `S_w <= B` is equivalent to `u_w/E_w < B`. A stopping-time proof must count how often these normalized terminal heights can remain in the low window as the path length grows.

The rank formulation can also be written purely in terminal coordinates: sort return words by `floor(U_w/E_w)` and gap words by `ceil(u_w/E_w)`. This is the same obstruction as sorting by least prefix residue, but it focuses attention on terminal escape and normalized stopping times.

For infinite words, the same terminal coordinates give the pointwise landing criterion: a positive ordinary obstruction exists exactly when the rounded normalized terminal coordinates stay bounded, equivalently eventually become constant.

These rounded terminal coordinates are nondecreasing along prefixes. So the obstruction is not arbitrary bounded oscillation; it is an eventual zero-increment tail in the rounded terminal coordinate.

That zero-increment tail is exactly an infinite orbit of the same partial map restarted from the terminal auxiliary state. This is useful mainly as a normalization: it shows the terminal viewpoint has not changed the mathematical obstruction, only made the stopping-time target sharper.

Locally, a zero terminal increment happens exactly when the auxiliary terminal state itself takes the same next partial-map step. For a fixed finite prefix, such a zero-increment tail is unique if it exists. The auxiliary state still grows during the tail by the terminal escape bounds. So any surviving obstruction must keep a rounded terminal coordinate fixed while the corresponding auxiliary terminal state follows one forced expanding positive orbit.

Finite zero-increment suffixes are exactly ordinary prefix congruences imposed on the auxiliary terminal state, with density equal to the reciprocal suffix modulus. Infinite zero-increment suffixes are the corresponding nested congruence/self-shadowing condition: the auxiliary terminal state must be the ordinary code selected by its own future suffix, a single 2-adic point for each fixed suffix. Every finite zero-increment terminal word is locally realizable from some auxiliary state. This rules out finite forbidden-pattern strategies in the terminal formulation too.

Summing over all suffixes of length `L`, the terminal zero-increment survival density is exactly `(2/15)^L` in the return system and `112^(-L)` in the reduced gap system. With bounded labels, the exact restricted rates are `((2/15)(1-16^(-(R+1))))^L` and `((1/112)(1-8^(-(K+1))))^L`. Again, that is sharp density decay, not a pointwise proof.

The self-shadowing condition propagates under the shift: every shifted suffix has its own positive ordinary code, and these shifted codes are exactly the later auxiliary states in the same expanding orbit.

Eventually periodic terminal tails are now excluded as well. The terminal-tail dichotomy leaves the same two subcases as the ordinary partial-map formulation: either a bounded-alphabet nonperiodic zero-increment tail, or an unbounded tail whose later auxiliary states approach the relevant `3`-adic reset point (`-85/88` for return, `-1/128` for the reduced gap map). The bounded-alphabet half is now an exact target too: for each fixed finite alphabet, the restricted least-residue minima must diverge.

Periodic bounded-alphabet shadows are settled explicitly. For any finite return period `w`, the repeated word `w^L` is the single congruence class of `-D_w/(P_w-Q_w)` modulo `Q_w^L`, and that rational lies in `[-1,0)`. For any finite gap period `w`, the repeated word `w^L` is the single congruence class of `C_w/(A_w-H_w)` modulo `H_w^L`, and that rational lies in `(0,1)`. Thus every periodic pattern has arbitrarily long finite shadows but no positive ordinary integer limit.

The bounded-alphabet obstruction is therefore not merely nonperiodic; by Morse-Hedlund, if its tail uses `q` symbols then its factor complexity must satisfy `p(m) >= m+q-1` for every `m`. Any eventually low-complexity itinerary would become eventually periodic and is already excluded.

The unbounded side is also sharper now: long return blocks require incoming height at least `(5*16^r-32)/33` and reset the output toward `-85/88` in `Q_3`; long zero gaps require incoming height at least `8^k` and reset the following gap state toward `-1/128`.

Finite reset neighborhoods are now explicitly ruled out as a shortcut. Inside any fixed congruence class `n ≡ -85/88 (mod 3^s)` or `a ≡ -1/128 (mod 3^s)`, the same dyadic finite-prefix densities and bounded-label densities hold. So the reset-spike alternative cannot be closed by any finite `3`-adic trap; it needs an infinite pointwise or height-sensitive argument.

Section 5 now packages these alternatives as sharpened endpoint theorems for both the binary return system and the reduced gap system.

There is also a weighted contraction: return backward fibers contract every positive power moment, and gap backward fibers contract every `theta`-moment satisfying `(43/81)^theta + (8/9)^theta < 1` (threshold about `2.28216`). Cubic mass is a simple strict case: the gap contraction constant is `43^3/(729*217) < 1`, despite finite merging. This is promising structure for a future rank proof, but frontier diagnostics show it does not by itself bound the number of low prefix residues uniformly; an additional terminal-height or stopping-time estimate is still needed.

The expansion-pressure identities sharpen the analytic picture: `sum E_w^-theta` decays exponentially for return words exactly when `(8/9)^theta + (16/27)^theta < 1` (threshold about `2.56743`), and for reduced gap words exactly when `(128/243)^theta + (8/9)^theta < 1` (threshold about `2.26483`). Cubic pressure is subcritical in both systems. This supports a high-moment stopping-time route, but still does not provide the missing terminal-window separation.

On the return side, terminal injectivity gives two rigorous low-window estimates. For `theta > 1`, the low-window inverse-expansion mass is at most `(B+1)^theta zeta(theta)`. More directly, with an expansion cutoff `E_w <= X`, the ordinary count is at most `ceil(X(B+1))-1`, because terminal states are distinct positive integers below `X(B+1)`. This is a real linear cutoff bound, but it leaves the hard case of many large-expansion words.

On the reduced gap side, backward contraction gives a weighted terminal-window estimate for `theta > 2`: the low-window inverse-expansion mass is at most `B^theta (43/81)^L zeta(theta-1)`, including merge multiplicity. Low expansion also bounds distinct terminal states by `floor(XB)`, and gives a multiplicity-adjusted word bound `sum_{u <= ceil(XB)-1} floor((43/81)^L u)`. These are real controls, but the cutoff count is quadratic in the terminal scale, so the full gap rank theorem still needs sharper multiplicity and high-expansion control.

The terminal-depth bounds add one more useful negative result: a fixed terminal state has only logarithmically bounded prefix depth (`U_w >= (9/8)^L` for return and `u_w > (114/115)(243/128)^L` for gap). So the remaining obstruction is not infinite depth over one terminal state; it is uniform breadth across low normalized windows, with merge multiplicity on the gap side.

The cutoff estimates should not be mistaken for near-proofs. Even the minimal expansion grows like `(9/8)^L` on the return side and `(243/128)^L` on the reduced gap side, while the desired survivor rates decay like `(2/15)^L` and `112^(-L)`. Therefore a successful rank theorem must use arithmetic separation of the normalized terminal heights, not just terminal-size growth or expansion cutoffs.

The expansion-shell diagnostic reinforces that point. On the checked `B=2^32-1` frontiers, low-window survivors occupy several dyadic expansion shells rather than a single extremal shell. The missing theorem has to explain separation inside and across those shells.

The weighted estimates do give formal shell counts: a shell `2^s <= E_w < 2^(s+1)` costs a factor `2^(theta(s+1))` when converting inverse-expansion mass into an ordinary count. This is useful for bounded shells, but it also makes the obstruction visible: high shells are exactly where weighted estimates lose counting power.

Fixed shells are finite-depth phenomena: return words in shell `s` have `L < log_{9/8}(2^(s+1))`, and reduced gap words have `L < log_{243/128}(2^(s+1))`. Thus any infinite obstruction must eventually move through arbitrarily high expansion shells.

The finite terminal-rank verifier sees this distinction already: on the checked low frontiers through `B=2^40-1`, the reduced gap system has terminal multiplicity `2` at more than one terminal state, including `12053155` and `72813864874`. That is small, but it confirms that the gap proof cannot simply copy the return injectivity argument.

The first nonconstant bounded alphabets are now explicit computational targets. The `{0,1}` return minima have been checked through length `20` and agree with the global minima in that range; the `{0,1}` gap minima have also been checked through length `20`, with the first difference from the unrestricted gap minima appearing at length `3`; fixed-one-count profiles are now checked through length `21`. There is also a new theoretical narrowing: every fixed-one-count stratum has diverging least residues, every fixed low-factor-complexity stratum `p_w(m) <= m` diverges, every balanced factor-window stratum with sublinear symbol count diverges, and the full balanced/Sturmian ordinary landing branch is now excluded. The proof reduces irrational balanced words to lower mechanical Sturmian codings, shows any ordinary landing would force anomalously delayed prefix recurrences, then uses the standard Sturmian recurrence function to produce fast prefix recurrences infinitely often. Thue-Morse, period-doubling, and all binary `2`-, `3`-, `4`-, `5`-, and `6`-uniform morphic fixed-point templates are also excluded. The q=6 proof is a useful caution: pure power-length prefixes show negative sampled margins in some cases, but symbolic prefixes such as `2*6^h` recur fast enough to close them. Diagnostics through q=8 are clean under the same symbolic-prefix scan, while q=9 leaves the concrete reduced-gap case `0->011111111, 1->100000000`; a targeted scan through symbolic prefix length `50,000` still finds no successful gap witness. More generally every bounded-defect perturbation of an eventually periodic template is ruled out. Any remaining `{0,1}` obstruction must now be higher-complexity than balanced Sturmian words, have uniformly positive-density labels, not admit any fixed periodic shadow with sublinear edit defect, satisfy the binary prefix-recurrence height barrier, avoid the density-free recurrence cutoffs, and evade the sharper density-recurrence exclusion inequality.

The first named aperiodic probes are benign: Fibonacci, Thue-Morse, period-doubling, and the irrational mechanical word of slope `sqrt(2)-1` all show roughly linear bit-growth in both return and reduced-gap prefix residues through length `1024`. This is useful diagnostic evidence for the low-complexity frontier, but it is not a proof for the full aperiodic class.

The balanced frontier was checked directly through length `64`: there are `27,834` balanced words at that level, with least balanced return residue bit length `186` and least balanced reduced-gap residue bit length `444`. This remains useful finite evidence, but the balanced/Sturmian branch is now proved excluded by the recurrence argument rather than by finite enumeration.

A long-prefix beam search through length `120` keeps selecting sparse low-residue candidates. Since fixed-count sparse strata are now theoretically excluded, this suggests the beam is mainly finding finite shadows of already-ruled-out tails rather than a plausible infinite obstruction.

## What to do next

1. Treat the paper as a rigorous density-and-structure result, not as a Collatz proof.
2. Make the 2-adic integer-code obstruction the central research problem: prove that every non-eventually-periodic infinite depth word has unbounded prefix residues, equivalently that the corresponding critical series cannot land 2-adically on a positive ordinary integer.
3. Keep the explicit long-chain family `m0 = 8^L - 1` in the paper. It prevents false finite-bound strategies and sets the lower bound `c >= 1/3` for any logarithmic growth-chain theorem.
4. Attack the uniform counting theorem directly. The computational evidence in `explorations/explore56_counting_discrepancy.py`, `explorations/explore57_start_counts.py`, `explorations/explore58_critical_discrepancy.py`, and `explorations/explore59_critical_clusters.py` is encouraging, but bounded verification is not a substitute for the discrepancy proof.
5. If seeking outside review, present the result as "elementary density bounds and a 2-adic obstruction for Collatz growth phases." That claim is defensible; "proof of Collatz" is not.
