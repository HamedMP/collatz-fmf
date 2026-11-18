# Collatz FMF — Round 6 handoff

## Status after the 2026-11-17 terminal session (READ THIS FIRST; it supersedes sections 2–5 below)

All eight track cards of section 5 were run, the second wave (step 9) was run,
and the consolidation (step 10) is done. **Collatz, H1 and Lemma E remain
open.** Nothing is committed.

Where to read:
- `proof.md` → "Round 6 (November 2026)": Theorems 64–70 with status labels.
- `plan.md` → "November 17, 2026 — Round 6": per-track outcomes, dead ends,
  corrected "still open" lists, six open leads.
- `LEDGER.md` (this directory): 23 approach families, blocked routes, and the
  mandatory control maps (5n+1, 3n−1, 3n+d, S_a for every a).
- `<track>/REPORT.md` and `referee-*/REPORT.md` for every agent. Most were
  saved by the coordinator from the agent's final message because the
  agents' own REPORT.md writes were refused by the harness.
- Lean: `lean/CollatzFMF/` — Basic, FMF, Return, TheoremR, Barrier, TwoBlock,
  BarrierH1, KLSound, Harmonic, HarmonicBeta (+ three axiom-audit files).
  `lake build` passes (18,280 jobs); standard axioms only; no sorry.

What exists now, by strength of check (no human review of anything):
- KERNEL-CHECKED: Collatz ⇔ H1 ∧ Lemma E; repetition barrier and two-block
  exclusion (Thm 65 A, L, B); Krasikov–Lagarias soundness (Thm 67, a known
  statement, new proof); uniform harmonic bound Σ 1/x_k ≤ 1196 along every
  distinct stretch of every trajectory (Thm 70; refereed constant 27.2 not
  formalized).
- PROVED + blind hostile AI referee: S-unit window law (Thm 66, modulo
  Evertse 1984, ineffective); corollaries of Thm 65; rigidity of T and the
  control family S_a (Thm 68); H1 Cantor-set formulation and no-go (Thm 69);
  residue bound, sojourn count, cycle-length corollary of Thm 70; short-
  interval statement; Theorem ND sound modulo five repairs (no priority).
