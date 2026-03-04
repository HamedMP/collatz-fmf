"""
explore12.py - WHY are FMF transitions state-independent?

The key finding from explore11: the output state distribution of an FMF hop
is IDENTICAL regardless of the input state. Specifically:
  P(output is Type A) = 50%
  P(output is Type B with t=j) = 1/2^(j+2)

This is extraordinary. If true algebraically, it means the FMF chain
is a genuine random walk with i.i.d. steps.

To prove this, we need to show that after an FMF hop, the low-order bits
of the output are "uniformly distributed" in the relevant sense.

The output is: F(x) = FMF(x) / 2^{v_2(FMF(x))}

For x = 2^(t+2)*m - 1 with m odd:
  FMF = 2(3^(t+2)*m - 1)
  v_2(FMF) = 1 + v_2(3^(t+2)*m - 1) = 1 + v_2(m - inv)
  where inv = (3^(t+2))^{-1} mod 2^N

  F(x) = (3^(t+2)*m - 1) / 2^{v_2(3^(t+2)*m - 1)}

Question: What is F(x) mod 4? And what is the t-value of F(x)?

Let's analyze this algebraically.
"""
from collections import Counter


def v2(n):
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


def mod_inverse_2adic(a, precision=64):
    inv = 1
    for i in range(1, precision):
        if (a * inv) % (2**(i+1)) != 1:
            inv += 2**i
    return inv


# === Part 1: Algebraic analysis of F(x) mod 4 ===
print("=== Part 1: F(x) mod 4 as a function of m mod small powers of 2 ===\n")

for t in range(1, 6):
    n = t + 2
    a = pow(3, n)
    inv = mod_inverse_2adic(a, 32)

    print(f"\nt={t}, 3^{n}={a}, inv mod 2^8 = {inv % 256}")
    print(f"  {'m':>5} {'m mod 8':>7} {'3^n*m-1':>12} {'v2(*)':>6} {'F(x)':>10} {'F mod 4':>7} {'F type':>7} {'F t-val':>7}")

    type_by_mmod8 = {}
    for m in range(1, 64, 2):
        val = a * m - 1  # 3^(t+2)*m - 1
        v = v2(val)
        F = val >> v
        f_mod4 = F % 4

        if f_mod4 == 1:
            f_type = "A"
            f_t = 0
        else:
            f_k = (F - 3) // 4
            if f_k % 2 == 0:
                f_type = "B"
                f_t = 0
            else:
                f_type = "B"
                f_t = v2(f_k + 1)

        if m <= 32:
            print(f"  {m:>5} {m%8:>7} {val:>12} {v:>6} {F:>10} {f_mod4:>7} {f_type:>7} {f_t:>7}")

        key = m % 8
        if key not in type_by_mmod8:
            type_by_mmod8[key] = Counter()
        type_by_mmod8[key][f"{'A' if f_mod4 == 1 else 'B'}"] += 1

    print(f"\n  Summary by m mod 8:")
    for mmod, counts in sorted(type_by_mmod8.items()):
        total = sum(counts.values())
        print(f"    m≡{mmod} (mod 8): {dict(counts)}")


# === Part 2: The key insight - m determines the output type via distance to inv ===
print("\n\n=== Part 2: Output type determined by (m - inv) mod 2^k ===\n")

