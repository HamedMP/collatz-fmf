# Collatz Mod-4 Exploration Plan

> **Historical status note (May 2026 review):** this is an exploratory work log,
> not the current manuscript and not the repository's claim boundary. Some early
> entries below record proof attempts or comparisons that were later corrected.
> The vetted statement of what is proved is in `paper/main.typ`,
> `proof-obligations.md`, `publication-readiness.md`, and `referee-brief.md`.
> In particular, the FMF density bounds are not a proof of Collatz and should
> not be described as directly stronger than Tao's almost-all orbit-minimum
> theorem, because the measured events are different.

## Summary of Hamed's Findings (Aug 2023)

### Core Framework
- Classify numbers mod 4: **odd** (4k+1, 4k+3), **mult of 4** (4k), **even-not-4** (4k+2)
- Modified Collatz U(x): divide by largest power of 2 (LPT), not just 2
- **T_i(x) = 3^i(x+1)/2^i - 1**: chains i odd-cycle operations into one formula
- **FMF conjecture**: for x = 4k+3, first multiple of 4 appears at step **3 + 2*TZB(k)**
  - TZB(k) = trailing zero bits of (k+1) in binary (i.e., v_2(k+1))

### Three cases for FMF:
1. **4k+1**: 3(4k+1)+1 = 12k+4 = 4(3k+1) -> immediate multiple of 4 (1 step via 3x+1)
2. **4k+3, k even**: 3 Collatz steps -> multiple of 4 (apply T_1 then 3x+1)
3. **4k+3, k odd**: fmf_step = 3 + 2*TZB(k) -- the deep pattern

### Identified Obstructions:
1. Can't easily predict if x/2^k lands in 4k+1 or 4k+3
2. Can't easily find the k parameter in x/2^k without calculation
3. FMF formula itself needs mathematical proof

---

## Exploration Plan

### Phase 1: Verify and extend FMF (explore01-03)
- [ ] explore01.py: Verify FMF formula for large ranges (millions), check for counterexamples
- [ ] explore02.py: Analyze the FMF *value* (not just step) -- is there a formula for the actual multiple of 4 reached?
- [ ] explore03.py: Track the ratio FMF_value / starting_number -- does it always decrease eventually?

### Phase 2: The descent question (explore04-06)
- [ ] explore04.py: After hitting FMF (a multiple of 4), trace what happens next. How many steps to the *next* FMF? Is there a pattern?
- [ ] explore05.py: For x=4k+3, compute FMF, then divide by LPT, classify mod 4, repeat. Map the full "FMF chain" until we reach a number < x
- [ ] explore06.py: Statistical analysis: for each starting x, how many FMF hops to reach a number < x? Distribution?

### Phase 3: Proving descent (explore07-09)
- [ ] explore07.py: Attempt to prove FMF formula algebraically for small TZB values (TZB=1,2,3,...)
- [ ] explore08.py: Investigate the 2-adic valuation connection -- TZB(k) = v_2(k+1). Explore using p-adic framework
- [ ] explore09.py: Look at the "obstruction" -- classifying x/2^k mod 4. Is there a pattern in the binary digits?

### Phase 4: Visualization and insight (explore10)
- [ ] explore10.py: Analyze FMF graph structure (text-based)

### Phase 5: Towards proof (explore11-14)
- [ ] explore11.py: Markov chain model of FMF dynamics
- [ ] explore12.py: Prove state-independent transitions algebraically
- [ ] explore13.py: Cycle exclusion analysis
- [ ] explore14.py: Formalize random walk drift argument (Cramer bound)

### Phase 6: Closing the gaps (explore15+)
- [ ] explore15.py: Supermartingale construction (f(x) = x^alpha)
- [ ] explore16.py: Autocorrelation decay of FMF increments
- [ ] Deeper analysis TBD based on findings

---

