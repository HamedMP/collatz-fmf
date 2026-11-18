# Referee Brief

This note is a review handoff for the FMF Collatz manuscript. It states what an
external reader should check, what is being claimed, and what is explicitly not
being claimed.

## Requested Review Scope

Please review the manuscript as a density-and-reduction paper, not as a proof of
the Collatz conjecture.

The most useful independent checks are:

1. Verify the FMF hop algebra in Sections 2 and 5.
2. Verify the natural-density normalizations in Sections 3--5.
3. Verify that the binary return and reduced `{0,1}` gap reductions in Sections
   6--8 are exact equivalences, not heuristic models.
4. Check that every use of computation is finite verification or diagnostic
   support, never a substitute for a universal theorem.
5. Check that Section 9 accurately states the remaining pointwise gap.

## Defensible Claims

The manuscript may claim:

- Exact First-Multiple-of-Four odd-to-odd hop formulas.
- A natural-density state distribution theorem from 2-adic unit structure.
- A fractional-moment contraction statement in the natural-density model.
- The Quartering Law for strict growth-B continuations.
- Existence of arbitrarily long finite growth-B shadows.
- Exact binary-depth return and reduced `{0,1}` gap partial-map reductions.
- Terminal-window, weighted-window, shell, and cutoff estimates for the first
  bounded-depth obstructions.
- Exclusion of periodic, finite-defect, low-complexity, balanced/Sturmian, and
  several small automatic/uniform-morphic obstruction templates.

## Claim Matrix

| Claim | Where to audit | What to check | Limitation to keep explicit |
| --- | --- | --- | --- |
| Exact FMF odd-to-odd hop formulas | Sections 2 and 5 | The Type A/Type B split, hop length, and output formulas cover every odd input and agree with the standard Collatz map. | Algebraic exactness does not by itself imply descent. |
| Natural-density state laws | Sections 3--4 | The sample space is odd starts in residue boxes, and the 2-adic inverse counts produce the stated distribution and fractional moment. | These are density-model statements, not independence along a fixed orbit. |
| Quartering Law | Section 5 | Conditional on already being in a growth-B hop, each further strict growth-B continuation imposes exactly one quarter of the remaining odd starts. | Density decay does not rule out an exceptional integer trajectory. |
| Finite growth-shadow construction | Section 5 | The all-zero branch gives arbitrarily long finite strict growth-B shadows. | This blocks finite forbidden-pattern proofs; it is not evidence for divergence. |
| Binary return reduction | Section 6 | The return-code congruences, partial map, critical-series landing criterion, and terminal-window identities are equivalent formulations. | The reduction leaves the unweighted rank/landing theorem open. |
| Reduced `{0,1}` gap reduction | Section 7 | The complete-gap survival density is `112^-L` and the gap partial map preserves ordinary-integer landing in both directions. | Gap merging and terminal multiplicity are not yet uniformly controlled. |
| Endpoint dichotomies | Section 8 | Any remaining bounded-depth obstruction is forced into the stated higher-complexity landing or reset-spike alternatives. | These dichotomies cover the first bounded-depth obstruction classes, not arbitrary mixed FMF epochs. |
| Template exclusions | Sections 6--8 | Periodic, finite-defect, low-complexity, balanced/Sturmian, and listed uniform-morphic branches are excluded by stated recurrence or compactness arguments. | The exclusions are class theorems, not a theorem for all aperiodic finite-alphabet words. |
| Universal uniform-morphic exclusion ("Theorem G", incl. q=9) | `proof.md` Section 23, Theorems 46 and 51 | Every binary fixed point of every `q`-uniform morphism, all `q >= 2`, admits no positive ordinary reduced-gap or return code; the q=9 boundary word is closed. | Excludes a symbolic class only; general non-morphic aperiodic words remain open. |
| Complexity thresholds for `{0,1}` landings | `proof.md` Section 23, Theorems 47 and 60 | Return landings need `liminf p(m)/m >= T_R` in `(3.1493, 3.1494)`, gap `>= T_G` in `(6.2390, 6.2391)`; sharpened 3-dependent versions `T_R' = 3.2439007`, `T_G' = 6.3942268`. | Lower bounds only; the ambient language is the full shift, so no complexity upper bound exists without H1 itself. |
| AP Survivor unconditional rank-type bounds | `proof.md` Section 23, Theorem 48 | `W_R(B,L) <= C((B+1)2^(-2.1L) + 2^(0.9L))`, `W_G(B,L) <= C(B 2^(-5.46L) + 2^(1.54L))`; floors `alpha_R = 0.287761`, `alpha_G = 0.212323`. | The additive `2^(0.9L)` defect means `g(L) -> 0` is NOT achieved; this is not the rank conjecture. |
| Exact criticality and counting no-gos | `proof.md` Section 23, Theorems 48 and 57 | The bases `2/15` and `1/112` are exactly critical; translate-invariant schemes saturate; every interval+AP class-counting certificate is `>= 1` for all `(B,L)`. | Negative results: they delimit proof strategies, they do not close the gap. |
| 5n+1 litmus on the endgame | `proof.md` Section 23, Theorem 49 | The entire rank apparatus transfers verbatim to 5n+1 (same `2/15`, `1/112`, `1/4`); `F_5(13) = 13` lies outside every excluded class. | Shows rank bounds alone can never imply convergence; it does not refute any Sections 5--8 theorem. |
| Two-lemma reduction with Lemma P | `proof.md` Section 23, Theorem 55 | H1 + Lemma E imply pointwise FMF descent and Collatz; Lemma P (no infinite positive orbit of `m' = (27m+1)/16`) is unconditional. | Conditional structure: neither H1 nor Lemma E is proved. |
| Mirror Equivalence and two-prime vacuity | `proof.md` Section 23, Theorem 61 | The 2-adic and 3-adic prefix data coincide under an explicit affine bijection; no two-prime pincer can prune the word tree. | A negative/structural result: it recasts H1, it does not prove it. |
| Cocycle, reset law, spike-ledger | `proof.md` Section 23, Theorem 62 | Cocycle and master identity; reset law via the Wronskian trichotomy; spike-ledger exclusion of depth spikes at geometric ratio `> log2(3)`. | Only the spike-ledger slice is an unconditional exclusion; the valuation-coincidence core of Lemma E remains open. |
| Certified descent record | `proof.md` Section 23, Theorem 54 | `sigma(x) = kappa(x)` for every odd `x > 1` with `kappa(x) <= 301,993` Terras steps. | Bounded-horizon only; the uncertified tree is an uncountable Cantor set, so no finite-modulus scheme can close the pointwise gap. |
| Cycle bound in FMF form | `proof.md` Section 23, Theorem 53 | The Simons--de Weger m-cycle count equals the FMF hop count: every nontrivial cycle makes `>= 92` FMF hops. | Rests on Hercher's `m <= 91` exclusion and the Barina `2^71` floor; higher milestones are conditional. |

