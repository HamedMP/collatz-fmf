<!-- Saved by the coordinator from the nd-referee agent's final message (the agent's own write was refused). -->
# nd-referee — hostile referee report on "Theorem ND" (PROOFS.md, 21 July 2026)

Referee run: 2026-11-17. Object: `notes/round4-july2026/s5-completion/PROOFS.md` (571 lines), summarised as Theorem 58 in `proof.md`. Checked against Tao's TeX (`nd-referee/tao-src/collatz.tex`, arXiv:1909.03562 v7). "TeX l.N" is a line of that file; "P l.N" is a line of PROOFS.md.

## (a) Summary

1. **Verdict: SOUND-MODULO-LISTED-REPAIRS.** No fatal gap found. Credence 0.80 that the repaired manuscript proves Theorem ND as stated. The residual risk is unwritten detail in Lemma R, and that I checked Tao's Section 7 only up to its statement.
2. Nothing silently assumes the conclusion. The sum-conditioned Fourier decay (P7) is a correct three-line conditioning. The Kronecker step (Lemma R) is true and provable but is the worst-written part and misquotes Rhin. The chain (Theorem 3-U) has uniform constants but a real, easily repaired grid mismatch.
3. 14 defects: 0 fatal, 5 fixable (STATE §E items 1–5, all confirmed, repairs checked), 9 cosmetic (new).
4. sA–sE all run and pass; my independent re-implementations reproduce their numbers. At n ≤ 8 the joint oscillation is 0.38–1.0, so the toy numerics are consistency checks, not evidence of m^-A decay.
5. Brute force to 10^8 cannot test the theorem (every n ≤ 10^8 reaches 1). It confirms direction and the litmus contrasts.
6. **No priority.** The exponent 1/25 is bookkeeping: with 7.616 the block method gives 0.4/8.616 = 0.046, and longer blocks would give up to about 1/(2·8.616) = 0.058.
7. Rhin: the printed all-heights statement has exponent 13.3; 7.616 holds only above an unprinted threshold. Primary source not obtained.
8. Tao's comment of 23 Aug 2026 is verified from the page itself (quoted in (f)).
9. Litmus passes: the argument transfers to 3n−1 and breaks for 5n+1 at five named places.
10. The bound is quantitatively vacuous at reachable scales: the chain constant is C/(1 − 1.001^(−1/25)) ≈ 25000·C, so it is nontrivial only for log N0 > 10^110.

## (b) Lemma by lemma against Tao v7

| PROOFS.md item | Tao v7 statement used (label, number, TeX line) | Follows? | New input, and is it proved |
|---|---|---|---|
| Lemma P7 (P l.98–122) | pairing identity and (7.5) `74`, TeX l.1123–1141; (7.10) `jeo` | Yes | S is the sum of the b_j (plus a_n for n odd), so it is measurable for the sigma-field Tao conditions on. Hence sum_s \|E 1_{S=s} χ\| ≤ E ∏\|f\|. Proved. |
| Lemma J* (P l.135–197) | Section 6: (6.1) `9n` reduction TeX l.928–936; (6.2) `ij`; (6.3) `ayo`; (6.5) `hepta`; (6.6)–(6.8); two-block identity TeX l.1023; Cor 6.3 TeX l.1059; Plancherel TeX l.1037 | Yes | This is the object of Remark 1.16 (TeX l.416). New: second factor summed over s' (P7 after splitting off the independent tail), and one extra Cauchy–Schwarz over O(√(n log n)) values of s. I re-derived (iv)–(ix); the powers of 3 and n balance. Needs the v6+ constant 0.99 in (6.7)–(6.8); PROOFS cites v7. |
| Prop 5.2-U (P l.205–248) | Prop 5.2 `approx-form` (5.8), TeX l.712–806; Prop 1.9 `rach` TeX l.269; Lemma 2.2 `chern`; Lemma 2.1 `iter-lem` | Yes | Density-agnostic. Narrower envelope and smaller m0; standoff (S) replaces Tao's (5.10) margin. Two constants misprinted (D5, D6). |
| Lemma K (P l.250–269) | (5.18) `max`, (5.19) `this`, TeX l.808–820 | Yes | Exact. Oddness of the reconstruction is automatic. This replaces Tao's weight identity at TeX l.823–827, the one genuinely log-density step. |
| Lemma B (P l.286–298) | none | Statement true; proof as written does not give it | D2. |
| Lemma M (P l.300–306) | Lemma 1.12 `recursive` TeX l.361 | Yes | Proved. True max-mass is about 1.46·2^-m. |
| Lemma W (P l.308–317) | (1.5) `fn-def`, (1.29) `syria` | Yes | Exact identity. |
| Lemma 5.3-U (P l.319–331) | Lemma 5.3 `loam` TeX l.858–915; (5.24) `chan`; (5.25) `mant` | Yes | Density-agnostic transplant with modulus 3^m0; one unwritten line (D10). |
| Lemma R (P l.333–399) | none (new) | True; proof incomplete as written | **The new arithmetic input**: equidistribution of {ℓ·log2 3} over a window of length about √(log x), via Erdős–Turán, Koksma and an irrationality measure. Provable as intended (D3, D4). |
| Theorem 5-U (P l.404–437) | replaces Prop 1.11 `transport`, (1.19), (1.20); limit equals Tao's (5.21) `Z-def` | Yes given the above | Assembly checked step by step, including that every Lemma-R live range lies in I_y − m0. |
| Theorem 3-U (P l.439–484) | Theorem 3.1 `main-alt` TeX l.539–588 | Yes after D1 | Dyadic covering replaces Tao's log-uniform covering (TeX l.587). |
| Theorem ND (P l.486–496) | Theorem 1.3 `main` | Yes | Trivial from 3-U. |