## Status Log
- **explore01.py**: DONE - FMF formula verified for 1M values of k. Zero failures across all three cases (4k+1, 4k+3 k even, 4k+3 k odd). Formula fmf_step = 3 + 2*TZB(k) holds perfectly.
- **explore02.py**: DONE - Found CLOSED-FORM for FMF value: **FMF(4k+3) = 3^(t+2)*(k+1)/2^(t-1) - 2** where t=TZB(k). Verified for 500K odd k values, zero failures. Also found k-even formula: FMF = 4(9j+4) where j=k/2. The ratio FMF/x ~ (3/2)^(t+1)*3/2 grows with TZB -- FMF is always LARGER than x.
- **explore03.py**: DONE - All 200 tested numbers eventually descend. Distribution: 44% descend in 1 hop, 27.5% in 2 hops, 81.5% in ≤3 hops. Key: v_2(FMF) determines LPT, and FMF = 2(3^(t+2)*m - 1) where k+1=2^t*m. The LPT uses the known result v_2(3^n-1) = v_2(n)+1 when n is even. Hard cases (27,31,47...) require 12-18 hops.
- **explore04.py**: DONE - FMF chains always show net_bits < 0 (more shrinkage than growth). The net log2 multiplier is always negative, meaning descent always occurs. Tightest case: x=63 with net_bits=-0.11 (ratio 0.968). Key: each 3x+1 grows by log2(3)=1.585 bits, but LPT divisions + internal /2 always win.
- **explore05.py**: DONE - PROVED the FMF formula algebraically! For x = 2^(t+2)*m - 1 (m odd), the sequence strictly alternates 3x+1 and /2, with coefficients following (3^(j+1)*2^(t+2-j), -2) at odd steps and (3^j*2^(t+2-j), -1) at even steps. The power of 2 in the leading term decreases by 1 every 2 steps, reaching 2^1 at step 2t+3, which is the first time divisibility by 4 occurs. Verified symbolically for t=1..15 and numerically for 1200 (t,m) pairs.
- **explore06.py**: DONE - v_2(3^n - 1) = 1 (n odd), v_2(n)+2 (n even). For 1-hop descent, need v_2(FMF) > 0.585*(t+2)+1. Descent fraction: 50% for t=1, drops as ~1/2^(0.585t). After no-descent FMF hop, odd_after splits ~50/50 between 4k+1 and 4k+3 -- this is key because 4k+1 cases give strong shrinkage (log2(3/4) per step).
- **explore07.py**: DONE - Hard cases: 2^n-1 are NOT always hardest; x=7527 needs 21 hops. Average hops stabilize at ~1.73, median=1 (most descend in 1 hop). Max hops grow ~logarithmically with range. The chain for 27 shows it passes through 31 (itself hard), accumulating growth until 4k+1 "release valves" trigger large divisions.
- **explore08.py**: DONE - v_2(FMF) has EXACT formula: v_2(FMF) = 1 + v_2(m - (3^(t+2))^{-1} mod 2^N). The 2-adic inverse determines everything. v_2 distribution among random odd m follows exact geometric: P(v_2 ≥ j) = 1/2^(j-1). This connects Collatz directly to 2-adic number theory. Verified 900 cases with 0 errors.
- **explore09.py**: DONE - Built FMF-accelerated Collatz engine. Verified exact match on 5000 numbers (0 errors). Compression ratio: ~6 Collatz steps per FMF hop. Example: 27 → 1 in 111 Collatz steps = 17 FMF hops through 18 odd milestones. The "odd milestone trajectory" is a vastly compressed view of Collatz dynamics.
- **explore10.py**: DONE - Analyzed FMF graph structure (text-based). Key findings: (1) **Hub nodes**: node 1 has in-degree 8, node 91 has in-degree 7, nodes 5 and 13 are major funnels. (2) **Convergence**: many numbers share the same FMF successor -- e.g., {63,95,121,143,215,323,485} all map to 91. (3) **Depth distribution**: mean 15.27 hops to reach 1 (range [3,10000]), max 42 hops (x=6171). 50% reach 1 within 14 hops. (4) **Release valve**: 4k+3 -> 4k+1 transitions occur ~50% of the time; 4k+1 successors always give immediate /4 shrinkage. (5) **Trajectory merging**: 27->31->121->91 then merges with 63->91, showing how hard cases share tails. Compression ratio: ~6 Collatz steps per FMF hop.
- **explore11.py**: DONE - Markov chain analysis. **MAJOR FINDING**: transition matrix is state-independent -- ALL rows identical (50% A, 25% B0, 12.5% B1, ...). Expected drift E[log2(F(x)/x)] = -0.830 bits/hop. Type A always shrinks (E=-1.42), Type B(t=0) E=-0.83, B(t=1) E=-0.25, B(t>=2) positive but rare. Overall P(shrink)=71.4%. Type distribution along chains: 52.3% A, 47.7% B. Theoretical formula E=0.585(t+2)-3 matches empirical to 4 decimal places.
- **explore12.py**: DONE - PROVED state-independence algebraically. Key: v_2(3^(t+2)*m-1) = v_2(m-inv) where inv is 2-adic inverse. As m ranges over odds, (m-inv)/2^v is uniformly distributed among odds. Since 3^(t+2) is odd, F(x) mod 4 is uniform over {1,3} -> P(A)=P(B)=50%. The t'-value of B outputs follows P(t'=j)=1/2^(j+1), also independent of input. Verified for t=1..7.
- **explore13.py**: DONE - Cycle exclusion analysis. Standard constraint: x*(2^K-3^n)=S. Known bounds: n>10^8 (Eliahou), x>5.76*10^18 computationally. In FMF terms: min cycle >1.67*10^7 hops. With drift -0.83: P(return) ~ exp(-8.3*10^6) ~ 0. Only trivial cycle 1->1 found. Closest 2^K to 3^n: ratio 0.002 at n=53.
- **explore14.py**: DONE - Random walk drift formalized. Distribution: mean=-0.830, var=2.683, std=1.638. **Cramer bound: theta*=0.6986**, giving P(max walk >= H) <= exp(-0.70*H). P(reach 1000x) < 0.095%. Drift UNIFORM across magnitudes (E=-0.83 for 8-bit through 18-bit x). Empirical peak growth distribution matches exponential bound perfectly. Max observed peak: 998.7x. **Remaining gap: i.i.d. assumption on increments needs justification via mixing conditions or supermartingale.**
- **explore15.py**: DONE - Supermartingale analysis. **Critical alpha*=1.008**: for alpha < 1.008, E[(F(x)/x)^alpha] < 1. BUT: since F is deterministic, f(x)=x^alpha is NOT a pointwise supermartingale (~29% of hops have F(x)>x). E[R^0.5] = 0.863, stable across all bit-lengths. Mod-8 transition analysis shows non-uniformity: x=7 mod 8 has avg ratio ~1.30, while x=5 mod 8 has ~0.47. A weighted Lyapunov L(x) = x^alpha * w(x mod 8) might address this. **Key insight: the supermartingale approach fails because F is deterministic. The gap IS the ergodicity/mixing question.**
- **explore16.py**: DONE - Autocorrelation analysis. Lag-1 corr = +0.082 (weak but nonzero). **Self-correcting behavior**: after large growth (X>3), P(shrink next)=0.82 and E[X_next]=-1.07. Growing hops cluster slightly: P(grow|grow)=0.363 vs P(grow)=0.295 (ratio 1.23). Max growing streak = 7 hops. **Type transitions are NOT fully state-independent along chains**: after B(t=4), 75% chance of B(t>=2) next; after B(t=2), 74% chance of Type A next. This is a COMPENSATORY mechanism -- large-t hops tend to be followed by Type A (shrinking) hops. **Conclusion: weak positive lag-1 correlation, but strong self-correction. The chain is weakly dependent, not i.i.d., but the self-correcting tendency makes it BETTER than i.i.d. for convergence.**
- **explore17.py**: DONE - **MAJOR RESULT**: Weighted Lyapunov L(x)=x^alpha * w(x mod M). Spectral radius rho(T) < 1 for ALL tested M (4,8,16,32,64) with optimal alpha=0.53 giving rho~0.8625. This means the weighted transition matrix IS a contraction! Convergence check: rho stabilizes at ~0.8638 as N grows from 10K to 500K. Eigenvector gives optimal weights (e.g., w(7 mod 8)=1.0, w(5 mod 8)=0.37). **Limitation: computed from finite samples. To prove universally, need to show the transition matrix entries converge to their limiting values, which follows from the 2-adic equidistribution of Theorem 12.**
- **explore18.py**: DONE - Self-correction mechanism analyzed. Higher t-values STRONGLY bias toward Type A next: B(t=2)->A at 73%, B(t=6)->A at 81%, B(t=9)->A at 87%, B(t=11)->A at 91%. BUT: v_2(FMF) alone does NOT predict next type (stays ~50/50). Growth magnitude also doesn't predict next hop (E[next]~-0.83 regardless). **Key finding: the self-correction is TYPE-dependent, not growth-dependent.** Large-t (B) hops produce outputs that are biased toward Type A. The consecutive v_2 values show odd/even parity effects rather than simple correlation.
- **explore19.py**: DONE - **MAJOR RESULT**: Analytical transition matrix computation. Confirmed **rho(T) = E[R^alpha]** exactly, because T is rank-1 (state-independence). Theoretical alpha* = 1.0002 (E[R^alpha]=1). At alpha=0.53: theoretical rho = 0.8638, matching empirical perfectly. **Key formulas**: E[R^alpha|A] = (3/4)^alpha * sum_v 2^(-v*alpha) * P(v), E[R^alpha|B(t)] = ((3/2)^(t+2))^alpha * same v-sum. The v_2 distribution for both A and B types follows exact geometric P(v=j)=1/2^j. Since T is rank-1, rho = trace = E[R^alpha] = P(A)*E[R^alpha|A] + sum_t P(B,t)*E[R^alpha|B(t)]. This converges for all alpha < alpha* because EACH TERM is computed from the EXACT 2-adic distribution, not finite samples. **This closes the convergence gap**: the transition matrix entries ARE their limiting values because they're determined by the 2-adic structure (Theorem 12). [Correction, July 2026 audit: alpha* = 1 EXACTLY, not 1.0002 — the reported 1.0002 was the root of the t<30-truncated series; M(1) = 1/4 + 3/16 + 9/16 = 1 is an exact rational identity.]
- **explore20.py**: DONE - **NEGATIVE RESULT**: Multi-step contraction FAILS. For NO fixed k does max_x L(F^k(x))/L(x) < 1. Worst-case L-ratios remain above 1 for all k=1..20, across all magnitude ranges [100, 10M]. The fraction of x with ratio > 1 decreases (28.6% at k=1 -> 0.88% at k=20) but worst-case values stay high (66x at k=20). Max consecutive growth hops: 10 (extremely rare, 3/250K). **Conclusion: pointwise k-hop contraction cannot prove Collatz.**
- **explore21.py**: DONE - **KEY FINDING**: Worst-case single-hop L-ratio GROWS with bit-length: 1.3 at 4-bit -> 42.2 at 21-bit. Numbers like 2^n-1 (high-t, minimal v_2=2) produce the worst cases. Growth anatomy: (t, v_2) decomposition shows growth when t is high and v_2 is small -- e.g., (t=6,v_2=2) gives mean ratio 12.8x. After growth, 33.6% still have two-hop ratio > 1. Peak L-ratio before eventual descent: 97.8x (x=159487, takes 12 hops). Max hops to L-descent: 32. Distribution: 64% descend in 1 hop, 83% in ≤2, 90% in ≤3. **The pointwise gap is REAL: average contraction is proven but worst-case growth is unbounded.**
- **explore22.py**: DONE - Growth phase structure. Max duration = 7 hops. 66.4% of phases are single-hop, 99.3% are ≤3 hops. Max total growth = 9.70 bits. **SURPRISE: t-values INCREASE within growth phases** (mean change +0.755, P(increase)=0.585). Growth bounded linearly by initial t: max ≈ (t+2)*0.585 for single hops, multi-hop phases can reach ~10 bits. 2^n-1 recovery times: 2^7-1 in 3 hops, 2^13-1 in 8 hops, 2^17-1 in 24 hops, 2^20-1 in 12 hops.
- **explore23.py**: DONE - 2^n-1 trajectory analysis. **F(2^n-1) is overwhelmingly Type A** (21/22 cases for n=3..24). First-hop ratio grows as ~(3/2)^n / 2^{v_2(3^n-1)-1}. Peak/start ratio grows with bit-length: max 13483x at 18-bit, avg stays ~3-4x. Some 2^n-1 trajectories pass through smaller 2^n-1 (e.g., 2^21-1 -> 31 = 2^5-1). v_2(FMF) for 2^n-1 follows pattern: 2 (n odd), v_2(n)+2 (n even). **Key: the big first hop almost always lands on Type A, guaranteeing immediate shrinkage next.**
- **explore24.py**: DONE - **KEY RESULT**: Epoch analysis (growth + recovery until descent below start). 100% descent rate (99,999/99,999). Epoch duration: mean=1.74, max=32, 71.4% descend in 1 hop. **Epoch duration / log2(x) ratio bounded by 3.15** (achieved at x=27). For x>1000, max ratio ~1.90. Recovery matches drift theory: recovery_hops ≈ peak_bits / 0.83. Growth phase mean 0.40 hops (most epochs don't grow!). Decomposition: growth is negligible (max 7), recovery dominates (max 31). Suggested C bound: epoch ≤ 4.73 * log2(x).
- **explore25.py**: DONE - **UNIVERSAL BOUND CONFIRMED** across 2917 tests spanning 3 to 60 bits. epoch_duration / log2(x) ≤ 2.83 globally (at x=31). For x > 10000, max ratio ≤ 1.63. For random 60-bit numbers, max ratio = 0.13. 2^n-1 tested up to n=44 (x~10^13): ALL descend, max ratio 1.41 (at n=17). High-t numbers (t up to 34): ALL descend. **The ratio DECREASES with magnitude** -- epoch duration grows as O(log x) but the constant shrinks. Random large numbers have avg epoch ~2 hops regardless of magnitude.
- **explore26.py**: DONE - **DETERMINISTIC PROOF ATTEMPT via Cesaro argument**. MIXED RESULTS: Cesaro argument fails (finite trajectories, ~0.3 error/hop). All product-of-ratios still converge.
- **explore27.py**: DONE - Growth phase mechanics: v_2 biased to 2 during growth (87.8%), m-values restricted to specific mod-8 classes, all long phases share "27 chain", P(continue|survived k) plateaus ~0.75, v_2 nearly independent (corr 0.035).
- **explore28.py**: DONE - Finite automaton has phantom cycles (7/8 at K=8). Actual trajectories don't follow them. Max growth phase: 37 hops (x=270271). mod-2^K too coarse.
- **explore35.py**: DONE - **m-TRANSFORMATION ERGODICITY**: Growth-B graph has ZERO cycles mod 2^K (K=4,6,8). 75-87% of states escape. m' = odd_part((3^(t+2)*m+1)/8). 3^a ≠ 2^b prevents exact cycles. t oscillates (t=0↔t=1). Proof outline written; gap is formal carry propagation argument.
- **explore34.py**: DONE - **GROWTH TERMINATION**: PROVED (mod 8) that P(output A | growth, v_2=2) = 1/2 exactly. Growth chains: P(continue)=0.356, max=7. Type A gap: mean=1.84, max=15. Remaining gap: m-evolution mod 2^K ergodicity.
- **explore33.py**: DONE - **CARRY PROPAGATION**: No carry invariant decreases monotonically. Growth = fewer carries (2.3 vs 4.2). Carry structure is consequence of 2-adic, not independent tool. Period-2 pattern of 3^{-n} in Z_2 noted.
- **explore32.py**: DONE - **MIXED-METRIC HEIGHT FUNCTION**: Optimal h = log2(m) + 2.1*t - 0.1*p. Violation rate 23.3% (vs 29.2% pure). Distinguishes 3n+1 from 5n+1 (mean delta_h -0.678 vs +0.327). Single-hop pointwise proof impossible. Multi-step violations decay exponentially.
- **explore30.py**: DONE - **5n+1 DISCRIMINANT**: 3 is the largest odd integer where a/4 < 1. Type A for 3n+1 always shrinks (ratio 3/4 < 1). Neither type shrinks for 5n+1. State-independence and v_2 geometric hold for BOTH maps. The structural difference is purely the contraction channel.
- **explore31.py**: DONE - **2-ADIC PROXIMITY CHAINS**: Proved v_2(inv_{t+1} - inv_t) = v_2(1-a) = 1 for a=3, 2 for a=5. Growth requires low proximity (p=1 in 79% of growth hops). Autocorrelation 0.20 -- proximity forgets quickly. Equidistribution of 3^n and 5^n mod 2^k identical (50% coverage). Open: does 1-bit inverse shift + m-value evolution guarantee p cannot stay small?
- **explore29.py**: DONE - **m-VALUE MAGNITUDE ANALYSIS**: (1) m grows +0.16 bits/hop during growth (t-dependent: t=0 shrinks -0.85, t=3 grows +3.52). (2) OVERALL m shrinks -0.72 to -0.80 bits/hop along full trajectories. (3) ALL longest growth phases (37 hops) share the same m-chain (192410→108231→11415→...). (4) Max m during growth bounded by ~10 bits above starting bit-length. (5) Fraction not descended by K hops decays exponentially: 28.6%→0.058% at K=20→0% at K=50. (6) Approximation m'≈3^(t+2)*m/2^(v+t'+2) has ~40% error (not O(1/m) as hoped). **HONEST ASSESSMENT**: We've identified the exact remaining gap -- going from average contraction to pointwise convergence -- which IS the fundamental difficulty of Collatz.

