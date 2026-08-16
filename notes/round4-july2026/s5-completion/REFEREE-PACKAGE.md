# Human-Referee Package: Theorem ND (Natural-Density Upgrade of Tao's Theorem)

Prepared 2026-07-31 for the candidate manuscript `PROOFS.md` in this directory
(produced July 21, 2026, round 4 of the multi-agent campaign). This package is
the entry point for a HUMAN analytic number theorist. It contains: the exact
statement and a one-page roadmap; a dependency table against Tao
arXiv:1909.03562v7; a risk-ranked checklist of the steps to attack first; a
script index with expected outputs; and an honest cover note on provenance.

**Status: CANDIDATE ONLY.** AI-generated, twice AI-refereed adversarially
(both verdicts NOT-REFUTED, minor findings), zero human review. Not established
mathematics. Excluded from proof-obligations.md. Do not cite as a theorem.

--------------------------------------------------------------------------------
## 1. Exact statement and one-page roadmap

### Statement (PROOFS.md, Theorems 3-U and ND)

**Theorem ND (candidate).** There is an absolute constant C such that for every
N0 >= 16 the set {N in N+1 : Col_min(N) > N0} has upper natural density at most
C log^(-1/25) N0 (and the same bound holds for {N odd : Syr_min(N) > N0}).
Consequently, for every f: N+1 -> R with f(N) -> infinity,

    Col_min(N) <= f(N)   for almost all N in the sense of NATURAL density

(the exceptional set has natural density 0). Here Col_min(N) is the minimal
element of the Collatz orbit of N, Syr_min the Syracuse analogue. This replaces
"logarithmic density" in Tao's Theorem 1.3 (arXiv:1909.03562) by natural
density, with an effective exceptional-density bound.

### Roadmap (one page)

Tao's proof needs logarithmic density in exactly two places (PROOFS.md Part I,
tags [LOG]): the weight identity after his (5.19) — the log-uniform 1/N mass at
a reconstructed preimage factors as the Geom(2) word probability 2^(-|a|) times
an a-free factor — and the wide-window covering step 3e. Everything else is
density-agnostic. The manuscript replaces the two [LOG] steps as follows,
working with uniform dyadic windows U_y (y dyadic, x^1.0003 <= y <= x^1.003):

1. **Lemma P7** (phased Prop 7.1). The s-pinned character sums
   sum_s |E[1_{S_n=s} chi(X_n)]| are bounded by Tao's OWN Section-7 majorant
   E prod_j |f(3^(2j-2) 2^(-b_[1,j]), b_j)| <<_A n^(-A): the total valuation
   S_n is measurable w.r.t. his pair-sum conditioning sigma-algebra G, so the
   s-sum telescopes and no step of Section 7 is re-proved.