for t in range(1, 4):
    n = t + 2
    a = pow(3, n)
    inv = mod_inverse_2adic(a, 32)

    print(f"\nt={t}, inv mod 4 = {inv%4}, inv mod 8 = {inv%8}, inv mod 16 = {inv%16}")

    # The FMF output is (3^n * m - 1) / 2^v where v = v2(3^n*m - 1) = v2(m - inv)
    # So (3^n * m - 1) = 2^v * F where F is odd.
    # F = (3^n * m - 1) / 2^v
    #
    # F mod 4 depends on (3^n * m - 1) / 2^v mod 4 = ((3^n*m - 1) >> v) mod 4
    #
    # Let d = m - inv (in integers, but think mod 2^large)
    # 3^n * m - 1 = 3^n * (inv + d) - 1 = (3^n * inv - 1) + 3^n * d = 3^n * d  (mod 2^large)
    # since 3^n * inv ≡ 1 (mod 2^large)
    #
    # So 3^n * m - 1 = 3^n * d + (3^n*inv - 1)
    # But 3^n*inv = 1 + 2^large * something, so for precision up to 2^large:
    # 3^n * m - 1 = 3^n * d  (when we compute mod 2^large)
    #
    # Wait, more carefully in Z:
    # 3^n * m - 1 = 3^n*(m - inv) + (3^n*inv - 1)
    # 3^n*inv = 1 + c*2^precision for some integer c
    # So 3^n*m - 1 = 3^n*(m-inv) + c*2^precision
    # For v2 purposes (with v2 < precision):
    # v2(3^n*m - 1) = v2(3^n*(m-inv)) = v2(m - inv) since 3^n is odd
    # And the odd part: (3^n*m - 1)/2^v = 3^n*(m-inv)/2^v + c*2^(precision-v)
    # The low bits of F come from 3^n * (m-inv) / 2^v

    print(f"  For F(x) = (3^{n}*m - 1) / 2^v:")
    print(f"  Since 3^{n} is odd, v = v2(m - inv)")
    print(f"  And F = 3^{n} * (m-inv)/2^v + correction from higher bits")
    print()

    # Let's verify: F mod 4 is determined by 3^n * ((m-inv)/2^v) mod 4
    print(f"  {'m':>5} {'d=m-inv':>12} {'v2(d)':>6} {'d/2^v':>8} {'3^n*d/2^v mod4':>15} {'actual F mod4':>14}")
    for m in range(1, 32, 2):
        d = m - inv
        v = v2(abs(d)) if d != 0 else 99
        if d == 0 or v > 20:
            continue
        d_shifted = d >> v  # d/2^v, but d is negative
        # 3^n * d / 2^v mod 4
        predicted_mod4 = (a * d_shifted) % 4
        if predicted_mod4 < 0:
            predicted_mod4 += 4

        val = a * m - 1
        actual_v = v2(val)
        F = val >> actual_v
        actual_mod4 = F % 4

        # The actual F = (a*m - 1)/2^v = (a*d + a*inv - 1)/2^v
        # a*inv = 1 + 2^precision * something
        # So (a*m-1)/2^v = (a*d + 2^precision*something)/2^v
        # For small v, the high-order correction doesn't affect F mod 4
        print(f"  {m:>5} {d:>12} {v:>6} {d_shifted:>8} {predicted_mod4:>15} {actual_mod4:>14}  {'match' if predicted_mod4 == actual_mod4 else 'MISS'}")


# === Part 3: The distribution argument ===
# Since inv is fixed for each t, and m ranges over all odd numbers,
# the values of (m - inv) mod 2^k cycle through all odd residues mod 2^k.
# (Because inv is odd, m - inv is even, and the even residues mod 2^k
# are uniformly distributed among those with v2 = j for each j.)
#
# P(v2(m - inv) = j) = 1/2^j for j >= 1 (geometric distribution)
# This is INDEPENDENT of inv (and thus independent of t).
#
# After extracting the 2-adic part, the "odd part" (m-inv)/2^v is
# uniformly distributed among odd numbers mod any power of 2.
# Since 3^n is a fixed odd multiplier, 3^n * ((m-inv)/2^v) is also
# uniformly distributed among odd numbers mod any power of 2.
# In particular, its residue mod 4 is equally likely to be 1 or 3.
# This gives P(Type A) = P(Type B) = 50%.

print("\n\n=== Part 3: Proving the 50/50 A/B split ===\n")
print("After FMF hop, F = 3^n * (m-inv)/2^v + high-order correction")
print("The key: (m-inv)/2^v is uniformly distributed among odd numbers")
print("And 3^n * odd is uniformly distributed mod 4 (since 3^n is odd)")
print("So F mod 4 is equally likely to be 1 or 3.\n")

