<!-- Saved by the coordinator from the srs-termination agent's final message (the agent's own write was refused). -->
# srs-termination track — REPORT (round 6, November 2026)

## (a) Summary

1. Built a SAT encoder for matrix-interpretation certificates (natural and arctic; extended-monotone "full" and weakly-monotone "top" variants; relative termination with rule removal) and a checker sharing no code with it.
2. The checker accepts three certificates transcribed from the Yolcu–Aaronson–Heule (YAH) paper (natural/full, natural/top-reversed, arctic/top-reversed d = 5 Farkas) and rejects a mutated one.
3. Reproduced by search 16 published YAH results: S∖{tO→2O}, the four mod-4 systems, and all 11 one-rule-deleted subsystems of T. Farkas was not reproduced by search.
4. Three new systems with written equivalence proofs and 10^6 validation: RET (⇔ H1), W (⇔ H1+, implies H1), G (⇔ all growth-B chains finite, implies H1).
5. H1+ has no cycles (PROVED); no infinite orbit for z ≤ 10^11; it is not known to follow from Collatz.
6. YAH's open "5 mod 8" conjecture implies SN(G), hence H1 (PROVED).
7. Calibrations partly fail: r = 0 found; Lemma P found only in the adapted coordinate; r = 1 not found.
8. Six negative controls: no rule removed from any.
9. Open systems RET, W, G, W01: no rule removable at any tested shape; the frontier equals that of the controls, so it is not evidence.
10. H1 reduces to relative termination of one rule in W (PROVED, certificates checked).

## (b) Statements

### B.0 Conventions

Symbols: `f` (x↦2x), `t` (2x+1); ternary digits `0,1,2` (x↦3x+d); `L` (constant 1, the leading digit); right markers `R`, `R0`, `R1` (x↦x) and `O` (x↦2x+1). A string s1…sk denotes s_k∘…∘s_1, as in YAH.

Auxiliary rules X = A ∪ B, each value-preserving:
- A = {f0→0f, f1→0t, f2→1f, t0→1t, t1→2f, t2→2t}
- B = {L0→Lt, L1→Lff, L2→Lft}

A canonical string is `L w m` (w digits, m a marker). For interpretations, [s1…sk] = [s1]∘…∘[sk].

### B.1 Soundness of the four certificate types — PROVED

"T removable from 𝓡" means SN(T rel 𝓡). Rule removal: SN(T rel 𝓡) and SN(𝓡∖T) give SN(𝓡).

**N-full.** Each symbol σ ↦ x ↦ M_σx + v_σ on ℕ^d with (M_σ)_{11} ≥ 1. All rules satisfy M_l ≥ M_r, v_l ≥ v_r; T-rules also (v_l)_1 > (v_r)_1. Then T is removable.

*Proof.* Let φ(w) = ([w](0))_1. For a step u l v → u r v put y = [v](0). Then [l](y) − [r](y) ≥ v_l − v_r ≥ 0 componentwise, with first component ≥ 1 for a T-rule. Applying [u] (M_u ≥ 0, (M_u)_{11} ≥ 1) keeps the difference ≥ 0 and the first component ≥ 1. So φ ∈ ℕ never increases and drops at T-steps. ∎

**A-full.** Matrices over ℕ ∪ {−∞} (max, +) with (M_σ)_{11} finite. All rules M_l ≥ M_r; T-rules M_l ≫ M_r entrywise (a ≫ b iff a > b or a = b = −∞). Then T is removable.

*Proof.* ≥ and ≫ survive max-plus multiplication on both sides. Products keep a finite (1,1) entry. So φ(w) = [w]_{11} ∈ ℕ never increases and drops at T-steps. ∎

**N-top / A-top.** Let K be a symbol set such that every rule either has no K-symbol, or has a K-symbol first on both sides and nowhere else; every T-rule starts with a K-symbol.
- N-top: affine maps on ℕ^d, no condition on M_{11}; all rules weakly decreasing; T-rules (v_l)_1 > (v_r)_1.
- A-top: max-plus affine maps over ℤ ∪ {−∞} with (M_σ)_{11} ≥ 0 or (v_σ)_1 ≥ 0; all rules weakly decreasing; T-rules M_l ≫ M_r and v_l ≫ v_r.

