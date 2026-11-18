<!-- Saved by the coordinator from the w5-fourier agent's final message (the agent's own write was refused). -->
# FULL REPORT — w5-fourier: pointwise power Fourier decay (PFD) for E

Date: 2026-11-18. Labels: PROVED (proof below), VERIFIED (finite, by the named script), CONJECTURED, CANDIDATE (hand heuristic), REFUTED. Nothing here was refereed by anyone but me.

Notation as in `w3-fp0/REPORT.md`.
- f_a(z) = (8z−1)/9, f_b(z) = 16z/27. A word v has P_v = 2A+3B, Q_v = 3A+4B, f_v = f_{v1}∘…∘f_{vn}.
- f_v(z) = (2^(Q_v)·z − D_v)/3^(P_v), with D_∅ = 0, D_{va} = 9D_v + 2^(Q_v), D_{vb} = 27D_v.
- E_k = E mod 2^k, N_k = #E_k, s = 0.2877608, T_k(ξ) = Σ_{c∈E_k} e(ξc/2^k).
- G(P,k) := T_k(h·3^(−P) mod 2^k). ‖x‖ is the distance to the nearest integer.

## (a) Summary

1. PFD ⇒ FP-0 is re-derived (Proposition 1, PROVED). Only integers 1 ≤ |h| ≤ N_K^δ at full scale K are needed, with |T_K(h)| ≤ C·N_K^(1−δ). Then N(Q,Q) ≤ C′·2^((s−δ′)Q), δ′ = (1−s)sδ/(1−sδ).
2. Proposition 2 (PROVED): this restricted (PFD-int) is equivalent to power equidistribution of the top ≍K bits of E_K in every dyadic window. FP-0 is the one-window, one-sided case.
3. Proposition 3 (PROVED, VERIFIED exactly): T_K(h) is, up to a real phase of size |h|/2^K, the Fourier transform of a 3-adically expanding self-similar point set at the 3-adic frequency ζ = −h·2^(−K). The family ζ ∈ Z_3 has bad parameters (ζ = 1, 2, 1/11) and generic square-root decay. (PFD) asks that the specific ζ = −h·2^(−K) behave generically.
4. The brief's "finite-state" hope is REFUTED, as the brief guessed. The node quantity is −(11h·2^(−k) mod 3^p)/3^p with p = P+5 growing along the path. Its size is governed by the top ternary digits, which are periodic in k only with period 2·3^(p−1).
5. Theorem 5 (PROVED): |T_K(ξ)| ≤ U_K(ξ) ≤ N_K·β^(g_K(ξ)), β = 1 − 0.4(1 − cos πε). U is the ab/ba pairing majorant (O(K²), positive terms); g is the minimum over block paths of the number of ε-good nodes.
6. VERIFIED (floats, K ≤ 3200): U_K(h)/N_K = N_K^(−0.145) for h = 1, 3, 5, 11, 2, 1001, 2^64+13. Longer blocks give 0.217 (r = 3) up to 0.341 (r = 8, K = 400). g_K(h)/K = 0.046–0.050 at ε = 0.1.
7. Lemma R (PROVED, VERIFIED): for ε ≤ 10⁻³ a run of J+1 consecutive bad nodes starting at (P₀,k₀) forces ‖11h·3^(−p)/2^(k₀)‖ ≤ ε·3^(−4J). At K = 1600, h = 1 the longest run is 2.
8. So (PFD-int) follows from (D): "no admissible path stays in the bad set". This is a statement on runs of equal binary digits of h·3^(−p) at heights k ≍ p. It is not an equivalence: (PFD) needs it only for all but N^(−δ) of the path mass.
9. Additive energy (VERIFIED k ≤ 44): En(E_k) ≈ N_k^2.19 at k = 44. L⁴ beats L² for large-value counts but still leaves 2^k·N^(−1.8) possible large frequencies.
10. Litmus: every statement is invariant under E ↦ −E and is a counting statement. Nothing implies E ∩ Z_{>0} = ∅. 5n+1 was not re-run for the new scripts.

## (b) Statements

### Proposition 1 (PFD-int ⇒ FP-0) — PROVED

**(PFD-int)_δ.** There are δ ∈ (0,1) and C such that |T_K(h)| ≤ C·N_K^(1−δ) for all K ≥ 1 and all integers 1 ≤ |h| ≤ N_K^δ.