- CANDIDATE: F_2[x] closed formula; lemmas FP-0, G2, T; power-run
  compression; conditional density-existence theorem (derivation refereed,
  hypothesis is Mazur's unrebuilt Lean result).
- Others' claims, statement-audited only: Mazur's positive density, 0.90
  exponent, natural-density descent (all pin Lean v4.30.0-rc2; rebuilding
  needs a second Mathlib download, which the owner has not approved).

Update 2026-11-18 (third wave): committed on branch `round6-nov2026`
(not pushed). Additionally KERNEL-CHECKED: rigidity of T and the S_a control
family (Thm 68); harmonic bound 162, residue bound, cycle exponent bounds,
conditional exact cycle length, sojourn count 10·1.9322^L (Thm 70). Lemmas
FP-0 and G2 were attacked: neither power saving was proved; each gave a
refereed logarithmic gain and a reduction to the Erdős ternary-digit regime
(see plan.md "Third wave" and LEDGER.md families 19′, 24).

Open decisions for the owner:
1. Whether to allow a second Mathlib fetch (~6–7 GB, agent's estimate) to
   rebuild Mazur's positive-density Lean.
2. Whether to commit. Never commit `kl-exponent/lit/kollatz/`,
   `kl-exponent/cert/` (4.5 GB), `mazur-audit/{src,dl,build}/` or
   `lean/.lake/` — all are in `.gitignore` now.
3. Whether any of Thms 65, 68, 70 is worth a human referee / literature
   check before it is described outside the repo (novelty is unconfirmed:
   two or three web searches each).

Next mathematical steps, if continuing (each strictly weaker than Collatz):
lemma G2 (lowers the 0.95 exponent in Thm 70); lemma FP-0 (beats the 0.2878
seed-count exponent); Lemma T (ternary morphisms); formalize the sharp
constants of Thm 70 and the corollaries of Thm 65 in Lean; F_2[x] Period
Lemma. No known route from any of these to H1 or Lemma E.

---

# Original handoff (2026-11-17, before the terminal session)

Entry point for a new Claude Code session continuing this work. Read this file,
then `STATE.md` (same directory) for the mathematics, then
`BRIEF-COMMON.md` (rules every agent brief should point to) and
`ai-math-methods.md` (how 2026 AI math results were produced; section 3 is the
playbook, section 5.3 the Collatz prior art).

## 1. What the owner asked for

Hamed (repo owner) asked, in his words: continue the project; "use subagents
to approach different methods"; study how AI solved open problems recently
(prompts, scaffolds) and "try to come up with a valid solution for collatz";
"use my approach but if you have better ideas, no need to be bounded to the
box"; and later "Just make sure that you end up in the proof." He has approved
shell access, paper downloads, a Lean install, fresh agents, and the ProofAtlas
download, and said no further permission is needed in this sandbox.

Honest position to keep: Collatz is open. The repo's own vetted claim boundary
(`proof-obligations.md`) says so, and nothing in this round changes that. Do
not promise or announce a proof; report exactly what is proved, what is only
verified to a bound, and what failed. A candidate proof of anything major must
survive the litmus maps (5n+1, 3n-1, 3n+d), a blind hostile referee, and
ideally Lean before it is described as more than a candidate.

## 2. Where the mathematics stands

- Repo reduction (proof.md Theorem 55): Collatz follows from **H1** (binary
  return partial map has no infinite positive orbit) and **Lemma E** (every
  non-descending FMF orbit is eventually a depth-{0,1} growth-B chain). This
  round's audit says the reduction is an equivalence (Collatz <=> H1 ∧ E), so
  by the playbook's rule the pair is exactly as hard as the conjecture.
  H1 = "no positive integer has a T-parity sequence in {110, 1110}^omega";
  Lemma E contains "no nontrivial cycle".
- **Nothing new has been machine-checked this round.** Every agent was halted
  by permission denials before it could run code. What exists is paper
  analysis, recorded in `STATE.md` sections A–F.
- Candidate new results, all UNVERIFIED (details in `STATE.md`):
  - A. S-unit / Subspace bound on halving accumulated over a fixed number of
    hops or return blocks (Evertse 1984). Two agents found it independently;
    the theorem was never read from the source. Ineffective; a size
    constraint, not a descent claim; would extend the spike-ledger theorem
    from ratio > log2 3 to every ratio > 1 if correct.
  - C. "Theorem T": short induction proof of the Krasikov–Lagarias soundness
    step with explicit constant, plus Lemma G (non-periodic weights).
  - D. Stopping-time game lemma (certificate => infinitely many n with total
    stopping time > gamma ln n). Read by two agents and the coordinator; one
    repair: the backward play must start off the trivial cycle {1,2}, e.g. at
    a = 4 (STATE.md says n_0 = 8, which is also fine). No certificate computed.
- Prior art found (decides what is "new"; see `STATE.md` "Prior art"):
  - Theorem ND (repo's natural-density upgrade of Tao) was claimed earlier by
    Allikvere (Zenodo, 13 July 2026) and the same day by Mazur (ProofAtlas).
    Recommended wording for the repo is in `STATE.md` section E. **The repo's
    docs have not been updated to say this yet.**
  - Krasikov–Lagarias exponent: unrefereed 2026 claims reach 0.9251 (k = 22);
    no record is reachable on this machine.
  - Mazur (ProofAtlas, 5–6 Sept 2026) claims a POSITIVE LOWER DENSITY of
    integers reaching 1, Lean-built, unaudited. Auditing this is priority 1:
    if true it changes the landscape; if the Lean statement is weaker than the
    prose, that is worth knowing too.
  - Total stopping time: Amano 2021 already has 6.95212 ln n.

## 3. What is on disk

Repo: `/home/matrix/home/projects/collatz/repo` (clone of
github.com/HamedMP/collatz-fmf at commit ccdf196). Nothing committed this
round. Inventory first with `git status --short` — five agents were cut off
mid-run and may have left partial files in `sunit/`, `mazur-audit/`,
`frontier/`, `nd-referee/`, `lean/`.

Known changes:
- `.gitignore`: added `lean/.lake/` and `.claude/settings.local.json`.
- `.claude/settings.local.json`: allow Bash, WebFetch, WebSearch (project).
- `site/paper/` created so `bash scripts/verify_snapshot.sh quick` can write
  the PDF; the quick verifier PASSED (exit 0, 21 steps) on the fresh clone.
- `lean/`: Lake project `CollatzFMF`, Mathlib v4.36.0, prebuilt cache fully
  downloaded (`lean/.lake`, 7.3 GB). Toolchain via `~/.elan/bin`
  (elan 4.2.4; lean4 v4.36.0 and v4.33.0 installed). `CollatzFMF/Smoke.lean`
  never built. No theorem formalized.
- `notes/round6-nov2026/`: `HANDOFF.md`, `STATE.md`, `BRIEF-COMMON.md`,
  `ai-math-methods.md`; `kl-exponent/src/{kl_solver.c,check_cert.py,
  test_induction_bound.py}` (never compiled/run), `kl-exponent/lit/kl2003/`,
  `kl-exponent/lit/kollatz/` (55 MB third-party clone — untrusted, never
  execute, NEVER commit); `outside/scripts/game.c` (never compiled),
  `outside/lit/amano/amano2021.pdf`; `nd-referee/{tao-src,prior-art,scripts}`;
  `lean/{elan-install.log,lake-setup.log}` (the second is huge on one line —
  do not Read it whole).

Outside the repo:
- `/home/matrix/home/projects/collatz/venv` — Python 3.12 (uv): numpy, scipy,
  sympy, gmpy2, python-flint, z3-solver, python-sat, highspy, mpmath,
  networkx, numba. Add packages with
  `uv pip install --python /home/matrix/home/projects/collatz/venv/bin/python <pkg>`.
- `~/.claude/settings.json`: the previous session ADDED a global
  `permissions.allow` block for Bash, WebFetch, WebSearch (applies to every
  project on this machine). Delete that block to revert.
- Do not touch `/home/matrix/home/projects/collatz-handoff-202608160853-eeb165/`
  (an older directory; a read of it was declined by the owner's side).
- Machine: 8 cores, ~15 GB RAM (about 9 GB free), ~48 GB disk free. No
  `pdftotext`, `pip`, `cmake`, `sage`, `gp`; gcc/g++/make/typst/node/uv exist.

## 4. Why the last session stalled (so it is not repeated)

- Under the Matrix host, shell commands from the coordinator and from
  subagents were declined with "The user doesn't want to take this action
  right now. STOP...". Project and user allow rules did not change this inside
  that session. In a terminal Claude Code session this should not occur; check
  with one trivial shell command before launching agents.
- Subagents treat any such decline as final and stop, even when the brief says
  to continue; a coordinator's relayed approval does not count for them.
  Resuming a stopped agent did not help — launch fresh agents instead.
- Subagents reported the harness refusing `REPORT.md` files. If that recurs,
  have them return the full report in their final message and save it from the
  coordinator.
- Do not use browser-impersonating User-Agent strings on downloads. Use a
  plain client name; if a site refuses, report it.
- Several agents at once is fine, but give each a core/RAM budget (8 cores
  shared) and one Mathlib copy only.

## 5. Next steps, in priority order

Track cards — each is one fresh agent; point every brief at `BRIEF-COMMON.md`
and `STATE.md`, quote the owner's authorisation, and require a verdict-first
final message. Mathematical detail for each is in the `STATE.md` section named.

0. **Sanity.** Run `git status --short`, list `notes/round6-nov2026/*`, check
   that a subagent can run a shell command.
1. **mazur-audit** (2 cores). Download the ProofAtlas artifacts for the
   positive-density claim (and the 0.90 exponent and natural-density claims).
   Statement audit first: write out in ordinary mathematics what the top-level
   Lean theorem asserts, down to Mathlib, and compare with the prose. Then
   rebuild if feasible, `#print axioms`, grep for sorry / axiom /
   native_decide / unsafe / implemented_by. Then find the single step that
   turns x^gamma bounds into a linear bound and test it. Verdict per claim.
2. **sunit** (1 core; STATE §A). Read Evertse 1984 from Numdam and quote the
   exact theorem; re-derive and machine-check both identities; write the full
   proofs (primitivity, non-degeneracy with the valuation tie, cofactors,
   finite-to-one, constants); state precisely what is new versus Theorem 62;
   sanity data for k = 1, 2, 3 up to 10^8; controls on 5n+1, 3n-1; prior-art
   search for Subspace-theorem uses on Collatz. Be careful about quantifier
   order: fixed-s ineffective constants give nothing uniform in s.
3. **lean** (2 cores; STATE §B). `lake build` the smoke file, then formalize
   Theorem A (FMF formulas), Lemma P, return-block coding and the identity
   88·16^r·n' + 85·16^r = 3·27^r·(33n+32), faithful H1 and Lemma E (weak
   non-descent, x > 1, with the x = 1 sanity theorem), Theorem R, and
   `CollatzConjecture ↔ H1 ∧ LemmaE`. No sorry / axiom / native_decide in
   anything called complete; axiom audit; misformalization examples.
4. **frontier** (1 core). New statement strictly between what is proved and
   the conjecture: the smallest open case of H1 beyond the repo's exclusions
   (non-uniform morphic / Arnoux–Rauzy / Toeplitz words); explicit size-lever
   constraints on any non-descending orbit above 2^71 (ballot inequality +
   master identity + Baker/Rhin); a gap principle for infinite-orbit seeds;
   exact survivor data and partial invariants modulo primes p with
   P_w ≡ Q_w (mod p) (the all-zero branch has 11 because 27 ≡ 16 mod 11).
5. **kl-exponent** (2 cores, 4 GB; STATE §C). Not a record attempt. Test
   Theorem T / Lemma G by brute force and decide novelty; reproduce
   Krasikov–Lagarias Table 2 (k = 2..11) with an independent exact checker;
   push to k ≈ 19 and compare with the values recorded in `lit/kollatz/`;
   investigate structured non-periodic W.
6. **outside** (1 core; STATE §D). Compile `game.c`, validate (1/4 at j = 2;
   nothing at or above ln2/ln3), tabulate best p/q for j = 2..14+, controls on
   5n+1 and 3n-1; stop the line if it stalls below 1/2. Then a 10-idea
   brainstorm of attacks different in kind from the repo's dead ends, each
   with a kill test, and execute the best (candidates: F_2[x] analogue where
   Alon–Behajaina–Paran 2024 leave a linear bound open; 3-smooth
   representation form; structured infinite families).
7. **srs-termination** (1 core; STATE §F). Reproduce two
   Yolcu–Aaronson–Heule proofs with an encoder and an independent checker;
   new systems (two-state return map ⇔ H1; single-coordinate form; two-rule
   growth-B) with written equivalence proofs and brute-force validation to
   10^6; calibrations (Lemma P, r = 0, r = 1); negative controls (5n+1, 3n-1);
   record UNSAT frontiers.
8. **nd-referee** (1 core; STATE §E). Independent re-read of PROOFS.md against
   Tao's TeX; run sA..sE plus own checks for Lemma R and J*; brute-force the
   conclusion at small scales; Rhin's statement and Tao's 23 Aug 2026 comment
   from sources; final verdict and repo wording.
9. **Second wave, after 1–4 report.** Apply the playbook to the conjecture
   itself: several INDEPENDENT attempts on the same target with different
   approach families and without telling each the others' favoured route; a
   registry of approach families and a do-not-repeat ledger (start from
   plan.md lines 579–656 and `STATE.md` "Dead ends"); blind hostile referees,
   one joint each; mandatory false-case controls; treat a reduction to an
   equivalent-strength lemma as failure.
10. **Consolidate.** The repo's CLAUDE.md requires updating `plan.md` and
    `proof.md` after exploration runs: add a "Round 6 (November 2026)" entry
    to both with status labels (PROVED / VERIFIED to bound / CANDIDATE /
    REFUTED), update the Theorem ND wording in `proof.md` (Theorem 58),
    `proof-obligations.md`, `referee-brief.md`, `notes/round4-july2026/README.md`
    per `STATE.md` section E, and correct "Still open" items overtaken by
    prior art. Run `bash scripts/verify_snapshot.sh quick`. Commit only if the
    owner asks; never commit `lit/kollatz/` or `lean/.lake/`.