Then T is removable.

*Proof.* Write a string as w_0 k_1 w_1 k_2 w_2 … with k_i ∈ K. No left-hand side straddles two blocks, and every rule preserves the block structure. In an infinite derivation with infinitely many T-steps, some block k w receives infinitely many; projecting to it gives an 𝓡-derivation where every T-step is at the left end. With x_0 = 0 (N-top) or (0, −∞, …) (A-top), φ(w) = ([w](x_0))_1 ∈ ℕ. Monotonicity gives no increase in any context. A left-end T-step strictly decreases φ: in A-top, [r s](x_0)_1 is finite and attained by a finite term whose l-counterpart is larger. ∎

Right-marker rules use the reversed system (SN is reversal-invariant). `check.py` verifies all conditions, including the marker condition with K computed as a closure, in exact integers.

**Monotonicity remark (PROVED).** A certificate removing ρ from 𝓡 also removes ρ from any 𝓡′ ⊆ 𝓡 containing ρ. So UNSAT for a subsystem is UNSAT for every supersystem at that shape, for that rule.

### B.2 Simulation lemma — PROVED

Let D be dynamic rules u m → v m′, with u a nonempty binary string and v having fewer binary symbols than u. Let F be a partial map on (value, marker) with:
- (i) F(m(u(x)), m) = (m′(v(x)), m′) for all x ≥ 0;
- (ii) the rule classes are disjoint and F is undefined elsewhere.

Let E be the exception points m(u(0)), one per rule.

**Lemma S.** If no point of E lies on an infinite F-orbit, then SN(D ∪ X) ⇔ F has no infinite orbit from any (m(y), m) with y ≥ 1.

*Proof.*
1. Cut a string after each marker and before each L. No left-hand side straddles a cut, so derivations split into pieces of forms c, L c, c m, L c m.
   - On c and L c only X applies, and SN(X) holds (YAH; also certified in my chains).
   - On c m, B never applies, A preserves the number of binary symbols, and dynamic rules decrease it.
   - So SN ⇔ no canonical string has an infinite derivation.
2. On canonical strings, X-steps preserve the value and dynamic steps apply F. By SN(X), an infinite derivation gives an infinite F-orbit.
3. Given an infinite F-orbit avoiding E, take the canonical binary string of z_0. F defined means y = 2^{|u|}k + val(u) with k ≥ 1 (k = 0 is the exception), so the rule matches. The X-normal form of L c is pure binary, so the string rewrites to the canonical binary string of z_1. Repeat. ∎

### B.3 The new systems

| name | dynamic rules (plus X) | arithmetic map |
|---|---|---|
| RET | `tttR0→22R0`, `ffffR0→00R1`, `fttR1→102R0`, `tttfR1→220R1` | depth 0: n≡7 (8) ↦ (9n+1)/8; n≡0 (16) ↦ 9n/16 to depth 1. Depth 1: n≡3 (8) ↦ (27n+7)/8 to depth 0; n≡14 (16) ↦ (27n+6)/16 |
| W | `ffffR→000R`, `tttR→22R` | z≡0 (16) ↦ 27z/16; z≡7 (8) ↦ (9z+1)/8 |
| G | `ttO→2tO`, `tftO→20O` | odd x≡7 (8) ↦ (3x+1)/2; x≡11 (16) ↦ (9x+5)/8 |
| W01 | `tttR→22R`, `tftffffR→12122R` | z≡7 (8) ↦ (9z+1)/8; z≡80 (128) ↦ (243z+16)/128 |
| P | `ttftR→211R` | m≡13 (16) ↦ (27m+1)/16 |

RET uses the paper's binary-depth normal form (m = 24n+23 at depth 0, 24n+13 at depth 1). Its block map 0→1^r→0 is the return map T(n) = (3·27^r w − 85)/88 with 33n+32 = 16^r w.

