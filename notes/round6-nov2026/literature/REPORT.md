<!-- Saved by the coordinator from the literature agent's final message (the agent's own write was refused). -->
# Full report (intended `literature/REPORT.md`)

Evidence grades: **[P]** primary source fetched and read today; **[S]** snippet or secondary only; **[M]** memory. Proofs were not checked. About 120 web queries in total across four threads.

## A. Uniform harmonic bound, residue, sojourn count, cycle length

**A1. Nikzad, Frinkle, Bagherzadeh, "On Bounds for Reciprocal Sums and Residues in Collatz Orbits, and Their Consequences"** [P]. Hexagon 2611.00033v1; title page "September 22, 2026 (draft) October 26, 2026 (revised)"; posted 3 Nov 2026; 127 pp; AI-assisted (ChatGPT), unrefereed. https://hexagonmath.org/2611.00033v1 (`dl/hexagonmath-2611.00033/`).
- Abstract: "Let F be a finite nonrepeating shortcut path whose input states are greater than 1, let R_F be the sum of the reciprocals of its odd inputs, and let ρ_F be its finite-path residue. Then R_F < 1, ρ_F < 4/3. … More generally, when each odd value greater than 1 is counted once, the corresponding reciprocal-sum and residue bounds hold for every forward orbit, without a termination assumption."
- Theorem 2.16 (Uniform Finiteness) is computation-free, with two proofs and coarse constants "R(n) < 40.941, ρ(n) < 8.45 × 10^5". The text adds: "In particular, B_ρ answers Roosendaal's Weak Residue Conjecture."
- Theorem 2.23: "Every terminating positive integer n satisfies ρ(n) < 4/3." It uses Roosendaal's delay-record range D = 28019077177231758495 and the residue record below 2^32.
- Corollary 3.20: "If the forward orbit of n does not terminate, then R°(n) ≤ 9/50 < log 2, ρ°(n) ≤ e^(3/50) < 2^(1/3), Π°(n) ≤ e^(9/25) < 2." The proof treats cycles and divergence separately. On a cycle this gives 3^a < 2^p < 2^(1/3)·3^a, hence p = ⌈a log₂3⌉. I did not find that sentence in the paper; it is a one-line corollary.
- Mechanism, from a co-author's MO answer of 9 Nov 2026: count odd iterates in (2^j, 2^(j+1)) with s odd steps in the next j steps, using "N_{j,s} ≤ C(j−1, s−1), Σ_j N_{j,s} ≤ 2·3^(s−1)" (Terras–Everett bijection and distinct endpoints), split at s = 3j/5. This is the same mechanism as Theorem 70.
- Constants: NFB bound odd terms (< 1 with computation, < 40.94 without) and residue 4/3. The repo bounds all terms (27.2; Lean 162) and residue 5.72. NFB is stronger on every listed consequence.

**A2. MathOverflow 513539, 24 July 2026** [P], "Is it known that a divergent Collatz trajectory must have summable reciprocals?" (`dl/stackexchange-api/`). It derives from García–Tal's equation (6) "#(O ∩ [a, a+X)) ≤ A X^(1−η) log(2X) for all a, X ≥ 1", hence Σ 1/x_j < ∞ and "m_k log 3 − k log 2 → +∞, which is strictly stronger … than the classical liminf m_k/k ≥ log 2/log 3 (Lagarias 1985, §2.7)". The asker found nothing in Lagarias's bibliographies, Wirsching's book or Rozier's papers.

**A3. García–Tal, Acta Arith. 90 (1999) 245–250** [P]. Equation (6): "#(P ∩ {a,…,a+k−1}) ≤ 2(⌊log_d(k)⌋+1)(k^(1−δ₁)+g(k))", uniform in the orbit, with inexplicit Heppner exponents. "Corollary 1. The Banach density of the orbit O(n) under H is zero." Finite orbits are dismissed as obvious, so terminating trajectories and cycles are not covered verbatim.

