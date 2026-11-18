<!-- Saved by the coordinator from the outside agent's final message (the agent's own write was refused). -->
# Round 6 — outside track report (2026-11-17)

Labels: PROVED (full proof below), VERIFIED (to the stated bound, by the stated script), CANDIDATE (believed, not proved), REFUTED. Nothing here proves or disproves Collatz.

## (a) Summary

1. **Stopping-time game: DEAD.** Lemma 1 is PROVED with the off-cycle repair. The solver was rewritten (`game2.c`), certificates are machine-verified, and the value is 1/4 at j = 2.
2. Best certified ones-ratio for j = 2..13: 0.250, 0.333, 0.375, 0.400, 0.400, 0.416, 0.431, 0.444, 0.450, 0.45, 0.46, 0.46. Increments are under 0.01 per digit.
3. The game is not the Applegate–Lagarias (A–L) certificate, but dominates it at equal digit budget (Prop. 4).
4. Controls: the 3n−1 game is isomorphic; 5n+1 gives 0.200–0.240 for j = 2..6 (ceiling ln2/ln5 = 0.431).
5. **Part 2, executed idea: the F_2[x] Collatz map.** Alon–Behajaina–Paran (ABP, arXiv:2401.03210) prove stopping time O(d^1.5). The growth of the maximum σ(d) is their open Question; they "suspect" non-linear from experiments, with no proof. The average is settled (Inselmann, arXiv:2401.12781).
6. PROVED: a path characterisation of the stopping time (Theorem A), a sparse bound (Prop. B), a cell formula (Lemma C), and a first-phase lower bound for an explicit family (Prop. D).
7. **CANDIDATE, VERIFIED to degree 262,656:** for f_j = Σ_{l=0}^{2^j} x^{(2^j+1)l}, t_min(f_j) = (4j−3)·4^j + 9·2^j ≈ 2d·log2 d. If true for all j, σ(d) = Ω(d log d), so the maximum is not linear.
8. The proof is reduced to one explicit Period Lemma (section (e)), verified for j ≤ 7. Two natural stronger forms are REFUTED.
9. Part 2 outcome: PARTIAL.
10. A 10-idea brainstorm is in section (f).

## (b) Statements and proofs

### Part 1. The stopping-time game

**Notation.** T(n) = n/2 for n even, (3n+1)/2 for n odd. σ_∞(n) is the least k with T^k(n) = 1. For n ≥ 1 with 3 ∤ n put E(n) = 2n and, when n ≡ 2 (mod 3), O(n) = (2n−1)/3.

**Elementary facts.**
- T(E(n)) = n, and 3 ∤ E(n).
- O(n) is an odd positive integer with T(O(n)) = n.
- 3 ∤ O(n) iff n mod 9 ∈ {2, 8}.
- If n = r + 3^j·u then O(n) = (2r−1)/3 + 2·3^{j−1}·u. So O(n) mod 3^{j−1} depends only on n mod 3^j, while its top ternary digit depends on u mod 3.

**Game G_j (j ≥ 2).** States are r mod 3^j with 3 ∤ r. Move E: r → 2r. Move O (legal iff r mod 9 ∈ {2, 8}): b = (2r−1)/3 mod 3^{j−1}, the adversary picks t ∈ {0,1,2}, and the new state is b + t·3^{j−1}.

A (j,p,q)-certificate (integers 0 < p < q) is g: states → Z_{≥0} such that every state r satisfies one of:
- (E) g(2r) ≤ g(r) − p;
- (O) r mod 9 ∈ {2, 8} and g(b + t·3^{j−1}) ≤ g(r) + q − p for t = 0, 1, 2.

**Lemma 1 (PROVED).** If a (j,p,q)-certificate exists then λ := ln 2 − (p/q)·ln 3 > 0, and for every γ < 1/λ there are infinitely many n with γ·ln n < σ_∞(n) < ∞.