**Theorem A (PROVED). SN(RET) ⇔ H1.**

*Proof.* Lemma S applies; the exceptions (7,R0), (0,R0), (3,R1), (14,R1) all stop within two steps. So SN(RET) ⇔ F_RET has no infinite orbit on n ≥ 1.
- (⇐ H1) If depth 0 recurs forever, consecutive depth-0 states form an infinite T-orbit. Otherwise the tail is n ↦ (27n+6)/16 forever; but 16(11n′+6) = 27(11n+6) (Lemma P, since 11m+1 = 24(11n+6)), forcing 16^k | 11n_0+6 for all k.
- (⇒ H1) An infinite T-orbit expands blockwise; n = 0 is stuck after one step. ∎

Every (n, depth) is a genuine Collatz state, so Collatz implies SN(RET).

**Theorem B (PROVED).**
1. SN(W) ⇔ H1+ := "F_W has no infinite orbit on positive integers".
2. H1 ⇔ F_W has no infinite orbit from z ≡ 10 (mod 11).
3. H1+ ⇒ H1.
4. F_W has no positive cycle.

*Proof.*
1. Lemma S; exceptions z = 0 (not positive) and z = 7 (7→8 stops).
2. For z = 33n+32 = 16^r w: r first-branch steps give 27^r w. The second branch applies iff w ≡ ε_r (8), and (9·27^r w+1)/8 = 33T(n)+32. Conversely the class z ≡ −1 (11) is invariant; the first branch cannot repeat forever; after a second-branch step z′ ≡ 2 (3), so z′ = 33n′+32.
3. Follows from 2.
4. F(z) > z on both branches. ∎

For z ≢ 10 (11) there is no Collatz meaning (m = (8z−3)/11 is not an integer), so H1+ is not implied by Collatz. Is H1+ true? CONJECTURED, not refuted. VERIFIED to 10^11:
- longest orbit is 16 steps (z = 32175923263);
- the count of z ≤ B with orbit length ≥ L matches (3/16)^L·B at every L down the table.

The fixed points z = 0 and z = −1 are unrepresentable because L is the digit 1.

**Theorem C (PROVED).**
1. SN(G) ⇔ no odd x ≥ 3 starts an infinite growth-B chain.
2. Collatz ⇒ SN(G) ⇒ H1.
3. YAH's open conjecture "every nonconvergent Collatz trajectory contains some n ≡ 5 (mod 8)" (termination of their S_2 = S∖{tfO→O}) implies SN(G).

*Proof.*
1. Lemma S; exceptions 7 and 11 (7→11→13 stops). For Type-B x = 2^{t+2}m − 1, the first branch lowers depth t ≥ 1 by one (m ↦ 3m). At depth 0 the hop is growth-B iff x ≡ 11 (16), and then F(x) = (9x+5)/8. So t first-branch steps plus one second-branch step are one growth-B hop.
2. An infinite T-orbit is an infinite depth-{0,1} chain. Growth-B hops multiply by more than 9/8.
3. x ≡ 7 (8) is S's rule tO→2O. For x ≡ 11 (16), tO→2O gives y = (3x+1)/2 ≡ 1 (8), then ffO→0O gives (3y+1)/4 = (9x+5)/8. So infinite F_G-orbits are infinite S_2-orbits. Directly: odd iterates along an infinite chain are ≡ 7, 3, 1 (mod 8), never 5 (`yahrel.py`, VERIFIED to 10^6). ∎

The converse of 3 is not claimed. YAH's "5 or 7 mod 8" map H contains our r = 0 letter ((9n+1)/8 on n ≡ 7 mod 8) but does not obviously imply H1.

**W01 (PROVED via Lemma S; exceptions 7, 80).** SN(W01) ⇔ no infinite F_W-orbit with all return letters in {0,1}, from any positive z. On z ≡ 10 (11) this is the open {0,1}-alphabet slice of H1.

### B.4 Calibrations (provably terminating)