**A4. `msharpe248/collatz`, `paper/orbit_summability.pdf`, 5 Sept 2026** [P], Lean. "Theorem 1. If N > 0 and ∀B ∃t (B < x_t), then Σ 1/x_t < ∞, sup_t c_t(N) < ∞, 2^t/3^(j_t) → 0." The majorant is seed-independent ("sum less than 1000"). Implied count exponent 0.985. The paper says "We make no claim of mathematical novelty." It covers unbounded orbits only.

**A5. Sojourn exponent.**
- Lagarias 1985, Theorem F, eq. (2.21) [P, formula image]: "|π*(x) − x| ≤ c₁ x^(1−η)", "η ≈ .05004…". §2.7 applies it only to terms never undercut later.
- rStation paper 28 (u/lyapunov_weaver, v3, 26 Oct 2026) [P]: θ = H₂(log₃2); Theorem 1 "G_{k²}(m) ≤ 2^86 m^θ/(1+log₂m)^(3/2)" for arbitrary interval location. It cites García–Tal, an earlier rStation post with (log)^(−1/2), and Leen (Zenodo 10.5281/zenodo.23252397, "every power exponent greater than H₂(log₃2)"). It notes "every orbit's distinct-state critical zeta sum is finite". It also claims an ineffective power saving m^(θ−γ).

**A6. Roosendaal and Luo** [P].
- Roosendaal, https://www.ericr.nl/wondrous/ : "Conjecture 2a: (weak residue conjecture) A number Res_max exists such that for every positive integer Res(N) < Res_max. … Conjecture 2b: (strong residue conjecture) For all N: Res(N) ≤ Res(993). … we will from now on assume that at least conjecture 2a holds, and also that Res_max ≪ 6." No upper bound is stated as proved.
- Luo, arXiv:2506.23070: Conjecture 1.1 "Res(N) < 2"; Theorem 3.5, assuming Collatz, "if O(N) ≥ 20, then Res(N) < O(N)^(1/9)".

**A7. Cycle length.** The classical result is log₂3 < p/a ≤ log₂(3 + 1/m) (Eliahou 1993 [S]). That gives p = ⌈a log₂3⌉ only when a < 3m·ln 2. The unconditional form follows from NFB Corollary 3.20.

**Repo changes for A.**
- Delete "not found in print … may be folklore" and cite A1–A5.
- Do not claim the weak residue conjecture first.
- The X^0.94996 count and its log saving are also anticipated.
- Still claimable: an independent, kernel-checked, computation-free proof for all trajectories.

## B. Rigidity

- **Bernstein–Lagarias, Canad. J. Math. 48 (1996), Appendix B** [P]: "a map is solenoidally conjugate to the 2-adic shift map S … if and only if it is of the form U_{V0,V1}" (Theorem B.2). Corollary A.3 identifies solenoidal bijections with 2-adic isometries. Property (I) says the parity-vector map is a solenoidal bijection, so every map with (I) has this form. S_a is an immediate instance, though not written down there.
- M. Monks, Discrete Math. 309 (2009) [bibliography entry]: "the only continuous endomorphisms of S whose parity vector is solenoidal are D, V∘D, S, and V∘S". This is a rigidity result in a different class.
- No uniqueness statement in Akin 2004 or Kraft–Monks 2010 (grep).
- No statement found that (I)+(II)+(III) forces T, after about 19 queries.
- Not obtained: Monks–Yazinski and Matthews–Watts full texts.

**Repo change:** present Theorem 68 as a corollary of Appendix B plus an archimedean pinning. "Rigidity" should not suggest that the classification of parity-prefix maps is new.

## C. Two-block exclusion