Claim: (PFD-int)_δ implies N(Q,Q) ≤ C′·2^((s−δ′)Q) with δ′ = (1−s)·sδ/(1−sδ).

Proof.
- N(Q,m) = #{c ∈ E_K : c/2^K ∈ [0, 2^(−m))} with K = Q+m. It is non-increasing in m because E_(Q+m+1) reduces into E_(Q+m). So N(Q,Q) ≤ N(Q,m) for m ≤ Q.
- Selberg's majorant (Montgomery, *Ten Lectures*, Ch. 1): for an arc I ⊂ R/Z and integer H ≥ 1 there is S⁺(x) = Σ_{|h|≤H} ŝ(h)e(hx) ≥ 1_I(x) with ŝ(0) = |I| + 1/(H+1) and |ŝ(h)| ≤ 1/(H+1) + min(|I|, 1/(π|h|)).
- Hence N(Q,m) ≤ Σ_h ŝ(h)·T_K(h) ≤ N_K(2^(−m) + 1/(H+1)) + Σ_{0<|h|≤H} (1/(H+1) + 2^(−m))·|T_K(h)|.
- Take H = 2^m − 1 with 2^m ≤ N_K^δ: N(Q,m) ≤ 2^(1−m)·N_K + 4C·N_K^(1−δ).
- 2^(sK) ≤ N_K ≤ 1.64·2^(sK). With m = ⌊θQ⌋, θ = sδ/(1−sδ), one has m/K ≤ sδ, so 2^m ≤ N_K^δ, and both terms are ≤ C′·2^((s−(1−s)θ)Q). ∎

Remarks.
- If the hypothesis carries a factor 2^(v₂(h)/2), the same proof works: Σ_{h≤H} 2^(v₂(h)/2) ≤ 3.42·H.
- If (PFD-int) is known only for |h| ≤ 2^(ηK) with η < sδ, take θ = η/(1−η): δ′ = (1−s)η/(1−η).
- Correction to the referee's wording: Lemma 4 at k = K with all h up to 2^(K−1) would need all ξ ≢ 0 and the weight 2^(v₂/2). The truncated majorant removes both needs.
- Correction to w4-wall summary item 7: frequencies h·3^(−P), P ≥ k, belong to the tail-block reduction. The full-scale reduction uses plain integers h. Integers h = 3^n ≤ N_K^δ have n/K ≤ 0.63·sδ ≤ 0.09, where w4's profile gives δ(n/K) ≥ 0.43.
- With the numerically observed δ = ½ this route gives δ′ = 0.12; the truth is presumably N(Q,Q) = O(1).

### Proposition 2 (what PFD-int says) — PROVED

For J = [j·2^(−m), (j+1)·2^(−m)) put Δ_K(J) = #{c ∈ E_K : c/2^K ∈ J} − 2^(−m)·N_K.
- (i) (PFD-int)_δ ⇒ |Δ_K(J)| ≤ C″·log N_K·N_K^(1−δ) for every m and J.
- (ii) If |Δ_K(J)| ≤ C·N_K^(1−δ₂) for all dyadic J with 2^m ≤ N_K^(δ₂/2), then |T_K(h)| ≤ (C+2π)·N_K^(1−δ₂/4) for 1 ≤ |h| ≤ N_K^(δ₂/4).

Proof.
- (i) Selberg majorant and minorant with H = ⌊N_K^δ⌋, as in Proposition 1; Σ_{h≤H} min(2^(−m), 1/h) ≤ 1 + log H.
- (ii) Choose m with N_K^(δ₂/2)/2 < 2^m ≤ N_K^(δ₂/2). Replacing e(hc/2^K) by e(hj/2^m) on J costs ≤ 2π|h|2^(−m) per point. Σ_J e(hj/2^m)·#(J) = Σ_J e(hj/2^m)·Δ_K(J) because 2^m ∤ h. So |T_K(h)| ≤ 2^m·C·N_K^(1−δ₂) + 2π|h|2^(−m)·N_K. ∎

Hierarchy: (PFD-int) ⇔ power equidistribution of the top cK bits ⇒ a Frostman bound #(E_K ∩ 2^K·J) ≤ N_K·2^(−γm) for all windows ⇒ FP-0 (window at 0 only). The second moment of T_K over |h| ≤ 2^m equals the window collision count Σ_J #(J)², so L² over h is circular (w3-fp0 dead end 4).