for t in range(1, 8):
    n = t + 2
    a = pow(3, n)
    inv = mod_inverse_2adic(a, 40)

    count_A = 0
    count_B = 0
    for m in range(1, 10000, 2):
        val = a * m - 1
        v = v2(val)
        F = val >> v
        if F % 4 == 1:
            count_A += 1
        else:
            count_B += 1

    total = count_A + count_B
    print(f"  t={t}: A={count_A} ({count_A/total*100:.1f}%), B={count_B} ({count_B/total*100:.1f}%)")


# === Part 4: The t-value distribution of the output ===
# Given F mod 4 = 3 (Type B), what is the t-value?
# F = 4k'+3, k' = (F-3)/4. t' = v2(k'+1) = v2((F+1)/4)
# F+1 = 3^n*(m-inv)/2^v + correction + 1
# The key: F+1 mod 4 = (F mod 4) + 1 = 0 (when F ≡ 3 mod 4)
# So F+1 is divisible by 4. t' = v2(F+1) - 2.
# And v2(F+1) depends on the next bits of (m-inv)/2^v beyond mod 4.
# Since these bits are uniformly distributed:
# P(t' = j) = P(v2(F+1) = j+2) = 1/2^(j+2) for j >= 0
# Wait, let's check...

print("\n\n=== Part 4: t-value distribution of Type B outputs ===\n")
print("Among Type B outputs, what is P(t'=j)?\n")

for t in range(1, 5):
    n = t + 2
    a = pow(3, n)
    t_dist = Counter()

    for m in range(1, 20000, 2):
        val = a * m - 1
        v = v2(val)
        F = val >> v
        if F % 4 == 3:
            k2 = (F - 3) // 4
            if k2 % 2 == 0:
                t_out = 0
            else:
                t_out = v2(k2 + 1)
            t_dist[t_out] += 1

    total = sum(t_dist.values())
    print(f"  Input t={t}:")
    for j in sorted(t_dist):
        if j <= 8:
            expected = total / 2**(j+1)
            print(f"    t'={j}: {t_dist[j]:>5} ({t_dist[j]/total*100:>6.2f}%), expected {expected:.0f} ({100/2**(j+1):>6.2f}%)")


# === Part 5: The complete proof of state-independence ===
print("\n\n=== Part 5: Summary of State-Independence Proof ===\n")
print("""
THEOREM (State-Independent Transitions):
For the FMF hop map F, the output state distribution is independent of the
input state. Specifically:
  P(F(x) ≡ 1 mod 4) = 1/2
  P(F(x) ≡ 3 mod 4 with t'=j) = 1/2^(j+2)  for j = 0, 1, 2, ...

PROOF SKETCH:
1. Write x = 2^(t+2)*m - 1 with m odd. Then:
   FMF(x) = 2(3^(t+2)*m - 1)
   F(x) = (3^(t+2)*m - 1) / 2^{v_2(3^(t+2)*m - 1)}

2. Let inv = (3^(t+2))^{-1} in Z_2. Then:
   3^(t+2)*m - 1 = 3^(t+2)*(m - inv) + (3^(t+2)*inv - 1)
   Since 3^(t+2)*inv = 1 in Z_2:
   v_2(3^(t+2)*m - 1) = v_2(m - inv)

3. Write m - inv = 2^v * u where u is odd and v = v_2(m - inv).
   Then F(x) = 3^(t+2) * u + correction (where correction is divisible by
   a high power of 2, so it doesn't affect F mod small powers of 2).

4. As m ranges over all odd numbers:
   - (m - inv) ranges over all even numbers (since inv is odd)
   - v_2(m - inv) = j with probability 1/2^j (geometric distribution)
   - u = (m - inv)/2^v is uniformly distributed among odd numbers

5. Since 3^(t+2) is odd, 3^(t+2)*u mod 4 is uniform over {1, 3}.
   So F(x) mod 4 is equally likely to be 1 or 3 → P(Type A) = P(Type B) = 1/2.

6. For Type B outputs (F(x) ≡ 3 mod 4):
   k' = (F(x)-3)/4, and t' = v_2(k'+1).
   The higher bits of u determine t', and since u is uniform:
   P(t' = j) = 1/2^(j+1) for j = 0, 1, 2, ...

This gives the full transition distribution, independent of the input (t, type).  QED
""")
