# Collatz Mod-4 Exploration Plan

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
- **explore19.py**: DONE - **MAJOR RESULT**: Analytical transition matrix computation. Confirmed **rho(T) = E[R^alpha]** exactly, because T is rank-1 (state-independence). Theoretical alpha* = 1.0002 (E[R^alpha]=1). At alpha=0.53: theoretical rho = 0.8638, matching empirical perfectly. **Key formulas**: E[R^alpha|A] = (3/4)^alpha * sum_v 2^(-v*alpha) * P(v), E[R^alpha|B(t)] = ((3/2)^(t+2))^alpha * same v-sum. The v_2 distribution for both A and B types follows exact geometric P(v=j)=1/2^j. Since T is rank-1, rho = trace = E[R^alpha] = P(A)*E[R^alpha|A] + sum_t P(B,t)*E[R^alpha|B(t)]. This converges for all alpha < alpha* because EACH TERM is computed from the EXACT 2-adic distribution, not finite samples. **This closes the convergence gap**: the transition matrix entries ARE their limiting values because they're determined by the 2-adic structure (Theorem 12).
- **explore20.py**: DONE - **NEGATIVE RESULT**: Multi-step contraction FAILS. For NO fixed k does max_x L(F^k(x))/L(x) < 1. Worst-case L-ratios remain above 1 for all k=1..20, across all magnitude ranges [100, 10M]. The fraction of x with ratio > 1 decreases (28.6% at k=1 -> 0.88% at k=20) but worst-case values stay high (66x at k=20). Max consecutive growth hops: 10 (extremely rare, 3/250K). **Conclusion: pointwise k-hop contraction cannot prove Collatz.**
- **explore21.py**: DONE - **KEY FINDING**: Worst-case single-hop L-ratio GROWS with bit-length: 1.3 at 4-bit -> 42.2 at 21-bit. Numbers like 2^n-1 (high-t, minimal v_2=2) produce the worst cases. Growth anatomy: (t, v_2) decomposition shows growth when t is high and v_2 is small -- e.g., (t=6,v_2=2) gives mean ratio 12.8x. After growth, 33.6% still have two-hop ratio > 1. Peak L-ratio before eventual descent: 97.8x (x=159487, takes 12 hops). Max hops to L-descent: 32. Distribution: 64% descend in 1 hop, 83% in ≤2, 90% in ≤3. **The pointwise gap is REAL: average contraction is proven but worst-case growth is unbounded.**
- **explore22.py**: DONE - Growth phase structure. Max duration = 7 hops. 66.4% of phases are single-hop, 99.3% are ≤3 hops. Max total growth = 9.70 bits. **SURPRISE: t-values INCREASE within growth phases** (mean change +0.755, P(increase)=0.585). Growth bounded linearly by initial t: max ≈ (t+2)*0.585 for single hops, multi-hop phases can reach ~10 bits. 2^n-1 recovery times: 2^7-1 in 3 hops, 2^13-1 in 8 hops, 2^17-1 in 24 hops, 2^20-1 in 12 hops.
- **explore23.py**: DONE - 2^n-1 trajectory analysis. **F(2^n-1) is overwhelmingly Type A** (21/22 cases for n=3..24). First-hop ratio grows as ~(3/2)^n / 2^{v_2(3^n-1)-1}. Peak/start ratio grows with bit-length: max 13483x at 18-bit, avg stays ~3-4x. Some 2^n-1 trajectories pass through smaller 2^n-1 (e.g., 2^21-1 -> 31 = 2^5-1). v_2(FMF) for 2^n-1 follows pattern: 2 (n odd), v_2(n)+2 (n even). **Key: the big first hop almost always lands on Type A, guaranteeing immediate shrinkage next.**
- **explore24.py**: DONE - **KEY RESULT**: Epoch analysis (growth + recovery until descent below start). 100% descent rate (99,999/99,999). Epoch duration: mean=1.74, max=32, 71.4% descend in 1 hop. **Epoch duration / log2(x) ratio bounded by 3.15** (achieved at x=27). For x>1000, max ratio ~1.90. Recovery matches drift theory: recovery_hops ≈ peak_bits / 0.83. Growth phase mean 0.40 hops (most epochs don't grow!). Decomposition: growth is negligible (max 7), recovery dominates (max 31). Suggested C bound: epoch ≤ 4.73 * log2(x).
- **explore25.py**: DONE - **UNIVERSAL BOUND CONFIRMED** across 2917 tests spanning 3 to 60 bits. epoch_duration / log2(x) ≤ 2.83 globally (at x=31). For x > 10000, max ratio ≤ 1.63. For random 60-bit numbers, max ratio = 0.13. 2^n-1 tested up to n=44 (x~10^13): ALL descend, max ratio 1.41 (at n=17). High-t numbers (t up to 34): ALL descend. **The ratio DECREASES with magnitude** -- epoch duration grows as O(log x) but the constant shrinks. Random large numbers have avg epoch ~2 hops regardless of magnitude.
- **explore26.py**: DONE - **DETERMINISTIC PROOF ATTEMPT via Cesaro argument**. MIXED RESULTS: Cesaro argument fails (finite trajectories, ~0.3 error/hop). All product-of-ratios still converge.
- **explore27.py**: DONE - Growth phase mechanics: v_2 biased to 2 during growth (87.8%), m-values restricted to specific mod-8 classes, all long phases share "27 chain", P(continue|survived k) plateaus ~0.75, v_2 nearly independent (corr 0.035).
- **explore28.py**: DONE - Finite automaton has phantom cycles (7/8 at K=8). Actual trajectories don't follow them. Max growth phase: 37 hops (x=270271). mod-2^K too coarse.
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

### explore32: Mixed-Metric Height Function (PRIORITY 3)
Define h(x) = alpha*log(m) + gamma*t - beta*v_2(m - 3^{-(t+2)}).
- Combines archimedean (size) and 2-adic (proximity) information
- Optimize (alpha, beta, gamma) to minimize max(delta_h) over FMF hops
- Goal: find parameters where h(F(x)) < h(x) for ALL tested x
- Engages directly with Tao's barrier (transcendence theory)

### explore33: Carry Propagation Analysis (PRIORITY 4)
Analyze binary carry patterns in 3^(t+2)*m multiplication.
- Binary: 3*m = m + (m << 1), carries determine v_2
- How carry chains relate to v_2 of the result
- Compare with 5*m = m + (m << 2) carry patterns
- Look for combinatorial invariant that decreases along FMF chains

### explore34: Growth Automaton on Extended State (PRIORITY 5)
Revisit finite automaton with additional state: (type, t, m mod 2^K, bit_length_of_m).
- Adding magnitude information may break phantom cycles
- Check if growth transitions require m to grow, eventually leaving any finite state space
- This would prove growth phases terminate