---

## Literature Review (critic.md)

A deep research review was conducted comparing this FMF framework against the published Collatz literature (Tao, Lagarias, Kontorovich, Carletti & Fanelli, etc.). Key findings:

- **FMF decomposition is genuinely novel** -- no published paper uses "first multiple of four" as the unit of analysis
- **Algebraic formulas (Theorems 1-4) are the strongest original contributions**
- **Average contraction results (drift, rho < 1) are equivalent to known heuristic calculations** rediscovered through a novel lens
- **State-independence (Theorem 12) is interesting** but related to Kontorovich-Lagarias residue class observations
- **Critical gap is the same as everyone else's**: pointwise convergence from average contraction
- **Tao's barrier**: any proof must engage with transcendence theory (separation of powers of 2 and 3)
- **5n+1 litmus test**: structural arguments (state-independence, rank-1) would hold for 5n+1 too -- only the drift sign differs. Framework must distinguish 3n+1 (convergent) from 5n+1 (divergent) via structure, not just drift.
- **Updated facts**: computational verification is 2^71 ~ 2.36x10^21 (Barina 2025); cycle lower bound is ~2.17x10^11 (Simons & de Weger)
- **Epoch bound is a reformulation, not a reduction** -- "every number descends" IS the conjecture

Full analysis in critic.md.

---

## Phase 7: New Directions (explore30+)

Based on literature review and gap analysis, five new exploration directions:

### explore30: 5n+1 Discriminant (PRIORITY 1) -- DONE
**THE DISCRIMINANT FOUND:** 3 is the largest odd integer where a/4 < 1. For 3n+1: Type A (x≡1 mod 4) gives IMMEDIATE FMF with ratio 3/4 < 1, **always shrinks** (P(shrink)=1.0). For 5n+1: the immediate FMF channel gives ratio 5/4 > 1, **always grows**. State-independence holds for BOTH (confirmed). v_2 distribution is geometric for BOTH. The structural difference is purely in the guaranteed contraction channel: only a < 4 (i.e., a=1 or a=3) has a/4 < 1. Drift decomposition: 3n+1 Type A = -1.415, Type B = -0.245, overall = -0.830. 5n+1 Type A = +1.322, Type B = -0.678, overall = +0.322.

### explore31: 2-Adic Proximity Chains (PRIORITY 2) -- DONE
**PROVED: Inverse Movement Theorem.** v_2(inv_{t+1} - inv_t) = v_2(1-a) for all t. For a=3: always 1 (minimum possible). For a=5: always 2. Algebraic proof: the difference is a^{-(t+2)} * (a^{-1} - 1) in Z_2, and v_2(a^{-1} - 1) = v_2(1-a)/v_2(a) = v_2(1-a) since a odd.

**Proximity dynamics:** Growth REQUIRES low proximity (p=1 accounts for 79.2% of growth hops). Shrinkage comes from high proximity (p>=3 for 67% of shrinkage hops). Autocorrelation is low (0.20) -- proximity sequence "forgets" quickly.

**Transition matrix P(p_{n+1}|p_n):** From p=1, 71.3% stay at p=1 (growth-sustaining) but 28.7% escape. From p=2, 66% jump to p=3 (shrinkage territory). No absorbing states in the growth region.

**Equidistribution:** Both 3^n and 5^n cover exactly 50% of odd residues mod 2^k (for all k tested). ord(3) = ord(5) = 2^(k-2) mod 2^k. Equidistribution alone doesn't distinguish them.

**Key difference from 5n+1:** For a=3, the inverse moves 1 bit per step (minimum); for a=5, it moves 2 bits. Combined with the 3/4 contraction channel (Theorem 30), the 1-bit shift means the target moves minimally, but 50% of hops bypass the proximity question entirely (Type A always shrinks).

### explore32: Mixed-Metric Height Function (PRIORITY 3) -- DONE
**Optimal h = log2(m) + 2.1*t - 0.1*p** (p = proximity). Violation rate 23.3% (vs 29.2% for pure log2(m)). Single-hop pointwise proof IMPOSSIBLE (growth unbounded for high-t, low-p). BUT: h DISTINGUISHES 3n+1 from 5n+1 (mean delta_h = -0.678 for 3n+1 vs +0.327 for 5n+1). Multi-step violations decay exponentially: 25.7% at k=1 -> 6.3% at k=10. The large gamma=2.1 coefficient shows t is the dominant growth driver. Proximity (beta=0.1) helps marginally but doesn't close the gap. CONCLUSION: no single-hop Lyapunov proof possible; need multi-step or different approach.

### explore33: Carry Propagation Analysis (PRIORITY 4) -- DONE
**NEGATIVE RESULT for proof.** No carry invariant monotonically decreases. Growth hops have FEWER carries (avg 2.3 vs 4.2 for shrinkage). 2-adic expansion of 3^{-n} has period 2 (...010101), 5^{-n} has period 4 (...11001100). Carry structure is a CONSEQUENCE of 2-adic structure, not an independent proof tool. The structural advantage of 3 remains in the ratio a/4 (Theorem 30), not in carry patterns.

### explore34: Rigorous Growth Phase Termination (PRIORITY 5) -- DONE
**PROVED (mod 8):** For growth hops with v_2=2, P(output Type A) = 1/2 EXACTLY. For each t, exactly 1 of 2 growth-enabling m-classes mod 8 gives Type A (guaranteed shrinkage), the other gives Type B. This is algebraic, not empirical.

**Growth chain statistics:** P(continue) = 0.356, max chain = 7, expected length = 1.55. P(chain >= k) ~ 0.36^k.

**Type A frequency:** mean gap = 1.84, max gap = 15 (across 200K starting values). 58.2% have gap=1 (immediate Type A).

**REMAINING GAP:** Need to show m-evolution doesn't systematically select B-producing residue classes. Phantom cycle exclusion (Theorem 28) handles finite state spaces. The infinite-state question reduces to: is the m-transformation mod 2^K ergodic?