### Proposition 3 (mirror: T_K is a 3-adic Fourier transform) — PROVED; VERIFIED exactly (`g1_mirror.py`, K = 22, 31, 37)

For x ∈ Z[1/6] let {x}_3 ∈ [0,1) be its 3-adic fractional part. E_K is parametrised by pairs (v, z): v a word at which the recursion E_j = f_a(E_(j−3)) ⊔ f_b(E_(j−4)) stops (κ = K − Q_v ∈ {0,1,2,3}), and z = 0 (κ = 0) or z ∈ {0, −1} (κ = 1,2,3); c = f_v(z) mod 2^K. With r = f_v(z) ∈ Z[1/3], a real number in (−2, 0]:

  e(h·c/2^K) = e(h·r/2^K)·e(−{h·r/2^K}_3), so T_K(h) = Σ_{(v,z)} e(h·r/2^K)·e(−{h·r/2^K}_3).

Proof. x = h·r/2^K ∈ Z[1/6] satisfies x − {x}_2 − {x}_3 ∈ Z. Since r ≡ c mod 2^K in Z_2, {x}_2 ≡ hc/2^K mod 1. ∎

Consequences.
- The real factor is 1 + O(|h|/2^K), irrelevant for |h| ≤ N_K^δ. The 3-adic factor is e(−(h·2^(−K)·n mod 3^P)/3^P) where r = n/3^P. So E_K/2^K ⊂ R/Z is the set of real IFS points (denominators 3^(P_v), P_v ≤ 0.75K) dilated by the unit 2^(−K) of Z/3^P.
- Family T^ζ := Σ e(−{ζ·r}_3), ζ ∈ Z_3. VERIFIED (`g5_distinct.py`, K = 22, 31, 37, 44): the points r are distinct mod 1 except exactly one coincident pair. So the mean of |T^ζ|² over ζ mod 3^Pmax is N_K + 2.
- VERIFIED at K = 22, 31, 37:

| ζ | \|T^ζ\|/N |
|---|---|
| 1 | 0.56, 0.62, 0.64 |
| 2 | 0.19, 0.21, 0.24 |
| 1/11 | 0.54, 0.44, 0.46 |
| 1/5 | 0.02, 0.0005, 0.005 |

  Random ζ give |T^ζ|/√N ≈ 1.0 (mean of 20) and ≤ 3.4 (max). ζ = 1 is the real self-similar measure of (8y+1)/9, 16y/27 at frequency 1; ζ = 1/11 is w4-wall's mod-11 resonance.
- Adversarial frequencies explained: for ξ = 3^n the 3-adic phase is trivial on every letter with P ≤ n, and the real phase 3^n·r/2^K is negligible while 3^n ≪ 2^K.
- Node form of the mirror (VERIFIED exactly, `g4_runs.py`): for all k, p, h, (11h·3^(−p) mod 2^k)/2^k + (11h·2^(−k) mod 3^p)/3^p − 11h/(2^k·3^p) ∈ Z. So the top bits of the running frequency are minus the top ternary digits of 11h·2^(−k) mod 3^p. "Good" is a function of (k mod 2·3^(d−1), h mod 3^d) only when p ≤ d.

### Proposition 4 (block identity and ab/ba pairing) — PROVED; VERIFIED (`g1_mirror.py`)

For k ≥ 8 and every ξ mod 2^k (inverses mod 2^k, e(y) meaning e(y/2^k)):

  T_k(ξ) = e(−ξ/9 − 8ξ/81)·T_(k−6)(ξ/81) + [e(−ξ/9) + e(−16ξ/243)]·T_(k−7)(ξ/243) + T_(k−8)(ξ/729).

f_ab(0) = −1/9 and f_ba(0) = −16/243 differ by −11/243, so

  |e(−ξ/9) + e(−16ξ/243)| = 2·|cos(π·(11·ξ·3^(−5) mod 2^k)/2^k)|.