## Claims To Reject

The manuscript should not be accepted as claiming:

- A proof of the Collatz conjecture.
- Pointwise descent for every odd integer.
- Independence along an individual deterministic trajectory.
- Empty exceptional sets from density-zero estimates.
- Universal theorems from finite verifier output.
- A theorem stronger than Tao's almost-all result without qualification.
- That the candidate Tao-upgrade manuscript is established mathematics or
  new: the natural-density form of Tao's theorem ("Theorem ND",
  `notes/round4-july2026/s5-completion/PROOFS.md`) is AI-generated with no
  human review and is not a repository claim. The result was first claimed by
  J. Allikvere (Zenodo, 13 July 2026) by essentially the same method and by
  L. Mazur (ProofAtlas, 21 July 2026, claimed Lean-checked); the repository
  claims no priority and no novelty. Known defects and repairs are listed in
  `notes/round6-nov2026/nd-referee/REPORT.md`.

## Main Gap To Check

The remaining proof target is the pair of lemmas in the refereed two-lemma
reduction (`proof.md` Section 23, Theorem 55): H1 + Lemma E imply pointwise FMF
descent and hence Collatz.

- **H1**: no infinite positive orbit of the binary return partial map,
  equivalently `mu_L -> infinity`. The original terminal-window bound
  `W_R(B,L) <= C(B+1)(2/15)^L` remains a sufficient fixed-height form (the gap
  analogue `W_G` is redundant given `W_R`, and any uniform `f(B)g(L)` with
  `g(L) -> 0` suffices), but any proof must be position-aware and must not be a
  class-counting certificate: the base `2/15` is exactly critical,
  translate-invariant schemes provably saturate, and every interval+AP
  class-counting certificate is `>= 1` for all `(B,L)`.
- **Lemma E**: every non-descending FMF orbit is eventually a depth-`{0,1}`
  growth-B chain. It must be proved by arithmetic, not letter statistics (no
  frequency-based quantitative form exists); its core is infinitely many exact
  valuation coincidences tied to rational seeds and the Lagarias periodicity
  conjecture; the unbounded-alphabet branch is partially closed by the
  spike-ledger theorem.

Rank bounds alone cannot close the gap: the rank apparatus is
multiplier-blind, and 5n+1 has the genuine cycle 13 outside every excluded
class. Lemma E carries all the 3-dependence. The current paper proves weighted,
shell, cutoff, periodic, complexity-threshold, and uniform-morphic exclusions,
plus the unconditional AP Survivor bounds, but neither H1 nor Lemma E.

## Files To Read First

- `site/paper/collatz-fmf.pdf`: rendered manuscript.
- `publication-readiness.md`: claim-boundary and submission audit.
- `proof-obligations.md`: completion checklist and missing theorem inventory.
- `submission-checklist.md`: source package, command, and claim-boundary gates.
- `diagnostics.md`: what the verifier scripts do and do not establish.
- `review.md`: critical review of the proof framing.

## Verification Commands

The quick smoke snapshot is:

```bash
bash scripts/verify_snapshot.sh quick
```

The full recorded snapshot is:

```bash
bash scripts/verify_snapshot.sh full
```

The full snapshot was last run successfully on May 14, 2026. Passing these
commands supports the algebra, reductions, finite certificates, paper build,
and diagnostic frontier stated in the repository notes. It does not prove the
missing pointwise Collatz theorem.

## Review Questions

- Are the FMF formulas and type splits correct for every odd input?
- Are the density calculations normalized over the intended sample spaces?
- Do the binary return and reduced-gap maps preserve ordinary-integer
  equivalence in both directions?
- Do the terminal-window identities exactly match the least prefix residues?
- Are the weighted and shell estimates stated with their correct limitations?
- Does any theorem accidentally infer pointwise behavior from density or Haar
  measure?
- Is the remaining rank/landing theorem stated sharply enough to guide future
  work?
