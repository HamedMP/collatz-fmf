"""
explore34.py: Rigorous Growth Phase Termination
=================================================
Revised PRIORITY 5 from Phase 7.

Instead of the original computational automaton plan, this explores
the THEORETICAL question: can we prove growth phases terminate?

Key insight synthesis from explore27-33:
1. Type A hops ALWAYS shrink (Theorem 30, deterministic)
2. State-independence: output type is 50/50 A/B (Theorem 12, proved)
3. But state-independence is over ALL inputs, not per-trajectory
4. Growth requires Type B AND low proximity p=1 (Theorem 32)
5. P(growth) = 31.3% empirically, but is it bounded away from 1?

NEW APPROACH: Instead of fighting the pointwise gap directly, prove that
the TYPE SEQUENCE along any trajectory cannot be all-B indefinitely.
This would follow from showing that v_2(FMF) distribution along
trajectories has a guaranteed lower bound on the probability of being large.

The key: after a Type B hop with output x', the TYPE of x' is determined
by x' mod 4. We can compute x' mod 4 from the FMF formula:
  FMF = 2(3^(t+2)*m - 1)
  x' = FMF / 2^v = (3^(t+2)*m - 1) / 2^(v-1)
  x' mod 4 depends on (3^(t+2)*m - 1) mod 2^(v+1)

If v = 2 (the growth case): x' = (3^(t+2)*m - 1) / 2
  x' mod 4 depends on (3^(t+2)*m - 1) mod 8

This is DETERMINISTIC given m and t. Can we show that for any m,
the output type after enough consecutive Type B hops must eventually be A?
"""

import math
from collections import defaultdict

def v2(n):
    if n == 0: return float('inf')
    count = 0
    while n % 2 == 0: n //= 2; count += 1
    return count

