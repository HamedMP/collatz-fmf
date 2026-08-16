# Towards a Proof of the Collatz Conjecture via the FMF Framework

> **Status note (May 2026 review):** this file is a research log, not a completed proof. The exact FMF formulas are solid, but the later average-contraction and growth-chain arguments do **not** prove the Collatz conjecture. The current cleaned-up version is the Typst paper in `paper/`, which recasts the strongest results as density theorems and leaves the pointwise "almost all to all" gap open.
>
> **Canonical source warning:** the theorem labels and proof sketches below are historical working notes. Do not cite this file as the current manuscript, a proof claim, or the repository's claim boundary. Use `paper/main.typ`, `proof-obligations.md`, `publication-readiness.md`, and `referee-brief.md` for the vetted statement of what is proved and what remains missing.

## 1. Setup and Notation

**Collatz function:** C(n) = n/2 if n even, 3n+1 if n odd.

**Modified Collatz U(x):** Apply C repeatedly, dividing by the largest power of 2 (LPT) at each even step. This maps odd numbers to odd numbers.

**2-adic valuation:** v_2(n) = largest k such that 2^k | n. Equivalently, the number of trailing zeros in binary.

**Mod-4 classification of odd numbers:**
- **Type A:** x ≡ 1 (mod 4), i.e., x = 4k+1
- **Type B:** x ≡ 3 (mod 4), i.e., x = 4k+3

**T_i operator (chained odd-step):** T_i(x) = 3^i(x+1)/2^i - 1

**FMF:** "First Multiple of Four" -- the first value in the Collatz sequence of an odd x that is divisible by 4.

---

## 2. Proved Theorems

### Theorem 1: FMF Step Count (explore01, explore05)

**Statement:** For any odd x, the number of Collatz steps to reach the first multiple of 4 is:

| Case | Condition | FMF step count |
|------|-----------|---------------|
| A | x ≡ 1 (mod 4) | 1 |
| B1 | x ≡ 3 (mod 4), k even (x = 4k+3) | 3 |
| B2 | x ≡ 3 (mod 4), k odd (x = 4k+3) | 3 + 2·v_2(k+1) |

**Proof (Case B2):** Write k+1 = 2^t · m with m odd, t ≥ 1. Then x = 2^(t+2)·m - 1. Starting from x, the Collatz sequence strictly alternates (3x+1, /2) with coefficients:

- Step 2j-1: value = 3^j · 2^(t+2-j+1) · m - 2 (even, ≡ 2 mod 4 since 3^j · 2^(t+2-j+1) ≡ 0 mod 4 for j ≤ t, minus 2)
- Step 2j: value = 3^j · 2^(t+2-j) · m - 1 (the /2 of previous; odd for j ≤ t)

The power of 2 in the leading coefficient decreases by 1 every two steps. At step 2t+2, the coefficient of m is 3^(t+1) · 2, so the value is 3^(t+1)·2m - 1 (odd). Then step 2t+3 = 3+2t applies 3x+1:

3(3^(t+1)·2m - 1) + 1 = 3^(t+2)·2m - 2 = 2(3^(t+2)·m - 1)

This is the FMF value. Since 3^(t+2)·m is odd (both factors odd), 3^(t+2)·m - 1 is even, so 2(3^(t+2)·m - 1) is divisible by 4.

**Verified:** Symbolically for t = 1..15, numerically for 1,200 (t,m) pairs with 0 errors. Also verified for 1M values of k with 0 failures. ∎

### Theorem 2: FMF Value Formula (explore02, explore05)

**Statement:** The FMF value for x = 4k+3 is:

| Case | FMF value |
|------|-----------|
| x = 4k+1 | 4(3k+1) = 12k+4 |
| x = 4k+3, k even, k=2j | 4(9j+4) = 36j+16 |
| x = 4k+3, k odd, t=v_2(k+1) | 3^(t+2)·(k+1)/2^(t-1) - 2 |

Equivalently for case B2: with k+1 = 2^t·m (m odd),
**FMF = 2(3^(t+2)·m - 1)**

**Verified:** 500K odd k values, zero failures. ∎

### Theorem 3: v_2(FMF) Exact Formula (explore08)

**Statement:** For x = 4k+3 with k odd, writing k+1 = 2^t·m:

**v_2(FMF) = 1 + v_2(m - (3^(t+2))^{-1} mod 2^N)**

where (3^(t+2))^{-1} is the 2-adic inverse of 3^(t+2).

**Proof sketch:** FMF = 2(3^(t+2)·m - 1). Since 3^(t+2) is a 2-adic unit:
v_2(3^(t+2)·m - 1) = v_2(m - (3^(t+2))^{-1}) in Z_2.

This follows from the multiplicativity of v_2 for units: for any 2-adic unit u,
v_2(u·a - 1) = v_2(a - u^{-1}).

**Verified:** 900 cases with 0 errors. ∎

### Theorem 4: v_2(3^n - 1) (known result, verified in explore06)

**Statement:**
- v_2(3^n - 1) = 1 if n is odd
- v_2(3^n - 1) = v_2(n) + 2 if n is even

---

## 3. The FMF Hop Map

### Definition

The **FMF hop** F: {odd numbers > 1} → {odd numbers} is defined as:

F(x) = FMF(x) / 2^{v_2(FMF(x))}

This maps each odd number to the next odd number obtained by finding the FMF and dividing by its LPT.

### Key Properties (empirically established)

**Property 1 (Completeness):** Every odd number > 1 has a well-defined FMF hop.

**Property 2 (Eventual descent):** For every odd x > 1, there exists n such that F^n(x) < x.

**Property 3 (Convergence to 1):** For every odd x > 1, there exists n such that F^n(x) = 1. (This is equivalent to the Collatz conjecture.)

**Property 4 (Compression):** On average, each FMF hop corresponds to ~6 Collatz steps.

### Growth/Shrinkage Analysis

At each FMF hop from x to F(x):
- **Growth factor:** 3^s where s = number of 3x+1 operations within the hop
- **Shrinkage factor:** 1/2^d where d = number of /2 operations (internal + LPT division)
- **Net multiplier:** F(x)/x = 3^s / 2^d

For case A (x = 4k+1): s=1, d=2+v_2(3k+1). Net ≈ 3/4 · 1/2^{extra}. Always shrinks.

For case B2 (x = 4k+3, k odd): s=(3+2t+1)/2 = t+2, d=(3+2t-1)/2 + v_2(FMF) = t+1+v_2(FMF).
Net multiplier ≈ 3^(t+2) / 2^(t+1+v_2(FMF)) = (3/2)^(t+2) / (2 · 2^{v_2(FMF)-2}).

For 1-hop descent: need v_2(FMF) > (t+2)·log_2(3/2) + 1 ≈ 0.585(t+2) + 1.

---

## 4. The Descent Problem

### What We Know

**Theorem 5 (Empirical):** Every odd number in [3, 10000] reaches 1 via FMF hops. Max depth = 42 hops (x=6171), mean depth = 15.27.

**Theorem 6 (Release Valve):** When a Type B number (4k+3) does an FMF hop, the result is Type A (4k+1) approximately 50% of the time. Type A hops always give net shrinkage (multiplier ≈ 3/4).

**Theorem 7 (v_2 Distribution):** Among random odd m, v_2(m - inv) follows a geometric distribution:
P(v_2(m - inv) = j) = 1/2^j for j ≥ 1.
E[v_2(m - inv)] = 2.

**Theorem 8 (Net Bits):** For all tested numbers (up to 10000), the net log_2 multiplier over a complete FMF chain to descent is always negative. Tightest case: x=63 with net_bits = -0.11.

### The Core Difficulty

To prove Collatz via FMF, we need to show that for every odd x > 1, the FMF chain eventually reaches 1. The barriers are:

1. **Successive m values are not independent.** The m parameter at hop n+1 depends on the result of hop n. We cannot simply apply the geometric distribution independently.

2. **No uniform contraction.** Individual hops can increase the value (when v_2(FMF) is small). Descent requires the *product* of multipliers to be < 1, which may take many hops.

3. **No periodic orbit exclusion.** We haven't proved that no cycle exists in the FMF graph (other than the fixed point at 1).

---

## 5. Proof Strategy

### Strategy A: Probabilistic Descent via Markov Chain

**Idea:** Model the FMF chain as a Markov chain on states (type, t-value). If the stationary distribution gives expected log-shrinkage < 0, this would prove "almost sure" descent, and with additional bounds, universal descent.

**Transition probabilities:**
- Type A (4k+1): always shrinks. Next number's type is ~50/50 A or B.
- Type B (4k+3): multiplier depends on v_2(FMF).
  - ~50% of time, result is Type A (release valve)
  - ~50% of time, result is Type B (continue)

**Expected log_2 multiplier per hop:**
- Type A hop: E[log_2(F(x)/x)] ≈ log_2(3/4) + adjustment = -0.415 + ...
- Type B hop with t: E[log_2(F(x)/x)] = (t+2)·log_2(3) - (t+1) - E[v_2(FMF)]

**Key question:** What is the expected v_2(FMF) conditioned on the chain history?

### Strategy B: 2-Adic Contraction

**Idea:** The FMF hop defines a map on the 2-adic integers Z_2. If this map is a contraction in the 2-adic metric (or some weighted metric), then every orbit converges.

**The map:** For x = 2^(t+2)·m - 1 (m odd):
F(x) = (3^(t+2)·m - 1) / 2^{v_2(3^(t+2)·m - 1)}

In 2-adic terms, this is: m ↦ (3^(t+2)·m - 1) · 2^{-v_2(3^(t+2)·m-1)}

The v_2 factor acts as a 2-adic "distance to the inverse."

### Strategy C: Lyapunov Function

**Idea:** Find a function L(x) such that L(F(x)) < L(x) for all x > 1. Natural candidates:
- L(x) = x (descent = reaching value < x)
- L(x) = log(x) (descent in bits)
- L(x) = some function of x's binary representation
- L(x) = 2-adic valuation of some transform of x

### Strategy D: Cycle Exclusion + Unbounded Growth Exclusion

**Idea:** Separately prove:
1. No cycle exists (other than 1→1)
2. No orbit diverges to infinity

For (1): A cycle of length n would need product of multipliers = 1 exactly.
For (2): The expected log-shrinkage is negative, so divergence requires infinite consecutive "bad" hops, which has probability 0.

---

## 6. Formulas Reference

| Formula | Expression | Source |
|---------|-----------|--------|
| FMF step (B2) | 3 + 2·v_2(k+1) | Theorem 1 |
| FMF value (A) | 4(3k+1) | Theorem 2 |
| FMF value (B1) | 4(9j+4), j=k/2 | Theorem 2 |
| FMF value (B2) | 2(3^(t+2)·m - 1) | Theorem 2 |
| v_2(FMF) | 1 + v_2(m - (3^{t+2})^{-1}) | Theorem 3 |
| T_i operator | 3^i(x+1)/2^i - 1 | Definition |
| v_2(3^n - 1) | 1 (n odd), v_2(n)+2 (n even) | Theorem 4 |
| Compression | ~6 Collatz steps per FMF hop | Empirical |
| Descent depth | Mean 15.27, max 42 (for [3,10000]) | Empirical |

---

## 7. Exploration Results

### Theorem 9: State-Independent Transitions (explore11)

**Statement:** The FMF hop output state distribution is independent of the input state. For ANY input state, the output follows:
- P(Type A) = 50%
- P(Type B, t=j) = 1/2^(j+2) for j = 0, 1, 2, ...

This is a geometric distribution: P(t ≥ j) = 1/2^(j+1).

**Verified:** Transition matrix computed from 50,000 odd numbers. All rows are identical within statistical noise.

### Theorem 10: Negative Expected Drift (explore11)

**Statement:** The expected log_2 multiplier per FMF hop is:

| State | E[log2(F(x)/x)] | P(shrink) |
|-------|-----------------|-----------|
| A(t=0) | -1.415 | 100% |
| B(t=0) | -0.830 | 50% |
| B(t=1) | -0.245 | 50% |
| B(t=2) | +0.340 | 25% |
| B(t≥3) | positive, growing | <25% |
| **Overall** | **-0.830** | **71.4%** |

The theoretical formula E[log2] = 0.585(t+2) - 3 for Type B matches empirical values to 4 decimal places.

**Type distribution along chains (from 25K trajectories):**
- Type A: 52.3% of all hops
- Type B: 47.7% of all hops
- Among Type B: 72.5% have t=0, 13.9% t=1, 7.6% t=2, 2.3% t=3, ...

### Theorem 11: Bounded Peak Growth (explore11)

**Empirical:** Peak growth ratio max(F^j(x))/x is bounded:
- x=27: peak = 33.7x
- x=703: peak = 52.8x
- x=6171: peak = 19.8x
- x=9663: peak = 350.8x (large t-values encountered)

---

## 8. Further Results (explore12-14)

### Theorem 12: Algebraic Proof of State-Independence (explore12)

**Statement:** The FMF output state distribution is state-independent because:
1. F(x) = (3^(t+2)*m - 1) / 2^{v_2(3^(t+2)*m - 1)}
2. v_2(3^(t+2)*m - 1) = v_2(m - inv) where inv is the 2-adic inverse of 3^(t+2)
3. As m ranges over odd numbers, (m - inv) is even (since inv is odd), and:
   - v_2(m - inv) = j with probability 1/2^j (geometric)
   - The odd part u = (m-inv)/2^v is uniform among odd numbers
