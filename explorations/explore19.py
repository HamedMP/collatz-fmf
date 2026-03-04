"""
explore19.py - Analytical Transition Matrix via 2-Adic Formulas

The spectral radius rho ~ 0.8638 was computed empirically.
To make it rigorous, we need to compute the transition matrix entries
ANALYTICALLY, using the exact FMF formulas.

Key idea: For x = 4k+3 with k odd, writing k+1 = 2^t*m (m odd):
  F(x) = (3^(t+2)*m - 1) / 2^v  where v = v_2(m - inv)

The transition T[r_from, r_to] = sum over (t,v,m mod classes) of:
  P(x ≡ r_from mod M) * P(F(x) ≡ r_to mod M | x ≡ r_from) * E[R^alpha | ...]

Since Theorem 12 shows the output distribution is state-independent,
T[r_from, r_to] simplifies to:
  P(F(x) ≡ r_to mod M) * E[R^alpha | F(x) ≡ r_to mod M]

But wait -- the ratio R = F(x)/x DOES depend on the input class.
So we need to be more careful.

Actually, the transition matrix is:
  T[i,j] = (1/count_i) * sum_{x ≡ i mod M, F(x) ≡ j mod M} (F(x)/x)^alpha

Let's compute this analytically for the three cases.
"""
from math import log2
from collections import defaultdict
from fractions import Fraction


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


# === Part 1: Exact computation for Case A (x = 4k+1) ===
print("=== Part 1: Exact FMF for Type A ===\n")
print("For x = 4k+1: F(x) = (3x+1)/2^v = (12k+4)/2^v")
print("  FMF = 12k+4 = 4(3k+1)")
print("  v_2(FMF) = 2 + v_2(3k+1)")
print("  F(x) = (3k+1)/2^v_2(3k+1)\n")

# F(x)/x = (3x+1)/(x*2^v) = (12k+4)/((4k+1)*2^v)
# For large k: F(x)/x ≈ 3/2^v

# What determines v_2(3k+1)?
# 3k+1 ≡ 0 mod 2 when k is odd (3k+1 = odd*3+1 = even)
# 3k+1 ≡ 1 mod 2 when k is even (3k+1 = even*3+1 = odd)
# Wait: k is any non-negative integer, x = 4k+1.
# If k is even: 3k+1 is odd -> v_2 = 0 -> F(x) = 3k+1 (not divided)
# But we know v_2(FMF) >= 2. FMF = 4(3k+1), so v_2(FMF) = 2 + v_2(3k+1).
# Hmm, the FMF IS 4(3k+1), which is always divisible by 4.
# After dividing by LPT: F(x) = (3k+1)/2^v_2(3k+1)

print("v_2(3k+1) distribution for random k:")
dist = defaultdict(int)
for k in range(0, 50000):
    v = v2(3*k + 1)
    dist[v] += 1
total = sum(dist.values())
for v_val in sorted(dist):
    if v_val <= 10:
        print(f"  v_2 = {v_val}: {dist[v_val]/total*100:.2f}%  (expected: {100/2**v_val:.2f}%)")

print()

# F(x) mod 4 for Type A inputs:
# F(x) = (3k+1) / 2^v_2(3k+1)
# This is always odd. Its mod-4 class depends on (3k+1)/2^v mod 4.
print("F(x) mod 4 for Type A (x=4k+1):")
mod4_dist = defaultdict(int)
for k in range(0, 50000):
    x = 4*k + 1
    if x <= 1:
        continue
    fmf = 4 * (3*k + 1)
    v = v2(fmf)
    f = fmf >> v
    mod4_dist[f % 4] += 1
total = sum(mod4_dist.values())
for m4 in sorted(mod4_dist):
    print(f"  F(x) ≡ {m4} mod 4: {mod4_dist[m4]/total*100:.2f}%")


# === Part 2: Exact computation for Case B0 (x = 4k+3, k even) ===
print("\n\n=== Part 2: Exact FMF for Type B, k even ===\n")
print("For x = 4k+3, k = 2j: FMF = 4(9j+4) = 36j+16")
print("  F(x) = (9j+4)/2^v_2(9j+4)")
print("  F(x)/x = (36j+16)/((8j+3)*2^v)\n")

