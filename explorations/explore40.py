"""
explore40.py: Complete Proof Assembly and Gap Audit
=====================================================

With Lemma G now proved (Theorem 40), we have all 7 lemmas.
This exploration assembles the complete proof and identifies
any remaining logical gaps in the chain:

  Lemma A (Type A shrinks) + Lemma B (state-independence) +
  Lemma C (average contraction rho < 1) + Lemma D (50/50 split) +
  Lemma E (no cycles) + Lemma F (no small cycles) +
  Lemma G (growth termination)
  => Collatz Conjecture

The proof must show: for every odd x > 1, the FMF trajectory
eventually reaches a value y < x. By well-ordering, this gives
convergence to 1.

Critical question: do the lemmas actually IMPLY the conjecture,
or is there still a logical gap?
"""

import math
from collections import defaultdict

def v2(n):
    if n == 0: return float('inf')
    count = 0
    while n % 2 == 0: n //= 2; count += 1
    return count

def fmf_hop_full(x):
    mod4 = x % 4
    if mod4 == 1:
        k = (x - 1) // 4
        fmf = 4 * (3 * k + 1)
        p = v2(fmf)
        return fmf >> p, 'A', 0, p, fmf, k + 1
    elif mod4 == 3:
        k = (x - 3) // 4
        t = v2(k + 1)
        m = (k + 1) >> t
        fmf_val = 2 * (3**(t+2) * m - 1)
        p = v2(fmf_val)
        return fmf_val >> p, 'B', t, p, fmf_val, m
    return None


# =====================================================
print("=== COMPLETE PROOF OF THE COLLATZ CONJECTURE ===")
print("=== (via the FMF Framework)                  ===")
print("=" * 55)
print()

print("THEOREM: For every positive odd integer x, the FMF trajectory")
print("of x reaches 1 in finitely many steps.")
print()
print("PROOF:")
print()

print("PART I: Every trajectory eventually DESCENDS (reaches y < x).")
print("-" * 55)
print()
print("Step 1 (Growth Phase Structure):")
print("  By Lemma A (Theorem 30), Type A hops always shrink: F(x) < x.")
print("  So growth can only occur on Type B hops.")
print("  By Lemma G (Theorem 40), every growth phase has length")
print("  at most log2(x)/2 + O(1).")
print()
print("Step 2 (Growth Phase Bound):")
print("  During a growth phase of length k:")
print("  - Each hop has ratio at most (3/2)^(t+2) / 4")
print("  - For the dominant case t=0: ratio ≤ 9/4")
print("  - For t=j: ratio ≤ (3/2)^(j+2) / 4")
print("  - The average ratio is bounded by sum over t-distribution")
print()
print("Step 3 (Recovery after Growth):")
print("  After a growth phase ends, the next hop is either:")
print("  (a) Type A: guaranteed shrinkage by factor < 3/4")
print("  (b) Type B with v_2 > 2: shrinkage by factor < (3/2)^(t+2)/2^v")
print("  Either way, the trajectory begins contracting.")
print()
print("Step 4 (Average Contraction):")
print("  By Lemma C (Theorem 19), the average contraction ratio is")
print("  rho = E[R^0.53] = 0.8638 < 1.")
print("  By state-independence (Lemma B, Theorem 12), this average")
print("  holds for EVERY starting state.")
print()
print("Step 5 (Descent Bound):")
print("  *** THIS IS THE GAP ***")
print("  We need: average contraction + growth termination => descent.")
print("  The issue: average contraction alone doesn't guarantee")
print("  descent for every specific trajectory.")
print()
print("  We need a STRONGER argument. Let's try:")
print()

# =====================================================
print("PART II: The Epoch Argument")
print("-" * 55)
print()
print("Definition: An EPOCH starting at x is the minimal prefix")
print("of the FMF trajectory such that x_N <= x for some N >= 1.")
print()
print("Claim: Every epoch has finite length.")
print()
print("Sub-proof:")
print("  Phase 1 (Growth): at most L = log2(x)/2 + O(1) hops (Lemma G)")
print("  Phase 2 (Recovery): the trajectory is above x but contracting.")
print("    - Average contraction rate: rho = 0.8638 per hop")
print("    - Peak value: at most x * (9/4)^L")
print("    - Expected recovery hops: log2(peak/x) / |log2(rho)|")
print("    = L * log2(9/4) / 0.21 ≈ L * 5.5")
print("    - Total epoch: L + 5.5*L = 6.5*L = 6.5 * log2(x)/2")
print("    ≈ 3.25 * log2(x)")
print()
print("  *** BUT: This is still an AVERAGE argument. ***")
print("  The recovery phase might have its OWN growth phases.")
print("  Each recovery growth phase is bounded by Lemma G,")
print("  but recovery growth phases use the CURRENT value, not x.")
print()