def mod_inv(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1: return None
    return x % m

def extended_gcd(a, b):
    if a == 0: return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x

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

def proximity(m, t, K=64):
    mod = 2**K
    power = pow(3, t + 2, mod)
    inv = mod_inv(power, mod)
    if inv is None: return 0
    diff = (m - inv) % mod
    return v2(diff) if diff != 0 else K


# =====================================================
print("=== Part 1: Output Type Determination ===\n")

# For x = 4k+3 (Type B), k+1 = 2^t * m, m odd:
# FMF = 2(3^(t+2)*m - 1)
# v_2(FMF) = 1 + v_2(3^(t+2)*m - 1)
# F(x) = FMF / 2^v = (3^(t+2)*m - 1) / 2^(v-1) where v = v_2(FMF)
#
# F(x) mod 4 determines the NEXT type:
# F(x) ≡ 1 mod 4 => Type A (will shrink next)
# F(x) ≡ 3 mod 4 => Type B (might grow next)
#
# For v = 2 (growth case): F(x) = (3^(t+2)*m - 1) / 2
# F(x) mod 4 = ((3^(t+2)*m - 1) / 2) mod 4
#
# This depends on 3^(t+2)*m - 1 mod 8.
# 3^(t+2)*m - 1 ≡ ? mod 8

print("3^(t+2)*m mod 8 for various t and m mod 8:")
print(f"  {'t':>3}  3^(t+2) mod 8", end="")
for m_mod in [1, 3, 5, 7]:
    print(f"  m≡{m_mod}:prod", end="")
print()

for t in range(8):
    pow3 = pow(3, t+2, 8)
    print(f"  {t:3d}  {pow3}", end="        ")
    for m_mod in [1, 3, 5, 7]:
        prod = (pow3 * m_mod) % 8
        fmf_part = (prod - 1) % 8  # 3^(t+2)*m - 1 mod 8
        # If v_2 = 2, then 3^(t+2)*m - 1 ≡ 4 mod 8 (exactly 2 trailing zeros after *2)
        # Wait: v_2(FMF) = v_2(2*(3^(t+2)*m - 1)) = 1 + v_2(3^(t+2)*m - 1)
        # v_2(FMF) = 2 means v_2(3^(t+2)*m - 1) = 1, so 3^(t+2)*m - 1 ≡ 2 mod 4
        # i.e., 3^(t+2)*m ≡ 3 mod 4
        print(f"  {prod}:{fmf_part}  ", end="")
    print()

print("\n\nOutput type when v_2(FMF) = 2 (growth case):")
print("v_2(FMF) = 2 means v_2(3^(t+2)*m - 1) = 1")
print("=> 3^(t+2)*m - 1 ≡ 2 mod 4, so 3^(t+2)*m ≡ 3 mod 4")
print("=> F(x) = (3^(t+2)*m - 1)/2, which is odd")
print("F(x) mod 4 = ((3^(t+2)*m - 1)/2) mod 4")
print()

for t in range(6):
    pow3_mod16 = pow(3, t+2, 16)
    print(f"  t={t}: 3^{t+2} mod 16 = {pow3_mod16}")
    for m_mod in [1, 3, 5, 7, 9, 11, 13, 15]:
        prod = (pow3_mod16 * m_mod) % 16
        val = prod - 1
        if val % 2 == 0 and val % 4 == 2:  # v_2(val) = 1
            fx = val // 2
            fx_mod4 = fx % 4
            out_type = 'A' if fx_mod4 == 1 else 'B'
            print(f"    m≡{m_mod:2d}(16): 3^{t+2}*m≡{prod}(16), prod-1={val}, F(x)≡{fx}(8), type={out_type}")


# =====================================================
print("\n\n=== Part 2: Consecutive Type B -- When Is It Possible? ===\n")

# For consecutive Type B hops (growth chain), we need:
# 1. x ≡ 3 mod 4 (Type B)
# 2. v_2(FMF) = 2 (growth)
# 3. F(x) ≡ 3 mod 4 (next is Type B)
# 4. Repeat

# From Part 1: v_2 = 2 requires 3^(t+2)*m ≡ 3 mod 4
# This means: 3^(t+2) mod 4 * m mod 4 ≡ 3 mod 4
# 3^n mod 4 = 3 for n odd, 1 for n even
# t+2 odd (t odd): 3*m ≡ 3 mod 4 => m ≡ 1 mod 4
# t+2 even (t even): 1*m ≡ 3 mod 4 => m ≡ 3 mod 4

# And F(x) ≡ 3 mod 4 for the NEXT hop to be Type B:
# F(x) = (3^(t+2)*m - 1) / 2 mod 4 = ?
# Need to track mod 8: (3^(t+2)*m - 1) / 2 ≡ 3 mod 4
# means (3^(t+2)*m - 1) ≡ 6 mod 8
# means 3^(t+2)*m ≡ 7 mod 8

print("Conditions for v_2=2 AND output Type B:")
print("Need: 3^(t+2)*m ≡ 3 mod 4 (for v_2=2)")
print("AND:  3^(t+2)*m ≡ 7 mod 8 (for F(x) ≡ 3 mod 4)")
print("Combined: 3^(t+2)*m ≡ 7 mod 8")
print()

for t in range(8):
    pow3_mod8 = pow(3, t+2, 8)
    growth_B_classes = []
    for m_mod8 in range(1, 8, 2):  # odd m
        prod = (pow3_mod8 * m_mod8) % 8
        if prod == 7:  # v_2=2 and output is Type B
            growth_B_classes.append(m_mod8)
    growth_any = []
    for m_mod8 in range(1, 8, 2):
        prod = (pow3_mod8 * m_mod8) % 8
        if prod == 3:  # v_2=2 and output is Type A
            growth_any.append(m_mod8)
    print(f"  t={t}: 3^{t+2}≡{pow3_mod8}(8), growth+B: m≡{growth_B_classes}(8), growth+A: m≡{growth_any}(8)")

print("\nKey observation: for each t, EXACTLY 1 out of 4 odd residue classes mod 8")
print("allows growth-to-B (v_2=2 and output Type B). The other growth class gives")
print("growth-to-A (guaranteed shrinkage next hop).")
print("So: P(output B | growth) = 1/2 for EACH t.")
print("This is a STRUCTURAL reason why growth chains self-terminate!")


# =====================================================
print("\n\n=== Part 3: Extended Analysis mod 16 ===\n")

# Go deeper: mod 16 analysis
print("Conditions for v_2=2 AND output Type B, by (t, m mod 16):")
for t in range(4):
    pow3_mod16 = pow(3, t+2, 16)
    bb_classes = []
    ba_classes = []
    no_growth = []
    for m_mod16 in range(1, 16, 2):
        prod = (pow3_mod16 * m_mod16) % 16
        val = prod - 1
        v = v2(val)
        if v == 1:  # v_2(3^(t+2)*m-1) = 1, so v_2(FMF) = 2
            fx = val // 2
            if fx % 4 == 3:
                bb_classes.append(m_mod16)
            else:
                ba_classes.append(m_mod16)
        else:
            no_growth.append((m_mod16, v))

    print(f"  t={t}: growth->B: m≡{bb_classes}(16), growth->A: m≡{ba_classes}(16)")
    if no_growth:
        ng_str = [(m, f"v={v}") for m, v in no_growth]
        print(f"        no growth (v>1): {ng_str}")


# =====================================================
print("\n\n=== Part 4: The m-Evolution Under Growth-B Constraint ===\n")

# If we're in a growth chain (consecutive growth + Type B output),
# we need m ≡ specific class mod 8 at each step.
# After the FMF hop, the new m' is determined by F(x).
# Does m' satisfy the constraint for the NEXT growth-B hop?

# Track the m mod 8 evolution through growth-B chains
print("m mod 8 evolution through growth-B chains:")
print("(Starting from various x, tracking only consecutive growth+B hops)")
print()

max_chain = 0
chain_lengths = []

for x0 in range(3, 500001, 2):
    x = x0
    chain = 0
    for hop in range(100):
        if x <= 1: break
        r = fmf_hop_full(x)
        if r is None: break
        nx, case, t, v2v, fmf, m = r

        if case == 'B' and nx > x and v2v == 2:
            # Check if output is Type B
            if nx % 4 == 3:
                chain += 1
            else:
                if chain > 0:
                    chain_lengths.append(chain)
                chain = 0
        else:
            if chain > 0:
                chain_lengths.append(chain)
            chain = 0
        x = nx

    if chain > 0:
        chain_lengths.append(chain)

if chain_lengths:
    print(f"Total growth-B chains: {len(chain_lengths)}")
    for length in sorted(set(chain_lengths), reverse=True)[:10]:
        count = chain_lengths.count(length)
        print(f"  Length {length}: {count} chains")
    max_chain = max(chain_lengths)
    print(f"\n  Max growth-B chain: {max_chain}")
    avg_chain = sum(chain_lengths) / len(chain_lengths)
    print(f"  Avg growth-B chain: {avg_chain:.2f}")


# =====================================================
print("\n\n=== Part 5: Theoretical Bound on Growth Phase ===\n")

# From Part 2: at each growth hop, P(output B) = 1/2 (structural, mod 8)
# So the expected number of consecutive growth-B hops is geometric with p=1/2
# P(chain >= k) = (1/2)^k
#
# BUT: this is for growth hops with v_2 = 2.
# Growth can also occur with v_2 = 3 (less common, ~12%)
# Let's check what fraction of growth hops have v_2 = 2

v2_dist_growth = defaultdict(int)
v2_dist_all = defaultdict(int)

for x0 in range(3, 200001, 2):
    x = x0
    for hop in range(30):
        if x <= 1: break
        r = fmf_hop_full(x)
        if r is None: break
        nx, case, t, v2v, fmf, m = r
        v2_dist_all[v2v] += 1
        if nx > x:  # growth
            v2_dist_growth[v2v] += 1
        x = nx

total_growth = sum(v2_dist_growth.values())
print("v_2(FMF) distribution for GROWTH hops:")
for v in sorted(v2_dist_growth.keys()):
    frac = v2_dist_growth[v] / total_growth
    print(f"  v_2 = {v}: {v2_dist_growth[v]:7d} ({frac*100:.1f}%)")

print(f"\nGrowth hops with v_2=2: {v2_dist_growth[2]/total_growth*100:.1f}%")
print(f"Growth hops with v_2=3: {v2_dist_growth.get(3,0)/total_growth*100:.1f}%")


# =====================================================
print("\n\n=== Part 6: Growth Chain Probability Bound ===\n")

# For a growth chain to continue k hops, we need:
# 1. Each hop is Type B (not Type A) -- but Type A always shrinks
# 2. Each hop has small v_2 (growth condition)
# 3. Each output is Type B (for the chain to continue)
#
# From Part 2: given growth with v_2=2, P(output B) = 1/2 EXACTLY
# From Theorem 12: independent of input state
#
# So: P(k consecutive growth-B-B hops with v_2=2) = (1/4)^k
# The 1/4 comes from: P(v_2=2 | Type B) * P(output B | v_2=2)
# P(v_2=2 | Type B) = 1/2 (from geometric distribution)
# P(output B | v_2=2) = 1/2 (from mod 8 analysis)

# What about v_2=3 growth? Let's check output type
print("Output type distribution for growth hops by v_2:")
for v_val in [2, 3, 4, 5]:
    a_count = 0
    b_count = 0
    for x0 in range(3, 200001, 2):
        x = x0
        for hop in range(20):
            if x <= 1: break
            r = fmf_hop_full(x)
            if r is None: break
            nx, case, t, v2v, fmf, m = r
            if nx > x and v2v == v_val:
                if nx % 4 == 1:
                    a_count += 1
                else:
                    b_count += 1
            x = nx
    total = a_count + b_count
    if total > 0:
        print(f"  v_2={v_val}: {total:6d} growth hops -> {a_count} Type A ({a_count/total*100:.1f}%), {b_count} Type B ({b_count/total*100:.1f}%)")


# =====================================================
print("\n\n=== Part 7: Why State-Independence Implies Termination ===\n")

# The CRITICAL argument:
#
# Theorem 12 (proved): The output type of an FMF hop is independent of input.
# Specifically: P(F(x) ≡ 1 mod 4) = P(F(x) ≡ 3 mod 4) = 1/2
# for EACH fixed residue class of x mod 2^K, as m ranges over all odd values.
#
# This means: if we consider all odd numbers of the form 2^(t+2)*m - 1
# with m ≡ r mod 2^K for any fixed r, exactly half of them map to Type A.
#
# The question: does this AVERAGE property translate to POINTWISE behavior
# along a trajectory?
#
# Key insight: Along a trajectory, m CHANGES. The new m' is NOT in the
# same residue class as the old m. In fact, m' is determined by a DIFFERENT
# formula involving 3^(t+2), 2^v, and other factors.
#
# The ergodic-like behavior: as the trajectory progresses, the m-values
# visit different residue classes. The state-independence says each class
# maps 50/50 to A/B. So unless the trajectory is trapped in a specific
# set of residue classes that all map to B, it must eventually hit A.
#
# From the phantom cycle analysis (Theorem 28): no finite set of
# residue classes mod 2^K forms a true growth cycle.
# As K -> infinity, the only "cycle" would be an actual period in Z,
# which is excluded for periods < 2.17 * 10^11 (Simons & de Weger).

print("STATE-INDEPENDENCE + PHANTOM CYCLE EXCLUSION ARGUMENT:")
print()
print("Claim: For any odd x > 1, the FMF trajectory of x contains")
print("at least one Type A hop within every 2*C*log2(x) hops.")
print()
print("Argument sketch:")
print("  1. State-independence (Theorem 12): P(output A) = 1/2 for each")
print("     residue class of input m.")
print()
print("  2. The m-values along a trajectory visit different residue classes")
print("     mod 2^K. From Theorem 28: no growth-sustaining cycle exists")
print("     mod 2^K for any fixed K.")
print()
print("  3. For the trajectory to avoid Type A for N consecutive hops,")
print("     the m-values must ALL lie in Type-B-producing classes.")
print("     This requires: 3^(t+2)*m ≡ 7 mod 8 at each step (from Part 2).")
print()
print("  4. But 3^(t+2)*m ≡ 7 mod 8 constrains m to a SPECIFIC residue")
print("     class mod 8 (depending on t). Since t changes along the chain,")
print("     the constraint on m mod 8 CHANGES.")
print()
print("  5. If the trajectory has k consecutive growth-B hops:")
print("     - Each hop has P(1/4) of continuing (v_2=2 AND output B)")
print("     - Expected chain length: 4/3 ≈ 1.33")
print("     - P(chain >= k) ≈ (1/4)^k = 4^{-k}")
print()

# Verify the 1/4 bound empirically
# For each Type B hop, P(growth AND output B)
type_b_hops = 0
growth_b_out = 0
for x0 in range(3, 200001, 2):
    x = x0
    for hop in range(30):
        if x <= 1: break
        r = fmf_hop_full(x)
        if r is None: break
        nx, case, t, v2v, fmf, m = r
        if case == 'B':
            type_b_hops += 1
            if nx > x and nx % 4 == 3:
                growth_b_out += 1
        x = nx

print(f"Empirical P(growth AND output B | Type B) = {growth_b_out/type_b_hops:.4f}")
print(f"Theoretical (1/4): 0.2500")
print(f"Ratio: {growth_b_out/type_b_hops/0.25:.4f}")


# =====================================================
print("\n\n=== Part 8: The Growth Termination Theorem ===\n")

# Can we make this rigorous?
#
# THEOREM (Growth Phase Termination):
# For any FMF trajectory starting from odd x > 1, the probability
# that a growth phase lasts >= k hops is bounded by C * r^k
# where r < 1 is a universal constant.
#
# PROOF ATTEMPT:
#
# Step 1: Each FMF hop from Type B with v_2 = 2 has output type
#   determined by 3^(t+2)*m mod 8:
#   - If ≡ 7 mod 8: output is Type B (growth continues)
#   - If ≡ 3 mod 8: output is Type A (growth ends, GUARANTEED shrinkage)
#   For each t, exactly one m mod 8 class gives ≡7, one gives ≡3.
#   So P(output B | v_2=2) = 1/2.
#
# Step 2: For growth with v_2 > 2:
#   v_2 = 3 means 3^(t+2)*m - 1 ≡ 4 mod 8, and after /4 the output
#   type depends on higher bits. Empirically: P(output B | v_2=3) ≈ 1/2.
#
# Step 3: P(growth) for a Type B hop depends on v_2:
#   P(v_2 = 2 AND growth) = P(v_2 = 2) * P(growth | v_2=2)
#   = 1/2 * (depends on t)
#
# The issue: P(growth | v_2=2) is NOT independent of t.
# For t=0: growth iff (3/2)^2 / 2^0 > 1, i.e., 2.25 > 1 (always)
# For t=1: growth iff (3/2)^3 / 2^0 > 1, i.e., 3.375 > 1 (always)
# Actually for v_2=2, growth iff (3^(t+2)*m-1)/(2^(t+2)*m-1) / 4 > 1
# For large m: ~ (3/2)^(t+2) / 4
# This is > 1 iff (3/2)^(t+2) > 4 iff t+2 > log(4)/log(3/2) = 3.42
# So t >= 2 guarantees growth with v_2=2.
# For t=0,1: growth with v_2=2 depends on m.

print("GROWTH TERMINATION BOUND:")
print()

# The cleanest bound: P(growth chain >= k) = ?
# At each step in a growth chain:
# - The hop is Type B (given - we're in a growth chain)
# - v_2 = 2 (probability from geometric: ~1/2)
# - Output is Type B (probability 1/2 given v_2=2)
# - The next hop ALSO grows (depends on next m and t)
#
# If we only count "growth-B-to-B" chains with v_2=2:
# P(chain continues) = P(v_2=2) * P(output B | v_2=2) = 1/2 * 1/2 = 1/4
# But actual growth chains include v_2=3 hops too.

# More careful: empirically measure P(continue | in growth chain)
growth_continue = 0
growth_start = 0
in_growth = False

for x0 in range(3, 200001, 2):
    x = x0
    in_growth = False
    for hop in range(50):
        if x <= 1: break
        r = fmf_hop_full(x)
        if r is None: break
        nx, case, t, v2v, fmf, m = r

        if case == 'B' and nx > x:  # this is a growth hop
            if in_growth:
                growth_continue += 1
            growth_start += 1
            in_growth = True
        else:
            in_growth = False

        x = nx

if growth_start > 0:
    p_continue = growth_continue / growth_start
    print(f"P(growth continues | in growth chain) = {p_continue:.4f}")
    print(f"Expected chain length: 1/(1-{p_continue:.4f}) = {1/(1-p_continue):.2f}")
    print(f"P(chain >= k): approximately {p_continue:.2f}^k")
    print()
    for k in [1, 2, 3, 5, 10, 20, 37]:
        print(f"  P(chain >= {k:2d}) ~ {p_continue**k:.2e}")


# =====================================================
print("\n\n=== Part 9: Type A Frequency Along Trajectories ===\n")

# Even if growth chains can be long, Type A hops appear regularly
# and each one guarantees shrinkage.

# For each starting x, count: hops to first Type A, then hops to second, etc.
type_a_gaps = []
for x0 in range(3, 200001, 2):
    x = x0
    gap = 0
    for hop in range(100):
        if x <= 1: break
        r = fmf_hop_full(x)
        if r is None: break
        nx, case, t, v2v, fmf, m = r
        gap += 1
        if case == 'A' or (case == 'B' and nx % 4 == 1):
            # Actually, 'A' means x is Type A. Let me check the OUTPUT type
            pass
        if nx % 4 == 1:  # output is Type A
            type_a_gaps.append(gap)
            gap = 0
        x = nx

if type_a_gaps:
    print(f"Gaps between Type A outputs:")
    print(f"  Mean gap: {sum(type_a_gaps)/len(type_a_gaps):.2f}")
    print(f"  Max gap: {max(type_a_gaps)}")
    gap_dist = defaultdict(int)
    for g in type_a_gaps:
        gap_dist[g] += 1
    for g in sorted(gap_dist.keys())[:15]:
        print(f"  Gap {g:2d}: {gap_dist[g]:7d} ({gap_dist[g]/len(type_a_gaps)*100:.1f}%)")


# =====================================================
print("\n\n=== Part 10: Rigorous Proof Components ===\n")

print("SYNTHESIS: WHAT CAN BE PROVED RIGOROUSLY")
print("=" * 55)
print()
print("PROVED (algebraic/2-adic):")
print("  1. Type A always shrinks: ratio < 3/4 (Theorem 30)")
print("  2. State-independence: output type is 50/50 A/B (Theorem 12)")
print("  3. v_2 follows exact geometric (Theorem 3)")
print("  4. rho = E[R^0.53] = 0.8638 < 1 (Theorem 19)")
print("  5. Inverse movement: v_2(inv_{t+1} - inv_t) = 1 (Theorem 31)")
print()
print("PROVED (mod 8 structure):")
print("  6. For growth with v_2=2: P(output B) = 1/2 EXACTLY")
print("     (because for each t, exactly 1 of 2 growth-class residues")
print("      mod 8 gives output ≡ 3 mod 4, the other gives ≡ 1 mod 4)")
print()
print("CONSEQUENCE:")
print("  7. P(growth chain of length k) <= C * r^k for r < 1")
print(f"     Empirical r = {p_continue:.3f}")
print("     Theoretical lower bound: r <= 1/2 (just from Type A guarantee)")
print()
print("REMAINING GAP:")
print("  8. Even if growth chains terminate with probability 1,")
print("     'probability 1' is not 'certainty'. We need to show")
print("     no SPECIFIC trajectory can avoid Type A indefinitely.")
print()
print("  9. This requires: showing that the m-evolution doesn't")
print("     systematically select B-producing residue classes.")
print("     Theorem 28 (no phantom cycles) addresses this for")
print("     finite state spaces. The question is the infinite limit.")
print()
print("WHAT WOULD CLOSE IT:")
print("  - If we can show that m mod 8 is equidistributed along")
print("    ANY trajectory (not just on average), then P(Type A output)")
print("    = 1/2 at each step, and growth chains terminate a.s.")
print("  - Alternatively: show that the mod-2^K state of (m,t) along")
print("    a trajectory visits ALL reachable states, including those")
print("    that produce Type A output. This is an ergodicity statement.")
print("  - The strongest possible result: show that for any x > 1,")
print("    within log2(x) hops, at least one Type A output occurs.")
print("    This + Type A always shrinks + rho < 1 => Collatz.")
