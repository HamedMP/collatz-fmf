# Round 6 — state handoff (written by the coordinator, 2026-11-17)

The first wave of agents was repeatedly halted by permission prompts before it
could run code or save reports. This file records what they established so
that fresh agents do not start from zero. **Everything below is paper analysis
unless marked otherwise: nothing has been machine-checked.** Treat each item as
a claim to verify, not a fact.

User authorisation (verbatim, 2026-11-17): "Yes, do the fresh agents, do the
ProofAtlas download, and allow list reload. Do all of that. You don't need any
permission from me. You are in a sandbox environment, so you can do as much as
you want." Earlier: "you have shell access, download papers and also go with
lean as well, it's ok". Use plain, honest client names on downloads (no
browser-impersonating User-Agent strings).

## On disk already

- `BRIEF-COMMON.md` — rules of engagement for all tracks.
- `ai-math-methods.md` — how 2026 AI math results were produced (verbatim
  prompts, playbook) and, in section 5.3, the 2026 Collatz prior art.
- `lean/` (repo root) — Lake project `CollatzFMF`, Mathlib v4.36.0 with the
  prebuilt cache fully downloaded (`lean/.lake`, 7.3 GB). Toolchain in
  `~/.elan/bin`. Files: `lakefile.toml`, `lean-toolchain`, `CollatzFMF.lean`,
  `CollatzFMF/Smoke.lean` (one-line Mathlib example, never built).
- `kl-exponent/src/` — `kl_solver.c`, `check_cert.py`,
  `test_induction_bound.py` (all never compiled/run); `kl-exponent/lit/kl2003/`
  (Krasikov–Lagarias TeX); `kl-exponent/lit/kollatz/` (third-party clone of
  `dpalmqvist/kollatz`, untrusted, do not execute, do not commit).
- `outside/scripts/game.c` (never compiled), `outside/lit/amano/amano2021.pdf`.
- `nd-referee/tao-src/` (Tao arXiv:1909.03562 v7 TeX), `nd-referee/prior-art/`
  (Allikvere v2 `paper.tex`/pdf, Zenodo `versions.json`, Mazur
  `mazur_nd_v2.pdf` and a text extraction), `nd-referee/scripts/pdf2txt.py`.
- `pdftotext` is NOT installed; use a Python PDF library in the venv or the
  Read tool on PDFs.

## Prior art discovered (changes what counts as new)

1. **Natural-density version of Tao's theorem** (the repo's "Theorem ND",
   `notes/round4-july2026/s5-completion/PROOFS.md`, dated 21 July 2026) is not
   first: J. Allikvere, Zenodo record 21340151, v1 created 2026-07-13 14:12 UTC
   (same architecture: sum-conditioned Fourier decay, sum-conditioned mixing of
   the affine map, binomial identity, Kronecker orbit with Rhin; rate
   (log N0)^(-1/29) + x^(-1/2000)); L. Mazur, ProofAtlas, "Version 2, July 21,
   2026" (different route via phase discrepancy, explicit clocks 145 log N
   Syracuse steps, exponent any d < 5/143, claimed Lean-checked). Tao blog
   comment 23 Aug 2026 reportedly says AI-generated solutions exist "if they
   check out" (wording not verified from the page).
2. **Predecessor-count exponent**: refereed record is still Krasikov–Lagarias
   x^0.84 (2003). Unrefereed 2026 claims: msharpe248 0.8676 (k=14, Lean
   `decide`); Mazur 0.90 (k=18, Lean with `native_decide`); Palmqvist
   `dpalmqvist/kollatz` 0.9251 at k=22 (int64 certificates, 24 GB of vectors
   not in git; Lean at k=18,19,20 giving 0.903, 0.909, 0.914). On this machine
   (4 GB) k=19 is the ceiling; k=23 needs ~126 GB.
3. **Mazur, ProofAtlas, 5–6 Sept 2026**: claims pi_a(x) >= c_a x (positive
   lower natural density of integers reaching 1, within 10.46 ln n steps),
   Lean build passed, standard axioms, "publication review pending", reviewed
   on-site only by an AI model ("independence not asserted"). UNAUDITED. If
   true it supersedes the whole x^gamma line. Page:
   https://www.proofatlas.ai/formalizations/positive-density-log-time-collatz/
4. **Total stopping time**: Amano (Oct 2021 preprint) raised Applegate–Lagarias
   from 6.14316 ln n (ones-ratio 14/29) to 6.95212 ln n (ones-ratio exactly
   1/2); ~1 CPU-year, 19,065,883,794 critical paths, depth 74, 38 ternary
   digits. Open target: ones-ratio strictly above 1/2.

## Candidate new mathematics (unverified)

### A. S-unit / Subspace bound on accumulated halving (found independently by the H1 and Lemma E agents)