# =====================================================
print("\nPART III: Can the Recovery Phase Have Unbounded Growth?")
print("-" * 55)
print()

# During recovery, the trajectory is above x but generally decreasing.
# Can the recovery phase itself have growth phases that push the
# trajectory even higher?
#
# YES, it can. This is the "peak growth" phenomenon (explore21).
# The peak can reach 97.8x before eventually descending.
#
# But: each GROWTH PHASE is bounded by Lemma G.
# And between growth phases, Type A hops always shrink.
# The question: can the recovery phase have infinitely many
# growth phases, each bounded, but collectively preventing descent?

# This is equivalent to asking: can the trajectory OSCILLATE
# forever above x without ever going below x?

# From Lemma E (Theorem 36): no cycles in the growth-B map.
# From Lemma F: no small cycles (period > 2.17 × 10^11).
# Combined: the trajectory cannot cycle above x.

# But: the trajectory could DIVERGE (go to infinity without cycling).
# This is precisely what happens for 5n+1!

# The key difference (Lemma A, Theorem 30): 3n+1 has a guaranteed
# contraction channel (Type A). 5n+1 doesn't.

# Can we prove that the contraction channel EVENTUALLY dominates?

print("The recovery phase has bounded growth phases (Lemma G).")
print("Between growth phases, Type A hops shrink by factor < 3/4.")
print("The trajectory can oscillate but cannot cycle (Lemma E).")
print()
print("Key question: does the trajectory DIVERGE or DESCEND?")
print()

# Let's examine the product of ratios along long epochs
print("Product analysis of long epochs:")
print()

epoch_products = []
for x0 in range(3, 500001, 2):
    x = x0
    log_product = 0
    hops = 0
    for hop in range(200):
        if x <= 1: break
        r = fmf_hop_full(x)
        if r is None: break
        nx, case, t, v2v, fmf, m = r

        log_product += math.log2(nx / x)
        hops += 1
        x = nx

        if nx < x0:
            epoch_products.append((x0, hops, log_product))
            break

# Check: does log_product ever stay positive for many hops?
long_epochs = [e for e in epoch_products if e[1] >= 10]
if long_epochs:
    print(f"  Epochs with >= 10 hops: {len(long_epochs)}")
    for x0, hops, lp in sorted(long_epochs, key=lambda e: -e[1])[:10]:
        print(f"    x0={x0:6d}: {hops:3d} hops, "
              f"log2(product) = {lp:+.2f}")

# Are there ANY trajectories that don't descend within 200 hops?
non_descenders = []
for x0 in range(3, 500001, 2):
    x = x0
    descended = False
    for hop in range(200):
        if x <= 1:
            descended = True
            break
        r = fmf_hop_full(x)
        if r is None: break
        nx = r[0]
        if nx < x0:
            descended = True
            break
        x = nx
    if not descended:
        non_descenders.append(x0)

print(f"\n  Non-descenders within 200 hops (in [3, 500K]): {len(non_descenders)}")
if non_descenders:
    print(f"    First few: {non_descenders[:10]}")


# =====================================================
print("\n\nPART IV: The Product Formula Approach")
print("-" * 55)
print()

# Instead of tracking individual hops, track the CUMULATIVE product.
# After N hops: x_N = x_0 * prod_{i=0}^{N-1} R_i
# where R_i = F(x_i) / x_i.
#
# log2(x_N / x_0) = sum_{i=0}^{N-1} log2(R_i)
#
# If this sum goes below 0, we have x_N < x_0 (descent).
#
# The sum is a RANDOM WALK with drift E[log2(R)] = -0.830.
# By the law of large numbers, sum/N -> -0.830 a.s.
# So the sum goes to -infinity.
#
# But we need it to go below 0 for EVERY starting x.
# The LLN is about almost every trajectory (in a measure-theoretic sense).
# For every SPECIFIC trajectory, we need the sum to hit 0.
#
# From the theory of random walks with negative drift:
# P(sum never goes below 0) = 0 (for i.i.d. increments with
# negative mean and finite variance).
#
# But the FMF increments are NOT i.i.d. They're deterministic
# (given by the dynamics). The question: is the deterministic
# sequence of increments "random enough" to apply the LLN?

# From Lemma B (state-independence): the output distribution
# is the same for every input state. This means:
# E[log2(R_i) | x_0, ..., x_{i-1}] = E[log2(R)] = -0.830
# for EVERY conditioning. This is a MARTINGALE property!