Hand proofs (PROVED): in each case a fixed linear form gains unbounded 2-adic valuation.
- r = 0: n+1 ↦ 9(n+1)/8.
- Lemma P: 16(11m′+1) = 27(11m+1); in n: 16(11n′+6) = 27(11n+6).
- r = 1: 128(115z′+16) = 243(115z+16).
- G depth-0 rule: 8(x′+5) = 9(x+5).
- G depth-lowering rule: x+1 ↦ 3(x+1)/2.

| system | fact | found? |
|---|---|---|
| RET-r0 `tttR0→22R0` | r = 0 only | YES, full chain, d ≤ 2 |
| W-r0 `tttR→22R` | r = 0 only, z-coordinate | YES, d ≤ 2 |
| W-16 `ffffR→000R` | Lemma P in the z-coordinate | YES, d ≤ 2 |
| G-1 `ttO→2tO` | depth lowering | YES, d ≤ 2 |
| G0y `ffffR→f00R` | G depth-0 rule in y = x+5 | YES, d ≤ 2 |
| P `ttftR→211R` | Lemma P, m-coordinate | NO |
| RET-11 `tttfR1→220R1` | Lemma P, n-coordinate | NO |
| G-0 `tftO→20O` | G depth-0 rule, x-coordinate | NO |
| RET-r1 (2 rules) | r = 1 only, n-coordinates | NO |
| W-r1 `tftffffR→12122R` | r = 1 only, z-coordinate | NO |
| RET-no01, RET-no10 | RET minus a switching rule | partial: stuck exactly on the Lemma-P loop rule |

Frontier for the NO rows:
- P: UNSAT for all seven types through natural (2,4), (3,2) and arctic (3,3); arctic top-reversed (3,4) UNSAT; natural top-reversed (3,3) timed out at 1200 s.
- RET-11: same through arctic (3,3), except natural top-reversed (2,3), (3,2), (2,4) timed out (20–30 s). Its 20-minute run was cancelled as redundant with P.
- G-0, RET-r1, W-r1: same, except natural top-reversed (3,2)/(2,4) timeouts for RET-r1 and (2,4) for W-r1.

Conclusion: the brief's "must succeed" calibrations succeed only in part. At d ≤ 3 the method captures "trailing zeros/ones of the represented number" and nothing that needs v_2 of another linear form (11m+1, 115z+16, x+5).

### B.5 Negative controls

| system | dynamic rules | loop replayed by `loops.py` |
|---|---|---|
| C5 (5n+1) | `fR→R`, `tR→dR` | 21 steps through 13 |
| C3m (3n−1) | `fR→R`, `tR→1R` | 7 steps through 5 |
| FMF5 | odd-to-odd form of 5n+1 | 18 steps |
| FMF3m | odd-to-odd form of 3n−1 | 5 steps (5↔7) |
| S3m | 3n−1 analogue of YAH's S | 31 steps through the 17-cycle, all 12 rules used |
| G5 | x=4k+1 ↦ 10k+3, x=64k+19 ↦ 10k+3 | 10 steps (13, 33, 83) |

Each is non-terminating by its replayed loop, and no loop rule is removable.

Result over the quick schedule (seven types):
- every call was UNSAT or timed out; zero rules removed from any control;
- natural decided through (2,4) and (3,2), with (3,3) mostly timing out at 30 s;
- arctic decided through (3,3)/(3,4).

`audit.py` reports "CONTROL OK" six times.

A sign-flipped W is not a usable control: its fixed point z = 1 = `L R` matches no rule.

### B.6 Frontier for the open systems

(d,V): dimension d; coefficients {0..V−1} (natural) or {−∞, 0..V−2} (arctic). Stage 0 throughout: nothing was ever removed from RET, W, G or W01.

| type | W | G | RET | W01 |
|---|---|---|---|---|
| nat full (both orientations) | U to (2,4), (3,2); (3,3) T30 | same | same | same |
| nat top-org (B rules) | U to (2,4), (3,2); (3,3) T30 | same | same | same |
| nat top-rev (dynamic rules) | U to (2,4), (3,2); (3,3) **T1200** | U to (2,4), (3,2); (3,3) **T1200** | U to (2,3), (3,2); (2,4), (3,3) T30 | U to (2,4), (3,2); (3,3) T30 |
| arc full | U to (3,4) | U to (3,4) | U to (3,4) | U to (3,4) |
| arc top-org | U to (3,3); (3,4) T30 | same | same | same |
| arc top-rev | U to (3,4) | U to (3,4) | U to (3,3); (3,4) T30 | U to (3,3); (3,4) T30 |

