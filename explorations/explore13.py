"""
explore13.py - Cycle Exclusion in FMF Chains

A cycle in the FMF graph would mean some odd number x maps back to itself
after n hops: F^n(x) = x.

For this to happen, the product of all multipliers must equal 1 exactly:
  product of (F^j(x) / F^{j-1}(x)) = 1

This means: 3^s / 2^d = 1, i.e., 3^s = 2^d, where s is total 3x+1 ops
and d is total /2 ops across the cycle.

Since log_2(3) is irrational, 3^s = 2^d only when s = d = 0.

But wait -- the +1 and -1 constants in the formulas mean this isn't exactly
3^s = 2^d. We need to be more careful.

Let's analyze what constraints a cycle would impose.
"""
from math import log2, gcd
from fractions import Fraction


def v2(n):
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


def fmf_hop(x):
    """Returns (next_odd, case, t_value, num_3x1_ops, num_div2_ops)."""
    mod4 = x % 4
    if mod4 == 1:
        k = (x - 1) // 4
        fmf = 4 * (3 * k + 1)
        p = v2(fmf)
        return fmf >> p, 'A', 0, 1, p + 0  # 1 multiply by 3, then p divides by 2
    elif mod4 == 3:
        k = (x - 3) // 4
        if k % 2 == 0:
            j = k // 2
            fmf = 4 * (9 * j + 4)
            p = v2(fmf)
            # 3 Collatz steps: 3x+1, /2, 3y+1 = 2 multiplies by 3, 1 internal /2
            return fmf >> p, 'B0', 0, 2, 1 + p
        else:
            t = v2(k + 1)
            fmf = 3**(t + 2) * (k + 1) // 2**(t - 1) - 2
            p = v2(fmf)
            # 3+2t Collatz steps: (t+2) multiplies by 3, (t+1) internal /2s
            return fmf >> p, 'Bt', t, t + 2, t + 1 + p
    return None, '', 0, 0, 0


# === Part 1: What would a cycle look like? ===
print("=== Part 1: Constraints on FMF Cycles ===\n")

print("For a cycle x -> F(x) -> F^2(x) -> ... -> F^n(x) = x:")
print("  Total 3x+1 operations: s")
print("  Total /2 operations: d")
print("  The exact relationship is NOT simply 3^s = 2^d")
print("  because of the +1 and -1 additive constants.\n")

print("The exact relationship for one Type A hop (x = 4k+1):")
print("  F(x) = (3x+1)/2^v = (3x+1)/2^v")
print("  So x_1 = (3x_0 + 1) / 2^{v_0}")
print()
print("For a cycle of length n:")
print("  x_0 -> x_1 -> ... -> x_n = x_0")
print("  x_{i+1} = (a_i * x_i + b_i) / 2^{v_i}")
print("  where a_i, b_i depend on the hop type.\n")

# For a cycle x -> x, we need:
# x = ((product of a_i) * x + sum of correction terms) / (product of 2^v_i)
# Let A = product of a_i, D = product of 2^v_i
# x * D = A * x + corrections
# x * (D - A) = corrections
# x = corrections / (D - A)
# For a cycle to exist, D != A and corrections/(D-A) must be a positive odd integer.

# In the pure 3n+1 problem, the constraint for a cycle of length n:
# Going through n odd numbers x_1, ..., x_n with:
# x_{i+1} = (3*x_i + 1) / 2^{k_i}
# Then: x_1 = (3^n * x_1 + (3^{n-1} + 3^{n-2}*2^{k_1} + ...)) / 2^{k_1+...+k_n}
# x_1 * (2^K - 3^n) = S (some positive integer depending on the k_i)
# For x_1 > 0, need 2^K > 3^n, i.e., K > n*log_2(3) ≈ 1.585*n

print("=== Part 2: Standard Cycle Constraint ===\n")
print("For a cycle visiting n odd numbers with total /2 count = K:")
print("  x_1 * (2^K - 3^n) = S > 0")
print("  Requires: K > n * log_2(3) ≈ 1.585n")
print("  And: (2^K - 3^n) must divide S\n")