# Actually, it's STRONGER than a martingale. It says the
# conditional expectation is CONSTANT at -0.830.
# This means: sum_{i=0}^{N-1} log2(R_i) = N * (-0.830) + M_N
# where M_N is a martingale with E[M_N] = 0.

# But wait: Lemma B says the output DISTRIBUTION is state-independent,
# which means E[log2(R_i)] = -0.830 regardless of the current state.
# However, E[log2(R_i) | x_{i-1}] might not equal E[log2(R)],
# because x_{i-1} determines R_i deterministically.

# The subtlety: state-independence says the distribution is the same
# for DIFFERENT inputs, not for the SAME input. For a specific x,
# R(x) = F(x)/x is a specific number, not random.

# THIS IS THE FUNDAMENTAL GAP.

print("THE FUNDAMENTAL GAP IDENTIFIED:")
print()
print("State-independence (Lemma B) gives:")
print("  E[log2(R)] = -0.830  (averaged over inputs)")
print()
print("But for a SPECIFIC trajectory x_0, x_1, x_2, ...,")
print("the values R_i = F(x_i)/x_i are DETERMINISTIC.")
print("We need: sum R_i goes to -infinity for every starting x_0.")
print()
print("The gap: going from AVERAGE contraction to EVERY-TRAJECTORY")
print("contraction. This is Tao's barrier.")
print()
print("HOWEVER: Lemma G changes the game.")
print()

# =====================================================
print("\nPART V: How Lemma G Fills the Gap")
print("-" * 55)
print()

# Lemma G says: growth phases have bounded length.
# This means: the trajectory cannot have an INFINITE INCREASING
# subsequence without interruption.
#
# More precisely: between any two growth phases, there's at least
# one Type A hop (which shrinks by factor < 3/4).
#
# Consider the WORST CASE:
# - Growth phase of length L_1 (bounded by log2(x)/2)
# - Type A hop: shrinks by factor < 3/4
# - Growth phase of length L_2
# - Type A hop: shrinks
# - ...
#
# The net ratio after one growth phase + one Type A:
# growth factor: at most (9/4)^{L_j} (worst case t=0 for all hops)
# shrinkage factor: at most 3/4
# Net: (9/4)^{L_j} * 3/4
#
# For L_j = 1: net = (9/4) * (3/4) = 27/16 = 1.6875 (still growing!)
# For L_j = 0: net = 3/4 (shrinking)
#
# So: ONE Type A hop after ONE growth hop is NOT enough.
# The question: how many Type A hops per growth hop?
#
# From the trajectory analysis: Type A hops constitute 52.3% of all hops.
# Growth phases are rare (only 28.6% of hops are in growth phases).
# So on average, there are ~2 Type A hops per growth hop.
#
# But we need this to hold for EVERY trajectory, not on average.

# From Lemma G: growth phase length <= L = log2(x)/2.
# After growth phase: the value is at most x * (9/4)^L.
# Type A hops shrink by 3/4 each.
# Need (3/4)^{N_A} * (9/4)^L < 1 for descent.
# N_A > L * log(9/4) / log(4/3) = L * 1.170 / 0.415 = L * 2.82

# So we need: after a growth phase of length L, the trajectory has
# AT LEAST 2.82 * L Type A hops before the NEXT growth phase.
# Is this guaranteed?

# NOT by Lemma G alone. Lemma G bounds the growth phases,
# but doesn't bound the GAPS between growth phases.

print("Analysis: How many Type A hops between growth phases?")
print()

# Measure the gaps
gap_data = defaultdict(list)
for x0 in range(3, 200001, 2):
    x = x0
    gap = 0  # consecutive non-growth hops (including Type A)
    last_growth_len = 0
    in_growth = False
    growth_len = 0

    for hop in range(100):
        if x <= 1: break
        r = fmf_hop_full(x)
        if r is None: break
        nx, case, t, v2v, fmf, m = r

        if nx > x:  # growth
            if not in_growth:
                if last_growth_len > 0:
                    gap_data[last_growth_len].append(gap)
                in_growth = True
                growth_len = 0
            growth_len += 1
            gap = 0
        else:  # non-growth
            if in_growth:
                last_growth_len = growth_len
                in_growth = False
            gap += 1
        x = nx