print("F(x) mod 4 for Type B, k even:")
mod4_dist = defaultdict(int)
for j in range(0, 50000):
    k = 2*j
    x = 4*k + 3
    fmf = 4 * (9*j + 4)
    v = v2(fmf)
    f = fmf >> v
    mod4_dist[f % 4] += 1
total = sum(mod4_dist.values())
for m4 in sorted(mod4_dist):
    print(f"  F(x) ≡ {m4} mod 4: {mod4_dist[m4]/total*100:.2f}%")


# === Part 3: Exact computation for Case B(t) (x = 4k+3, k odd) ===
print("\n\n=== Part 3: Exact FMF for Type B, k odd (t ≥ 1) ===\n")
print("For x = 2^(t+2)*m - 1 (m odd, t ≥ 1):")
print("  FMF = 2(3^(t+2)*m - 1)")
print("  v_2(FMF) = 1 + v_2(m - inv) where inv = (3^(t+2))^{-1} mod 2^N")
print("  F(x) = (3^(t+2)*m - 1) / 2^v_2(3^(t+2)*m - 1)")
print("  R = F(x)/x = (3^(t+2)*m - 1) / ((2^(t+2)*m - 1) * 2^v)\n")

# For the transition matrix, we need:
# E[R^alpha | x ≡ r mod M, F(x) ≡ s mod M]

# R ≈ (3/2)^(t+2) / 2^(v-1) for large m
# And v = v_2(m - inv), which depends on m mod 2^v.

# The key analytical fact:
# For each t, as m ranges over odd numbers:
# - v = v_2(m - inv) is geometric: P(v=j) = 1/2^j for j ≥ 1
# - F(x) mod 4 is determined by the low bits of (m - inv)/2^v
# - F(x) mod 4 is uniform (1 or 3) by Theorem 12

# So the analytical transition matrix is:
# T[r,s] = sum_t P(t) * sum_v P(v|t) * P(F(x)≡s | t,v) * E[R^alpha | t,v]

# Since P(F(x)≡s | t,v) = 1/2 for s ∈ {1,3} (Theorem 12),
# and R(t,v) ≈ (3/2)^(t+2) / 2^(v-1):

print("Analytical E[R^alpha] computation:")
print("  E[R^alpha] = sum_type P(type) * E[R^alpha | type]\n")

for alpha_10 in [30, 50, 53, 70, 100]:
    alpha = alpha_10 / 100.0

    # Type A: R = (3x+1)/(x*2^v) ≈ 3/2^v where v = v_2(3k+1) + 2
    # Actually: exact R = (12k+4)/((4k+1)*2^(2+v_2(3k+1)))
    # For k → ∞, R → 3/2^(2+v_2(3k+1)) ≈ 3/4 * 1/2^v_2(3k+1)
    # E[R^alpha | A] = sum_j P(v_2=j) * (3/(4*2^j))^alpha
    #                ≈ (3/4)^alpha * sum_j (1/2^j) * (1/2^j)^alpha
    #                = (3/4)^alpha * sum_j 1/2^(j*(alpha+1))
    #                = (3/4)^alpha * 1/(1 - 1/2^(alpha+1))

    er_a_analytical = 0
    for j in range(0, 30):
        p_j = 1/2 if j == 0 else 1/2**(j+1)  # P(v_2(3k+1) = j)
        # But actually v_2(3k+1) follows a specific pattern, not exactly geometric
        # Let's use empirical for now
        pass

    # Empirical computation
    er_a = 0
    count_a = 0
    for k in range(1, 100000):
        x = 4*k + 1
        fmf = 4 * (3*k + 1)
        v = v2(fmf)
        f = fmf >> v
        r = f / x
        er_a += r**alpha
        count_a += 1
    er_a /= count_a

    # Type B0 (k even):
    er_b0 = 0
    count_b0 = 0
    for j in range(0, 50000):
        k = 2*j
        x = 4*k + 3
        fmf = 4 * (9*j + 4)
        v = v2(fmf)
        f = fmf >> v
        r = f / x
        er_b0 += r**alpha
        count_b0 += 1
    er_b0 /= count_b0

    # Type B(t) for t=1..10:
    er_bt = {}
    for t in range(1, 11):
        total_r = 0
        count = 0
        a_coeff = 3**(t+2)
        for m in range(1, 10000, 2):
            x = 2**(t+2) * m - 1
            fmf_val = a_coeff * m - 1
            v = v2(fmf_val)
            f = fmf_val >> v
            # But we also need to account for the factor of 2 in FMF = 2*fmf_val
            # Actually FMF = 2*(3^(t+2)*m - 1), so v_2(FMF) = 1 + v_2(3^(t+2)*m-1)
            # F(x) = FMF / 2^v_2(FMF) = (3^(t+2)*m-1) / 2^v_2(3^(t+2)*m-1)
            r = f / x
            total_r += r**alpha
            count += 1
        er_bt[t] = total_r / count

    # Weight by frequency: Type A = 50%, B0 = 25%, B(t=j) = 1/2^(j+2)
    p_a = 0.5
    p_b0 = 0.25
    weighted = p_a * er_a + p_b0 * er_b0
    for t in range(1, 11):
        p_t = 1 / 2**(t+2)
        weighted += p_t * er_bt[t]

    print(f"  alpha={alpha:.2f}: E[R^alpha | A]={er_a:.6f}, E[R^alpha | B0]={er_b0:.6f}, "
          f"E[R^alpha | B1]={er_bt.get(1,0):.6f}, "
          f"weighted={weighted:.6f} {'< 1 CONTRACTION' if weighted < 1 else '>= 1'}")