- **Dubickas, Glasgow Math. J. 51 (2009), Theorem 5** [P]: for x_n → ∞ under the Collatz map with parity word X, "P(X, n) > 1.70951129n for each sufficiently large n". The proof is the repetition barrier: two equal length-m factors at nearby positions give 2^m | x_n − x_s against x_n < (3/2)^n(x_0+1). This excludes all Sturmian itineraries (complexity n+1). Agent inference: it also excludes two-block codings of Sturmian words.
- **Allikvere, Zenodo 10.5281/zenodo.21543841 (25 July 2026)** [P], unrefereed: "Quantitative periodic shadow" theorem; corollary "Internal squares after a shift"; "If w is a Sturmian word, then Φ(w) ∉ Q"; Φ(w) ∈ Q implies dio(w) ≤ max(1, δ log₂3).
- **De Jesús, Zenodo 10.5281/zenodo.23108509 (2 Oct 2026)** [P]: v aperiodic and Φ(v) ∈ Q imply p_v(L) > L/(g*(v)+ε). Agent computation: for ones-density in [2/3, 3/4] this excludes words with liminf p(L)/L below about 5.3 to 17.7.
- **`msharpe248/collatz`** [P]:
  - `prefix_power` (29 Aug 2026): "If the itinerary of n is ℓ-periodic on its first M letters … then T^ℓ(n) = n or 2^(M−ℓ) ≤ max(n, T^ℓ(n))".
  - No itinerary is a shift of the fixed point of 1→110, 0→011 (Mahler method).
  - `mechanical_classification.pdf` (5 Sept 2026): "For all α, ρ ∈ R and N > 0, HasItin(α, ρ, N) implies α = 1/2 and N ∈ {1, 2}", with "not … a claim of mathematical novelty".
- Dubickas, Acta Arith. 137 (2009) [P]: the Mahler-problem analogue, using the fact that Sturmian words "begin in arbitrarily long squares".
- López–Stoll, arXiv:2101.12747 [P]: poses "Is it true that for any aperiodic word v there is no x ∈ Q_odd, having v as parity vector?" Its Theorem 1 would subsume C, but the proof looks flawed; do not rely on it.
- Hexagon 2611.00459 (De Jesús, 15 Nov 2026) [abstract]: "An initial square UU in a failing word satisfies |U| < 35 log₂ k."

**What may remain:** the weighted two-block lemma (L) as combinatorics, and exclusion of non-primitive morphic two-block words with complexity above the Dubickas and De Jesús thresholds. The repo should state exactly which words (B) reaches that those bounds do not.

**Repo change:** (A) "Repetition barrier" must cite Dubickas 2009. The episturmian/Sturmian corollary is known for two letters.

## D. S-unit window law

- **Chang, arXiv:2603.11066** [P] (the agent read an older text; the current version is v6, 233 pp): S-unit reformulation "(m+1)·3^L − T^L(m)·2^{S_L} = 2^L − P_L"; "Subspace Theorem blocked (coefficients depend on L)". Chang proves no finiteness statement. His obstruction is for L → ∞; the window law fixes k, so it is neither implied nor contradicted. The write-up should say why.
- Template results: Bugeaud–Evertse, arXiv:1611.00485, Theorem 1.1 ("[u_n]_S ≤ |u_n|^ε", ineffective, "an easy consequence of work of Evertse") [P]; Corvaja–Zannier, arXiv:math/0311030 [P]; Bugeaud–Corvaja–Zannier 2003.
- rStation paper 30 v2, Lemma 11.1 (26 Oct 2026) [via summary]: a fixed-place Subspace argument on Collatz numerators; not the hop-window statement.
- Verger-Gaugry, arXiv:2611.14569 (9 Nov 2026) [P]: Bennett–Billerey S-unit theorem applied to primes at "wave-minima" of a divergent trajectory; a different statement.
- Not found: any bound v₂(…) ≤ (1+δ)log₂m for k-hop windows.

## E. Log savings