print(f"  {'growth_len':>10}  {'count':>6}  {'avg_gap':>8}  {'min_gap':>8}  {'needed':>8}")
for gl in sorted(gap_data.keys())[:8]:
    vals = gap_data[gl]
    if len(vals) < 10:
        continue
    avg_gap = sum(vals) / len(vals)
    min_gap = min(vals)
    needed = math.ceil(gl * 2.82)
    print(f"  {gl:10d}  {len(vals):6d}  {avg_gap:8.2f}  {min_gap:8d}  {needed:8d}")


# =====================================================
print("\n\nPART VI: The Contraction Ratio After Growth + Gap")
print("-" * 55)
print()

# For each epoch, compute the actual contraction ratio
# WITHIN the epoch: product of all hop ratios.
# If this is always < 1, then every epoch descends.

epoch_ratios = []
for x0 in range(3, 500001, 2):
    x = x0
    log_ratio = 0
    hops = 0
    descended = False

    for hop in range(200):
        if x <= 1:
            descended = True
            break
        r = fmf_hop_full(x)
        if r is None: break
        nx, case, t, v2v, fmf, m = r

        log_ratio += math.log2(nx / x)
        hops += 1

        if nx < x0:
            epoch_ratios.append((x0, hops, log_ratio, 2**log_ratio))
            descended = True
            break
        x = nx

    if not descended:
        epoch_ratios.append((x0, hops, log_ratio, 2**log_ratio))

# All epochs should have log_ratio < 0 (descent)
non_descending = [e for e in epoch_ratios if e[2] >= 0]
print(f"Epochs tested: {len(epoch_ratios)}")
print(f"Non-descending epochs: {len(non_descending)}")
print()

# What's the MAXIMUM log_ratio at any point during an epoch?
# (i.e., the peak of the random walk before descent)
max_peak = 0
max_peak_x = 0
for x0 in range(3, 100001, 2):
    x = x0
    cum_log = 0
    peak = 0

    for hop in range(200):
        if x <= 1: break
        r = fmf_hop_full(x)
        if r is None: break
        nx = r[0]
        cum_log += math.log2(nx / x)
        if cum_log > peak:
            peak = cum_log
        if nx < x0:
            break
        x = nx

    if peak > max_peak:
        max_peak = peak
        max_peak_x = x0

print(f"Maximum peak during any epoch: {max_peak:.2f} bits")
print(f"  (at x0={max_peak_x}, ratio = {2**max_peak:.2f}x)")
print()

# Distribution of epoch log_ratios
if epoch_ratios:
    log_rs = [e[2] for e in epoch_ratios[:250000]]
    print(f"Epoch log2(ratio) distribution ({len(log_rs)} epochs):")
    print(f"  Mean: {sum(log_rs)/len(log_rs):.4f}")
    print(f"  Max: {max(log_rs):.4f}")
    print(f"  Min: {min(log_rs):.4f}")
    print(f"  P(ratio < 0): {sum(1 for r in log_rs if r < 0)/len(log_rs):.6f}")


# =====================================================
print("\n\nPART VII: The Complete Proof (with identified gaps)")
print("=" * 55)
print()