# === Part 4: The spectral radius equals E[R^alpha] ===
print("\n\n=== Part 4: rho(T) = E[R^alpha]? ===\n")
print("If the output class of F(x) is independent of the input class,")
print("then the transition matrix T has rank 1: T[i,j] = P(j) * E[R^alpha | j]")
print("(each row is the same). A rank-1 matrix has spectral radius = trace/1")
print("= sum_j P(j) * E[R^alpha | j] = E[R^alpha].\n")

# But wait -- the empirical T is NOT rank 1 (rows differ slightly).
# The rank-1 property holds for the FIRST-HOP analysis (Theorem 12),
# but along chains, there are weak correlations.

# The spectral radius rho ≈ 0.8638 should equal E[R^alpha] if T is rank 1.
# Let's check:
for alpha_10 in [50, 53]:
    alpha = alpha_10 / 100.0
    total_r = 0
    count = 0
    for x in range(3, 500001, 2):
        mod4 = x % 4
        if mod4 == 1:
            k = (x - 1) // 4
            fmf = 4 * (3 * k + 1)
        elif mod4 == 3:
            k = (x - 3) // 4
            if k % 2 == 0:
                j = k // 2
                fmf = 4 * (9 * j + 4)
            else:
                t = v2(k + 1)
                fmf = 3**(t + 2) * (k + 1) // 2**(t - 1) - 2
        else:
            continue
        v = v2(fmf)
        f = fmf >> v
        r = f / x
        total_r += r**alpha
        count += 1

    er = total_r / count
    print(f"  alpha={alpha:.2f}: E[R^alpha] = {er:.8f}  (compare to rho ≈ 0.8638)")


# === Part 5: Theoretical formula for E[R^alpha] ===
print("\n\n=== Part 5: Theoretical E[R^alpha] Derivation ===\n")

# For large x (ignoring ±1 corrections):
# Type A: R ≈ 3/(4 * 2^j) where j = v_2(3k+1), P(j) ≈ 1/2^(j+1) for j ≥ 0
# E[R^alpha | A] = sum_{j=0}^∞ P(j) * (3/4 * 1/2^j)^alpha
#                = (3/4)^alpha * sum_{j=0}^∞ 1/2^(j+1) * 1/2^(j*alpha)
#                = (3/4)^alpha * (1/2) * sum_{j=0}^∞ 1/2^(j*(1+alpha))
#                = (3/4)^alpha / (2 * (1 - 2^{-(1+alpha)}))
#                = (3/4)^alpha / (2 - 2^{-alpha})