- **E(i).** Lagarias, "Ternary expansions of powers of 2", arXiv:math/0512006 [P]: Theorem 1.4 "#{n ≤ X : (λ2^n)_3 omits the digit 2} ≤ 2X^{α_0}". It poses combining top-digit and low-digit constraints as open: "It seems a challenging problem to find a method that effectively combines the two approaches". No log-saving count for a 2-adic Cantor set was found. Abram–Lagarias, Burrell–Yu and Dimitrov–Howe were seen as snippets or headings only.
- **E(ii).** Anticipated by rStation paper 28 (A5 above) with the better exponent 3/2 and arbitrary windows. The repo's (log X)^(−0.986)·log log X is weaker.

## F. Short intervals

- Tao blog, comment of 23 Aug 2026 (local copy) [P]. An anonymous commenter asks whether short intervals always contain an integer provably reaching 1, with a logarithmic saving. Tao: "there are now some AI-generated solutions to the natural density version of my result; if they check out, they should be able to give something along the lines of your statement … and possibly even a logarithmic saving as you indicate. However, this would need to be done carefully." No reference is given.
- Tijdeman, Compositio Math. 28 (1974) 159–162 [P; displayed inequalities lost in extraction, statement from memory and snippet]: gaps between consecutive integers composed of fixed primes are below n/(log n)^C. This is the same mechanism (convergents of log 2/log 3 plus an irrationality measure).
- F is not a literal corollary, since 3-smooth numbers are not known to reach 1.
- No short-interval statement in Krasikov–Lagarias (abstract), the bibliographies, or Tao's paper. Wirsching's book was not checked.

**Repo change:** cite Tijdeman 1973/74 and the Tao exchange; keep "folklore-level".

## G. Status of third-party claims (all [P] unless marked)

- **Mazur.** "Explicit Positive-Density Collatz Convergence in Logarithmic Time", v2.1, 6 Sept 2026, at proofatlas.ai. Not on arXiv; status "Review pending"; no retraction.
  - Tao has not replied to Mazur's comments of 5 and 6 Sept.
  - Kontorovich [S, Digg mirror of an X post]: "I went through the Lean (or rather, had my AI do it) and I think it's right."
  - Third-party rebuild of Mazur's Lean: `neljaouh/ConjectureA` (26–29 Sept).
  - Follow-ups: Kenny Lau / Axiom, Hexagon 2610.00249 ("AxiomProver" refinement, separate repo); Shaik, Hexagon 2610.00523 and 2610.00299.
  - All of this is AI-assisted and unrefereed, and much of it builds on Mazur's artifact.
  - Mazur's 6 Sept comment: "if any Collatz counterexample exists, the set of counterexamples has positive lower natural density. So … proving almost all positive integers reach 1 … would suffice". This is prior art for the repo's conditional "density one ⇔ Collatz" item.
- **Allikvere.** Zenodo 10.5281/zenodo.21499244 (v2, 22 July 2026); no refereeing or formalization found.
- **`dpalmqvist/kollatz`.** Created 8 Oct 2026; the 0.9251 (k = 22) claim is its own; Lean only at k = 18–20. A higher claim exists: Müller, Zenodo 10.5281/zenodo.21643795, exponent 0.93756 at depth 25. `msharpe248` has a Lean-checked 0.8676.
- **Chang.** v6, 22 Apr 2026.
- **Luo.** v3, 16 July 2026.
- **Barina.** 2075·2^60 ≈ 2^71.02, so "2^71" still holds.
- **arXiv:2601.03297.** v9, 11 Nov 2026, retitled, still conditional.
- **Caution [S].** An AI-generated Lean "disproof" of Collatz in July 2026 exploited a kernel bug patched 28 July; this bears on Lean toolchains pinned from that period.

## Not checked
Wirsching LNM 1681, Korec 1994 full text, Eliahou 1993 full text, Monks–Yazinski (403), Matthews–Watts, Leen's Zenodo appendix, rStation papers beyond 28, 30 and 42, and Tao blog comments older than July 2026.