For an r-block and k ≥ 4r: G(P,k) = Σ_{A=0}^{r} S_A(P,k)·G(P+P_A, k−Q_A), with S_A = Σ_{u: #a = A} e(−h·D_u·3^(−(P+P_A))/2^k). Two words u, u′ with equal letter counts differ in phase by e((D_{u′} − D_u)·h·3^(−(P+P_A))/2^k).

Proof. Apply Proposition E twice (resp. r times); f_u(0) = −D_u/3^(P_u). ∎

### Theorem 5 (pairing majorant) — PROVED

Fix ε ∈ (0, ½) and an integer h ≠ 0. A node (P,k), k ≥ 8, is **ε-good** if ‖11h·3^(−(P+5))/2^k‖ ≥ ε. Put w(P,k) = 2|cos(π·11h·3^(−(P+5))/2^k)|, which is ≤ 2cos πε at good nodes. Define

- U(P,k) = N_k for k < 8; U(P,k) = U(P+4,k−6) + w(P,k)·U(P+5,k−7) + U(P+6,k−8) for k ≥ 8;
- g(P,k) = 0 for k < 8; g(P,k) = 1[(P,k) good] + min(g(P+4,k−6), g(P+5,k−7), g(P+6,k−8)) for k ≥ 8.

Then |G(P,k)| ≤ U(P,k) ≤ N_k·β^(g(P,k)) with β = 1 − 0.4·(1 − cos πε). In particular |T_K(h)| ≤ N_K·β^(g_K(h)), g_K(h) := g(0,K). The same holds for any ξ mod 2^K in place of h.

Proof.
- |G| ≤ U: induction on k with Proposition 4 and |T_k| ≤ N_k.
- N_k = N_(k−6) + 2N_(k−7) + N_(k−8) for k ≥ 8. N_j is non-decreasing for j ≥ 1, so for k ≥ 10, N_(k−6) ≤ 2N_(k−7) and N_(k−8) ≤ N_(k−7), giving 2N_(k−7) ≥ 0.4·N_k. For k = 8, 9 the ratio is 4/7, 4/8.
- With g* the minimum over the three children, U(P,k) ≤ β^(g*)·[N_(k−6) + w·N_(k−7) + N_(k−8)]. At a good node the bracket is ≤ N_k − 2(1 − cos πε)N_(k−7) ≤ β·N_k; otherwise it is ≤ N_k. ∎

**Corollary 6 — implication PROVED, hypothesis CONJECTURED.**
(D)_{η,ε,c}: for all K ≥ K₀ and all integers 1 ≤ |h| ≤ 2^(ηK), every block path from (0,K) (steps (ΔP, Δk) ∈ {(4,−6), (5,−7), (6,−8)}, continued while k ≥ 8) meets at least cK ε-good nodes.
Then (PFD-int) holds with δ = min(η/s, c·log₂(1/β)/s), hence FP-0 by Proposition 1.

U is a rigorous upper bound for |T_K(h)| for each (K,h), computable in O(K²) with positive terms only, so double precision suffices.

### Lemma R (bad runs are exact) — PROVED; VERIFIED (`g4_runs.py`: 0 violations on 343,688 bad nodes)

Let ε ≤ 10⁻³ and let m(P,k) be the symmetric residue of 11h·3^(−(P+5)) mod 2^k, so bad ⇔ |m| < ε2^k. If (P,k) and its child (P+ΔP, k−ΔQ) are both bad then m(P,k) = 3^(ΔP)·m(P+ΔP, k−ΔQ) as integers. Hence a path (P₀,k₀), …, (P_J,k_J) of J+1 consecutive bad nodes forces

  ‖11h·3^(−(P_J+5))/2^(k₀)‖ ≤ ε·3^(−(P_J−P₀)) ≤ ε·3^(−4J),

i.e. the 2-adic integer 11h·3^(−(P_J+5)) has at least ⌊6.34J⌋ + 9 equal bits immediately below position k₀.

Proof. m ≡ 3^(ΔP)·m′ mod 2^(k−ΔQ), |m| < ε2^k, |3^(ΔP)m′| < ε·3^(ΔP)·2^(k−ΔQ), and ε(2^(ΔQ) + 3^(ΔP)) ≤ 985ε < 1. So the difference is a multiple of 2^(k−ΔQ) of absolute value below 2^(k−ΔQ). Iterate; then 11h·3^(−(P_J+5)) ≡ m(P_J,k_J) mod 2^(k₀). ∎

Consequences.
- A bad run from the root (P₀ = 0, |11h|·3^5 < 2^(K−1)) forces 3^(P_J+5) | 11h exactly. For 3 ∤ h the root is good; for h = 3^n·u the head is bad for about n/4.4 nodes. This is w4-wall's adversarial mechanism, now a lemma.
- For fixed h with 3 ∤ h, (D) follows from (R*)_L: there is no (p,k), 8 ≤ k ≤ K, 9 ≤ p ≤ 0.75(K−k)+11, with ‖11h·3^(−p)/2^k‖ < 10⁻³·3^(−4L). Then every L+1 consecutive nodes contain a good one, so c ≥ 1/(9(L+1)).
- (R*) is Erdős-type: runs of equal bits in the 2-adic expansion of 3^(−p) at heights k ≥ 4p/3; by the mirror, runs of 0s or 2s at the top of 11h·2^(−k) mod 3^p.
- VERIFIED: K = 1600, h = 1, ε = 10⁻³: 1,899 bad nodes of 953,610 (fraction 0.00199 = 2ε), longest run 2. K = 800, h = 2^64+13: longest run 1. K = 1600, h = 3^300: longest run 74.

### Numerics — VERIFIED (floats; `g2_major.py`, `out_major.txt`, `out_adv.txt`)

δ_U := −log(U_K/N_K)/log N_K (2-blocks); g = g_K(h) at ε = 0.1 (β = 0.9782).

| K | h = 1 | 3 | 5 | 11 | 2 | 1001 | 2^64+13 | 3^40 |
|---|---|---|---|---|---|---|---|---|
| 800: δ_U | 0.149 | 0.144 | 0.140 | 0.139 | 0.145 | 0.146 | 0.146 | 0.131 |
| 1600: δ_U | 0.142 | 0.145 | 0.144 | 0.148 | 0.146 | 0.146 | 0.142 | 0.138 |
| 3200: δ_U | 0.145 | 0.145 | 0.144 | 0.144 | 0.144 | 0.146 | 0.144 | 0.142 |
| 3200: g/K | 0.0475 | 0.0459 | 0.0459 | 0.0466 | 0.0456 | 0.0456 | 0.0469 | 0.0431 |

- The annealed prediction for uniform node phases is the root of y⁶ + (4/π)y⁷ + y⁸ = 1: y = 0.8431, δ = 0.144.
- The fraction of good nodes is 0.800 = 1 − 2ε to three digits for h coprime to 3, so the field (P,k) ↦ 11h·3^(−(P+5))/2^k is numerically equidistributed over the cone.
- g at K = 800, h = 1 by ε: 0.02 → 82; 0.05 → 65; 0.1 → 40; 0.2 → 7; 0.3 → 1. The δ proved from g (0.005 at ε = 0.1) is far below δ_U.
- Longer blocks, h = 1: r = 3: 0.217, r = 4: 0.266, r = 5: 0.291 (all K = 800); r = 6: 0.307 (K = 200); r = 8: 0.341 (K = 400). The true exponent is about 0.5.

Adversarial ξ = 3^n at K = 800:

| n/K | 0.05 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.63 | 0.66 | 0.7 |
|---|---|---|---|---|---|---|---|---|---|---|
| δ_U | 0.131 | 0.120 | 0.102 | 0.086 | 0.067 | 0.044 | 0.023 | 0.016 | 0.062 | 0.131 |

This has the same shape as w4-wall's true profile, scaled by about 0.29; g = 1 at n/K = 0.63.

Additive energy (`g3_energy.py`, exact): En = #{a+b ≡ c+d mod 2^k}.

| k | 16 | 24 | 32 | 40 | 44 |
|---|---|---|---|---|---|
| N_k | 32 | 156 | 778 | 3833 | 8505 |
| log En/log N | 2.279 | 2.237 | 2.219 | 2.199 | 2.192 |
| En/(2N²−N) | 1.33 | 1.66 | 2.15 | 2.59 | 2.83 |

En/(2N²) grows like N^0.12 (k = 28…44), so the energy exponent is about 2.12–2.19: low but not minimal. #{ξ : |T_k(ξ)| ≥ N^(1−δ)} ≤ 2^k·En/N^(4−4δ) ≈ 2^k·N^(−1.8+4δ), against 2^k·N^(−1+2δ) from Parseval. Neither localises the large frequencies.

### Literature (task 1)

[R] = abstract fetched this session through the arXiv API and quoted verbatim; [M] = from memory.

- **Solomyak, arXiv:1906.12164 [R]:** "after removing a zero Hausdorff dimension exceptional set of parameters, all self-similar measures on the line have a power decay of the Fourier transform at infinity. In the homogeneous case, when all contraction ratios are equal, this is essentially due to Erdős and Kahane." Parameters are contraction vectors; there is no criterion for a given one.
- **Mosquera–Shmerkin, arXiv:1710.06812 [R]:** "R. Kaufman and M. Tsujii proved that the Fourier transform of self-similar measures has a power decay outside of a sparse set of frequencies." This is the closest analogue: our IFS is fixed and the question is whether ζ = −h·2^(−K) lies in the sparse set.
- **Li–Sahlsten, arXiv:1902.00426 [R]:** Rajchman "if log r_i / log r_j is irrational for some i ≠ j"; the rate "is also shown to be logarithmic if log r_i / log r_j is diophantine". Method: "quantitative renewal theorems for stopping times of random walks on R". Our analogue of the renewal step is the spread of P at fixed Q (w3-fp0 Lemma 2).
- **Varjú–Yu, arXiv:2004.09358 [R]:** "quantitative decay rates of Fourier transform of some self-similar measures"; "random walks on lattices and Diophantine approximation in number fields". Logarithmic-type rates [M].
- **Brémont, arXiv:1910.03463 [R]; Rapaport, arXiv:2104.03955 [R]:** characterisations of the Rajchman property, no rate.
- **Algom–Rodriguez Hertz–Wang, arXiv:2012.06529 [R]:** "When Φ is self similar and satisfies a certain Diophantine condition, we establish a logarithmic rate of decay."
- **Baker–Khalil–Sahlsten, arXiv:2407.16699 [R]:** "polylogarithmic Fourier decay for Diophantine self-similar measures, and polynomial decay for Patterson-Sullivan measures of convex cocompact hyperbolic manifolds, Gibbs measures associated to non-integrable C² conformal systems".
- **Bourgain–Dyatlov, arXiv:1704.02909 [R]:** "This bound uses the fact that transformations in the group Γ are nonlinear, together with estimates on exponential sums due to Bourgain which follow from the discretized sum-product theorem in R."
- **Sahlsten–Stevens, arXiv:2009.01703 [R]:** "When T is totally non-linear, then μ̂(ξ) → 0 at a polynomial rate". **Baker–Sahlsten, arXiv:2306.01389 [R]:** polynomial rate "for any C² iterated function system satisfying UNI", overlaps allowed.
- **Baker–Banaji, arXiv:2602.05593 [R]:** Rajchman self-similar measures with arbitrarily slow decay exist.
- **Han Yu, arXiv:2101.05910 [R]:** "a fine analysis of the Fourier coefficients of self-similar measures together with an Erdős-Kahane type argument", for missing-digit measures.
- **p-adic analogues:** one search found no paper on Fourier decay of self-similar measures on Q_p. The search was not exhaustive.
- Leclerc's work was not looked up.

Which mechanism applies.
- Every power-decay theorem for a specific measure uses nonlinearity (UNI, total non-linearity, sum-product). There the derivative cocycle at a fixed scale takes exponentially many well-spread values.
- Here the maps are affine. At 2-adic depth q the multiplier 3^(−P) takes only about √q (typical) to q/12 (all) values, a progression of exponents. That is the structure of a self-similar measure with two incommensurable ratios.
- For such a given measure the best theorems are (poly)logarithmic (Li–Sahlsten, Varjú–Yu, ARW, BKS). That is exactly the strength of Theorems A, A′ (a power of K = log N).
- Power decay for self-similar measures is known only generically (Erdős–Kahane, Solomyak) or off a sparse frequency set (Kaufman, Tsujii).
- Verdict: (PFD) for E is the 2-adic twin of the open problem "power decay for an explicit non-homogeneous self-similar measure". Bourgain–Dyatlov does not apply: the multipliers 9^(−1), 27^(−1) commute and there is no nonlinearity.

## (c) Scripts

Directory `/home/matrix/home/projects/collatz/repo/notes/round6-nov2026/w5-fourier/`, PY = `/home/matrix/home/projects/collatz/venv/bin/python`.

- `$PY g1_mirror.py K` (K ≤ 37, seconds): word parametrisation of E_K; mirror identity in exact rationals for 9 values of h (expected `failures = 0`); ab/ba modulus formula and 2-block recursion against direct sums (expected 0 failures); ζ-family table; `|T^zeta|/sqrt(N)` equal to the true `|T_K(1)|/sqrt(N)`.
- `$PY g2_major.py K num [r=2] [eps=0.1]`: U/N, δ_U, g, good-node fraction. `num` is a Python expression such as `"3**504"`. For r > 2 only δ_U is meaningful. `run_major.sh` and `run_adv.sh` produce `out_major.txt` and `out_adv.txt`.
- `$PY g3_energy.py 44`: additive energy table (about 1 GB RAM at k = 44).
- `$PY g4_runs.py K num [eps=1/1000]`: node mirror identity (exact), bad-node count, longest bad run, exactness violations (expected 0).
- `$PY g5_distinct.py K`: distinctness of the points r mod 1 (expected: points − 1).

## (d) Brainstorm and dead ends

| # | Idea | Kill test | Outcome |
|---|---|---|---|
| 1 | Finite-state good/bad condition from periodic ternary digits of 2^(−k) | which digits control the real size? | DEAD: the top digits (position p−1, p = P+5 growing). Finite-state only for p ≤ d, i.e. the first ≈ d/2.4 letters: a constant factor |
| 2 | Other sibling pairings with an "easy" phase | phase-difference formula | DEAD: the phase is (D_{u′}−D_u)·h·3^(−(P+P_u))/2^k with \|D_{u′}−D_u\| < 3^(P_u). The node's 3^P never cancels unless P = 0, where an r-block with r ≍ K is the whole sum |
| 3 | Positive proportion of good nodes on every path, unconditionally | Lemma R | OPEN, Erdős-type (R*). Proved only: root good if 3 ∤ h; nodes with p ≤ p₀ or k ≤ k₀ good for ε = ε(p₀,k₀). Constant factor |
| 4 | Korobov-range sums for a (1−c) factor at each of (log K)^(3/2) tail levels | are levels independent? | DEAD: goodness at all levels l ≤ L of one tail depends on all bits of 3^(−i) mod 2^L. Joint equidistribution over n levels at precision 2^(−d) needs a saving 2^(−dn) from one sum, so n ≲ c·log K. A first-moment argument gives only a constant factor |
| 5 | Average over K (FP-0 for most Q) | how many letters see 2^(−K) equidistributed? | DEAD: 2^(−K) mod 3^p equidistributes over K ≤ X only for p ≲ 2·log₃X, the first O(log K) letters (w3-fp0 dead end 10) |
| 6 | Average over h (large sieve) | Σ_h \|T_K(h)\|² | CIRCULAR: equals the window collision count, the Frostman form of FP-0 (Proposition 2) |
| 7 | Fourth moment / additive energy | energy exponent | 2.12–2.19 (VERIFIED k ≤ 44). Improves the large-frequency count to 2^k·N^(−1.8); cannot certify a given ξ |
| 8 | Erdős–Kahane over the 3-adic parameter ζ | is ζ = −h·2^(−K) covered? | NOT A PROOF: generic ζ decay, bad ζ exist (1, 2, 1/11). A small exceptional set cannot be shown to miss a given countable family |
| 9 | Bourgain–Dyatlov / sum-product | nonlinearity? | DEAD: affine maps with commuting multipliers; multipliers at depth q form a progression of length ≤ q |
| 10 | abc / Ridout for (R*) | exponents | CANDIDATE (hand computation): a run needs 11h = m·3^p + t·2^k with \|m\| ≤ ε2^k·3^(−ΔP), \|t\| ≤ ε3^(P₀+5). abc would give ΔP ≤ 0.63·log₂\|h\| + ε′K, i.e. runs of length o(K), not O(1). Ridout gives nothing unless ΔP ≥ P₀ |
| 11 | Majorant with longer blocks | δ_U(r) | WORKS numerically (0.145 → 0.34 at r = 8), but the hypothesis stays of the same digit type |

Hostile self-review.
- Proposition 1: the monotonicity and Selberg coefficient bounds are standard; I did not re-derive Selberg's construction. The bound is never below 2^(1−m)·N_K, so there is no conflict with Theorems 48/57.
- Theorem 5 is elementary. The constant 0.4 was checked: min over 8 ≤ k ≤ 3200 of 2N_(k−7)/N_k is 0.445. Proposition 4 was checked against direct sums (k ≤ 20, random ξ).
- `g2_major.py` uses the top 60 bits of the residue and doubles. δ_U and g are float-verified, not exact; g could flip at a node within 2^(−50) of the threshold.
- The grids in `g2_major.py` and `g4_runs.py` include nodes not reachable from (0,K); fractions are over the grid.
- "ζ = 1, 2, 1/11 give no decay" is numerical at K ≤ 37 only.
- (D) was tested for eight values of h only, not searched adversarially over |h| ≤ 2^(ηK).
- Litmus. All statements are about |T|, invariant under E ↦ −E, where the set contains 1. Corollary 6 and Lemma R use only the multipliers 3^(−2), 3^(−3) and shifts 3, 4; the constant 11 is 27 − 16. For 5n+1 the same proofs apply with other constants (not run). Nothing touches H1.
- No `exploreXX.py` was run; `plan.md` and `proof.md` were not edited, per the track rule.

## (e) Best lead

**Lemma (R*) for h = 1, weakest useful form.** There are L and K₀ such that for K ≥ K₀ no block path from (0,K) contains L+1 consecutive nodes (P,k) with ‖11·3^(−(P+5))/2^k‖ < 10⁻³.
- By Lemma R it suffices that ‖11·3^(−p)/2^k‖ ≥ 10⁻³·3^(−4L) for all 8 ≤ k ≤ K, 9 ≤ p ≤ 0.75(K−k)+11. In words: the 2-adic expansion of 11·3^(−p) has no run of 6.34L+10 equal bits ending just below a height k in that cone.
- It gives |T_K(1)| ≤ N_K^(1−δ). The uniform version over |h| ≤ 2^(ηK), hypothesis (D), gives FP-0.

**Intermediate target, not attempted: a Tsujii-type large-deviation theorem (CONJECTURED).** #{ξ mod 2^k : |T_k(ξ)| ≥ N_k^(1−δ)} ≤ 2^(κ(δ)k) with κ(δ) → 0 as δ → 0.
- The majorant of Theorem 5 is the natural tool: U_k(ξ) large forces most path mass through bad nodes, and by Lemma R bad runs pin ξ·3^(−p) mod 2^k to few residues.
- It would not give FP-0 alone. One must still show that the integers h ≤ N^δ (or the tail-block multipliers h·3^(−P)) avoid a sparse set. It would replace "the orbit of 3 equidistributes" by "the orbit of 3 does not stay in a set of size 2^(κk)".

**Credences**

| Claim | Credence |
|---|---|
| Proposition 1 (PFD-int ⇒ FP-0, δ′ formula) | 93% |
| Proposition 2 | 90% |
| Proposition 3 (mirror identity) | 98% |
| Proposition 4, Theorem 5 | 96% |
| Lemma R | 96% |
| Corollary 6 implication | 92% |
| (D) true for some η, ε, c | 80% |
| (PFD-int) true | 88% |
| (D) or (PFD-int) provable with published tools | 3% |
| Tsujii-type large-deviation bound provable | 40% |
| This family yields H1 | < 1% |

Sources:
- [arXiv:1906.12164](https://arxiv.org/abs/1906.12164) (Solomyak)
- [arXiv:1710.06812](https://arxiv.org/abs/1710.06812) (Mosquera–Shmerkin)
- [arXiv:1902.00426](https://arxiv.org/abs/1902.00426) (Li–Sahlsten)
- [arXiv:2004.09358](https://arxiv.org/abs/2004.09358) (Varjú–Yu)
- [arXiv:1910.03463](https://arxiv.org/abs/1910.03463) (Brémont)
- [arXiv:2104.03955](https://arxiv.org/abs/2104.03955) (Rapaport)
- [arXiv:2012.06529](https://arxiv.org/abs/2012.06529) (Algom–Rodriguez Hertz–Wang)
- [arXiv:2407.16699](https://arxiv.org/abs/2407.16699) (Baker–Khalil–Sahlsten)
- [arXiv:1704.02909](https://arxiv.org/abs/1704.02909) (Bourgain–Dyatlov)
- [arXiv:2009.01703](https://arxiv.org/abs/2009.01703) (Sahlsten–Stevens)
- [arXiv:2306.01389](https://arxiv.org/abs/2306.01389) (Baker–Sahlsten)
- [arXiv:2602.05593](https://arxiv.org/abs/2602.05593) (Baker–Banaji)
- [arXiv:2101.05910](https://arxiv.org/abs/2101.05910) (Han Yu)