# The FMF framework compresses multiple steps, but the constraint is the same
# because each FMF hop is just a sequence of standard Collatz steps.
# A cycle in the FMF graph IS a cycle in the Collatz graph (visiting odd numbers only).

# Known results on Collatz cycles:
# - Any cycle (other than 1->1) must have length > 10^8 (Eliahou 1993)
# - For n odd steps with total k = sum of exponents:
#   x = sum_{j=0}^{n-1} 3^j * 2^{k_{j+1}+...+k_n} / (2^k - 3^n)
#   This must be a positive integer

# Let's compute for small cycle lengths what x would need to be:
print("=== Part 3: Minimum x for hypothetical cycles ===\n")
print(f"{'n (odd steps)':>14} {'K min':>6} {'K max':>6} {'2^K - 3^n':>15} {'min cycle x':>15}")

for n in range(1, 25):
    K_min = int(n * log2(3)) + 1  # minimum K for 2^K > 3^n
    K_max = 2 * n  # reasonable upper bound

    three_n = 3**n
    best_x = None
    best_K = None

    for K in range(K_min, K_max + 5):
        denom = 2**K - three_n
        if denom <= 0:
            continue

        # The numerator S is bounded: S < n * 3^n (rough upper bound)
        # The minimum x in a cycle is at least 1
        # x = S / denom, and S depends on the specific k_i values
        # For the simplest case (all k_i = K/n approximately):
        # S = sum_{j=0}^{n-1} 3^j * 2^{K*(n-1-j)/n} approximately
        # which is roughly (2^K - 3^n) * n / (something)

        # Actually, the minimum possible x in a cycle with n odd numbers:
        # By Steiner (1977): x > 2^(K/(n+1))
        # By Eliahou (1993): for n > 1, any cycle has min element > 2^40
        min_x = 2**(K/(n+1)) if K > 0 else 1

        if best_x is None or min_x < best_x:
            best_x = min_x
            best_K = K

    if n <= 20:
        print(f"{n:>14} {K_min:>6} {K_max:>6} {2**K_min - three_n:>15} {best_x:>15.0f}")


# === Part 4: FMF-specific cycle analysis ===
print("\n\n=== Part 4: FMF-Specific Cycle Analysis ===\n")
print("In the FMF framework, a cycle visits odd numbers x_1, ..., x_n")
print("where each transition is an FMF hop (possibly multiple Collatz steps).\n")

# For each hop i, if x_i is Type A:
#   x_{i+1} = (3*x_i + 1) / 2^{v_i}, contributing 1 multiply-by-3
# If x_i is Type B with t-value t_i:
#   Contributes (t_i + 2) multiplies-by-3

# Total 3x operations: s = sum of (1 for A, t_i+2 for B with t_i)
# Total /2 operations: K = total of all divisions

# For a cycle: 2^K - 3^s must divide the correction sum.

print("Checking: can short FMF cycles exist?\n")
# Try to find any cycle of FMF length 1, 2, 3, ...
# Length 1: F(x) = x. Need (3x+1)/2^v = x for Type A -> 3x+1 = x*2^v -> x(2^v-3) = 1 -> x=1 only if v=2
# Length 2: F(F(x)) = x.