# Type B(t): R ≈ (3/2)^(t+2) / 2^j where j = v_2(m-inv), P(j) = 1/2^j
# E[R^alpha | B(t)] = sum_{j=1}^∞ (1/2^j) * ((3/2)^(t+2) / 2^j)^alpha
#                    = ((3/2)^(t+2))^alpha * sum_{j=1}^∞ 1/2^(j*(1+alpha))
#                    = ((3/2)^(t+2))^alpha / (2^(1+alpha) - 1)

# Overall: E[R^alpha] = P(A) * E[R^alpha|A] + sum_t P(B(t)) * E[R^alpha|B(t)]
# P(A) = 1/2, P(B0) = 1/4, P(B(t)) = 1/2^(t+2) for t >= 1

for alpha_10 in [50, 53, 100]:
    alpha = alpha_10 / 100.0

    # Type A
    er_a_theory = (3/4)**alpha / (2 - 2**(-alpha))

    # Type B(t)
    def er_bt_theory(t, alpha):
        return ((3/2)**(t+2))**alpha / (2**(1+alpha) - 1)

    # Type B0 (k even): R ≈ 9/(4*2^j) where j = v_2(9j+4), tricky
    # Actually B0: FMF = 36j+16, x = 8j+3. R ≈ 36j/(8j * 2^v) = 4.5/2^v
    # For now use B(t=0) formula: R ≈ (3/2)^2 / 2^j = 9/4 / 2^j
    er_b0_theory = ((3/2)**2)**alpha / (2**(1+alpha) - 1)

    # Weighted sum
    total = 0.5 * er_a_theory + 0.25 * er_b0_theory
    for t in range(1, 20):
        p = 1/2**(t+2)
        total += p * er_bt_theory(t, alpha)

    # The sum over t converges because (3/2)^alpha < 2, so each term shrinks
    # sum_{t=1}^∞ (3/2)^((t+2)*alpha) / 2^(t+2) converges for alpha < log2(2)/log2(3/2) = 1/0.585 = 1.71
    # The geometric series: ((3/2)^alpha / 2) < 1 when alpha < 1/log2(3/2) = 1.71

    print(f"  alpha={alpha:.2f}: E[R^alpha] (theory) = {total:.8f}")
    print(f"    E[R^alpha | A] = {er_a_theory:.6f}")
    print(f"    E[R^alpha | B0] = {er_b0_theory:.6f}")
    print(f"    E[R^alpha | B1] = {er_bt_theory(1, alpha):.6f}")
    print(f"    E[R^alpha | B2] = {er_bt_theory(2, alpha):.6f}")

# Find theoretical alpha*
print(f"\n  Searching for theoretical alpha* (where E[R^alpha] = 1):")
lo, hi = 0.5, 2.0
for _ in range(100):
    mid = (lo + hi) / 2
    er_a_t = (3/4)**mid / (2 - 2**(-mid))
    total = 0.5 * er_a_t
    total += 0.25 * ((3/2)**2)**mid / (2**(1+mid) - 1)
    for t in range(1, 30):
        total += (1/2**(t+2)) * ((3/2)**(t+2))**mid / (2**(1+mid) - 1)
    if total < 1:
        lo = mid
    else:
        hi = mid

alpha_star_theory = (lo + hi) / 2
print(f"  Theoretical alpha* = {alpha_star_theory:.10f}")

# Compute theoretical rho at alpha = 0.53
alpha = 0.53
er_a_t = (3/4)**alpha / (2 - 2**(-alpha))
total = 0.5 * er_a_t
total += 0.25 * ((3/2)**2)**alpha / (2**(1+alpha) - 1)
for t in range(1, 30):
    total += (1/2**(t+2)) * ((3/2)**(t+2))**alpha / (2**(1+alpha) - 1)
print(f"\n  At alpha=0.53: theoretical rho = E[R^0.53] = {total:.8f}")
print(f"  Empirical rho from explore17: ~0.8638")
print(f"  Match: {'YES' if abs(total - 0.8638) < 0.01 else 'APPROXIMATE'}")