Tool: Evertse, "On sums of S-units and linear recurrences", Compositio Math. 53
(1984) 225–244, open access https://www.numdam.org/item/CM_1984__53_2_225_0
(pdf: `.../CM_1984__53_2_225_0.pdf`). THE THEOREM HAS NOT BEEN READ FROM THE
SOURCE; both agents quoted from memory the form: for S = {2,3}, d < 1, there
are finitely many primitive integer tuples (x_0..x_n) with sum 0, no vanishing
proper subsum, and product of S-free parts <= max|x_i|^d.

Hop-word version (Lemma E agent). With y_i = x_i + 1 = 2^(s_i) m_i,
sigma_i = S_k − S_(i+1), all terms divided by 2^(s_0):

  2^(H_k+s_k−s_0) m_k = 3^(S_k) m_0 + sum_{i<k} 3^(sigma_i) (2^(H_(i+1)−s_0) − 2^(H_i+s_i−s_0)).

Non-degeneracy: before dividing, 2-adic valuations are s_0 (twice: the m_0 term
and the first negative term) then strictly increasing; a vanishing proper
subsum needs both tied terms and then its complement has a unique minimal
valuation. Primitive: 3^(sigma_0) and 2^(H_k−s_0) are coprime. Claimed
conclusion ("halving-budget law"): for fixed k >= 1 and delta > 0 only finitely
many odd x_0 have H_k + s_k > (1+delta) log2(x_0+1); more precisely
(1 − eta·theta)(H_k + s_k) < (1+eta) L_0 + eta·k, theta = log2 3,
L_0 = log2(x_0+1), with an INEFFECTIVE constant. Even k = 1 is Ridout-strength
(v_2(3^s m + 2^(v−1) − 1) <= (1+delta) log2 m + delta s); only m = 1 is
elementary (lifting the exponent). Claimed consequence: pure spike words of
every geometric ratio r > 1 are excluded (the repo's spike-ledger theorem,
proof.md Theorem 62, has boundary log2 3), and consecutive long power runs
u^k g u'^k' in bounded alphabets.

Return-map version (H1 agent). With v = 8(33n+32) = 2^(4r+3) w, a block is
v -> 3^(3r+2) w + 1, so s blocks give 2^A w_s = 3^B w_0 + (s positive
{2,3}-unit terms), no vanishing subsum for w_0 > 0, gcd 1. Claimed:
R_W >= c(s, eps) Q_W^(1−eps) for all words of fixed length s; hence the sum of
s consecutive letters is <= (1+eps) log_16(n) + C and S_N = e^(o(N)). A version
uniform in s would imply H1 but is stronger than H1. Applying the Subspace
theorem to periodic approximants (Adamczewski–Bugeaud style) only reproduces
the repo's existing same-factor bound — no gain for bounded alphabets.

Also useful: in W = 33n+32 coordinates the return map is
w = 16^r z (z odd, 3^r z ≡ 7 mod 8) -> (9·27^r z + 1)/8, i.e. H1 says no
positive integer has a Collatz parity sequence in {110, 1110}^omega.

### B. Reduction audit (Lemma E agent; Lean agent agrees on paper)