PROOFS.md's equation numbers (5.12)–(5.26), (6.2)–(6.8), (7.4), (7.5) agree with a programmatic count of the v7 TeX.

Tao uses log density in two places. At TeX l.821–827 the 1/N weight factorises; this is replaced by K + J* + W + R. At TeX l.587 he covers [1,x] by [y, y^α]; this is replaced by dyadic blocks. Everything else is density-agnostic, as PROOFS Part I says.

## (c) Defect list

### Fatal
None.

### Fixable with repair (STATE §E 1–5; all confirmed, repairs verified)

**D1. Theorem 3-U chain grid (P l.449–451, 468–469, 473–474).** Thresholds are x_b^(α^j) with x_b fixed, but the endgame needs X = z^(1/α) for arbitrary dyadic z, which is off that grid.
- Repair: for each z put X_0 = z^(1/α), X_j = X_0^(α^-j), and stop at the first X_J < N0^(1/α).
- Then X_J ≥ N0^(1/α²) is still large, and Pass ≤ X_J ≤ N0 gives the base with probability 1 − O(X_J^-c). This is Tao's device at TeX l.569–578.
- P l.477–479: the sum must include the block containing Z, giving eps·Z rather than eps·Z/2.

**D2. Lemma B (P l.286–298).** The stated C·y·x^-0.5 does not follow: the proof invokes J*, whose error y·|I_y|·m0^-30 is only polylogarithmic, and the text trails off at l.293.
- Repair A (STATE's): state the bound as C·y·x^-0.6 + C·y·|I_y|·m0^-A ≤ y·log^-10 x, which is all 5-U(c) needs.
- Repair B (mine, keeps the stated bound): use no J*. Bound P(S=s, X≡M mod 3^ℓ) ≤ C(2/3)^ℓ by Lemma M at full scale, and 2^s ≤ 4·3^ℓ·y/M. The contribution is then ≤ C·y·Σ_ℓ 2^ℓ Σ_{M∈Bdry} 1/M ≤ y·x^-0.69, since 2^ℓ ≤ x^(0.0073+o(1)).

**D3. Lemma R step (4) (P l.368–379) and error terms (P l.348–350, 366–367).** Step (4) is not a proof as written ("Int := … handled below").
- Repair: on a block, P(S_k = s*(ℓ) − t) = G(ℓ_1)(1 + O(J0·K/√k) + O(K³/√k)); then apply Koksma to w(u) = 2^(1−u) alone.
- The LLT error is relative O(K³/√k), not absolute O(k^-3/2); its sum is still log^(-1/2+o(1)) x.
- Exponents close as claimed: 0.4/8.616 = 0.0464 > 1/25, and freezing costs log^(-0.1+o(1)) x.
- The t-hypothesis at l.335–336 is garbled. The lemma needs only that the live range lies in I with k ≥ c·log x there.

**D4. Rhin (P l.383–386, 511–513).** "≥ H^-7.616 for H ≥ 2" is a misquotation (see (f)).
- Repair: use ||q·log2 3|| ≥ c·q^-7.616 for all q ≥ 1, with c > 0 absorbing small q. The Erdős–Turán step is unchanged.
- Consequence to state: the constant C in Theorem ND is not explicit.
- With only the printed all-heights exponent 13.3, the same proof gives exponent 0.4/14.3 ≈ 0.028 (1/36), not 1/25.

**D5. Prop 5.2-U(3) (P l.228).** (3/4)^n0 = x^-0.0415, not x^-0.125; the conclusion ≥ x^0.87 stands.

### Cosmetic (new)

- **D6.** P l.241–242: should carry e^-(2·Lam·log 2 + C). It needs m0·log(4/3) > 2·Lam·log 2 + Lam''; (S) gives 10·Lam''.
- **D7.** P l.423–424: "m0^-A beats every power of log x" is false; m0^-A = log^(-A/2+o(1)) x. With A = 750 the needed log^-10 x holds.
- **D8.** P l.144–154: telescoping indices are inconsistent. Correct as TeX l.928–936.
- **D9.** P l.218–221: Prop 1.9 needs d_TV ≪ 2^-n' = x^-0.3 (TeX l.271). It holds; the distance is in fact exactly 0 because y is a power of two ≥ 2^(3·n0).
- **D10.** P l.327–331: the terms with 2^|v| > x^(1/2) are unwritten; they are negligible.
- **D11.** P l.261–267 and l.279–280: the "CAUTION" paragraph is muddled and the "type (ii) EMPTY" clause is unnecessary.
- **D12.** P l.203 and sA's "decay … visible": at n ≤ 8, Osc^J is 0.38–1.0, so there is no evidence of decay. sE prints 1.34 where the lemma says 1.36.
- **D13.** P l.530–538 (sD): the toy regime y/x = 2^9 is outside the theorem's regime. My enumeration gives TV 0.0059 at x = 2^10, 2^12, 2^14 with y/x = 2^10, and 0.012 at y/x = 2^8. The error is governed by log(y/x).
- **D14.** P l.561–571 and Theorem 58: the claim to be "answering the question he raises" must give way to the attribution in (h).

Observation on Tao v7, not on PROOFS: TeX l.913 sums 2^(-a/2) over m0 letters, which is (1+√2)^m0 rather than O(1). The sharper bound 2^-|a|·a_m0 at TeX l.895 does sum to O(1), and PROOFS uses that form, so it is unaffected.

## (d) Scripts and outputs (one core, `taskset -c 7 nice -n 5`)

Their scripts, run from `notes/round4-july2026/s5-completion/`; full outputs in `nd-referee/out/`:

| Script | Time | Result |
|---|---|---|
| sA_joint_mixing.py | 4 s | ALL PASS (A1, A1-n2, A2, A3, A4); Osc^J/Osc ratio 1.27–1.80 at n = 6..8 |
| sB_phased_sec7.py | 14 s | ALL PASS; e.g. n=7, ξ=1: 0.04883812 ≤ 0.26975630 |
| sC_lemmaR.py | 4 min | ALL PASS; worst error 1.0e-2 (300), 4.6e-3 (1000), 1.9e-3 (3000), 1.7e-3 (6000); factor 2.409422 vs 2.409421 |
| sD_endtoend.py | 2.5 min | ALL PASS; TV 0.00204 / 0.00153; excess +0.399, +0.276, +0.189, +0.124, +0.075 |
| sE_maxmass.py | 27 s | ALL PASS; C = 1.354503 |

My own code, in `nd-referee/scripts/`, with no reuse of theirs:

- **`ref_lemmaR.py` → `out/ref_lemmaR.out`.** For slope log2 3, K → 3.4760595 with max error 3.0e-2 (k=30), 4.9e-3 (1000), 1.7e-3 (10^4), 1.3e-3 (10^5), over 48 random (phase, t, m0) per scale.
  - Rational slopes 3/2, 8/5, 19/12 give phase-dependent K with spreads 0.99, 0.49, 0.19 that do not shrink.
  - Slope 8/5 + 10^-9 behaves like 8/5 at every tested scale, so an irrationality *measure* is what is needed.
  - Slope log2 5 also converges (to 1/ln(5/4)), so Lemma R alone does not see the sign of the drift.
- **`ref_Jstar.py 8` → `out/ref_Jstar.out`.** Tao's Z/9 table is reproduced; max-mass is 1.46·2^-m; the Osc^J table agrees with sA to about 4e-5. The P7 inequality holds in all 35 rows (n = 4..8) and matches sB exactly where they overlap.
- **`ref_cf_log23.py` → `out/ref_cf_log23.out`.** Over 293 convergents up to q = 10^150, the max partial quotient is 964, min ||qβ||·q = 0.00104, and min ||qβ||·q^7.616 = 0.415 (at q = 1).
- **`brute.c` → `out/brute.out`** (62 s CPU):
  - (A) Every n ≤ 10^8 has an iterate below itself (longest stopping time 613 at n = 63728127), so the exceptional proportion is exactly 0 for any f ≥ 1.
  - (B) Odd n in [N/2, N) reaching ≤ ln N within t·ln n/ln(4/3) Syracuse steps, at N = 10^8: 0.555 (t=1), 0.885 (t=1.5).
  - (C) 3n+1 and 3n−1 reach ≤ 20 for all odd n ≤ 10^7. 5n+1 reaches ≤ 1000 for 45.9%, 20.7%, 9.3%, 4.2% of odd n ≤ 10^4..10^7.
  - (D) First-passage law, exhaustive, x = 2^14: uniform [y,2y) vs [2y,4y) TV 0.0060; vs log-uniform [y,8y) TV 0.0050; cumulative laws agree to 3–4 digits. This is consistent with the limit being Tao's Q.

## (e) Litmus

- **3n−1.** Every step transfers with F_n replaced by −F_n. The conclusion is true for 3n−1 and compatible with its cycles through 5 and 17, because the theorem never says the minimum is 1.
- **5n+1.** The argument fails, as it must, at five places:
  - (1.19)-U (P l.234–235): needs 3·2^-1.9 < 1, but 5·2^-1.9 > 1.
  - I_y and standoff (S) (P l.209, l.35): both divide by log(4/3) > 0.
  - Lemma R's sweep direction (P l.357): δ = 2 − log2 3 > 0.
  - Tao's Section 6 stopping time (TeX l.932): 0.9 must exceed log 3/(2 log 2) = 0.79, whereas log 5/(2 log 2) = 1.16.
  - Cor 6.3 (TeX l.1080): decay exp(−j·log(4/3)).
- The +1 enters only through F_n and Lemma 1.12. Irrationality of log2 3 enters only in Lemma R.

## (f) Sources

**Rhin.** The primary (Progr. Math. 71 (1987), 155–164) was not obtained; it is paywalled. Secondary sources, saved in `nd-referee/sources/rhin/`:
- Zudilin, arXiv:math/0404523v2, Theorem 3: "The irrationality exponent of any nonzero γ ∈ Q log 2 + Q log 3 satisfies the inequality μ(γ) < 8.616" (after Rhin). This is an exponent, i.e. asymptotic.
- Amoroso, Ann. Inst. Fourier 43 (1993), p.1182: μ(log 3) ≤ 7.616 "arises as a particular case of a linear independence measure between 1, log 2, log 3".
- Mazur (`prior-art/mazur/mazur_nd_v2.txt` l.357–367, l.1202): Rhin p.160 (7) gives |u0 + u1 log 2 + u2 log 3| ≥ H^-13.3 for H ≥ 2; (8) is the 7.616 line, whose "effective threshold is not printed in a form consumed by the proof".
- Allikvere (`paper.tex` l.767–769) also says "H large".
- Simons–de Weger could not be fetched (host did not resolve).

**Form valid for all q ≥ 1:**
- Explicit: ||q·log2 3|| ≥ (2^-13.3/ln 2)·q^-13.3.
- Non-explicit: ||q·log2 3|| ≥ c·q^-7.616 for some c > 0 not given in print.
- No later improvement for log 3/log 2 (Wu, Wu–Wang) was verified.

**Tao's blog.** Fetched with `curl -A "collatz-fmf-research/1.0"`, HTTP 200, saved as `sources/taoblog/post.html`. Comment 694077, "23 August, 2026 at 8:43 pm", Terence Tao, verbatim:

> Apparently, there are now some AI-generated solutions to the natural density version of my result; if they check out, they should be able to give something along the lines of your statement for some h(x) = o(x), and possibly even a logarithmic saving as you indicate. However, this would need to be done carefully. (My original argument now has some Lean formalizations, so perhaps this claim could also be formalized as well.)

The same page carries three other relevant comments:
- Mazur, 21 July 2026 10:39 am, announcing the ProofAtlas work.
- Allikvere, 25 July 2026, giving his timeline (Zenodo v1 July 13, v2 July 22).
- The 5–6 July exchange in which Tao replaces 1/2 by 0.99 from (6.7) onwards. This is the v6 fix that J* relies on.

## (g) Prior art

- **Allikvere.** `versions.json` shows record 21340151 created 2026-07-13T14:12:04 UTC (v1) and record 21499244 created 2026-07-22T19:48:48 UTC (v2). The on-disk `paper.tex` md5 17a3eeaa… and `paper.pdf` md5 02825ab5… match the v2 record.
  - Architecture (`paper.tex` l.138–232): Theorem B, sum-conditioned Fourier decay (= P7, in conditional rather than summed form); Theorem C, sum-conditioned mixing of the affine map (= J*); binomial identity (= Lemma K); Lemma E, weighted equidistribution along the Kronecker orbit with Rhin (= Lemma R, same block/Erdős–Turán/Koksma proof); iteration of Tao's Section 3.
  - Rate (log N0)^(-1/29) + x^(-1/2000), plus a clock of (1+o(1)) ln N/ln(4/3) Syracuse steps that the repo lacks. He quotes Rhin correctly.
- **Mazur.** "Date: Version 2, July 21, 2026" (txt l.58; PDF created 2026-07-22 01:55 UTC).
  - Different route: compares the natural-counting block law with Tao's logarithmic one by phase discrepancy, using only the explicit 13.3 statement.
  - Exponent any d < 5/143; clocks 145 ln N (Syracuse) and 436 ln N (Collatz); claimed checked in Lean 4, including a reconstruction of the Rhin input. Not audited here.
- **Repo beyond them:** nothing of substance. PROOFS.md is self-dated 21 July and first committed 2026-08-16. It is Allikvere's proof with a summed form of the Fourier bound, dyadic windows, and a nominal 1/25 resting on the misquoted Rhin statement. STATE's finding is confirmed.

## (h) Recommended wording for the Theorem ND entry

> **Theorem 58 (candidate; AI-generated, no human review).** For every N0 ≥ 16 the set {N : Col_min(N) > N0} has upper natural density at most C·(log N0)^(-1/25), with an absolute constant C that is not explicit; hence Col_min(N) ≤ f(N) for almost all N in natural density whenever f → ∞. Derivation: `notes/round4-july2026/s5-completion/PROOFS.md` (self-dated 21 July 2026; first committed 16 August 2026), to be read with the five repairs and nine corrections of the round-6 nd-referee report; an AI referee found no fatal gap. **Priority:** the result was first claimed by J. Allikvere (Zenodo 10.5281/zenodo.21340150, version 1 of 13 July 2026) by essentially the same method, and by L. Mazur (ProofAtlas, version 2 dated 21 July 2026, claimed Lean-checked) with explicit time bounds; T. Tao (blog comment, 23 August 2026) refers to such work as AI-generated solutions "if they check out". The repository claims no priority and no novelty; the exponent 1/25 is a bookkeeping choice that depends on Rhin's 1987 measure for 1, log 2, log 3 with exponent 7.616 above an unspecified height (the explicit all-heights exponent 13.3 gives about 1/36 by the same argument). Not established mathematics; excluded from `proof-obligations.md`.

## (i) Not done

- Tao's Section 7 proof of (7.10) was not re-refereed; it is taken as published.
- Rhin's paper was not read; D4 rests on concordant secondary sources.
- Mazur's Lean artifact and Allikvere's proof were not audited, only their architecture and dates.
- Numerics at reachable scales cannot distinguish a true log^-c bound from a false one.

## (j) Best lead

Rewrite Lemma R as a standalone lemma in Allikvere's Lemma E form: for a weight w of total variation V and mass W on a window, and f of bounded variation V_f,

|Σ w(n) f({nβ+u}) − W∫f| ≪ ℓ0·V + V_f·(W·ℓ0^(-1/μ) + V·ℓ0^(1−1/μ)).

With that and D1–D5 the manuscript is ready for a human referee; nothing else needs new mathematics.