### explore35: m-Transformation Ergodicity -- DONE
**KEY RESULT:** Growth-B transition graph has ZERO CYCLES mod 2^K for K=4,6,8. Growth-B states are NOT absorbing: 75-87% escape per step. The explicit m-map is m' = odd_part((3^(t+2)*m + 1)/8). No exact cycles possible (3^a ≠ 2^b). t-values oscillate (t=0->t'=1 at 74%, t=1->t'=0 at 91%), never grow unbounded.

**Proof outline** for growth termination:
1. Each growth hop is Type B (Theorem 30) ✓
2. Growth-B requires specific m mod 8 class ✓
3. No cycle in (t, m mod 2^K) state space (verified K≤8) ✓
4. m grows -> eventually leaves any finite state space ✓
5. GAP: need formal proof that carry propagation disrupts low bits

### explore36: Formal Equidistribution and Proof Closure -- DONE
**Growth-B orbits are SHORT:** max orbit in (t, m mod 2^K) = 3-4 steps (K up to 12). Growth chain length / log2(m) DECREASES for large m (from ~2.0 to ~0.1). The growth-B map covers ~23-25% of odd residues per step. 2-adic contraction fails (v_2(F(x)-1) doesn't increase).

**Complete proof structure assembled (6 proved lemmas, 1 missing):**
- Lemma A: Type A always shrinks (Th. 30) [PROVED]
- Lemma B: State-independence (Th. 12) [PROVED]
- Lemma C: Average contraction rho < 1 (Th. 19) [PROVED]
- Lemma D: Growth-B 50/50 A/B split (Th. 35) [PROVED]
- Lemma E: No cycles in growth-B map (Th. 36) [PROVED]
- Lemma F: No small cycles (external) [KNOWN]
- **Lemma G: Growth termination for ALL x [MISSING]**

**Lemma G reduces to:** proving the map m -> odd_part((3^(t+2)*m+1)/8) has no invariant subset in the growth-B domain of Z_2. This is the FUNDAMENTAL Collatz gap (pointwise vs average) narrowed to a precise 2-adic question.

### explore37: Compatibility Tree Density Decay -- DONE
**KEY RESULT:** Growth chain density decays as (1/4)^k, not (1/2)^k. Compatibility tree of growth-B chains mod 2^K terminates for ALL K tested (8-16). Max chain length mod 2^K grows as ~K/2. Per-step continuation probability P(continue) ≈ 0.25, decomposing as P(Type B output) × P(growth-B | Type B) ≈ 0.50 × 0.50. Verified exact density at K=16: chain≥1 = 0.25, chain≥2 = 0.0625, chain≥3 = 0.0155, chain≥4 = 0.0039, chain≥5 = 0.0009, chain≥6 = 0.0002, chain≥7 = 0.00003, chain≥8 = 0. Max chain_len/log2(m) = 0.59 for m > 1000. Proof attempt: density (1/4)^k + chain length O(log m). Gap: need ALGEBRAIC proof of (1/4)^k bound. The mod-8 halving (1/2) is proved (Theorem 35); the additional 1/2 from v_2 distribution needs formalization.

### explore38: Algebraic Proof of the 1/4 Continuation Rate -- DONE
**KEY RESULT: THE QUARTERING LAW.** P(continue growth-B) = 1/4 EXACTLY. Proved by combining: (i) Theorem 35 gives P(Type B output | growth) = 1/2 (ii) m' mod 8 is equidistributed from growth-B inputs (verified: each odd residue gets 25.0% at K=16, 20, converges to exact 1/4 at K=24). The equidistribution follows from the affine structure of m -> (3^(t+2)*m+1)/8 over Z_2. Mod-8 transition table: exactly 4/16 = 25% of growth-B (t, m mod 8) states continue. The decomposition: P(v_2=2) = 1/2 (half of odd m' have 3^(t'+2)*m' ≡ 3 mod 4) × P(Type B | v_2=2) = 1/2 = 1/4. REMAINING: formalize WHY m' mod 8 is equidistributed -- this follows from 3^(t+2) being a unit mod 2^K (so multiplication is a permutation), making the affine map m -> (3^(t+2)*m+1)/8 measure-preserving on Z_2.

### explore39: Formal Proof of P(continue)=1/4 (The Second 1/2) -- DONE
**LEMMA G CLOSED (pending one formality).** The full algebraic proof:
1. **v_2 geometric**: 3^(t+2) is a unit mod 2^K, so 3^(t+2)*m - 1 is uniform over even residues. P(v_2=j) = 1/2^j EXACTLY (verified 0 error at K=8,12,16).
2. **Type B | v_2**: Write 3^(t+2)*m-1 = 2^w*q. Bits w,w+1 are independent of bits 0..w-1. So q mod 4 is equidistributed => P(Type B | v_2=w) = 1/2 EXACTLY for every w (verified at K=12,16).
3. **Odd Part Equidistribution Lemma**: If q uniform mod 2^N, then odd_part(q) mod 2^j is equidistributed for j <= N-v_2(q). Pure counting argument.
4. **q uniform**: Growth-B gives q = (3^(t+2)*m+1)/8 uniform mod 2^{K-3} (unit mult + /8).
5. **m' mod 8 equidistributed**: From (3)+(4), m' mod 8 ∈ {1,3,5,7} each with P=1/4. Verified EXACT at K=12,16,20 for every t'.
6. **P(continue) = 1/4**: Growth-B selects 1/4 of odd m' mod 8. By (5), P=1/4. QED.

**Remaining formality:** The (1/4)^k bound uses independence across steps. State-independence (Th. 12) implies each step's continuation probability is 1/4 regardless of history, giving exact independence. One subtlety: density (1/4)^k → 0 proves the compatible SET shrinks, but connecting this to INDIVIDUAL trajectories requires noting that m's bit-consumption (2 bits/step) outpaces bit-growth (~1.17 bits for t=0), giving net precision gain of ~0.83 bits/step.

### explore40: Complete Proof Assembly and Gap Audit -- DONE
**HONEST ASSESSMENT.** All 12 key results proved. Zero non-descenders in [3, 500K]. P(descend) = 1.000000 across 250K epochs. The remaining gap: "average contraction + bounded growth + deterministic contraction channel => descent." This is NARROWER than Tao's barrier: Tao has only average contraction, FMF adds bounded growth (Lemma G), pointwise Type A contraction (Lemma A), and the quartering law (Theorem 40). The gap reduces to: proving that the bit-consumption (~1 bit/step from carry propagation) outpaces bit-growth (~0.17 bits/step from m growing), giving net 0.83 bits consumed per step, so after log2(m)/0.83 ≈ 1.2*log2(m) steps, the growth-B chain MUST end because all original bits are consumed.

### explore41: Bit Consumption vs Growth -- DONE
**KEY RESULTS:**
1. **Bit consumption**: E[t'] = 1.0000, average consumption = 4.0 bits/step, net = 3.83 bits/step after subtracting growth
2. **Carry depth D(j) = j + C**: excess is CONSTANT per t (C=14 for t=0, C=18 for t=1, C=15 for t=2)
3. **Growth-B orbit length**: max_orbit/K converges downward (0.60 at K=10 → 0.35 at K=20), suggesting O(K) bound
4. **0.55*log2(m)+3 bound**: 0 violations in 1.5M tests, max chain/log2(m) = 1.29
5. **Average chain length stable**: ~1.33 across all bit sizes (5-29), confirming chains are short
6. **HONEST GAP IDENTIFIED**: The precision argument (Step 4 of formal proof) is a counting/density argument, NOT a pointwise argument. The density (1/4)^k < 1/m for k > K/2 shows the compatible SET is empty among K-bit integers, but each step consumes ~3-4 bits of precision, so after B/3 steps the mod-2^B analysis loses resolution. The gap between trackable steps (~B/3) and the density bound (~B/2) cannot be closed by taking larger K.
7. **Proposed Theorem 41**: growth_chain_length <= 0.55 * log2(m_0) + 3. Formal bound derived from bit consumption vs growth rate: each step consumes 1 step of the bound but only adds 0.085 steps from growth, so bound decreases by 0.915/step. VERIFIED: 0 violations across ~1.5M growth chains in [3, 500K], max chain/log2(m) = 1.29.

**CRITICAL REASSESSMENT**: The proof claim in Lemma G needs correction. What is proved:
- P(continue growth-B) = 1/4 exactly [ALGEBRAIC]
- Density of chain ≥ k is (1/4)^k [ALGEBRAIC]
- Growth chains terminate for density-1 set of integers [PROVED]
- Growth chains terminate for EVERY integer [NOT PROVED -- same gap as Tao]
- Growth chain length bound 0.55*log2(m) [EMPIRICAL -- 0 violations but not proved]
- "Bounded growth + average contraction => descent" [CONCRETE REMAINING QUESTION]

The FMF Quartering Law gives elementary exponential decay, `(1/4)^k`, for the
strict growth-chain event. Later audit clarified that this should not be
compared as a direct strengthening of Tao's theorem, because Tao controls a
different orbit-minimum event. The "almost all to all" gap remains.

**What explore41 adds beyond explore40:** (1) Measured actual bit consumption per step (~4 bits, far exceeding growth of 0.17 bits). (2) Showed carry depth D(j) = j + C is linear (constant excess). (3) Proposed and verified the 0.55*log2(m) bound. (4) Identified the PRECISE mathematical gap: the mod-2^K analysis can track ~K/3 steps but needs ~K/2 for the density argument. (5) Showed the remaining question "bounded growth + average contraction => descent" is strictly narrower than Tao's barrier, since FMF has pointwise growth bounds that Tao doesn't.

### explore42: Ergodicity of FMF Map mod 2^K -- DONE
**NEGATIVE RESULT.** The FMF map mod 2^K is NOT ergodic:
- NOT injective (~half the nodes have in-degree 0)
- NOT strongly connected (almost all SCCs are singletons; biggest SCC = 6 at K=8)
- Attracting set is vanishing (12.5% at K=4 → ~0.05% at K=12)
- TV distance to uniform stays near 1.0 and WORSENS with K
- Max fraction of states visited by any orbit: 62.5% (K=4) → 1.6% (K=12)

**KEY INSIGHT:** Actual large-number trajectories visit far MORE residues than the mod-2^K orbit predicts. At K=4, all test numbers hit all 8 residues. This is because high bits change at every step, effectively jumping between branches of the mod-2^K tree. The equidistribution comes from the changing number, not from ergodicity of a fixed-modulus map.

**VERDICT:** Ergodicity cannot close the gap. The right approach is either: (1) a multi-scale argument where high-bit changes drive equidistribution, (2) an effective independence argument for consecutive outputs, or (3) a tree structure argument.

### explore43: 2-adic Expansion of Growth-B Map -- DONE
**KEY RESULT: Growth-B map is 2-adically EXPANDING, not contracting.**
- Expansion factor = 2^{3+t'} per step (at least 8, average ~16)
- Division by 8 increases 2-adic norm; odd_part adds 2^{t'} more
- Expansion matches theory EXACTLY for all (t, t') combinations
- Equidistribution mod 2^k is essentially perfect (chi-squared/dof near 0)

**CONSEQUENCE:** The expansion EXPLAINS the Quartering Law — expanding maps scramble low bits → equidistribution → each step's growth-B condition is effectively independent. No positive-measure invariant set can exist in the growth-B domain.

**LIMITATION:** Cannot rule out measure-zero invariant sets containing integers. Since Z ⊂ Z_2 already has Haar measure 0, the measure-theoretic conclusion doesn't transfer to "all integers."

### explore44: Sharp Almost-All Formalization and Tao Comparison -- DONE
**PRECISE STATEMENT OF WHAT IS PROVED:**
- Natural-density control for strict FMF growth-chain events, which are narrower
  than Tao's orbit-minimum event and therefore not directly comparable
- Exponential decay (1/4)^k for that isolated growth-chain event
- Elementary proof (mod-8 arithmetic vs 3-adic entropy)
- Corrected normalization after later audit: among all odd starts, strict
  growth-B chains of length at least k have density 4^-k; the expression
  2/4^k applies only after conditioning on a Type B start.

**EXCEPTIONAL SET IS PROVABLY INFINITE:**
- By pigeonhole: for C < 1, infinitely many n have chain ≥ C·log_4(n)
- This is NOT a bug — it's a structural feature of residue class arguments
- Baker's theorem cannot help: chain conditions are 2-adic, Baker is archimedean
- Max chain found: length 10 at x=162927, chain/log_4(N) ≈ 1.003

**BAKER'S THEOREM ANALYSIS:**
- Linear forms |a·ln(2) - b·ln(3)| for actual long chains are vastly above Baker's lower bound (e.g., 3.33 vs 1.68e-38)
- Baker bounds the wrong thing: it constrains real-valued proximity, but chain conditions are mod-2^K constraints

**HONEST ASSESSMENT:**
1. The Quartering Law + density corollary are rigorous, publishable results
2. The Tao comparison must be qualified because the FMF and Tao events are
   different; natural density is stronger only when the same event is measured
3. The "almost all → all" gap is a frontier problem in p-adic dynamics
4. No known tool (Baker, ergodic theory, 2-adic expansion) can close it
5. Closing requires new mathematics: effective equidistribution in Z_2, p-adic Littlewood-type results, or mixing estimates for the Collatz map
6. Publishable venues: Experimental Mathematics, American Mathematical Monthly, Integers

---

## Phase 8: Paper Writing

### Paper structure: /paper/main.typ (Typst)
- Current title: "First-Multiple-of-Four Coordinates for Collatz Growth Chains:
  Density Bounds and Pointwise Obstruction Reductions"
- 8 sections planned: Introduction, FMF Formulas, State Independence, Contraction, Quartering Law, Gap Analysis, Growth Bounds, Future

### Status
- **01-introduction.typ**: DONE - Covers conjecture statement, FMF idea, main results (Theorems A-D), honest framing of gap, paper outline. Citations: @tao2022, @lagarias2021, @barina2025, @simons2005.
- **02-fmf-formulas.typ**: DONE - Definitions (Collatz, v_2, Type A/B, T_i, FMF, hop map), Theorem A (FMF Step Formula) with full Case B2 proof, Lemma (v_2 of FMF via 2-adic inverse), Lemma (v_2(3^n-1)), hop map properties (Type A shrinkage, Type B growth, compression).
- **03-state-independence.typ**: DONE - Theorem B (State Independence) with full 4-step proof via 2-adic inverses, remark on Kontorovich-Lagarias, Observation (drift -0.830 bits/hop), Observation (self-correction after high-t hops).
- **04-contraction.typ**: DONE - Lemma (a/4 discriminant: 3 is largest odd < 4), Theorem C (Spectral Contraction, rho=0.8638 at alpha=0.53, alpha*=1 exactly — corrected July 2026 from the truncated 1.0002) with proof via rank-1 reduction, Lemma (inverse movement rate), remark connecting to Carletti-Fanelli.
- **05-quartering-law.typ**: DONE - Growth chain definition, 4 supporting lemmas (Growth-to-Type-A Split, v_2 Geometric Distribution, Type B Conditioned on v_2, Odd Part Equidistribution), Theorem D (Quartering Law: P(continue)=1/4, delta_k=2/4^k), Proposition (2-adic Expansion: factor >= 8, explains equidistribution), Lemma (Growth-B Acyclicity: zero cycles for K=4,6,8, 3^a != 2^b).
- **06-binary-return-codes.typ**: DONE - Binary return-code reductions, terminal-window estimates, bounded-alphabet obstruction classes, balanced/Sturmian and small morphic-template exclusions.
- **07-reduced-gap-codes.typ**: DONE - Reduced `{0,1}` gap partial map, terminal-window estimates, prefix minima, and low-window/rank criteria.
- **08-endpoint-dynamics.typ**: DONE - Reduced-gap endpoint dynamics, growth-B coding endpoint, terminal-tail formulation, and reset-spike dichotomy.
- **09-gap-analysis.typ**: DONE - What IS proved, what is NOT proved, Tao comparison, 5n+1 litmus test, why the gap is hard, precise remaining question, honest summary.
- **10-growth-bounds.typ**: DONE - Observation (Epoch Duration: <= 2.83*log2(x), 100% descent, ratio decreases), Observation (Growth Phase Structure: max 7 hops, 66.4% single-hop, t increases within phases), Observation (2^n-1 Trajectories: 21/22 Type A, recovery scaling), Conjecture (Growth Chain Bound: 0.55*log2(m)+3), Observation (Bit Consumption: ~4 bits consumed, ~0.17 bits growth per step).
- **11-future.typ**: DONE - Future directions: effective equidistribution, invariant sets in Z_2, critical-series landing, uniform terminal-window counting, and computational extensions.

---

## Phase 9: Multi-Agent Audit and Novel-Attack Session (July 19, 2026)

A two-workflow swarm session (7 verification agents, 11 attack agents, adversarial
refuter pairs for every claimed result) independently re-verified the proved core
and attacked the open gaps. Findings recorded here as they land; full structured
outputs in the session scratchpad and task files.

### Audit verdicts (all claims independently re-implemented from scratch)
- **fmf-algebra: CONFIRMED.** Theorems A/1-4 exact; universal-in-m parametric check
  for every t=1..300, exhaustive to 2e6, random 2^64, engineered v_2 up to 129.
  Zero discrepancies. (Fixed: parity-label typo in proof.md Theorem 1 proof.)
- **state-independence: CONFIRMED.** Exact counts verified at K=18,22 for t=0..8;
  paper framing honest (density, not trajectory independence).
- **contraction: CONFIRMED with one real error found.** M(0.53)=0.8637601186...
  correct; rank-1 argument valid; BUT **alpha* = 1 EXACTLY, not 1.0002** —
  M(1) = 1/4 + 3/16 + 9/16 = 1 is an exact rational identity (the 1.0002 was the
  root of explore19.py's t<30-truncated series). Paper + logs corrected.
- **quartering-law: CONFIRMED.** Exact 4^-k densities verified at K=20,24; paper
  normalization correct; shadow construction verified hop-by-hop. Presentation
  gaps noted (cylinder single-AP lemma + countable additivity should be explicit).
- **reductions (paper Sec 6-8): CONFIRMED as exact equivalences.** Full chain
  re-implemented independently; constants re-derived (2/15 = sum 2^-(4r+3),
  1/112 = sum 2^-(3k+7)); all six repo verifiers pass; two one-line proof
  repairs noted (strict M_w > -1; density countable additivity).
- **repo-verifier: PASS** (35/35 steps, quick mode, ~65-88s).
- **claim-architecture: SOUND & HONEST**, with the sharpest caveat: completion-gate
  step 4 (bounded-depth -> all mixed epochs) has NO writeup anywhere — it is a
  second major gap behind the rank conjecture; W_G is logically redundant given
  W_R (the {0,1} gap system is a sub-case of the return system).

### New results from attack agents (each survived 2 adversarial refuters unless noted)
- **q=9 boundary word EXCLUDED (PROVED, refereed x2).** The last open uniform-morphic
  boundary case (0->011111111, 1->100000000; base-9 digit-parity word) has NO
  positive ordinary reduced-gap code (corollary: no return code). New tool:
  **factor-recurrence height barrier** — applies the gap shift-code recurrence +
  forced-orbit prefix equivalence to two occurrences of an ARBITRARY factor
  (incl. overlapping), vs the repo's initial-prefix-only barrier. The scaled 8th
  power B_t^8 at positions 9^t and 2*9^t forces prefix modulus 2^(68*9^t+12*(-7)^t)
  against orbit growth A*3^(12*9^t)/2^(17*9^t), i.e. A > 2^(55*9^t) for all t —
  impossible. Also computed the word's initial recurrence function EXACTLY:
  min sigma(l)/l = 17/2 globally, proving the old initial-prefix route was
  structurally dead (needed < 8.41772).
- **Complexity threshold theorem (PROVED, refereed x2).** New Same-Factor
  State-Separation Lemma + occurrence-counting bound: every {0,1} return landing
  word must have liminf p(m)/m >= T_R in (3.1493, 3.1494); every {0,1} reduced-gap
  landing word needs liminf p(m)/m >= T_G in (6.2390, 6.2391). Subsumes the
  periodic/Sturmian/low-complexity/bounded-defect exclusions in one stroke and
  independently re-closes q=9 (its complexity is p(m)=4(m-1) < 6.239m). The open
  {0,1} regime is now: aperiodic words with liminf p(m)/m above ~3.15 (return) /
  ~6.24 (gap).
- **First unconditional unweighted rank-type bounds (AP Survivor Theorem,
  REFEREED July 21 — CONFIRMED).** W_R(B,L) <= C((B+1)2^(-2.1L) + 2^(0.9L)) and
  W_G(B,L) <= C(B*2^(-5.46L) + 2^(1.54L)) uniformly — exponential main term with
  no expansion cutoff, via first-block AP decomposition; survivor exponent floors
  alpha_R = 0.287761, alpha_G = 0.212323. Referee independently re-derived every
  constant, reran the recursion to N=10^8, and brute-forced W_R to B=2^18, L=12
  (bound holds with C≈0.11 vs claimed 4.46). PLUS the saturation obstruction:
  CONFIRMED as stated in the theorem (translate-invariant counting can never
  reach C(B+1)theta^L; witness A*(1,L)=1 via 8^L-1), but the informal summary's
  "includes all second-moment/Cauchy-Schwarz/large-sieve variants" is a scope
  overclaim (minor): only their TRANSLATE-INVARIANT forms are foreclosed;
  position-aware sieve arguments exploiting the anchored range [0,B] remain
  open — indeed they are exactly what the obstruction says a proof must use.
  Also CONFIRMED: ANY uniform bound with g(L)->0 suffices downstream (sharp
  bases 2/15, 1/112 not needed); note the AP Survivor bound itself does NOT
  satisfy g->0 (the 2^(0.9L) term diverges), disclosed by the claimant.
- **5n+1 litmus on the endgame (REFEREED July 21 — CONFIRMED): the rank
  conjecture is 3-FREE.** The return/gap gate moduli, 2/15 and 1/112 constants,
  quartering 1/4, terminal windows, and periodic exclusions all transfer VERBATIM
  to 5n+1 (P_r = 25·125^r, D_r = (160·125^r-51·16^r)/109 change; the dyadic
  structure — Q_r = 2^(4r+3), elementary denominators (8,16,8,16) — doesn't).
  Referee re-derived the a=5 block coding from scratch, confirmed the survival
  bases are purely 2-adic (2/15 = (1/8)/(1-1/16), 15 = 2^4-1 not 3·5; the
  multiplier only shifts odd gate residues), and confirmed F_5(13)=13 (a genuine
  5n+1 cycle with v_2(FMF)=5, OUTSIDE every excluded symbolic class) and the
  divergent orbit of 7 (+0.6439 bits/hop, matching 2log2(5)-4). So W_R/W_G rank
  bounds alone can never imply convergence; the excluded classes are consistent
  with both convergence and divergence, and the constant 3 (a < 4, the only
  a-dependent levers being (ax+1)/4 < x and drift 2log2(a)-4) must enter at
  completion-gate step 4 (mixed recovery epochs), which has no writeup. One
  framing overreach withdrawn: referee-brief.md/proof-obligations.md already
  state rank is necessary-not-sufficient ("at minimum ... or a different
  pointwise theorem"), so the claim's documentation flag was too harsh; no repo
  artifact is refuted — every Sections 5-8 theorem is correct, just
  multiplier-independent.
- **Literature sweep:** Barina 2^71 still the record (2026-07); arXiv:2601.03297
  v5 DOWNGRADED its finitely-many-cycles claim to conditional — must not be cited
  as unconditional; no post-Tao density improvement exists; relevant tools located:
  Charlier-Rampersad-Shallit computable recurrence constants for k-automatic
  sequences, Chen-Winterhof 2025 2-adic transcendence of automatic sequences,
  Adamczewski-Faverjon Mahler method. (Its one structural side-claim was REFUTED
  by both referees — odometer coding counterexample was miscategorized.)
- **Terras parity-vector program (REFEREED July 21 — split verdict, core
  CONFIRMED):** exact maximal descent-
  certificate frontier to n=28 = OEIS A076227 with ZERO additive failures =>
  every x>=2 with coefficient stopping time tau(x)<=28 has sigma(x)=tau(x)
  (bounded-horizon verification of Terras' open CST conjecture, complementary to
  bounded-x checks). Hybrid FMF+parity certificates provably gain NOTHING at any
  horizon (FMF hops ARE parity certificates in different coordinates — explicit
  bijection). FMF single-hop certificates plateau at density 0.85686...; full
  parity certificates -> 1. Paradox-size bound: enumeration of paradoxical values
  for all 7 known paradoxical pairs is PROVABLY COMPLETE (max bound 2^38.3 << 2^71).
  Negative delimiter: uncertified frontier grows ~1.93^n forever — no finite-
  modulus certificate scheme can close the pointwise gap.
  Referee outcome: both referees independently reverified the computations; one
  refuted-as-stated (fixable) on two points now withdrawn: Theorem H(c)'s
  backward direction was labeled proved but is unproven (non-load-bearing side
  statement), and the "bounded horizon, all x" CST lemma is classical (Terras
  1976 machinery), so its novelty framing was dropped. Everything load-bearing
  stands.
- **Tao renewal interface (REFEREED July 21 — CONFIRMED x2, minor):** PROVED
  renewal correspondence —
  FMF hops = renewal blocks of Tao's Syracuse valuation sequence at letters >= 2;
  every FMF density law is a functional of the iid-Geom(2) layer that is already
  exact in Tao's framework. Mapped exactly where log density enters Tao's proof
  (Archimedean spread exp(O(sqrt n)) after (1.17) + Prop 1.11 quasi-invariance);
  natural-density upgrade reduced to two sharply-stated lemmas (tilted Prop 1.17
  for Geom(mu), mu~2; first-passage stabilization from uniform windows), with the
  k <= n^(1/2-delta) regime PROVED to follow from Tao's published results.

### July 21 completion round (resumed workflow; all results refereed x2 unless noted)
- **Theorem G — ALL uniform-morphic templates excluded at once (automata-tag,
  CONFIRMED x2, minor):** every binary fixed point of EVERY q-uniform morphism
  (all q >= 2 simultaneously, no aperiodicity/primitivity hypothesis) admits no
  positive ordinary reduced-gap or return code (certificates A > 2^(3*q^t),
  M+1 > 2^(q^t) for all t). Coding corollaries: fixed points over alphabets
  <= 6 letters (gap) / <= 3 (return); every binary q-automatic gap word with a
  <= 6-state msd-first DFAO, any q. Subsumes the repo's separate q=2..6
  classifications AND the q=9 boundary word (one-copy streamlining of the 8-copy
  proof) in one stroke. Also: exact closed-form recurrence function for the q=9
  word, R(n) = 747*9^k + n - 1 on bands [9^k+2, 9^(k+1)+1], R(n) <= 748n-1
  sharp; initial-prefix recurrence tau(n) >= 8.5n with liminf exactly 17/2,
  PROVING the old density-recurrence route could never close q=9 — it fails by
  exactly the Pythagorean comma 3^12/2^19.
- **Transfer-operator program: rigorous NEGATIVE result (no claims — nothing to
  refute):** the spectral route provably cannot close the pointwise gap. The
  Syracuse/FMF transfer operators are exactly nilpotent-plus-rank-one at every
  finite level (spectrum {1} u {0}); Hoelder gap g_alpha = 1/(2^(1+alpha)-1)
  (=1/3 at alpha=1) with FMF gap = g^2 = 1/9 (exact squaring identity). Three
  proved obstructions: (1) operator-level 5x+1 litmus — ALL 2-adic transfer
  data identical for every odd multiplier q; (2) dense null trichotomy —
  reach-1 (countable dense), divergence-type (uncountable dense), and extra
  ergodic measures coexist on mutually dense Haar-null sets, so a.e. is
  topologically optimal (no continuity/norm upgrade to everywhere); (3)
  Berg-Meinardus truncation space grows linearly ~N/6 (verified to N=3e6) —
  no certified finite truncation. Only 3-specific spectral quantity found:
  L2-criticality sum 4^-k = 1/3 = |3|_3 exactly.
- **Diophantine cycle bounds at the 2025 floor (CONFIRMED x2, fixable
  constants):** the 2^71 verification floor does NOT extend Hercher's m <= 91
  m-cycle exclusion — the unique surviving candidate is the 43rd convergent of
  log2(3), (K,L) = (205632218873398596256, 120287136981023372109), whose gap
  6.24e-43 sits 5.1x below the achievable width floor; m=92 becomes excludable
  iff the floor reaches 2^73.869. Conditional milestone map computed
  (2^74 => m<=92 ... 2^90 => m<=122); binding obstructions are exactly the
  convergents before the large partial quotients 37, 55. NEW IDENTITY (proved):
  the Simons-de Weger m-cycle count EQUALS the number of FMF hops — so the
  current record reads "every nontrivial Collatz cycle makes >= 92 FMF hops."
  All-growth-B cycles impossible; the 3n-1 map's 17-cycle is an all-B 2-hop
  cycle, so no sign-agnostic argument can force a Type A hop.
- **Certified-descent record (CONFIRMED x2, minor): sigma(x) = kappa(x) for
  EVERY odd x > 1 with coefficient stopping time kappa(x) <= 301,993** (Terras
  steps; 492,529 in single-step convention) — a new self-contained pointwise
  descent record, extending Terras 1976 (2,593) x116 and Garner 1981 (64,508,
  conditional) x4.7. Method: proved threshold lemma (exceptions <= B(m)), exact
  integer ledger Theta(301,993) = 10,824,133,905, zero-exception scan of 1.35e9
  candidates. Equivalent form: for every n <= 301,993, every odd x > 1 outside
  the explicit ballot family B_n mod 2^n (|B_n| = A076227(n), density
  < 2^(-15,093) at the top horizon) descends below itself within n steps,
  uniformly in x. Corollary: every nontrivial cycle has Terras length > 301,993
  (noted: cycle bounds via Hercher are stronger). PLUS exact structure of the
  uncertified tree: ballot characterization, 1-or-2 branching with deficits at
  Beatty jumps of log_3 2, no leaves, an uncountable Cantor set of box dimension
  in [0.946954, 0.949956] — and a REFUTATION of the conjecture that the
  uncertified tree is the closure of FMF growth-B patterns (strict inclusion,
  exponential gap: Narayana growth 1.46557 vs gamma >= 1.9279). Conditional on
  Rozier-Terracol (Discrete Math. 2026) the horizon extends to 665,684,250.

### July 21 endgame round (3 focused attacks on the surviving leads; ALL refereed x2, minor findings only)
- **Mixed-epoch bridge — the missing completion-gate step 4 now EXISTS.**
  Mixed recovery epochs formalized exactly as (s,v) hop words (s=v_2(x+1),
  v=v_2(FMF)); every finite hop word occupies exactly one residue class mod
  2^(H+1) — generalizing the growth-B shadow theorem to ARBITRARY mixed
  patterns (no finite forbidden-pattern strategy can work). **Theorem R
  (two-lemma reduction, PROVED):** [H1: no infinite positive orbit of the
  binary return map T] + [Lemma E] => pointwise FMF descent => Collatz.
  **Lemma E, stated precisely for the first time:** every non-descending FMF
  orbit is eventually a depth-{0,1} growth-B chain. E's 5n+1 analogue is FALSE
  (witness F_5(13)=13, letter (3,5)) — E carries ALL the 3-dependence, exactly
  as the litmus demanded. Supporting new theorems: **Lemma P** (unconditional,
  one paragraph): no infinite positive orbit of m'=(27m+1)/16, via the exact
  identity 16(11m'+1)=27(11m+1) forcing v_2(11m_0+1) >= 4k; ballot inequality
  for non-descending prefixes (S_N/N >= log_{3/2}2 ~ 1.7095 — the coefficient
  2-log2(a) flips sign at a=4, the exact entry point of the constant 3);
  bounded depth-sum orbits descend with effective bound l <= 1+1.4094*T';
  eventually-periodic hop words are exactly cycles (expanding case impossible
  by a sign/valuation argument), so no divergent orbit has an eventually
  periodic hop word. New exact identity: alpha_R = log2(1/y), y^3+y^4=1 —
  the rank program's entire scope has box dimension 0.2878 versus >= 0.9470
  for the uncertified Cantor set Lemma E must empty: the rank conjecture
  addresses a dimension-0.288 slice of a dimension-0.947 problem.
- **Tao natural-density lemma S4 essentially RESOLVED.** Theorem S4-T (proved
  by complete tilt-dependence audit of Tao Section 7): tilted Prop 1.17 holds
  for Geom(mu)-driven Syracuse characters uniformly on every compact of the
  contractive regime q in (q*,1), q* = 1-log2/log3 — the prior k <= n^(1/2-d)
  restriction is REMOVED for all tilts the program needs; joint affine version
  (Tao's Remark 1.16 object) comes at zero extra cost. Sharp negative: Prop
  1.14's collision-entropy step is EXACTLY critical at mu=2 (poly(k) iff
  q=1/2) — it survives precisely the shrinking tilts |q-1/2| <= K/sqrt(k)
  needed and provably fails for fixed tilts. S5 (first-passage stabilization)
  precisely formulated; combinatorial kernel proved (exhaustive fiber
  bijection), analytic input proved via Rhin's effective irrationality measure
  (log^-0.131 x equidistribution); what remains is a write-up-scale rebuild of
  Tao's Section 5 bookkeeping — no obstruction identified, but NOT proved.
  Even full S4+S5 yields natural-density almost-all, not all.
- **Position-aware rank counting: DEFINITIVELY resolved, negatively — with
  exact two-sided theorems.** (T1) Thick-word floor W_R(B,L) >= C(L+s,s):
  sup_L W_R(B,L) >= B^(alpha_R-o(1)) inside the anchored window, so the
  AP-Survivor exponent (floor alpha_R = 0.287761 = -log2 y, y^3+y^4=1) is
  OPTIMAL even for position-aware counting. (T2) The base 2/15 is EXACTLY
  critical: for every rho < 2/15 the bound C(B+1)rho^L is FALSE along
  (L,B)=(15s, 2^(49s)) via the exact identity 16H(1/16) = 49+15·log2(2/15);
  at 2/15 the floor ratio is Theta(s^-1/2). Gap analogue: 1/112 exactly
  critical (8H(1/8) = 52-7·log2(112)). (E) The per-B decay target is
  EQUIVALENT to mu_L -> infinity — sufficient downstream but not one bit
  easier. (BLOCKING) Every interval+AP class-counting certificate is >= 1
  for all (B,L) via the r=0 chain (witness: true W_R(100,3)=0, certified >=1)
  — no such scheme can prove H_R(B) < infinity for ANY B. The positional
  deep-gate cutoff is real (16^r > 33B+32 => empty) but the 2^(0.9L) defect
  is the thick-class count, positionally irremovable. 5n+1: transfers
  verbatim, expected and consistent.

### July 21 round 4 (S5 completion, Lemma E, complexity pincer; artifacts in notes/round4-july2026/)
- **THEOREM ND (candidate): natural-density upgrade of Tao's theorem —
  claimed PROVED, refereed x2 (both NOT-REFUTED, minor), AWAITING HUMAN
  REVIEW.** Statement: {N : Col_min(N) > N0} has upper natural density
  <= C·log^(-1/25) N0; hence Col_min(N) <= f(N) for almost all N in NATURAL
  density, every f -> infinity. Three new proved components: Lemma P7 (Tao's
  Section-7 majorant bounds s-pinned character sums for free — total valuation
  is measurable w.r.t. his pair-sum conditioning); Lemma J* (fine-scale mixing
  of the ENTIRE affine map (S_n, X_n) — exactly the object of Tao's Remark
  1.16, which Tao called "plausibly attainable"; proof reruns his Section 6
  with the phase riding along; the collision-entropy criticality never
  activates because unitary phases are free in L2); Lemma R (pinned-sum
  renewal-equidistribution with limit 1/ln(4/3), driven by Rhin's
  irrationality measure of log2(3)). Glued by uniform-window Prop 5.2-U; the
  limiting first-passage measure is IDENTICAL to Tao's log-density one. Both
  referees verified every Tao citation verbatim against the local v7 text and
  reran all scripts. Full 571-line manuscript:
  notes/round4-july2026/s5-completion/PROOFS.md. **This is a candidate
  manuscript, not established mathematics, until a human analytic number
  theorist reviews it. It does not change proof-obligations.md.**
- **Lemma E partials (refereed: load-bearing content confirmed x2; one
  side-clause LE1(c) needs a one-line trivial-cycle carve-out).** New:
  hop-word factor barrier (effective complexity threshold for bounded-alphabet
  non-eventually-periodic hop words); depth-{0,1,2} words need liminf
  p(m)/m >= 3/log2(41/16) = 2.20986 — first proved slice of E strictly beyond
  depth {0,1}; complete invariant table for (s,v) block maps (depth-2 analogue
  of Lemma P: 32(49m'+1) = 81(49m+1), invariant 7^2; general d_s = 3^s-2^(s+1);
  block-power lemma kills all u^infty tails with |u| <= 91 via Hercher, and
  all-expanding u unconditionally); reduction R_2: H1^(0){0,1,2} + H1^(1){1,2}
  + E_2 => Collatz. NEGATIVE: rigorous LP no-go — the ballot inequality
  constrains letter frequencies only via the expanding/contracting dichotomy;
  exact witnesses reach non-G01 density 1, so NO statistical/frequency
  quantitative form of E exists. E remains open in the high-complexity and
  unbounded-alphabet regimes.
- **Complexity pincer: PROVABLY IMPOSSIBLE (negative result, no claims).**
  The ambient language of both coding systems is the FULL shift (every binary
  word occupies one nonempty residue class; entropy log 2); every infinite
  word — including p(m) = 2^m ones — is the exact itinerary of a unique
  2-adic seed. Any complexity upper bound would need positive-integrality of
  the seed = H1 itself. SALVAGE: sharpened effectivized thresholds
  T_R' = 3.2439007 (return), T_G' = 6.3942268 (gap) — improving the refereed
  3.1493/6.2390, now pointwise and density-coupled, with uniform-density floor
  7.5691 for both systems; genuinely 3-dependent (T_R'(a) = 3/(5·log2(a)-7)
  vacuous exactly at a >= 4 — litmus passed). Empirical: beam minimizers to
  L=120 have max p(m)/m <= 2.11, far below thresholds — the low-residue
  frontier is locked in the already-excluded low-complexity regime.

### July 21 round 5 (the last two untried routes; artifacts in notes/round5-july2026/)
- **Two-prime pincer on H1: PROVED exactly VACUOUS (definitive negative
  result).** New **Mirror Equivalence Lemma** (one-line proof, machine-verified
  2184 words, both a=3 and a=5): the auxiliary state U_N of the least 2-adic
  prefix residue EQUALS the least nonnegative residue V_N of the composed
  3-adic class mod 3^(2N+3S_N) — the 3-adic and 2-adic prefix data are the
  same information under an explicit affine bijection (stronger than CRT
  independence). **Theorem V (two-prime vacuity):** "3-adically consistent
  with positive states below the envelope of M" <=> R_N <= M, verbatim the
  rank condition (398,480 checks, 0 violations); the per-block 3-adic
  consistency fraction is exactly 1, so no such pincer can ever prune the
  word tree — the route collapses onto the rank program already proved
  optimal (Thms 48/57). Kill census over 10^6 seeds: all kills are 2-adic
  gate failures (7/15 + 6/15 per step), zero positivity kills, zero 3-adic
  kills; a-blind (5-adic mirror for 5n+1 identical, dictionary 11<->109,
  85<->51). Salvage: exact two-prime information ledger (letter r = 4r+3 seed
  bits forward, 3r+2 state trits backward; the state's low ternary digits
  spell the REVERSED recent word) and a new equivalent "mirror form" of H1 as
  a small-least-residue statement mod powers of 3 with 2-power denominators —
  landing exactly in the Erdos-Lagarias ternary-digits-of-2^n / Furstenberg
  x2x3 rigidity problem class.
- **Arithmetic route to Lemma E (refereed x2, minor): mechanism completely
  mapped; core reformulated; one new unconditional exclusion.** A1 (cocycle):
  (D,B) compose by the twisted cocycle B_uw = 3^(S_w) B_u + 2^(H_u) B_w;
  Lemma P is the power-degenerate case. A2 (master identity):
  v_2(D_p x_0 - B_p) = H_p + v_2(x_0 - x_k) for every prefix — every prefix
  is an exact divisibility on one integer. A3 (classification): fixed-form
  Lemma-P-style certificates exist IFF the word's 2-adic seed is RATIONAL;
  for irrational seeds the mechanism provably cannot apply; recognizing
  aperiodic rational-seed words is the Lagarias periodicity conjecture.
  B (reset law, proved): intervening letters RESET (not shift) the
  divisibility accumulation via the Wronskian trichotomy
  nu' = min(nu, omega) - H_m with omega given by a closed formula; the
  residual core of Lemma E is precisely "infinitely many exact valuation
  coincidences = 2-adic near-approaches to eventually-periodic rational
  seeds," with orbit SIZE the only non-circular lever. NEW UNCONDITIONAL:
  **spike-ledger theorem** — all hop words whose depth spikes outrun the
  drift budget at geometric ratio > log2(3) are excluded (sharp boundary,
  multiplier-covariant): a new proved slice of the unbounded-alphabet branch.
  Hierarchy pincer: definitively impossible (transported thresholds
  T_block(d,D) strictly DECREASE with depth, vacuous at d >= 13).
- **Net position after round 5: every defined attack route has now been run
  to a refereed theorem or a proved dead end.** H1 in mirror form sits in the
  Furstenberg x2x3 / Erdos ternary-digit rigidity class; Lemma E's core is a
  2-adic Diophantine-approximation statement tied to the Lagarias
  periodicity conjecture. Both are recognized frontier problems; no further
  structural lever inside the framework is known.

### Corrections applied to repo this session
- paper/sections/04-contraction.typ: alpha* = 1 exact + rational identity + tail
  bound making M(0.53) < 1 a proved statement (was "numerical evaluation").
- paper/sections/09-gap-analysis.typ: same correction.
- proof.md: alpha* corrections (2 sites) + Theorem 1 proof parity-label typo.
- plan.md: explore19/04-contraction entries annotated with the correction.
- Paper recompiles clean (typst compile OK).

### Still open after this session
- The pointwise gap stands. Sharpened to: (a) {0,1} landing words with
  liminf p(m)/m above the new thresholds AND outside every uniform-morphic
  fixed-point/coding class (Theorem G); (b) unbounded-alphabet/reset-spike
  branches; (c) completion-gate step 4 (mixed epochs) — where the constant 3
  MUST enter (5n+1 litmus, confirmed at both counting and operator level); (d)
  the unweighted rank bound at base < 1 (AP Survivor gives exponential main term
  but with additive 2^(0.9L) defect term; any g(L)->0 bound suffices, and the
  proof must be position-aware — translate-invariant schemes provably saturate).
- Routes PROVED unable to close the gap (negative delimiters, this session):
  finite-modulus certificate schemes at any horizon (uncertified frontier grows
  ~1.93^n; uncertified tree is an uncountable Cantor set); 2-adic transfer-
  operator/spectral arguments (operator data is multiplier-blind; a.e. is
  topologically optimal on Z_2); Berg-Meinardus truncation; density-recurrence
  prefix barriers for q=9 (blocked by the Pythagorean comma); translate-
  invariant window counting; Baker/archimedean bounds (wrong metric).
- Most promising open leads: the two sharply-stated lemmas that would upgrade
  Tao's theorem to natural density (tilted Prop 1.17 + first-passage
  stabilization); position-aware terminal-height counting for the rank bound;
  mixed-epoch writeup where a < 4 enters; extending Theorem G from uniform-
  morphic to general morphic/automatic landing words.

### July 31, 2026 — consolidation round (no new mathematics)

Integrated the July 19-21 refereed campaign into the repository's public-facing
artifacts via a 4-agent workflow (3 writers + 1 claim-boundary reviewer):

- paper/sections/12-july2026-addendum.typ (new, ~7 pages) wired into main.typ:
  addendum with the campaign's theorem statements and proof sketches (Thms 46-49,
  51, 53-55, 57, 60-62 in proof.md numbering), plus a clearly-flagged final
  remark that the Theorem ND natural-density upgrade is CANDIDATE-only.
- Claim-boundary docs updated: proof-obligations.md (12 new established rows,
  gap restated as H1 + Lemma E, candidate table for Thm ND), referee-brief.md,
  publication-readiness.md, diagnostics.md (notes/ script index).
- notes/round4-july2026/s5-completion/REFEREE-PACKAGE.md (new, ~300 lines):
  human-referee package for Theorem ND — statement + roadmap, 19-row Tao v7
  dependency table, 8 risk-ranked verification targets, script index with
  expected outputs, honest provenance cover note.
- Review agent findings (all fixed in place): the addendum preamble had
  over-claimed "refereed x2" for Thms 60 and 61 (machine-verified negative
  results, no separate referee records) — carved out; same over-attribution
  fixed in proof-obligations.md, diagnostics.md, publication-readiness.md;
  one wrong section cross-reference fixed. 30+ constants spot-checked, zero
  errors. typst compile clean; bash scripts/verify_snapshot.sh quick passes.

Referee-status ledger (for future claim hygiene): Thms 45-49, 51-57, 59, 62
refereed (48/49 single-pass, rest x2); Thms 60, 61 proved + machine-verified
but NOT separately refereed; Thm 58 (ND) candidate-only, awaiting human review.

Repo state: all changes uncommitted (commit only on request). Next human
decisions unchanged: human expert review of the ND manuscript (start at
REFEREE-PACKAGE.md), then whether to publish the addendum.
