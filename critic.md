# Deep Research: proof.md vs. the State of the Art

## Executive Summary

The FMF framework is **genuinely original** -- the "First Multiple of Four" decomposition doesn't appear in any published literature. The mathematical content is largely correct in its empirical claims, and several of the theorems are interesting. However, the document has some significant issues when measured against the professional mathematics literature.

---

## 1. What the Literature Says (State of the Art)

### Rigorous Results (accepted by the mathematical community)

| Result | Author(s) | Year |
|--------|-----------|------|
| Almost all orbits attain almost bounded values (log density) | Tao | 2019/2022 |
| Density of integers reaching 1 is at least x^0.84 | Krasikov & Lagarias | 2003 |
| Computational verification up to 2^71 ~ 2.36 x 10^21 | Barina | 2025 |
| No nontrivial cycle with period < ~2.17 x 10^11 | Eliahou (1993), Simons & de Weger (2005) | Various |
| Finitely many periodic orbits (topological approach) | arXiv:2601.03297 | 2025 |
| Stochastic models predict convergence/divergence correctly | Kontorovich & Lagarias | 2009 |
| Average contraction via invariant Markov chain | Carletti & Fanelli | 2017 |

### Key Insight from Tao

Tao explicitly identifies the **fundamental barrier**: "any proof of the Collatz conjecture must either use existing results in transcendence theory, or contribute new methods to transcendence theory." The core difficulty is separating powers of 2 from powers of 3. He also notes: "unless a dynamical system is somehow polynomial, nilpotent, or unipotent in nature, the current state of ergodic theory is usually only able to say something meaningful about generic orbits, but not about all orbits."

---

## 2. Comparison: FMF Framework vs. Literature

### What's Good and Original

1. **The FMF decomposition itself is novel.** No published paper uses the "first multiple of four" as the fundamental unit of analysis. This is a creative repackaging of the Collatz dynamics.
2. **Theorems 1-4 (FMF formulas)** are correct algebraic identities. The step-count and value formulas are clean and verifiable.
3. **Theorem 12 (state-independence)** is an interesting structural observation -- that the output distribution of FMF hops is independent of the input state. This is related to, but not identical to, known results about equidistribution of Collatz residues.
4. **The empirical work is thorough.** The exploration scripts show careful numerical investigation.

### Where It Aligns with Known Results

| FMF Result | Known Equivalent |
|------------|-----------------|
| Drift E[log2(R)] = -0.830 (Theorem 10) | Well-known: E[log2] per odd step ~ log2(3/4) = -0.415, "per FMF hop" doubles this since each hop ~ 2 odd steps on average |
| State-independence (Theorem 12) | Related to Kontorovich-Lagarias observation that residue class distributions converge quickly |
| Cramer bound (Theorem 14) | Standard large deviations applied to Collatz random walk -- appears in multiple heuristic analyses |
| alpha* ~ 1 critical exponent (Theorems 15, 19) | Known: E[(3/4)^alpha * correction] = 1 near alpha = 1 is classical |
| Self-correction (Theorem 18) | Partially known: Carletti & Fanelli observed similar compensatory dynamics mod 8 |

### Where It Has Problems

The document's biggest weakness is the gap between what it claims and what it proves. Several "theorems" are empirical observations labeled as theorems, and the proof.md conflates three very different things:
1. Exact algebraic identities (genuinely proved -- Theorems 1-4)
2. Probabilistic/statistical observations (empirically verified, not proved -- Theorems 9, 10, 14, 18, 22-27)
3. Claims that would resolve the conjecture if true (unproved -- the epoch bound)

---

## 3. Specific Critiques

### Critique 1: The "Rank-1 Closes the Gap" Claim (Section 12, Theorem 19)

The document says: *"Why this closes the gap: The transition matrix entries are NOT computed from finite samples -- they are determined by the exact 2-adic distribution."*

**This does NOT close the gap.** The transition matrix being rank-1 means the *one-step* output distribution is state-independent. But this gives E[R^alpha] < 1 as an *average* over all possible inputs, not a *pointwise* guarantee for every trajectory. The document correctly identifies this later (Gap 3 in Section 13), but the framing in Theorem 19 is misleading.

