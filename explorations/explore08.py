"""
explore08.py - Generalized FMF: first multiple of 2^p in Collatz sequence

The FMF formula tells us when x=4k+3 first reaches a multiple of 4 (2^2).
Can we generalize to "first multiple of 2^p" (FMP)?

This would be powerful because: if we can predict v_2(FMF) exactly
(not just that it's ≥ 2), we can compute the LPT and thus the exact
odd number after the FMF step.

Key idea: From the proof, FMF = 2(3^(t+2)*m - 1).
v_2(FMF) = 1 + v_2(3^(t+2)*m - 1)

And v_2(3^(t+2)*m - 1) depends on m mod 2^something.
Since 3^(t+2) is odd, its inverse mod 2^n exists.
3^(t+2)*m ≡ 1 (mod 2^v) iff m ≡ (3^(t+2))^{-1} (mod 2^v)

So v_2(3^(t+2)*m - 1) = v_2(m - inv) where inv = (3^(t+2))^{-1} mod 2^large
i.e., the 2-adic valuation is determined by how closely m matches the
2-adic inverse of 3^(t+2).
"""


def v2(n):
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


def tzb(k):
    return v2(k + 1)


def mod_inverse_2adic(a, precision=64):
    """Compute a^{-1} mod 2^precision for odd a, using Hensel lifting."""
    # Start: a * 1 ≡ a mod 2. Since a is odd, a ≡ 1 mod 2, so inv = 1 works mod 2.
    inv = 1
    for i in range(1, precision):
        # Lift: if a*inv ≡ 1 mod 2^i, make it work mod 2^(i+1)
        if (a * inv) % (2**(i+1)) != 1:
            inv += 2**i
    return inv


# Part 1: Compute 2-adic inverses of 3^(t+2)
print("=== 2-adic inverses of 3^(t+2) (mod 2^20) ===")
for t in range(1, 10):
    n = t + 2
    a = pow(3, n)
    inv = mod_inverse_2adic(a, 20)
    print(f"t={t}, 3^{n}={a:>10}, inv mod 2^20 = {inv:>10}, "
          f"verify: {a}*{inv} mod 2^20 = {(a*inv) % 2**20}")


# Part 2: v_2(FMF) as a function of m, explained by distance to 2-adic inverse
print(f"\n\n=== v_2(3^(t+2)*m - 1) = v_2(m - inv_2adic) ===")
for t in [1, 2, 3]:
    n = t + 2
    a = pow(3, n)
    inv = mod_inverse_2adic(a, 20)
    print(f"\nt={t}, 3^{n}={a}, 2-adic inv = {inv} = {bin(inv)}")
    print(f"  inv mod 4 = {inv % 4}, inv mod 8 = {inv % 8}, inv mod 16 = {inv % 16}, inv mod 32 = {inv % 32}")
    print(f"  {'m':>5} {'m binary':>15} {'v2(3^n*m-1)':>12} {'m-inv mod 2^6':>15} {'v2(m-inv)':>10}")
    for m in range(1, 32, 2):
        val = a * m - 1
        v = v2(val)
        diff = (m - inv) % 64
        v_diff = v2(m - (inv % 64)) if m != inv % 64 else "inf"
        # Actually compute v_2(m - inv) properly in Z
        diff_actual = m - inv
        v_actual = v2(abs(diff_actual)) if diff_actual != 0 else "inf"
        print(f"  {m:>5} {bin(m):>15} {v:>12} {diff:>15} {v_actual!s:>10}")


# Part 3: The EXACT v_2(FMF) formula
# v_2(FMF) = 1 + v_2(3^(t+2)*m - 1)
# And 3^(t+2)*m - 1 = 3^(t+2)*(m - inv_2adic(3^(t+2)))  where the multiplication
# is in the 2-adic sense. Actually more precisely:
# 3^n * m - 1 = 3^n * (m - (3^n)^{-1}) in Z_2
# v_2(3^n * m - 1) = v_2(3^n) + v_2(m - (3^n)^{-1}) = 0 + v_2(m - inv)
# since 3^n is a 2-adic unit.
# So v_2(FMF) = 1 + v_2(m - inv_2adic(3^(t+2)))
# This is exact and deterministic!

print(f"\n\n=== EXACT v_2(FMF) formula verification ===")
print(f"v_2(FMF) = 1 + v_2(m - 3^(-(t+2)) mod 2^N)")
errors = 0
total = 0
for t in range(1, 10):
    n = t + 2
    a = pow(3, n)
    inv = mod_inverse_2adic(a, 30)
    for m in range(1, 200, 2):
        fmf = 2 * (a * m - 1)
        v_actual = v2(fmf)
        # Our formula: 1 + v_2(m - inv)
        # But inv is huge. We need v_2(m - inv) in the 2-adic sense.
        # In integers: m - inv is a large negative number. v_2 of it equals v_2(inv - m).
        diff = abs(m - inv)
        v_predicted = 1 + v2(diff) if diff > 0 else None
        total += 1
        if v_predicted != v_actual and diff > 0:
            errors += 1
            if errors <= 5:
                print(f"  MISMATCH: t={t}, m={m}, v_actual={v_actual}, v_predicted={v_predicted}")

print(f"Verified {total} cases: {errors} errors")


# Part 4: What does this mean for descent?
# After FMF, odd_after = FMF / 2^v_2(FMF) = (3^(t+2)*m - 1) / 2^v_2(3^(t+2)*m-1)
# = (3^(t+2)*m - 1) / 2^v_2(m - inv)
# For descent, we need odd_after < x = 2^(t+2)*m - 1
# i.e., (3^(t+2)*m - 1) / 2^v < 2^(t+2)*m - 1
# For large m: 3^(t+2) / 2^v < 2^(t+2)
# v > (t+2)*log2(3/2) = (t+2)*0.585

# The key: v_2(m - inv) is essentially a "random" 2-adic valuation.
# P(v_2(m - inv) >= j) = 1/2^(j-1) for j >= 1 (among odd m).
# Wait, is that right? m and inv are both odd (since 3^n ≡ 1 mod 2 => inv ≡ 1 mod 2).
# m - inv is even. Let inv_low = inv mod 2^k for some k.
# Then v_2(m - inv_low) depends on m mod 2^k.

# For "random" odd m: P(v_2(m - inv) = j) for j >= 1:
# m ≡ inv mod 2^j and m ≢ inv mod 2^(j+1)
# Among odd m mod 2^(j+1): 2^j choices. inv determines one residue class mod 2^(j+1).
# P(m ≡ inv mod 2^(j+1)) = 1/2^j (among odd m mod 2^(j+1))
# So P(v_2 >= j+1) = 1/2^j, P(v_2 = j) = 1/2^(j-1) - 1/2^j = 1/2^j for j >= 1.
# E[v_2] = sum j * 1/2^j = 2. Same as geometric.

print(f"\n\n=== v_2(m - inv) distribution for random odd m ===")
for t in [1, 3, 5]:
    n = t + 2
    a = pow(3, n)
    inv = mod_inverse_2adic(a, 30)
    from collections import Counter
    dist = Counter()
    for m in range(1, 10000, 2):
        diff = abs(m - inv)
        v = v2(diff)
        dist[v] += 1
    total = sum(dist.values())
    print(f"\nt={t}, inv mod 32 = {inv % 32}:")
    for v_val in sorted(dist):
        if v_val <= 15:
            expected = total / 2**v_val
            print(f"  v_2 = {v_val:>2}: {dist[v_val]:>5} ({dist[v_val]/total*100:>6.2f}%), expected ~ {expected:.0f} ({100/2**v_val:.2f}%)")