for cycle_len in range(1, 6):
    print(f"--- FMF cycle length {cycle_len} ---")
    # For each possible sequence of (type, t-value) patterns:
    # This grows exponentially, so just check a few cases

    # Type A only:
    s_a = cycle_len  # each A contributes 1 multiply
    print(f"  All Type A: s={s_a} multiplies-by-3")
    # Need 2^K = 3^{s_a} * x + corrections, with x = corrections/(2^K - 3^s_a)
    # The key: 2^K > 3^{s_a}, so K >= ceil(s_a * log2(3)) = ceil({s_a * 1.585})
    K_min = int(s_a * log2(3)) + 1
    for K in range(K_min, K_min + 5):
        denom = 2**K - 3**s_a
        if denom > 0:
            # For all-A cycle, the correction sum can be computed
            # For cycle a->a with both Type A:
            # x1 = (3x0+1)/2^k0, x0 = (3x1+1)/2^k1
            # x0 = (3*(3x0+1)/2^k0 + 1)/2^k1 = (9x0 + 3 + 2^k0)/(2^(k0+k1))
            # x0 * 2^(k0+k1) = 9x0 + 3 + 2^k0
            # x0 * (2^K - 9) = 3 + 2^k0 where K = k0+k1
            if cycle_len == 2 and denom > 0:
                for k0 in range(1, K):
                    k1 = K - k0
                    numerator = 3 + 2**k0
                    if numerator % denom == 0:
                        x0 = numerator // denom
                        if x0 > 0 and x0 % 2 == 1 and x0 % 4 == 1:
                            print(f"    K={K}, k0={k0}, k1={k1}: x0={x0}")
                            # Verify
                            x1 = (3*x0 + 1) >> v2(3*x0+1)
                            x_back = (3*x1 + 1) >> v2(3*x1+1)
                            print(f"    Verify: {x0} -> {x1} -> {x_back}, cycle={'YES' if x_back == x0 else 'NO'}")
            print(f"    K={K}: 2^{K} - 3^{s_a} = {denom}")


# === Part 5: Steiner's bound applied to FMF ===
print("\n\n=== Part 5: Lower Bounds on Cycle Elements ===\n")
print("Known results (from standard Collatz cycle theory):")
print("  - Steiner (1977): min element > 2^{K/(n+1)} where K = total /2 ops")
print("  - Eliahou (1993): any non-trivial cycle has length > 10^8")
print("  - Verified computationally: no cycle for x < 20 * 2^58 ≈ 5.76 * 10^18\n")

print("Combined with FMF compression ratio (~6 steps/hop):")
print("  A cycle of n FMF hops ≈ 6n Collatz steps")
print("  Minimum cycle in Collatz: > 10^8 steps")
print("  Minimum FMF cycle: > 10^8 / 6 ≈ 1.67 * 10^7 hops")
print("  With negative expected drift of -0.83 bits/hop:")
print("  P(returning to start after n hops) ≈ exp(-0.83n)")
print("  For n = 10^7: P ≈ exp(-8.3 * 10^6) ≈ 0  (effectively impossible)")


# === Part 6: Exact cycle constraint from FMF ===
print("\n\n=== Part 6: Why 3^s = 2^d is impossible (for s, d > 0) ===\n")
print("Fundamental Theorem of Arithmetic:")
print("  3^s and 2^d share no prime factors.")
print("  3^s = 2^d has no solution for s, d > 0.\n")

print("But Collatz cycles need 2^K > 3^n (not equality).")
print("The constraint is: x * (2^K - 3^n) = S")
print("where S is a sum of terms involving the specific division pattern.\n")

print("The FMF framework helps by providing EXACT formulas for S:")
print("  Each hop contributes a known term to the correction sum.")
print("  For Type A: correction = 1 (from the +1 in 3x+1)")
print("  For Type B(t): correction involves 3^(t+2)/(2^(t-1))")
print()

# The key insight: for a cycle to exist, 2^K - 3^n must be "small enough"
# relative to the correction terms. But 2^K - 3^n grows exponentially
# while the corrections grow at a rate determined by the cycle structure.

# Check how close 2^K can be to 3^n:
print("Closest approaches of 2^K to 3^n (|2^K - 3^n| / 3^n):")
closest = []
for n in range(1, 100):
    three_n = 3**n
    K = round(n * log2(3))
    for k in [K-1, K, K+1]:
        if k > 0:
            ratio = abs(2**k - three_n) / three_n
            closest.append((ratio, n, k))

closest.sort()
for ratio, n, k in closest[:15]:
    print(f"  n={n:>3}, K={k:>4}: |2^K - 3^n|/3^n = {ratio:.10f}, 2^K - 3^n = {2**k - 3**n}")