*Proof.* Start at n_0 = 4. Here 3 ∤ 4, T(4) = 2, T(2) = 1, so σ_∞(4) = 2 and 4 is not on the cycle {1, 2}.

Given n_k with 3 ∤ n_k, let r = n_k mod 3^j. If (E) holds at r, put n_{k+1} = E(n_k). Otherwise (O) holds, r mod 9 ∈ {2, 8}, and we put n_{k+1} = O(n_k); this is an integer not divisible by 3 whose residue mod 3^j is one of the three states b + t·3^{j−1}.

In both cases T(n_{k+1}) = n_k, 3 ∤ n_{k+1}, and g(n_{k+1}) ≤ g(n_k) − p + q·[move = O]. Let m_k be the number of O-moves among the first k. Summing and using g ≥ 0 gives 0 ≤ g(n_k) ≤ g_0 − pk + q·m_k, so m_k ≥ (pk − g_0)/q, where g_0 = g(4 mod 3^j).

- (i) Distinctness. If n_k = n_l with k < l then n_k = T^{l−k}(n_l) = T^{l−k}(n_k), so n_k is periodic and n_0 = T^k(n_k) lies on the same cycle. But 4 is on no cycle (its forward orbit is 4, 2, 1, 2, 1, …).
- (ii) Size. E(n) = 2n and O(n) < 2n/3, so n_k ≤ 4·2^k·3^{−m_k} ≤ C·e^{λk} with C = 4·3^{g_0/q}.
- (iii) λ > 0. Otherwise n_k ≤ C for all k, contradicting (i).
- (iv) Stopping time. T^i(n_k) = n_{k−i} for i ≤ k, and no n_i equals 1 (else n_0 ∈ {1, 2}). So σ_∞(n_k) = k + 2. By (ii), k ≥ (ln n_k − ln C)/λ. By (i), n_k → ∞, so σ_∞(n_k)/ln n_k ≥ (1 − ln C/ln n_k)/λ → 1/λ. ∎

**Corollary 2 (PROVED, from (iii)).** No (j,p,q)-certificate has p/q ≥ ln2/ln3 = 0.6309….

**Referee notes on Lemma 1.**
1. The repair is necessary. Started at n_0 = 1, a certificate may dictate 1 –E→ 2 –O→ 1 –E→ 2 …, a legal infinite play with ones-ratio 1/2 that produces no new integers. Step (i) is exactly where "off the cycle" is used; a start that reaches 1 is needed for finiteness.
2. The adversary quantifier is needed because the top digit of O(n) is not a function of the state.
3. g is only evaluated on residues prime to 3; g ≥ 0 is used only for g(n_k) ≥ 0.
4. Litmus. The lemma is a statement about backward trees and transfers verbatim to (an+c)/2. It says nothing about whether all n reach 1, so there is nothing for 5n+1 or 3n−1 to contradict. The constant 3 enters only through ln 3 and the mod-9 rule; positivity enters only in (iii).

**Proposition 3 (PROVED; also VERIFIED by program).** v_2 := sup{p/q : a (2,p,q)-certificate exists} = 1/4, attained.

*Proof.* States are 1, 2, 4, 5, 7, 8. The doubling cycle is 1→2→4→8→7→5→1. O from 2 leads to {1, 4, 7}; O from 8 leads to {2, 5, 8}.

Certificate for 1/4: g(1)=1, g(2)=0, g(4)=1, g(8)=0, g(7)=3, g(5)=2, with O at 2 and 8 and E elsewhere. Checks:
- g(2)+3 ≥ max(g(1), g(4), g(7)) = 3;
- g(8)+3 ≥ max(g(2), g(5), g(8)) = 2;
- g(1)−1 = g(2), g(4)−1 = g(8), g(7)−1 = g(5), g(5)−1 = g(1).