The controls (B.5) and the unfound calibrations (B.4) produce the same table. An UNSAT frontier here is information about the method only.

**One-rule deletions** ("mini" schedule: natural d ≤ 2, arctic d ≤ 2, 8 s per call):

| system | full checked proof | partial | nothing removed |
|---|---|---|---|
| W | minus `ffffR→000R`, `tttR→22R`, f1, f2, t0, t1, L0 | — | minus f0→0f, t2→2t, L1→Lff, L2→Lft |
| G | minus `tftO→20O`, f1, f2, t0, L0 | — | minus `ttO→2tO` (= G-0), f0, t1, t2, L1, L2 |
| RET | minus f0, f1, f2, t0, L0 | minus 0→1 or 1→0: stuck on the P-loop; minus t1: stuck on the P-loop; minus t2: only `tttR0→22R0` removed | minus 0→0, minus 1→1 (the r ≤ 1 slice), minus L1, minus L2 |

Deleting an auxiliary rule changes the arithmetic meaning; those proofs are not slices of H1.

### B.7 Reproduction of YAH

| system | my smallest found | YAH's script parameters |
|---|---|---|
| S∖{tO→2O} | natural top-rev d=2, V=3 | natural d=2, width 5 |
| C-0mod4 | natural d=3, V=3 (54 s) | natural d=3, width 4 |
| C-2mod4 | natural d=1 | natural d=2, width 4 |
| T-1mod4 | natural d=2, V=3 | natural d=2, width 4 |
| T-3mod4 | natural d=2, V=5 | natural d=3, width 5 |
| T minus one rule, 9 of 11 | d ≤ 2 with free rule removal | D = 1–5 in their table |
| T∖{f0→0f} | natural top d=4, V=2 | natural D=4, V=2 (same) |
| T∖{L2→Lft} | arctic top d=4, V=3; natural (4,2) timed out at 300 s | arctic D=4, V=3 (same); natural D=4, V=4 |
| Farkas | not found: arctic top-rev d=5, V=8 timed out at 1200 s twice (default and negative phase) | arctic d=5, V=8 |

Notes:
- Their width also caps composed entries; mine does not. My V is therefore a weaker restriction, and a smaller V on my side is expected.
- Their Farkas timings: single CaDiCaL 44 s with negative branching, over 240 s with phase saving; 9 s with 8 parallel shuffled instances.

## (c) Scripts

All in `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/srs-termination/`; PY = `/home/matrix/home/projects/collatz/venv/bin/python`.

| command | expected output |
|---|---|
| `$PY validate.py 1000000` (≈4 min) | W 187499, RET 374997, G 187498, P 62499 rule applications validated; exception lists as in B.3; three `cross` lines; `identities … OK` (saved in `logs/validate.log`) |
| `$PY validate.py 1000000 W01` | 132810 applications; exceptions (7), (80) |
| `$PY yahrel.py` | `yahrel: OK for all odd x <= 1000000 (125001 growth-B hops …)` |
| `$PY loops.py` | six loop lines |
| `$PY wsearch.py 100000000000` | records up to (16, 32175923263) (saved in `logs/wsearch_1e11.log`) |
| `$PY check.py published/yah_*.json` | `step OK` each; `published/MUTATED_should_fail.json` gives `CHECK FAILED` |
| `$PY audit.py` | 85 chains all `checker:OK`, 40 full proofs, six `CONTROL OK`, `ALL CHECKS PASSED`, then all frontier tables (saved in `logs/audit_final.txt`) |
| `bash runq.sh <phase>` | reruns calib, neg, main, front, yahT, sub, farkas, calib2, or `deep W` |