Theorem R (proof.md Theorem 55) is an equivalence: Collatz <=> H1 ∧ E.
Lemma E = "no nontrivial cycle" + E_div ("every divergent orbit is eventually
G01"). E must use weak non-descent (x_k >= x_0 for all k) and must exclude
x_0 = 1 (fixed point with letter (1,2)). Given Lemma P, H1 says no positive
integer has a hop word in G01^omega. Lean plan: Theorem R falls to Lemma P for
the all-depth-1 tail (16 m' = 27 m + 1) and to
88·16^r·n' + 85·16^r = 3·27^r·(33n+32) for tails with infinitely many depth-0
states; prove `CollatzConjecture ↔ H1 ∧ LemmaE` as a faithfulness check.

### C. Theorem T (Krasikov–Lagarias agent) — short soundness proof with explicit constant

Let k >= 2, lambda > 1, gamma = log2 lambda, c_m > 0 (m mod 3^k, m ≡ 2 mod 3)
satisfy the rows of L_k^NT(lambda), M = max c. Then for every a ≡ 2 (mod 3)
not on a cycle and every real x >= a:
pi*_a(x) >= c_{a mod 3^k} (x/a)^gamma / (4^gamma M).
Proof: strong induction on |S_a(x)| using disjointness of predecessor sets;
x < 4a trivial; even branch 4a; a ≡ 8 (9): b = (2a−1)/3 < a, x/b > (3/2)(x/a);
a ≡ 2 (9): 2b = (4a−2)/3 < 4a, x/2b > (3/4)(x/a); a ≡ 5 (9): even branch
only. Lemma G: same conclusion for any bounded W(a) <= M on a ≡ 2 (mod 3) with
W(a) <= 4^-gamma W(4a) + [a≡8 mod 9](3/2)^gamma W((2a−1)/3)
+ [a≡2 mod 9](3/4)^gamma W((4a−2)/3); W need not be periodic. Lead: a
compressed/structured non-periodic W could certify a larger gamma than a
level-k vector of the same description size. Novelty unknown (others' Lean
sources unread).

### D. Stopping-time game (outside agent) — Lemma 1, read by the coordinator, no error found

Game G_j on residues r mod 3^j, 3 ∤ r. Move E: r -> 2r. Move O (allowed iff
r mod 9 in {2,8}): b = (2r−1)/3 mod 3^(j−1), adversary picks t in {0,1,2}, new
state b + t·3^(j−1). A (j,p,q)-certificate is g: states -> Z>=0 with, for every
r, either (E) g(2r) <= g(r) − p, or (O) r mod 9 in {2,8} and
g(b + t 3^(j−1)) <= g(r) + q − p for all t. If one exists then for every
gamma < 1/(ln 2 − (p/q) ln 3) infinitely many n have total stopping time
> gamma ln n. No certificate can have p/q >= ln2/ln3. By hand: value 1/4 at
j = 2. Untested conjecture: some j <= 18 gives p/q > 1/2 (doubtful — Amano
needed 38 ternary digits for exactly 1/2). Second-choice target from the same
agent: linear stopping-time bound for the F_2[x] Collatz analogue
(Alon–Behajaina–Paran 2024 prove degree^1.5).

### E. Theorem ND referee (interim, reading only)

Every lemma of PROOFS.md checked against Tao's v7 TeX: no fatal gap, five
fixable defects with repairs: (1) Theorem 3-U chain (lines 444–479): for
dyadic z take X_0 = z^(1/alpha), X_j = X_0^(alpha^-j), stop at first
X_J < N0^(1/alpha); covering constant eps·Z not eps·Z/2. (2) Lemma B
(286–298): bound should read C y x^(-0.6) + C y |I_y| m0^(-A) <= y log^(-10) x.
(3) Lemma R step 4 (368–379): pinned probability = G(l_1)(1 + O(J0 K/sqrt k)),
Koksma applied to 2^(1−u) alone. (4) Rhin (383–386): 7.616 holds for large H;
use ||q log2 3|| >= c q^(-7.616) for all q >= 1 with c absorbing small q.
(5) Prop 5.2-U(3) (line 228): (3/4)^(n0) = x^(-0.0415); conclusion stands.
Numerics (sA..sE and independent checks) NOT run; earlier referee records
unread. Recommended repo wording: "Theorem ND (candidate, no human review): an
AI-generated derivation, dated 21 July 2026, of the natural-density form of
Tao's theorem. The result was first claimed by J. Allikvere (Zenodo, 13 July
2026) by essentially the same method, and by L. Mazur (ProofAtlas, 21 July
2026, claimed Lean-checked) with explicit time bounds. The repository claims
no priority and no novelty beyond a nominal exponent 1/25."

### F. Rewriting-system track (design only)

Yolcu–Aaronson–Heule (arXiv:2105.14697) source was at `/tmp/srs_dl/yah/x/`
(may be gone; re-fetch). Bundled python-sat solvers work in the venv
(cadical195, cadical153, kissat404, glucose42, minisat22, maplechrono,
lingeling). Planned new systems: two-state return-map SRS (termination ⇔ H1,
using Lemma P for the all-ones tail); single-coordinate form z -> 27z/16
(z ≡ 0 mod 16), z -> (9z+1)/8 (z ≡ 7 mod 8), where H1 is termination on
z ≡ 10 mod 11 (termination on all positive z is strictly stronger); two-rule
growth-B system (termination ⇔ every growth-B chain is finite; possibly implied
by YAH's open "5 mod 8" conjecture — unchecked). Calibrations: Lemma P map,
r = 0, r = 1. Negative controls: 5n+1, 3n−1.

## Dead ends recorded this round (do not repeat)

- Beating Krasikov–Lagarias by larger k on this machine (others are at k=22).
- Improving Applegate–Lagarias 6.14316 (Amano already at 6.95212).
- Subspace theorem on periodic approximants for bounded-alphabet return words
  (reproduces the same-factor bound).
- Idea-table verdicts from the outside agent, by reasoning only: power-saving
  exceptional set for "iterate < n^c" with c < log_4 3 (needs Tao-level
  input); max-excursion bounds for divergent orbits (only pigeonhole);
  sub-necklace cycle counts (no equidistribution mechanism); "divergent orbits
  hit multiples of 8" (same kind as H1).