4. Since 3^(t+2) is an odd constant, 3^(t+2)*u mod 4 is uniform over {1,3}
5. Therefore P(Type A) = P(Type B) = 1/2, independent of input (t, type)
6. For Type B outputs: P(t'=j) = 1/2^(j+1), also independent of input

**Verified:** mod-4 predictions match actual F(x) in all tested cases. A/B split confirmed at exactly 50.0% for t=1 through t=7.

### Theorem 13: Cycle Constraints (explore13)

**Statement:** Any non-trivial Collatz cycle visiting n odd numbers with total K divisions by 2 satisfies:
- x * (2^K - 3^n) = S, where S is a positive correction sum
- 2^K > 3^n, i.e., K > n*log_2(3) ≈ 1.585n
- (Known) Any cycle must have n > 10^8 (Eliahou 1993)
- (Known) Verified computationally: no cycle for x < 5.76 * 10^18

**FMF implications:**
- In FMF terms, minimum cycle length > 10^8/6 ≈ 1.67 * 10^7 hops
- With drift -0.83 bits/hop: P(return after n hops) ≈ exp(-0.83n)
- For n = 10^7: P ≈ exp(-8.3 * 10^6) ≈ 0

### Theorem 14: No Divergence via Cramer Bound (explore14)

**Statement:** The FMF random walk has drift mu = -0.830, variance sigma^2 = 2.683.
The MGF M(theta) = E[exp(theta*X)] equals 1 at **theta* = 0.6986**.

By the Cramer-Lundberg inequality:
**P(max_n S_n >= H) <= exp(-0.6986 * H)**

Concrete bounds:
| Target | H (bits) | P(reached) upper bound |
|--------|----------|----------------------|
| 2x | 1 | 49.7% |
| 10x | 3.32 | 9.8% |
| 100x | 6.64 | 0.96% |
| 1000x | 9.97 | 0.095% |

**Drift uniformity:** E[log2(F(x)/x)] = -0.83 for ALL bit-lengths tested (8-bit through 18-bit), confirming the drift is magnitude-independent.

**Empirical verification:** Peak growth distribution matches the exponential bound. Max observed peak: 9.96 bits (998.7x), consistent with exp(-0.6986 * 9.96) ≈ 0.1%.

---

## 9. Remaining Gaps for Complete Proof

### Gap 1: Independence / Mixing (Critical)
The i.i.d. assumption on increments is approximate. Successive FMF hops are NOT truly independent because x_{n+1} depends on x_n. To make the Cramer bound rigorous, we need either:
- **Mixing conditions:** Show that correlations between X_i and X_{i+k} decay exponentially in k
- **Supermartingale construction:** Find f such that E[f(F(x)) | x] <= c * f(x) for c < 1
- This is the key remaining mathematical challenge

### Gap 2: Cycle Exclusion (Strong but not complete)
The probabilistic bound makes cycles "effectively impossible" but doesn't mathematically prove they can't exist. Options:
- Formalize the correction sum S in terms of FMF formulas
- Show S < 2^K - 3^n always, using FMF value bounds
- Or prove a direct supermartingale argument that rules out returns

### Gap 3: From "No Divergence" to "Reaches 1"
Even with no divergence and no cycles, need to show the trajectory actually reaches 1 (not just stays bounded). The negative drift gives this: a bounded random walk with negative drift eventually crosses any threshold.

---

## 10. Results from explore15-16

### Theorem 15: Critical Exponent alpha* = 1.008 (explore15)

**Statement:** E[(F(x)/x)^alpha] < 1 for all alpha < alpha* = 1.008.
At alpha = 0.5: E[R^0.5] = 0.863, uniform across all bit-lengths.

**BUT:** Since F is deterministic (not random), f(x) = x^alpha is NOT a pointwise supermartingale. About 29% of hops have F(x) > x. The supermartingale approach requires randomness.

**Mod-8 non-uniformity:** x = 7 mod 8 gives avg ratio ~1.30 (growing), while x = 5 mod 8 gives ~0.47 (shrinking). A weighted Lyapunov L(x) = x^alpha * w(x mod 8) is a potential avenue.

### Theorem 16: Weak Correlations with Self-Correction (explore16)

**Statement:** Along FMF chains, consecutive log2-multipliers have:
- Lag-1 autocorrelation: +0.082 (weak positive)
- Lag-4: +0.020 (~independent)
- Lag-5: +0.006 (~independent)

**Self-correcting behavior:**
- After large growth (X > 3): P(shrink next) = 0.82, E[X_next] = -1.07
- After large growth (1 < X < 3): P(shrink next) = 0.88, E[X_next] = -0.81
- Growing hops cluster slightly: P(grow|grow) = 0.363 vs P(grow) = 0.295 (ratio 1.23)
- Max observed growing streak: 7 hops

**Type-dependent transitions (along chains, not just one-hop):**
- After B(t=4): 75% chance of B(t>=2) next
- After B(t=2): 74% chance of Type A next (strong shrinkage)
- This compensatory mechanism means large-t hops tend to be followed by Type A

**Conclusion:** The chain is weakly dependent, NOT i.i.d. The self-correcting tendency (large growth -> likely shrinkage next) actually makes convergence MORE likely than the i.i.d. model predicts.

---

## 11. Results from explore17-18

### Theorem 17: Spectral Radius Contraction (explore17) -- KEY RESULT

**Statement:** For the weighted Lyapunov function L(x) = x^alpha * w(x mod M), the spectral radius of the transition matrix satisfies rho(T) < 1 for optimal alpha = 0.53.

| M | alpha | rho(T) | Status |
|---|-------|--------|--------|
| 4 | 0.53 | 0.8627 | CONTRACTION |
| 8 | 0.53 | 0.8629 | CONTRACTION |
| 16 | 0.53 | 0.8621 | CONTRACTION |
| 32 | 0.53 | 0.8625 | CONTRACTION |
| 64 | 0.53 | 0.8626 | CONTRACTION |

**Optimal weights (M=8):**
- w(1 mod 8) = 0.669, w(3 mod 8) = 0.633, w(5 mod 8) = 0.366, w(7 mod 8) = 1.000

**Convergence of rho with N:**
- N=10K: 0.86129
- N=50K: 0.86336
- N=100K: 0.86332
- N=200K: 0.86384
- N=500K: 0.86380

The spectral radius **stabilizes** at ~0.8638, strongly suggesting convergence to a limit < 1.

**Corrected interpretation:** If the transition matrix entries converge to their limiting values, then the weighted model has average contraction. This is useful evidence, but it is not a pointwise contraction under the deterministic FMF map and does not prove Collatz.

### Theorem 18: Type-Dependent Self-Correction (explore18)

**Statement:** After high-t hops, the next hop is strongly biased toward Type A:

| Current state | P(Type A next) |
|--------------|----------------|
| B(t=1) | 51.4% |
| B(t=2) | 72.8% |
| B(t=3) | 54.9% |
| B(t=4) | 14.2% (anomalous) |
| B(t=5) | 63.0% |
| B(t=6) | 80.7% |
| B(t=9) | 86.9% |
| B(t=11) | 91.2% |

**However:** v_2(FMF) alone does NOT predict next type (~50/50 regardless). Growth magnitude also doesn't predict next hop. The self-correction is **type-dependent, not growth-dependent.**

The compensatory mechanism: high-t B hops produce outputs whose binary structure is biased toward Type A classification. This is a structural property of the 2-adic map, not a statistical artifact.

---

## 12. Results from explore19

### Theorem 19: Analytical Transition Matrix (explore19) -- AVERAGE CONTRACTION ONLY

**Statement:** The transition matrix T is rank-1 (all rows identical) because of state-independence (Theorem 12). Therefore:

**rho(T) = E[R^alpha]** (spectral radius = expected value of ratio^alpha)

The expected value decomposes exactly:

**E[R^alpha] = P(A) * E[R^alpha | A] + sum_{t>=0} P(B,t) * E[R^alpha | B(t)]**

where:
- P(A) = 1/2, P(B,t=j) = 1/2^(j+2)
- E[R^alpha | A] = E[(3k+1)^alpha / (4k+1)^alpha * (1/2^v)^alpha] where v = v_2(3k+1)
- E[R^alpha | B(t)] = E[((3^(t+2)*m-1) / (2^(t+2)*m-1))^alpha * (1/2^v)^alpha]

**Key insight:** For large x, the ratio (3k+1)/(4k+1) -> 3/4 and (3^(t+2)*m)/(2^(t+2)*m) -> (3/2)^(t+2). The v_2 distribution follows exact geometric P(v=j) = 1/2^j from Theorem 3.

**Results:**

| alpha | E[R^alpha | A] | E[R^alpha | B0] | E[R^alpha | B1] | E[R^alpha] (total) |
|-------|---------------|----------------|----------------|-------------------|
| 0.30 | 0.7723 | 0.8722 | 0.9851 | 0.8861 |
| 0.50 | 0.6698 | 0.8204 | 1.0048 | 0.8616 |
| 0.53 | 0.6567 | 0.8141 | 1.0094 | 0.8610 |
| 1.00 | 0.5000 | 0.7500 | 1.1251 | 0.9684 |

**Theoretical alpha* = 1 exactly** (where E[R^alpha] = 1). [Corrected July 2026: the earlier reported value 1.0002 was a truncation artifact of explore19.py's t<30 series cutoff. The exact series at alpha=1 evaluates to the rational identity M(1) = 1/4 + 3/16 + 9/16 = 1.]

At alpha = 0.53: theoretical rho = 0.8638, matching empirical value from explore17 to 4 significant figures.

**Corrected status:** This does **not** close the pointwise gap. The fractional-moment entries are determined by exact 2-adic density calculations, but they are still average statements over residue classes. They do not imply that every deterministic trajectory samples those residue classes with the required frequencies.

**Verified:** Theoretical predictions match empirical computations for N = 10K through 500K.

---

## 13. Final Gap Analysis (Updated)

### Gap Status After explore19

**Gap 1 (Independence/Mixing): RESOLVED by Rank-1 Structure**
The transition matrix is rank-1 (Theorem 12 + Theorem 19). This means rho(T) = E[R^alpha], which is a SCALAR quantity computed from the exact 2-adic distribution. No mixing or independence assumption is needed for the spectral radius -- it follows directly from the algebraic structure.

**Gap 2 (Cycle Exclusion): PARTIALLY RESOLVED**
If rho < 1 proves convergence to 0 in log-scale (which it does for an average trajectory), then no finite cycle exists because a cycle would require rho = 1. Combined with Theorem 13 (n > 10^8 for any cycle), this is very strong but technically the rank-1 spectral radius gives AVERAGE contraction, not pointwise.

**Gap 3 (Pointwise vs Average): THIS IS THE REMAINING GAP**
rho(T) < 1 proves that E[L(F(x))] < rho * L(x) ON AVERAGE over residue classes. But we need this for EVERY x, not just on average. The issue: some individual x values have F(x) > x (about 29% of hops grow). The weighted Lyapunov L(x) = x^0.53 * w(x mod M) can't be a pointwise supermartingale because F is deterministic.

**What would complete the proof:**
1. Show that for every x, there exists N(x) such that L(F^N(x)) < L(x) -- i.e., after some bounded number of hops, the Lyapunov function decreases
2. OR: Show that the self-correction mechanism (Theorem 18) guarantees that growth phases are always bounded and followed by sufficient shrinkage
3. OR: Prove a multi-step contraction: E[L(F^k(x))] < c^k * L(x) for some c < 1 and k large enough, with the expectation taken over the 2-adic distribution of intermediate m-values

---

## 14. Results from explore20-21

### Theorem 20: Multi-Step Contraction Fails (explore20) -- NEGATIVE RESULT

**Statement:** There is NO fixed k such that L(F^k(x))/L(x) < 1 for ALL odd x > 1.

For every k tested (1 through 20), there exist starting values x where the k-hop L-ratio exceeds 1. The worst cases are:
- k=1: worst ratio 17.9 (x=131071 = 2^17 - 1)
- k=5: worst ratio 42.5 (x=116507)
- k=20: worst ratio 66.3 (x=134379)

The fraction of x with ratio > 1 decreases with k (28.6% at k=1 -> 0.88% at k=20), but the worst-case value does not converge to below 1.

**Max consecutive growth hops:** 10 (in 3 out of 250,000 chains), showing growth phases are finite but can be long.

### Theorem 21: Unbounded Worst-Case Growth (explore21)

**Statement:** The worst-case single-hop L-ratio grows with bit-length and is unbounded:

| Bits | Max L-ratio | Worst x |
|------|-----------|---------|
| 9 | 3.2 | 511 |
| 13 | 7.6 | 8191 |
| 17 | 17.9 | 131071 |
| 21 | 42.2 | 2097151 |

Pattern: worst cases are 2^n - 1 (Mersenne-like numbers), which have t = n-2 and v_2 = 2, giving growth ratio ~ (3/2)^n / 4.

**Growth anatomy by (t, v_2):**
- Growth occurs when v_2 <= t+1 (roughly)
- For t=6, v_2=2: mean ratio = 12.8, max = 12.8
- Growth ratio ≈ (3/2)^(t+2) / 2^(v_2-1)

**Two-hop analysis:** After a growth hop, 33.6% of next hops also produce cumulative growth. But every tested number eventually L-descends: max hops to L-descent = 32, and 64% descend in 1 hop.

**Implication:** A pointwise Lyapunov argument is impossible -- individual growth hops are unbounded. Any proof must account for this by showing growth phases always terminate.

---

## 15. Updated Gap Analysis (After explore20-21)

### The Fundamental Challenge

**What is proven:**
1. Average contraction: rho = 0.8638 < 1 (Theorem 19) -- rigorously derived from exact 2-adic formulas
2. No non-trivial cycles exist with n < 10^8 odd steps (Theorem 13)
3. Drift is uniformly negative across all magnitudes (Theorem 10)
4. Growth phases are finite (max consecutive growth: 10 hops, Theorem 20)
5. Self-correction: high-t hops bias next hop toward Type A (Theorem 18)

**What is NOT proven:**
1. That growth phases terminate FOR EVERY starting point (only empirically verified)
2. That the trajectory reaches 1 (not just descends)

### New Proof Strategies

**Strategy E: Ergodic Theory Approach**
The FMF map is a measure-preserving transformation on the 2-adic integers. If the map is ergodic, then Birkhoff's theorem guarantees that time averages equal space averages. Since the space average gives E[log2(R)] = -0.83 < 0, almost every trajectory would converge. The remaining question: does "almost every" = "every"?

**Strategy F: Growth Phase Duration Bound**
Show that for x = 2^(t+2)*m - 1 with large t (the growth cases), the output F(x) has a SMALLER t-value with high probability. From Theorem 18: P(Type A next | B(t)) ~ 90% for large t. If t decreases by at least 1 on average each hop, growth phases have expected duration ~ t, and the total growth is bounded by sum of (3/2)^(t-j) terms = O((3/2)^t).

**Strategy G: Density-Zero Exception Sets**
Show that the set of x for which L(F^k(x)) > L(x) has density → 0 as k → ∞ (confirmed by explore20: 28.6% → 0.88%). If we can show the density approaches 0 AND the set has no "stable" members (every x eventually leaves the set), this proves convergence.

---

## 16. Results from explore22-23

### Theorem 22: Growth Phase Structure (explore22)

**Statement:** Growth phases (consecutive hops where F(x) > x) have:

| Duration | Frequency | Avg growth |
|----------|-----------|-----------|
| 1 hop | 66.4% | +0.79 bits |
| 2 hops | 12.2% | +1.49 bits |
| 3 hops | 20.7% | +2.39 bits |
| 4+ hops | 0.7% | +3-7 bits |

Maximum observed duration: 7 hops. Maximum total growth: 9.70 bits.

**Surprising finding:** Within growth phases, t-values tend to INCREASE (mean change +0.755, P(increase) = 0.585). Growth phases don't terminate because t decreases -- they terminate because eventually v_2(FMF) is large enough to produce a shrinkage hop despite the high t.

**Growth bounded by initial t:** For initial t-value t_0, the average growth is approximately (t_0+2) * 0.585 bits for single hops. Multi-hop phases can accumulate up to ~10 bits but this maximum appears stable across magnitudes.

### Theorem 23: 2^n - 1 Trajectories (explore23) -- STRUCTURAL RESULT

**Statement:** For x = 2^n - 1 (the hardest cases for single-hop growth):

1. **First hop type:** F(2^n - 1) is Type A in 21 out of 22 cases (n=3..24). This guarantees the SECOND hop is always a shrinkage.

2. **First hop ratio:** F(x)/x = (3^n - 1) / ((2^n - 1) * 2^{v_2(3^n-1)-1}). For n odd: v_2 = 2, ratio ≈ (3/2)^n / 2 (can be very large). For n even: v_2 = v_2(n) + 2, ratio is much smaller.

3. **Recovery time:** Net descent from start is achieved in:
   - 2^7 - 1: 3 hops
   - 2^10 - 1: 2 hops
   - 2^13 - 1: 8 hops
   - 2^17 - 1: 24 hops
   - 2^20 - 1: 12 hops
   Recovery takes approximately growth_bits / 0.83 hops (ratio of initial growth to average drift).

4. **Peak values:** Peak/start ratio grows with bit-length but average stays modest (~3-4x). Worst observed: x=159487 with peak/start = 13483x.

5. **Trajectory sharing:** Some 2^n - 1 trajectories pass through smaller 2^(m) - 1 values (e.g., 2^21-1 passes through 31 = 2^5-1).

**Key structural insight:** The reason F(2^n-1) is almost always Type A is that (3^n - 1) / 2^{v-1}, after division by LPT, tends to be ≡ 1 mod 4. This is because 3^n - 1 ≡ 2 mod 4 for all n, and the remaining even divisions keep the result in the ≡ 1 mod 4 class.

---

## 17. Synthesis: The Path to a Complete Proof

### What We Have

The FMF framework has established:

1. **Exact algebraic formulas** for FMF steps, values, and 2-adic structure (Theorems 1-4)
2. **State-independent transitions** proved algebraically (Theorem 12)
3. **Average contraction** rho = 0.8638 < 1, derived from exact 2-adic formulas (Theorem 19)
4. **No non-trivial cycles** for n < 10^8 (Theorem 13)
5. **Self-correction** mechanism: high-t -> Type A next (Theorem 18)
6. **Growth phases are short and bounded**: max 7 hops, max ~10 bits (Theorem 22)
7. **Hardest cases (2^n-1)**: first hop lands on Type A, recovery in O(n) hops (Theorem 23)

### The Remaining Gap

**Pointwise descent is NOT provable by Lyapunov functions** because individual hops can grow unboundedly (Theorem 21). Any proof must use a fundamentally different approach.

### Possible Closing Arguments

**Argument A: Probabilistic + Computational**
- Computationally verify Collatz for all x < X_0 (current: 2.95 * 10^20)
- For x > X_0: the trajectory enters [3, X_0] with probability > 1 - epsilon per hop sequence of length K
- Since K ~ log(x)/0.83, the probability of NEVER entering [3, X_0] is bounded by (1-epsilon)^{x/K} -> 0
- This gives "almost all" but not "all"

**Argument B: Growth Phase Dominance**
- Show that for ANY x, the growth phase from x has bounded duration D(x)
- After the growth phase, the trajectory is at x' < C * x for some constant C
- The average contraction then takes over: after O(log(C*x)/0.83) more hops, we reach x'' < x
- Iterate: each "epoch" (growth + recovery) takes O(log x) hops and brings us to a smaller value

**Argument C: Well-Ordering / Transfinite Induction**
- Define a well-ordering on odd numbers based on their FMF trajectories
- Show that each orbit is eventually well-ordered below the starting point
- This requires showing no infinite ascending chains exist

### Next Explorations

#### explore24: Epoch Analysis
- Define an "epoch" as: growth phase + recovery (until x' < x)
- For each starting x, measure: epoch duration, growth phase duration, recovery duration
- Is epoch duration bounded by C * log(x) for some constant C?

### Theorem 24: Epoch Duration Bound (explore24) -- STRONGEST EMPIRICAL RESULT

**Statement:** For every odd x in [3, 200000], the epoch (hops until trajectory drops below x) satisfies:

**epoch_duration(x) <= 3.15 * log2(x)**

with equality approached only at x = 27 (the famous hard case). For x > 1000, the bound tightens to ~1.90 * log2(x).

**Statistics:** 100% descent rate (99,999 / 99,999 numbers). Mean epoch = 1.74 hops. Max epoch = 32 hops. Distribution: 71.4% in 1 hop, 86.0% in ≤2, 91.2% in ≤3.

**Decomposition:** Each epoch splits into growth (mean 0.40, max 7 hops) and recovery (mean 1.33, max 31 hops). Recovery hops closely match theory: recovery ≈ peak_growth_bits / 0.83.

**Conditional implication:** If epoch_duration(x) <= C * log2(x) for all x, then:
1. Each epoch brings x to some x' < x
2. The next epoch has duration <= C * log2(x') < C * log2(x)
3. The total number of hops to reach 1 from x is at most sum_{i=0}^{x} C * log2(x - i), which is finite
4. Therefore every trajectory reaches 1

**What remains:** Proving the C * log2(x) bound for ALL x (not just x <= 200K). The bound appears to be getting TIGHTER as x grows (3.15 at x=27 -> ~1.9 for x > 1000), which suggests it holds universally.

---

## 18. Next Explorations

#### explore25: Large-x Epoch Duration
- Test the C * log2(x) bound for much larger numbers (x up to 10^8 or higher)
- Use targeted testing: focus on numbers with large t-values (the growth-prone ones)
- Check: does the ratio epoch_duration / log2(x) continue to decrease for larger x?

### Theorem 25: Universal Epoch Bound (explore25)

**Statement:** Across 2917 tests spanning 3 to 60 bits (including 2^n-1 for n up to 44, random numbers, and high-t numbers):

**epoch_duration(x) <= 2.83 * log2(x)** for all tested x

with the bound achieved only at x = 31. For x > 10000, the tighter bound ~1.63 * log2(x) holds.

**Key evidence:**
- 2^n - 1 for n = 3..44: all descend. Ratios range from 0.13 to 2.83, trending downward for large n
- Random 40-bit numbers: max epoch = 48, ratio = 1.20
- Random 60-bit numbers: max epoch = 8, ratio = 0.13
- High-t numbers (t up to 34): all descend. Worst ratio = 1.63 (x = 10485759)
- The ratio **decreases** with magnitude, suggesting the bound tightens for large x

**Theoretical argument for the bound:**
1. t ≤ log2(x) - 2 (structural constraint: x = 2^(t+2)*m - 1 ≥ 2^(t+2) - 1)
2. Max growth per hop ≤ (t+2) * 0.585 - 1 ≈ log2(x) * 0.585 bits
3. Growth phase max duration D (empirically ≤ 10, unknown if constant)
4. Recovery ≈ total_growth / 0.83 hops
5. If D is bounded: epoch ≤ D + D * log2(x) * 0.585 / 0.83 ≈ 0.7D * log2(x) for large x

---

## 19. Current Proof Status

### What Is Rigorously Proved

1. **FMF formulas** (Theorems 1-4): Exact, verified algebraically and computationally
2. **State-independence** (Theorem 12): Proved via 2-adic inverse structure
3. **Average contraction** (Theorem 19): rho = E[R^0.53] = 0.8638 < 1, from exact 2-adic formulas
4. **No small cycles** (Theorem 13): Any cycle needs n > 10^8 odd steps

### What Is Strongly Supported but Not Proved

5. **Epoch bound** (Theorems 24-25): epoch ≤ C * log2(x), confirmed up to 60-bit numbers
6. **Growth phase duration bounded** (Theorem 22): max 7-10 hops, needs proof
7. **Every trajectory reaches 1**: confirmed computationally to 2.95 * 10^20

### The Logical Gap

The proof chain would be:
- Average contraction + epoch bound => every trajectory descends
- Every trajectory descends + no cycles => every trajectory reaches 1

The epoch bound is the critical piece. If we could prove it, Collatz follows.

### Theorem 26: Cesaro Argument -- Partial Result (explore26)

**Statement:** The 2-adic Cesaro argument (equidistribution along orbits => time average = space average => convergence) has a fundamental limitation.

**What was tested:**
1. Equidistribution of F^n(x) mod 4 along trajectories
2. Asymptotic ratio R vs 3^s/2^d approximation error
3. Orbit residue coverage for mod 4, 8, 16, 32
4. Sum of error terms along trajectories
5. Product of ratios along trajectories

**Key findings:**

| Metric | Result | Needed |
|--------|--------|--------|
| Equidist mod 4 | ~50/50 but with deviations (x=127: 87.5% A) | Exact 50/50 |
| R vs 3^s/2^d error | 14-24% avg, 55% max | O(1/x) |
| Coverage mod 32 | 0.8% of trajectories | 100% |
| Error per hop | 0.27-0.32 bits | -> 0 |
| Avg log(R^alpha)/hop | -0.15 to -0.50 | -0.44 |

**Why the Cesaro argument fails:**
1. Trajectories are FINITE (they reach 1), so asymptotic equidistribution is irrelevant
2. The approximation R ≈ 3^s/2^d has O(1/x) error only for large x, and error per hop is ~0.3 even for x ~ 10^8
3. For finite trajectories, the sum of errors can exceed the sum of ideal contributions
4. Residue coverage for higher moduli is poor -- trajectories are too short

**What still works:**
- All product-of-ratios tests confirm convergence (product -> 0 in every case)
- Average drift per hop is consistently negative (-0.28 to -0.87 across all tests)
- The state-independence (Theorem 12) ensures TYPE sequence is effectively i.i.d.

**Implication:** The deterministic proof cannot rely on equidistribution/ergodic theory for finite trajectories. Need a different approach that works with finite-length sequences.

### Next Explorations

### Theorem 27: Growth Phase Mechanics (explore27) -- CRITICAL STRUCTURAL RESULT

**Statement:** Growth phases have rigid structural constraints:

**1. v_2 is overwhelmingly minimal during growth:**

| v_2 | P(v_2 \| growth) | P(v_2 \| all) |
|-----|-----------------|-------------|
| 2 | 0.878 | 0.476 |
| 3 | 0.115 | 0.248 |
| 4 | 0.005 | 0.175 |
| 5+ | 0.002 | 0.101 |

**2. m-values are restricted by residue class during growth:**

| State | Growth m-classes mod 8 | Excluded classes |
|-------|----------------------|-----------------|
| B(t=1) | m ≡ 1, 5 mod 8 | m ≡ 3, 7 (0% growth) |
| B(t=2) | m ≡ 3, 5, 7 mod 8 | m ≡ 1 (0% growth) |
| B(t=3) | m ≡ 1, 5, 7 mod 8 | m ≡ 3 (0% growth) |

**3. Universal growth chain:** ALL long growth phases (3+ hops) in [3, 500K] feed into the same m-value sequence: 11 → 13 → 11 → 111 → 21 → 35 → 5 → 57 → 144 → 108 → 81. This is the "27/31 chain."

**4. Conditional continuation probability:** P(continue | survived k hops) plateaus at ~0.75, giving geometric tail P(length >= k) ~ 0.75^k.

**5. v_2 values nearly independent:** Lag-1 correlation = 0.035 (all hops), -0.038 (growth hops). Joint distribution during consecutive growth dominated by (v_2=2, v_2=2) at 76%.

**KEY INSIGHT FOR PROOF:** Growth chains are constrained to hop between specific m-residue classes (depending on the type/t at each step). The allowed transitions form a FINITE AUTOMATON on states (type, t, m mod 2^K). If this automaton has no infinite paths (no growth-sustaining cycles), then growth phases must terminate.

### Theorem 28: Growth Automaton Has Phantom Cycles (explore28)

**Statement:** The finite automaton on states (t, m mod 2^K) has cycles with net growth, but these cycles are "phantoms" -- actual trajectories do not follow them.

**Growth-allowing m-classes by t:**

| t | P(growth) |
|---|-----------|
| 0 | 50% |
| 1 | 75% |
| 2 | 93.8% |
| 3 | 96.9% |
| 4 | 99.2% |
| 5+ | ~100% |

**Automaton cycles (K=8):** 8 cycles found, 7 with net growth (+0.17 to +1.68 bits/cycle).

**BUT: Actual trajectories disagree.** Cycle 3 (len=3, predicted +1.68 bits) gives -1.05 bits when tested with real numbers. The higher-order bits of m (beyond mod 2^K) determine the actual v_2, breaking the phantom cycle.

**Why mod-2^K is insufficient:** v_2(m - inv) depends on ALL bits of m, not just the lowest K. When m returns to the same residue class mod 2^K, the bits above position K are different, giving a different v_2 value.

**Max actual growth phase in [3, 500K]: 37 hops** (x=270271).

**Implication:** Local state analysis (m mod 2^K) cannot prove growth termination. The full m-value evolution has structure that prevents cycling, but this structure is not captured by finitely many residue classes.

#### The Path Forward

The remaining gap can potentially be closed by one of:

1. **m-value magnitude argument:** Show that m grows during growth phases, eventually becoming too large for the residue class to sustain growth (since higher bits disrupt the pattern)

2. **Probabilistic-to-deterministic bridge:** The average contraction rho = 0.8638 < 1 is PROVEN for every x (not just random x). Show that any trajectory spending C*log(x) hops must accumulate enough descent to overcome any bounded growth phase

3. **Computable verification + tail bound:** Verify up to X_0, then show for x > X_0 the drift dominates growth

### Theorem 29: m-Value Evolution (explore29)

**Statement:** The m-value (in x = 2^(t+2)*m - 1) evolves as follows:

| Context | E[log2(m'/m)] |
|---------|--------------|
| All hops | -0.72 to -0.80 |
| Growth hops (t=0) | -0.85 |
| Growth hops (t=2) | +1.97 |
| Growth hops (t=5) | +6.44 |
| Growth hops overall | +0.16 |

**m grows modestly during growth phases** (+0.16 bits/hop average), but **shrinks along full trajectories** (-0.80 bits/hop), tracking the overall drift closely.

**Critical finding:** ALL longest growth phases (37 hops, x=270271 and relatives) share the identical m-chain: 192410 → 108231 → 11415 → 16253 → 3332373 → ... This is a "universal growth attractor" -- many starting values feed into this single long chain.

**m magnitude during growth is bounded:** Max m during growth for N-bit starting values is approximately 2^{N+10}. The growth in m is proportional to the bit-length, not exponential.

**Descent fraction by hop count:**

| K hops | Fraction not descended |
|--------|----------------------|
| 1 | 28.6% |
| 2 | 14.0% |
| 5 | 4.2% |
| 10 | 0.95% |
| 20 | 0.058% |
| 50 | 0.000% |

Decay is exponential with base ~0.67: P(no descent by K) ≈ 0.29 * 0.67^K.

---

## 17. Key Insight Summary

The FMF framework transforms Collatz into a walk on log-scale with:
1. **Deterministic** step/value formulas (Theorems 1-3)
2. **State-independent** first-hop transitions (Theorem 12)
3. **Negative drift** mu = -0.83 (Theorem 10, uniform across magnitudes)
4. **Exponential tail bound** via Cramer: P(reach H) <= exp(-0.70*H) (Theorem 14)
5. **Critical exponent** alpha* = 1 exactly for E[R^alpha] = 1 (Theorem 19; corrected July 2026 from the truncated values 1.008 and 1.0002 — M(1) = 1/4 + 3/16 + 9/16 = 1 is an exact rational identity)
6. **Self-correcting** dynamics: high-t hops bias toward Type A next (Theorem 18)
7. **Known cycle lower bounds** making non-trivial cycles effectively impossible (Theorem 13)
8. **Spectral radius = E[R^alpha]** exactly, via rank-1 structure (Theorem 19)
9. **rho = 0.8638 < 1** at alpha = 0.53 -- average contraction proven analytically (Theorems 17, 19)

**Status:** Average contraction is PROVEN (rho < 1 follows from exact 2-adic formulas). The Cesaro/equidistribution approach FAILS for finite trajectories (Theorem 26). The remaining gap is **pointwise vs average**: showing that every individual trajectory eventually contracts. The most promising path: prove that growth phases must terminate (via 2-adic m-value evolution), which gives a deterministic epoch bound.

---

## 20. Literature Comparison and Critical Assessment

### Positioning Against Published Results

| Published Result | FMF Equivalent | Relationship |
|-----------------|----------------|--------------|
| Tao (2022): Almost all orbits attain almost bounded values (log density) | Theorems 24-25: epoch bound | Tao's result is STRONGER (rigorous "almost all") but WEAKER (log density, not "all") |
| Carletti & Fanelli (2017): Average contraction via Markov chain mod 8 | Theorem 19: rho = 0.8638 | Equivalent result, FMF route is more structured (mod 4 + exact formulas) |
| Krasikov & Lagarias (2003): Density reaching 1 >= x^0.84 | Not addressed | Their density result is rigorous; FMF doesn't improve on this |
| Kontorovich & Lagarias (2009): Stochastic models for 3x+1 and 5x+1 | Theorem 12: state-independence | Related -- both observe rapid mixing of residue classes |
| Barina (2025): Verified up to 2^71 ~ 2.36 x 10^21 | Theorem 25: tested to 60 bits | Barina's computational reach is much larger |
| Simons & de Weger (2005): No cycle with period < ~2.17 x 10^11 | Theorem 13: cited n > 10^8 | FMF understated the known bound |
| arXiv:2601.03297 (2025): Finitely many periodic orbits | Not addressed | Stronger than FMF cycle analysis |

### The 5n+1 Litmus Test

**Critical diagnostic:** The FMF structural arguments (state-independence, rank-1 transition matrix, epoch analysis) do NOT use the specific value 3 in any essential way beyond determining the sign of the drift. For the 5n+1 problem (which has divergent orbits), the analogous framework would produce:
- State-independence: still holds (same 2-adic argument)
- Rank-1 transition matrix: still holds
- Drift: POSITIVE (log2(5/2) > 1), so rho > 1

The structural arguments cannot distinguish 3n+1 from 5n+1 -- only the drift sign differs. **Any proof via FMF must find a mechanism specific to the constant 3.**

### Tao's Fundamental Barrier

Tao (2011) argues: "any proof of the Collatz conjecture must either use existing results in transcendence theory, or contribute new methods to transcendence theory." The core difficulty is the separation of powers of 2 and 3. The FMF framework's 2-adic analysis operates at a level that doesn't engage with this barrier.

Additionally: "unless a dynamical system is somehow polynomial, nilpotent, or unipotent in nature, the current state of ergodic theory is usually only able to say something meaningful about generic orbits, but not about all orbits."

### Theorem Classification

Items that are rigorously proved:
- Theorems 1-4: Algebraic identities (FMF formulas)
- Theorem 12: State-independence (2-adic argument)
- Theorem 19: rho = E[R^alpha] via rank-1 structure (follows from Theorem 12)

Items that are empirical observations (should be labeled "Conjecture" or "Observation"):
- Theorems 9, 11, 22-27: Empirical, not proved
- Theorems 14, 15: Apply known techniques (Cramer, supermartingale) under i.i.d. assumption that isn't justified

### Updated Facts
- Computational verification: 2^71 ~ 2.36 x 10^21 (Barina, J. Supercomputing, 2025)
- Cycle lower bound: period > ~2.17 x 10^11 (Simons & de Weger, 2005)
- Epoch bound is a REFORMULATION of the conjecture, not a reduction

---

## 21. New Proof Directions

### Theorem 30: The 3/4 Discriminant (explore30) -- STRUCTURAL RESULT

**Statement:** For the generalized map C_a(x) = ax+1 (a odd), the FMF structure depends critically on whether a < 4:

**For a = 3 (3n+1):**
- Type A (x ≡ 1 mod 4): 3(4k+1)+1 = 4(3k+1). Immediate FMF. Ratio = (3k+1)/(4k+1) < 3/4. **ALWAYS SHRINKS.**
- Type B (x ≡ 3 mod 4): Delayed FMF (3+2t steps). Growth ~ 3^(t+2)/2^d. Can grow.
- **50% of hops guaranteed to shrink (pointwise, deterministic).**

**For a = 5 (5n+1):**
- Type A (x ≡ 1 mod 4): 5(4k+1)+1 = 2(10k+3). NOT immediate FMF. Requires s ≥ 2 multiplications by 5, giving growth ~ 5^s/2^v >> 1. **ALWAYS GROWS (P(shrink) = 0.0000).**
- Type B (x ≡ 3 mod 4): 5(4k+3)+1 = 4(5k+4). Immediate FMF. Ratio = (5k+4)/(4k+3) > 5/4. **ALWAYS GROWS.**
- **Neither channel guarantees shrinkage.**

**The mechanism:** The immediate FMF channel gives ratio a/4. For a = 3: 3/4 < 1 (contraction). For a ≥ 5: a/4 > 1 (expansion). **3 is the largest odd integer less than 4.** This is what makes 3n+1 special.

**State-independence holds for both:** P(Type A output) = P(Type B output) = 1/2, verified for both 3n+1 and 5n+1. v_2 distribution is geometric for both. The structural arguments are identical except for the drift sign.

**Drift decomposition:**

| Map | E[log2(R)\|Type A] | E[log2(R)\|Type B] | Overall E[log2(R)] |
|-----|-------------------|-------------------|-------------------|
| 3n+1 | -1.415 (always <0) | -0.245 | -0.830 |
| 5n+1 | +1.322 (always >0) | -0.678 | +0.322 |

**The 3/4 channel gives 3n+1 a pointwise contraction guarantee that 5n+1 lacks.** Any proof of Collatz must exploit this specific mechanism.

### Direction A: 5n+1 Discriminant -- COMPLETED (Theorem 30)

### Theorem 31: Inverse Movement Rate (explore31) -- PROVED

**Statement:** For a odd, the 2-adic inverse of a^(t+2) moves at a fixed rate:

**v_2(a^{-(t+3)} - a^{-(t+2)}) = v_2(1-a) for all t >= 0.**

- For a = 3: v_2(1-3) = v_2(-2) = **1** (minimum possible nonzero shift)
- For a = 5: v_2(1-5) = v_2(-4) = **2**
- For a = 7: v_2(1-7) = v_2(-6) = **1**

**Proof:** a^{-(t+3)} - a^{-(t+2)} = a^{-(t+2)} * (a^{-1} - 1) in Z_2. Since a is odd, v_2(a^{-(t+2)}) = 0. And v_2(a^{-1} - 1) = v_2((1-a)/a) = v_2(1-a) + v_2(a^{-1}) = v_2(1-a) + 0 = v_2(1-a). QED.

### Theorem 32: Proximity Dynamics (explore31) -- STRUCTURAL RESULT

**Statement:** Define proximity p_n = v_2(m_n - inv_{t_n}) where inv_t = (3^(t+2))^{-1} mod 2^K. Along FMF trajectories:

**1. Growth requires low proximity:**

| p | P(p | growth) | P(p | shrinkage) |
|---|---------------|-----------------|
| 1 | 0.792 | 0.000 |
| 2 | 0.197 | 0.221 |
| 3 | 0.008 | 0.370 |
| 4 | 0.003 | 0.295 |
| 5+ | 0.000 | 0.115 |

Growth hops are concentrated at p=1 (m is 2-adically close to the inverse). Shrinkage hops require p >= 2, with the bulk at p=3-4.

**2. Low autocorrelation:** Lag-1 correlation of proximity = 0.20. The proximity sequence effectively forgets its state after 1-2 steps.

**3. Transition matrix P(p_{n+1} | p_n) for consecutive Type B hops:**

| p_n \ p_{n+1} | 1 | 2 | 3 | 4+ |
|---------------|-------|-------|-------|-------|
| 1 | 0.713 | 0.137 | 0.081 | 0.069 |
| 2 | 0.219 | 0.088 | 0.660 | 0.034 |
| 3 | 0.597 | 0.226 | 0.090 | 0.087 |

From p=1 (growth-sustaining): 71.3% stay at p=1, but 28.7% escape per hop. This gives expected growth run at p=1 of ~3.5 consecutive hops before escaping.

From p=2: 66% jump to p=3 (shrinkage territory). No growth-sustaining absorbing state exists.

**4. Equidistribution:** ord(3) = ord(5) = 2^(k-2) mod 2^k. Both cover exactly 50% of odd residues. Equidistribution alone does NOT distinguish 3n+1 from 5n+1.

**Implications for proof:** The proximity analysis shows that growth requires m to be 2-adically close to inv_t (within 1 bit). The low autocorrelation means this closeness is not self-sustaining. Combined with Theorem 30 (50% of hops are Type A, which bypass proximity entirely and always shrink), sustained growth requires both: (a) repeatedly landing on Type B (probability 1/2 each hop, independent), AND (b) having p=1 each time (probability ~0.5 conditional on Type B). The combined probability of k consecutive growth hops is thus ~(1/4)^k, giving exponential decay.

### Direction B: 2-Adic Proximity Chains -- COMPLETED (Theorems 31-32)

**Remaining open question:** Does the 1-bit inverse shift for a=3 (Theorem 31), combined with the m-value transformation, rigorously guarantee that proximity p_n cannot stay at 1 indefinitely? The empirical evidence (autocorrelation 0.20, escape probability 0.287 per hop) strongly suggests yes, but a rigorous proof requires understanding how m evolves jointly with inv_t.

### Theorem 33: Mixed-Metric Height Function (explore32) -- STRUCTURAL RESULT

**Statement:** Define h(m, t, p) = alpha*log2(m) + gamma*t - beta*p where p = v_2(m - 3^{-(t+2)}).

**Optimal parameters:** alpha = 1.0, gamma = 2.1, beta = 0.1.

**Results:**

| Metric | Violation rate | Mean delta_h |
|--------|---------------|-------------|
| Pure log2(m) | 29.24% | -0.632 |
| Mixed h (optimal) | 23.31% | -0.678 |

**The mixed metric distinguishes 3n+1 from 5n+1:**

| Map | Mean delta_h | Violation rate |
|-----|-------------|---------------|
| 3n+1 | -0.678 | 23.3% |
| 5n+1 | +0.327 | 54.2% |

This is significant: the same height function DECREASES on average for 3n+1 and INCREASES on average for 5n+1. The 2-adic proximity term (beta=0.1) contributes marginally; the dominant factor is the t-penalty (gamma=2.1).

**Single-hop obstruction:** No height function h(m,t,p) can achieve zero single-hop violations. For Type B with large t and v_2 = 2, the growth is (3/2)^(t+2)/4, which is unbounded.

**Multi-step decay:**

| k hops | Violation rate |
|--------|---------------|
| 1 | 25.7% |
| 2 | 20.6% |
| 3 | 17.8% |
| 5 | 12.1% |
| 10 | 6.3% |

Violations decay approximately as ~0.86^k (consistent with rho = 0.8638).

**Growth vs proximity tradeoff:** For growth hops at t >= 2, delta_p has mixed sign (sometimes positive, sometimes negative). The correlation between delta_log_m and delta_p is weak, meaning the proximity dimension provides partially independent information but not enough to fully compensate.

**Proof implication:** A single-hop pointwise Lyapunov proof is rigorously impossible. The path forward requires either (a) multi-step contraction bounds with effective error terms, or (b) a qualitatively different approach that doesn't rely on per-hop decrease.

### Direction C: Mixed-Metric Height Function -- COMPLETED (Theorem 33)

The mixed metric confirms that 2-adic proximity is proof-relevant and structurally distinguishes 3n+1 from 5n+1, but cannot close the pointwise gap on single hops.

### Theorem 34: Carry Propagation (explore33) -- NEGATIVE RESULT

**Statement:** No simple combinatorial function of the binary structure of m monotonically decreases along FMF trajectories.

**Tested candidates:**

| Invariant | P(decrease) | P(increase) | Net bias |
|-----------|-------------|-------------|----------|
| popcount(m) | 47.6% | 28.6% | +19.0% |
| ones_runs(m) | 32.3% | 22.5% | +9.8% |
| carry_count(m,2m) | 46.2% | 37.9% | +8.4% |
| carry_chain(m,2m) | 45.5% | 38.2% | +7.3% |
| popcount(m)*t | 49.2% | 35.5% | +13.7% |
| log2(m)/(p+1) | 53.5% | 46.5% | +6.9% |

All show a bias toward decrease (consistent with overall contraction) but none are monotone.

**Carry structure difference (growth vs shrinkage):**
- Growth hops: avg 2.3 carries, avg max chain 2.0
- Shrinkage hops: avg 4.2 carries, avg max chain 3.6
- Growth requires simpler binary structure (fewer carries).

**2-adic periodicity:** 3^{-n} mod 2^K has period-2 pattern in lowest bits (...010101). 5^{-n} has period-4 (...11001100). The bit density of a^{-n} in Z/2^K Z is ~0.48 for both.

**Conclusion:** The carry structure is a consequence of the 2-adic structure (Theorems 3, 31), not an independent proof tool. The ratio a/4 (Theorem 30) remains the primary structural discriminant.

### Direction D: Carry Propagation Analysis -- COMPLETED (Theorem 34, negative result)

### Theorem 35: Growth-to-Type-A Structural Split (explore34) -- PROVED

**Statement:** For a Type B FMF hop with v_2(FMF) = 2 (the dominant growth mode, 87.9% of growth hops), the output type is EXACTLY 50/50 Type A vs Type B, determined by m mod 8.

**Proof:** v_2(FMF) = 2 requires v_2(3^(t+2)*m - 1) = 1, i.e., 3^(t+2)*m ≡ 3 mod 4. The output F(x) = (3^(t+2)*m - 1)/2 has type determined by F(x) mod 4 = ((3^(t+2)*m - 1)/2) mod 4.

For each t, 3^(t+2) mod 8 is either 1 (t even) or 3 (t odd). The growth+output analysis mod 8:

| t parity | 3^(t+2) mod 8 | Growth -> A | Growth -> B |
|----------|---------------|-------------|-------------|
| even | 1 | m ≡ 3 mod 8 | m ≡ 7 mod 8 |
| odd | 3 | m ≡ 1 mod 8 | m ≡ 5 mod 8 |

In each case: exactly 1 of 4 odd residue classes mod 8 gives growth+A, exactly 1 gives growth+B, and 2 give no growth (higher v_2). The A/B split is 50/50. QED.

**Growth chain statistics:**
- P(growth continues | in growth chain) = 0.356
- Expected chain length = 1.55
- Max observed chain = 7 (in [3, 500K])
- P(chain >= k) ~ 0.36^k (exponential decay)

**Type A output frequency along trajectories:**
- Mean gap between Type A outputs: 1.84 hops
- Max gap: 15 hops
- P(gap = 1): 58.2%, P(gap <= 3): 88.2%

**Corollary (Theorem 35a):** For v_2 = 2 growth hops, a growth chain of length k requires the m-values at each step to lie in the specific B-producing residue class mod 8 (which depends on t at that step). Since t changes along the chain, the constraint on m mod 8 alternates between m ≡ 7 (t even) and m ≡ 5 (t odd). This is NOT self-sustaining: the m-transformation maps m ≡ 7 mod 8 to a new m' whose mod 8 class is determined by higher bits of m.

### Direction E: Effective Equidistribution Bounds

Use exponential sum / Gauss sum techniques to bound the equidistribution rate of 3^n mod 2^k. If equidistribution is fast enough relative to how m evolves, it bounds how long "bad" m-values (those close to the 2-adic inverse) can persist along a chain. This connects FMF to established analytic number theory.

### Theorem 36: Growth-B Acyclicity (explore35) -- PROVED for K <= 8

**2026 status note:** This finite-truncation statement is superseded by the cleaner exact lemma in `paper/sections/05-quartering-law.typ`: a cycle made entirely of growth-B hops is impossible because each growth-B hop strictly increases the odd value. The finite residue-graph computations are therefore only exploratory evidence about escape rates. They are not needed for acyclicity, and they do not address the real remaining obstruction: an infinite nonperiodic growth-B path in positive integers.

**Statement:** The growth-B transition map on the state space (t, m mod 2^K) has NO CYCLES for K = 4, 6, 8.

**The explicit map:** For a Type B hop with v_2(FMF) = 2 and output Type B:
- m' = odd_part((3^(t+2)*m + 1) / 8)
- t' = v_2((3^(t+2)*m + 1) / 8)

**Results:**

| K | Growth-B states | Cycles | States escaping |
|---|----------------|--------|-----------------|
| 4 | 8 | 0 | 87.5% |
| 6 | 48 | 0 | 79.2% |
| 8 | 256 | 0 | 75.8% |

**Why no cycles (algebraic argument):** For a cycle of length k to exist in the exact m-transformation, we'd need the product of ratios to equal 1:
- Product = prod_{i=1}^k (3^(t_i+2) / 2^(t'_i+3)) = 1
- This requires 3^(sum(t_i+2)) = 2^(sum(t'_i+3))
- But 3^a = 2^b has no solution for positive integers a, b (fundamental theorem of arithmetic)
- Therefore no exact cycle exists in (m, t) space. QED.

**Escape reasons from growth-B (mod 2^8):**
- Output Type A: 25.8% (guaranteed shrinkage)
- Higher v_2 (> 2): 49.2% (extra shrinkage)
- Stays in growth-B: 24.2%

**t-value dynamics in growth-B chains:**
- t = 0 -> t' = 1 (74%), t' = 0 (16%)
- t = 1 -> t' = 0 (91%)
- t values oscillate, never grow unbounded

**Proof outline for growth termination:**
1. An infinite growth chain requires all hops to be Type B (Theorem 30)
2. Growth-B requires m in specific residue class mod 8 (depends on t)
3. No cycle exists in (t, m mod 2^K) for any K (Theorem 36 + Theorem 28)
4. m grows during growth-B chains (m'/m >= 9/8 for t=0)
5. *Gap:* need to show that carry propagation from growing m disrupts the mod-2^K pattern, forcing escape from growth-B states

### Theorem 37: Equidistribution and Orbit Bounds (explore36) -- PROVED

**Statement:** (a) For K >= 3, ord(3, 2^K) = 2^(K-2), confirmed for K = 3..15. (b) Growth-B orbits in the (t, m mod 2^K) state space have length at most 3-4 steps for K up to 12. (c) Growth chain length / log2(m) is a DECREASING function of m: from ~2.0 at small m to ~0.1 at large m (verified up to m ~ 10^6). (d) The 2-adic contraction approach FAILS: v_2(F(x) - 1) does not increase on average along FMF trajectories.

**Key result (c):** The ratio max_chain / log2(m) empirically satisfies:

| log2(m) range | max chain | ratio |
|---------------|-----------|-------|
| 1-5 | 7 | ~2.0 |
| 10-15 | 7 | ~0.5 |
| 15-20 | 10 | ~0.5 |

**Significance:** Growth chains get proportionally SHORTER for larger m. This is consistent with the density decay of the compatibility tree (Theorem 38), but the pointwise bound is not yet proved.

**On 2-adic contraction (d):** Mean change in v_2(F(x) - 1) is negative (-0.178), so the FMF map does NOT contract toward 1 in the 2-adic metric. This rules out a direct 2-adic contraction proof.

---

### Theorem 38: Compatibility Tree Density Decay (explore37) -- PROVED

**Statement:** Let G_k(K) = {m mod 2^K : m odd, generates a growth-B chain of length >= k starting at t=0}. Then:
1. |G_k(K)| / (2^(K-1)) decays GEOMETRICALLY with k at rate ~1/4 per step.
2. For ALL K tested (8, 10, 12, 14, 16), G_k(K) eventually becomes empty (all chains terminate mod 2^K).
3. The per-step continuation probability is P(continue) ~ 0.25, not 0.50.

**Exact density measurements (mod 2^K):**

| k | K=10 | K=12 | K=14 | K=16 |
|---|------|------|------|------|
| 1 | 0.2500 | 0.2500 | 0.2500 | 0.2500 |
| 2 | 0.0605 | 0.0625 | 0.0624 | 0.0625 |
| 3 | 0.0156 | 0.0151 | 0.0155 | 0.0155 |
| 4 | 0.0020 | 0.0044 | 0.0042 | 0.0039 |
| 5 | 0 | 0.0005 | 0.0012 | 0.0009 |
| 6 | | 0.0005 | 0.0005 | 0.0002 |
| 7 | | 0 | 0.0001 | 0.00003 |

**Per-step ratios converge to ~0.25:**
- Step 1→2: 0.250
- Step 2→3: 0.249
- Step 3→4: 0.252
- Step 4→5: 0.242
- Higher steps: fluctuate but stay well below 0.5

**Why 1/4 (not 1/2):** The continuation probability decomposes as:
- P(output Type B | growth-B) = 1/2 (Theorem 35)
- P(output is growth-B | output Type B) ~ 1/2 (from v_2 distribution)
- P(continue) = P(Type B) * P(growth-B | Type B) ~ 1/4

**Compatibility tree terminates for all K:**

| K | Max chain length mod 2^K |
|---|--------------------------|
| 8 | 3 |
| 10 | 5 |
| 12 | 6 |
| 14 | 8 |
| 16 | 11 |

Max chain length grows as ~K/2, consistent with the density (1/4)^k requiring k <= K/2 for non-empty compatible sets.

**Proof attempt for growth termination (Lemma G):**
1. Step 1 (Mod-8 halving): Theorem 35 gives exact 50/50 A/B split (PROVED).
2. Step 2: Bit consumption per step: m' mod 2^j requires ~(j+8) bits of m (COMPUTED).
3. Step 3: Density of k-step compatible sets decays as (1/4)^k (VERIFIED to K=16).
4. Step 4: For a specific integer m with K bits, chain length <= K/2 = O(log m).
5. **Gap**: Need to prove Step 3 algebraically (currently empirical for k > 3).

**Lemma G gap: CLOSED by Theorem 40.**
P(continue | growth-B) = 1/4 is proved algebraically via the Odd Part Equidistribution Lemma (explore39). The decomposition: P(v_2=2) = 1/2 (geometric distribution, since 3^(t+2) is a unit) times P(Type B | v_2=2) = 1/2 (Type Independence Lemma) = 1/4.

---

### Theorem 39: The Quartering Law (explore38) -- PROVED

**Statement:** P(output is growth-B | input is growth-B) = 1/4 exactly in the limit K -> infinity.

**Decomposition:**
- P(v_2 = 2 at output) = 1/2: Among all odd m', exactly half satisfy 3^(t'+2)*m' ≡ 3 mod 4 (which gives v_2(FMF) = 2).
- P(Type B output | v_2 = 2) = 1/2: Of those with v_2=2, exactly half have output Type B (Theorem 35).
- Combined: P(growth-B output) = 1/2 * 1/2 = 1/4.

**Verification (convergence to 1/4):**

| K | P(continue) |
|---|-------------|
| 4 | 0.1250 |
| 8 | 0.2422 |
| 12 | 0.2502 |
| 16 | 0.2500 |
| 18 | 0.2500 |
| 24 | 0.2500 |

**Equidistribution of m' mod 8:** From growth-B inputs, m' is equidistributed among {1, 3, 5, 7} mod 8 (each gets 25.0% at K >= 16). This follows from the affine structure of the growth-B map: m -> (3^(t+2)*m + 1)/8 is an affine map on Z/2^K Z, and since 3^(t+2) is a unit mod 2^K, the map permutes residue classes uniformly.

**Mod-8 transition table (algebraic):** Among the 16 growth-B states (t, m mod 8) for t = 0..15, exactly 4 have outputs that are also growth-B:
- (t=2, m≡7) → (t'=0, m'≡7): CONTINUES
- (t=5, m≡5) → (t'=0, m'≡7): CONTINUES
- (t=12, m≡7) → (t'=1, m'≡5): CONTINUES
- (t=15, m≡5) → (t'=1, m'≡5): CONTINUES

This gives 4/16 = 1/4 EXACTLY.

**Corollary (Growth Chain Bound):** P(growth chain of length >= k) <= (1/4)^k. For an integer m with K = ceil(log2(m)) bits, chain length <= K/2 = log2(m)/2 + O(1).

**The algebraic argument for equidistribution:**
1. For fixed t, the map m -> 3^(t+2)*m is a permutation of odd residues mod 2^K (since 3^(t+2) is a 2-adic unit).
2. Adding 1 is a translation (preserves Haar measure on Z_2).
3. Dividing by 8 and taking odd_part extracts bits in a measure-preserving way.
4. Therefore m' mod 8 is equidistributed when m ranges over any fixed residue class mod 8.
5. Since growth-B selects 1 of 4 odd residues mod 8 (for each t'), P(output is growth-B) = 1/4.

**Remaining formalization:** The measure-preservation argument in step 3 needs to account for the t'-dependent extraction (odd_part removes different numbers of 2-factors depending on the specific m). This is the final gap.

---

### Theorem 40: The Quartering Law -- Complete Algebraic Proof (explore39) -- PROVED

**Statement:** For the growth-B map m -> m' = odd_part((3^(t+2)*m + 1)/8), the probability that the output state is growth-B is exactly 1/4. Consequently, P(growth chain of length >= k) <= (1/4)^k.

**Complete Proof:**

**Lemma (v_2 Geometric Distribution):** For odd m uniform mod 2^K, v_2(3^(t+2)*m - 1) follows exact geometric with P(v_2 = j) = 1/2^j.

*Proof:* 3^(t+2) is a unit mod 2^K (since gcd(3,2)=1). So m -> 3^(t+2)*m is a bijection on odd residues. Thus 3^(t+2)*m - 1 is uniform over even residues mod 2^K. Among even numbers mod 2^K, exactly 1/2^j have v_2 = j. QED

**Lemma (Type Independence):** P(Type B | v_2(FMF) = v) = 1/2 for any v >= 2.

*Proof:* Write 3^(t+2)*m - 1 = 2^w * q with q odd. Output type depends on q mod 4. Since 3^(t+2)*m - 1 is uniform mod 2^{w+2}, and the residues with v_2 = w are {2^w, 3·2^w} (giving q ≡ 1, 3 mod 4 respectively), both are equally likely. QED

**Lemma (Odd Part Equidistribution):** If q is uniform over integers mod 2^N, then odd_part(q) mod 2^j is equidistributed over odd residues for j <= N - v_2(q).

*Proof:* Fix s = v_2(q). Among {0,...,2^N-1} with v_2 = s, the values are {2^s * r : r odd, r < 2^{N-s}}. There are 2^{N-s-1} such values, and r takes each odd value mod 2^{N-s} exactly once. QED

**Main Proof (Theorem 40):**

Step 1: 3^(t+2)*m + 1 ≡ 0 mod 8 (from growth-B: 3^(t+2)*m ≡ 7 mod 8).

Step 2: q = (3^(t+2)*m + 1)/8 is uniform mod 2^{K-3} as m ranges over growth-B class (since 3^(t+2) is a unit, the multiplication is a bijection, and /8 preserves uniformity).

Step 3: m' = odd_part(q) has m' mod 8 equidistributed over {1,3,5,7} (by Odd Part Equidistribution Lemma applied to q with N = K-3).

Step 4: Growth-B at next step requires 3^(t'+2)*m' ≡ 7 mod 8. Since 3^(t'+2) mod 8 ∈ {1, 3}, this selects exactly 1 of 4 odd residues mod 8. By Step 3, P = 1/4. QED

**Verification (exact results):**

| Property | Expected | Observed (K=16) |
|----------|----------|-----------------|
| m' ≡ 1 mod 8 | 0.2500 | 0.2500 |
| m' ≡ 3 mod 8 | 0.2500 | 0.2500 |
| m' ≡ 5 mod 8 | 0.2500 | 0.2500 |
| m' ≡ 7 mod 8 | 0.2500 | 0.2500 |
| P(v_2=2 next hop) | 0.5000 | 0.4999 |
| P(continue growth-B) | 0.2500 | 0.2499 |
| P(Type B | v_2=w) | 0.5000 | 0.5000 |

All equidistribution results are EXACT (verified at K=8,12,16,20,24).

**Corollary (Lemma G -- Growth Termination):** Every growth chain has finite length, bounded by O(log x). Proof: P(chain >= k) = (1/4)^k (by state-independence, Theorem 12, each step's continuation is independent). For m with K = ceil(log2(m)) bits, k > K/2 gives (1/4)^k < 2^{-K} < 1/m.

**Proof dependencies (all algebraic):**
1. gcd(3, 2) = 1, so 3^(t+2) is a unit mod 2^K [trivial]
2. Unit multiplication permutes residues mod 2^K [ring theory]
3. Odd Part Equidistribution [counting argument]
4. Growth-B selects 1 of 4 odd residues mod 8 [arithmetic]

---

### Lemma G Status: PROVED for almost all integers (Theorem 40); NOT proved for ALL integers

**What is proved (algebraic):**
- P(continue growth-B) = 1/4 exactly (Theorem 40)
- Density of chain ≥ k among odd residues mod 2^K is (1/4)^k exactly
- For B-bit integers: count with chain ≥ k is 2^{B-1} × (1/4)^k = 2^{B-1-2k}
- For k > (B-1)/2: count < 1, so NO B-bit integer has chain ≥ k

**The gap (same as Tao's barrier):**
The counting argument assumes the mod-2^B analysis tracks the full chain. But each growth-B step consumes ~3-4 bits of precision (carry depth). After ~B/3 steps, the mod-2^B analysis runs out of resolution. The density bound gives termination within ~B/2 steps, but tracking only reaches ~B/3 steps. This gap cannot be closed by taking larger K.

Density → 0 does NOT imply the set is empty for specific integers. (Analogy: primes have density 0 but infinitely many exist.) The intersection ∩_k {m : chain(m) ≥ k} has Haar measure 0 in Z_2, but measure-zero sets can contain positive integers.

**Current correction:** The `(1/4)^k` exponential density decay is a sharp
natural-density statement for the strict growth-B event. It should not be
presented as directly stronger than Tao's theorem, because Tao controls orbit
minima while this log controls one isolated growth mechanism. The "almost all
to all" barrier remains.

---

### Theorem 41: Bit Consumption and Growth Chain Length (explore41)

**Statement:** The growth-B map m → m' = odd_part((3^(t+2)*m+1)/8) has:

1. **Carry depth:** m' mod 2^j is determined by m mod 2^{j+C} where C is constant per t (C=14 for t=0, C=18 for t=1, C=15 for t=2). Average bit consumption = 4.0 bits/step. Net consumption after growth: 3.83 bits/step.

2. **Orbit bound (empirical):** Growth-B orbit length mod 2^K is at most ~0.55K. The ratio max_orbit/K converges downward (0.60 at K=10 → 0.35 at K=20).

3. **Chain length bound (empirical):** 0 violations of chain ≤ 0.55·log2(m)+3 in 1.5M tests. Max chain/log2(m) = 1.29. Average chain length ~1.33, stable across bit sizes 5-29.

4. **Formal bound attempt:** For the chain to continue k steps, m_0 must lie in a residue class mod 2^{3+kB} of density (1/4)^k. Adjusting for growth: bound = log2(m_0)/(2-0.17) ≈ 0.55·log2(m_0).

**Gap:** The density argument proves the bound for ALMOST ALL integers (density 1), but the precision-tracking limitation (each step consumes ~3-4 bits, so mod-2^B analysis exhausts after ~B/3 steps while the density bound needs ~B/2 steps) prevents a pointwise proof for EVERY integer.

---

### Direction F: m-Transformation Ergodicity -- COMPLETED (Theorems 36-41)

The compatibility tree (Theorem 38) provides the strongest evidence yet for growth termination. Key advances:
1. Acyclicity in finite state spaces (Theorem 36) ✓
2. Density decay at rate ~(1/4)^k (Theorem 38) ✓
3. Orbit bounds decrease with m-magnitude (Theorem 37) ✓
4. Max chain / log2(m) bounded by ~0.5 for large m (empirical) ✓

The (1/4)^k density decay is now proved algebraically (Theorem 40). The
equidistribution chain is: unit multiplication -> q uniform -> odd part
equidistribution -> m' mod 8 uniform -> growth-B selects 1/4. Later audit
clarified that this is a natural-density cylinder calculation, not independence
along each deterministic trajectory. Theorem 41 adds the bit consumption
analysis: 4.0 bits consumed per step, net 3.83 after growth. The chain length
bound 0.55·log2(m) holds empirically with 0 violations in 1.5M tests.

**Status correction:** Lemma G is a density statement, not a theorem for every
integer. The gap is the same "almost all to all" barrier that appears throughout
Collatz work. The FMF decay rate applies to a narrower growth-chain event and is
not directly comparable to Tao's orbit-minimum theorem.

---

### Theorem 42: Non-Ergodicity of FMF Map mod 2^K (explore42)

**Statement:** The FMF map on odd residues mod 2^K is NOT ergodic for any K ≥ 4.

**Evidence:**
- The map is not injective (~half of nodes have in-degree 0)
- Almost all strongly connected components are singletons (size 1)
- Attracting set fraction: 12.5% (K=4) → 0.05% (K=12)
- TV distance to uniform stays near 1.0 and worsens with K
- Max fraction of states visited by any orbit: 62.5% (K=4) → 1.6% (K=12)

**Key observation:** Actual trajectories of large integers visit far more residues mod 2^K than the mod-2^K orbit predicts. This is because high bits change at every step, jumping between branches. The equidistribution in real trajectories is driven by the changing magnitude of the number, not by ergodicity of a fixed-modulus map.

**Consequence:** Ergodicity-based approaches cannot close the "almost all → all" gap.

---

### Theorem 43: 2-adic Expansion of Growth-B Map (explore43)

**Statement:** The growth-B map m → m' = odd_part((3^{t+2}m+1)/8) is 2-adically expanding with factor exactly 2^{3+t'} per step, where t' = v_2((3^{t+2}m+1)/8).

**Proof sketch:** For m_1, m_2 both in the growth-B domain with the same output valuation t':
- (3^{t+2}m_1 + 1) - (3^{t+2}m_2 + 1) = 3^{t+2}(m_1 - m_2)
- |3^{t+2}|_2 = 1 (unit), so |difference|_2 = |m_1 - m_2|_2
- Division by 2^{3+t'} gives |m'_1 - m'_2|_2 = 2^{3+t'} · |m_1 - m_2|_2

Minimum expansion: 8 (when t'=0). Average expansion: ~16 (since E[t']=1).

**Consequences:**
1. **Explains the Quartering Law:** Expansion scrambles low bits → equidistribution mod 2^k → each step's growth-B condition is effectively independent
2. **No positive-measure invariant set:** Any set trapped in growth-B forever must have Haar measure 0
3. **Cannot rule out measure-zero invariant sets:** Since Z ⊂ Z_2 has measure 0, this doesn't transfer to "all integers"

---

### Theorem 44: Sharp Density Result and Comparison with Tao (explore44)

**Statement (FMF Density Theorem):** Let E_k = {n odd : the FMF trajectory of n contains a growth-B chain of length ≥ k}. Then:

1. Among odd residues mod 2^K (K ≥ 2k+3), the fraction in E_k is exactly (1/4)^k
2. The natural density of E_k is (1/4)^k (equivalently, 2/4^k for initial chains)
3. For any ε > 0, the set {n : max growth chain in trajectory of n exceeds ε·log₂(n)} has natural density 0

**Comparison with Tao (2022):**

| Aspect | FMF Quartering Law | Tao (2022) |
|--------|-------------------|------------|
| Density type | Natural (stronger) | Logarithmic |
| Decay rate | (1/4)^k exponential | Sub-polynomial |
| Proof method | Elementary mod-8 | 3-adic entropy, renewal |
| Controls | Growth chain length | Col_min directly |
| Gap to full proof | Same | Same |

**The exceptional finite-shadow set is provably infinite:** The explicit all-zero family `m_0 = 8^L - 1`, `x_L = 4m_0 - 1`, has at least `L` consecutive growth-B hops. Thus any universal logarithmic upper bound for growth-B chain length needs constant at least `1/3` in base-2 logarithms, equivalently `2/3` in base-4 logarithms. The stronger old pigeonhole claim with arbitrary `C < 1` is not justified by the fixed-length density theorem alone.

**Baker's theorem cannot close the gap:** Growth chain conditions are 2-adic (residue classes mod 2^K), while Baker's theorem bounds archimedean quantities (|2^a - 3^b|). The two operate on orthogonal structures.

**What would close the gap:** Effective equidistribution in Z_2, p-adic Littlewood-type results, or mixing estimates for the Collatz map — all open frontier problems in number theory.

---

### Direction G: Closing the "Almost All → All" Gap -- INVESTIGATED, GAP REMAINS (Theorems 42-44)

Three approaches investigated in parallel:
1. **Ergodicity (Th. 42):** FMF map mod 2^K is not ergodic. Cannot help.
2. **2-adic expansion (Th. 43):** Map expands by factor ≥ 8. Explains the Quartering Law structurally, rules out positive-measure invariant sets, but cannot rule out measure-zero invariant sets.
3. **Transcendence theory (Th. 44):** Baker's theorem is archimedean; chain conditions are 2-adic. Orthogonal structures. Cannot help.

**Conclusion:** The "almost all → all" gap is a frontier problem that likely requires genuinely new mathematical tools. The FMF framework has produced the sharpest known density result for growth chain termination, but closing the gap to a full proof appears to be beyond current methods.

---

## 22. Paper Write-Up

Formal Typst paper in `/paper/`. Sections 1-4 written (2026-03-04):

- **Section 1 (Introduction):** Conjecture statement, FMF idea, Theorems A-D summary, honest gap statement, outline.
- **Section 2 (FMF Formulas):** Definitions, Theorem A with full Case B2 proof, v_2(FMF) lemma, v_2(3^n-1) lemma, hop properties.
- **Section 3 (State Independence):** Theorem B with 4-step 2-adic proof, drift observation, self-correction observation.
- **Section 4 (Spectral Contraction):** a/4 discriminant lemma, Theorem C (rho=0.8638, rank-1 reduction), inverse movement rate lemma.

Sections 5-8 written (2026-03-04):

- **Section 5 (Quartering Law):** Growth chain definition, 4 lemmas (Growth-to-Type-A Split, v_2 Geometric, Type B | v_2, Odd Part Equidistribution), Theorem D (P(continue)=1/4, delta_k=2/4^k), Proposition (2-adic Expansion), Lemma (Acyclicity).
- **Section 6 (Gap Analysis):** What is/isn't proved, Tao comparison (natural vs logarithmic density, exponential vs sub-polynomial decay, elementary vs entropy methods), 5n+1 litmus test, why gap is hard (Tao's barrier, Baker mismatch), precise remaining question as conjecture (Growth-B Domain Emptiness).
- **Section 7 (Growth Bounds):** Epoch duration observation, growth phase structure observation, 2^n-1 trajectories, growth chain bound conjecture (0.55*log2(m)+3), bit consumption observation.
- **Section 8 (Future Directions):** Effective equidistribution, Z_2 invariant sets, computational extensions, Syracuse random variable connection, code availability, acknowledgments.

Paper theorem labels: Theorem A = FMF Step Formula, Theorem B = State Independence, Theorem C = Spectral Contraction, Theorem D = Quartering Law. All 8 sections complete.

---

## 23. July 2026 Audit and New Theorems (Multi-Agent Session)

> Status: results below were produced by an adversarial multi-agent session on
> July 19, 2026. Each "refereed x2" item survived two independent adversarial
> verification agents that re-implemented and attacked every step. Items marked
> "pending referees" await the second referee round. Vetted claim boundary
> remains proof-obligations.md; this section is the session log.

### Theorem 45: Exact Critical Exponent alpha* = 1 (CORRECTION of Theorems 15/19)

**Statement:** In the FMF density model of Theorem C, the fractional-moment
series satisfies M(1) = 1 EXACTLY:

M(1) = 1/2·(3/4)/(2−1/2) + 1/4·(9/4)/3 + (1/3)·Σ_{t≥1}(3/4)^{t+2}
     = 1/4 + 3/16 + 9/16 = 1.

Hence alpha* = 1 exactly. The values 1.008 (explore15) and 1.0002 (explore19)
were truncation artifacts (t<30 cutoff). Since every summand of M is strictly
increasing in alpha, M(alpha) < 1 for all alpha < 1, which upgrades the
previously numerical claim M(0.53) ≈ 0.8638 < 1 to a proved strict inequality.
This is the FMF form of the classical fact that the Syracuse first-moment
heuristic Σ 2^{-a}·(3/2^a) = 1 is exactly critical. [PROVED; independently
verified three times: contraction auditor, architecture auditor, main session.]

### Theorem 46: q=9 Boundary Word Exclusion (refereed x2) — CLOSES the last open uniform-morphic template

**Statement:** The fixed point w of the 9-uniform morphism 0→011111111,
1→100000000 (equivalently w_n = parity of the number of nonzero base-9 digits
of n) has no positive ordinary reduced-gap code, and no positive ordinary
return code.

**New tool (Factor-Recurrence Height Barrier):** if an infinite {0,1} gap word
with positive ordinary code A has equal length-m factors (ones-count kappa) at
positions i < i', then the shifted-suffix states a_i ≡ a_{i'} (mod 2^{7m+3kappa})
with a_{i'} > a_i, forcing 2^{7m+3kappa} < a_{i'} ≤ A(243/128)^{i'}(9/8)^{K_{i'}}.
This strictly generalizes the paper's initial-prefix-recurrence barrier to
arbitrary (including overlapping) factor occurrences. Applied to the scaled
8th-power factor B_t^8 = w[9^t..10·9^t) occurring at positions 9^t and 2·9^t
for every t ≥ 1, the modulus 2^{68·9^t+12(−7)^t} beats the growth envelope
A·3^{12·9^t}/2^{17·9^t}, forcing A > 2^{55·9^t} for every t — impossible.

**Secondary:** the initial recurrence function of w is exactly
sigma(l) = 17·9^t on (9^t, 2·9^t], = 90·9^t on (2·9^t, 9^{t+1}], sigma(1)=10;
min sigma(l)/l = 17/2, so the old initial-prefix route (needed < 8.41772) was
provably dead, not merely dead to length 50,000.

### Theorem 47: Complexity Threshold for {0,1} Landings (refereed x2)

**Statement (Same-Factor State-Separation + occurrence counting):** every
infinite {0,1} return word with a positive ordinary return code must satisfy
liminf p(m)/m ≥ T_R ∈ (3.1493, 3.1494); every infinite {0,1} reduced-gap word
with a positive ordinary gap code must satisfy liminf p(m)/m ≥ T_G ∈ (6.2390,
6.2391), where p is factor complexity. Mechanism: equal factors at two positions
force state congruence mod the standalone factor modulus (2^{3m+4·ones} return,
2^{7m+3·ones} gap) plus strict state growth, so few distinct factors ⇒ too many
forced coincidences ⇒ states outrun the landing growth envelope.

**Consequences:** subsumes in one stroke the eventually-periodic, fixed-defect,
sparse-label, low-complexity (p(m) ≤ m), and balanced/Sturmian exclusions;
applies to non-recurrent words untouchable by prefix-recurrence machinery;
independently re-closes q=9 (p(m) = 4(m−1) < 6.239·m). Remaining open {0,1}
regime: aperiodic words with liminf p(m)/m above the thresholds.

### Theorem 48: AP Survivor Bounds — first unconditional unweighted rank-type estimates (REFEREED July 21: main bounds and downstream-sufficiency CONFIRMED; saturation obstruction confirmed as stated but its summary's "all sieve variants" gloss narrowed to translate-invariant forms only)

**Statement:** with D_L the set of integers formally admitting ≥ L binary return
blocks, there is an absolute C with, for every arithmetic progression P of odd
difference and length N: #(P ∩ D_L) ≤ C·N^{3/10} for all L ≥ log_8 N + 3, and
#(P ∩ D_L) ≤ C(N·2^{−2.1L} + 2^{0.9L}) for all L. Hence
W_R(B,L) ≤ C((B+1)2^{−2.1L} + 2^{0.9L}); gap analogue W_G(B,L) ≤
C(B·2^{−5.46L} + 2^{1.54L}). Exponent floors: alpha_R = 0.287761 (root of
Σ_r 2^{−(4r+3)β} = 1), alpha_G = 0.212323.

**Saturation obstruction (proved):** translate-invariant counting schemes
(second-moment/Cauchy-Schwarz/large-sieve on congruence-class structure) cannot
reach C(B+1)θ^L, since sup over translated APs of length 1 stays ≥ 1 at every L.
Any proof of the full rank conjecture must use arithmetic separation of
normalized terminal heights — confirming Section 6's own diagnosis.

**Downstream simplification (proved):** the endpoint application does NOT need
the sharp bases 2/15, 1/112 — any uniform f(B)g(L) with g(L) → 0 suffices; the
sharp bases matter only for the survival-depth constants.

### Theorem 49: The Rank Conjecture is 3-Free — 5n+1 Litmus on the Endgame (REFEREED July 21: CONFIRMED — a=5 block coding re-derived independently (P_r = 25·125^r, D_r = (160·125^r−51·16^r)/109, same Q_r = 2^(4r+3)); survival bases proved purely 2-adic; F_5(13)=13 lies outside every excluded class (v_2=5); the secondary documentation flag against referee-brief.md was withdrawn as overreach)

**Statement:** the entire binary return/gap counting apparatus transfers
verbatim to 5n+1: same gate moduli Q_r = 2^{4r+3}, q_k = 2^{3k+7}, same
constants 2/15 and 1/112, same quartering 1/4, same terminal-window identities
and periodic exclusions (with P_r = a^2(a^3)^r, a = 5). Since 5n+1 has a proven
nontrivial cycle (13) and (conjecturally) divergent orbits, the W_R/W_G rank
conjecture — even proved with sharp constants and combined with completion-gate
steps 1–3 — cannot imply convergence. The constant 3 must enter at step 4
(mixed growth/recovery epochs), where a/4 < 1 gives 3n+1 its deterministic
Type-A contraction channel (F_5(13) = 13 is the concrete witness that the 5n+1
endgame has an FMF fixed point outside every excluded class).

**Repo framing consequence:** referee-brief.md / proof-obligations.md should
present the rank theorem as necessary-for-this-route but structurally
insufficient; step 4 is where the actual Collatz content lives.

### Theorem 50: FMF–Tao Renewal Correspondence (REFEREED July 21: CONFIRMED x2, minor caveats)

**Statement:** the FMF hop decomposition coincides with the renewal
decomposition of Tao's Syracuse valuation sequence a_i = v_2(3·Syr^{i−1}(N)+1)
at letters a_i ≥ 2 (Type A ↔ block (b), b ≥ 2; Type B with k+1 = 2^t m ↔ block
(1,…,1,b) with t+1 ones). Every FMF exact density law is therefore a functional
of the iid-Geom(2) layer that is already exact in Tao's framework. The
natural-density upgrade of Tao's theorem reduces to two sharply-stated lemmas
(tilted character-decay for Geom(μ), μ ≈ 2 uniform; first-passage stabilization
from uniform windows); the regime 3^k with k ≤ n^{1/2−δ} is PROVED to follow
from Tao's published Prop 1.17. [Checked numerically: tilted character sums
decay at rates 0.61–0.88/step across the needed tilt range.]

### Parity-Certificate Program Results (REFEREED July 21: split verdict — all load-bearing computations independently confirmed; Theorem H(c) backward direction withdrawn as unproven side statement; the "bounded horizon, all x" CST lemma is classical Terras 1976 machinery, novelty framing dropped)

- Exact maximal mod-2^n descent certificates to n = 28: uncertified counts equal
  OEIS A076227 with ZERO additive failures at every frontier step ⇒ every
  integer x ≥ 2 with coefficient stopping time tau(x) ≤ 28 satisfies
  sigma(x) = tau(x) (bounded-horizon verification of Terras' CST conjecture,
  complementary to the bounded-x literature).
- Hybrid no-gain theorem: FMF-pattern certificates ARE parity certificates
  (explicit block bijection: FMF hop with v_2(x+1)=j ↔ parity block 1^j 0^w);
  hybrids certify exactly the Terras classes at every modulus/horizon ≤ 28.
- Paradox-size bound: enumeration of paradoxical stopping values for all 7 known
  paradoxical pairs is provably complete (largest bound ~2^38.3 << 2^71 Barina).
- Delimiter: the uncertified frontier grows ~1.93^n forever — no finite-modulus
  certificate scheme, with any horizon, can close the pointwise gap.

### Theorem 51: Universal Uniform-Morphic Exclusion — "Theorem G" (July 21, refereed x2, minor)

**Statement:** Let y ∈ {0,1}^∞ be a fixed point of ANY q-uniform morphism
φ: {0,1} → {0,1}^q, q ≥ 2 (no aperiodicity or primitivity assumed). Then y
admits no positive ordinary reduced-gap code: a code A would have to satisfy
A > 2^{3·q^t} for every t ≥ 0. Return form: M + 1 > 2^{q^t}. Coding form: fixed
points over alphabets of ≤ 6 letters (gap) / ≤ 3 letters (return) are excluded,
hence every binary q-automatic gap word with a ≤ 6-state msd-first DFAO, for
every q. Proof: pigeonhole equal letters at positions p1 < p2 ≤ 2; φ^t-images
give the same length-q^t factor at p1·q^t and p2·q^t ≤ 2q^t; the shift-code +
forced-prefix-congruence lemmas force the two orbit states congruent mod
2^{7m+3κ} while strict monotonicity and the growth envelope cap the later
state — integer certificates 3^7 < 2^12 (gap), 3^5 < 2^8 (return). Subsumes the
repo's separate q = 2..6 classifications and the q=9 boundary word (Theorem 46)
in one argument. Companion mechanical theorems for the q=9 word: exact
recurrence function R(n) = 747·9^k + n − 1 on bands [9^k+2, 9^{k+1}+1],
R(n) ≤ 748n − 1 sharp; initial-prefix recurrence τ(n) ≥ 8.5n with liminf
exactly 17/2 — proving the density-recurrence route could never have closed
q=9 (it fails by exactly the Pythagorean comma 3^12/2^19).

### Theorem 52: Transfer-Operator No-Go Package (July 21; negative result)

The spectral/functional-equation route is exactly mapped and provably cannot
close the pointwise gap. Positive structure (exact): Syracuse and FMF transfer
operators on Z_2 (and the annealed 3-adic chains mod 3^j) are
nilpotent-plus-rank-one at every finite level (spectrum {1} ∪ {0}, finite-time
exact mixing); Hölder gap g_α = 1/(2^{1+α} − 1) (= 1/3 at α = 1), FMF hop gap
= g² = 1/9 (exact squaring identity). Obstructions (proved): (1) operator-level
5x+1 litmus — branch weights, contraction ratios, Hölder constants and all
finite-level spectra are IDENTICAL for qx+1 for every odd q, and 5x+1 has the
integer cycle {13, 33, 83}; (2) dense-null trichotomy — reach-1 points
(countable, dense), divergence-type points (uncountable, dense), and extra
ergodic invariant measures coexist on mutually dense Haar-null sets, so
almost-everywhere is topologically optimal on Z_2; (3) the Berg–Meinardus
truncated solution space has dimension ~N/6 growing linearly (verified exactly
to N = 3·10^6) — certified finite truncation is impossible. Sole 3-specific
spectral quantity found: L²-criticality Σ 4^{−k}·(weights) = 1/3 = |3|_3.

### Theorem 53: Cycle Bounds at the 2^71 Floor + FMF Hop Identity (July 21, refereed x2)

(1) The 2025 verification floor 2^71 does NOT extend Hercher's m ≤ 91 m-cycle
exclusion: the unique surviving candidate at m = 92 is the 43rd convergent of
log₂3, (K, L) = (205632218873398596256, 120287136981023372109), with gap
6.2447·10^{−43}, a factor 5.1 below the achievable width floor; m = 92 becomes
excludable iff the floor reaches ≈ 2^{73.869}. Conditional milestone map:
2^74 ⇒ m ≤ 92; 2^76 ⇒ 100; 2^82 ⇒ 103; 2^90 ⇒ 122 — binding obstructions are
exactly the convergents preceding the large partial quotients 37, 55.
(2) NEW IDENTITY (proved): the Simons–de Weger local-minimum count m of any
nontrivial cycle EQUALS its number of FMF hops. Hence the current record reads:
**every nontrivial Collatz cycle makes at least 92 FMF hops.** All-growth-B
cycles are impossible; the 3n−1 map's 17-cycle is an all-B 2-hop cycle, so no
sign-agnostic argument can force a Type A hop in a hypothetical cycle.

### Theorem 54: Pointwise Descent Record σ = κ to Horizon 301,993 (July 21, refereed x2, minor)

**Statement:** for EVERY odd x > 1 (unbounded) with coefficient stopping time
κ(x) ≤ 301,993 Terras steps (492,529 single steps): T^j(x) > x for j < κ(x) and
T^{κ(x)}(x) < x, i.e. σ(x) = κ(x). Extends Terras 1976 (2,593) by ×116 and
Garner 1981 (64,508, conditional) by ×4.7; self-contained (proved threshold
lemma with exceptions ≤ B(m) = ⌊(m·3^m − 1)/(2(2^n − 3^m))⌋, exact integer
ledger Θ(301,993) = 10,824,133,905, zero-exception scan of 1.35·10^9
candidates). Equivalent: for every n ≤ 301,993, every odd x > 1 outside the
explicit ballot family B_n mod 2^n (|B_n| = A076227(n), density < 2^{−15,093}
at the top horizon) descends below itself within n steps. Corollary: every
nontrivial cycle has Terras length > 301,993 (Hercher's bounds remain
stronger). Structure theorem for the uncertified tree: exact ballot
characterization, 1-or-2 branching with deficits precisely at Beatty jumps of
log₃2, no leaves; an uncountable Cantor set of box dimension in
[0.946954, 0.949956]. REFUTED: the conjecture that the uncertified tree is the
closure of FMF growth-B patterns (strict inclusion with exponential gap:
Narayana growth 1.46557 vs γ ≥ 1.9279). Conditional on Rozier–Terracol
(Discrete Math. 2026), the horizon extends to κ ≤ 665,684,250.

### Theorem 55: The Two-Lemma Reduction and Lemma E (July 21 endgame, refereed x2, minor)

**Theorem R (PROVED, conditional structure):** Let H1 = "the binary return
partial map T(n) has no infinite positive-integer orbit" (equivalently
μ_L → ∞). Let **Lemma E** = "every non-descending FMF orbit is eventually a
depth-{0,1} growth-B chain" (letters l_j = (s_j, v_j) ∉ G01 = {(2,2),(3,2)}
only finitely often, where s = v_2(x+1), v = v_2(FMF)). Then H1 + E ⇒ every
odd x > 1 has finite epoch ⇒ pointwise FMF descent ⇒ Collatz. Proof uses the
new unconditional **Lemma P**: no infinite positive orbit of m' = (27m+1)/16,
because 16(11m'+1) = 27(11m+1) forces v_2(11m_0+1) ≥ 4k for all k.
Lemma E's 5n+1 analogue is FALSE (F_5(13) = 13, hop letter (3,5)): E carries
ALL the 3-dependence of any completion through this framework. Supporting
partials (proved): the ballot inequality for non-descending prefixes
(S_N/N ≥ log_{3/2}2; the coefficient 2 − log₂a flips sign at a = 4); bounded
depth-sum orbits descend effectively (l ≤ 1 + 1.4094·T′); eventually-periodic
hop words are exactly cycles (no divergent orbit has an eventually periodic
hop word); mixed-pattern shadow theorem (every finite hop word is one residue
class mod 2^(H+1) — no finite forbidden-pattern strategy works). Dimension
identity: α_R = −log₂ y with y³ + y⁴ = 1; the rank program's scope has box
dimension 0.2878 vs ≥ 0.9470 for the uncertified Cantor set E must empty.

### Theorem 56: Tilted Character Decay S4-T and the State of the Tao Upgrade (July 21, refereed x2, minor)

Tao's Proposition 1.17 generalizes verbatim to Geom(μ)-driven Syracuse
characters uniformly on every compact of the contractive regime
q ∈ (q*, 1), q* = 1 − log2/log3: the k ≤ n^(1/2−δ) restriction is removed for
all tilts the natural-density program needs; the joint affine version (Tao's
Remark 1.16) holds at zero extra cost. Exact criticality: Prop 1.14's
collision-entropy step costs exp[βk(1 − H₂(q))ln2] — polynomial iff q = 1/2 —
so it survives exactly the shrinking tilts |q − 1/2| ≤ K/√k required and
fails for fixed tilts. S5 (first-passage stabilization): combinatorial kernel
proved (exhaustive fiber bijection), analytic equidistribution input proved
via Rhin's irrationality measure of log₂3 (rate log^{−0.131}x); the remaining
work is a rebuild of Tao's Section 5 bookkeeping with pinned sums — no
obstruction identified, NOT yet proved. Full S4+S5 would give natural-density
almost-all, not all.

### Theorem 57: Exact Criticality of the Rank Bases and the Class-Counting No-Go (July 21, refereed x2, minor)

(T1) W_R(B,L) ≥ C(L+s, s), s = ⌊(⌊log₂B⌋ − 3L)/4⌋; hence
sup_L W_R(B,L) ≥ B^(α_R − o(1)) inside the anchored window — the AP-Survivor
exponent α_R = 0.287761 is optimal even for position-aware counting.
(T2) For every ρ < 2/15, W_R(B,L) ≤ C(B+1)ρ^L is FALSE along
(L,B) = (15s, 2^(49s)) via 16·H(1/16) = 49 + 15·log₂(2/15); the base 2/15 is
exactly critical (floor ratio Θ(s^{−1/2}) at 2/15). Gap analogue: 1/112
exactly critical via 8·H(1/8) = 52 − 7·log₂112. (E) The per-B decay target
[∀B: W_R(B,L) ≤ C_B·g(L), g → 0] is EQUIVALENT to μ_L → ∞. (BLOCKING) Every
certificate from the interval+AP counting recursion is ≥ 1 for all (B,L) via
the r = 0 chain (witness: W_R(100,3) = 0, certified ≥ 1) — no class-counting
scheme can prove H_R(B) < ∞ for any B. Positional deep-gate emptiness
(16^r > 33B + 32 ⇒ empty below B) is real but does not remove the thick-class
defect term. All statements transfer verbatim to 5n+1, as expected.

### Theorem 58 (CANDIDATE — awaiting human review): Natural-Density Upgrade of Tao's Theorem ("Theorem ND", July 21 round 4, AI-refereed x2 NOT-REFUTED)

**Claimed statement:** there is an absolute C such that for every N0 ≥ 16,
the set {N : Col_min(N) > N0} has upper natural density ≤ C·log^(−1/25) N0;
consequently Col_min(N) ≤ f(N) for almost all N in NATURAL density, for every
f → ∞. New components (each claimed proved, machine-checked): Lemma P7
(s-pinned character sums bounded by Tao's own Section-7 majorant — the total
valuation is measurable w.r.t. his pair-sum conditioning); **Lemma J*** — the
fine-scale mixing of the entire affine map (S_n, X_n), exactly the object of
Tao's Remark 1.16 ("plausibly attainable from the methods in this paper");
Lemma R (pinned-sum renewal-equidistribution, limit 1/ln(4/3), via Rhin's
effective irrationality measure of log₂3); uniform-window Prop 5.2-U with
standoff inequality. The limiting first-passage measure equals Tao's
log-density one. Manuscript: notes/round4-july2026/s5-completion/PROOFS.md
(571 lines). **Status: candidate only. Two independent adversarial AI
referees failed to refute (minor findings; all Tao citations verified against
the arXiv v7 text; all scripts pass). NOT established mathematics until
reviewed by a human expert; excluded from proof-obligations.md.**

### Theorem 59: Lemma E Partials — Depth Hierarchy and the Statistical No-Go (July 21 round 4, refereed; one-clause repair to LE1(c) noted)

Hop-word factor barrier: every odd x whose hop word lies in a finite alphabet
A and is not eventually periodic satisfies p(m) > (h_min·m + 1 −
log₂(x₀+1))/Γ for all m. Corollary: depth-{0,1,2} hop words need
liminf p(m)/m ≥ 3/log₂(41/16) = 2.20986 — the first proved slice of Lemma E
strictly beyond depth {0,1}. Invariant table: the depth-2 analogue of Lemma P
is 32(49m′+1) = 81(49m+1) (invariant 7²); general d_s = 3^s − 2^(s+1);
block-power lemma v_2(D_u x − B_u) ≥ k·H_u kills all periodic-tail u^∞
obstructions (|u| ≤ 91 via Hercher; all-expanding u unconditionally).
Reduction R₂: H1 over depth-{0,1,2} + depth-{1,2} + E₂ ⇒ Collatz. NO-GO:
the ballot inequality restricts letter frequencies only through the
expanding/contracting dichotomy — exact witnesses achieve non-G01 letter
density 1 among non-descending prefixes, so no purely statistical
(frequency-based) quantitative form of Lemma E can exist; E must be proved by
arithmetic, not letter statistics.

### Theorem 60: Full-Shift Ambient Language and the Sharpened 3-Dependent Thresholds (July 21 round 4)

The ambient language of the binary return and reduced-gap coding systems is
the full shift: every finite binary word occupies exactly one nonempty
residue class, and every infinite word is the exact itinerary of a unique
2-adic seed (the all-zero seed is −1). Hence NO upper bound on landing-word
factor complexity follows from the generation mechanism — a complexity pincer
is impossible without invoking H1 itself. Salvage theorems: sharpened
pointwise density-coupled thresholds — return landing words satisfy
p_w(m) ≥ (3m − log₂(M+1))/(5log₂3 − 7), giving liminf p/m ≥ T_R′ =
3.2439007; gap: T_G′ = 6.3942268; uniform-density floor 7/(5log₂3 − 7) =
7.5691 for both. The bound is genuinely 3-dependent: T_R′(a) = 3/(5log₂a − 7)
becomes vacuous exactly at a ≥ 4 — the first complexity-type exclusion that
passes the 5n+1 litmus.

### Theorem 61: Mirror Equivalence and Two-Prime Vacuity (July 21 round 5; definitive negative result)

**Mirror Equivalence Lemma:** for every return word prefix,
U_N = (P_N R_N + D_N)/Q_N equals the least nonnegative residue V_N of
D_N Q_N^{-1} mod P_N = 3^(2N+3S_N). Proof: Q_N | P_N R_N + D_N;
0 < U_N < P_N from 0 < D_N < P_N; U_N Q_N ≡ D_N mod P_N; a class mod P_N has
one member in [0, P_N). The 2-adic and 3-adic prefix data are therefore the
SAME information under an explicit affine bijection. **Theorem V:** for fixed
M and word w, 3-adic consistency with positive integer states below the
envelope of M ⟺ R_N ≤ M — verbatim the rank condition; the per-block 3-adic
consistency fraction is exactly 1 and no two-prime pincer can prune the word
tree beyond the (already exponent-optimal) rank program. Kill census (10^6
seeds, a = 3 and a = 5): all kills are 2-adic gate failures; zero 3-adic or
positivity kills; the apparatus is a-blind (5-adic mirror identical).
Salvage: exact information ledger (letter r consumes 4r+3 seed bits forward
and dictates 3r+2 state trits backward — the state's low ternary digits spell
the reversed recent word), and the **mirror form of H1**: a small-least-
residue statement modulo powers of 3 with 2-power denominators, placing H1 in
the Erdős–Lagarias ternary-digits-of-2^n / Furstenberg ×2×3 rigidity class.

### Theorem 62: The Cocycle, the Reset Law, and the Core of Lemma E (July 21 round 5, refereed ×2, minor)

A1 (cocycle): B_uw = 3^(S_w) B_u + 2^(H_u) B_w and identically for D; Lemma P
is the power-degenerate case. A2 (master identity):
v_2(D_p x₀ − B_p) = H_p + v_2(x₀ − x_k) for every prefix p of every hop word.
A3 (classification): a fixed-form certificate with forced
v_2(a·x₀ + b) → ∞ exists iff the word's 2-adic seed ξ(w) is rational
(a·ξ + b = 0); for irrational seeds the Lemma-P mechanism provably cannot
apply; recognizing aperiodic rational-seed words is equivalent in difficulty
to the Lagarias periodicity conjecture. B (reset law): crossing an
intervening block m updates ν = v_2(U_u) by ν′ = min(ν, ω) − H_m — a RESET to
the Wronskian level ω(u,m) = v_2(D_u B_m − B_u D_m), given by a proved closed
formula; the only escape is the coincidence channel ν = ω. Hence the residual
core of Lemma E: an infinite non-descending obstruction requires infinitely
many exact valuation coincidences — 2-adic near-approaches to eventually-
periodic rational seeds — with orbit size the only non-circular lever.
**Spike-ledger theorem (new, unconditional):** all hop words whose depth
spikes outrun the drift budget at geometric ratio > log₂3 are excluded
(sharp; multiplier-covariant) — a proved slice of the unbounded-alphabet
branch. Hierarchy pincer impossible: transported thresholds strictly decrease
with depth.

### Observation 63: FM2^k Hops Are Geometric Aggregates of FMF Hops (August 16, 2026; machine-verified, not refereed)

**Statement:** For k >= 3 define FM2^k(x) as the first orbit value of odd x
divisible by 2^k and F_k(x) = FM2^k(x)/2^{v_2}. Then (i) the number N of FMF
hops composing one FM2^k hop is geometric with P(N=j) = p(1-p)^{j-1},
p = 2^{-(k-2)}, in 2-adic density (verified exactly mod 2^16 for k=3,4,5);
(ii) by Wald's identity the mean log2-drift per Collatz step equals
(log2 3 - 2)/3 for every k (measured -0.135..-0.139 for k=2..6); (iii) the
worst-case single-hop ratio grows without bound in the bit-length for every k,
with 2^n-1 the common adversary; (iv) k=2 is the largest k for which the hop
map is total on odd integers > 1, since the cycle 1->4->2->1 contains no
multiple of 8.

**Proof sketch:** (i) is the geometric law for v_2(FMF) (Lemma, Section 2)
applied at each landing with the density-level independence of Theorem B;
(ii) is Wald with the stopping time N; (iii) FM2^k(2^n-1) is reached at the
first FMF landing of 2^n-1 with v_2 >= k, which for k <= v_2(3^n-1)+1 is the
FMF landing itself. (iv) is inspection of the trivial cycle.

**Consequence:** the FMF framework is the k=2 member of the Terras parity-vector
family; changing k re-chunks the same chain and does not touch H1 or Lemma E.
Script: explorations/explore82_fm2k_generalization.py.

### Audit Outcome Summary

All core claims CONFIRMED (Theorems A–D, Sections 6–8 reductions, verifier
35/35). One numerical error found and fixed (alpha* = 1 exactly). Presentation
repairs identified: explicit cylinder-AP lemma + countable-additivity line for
Theorem D; strict M_w > −1 induction for terminal windows; completion-gate
step 4 disclosed as an unwritten second gap; W_G noted as logically redundant
given W_R. Literature: Barina 2^71 still current; arXiv:2601.03297 v5 downgraded
its cycle-finiteness claim to conditional (do not cite as unconditional).

**The Collatz conjecture remains open.** The pointwise gap now stands sharpened:
{0,1} landings need liminf p(m)/m > 3.1493 (return) / 6.2390 (gap); q ≤ 9
uniform-morphic templates are ALL excluded; translate-invariant counting cannot
finish the rank bound; and any completion through this route must inject the
constant 3 at the mixed-epoch stage.
