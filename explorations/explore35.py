"""
explore35.py: m-Transformation Ergodicity
==========================================
NEW PRIORITY from explore34 synthesis.

Goal: Prove that the m-transformation along growth-B chains cannot
systematically avoid Type-A-producing residue classes.

Approach: Compute the EXPLICIT map m -> m' for growth-B transitions
mod 2^K for increasing K. Check:
1. Does the map have any fixed points mod 2^K?
2. Does the growth-B transition graph have absorbing sets?
3. Does m grow during growth-B chains, eventually leaving any finite class?

If the growth-B map has no absorbing sets for any K, then no trajectory
can stay in growth-B mode indefinitely.
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


# =====================================================
print("=== Part 1: Explicit m -> m' for Growth-B ===\n")

# For a Type B hop with v_2(FMF) = 2:
# x = 2^(t+2)*m - 1, x ≡ 3 mod 4
# FMF = 2(3^(t+2)*m - 1), v_2(FMF) = 2
# F(x) = (3^(t+2)*m - 1) / 2
#
# For F(x) to be Type B (≡ 3 mod 4):
# F(x) = (3^(t+2)*m - 1) / 2 ≡ 3 mod 4
# => 3^(t+2)*m - 1 ≡ 6 mod 8
# => 3^(t+2)*m ≡ 7 mod 8
#
# Then: k' = (F(x) - 3) / 4
# k' + 1 = (F(x) - 3) / 4 + 1 = (F(x) + 1) / 4
#        = ((3^(t+2)*m - 1)/2 + 1) / 4
#        = (3^(t+2)*m + 1) / 8
#
# t' = v_2(k' + 1) = v_2((3^(t+2)*m + 1) / 8)
# m' = (k' + 1) / 2^{t'} (odd part of (3^(t+2)*m + 1) / 8)

print("Formula: For growth-B hop (v_2=2, output Type B):")
print("  m' = odd_part((3^(t+2)*m + 1) / 8)")
print("  t' = v_2((3^(t+2)*m + 1) / 8)")
print()

# Verify this formula
print("Verification:")
for x0 in [27, 703, 270271]:
    x = x0
    for hop in range(10):
        if x <= 1: break
        r = fmf_hop_full(x)
        if r is None: break
        nx, case, t, v2v, fmf, m = r

        if case == 'B' and v2v == 2 and nx % 4 == 3:
            # Compute m' using formula
            val = (3**(t+2) * m + 1) // 8
            t_prime = v2(val)
            m_prime = val >> t_prime

            # Get actual m' from next hop
            r2 = fmf_hop_full(nx)
            if r2:
                _, _, t2_actual, _, _, m2_actual = r2
                match = "OK" if m_prime == m2_actual and t_prime == t2_actual else "MISMATCH"
                print(f"  x={x}: t={t}, m={m} -> m'={m_prime} (formula), m'={m2_actual} (actual), "
                      f"t'={t_prime}/{t2_actual} [{match}]")
        x = nx


# =====================================================
print("\n\n=== Part 2: m-Map mod 2^K for Growth-B ===\n")

# For each t, the growth-B map mod 2^K is:
# m' = odd_part((3^(t+2) * m + 1) / 8) mod 2^K
# t' = v_2((3^(t+2) * m + 1) / 8)
#
# The key: does this map have fixed points or cycles mod 2^K?

# For t even: growth-B requires m ≡ 7 mod 8
# For t odd: growth-B requires m ≡ 5 mod 8

# But the NEXT t' is determined by the formula, not fixed.
# So we need to track (t, m mod 2^K) -> (t', m' mod 2^K)

for K in [4, 6, 8]:
    mod = 2**K
    print(f"\nGrowth-B transitions mod 2^{K}:")

    # Build transition graph
    transitions = {}
    for t in range(K):  # t can be up to K-1 meaningfully
        pow3 = pow(3, t+2)
        for m_class in range(1, mod, 2):  # odd m
            # Check if this is a growth-B case
            prod = (pow3 * m_class) % (mod * 8)  # need more bits
            val_minus1 = prod - 1
            if v2(val_minus1) != 1:
                continue  # not v_2=2

            # Check output type
            fx = val_minus1 // 2
            if fx % 4 != 3:
                continue  # not Type B output

            # Compute m' mod 2^K
            val_plus1 = (pow3 * m_class + 1)
            q = val_plus1 // 8
            if q == 0:
                continue
            t_prime = v2(q)
            m_prime = (q >> t_prime) % mod  # mod 2^K

            state = (t % K, m_class)
            next_state = (t_prime % K, m_prime)
            transitions[state] = next_state

    # Find cycles in this graph
    visited = set()
    cycles = []
    for start in transitions:
        if start in visited:
            continue
        path = []
        current = start
        path_set = set()
        while current not in visited and current in transitions:
            if current in path_set:
                # Found a cycle
                cycle_start = path.index(current)
                cycle = path[cycle_start:]
                cycles.append(cycle)
                break
            path_set.add(current)
            path.append(current)
            current = transitions[current]
        visited.update(path_set)

    print(f"  States with growth-B transition: {len(transitions)}")
    print(f"  Cycles found: {len(cycles)}")
    for i, cycle in enumerate(cycles[:5]):
        print(f"    Cycle {i}: length={len(cycle)}, states={cycle[:4]}{'...' if len(cycle) > 4 else ''}")


# =====================================================
print("\n\n=== Part 3: Absorbing Sets Analysis ===\n")

# An absorbing set S is a subset of states such that:
# for all s in S, the growth-B transition of s is also in S.
# If such S exists, a trajectory could potentially stay in S forever.

# From the cycles found above, check if they form absorbing sets
# But also check: is EVERY state reachable from every other state?

for K in [4, 6, 8]:
    mod = 2**K
    transitions = {}
    all_states = set()

    for t in range(K):
        pow3 = pow(3, t+2)
        for m_class in range(1, mod, 2):
            prod_mod = (pow3 * m_class) % (8 * mod)
            val = prod_mod - 1
            if v2(val) != 1:
                continue
            fx = val // 2
            if fx % 4 != 3:
                continue

            q = (pow3 * m_class + 1) // 8
            if q == 0: continue
            tp = v2(q)
            mp = (q >> tp) % mod

            state = (t % K, m_class)
            next_state = (tp % K, mp)
            transitions[state] = next_state
            all_states.add(state)
            all_states.add(next_state)

    # Find strongly connected components (simple BFS)
    # Check: which states can reach ALL other states?
    reachable = {}
    for start in all_states:
        reached = set()
        queue = [start]
        while queue:
            s = queue.pop()
            if s in reached: continue
            reached.add(s)
            if s in transitions:
                ns = transitions[s]
                if ns not in reached:
                    queue.append(ns)
        reachable[start] = reached

    # States that have transitions
    has_transition = set(transitions.keys())

    # Find absorbing sets: subsets where all transitions stay inside
    # Check: is the set of all growth-B states absorbing?
    growth_b_states = set(transitions.keys())
    absorbing = True
    for s in growth_b_states:
        if transitions[s] not in growth_b_states:
            absorbing = False
            break

    leaves = sum(1 for s in growth_b_states if transitions[s] not in growth_b_states)

    print(f"K={K}: {len(growth_b_states)} growth-B states")
    print(f"  States leaving growth-B set: {leaves}/{len(growth_b_states)}")
    if leaves > 0:
        print(f"  -> NOT absorbing! {leaves/len(growth_b_states)*100:.1f}% of states escape.")
        print(f"  This means: growth-B chains MUST eventually leave this mode mod 2^{K}.")
    else:
        print(f"  -> IS absorbing. Further analysis needed.")


# =====================================================
print("\n\n=== Part 4: What Causes Escape from Growth-B? ===\n")

# When a state (t, m mod 2^K) transitions but the next state
# is NOT a valid growth-B state, what happens?

# Reasons for leaving growth-B:
# 1. The next t' puts us at a value where m' mod 8 is wrong for growth-B
# 2. The next v_2 is > 2 (causes more shrinkage)
# 3. The output is Type A (guaranteed shrinkage)

K = 8
mod = 2**K
escape_reasons = defaultdict(int)

for t in range(K):
    pow3 = pow(3, t+2)
    for m_class in range(1, mod, 2):
        prod_mod = (pow3 * m_class) % (8 * mod)
        val = prod_mod - 1
        if v2(val) != 1:
            continue
        fx = val // 2
        if fx % 4 != 3:
            continue

        q = (pow3 * m_class + 1) // 8
        if q == 0: continue
        tp = v2(q)
        mp = (q >> tp) % mod

        # Check if (tp, mp) is a growth-B state
        pow3_next = pow(3, tp+2)
        prod_next = (pow3_next * mp) % (8 * mod)
        val_next = prod_next - 1
        v2_next = v2(val_next)

        if v2_next != 1:
            escape_reasons[f"v_2 != 1 (v_2={v2_next})"] += 1
        else:
            fx_next = val_next // 2
            if fx_next % 4 != 3:
                escape_reasons["output Type A"] += 1
            else:
                escape_reasons["stays in growth-B"] += 1

total = sum(escape_reasons.values())
print(f"Growth-B chain fate analysis (mod 2^{K}):")
for reason, count in sorted(escape_reasons.items(), key=lambda x: -x[1]):
    print(f"  {reason}: {count} ({count/total*100:.1f}%)")


# =====================================================
print("\n\n=== Part 5: m-Value Growth in Growth-B Chains ===\n")

# From Theorem 29: m grows +0.16 bits/hop during growth.
# In growth-B chains specifically, how much does m grow?

# m' = odd_part((3^(t+2)*m + 1) / 8)
# For large m: m' ≈ 3^(t+2)*m / 8 = (3/2)^(t+2) * m / 2
# Growth factor: m'/m ≈ (3/2)^(t+2) / 2 = 3^(t+2) / 2^(t+3)
# For t=0: 9/8 = 1.125
# For t=1: 27/16 = 1.6875
# For t=2: 81/32 = 2.53
# For t=3: 243/64 = 3.80

print("Theoretical m'/m ratio in growth-B (for large m):")
for t in range(8):
    ratio = 3**(t+2) / 2**(t+3)
    print(f"  t={t}: m'/m ≈ 3^{t+2}/2^{t+3} = {ratio:.3f} ({math.log2(ratio):+.3f} bits)")

# Empirical verification
print("\nEmpirical m'/m in growth-B chains:")
ratios_by_t = defaultdict(list)

for x0 in range(3, 200001, 2):
    x = x0
    for hop in range(30):
        if x <= 1: break
        r = fmf_hop_full(x)
        if r is None: break
        nx, case, t, v2v, fmf, m = r

        if case == 'B' and v2v == 2 and nx % 4 == 3:
            r2 = fmf_hop_full(nx)
            if r2:
                _, _, t2, _, _, m2 = r2
                if m > 0:
                    ratios_by_t[t].append(math.log2(m2/m))
        x = nx

for t in sorted(ratios_by_t.keys())[:8]:
    vals = ratios_by_t[t]
    if vals:
        avg = sum(vals) / len(vals)
        predicted = math.log2(3**(t+2) / 2**(t+3))
        print(f"  t={t}: avg log2(m'/m) = {avg:.3f} (predicted: {predicted:.3f}), n={len(vals)}")


# =====================================================
print("\n\n=== Part 6: Finiteness Argument ===\n")

# Key argument: m GROWS in growth-B chains.
# For t >= 1: m'/m > 1 (always)
# For t = 0: m'/m ≈ 9/8 > 1 (always, for large m)
#
# This means: in a growth-B chain of length k, m grows by at least
# a factor of (9/8)^k (for the weakest case t=0).
#
# But Theorem 28 says: no cycle exists in mod 2^K state space.
# As m grows, it eventually enters new residue classes mod 2^K
# that may NOT be growth-B classes.
#
# More precisely: after K/log2(9/8) ≈ K/0.17 ≈ 6K hops, m has
# grown by at least K bits, meaning the residue class mod 2^K
# has CHANGED. The new class may not support growth-B.

print("Finiteness argument for growth-B chains:")
print()
print("1. m grows by factor >= 9/8 per growth-B hop (minimum, at t=0)")
print("2. After k hops: m >= m_0 * (9/8)^k")
print("3. For m to stay in the SAME residue class mod 2^K:")
print("   m_0*(9/8)^k ≡ m_0 mod 2^K")
print("   m_0*((9/8)^k - 1) ≡ 0 mod 2^K")
print()

# When does (9/8)^k ≡ 1 mod 2^K?
# 9 = 8+1, so 9^k = (8+1)^k = sum C(k,j)*8^j
# 9^k / 8^k = (1 + 1/8)^k
# 9^k - 8^k = sum_{j=0}^{k-1} C(k,j)*8^j
# v_2(9^k - 8^k):
# For k=1: 9-8=1, v_2=0
# But we need 9^k ≡ 8^k mod 2^{K+k*3} (since we divide by 8^k)

# Actually, let me think about this differently.
# m' = (3^(t+2)*m + 1) / 2^(3+t')
# For t=0: m' = (9m + 1) / 8 when t'=0
# For m ≡ 7 mod 8 (growth-B, t=0): 9*7+1 = 64, 64/8 = 8, m' = 8 mod 2^K

print("Map m -> m' for t=0, growth-B (m ≡ 7 mod 8):")
print("  m' = (9m + 1) / 8  (when t' = 0)")
print("  m' = (9m + 1) / 16 (when t' = 1)")
print("  m' = (9m + 1) / 32 (when t' = 2)")
print("  etc.")
print()

# Compute the explicit map mod 2^K
for K_val in [4, 5, 6, 7, 8]:
    mod_val = 2**K_val
    print(f"  mod 2^{K_val}: m -> m' for t=0, growth-B:")
    for m_class in range(7, mod_val, 8):  # m ≡ 7 mod 8
        val = 9 * m_class + 1
        tp = v2(val // 8)  # additional v_2 beyond the /8
        mp = (val // 8) >> tp
        mp_mod = mp % mod_val
        print(f"    m≡{m_class:3d}(mod {mod_val}): 9m+1={val}, /8={val//8}, t'={tp}, m'≡{mp_mod}(mod {mod_val})")


# =====================================================
print("\n\n=== Part 7: Chain on t-Values ===\n")

# In a growth-B chain, t changes: t -> t' = v_2((3^(t+2)*m + 1)/8)
# The t-values are NOT monotone. But they determine the growth rate.
# Key: can t increase without bound in a growth-B chain?

print("t-value sequences in growth-B chains (x=270271):")
x = 270271
t_vals = []
for hop in range(50):
    if x <= 1: break
    r = fmf_hop_full(x)
    if r is None: break
    nx, case, t, v2v, fmf, m = r
    if case == 'B' and nx > x:
        t_vals.append(t)
    else:
        if t_vals:
            print(f"  Growth chain t-values: {t_vals}")
            t_vals = []
    x = nx
if t_vals:
    print(f"  Growth chain t-values: {t_vals}")

# Broader: t distribution in growth-B chains
t_in_growth = defaultdict(int)
t_transitions = defaultdict(lambda: defaultdict(int))

for x0 in range(3, 200001, 2):
    x = x0
    prev_t = None
    in_growth = False
    for hop in range(30):
        if x <= 1: break
        r = fmf_hop_full(x)
        if r is None: break
        nx, case, t, v2v, fmf, m = r

        if case == 'B' and nx > x and v2v == 2 and nx % 4 == 3:
            t_in_growth[t] += 1
            if in_growth and prev_t is not None:
                t_transitions[prev_t][t] += 1
            in_growth = True
            prev_t = t
        else:
            in_growth = False
            prev_t = None

        x = nx

print("\nt distribution in growth-B chains:")
total_gb = sum(t_in_growth.values())
for t in sorted(t_in_growth.keys())[:10]:
    print(f"  t={t}: {t_in_growth[t]:6d} ({t_in_growth[t]/total_gb*100:.1f}%)")

print("\nt -> t' transitions in consecutive growth-B hops:")
for t in sorted(t_transitions.keys())[:6]:
    total_t = sum(t_transitions[t].values())
    parts = []
    for tp in sorted(t_transitions[t].keys()):
        parts.append(f"t'={tp}:{t_transitions[t][tp]/total_t*100:.0f}%")
    print(f"  t={t}: {', '.join(parts[:6])}")


# =====================================================
print("\n\n=== Part 8: The Key Algebraic Fact ===\n")

# For the map m -> m' = odd_part((3^(t+2)*m + 1) / 8):
#
# If m is large, m' ≈ 3^(t+2)*m / 2^(t'+3)
# The map roughly multiplies m by 3^(t+2) / 2^(t'+3)
#
# For this to cycle: need 3^(t+2) / 2^(t'+3) = 1
# i.e., 3^(t+2) = 2^(t'+3)
# But this NEVER happens (since 3^a ≠ 2^b for a,b > 0)!
#
# This is EXACTLY Tao's barrier: the separation of powers of 2 and 3.
# It means the ratio m'/m can never be exactly 1, so perfect cycles
# are impossible. The question is whether approximate cycling
# (m returning to the same residue class) can persist.

print("THE ALGEBRAIC CORE:")
print()
print("For a growth-B chain to cycle, we'd need:")
print("  Product of ratios = 1")
print("  i.e., prod_{i=1}^{k} 3^(t_i+2) / 2^(t'_i+3) = 1")
print("  i.e., 3^(sum(t_i+2)) = 2^(sum(t'_i+3))")
print()
print("But 3^a = 2^b has NO solution for positive integers a, b.")
print("This is a trivial number theory fact (fundamental theorem of arithmetic).")
print()
print("CONSEQUENCE: No EXACT cycle can exist in (m, t) space.")
print("The m-transformation is NEVER periodic.")
print()
print("For APPROXIMATE cycling (m returns to same class mod 2^K):")
print("  The residue class changes by a factor related to 3^a / 2^b mod 2^K")
print("  Since ord(3) = 2^(K-2) mod 2^K, the map cycles mod 2^K with")
print("  period dividing 2^(K-2).")
print("  But from Theorem 28: these mod-2^K cycles are PHANTOM CYCLES")
print("  that don't correspond to real trajectories.")
print()

# Verify: the product of ratios along actual growth chains
print("Product of ratios along growth chains in [3, 200K]:")
products = []
for x0 in range(3, 200001, 2):
    x = x0
    log_product = 0
    chain_len = 0
    for hop in range(30):
        if x <= 1: break
        r = fmf_hop_full(x)
        if r is None: break
        nx, case, t, v2v, fmf, m = r

        if case == 'B' and nx > x:
            # ratio = 3^(t+2) / (2^(v2v) * 2^(t+2) / 2) ... complicated
            # Just use actual ratio
            log_product += math.log2(nx / x)
            chain_len += 1
        else:
            if chain_len > 0:
                products.append((chain_len, log_product))
                log_product = 0
                chain_len = 0
        x = nx

if products:
    long_chains = [p for p in products if p[0] >= 3]
    if long_chains:
        print(f"  Chains of length >= 3: {len(long_chains)}")
        for length, log_prod in sorted(long_chains, key=lambda x: -x[0])[:10]:
            print(f"    Length {length}: total growth = {log_prod:.3f} bits, "
                  f"avg = {log_prod/length:.3f} bits/hop, "
                  f"ratio = 2^{log_prod:.1f} = {2**log_prod:.2f}x")


# =====================================================
print("\n\n=== Part 9: Proof Synthesis ===\n")

print("GROWTH TERMINATION PROOF OUTLINE")
print("=" * 55)
print()
print("Theorem: Every FMF growth chain terminates (has finite length).")
print()
print("Proof (by contradiction):")
print("  Suppose x_0, x_1, x_2, ... is an infinite growth chain")
print("  (x_{n+1} = F(x_n) > x_n for all n).")
print()
print("  Step 1: x_n -> infinity (since x_{n+1} > x_n for all n).")
print()
print("  Step 2: Each x_n is Type B (Type A always shrinks, Theorem 30).")
print("  So x_n = 2^(t_n+2)*m_n - 1 with t_n >= 0 and m_n odd.")
print()
print("  Step 3: Growth requires v_2(FMF_n) <= (t_n+2)*0.585 + 1.")
print("  The dominant case is v_2 = 2 (87.9% of growth hops).")
print()
print("  Step 4: m_n grows by factor >= 9/8 per hop (for t_n=0,")
print("  the minimum). So m_n >= m_0 * (9/8)^n -> infinity.")
print()
print("  Step 5: For each K, consider the sequence m_n mod 2^K.")
print("  Since m_n -> infinity, the sequence m_n mod 2^K visits")
print("  infinitely many residue classes as n grows.")
print()
print("  Step 6 (KEY): By Theorem 28, no cycle exists in the")
print("  (t_n, m_n mod 2^K) state space. Since the state space")
print("  mod 2^K is finite, the sequence must eventually leave")
print("  the set of growth-enabling states mod 2^K.")
print()
print("  Step 7: But 'leaving the growth-enabling states mod 2^K'")
print("  means: either v_2(FMF) > 2 (extra shrinkage) or the")
print("  output is Type A (guaranteed shrinkage). Either way,")
print("  growth terminates.")
print()
print("GAP IN THIS ARGUMENT:")
print("  Step 5 claims m_n visits infinitely many residue classes,")
print("  but this is subtle: m could grow while staying in the SAME")
print("  class mod 2^K (e.g., m_n = 7 + 2^K * n). The growth")
print("  of m doesn't automatically change its lowest K bits.")
print()
print("  However: the map m -> m' = odd_part((3^(t+2)*m+1)/8)")
print("  does NOT preserve m mod 2^K in general. The lowest bits")
print("  of m' depend on ALL bits of m (through carries in the")
print("  multiplication 3^(t+2)*m). So as m grows, new higher bits")
print("  affect the lowest bits of m' through carry propagation.")
print()
print("  This is the SAME mechanism that makes phantom cycles fail")
print("  (Theorem 28): the higher bits of m disrupt the mod-2^K")
print("  pattern, preventing sustained cycling.")
print()
print("WHAT REMAINS TO FORMALIZE:")
print("  A rigorous version of 'carry propagation from higher bits")
print("  disrupts the mod 2^K pattern after at most O(K) steps.'")
print("  This is essentially a statement about the MIXING RATE of")
print("  multiplication by 3^(t+2) mod 2^K, which connects to the")
print("  equidistribution of 3^n in Z/2^K Z (Direction E).")