Upper bound: let the adversary answer O at 2 by 7 and O at 8 by 5. A certificate at ratio p/q yields an infinite play in the finite graph {1→2, 2→4, 2–O→7, 4→8, 8→7, 8–O→5, 7→5, 5→1}. On any cycle of the play, Σ(−p + q·[O]) ≥ 0. The simple cycles are (1,2,4,8,7,5) with 0 O's of 6, (1,2,7,5) with 1 of 4, and (1,2,4,8,5) with 1 of 5. So p/q ≤ 1/4. ∎

Program: `game2 3 1 2 1 4 100` gives OK; `game2 3 1 2 251 1000 6000` gives FAIL with the exact cap.

**Proposition 4 (PROVED as a sketch): relation to Applegate–Lagarias / Amano.** An A–L certificate is a finite ternary prefix code of classes a mod 3^{l+1}, each with a "critical path" in the pruned inverse tree with l ones and ones-ratio ≥ α, valid for every integer in the class (Amano 2021, §2). If every code word has l+1 ≤ j, then every p/q < α has a (j,p,q)-certificate, hence v_j ≥ α.

*Sketch.* In G_j the player always knows n mod 3^j. At a chunk start this determines the code word and so the whole critical path, whose legality depends only on the root class. Every sequence of adversary digits is realised by an actual integer root, so the path can be followed. Chunks have bounded length and ratio ≥ α, so the mean payoff is ≥ α. A finite mean-payoff game with value ≥ α has an energy potential for every rational below α. ∎