Tao's insight applies here: knowing the average behavior is relatively easy (the drift is -0.83, everyone agrees). The hard part is controlling **every single trajectory**. The rank-1 observation is interesting but doesn't escape the fundamental barrier that Tao identified.

### Critique 2: Computational Verification Number is Outdated

The document cites 2.95 x 10^20. The current record is **2^71 ~ 2.36 x 10^21** (Barina, 2025).

### Critique 3: Cycle Exclusion Bound is Understated

The document cites "n > 10^8 (Eliahou 1993)." The current best known bound is that any nontrivial cycle must have period > ~2.17 x 10^11 (Simons and de Weger extended Eliahou's method).

### Critique 4: The Epoch Bound Strategy Has a Known Obstacle

Theorems 24-25 establish epoch_duration(x) <= C * log2(x) empirically. The document then argues (Section 17) that this would prove Collatz if established universally. But this is essentially restating the conjecture in different language. The epoch bound says "every number eventually goes below itself" -- which **is** the Collatz conjecture for the Syracuse map. The problem hasn't been reduced; it's been reformulated.

### Critique 5: Engagement with Tao's Barrier -- PARTIALLY ADDRESSED (explore30)

Tao showed that *any proof must engage with transcendence theory* (the separation of powers of 2 and 3). The original FMF framework didn't address this.

**The 5n+1 litmus test was run (explore30).** Results:

The structural arguments (state-independence, rank-1 matrix, v_2 geometric distribution) hold identically for 5n+1, as predicted. However, **a concrete discriminant was found:**

- **3n+1 Type A channel:** 3(4k+1)+1 = 4(3k+1). Ratio = 3/4 < 1. **Always shrinks.**
- **5n+1 Type A channel:** 5(4k+1)+1 = 2(10k+3). Ratio = 5/4 > 1. **Always grows.**

**3 is the largest odd integer where a/4 < 1.** This gives 3n+1 a guaranteed pointwise contraction on 50% of hops that 5n+1 completely lacks. The drift decomposition confirms this:

| Map | E[log2(R)\|Type A] | E[log2(R)\|Type B] | Overall |
|-----|-------------------|-------------------|---------|
| 3n+1 | -1.415 (always <0) | -0.245 | -0.830 |
| 5n+1 | +1.322 (always >0) | -0.678 | +0.322 |

**Status of this critique:** The FMF framework now has a structural mechanism that distinguishes 3n+1 from 5n+1 (the 3/4 contraction channel). However, this mechanism alone doesn't complete the proof -- it explains *why* the drift is negative but doesn't resolve the pointwise convergence gap. The next step is to show that the guaranteed 50% contraction channel, combined with the self-correction mechanism (Theorem 18), forces every trajectory to eventually contract. This still requires engaging with the specific arithmetic of powers of 3 mod powers of 2.

### Critique 6: Theorem Numbering vs. Rigor

Several items labeled "Theorem" should be "Conjecture" or "Empirical Observation":
- **Theorem 9**: "State-Independent Transitions" -- labeled "empirically established" then later given algebraic proof in Theorem 12. OK, but the proof sketch in Theorem 12 is informal.
- **Theorem 11**: "Bounded Peak Growth" -- purely empirical, not a theorem
- **Theorems 22-27**: All empirical, not proved

---

## 4. What's Actually Close to the State of the Art

The FMF work is most comparable to:

1. **Carletti & Fanelli (2017)**: They also build a Markov chain on residue classes with an invariant measure and show average contraction. The FMF framework is a more structured version of essentially the same idea, using mod-4 states instead of mod-8.

2. **The spectral calculus preprint (2025)**: A recent preprint by an independent researcher claims to establish a spectral gap via transfer operator methods -- this is the operator-theoretic analog of the rho < 1 result. Like this work, it reduces the conjecture to excluding a specific forward-dynamical pathology.

3. **The topological/ergodic approach (arXiv:2601.03297)**: Proves finitely many cycles exist using thermodynamic formalism. This is stronger than the cycle analysis in proof.md but still doesn't prove the full conjecture.

---

## 5. Bottom Line Assessment

| Aspect | Rating | Notes |
|--------|--------|-------|
| Originality of FMF framework | **High** | Novel decomposition, not in literature |
| Correctness of algebraic formulas (Th 1-4) | **Solid** | Verifiable, likely correct |
| Quality of empirical investigation | **Very good** | Thorough, well-organized explorations |
| Gap identification | **Accurate** | Correctly identifies the pointwise vs average gap |
| Claims vs. what's actually proved | **Overstated** | Many "theorems" are empirical; Th 19 "closes the gap" language is misleading |
| Engagement with existing literature | **Weak → Improving** | No citations initially; 5n+1 comparison now addresses Tao's barrier partially |
| Novelty of mathematical contribution | **Moderate → Solid** | FMF formulas + the 3/4 discriminant (Theorem 30) are genuinely new |
| Path to proof | **Clearer than before, still open** | 3/4 channel identified as the mechanism; pointwise gap remains |

### The Honest Summary (Updated after explore30)

This work is a well-executed empirical and semi-algebraic investigation that rediscovers many known phenomena through a novel lens (the FMF decomposition). The algebraic formulas (Theorems 1-4) and the 3/4 discriminant (Theorem 30) are the strongest original contributions.

**The 5n+1 discriminant (Theorem 30) is a genuine advance.** It identifies a concrete structural mechanism -- the Type A contraction channel with ratio 3/4 < 1 -- that distinguishes 3n+1 from divergent maps. This is not just the drift sign; it's a *pointwise* guarantee: every Type A hop shrinks, deterministically. No published paper frames the 3-vs-5 distinction this cleanly through the FMF lens.

**The remaining gap** is still the same fundamental challenge: showing that the 50% guaranteed contraction channel, combined with self-correction dynamics, forces *every* trajectory to converge. The 3/4 channel gives a stronger starting point than pure average arguments, but converting "50% of hops always shrink" into "every trajectory eventually reaches 1" still requires new ideas -- likely involving the specific 2-adic arithmetic of powers of 3 (proximity chains, carry propagation, or equidistribution bounds).

**What's changed:** The framework now has a proof-relevant structural distinction that passes the 5n+1 litmus test. The question has sharpened from "why does 3n+1 converge?" to "why does the 3/4 contraction channel, which fires on 50% of hops, always eventually dominate?"

---

## References

- Tao, T. "Almost all orbits of the Collatz map attain almost bounded values." Forum of Mathematics, Pi 10 (2022): e12. arXiv:1909.03562
- Tao, T. "The Collatz conjecture, Littlewood-Offord theory, and powers of 2 and 3." Blog post, 2011.
- Barina, D. "Improved verification limit for the convergence of the Collatz conjecture." Journal of Supercomputing 81, 810 (2025).
- Carletti, T. & Fanelli, D. "Quantifying the degree of average contraction of Collatz orbits." Bollettino dell'Unione Matematica Italiana (2017). arXiv:1612.07820
- Kontorovich, A. & Lagarias, J. "Stochastic models for the 3x+1 and 5x+1 problems." arXiv:0910.1944 (2009).
- Lagarias, J. "The 3x+1 Problem: An Overview." arXiv:2111.02635 (2021).
- Krasikov, I. & Lagarias, J. "Bounds for the 3x+1 problem using difference inequalities." Acta Arithmetica 109 (2003): 237-258.
- Eliahou, S. "The 3x+1 problem: new lower bounds on nontrivial cycle lengths." Discrete Mathematics 118 (1993): 45-56.
- Simons, J. & de Weger, B. "Theoretical and computational bounds for m-cycles of the 3n+1 problem." Acta Arithmetica 117 (2005): 51-70.
- Mori, T. "Application of Operator Theory for the Collatz Conjecture." arXiv:2411.08084 (2024).
- "On the Collatz Conjecture: Topological and Ergodic Approach." arXiv:2601.03297 (2025).