What `validate.py` cross-checks, all for inputs ≤ 10^6:
- the two-state block map equals the paper's T(n) and the W-block on z = 33n+32;
- the two-state map equals the real Collatz FMF growth-B hop onto a continuing Type-B state of depth ≤ 1;
- a G-run equals the real growth-B hop.

Files: `encoder.py`, `check.py`, `prove.py`, `systems.py`, `certs/`, `results/*.jsonl`, `published/`, `lit/yah/` (arXiv source), `lit/yah-code/` (YAH GitHub repo, read only, nothing executed). Solver: CaDiCaL 1.9.5 via python-sat on one shared core, so wall-clock timeouts are pessimistic.

One checker/driver disagreement occurred and was resolved. `check.py` rejected a SAT answer on RET minus f0→0f because its marker set was not closed under R0↔R1. The certificate was sound; the checker's condition was corrected to the closure in B.1 and the run repeated.

## (d) Dead ends

1. **RET in n-coordinates with small interpretations.** It contains the Lemma-P loop `tttfR1→220R1`, which the solver cannot remove even from the one-rule system RET-11. By monotonicity it cannot be removed from RET at those shapes. Use W.
2. **Lemma P in m-coordinates (system P).** Same reason: v_2(11m+1) is invisible at d ≤ 3.
3. **Reading UNSAT as evidence.** The open systems and the non-terminating controls have the same frontier.
4. **A negative-integer control for W.** The fixed point z = 1 is not rewritable.
5. **Farkas by single-core search.** 2 × 1200 s timeouts; it needs YAH's parallel shuffled instances.
6. **Adapted coordinates for two-rule systems.** Moving a fixed point to 0 trivialises one rule (W-16, G0y), but the two rules of W, G or W01 have different fixed forms (z and z+1; x+1 and x+5; z+1 and 115z+16).
7. **Tropical variant.** The draft's version was removed unrun; no soundness proof was written.

## (e) Best lead

**Target lemma.** There is an N-top or A-top interpretation of rev(W) in which all 11 rules are weakly decreasing and `R t t t → R 2 2` (or `R f f f f → R 0 0 0`) is strict.

Either instance proves H1+, hence H1, because W∖{ffffR→000R} and W∖{tttR→22R} are already certified terminating (`certs/W~0.sub.json`, `certs/W~1.sub.json`). Frontier to beat: natural (3,3) undecided after 1200 s; arctic UNSAT through (3,4).

Suggested order:
1. **W01**, where both one-rule subsystems are provable and the statement is an open slice of H1.
2. **An alphabet in which a second linear form (z+1 or 115z+16) is carried explicitly**, since the calibrations show only valuations of the represented number are visible.
3. **YAH-scale parallel compute.** They spent thousands of CPU hours on S_1 and S_2 without success, and S_2 implies SN(G).

## Brainstorm record

| # | idea | kill test | outcome |
|---|---|---|---|
| 1 | RET in n-coordinates | one-rule subsystems | dead end 1 |
| 2 | W single coordinate | does Lemma P become trivial? | yes; best target |
| 3 | G growth-B system | relation to YAH | implied by their open S_2 |
| 4 | weakly monotone top certificates on reversed systems | YAH S_3, mod-4 | reproduced |
| 5 | arctic | Farkas | checker passes; search fails |
| 6 | one-rule deletions | which stay hard | B.6 |
| 7 | adapted coordinates | W-16, G0y | single rules only |
| 8 | composite bounded-alphabet system W01 | quick schedule | nothing removable |
| 9 | controls with replayed loops | `loops.py` | pass |
| 10 | 3-adic mirror system (proof.md Theorem 61) | — | not attempted |
| 11 | negative phase | Farkas | no help in 1200 s |

## Confidence

- B.1, Lemma S, Theorems A–C: PROVED; ≈ 95% each.
- Each "U": ≈ 90% a true UNSAT. Encoder completeness is supported only by the 16 reproductions and by matching YAH's (4,2) and (4,3) parameters on two rows.
- H1, H1+, SN(G): no change in credence.