So the two are not the same object:
- A–L read l+1 digits, spend them, and re-read: a block window of adaptive depth (38 digits but only 1.9·10^10 classes for Amano's 1/2).
- G_j has a sliding window of exactly j digits refreshed after every move. It is solved exactly as a mean-payoff game but needs 3^j memory.

Consequences: v_j is non-decreasing in j (a certificate lifts from j to j+1), lim v_j ≥ 1/2 (Amano plus Prop. 4), and lim v_j ≤ ln2/ln3.

**Table (3n+1).** "best" is the largest p with an OK run at that q. "fails at" is the first FAIL; it is rigorous only where the cap is the exact energy bound (states·q).

| j | states | best p/q | fails at | cap | likely exact | 1/λ |
|---|---|---|---|---|---|---|
| 2 | 6 | 250/1000 | 251/1000 | exact | 1/4 (proved) | 2.39 |
| 3 | 18 | 333/1000 | 334/1000 | exact | 1/3 | 3.06 |
| 4 | 54 | 375/1000 | 376/1000 | exact | 3/8 | 3.56 |
| 5 | 162 | 400/1000 | 401/1000 | exact | 2/5 | 3.94 |
| 6 | 486 | 400/1000 | 401/1000 | 300q | 2/5 | 3.94 |
| 7 | 1458 | 416/1000 | 417/1000 | 300q | 5/12 | 4.24 |
| 8 | 4374 | 431/1000 | 432/1000 | 300q | — | 4.55 |
| 9 | 13122 | 444/1000 | 445/1000 | 300q | 4/9 | 4.87 |
| 10 | 39366 | 450/1000 | 451/1000 | 300q | 9/20 | 5.03 |
| 11 | 118098 | 45/100 | 46/100 | 150q | — | 5.03 |
| 12 | 354294 | 46/100 | 47/100 | 150q | — | 5.33 |
| 13 | 1062882 | 46/100 | 47/100 | 150q | — | 5.33 |

- Reference points: A–L 14/29 = 0.4828 (6.143), Amano 1/2 (6.952), ceiling 0.6309.
- VERIFIED: v_j ≥ the "best" column for j = 2..13. `verify_cert.py` checked every dumped certificate: all states (0 violations), 20,000 random integers against true predecessors, and a 2000-step Lemma-1 play from n_0 = 4.
- The "fails at" column is heuristic for j ≥ 6.
- j = 14 was not run. The stall was already clear and CPU was scarce (core 7 was heavily shared).

**Verdict: DEAD.** The line stalls near 0.46. Reaching 1/2 would need j around 30 (3^30 states) and would only reproduce Amano.

**Controls.**
- 3n−1: r → −r maps E to E and O (legal iff r mod 9 ∈ {1, 7}, child (2r+1)/3) to O, so the games are isomorphic. VERIFIED equal values 0.250, 0.333, 0.375, 0.400, 0.400, 0.416, 0.431 for j = 2..8.
- 5n+1 (O legal iff 5 | 2r−1 and 25 ∤ 2r−1; five adversary digits): 40/200, 40/200, 40/200, 43/200, 48/200 for j = 2..6 (exact cap for j = 2, 3). Ceiling ln2/ln5 = 0.4307. No anomaly.

### Part 2. The F_2[x] Collatz map

**Setting (ABP).** T(f) = f/x if f(0) = 0, and (x+1)f + 1 if f(0) = 1. t_min(f) is the least k with T^k(f) = 1; σ(d) is the maximum over deg f = d. For F with F(0) = 1, let S_3(F) = (x+1)F with its leading term removed, and t(F) the least k with S_3^k(F) = 1.

ABP prove:
- t_min(f) = 2·t(f^) + deg f for odd f, where f^ is the coefficient reversal;
- S_3^k(F) = ((x+1)^k·F)|_{≤m_k} with m_k = deg S_3^k(F);
- t((x+1)^r·g) ≤ 2^s − r + t(g) when deg((x+1)^r·g) < 2^s;
- t(x^n + g) = r − 1 + t((x+1)^{r−1}·g) for r = n − deg g (the case x+1 is the only exception);
- t ≤ √2·n^1.5.

**Array.** For Φ with Φ(0) = 1 let A_r[c] = [x^c](1+x)^r·Φ. Then A_{r+1}[c] = A_r[c] + A_r[c−1] (rule 60, Pascal mod 2) and A_r[0] = 1.

**Theorem A (PROVED; path characterisation).** Let F ≠ 1, F(0) = 1, n = deg F, m_r = deg S_3^r(F).
1. m_{r+1} = max{c ≤ m_r : A_{r+1}[c] = 1}.
2. If μ_0 ≥ μ_1 ≥ … ≥ μ_R are columns with μ_0 ≤ n and A_r[μ_r] = 1 for all r ≤ R (a non-increasing 1-path), then m_r ≥ μ_r for all r ≤ R.
3. t(F) = 1 + max{R : there is a non-increasing 1-path of length R with μ_R ≥ 1}.

*Proof.*
(1) Put h = S_3^r(F), m = m_r. Then S_3(h) = (1+x)h + x^{m+1} = ((1+x)h)|_{≤m}, and h ≡ (1+x)^r·F mod x^{m+1}. So ((1+x)h)|_{≤m} = ((1+x)^{r+1}·F)|_{≤m}, whose degree is the largest c ≤ m with A_{r+1}[c] = 1 (c = 0 qualifies).
(2) Induction: μ_{r+1} ≤ μ_r ≤ m_r and A_{r+1}[μ_{r+1}] = 1 give m_{r+1} ≥ μ_{r+1} by (1).
(3) (m_r) is itself such a path, with m_r ≥ 1 exactly for r < t(F). Conversely a path with μ_R ≥ 1 forces m_R ≥ 1, so R < t(F). ∎

Corollaries (PROVED):
- Monotonicity: t(Φ|_{≤m}) ≤ t(Φ|_{≤m'}) for m ≤ m'.
- Periodicity: if n < 2^s then A_{r+2^s}[c] = A_r[c] for c < 2^s, hence S_3^{2^s}(F) = F|_{≤m_{2^s}}.

VERIFIED: dynamic programme against t on 300 random F of degree ≤ 14 (inline check, not saved as a script).

**Proposition B (PROVED; sparse bound).** t(F) ≤ Σ over exponents e ≥ 1 in the support of F of 2^{⌈log2 e⌉}. In particular t(F) < 2n(w−1) for F of degree n with w terms.

*Proof.* Induction on the number of terms. Write F = x^N + G with deg G = N − r. If F = x+1 then t = 1 = 2^0. Otherwise t(F) = r − 1 + t((x+1)^{r−1}·G) ≤ r − 1 + 2^s − (r−1) + t(G) = 2^s + t(G), where 2^{s−1} ≤ N−1 < 2^s, so 2^s = 2^{⌈log2 N⌉}. ∎

VERIFIED on 20,000 random F (inline check). So a superlinear example needs unboundedly many terms.

**The family.** Fix j ≥ 1, M = 2^j, a = M+1, Φ = 1/(1+x^a) = Σ_l x^{al}, and F_c = Φ|_{≤ac} = Σ_{l=0}^{c} x^{al}. F_c is palindromic, so t_min(F_c) = 2·t(F_c) + ac.

**Lemma C (PROVED; cell formula).** For 0 ≤ q < M, 0 ≤ ρ < M, 1 ≤ c1 ≤ M, 0 ≤ δ ≤ M:

A_{Mq+ρ}[a·c1 − δ] ≡ #{d ⊆ q : δ ≤ d ≤ c1, (d−δ) ⊆ ρ} + #{d ⊆ q : d ≤ min(c1−1, δ−2), (a+d−δ) ⊆ ρ} (mod 2),

where u ⊆ v means the binary digits of u are among those of v.

*Proof.* (1+x)^{Mq} = (1+x^M)^q = Σ_{d⊆q} x^{Md}, so row Mq+ρ is (1+x)^ρ·Σ_{d⊆q} Σ_{l≥0} x^{Md+al}, and Md + al = a(l+d) − d. By Lucas, the coefficient at X = a·c1 − δ counts pairs (d, l) with (X − Md − al) ⊆ ρ. Here X − Md − al = a(c1−l−d) + (d−δ) must lie in [0, M−1]. That forces either c1−l−d = 0 with d ≥ δ (and l ≥ 0 means d ≤ c1), or c1−l−d = 1 with d ≤ δ−2 (and d ≤ c1−1). ∎

VERIFIED exhaustively for j = 4 (inline check).

**Proposition D (PROVED; clean phase).** For 0 ≤ q ≤ c ≤ M−1 and 0 ≤ ρ < M:
- A_{Mq+ρ}[ac − q] = 1 whenever q + ρ ≤ M;
- for q < c, A_{Mq+ρ}[ac − q − 1] = 1 whenever q + ρ ≥ M.

Consequently t(F_c) ≥ Mc + M − c + 1. For c = M−1 (degree n = M²−1) this is t ≥ n − √(n+1) + 3.

*Proof.* A_r[X] = Σ_{i≥0} C(r, X − ai) mod 2. For X = ac − q we have X − ai = M(c−i) + (c−i−q).
- If c−i > q, the Lucas factor C(q, c−i) vanishes.
- c−i = q contributes C(q,q)·C(ρ,0) = 1.
- For c−i = s+1 ≤ q−1 the term is C(q,s)·C(ρ, M+1−q+s).

By Vandermonde, Σ_{s=0}^{q} C(q,s)·C(ρ, M+1−q+s) = C(q+ρ, M+1), and the terms s = q−1, q vanish because ρ < M. So A = 1 + C(q+ρ, M+1), which is 1 for q+ρ ≤ M.

For X−1 the same computation gives A = C(q+ρ, M) mod 2, which is 1 for M ≤ q+ρ ≤ 2M−1.

Path: in block q (rows Mq … Mq+M−1) stay in column ac−q while ρ ≤ M−q, then in column ac−q−1. At row M(q+1) that column is ac−(q+1) and the first formula applies again. This runs through q = 0, …, c−1 and, in block c, for ρ ≤ M−c in column ac−c = Mc ≥ 1. That is a non-increasing 1-path of length Mc + M − c. Apply Theorem A(3). ∎

VERIFIED for j ≤ 5, all c (inline check). Meaning: for the first ~n rows the staircase of F_c loses only one level per M rows.

**Statement E (CANDIDATE).** t(F_{2^i}) = 2^{j+2}·((i−1)·2^{i−1} + 1) for 1 ≤ i ≤ j.

- VERIFIED for all 1 ≤ i ≤ j ≤ 7 and for i = j ≤ 9 (degree 262,656; 4,196,352 steps). The j = 10 run was killed for CPU.
- For i = j: f_j := F_M has degree d = 4^j + 2^j, t(f_j) = (j−1)·2^{2j+1} + 2^{j+2}, and t_min(f_j) = (4j−3)·4^j + 9·2^j. This was checked directly with the original map T for j ≤ 5.
- If E holds for all j: σ(d) ≥ (2·log2 d − 3 − o(1))·d along d = 4^j + 2^j, so σ(d) is not O(d).
- Novelty: ABP 2024 say they have no proof of superlinearity. arXiv API queries on 2026-11-17 returned only 2401.03210, 2401.12781, 2312.00390. That is not a full literature search.

**Statement F (CANDIDATE; VERIFIED j ≤ 7): Period Lemma.** Let C = {2^e : 0 ≤ e ≤ j} ∪ {2^e − 2^i : 0 ≤ i < e ≤ j}. For c ∈ C let P = 2^{bitlength(ac)}. Then S_3^r(F_c) ≠ 1 for r < P, and S_3^P(F_c) equals:
- F_{c−lowbit(c)} if c is not a power of two;
- F_{c−2} if c = 2^e ≥ 2;
- 1 if c = 1.

F implies E: from c = 2^e the chain 2^e → 2^e−2 → 2^e−4 → … → 2^{e−1} costs 2^{j+e+1} + (e−2)·2^{j+e} = e·2^{j+e} rows for e ≥ 2, and Σ_{e=2}^{i} e·2^{j+e} + 2^{j+2} = 2^{j+2}·((i−1)·2^{i−1} + 1). For the lower bound in E only "level ≥" is needed, i.e. one non-increasing 1-path per c ∈ C.

**Brute force (VERIFIED).** τ(n) := max t(F) over deg F = n, so σ(d) = 2τ(d) + d on odd f.

| n | 8 | 12 | 16 | 20 | 24 | 28 |
|---|---|---|---|---|---|---|
| τ(n) | 13 | 23 | 35 | 51 | 64 | 76 |
| τ/n | 1.63 | 1.92 | 2.19 | 2.55 | 2.67 | 2.71 |

The mean of t over degree n is n − 1.18 at n = 24. The beam-search bests (`f2beam.py`) at n = 15, 20, 24, 29, 34, 39 are built from 1 + x^5 + x^10 + …; the n = 24 one matches the exhaustive maximum. This is how the family was found.

## (c) Scripts

All in `outside/scripts/`; PY = `/home/matrix/home/projects/collatz/venv/bin/python`.

- `gcc -O2 -o game2 game2.c`, then `./game2 a c j p q cap [dump]`: energy-game solver for (an+c)/2.
  - `./game2 3 1 2 1 4 100` → `… p/q=1/4 OK sweeps=3 maxcredit=3`
  - `./game2 3 1 2 251 1000 6000` → `FAIL`
  - `game.c` is the stale 3n+1-only draft, superseded; its stale binary was deleted.
- `PY tabulate2.py a c jmin jmax q capmult [dumpdir]`: binary search. `PY tabulate2.py 3 1 2 10 1000 300 ../data/certs` reproduces rows j = 2..10. Logs are in `data/tab_*.log`.
- `PY verify_cert.py a c j p q certfile [n0] [steps]` → `violations=0`, `moves agree …`, `Lemma-1 play … T^k(n_k)=n0 OK`. All files in `data/certs/` pass.
- `gcc -O2 -o f2max f2max.c; ./f2max 1 24`: exhaustive τ(n), argmax, mean (`data/f2max_*.log`, n ≤ 28).
- `PY f2family.py 7 9` → `all (j,i) with 1<=i<=j<=7: OK`, `j=8 … OK`, `j=9 n=262656 t=4196352 … OK`.
- `PY f2period.py 7` → `violations=0` for each j (the saved file was re-run to j = 5; the j ≤ 7 claim comes from an inline run of the same test).
- `PY f2crash.py 5` → shows the false block lemma: 1, 6, 29, 134 violations for j = 2..5.
- `f2lib.py` (S_3, t, T, reversal); `f2beam.py`, `f2sparse.py`, `f2anneal.py` are exploration only.
- Literature: `lit/abp/` (ABP PDF and TeX), `lit/amano/amano2021.{pdf,txt}`.

## (d) Dead ends

1. **Game beyond j ≈ 13.** Memory is 4·3^j bytes and divergence detection is slow near the threshold. Values creep by under 0.01 per digit. Prop. 4 shows the limit is at least 1/2, but only an adaptive (A–L style) window reaches enough digits, and that is Amano's computation.
2. **Game as a Collatz statement.** It is sign-blind (3n−1 isomorphic) and multiplier-generic. It can only produce "infinitely many n with long finite stopping time".
3. **F_2[x], clean paths only.** The paths of Prop. D exist at every dyadic scale: window C with 2^{e−1} ≤ C < 2^e is rideable in block q iff q mod 2^e < C. Chaining only such paths gives at most ~2M blocks, so t = O(n). The log factor comes entirely from the "crash" blocks (q mod 2^e ≥ C), where the true staircase loses about a levels per block.
4. **REFUTED: block lemma.** "From row Mq, level ac, the staircase is at level ≥ a(c−1) at row M(q+1), for all q, c" is false: 134 of 992 pairs fail at j = 5, with shortfall up to 2a.
5. **REFUTED: Period Lemma for all c.** It fails outside C (j = 4: c = 5, 9, 10, 11, 13).
6. **Random and structured search.**
   - Annealing finds nothing (t/n ≈ 1.6–2.4 for n ≤ 256).
   - The squaring recursion H → x^N + H² gives t/n → 2.
   - Trinomials reached at most 4n/3 in the sampled degrees.
   - Four terms reach 2n (x^n + x^{2a} + x^a + 1, a = n/4 + 1).
7. **Porting to the integers.** Theorem A rests on truncation monotonicity (columns ≤ m evolve autonomously). For integers this fails at once: σ_∞(27) = 70, σ_∞(27+32) = 22, σ_∞(27+64) = 59. Carries are the whole obstruction. F_2[x] is "Collatz without carries", and its 5n+1-type analogues are also eventually periodic (Behajaina–Paran), so the method fails the 5n+1 litmus by construction.

## (e) Best lead (precise lemma)

**Period Lemma, lower-bound form.** Let M = 2^j, a = M+1, A_r[c] = [x^c](1+x)^r/(1+x^a) = Σ_{i≥0} C(r, c−ai) mod 2. For every c = 2^e − 2^i with 1 ≤ i ≤ e−2 and e ≤ j (so c' := c − 2^i ≥ 2^{e−1}), there are columns μ_0 = ac ≥ μ_1 ≥ … ≥ μ_P = ac', with P = 2^{j+e}, and A_r[μ_r] = 1 for all r.

With Theorem A, monotonicity and periodicity, the case e = j alone gives t(F_{2^j}) ≥ (j−2)·4^j, hence σ(d) ≥ c·d·log d. Prop. D already supplies the first c·M rows (μ_{Mq+ρ} ∈ {ac−q, ac−q−1}).

What is missing is the path through the last 2^i blocks, q = c, …, 2^e − 1 (mod 2^e), where it must drop from Mc to ac' (about a per block). Observed shape at j = 4, c = 12, block q = 13, window c1 = 11: the depth δ below 11a is 0, 1, 1, 9, 9, 9, 9, 9, 10, 10, 10, 14, 14, 14, 14 for ρ = 0..14. These are constant columns with jumps. The first long plateau is δ = max{d ⊆ q, d ≤ c1}, which Lemma C shows is a 1-cell for ρ ≤ M − δ. A proof should come from Lemma C by induction on e.

Second lead: an upper bound O(d log d). Prop. B's term-by-term accounting (gain ≤ 2^s per term) and the periodicity corollary are the natural tools; nothing was proved.

## (f) Brainstorm: ten attacks different in kind from the repo's dead ends

| # | Idea | Cheapest kill test | Barrier class | Verdict |
|---|---|---|---|---|
| 1 | F_2[x] neighbour: growth of the maximal stopping time | Brute-force τ(n), look for a family | Neighbour problem, carry-free; fails 5n+1 litmus by design | EXECUTED: PARTIAL |
| 2 | Sliding-window 3-adic game for long stopping times | Value at j ≤ 13 vs 1/2 | Tree statement only; sign-blind | EXECUTED: DEAD |
| 3 | 3-smooth representations: n reaches 1 with k odd steps iff 2^A = 3^k·n + Σ 3^{k−1−i}·2^{a_i}; count solutions mod 3^k | Does the counting lemma differ for 5? (2 is a primitive root mod 5^k too) | Identical for 5n+1 at the surjectivity level, so fails litmus; the counting form is Krasikov–Lagarias | Killed by reasoning |
| 4 | Explicit infinite families reaching 1 (fixed exponent patterns in the inverse tree) with counting | Count members ≤ x at depth D | Depth-D families have ~(log x)^D/D! members; x^δ needs unbounded depth, which is the KL exponent line | Only cosmetic theorems |
| 5 | Arithmetic progressions in σ_∞(2^n + 1) (MathOverflow conjecture; ABP prove the F_2[x] analogue) | σ_∞(2^{2m}+1) = 2m + σ_∞(3^m+1) is elementary; test whether orbits of 3^m+1 and 3^{m+1}+2 merge at bounded height | Needs binary digits of 3^m (×2×3 strength) | As hard as known open problems |
| 6 | Ladder Z/2^k[x] between F_2[x] and Z | Read Behajaina–Paran 2312.00390 | Positive characteristic already gives eventual periodicity; Z does not embed (constants have trivial orbits) | Dead |
| 7 | Base-6 / carry-save cellular-automaton form with a path characterisation like Theorem A | Test truncation monotonicity on integers | Fails immediately (27 vs 59, 91) | Dead, with the precise reason |
| 8 | Baker-type bounds for "almost cycles" (returns within n^{1−δ}) | Must a divergent orbit almost-return? | No; and Baker applies equally to 5n+1, which has cycles | Low value |
| 9 | Carry-entropy of the 3n+1 transducer vs 5n+1 | Compare carry statistics on both maps | Multiplier-blind statistics; same kind as the statistical Lemma E dead end | Not pursued |
| 10 | Upper bound O(d log d) in F_2[x] via multi-scale periodicity | Find any F with τ/n growing faster than log n | Neighbour problem | Open; second lead in (e) |

Only ideas 1 and 2 were executed; 3–9 were killed by reasoning, not by experiment (except the three integers in idea 7).

## Credences

- Lemma 1, Cor. 2, Prop. 3, Theorem A, Prop. B, Lemma C, Prop. D correct as stated: 95–97% each.
- Prop. 4: 85% (the proof is a sketch).
- Statement E for all j: 90%. Statement F for all j: 85%.
- σ(d) superlinear in F_2[x]: 93%. Unpublished as of today: 60%.
- Game reaching ratio > 1/2 with j ≤ 20: under 2%.