print("PROOF OF THE COLLATZ CONJECTURE (FMF Framework)")
print()
print("Given: Odd x > 1. Show: the FMF trajectory of x reaches 1.")
print()
print("Step 1 (Structuring the trajectory):")
print("  The trajectory x = x_0, x_1, x_2, ... consists of")
print("  alternating GROWTH PHASES (x_{i+1} > x_i) and")
print("  CONTRACTION PHASES (x_{i+1} < x_i).")
print()
print("Step 2 (Growth phase bound -- Lemma G, Theorem 40):")
print("  Each growth phase has length at most L_j <= log2(x_j)/2 + O(1),")
print("  where x_j is the value at the start of the j-th growth phase.")
print()
print("Step 3 (Contraction channel -- Lemma A, Theorem 30):")
print("  Each contraction phase contains at least one Type A hop")
print("  with ratio F(x)/x < 3/4.")
print()
print("Step 4 (No divergence):")
print("  Suppose the trajectory diverges: x_n -> infinity.")
print("  Then it has infinitely many growth phases and")
print("  infinitely many contraction phases.")
print()
print("  The cumulative log-ratio:")
print("  S_N = sum_{i=0}^{N-1} log2(R_i)")
print()
print("  Must go to +infinity (since x_N = x_0 * 2^{S_N}).")
print()
print("  By Lemma B (state-independence), each R_i has the same")
print("  distribution, with E[log2(R)] = -0.830.")
print()
print("  *** GAP: This is an AVERAGE over all inputs, not a")
print("  conditional expectation along a trajectory. ***")
print()
print("  HOWEVER: The key constraint is:")
print("  - Type A hops have log2(R) < log2(3/4) = -0.415")
print("  - Type A hops are DETERMINISTIC contractions")
print("  - Growth phases produce at most C*log2(x) bits of growth")
print("  - Type A hops remove at least 0.415 bits per hop")
print()
print("Step 5 (Type A frequency bound):")
print("  From the quartering law (Theorem 40):")
print("  P(output is Type A | any state) >= 1/4")
print("  (since growth-B occupies at most 1/4 of states,")
print("   and even within growth-B, half produce Type A).")
print()
print("  More precisely: from ANY state, the probability of")
print("  the next hop being Type A is >= 1/4.")
print("  (This is 1/2 from Theorem 12: P(Type A) = 1/2,")
print("   but even among Type B outputs, many cause shrinkage.)")
print()
print("Step 6 (The key bound):")
print("  After K = log2(x) hops:")
print("  - Expected number of Type A hops: >= K/2 (from P(A) = 1/2)")
print("  - Each Type A hop contributes at least -0.415 to S_N")
print("  - Growth phases contribute at most sum L_j * 1.17 bits")
print("  - Lemma G: sum L_j <= sum log2(x_j)/2")
print()
print("  *** GAP: Need to bound sum log2(x_j) in terms of")
print("  the trajectory's history. This requires controlling")
print("  the peak values during growth phases. ***")
print()
print("Step 7 (Epoch bound -- conditional on Step 6):")
print("  If sum L_j / N -> 0 (growth phases become rare),")
print("  then S_N / N -> -0.830 (contraction dominates),")
print("  and S_N < 0 for N > log2(x) / 0.830 ≈ 1.2 * log2(x).")
print("  This gives descent within O(log x) hops.")
print()

# =====================================================
print("\nPART VIII: Honest Assessment")
print("=" * 55)
print()

print("WHAT IS RIGOROUSLY PROVED:")
print("  1. FMF algebraic formulas (Theorems 1-4)")
print("  2. State-independence of FMF transitions (Theorem 12)")
print("  3. Average contraction rho = 0.8638 < 1 (Theorem 19)")
print("  4. Type A always shrinks by factor < 3/4 (Theorem 30)")
print("  5. 3/4 discriminant: unique to a=3 (Theorem 30)")
print("  6. v_2 geometric distribution (explore39)")
print("  7. Type B | v_2 = 1/2 exactly (explore39)")
print("  8. Quartering law: P(continue growth-B) = 1/4 (Theorem 40)")
print("  9. Odd Part Equidistribution Lemma (explore39)")
print("  10. Growth phase length <= log2(x)/2 (Theorem 40 corollary)")
print("  11. No cycles in growth-B map (Theorem 36)")
print("  12. No small cycles (external: Simons & de Weger)")
print()
print("WHAT IS NOT YET PROVED:")
print("  13. Every trajectory reaches a value below its start")
print("      (this IS the Collatz conjecture for Syracuse)")
print()
print("THE REMAINING GAP:")
print("  The 12 proved results reduce the conjecture to:")
print("  'Average contraction + bounded growth phases => descent'")
print()
print("  This is a WEAKER version of Tao's barrier:")
print("  - Tao: average contraction (almost all orbits) ≠> all orbits")
print("  - FMF: average contraction + growth bounded by O(log x)")
print("         + Type A guaranteed contraction + quartering law")
print("         =>? all orbits descend")
print()
print("  The FMF framework has NARROWED the gap to:")
print("  'Does bounded growth + deterministic contraction channel")
print("   + (1/4)^k growth chain density imply descent?'")
print()
print("  This is a CONCRETE QUESTION about 1D random walks with")
print("  negative drift, bounded positive excursions, and deterministic")
print("  negative jumps at a fraction >= 1/2 of steps.")
print()
print("  In the classical probability literature, this would follow")
print("  from the STRONG LAW OF LARGE NUMBERS applied to the")
print("  increments log2(R_i). The question is whether the")
print("  deterministic FMF dynamics satisfy the conditions for SLLN.")
print()
print("  The state-independence (Theorem 12) makes the increments")
print("  'essentially i.i.d.' in the sense that their distribution")
print("  doesn't depend on the current state. But 'same distribution'")
print("  is NOT the same as 'independent'. The increments could be")
print("  correlated in a way that prevents the SLLN from applying.")
print()
print("  From explore16: lag-1 autocorrelation is 0.082 (weak).")
print("  From explore18: self-correcting behavior (large growth")
print("  followed by high P(shrink)).")
print("  These suggest the increments ARE mixing, but the formal")
print("  proof of mixing is not yet established.")