2. **Lemma J*** (joint fine-scale mixing; the object of Tao's Remark 1.16).
   d_TV((S_n, X_n), (S_n, X_n + Unif(3^m Z/3^n Z))) <<_A m^(-A). Proof = rerun
   of Tao's Section 6 with the S-marginal riding along: same events E, E_k,
   B_k, C_{k,l}; the exact two-block factorization ghat_s(xi) = FF(xi) *
   SF_{s-l}(xi) on C_{k,l}; second factor summed over s by Lemma P7 at scale
   n'' = n-k-j-1; first factor unchanged (Plancherel + Cor 6.3); one extra
   Cauchy-Schwarz over the O(sqrt(n log n)) live s values (cost n^(1/4),
   absorbed). The collision-entropy criticality of Prop 1.14 (fixed-tilt
   no-go, proof.md Theorem 56) never activates: the pinning phases are
   unitary and Section 6's L2 steps are phase-blind.

3. **Prop 5.2-U + Lemma K** (uniform-window formula and exact pinning). For
   dyadic windows the first-passage probability becomes an exact lattice-point
   count: P(Aff_a(U_y) = M) = (2/y) * [congruence mod 3^ell] * [window], with
   |a| pinned to s*(ell,M) = ceil(ell log2(3) + log2(y/M)). The Geom(2) weight
   2^(-|a|) emerges from COUNTING (2^(s*) words), not from the measure. Fake
   triples (orbit dips below x and re-ascends) are killed by the standoff
   inequality (S): m0 log(4/3) >= 10 Lam'', with m0 = ceil(sqrt(log x)
   (loglog x)^2) chosen SMALLER than Tao's m0 and Lam'' = 3 Lam log2 + C2,
   Lam = C0 sqrt(log x loglog x).

4. **Lemma R** (renewal-Gaussian-equidistribution; the analytic heart). The
   sum over word lengths ell of 2^(1-frac(g(ell))) P(S_{ell-m0} = s*(ell)-t),
   g(ell) = ell log2(3) + gamma, converges to 1/log(4/3) = 3.4760594967...
   uniformly in the offset gamma and shift t, with error O(log^(-1/25) x).
   Mechanism: exact composition law P(S_k = s) = C(s-1,k-1) 2^(-s) + local CLT;
   blocks of length J0 = log^(2/5) x with Gaussian freezing; Koksma per block
   on the coupled BV function h(u) = 2^(1-u) G(... + 1 - u); discrepancy of
   {ell log2 3} via Erdos-Turan + Rhin 1987 (|u log2 + v log3| >= H^(-7.616),
   so D*_J << J^(-1/8.616)), giving the bottleneck log^(-0.0464) x > target
   log^(-1/25) x. The equidistribution of {ell log2 3} supplies the Archimedean
   mixing that logarithmic density previously provided for free.

5. **Assembly.** Theorem 5-U: P(Pass_x(U_y) in E) = Q_x(E) + O(log^(-1/25) x)
   with Q_x(E) = (2/log(4/3)) sum_{M in E'} 3^(m0) pi_{m0}(M)/M — IDENTICAL to
   Tao's (5.20)-(5.21) log-density limit measure; hence window stabilization
   (1.20)-U. Theorem 3-U: Tao's Section-3 threshold chain (alpha = 1.001,
   base case Pass <= x_b <= N0 free, small->large transfers, window swap by
   5-U, geometric telescoping with ratio alpha^(-1/25), chain constant
   ~2.5e4), then dyadic covering and odd-part reduction. Theorem ND follows
   by diagonalization.

Supporting lemmas: K (pinned kernel, machine-verified exhaustively in a prior
refereed round), W (exact last-m0-letter split, law(psi) = Syrac(Z/3^m0)
exactly), M (max-mass <= 1.36 (2/3)^m, C = 1.354503), B (boundary pairs
<= y x^(-0.5)), 5.3-U (Tao's Lemma 5.3 transplanted to scale m0).

--------------------------------------------------------------------------------
## 2. Dependency table: Tao arXiv:1909.03562v7

Every numbered result of Tao's paper that the manuscript touches. "Black box" =
statement used as published, proof not re-entered. "Rerun with modification" =
proof re-executed with a stated change; the referee must check the change, not
the original. Line numbers refer to the plain-text v7 copy used in the session
(see Section 5 caveat: that copy is not bundled here).

| Tao item | What it is | How used | Where in PROOFS.md |
|---|---|---|---|
| (1.5), (1.7), (1.13) | F_n, Aff_a, 0 < F_n <= 3^n | conventions, verbatim | Part 0 |
| (1.22), (1.29) | Syrac(Z/3^n), reversal form | conventions; reversal underlies Lemma W | Part 0, Lemma W |
| Prop 1.9 | mod-2^n equidistribution => Geom(2) TV bound | black box | 5.2-U step (1) |
| Prop 1.11 | first-passage stabilization (log density) | REPLACED by uniform-window analogue | Theorem 5-U |
| Lemma 1.12 | Syracuse offset recursion | black box (drives the induction) | Lemma M |
| Prop 1.14 | fine-scale mixing of X_n | S-marginal special case of J*; its PROOF (Section 6) rerun with modification | Lemma J* |
| Remark 1.16 | joint mixing of the entire affine map, "plausibly attainable" | the object J* constructs | Lemma J*, cover note |
| Prop 1.17 / Section 7 | character-sum decay; majorant (7.5): E prod_j \|f\| <<_A n^(-A) | black box THROUGH the majorant only; no step of Section 7 modified | Lemma P7 |
| (1.19), (1.20) | no-infinite-passage; window comparison | re-proved for uniform windows | (1.19)-U in 5.2-U; (1.20)-U in 5-U |
| Lemma 2.1 | uniqueness of the valuation tuple / reconstruction | black box | Lemma K, 5.2-U step (5) |
| Lemma 2.2 | Chernoff bounds for Geom(2) sums | black box | 5.2-U(2), J* (iii), Lemma R (1) |
| Section 3 (Thm 1.6/3.1 chain) | threshold iteration | rerun with modification (dyadic covering replaces log-covering 3e) | Theorem 3-U |
| Prop 5.2, (5.13)-(5.19) | approximate formula, reconstruction, weight identity | rerun with modification (uniform windows; weight identity REPLACED by K + R) | Prop 5.2-U, Lemma K |
| (5.20)-(5.21) | log-density limit measure | comparison target: Q_x(E) is proved IDENTICAL | Theorem 5-U |
| Lemma 5.3 + (5.24)-(5.26) | harmonic AP counting | rerun with modification (scale n-m0 -> m0; density-agnostic) | Lemma 5.3-U |
| Section 6: (6.2), (6.3), (6.5), (6.8); events E, E_k, B_k, C_{k,l} | mixing machinery | rerun with modification (phase rides along) | Lemma J* (b) |
| two-block factorization (v7 line ~2682) | X_n = F_{k+1}(block1) + 3^(k+1) 2^(-l) F_{n-k-1}(block2) on C_{k,l} | used exactly; machine-verified exhaustively (sA-A4) | J* (vi) |
| frequency reduction (v7 line ~2707) | xi = 3^j 2^l xi', n'' = n-k-j-1 >> n | used exactly | J* (vii) |
| Cor 6.3 | injectivity => sum_Y P^2 <= 2^(-l) | black box | J* (viii) |

Non-Tao external inputs (all published): Rhin 1987 (Prog. Math. 71, 155-164:
linear-forms measure |u log2 + v log3| >= H^(-7.616) for H = max(|u|,|v|) >= 2,
hence mu(log2 3) <= 8.616 — verified against the literature by referee 2; any
finite irrationality measure yields some exponent c* > 0); Erdos-Turan and
Koksma inequalities; Stirling / local CLT with explicit remainder.

--------------------------------------------------------------------------------
## 3. Risk-ranked referee checklist

Ranked by (subtlety x centrality). Both AI referee records (see
`../full-claims-and-referee-records.txt`, TARGET s5-completion) and the
manuscript's own honesty notes (PROOFS.md Part IV) feed this ranking. Every
item below was checked by both AI referees and none failed; that is evidence,
not proof.

### Risk 1 — Lemma R step (4): the coupled Koksma application (u_ell inside the Gaussian)
- **Claim.** The block summand 2^(1-u_ell) P(S_k = s*(ell)-t) can be treated,
  after Gaussian freezing, as a single BV function h(u) = 2^(1-u) G(zlin + 1-u)
  of u_ell = frac(g(ell)), with V(h) <= C G, so Koksma + the discrepancy of
  {ell log2 3} give the block error. The subtlety: s*(ell) = g(ell) + (1 -
  u_ell), so the SAME u_ell appears in both the weight and the Gaussian pin —
  no independence is available or claimed.
- **Why it might fail.** If the freezing error or the BV constant is
  mis-estimated, the u-coupling could contribute a term that does not average
  out; referee 2 noted the write-up "conflates pre-/post-freezing objects" —
  h must be ell-free for Koksma, and step (3)'s freezing bound is what licenses
  the replacement. This is presentational in the referees' judgment, but it is
  the single step where a real gap is most plausible.
- **What the AI referees checked.** Both re-derived the constant 1/log(4/3) =
  1/((2 - log2 3) log 2) exactly; referee 1 re-derived the O(1) z-shift cost
  K/sqrt(k) of the coupling and the live-range containment (center offset
  ~7.2 Lam vs padding Lam'/log(4/3) ~ 48 Lam); referee 2 confirmed V(h) <= CG
  including the wrap jump. Numerics: sC and two independent implementations
  hit 3.4760595 uniformly over random phases/shifts (12/12 trials, |err| <=
  3.1e-3).
- **Fastest human check.** Rewrite step (4) yourself at full epsilon detail for
  ONE block: freeze G at ell_1 (using step (3)), verify the resulting h is a
  genuine one-variable BV function with the claimed constant, apply Koksma,
  and un-freeze. Half a day. To BREAK it: exhibit a phase gamma where the
  coupling term is Omega(1) per block — the sC setup (script here) makes that
  testable numerically first.

### Risk 2 — Lemma J* steps (vi)-(vii): two-block factorization and the s-pinned second factor
- **Claim.** On C_{k,l}: ghat_s(xi) = FF(xi) * SF_{s-l}(xi) EXACTLY (S_n =
  l + S'' with S'' block-2-measurable; E_k, B_k, C_{k,l} block-1-measurable),
  and the s'-summed second factor is bounded by Lemma P7 at scale n'' =
  n-k-j-1, uniformly in xi outside the coarse lattice, with the extra block-2
  letters handled by independence + triangle inequality.
- **Why it might fail.** The factorization requires every event in play to be
  measurable in the right block, and P7 is applied in (1.29)-reversed indexing
  at a different scale — an indexing slip (the session itself fixed an sA-A4
  indexing bug in the SCRIPT) or a uniformity loss in xi would break the
  chain. This is the mathematical core of the whole manuscript (Remark 1.16).
- **What the AI referees checked.** Both verified the factorization display
  verbatim against Tao v7 (line ~2682) and its exhaustive machine check
  (sA-A4: all 4^6 words at n=6, k=2); referee 2 verified that F'' mod 3^(n'')
  depends on exactly the first n'' block-2 letters in reversed indexing and
  that the reversal is a measure-preserving bijection; both confirmed Tao's
  own measurability assertions for E_k, B_k, C_{k,l}.
- **Fastest human check.** Read Tao Section 6 (his proof of Prop 1.14)
  side-by-side with J* (b)(i)-(ix) and tick each of the two claimed departures;
  re-derive S_n = l + S'' on C_{k,l} from the definitions. One day. To BREAK
  it: find one event among E_k, B_k, C_{k,l} that is NOT block-1-measurable,
  or a xi in the excluded lattice range where the P7 bound is applied.

### Risk 3 — Lemma J* step (iv): the extra Cauchy-Schwarz over live s values
- **Claim.** sum_{good s} ||g_s - A_m g_s||_1 <= (C_A sqrt(n log n))^(1/2)
  3^(n/2) (sum_s ||...||_2^2)^(1/2); the n^(1/4+o(1)) cost is absorbed by
  taking A' = A + O(C_A^2) + 4, meeting a per-(k,l) target n^(-A-3) (vs Tao's
  n^(-A-2)).
- **Why it might fail.** Pure bookkeeping — but bookkeeping across Tao's
  (k,l)-union (n^(1/2+o(1)) pairs), the bad-s Chernoff tail, and the not-E
  error, any one of which could silently eat the budget if an exponent is off.
- **What the AI referees checked.** Referee 1: "pure bookkeeping, but worth
  re-deriving" — re-derived it; the 3^(n/2) from L1->L2 cancels against
  Plancherel's 3^(-n/2). Referee 2 re-checked the full budget: per-(k,l)
  n^(1/4) * n^(-A'+O(C_A^2)) <= n^(-A-3), union n^(1/2+o(1)), consistent for
  arbitrary A.
- **Fastest human check.** One page of exponent accounting with Tao's (6.5)
  and (6.8) ranges in hand. Two hours.

### Risk 4 — Prop 5.2-U step (4) + Lemma K: standoff inequality, sandwich, fake triples
- **Claim.** (a) Backward direction: if Syr^(n-m0)(U_y) = M in E', the standoff
  (S) m0 log(4/3) >= 10 Lam'' forces the whole prefix orbit above x, so
  T_x(U_y) = n exactly — no double counting across n. (b) Without the envelope
  a single N CAN pin at several n (orbit re-ascent; the manuscript itself
  flags this — an earlier draft overclaimed unconditional uniqueness); all
  such fake triples have valuation deviation >= log(4/3)/log2 * m0 =
  0.415 m0 >> Lam, land outside A^(ell), and are charged to the sandwich
  error <= |I_y| log^(-10) x via the per-(s,Y) weight bound W <= y(1+x^(-0.8)).
- **Why it might fail.** This is the historically dangerous spot of any
  Section-5 rebuild (double counting). The argument leans on the interplay of
  three window constants (C0, C1, C2 with Lam' = 20 Lam log2 + C1, Lam'' =
  3 Lam log2 + C2) given at orders-of-magnitude granularity, and on m0 being
  simultaneously >> Lam (standoff) and small enough that m0^(-A) beats every
  log power (J*-replacement).
- **What the AI referees checked.** Referee 2 independently re-derived the
  window constants, initially SUSPECTED a 4Lam-vs-3Lam mismatch in the forward
  direction, and resolved it (using Syr^(n-1) > x rather than Syr^n <= x: only
  2 Lam log2 + C needed — constants right). Both re-derived W <= y + 2^s with
  2^s <= y x^(-0.8). The sD experiment confirms the mechanism at toy scale:
  fake-triple excess decays geometrically in m0 (ratio ~2/3), exactly as the
  standoff analysis predicts.
- **Fastest human check.** Redo 5.2-U step (3)-(4) with explicit C0, C1, C2
  (pick C0 = 100, derive C1, C2) and verify (S) and both directions close.
  Half a day. To BREAK it: construct an orbit that dips below x and re-ascends
  into E' while keeping every partial valuation sum within Lam of 2j — the
  0.415 m0 >> Lam deviation bound says this is impossible; check that bound's
  derivation first.

### Risk 5 — Lemma R step (5): discrepancy, the Rhin exponent, and the 1/25 margin
- **Claim.** D*_J of {ell log2 3 + gamma} on blocks of length J0 = log^(2/5) x
  is <= C J0^(-1/8.616) = C log^(-0.0464) x (Erdos-Turan with cutoff Kf =
  J^(1/8.616), shift-invariance costing a factor 2), and 0.0464 > 1/25 = 0.04
  with margin — the rate bottleneck of the whole theorem.
- **Why it might fail.** The Rhin citation must actually give ||q log2 3|| >=
  c q^(-7.616) (linear-forms measure => irrationality measure conversion), and
  the Erdos-Turan optimization must be right; a factor slip here silently
  shrinks c* below the claimed 1/25 (though ANY finite measure keeps some
  c* > 0, so the theorem's shape survives).
- **What the AI referees checked.** Referee 1 recomputed every error exponent
  independently; referee 2 confirmed Rhin 1987 against the literature (mu <=
  8.616 for nonzero elements of Q log2 + Q log3) and re-derived the
  Erdos-Turan optimization.
- **Fastest human check.** Pull Rhin's paper, confirm the stated measure and
  the conversion to ||q log2 3||; redo the Erdos-Turan optimization (three
  lines). Two hours. This is also the easiest place to IMPROVE the result
  (sharper measures raise c*).

### Risk 6 — Boundary/pinning measure estimates: Lemma K's boundary pairs and Lemma B
- **Claim.** The pin s_pin equals s*(ell,M) = ceil(g_M(ell)) except on
  BOUNDARY pairs where frac(g_M(ell)) is within 2 x^(-0.7) of 0 (since
  0 < F_ell(a) <= 3^(n0) <= x^(-0.74) M on E'); the total boundary
  contribution to COUNT is <= C y x^(-0.5) (Lemma B, via J* at coarse scale +
  Lemma M max-mass + #Bdry(ell) <= 4 x^(-0.7) * range).
- **Why it might fail.** Lemma B is the sketchiest proof in the manuscript
  ("assemble as in Part III") — referee 2: "proved at sketch density,
  acceptable given the x^(-0.5)-vs-log^(-1/25) margins". The margin is huge,
  but the assembly it invokes is the same pipeline being refereed, so an error
  in Part III would propagate here rather than be caught here.
- **What the AI referees checked.** Both verified F_ell/M <= x^(-0.74) and the
  boundary-measure count; referee 1 re-derived the AP structure behind the
  weight bound (W); the assembly pipeline itself was checked as Risk items
  1-4.
- **Fastest human check.** Write out Lemma B's five-line assembly in full,
  reusing the (by then verified) Part III steps. One hour; do it AFTER
  Risks 1-4.

### Risk 7 — Theorem 3-U: chain bookkeeping (dyadic slack, per-z re-basing)
- **Claim.** The threshold chain (alpha = 1.001) transfers only small->large
  (deterministic orbit inclusion, no side condition); both windows at each
  swap have exponents inside [1.0003, 1.003] after dyadic slack; the endgame
  applies the chain to X = z^(1/alpha) for each dyadic z; geometric
  telescoping gives constant (1 - alpha^(-1/25))^(-1) ~ 2.5e4.
- **Why it might fail.** "Elementary but fiddly" (manuscript's own words). The
  per-z re-basing of the chain is GLOSSED in the write-up — referee 1: fixable
  in one line, and verified the fix works (the base case works for ANY
  threshold in [x_b, x_b^alpha), so the chain reaches every X). An earlier
  session draft had the transfer direction outright wrong (caught and
  re-architected before refereeing) — history says this step deserves
  suspicion.
- **What the AI referees checked.** Both verified the transfer direction, base
  case (Pass <= x_b <= N0 free), window exponents (1.001, 1.002001 in range
  after O(1/log x) dyadic slack), telescoping, covering, and the odd-part
  reduction Col_min(2^e N') = Col_min(N') <= Syr_min(N').
- **Fastest human check.** Write the one-line per-z re-basing repair yourself
  and re-run the chain on paper. Two hours.

### Risk 8 — Lemma 5.3-U: the scale transplant of Tao's Lemma 5.3
- **Claim.** Tao's Lemma 5.3 (harmonic sum over E' in a residue class) holds
  with modulus 3^(m0) in place of 3^(n-m0): sum_{M in E', M = r mod 3^m0} 1/M
  <= C 3^(-m0). The proof never used the measure — only (1.7), the (5.24)
  v-subwindow, CRT, AP harmonic sums (5.25)-(5.26), and the 2^v > x^(1/2)
  case with its extra lower bound.
- **Why it might fail.** A hidden scale dependence in (5.24) or in the
  2^v > x^(1/2) branch would break the transplant; this lemma aggregates the
  Lemma R errors (sum_M 3^m0 pi_m0(M)/M <= C), so it is load-bearing for the
  final rate.
- **What the AI referees checked.** Both read Tao's full Lemma 5.3 proof and
  re-derived the transplant independently (geometric v-sums; the 2^|v| >
  x^(0.5) branch summing to x^(-0.1+o(1)) << 3^(-m0)); both call it genuinely
  density-agnostic.
- **Fastest human check.** Read Tao's Lemma 5.3 proof once, replay it with
  m0 in place of n-m0. Two hours.

Items the referees judged NOT to need attention: P7 (three-line conditioning
argument — but note it is load-bearing; referee 2 verified Tao's own statement
that conditioning on the b_j makes the a_{2j} and a_n independent, and referee
1 stress-tested the odd-n unpaired-letter case the claimant never tested),
Lemma W (exact identity), Lemma M (one-line induction), Lemma K's kernel
(exhaustively machine-verified in a prior refereed round).

Known minor defects, disclosed by the AI referees (none load-bearing; fix
before submission): garbled t-range sentence in Lemma R's statement; the
h_{ell_1}(u) pre-/post-freezing notation conflation (Risk 1); "|S_{n0}| >
1.9 n0" typo in 5.2-U(3) (should be one-sided); dead function theory_mass()
in sD_endtoend.py; "superpolynomially small" wording for |I_y| m0^(-A)
(actually log^(-375) x-ish — ample); Theorem 3-U per-z re-basing gloss
(Risk 7); effective thresholds astronomically large (asymptotic statement
only — the standoff needs (llx)^(3/2) large).

--------------------------------------------------------------------------------
## 4. Script index

All five scripts live in this directory and were rerun clean on 2026-07-31
(python3, Apple Silicon; wall-clock times below; no dependencies beyond the
standard library). They are SUPPORTING evidence at toy scales — the theorem's
content is asymptotic and is NOT machine-checkable; a passing script rules out
the corresponding exact identity being wrong, nothing more.

| Script | What it checks | Key expected output | Runtime |
|---|---|---|---|
| `sA_joint_mixing.py` | Exact joint (S,X) integer-DP tables (rows = negative-binomial law, columns = Lemma 1.12 law, incl. Tao's published Z/9 table); exact joint oscillation Osc^J at n <= 8 (tracks plain Osc within factor < 1.9); exhaustive two-block factorization identity at n=6, k=2 (J* step (vi)) | `[A4] PASS X_n = F_(k+1)(block1) + 3^(k+1) 2^(-l) F_(n-k-1)(block2) mod 3^n for all 4^6 words, n=6,k=2` ... `ALL sA CHECKS COMPLETE` | ~1.4 s |
| `sB_phased_sec7.py` | Lemma P7 inequality at n=7,8 for six frequencies coprime to 3 (~5x margin); consistency plain \|S_chi\| <= summed version | `[B1] PASS Lemma P7 inequality holds at n=7,8 for all tested xi coprime to 3`; `[B2] PASS plain \|S_chi\| <= summed phased version` | ~1.7 s |
| `sC_lemmaR.py` | Lemma R constant: K -> 1/log(4/3) = 3.4760595 uniformly over random phases/shifts; Gaussian-sweep factor 1/(2 - log2 3) | `[C1] PASS K -> 1/ln(4/3); worst errors by scale: {300: '1.0e-02', 1000: '4.6e-03', 3000: '1.9e-03', 6000: '1.7e-03'}`; `factor check: sum_ell P(S_ell = s*) = 2.409422 vs 1/(2-log2 3) = 2.409421` | ~94 s |
| `sD_endtoend.py` | Exhaustive (sampling-free) end-to-end at x = 2^12: window stabilization (the (1.20)-U claim), fake-triple excess decay in m0, shape-TV against the predicted limit law. Reference output preserved in `sD_final.log` | From `sD_final.log`: `TV(emp_y1, emp_y2) = 0.00204   TV(emp_y1, emp_y3) = 0.00153   [stabilization]`; `excess decay ratios (m0=2..6): ['0.691', '0.685', '0.657', '0.601']  [geometric ~ 2/3]`; `[D2] PASS shape agreement improves with m0 (3 -> 6): 0.0873 -> 0.0556 (m0=8 truncated: 0.0669)` | ~51 s |
| `sE_maxmass.py` | Lemma M exact (Fractions): parity-class structure and max-mass of Syrac(Z/3^m) for m <= 7; C = 1.354503 | `[E0] PASS admissible exponents form one parity class mod 2 (both residues)`; `[E1] PASS max-mass <= 1.34 (2/3)^m exactly for m <= 7` | ~14 s |

Note the sD m0=8 row carries a disclosed enumeration-cutoff artifact
(MMAX = 1024x); and the toy-scale free-count excess is EXPECTED (the standoff
(S) fails for bounded m0 — its geometric decay is the confirmation, not its
absence).

Not bundled (session-scratchpad artifacts, referenced by PROOFS.md and the
referee records but not preserved in the repo): the local Tao source copy
`tao-natural-density/tao_v7.txt` (fetch arXiv:1909.03562v7 yourself — every
line-number citation must be re-anchored against your copy), the prior-round
`verify_s5.py` / `verify_s4.py` (exhaustive 16384-point kernel check), and the
two referee stress scripts `ref1_reversal_p7.py` / `ref2_windows_lemmaR.py`.
The refereed prior-round inputs they checked are summarized in proof.md
Theorem 56.

--------------------------------------------------------------------------------
## 5. Cover note (read this before investing time)

**Provenance.** This manuscript was written entirely by an AI agent on July 21,
2026, in a multi-agent session (claimant agent + two independent adversarial
AI referee agents, run sequentially). Both referees returned NOT REFUTED with
minor findings only: every Tao citation was verified verbatim against a local
copy of the arXiv v7 text, every new mechanism re-derived independently, all
five scripts rerun with exactly the claimed numbers, and both referees wrote
additional stress tests (odd-n P7 cases; an independent end-to-end at a second
toy scale x = 2^9 with TV 0.009-0.013). No human has reviewed any part of it.
Two AI passes are correlated evidence: the referees share training lineage and
possible blind spots with the claimant, and AI-generated analytic number
theory at this length has a base rate of subtle errors that machine checks at
n <= 8 and x = 2^12 cannot catch. Treat the document exactly as an unrefereed
preprint from an unknown author.

**Why it is plausible.** (i) Tao himself predicted the key object: Remark 1.16
of his paper says the fine-scale mixing of the entire affine map — exactly
Lemma J* — "looks plausibly attainable from the methods in this paper", and
his introduction (line ~295 of v7) says "it is plausible that some refinement
of the arguments below will allow one to replace logarithmic density by
natural density". The manuscript does not invent a new method; it executes the
refinement Tao gestured at. (ii) The mechanism reuses Tao's own majorant:
Lemma P7 re-proves NOTHING in Section 7 — it observes that the total valuation
is measurable with respect to Tao's own conditioning, so his (7.5) bound
covers the pinned sums for free; Lemma J* is his Section 6 with one factor
riding along. (iii) The known obstruction is genuinely dodged, not ignored:
the fixed-tilt collision-entropy criticality (proof.md Theorem 56's sharp
negative) concerns non-unitary tilts, and the pinning phases here are unitary.
(iv) The limiting first-passage measure comes out IDENTICAL to Tao's
log-density one — a nontrivial consistency check, confirmed exactly at toy
scale by sD. (v) The prior refereed rounds (proof.md Theorems 50, 56) had
already reduced the upgrade to two sharply-stated lemmas; this manuscript's
S4 half was proved there, and only the S5 half is new here.

**What acceptance would mean.** The first density improvement of Tao's
theorem: "almost all" in natural density, with an effective exceptional bound
C log^(-1/25) N0, answering the question raised in his paper and constructing
his Remark 1.16 object. It would still be an almost-all statement — it implies
NOTHING pointwise, does not touch the Collatz conjecture proper, and does not
interact with this repository's pointwise gap (the repo's claim boundary in
proof-obligations.md is unchanged either way). The rate 1/25 is not optimized;
any improvement of the irrationality measure of log2 3 improves it.

**What refutation would mean.** Most plausibly a localized failure at Risk 1,
2, or 4 above — in which case the S4 half (refereed, proof.md Theorem 56) and
the reduction of the upgrade to a Section-5 rebuild remain standing, and the
failure point would itself be informative (it would identify what logarithmic
density buys that the renewal argument cannot replace). A refutation would
also be a valuable data point on the reliability of adversarially-refereed AI
mathematics at this depth. Either outcome is worth having; that is why this
package exists.

**Suggested review order.** Read PROOFS.md Part 0 + Part I (the density-tag
skeleton) against Tao's paper first (half a day); then Risks 2-3 (J*, one
day); then Risk 1 (Lemma R, half a day); then Risks 4-8 (one day). A focused
expert should reach a verdict in roughly three to four working days.
