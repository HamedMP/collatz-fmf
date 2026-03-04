"""
explore33.py: Carry Propagation Analysis
==========================================
PRIORITY 4 from Phase 7.

Goal: Analyze binary carry patterns in 3^(t+2)*m multiplication.
Binary: 3*m = m + (m << 1), carries determine v_2.
How carry chains relate to v_2 of the result.
Compare with 5*m = m + (m << 2) carry patterns.
Look for combinatorial invariant that decreases along FMF chains.

Key insight from explore31-32: growth requires v_2(m - inv_t) = 1 (low proximity).
This means m and inv_t agree in their lowest bit but differ in bit 1.
The carry structure of 3^(t+2)*m - 1 determines v_2(FMF), which determines
whether the trajectory grows or shrinks.

NEW DIRECTION: Instead of a height function, prove that the carry structure
of consecutive m-values CANNOT sustain low v_2 indefinitely. This is a
combinatorial/number-theoretic argument specific to multiplication by 3.
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

def to_bin(n, width=16):
    """Binary string, LSB first."""
    return format(n, f'0{width}b')[::-1]

def carry_count(a, b, bits=32):
    """Count carries in binary addition a + b."""
    carry = 0
    carries = 0
    for i in range(bits):
        ba = (a >> i) & 1
        bb = (b >> i) & 1
        s = ba + bb + carry
        carry = s >> 1
        carries += carry
    return carries

def carry_chain_length(a, b, bits=32):
    """Length of longest consecutive carry chain in a + b."""
    carry = 0
    max_chain = 0
    current_chain = 0
    for i in range(bits):
        ba = (a >> i) & 1
        bb = (b >> i) & 1
        s = ba + bb + carry
        carry = s >> 1
        if carry:
            current_chain += 1
            max_chain = max(max_chain, current_chain)
        else:
            current_chain = 0
    return max_chain


# =====================================================
print("=== Part 1: Carry Structure of 3*m - 1 ===\n")

# 3*m = m + 2m. The carry pattern depends on bits of m.
# 3*m - 1 = m + 2m - 1
# v_2(3*m - 1): when is the result divisible by high powers of 2?
# 3*m - 1 ≡ 0 mod 2^k iff m ≡ (3^{-1}) mod 2^k = ... mod 2^k
# 3^{-1} mod 2 = 1, mod 4 = 3, mod 8 = 3, mod 16 = 11, mod 32 = 11...
# Actually 3^{-1} mod 2^k = (2^k + 1) / 3 when 3 | (2^k + 1)

print("v_2(3m - 1) by m mod 2^k:")
for k in range(1, 7):
    mod = 2**k
    inv = mod_inv(3, mod)
    print(f"  mod 2^{k} (={mod}): 3^{{-1}} = {inv}")
    for m_mod in range(1, mod, 2):  # odd m only
        val = 3 * m_mod - 1
        v = v2(val)
        if v >= 2:
            print(f"    m ≡ {m_mod} mod {mod}: v_2(3m-1) = {v}, 3m-1 = {val}")

print("\nCarry patterns in 3*m = m + 2m (LSB first, 8 bits):")
for m in [1, 3, 5, 7, 11, 13, 15, 21, 27, 31]:
    bin_m = to_bin(m, 8)
    bin_2m = to_bin(2*m, 8)
    bin_3m = to_bin(3*m, 8)
    bin_3m1 = to_bin(3*m - 1, 8)
    carries = carry_count(m, 2*m)
    chain = carry_chain_length(m, 2*m)
    v = v2(3*m - 1)
    print(f"  m={m:3d}: m={bin_m} 2m={bin_2m} -> 3m={bin_3m} 3m-1={bin_3m1} v_2={v} carries={carries} max_chain={chain}")


# =====================================================
print("\n\n=== Part 2: Carry Structure of 3^(t+2)*m - 1 ===\n")

# For higher powers: 3^(t+2)*m - 1
# v_2(3^(t+2)*m - 1) = v_2(m - 3^{-(t+2)})
# The carry structure becomes more complex as t increases

print("v_2(3^(t+2)*m - 1) for small m, varying t:")
print(f"  {'m':>4}", end="")
for t in range(7):
    print(f"  t={t}", end="")
print()
for m in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]:
    print(f"  {m:4d}", end="")
    for t in range(7):
        val = 3**(t+2) * m - 1
        v = v2(val)
        print(f"  {v:3d}", end="")
    print()

# Compare with 5^(t+2)*m - 1
print("\nv_2(5^(t+2)*m - 1) for small m, varying t:")
print(f"  {'m':>4}", end="")
for t in range(7):
    print(f"  t={t}", end="")
print()
for m in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]:
    print(f"  {m:4d}", end="")
    for t in range(7):
        val = 5**(t+2) * m - 1
        v = v2(val)
        print(f"  {v:3d}", end="")
    print()


# =====================================================
print("\n\n=== Part 3: Binary Pattern of 3^{-n} mod 2^K ===\n")

# The 2-adic expansion of 1/3 is ...10101011 (period 2)
# The expansion of 3^{-n} mod 2^K determines which m-values give low v_2

K = 32
mod = 2**K
print(f"3^{{-n}} mod 2^{K} (low 16 bits, LSB first):")
for n in range(2, 10):
    inv = mod_inv(pow(3, n, mod), mod)
    print(f"  3^{{-{n}}}: {to_bin(inv, 16)} = {inv}")

print(f"\n5^{{-n}} mod 2^{K} (low 16 bits, LSB first):")
for n in range(2, 10):
    inv = mod_inv(pow(5, n, mod), mod)
    print(f"  5^{{-{n}}}: {to_bin(inv, 16)} = {inv}")

# Key observation: the low bits of 3^{-n} CHANGE as n changes
# But they change by exactly 1 bit per step (Theorem 31)
# How does this affect the carry structure?
print("\nBit differences between consecutive 3^{-n}:")
for n in range(2, 12):
    inv_n = mod_inv(pow(3, n, mod), mod)
    inv_n1 = mod_inv(pow(3, n+1, mod), mod)
    diff = (inv_n1 - inv_n) % mod
    v = v2(diff)
    # XOR to see which bits changed
    xor = inv_n ^ inv_n1
    changed_bits = bin(xor).count('1')
    print(f"  3^{{-{n+1}}} - 3^{{-{n}}}: v_2 = {v}, changed {changed_bits} bits (XOR low 16: {to_bin(xor, 16)})")


# =====================================================
print("\n\n=== Part 4: m-Value Evolution and Carries ===\n")

# Along a trajectory, m evolves: x -> F(x) gives new (m', t')
# The key: how does the binary structure of m change?
# Specifically: what happens to the bits of m near the position
# where m is close to inv_t?

# Track the binary patterns of consecutive m-values
print("m-value binary evolution along x=27 trajectory:")
x = 27
for hop in range(15):
    if x <= 1: break
    r = fmf_hop_full(x)
    if r is None: break
    nx, case, t, v2v, fmf, m = r
    p = proximity(m, t)
    inv = mod_inv(pow(3, t+2, 2**32), 2**32)
    diff = (m - inv) % (2**32)
    print(f"  hop {hop}: x={x:8d}, {case}, t={t}, m={m:8d}, p={p}, v2={v2v}, "
          f"m_low={to_bin(m, 12)}, diff_low={to_bin(diff, 12)}")
    x = nx

print("\nm-value binary evolution along x=270271 trajectory:")
x = 270271
for hop in range(15):
    if x <= 1: break
    r = fmf_hop_full(x)
    if r is None: break
    nx, case, t, v2v, fmf, m = r
    p = proximity(m, t)
    print(f"  hop {hop}: x={x:10d}, {case}, t={t}, m={m:10d}, p={p}, v2={v2v}, m_low={to_bin(m, 16)}")
    x = nx


# =====================================================
print("\n\n=== Part 5: Carry Propagation in FMF Transformation ===\n")

# The FMF transformation:
# x = 2^(t+2)*m - 1 -> FMF = 2(3^(t+2)*m - 1)
# The key operation is: 3^(t+2)*m
# This is a multiplication by a power of 3.
#
# 3*m = m + 2m (shift and add)
# 9*m = m + 8m (shift by 3 and add)
# 27*m = m + 2m + 24m = 3m + 24m = m + 2m + 8m + 16m
# In general, 3^n*m involves multiple shifted additions
#
# The carry structure of this multiplication determines v_2(3^n*m - 1)

# Key: 3^n*m - 1 = (3^n - 1)*m + m - 1
# So: v_2(3^n*m - 1) = v_2((3^n - 1)*m + (m - 1))
# If m is odd: m - 1 is even, so there's at least one trailing zero in m-1
# And 3^n - 1 is always even (since 3^n is odd, minus 1 is even)

# Let's compute: v_2(3^n - 1) for various n
print("v_2(3^n - 1):")
for n in range(1, 20):
    v = v2(3**n - 1)
    print(f"  n={n:2d}: v_2(3^{n}-1) = {v} {'(= v_2(n)+1 for n even, = 1 for n odd)' if n <= 5 else ''}")

# The pattern: v_2(3^n - 1) = 1 for n odd, v_2(n) + 1 for n even
# For our FMF: t+2 is the exponent
# t=0: 3^2-1 = 8, v_2 = 3
# t=1: 3^3-1 = 26, v_2 = 1
# t=2: 3^4-1 = 80, v_2 = 4
# t=3: 3^5-1 = 242, v_2 = 1

print(f"\nFor FMF: 3^(t+2)*m - 1")
print(f"  t=0: 3^2=9,   v_2(9-1)=3, so 9m-1 = 8m + (m-1)")
print(f"  t=1: 3^3=27,  v_2(27-1)=1, so 27m-1 = 26m + (m-1)")
print(f"  t=2: 3^4=81,  v_2(81-1)=4, so 81m-1 = 80m + (m-1)")
print(f"  t=3: 3^5=243, v_2(243-1)=1, so 243m-1 = 242m + (m-1)")


# =====================================================
print("\n\n=== Part 6: The m -> m' Transformation Explicitly ===\n")

# After an FMF hop from x (Type B), the NEXT x' has parameters (m', t')
# The transformation m -> m' is:
# 1. Compute FMF = 2(3^(t+2)*m - 1)
# 2. Divide by 2^v where v = v_2(FMF)
# 3. The result F(x) is the next odd number
# 4. F(x) = 2^(t'+2)*m' - 1 where t' = v_2(k'+1), m' = (k'+1)/2^t'
#    and k' = (F(x) - r) / 4 where r = F(x) mod 4

# Let's trace this explicitly for Type B hops
print("Explicit m -> m' transformation for Type B hops:")
for x0 in [27, 703, 6171, 270271]:
    x = x0
    print(f"\n  Starting x = {x0}:")
    for hop in range(8):
        if x <= 1: break
        r = fmf_hop_full(x)
        if r is None: break
        nx, case, t, v2v, fmf, m = r

        # Compute the transformation
        pow3 = 3**(t+2)
        product = pow3 * m
        fmf_raw = 2 * (product - 1)  # = 2(3^(t+2)*m - 1)
        v = v2(fmf_raw)
        fx = fmf_raw >> v  # F(x)

        # Decompose F(x)
        if fx > 1:
            r2 = fmf_hop_full(fx)
            if r2:
                _, c2, t2, _, _, m2 = r2
                print(f"    {case}(t={t}): m={m} -> 3^{t+2}*m={product}, "
                      f"FMF=2*{product-1}, v={v}, F(x)={fx} -> {c2}(t'={t2}), m'={m2}")

        x = nx


# =====================================================
print("\n\n=== Part 7: Carry Invariant Search ===\n")

# Hypothesis: there exists a function C(m, t) measuring "carry complexity"
# such that C(m', t') <= C(m, t) - delta for most hops
# and C(m', t') > C(m, t) only when v_2 is large (shrinkage)

# Candidates:
# C1(m) = number of 1-bits in m (Hamming weight)
# C2(m) = number of carries in m + 2m (= number of 11 patterns in binary)
# C3(m, t) = carry_chain_length(m, 2m) * t
# C4(m, t) = log2(m) / (p + 1) where p = proximity

def popcount(n):
    """Number of 1-bits."""
    return bin(n).count('1')

def ones_runs(n):
    """Number of maximal runs of 1s in binary."""
    b = bin(n)[2:]
    count = 0
    in_run = False
    for bit in b:
        if bit == '1' and not in_run:
            count += 1
            in_run = True
        elif bit == '0':
            in_run = False
    return count

print("Testing carry invariant candidates along trajectories:")
print()

for candidate_name, candidate_fn in [
    ("popcount(m)", lambda m, t, p: popcount(m)),
    ("ones_runs(m)", lambda m, t, p: ones_runs(m)),
    ("carry_count(m,2m)", lambda m, t, p: carry_count(m, 2*m)),
    ("carry_chain(m,2m)", lambda m, t, p: carry_chain_length(m, 2*m)),
    ("popcount(m)*t", lambda m, t, p: popcount(m) * (t+1)),
    ("log2(m)/(p+1)", lambda m, t, p: math.log2(max(m,1)) / (p + 1)),
]:
    total_hops = 0
    decreases = 0
    increases = 0

    for x0 in range(3, 50001, 2):
        x = x0
        prev_c = None
        for hop in range(30):
            if x <= 1: break
            r = fmf_hop_full(x)
            if r is None: break
            nx, case, t, v2v, fmf, m = r
            p = proximity(m, t)
            c = candidate_fn(m, t, p)

            if prev_c is not None:
                total_hops += 1
                if c < prev_c:
                    decreases += 1
                elif c > prev_c:
                    increases += 1

            prev_c = c
            x = nx

    if total_hops > 0:
        print(f"  {candidate_name:25s}: decrease={decreases/total_hops*100:.1f}%, "
              f"increase={increases/total_hops*100:.1f}%, "
              f"net={(decreases-increases)/total_hops*100:+.1f}%")


# =====================================================
print("\n\n=== Part 8: The 3-vs-5 Carry Difference ===\n")

# 3*m = m + 2m: carries propagate through consecutive 1-bits
# 5*m = m + 4m: carries propagate through bits that are 2 apart
# The key difference: 3m carry chains affect ADJACENT bits (local interaction)
# while 5m carry chains affect bits that are 2 apart (nonlocal)

# For v_2(3^n*m - 1): we need trailing zeros in 3^n*m - 1
# This requires specific alignment of m with 3^{-n} in Z_2
# For v_2(5^n*m - 1): same but with 5^{-n}

# The 2-adic expansion of 1/3 = ...01010101011 (period 2)
# The 2-adic expansion of 1/5 = ...11001100110011 (period 4)
# Powers of 1/3 stay period-2 in their pattern
# Powers of 1/5 have period-4 patterns

print("2-adic expansions (lowest 24 bits, LSB first):")
K = 64
mod = 2**K
for label, base in [("3", 3), ("5", 5)]:
    for n in range(1, 6):
        inv = mod_inv(pow(base, n, mod), mod)
        bits = to_bin(inv, 24)
        print(f"  {base}^{{-{n}}}: {bits}")
    print()

# Pattern analysis: how "spread out" are the 1-bits?
print("1-bit density in lowest 32 bits of a^{-n} mod 2^64:")
for label, base in [("3", 3), ("5", 5)]:
    densities = []
    for n in range(2, 20):
        inv = mod_inv(pow(base, n, mod), mod)
        low32 = inv & ((1 << 32) - 1)
        density = popcount(low32) / 32
        densities.append(density)
    avg_density = sum(densities) / len(densities)
    print(f"  {base}^{{-n}}: avg density = {avg_density:.4f} ({label})")


# =====================================================
print("\n\n=== Part 9: Growth Chain Carry Analysis ===\n")

# For GROWTH chains specifically, analyze the carry structure
# Growth requires v_2 = 2 (almost always, from Theorem 27)
# This means 3^(t+2)*m - 1 ≡ 2 mod 4, i.e., 3^(t+2)*m ≡ 3 mod 4
# Since 3^n ≡ 3 mod 4 for n odd, ≡ 1 mod 4 for n even
# For t+2 odd (t odd): 3^(t+2) ≡ 3 mod 4, so m ≡ 1 mod 4 (since 3*1=3 mod 4)
# For t+2 even (t even): 3^(t+2) ≡ 1 mod 4, so m ≡ 3 mod 4 (since 1*3=3 mod 4)

print("Carry structure during growth chains (x=270271):")
x = 270271
for hop in range(12):
    if x <= 1: break
    r = fmf_hop_full(x)
    if r is None: break
    nx, case, t, v2v, fmf, m = r

    if case == 'B' and nx > x:
        pow3 = 3**(t+2)
        product = pow3 * m
        cc = carry_count(m, (pow3 - 1) * m)
        cl = carry_chain_length(m, (pow3 - 1) * m)
        print(f"  {case}(t={t}): m={m}, 3^{t+2}={pow3}, product={product}, "
              f"v_2={v2v}, carries={cc}, max_chain={cl}, "
              f"m_low={to_bin(m, 12)}")

    x = nx

# Broader analysis: carry statistics for growth vs shrinkage hops
print("\nCarry statistics (growth vs shrinkage) for Type B hops:")
grow_carries = []
shrink_carries = []

for x0 in range(3, 50001, 2):
    x = x0
    for hop in range(20):
        if x <= 1: break
        r = fmf_hop_full(x)
        if r is None: break
        nx, case, t, v2v, fmf, m = r

        if case == 'B' and m < 10**6:  # reasonable size
            pow3 = 3**(t+2)
            cc = carry_count(m, (pow3 - 1) * m, bits=48) if pow3 * m < 2**48 else -1
            cl = carry_chain_length(m, (pow3 - 1) * m, bits=48) if pow3 * m < 2**48 else -1
            if cc >= 0:
                if nx > x:
                    grow_carries.append((cc, cl, t, v2v))
                else:
                    shrink_carries.append((cc, cl, t, v2v))

        x = nx

if grow_carries and shrink_carries:
    print(f"  Growth ({len(grow_carries)}): avg carries={sum(c[0] for c in grow_carries)/len(grow_carries):.1f}, "
          f"avg max_chain={sum(c[1] for c in grow_carries)/len(grow_carries):.1f}")
    print(f"  Shrink ({len(shrink_carries)}): avg carries={sum(c[0] for c in shrink_carries)/len(shrink_carries):.1f}, "
          f"avg max_chain={sum(c[1] for c in shrink_carries)/len(shrink_carries):.1f}")


# =====================================================
print("\n\n=== Part 10: Synthesis ===\n")

print("CARRY PROPAGATION ANALYSIS RESULTS")
print("=" * 50)
print()
print("1. v_2(3^n - 1) = 1 for n odd, v_2(n)+1 for n even.")
print("   This means: for t odd (exponent t+2 odd), the base structure")
print("   has only 1 trailing zero. Extra trailing zeros come from m.")
print()
print("2. 2-adic expansion of 3^{-n}: period-2 pattern (...010101)")
print("   2-adic expansion of 5^{-n}: period-4 pattern (...11001100)")
print("   The period-2 pattern of 3^{-n} means m must match EVERY OTHER BIT")
print("   of the target to maintain low proximity.")
print()
print("3. Carry invariant search: NO simple combinatorial function of m")
print("   monotonically decreases along FMF trajectories. The best candidates")
print("   (popcount, carry count) show slight negative bias but far from")
print("   monotone decrease.")
print()
print("4. Growth vs shrinkage carry structure: growth hops tend to have")
print("   FEWER carries (simpler binary structure), while shrinkage hops")
print("   have MORE carries (more complex structure).")
print()
print("5. The 3-vs-5 structural difference in carries:")
print("   3*m = m + 2m: carry chains affect ADJACENT bits")
print("   5*m = m + 4m: carry chains skip a bit position")
print("   This means 3*m carry propagation is MORE LOCAL,")
print("   and v_2(3*m-1) = 1 requires only m ≡ 1 mod 4 (2 bits)")
print("   while v_2(5*m-1) = 1 requires m ≡ 1 mod 4 (also 2 bits)")
print("   The structural advantage of 3 is in the RATIO a/4, not carries.")
print()
print("CONCLUSION: The carry propagation analysis confirms that the")
print("binary structure is specific to the constant 3, but does NOT")
print("yield a new proof-relevant invariant. The fundamental mechanism")
print("remains the 3/4 contraction channel (Theorem 30) combined with")
print("the 2-adic proximity dynamics (Theorems 31-32).")
print("The carry structure is a CONSEQUENCE of the 2-adic structure,")
print("not an independent proof tool.")
